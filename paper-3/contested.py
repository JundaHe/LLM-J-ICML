"""
contested — PROTOCOL_CALIBRATION.md G3: which items will people disagree on? Per test item, predictors (one number each):
  conf       judge confidence = 1 − entropy(judge's own distribution)/log K   (sign-flipped so that larger ⇒ more predicted disagreement: we use entropy)
  map_disp   variance of the panel-map distribution at the judge score s (large when θ sits between cut-points)   — the hypothesis
  loc_only   |s − scale midpoint| negated (a trivial 'extreme scores are consensual' baseline)
Targets on the test items from the held-out ratings: dispersion = variance of the ratings; contested = range ≥ 2 (ordinal K ≥ 4) / both extreme classes present (K = 3).
Metrics: Spearman(predictor, dispersion) and AUROC(predictor, contested); item-cluster bootstrap. Judge = Q0 (v1); map fitted on calibration groups (30 %) as in judge_map.py.
Usage: python contested.py --panel dices [--splits 3 --B 500]
"""
import os, sys, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, HERE); sys.path.insert(0, P2)
import pools, data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--splits", type=int, default=3); ap.add_argument("--B", type=int, default=500); ap.add_argument("--tag", default=""); args = ap.parse_args()
P = pools.LOADERS[args.panel](); K = P["K"]; LV = np.arange(K, dtype=float); R = P["ratings"]; N = len(P["items"]); PAN2 = data_panels.load(P["panel"]); G = np.asarray(PAN2.get("groups", PAN2["item_ids"]))
F = np.load(f"{P2}/features/{P['panel']}/{PAN2['model'].split('/')[-1]}.npz", allow_pickle=True); Q = F["Q0"].astype(float); s = Q @ LV
OUT = f"{HERE}/results/contested/{args.panel}{args.tag}"; os.makedirs(OUT, exist_ok=True)
def op_probs(sv, par):
    a, b = par[0], par[1]; cuts = np.concatenate([[par[2]], par[2] + np.cumsum(np.log1p(np.exp(par[3:])))]); theta = a + b * sv
    cdf = norm.cdf(cuts[None, :] - theta[:, None]); cdf = np.concatenate([np.zeros((len(sv), 1)), cdf, np.ones((len(sv), 1))], 1); return np.clip(np.diff(cdf, axis=1), 1e-9, 1)
def fit_map(sv, y):
    def nll(par): return -np.log(op_probs(sv, par)[np.arange(len(y)), y]).sum() + 0.01 * (par[1] ** 2 + (par[3:] ** 2).sum())
    return minimize(nll, np.concatenate([[0.0, 1.0, -0.5 * (K - 2) - 0.5], np.zeros(K - 2)]), method="L-BFGS-B").x
def auroc(score, pos):
    pos = np.asarray(pos, bool); sp, sn = score[pos], score[~pos]
    if len(sp) == 0 or len(sn) == 0: return np.nan
    return float(np.mean([(x > sn).mean() + 0.5 * (x == sn).mean() for x in sp]))
def ci(v): v = [x for x in v if x == x]; return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if v else [np.nan, np.nan]
rows = []
for isplit in range(args.splits):
    ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]; g_ca = set(ug[: int(.3 * len(ug))])
    ca = np.array([i for i in range(N) if G[i] in g_ca]); te = np.array([i for i in range(N) if G[i] not in g_ca])
    Rca = R[R.item.isin(set(ca))]; Rte = R[R.item.isin(set(te))]; par = fit_map(s[Rca.item.to_numpy()], Rca.y.to_numpy()); Pm = op_probs(s, par)
    g = Rte.groupby("item").y; disp = g.var(ddof=0); rng_ = g.max() - g.min(); cnt = g.size(); items = disp.index.to_numpy(); items = items[cnt.loc[items].to_numpy() >= 3]
    y_disp = disp.loc[items].to_numpy(); contested = rng_.loc[items].to_numpy() >= 2
    topq = y_disp >= np.quantile(y_disp, 0.75)                         # Amendment: 'most contested quartile' indicator — defined on every panel, incl. dense ones where range ≥ 2 is ~always true
    pred = {"entropy": -(Q[items] * np.log(Q[items] + 1e-12)).sum(1), "map_disp": (Pm[items] * (LV[None, :] - (Pm[items] @ LV)[:, None]) ** 2).sum(1), "loc_mid": -np.abs(s[items] - (K - 1) / 2)}
    ask_f = f"{HERE}/results/ask/{args.panel}.npz"
    if os.path.exists(ask_f): pred["ask_llm"] = np.load(ask_f, allow_pickle=True)["disagree"][items]      # G3 predictor (iii): the LLM asked directly how much annotators will disagree
    def stats(idx):
        out = {}
        for k, v in pred.items(): out[f"spearman_{k}"] = float(spearmanr(v[idx], y_disp[idx]).correlation); out[f"auroc_{k}"] = auroc(v[idx], contested[idx]); out[f"auroc_topq_{k}"] = auroc(v[idx], topq[idx])
        return out
    full = stats(np.arange(len(items))); brng = np.random.RandomState(100 + isplit); bs = {k: [] for k in full}; grp_items = G[items]; ug2 = np.unique(grp_items)
    for b in range(args.B):
        draw = brng.choice(ug2, len(ug2), replace=True); idx = np.concatenate([np.where(grp_items == gg)[0] for gg in draw])
        for k, v in stats(idx).items(): bs[k].append(v)
    row = dict(isplit=isplit, n_items=int(len(items)), contested_rate=float(contested.mean()), **full, **{f"{k}_ci95": ci(v) for k, v in bs.items()}); rows.append(row)
    print(f"split {isplit}: n={len(items)} contested {contested.mean():.2f} | spearman entropy {full['spearman_entropy']:+.3f}  map_disp {full['spearman_map_disp']:+.3f}  loc_mid {full['spearman_loc_mid']:+.3f} | AUROC entropy {full['auroc_entropy']:.3f}  map_disp {full['auroc_map_disp']:.3f}  loc_mid {full['auroc_loc_mid']:.3f}", flush=True)
df = pd.DataFrame(rows); df.to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
summ = {k: float(df[k].mean()) for k in df.columns if k.startswith(("spearman_", "auroc_")) and not k.endswith("_ci95")}
json.dump(dict(panel=args.panel, splits=args.splits, mean=summ, rows=rows), open(f"{OUT}/summary.json", "w"), indent=1, default=float); print(args.panel, json.dumps(summ))
