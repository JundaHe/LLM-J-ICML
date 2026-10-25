"""Pairwise-contrast analysis tolerant of missing arms: for each contrast (a − b), use the folds where both arms exist; item-level RPS averaged over those folds; item-clustered bootstrap.
Usage: python analysis_v3.py results_v2/why/s0 [--B 2000]"""
import sys, os, json, glob, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis_v2 import load_arm, fit_cal, calib, rps, K
root = sys.argv[1].rstrip("/"); B = 2000
parts = root.split("/"); crit = [x for x in parts if x in ("why", "what", "readability")][-1]; M_R = 9 if crit == "readability" else 6
ARMS = ["hard", "chen0", "chen", "perm", "perm_mode", "mean2", "proto"]
CONTRASTS = [("Δ_soft = hard − chen", "hard", "chen"), ("Δ_adv = chen0 − chen", "chen0", "chen"), ("Δ_link = perm − chen", "perm", "chen"), ("Δ_link_mode = perm_mode − chen", "perm_mode", "chen"),
             ("perm_mode − hard", "perm_mode", "hard"), ("Δ_mean2 = chen − mean2", "chen", "mean2"), ("mean2 − hard", "mean2", "hard"), ("perm_mode − mean2", "perm_mode", "mean2"), ("chen − proto", "chen", "proto"), ("proto − hard", "proto", "hard"), ("mean2 − proto", "mean2", "proto")]
res = {a: {} for a in ARMS}; res_raw = {a: {} for a in ARMS}; res_common = {a: {} for a in ARMS}; groups = {}; rows = []; cal_pool = {}
for fd in sorted(glob.glob(f"{root}/f*")):
    f = int(os.path.basename(fd)[1:]); T = [r for r in range(M_R) if r != f]
    for a in ARMS:
        path = f"{fd}/{a}"
        if not os.path.exists(f"{path}/P_test.npy"): continue
        Pt, Pc, Ht, Hc, it, meta = load_arm(path, crit); p0 = np.bincount(Hc[:, T].ravel(), minlength=K) / Hc[:, T].size
        Tc, lam = fit_cal(Pc, Hc[:, T], p0); Q = calib(Pt, Tc, lam, p0); r = rps(Q, Ht[:, f]); res[a][f] = r; res_raw[a][f] = rps(Pt, Ht[:, f]); cal_pool.setdefault(f, []).append((a, Pt, Pc, Hc[:, T], p0, Ht[:, f]))
        groups[f] = pd.factorize(it.hash if "hash" in it.columns else it.snippet_id)[0]
        rows.append(dict(fold=f, arm=a, rps_cal=float(r.mean()), T=Tc, lam=lam, loss=meta.get("final_loss"), changed=meta.get("changed_fraction"), mean_shift=meta.get("mean_shift_mean")))
COMMON_ROSTER = ["hard", "chen", "perm", "perm_mode"]      # fixed roster for the common map (Codex round 8): comparable across partitions regardless of which extra arms exist
for f, lst in cal_pool.items():
    use = [x for x in lst if x[0] in COMMON_ROSTER] if all(any(x[0] == a for x in lst) for a in COMMON_ROSTER) else lst
    Pc_all = np.concatenate([x[2] for x in use]); Hc_all = np.concatenate([x[3] for x in use]); Tc, lam = fit_cal(Pc_all, Hc_all, use[0][4])
    for a, Pt, Pc, HcT, p0_, Htf in lst: res_common[a][f] = rps(calib(Pt, Tc, lam, p0_), Htf)
tab = pd.DataFrame(rows); print("arm-specific calibrated RPS"); print(tab.pivot_table(index="fold", columns="arm", values="rps_cal").round(4).to_string()); print("raw RPS"); print(pd.DataFrame([dict(fold=f, arm=a, raw=float(v.mean())) for a in ARMS for f, v in res_raw[a].items()]).pivot_table(index="fold", columns="arm", values="raw").round(4).to_string())
print("final training loss by arm:", tab.groupby("arm").loss.mean().round(4).to_dict())
rng = np.random.RandomState(0); out = {}
for name, a, b in CONTRASTS:
    folds = sorted(set(res[a]) & set(res[b]))
    if not folds: continue
    diff = np.mean([res[a][f] - res[b][f] for f in folds], 0); g = groups[folds[0]]; uniq = np.unique(g)
    vals = [diff[np.concatenate([np.where(g == x)[0] for x in rng.choice(uniq, len(uniq), replace=True)])].mean() for _ in range(B)]
    draw = np.mean([res_raw[a][f] - res_raw[b][f] for f in folds], 0); dcom = np.mean([res_common[a][f] - res_common[b][f] for f in folds], 0); rng2 = np.random.RandomState(1)
    vraw = [draw[np.concatenate([np.where(g == x)[0] for x in rng2.choice(uniq, len(uniq), replace=True)])].mean() for _ in range(B)]
    out[name] = dict(raw=float(draw.mean()), raw_lo=float(np.percentile(vraw, 2.5)), raw_hi=float(np.percentile(vraw, 97.5)), common=float(dcom.mean()), cal=float(diff.mean()), cal_lo=float(np.percentile(vals, 2.5)), cal_hi=float(np.percentile(vals, 97.5)), n_folds=len(folds))
    o = out[name]; print(f"  {name:32s} RAW {o['raw']:+.4f} [{o['raw_lo']:+.4f}, {o['raw_hi']:+.4f}] | common-map {o['common']:+.4f} | arm-cal {o['cal']:+.4f} [{o['cal_lo']:+.4f}, {o['cal_hi']:+.4f}]  folds={len(folds)}")
json.dump(dict(contrasts=out, rps={a: float(np.mean([v.mean() for v in res[a].values()])) for a in ARMS if res[a]}), open(f"{root}/analysis_v3.json", "w"), indent=1)
