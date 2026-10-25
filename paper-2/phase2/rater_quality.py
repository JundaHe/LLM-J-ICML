"""
rater_quality — RATER_QUALITY_PROTOCOL.md Q2 on DICES-350: can inattentive raters be identified, and does an LLM judge (zero-shot Qwen2.5-7B score distribution Q0,
features/dices/*.npz) add information beyond human-only agreement? Labelled positives = the 19 raters the DICES authors removed (data_panels.DICES_REMOVED).
Scores per rater r (over the items r rated; DICES-350 is fully crossed):
  H       1 − |y_r − median(others)| / (K − 1)                       human-only leave-one-rater-out agreement
  L       1 − |y_r − argmax Q0| / (K − 1);  L_lp = mean log Q0[y_r]  judge-only agreement (two variants)
  *_high  the same restricted to high-consensus items (others' modal share ≥ 0.8)
  RA      rank-average of H_high and L_high
Evaluation: AUROC flagged-vs-retained with a rater bootstrap (B = 2,000); partial AUROC at FPR ≤ 10 %; synthetic-rater positive control (S = 10 uniform random raters, 200 replicates);
bias check: among retained raters, Pearson r between L and the signed lean toward the judge's answer relative to the panel median.
Usage: python rater_quality.py [--B 2000]
"""
import sys, os, json, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--S", type=int, default=10); ap.add_argument("--reps_syn", type=int, default=200); ap.add_argument("--thr", type=float, default=0.8); args = ap.parse_args()

PAN = data_panels.load("dices_raw"); H = PAN["H"].astype(int); K = PAN["K"]; NI, NR = H.shape; raters = PAN["rater_ids"].astype(str)
flag = np.array([r in data_panels.DICES_REMOVED for r in raters]); assert flag.sum() == 19, flag.sum()
F = np.load(f"{HERE}/features/dices/Qwen2.5-7B-Instruct.npz", allow_pickle=True); Q0 = F["Q0"].astype(float); assert Q0.shape == (NI, K)
P104 = data_panels.load("dices"); assert np.array_equal(np.asarray(P104["item_ids"]).astype(str), F["item_ids"].astype(str)), "Q0 rows not aligned with DICES items"
jmode = Q0.argmax(1); logQ = np.log(np.clip(Q0, 1e-9, 1))

def scores_for(Hm, idx_r, thr):
    """per-rater scores for the raters in idx_r of the rating matrix Hm (items x raters); others = all other raters in Hm"""
    out = {k: np.zeros(len(idx_r)) for k in ("H", "L", "L_lp", "H_high", "L_high", "n_high", "lean")}
    for t, r in enumerate(idx_r):
        y = Hm[:, r]; oth = np.delete(Hm, r, axis=1); med = np.median(oth, 1); share = np.array([np.bincount(row, minlength=K).max() for row in oth]) / oth.shape[1]; hi = share >= thr
        dH = 1 - np.abs(y - med) / (K - 1); dL = 1 - np.abs(y - jmode) / (K - 1)
        out["H"][t] = dH.mean(); out["L"][t] = dL.mean(); out["L_lp"][t] = logQ[np.arange(NI), y].mean(); out["n_high"][t] = hi.sum()
        out["H_high"][t] = dH[hi].mean() if hi.any() else np.nan; out["L_high"][t] = dL[hi].mean() if hi.any() else np.nan
        out["lean"][t] = (np.sign(jmode - med) * (y - med) / (K - 1)).mean()            # > 0: the rater deviates from the panel toward the judge's answer
    return out
def rank_avg(a, b):
    from scipy.stats import rankdata
    return (rankdata(np.nan_to_num(a, nan=np.nanmin(a))) + rankdata(np.nan_to_num(b, nan=np.nanmin(b)))) / 2
def auroc(score, pos, max_fpr=None):
    """AUROC of 'low score ⇒ positive' (flagged raters should score LOW); partial AUROC normalised to [0,1] if max_fpr given"""
    s = -np.asarray(score, float); pos = np.asarray(pos, bool)
    if pos.sum() == 0 or (~pos).sum() == 0: return np.nan
    P, N = s[pos], s[~pos]
    if max_fpr is None: return float(np.mean([(p > N).mean() + 0.5 * (p == N).mean() for p in P]))
    thr_n = np.quantile(N, 1 - max_fpr); tpr = np.mean(P > thr_n); return float(tpr)        # TPR at the FPR = max_fpr operating point

S = scores_for(H, np.arange(NR), args.thr); S["RA"] = rank_avg(S["H_high"], S["L_high"])
KEYS = ("H", "L", "L_lp", "H_high", "L_high", "RA")
pt = {k: auroc(S[k], flag) for k in KEYS}; pt10 = {k: auroc(S[k], flag, 0.10) for k in KEYS}
rng = np.random.RandomState(7); bs = {k: [] for k in KEYS}; bsd = []
for b in range(args.B):
    idx = rng.randint(0, NR, NR)
    for k in KEYS: bs[k].append(auroc(S[k][idx], flag[idx]))
    bsd.append(auroc(S["RA"][idx], flag[idx]) - auroc(S["H_high"][idx], flag[idx]))
def ci(v): v = [x for x in v if x == x]; return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
# synthetic positive control
syn = {k: [] for k in KEYS}; srng = np.random.RandomState(11); keep104 = np.where(~flag)[0]
for rep in range(args.reps_syn):
    Hs = np.concatenate([H[:, keep104], srng.randint(0, K, (NI, args.S))], 1); lab = np.r_[np.zeros(len(keep104), bool), np.ones(args.S, bool)]
    Ss = scores_for(Hs, np.arange(Hs.shape[1]), args.thr); Ss["RA"] = rank_avg(Ss["H_high"], Ss["L_high"])
    for k in KEYS: syn[k].append(auroc(Ss[k], lab))
# bias check among retained raters
ret = ~flag; r_bias = float(np.corrcoef(S["L"][ret], S["lean"][ret])[0, 1]); r_bias_high = float(np.corrcoef(np.nan_to_num(S["L_high"][ret]), S["lean"][ret])[0, 1])
res = dict(panel="dices_raw", n_raters=int(NR), n_flagged=int(flag.sum()), n_items=int(NI), thr_high=args.thr, mean_n_high=float(S["n_high"].mean()),
           auroc=pt, auroc_ci95={k: ci(v) for k, v in bs.items()}, tpr_at_fpr10=pt10, delta_RA_minus_Hhigh=dict(est=pt["RA"] - pt["H_high"], ci95=ci(bsd)),
           synthetic_auroc={k: dict(mean=float(np.nanmean(v)), ci95=ci(v)) for k, v in syn.items()}, bias_check=dict(pearson_L_vs_lean_retained=r_bias, pearson_Lhigh_vs_lean_retained=r_bias_high),
           flagged_scores={k: [float(x) for x in S[k][flag]] for k in ("H", "L", "H_high", "L_high")}, retained_mean={k: float(np.nanmean(S[k][ret])) for k in ("H", "L", "H_high", "L_high")}, flagged_mean={k: float(np.nanmean(S[k][flag])) for k in ("H", "L", "H_high", "L_high")},
           protocol="RATER_QUALITY_PROTOCOL.md Q2")
print(f"DICES-350: {NR} raters, {flag.sum()} flagged; high-consensus items per rater (others' modal share ≥ {args.thr}): {S['n_high'].mean():.0f}/{NI}")
for k in KEYS: print(f"  AUROC {k:7s} {pt[k]:.3f} [{res['auroc_ci95'][k][0]:.3f},{res['auroc_ci95'][k][1]:.3f}]   TPR@FPR10 {pt10[k]:.2f}   synthetic AUROC {res['synthetic_auroc'][k]['mean']:.3f}")
print(f"  RA − H_high: {res['delta_RA_minus_Hhigh']['est']:+.3f} {res['delta_RA_minus_Hhigh']['ci95']}")
print(f"  means flagged vs retained: " + ", ".join(f"{k} {res['flagged_mean'][k]:.3f}/{res['retained_mean'][k]:.3f}" for k in ("H", "L", "H_high", "L_high")))
print(f"  bias check (retained): r(L, lean toward judge) = {r_bias:+.3f}; r(L_high, lean) = {r_bias_high:+.3f}")
os.makedirs(f"{HERE}/results/rater_quality", exist_ok=True); json.dump(res, open(f"{HERE}/results/rater_quality/dices.json", "w"), indent=1, default=float)
