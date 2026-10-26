"""
judge_map — PROTOCOL_CALIBRATION.md G2: turn a black-box judge's score into a target panel's rating distribution with a panel map (ordered probit on the judge score),
versus the judge's own distribution, temperature scaling and a Dirichlet/climatology mixture, all fitted on calibration items and evaluated against HELD-OUT RATERS on test items.
Judges available without GPU: (a) Q0 — the frozen base model's zero-shot score distribution (paper-2 features/<panel>/*.npz); (b) --scores <csv> with columns item_id,score (e.g. paper-1 judge outputs);
(c) paper-2 LoRA judges via --lora <dir with P_test.npy/items_test.csv> (test items only; calibration from P_calib.npy).
Evaluation: for persistent-rater panels, leave-one-rater-out — the map is fitted on the other raters' calibration ratings and scored on the held-out rater's test ratings, averaged over raters (CSJE-style);
for position panels, ratings of the test items are the targets. Metric: RPS. Item-cluster bootstrap for intervals.
Usage: python judge_map.py --panel dices [--judge q0|scores|lora] [--scores file.csv] [--lora dir] [--splits 3] [--B 500]
"""
import os, sys, json, argparse, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, HERE); sys.path.insert(0, P2)
import pools, data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--judge", default="q0"); ap.add_argument("--scores", default=None); ap.add_argument("--lora", default=None)
ap.add_argument("--splits", type=int, default=3); ap.add_argument("--B", type=int, default=500); ap.add_argument("--n_cal_list", default="20,50,all"); ap.add_argument("--tag", default=""); args = ap.parse_args()
P = pools.LOADERS[args.panel](); K = P["K"]; LV = np.arange(K, dtype=float); R = P["ratings"]; N = len(P["items"]); PAN2 = data_panels.load(P["panel"]); G = np.asarray(PAN2.get("groups", PAN2["item_ids"]))
OUT = f"{HERE}/results/judge_map/{args.panel}__{args.judge}{args.tag}"; os.makedirs(OUT, exist_ok=True)
# ---- judge score s and (optionally) its own distribution Q
if args.judge == "q0":
    F = np.load(f"{P2}/features/{P['panel']}/{PAN2['model'].split('/')[-1]}.npz", allow_pickle=True); Q = F["Q0"].astype(float); s = Q @ LV
elif args.judge == "scores":
    sc = pd.read_csv(args.scores); m = dict(zip(sc.item_id.astype(str), sc.score.astype(float))); s = np.array([m.get(str(i), np.nan) for i in P["items"]]); Q = None
elif args.judge == "lora":
    # paper-2 LoRA judge: P_calib / P_test for the cell's own calibration and test items (other items get NaN and are excluded); its own distribution is Q
    s = np.full(N, np.nan); Q = np.full((N, K), np.nan)
    for part in ("calib", "test"):
        Pm = np.load(f"{args.lora}/P_{part}.npy"); rows_ = pd.read_csv(f"{args.lora}/items_{part}.csv")["row"].to_numpy(); Q[rows_] = Pm; s[rows_] = Pm @ LV
    LORA_META = json.load(open(f"{args.lora}/meta.json")); LORA_CALIB_ROWS = set(pd.read_csv(f"{args.lora}/items_calib.csv")["row"].to_numpy().tolist())
else: raise SystemExit("unknown judge")
ok = ~np.isnan(s)
def rps_rows(Pm_rows, y): cdf = np.cumsum(Pm_rows, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def op_probs(sv, par):
    a, b = par[0], par[1]; cuts = np.concatenate([[par[2]], par[2] + np.cumsum(np.log1p(np.exp(par[3:])))]); theta = a + b * sv
    cdf = norm.cdf(cuts[None, :] - theta[:, None]); cdf = np.concatenate([np.zeros((len(sv), 1)), cdf, np.ones((len(sv), 1))], 1); return np.clip(np.diff(cdf, axis=1), 1e-9, 1)
def fit_map(sv, y, prior=None, lam=0.0):
    def nll(par): return -np.log(op_probs(sv, par)[np.arange(len(y)), y]).sum() + (lam * ((par - prior) ** 2).sum() if prior is not None else 0.01 * (par[1] ** 2 + (par[3:] ** 2).sum()))
    p0 = prior if prior is not None else np.concatenate([[0.0, 1.0, -0.5 * (K - 2) - 0.5], np.zeros(K - 2)]); return minimize(nll, p0, method="L-BFGS-B").x
def temp_apply(Qm, T, lam, clim): q = np.exp(np.log(np.clip(Qm, 1e-9, 1)) / T); q /= q.sum(1, keepdims=True); return (1 - lam) * q + lam * clim
def fit_temp(Qm_rows, y, clim, with_mix=True):
    best = None
    for T in (0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0):
        for lam in ((0.0, 0.1, 0.2, 0.3, 0.5, 0.7) if with_mix else (0.0,)):
            nll = -np.log(temp_apply(Qm_rows, T, lam, clim)[np.arange(len(y)), y]).sum()
            if best is None or nll < best[0]: best = (nll, T, lam)
    return best[1], best[2]
NCAL = [x for x in args.n_cal_list.split(",")]
persistent = P["raters"].persistent.astype(bool); pers_ids = set(P["raters"].index[persistent])

def evaluate(isplit):
    if args.judge == "lora":   # the LoRA cell fixes calibration/test items; the evaluator rater (excluded from training) is the natural held-out target, but all raters' test ratings are scored as in the other judges
        ca = np.array([i for i in range(N) if i in LORA_CALIB_ROWS]); te = np.array([i for i in range(N) if ok[i] and i not in LORA_CALIB_ROWS])
    else:
        ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]; g_ca = set(ug[: int(.3 * len(ug))])    # 30 % calibration groups, 70 % test (no training here)
        ca = np.array([i for i in range(N) if G[i] in g_ca and ok[i]]); te = np.array([i for i in range(N) if G[i] not in g_ca and ok[i]])
    Rca = R[R.item.isin(set(ca))]; Rte = R[R.item.isin(set(te))]; clim = np.bincount(Rca.y.to_numpy(), minlength=K) / len(Rca)
    rows = []
    def add(name, Pm_full, extra=None):
        # score against every test rating (position panels) or leave-one-rater-out (handled by the caller passing the right fit); here: all test ratings
        r = rps_rows(Pm_full[Rte.item.to_numpy()], Rte.y.to_numpy()).mean(); d = dict(isplit=isplit, arm=name, rps=float(r), n_test_ratings=int(len(Rte))); d.update(extra or {}); rows.append(d)
    if Q is not None: add("judge-own", Q)
    for n in NCAL:
        sub = Rca if n == "all" else Rca.sample(n=min(int(n), len(Rca)), random_state=1000 + isplit)
        par = fit_map(s[sub.item.to_numpy()], sub.y.to_numpy()); add(f"map({n})", op_probs(s, par), {"n_cal": int(len(sub))})
        if Q is not None:
            T, lam = fit_temp(Q[sub.item.to_numpy()], sub.y.to_numpy(), clim, with_mix=False); add(f"temp({n})", temp_apply(Q, T, lam, clim), {"n_cal": int(len(sub)), "T": T})
            T, lam = fit_temp(Q[sub.item.to_numpy()], sub.y.to_numpy(), clim, with_mix=True); add(f"temp+mix({n})", temp_apply(Q, T, lam, clim), {"n_cal": int(len(sub)), "T": T, "lam": lam})
    # leave-one-rater-out panel map for persistent raters: map fitted on the OTHER raters' calibration ratings, scored on the held-out rater's test ratings; plus per-rater offset from the rater's own calibration ratings
    if len(pers_ids) >= 3:
        loo_map, loo_rater, loo_own = [], [], []
        for rid in sorted(pers_ids):
            te_r = Rte[Rte.rater == rid]; ca_r = Rca[Rca.rater == rid]; ca_o = Rca[Rca.rater != rid]
            if len(te_r) < 5 or len(ca_o) < 20: continue
            par = fit_map(s[ca_o.item.to_numpy()], ca_o.y.to_numpy()); loo_map.append(rps_rows(op_probs(s, par)[te_r.item.to_numpy()], te_r.y.to_numpy()).mean())
            if len(ca_r) >= 5:
                def nll_a(a_): p_ = par.copy(); p_[0] = a_[0]; return -np.log(op_probs(s[ca_r.item.to_numpy()], p_)[np.arange(len(ca_r)), ca_r.y.to_numpy()]).sum() + 0.5 * (a_[0] - par[0]) ** 2
                pr = par.copy(); pr[0] = minimize(nll_a, np.array([par[0]]), method="L-BFGS-B").x[0]; loo_rater.append(rps_rows(op_probs(s, pr)[te_r.item.to_numpy()], te_r.y.to_numpy()).mean())
            if Q is not None: loo_own.append(rps_rows(Q[te_r.item.to_numpy()], te_r.y.to_numpy()).mean())
        if loo_map: rows.append(dict(isplit=isplit, arm="map(all)-LOO-rater", rps=float(np.mean(loo_map)), n_raters=len(loo_map)))
        if loo_rater: rows.append(dict(isplit=isplit, arm="map+rater-offset-LOO", rps=float(np.mean(loo_rater)), n_raters=len(loo_rater)))
        if loo_own: rows.append(dict(isplit=isplit, arm="judge-own-LOO-rater", rps=float(np.mean(loo_own)), n_raters=len(loo_own)))
    return rows

t0 = time.time(); rows = []
for isplit in range(args.splits): rows += evaluate(isplit)
df = pd.DataFrame(rows); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
g = df.groupby("arm")["rps"].agg(["mean", "sem", "count"]).sort_values("mean").round(5)
txt = f"# judge_map — {args.panel} / judge={args.judge}: {N} items, K={K}, {R.rater.nunique()} raters ({len(pers_ids)} persistent); {args.splits} calibration/test splits\n\n```\n{g.to_string()}\n```\n"
open(f"{OUT}/summary.md", "w").write(txt); print(txt, f"[{time.time()-t0:.0f}s]")
