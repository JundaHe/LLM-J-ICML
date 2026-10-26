"""
Finite-rater annotation-side analysis (A/G/B) — implements FINITE_RATER_PROTOCOL.md incl. Amendment 1. CPU only; no model is trained.

Per panel and P1 size a, over random disjoint splits of each item's rating positions into P1 (a ratings) and P2 (held-out ratings):
  A1  = S(h1) − S(q)       scored on the P2 ratings (S = RPS for ordinal, Brier for nominal); negative ⇔ the raw a-rater histogram beats the T-only comparator
  q   = primary comparator: response-based smoother within mode over the location coordinate (other-fold items' P2 histograms as responses; (bw, λ) by inner grouped CV)
  A1x = same with the secondary exact-T comparator (cell means of other-fold P1 histograms with the KL-projection fallback; reproduces T exactly)
  M, X: r1 = h1 − q, r2 = h2 − q;  M = ‖C r1‖²/n,  X = ⟨C r1, C r2⟩/n;  exact identity A1 = M − 2X;  ρ = X/M
  N   = (1/n) Σ_k F̂(1 − F̂)/(a − 1)  (unbiased multinomial noise of h1);  Δ = N − A1  (error of the T-only comparator)
  A2  = S(d) − S(h1), d = the audit's donor replacement of the P1 histograms (ordinal pmmx / nominal pzc); intention-to-treat over all items (secondary)
Dense panels also give Δ_ref (reference-panel comparator) via --ref.
Bootstrap: B replicates resample groups, re-assign outer folds, refit q with the full-data (bw, λ), redraw R_boot splits (and rematch donors for A2).
Usage: python finite_rater.py --panel chaosnli_mnli [--a 2,3,5] [--R 20] [--B 500] [--a2] [--loo] [--ref]
"""
import sys, os, json, argparse, time, numpy as np
from paths import LLMJ
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
import data_panels, targets as tgt
from support_audit import z_label, random_max_matching
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--a", default=None); ap.add_argument("--b", type=int, default=20)
ap.add_argument("--R", type=int, default=20); ap.add_argument("--B", type=int, default=500); ap.add_argument("--R_boot", type=int, default=5)
ap.add_argument("--a2", action="store_true"); ap.add_argument("--B_a2", type=int, default=200); ap.add_argument("--R_a2", type=int, default=2)
ap.add_argument("--loo", action="store_true", help="a = m-1, |P2| = 1, held-out position drawn independently per item (R repetitions)")
ap.add_argument("--ref", action="store_true", help="dense panels: reference-panel comparator Δ_ref")
ap.add_argument("--tag", default=""); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; NI, M = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(NI)))
NOMINAL = args.panel.startswith("chaosnli"); NRM = 1.0 if NOMINAL else (K - 1)
BW_GRID = (0.05, 0.1, 0.2, 0.4); LAM_GRID = (0.0, 1.0, 5.0, 20.0)

def C(P): return P if NOMINAL else np.cumsum(P, -1)[..., :-1]
def score(P, Y):
    out = np.zeros(len(P)); CP = C(P)
    for j in range(Y.shape[1]): out += ((CP - C(np.eye(K)[Y[:, j]])) ** 2).sum(1) / NRM
    return out / Y.shape[1]
def hist(Hs): return np.stack([np.bincount(r, minlength=K) for r in Hs]) / Hs.shape[1]
def T_of(H1):
    """mode z, location coordinate t (ordinal: mean; nominal: modal share), exact-T cell key, exact statistic"""
    if NOMINAL:
        h = hist(H1); z = h.argmax(1); return z, h.max(1), np.round(h.max(1) * H1.shape[1]).astype(int), h.max(1)
    z = np.array([z_label(r) for r in H1]); return z, H1.mean(1) / (K - 1), H1.sum(1), H1.mean(1)
def folds_for(groups, seed, k=5):
    ug = np.unique(groups); perm = np.random.RandomState(seed).permutation(len(ug)); f = {g: perm[i] % k for i, g in enumerate(ug)}; return np.array([f[g] for g in groups])

def smoother(z_tr, t_tr, R_tr, z_te, t_te, bw, lam):
    """within-mode Gaussian kernel regression of the response histograms R_tr on t, shrunk toward the mode prototype"""
    q = np.zeros((len(z_te), K)); glob = R_tr.mean(0)
    for zz in np.unique(z_te):
        te = np.where(z_te == zz)[0]; tr = np.where(z_tr == zz)[0]
        if len(tr) == 0: q[te] = glob; continue
        pi = R_tr[tr].mean(0); W = np.exp(-(t_te[te, None] - t_tr[None, tr]) ** 2 / (2 * bw ** 2))
        q[te] = (W @ R_tr[tr] + lam * pi) / (W.sum(1, keepdims=True) + lam + 1e-12)
    return q
def fit_q(fold, z, t, R2, bw, lam):
    q = np.zeros((len(z), K))
    for f in np.unique(fold):
        te = fold == f; q[te] = smoother(z[~te], t[~te], R2[~te], z[te], t[te], bw, lam)
    return q
def select_bw_lam(groups, z, t, R2, Y2):
    """inner grouped CV within the data (4 folds), scoring rule vs held-out ratings"""
    fi = folds_for(groups, 777, 4); best = None
    for bw in BW_GRID:
        for lam in LAM_GRID:
            q = fit_q(fi, z, t, R2, bw, lam); s = score(q, Y2).mean()
            if best is None or s < best[0] - 1e-12: best = (s, bw, lam)
    return best[1], best[2]
def exactT_q(fold, z, key, stat, h1):
    """secondary comparator: exact-T cell mean of other-fold P1 histograms (>= 3 items), else the KL projection of the other-fold mode prototype"""
    q = np.zeros_like(h1); cache = {}
    for f in np.unique(fold):
        oth = fold != f; cells = {}; protos = {}
        for zz in range(K): sel = oth & (z == zz); protos[zz] = h1[sel].mean(0) if sel.any() else np.full(K, 1 / K)
        for i in np.where(oth)[0]: cells.setdefault((int(z[i]), int(key[i])), []).append(i)
        for i in np.where(fold == f)[0]:
            ck = (int(z[i]), int(key[i])); mem = cells.get(ck, [])
            if len(mem) >= 3: q[i] = h1[mem].mean(0); continue
            if (f,) + ck not in cache:
                base = protos[ck[0]] + 1e-6; base /= base.sum()
                cache[(f,) + ck] = tgt.nominal_zc(base, ck[0], stat[i]) if NOMINAL else tgt.ordinal_mode_mean(base, ck[0], stat[i])
            q[i] = cache[(f,) + ck]
    return q
def donor(H1, h1, rng):
    if NOMINAL: z = h1.argmax(1); c = h1.max(1); bins = np.floor(c / 0.1).astype(int)
    else: z = np.array([z_label(r) for r in H1]); mu = H1.mean(1); bins = np.floor(mu / 0.1).astype(int)
    cells = {}
    for i in range(len(H1)): cells.setdefault((int(z[i]), int(bins[i])), []).append(i)
    mp = {}
    for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(H1[i], minlength=K)) for i in items], rng))
    d = h1.copy()
    for a_, b_ in mp.items(): d[a_] = tgt.nominal_zc(h1[b_], int(z[a_]), c[a_]) if NOMINAL else tgt.ordinal_mode_mean(h1[b_], int(z[a_]), mu[a_])
    changed = np.zeros(len(H1), bool); changed[list(mp)] = True
    return d, changed

def splits(Hm, a, b, rep, loo_pos=None):
    """returns P1 ratings, P2 ratings for every row of Hm"""
    n = len(Hm)
    if loo_pos is not None:   # a = m − 1, |P2| = 1, the held-out POSITION drawn independently per item (Amendment 2: a common held-out position lets q learn that rater's bias)
        rng = np.random.RandomState(700001 + loo_pos); hp = rng.randint(0, Hm.shape[1], n); keep = np.ones(Hm.shape, bool); keep[np.arange(n), hp] = False
        return Hm[keep].reshape(n, Hm.shape[1] - 1), Hm[np.arange(n), hp][:, None]
    rng = np.random.RandomState(100003 * a + rep); perm = np.argsort(rng.rand(n, Hm.shape[1]), 1)
    return np.take_along_axis(Hm, perm[:, :a], 1), np.take_along_axis(Hm, perm[:, a:a + b], 1)

def one_pass(Hm, groups, a, b, rep, bw, lam, fold_seed, loo_pos=None, with_exact=True, with_a2=False):
    H1, Y2 = splits(Hm, a, b, rep, loo_pos); h1 = hist(H1); h2 = hist(Y2); z, t, key, stat = T_of(H1)
    fold = folds_for(groups, fold_seed); q = fit_q(fold, z, t, h2, bw, lam)
    s1 = score(h1, Y2); sq = score(q, Y2); r1 = C(h1 - q); r2 = C(h2 - q)
    Mi = (r1 ** 2).sum(1) / NRM; Xi = (r1 * r2).sum(1) / NRM
    assert np.allclose(s1 - sq, Mi - 2 * Xi, atol=1e-9), "identity A1 = M − 2X violated"
    F = C(h1); Ni = (F * (1 - F)).sum(1) / ((a - 1) * NRM)
    out = dict(A1=s1 - sq, M=Mi, X=Xi, N=Ni)
    if with_exact:
        qx = exactT_q(fold, z, key, stat, h1); out["A1x"] = s1 - score(qx, Y2)
    if with_a2:
        d, ch = donor(H1, h1, np.random.RandomState(31 * rep + 7)); out["A2"] = score(d, Y2) - s1; out["_changed"] = ch; out["_tv"] = 0.5 * np.abs(d - h1).sum(1)
    return out

def summarise(acc_list):
    keys = [k for k in acc_list[0] if not k.startswith("_")]; return {k: np.mean([o[k] for o in acc_list], 0) for k in keys}

def ref_pass(Hm, groups, rep, bw, lam, fold_seed, nref, nb):
    """reference-panel comparator: T from an independent nref-rating subset; Δ_ref from two further disjoint nb-rating subsets"""
    rng = np.random.RandomState(500009 + rep); perm = np.argsort(rng.rand(len(Hm), Hm.shape[1]), 1)
    Href = np.take_along_axis(Hm, perm[:, :nref], 1); Y2 = np.take_along_axis(Hm, perm[:, nref:nref + nb], 1); Y3 = np.take_along_axis(Hm, perm[:, nref + nb:nref + 2 * nb], 1)
    z, t, _, _ = T_of(Href); h2 = hist(Y2); h3 = hist(Y3); fold = folds_for(groups, fold_seed)
    q = fit_q(fold, z, t, h2, bw, lam)    # responses h2 of OTHER-fold items only
    return (C(h2 - q) * C(h3 - q)).sum(1) / NRM

def boot_items(groups, rng):
    ug = np.unique(groups); draw = rng.randint(0, len(ug), len(ug)); idx = []; newg = []
    gi = {g: np.where(groups == g)[0] for g in ug}
    for k, d in enumerate(draw): idx.extend(gi[ug[d]]); newg.extend([d] * len(gi[ug[d]]))   # copies of the same group keep ONE id → same cross-fitting fold (fix 2026-10-26: distinct ids let copies of a test item sit in training folds)
    return np.array(idx), np.array(newg)

def ci(v): return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]

def run_a(a, b, loo):
    t0 = time.time()
    # (bw, λ) selected once per (panel, a) on split rep 0 of the full data
    H1, Y2 = splits(H, a, b, 0, (0 if loo else None)); z, tt, _, _ = T_of(H1); bw, lam = select_bw_lam(G0, z, tt, hist(Y2), Y2)
    pos_list = list(range(args.R)) if loo else [None] * args.R      # loo: R independent per-item random held-out positions
    full = summarise([one_pass(H, G0, a, b, r, bw, lam, 1, loo_pos=p, with_exact=True) for r, p in enumerate(pos_list)])
    pt = {k: float(v.mean()) for k, v in full.items()}
    brng = np.random.RandomState(2024 + a); bs = {k: [] for k in ("A1", "A1x", "M", "X", "N", "Delta", "rho")}
    for bi in range(args.B):
        idx, ng = boot_items(G0, brng); Hb = H[idx]
        pl = [pos_list[j] for j in brng.choice(len(pos_list), min(args.R_boot, len(pos_list)), replace=False)] if loo else [None] * args.R_boot
        o = summarise([one_pass(Hb, ng, a, b, 10_000 + 37 * bi + r, bw, lam, 1000 + bi, loo_pos=p, with_exact=True) for r, p in enumerate(pl)])
        m = {k: float(v.mean()) for k, v in o.items()}; m["Delta"] = m["N"] - m["A1"]; m["rho"] = m["X"] / m["M"] if m["M"] > 1e-12 else np.nan
        for k in bs: bs[k].append(m[k])
    pt["Delta"] = pt["N"] - pt["A1"]; pt["rho"] = pt["X"] / pt["M"] if pt["M"] > 1e-12 else float("nan")
    row = dict(a=a, b=b, loo=loo, bw=bw, lam=lam, n_splits=len(pos_list), est=pt, ci95={k: ci([x for x in v if x == x]) for k, v in bs.items()})
    row["nu_hat"] = a * (pt["M"] - pt["X"]); row["a_cross_extrap"] = row["nu_hat"] / pt["X"] if pt["X"] > 1e-12 else float("inf")
    if args.a2:
        a2 = [one_pass(H, G0, a, b, r, bw, lam, 1, loo_pos=p, with_exact=False, with_a2=True) for r, p in enumerate(pos_list[: max(args.R_a2 * 2, 4)])]
        itt = float(np.mean([o["A2"].mean() for o in a2])); chg = float(np.mean([o["_changed"].mean() for o in a2]))
        chg_eff = float(np.mean([o["A2"][o["_changed"]].mean() for o in a2 if o["_changed"].any()])); tvc = float(np.mean([o["_tv"][o["_changed"]].mean() for o in a2 if o["_changed"].any()]))
        ba = []
        for bi in range(args.B_a2):
            idx, ng = boot_items(G0, brng); Hb = H[idx]; pl = [pos_list[j] for j in brng.choice(len(pos_list), min(args.R_a2, len(pos_list)), replace=False)] if loo else [None] * args.R_a2
            ba.append(np.mean([one_pass(Hb, ng, a, b, 20_000 + 41 * bi + r, bw, lam, 3000 + bi, loo_pos=p, with_exact=False, with_a2=True)["A2"].mean() for r, p in enumerate(pl)]))
        row["A2"] = dict(itt=itt, itt_ci95=ci(ba), changed_fraction=chg, changed_item_effect=chg_eff, tv_changed=tvc)
    row["seconds"] = round(time.time() - t0, 1)
    e, c = row["est"], row["ci95"]
    print(f"{args.panel} a={a:3d} b={b:2d} bw={bw} λ={lam}  A1 {e['A1']:+.5f} [{c['A1'][0]:+.5f},{c['A1'][1]:+.5f}]  A1x {e['A1x']:+.5f}  M {e['M']:.5f}  X {e['X']:+.5f} [{c['X'][0]:+.5f},{c['X'][1]:+.5f}]"
          f"  ρ {e['rho']:.3f}  N {e['N']:.5f}  Δ {e['Delta']:.5f}" + (f"  A2 itt {row['A2']['itt']:+.5f} chg {row['A2']['changed_fraction']:.2f}" if args.a2 else "") + f"  [{row['seconds']}s]", flush=True)
    return row

res = dict(panel=args.panel, nominal=NOMINAL, K=K, n_items=int(NI), m=int(M), R=args.R, B=args.B, R_boot=args.R_boot, protocol="FINITE_RATER_PROTOCOL.md (amendment 1)", rows=[])
A_LIST = [M - 1] if args.loo else [int(x) for x in (args.a or "2,3,5,8,10,15,20,30,40").split(",") if int(x) + 1 <= M]
for a in A_LIST:
    b = 1 if args.loo else min(args.b, M - a)
    res["rows"].append(run_a(a, b, args.loo))
if args.ref:
    nref, nb = (40, 20) if M >= 80 else (30, 15)
    H1, Y2 = splits(H, nref, nb, 0); z, tt, _, _ = T_of(H1); bw, lam = select_bw_lam(G0, z, tt, hist(Y2), Y2)
    dr = np.mean([ref_pass(H, G0, r, bw, lam, 1, nref, nb) for r in range(args.R)], 0); brng = np.random.RandomState(99); bd = []
    for bi in range(args.B):
        idx, ng = boot_items(G0, brng); bd.append(float(np.mean([ref_pass(H[idx], ng, 30_000 + 13 * bi + r, bw, lam, 5000 + bi, nref, nb).mean() for r in range(args.R_boot)])))
    res["delta_ref"] = dict(nref=nref, nb=nb, bw=bw, lam=lam, est=float(dr.mean()), ci95=ci(bd))
    print(f"{args.panel} Δ_ref (T from {nref} ratings) {dr.mean():+.5f} [{ci(bd)[0]:+.5f},{ci(bd)[1]:+.5f}]", flush=True)
os.makedirs(f"{HERE}/results/finite_rater", exist_ok=True)
json.dump(res, open(f"{HERE}/results/finite_rater/{args.panel}{'_loo' if args.loo else ''}{args.tag}.json", "w"), indent=1, default=float)
