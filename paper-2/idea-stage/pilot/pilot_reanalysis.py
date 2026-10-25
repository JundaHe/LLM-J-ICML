"""
Re-analysis after the round-1 external review (fixes applied):
 - inference clustered by source diff (hash): 240 test rows = 120 diffs x {developer, generated}
 - ONE shared calibrator (temperature T + climatology mixture lam), fitted on ALL six raters' labels by hash-grouped
   2-fold cross-fitting, applied IDENTICALLY to every arm (CE, KL, permuted, k=2/k=6 arms)  [symmetric; still
   transductive on the test set -> the experiment plan moves it to an untouched validation split]
 - ordinal threshold-Brier decomposition: Brier_k = REL - RES + UNC (10 forecast bins); RES summed over the four
   thresholds = item-conditioned resolution ("information beyond calibration")
 - location control: cross-fitted cubic polynomial of entropy on the judge's EXPECTED score (grouped 5-fold);
   residual -> Low-stratum AUROC; tie-aware AUROC
 - k=2 arms additionally scored on the four rater identities NOT used for their targets (raters [3,5] were used)
Usage: python pilot_reanalysis.py
"""
import os, sys, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csje_eval as E, cm_data
from sklearn.model_selection import GroupKFold
K = 5; LV = np.arange(K); B = 1000
RUNS = ["base_zeroshot", "ce_median_s0", "kl_soft_s0", "kl_soft_permuted_s0", "kl_raw_k2_s0", "crps_k2_s0", "pp_crps_k2_s0", "crps_k6_s0", "pp_crps_k6_s0"]
SEEN_K2 = [3, 5]
full = pd.concat([cm_data.load("developer", 4000), cm_data.load("generated", 4000)]).reset_index(drop=True)
te = pd.read_csv("results/ce_median_s0/test_items.csv"); d = te.merge(full, on=["hash", "msg_type"], how="left")
groups = pd.factorize(d.hash)[0]; n = len(d)
tr_mask = ~full.set_index(["hash", "msg_type"]).index.isin(list(zip(te.hash, te.msg_type))); dtr = full[tr_mask]

def rps(P, y):
    cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0):
    Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
def fit_shared_calibrator(P, H, p0):
    """cross-fitted over hash groups; objective = mean RPS over ALL raters; returns calibrated P"""
    out = np.zeros_like(P)
    for tr, va in GroupKFold(2).split(P, groups=groups):
        best = None
        for T in [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]:
            for lam in [0, .05, .1, .2, .3, .5]:
                Q = calib(P[tr], T, lam, p0); s = np.mean([rps(Q, H[tr, r]).mean() for r in range(H.shape[1])])
                if best is None or s < best[0]: best = (s, T, lam)
        out[va] = calib(P[va], best[1], best[2], p0)
    return out
def decomposition(P, H, bins=10):
    """threshold-Brier REL/RES/UNC summed over thresholds, pooled over raters (forecast f_k = P(Y<=k))"""
    REL = RES = UNC = 0.0
    for k in range(K - 1):
        f = np.repeat(np.cumsum(P, 1)[:, k], H.shape[1]); o = (H <= k).astype(float).ravel()
        ob = o.mean(); bidx = np.minimum((f * bins).astype(int), bins - 1)
        for b in range(bins):
            m = bidx == b
            if m.any(): REL += m.mean() * (f[m].mean() - o[m].mean()) ** 2; RES += m.mean() * (o[m].mean() - ob) ** 2
        UNC += ob * (1 - ob)
    return REL / (K - 1), RES / (K - 1), UNC / (K - 1)
def cluster_boot(stat_fn, seed=0):
    rng = np.random.RandomState(seed); uniq = np.unique(groups); vals = []
    for _ in range(B):
        g = rng.choice(uniq, len(uniq), replace=True); idx = np.concatenate([np.where(groups == x)[0] for x in g]); vals.append(stat_fn(idx))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
def loc_controlled_auroc(P, low):
    ent = E.entropy(P); ev = P @ LV; resid = np.zeros(n)
    for tr, va in GroupKFold(5).split(P, groups=groups):
        X = np.vander(ev[tr], 4); beta = np.linalg.lstsq(X, ent[tr], rcond=None)[0]; resid[va] = ent[va] - np.vander(ev[va], 4) @ beta
    return E.auroc(ent, low), E.auroc(-np.abs(ev - 2.0), low), E.auroc(resid, low)

report = {}
for crit in ["what", "why"]:
    H = cm_data.H(d, crit); Htr = cm_data.H(dtr, crit); m = H.shape[1]
    p0 = np.bincount(Htr.ravel(), minlength=K) / Htr.size; low = E.strata(H) == "Low"
    Ps = {r: np.load(f"results/{r}/P_{crit}.npy") for r in RUNS if os.path.exists(f"results/{r}/P_{crit}.npy")}
    rows = {}; per_item = {}
    for name, P in Ps.items():
        Pc = fit_shared_calibrator(P, H, p0)
        for tag, Q in [("raw", P), ("cal", Pc)]:
            R = np.stack([rps(Q, H[:, r]) for r in range(m)], 1)           # n x 6
            rel, res, unc = decomposition(Q, H)
            unseen = [r for r in range(m) if r not in SEEN_K2]
            rows[f"{name}|{tag}"] = {"RPS": float(R.mean()), "RPS_unseen4": float(R[:, unseen].mean()), "REL": rel, "RES": res,
                                     "RPS_ci": cluster_boot(lambda idx, R=R: R[idx].mean())}
            per_item[f"{name}|{tag}"] = R.mean(1)
        a_raw, a_loc, a_res = loc_controlled_auroc(P, low); rows[f"{name}|raw"].update(ent_low_raw=a_raw, loc_only=a_loc, ent_low_resid=a_res)
    clim = np.tile(p0, (n, 1)); Rc = np.stack([rps(clim, H[:, r]) for r in range(m)], 1).mean()
    panel = np.stack([np.stack([np.bincount(np.delete(H, r, 1)[i], minlength=K) / (m - 1) for i in range(n)]) for r in range(m)])
    Rp = np.mean([rps(panel[r], H[:, r]).mean() for r in range(m)])
    def contrast(a, b, seed=0):
        diff = per_item[a] - per_item[b]; return [float(diff.mean()), *cluster_boot(lambda idx: diff[idx].mean(), seed)]
    C = {}
    for tag in ["raw", "cal"]:
        C[f"CE−KL ({tag})"] = contrast(f"ce_median_s0|{tag}", f"kl_soft_s0|{tag}")
        C[f"CE−permKL ({tag})"] = contrast(f"ce_median_s0|{tag}", f"kl_soft_permuted_s0|{tag}")
        C[f"permKL−KL ({tag})"] = contrast(f"kl_soft_permuted_s0|{tag}", f"kl_soft_s0|{tag}")
    C["CE(cal)−KL(raw)  [old N1-style, symmetric now]"] = contrast("ce_median_s0|cal", "kl_soft_s0|raw")
    report[crit] = {"climatology_RPS": float(Rc), "panel_RPS": float(Rp), "rows": rows, "contrasts": C}
    print(f"\n[{crit}] climatology RPS={Rc:.4f}  5-rater panel RPS={Rp:.4f}   (cluster-by-diff 95% CIs, B={B})")
    print(f"   {'arm':28s} {'RPS raw':>8s} {'RPS cal':>8s} {'unseen4 raw':>11s} {'REL raw/cal':>12s} {'RES raw/cal':>12s} | ent→Low raw / loc-only / resid")
    for name in Ps:
        r0, r1 = rows[f"{name}|raw"], rows[f"{name}|cal"]
        print(f"   {name:28s} {r0['RPS']:8.4f} {r1['RPS']:8.4f} {r0['RPS_unseen4']:11.4f} {r0['REL']:.4f}/{r1['REL']:.4f} {r0['RES']:.4f}/{r1['RES']:.4f} | {r0['ent_low_raw']:.3f} / {r0['loc_only']:.3f} / {r0['ent_low_resid']:.3f}")
    for k, v in C.items(): print(f"   Δ {k:42s} {v[0]:+.4f}  CI[{v[1]:+.4f}, {v[2]:+.4f}]")
json.dump(report, open("results/pilot_reanalysis.json", "w"), indent=1, default=float)
