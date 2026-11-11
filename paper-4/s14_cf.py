"""Stage 14 S14-1 (PROTOCOL_STAGE14.md §1.4): linear collaborative-filtering reference on Jester (rung L0, seen jokes) and two diagnostic learners on held-out jokes
(CF-text: joke means and loadings regressed on text PCs; ISO: per-rater ridge on text PCs with an isotropic prior). Same folds and the same support draws as
factorised_rm.py (rows of jester_raters in loader order). Output: results/stage14_cf.json (per fold, k, draw, rater: concordant-pair counts and denominators)."""
import os, sys, json, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
PAN = data_panels.load("jester_raters"); Y = PAN["H"].reshape(-1).astype(float); ev = [e[0] for e in PAN["evaluators"]]; raters = sorted(set(ev)); rid = {r: j for j, r in enumerate(raters)}
R = np.array([rid[e] for e in ev]); NR = len(raters); us, J = np.unique(np.asarray(PAN["snippet_ids"]), return_inverse=True); NJ = len(us); Ymat = np.full((NR, NJ), np.nan); Ymat[R, J] = Y
F_ = np.load(f"{P2}/features/jester_items/Qwen2.5-7B-Instruct.npz", allow_pickle=True); pos = {s: j for j, s in enumerate(F_["item_ids"].astype(str))}
Eu = F_["E_last"][[pos[s] for s in us.astype(str)]].astype(np.float64); Eu -= Eu.mean(0); U0, S0, _ = np.linalg.svd(Eu, full_matrices=False); XF = U0 * S0
def Xd(xd): x = XF[:, :xd]; return x / x.std(0)
KS = (5, 10, 20, 50); RANKS = (1, 2, 4, 8, 16); LAMS = (0.1, 1, 10, 100, 1000); XDS = (4, 8, 16, 32, 64); TAUS = (0.1, 1, 10, 100, 1000, 10000)
# folds as factorised_rm.py (one rater group; item groups = jokes in np.unique order)
ids = np.arange(NR)[np.random.RandomState(0).permutation(NR)]; rfold = np.zeros(NR, int); rfold[ids] = np.arange(NR) % 5
jfold = np.random.RandomState(0).permutation(NJ) % 5; vj = np.random.RandomState(1).rand(NJ) < 0.15
def cf_fit(rr, jj):
    """joke means, rater-centred residual SVD (missing = 0): loadings scaled so that rater factors have unit variance"""
    M = Ymat[np.ix_(rr, jj)]; mu = np.nanmean(M, 0); E = M - mu; b = np.nanmean(E, 1); E = E - b[:, None]; E[np.isnan(E)] = 0; U_, S_, Vt_ = np.linalg.svd(E, full_matrices=False)
    return mu, Vt_.T * (S_ / np.sqrt(len(rr))), U_ * np.sqrt(len(rr)), b
def solve(A, e, lam):
    """ridge on all columns but the first (intercept)"""
    P = lam * np.eye(A.shape[1]); P[0, 0] = 1e-3; return np.linalg.solve(A.T @ A + P, A.T @ e)
def ridge_map(Xtr, T, lam):
    xm, tm = Xtr.mean(0), T.mean(0); W = np.linalg.solve((Xtr - xm).T @ (Xtr - xm) + lam * np.eye(Xtr.shape[1]), (Xtr - xm).T @ (T - tm)); return lambda Xn: (Xn - xm) @ W + tm
def conc(y, e):
    ui, uj = np.triu_indices(len(y), 1); ok = y[ui] != y[uj]; sg = np.sign(e[ui] - e[uj])[ok] * np.sign(y[ui] - y[uj])[ok]; return float((sg > 0).sum() + 0.5 * (sg == 0).sum()), int(ok.sum())
out = {"protocol": "PROTOCOL_STAGE14.md S14-1 (L0, CF-text, ISO)", "folds": [], "per_rater": []}; t0 = time.time()
for f in range(5):
    tr_r = np.where(rfold != f)[0]; jtr = np.where(jfold != f)[0]; jte = np.where(jfold == f)[0]; jfit = jtr[~vj[jtr]]; jva = jtr[vj[jtr]]; pj = {j: i for i, j in enumerate(jtr)}; pf = {j: i for i, j in enumerate(jfit)}
    idx_ad_pool = np.where((rfold[R] == f) & (jfold[J] != f))[0]; idx_te = np.where((rfold[R] == f) & (jfold[J] == f))[0]; test_raters = np.unique(R[idx_te])
    vr = np.random.RandomState(3 + f).choice(tr_r, len(tr_r) // 5, replace=False); in_r = np.setdiff1d(tr_r, vr)
    mu5, V5, _, _ = cf_fit(in_r, jtr); mu, V, _, _ = cf_fit(tr_r, jtr); muf, Vf, Uf, bf = cf_fit(tr_r, jfit); mu5f = np.nanmean(Ymat[np.ix_(in_r, jfit)], 0); info = {"fold": f, "sel": {}}
    for k in KS:
        # ---- L0: rank and ridge on pseudo-new training raters (squared error on their non-support ratings of training jokes)
        se = np.zeros((len(RANKS), len(LAMS))); cnt = 0
        for dr in range(2):
            rng5 = np.random.RandomState(50_000 + 100 * k + dr)
            for r in vr:
                obs = np.where(~np.isnan(Ymat[r, jtr]))[0]; s = rng5.choice(obs, k, replace=False); q = np.setdiff1d(obs, s); y = Ymat[r, jtr]; cnt += len(q)
                for a, rk in enumerate(RANKS):
                    A = np.c_[np.ones(k), V5[s, :rk]]
                    for b_, lam in enumerate(LAMS): th = solve(A, y[s] - mu5[s], lam); se[a, b_] += ((y[q] - mu5[q] - th[0] - V5[q, :rk] @ th[1:]) ** 2).sum()
        a, b_ = np.unravel_index(se.argmin(), se.shape); rk, lam = RANKS[a], LAMS[b_]
        # ---- CF-text: text dimension and ridge on validation jokes (training raters; loadings of rank rk from the non-validation training jokes)
        best = None
        for xd in XDS:
            X = Xd(xd)
            for lt in LAMS:
                g = ridge_map(X[jfit], np.c_[muf, Vf[:, :rk]], lt)(X[jva]); pred = g[:, 0][None, :] + bf[:, None] + Uf[:, :rk] @ g[:, 1:].T; v = np.nanmean((Ymat[np.ix_(tr_r, jva)] - pred) ** 2)
                if best is None or v < best[0]: best = (float(v), xd, lt)
        _, xd, lt = best; X = Xd(xd); g = ridge_map(X[jtr], np.c_[mu, V[:, :rk]], lt)(X[jte]); mut, Vt_ = g[:, 0], g[:, 1:]
        # ---- ISO: prior strength on pseudo-new training raters (support on non-validation training jokes, scored on validation jokes)
        mu5v = ridge_map(X[jfit], mu5f[:, None], lt)(X[jva])[:, 0]; st = np.zeros(len(TAUS))
        for dr in range(2):
            rng5 = np.random.RandomState(60_000 + 100 * k + dr)
            for r in vr:
                obs = np.where(~np.isnan(Ymat[r, jfit]))[0]; s = rng5.choice(obs, k, replace=False); A = np.c_[np.ones(k), X[jfit[s]]]; yv = Ymat[r, jva]; okv = ~np.isnan(yv)
                for c, tau in enumerate(TAUS): th = solve(A, Ymat[r, jfit[s]] - mu5f[s], tau); st[c] += ((yv - mu5v - th[0] - X[jva] @ th[1:])[okv] ** 2).sum()
        tau = TAUS[int(st.argmin())]; info["sel"][k] = {"rank": rk, "lam": lam, "xd": xd, "lam_text": lt, "tau": tau}
        # ---- test raters: the pipeline's support draws
        for dr in range(5):
            rng = np.random.RandomState(10_000 * f + 100 * k + dr)
            for r in test_raters:
                pool = idx_ad_pool[R[idx_ad_pool] == r]
                if len(pool) < k: continue
                sup = rng.choice(pool, k, replace=False); s = np.array([pj[j] for j in J[sup]]); q = np.array([pj[j] for j in J[np.setdiff1d(pool, sup)]]); y = Ymat[r, jtr]
                th = solve(np.c_[np.ones(k), V[s, :rk]], y[s] - mu[s], lam); c_cf, den_s = conc(y[q], mu[q] + V[q, :rk] @ th[1:]); c_mu, _ = conc(y[q], mu[q])
                okt = ~np.isnan(Ymat[r, jte]); yt = Ymat[r, jte][okt]; c_cft, den_t = conc(yt, (mut + Vt_ @ th[1:])[okt]); c_mut, _ = conc(yt, mut[okt])
                tw = solve(np.c_[np.ones(k), X[jtr[s]]], y[s] - mu[s], tau); c_iso, _ = conc(yt, (mut + X[jte] @ tw[1:])[okt])
                out["per_rater"].append({"fold": f, "k": k, "draw": dr, "rater": int(r), "den_s": den_s, "cf_conc": c_cf, "mu_conc": c_mu, "den_t": den_t, "cft_conc": c_cft, "iso_conc": c_iso, "mut_conc": c_mut})
        print(f"fold {f} k={k} selected {info['sel'][k]} [{time.time()-t0:.0f}s]", flush=True)
    out["folds"].append(info)
json.dump(out, open(f"{HERE}/results/stage14_cf.json", "w")); print("saved", len(out["per_rater"]), "rows")
