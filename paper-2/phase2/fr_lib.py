"""
fr_lib — shared finite-rater primitives, lifted verbatim (parametrised by K / NOMINAL instead of module globals) from finite_rater.py so that new analyses
(decode_residual.py, shrink_targets.py) use exactly the same splits, scoring rule, exact-T comparator, response-based smoother and bootstrap as T9.
finite_rater.py itself is left untouched (frozen results).
"""
import sys, os, numpy as np
from paths import LLMJ
sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
import targets as tgt
from support_audit import z_label, random_max_matching   # noqa: F401  (random_max_matching re-exported for donor constructions)

BW_GRID = (0.05, 0.1, 0.2, 0.4); LAM_GRID = (0.0, 1.0, 5.0, 20.0)

class Panel:
    """K, NOMINAL and the derived operators for one panel."""
    def __init__(self, K, nominal):
        self.K = K; self.NOMINAL = nominal; self.NRM = 1.0 if nominal else (K - 1)
    def C(self, P): return P if self.NOMINAL else np.cumsum(P, -1)[..., :-1]
    def score(self, P, Y):
        """mean proper score (RPS / Brier) of forecasts P (items x K) against ratings Y (items x b)"""
        out = np.zeros(len(P)); CP = self.C(P); K = self.K
        for j in range(Y.shape[1]): out += ((CP - self.C(np.eye(K)[Y[:, j]])) ** 2).sum(1) / self.NRM
        return out / Y.shape[1]
    def hist(self, Hs): return np.stack([np.bincount(r, minlength=self.K) for r in Hs]) / Hs.shape[1]
    def T_of(self, H1):
        """mode z, location coordinate t (ordinal: mean/(K-1); nominal: modal share), exact-T cell key, exact statistic"""
        if self.NOMINAL:
            h = self.hist(H1); z = h.argmax(1); return z, h.max(1), np.round(h.max(1) * H1.shape[1]).astype(int), h.max(1)
        z = np.array([z_label(r) for r in H1]); return z, H1.mean(1) / (self.K - 1), H1.sum(1), H1.mean(1)
    # ---- comparators
    def smoother(self, z_tr, t_tr, R_tr, z_te, t_te, bw, lam):
        K = self.K; q = np.zeros((len(z_te), K)); glob = R_tr.mean(0)
        for zz in np.unique(z_te):
            te = np.where(z_te == zz)[0]; tr = np.where(z_tr == zz)[0]
            if len(tr) == 0: q[te] = glob; continue
            pi = R_tr[tr].mean(0); W = np.exp(-(t_te[te, None] - t_tr[None, tr]) ** 2 / (2 * bw ** 2))
            q[te] = (W @ R_tr[tr] + lam * pi) / (W.sum(1, keepdims=True) + lam + 1e-12)
        return q
    def fit_q(self, fold, z, t, R2, bw, lam):
        q = np.zeros((len(z), self.K))
        for f in np.unique(fold):
            te = fold == f; q[te] = self.smoother(z[~te], t[~te], R2[~te], z[te], t[te], bw, lam)
        return q
    def select_bw_lam(self, groups, z, t, R2, Y2):
        fi = folds_for(groups, 777, 4); best = None
        for bw in BW_GRID:
            for lam in LAM_GRID:
                q = self.fit_q(fi, z, t, R2, bw, lam); s = self.score(q, Y2).mean()
                if best is None or s < best[0] - 1e-12: best = (s, bw, lam)
        return best[1], best[2]
    def exactT_q(self, fold, z, key, stat, h1):
        """exact-T comparator: other-fold exact-T cell mean of P1 histograms (>= 3 items), else the KL projection of the other-fold mode prototype; reproduces T exactly"""
        K = self.K; q = np.zeros_like(h1); cache = {}
        for f in np.unique(fold):
            oth = fold != f; cells = {}; protos = {}
            for zz in range(K): sel = oth & (z == zz); protos[zz] = h1[sel].mean(0) if sel.any() else np.full(K, 1 / K)
            for i in np.where(oth)[0]: cells.setdefault((int(z[i]), int(key[i])), []).append(i)
            for i in np.where(fold == f)[0]:
                ck = (int(z[i]), int(key[i])); mem = cells.get(ck, [])
                if len(mem) >= 3: q[i] = h1[mem].mean(0); continue
                if (f,) + ck not in cache:
                    base = protos[ck[0]] + 1e-6; base /= base.sum()
                    cache[(f,) + ck] = tgt.nominal_zc(base, ck[0], stat[i]) if self.NOMINAL else tgt.ordinal_mode_mean(base, ck[0], stat[i])
                q[i] = cache[(f,) + ck]
        return q

def folds_for(groups, seed, k=5):
    ug = np.unique(groups); perm = np.random.RandomState(seed).permutation(len(ug)); f = {g: perm[i] % k for i, g in enumerate(ug)}; return np.array([f[g] for g in groups])

def splits(Hm, a, b, rep, loo_pos=None):
    """P1 (a ratings) and P2 (b ratings) for every row of Hm; loo_pos: a = m−1, |P2| = 1, held-out POSITION drawn independently per item (Amendment 2 of FINITE_RATER_PROTOCOL.md)"""
    n = len(Hm)
    if loo_pos is not None:
        rng = np.random.RandomState(700001 + loo_pos); hp = rng.randint(0, Hm.shape[1], n); keep = np.ones(Hm.shape, bool); keep[np.arange(n), hp] = False
        return Hm[keep].reshape(n, Hm.shape[1] - 1), Hm[np.arange(n), hp][:, None]
    rng = np.random.RandomState(100003 * a + rep); perm = np.argsort(rng.rand(n, Hm.shape[1]), 1)
    return np.take_along_axis(Hm, perm[:, :a], 1), np.take_along_axis(Hm, perm[:, a:a + b], 1)

def boot_items(groups, rng):
    ug = np.unique(groups); draw = rng.randint(0, len(ug), len(ug)); idx = []; newg = []
    gi = {g: np.where(groups == g)[0] for g in ug}
    for k, d in enumerate(draw): idx.extend(gi[ug[d]]); newg.extend([k] * len(gi[ug[d]]))
    return np.array(idx), np.array(newg)

def ci(v): v = [x for x in v if x == x]; return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
