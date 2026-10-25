"""
Location diagnostic (Codex round 5 §2): does the judge learn item LOCATION from the target, and does the evaluator reward it?
For each panel / fold / arm, on test items, with q = predicted pmf (raw and arm-calibrated):
  mu_hat = E_q[Y];  mu_-e = mean of the target raters (evaluator excluded);  z = mode of target raters
  rho_within(mu_hat, mu_-e | z)   partial Spearman controlling for the mode  (overall Spearman mostly rediscovers the mode)
  rho_within(mu_-e, y_e | z)      target-side relevance: does the target mean predict the held-out evaluator beyond the mode?
  slope / intercept of mu_hat on mu_-e; MAE; mean entropy; mean max-prob; fitted (T, lam)
  RPS decomposed by cumulative threshold t: mean (F_q(t) - 1[y_e <= t])^2 for t = 0..K-2, per arm; differences chen − perm_mode by threshold
Usage: python diag_location.py commit why | commit what | summeval
"""
import sys, os, json, glob, numpy as np, pandas as pd
from paths import LLMJ
sys.path.insert(0, LLMJ + "/paper-2/phase2"); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label
which = sys.argv[1]
if which == "commit":
    crit = sys.argv[2]; K = 5; bench = pd.read_csv(LLMJ + "/code/commit_message/data/CM-benchmark.csv"); H = bench[[f"{crit}_{i}" for i in range(1, 7)]].to_numpy(int)
    root = f"{LLMJ}/paper-2/idea-stage/pilot/results_v2/{crit}/s0"; arms = ["hard", "chen", "perm", "perm_mode", "mean2", "proto"]; ev_of = lambda meta, f: f; M = 6
else:
    import data_panels; PAN = data_panels.load("summeval_coherence8"); H = PAN["H"]; K = PAN["K"]; root = LLMJ + "/paper-2/phase2/results/lora/summeval_coherence8/s0"
    arms = ["hard", "chen", "perm", "perm_mode", "mean2", "proto"]; ev_of = lambda meta, f: meta["evaluator"]; M = H.shape[1]
LV = np.arange(K)
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0): Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
def fit_cal(Pc, Hc, p0):
    best = None
    for T in [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]:
        for lam in [0, .05, .1, .2, .3, .5]:
            s = np.mean([rps(calib(Pc, T, lam, p0), Hc[:, r]).mean() for r in range(Hc.shape[1])])
            if best is None or s < best[0]: best = (s, T, lam)
    return best[1], best[2]
def partial_spearman(x, y, z):
    """within-mode association with CATEGORICAL control for the mode (Codex round 6): rank x and y within each mode stratum, centre per stratum, pool, then Pearson"""
    x = np.asarray(x, float); y = np.asarray(y, float); z = np.asarray(z); ex = np.zeros(len(x)); ey = np.zeros(len(y))
    for c in np.unique(z):
        m = z == c
        if m.sum() < 3: ex[m] = 0; ey[m] = 0; continue
        rx = pd.Series(x[m]).rank().to_numpy(); ry = pd.Series(y[m]).rank().to_numpy(); ex[m] = rx - rx.mean(); ey[m] = ry - ry.mean()
    return float((ex * ey).mean() / (ex.std() * ey.std() + 1e-12))
rows = []; thr = {}
for fd in sorted(glob.glob(f"{root}/f*")):
    f = int(os.path.basename(fd)[1:])
    for a in arms:
        p = f"{fd}/{a}"
        if not os.path.exists(f"{p}/P_test.npy"): continue
        meta = json.load(open(f"{p}/meta.json")); E = ev_of(meta, f); T = [r for r in range(M) if r != E]
        Pt, Pc = np.load(f"{p}/P_test.npy"), np.load(f"{p}/P_calib.npy"); it = pd.read_csv(f"{p}/items_test.csv").row.to_numpy(); ic = pd.read_csv(f"{p}/items_calib.csv").row.to_numpy()
        Ht, Hc = H[it], H[ic]; p0 = np.bincount(Hc[:, T].ravel(), minlength=K) / Hc[:, T].size; Tc, lam = fit_cal(Pc, Hc[:, T], p0)
        mu_e = Ht[:, T].mean(1); z = np.array([z_label(r) for r in Ht[:, T]]); ye = Ht[:, E]
        for est, Q in (("raw", Pt), ("arm", calib(Pt, Tc, lam, p0))):
            mu_hat = Q @ LV; slope, intercept = np.polyfit(mu_e, mu_hat, 1)
            rows.append(dict(fold=f, arm=a, est=est, rho_within_pred=partial_spearman(mu_hat, mu_e, z), rho_within_target=partial_spearman(mu_e, ye, z), slope=slope, intercept=intercept, mae=float(np.abs(mu_hat - mu_e).mean()),
                             entropy=float(-(Q * np.log(Q + 1e-12)).sum(1).mean()), maxprob=float(Q.max(1).mean()), T=Tc, lam=lam, rps=float(rps(Q, ye).mean())))
            cdf = np.cumsum(Q, 1)
            for t in range(K - 1): thr.setdefault((a, est, t), []).append(float(((cdf[:, t] - (ye <= t)) ** 2).mean()))
df = pd.DataFrame(rows); pd.set_option("display.width", 250)
# identical completed folds across arms (Codex round 6): keep only folds where every arm is present
folds_all = [f for f in df.fold.unique() if set(df[df.fold == f].arm) >= set(arms)]; df = df[df.fold.isin(folds_all)]; print("folds used (all arms present):", folds_all)
print(f"### location diagnostic: {which} {sys.argv[2] if which == 'commit' else ''}  (means over folds)")
print(df.groupby(["est", "arm"])[["rps", "rho_within_pred", "rho_within_target", "slope", "intercept", "mae", "entropy", "maxprob", "T", "lam"]].mean().round(4).to_string())
print("\nRPS by cumulative threshold t (mean over folds), raw:")
print(pd.DataFrame({a: [np.mean(thr[(a, "raw", t)]) for t in range(K - 1)] for a in arms if (a, "raw", 0) in thr}, index=[f"t<={t}" for t in range(K - 1)]).round(4).to_string())
print("\nRPS by cumulative threshold t, arm-calibrated:")
print(pd.DataFrame({a: [np.mean(thr[(a, "arm", t)]) for t in range(K - 1)] for a in arms if (a, "arm", 0) in thr}, index=[f"t<={t}" for t in range(K - 1)]).round(4).to_string())
