"""
SummEval optimizer/permutation replication block (frozen before inspecting chain7 output — Codex round 8).
Design: panel summeval_coherence8 (train_judge_v3 outputs), split 0, expert folds {0,1,2} (eval_raters 0,1,2 → fold index = evaluator), joint seed realizations
{opt 2000/perm 1000 (results/lora/summeval_coherence8/s0), opt 2001/perm 2501 (s0_seed2001), opt 2002/perm 2502 (s0_seed2502)} × frozen roster {chen, perm, perm_mode}.
Groups: source document (PAN['groups']) — the unit for calibration and test resampling and for the estimator.
Estimands per (seed, fold): RAW primary; COMMON map fitted on the pooled calibration predictions of the three roster arms (equal weight; ties → identity); ARM-specific map.
Estimator: document-mean loss differences → mean over documents → mean over the 3 fixed folds → mean over seeds. Crossed bootstrap over seeds, calibration documents (refit), test documents.
Reports: pooled estimates + 95 % percentile CIs (raw / common / arm / common − raw / arm − raw), seed- and fold-specific estimates, n's, boundary-hit frequencies,
equivalence by the 90 % CI criterion for perm − chen (raw) at ±.001/.002/.003 (post hoc bands; .002 was frozen after SummEval seed-2000 folds were seen).
Joint seed realizations: optimizer and permutation randomness are resampled together and cannot be separated. One item split, one base family.
Usage: ~/miniconda3/envs/skill1/bin/python analysis_block_summeval.py [--B 10000] [--allow_incomplete]
"""
import sys, os, json, argparse, itertools, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=10000); ap.add_argument("--allow_incomplete", action="store_true"); args = ap.parse_args()
PAN = data_panels.load("summeval_coherence8"); H = PAN["H"]; K = PAN["K"]; LV = np.arange(K); G = np.asarray(PAN["groups"])
ROSTER = ["chen", "perm", "perm_mode"]; FOLDS = [0, 1, 2]; SEEDS = [2000, 2001, 2002]; PERM_OF = {2000: 1000, 2001: 2501, 2002: 2502}
ROOT = f"{HERE}/results/lora/summeval_coherence8"
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0): Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
TS = [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]; LAMS = [0, .05, .1, .2, .3, .5]; GRID = sorted([(T, l) for T in TS for l in LAMS], key=lambda g: (abs(np.log(g[0])), g[1]))
def fit_cal(Pc, Hc, p0):
    best = None
    for T, lam in GRID:
        s = np.mean([rps(calib(Pc, T, lam, p0), Hc[:, r]).mean() for r in range(Hc.shape[1])])
        if best is None or s < best[0] - 1e-12: best = (s, T, lam)
    return best[1], best[2]
def path(seed, fold, arm): return f"{ROOT}/s0{'' if seed == 2000 else f'_seed{seed}'}/f{fold}/{arm}"
cells = {}; missing = []
for seed, fold, arm in itertools.product(SEEDS, FOLDS, ROSTER):
    p = path(seed, fold, arm)
    if not os.path.exists(f"{p}/P_test.npy"): missing.append((seed, fold, arm)); continue
    meta = json.load(open(f"{p}/meta.json")); it = pd.read_csv(f"{p}/items_test.csv"); ic = pd.read_csv(f"{p}/items_calib.csv"); Pt = np.load(f"{p}/P_test.npy"); Pc = np.load(f"{p}/P_calib.npy")
    assert meta["evaluator"] == fold and meta["split"] == 0 and meta["arm"] == arm and meta["opt_seed"] == seed, (p, meta.get("evaluator"), meta.get("opt_seed"))
    assert arm == "chen" or meta["perm_seed"] == PERM_OF[seed], (p, meta.get("perm_seed"))
    assert Pt.shape == (len(it), K) and Pc.shape == (len(ic), K) and np.isfinite(Pt).all() and np.isfinite(Pc).all() and np.allclose(Pt.sum(1), 1, atol=1e-4), p
    cells[(seed, fold, arm)] = dict(Pt=Pt, Pc=Pc, it=it.row.to_numpy(), ic=ic.row.to_numpy(), T=meta["targets"])
if missing and not args.allow_incomplete: sys.exit(f"incomplete block: missing {len(missing)} cells, e.g. {missing[:6]}")
present = sorted({(s, f) for (s, f, a) in cells if all((s, f, b) in cells for b in ROSTER)}); seeds_present = sorted({s for s, f in present}); folds_present = sorted({f for s, f in present})
ref = cells[(present[0][0], present[0][1], ROSTER[0])]
for key, c in cells.items(): assert (c["it"] == ref["it"]).all() and (c["ic"] == ref["ic"]).all(), f"item alignment differs in {key}"
IT, IC = ref["it"], ref["ic"]; gt = pd.factorize(G[IT])[0]; gc = pd.factorize(G[IC])[0]; test_groups = [np.where(gt == g)[0] for g in np.unique(gt)]; cal_groups = [np.where(gc == g)[0] for g in np.unique(gc)]
print(f"### SummEval block: seeds={seeds_present} folds={folds_present} roster={ROSTER} | n_test_docs={len(test_groups)} (rows {len(IT)}) n_cal_docs={len(cal_groups)} | B={args.B}")
CONTRASTS = [("perm − chen", "perm", "chen"), ("perm_mode − chen", "perm_mode", "chen"), ("perm_mode − perm", "perm_mode", "perm")]
def gmeans(v, groups): return np.array([v[g].mean() for g in groups])
def cell_losses(s, f, cal_rows, test_rows, tgi):
    T = cells[(s, f, ROSTER[0])]["T"]; Hc = H[IC[cal_rows]][:, T]; p0 = np.bincount(Hc.ravel(), minlength=K) / Hc.size; yt = H[IT[test_rows]][:, f]
    Pc_all = np.concatenate([cells[(s, f, a)]["Pc"][cal_rows] for a in ROSTER]); Hc_all = np.concatenate([Hc for _ in ROSTER]); Tc, lc = fit_cal(Pc_all, Hc_all, p0); out = {}; fitted = {"common": (Tc, lc)}
    for a in ROSTER:
        Pt = cells[(s, f, a)]["Pt"][test_rows]; Pc = cells[(s, f, a)]["Pc"][cal_rows]; Ta, la = fit_cal(Pc, Hc, p0); fitted[a] = (Ta, la)
        out[a] = dict(raw=gmeans(rps(Pt, yt), tgi), common=gmeans(rps(calib(Pt, Tc, lc, p0), yt), tgi), arm=gmeans(rps(calib(Pt, Ta, la, p0), yt), tgi))
    return out, fitted
L0 = {sf: cell_losses(sf[0], sf[1], np.arange(len(IC)), np.arange(len(IT)), test_groups) for sf in present}
def cval(L, a, b, e, seeds): return float(np.mean([np.mean([np.mean(L[(s, f)][0][a][e] - L[(s, f)][0][b][e]) for f in folds_present if (s, f) in L]) for s in seeds]))
est = {(n, e): cval(L0, a, b, e, seeds_present) for n, a, b in CONTRASTS for e in ("raw", "common", "arm")}
per_seed = {(n, e): {s: cval(L0, a, b, e, [s]) for s in seeds_present} for n, a, b in CONTRASTS for e in ("raw", "common", "arm")}
per_fold = {(n, e): {f: float(np.mean([np.mean(L0[(s, f)][0][a][e] - L0[(s, f)][0][b][e]) for s in seeds_present if (s, f) in L0])) for f in folds_present} for n, a, b in CONTRASTS for e in ("raw", "common", "arm")}
rng = np.random.RandomState(0); boot = {k: [] for k in est}; bdiff = {(n, d): [] for n, _, _ in CONTRASTS for d in ("common − raw", "arm − raw")}; hits = {"T_lo": 0, "T_hi": 0, "lam_hi": 0, "n": 0}
for _ in range(args.B):
    sdraw = rng.choice(seeds_present, len(seeds_present), replace=True)
    cg = rng.choice(len(cal_groups), len(cal_groups), replace=True); cal_rows = np.concatenate([cal_groups[g] for g in cg])
    tg = rng.choice(len(test_groups), len(test_groups), replace=True); test_rows = np.concatenate([test_groups[g] for g in tg]); tgi = []; pos = 0
    for g in tg: tgi.append(np.arange(pos, pos + len(test_groups[g]))); pos += len(test_groups[g])
    Lb = {}
    for s in set(sdraw):
        for f in folds_present:
            if (s, f) in L0:
                Lb[(s, f)] = cell_losses(s, f, cal_rows, test_rows, tgi)
                for a, (Ta, la) in Lb[(s, f)][1].items(): hits["n"] += 1; hits["T_lo"] += Ta == TS[0]; hits["T_hi"] += Ta == TS[-1]; hits["lam_hi"] += la == LAMS[-1]
    for n, a, b in CONTRASTS:
        v = {e: cval(Lb, a, b, e, sdraw) for e in ("raw", "common", "arm")}
        for e in v: boot[(n, e)].append(v[e])
        bdiff[(n, "common − raw")].append(v["common"] - v["raw"]); bdiff[(n, "arm − raw")].append(v["arm"] - v["raw"])
def pct(v, q): return float(np.percentile(v, q)) if len(v) else float("nan")
rows = []
for n, a, b in CONTRASTS:
    for e in ("raw", "common", "arm"):
        v = np.array(boot[(n, e)]); rows.append(dict(contrast=n, estimand=e, est=est[(n, e)], lo=pct(v, 2.5), hi=pct(v, 97.5), lo90=pct(v, 5), hi90=pct(v, 95), per_seed=per_seed[(n, e)], per_fold=per_fold[(n, e)]))
        print(f"  {n:18s} {e:7s} {est[(n, e)]:+.4f} [{pct(v, 2.5):+.4f}, {pct(v, 97.5):+.4f}]  seeds {{{', '.join(f'{k}: {x:+.4f}' for k, x in per_seed[(n, e)].items())}}}  folds {{{', '.join(f'{k}: {x:+.4f}' for k, x in per_fold[(n, e)].items())}}}")
    for d in ("common − raw", "arm − raw"):
        v = np.array(bdiff[(n, d)]); rows.append(dict(contrast=n, estimand=d, est=float(np.mean(v)) if len(v) else np.nan, lo=pct(v, 2.5), hi=pct(v, 97.5), lo90=np.nan, hi90=np.nan, per_seed={}, per_fold={}))
        print(f"  {n:18s} {d:13s} {float(np.mean(v)) if len(v) else float('nan'):+.4f} [{pct(v, 2.5):+.4f}, {pct(v, 97.5):+.4f}]")
pc = [r for r in rows if r["contrast"] == "perm − chen" and r["estimand"] == "raw"][0]
print("  equivalence by the 90% CI criterion (post hoc bands), perm − chen raw:", {eps: bool(pc["lo90"] > -eps and pc["hi90"] < eps) for eps in (0.001, 0.002, 0.003)})
print("  boundary hits over refits:", {k: (round(v / max(hits['n'], 1), 3) if k != "n" else v) for k, v in hits.items()}); print("  NOTE: joint seed realizations (optimizer + permutation); one split; one base family.")
json.dump(dict(seeds=seeds_present, folds=folds_present, roster=ROSTER, B=args.B, rows=rows, boundary_hits=hits), open(f"{ROOT}/analysis_block_summeval.json", "w"), indent=1, default=str)
