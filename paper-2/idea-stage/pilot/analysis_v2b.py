"""
Analysis for the final protocol: per (criterion, split) gather arms x evaluator folds, calibrate each arm on its calibration split
against the TARGET raters only, score the test items against the EXCLUDED rater with RPS, and report
  Δ_soft = RPS(hard) − RPS(chen);  Δ_adv = RPS(chen0) − RPS(chen);  Δ_link^ITT = RPS(perm) − RPS(chen)
with diff-clustered bootstrap CIs (B = 2000), per-fold estimates, intensities (changed fraction) and dose from the certificates.
Usage: python analysis_v2.py results_v2/why/s0   (expects results_v2/why/s0/f{0..5}/{hard,chen0,chen,perm}/)
"""
import sys, os, json, glob, numpy as np, pandas as pd
K = 5; LV = np.arange(K); ROOT = "/mnt/hdd2/jundahe/LLM-J/code/commit_message"
bench = pd.read_csv(f"{ROOT}/data/CM-benchmark.csv")
RD = "/mnt/hdd2/jundahe/LLM-J/code/code_readability"; _M = pd.read_csv(f"{RD}/data/scalabrino/scores.csv", index_col=0); _ds = pd.read_csv(f"{RD}/data/coreeval_snippets/Scalabrino_java_Code.csv")
H_RD = np.array([_M.iloc[:, list(_M.columns).index(f"Snippet{int(s)}")].to_numpy(int) for s in _ds.snippet_id]) - 1
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0): Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
GRID_T = [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]; GRID_L = [0, .05, .1, .2, .3, .5]
def fit_cal(Pc, Hc_targets, p0):
    best = None
    for T in GRID_T:
        for lam in GRID_L:
            Q = calib(Pc, T, lam, p0); s = np.mean([rps(Q, Hc_targets[:, r]).mean() for r in range(Hc_targets.shape[1])])
            if best is None or s < best[0]: best = (s, T, lam)
    return best[1], best[2]
def load_arm(path, crit):
    Pt = np.load(f"{path}/P_test.npy"); Pc = np.load(f"{path}/P_calib.npy")
    it = pd.read_csv(f"{path}/items_test.csv"); ic = pd.read_csv(f"{path}/items_calib.csv"); meta = json.load(open(f"{path}/meta.json"))
    H = H_RD if crit == "readability" else bench[[f"{crit}_{i}" for i in range(1, 7)]].to_numpy(int)
    return Pt, Pc, H[it.row.to_numpy()], H[ic.row.to_numpy()], it, meta
def analyse(root, B=2000, seed=0):
    parts = root.rstrip("/").split("/"); crit = [x for x in parts if x in ("why", "what", "readability")][-1]; M_R = 9 if crit == "readability" else 6; folds = sorted(glob.glob(f"{root}/f*")); arms = ["hard", "chen0", "chen", "perm", "perm_mode"]
    per_item = {a: [] for a in arms}; per_fold = {a: [] for a in arms}; intens = []; groups = None; rows = []
    for fd in folds:
        f = int(os.path.basename(fd)[1:]); T = [r for r in range(M_R) if r != f]; res = {}
        for a in arms:
            path = f"{fd}/{a}"
            if not os.path.exists(f"{path}/P_test.npy"): continue
            Pt, Pc, Ht, Hc, it, meta = load_arm(path, crit)
            p0 = np.bincount(Hc[:, T].ravel(), minlength=K) / Hc[:, T].size         # climatology from target raters (calib split stands in for train)
            Tc, lam = fit_cal(Pc, Hc[:, T], p0); Q = calib(Pt, Tc, lam, p0)
            r = rps(Q, Ht[:, f]); res[a] = r
            if groups is None: groups = pd.factorize(it.hash if "hash" in it.columns else it.snippet_id)[0]
            rows.append(dict(fold=f, arm=a, T=Tc, lam=lam, rps_raw=float(rps(Pt, Ht[:, f]).mean()), rps_cal=float(r.mean()),
                             changed=meta.get("changed_fraction"), dose=meta.get("dose_tv_mean"), steps=meta.get("n_steps")))
            if a == "perm": intens.append(meta.get("changed_fraction"))
        if all(a in res for a in arms):
            for a in arms: per_item[a].append(res[a]); per_fold[a].append(float(res[a].mean()))
    tab = pd.DataFrame(rows); print(tab.to_string(index=False))
    if not per_item["hard"]: print("no complete fold yet"); return
    M = {a: np.mean(per_item[a], 0) for a in arms}           # item-level RPS averaged over completed folds (each fold = different evaluator)
    rng = np.random.RandomState(seed); uniq = np.unique(groups)
    def boot(diff):
        vals = []
        for _ in range(B):
            g = rng.choice(uniq, len(uniq), replace=True); idx = np.concatenate([np.where(groups == x)[0] for x in g]); vals.append(diff[idx].mean())
        return float(diff.mean()), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
    out = {"n_folds": len(per_item["hard"]), "n_test_items": int(len(M["hard"])), "n_diffs": int(len(uniq)),
           "mean_changed_fraction": float(np.mean(intens)) if intens else None,
           "RPS": {a: float(M[a].mean()) for a in arms},
           "Δ_soft  = hard − chen": boot(M["hard"] - M["chen"]), "Δ_adv   = chen0 − chen": boot(M["chen0"] - M["chen"]),
           "Δ_link^ITT = perm − chen": boot(M["perm"] - M["chen"]), "Δ_link_mode = perm_mode − chen": boot(M["perm_mode"] - M["chen"]), "perm_mode − perm": boot(M["perm_mode"] - M["perm"]), "perm_mode − hard": boot(M["perm_mode"] - M["hard"]), "per_fold_RPS": per_fold}
    print(json.dumps(out, indent=1)); json.dump(out, open(f"{root}/analysis_v2b.json", "w"), indent=1)
if __name__ == "__main__":
    analyse(sys.argv[1])
