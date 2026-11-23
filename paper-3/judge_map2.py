"""
judge_map2 — PROTOCOL_CALIBRATION.md G2 with Amendment 3: turn a black-box judge's score into a target panel's rating distribution with a panel map (ordered probit on the
judge score), against generic calibrators fitted on the same n calibration ratings: climatology (judge ignored), the rounded score as a point mass, point mass + climatology
mixture, histogram binning on the rounded score, binning on equal-count bins of the raw score (continuous scores), and — for judges with a distribution of their own —
temperature scaling with and without the mixture. Leave-one-rater-out arms on persistent-rater panels (map, map + per-rater offset, binning).
Judges: q0 (frozen base model's zero-shot distribution, paper-2 features), lora (paper-2 LoRA judge cell, one fixed split), frontier (paper-1 frontier judge outputs, read in
place from --p1; integer 1–5 on Crupi, mean of six runs on Scalabrino).
Intervals: bootstrap over item groups, one draw of group multiplicities per replicate applied to every split's test items; statistic = mean over splits of the weighted mean
RPS (difference). The fitted calibrators are held fixed, so the intervals cover test-item sampling only.
Usage: python judge_map2.py --panel crupi_ca --judge frontier --model openai_gpt-5_5 [--splits 20] [--B 1000]
"""
import os, sys, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, HERE); sys.path.insert(0, P2)
import pools, data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--judge", default="q0"); ap.add_argument("--model", default=None); ap.add_argument("--lora", default=None)
ap.add_argument("--p1", default="/scratch/jundahe/ICSE2027-LLM-Judge/paper-1/replication_package"); ap.add_argument("--splits", type=int, default=20); ap.add_argument("--B", type=int, default=1000)
ap.add_argument("--n_cal_list", default="20,50,all"); ap.add_argument("--tag", default=""); args = ap.parse_args()
P = pools.LOADERS[args.panel](); K = P["K"]; LV = np.arange(K, dtype=float); R = P["ratings"]; N = len(P["items"]); PAN2 = data_panels.load(P["panel"])
_, GI = np.unique(np.asarray(PAN2.get("groups", PAN2["item_ids"])), return_inverse=True); NG = int(GI.max() + 1)
name = args.judge if args.judge != "frontier" else args.model; OUT = f"{HERE}/results/judge_map2/{args.panel}__{name}{args.tag}"; os.makedirs(OUT, exist_ok=True)
# ---- judge score s on the 0..K-1 scale and (optionally) its own distribution Q
Q = None; LORA_CALIB_ROWS = None
if args.judge == "q0":
    F = np.load(f"{P2}/features/{P['panel']}/{PAN2['model'].split('/')[-1]}.npz", allow_pickle=True); Q = F["Q0"].astype(float); s = Q @ LV
elif args.judge == "lora":
    s = np.full(N, np.nan); Q = np.full((N, K), np.nan)
    for part in ("calib", "test"):
        Pm = np.load(f"{args.lora}/P_{part}.npy"); rows_ = pd.read_csv(f"{args.lora}/items_{part}.csv")["row"].to_numpy(); Q[rows_] = Pm; s[rows_] = Pm @ LV
    LORA_CALIB_ROWS = set(pd.read_csv(f"{args.lora}/items_calib.csv")["row"].to_numpy().tolist()); args.splits = 1
elif args.judge == "frontier":
    if args.panel.startswith("crupi_"):
        crit = {"crupi_ca": "CA", "crupi_conc": "Conciseness", "crupi_flu": "Fluency"}[args.panel]; m = {}; hum = {}
        for L in ("Java", "Python"):
            d = pd.read_json(f"{args.p1}/task1_code_summarization/judge_scores_frontier/{args.model}/{L}/scores.jsonl", lines=True)
            for t, g, v, h in zip(d.target_id, d.generated_by, d[f"{crit}_llm"], d[[f"{crit}_{i}" for i in (1, 2, 3)]].to_numpy()): m[f"{L}_{t}_{g}"] = float(v); hum[f"{L}_{t}_{g}"] = tuple(int(x) - 1 for x in h)
        H2 = PAN2["H"]; assert all(hum[str(it)] == tuple(H2[i]) for i, it in enumerate(P["items"]) if str(it) in hum), "human ratings in the judge file differ from the panel"
    elif args.panel == "scalabrino":
        d = pd.read_json(f"{args.p1}/task3_code_readability/judge_scores_frontier/{args.model}/scores.jsonl", lines=True); m = {str(k): float(v) for k, v in d.groupby("snippet_id").normalized_score.mean().items()}
    else: raise SystemExit("no frontier judge outputs for this panel")
    s = np.array([m.get(str(i), np.nan) for i in P["items"]]) - 1.0
else: raise SystemExit("unknown judge")
ok = ~np.isnan(s); CONT = bool(np.any(np.abs(s[ok] - np.rint(s[ok])) > 1e-9))   # continuous-score judge → qbin is defined
def rps_rows(Pm_rows, y): cdf = np.cumsum(Pm_rows, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def op_probs(sv, par):
    a, b = par[0], par[1]; cuts = np.concatenate([[par[2]], par[2] + np.cumsum(np.log1p(np.exp(par[3:])))]); theta = a + b * sv
    cdf = norm.cdf(cuts[None, :] - theta[:, None]); cdf = np.concatenate([np.zeros((len(sv), 1)), cdf, np.ones((len(sv), 1))], 1); return np.clip(np.diff(cdf, axis=1), 1e-9, 1)
def fit_map(sv, y):
    def nll(par): return -np.log(op_probs(sv, par)[np.arange(len(y)), y]).sum() + 0.01 * (par[1] ** 2 + (par[3:] ** 2).sum())
    return minimize(nll, np.concatenate([[0.0, 1.0, -0.5 * (K - 2) - 0.5], np.zeros(K - 2)]), method="L-BFGS-B").x
def temp_apply(Qm, T, lam, clim): q = np.exp(np.log(np.clip(Qm, 1e-9, 1)) / T); q /= q.sum(1, keepdims=True); return (1 - lam) * q + lam * clim
def fit_temp(Qm_rows, y, clim, with_mix=True):
    best = None
    for T in (0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0):
        for lam in ((0.0, 0.1, 0.2, 0.3, 0.5, 0.7) if with_mix else (0.0,)):
            nll = -np.log(temp_apply(Qm_rows, T, lam, clim)[np.arange(len(y)), y]).sum()
            if best is None or nll < best[0]: best = (nll, T, lam)
    return best[1], best[2]
LEV = np.clip(np.rint(np.where(ok, s, 0)), 0, K - 1).astype(int); ONE = np.eye(K)[LEV]
def clim_of(y): return (np.bincount(y, minlength=K) + 0.5) / (len(y) + 0.5 * K)
def fit_mix(items, y, clim):
    best = None
    for lam in np.arange(0.05, 0.951, 0.05):
        nll = -np.log(((1 - lam) * ONE[items] + lam * clim)[np.arange(len(y)), y]).sum()
        if best is None or nll < best[0]: best = (nll, lam)
    return best[1]
def bin_table(b_items, y, nb, clim):
    """histogram binning: per bin, the calibration ratings' histogram plus a pseudo-count of 5 ratings distributed as the climatology"""
    C = np.zeros((nb, K)); np.add.at(C, (b_items, y), 1); return (C + 5 * clim) / (C.sum(1, keepdims=True) + 5)
def qbins(sv_cal):
    e = np.unique(np.quantile(sv_cal, [0.2, 0.4, 0.6, 0.8])); return e, (lambda sv: np.searchsorted(e, sv, side="right"))
NCAL = args.n_cal_list.split(","); persistent = P["raters"].persistent.astype(bool); PERS = sorted(set(P["raters"].index[persistent])) if persistent.sum() >= 3 else []
SUM, CNT = {}, []            # pooled arms: SUM[arm][split] = per-group sum of per-rating RPS on the test ratings; CNT[split] = per-group number of test ratings
LSUM, LCNT = {}, []          # leave-one-rater-out arms: [split] → (raters × groups) sums (NaN rows for raters without the arm) and counts
META = []
def evaluate(isplit):
    if LORA_CALIB_ROWS is not None:
        ca = np.array([i for i in range(N) if i in LORA_CALIB_ROWS]); te = np.array([i for i in range(N) if ok[i] and i not in LORA_CALIB_ROWS])
    else:
        ug = np.random.RandomState(isplit).permutation(NG); g_ca = set(ug[: int(.3 * NG)].tolist())   # 30 % calibration groups, 70 % test (the judge is not trained here)
        ca = np.array([i for i in range(N) if GI[i] in g_ca and ok[i]]); te = np.array([i for i in range(N) if GI[i] not in g_ca and ok[i]])
    Rca = R[R.item.isin(set(ca.tolist()))]; Rte = R[R.item.isin(set(te.tolist()))]; it_te = Rte.item.to_numpy(); y_te = Rte.y.to_numpy(); g_te = GI[it_te]
    CNT.append(np.bincount(g_te, minlength=NG).astype(float)); meta = dict(isplit=isplit, n_cal_ratings=int(len(Rca)), n_test_ratings=int(len(Rte)))
    def add(arm, Pm_full): SUM.setdefault(arm, []).append(np.bincount(g_te, weights=rps_rows(Pm_full[it_te], y_te), minlength=NG))
    add("onehot", ONE)
    if Q is not None: add("judge-own", np.where(ok[:, None], Q, 1.0 / K))
    sz = np.where(ok, s, 0.0)
    for n in NCAL:
        sub = Rca if n == "all" else Rca.sample(n=min(int(n), len(Rca)), random_state=1000 + isplit); it = sub.item.to_numpy(); y = sub.y.to_numpy(); clim = clim_of(y)
        add(f"clim({n})", np.tile(clim, (N, 1))); lam = fit_mix(it, y, clim); add(f"onehot+mix({n})", (1 - lam) * ONE + lam * clim); meta[f"lam_mix({n})"] = float(lam)
        add(f"bin({n})", bin_table(LEV[it], y, K, clim)[LEV])
        if CONT: e, f = qbins(s[it]); add(f"qbin({n})", bin_table(f(s[it]), y, len(e) + 1, clim)[f(sz)])
        add(f"map({n})", op_probs(sz, fit_map(s[it], y)))
        if Q is not None:
            T, _ = fit_temp(Q[it], y, clim, with_mix=False); add(f"temp({n})", temp_apply(np.where(ok[:, None], Q, 1.0 / K), T, 0.0, clim))
            T, lam = fit_temp(Q[it], y, clim, with_mix=True); add(f"temp+mix({n})", temp_apply(np.where(ok[:, None], Q, 1.0 / K), T, lam, clim))
    # leave-one-rater-out: calibrators fitted on the OTHER raters' calibration ratings, scored on the held-out rater's test ratings; the offset uses the rater's own calibration ratings
    if PERS:
        S = {a: np.full((len(PERS), NG), np.nan) for a in ("map(all)-LOO", "map+rater-offset-LOO", "bin(all)-LOO")}; C = np.zeros((len(PERS), NG))
        for ri, rid in enumerate(PERS):
            te_r = Rte[Rte.rater == rid]; ca_r = Rca[Rca.rater == rid]; ca_o = Rca[Rca.rater != rid]
            if len(te_r) < 5 or len(ca_o) < 20 or len(ca_r) < 5: continue
            it_r = te_r.item.to_numpy(); y_r = te_r.y.to_numpy(); g_r = GI[it_r]; C[ri] = np.bincount(g_r, minlength=NG); io = ca_o.item.to_numpy(); yo = ca_o.y.to_numpy()
            par = fit_map(s[io], yo); S["map(all)-LOO"][ri] = np.bincount(g_r, weights=rps_rows(op_probs(s[it_r], par), y_r), minlength=NG)
            ic = ca_r.item.to_numpy(); yc = ca_r.y.to_numpy()
            def nll_a(a_): p_ = par.copy(); p_[0] = a_[0]; return -np.log(op_probs(s[ic], p_)[np.arange(len(yc)), yc]).sum() + 0.5 * (a_[0] - par[0]) ** 2
            pr = par.copy(); pr[0] = minimize(nll_a, np.array([par[0]]), method="L-BFGS-B").x[0]; S["map+rater-offset-LOO"][ri] = np.bincount(g_r, weights=rps_rows(op_probs(s[it_r], pr), y_r), minlength=NG)
            S["bin(all)-LOO"][ri] = np.bincount(g_r, weights=rps_rows(bin_table(LEV[io], yo, K, clim_of(yo))[LEV[it_r]], y_r), minlength=NG)
        for a in S: LSUM.setdefault(a, []).append(S[a])
        LCNT.append(C)
    META.append(meta)
t0 = time.time()
for isplit in range(args.splits): evaluate(isplit)
rng = np.random.RandomState(17); W = np.vstack([np.ones(NG), rng.multinomial(NG, np.ones(NG) / NG, size=args.B)])   # row 0 = the point estimate
def stat(arm):
    """(1 + B) vector: mean over splits of the weighted mean RPS of an arm"""
    if arm in SUM: return np.mean([(W @ S_) / np.maximum(W @ C_, 1e-12) for S_, C_ in zip(SUM[arm], CNT)], axis=0)
    out = []
    for S_, C_ in zip(LSUM[arm], LCNT):
        good = ~np.isnan(S_[:, 0]); num = W @ S_[good].T; den = W @ C_[good].T; out.append(np.nanmean(np.where(den > 0, num / np.maximum(den, 1e-12), np.nan), axis=1))
    return np.mean(out, axis=0)
def ci(v): return [float(v[0]), float(np.nanpercentile(v[1:], 2.5)), float(np.nanpercentile(v[1:], 97.5))]
ST = {a: stat(a) for a in list(SUM) + list(LSUM)}; res = {"arms": {a: ci(v) for a, v in ST.items()}, "contrasts": {}}
for n in NCAL:
    for b in ("clim", "onehot+mix", "bin", "qbin", "temp", "temp+mix"):
        if f"{b}({n})" in ST: res["contrasts"][f"map({n}) - {b}({n})"] = ci(ST[f"map({n})"] - ST[f"{b}({n})"])
    res["contrasts"][f"map({n}) - onehot"] = ci(ST[f"map({n})"] - ST["onehot"]); res["contrasts"][f"bin({n}) - clim({n})"] = ci(ST[f"bin({n})"] - ST[f"clim({n})"])
if LSUM:
    res["contrasts"]["map+rater-offset-LOO - map(all)-LOO"] = ci(ST["map+rater-offset-LOO"] - ST["map(all)-LOO"]); res["contrasts"]["map(all)-LOO - bin(all)-LOO"] = ci(ST["map(all)-LOO"] - ST["bin(all)-LOO"])
    res["n_loo_raters"] = int(np.mean([(~np.isnan(S_[:, 0])).sum() for S_ in LSUM["map(all)-LOO"]]))
res.update(panel=args.panel, judge=name, K=K, n_items=int(ok.sum()), n_groups=NG, n_raters=int(R.rater.nunique()), n_persistent=len(PERS), splits=args.splits, B=args.B, continuous_score=CONT, meta=META)
json.dump(res, open(f"{OUT}/summary.json", "w"), indent=1)
L = [f"# judge_map2 — {args.panel} / judge = {name}: {int(ok.sum())} items in {NG} groups, K = {K}, {R.rater.nunique()} raters ({len(PERS)} persistent); {args.splits} splits; RPS, 95 % item-group bootstrap (B = {args.B})", "", "| arm | RPS |", "|---|---|"]
L += [f"| {a} | {v[0]:.4f} [{v[1]:.4f}, {v[2]:.4f}] |" for a, v in sorted(res["arms"].items(), key=lambda kv: kv[1][0])] + ["", "| contrast | difference |", "|---|---|"]
L += [f"| {a} | {v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}] |" for a, v in res["contrasts"].items()]
open(f"{OUT}/summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L), f"\n[{time.time()-t0:.0f}s]")
