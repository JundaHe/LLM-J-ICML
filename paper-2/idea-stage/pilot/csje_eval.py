"""
CSJE / HCA evaluation harness for pilot experiments (reusable).

Inputs
------
H : (n, m) int array of per-annotator ratings (levels 0..K-1 or 1..K, any integer range)
J : (n,) point predictions of a judge            (optional)
P : (n, K) predicted rating distribution          (optional; columns = levels in `levels`)

Outputs
-------
- strata (High/Partial/Low) with the paper's rules: Range for m=6, MA for m=3 and m=9
- per-stratum ordinal Krippendorff alpha of judge vs pooled median, and of a held-out
  human vs the median of the remaining raters (alpha_ref)  -> Delta_match = alpha_ref - alpha_HL
- HCA (precision-weighted, linear distance) with item bootstrap CI, overall + per stratum,
  mirroring commit_message/scripts/rq2_frontier_hca.py
- distribution metrics (if P given): CRPS vs empirical human CDF, held-out-rater NLL,
  entropy-vs-Low-stratum AUROC (does the judge's uncertainty predict human disagreement?)
"""
from __future__ import annotations
import numpy as np


# ----------------------------------------------------------------------------- strata
def strata(H: np.ndarray) -> np.ndarray:
    """Return array of 'High'/'Partial'/'Low' using the paper's panel-specific rules."""
    H = np.asarray(H, float)
    n, m = H.shape
    rng = H.max(1) - H.min(1)
    out = np.empty(n, dtype=object)
    if m == 6:                      # commit messages: Range
        out[rng == 0] = "High"; out[rng == 1] = "Partial"; out[rng >= 2] = "Low"
    else:                           # modal agreement
        ma = np.array([np.max(np.unique(r, return_counts=True)[1]) / m for r in H])
        if m == 3:
            out[ma >= 0.999] = "High"; out[(ma < 0.999) & (ma >= 2 / 3 - 1e-9)] = "Partial"; out[ma < 2 / 3 - 1e-9] = "Low"
        else:                       # nine raters: relaxed thresholds on agreement WITH THE MEDIAN (paper's MA for m=9)
            med = np.median(H, 1); pa = (H == med[:, None]).mean(1)
            out[pa >= 5 / 9 - 1e-9] = "High"; out[(pa < 5 / 9 - 1e-9) & (pa >= 3 / 9 - 1e-9)] = "Partial"; out[pa < 3 / 9 - 1e-9] = "Low"
    return out


# ----------------------------------------------------------------------------- alpha
def kripp_alpha_ordinal(a: np.ndarray, b: np.ndarray) -> float:
    """Ordinal Krippendorff's alpha for two complete raters a, b (n items)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2:
        return np.nan
    vals = np.unique(np.concatenate([a, b]))
    # value counts over all units (2 raters each)
    n_c = {v: float(np.sum(a == v) + np.sum(b == v)) for v in vals}
    N = 2.0 * len(a)
    idx = {v: i for i, v in enumerate(vals)}
    # ordinal metric delta^2 between categories c<k: (sum_{g=c}^{k} n_g - (n_c+n_k)/2)^2
    cum = np.cumsum([n_c[v] for v in vals])
    def delta2(c, k):
        if c == k:
            return 0.0
        i, j = sorted((idx[c], idx[k]))
        s = cum[j] - (cum[i - 1] if i > 0 else 0.0)
        return (s - (n_c[c] + n_c[k]) / 2.0) ** 2
    Do = np.mean([delta2(x, y) for x, y in zip(a, b)])   # two raters: each unit contributes one unordered pair (coincidence form / 2)
    De = 0.0
    for c in vals:
        for k in vals:
            De += n_c[c] * n_c[k] * delta2(c, k)
    De /= N * (N - 1.0)
    return 1.0 - Do / De if De > 0 else np.nan


def pooled_median(H: np.ndarray) -> np.ndarray:
    return np.median(H, axis=1)


def alpha_judge_vs_pool(H, J, mask=None):
    med = pooled_median(H)
    if mask is not None:
        med, J = med[mask], J[mask]
    return kripp_alpha_ordinal(np.round(med * 2) / 2, np.asarray(J, float))


def alpha_ref_heldout(H, mask=None):
    """Held-out human scored vs median of remaining raters, averaged over which rater is held out."""
    H = np.asarray(H, float)
    n, m = H.shape
    vals = []
    for r in range(m):
        rest = np.delete(H, r, axis=1)
        med = np.median(rest, axis=1)
        a, b = H[:, r], med
        if mask is not None:
            a, b = a[mask], b[mask]
        vals.append(kripp_alpha_ordinal(np.round(b * 2) / 2, a))
    return float(np.nanmean(vals))


# ----------------------------------------------------------------------------- HCA
def _hca_parts(H: np.ndarray):
    H = np.asarray(H, float)
    n, m = H.shape
    d = np.abs(H[:, :, None] - H[:, None, :])
    C = d.sum(axis=(1, 2)) / (m * (m - 1))
    vals, counts = np.unique(H.astype(int), return_counts=True)
    p = counts / counts.sum()
    Drnd = np.array([(p * np.abs(vals[:, None] - H[i][None, :]).mean(axis=1)).sum() for i in range(n)])
    W = np.maximum(0.0, Drnd - C)
    return C, Drnd, W


def hca(H, J, B=2000, seed=0, mask=None, P=None, levels=None):
    """HCA of judge J (point) or of a distribution P (expected linear distance). Returns (hca, lo, hi, S)."""
    H = np.asarray(H, float)
    C, Drnd, W = _hca_parts(H)
    if P is not None:
        lv = np.asarray(levels, float)
        D = np.array([(P[i][:, None] * np.abs(lv[:, None] - H[i][None, :])).sum(0).mean() for i in range(len(H))])
    else:
        D = np.abs(H - np.asarray(J, float)[:, None]).mean(axis=1)
    if mask is not None:
        C, Drnd, W, D = C[mask], Drnd[mask], W[mask], D[mask]
    n = len(C)
    den = np.sum(W * (Drnd - C))
    point = 1 - np.sum(W * (D - C)) / den if den > 0 else np.nan
    S = float(np.mean(np.maximum(Drnd - C, 0)) / np.mean(C)) if np.mean(C) > 0 else np.inf
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(B):
        s = rng.choice(n, size=n, replace=True)
        den_s = np.sum(W[s] * (Drnd[s] - C[s]))
        if den_s > 0:
            out.append(1 - np.sum(W[s] * (D[s] - C[s])) / den_s)
    lo, hi = (np.percentile(out, 2.5), np.percentile(out, 97.5)) if out else (np.nan, np.nan)
    return float(point), float(lo), float(hi), S


def hca_heldout_human(H, B=500, seed=0, mask=None):
    """Sanity anchor: average HCA of each rater scored against the others (should be ~1)."""
    H = np.asarray(H, float)
    vals = []
    for r in range(H.shape[1]):
        rest = np.delete(H, r, axis=1)
        vals.append(hca(rest, H[:, r], B=B, seed=seed, mask=mask)[0])
    return float(np.mean(vals))


# ----------------------------------------------------------------------------- distribution metrics
def empirical_dist(H, levels):
    lv = np.asarray(levels)
    return np.stack([(np.asarray(h)[:, None] == lv[None, :]).mean(0) for h in H])


def crps(P, H, levels):
    """Mean CRPS between predicted pmf P and the empirical human pmf (ordinal levels, unit spacing)."""
    Q = empirical_dist(H, levels)
    return float(np.mean(np.sum((np.cumsum(P, 1) - np.cumsum(Q, 1)) ** 2, 1)))


def heldout_nll(P, H, levels, eps=1e-6):
    """Mean negative log-likelihood of every individual human rating under P."""
    lv = list(levels)
    idx = np.vectorize(lambda v: lv.index(int(v)))(np.asarray(H))
    Pc = np.clip(P, eps, 1)
    return float(-np.mean(np.log(np.take_along_axis(Pc, idx, axis=1))))


def entropy(P, eps=1e-12):
    return -np.sum(P * np.log(P + eps), 1)


def auroc(score, y):
    """AUROC of `score` for binary labels y (1 = positive)."""
    score = np.asarray(score, float); y = np.asarray(y).astype(bool)
    pos, neg = score[y], score[~y]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    from scipy.stats import rankdata
    ranks = rankdata(np.concatenate([pos, neg]))            # average ranks: ties count 1/2 (constant predictor -> 0.5)
    return float((ranks[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def disagreement_auroc(P, H):
    """Does predicted entropy separate Low-consensus items from High-consensus ones?"""
    st = strata(H)
    return auroc(entropy(P), st == "Low")


# ----------------------------------------------------------------------------- report
def full_report(H, J=None, P=None, levels=None, B=1000, name="judge"):
    H = np.asarray(H, float)
    st = strata(H)
    if J is None and P is not None:
        J = np.asarray(levels)[np.argmax(P, 1)]
    rep = {"name": name, "n": int(len(H)), "strata_share": {s: float(np.mean(st == s)) for s in ["High", "Partial", "Low"]}}
    rep["overall"] = {"alpha_HL": alpha_judge_vs_pool(H, J), "alpha_ref": alpha_ref_heldout(H)}
    h, lo, hi, S = hca(H, J, B=B)
    rep["overall"].update(HCA=h, HCA_ci=[lo, hi], S=S)
    if P is not None:
        hd, lod, hid, _ = hca(H, None, B=B, P=P, levels=levels)
        rep["overall"].update(HCA_dist=hd, HCA_dist_ci=[lod, hid], CRPS=crps(P, H, levels),
                              NLL=heldout_nll(P, H, levels), disagree_AUROC=disagreement_auroc(P, H))
    rep["per_stratum"] = {}
    for s in ["High", "Partial", "Low"]:
        mk = st == s
        if mk.sum() < 5:
            continue
        a_hl = alpha_judge_vs_pool(H, J, mk); a_ref = alpha_ref_heldout(H, mk)
        h, lo, hi, S = hca(H, J, B=B, mask=mk)
        rep["per_stratum"][s] = {"n": int(mk.sum()), "alpha_HL": a_hl, "alpha_ref": a_ref,
                                 "Delta_match": a_ref - a_hl, "HCA": h, "HCA_ci": [lo, hi], "S": S}
        if P is not None:
            hd, lod, hid, _ = hca(H, None, B=B, mask=mk, P=P, levels=levels)
            rep["per_stratum"][s].update(HCA_dist=hd, CRPS=crps(P[mk], H[mk], levels), NLL=heldout_nll(P[mk], H[mk], levels))
    return rep


if __name__ == "__main__":
    # sanity: commit-message developer pool, held-out human anchor ~ 1; strata shares match paper
    import pandas as pd, json, sys
    df = pd.read_csv("/mnt/hdd2/jundahe/LLM-J/code/commit_message/data/CM-benchmark.csv")
    for pool in ["developer", "generated"]:
        d = df[df.msg_type == pool]
        for c in ["what", "why"]:
            H = d[[f"{c}_{i}" for i in range(1, 7)]].to_numpy(int)
            st = strata(H)
            share = {s: round(float(np.mean(st == s)), 3) for s in ["High", "Partial", "Low"]}
            print(pool, c, "n=", len(H), "strata", share, "held-out-human HCA≈", round(hca_heldout_human(H, B=200), 3),
                  "alpha_ref", round(alpha_ref_heldout(H), 3), "median-judge HCA", round(hca(H, np.round(np.median(H, 1)), B=200)[0], 3))
