"""R20-1 (ROUND20_PROTOCOL.md): decoding gain against the other panel's OWN shape, G = G_own + G_cross (q2 = panel 2's exact comparator, same folds),
X_own / X_cross, and the valid-forecast contrasts GP (cell-projected forecast vs q1) and ΔGP = GP − GP_perm; point estimate (R) + paired item-cluster bootstrap (B).
Reuses decode_residual.py (definitions up to the point estimate) and the R19-8 cell projection; hooks: clip_gain (called once per direction), folds_for, permutation.
Usage: python decode_decomp.py --panel summeval_coherence8 --a 4 [--plant 0.6 --plant_seed 0] [--R 10 --B 200 --R_boot 3]"""
import sys, os, json, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(f"{HERE}/decode_residual.py").read(); src = src[:src.index("t0 = time.time()\n# ---- point")]
exec(compile(src, "decode_residual.py", "exec"))
def cell_project(qt, Fhat):          # as decode_validity.py (R19-8)
    K_ = len(qt); z = int(np.argmax(qt)); cons = [{"type": "eq", "fun": lambda q: q.sum() - 1}]
    if NOMINAL:
        cons += [{"type": "eq", "fun": lambda q: q[z] - qt[z]}, {"type": "ineq", "fun": lambda q: qt[z] - np.delete(q, z)}]; obj = lambda q: ((q - Fhat) ** 2).sum()
    else:
        mu = (np.arange(K_) * qt).sum(); cons += [{"type": "eq", "fun": lambda q: (np.arange(K_) * q).sum() - mu}, {"type": "ineq", "fun": lambda q: q[z] - np.delete(q, z)}]
        obj = lambda q: ((np.cumsum(q)[:-1] - Fhat) ** 2).sum()
    x0 = np.clip(qt, 1e-6, None); x0 /= x0.sum()
    r = minimize(obj, x0, method="SLSQP", bounds=[(0, 1)] * K_, constraints=cons, options=dict(ftol=1e-14, maxiter=200))
    q = np.clip(r.x, 0, None); return q / q.sum()
def proj_gain(qT, rhat, Y2):
    if NOMINAL: Fh = qT + rhat; q = Fh.copy()
    else:
        Fh = np.cumsum(qT, 1)[:, :-1] + rhat; q = np.diff(np.concatenate([np.zeros((len(Fh), 1)), Fh, np.ones((len(Fh), 1))], 1), axis=1)
    z = qT.argmax(1); ar = np.arange(len(q)); bad = (q < -1e-9).any(1) | (q > q[ar, z][:, None] + 1e-9).any(1)
    bad |= (np.abs(q[ar, z] - qT[ar, z]) > 1e-9) if NOMINAL else (np.abs(q @ np.arange(K) - qT @ np.arange(K)) > 1e-9)
    for i in np.where(bad)[0]: q[i] = cell_project(qT[i], Fh[i])
    LAST["gp_i"] = P.score(qT, Y2) - P.score(q, Y2); return float(np.mean(LAST["gp_i"]))   # R21-1: keep the per-item vector
STATS = []; LAST = {}
_folds = folds_for
def folds_for(groups, seed, k=5):
    f = _folds(groups, seed, k)
    if k == 5: LAST["fold"] = f
    return f
def parts(qT, rhat, Y2):
    h2 = P.hist(Y2); z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(LAST["fold"], z2, key2, stat2, h2); s2 = C(h2 - q2); d = C(q2 - qT)
    g = (2 * (rhat * s2).sum(1) - (rhat ** 2).sum(1)) / NRM
    return dict(G_own=float(np.mean(g)), G_cross=float(np.mean(2 * (rhat * d).sum(1) / NRM)), s2=s2, d=d, g_i=g, v_i=(rhat * s2).sum(1) / NRM)
def clip_gain(qT, rhat, Y2):             # hook: once per direction, after the residual decoder
    p = parts(qT, rhat, Y2); LAST["ctx"] = (qT, Y2, p["s2"], p["d"])
    STATS.append(dict(G_own=p["G_own"], G_cross=p["G_cross"], GP=proj_gain(qT, rhat, Y2), i_G_own=p["g_i"], i_V_own=p["v_i"], i_GP=LAST["gp_i"])); return 0.0
_perm = within_T_permutation
def within_T_permutation(X, z, key, rng):
    Xp, frac = _perm(X, z, key, rng); LAST["Xp"] = Xp; return Xp, frac
_crossfit = crossfit_predict
def crossfit_predict(X, Y, fold, groups, alphas):
    out = _crossfit(X, Y, fold, groups, alphas)
    if X is LAST.get("Xp") and "ctx" in LAST:
        qT, Y2, s2, d = LAST.pop("ctx"); rp = out[0]
        gp = (2 * (rp * s2).sum(1) - (rp ** 2).sum(1)) / NRM
        STATS[-1].update(GP_perm=proj_gain(qT, rp, Y2), G_own_perm=float(np.mean(gp)), i_GP_perm=LAST["gp_i"], i_G_own_perm=gp)
    return out
_one_direction = one_direction
def one_direction(X, H1, Y2, groups, fold_seed, rng_perm, alphas=None):   # add X_own / X_cross (R19-1) on the same split
    o, u = _one_direction(X, H1, Y2, groups, fold_seed, rng_perm, alphas)
    h1 = P.hist(H1); z, t, key, stat = P.T_of(H1); qT = P.exactT_q(LAST["fold"], z, key, stat, h1); r1 = C(h1 - qT)
    h2 = P.hist(Y2); z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(LAST["fold"], z2, key2, stat2, h2)
    STATS[-1].update(G=float(np.mean(o["G"])), X=float(np.mean(o["X"])), X_own=float(np.mean((r1 * C(h2 - q2)).sum(1) / NRM)), X_cross=float(np.mean((r1 * C(q2 - qT)).sum(1) / NRM)), i_X_own=(r1 * C(h2 - q2)).sum(1) / NRM)
    return o, u
KEYS = ("G", "G_own", "G_cross", "X", "X_own", "X_cross", "GP", "GP_perm", "G_own_perm")
IKEYS = ("G_own", "V_own", "X_own", "GP", "GP_perm", "G_own_perm")
ITEM = []                                   # R21-1: per-item contributions of the point-estimate reps (mean over the two directions)
def rep_stats(X, Hm, groups, rep, fold_seed, alphas, keep_items=False):
    STATS.clear(); _, used = one_rep(X, Hm, groups, rep, fold_seed, alphas)
    if keep_items: ITEM.append({k: np.mean([s["i_" + k] for s in STATS], 0) for k in IKEYS})
    return {k: float(np.mean([s[k] for s in STATS])) for k in KEYS}, used
def clt(groups):
    """R21-1: cluster (item-group) CLT intervals for means and delta-method intervals for ratios, from per-item contributions
    averaged over the R point-estimate reps; the cross-fitted predictions are held fixed, so no item is duplicated."""
    v = {k: np.mean([it[k] for it in ITEM], 0) for k in IKEYS}; v["dGP"] = v["GP"] - v["GP_perm"]; v["G_own_net"] = v["G_own"] - v["G_own_perm"]
    ug, gi = np.unique(groups, return_inverse=True); n = len(groups); G = len(ug)
    def se(u): T = np.bincount(gi, u - u.mean()); return float(np.sqrt(G / (G - 1) * (T ** 2).sum()) / n)
    out = {}
    for k, u in v.items(): m = float(u.mean()); s_ = se(u); out[k] = dict(est=m, se=s_, ci95=[m - 1.96 * s_, m + 1.96 * s_])
    xb = v["X_own"].mean()
    for num in ("G_own", "G_own_net", "dGP"):
        th = v[num].mean() / xb; s_ = se((v[num] - th * v["X_own"]) / xb); out[f"{num}/X_own"] = dict(est=float(th), se=s_, ci95=[th - 1.96 * s_, th + 1.96 * s_])
    return out
def derived(v):
    v = dict(v); v["dGP"] = v["GP"] - v["GP_perm"]
    for num, den in (("G", "X"), ("G_own", "X_own"), ("dGP", "X_own"), ("GP", "X_own")): v[f"{num}/{den}"] = v[num] / v[den] if v[den] > 1e-9 else float("nan")
    return v
t0 = time.time(); reps = []; alphas = None
for r in range(args.R):
    s, used = rep_stats(E, H, G0, r, 1, None, keep_items=True); reps.append(s)
    if r == 0: alphas = used
pt = derived({k: float(np.mean([x[k] for x in reps])) for k in KEYS}); CLT = clt(G0)
print(f"{args.panel}{args.tag} CLT " + "  ".join(f"{k} {d['est']:+.6f} [{d['ci95'][0]:+.6f},{d['ci95'][1]:+.6f}]" for k, d in CLT.items()), flush=True)
print(f"{args.panel}{args.tag} point " + "  ".join(f"{k} {v:+.5f}" for k, v in pt.items()) + f"  [{time.time()-t0:.0f}s]", flush=True)
brng = np.random.RandomState(2026 + args.a); bs = []
for bi in range(args.B):
    idx, ng = boot_items(G0, brng)
    rs = [rep_stats(E[idx], H[idx], ng, 10_000 + 37 * bi + r, 1000 + bi, alphas)[0] for r in range(args.R_boot)]
    bs.append(derived({k: float(np.mean([x[k] for x in rs])) for k in KEYS}))
    if (bi + 1) % 25 == 0: print(f"  boot {bi+1}/{args.B} [{time.time()-t0:.0f}s]", flush=True)
cis = {k: ci([b[k] for b in bs]) for k in pt} if bs else {}
print(f"{args.panel}{args.tag} FINAL " + "  ".join(f"{k} {pt[k]:+.5f} [{cis[k][0]:+.5f},{cis[k][1]:+.5f}]" for k in pt) if bs else "no bootstrap", flush=True)
os.makedirs(f"{HERE}/results/decode_decomp", exist_ok=True)
json.dump(dict(panel=args.panel, a=args.a, b=args.b, R=args.R, B=args.B, R_boot=args.R_boot, tag=args.tag, protocol="ROUND20_PROTOCOL.md R20-1", est=pt, ci95=cis, clt=CLT, boot=bs, seconds=round(time.time() - t0, 1)),
          open(f"{HERE}/results/decode_decomp/{args.panel}{args.tag}.json", "w"), indent=1)
