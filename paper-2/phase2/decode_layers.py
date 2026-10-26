"""
decode_layers — DECODING_PROTOCOL.md Amendment 2(a): INSPECTOR-style multi-layer probing re-test of Gate D. Same estimands as decode_residual.py (G, V, permutation control, positive
control, symmetrised, group cross-fitting, bootstrap), but the features are the per-layer mean- and last-pooled hidden states (features_layers/<panel>/*.npz, each layer PCA-128,
label-free) and the decoder concatenates the top-K layers chosen GREEDILY by inner-CV MSE on r1 (K ≤ k_max), ridge with nested α. Reports which layers were selected.
Usage: python decode_layers.py --panel summeval_coherence8 [--a 4] [--R 10] [--B 300] [--k_max 4] [--pool mean|last|both]
"""
import sys, os, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, boot_items, ci
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--a", type=int, default=None); ap.add_argument("--b", type=int, default=None)
ap.add_argument("--R", type=int, default=10); ap.add_argument("--B", type=int, default=300); ap.add_argument("--R_boot", type=int, default=3); ap.add_argument("--k_max", type=int, default=4); ap.add_argument("--pool", default="both")
ap.add_argument("--d_layer", type=int, default=32, help="components kept per layer before concatenation"); ap.add_argument("--tag", default=""); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; NI, M = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(NI))); NOMINAL = args.panel.startswith("chaosnli"); P = Panel(K, NOMINAL); C = P.C; NRM = P.NRM
F = np.load(f"{HERE}/features_layers/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); assert np.array_equal(np.asarray(PAN["item_ids"]).astype(str), F["item_ids"].astype(str))
LAY = {}
for l in range(len(F["layers"])):
    if args.pool in ("mean", "both"): LAY[f"mean{l}"] = F["mean"][l, :, : args.d_layer].astype(np.float64)
    if args.pool in ("last", "both"): LAY[f"last{l}"] = F["last"][l, :, : args.d_layer].astype(np.float64)
LAY = {k: v for k, v in LAY.items() if np.isfinite(v).all() and v.std(0).max() > 1e-8}
ALPHAS = [1e-1, 1, 10, 100, 1000, 1e4, 1e5]
if args.a is None: args.a = (M + 1) // 2 if M <= 12 else 20
if args.b is None: args.b = (M - args.a) if M <= 12 else min(20, M - args.a)

def ridge_fit(X, Y, alpha): mx, my = X.mean(0), Y.mean(0); Xc = X - mx; W = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ (Y - my)); return W, mx, my
def ridge_pred(X, W, mx, my): return (X - mx) @ W + my
def std_fit(Xtr, Xte): mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6; return (Xtr - mu) / sd, (Xte - mu) / sd
def cv_mse(X, Y, groups, alpha=None):
    fi = folds_for(groups, 4242, 4); best = None
    for al in ([alpha] if alpha is not None else ALPHAS):
        err = 0.0
        for f in range(4):
            te = fi == f; Ztr, Zte = std_fit(X[~te], X[te]); W, mx, my = ridge_fit(Ztr, Y[~te], al); err += ((ridge_pred(Zte, W, mx, my) - Y[te]) ** 2).sum()
        if best is None or err < best[0]: best = (err, al)
    return best
def greedy_layers(Y, groups, idx_tr):
    """greedy forward selection of layers by inner-CV MSE on r1 (training items of the outer fold only)"""
    chosen, cur = [], None
    for _ in range(args.k_max):
        cand = None
        for name in LAY:
            if name in chosen: continue
            X = np.concatenate([LAY[n][idx_tr] for n in chosen + [name]], 1); err, al = cv_mse(X, Y, groups)
            if cand is None or err < cand[0]: cand = (err, name, al)
        if cur is not None and cand[0] >= cur - 1e-9: break
        cur = cand[0]; chosen.append(cand[1]); alpha = cand[2]
    return chosen, alpha
def crossfit_predict(Y, fold, groups, fixed=None):
    Yh = np.zeros_like(Y, dtype=float); used = {}
    for f in np.unique(fold):
        te = fold == f; tr = ~te
        if fixed is None: chosen, al = greedy_layers(Y[tr], groups[tr], np.where(tr)[0])
        else: chosen, al = fixed[int(f)]
        X = np.concatenate([LAY[n] for n in chosen], 1); Ztr, Zte = std_fit(X[tr], X[te]); W, mx, my = ridge_fit(Ztr, Y[tr], al); Yh[te] = ridge_pred(Zte, W, mx, my); used[int(f)] = (chosen, al)
    return Yh, used
def within_T_perm(z, key, rng):
    perm = np.arange(len(z)); cells = {}
    for i in range(len(z)): cells.setdefault((int(z[i]), int(key[i])), []).append(i)
    for items in cells.values():
        if len(items) > 1: items = np.array(items); perm[items] = items[rng.permutation(len(items))]
    return perm
def one_direction(H1, Y2, groups, fold_seed, rng, fixed=None):
    h1 = P.hist(H1); h2 = P.hist(Y2); z, t, key, stat = P.T_of(H1); fold = folds_for(groups, fold_seed)
    qT = P.exactT_q(fold, z, key, stat, h1); r1 = C(h1 - qT); r2 = C(h2 - qT); Xi = (r1 * r2).sum(1) / NRM; Mi = (r1 ** 2).sum(1) / NRM
    rhat, used = crossfit_predict(r1, fold, groups, fixed); V = (rhat * r2).sum(1) / NRM; G = (2 * (rhat * r2).sum(1) - (rhat ** 2).sum(1)) / NRM
    loc1 = H1.mean(1) if not NOMINAL else h1.max(1); loc2 = Y2.mean(1) if not NOMINAL else h2.max(1); lhat, _ = crossfit_predict(loc1[:, None], fold, groups, used); pos = float(spearmanr(lhat[:, 0], loc2).correlation)
    perm = within_T_perm(z, key, rng); global LAY; LAY_orig = LAY; LAY = {k: v[perm] for k, v in LAY_orig.items()}
    try: rp, _ = crossfit_predict(r1, fold, groups, used)
    finally: LAY = LAY_orig
    Gp = (2 * (rp * r2).sum(1) - (rp ** 2).sum(1)) / NRM
    return dict(G=G.mean(), V=V.mean(), negA1x=(2 * Xi - Mi).mean(), X=Xi.mean(), M=Mi.mean(), G_perm=Gp.mean(), pos_ctrl=pos), used
def one_rep(Hm, groups, rep, fold_seed, fixed=None):
    H1, H2 = splits(Hm, args.a, args.b, rep); rng = np.random.RandomState(900_001 + rep)
    o1, u1 = one_direction(H1, H2, groups, fold_seed, rng, None if fixed is None else fixed[0]); o2, u2 = one_direction(H2, H1, groups, fold_seed + 1, rng, None if fixed is None else fixed[1])
    return {k: (o1[k] + o2[k]) / 2 for k in o1}, (u1, u2)

t0 = time.time(); reps = []; fixed0 = None
for r in range(args.R):
    o, used = one_rep(H, G0, r, 1); reps.append(o)
    if r == 0: fixed0 = used; print(f"  rep0 layers (dir1): {[(f, c) for f, (c, a) in used[0].items()]}", flush=True)
pt = {k: float(np.mean([o[k] for o in reps])) for k in reps[0]}
print(f"{args.panel} layers a={args.a} b={args.b} pool={args.pool} k_max={args.k_max}  point: G {pt['G']:+.5f}  V {pt['V']:+.5f}  G_perm {pt['G_perm']:+.5f}  negA1x {pt['negA1x']:+.5f}  pos_ctrl {pt['pos_ctrl']:.3f}  [{time.time()-t0:.0f}s]", flush=True)
bs = {k: [] for k in pt}; brng = np.random.RandomState(2026 + args.a)
for bi in range(args.B):
    idx, ng = boot_items(G0, brng); Hb = H[idx]; LAY_full = LAY; LAY = {k: v[idx] for k, v in LAY_full.items()}
    try: o = {k: float(np.mean([one_rep(Hb, ng, 10_000 + 37 * bi + r, 1000 + bi, fixed0)[0][k] for r in range(args.R_boot)])) for k in pt}
    finally: LAY = LAY_full
    for k in pt: bs[k].append(o[k])
    if (bi + 1) % 50 == 0: print(f"  boot {bi+1}/{args.B}  G {np.mean(bs['G']):+.5f} [{ci(bs['G'])[0]:+.5f},{ci(bs['G'])[1]:+.5f}]  [{time.time()-t0:.0f}s]", flush=True)
res = dict(panel=args.panel, a=args.a, b=args.b, pool=args.pool, k_max=args.k_max, d_layer=args.d_layer, R=args.R, B=args.B, protocol="DECODING_PROTOCOL.md Amendment 2(a)", layers_rep0={str(f): c for f, (c, a) in fixed0[0].items()}, est=pt, ci95={k: ci(v) for k, v in bs.items()}, seconds=round(time.time() - t0, 1))
print(f"{args.panel} LAYERS FINAL  G {pt['G']:+.5f} [{res['ci95']['G'][0]:+.5f},{res['ci95']['G'][1]:+.5f}]  V {pt['V']:+.5f}  G_perm {pt['G_perm']:+.5f} [{res['ci95']['G_perm'][0]:+.5f},{res['ci95']['G_perm'][1]:+.5f}]  pos_ctrl {pt['pos_ctrl']:.3f}  [{res['seconds']}s]", flush=True)
os.makedirs(f"{HERE}/results/decoding_layers", exist_ok=True); json.dump(res, open(f"{HERE}/results/decoding_layers/{args.panel}{args.tag}.json", "w"), indent=1, default=float)
