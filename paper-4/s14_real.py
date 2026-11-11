"""Stage 14 Amendment 1, A1-4 summary (PROTOCOL_STAGE14.md): the paper's held-out-item panels with the corrected latent models. Rungs a (`_wa`: whitened adaptation
prior, penalties by validation log-likelihood) and b (`_wb`: whitened prior, rater-side penalties and adaptation strength by pseudo-new-rater concordance on
validation items), against the published configuration where a run with the permutation control exists. Part 1: semi-synthetic positive control (direction accuracy,
own − another rater's parameters, k = 20; power = lower bound > +1 point; null sound = interval within ±0.5 of zero). Part 2: real panels (latent minus its scale-use
comparator in log-likelihood; direction and concordance own − other / own − k = 0). Rater bootstrap over (fold, rater), seed 17, B = 2000, draws averaged within
rater. Post hoc. Output: results/stage14_real.json / .md (partial results are summarised with the folds that exist)"""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
def load(panel, tag): return [json.load(open(f)) for f in sorted(glob.glob(f"{R}/stage2a_{panel}{tag}_f?.json"))]
def lin(rs, terms, den, sc=100.0):
    """Σ coef · (per-rater draw-mean of key at k), every term rescaled to the first term's denominator; ratio estimator and rater bootstrap (as s14_fix.py)"""
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rs: by[(r["fold"], r["rater"])][r["k"]].append(r)
    d, w = [], []
    for z, kk in by.items():
        if any(k not in kk or key not in kk[k][0] for _, k, key in terms): continue
        w0 = np.mean([x[den] for x in kk[terms[0][1]]])
        if w0 <= 0 or any(np.mean([x[den] for x in kk[k]]) <= 0 for _, k, _ in terms): continue
        d.append(sum(c * np.mean([x[key] for x in kk[k]]) * w0 / np.mean([x[den] for x in kk[k]]) for c, k, key in terms)); w.append(w0)
    if not d: return None
    d, w = np.array(d), np.array(w); rng = np.random.RandomState(17); bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]
    return [sc * d.sum() / w.sum(), sc * np.percentile(bs, 2.5), sc * np.percentile(bs, 97.5), len(d)]
fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
SYN = {"multipref_synth_t0": 0.0, "multipref_synth_t5": 5.2, "multipref_synth_t10": 10.1}
REAL = {"multipref_overall": (20, "_A5perm"), "dices": (20, None), "prism": (20, None), "dorn_raters": (10, "")}
COMP = lambda panel, m: ("F" if m == "L" else "DFs" if panel.startswith("multipref") else "DF")
def cells(panel, rs, k):
    c = {}
    for m in ("DL", "L", "DF", "DFs", "F"):
        for mt, den in (("dir", "n_dir"), ("conc", "conc_den")):
            c[f"{m}_{mt}_own-other"] = lin(rs, [(1, k, f"{m}_{mt}"), (-1, k, f"{m}_perm_{mt}")], den); c[f"{m}_{mt}_own-k0"] = lin(rs, [(1, k, f"{m}_{mt}"), (-1, 0, f"{m}_{mt}")], den)
    for m in ("DL", "L"):
        q = COMP(panel, m); c[f"{m}_ll-{q}"] = lin(rs, [(1, k, f"{m}_ll"), (-1, k, f"{q}_ll")], "n")
        if m == "DL" and q == "DFs": c["DL_ll-DF"] = lin(rs, [(1, k, "DL_ll"), (-1, k, "DF_ll")], "n")
        if "DF_ll" in rs[0]: c[f"{m}_ll-DFany"] = lin(rs, [(1, k, f"{m}_ll"), (-1, k, "DF_ll")], "n")   # against the softmax offsets, whatever the latent's family
        c[f"{m}_ll-D"] = lin(rs, [(1, k, f"{m}_ll"), (-1, k, "D_ll")], "n"); c[f"{q}_ll-D"] = lin(rs, [(1, k, f"{q}_ll"), (-1, k, "D_ll")], "n")
        for mt, den in (("dir", "n_dir"), ("conc", "conc_den")):
            c[f"{m}-{q}_{mt}_own-other"] = lin(rs, [(1, k, f"{m}_{mt}"), (-1, k, f"{m}_perm_{mt}"), (-1, k, f"{q}_{mt}"), (1, k, f"{q}_perm_{mt}")], den)
    return {a: b for a, b in c.items() if b is not None}
out = {"part1": {}, "part2": {}, "selected": {}}
RUNGS = (("published", None), ("a", "_wa"), ("b", "_wb"))
for panel in list(SYN) + list(REAL):
    k = 20 if panel in SYN else REAL[panel][0]; blk = {}
    for nm, tag in RUNGS:
        if tag is None: tag = "" if panel in SYN else REAL[panel][1]
        if tag is None: continue
        runs = load(panel, tag)
        if not runs: continue
        rs = [r for o in runs for r in o["per_rater"]]; c = cells(panel, rs, k); c["folds"] = sorted(fo["fold"] for o in runs for fo in o["folds"]); blk[nm] = c
        out["selected"][f"{panel}|{nm}"] = [{"fold": fo["fold"], "lam": {m: fo["lam"].get(m) for m in ("DL", "L", "DF", "DFs", "F")}, "lam_adapt": {a: b for a, b in fo["lam_adapt"].items() if a.endswith(f"_{k}")}, "sel_conc": fo.get("sel_conc", {})} for o in runs for fo in o["folds"]]
    out["part1" if panel in SYN else "part2"][panel] = blk
# ---- readings
for panel, blk in out["part1"].items():
    for nm, c in blk.items():
        c["power"] = {m: bool(c[f"{m}_dir_own-other"][1] > 1) for m in ("DL", "L") if f"{m}_dir_own-other" in c}
        if panel == "multipref_synth_t0": c["null_sound"] = {m: bool(c[f"{m}_dir_own-other"][1] <= 0.5 and c[f"{m}_dir_own-other"][2] >= -0.5) for m in ("DL", "L") if f"{m}_dir_own-other" in c}
for panel, blk in out["part2"].items():
    for nm, c in blk.items():
        c["reading"] = {}
        for m in ("DL", "L"):
            q = COMP(panel, m); ll = c.get(f"{m}_ll-{q}"); do = c.get(f"{m}_dir_own-other"); dd = c.get(f"{m}-{q}_dir_own-other")
            if ll is None or do is None: continue
            if ll[1] > 0 or (do[1] > 0 and dd is not None and dd[0] > 0):
                co = c.get(f"{m}_conc_own-other"); c["reading"][m] = "contradicted" + (", practically meaningful" if do[1] > 1 or (co is not None and co[1] > 1) else "")
            elif ll[2] <= 0.5 and do[2] < 1: c["reading"][m] = "stands"
            else: c["reading"][m] = "inconclusive"
L = ["# Stage 14 Amendment 1, A1-4 — held-out items with the corrected latent models (post hoc; points or ×100 nats per rating, 95 % rater bootstrap)", "",
     "## Part 1 — semi-synthetic positive control (MultiPref; direction accuracy, own − another rater's parameters, k = 20)", "",
     "| panel | oracle gain | rung | folds | DL own − other | L own − other | DFs own − other | F own − other | DL − DFs | L − F | power (DL / L) |", "|---" * 11 + "|"]
for panel, blk in out["part1"].items():
    for nm, c in blk.items():
        g = lambda q: fmt(c.get(q)); pw = " / ".join("yes" if c["power"].get(m) else "no" if m in c["power"] else "—" for m in ("DL", "L"))
        L.append(f"| {panel.split('_')[-1]} | +{SYN[panel]} | {nm} | {len(c['folds'])} | {g('DL_dir_own-other')} | {g('L_dir_own-other')} | {g('DFs_dir_own-other')} | {g('F_dir_own-other')} | {g('DL-DFs_dir_own-other')} | {g('L-F_dir_own-other')} | {pw}" + (f"; null sound: {c['null_sound']}" if "null_sound" in c else "") + " |")
L += ["", "## Part 2 — real panels (k = 20; Dorn k = 10)", ""]
for panel, blk in out["part2"].items():
    L += [f"**{panel}**", "", "| rung | folds | latent | LL latent − comparator | LL latent − D | LL comparator − D | direction own − other | comparator's | latent − comparator | direction own − k0 | concordance own − other | comparator's | latent − comparator | concordance own − k0 | reading |", "|---" * 15 + "|"]
    for nm, c in blk.items():
        for m in ("DL", "L"):
            q = COMP(panel, m); g = lambda x: fmt(c.get(x))
            if f"{m}_ll-D" not in c: continue
            L.append(f"| {nm} | {len(c['folds'])} | {m} (vs {q}) | {g(f'{m}_ll-{q}')} | {g(f'{m}_ll-D')} | {g(f'{q}_ll-D')} | {g(f'{m}_dir_own-other')} | {g(f'{q}_dir_own-other')} | {g(f'{m}-{q}_dir_own-other')} | {g(f'{m}_dir_own-k0')} | {g(f'{m}_conc_own-other')} | {g(f'{q}_conc_own-other')} | {g(f'{m}-{q}_conc_own-other')} | {g(f'{m}_conc_own-k0')} | {c['reading'].get(m, '—')} |")
    L += ["", "Latent against the softmax scale-use offsets DF (cross-family for L), log-likelihood ×100: " + "; ".join(f"{nm} {m}: {fmt(c.get(f'{m}_ll-DFany'))}" for nm, c in blk.items() for m in ("DL", "L") if f"{m}_ll-DFany" in c), ""]
L += ["## Selected penalties (λ_text, λ_rater, λ_W), adaptation strength at the reported k, and rung b's selection cell", "", "| panel | rung | fold | DL | L | strengths | selection cell (raters / informative pairs) |", "|---" * 7 + "|"]
for key, rows in out["selected"].items():
    for s in rows: L.append(f"| {key.split('|')[0]} | {key.split('|')[1]} | {s['fold']} | {s['lam'].get('DL')} | {s['lam'].get('L')} | {s['lam_adapt']} | {s['sel_conc'].get('n_raters', '—')} / {s['sel_conc'].get('n_pairs', '—')}{' (below 5,000: flagged)' if s['sel_conc'].get('n_pairs', 10**9) < 5000 else ''} |")
json.dump(out, open(f"{R}/stage14_real.json", "w"), indent=1); open(f"{R}/stage14_real.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
