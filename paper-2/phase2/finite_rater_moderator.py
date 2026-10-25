"""
Prospectively specified secondary moderator analysis (FINITE_RATER_PROTOCOL.md, original "Secondary" section + Amendment 1 items 5 and 10). Dense panels only.
Per item and repetition, four disjoint random rating subsets of 10: P0 → shape score B_i; P1 → T (mode, location) for the comparator q;
P2, P3 → δ_i = ⟨C(h2 − q), C(h3 − q)⟩/n, the item's cross-panel agreement of the residual beyond the T-comparator (unbiased for ‖C(p − q)‖²/n).
q: response-based smoother within mode (other-fold items' P2 histograms as responses), (bw, λ) by inner grouped CV (finite_rater.py functions).
B_i: ordinal max_{v−u≥2} 4 h0_u h0_v ; nominal max_{u<v} 4 h0_u h0_v ; standardised within panel.
Model per panel: δ ~ β·B_std + γ1·N̂ (P1 multinomial noise) + γ2·entropy(h0) + fixed effects of the P1 location bin (width 0.1 on the normalised scale).
Primary tests: β pooled by inverse-variance weighting over ordinal panels (DICES-350, DICES-990, BW) and over nominal panels (ChaosNLI MNLI, SNLI).
Point estimate: mean over R = 20 assignments; 95 % CI: B = 500 replicates, each resampling groups and drawing R_boot = 2 new assignments.
Usage: python finite_rater_moderator.py
"""
import os, sys, json, numpy as np
from paths import LLMJ
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
import data_panels
from support_audit import z_label
R, B, R_BOOT, SZ = 20, 500, 2, 10
PANELS = [("dices", False), ("dices990", False), ("bw", False), ("chaosnli_mnli", True), ("chaosnli_snli", True)]
BW_GRID = (0.05, 0.1, 0.2, 0.4); LAM_GRID = (0.0, 1.0, 5.0, 20.0)

def setup(key, nominal):
    PAN = data_panels.load(key); H = PAN["H"].astype(int); K = PAN["K"]; G = np.asarray(PAN.get("groups", np.arange(len(H)))); n_ = 1.0 if nominal else K - 1
    C = (lambda P: P) if nominal else (lambda P: np.cumsum(P, -1)[..., :-1])
    def hist(Hs): return np.stack([np.bincount(r, minlength=K) for r in Hs]) / Hs.shape[1]
    def T_of(H1):
        if nominal: h = hist(H1); return h.argmax(1), h.max(1)
        return np.array([z_label(r) for r in H1]), H1.mean(1) / (K - 1)
    def folds(groups, seed, k):
        ug = np.unique(groups); perm = np.random.RandomState(seed).permutation(len(ug)); f = {g: perm[i] % k for i, g in enumerate(ug)}; return np.array([f[g] for g in groups])
    def smoother(z_tr, t_tr, R_tr, z_te, t_te, bw, lam):
        q = np.zeros((len(z_te), K)); glob = R_tr.mean(0)
        for zz in np.unique(z_te):
            te = np.where(z_te == zz)[0]; tr = np.where(z_tr == zz)[0]
            if len(tr) == 0: q[te] = glob; continue
            W = np.exp(-(t_te[te, None] - t_tr[None, tr]) ** 2 / (2 * bw ** 2)); q[te] = (W @ R_tr[tr] + lam * R_tr[tr].mean(0)) / (W.sum(1, keepdims=True) + lam + 1e-12)
        return q
    def fit_q(fold, z, t, R2, bw, lam):
        q = np.zeros((len(z), K))
        for f in np.unique(fold): te = fold == f; q[te] = smoother(z[~te], t[~te], R2[~te], z[te], t[te], bw, lam)
        return q
    def score(P, Y):
        out = np.zeros(len(P)); CP = C(P)
        for j in range(Y.shape[1]): out += ((CP - C(np.eye(K)[Y[:, j]])) ** 2).sum(1) / n_
        return out / Y.shape[1]
    def bimod(h0):
        best = np.zeros(len(h0))
        for u in range(K):
            for v in range(u + (1 if nominal else 2), K): best = np.maximum(best, 4 * h0[:, u] * h0[:, v])
        return best
    def assign(Hm, seed):
        rng = np.random.RandomState(seed); perm = np.argsort(rng.rand(*Hm.shape), 1); parts = [np.take_along_axis(Hm, perm[:, k * SZ:(k + 1) * SZ], 1) for k in range(4)]; return parts
    def items(Hm, groups, seed, bw, lam):
        P0, P1, P2, P3 = assign(Hm, seed); h0, h1, h2, h3 = hist(P0), hist(P1), hist(P2), hist(P3); z, t = T_of(P1)
        q = fit_q(folds(groups, seed + 1, 5), z, t, h2, bw, lam)
        delta = (C(h2 - q) * C(h3 - q)).sum(1) / n_; F = C(h1); Nhat = (F * (1 - F)).sum(1) / ((SZ - 1) * n_)
        ent0 = -(h0 * np.log(h0 + 1e-12)).sum(1); Bs = bimod(h0); Bs = (Bs - Bs.mean()) / (Bs.std() + 1e-12); loc = np.floor(t / 0.1).astype(int)
        return delta, Bs, Nhat, ent0, loc, bimod(h0)
    # (bw, λ) once, by inner grouped CV on assignment 0
    P0, P1, P2, P3 = assign(H, 0); z, t = T_of(P1); h2 = hist(P2); fi = folds(G, 777, 4); best = None
    for bw in BW_GRID:
        for lam in LAM_GRID:
            s = score(fit_q(fi, z, t, h2, bw, lam), P2).mean()
            if best is None or s < best[0] - 1e-12: best = (s, bw, lam)
    return H, G, items, best[1], best[2]

def beta(delta, Bs, Nhat, ent0, loc):
    locs = np.unique(loc); FE = (loc[:, None] == locs[None, 1:]).astype(float)
    X = np.column_stack([np.ones(len(delta)), Bs, Nhat, ent0, FE]); coef, *_ = np.linalg.lstsq(X, delta, rcond=None); return float(coef[1])

out = {}
for key, nominal in PANELS:
    H, G, items, bw, lam = setup(key, nominal)
    pts, tert = [], []
    for r in range(R):
        d, Bs, Nh, e0, loc, braw = items(H, G, 1000 + r, bw, lam); pts.append(beta(d, Bs, Nh, e0, loc))
        cut = np.quantile(Bs, [1 / 3, 2 / 3]); tert.append([float(d[Bs <= cut[0]].mean()), float(d[(Bs > cut[0]) & (Bs <= cut[1])].mean()), float(d[Bs > cut[1]].mean())])
    rng = np.random.RandomState(5); ug = np.unique(G); gi = {g: np.where(G == g)[0] for g in ug}; bs = []
    for bi in range(B):
        draw = rng.randint(0, len(ug), len(ug)); idx = np.concatenate([gi[ug[k]] for k in draw]); ng = np.concatenate([[j] * len(gi[ug[k]]) for j, k in enumerate(draw)])
        bs.append(np.mean([beta(*items(H[idx], ng, 50_000 + 7 * bi + r, bw, lam)[:5]) for r in range(R_BOOT)]))
    est = float(np.mean(pts)); lo, hi = np.percentile(bs, [2.5, 97.5]); se = float(np.std(bs))
    out[key] = dict(nominal=nominal, beta=est, ci95=[float(lo), float(hi)], se=se, bw=bw, lam=lam, delta_by_B_tertile=np.mean(tert, 0).tolist())
    print(f"{key:15s} β(B_std) = {est:+.5f} [{lo:+.5f}, {hi:+.5f}]  δ by B tertile (low/mid/high) {np.round(np.mean(tert, 0), 5).tolist()}", flush=True)
for name, keys in (("ordinal", ["dices", "dices990", "bw"]), ("nominal", ["chaosnli_mnli", "chaosnli_snli"])):
    w = np.array([1 / out[k]["se"] ** 2 for k in keys]); b = np.array([out[k]["beta"] for k in keys]); pooled = float((w * b).sum() / w.sum()); se = float(1 / np.sqrt(w.sum()))
    out[f"pooled_{name}"] = dict(beta=pooled, se=se, ci95=[pooled - 1.96 * se, pooled + 1.96 * se], panels=keys)
    print(f"POOLED {name}: β = {pooled:+.5f} [{pooled - 1.96 * se:+.5f}, {pooled + 1.96 * se:+.5f}]", flush=True)
json.dump(out, open(f"{HERE}/results/finite_rater/moderator.json", "w"), indent=1)
