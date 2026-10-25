"""Contrast analysis for train_judge_v3.py outputs (reports arm-specific post-calibration RPS as primary and raw RPS alongside — Codex round 3) (any panel in data_panels): per fold, calibrate each arm on its calib items against the TARGET raters
(temperature + climatology shrinkage, same grid as Phase 1), score test items with RPS against the EVALUATOR rater, then paired contrasts on the folds
where both arms exist, with item-clustered bootstrap (groups = PAN['groups'] if present).
Usage: python analysis_lora_v3.py results/lora/summeval_coherence8/s0"""
import sys, os, json, glob, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import data_panels
root = sys.argv[1].rstrip("/"); panel = root.split("/")[-2]; PAN = data_panels.load(panel); H = PAN["H"]; K = PAN["K"]; LV = np.arange(K); B = 2000
G = PAN.get("groups", np.arange(H.shape[0]))
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0): Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
def fit_cal(Pc, Hc, p0):
    best = None
    for T in [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]:
        for lam in [0, .05, .1, .2, .3, .5]:
            s = np.mean([rps(calib(Pc, T, lam, p0), Hc[:, r]).mean() for r in range(Hc.shape[1])])
            if best is None or s < best[0]: best = (s, T, lam)
    return best[1], best[2]
ARMS = ["hard", "chen0", "chen", "perm", "perm_mode", "mean2", "proto"]
CONTRASTS = [("Δ_soft = hard − chen", "hard", "chen"), ("Δ_link = perm − chen", "perm", "chen"), ("Δ_link_mode = perm_mode − chen", "perm_mode", "chen"), ("perm_mode − hard", "perm_mode", "hard"),
             ("Δ_mean2 = chen − mean2", "chen", "mean2"), ("mean2 − hard", "mean2", "hard"), ("chen − proto", "chen", "proto"), ("proto − hard", "proto", "hard"), ("mean2 − proto", "mean2", "proto")]
res = {a: {} for a in ARMS}; res_raw = {}; res_common = {}; grp = {}; rows = []; cal_pool = {}
for fd in sorted(glob.glob(f"{root}/f*")):
    f = int(os.path.basename(fd)[1:])
    for a in ARMS:
        path = f"{fd}/{a}"
        if not os.path.exists(f"{path}/P_test.npy"): continue
        meta = json.load(open(f"{path}/meta.json")); E = meta["evaluator"]; T = meta["targets"]
        Pt, Pc = np.load(f"{path}/P_test.npy"), np.load(f"{path}/P_calib.npy"); it, ic = pd.read_csv(f"{path}/items_test.csv"), pd.read_csv(f"{path}/items_calib.csv")
        Ht, Hc = H[it.row.to_numpy()], H[ic.row.to_numpy()]; p0 = np.bincount(Hc[:, T].ravel(), minlength=K) / Hc[:, T].size
        Tc, lam = fit_cal(Pc, Hc[:, T], p0); r = rps(calib(Pt, Tc, lam, p0), Ht[:, E]); res[a][f] = r; grp[f] = pd.factorize(G[it.row.to_numpy()])[0]
        res_raw.setdefault(a, {})[f] = rps(Pt, Ht[:, E]); cal_pool.setdefault(f, []).append((a, Pt, Pc, Hc[:, T], p0, Ht[:, E]))
        rows.append(dict(fold=f, evaluator=E, arm=a, rps_cal=float(r.mean()), rps_raw=float(rps(Pt, Ht[:, E]).mean()), T=Tc, lam=lam, loss=meta.get("final_loss"), changed=meta.get("changed_fraction"), mean_shift=meta.get("mean_shift_mean"), steps=meta.get("n_steps")))
# common-map sensitivity: one (T, lam) per fold fitted on the POOLED calibration predictions of all arms present
for f, lst in cal_pool.items():
    Pc_all = np.concatenate([x[2] for x in lst]); Hc_all = np.concatenate([x[3] for x in lst]); p0 = lst[0][4]; Tc, lam = fit_cal(Pc_all, Hc_all, p0)
    for a, Pt, Pc, HcT, p0_, HtE in lst: res_common.setdefault(a, {})[f] = rps(calib(Pt, Tc, lam, p0_), HtE)
tab = pd.DataFrame(rows); print("arm-specific calibrated RPS"); print(tab.pivot_table(index="fold", columns="arm", values="rps_cal").round(4).to_string()); print("raw RPS"); print(tab.pivot_table(index="fold", columns="arm", values="rps_raw").round(4).to_string()); print("train loss:", tab.groupby("arm").loss.mean().round(4).to_dict())
rng = np.random.RandomState(0); out = {}
for name, a, b in CONTRASTS:
    folds = sorted(set(res[a]) & set(res[b]))
    if not folds: continue
    diff = np.mean([res[a][f] - res[b][f] for f in folds], 0); g = grp[folds[0]]; uniq = np.unique(g)
    vals = [diff[np.concatenate([np.where(g == x)[0] for x in rng.choice(uniq, len(uniq), replace=True)])].mean() for _ in range(B)]
    draw = np.mean([res_raw[a][f] - res_raw[b][f] for f in folds], 0); dcom = np.mean([res_common[a][f] - res_common[b][f] for f in folds], 0)
    rng2 = np.random.RandomState(1); vraw = [draw[np.concatenate([np.where(g == x)[0] for x in rng2.choice(uniq, len(uniq), replace=True)])].mean() for _ in range(B)]
    out[name] = dict(raw=float(draw.mean()), raw_lo=float(np.percentile(vraw, 2.5)), raw_hi=float(np.percentile(vraw, 97.5)), common=float(dcom.mean()),
                     cal=float(diff.mean()), cal_lo=float(np.percentile(vals, 2.5)), cal_hi=float(np.percentile(vals, 97.5)), n_folds=len(folds))
    o = out[name]; print(f"  {name:32s} RAW {o['raw']:+.4f} [{o['raw_lo']:+.4f}, {o['raw_hi']:+.4f}] | common-map {o['common']:+.4f} | arm-cal {o['cal']:+.4f} [{o['cal_lo']:+.4f}, {o['cal_hi']:+.4f}]  folds={len(folds)}")
json.dump(dict(panel=panel, estimands="raw (T=1,lam=0) primary; common-map sensitivity; arm-specific calibrated secondary", contrasts=out, rps_cal={a: float(np.mean([v.mean() for v in res[a].values()])) for a in ARMS if res[a]}, rps_raw={a: float(np.mean([v.mean() for v in res_raw[a].values()])) for a in res_raw}), open(f"{root}/analysis_lora_v3.json", "w"), indent=1)
