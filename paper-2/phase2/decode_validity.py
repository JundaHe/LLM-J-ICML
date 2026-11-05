"""R19-8 (ROUND19_PROTOCOL.md): constraint violations of the decoded forecast q_T + C⁻¹r̂ and the gain of its projection onto q_T's exact mode-and-mean cell.
Reuses decode_residual.py (definitions only, up to the point estimate); clip_gain is replaced by a hook that projects and records. Point estimate only.
Usage: python decode_validity.py --panel summeval_coherence8 --a 4 [--plant 0.6] [--R 10]"""
import sys, os, json, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(f"{HERE}/decode_residual.py").read(); src = src[:src.index("t0 = time.time()\n# ---- point")]
exec(compile(src, "decode_residual.py", "exec"))
STATS = []
def cell_project(qt, Fhat):
    K_ = len(qt); z = int(np.argmax(qt)); cons = [{"type": "eq", "fun": lambda q: q.sum() - 1}]
    if NOMINAL:
        cons += [{"type": "eq", "fun": lambda q: q[z] - qt[z]}, {"type": "ineq", "fun": lambda q: qt[z] - np.delete(q, z)}]
        obj = lambda q: ((q - Fhat) ** 2).sum()
    else:
        mu = (np.arange(K_) * qt).sum(); cons += [{"type": "eq", "fun": lambda q: (np.arange(K_) * q).sum() - mu}, {"type": "ineq", "fun": lambda q: q[z] - np.delete(q, z)}]
        obj = lambda q: ((np.cumsum(q)[:-1] - Fhat) ** 2).sum()
    x0 = np.clip(qt, 1e-6, None); x0 /= x0.sum()
    r = minimize(obj, x0, method="SLSQP", bounds=[(0, 1)] * K_, constraints=cons, options=dict(ftol=1e-14, maxiter=200))
    q = np.clip(r.x, 0, None); return q / q.sum()
def clip_gain(qT, rhat, Y2, record=True):            # hook: called once per direction inside one_direction; R19-8a calls it again on the permuted forecast
    if NOMINAL: q = qT + rhat; Fh = q
    else:
        Fh = np.cumsum(qT, 1)[:, :-1] + rhat; q = np.diff(np.concatenate([np.zeros((len(Fh), 1)), Fh, np.ones((len(Fh), 1))], 1), axis=1)
    z = qT.argmax(1); ar = np.arange(len(q)); neg = (q < -1e-9).any(1)
    if NOMINAL: modev = np.abs(q[ar, z] - qT[ar, z]) > 1e-6; modev |= (q > q[ar, z][:, None] + 1e-6).any(1); dmean = np.zeros(len(q))
    else:
        modev = (q > q[ar, z][:, None] + 1e-9).any(1); dmean = np.abs(q @ np.arange(K) - qT @ np.arange(K))
    bad = neg | modev | (dmean > 1e-9); qs = q.copy()
    for i in np.where(bad)[0]: qs[i] = cell_project(qT[i], Fh[i])
    gp = float(np.mean(P.score(qT, Y2) - P.score(qs, Y2)))
    if record: STATS.append(dict(neg=float(neg.mean()), mode=float(modev.mean()), mean=float((dmean > 1e-6).mean()), any=float(bad.mean()), G_proj=gp))
    return gp
_crossfit = crossfit_predict; _perm = within_T_permutation; LAST = {}
def within_T_permutation(X, z, key, rng):      # R19-8a: remember the permuted features so the permuted forecast can be projected too
    Xp, frac = _perm(X, z, key, rng); LAST["Xp"] = Xp; return Xp, frac
def crossfit_predict(X, Y, fold, groups, alphas):
    out = _crossfit(X, Y, fold, groups, alphas)
    if X is LAST.get("Xp") and "ctx" in LAST:
        qT, Y2 = LAST.pop("ctx"); STATS[-1]["G_proj_perm"] = clip_gain(qT, out[0], Y2, record=False)
    return out
_clip = clip_gain
def clip_gain(qT, rhat, Y2, record=True):
    g = _clip(qT, rhat, Y2, record)
    if record: LAST["ctx"] = (qT, Y2)
    return g
t0 = time.time(); reps = []
for r in range(args.R):
    STATS.clear(); o, _ = one_rep(E, H, G0, r, 1); reps.append(dict(G=float(np.mean(o["G"])), X=float(np.mean(o["X"])), **{k: float(np.mean([s[k] for s in STATS])) for k in STATS[0]}))
pt = {k: float(np.mean([x[k] for x in reps])) for k in reps[0]}; pt["G_over_X"] = pt["G"] / pt["X"] if pt["X"] > 1e-9 else float("nan"); pt["dG_proj"] = pt["G_proj"] - pt["G_proj_perm"]; pt["G_proj_over_X"] = pt["G_proj"] / pt["X"] if pt["X"] > 1e-9 else float("nan"); pt["dG_proj_over_X"] = pt["dG_proj"] / pt["X"] if pt["X"] > 1e-9 else float("nan")
print(f"{args.panel}{args.tag} a={args.a}  G {pt['G']:+.5f}  G_proj {pt['G_proj']:+.5f}  X {pt['X']:+.5f}  G/X {pt['G_over_X']:+.3f}  G_proj/X {pt['G_proj_over_X']:+.3f}  G_proj_perm {pt['G_proj_perm']:+.5f}  dG_proj {pt['dG_proj']:+.5f}  dG_proj/X {pt['dG_proj_over_X']:+.3f}  viol: any {pt['any']:.3f} neg {pt['neg']:.3f} mode {pt['mode']:.3f} mean {pt['mean']:.3f}  [{time.time()-t0:.0f}s]", flush=True)
os.makedirs(f"{HERE}/results/decode_validity", exist_ok=True)
json.dump(dict(panel=args.panel, a=args.a, R=args.R, tag=args.tag, protocol="ROUND19_PROTOCOL.md R19-8", est=pt, reps=reps), open(f"{HERE}/results/decode_validity/{args.panel}{args.tag}.json", "w"), indent=1)
