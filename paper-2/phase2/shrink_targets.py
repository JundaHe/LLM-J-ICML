"""
shrink_targets — SHRINKAGE_PROTOCOL.md step 1 (annotation side, learner-free; Gate A). CPU only.

Per panel: ratings of every item are split (R repetitions) into P1 (a ratings; the "training" histogram h1) and held-out P2 (|P2| = 1 on small panels, 20 on dense panels).
Every forecast of P2 is built from P1 only and is cross-fitted over 5 outer item folds (PAN groups) wherever it involves other items:
  raw        h1                                                      (λ = 1)
  qT         exact-T comparator (fr_lib.Panel.exactT_q; same mode and mean as h1)        (λ = 0)
  shr        q_T + λ̂ (h1 − q_T) — THE METHOD; λ̂_f = clip(ΣX/ΣM, 0, 1) over other-fold items, where X_i, M_i come from an inner leave-one-rating-out INSIDE P1 of those items
             (r_{−j} = C(h_{−j} − q^in), r_j = C(e_{y_j} − q^in), q^in = exact-T comparator cross-fitted among the other-fold items' (a−1)-rating histograms). Uses P1 only.
  shr_cv     q_T + λ (h1 − q_T), λ ∈ {0, .1, …, 1} chosen on other-fold items' HELD-OUT ratings (ceiling, not a training-time method)
  js, jsp    Hausser–Strimmer James–Stein shrinkage of h1 toward uniform / toward the other-fold mode prototype π_z (closed-form λ_JS from h1 and a alone)
  dir        (a h1 + κ π_z)/(a + κ), κ ∈ {0.5, 1, 2, 4, 8, 16} by other-fold held-out score (ceiling; = the heads' `shrunk` arm)
  ls         (1 − ε) h1 + ε/K, ε ∈ {.02, .05, .1, .2, .3} by other-fold held-out score (ceiling)
  qs, shr_s  response-based smoothed comparator of FINITE_RATER_PROTOCOL.md (needs other-fold items' P2 as responses) and λ̂-shrinkage toward it ("smoothed" variants)
Scores: RPS (ordinal) / Brier (nominal) against P2; per-arm mean score and contrasts vs raw and vs qT.
Bootstrap: B item-cluster replicates re-assign folds, refit comparators, λ̂ and all CV choices, redraw R_boot splits.
Usage: python shrink_targets.py --panel summeval_coherence8 [--a 7] [--R 20] [--B 500] [--R_boot 5] [--R_in 3] [--tag x]
"""
import sys, os, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, boot_items, ci

ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--a", type=int, default=None); ap.add_argument("--b", type=int, default=None)
ap.add_argument("--R", type=int, default=20); ap.add_argument("--B", type=int, default=500); ap.add_argument("--R_boot", type=int, default=5); ap.add_argument("--R_in", type=int, default=3)
ap.add_argument("--no_smooth", action="store_true"); ap.add_argument("--tag", default=""); args = ap.parse_args()

PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; NI, M = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(NI)))
NOMINAL = args.panel.startswith("chaosnli"); P = Panel(K, NOMINAL); C = P.C
DENSE = M >= 60
if args.a is None: args.a = M - 1 if not DENSE else 10
if args.b is None: args.b = 1 if not DENSE else 20
assert args.a + args.b <= M and args.a >= 3
LAM_GRID = np.round(np.arange(0, 1.01, 0.1), 2); KAPPA_GRID = (0.5, 1, 2, 4, 8, 16); EPS_GRID = (0.02, 0.05, 0.1, 0.2, 0.3)

def protos(fold, z, h):
    """other-fold mode prototypes π_z per fold"""
    out = np.zeros_like(h)
    for f in np.unique(fold):
        oth = fold != f
        for zz in range(K):
            sel = oth & (z == zz); pi = h[sel].mean(0) if sel.any() else np.full(K, 1 / K); out[(fold == f) & (z == zz)] = pi
    return out

def js_shrink(h, a, target):
    """Hausser & Strimmer (2009) James–Stein shrinkage intensity toward `target`, per item, clipped to [0, 1]"""
    num = (1 - (h ** 2).sum(1)) / (a - 1); den = ((target - h) ** 2).sum(1); lam = np.where(den > 1e-12, num / np.clip(den, 1e-12, None), 1.0); lam = np.clip(lam, 0, 1)
    return lam[:, None] * target + (1 - lam[:, None]) * h, lam

def lambda_hat_inner(H1_oth, g_oth, rng):
    """From P1 ratings of the other-fold items ONLY (training-time information): inner leave-one-rating-out (R_in draws) with an inner 5-fold exact-T comparator.
    Returns λ̂ = clip(ΣX/ΣM) and, on the same inner held-out ratings, the Dirichlet κ and label-smoothing ε that minimise the inner score (fair, P1-only versions of the tuned baselines)."""
    n, a = H1_oth.shape; sx = sm = 0.0; sk = {k_: 0.0 for k_ in KAPPA_GRID}; se = {e_: 0.0 for e_ in EPS_GRID}
    for r in range(args.R_in):
        hp = rng.randint(0, a, n); keep = np.ones((n, a), bool); keep[np.arange(n), hp] = False
        Hm1 = H1_oth[keep].reshape(n, a - 1); y = H1_oth[np.arange(n), hp][:, None]
        hm1 = P.hist(Hm1); z, t, key, stat = P.T_of(Hm1); fi = folds_for(g_oth, 5000 + r, 5); q = P.exactT_q(fi, z, key, stat, hm1); pin = protos(fi, z, hm1)
        r1 = C(hm1 - q); r2 = C(np.eye(K)[y[:, 0]] - q); sx += (r1 * r2).sum(); sm += (r1 ** 2).sum()
        for k_ in KAPPA_GRID: sk[k_] += P.score(((a - 1) * hm1 + k_ * pin) / (a - 1 + k_), y).sum()
        for e_ in EPS_GRID: se[e_] += P.score((1 - e_) * hm1 + e_ / K, y).sum()
    lam = float(np.clip(sx / sm, 0, 1)) if sm > 1e-12 else 0.0
    return lam, min(sk, key=sk.get), min(se, key=se.get)

def one_rep(Hm, groups, rep, fold_seed, loo_pos=None):
    H1, Y2 = splits(Hm, args.a, args.b, rep, loo_pos); h1 = P.hist(H1); z, t, key, stat = P.T_of(H1); fold = folds_for(groups, fold_seed)
    qT = P.exactT_q(fold, z, key, stat, h1); pi = protos(fold, z, h1); n = len(h1)
    S = {}; S["raw"] = P.score(h1, Y2); S["qT"] = P.score(qT, Y2)
    # tuned ceilings and the method, fold by fold
    shr = np.zeros_like(h1); shr_cv = np.zeros_like(h1); dirq = np.zeros_like(h1); lsq = np.zeros_like(h1); dir_in = np.zeros_like(h1); ls_in = np.zeros_like(h1); lam_hat = {}; lam_cv = {}; kap = {}; eps = {}
    rng = np.random.RandomState(777_001 + rep)
    for f in np.unique(fold):
        te = fold == f; oth = ~te
        lam_hat[int(f)], k_in, e_in = lambda_hat_inner(H1[oth], groups[oth], rng)
        shr[te] = qT[te] + lam_hat[int(f)] * (h1[te] - qT[te])
        dir_in[te] = (args.a * h1[te] + k_in * pi[te]) / (args.a + k_in); ls_in[te] = (1 - e_in) * h1[te] + e_in / K      # P1-only tuned baselines (fair comparison with shr)
        # ceilings: choose on other-fold items' held-out ratings
        best = min(LAM_GRID, key=lambda l: P.score(qT[oth] + l * (h1[oth] - qT[oth]), Y2[oth]).mean()); lam_cv[int(f)] = float(best); shr_cv[te] = qT[te] + best * (h1[te] - qT[te])
        bk = min(KAPPA_GRID, key=lambda k_: P.score((args.a * h1[oth] + k_ * pi[oth]) / (args.a + k_), Y2[oth]).mean()); kap[int(f)] = bk; dirq[te] = (args.a * h1[te] + bk * pi[te]) / (args.a + bk)
        be = min(EPS_GRID, key=lambda e_: P.score((1 - e_) * h1[oth] + e_ / K, Y2[oth]).mean()); eps[int(f)] = be; lsq[te] = (1 - be) * h1[te] + be / K
    S["shr"] = P.score(shr, Y2); S["shr_cv"] = P.score(shr_cv, Y2); S["dir"] = P.score(dirq, Y2); S["ls"] = P.score(lsq, Y2); S["dir_in"] = P.score(dir_in, Y2); S["ls_in"] = P.score(ls_in, Y2)
    jsu, _ = js_shrink(h1, args.a, np.full_like(h1, 1 / K)); jsp, _ = js_shrink(h1, args.a, pi); S["js"] = P.score(jsu, Y2); S["jsp"] = P.score(jsp, Y2)
    out = dict(scores=S, lam_hat=float(np.mean(list(lam_hat.values()))), lam_cv=float(np.mean(list(lam_cv.values()))), kappa=float(np.mean(list(kap.values()))), eps=float(np.mean(list(eps.values()))))
    if not args.no_smooth:
        h2 = P.hist(Y2); bw, lam = P.select_bw_lam(groups, z, t, h2, Y2) if rep == 0 or not hasattr(one_rep, "bwlam") else one_rep.bwlam
        one_rep.bwlam = (bw, lam); qs = P.fit_q(fold, z, t, h2, bw, lam); S["qs"] = P.score(qs, Y2)
        shr_s = np.zeros_like(h1)
        for f in np.unique(fold):
            te = fold == f; shr_s[te] = qs[te] + lam_hat[int(f)] * (h1[te] - qs[te])      # same λ̂ (exact-T inner estimate) applied toward the smoothed comparator
        S["shr_s"] = P.score(shr_s, Y2)
    return out

ARMS = ["raw", "qT", "shr", "shr_cv", "js", "jsp", "dir", "ls", "dir_in", "ls_in"] + ([] if args.no_smooth else ["qs", "shr_s"])
def aggregate(reps):
    sc = {k: float(np.mean([o["scores"][k].mean() for o in reps])) for k in ARMS}
    return dict(score=sc, vs_raw={k: sc[k] - sc["raw"] for k in ARMS}, vs_qT={k: sc[k] - sc["qT"] for k in ARMS},
                lam_hat=float(np.mean([o["lam_hat"] for o in reps])), lam_cv=float(np.mean([o["lam_cv"] for o in reps])), kappa=float(np.mean([o["kappa"] for o in reps])), eps=float(np.mean([o["eps"] for o in reps])))

t0 = time.time(); loo = not DENSE
pos_list = list(range(args.R)) if loo else [None] * args.R
full = aggregate([one_rep(H, G0, r, 1, loo_pos=p) for r, p in enumerate(pos_list)])
print(f"{args.panel} a={args.a} b={args.b} n={NI}  λ̂ {full['lam_hat']:.3f}  λ_cv {full['lam_cv']:.2f}  κ {full['kappa']:.1f}  ε {full['eps']:.2f}  | score raw {full['score']['raw']:.5f}  qT {full['score']['qT']:.5f}  shr {full['score']['shr']:.5f}  "
      f"| vs raw: shr {full['vs_raw']['shr']:+.5f} shr_cv {full['vs_raw']['shr_cv']:+.5f} js {full['vs_raw']['js']:+.5f} jsp {full['vs_raw']['jsp']:+.5f} dir {full['vs_raw']['dir']:+.5f} ls {full['vs_raw']['ls']:+.5f} qT {full['vs_raw']['qT']:+.5f}  [{time.time()-t0:.0f}s]", flush=True)
bs = {("vs_raw", k): [] for k in ARMS}; bs.update({("vs_qT", k): [] for k in ARMS}); bs.update({("lam_hat", ""): []})
brng = np.random.RandomState(2027 + args.a)
for bi in range(args.B):
    idx, ng = boot_items(G0, brng); Hb = H[idx]
    pl = [pos_list[j] for j in brng.choice(len(pos_list), min(args.R_boot, len(pos_list)), replace=False)] if loo else [None] * args.R_boot
    o = aggregate([one_rep(Hb, ng, 10_000 + 37 * bi + r, 1000 + bi, loo_pos=p) for r, p in enumerate(pl)])
    for k in ARMS: bs[("vs_raw", k)].append(o["vs_raw"][k]); bs[("vs_qT", k)].append(o["vs_qT"][k])
    bs[("lam_hat", "")].append(o["lam_hat"])
    if (bi + 1) % 50 == 0: print(f"  boot {bi+1}/{args.B}  shr−raw {np.mean(bs[('vs_raw','shr')]):+.5f} [{ci(bs[('vs_raw','shr')])[0]:+.5f},{ci(bs[('vs_raw','shr')])[1]:+.5f}]  shr−qT {np.mean(bs[('vs_qT','shr')]):+.5f} [{ci(bs[('vs_qT','shr')])[0]:+.5f},{ci(bs[('vs_qT','shr')])[1]:+.5f}]  [{time.time()-t0:.0f}s]", flush=True)
res = dict(panel=args.panel, nominal=NOMINAL, K=K, n_items=int(NI), m=int(M), a=args.a, b=args.b, dense=DENSE, R=args.R, B=args.B, R_boot=args.R_boot, R_in=args.R_in, protocol="SHRINKAGE_PROTOCOL.md step 1",
           arms=ARMS, est=full, ci95=dict(vs_raw={k: ci(bs[("vs_raw", k)]) for k in ARMS}, vs_qT={k: ci(bs[("vs_qT", k)]) for k in ARMS}, lam_hat=ci(bs[("lam_hat", "")])), seconds=round(time.time() - t0, 1))
c = res["ci95"]
print(f"{args.panel} FINAL a={args.a}  λ̂ {full['lam_hat']:.3f} [{c['lam_hat'][0]:.3f},{c['lam_hat'][1]:.3f}]  shr−raw {full['vs_raw']['shr']:+.5f} [{c['vs_raw']['shr'][0]:+.5f},{c['vs_raw']['shr'][1]:+.5f}]  shr−qT {full['vs_qT']['shr']:+.5f} [{c['vs_qT']['shr'][0]:+.5f},{c['vs_qT']['shr'][1]:+.5f}]"
      f"  | baselines vs raw: " + ", ".join(f"{k} {full['vs_raw'][k]:+.5f}" for k in ("shr_cv", "js", "jsp", "dir", "ls", "dir_in", "ls_in")) + f"  [{res['seconds']}s]", flush=True)
os.makedirs(f"{HERE}/results/shrinkage", exist_ok=True)
json.dump(res, open(f"{HERE}/results/shrinkage/{args.panel}_a{args.a}{args.tag}.json", "w"), indent=1, default=float)
