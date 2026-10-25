"""
Pilot A — learned disagreement vs learned smoothing (contradiction#1 + diagnostic#2 nulls + distributional skill score).
Every judge (and every null) is scored against each held-out rater r with the ranked probability score
    RPS_r = sum_k (CDF_q(k) - 1[Y_r <= k])^2 / (K-1)        (bounded ordinal proper score; K=5)
and NLL_r = -log q(Y_r); strata for item i come from the five raters other than r.
Nulls (item-independent, fitted on TRAIN items or cross-fitted on test):
  N1 temperature+marginal mixture on a point judge:  q' = softmax(log q / T) * (1-lam) + lam * p_clim   (cross-fitted 2-fold over test items, fit by NLL)
  N2 location-conditional human pmf: p_train(rating | judge's argmax level)   (uses train-item human ratings; judge-side conditioning only)
  N3 climatology: criterion marginal from train items
Skill score (distributional HCA):  skill = 1 - (RPS_model - RPS_panel)/(RPS_clim - RPS_panel), RPS_panel = RPS of the other-5-rater empirical pmf vs Y_r.
Usage: python pilot_a_analysis.py base_zeroshot ce_median_s0 kl_soft_s0 kl_soft_permuted_s0 ...
"""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csje_eval as E, cm_data
K = 5; LV = np.arange(K)
full = pd.concat([cm_data.load("developer", 4000), cm_data.load("generated", 4000)]).reset_index(drop=True)

def rps(P, y):            # P: n x K pmf, y: n ints -> per-item RPS normalised by K-1
    cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float)
    return ((cdf - step) ** 2).sum(1) / (K - 1)
def nll(P, y): return -np.log(np.clip(P[np.arange(len(y)), y], 1e-6, 1))
def temp_mix(P, y, p_clim, folds=2, seed=0):
    """cross-fitted temperature + climatology mixture; returns calibrated pmf for every item"""
    n = len(P); idx = np.random.RandomState(seed).permutation(n); out = np.zeros_like(P); logP = np.log(np.clip(P, 1e-9, 1))
    grid_T = [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]; grid_l = [0, .05, .1, .2, .3, .5, .7]
    for f in range(folds):
        va = idx[f::folds]; tr = np.setdiff1d(idx, va); best = None
        for T in grid_T:
            for l in grid_l:
                Q = np.exp(logP[tr] / T); Q /= Q.sum(1, keepdims=True); Q = (1 - l) * Q + l * p_clim
                s = nll(Q, y[tr]).mean()
                if best is None or s < best[0]: best = (s, T, l)
        _, T, l = best; Q = np.exp(logP[va] / T); Q /= Q.sum(1, keepdims=True); out[va] = (1 - l) * Q + l * p_clim
    return out

def analyse(runs, B=1000, seed=0):
    rng = np.random.RandomState(seed); report = {}
    te = pd.read_csv(f"results/{runs[0]}/test_items.csv"); d = te.merge(full, on=["hash", "msg_type"], how="left")
    tr_mask = ~full.set_index(["hash", "msg_type"]).index.isin(list(zip(te.hash, te.msg_type))); dtr = full[tr_mask]
    for crit in ["what", "why"]:
        H = cm_data.H(d, crit); Htr = cm_data.H(dtr, crit); n, m = H.shape
        p_clim = np.bincount(Htr.ravel(), minlength=K) / Htr.size
        # location-conditional table from train: p(rating | level) — index by the judge's argmax level at test time
        P_by_level = np.stack([(np.bincount(Htr[np.round(np.median(Htr, 1)).astype(int) == l].ravel(), minlength=K) + 1) for l in LV]).astype(float)
        P_by_level /= P_by_level.sum(1, keepdims=True)
        models = {}
        for run in runs:
            P = np.load(f"results/{run}/P_{crit}.npy"); models[run] = P
        # nulls built from the pooled-SFT judge if present, else zero-shot
        base_key = "ce_median_s0" if "ce_median_s0" in models else runs[0]
        models["N1 temp+mix(" + base_key + ")"] = None   # filled per rater below (needs y) -> use cross-fitted on mean over raters: fit on rater-pooled targets
        models["N2 loc-cond(" + base_key + ")"] = P_by_level[models[base_key].argmax(1)]
        models["N3 climatology"] = np.tile(p_clim, (n, 1))
        # per-rater scoring
        per = {}; strata_r = []
        for r in range(m):
            y = H[:, r]; others = np.delete(H, r, 1); st = E.strata_generic(others) if hasattr(E, "strata_generic") else None
            # strata from 5 raters: use Range rule (High=0, Partial=1, Low>=2) to mirror the 6-rater rule
            rngv = others.max(1) - others.min(1); st = np.where(rngv == 0, "High", np.where(rngv == 1, "Partial", "Low")); strata_r.append(st)
            panel = np.stack([np.bincount(o, minlength=K) / (m - 1) for o in others])
            for k, P in models.items():
                if P is None:
                    Pk = temp_mix(models[base_key], y, p_clim, seed=seed + r)
                else: Pk = P
                per.setdefault(k, {"rps": [], "nll": [], "st": []})
                per[k]["rps"].append(rps(Pk, y)); per[k]["nll"].append(nll(Pk, y)); per[k]["st"].append(st)
            per.setdefault("panel(5 raters)", {"rps": [], "nll": [], "st": []})
            per["panel(5 raters)"]["rps"].append(rps(panel, y)); per["panel(5 raters)"]["nll"].append(nll((panel + 1e-3) / (1 + K * 1e-3), y)); per["panel(5 raters)"]["st"].append(st)
        # aggregate: item x rater arrays
        res = {}
        for k, v in per.items():
            R = np.stack(v["rps"], 1); N = np.stack(v["nll"], 1); S = np.stack(v["st"], 1)
            res[k] = {"RPS": float(R.mean()), "NLL": float(N.mean()), **{s: float(R[S == s].mean()) for s in ["High", "Partial", "Low"]}}
        Rc, Rp = res["N3 climatology"]["RPS"], res["panel(5 raters)"]["RPS"]
        for k in res: res[k]["skill"] = float(1 - (res[k]["RPS"] - Rp) / (Rc - Rp))
        # paired item bootstrap for key contrasts
        def contrast(a, b, stratum=None):
            Ra = np.stack(per[a]["rps"], 1); Rb = np.stack(per[b]["rps"], 1); S = np.stack(per[a]["st"], 1)
            if stratum: Ra = np.where(S == stratum, Ra, np.nan); Rb = np.where(S == stratum, Rb, np.nan)
            diff = np.nanmean(Ra - Rb, 1); diff = diff[~np.isnan(diff)]
            boots = [diff[rng.randint(0, len(diff), len(diff))].mean() for _ in range(B)]
            return [float(diff.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
        contrasts = {}
        if "ce_median_s0" in models and "kl_soft_s0" in models:
            n1 = "N1 temp+mix(ce_median_s0)"
            contrasts["ce_median − kl_soft (total gain)"] = contrast("ce_median_s0", "kl_soft_s0")
            contrasts["ce_median − N1 (gain reproduced by item-independent smoother)"] = contrast("ce_median_s0", n1)
            contrasts["N1 − kl_soft (item-specific residual)"] = contrast(n1, "kl_soft_s0")
            contrasts["N1 − kl_soft, Low stratum"] = contrast(n1, "kl_soft_s0", "Low")
            tot = contrasts["ce_median − kl_soft (total gain)"][0]; rep = contrasts["ce_median − N1 (gain reproduced by item-independent smoother)"][0]
            res["smoothing_share"] = float(rep / tot) if abs(tot) > 1e-9 else float("nan")
        if "kl_soft_permuted_s0" in models and "kl_soft_s0" in models:
            contrasts["permuted − true kl_soft (placebo gap)"] = contrast("kl_soft_permuted_s0", "kl_soft_s0")
            contrasts["permuted − true kl_soft, Low"] = contrast("kl_soft_permuted_s0", "kl_soft_s0", "Low")
        # location-controlled entropy -> Low AUROC (strata from all 6 raters for this diagnostic)
        st6 = E.strata(H); low = st6 == "Low"; ent_res = {}
        for k, P in models.items():
            if P is None: continue
            ent = E.entropy(P); lvl = P.argmax(1); X = np.eye(K)[lvl]; resid = ent - X @ np.linalg.lstsq(X, ent, rcond=None)[0]
            ent_res[k] = {"raw": E.auroc(ent, low), "level_adjusted": E.auroc(resid, low)}
        res["entropy_to_Low_AUROC"] = ent_res; res["contrasts"] = contrasts
        report[crit] = res
        print(f"\n[{crit}]  {'model':38s} {'RPS':>6s} {'High':>6s} {'Part':>6s} {'Low':>6s} {'NLL':>6s} {'skill':>6s} | ent→Low raw/adj")
        for k, v in res.items():
            if k in ("smoothing_share", "entropy_to_Low_AUROC", "contrasts"): continue
            e = ent_res.get(k, {}); print(f"   {k:38s} {v['RPS']:6.3f} {v['High']:6.3f} {v['Partial']:6.3f} {v['Low']:6.3f} {v['NLL']:6.3f} {v['skill']:6.3f} | {e.get('raw', float('nan')):.3f}/{e.get('level_adjusted', float('nan')):.3f}")
        for k, v in contrasts.items(): print(f"   Δ {k}: {v[0]:+.4f} CI[{v[1]:+.4f},{v[2]:+.4f}]")
        if "smoothing_share" in res: print(f"   smoothing share = {res['smoothing_share']:.2f}")
    json.dump(report, open("results/pilot_a_report.json", "w"), indent=1, default=float)

if __name__ == "__main__":
    analyse(sys.argv[1:])
