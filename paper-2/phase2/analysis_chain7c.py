"""
chain7c commit block analysis (Codex round 10 design) — FIXED donor mapping (perm_seed 1000 for every optimizer seed), so seed-to-seed variation is OPTIMIZER variability
alone; no-adversary bridge arms chen0 / perm_mode0 paired with chen / perm_mode; interaction (perm_mode − chen) − (perm_mode0 − chen0) implicates/exonerates the adversarial term.
Derived from analysis_chain7.py (Codex rounds 5–6 specification), whose text follows. This is ONE outer item split (0) and ONE base family (Qwen2.5-Coder-7B):
call it an "optimizer/permutation replication block", not the overall replication standard.
Design: commit, criterion in {why, what}; optimiser seeds {2000, 2001, 2002} × evaluator folds {0, 1, 2} × the FROZEN roster {hard, chen, perm, perm_mode, sordm}.
Permutation seeds are paired with optimiser seeds (2000→1000, 2001→2501, 2002→2502): optimiser and permutation randomness are jointly resampled and cannot be separated.
Groups: commit items are paired (developer / generated) rows sharing a hash → the hash is the sampling unit for calibration and test resampling and for the estimator.
Estimands per (seed, fold): RAW (T=1, λ=0) primary; COMMON map (one T, λ fitted on calibration predictions pooled with equal arm weight over the roster, ties → identity);
ARM-specific map. p0 = climatology of the target raters on the (resampled) calibration items.
Estimator: d_sfg (group mean of per-row loss differences) → mean over groups → mean over the 3 fixed folds → mean over seeds.
Crossed bootstrap: seeds with replacement; calibration GROUPS with replacement (calibrators refit); test GROUPS with replacement; same draws for all arms / estimands / contrasts.
Reports: pooled estimate + percentile CI (raw / common / arm / common − raw), seed-specific and fold-specific estimates, n_seed/n_fold/n_group, grid boundary-hit frequencies,
equivalence by the 90 % CI criterion for perm − chen (raw) at margins .001/.002/.003.
Usage: ~/miniconda3/envs/skill1/bin/python analysis_chain7c.py why [--B 10000] [--allow_incomplete]
"""
import sys, os, json, glob, argparse, itertools, numpy as np, pandas as pd
from paths import LLMJ
ap = argparse.ArgumentParser(); ap.add_argument("crit"); ap.add_argument("--B", type=int, default=10000); ap.add_argument("--allow_incomplete", action="store_true")
args = ap.parse_args(); crit = args.crit; K = 5; LV = np.arange(K)
ROSTER = ["chen", "perm_mode", "chen0", "perm_mode0"]; FOLDS = [0, 1, 2]; SEEDS = [2000, 2001, 2002]; PERM_OF = {2000: 1000, 2001: 1000, 2002: 1000}   # fixed donor mapping; hard (seeds 2001/2002 last in chain7c) analysed separately when present
ROOT = LLMJ + "/paper-2/idea-stage/pilot/results_v2"; bench = pd.read_csv(LLMJ + "/code/commit_message/data/CM-benchmark.csv")
H = bench[[f"{crit}_{i}" for i in range(1, 7)]].to_numpy(int); HASH = pd.factorize(bench.hash)[0]
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def calib(P, T, lam, p0): Q = np.exp(np.log(np.clip(P, 1e-9, 1)) / T); Q /= Q.sum(1, keepdims=True); return (1 - lam) * Q + lam * p0
TS = [0.5, 0.7, 0.85, 1.0, 1.25, 1.5, 2, 3, 4, 6]; LAMS = [0, .05, .1, .2, .3, .5]
GRID = sorted([(T, lam) for T in TS for lam in LAMS], key=lambda g: (abs(np.log(g[0])), g[1]))
def fit_cal(Pc, Hc, p0):
    best = None
    for T, lam in GRID:
        s = np.mean([rps(calib(Pc, T, lam, p0), Hc[:, r]).mean() for r in range(Hc.shape[1])])
        if best is None or s < best[0] - 1e-12: best = (s, T, lam)
    return best[1], best[2]
def path(seed, fold, arm): return f"{ROOT}/{crit}/s0{'' if seed == 2000 else f'_seed{seed}'}/f{fold}/{arm}"
# ---------------- load + validate
cells = {}; missing = []
for seed, fold, arm in itertools.product(SEEDS, FOLDS, ROSTER):
    p = path(seed, fold, arm)
    if not os.path.exists(f"{p}/P_test.npy"): missing.append((seed, fold, arm)); continue
    meta = json.load(open(f"{p}/meta.json")); it = pd.read_csv(f"{p}/items_test.csv"); ic = pd.read_csv(f"{p}/items_calib.csv"); Pt = np.load(f"{p}/P_test.npy"); Pc = np.load(f"{p}/P_calib.npy")
    assert meta["evaluator"] == fold and meta["split"] == 0 and meta["arm"] == arm and meta.get("criterion", crit) == crit, (p, meta)
    assert meta["opt_seed"] == seed and (arm not in ("perm", "perm_mode", "perm_mode0") or meta["perm_seed"] == PERM_OF[seed]), (p, meta.get("opt_seed"), meta.get("perm_seed"))
    assert Pt.shape == (len(it), K) and Pc.shape == (len(ic), K) and np.isfinite(Pt).all() and np.isfinite(Pc).all() and np.allclose(Pt.sum(1), 1, atol=1e-4) and np.allclose(Pc.sum(1), 1, atol=1e-4), p
    cells[(seed, fold, arm)] = dict(Pt=Pt, Pc=Pc, it=it.row.to_numpy(), ic=ic.row.to_numpy(), T=[r for r in range(6) if r != fold])
if missing and not args.allow_incomplete: sys.exit(f"incomplete balanced block: missing {len(missing)} cells, e.g. {missing[:5]}")
present = sorted({(s, f) for (s, f, a) in cells if all((s, f, b) in cells for b in ROSTER)})
if not present: sys.exit(f"no complete (seed, fold) cell yet for roster {ROSTER}; present arms: {sorted(set(k[2] for k in cells))}")
seeds_present = sorted({s for s, f in present}); folds_present = sorted({f for s, f in present})
ref = cells[(present[0][0], present[0][1], ROSTER[0])]
for key, c in cells.items(): assert (c["it"] == ref["it"]).all() and (c["ic"] == ref["ic"]).all(), f"item alignment differs in {key}"   # identical item rows/order in every cell
IT, IC = ref["it"], ref["ic"]; G_test = HASH[IT]; G_cal = HASH[IC]; ug_test = np.unique(G_test); ug_cal = np.unique(G_cal)
test_groups = [np.where(G_test == g)[0] for g in ug_test]; cal_groups = [np.where(G_cal == g)[0] for g in ug_cal]
print(f"### {crit}: block seeds={seeds_present} folds={folds_present} roster={ROSTER} | n_seed={len(seeds_present)} n_fold={len(folds_present)} n_test_groups={len(ug_test)} (rows {len(IT)}) n_cal_groups={len(ug_cal)} | B={args.B}")
CONTRASTS = [("perm_mode − chen", "perm_mode", "chen"), ("perm_mode0 − chen0", "perm_mode0", "chen0"), ("chen0 − chen", "chen0", "chen"), ("perm_mode0 − perm_mode", "perm_mode0", "perm_mode")]
INTERACTION = ("Δadv − Δ0", ("perm_mode", "chen"), ("perm_mode0", "chen0"))   # (perm_mode − chen) − (perm_mode0 − chen0)
def group_means(v, groups): return np.array([v[g].mean() for g in groups])
def cell_losses(s, f, cal_rows, test_rows, test_groups_idx):
    """per-arm GROUP-mean losses under raw/common/arm for one (seed, fold); cal_rows/test_rows index the cell's calibration/test rows; returns dict arm -> {est: array over groups}, fitted maps"""
    T = cells[(s, f, ROSTER[0])]["T"]; Hc = H[IC[cal_rows]][:, T]; p0 = np.bincount(Hc.ravel(), minlength=K) / Hc.size; yt = H[IT[test_rows]][:, f]
    Pc_all = np.concatenate([cells[(s, f, a)]["Pc"][cal_rows] for a in ROSTER]); Hc_all = np.concatenate([Hc for _ in ROSTER]); Tc, lc = fit_cal(Pc_all, Hc_all, p0)
    out = {}; fitted = {"common": (Tc, lc)}
    for a in ROSTER:
        Pt = cells[(s, f, a)]["Pt"][test_rows]; Pc = cells[(s, f, a)]["Pc"][cal_rows]; Ta, la = fit_cal(Pc, Hc, p0); fitted[a] = (Ta, la)
        out[a] = dict(raw=group_means(rps(Pt, yt), test_groups_idx), common=group_means(rps(calib(Pt, Tc, lc, p0), yt), test_groups_idx), arm=group_means(rps(calib(Pt, Ta, la, p0), yt), test_groups_idx))
    return out, fitted
all_rows = np.arange(len(IT)); all_cal = np.arange(len(IC))
L0 = {sf: cell_losses(sf[0], sf[1], all_cal, all_rows, test_groups) for sf in present}
def contrast_val(L, a, b, e, seed_list):
    return float(np.mean([np.mean([np.mean(L[(s, f)][0][a][e] - L[(s, f)][0][b][e]) for f in folds_present if (s, f) in L]) for s in seed_list]))
def inter_val(L, e, seed_list): return contrast_val(L, "perm_mode", "chen", e, seed_list) - contrast_val(L, "perm_mode0", "chen0", e, seed_list)
hashes = {k: json.load(open(f"{path(*k)}/meta.json")).get("mapping_hash") for k in cells if k[2] in ("perm_mode", "perm_mode0")}
by_fold = {}
for (s_, f_, a_), h_ in hashes.items(): by_fold.setdefault(f_, set()).add(h_)
print("  donor-mapping hashes per fold (must be ONE value per fold across seeds and both permutation arms; None = pre-hash run):", {f: sorted(map(str, v)) for f, v in by_fold.items()})
est = {}; per_seed = {}; per_fold = {}
for name, a, b in CONTRASTS:
    for e in ("raw", "common", "arm"):
        est[(name, e)] = contrast_val(L0, a, b, e, seeds_present)
        per_seed[(name, e)] = {s: contrast_val(L0, a, b, e, [s]) for s in seeds_present}
        per_fold[(name, e)] = {f: float(np.mean([np.mean(L0[(s, f)][0][a][e] - L0[(s, f)][0][b][e]) for s in seeds_present if (s, f) in L0])) for f in folds_present}
for e in ("raw", "common", "arm"):
    est[(INTERACTION[0], e)] = inter_val(L0, e, seeds_present); per_seed[(INTERACTION[0], e)] = {s_: inter_val(L0, e, [s_]) for s_ in seeds_present}
    per_fold[(INTERACTION[0], e)] = {f: float(np.mean([(np.mean(L0[(s_, f)][0]["perm_mode"][e] - L0[(s_, f)][0]["chen"][e]) - np.mean(L0[(s_, f)][0]["perm_mode0"][e] - L0[(s_, f)][0]["chen0"][e])) for s_ in seeds_present if (s_, f) in L0])) for f in folds_present}
# within-fold optimizer-seed sign table for the two permutation contrasts (fixed donor mapping ⇒ differences across seeds are optimizer variability)
for name, a, b in CONTRASTS[:2]:
    tab = {f: {s_: round(float(np.mean(L0[(s_, f)][0][a]["raw"] - L0[(s_, f)][0][b]["raw"])), 4) for s_ in seeds_present if (s_, f) in L0} for f in folds_present}
    print(f"  within-fold seed table (raw) {name}: {tab}")
# ---------------- crossed bootstrap over seeds, calibration groups (refit), test groups
rng = np.random.RandomState(0); boot = {k: [] for k in est}; boot_cr = {name: [] for name, _, _ in CONTRASTS}; boot_ar = {name: [] for name, _, _ in CONTRASTS}; boot_ac = {name: [] for name, _, _ in CONTRASTS}; hits = {"T_lo": 0, "T_hi": 0, "lam_hi": 0, "n": 0}
for _ in range(args.B):
    sdraw = rng.choice(seeds_present, len(seeds_present), replace=True)
    cal_g = rng.choice(len(cal_groups), len(cal_groups), replace=True); cal_rows = np.concatenate([cal_groups[g] for g in cal_g])
    tg = rng.choice(len(test_groups), len(test_groups), replace=True); test_rows = np.concatenate([test_groups[g] for g in tg]); tgi = []; pos = 0
    for g in tg: tgi.append(np.arange(pos, pos + len(test_groups[g]))); pos += len(test_groups[g])
    Lb = {}
    for s in set(sdraw):
        for f in folds_present:
            if (s, f) in L0:
                Lb[(s, f)] = cell_losses(s, f, cal_rows, test_rows, tgi)
                for a, (Ta, la) in Lb[(s, f)][1].items(): hits["n"] += 1; hits["T_lo"] += Ta == TS[0]; hits["T_hi"] += Ta == TS[-1]; hits["lam_hi"] += la == LAMS[-1]
    for name, a, b in CONTRASTS:
        vals = {e: contrast_val(Lb, a, b, e, sdraw) for e in ("raw", "common", "arm")}
        for e in vals: boot[(name, e)].append(vals[e])
        boot_cr[name].append(vals["common"] - vals["raw"]); boot_ar[name].append(vals["arm"] - vals["raw"]); boot_ac[name].append(vals["arm"] - vals["common"])
    for e in ("raw", "common", "arm"): boot[(INTERACTION[0], e)].append(inter_val(Lb, e, sdraw))
def pct(v, q): return float(np.percentile(v, q)) if len(v) else float("nan")
rows = []
for name, a, b in CONTRASTS + [(INTERACTION[0], None, None)]:
    for e in ("raw", "common", "arm"):
        v = np.array(boot[(name, e)]); rows.append(dict(contrast=name, estimand=e, est=est[(name, e)], lo=pct(v, 2.5), hi=pct(v, 97.5), lo90=pct(v, 5), hi90=pct(v, 95), per_seed=per_seed[(name, e)], per_fold=per_fold[(name, e)]))
    for lab, bb, e1, e2 in (("common − raw", boot_cr, "common", "raw"), ("arm − raw", boot_ar, "arm", "raw"), ("arm − common", boot_ac, "arm", "common")):
        if name not in bb: continue
        v = np.array(bb[name]); rows.append(dict(contrast=name, estimand=lab, est=est[(name, e1)] - est[(name, e2)], lo=pct(v, 2.5), hi=pct(v, 97.5), lo90=float("nan"), hi90=float("nan"), per_seed={}, per_fold={}))
for r in rows:
    print(f"  {r['contrast']:18s} {r['estimand']:13s} {r['est']:+.4f} [{r['lo']:+.4f}, {r['hi']:+.4f}]" + (f"  seeds {{{', '.join(f'{k}: {v:+.4f}' for k, v in r['per_seed'].items())}}}  folds {{{', '.join(f'{k}: {v:+.4f}' for k, v in r['per_fold'].items())}}}" if r["per_seed"] else ""))
pc = [r for r in rows if r["contrast"] == INTERACTION[0] and r["estimand"] == "raw"][0]
print("  interaction Δadv − Δ0 (raw) 90% CI:", f"[{pc['lo90']:+.4f}, {pc['hi90']:+.4f}]", "— within ±.002 band:", bool(pc["lo90"] > -0.002 and pc["hi90"] < 0.002))
print("  calibration-grid boundary hits over bootstrap refits:", {k: (round(v / max(hits['n'], 1), 3) if k != "n" else v) for k, v in hits.items()})
print("  fitted maps (full data):", {f"s{s}f{f}": L0[(s, f)][1] for (s, f) in present})
print("  NOTE: one outer item split, one base family, folds 0–2 only (claims conditional on Qwen / split 0 / folds 0–2); donor mapping FIXED ⇒ seed resampling = optimizer variability; 3 seeds is a floor, not strong variance estimation.")
json.dump(dict(crit=crit, seeds=seeds_present, folds=folds_present, roster=ROSTER, B=args.B, n_test_groups=int(len(ug_test)), n_cal_groups=int(len(ug_cal)), rows=rows, boundary_hits=hits), open(f"{ROOT}/{crit}/analysis_chain7c.json", "w"), indent=1, default=str)
