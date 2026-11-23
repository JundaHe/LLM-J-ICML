"""Stage 15 S15-2 (PROTOCOL_STAGE15.md): scale use against the content interaction with the same offsets. Runs tagged `_s15` (rung a, `--decomp`, kinds DFL / FL on
top of the frozen DF / F). (1) Stage-wise model against its base: staged − base, staged − staged with the latent at the prior mean (`z0`), staged − staged with
another rater's latent and the own offsets (`perm`). (2) The adopted latents DL / L with the item-independent part and the interaction taken from different raters:
`sh` (own shift only), `ia` (own interaction only), `xi` (own shift, other's interaction), `xs` (other's shift, own interaction). Positive control on the synthetic
draws t0 / t5 / t10; reading rule of §2.4. Rater bootstrap over (fold, rater), seed 17, B = 2000 (as s14_real.py). Post hoc. Output: results/stage15_decomp.json / .md"""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); TAG = "_s15"
def load(panel): return [json.load(open(f)) for f in sorted(glob.glob(f"{R}/stage2a_{panel}{TAG}_f?.json"))]
def lin(rs, terms, den, sc=100.0):
    """Σ coef · (per-rater draw-mean of key at k), every term rescaled to the first term's denominator; ratio estimator and rater bootstrap (as s14_real.py)"""
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
PANELS = {"multipref_synth_t0": 20, "multipref_synth_t5": 20, "multipref_synth_t10": 20, "multipref_overall": 20, "dices": 20, "prism": 20, "dorn_raters": 10}
FAMS = (("DFL", "DF", "DL"), ("FL", "F", "L")); MT = (("ll", "n"), ("dir", "n_dir"), ("conc", "conc_den"))
def cells(rs, k):
    c = {}
    for S, Bm, M in FAMS:
        for mt, den in MT:
            c[f"{S}-{Bm}_{mt}"] = lin(rs, [(1, k, f"{S}_{mt}"), (-1, k, f"{Bm}_{mt}")], den); c[f"{M}-{Bm}_{mt}"] = lin(rs, [(1, k, f"{M}_{mt}"), (-1, k, f"{Bm}_{mt}")], den)
            c[f"{S}-z0_{mt}"] = lin(rs, [(1, k, f"{S}_{mt}"), (-1, k, f"{S}_z0_{mt}")], den); c[f"{S}-perm_{mt}"] = lin(rs, [(1, k, f"{S}_{mt}"), (-1, k, f"{S}_perm_{mt}")], den)
            c[f"{Bm}-perm_{mt}"] = lin(rs, [(1, k, f"{Bm}_{mt}"), (-1, k, f"{Bm}_perm_{mt}")], den); c[f"{Bm}-k0_{mt}"] = lin(rs, [(1, k, f"{Bm}_{mt}"), (-1, 0, f"{Bm}_{mt}")], den)
            for v in ("perm", "xi", "xs", "sh", "ia"): c[f"{M}-{v}_{mt}"] = lin(rs, [(1, k, f"{M}_{mt}"), (-1, k, f"{M}_{v}_{mt}")], den)
            c[f"{M}-k0_{mt}"] = lin(rs, [(1, k, f"{M}_{mt}"), (-1, 0, f"{M}_{mt}")], den); c[f"{M}_sh-k0_{mt}"] = lin(rs, [(1, k, f"{M}_sh_{mt}"), (-1, 0, f"{M}_{mt}")], den); c[f"{M}_ia-k0_{mt}"] = lin(rs, [(1, k, f"{M}_ia_{mt}"), (-1, 0, f"{M}_{mt}")], den)
    return {a: b for a, b in c.items() if b is not None}
out = {"panels": {}, "control": {}, "selected": {}}
for panel, k in PANELS.items():
    runs = load(panel)
    if not runs: continue
    rs = [r for o in runs for r in o["per_rater"]]; c = cells(rs, k); c["folds"] = sorted(fo["fold"] for o in runs for fo in o["folds"]); c["reading"] = {}; out["panels"][panel] = c
    out["selected"][panel] = [{"fold": fo["fold"], "lam": {m: fo["lam"].get(m) for m in ("DF", "DFL", "DL", "F", "FL", "L")}, "lam_adapt": {a: b for a, b in fo["lam_adapt"].items() if a.endswith(f"_{k}")}} for o in runs for fo in o["folds"]]
    for S, Bm, M in FAMS:
        if f"{S}-{Bm}_ll" not in c: continue
        ll, pl, pc = c[f"{S}-{Bm}_ll"], c[f"{S}-perm_ll"], c[f"{S}-perm_conc"]
        c["reading"][S] = "interaction adds" if ll[1] > 0 and (pl[1] > 0 or pc[1] > 0) else "no interaction beyond the offsets" if ll[2] <= 0.5 and pc[2] < 1 else "inconclusive"
        xs, xi, xc = c[f"{M}-xs_ll"], c[f"{M}-xi_ll"], c[f"{M}-xi_conc"]
        c["reading"][M] = " + ".join(t for t, ok in (("shift", xs[1] > 0 and xi[2] <= 0.5 and xc[2] < 1), ("interaction", xi[1] > 0)) if ok) or "neither rule met"
for S, Bm, M in FAMS:                                                      # positive control of the stage-wise models (a null on a real panel is read only if it passes)
    t10 = out["panels"].get("multipref_synth_t10", {}).get(f"{S}-perm_dir"); t0 = out["panels"].get("multipref_synth_t0", {}).get(f"{S}-perm_dir")
    out["control"][S] = {"t10_power": None if t10 is None else bool(t10[1] > 1), "t0_sound": None if t0 is None else bool(t0[1] <= 0.5 and t0[2] >= -0.5)}
L = ["# Stage 15 S15-2 — scale use against the content interaction with the same offsets (post hoc; rung a; k = 20, Dorn k = 10; ×100 nats or points per rating, 95 % rater bootstrap)", "",
     f"Positive control of the stage-wise models (t10: own − other on the interaction, direction, lower bound > +1; t0: interval intersects ±0.5): {out['control']}", "",
     "## Stage-wise model against its base (identical offsets)", "",
     "| panel | folds | staged (base) | LL staged − base | LL staged − prior-mean latent | LL own − other latent | direction staged − base | direction own − other latent | concordance staged − base | concordance own − other latent | base: LL own − k0 | base: concordance own − other | reading |", "|---" * 13 + "|"]
for panel, c in out["panels"].items():
    g = lambda q: fmt(c.get(q))
    for S, Bm, M in FAMS:
        if f"{S}-{Bm}_ll" in c: L.append(f"| {panel} | {len(c['folds'])} | {S} ({Bm}) | {g(f'{S}-{Bm}_ll')} | {g(f'{S}-z0_ll')} | {g(f'{S}-perm_ll')} | {g(f'{S}-{Bm}_dir')} | {g(f'{S}-perm_dir')} | {g(f'{S}-{Bm}_conc')} | {g(f'{S}-perm_conc')} | {g(f'{Bm}-k0_ll')} | {g(f'{Bm}-perm_conc')} | {c['reading'].get(S, '—')} |")
L += ["", "## The adopted latents: item-independent part and interaction from different raters", "",
      "| panel | latent | LL own − k0 | LL own shift only − k0 | LL own interaction only − k0 | LL own − (other's shift) | LL own − (other's interaction) | LL own − other (both) | concordance own − (other's interaction) | concordance own − (other's shift) | direction own − (other's interaction) | direction own − (other's shift) | LL latent − offsets | reading |", "|---" * 14 + "|"]
for panel, c in out["panels"].items():
    g = lambda q: fmt(c.get(q))
    for S, Bm, M in FAMS:
        if f"{M}-xi_ll" in c: L.append(f"| {panel} | {M} | {g(f'{M}-k0_ll')} | {g(f'{M}_sh-k0_ll')} | {g(f'{M}_ia-k0_ll')} | {g(f'{M}-xs_ll')} | {g(f'{M}-xi_ll')} | {g(f'{M}-perm_ll')} | {g(f'{M}-xi_conc')} | {g(f'{M}-xs_conc')} | {g(f'{M}-xi_dir')} | {g(f'{M}-xs_dir')} | {g(f'{M}-{Bm}_ll')} | {c['reading'].get(M, '—')} |")
L += ["", "## Selected penalties (λ_text, λ_rater, λ_W) and adaptation strengths at the reported k", "", "| panel | fold | DFL | FL | strengths |", "|---|---|---|---|---|"]
for panel, rows in out["selected"].items():
    for s in rows: L.append(f"| {panel} | {s['fold']} | {s['lam'].get('DFL')} | {s['lam'].get('FL')} | {s['lam_adapt']} |")
json.dump(out, open(f"{R}/stage15_decomp.json", "w"), indent=1); open(f"{R}/stage15_decomp.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[:L.index("## Selected penalties (λ_text, λ_rater, λ_W) and adaptation strengths at the reported k")]))
