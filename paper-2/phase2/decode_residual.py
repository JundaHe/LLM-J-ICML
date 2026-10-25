"""
decode_residual — implements DECODING_PROTOCOL.md (Gate D). CPU only.

Per panel and split repetition r: ratings of every item are split into P1 (a) and P2 (b). With the exact-T comparator q_T of P1 (fr_lib.Panel.exactT_q, cross-fitted over
5 outer item folds), r1 = C(h1 − q_T) and r2 = C(h2 − q_T). A group-cross-fitted multi-output ridge (label-free PCA-256 → fold-wise standardise + PCA-64 → ridge, α by
nested 4-fold grouped CV) predicts r1 from the frozen features; r̂ is scored on r2:
  V  = ⟨r̂, r2⟩/n                 covariance with the independent panel's residual
  G  = (2⟨r̂, r2⟩ − ‖r̂‖²)/n      proper-score gain of q_T + r̂ over q_T on P2 ratings (PRIMARY)
  Gc = same after clipping q_T + C⁻¹r̂ to the simplex (sensitivity)
  negA1x = 2X − M (gain of the raw P1 histogram, r̂ := r1), X, M      reference quantities
  G_perm, V_perm: within-exact-T-cell permutation of the features (null control)
  pos_ctrl: out-of-fold Spearman of ridge-predicted P1 mean (modal share) with the P2 mean (pipeline positive control)
Symmetrised: the roles of P1/P2 are swapped (comparator from P2, decoder fitted on r2', scored on r1') and the two directions averaged.
Bootstrap: item-cluster replicates re-assign folds, refit q_T / PCA / ridge (α fixed per fold at the full-data choice), redraw R_boot splits.
Usage: python decode_residual.py --panel summeval_coherence8 [--a 4] [--R 10] [--B 500] [--R_boot 3] [--d 64] [--feat_key E_last] [--tag x]
"""
import sys, os, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")   # small dense ops: BLAS oversubscription on the shared 32-core node made a 6 s run take > 15 min
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, boot_items, ci

ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--a", type=int, default=None); ap.add_argument("--b", type=int, default=None)
ap.add_argument("--R", type=int, default=10); ap.add_argument("--B", type=int, default=500); ap.add_argument("--R_boot", type=int, default=3)
ap.add_argument("--d", type=int, default=64); ap.add_argument("--d_pre", type=int, default=256); ap.add_argument("--feat_key", default="E_last")
ap.add_argument("--reselect_alpha", action="store_true", help="re-select α inside every bootstrap replicate (sensitivity)")
ap.add_argument("--tag", default=""); args = ap.parse_args()

PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; NI, M = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(NI)))
NOMINAL = args.panel.startswith("chaosnli"); P = Panel(K, NOMINAL); C = P.C; NRM = P.NRM
F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True)
assert np.array_equal(np.asarray(PAN["item_ids"]).astype(str), F["item_ids"].astype(str)), "feature rows not aligned with panel rows"
E = F[args.feat_key].astype(np.float64)
# label-free pre-reduction (uses features only, never ratings)
if args.d_pre > 0 and args.d_pre < E.shape[1]:
    mu0 = E.mean(0); U, S, Vt = np.linalg.svd(E - mu0, full_matrices=False); E = (E - mu0) @ Vt[: args.d_pre].T
ALPHAS = [1e-2, 1e-1, 1, 10, 100, 1000, 1e4, 1e5] if args.d > 0 else [1e-1, 1, 10, 100, 1000, 1e4, 1e5, 1e6]   # Amendment 1: top extended so that "no signal" (r̂ → 0) is representable
if args.a is None: args.a = (M + 1) // 2 if M <= 12 else 20
if args.b is None: args.b = (M - args.a) if M <= 12 else min(20, M - args.a)
assert args.a + args.b <= M

# ------------------------------------------------------------------ ridge with fold-wise PCA
def ridge_fit(X, Y, alpha):
    mx, my = X.mean(0), Y.mean(0); Xc = X - mx; W = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ (Y - my)); return W, mx, my
def ridge_pred(X, W, mx, my): return (X - mx) @ W + my
def project(Xtr, Xte, d):
    """d > 0: centre on the training rows and whitened PCA to d components fitted on training rows only (as probe_mean2; NO per-dimension standardisation — that would
    equalise the variances of the pre-reduced scores and make the component choice arbitrary). d <= 0: standardise all dimensions (full-feature ridge)."""
    mu = Xtr.mean(0)
    if d <= 0 or d >= Xtr.shape[1]:
        sd = Xtr.std(0) + 1e-6; return (Xtr - mu) / sd, (Xte - mu) / sd
    Ztr = Xtr - mu; Zte = Xte - mu
    dd = min(d, len(Ztr) // 4); U, S, Vt = np.linalg.svd(Ztr, full_matrices=False); Wp = Vt[:dd].T / (S[:dd] / np.sqrt(len(Ztr)) + 1e-6)
    return Ztr @ Wp, Zte @ Wp
def select_alpha(X, Y, groups):
    fi = folds_for(groups, 4242, 4); best = None
    for al in ALPHAS:
        err = 0.0
        for f in range(4):
            te = fi == f; Ztr, Zte = project(X[~te], X[te], args.d); W, mx, my = ridge_fit(Ztr, Y[~te], al); err += ((ridge_pred(Zte, W, mx, my) - Y[te]) ** 2).sum()
        if best is None or err < best[0] - 1e-12: best = (err, al)
    return best[1]
def crossfit_predict(X, Y, fold, groups, alphas=None):
    """out-of-fold ridge predictions of Y from X; returns predictions and the α used per fold"""
    Yh = np.zeros_like(Y, dtype=float); used = {}
    for f in np.unique(fold):
        te = fold == f; al = alphas[int(f)] if alphas is not None else select_alpha(X[~te], Y[~te], groups[~te])
        Ztr, Zte = project(X[~te], X[te], args.d); W, mx, my = ridge_fit(Ztr, Y[~te], al); Yh[te] = ridge_pred(Zte, W, mx, my); used[int(f)] = al
    return Yh, used

def within_T_permutation(X, z, key, rng):
    """permute feature rows among items that share the exact-T cell (mode, exact key) of P1; singleton cells unchanged"""
    Xp = X.copy(); cells = {}
    for i in range(len(z)): cells.setdefault((int(z[i]), int(key[i])), []).append(i)
    moved = 0
    for items in cells.values():
        if len(items) < 2: continue
        items = np.array(items); perm = rng.permutation(len(items))
        for _ in range(10):                       # avoid fixed points where possible
            if not np.any(perm == np.arange(len(items))): break
            perm = rng.permutation(len(items))
        Xp[items] = X[items[perm]]; moved += int(np.sum(perm != np.arange(len(items))))
    return Xp, moved / len(z)

def clip_gain(qT, rhat, Y2):
    """sensitivity: score of the clipped/renormalised forecast q_T + C⁻¹ r̂ against P2 ratings, minus score of q_T"""
    if NOMINAL: q = qT + rhat
    else:
        Fh = np.cumsum(qT, 1)[:, :-1] + rhat; Fh = np.clip(Fh, 0, 1); Fh = np.maximum.accumulate(Fh, 1); q = np.diff(np.concatenate([np.zeros((len(Fh), 1)), Fh, np.ones((len(Fh), 1))], 1), axis=1)
    q = np.clip(q, 0, None); q = q / np.clip(q.sum(1, keepdims=True), 1e-12, None)
    return P.score(qT, Y2) - P.score(q, Y2)

def one_direction(X, H1, Y2, groups, fold_seed, rng_perm, alphas=None):
    """fit on the residual of H1 (relative to its own exact-T comparator), score on the ratings Y2"""
    h1 = P.hist(H1); h2 = P.hist(Y2); z, t, key, stat = P.T_of(H1); fold = folds_for(groups, fold_seed)
    qT = P.exactT_q(fold, z, key, stat, h1); r1 = C(h1 - qT); r2 = C(h2 - qT)
    Xi = (r1 * r2).sum(1) / NRM; Mi = (r1 ** 2).sum(1) / NRM
    rhat, used = crossfit_predict(X, r1, fold, groups, alphas)
    V = (rhat * r2).sum(1) / NRM; G = (2 * (rhat * r2).sum(1) - (rhat ** 2).sum(1)) / NRM; Gc = clip_gain(qT, rhat, Y2)
    # positive control: predict the P1 location, score against the P2 location
    loc1 = (H1.mean(1) if not NOMINAL else h1.max(1)); loc2 = (Y2.mean(1) if not NOMINAL else h2.max(1))
    lhat, _ = crossfit_predict(X, loc1[:, None], fold, groups, alphas); pos = float(spearmanr(lhat[:, 0], loc2).correlation)
    # null control: within-T feature permutation
    Xp, frac = within_T_permutation(X, z, key, rng_perm); rp, _ = crossfit_predict(Xp, r1, fold, groups, used)
    Vp = (rp * r2).sum(1) / NRM; Gp = (2 * (rp * r2).sum(1) - (rp ** 2).sum(1)) / NRM
    return dict(G=G, V=V, Gc=Gc, negA1x=2 * Xi - Mi, X=Xi, M=Mi, G_perm=Gp, V_perm=Vp, pos_ctrl=pos, perm_frac=frac), used

def one_rep(X, Hm, groups, rep, fold_seed, alphas=None):
    H1, H2 = splits(Hm, args.a, args.b, rep); rng = np.random.RandomState(900_001 + rep)
    o1, u1 = one_direction(X, H1, H2, groups, fold_seed, rng, None if alphas is None else alphas[0])
    o2, u2 = one_direction(X, H2, H1, groups, fold_seed + 1, rng, None if alphas is None else alphas[1])
    out = {}
    for k in o1:
        out[k] = (o1[k] + o2[k]) / 2 if np.ndim(o1[k]) else float((o1[k] + o2[k]) / 2)
    return out, (u1, u2)

def mean_over(reps):
    return {k: (np.mean([o[k] for o in reps], 0) if np.ndim(reps[0][k]) else float(np.mean([o[k] for o in reps]))) for k in reps[0]}

t0 = time.time()
# ---- point estimate: R splits, α selected per fold by nested CV (rep 0's α reused for the bootstrap unless --reselect_alpha)
reps = []; alphas_rep0 = None
for r in range(args.R):
    o, used = one_rep(E, H, G0, r, 1); reps.append(o)
    if r == 0: alphas_rep0 = used
full = mean_over(reps); pt = {k: float(np.mean(v)) if np.ndim(v) else v for k, v in full.items()}
print(f"{args.panel} a={args.a} b={args.b} d={args.d} key={args.feat_key}  point: G {pt['G']:+.5f}  V {pt['V']:+.5f}  Gc {pt['Gc']:+.5f}  G_perm {pt['G_perm']:+.5f}  negA1x {pt['negA1x']:+.5f}  X {pt['X']:+.5f}  M {pt['M']:.5f}  pos_ctrl {pt['pos_ctrl']:.3f}  perm_frac {pt['perm_frac']:.2f}  α {alphas_rep0}  [{time.time()-t0:.0f}s]", flush=True)

# ---- bootstrap
KEYS = ("G", "V", "Gc", "negA1x", "X", "M", "G_perm", "V_perm", "pos_ctrl"); bs = {k: [] for k in KEYS}
brng = np.random.RandomState(2026 + args.a)
for bi in range(args.B):
    idx, ng = boot_items(G0, brng); Hb = H[idx]; Xb = E[idx]
    o = mean_over([one_rep(Xb, Hb, ng, 10_000 + 37 * bi + r, 1000 + bi, None if args.reselect_alpha else alphas_rep0)[0] for r in range(args.R_boot)])
    for k in KEYS: bs[k].append(float(np.mean(o[k])) if np.ndim(o[k]) else o[k])
    if (bi + 1) % 50 == 0: print(f"  boot {bi+1}/{args.B}  G {np.mean(bs['G']):+.5f} [{ci(bs['G'])[0]:+.5f},{ci(bs['G'])[1]:+.5f}]  [{time.time()-t0:.0f}s]", flush=True)
res = dict(panel=args.panel, nominal=NOMINAL, K=K, n_items=int(NI), m=int(M), a=args.a, b=args.b, R=args.R, B=args.B, R_boot=args.R_boot, d=args.d, d_pre=args.d_pre, feat_key=args.feat_key,
           protocol="DECODING_PROTOCOL.md", alphas=alphas_rep0, est=pt, ci95={k: ci(v) for k, v in bs.items()}, seconds=round(time.time() - t0, 1))
e, c = res["est"], res["ci95"]
print(f"{args.panel} FINAL  G {e['G']:+.5f} [{c['G'][0]:+.5f},{c['G'][1]:+.5f}]  V {e['V']:+.5f} [{c['V'][0]:+.5f},{c['V'][1]:+.5f}]  G_perm {e['G_perm']:+.5f} [{c['G_perm'][0]:+.5f},{c['G_perm'][1]:+.5f}]"
      f"  negA1x {e['negA1x']:+.5f} [{c['negA1x'][0]:+.5f},{c['negA1x'][1]:+.5f}]  pos_ctrl {e['pos_ctrl']:.3f}  [{res['seconds']}s]", flush=True)
os.makedirs(f"{HERE}/results/decoding", exist_ok=True)
json.dump(res, open(f"{HERE}/results/decoding/{args.panel}_d{args.d}_{args.feat_key}{args.tag}.json", "w"), indent=1, default=float)
