"""Stage 15 S15-1 (PROTOCOL_STAGE15.md): the corrected latent detectors over the existing synthetic draws and injection families. Rung a (`_wa`) on the null,
random-direction, in-span and semantic families; rung b (`_wb`) on null, random and semantic. Per draw, k = 20: direction accuracy own − another rater's parameters
(detection = lower bound > +1 point; null sound = interval intersects [−0.5, +0.5]), own − k = 0, concordance, log-likelihood latent − scale-use comparator.
Frequency rule (Stage 7 Am. 4): detects if the rule fires in ≥ 3 of 4 draws, fails if ≤ 1 of 4, unstable otherwise. Rater bootstrap over (fold, rater), seed 17,
B = 2000, as s14_real.py. Post hoc. Output: results/stage15_synth.json / .md (draws with fewer than 5 folds are listed but not counted)"""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); K = 20
def load(panel, tag): return [json.load(open(f)) for f in sorted(glob.glob(f"{R}/stage2a_multipref_synth_{panel}{tag}_f?.json"))]
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
SD = ("", "s11", "s12", "s13")
FAM = {"null": {0: [f"t0{s}" for s in SD]}, "random": {g: [f"t{g}{s}" for s in SD] for g in (5, 10)}, "in-span": {g: [f"x{g}{s}" for s in SD] for g in (5, 10)}, "semantic": {g: [f"sem{g}{s}" for s in SD] for g in (5, 10)}}
ORA = {}
for f in glob.glob(f"{R}/synth/synth_meta*.json"):
    for t, v in json.load(open(f)).items():
        if isinstance(v, dict) and "oracle_gain_realised" in v: ORA[t] = 100 * v["oracle_gain_realised"]
def cells(rs):
    c = {}
    for m, q in (("DL", "DFs"), ("L", "F")):
        for mt, den in (("dir", "n_dir"), ("conc", "conc_den")):
            c[f"{m}_{mt}_own-other"] = lin(rs, [(1, K, f"{m}_{mt}"), (-1, K, f"{m}_perm_{mt}")], den); c[f"{m}_{mt}_own-k0"] = lin(rs, [(1, K, f"{m}_{mt}"), (-1, 0, f"{m}_{mt}")], den)
        c[f"{q}_dir_own-other"] = lin(rs, [(1, K, f"{q}_dir"), (-1, K, f"{q}_perm_dir")], "n_dir"); c[f"{m}_ll-{q}"] = lin(rs, [(1, K, f"{m}_ll"), (-1, K, f"{q}_ll")], "n")
    return c
out = {"draws": {}, "frequency": {}, "pooled": {}}; RUNGS = (("a", "_wa"), ("b", "_wb"))
for fam, st in FAM.items():
    for g, panels in st.items():
        for nm, tag in RUNGS:
            pool = []; n_ok = 0; cnt = collections.Counter()
            for p in panels:
                runs = load(p, tag); folds = sorted(fo["fold"] for o in runs for fo in o["folds"])
                if not runs: continue
                rs = [r for o in runs for r in o["per_rater"]]; c = cells(rs); c["folds"] = folds; c["oracle"] = ORA.get(p); out["draws"][f"{p}|{nm}"] = c
                if len(folds) < 5: continue
                n_ok += 1; pool += [dict(r, rater=(r["rater"])) for r in rs]
                for m in ("DL", "L"):
                    v = c[f"{m}_dir_own-other"]; v0 = c[f"{m}_dir_own-k0"]; c[f"{m}_detect"] = bool(v[1] > 1); c[f"{m}_sound"] = bool(v[1] <= 0.5 and v[2] >= -0.5); c[f"{m}_excl0"] = bool(v[1] > 0 or v[2] < 0)
                    cnt[f"{m}_detect"] += c[f"{m}_detect"]; cnt[f"{m}_sound"] += c[f"{m}_sound"]; cnt[f"{m}_excl0"] += c[f"{m}_excl0"]; cnt[f"{m}_k0_lb1"] += bool(v0[1] > 1); cnt[f"{m}_k0_lb0"] += bool(v0[1] > 0)
            if not n_ok: continue
            fr = {"n_draws": n_ok, **cnt}
            for m in ("DL", "L"):
                d = cnt[f"{m}_detect"]
                fr[f"{m}_reading"] = ("incomplete" if n_ok < 4 else ("null-sound" if d == 0 and cnt[f"{m}_sound"] == 4 else "null NOT sound") if g == 0 else "detects" if d >= 3 else "fails" if d <= 1 else "unstable")
            out["frequency"][f"{fam}|{g}|{nm}"] = fr; out["pooled"][f"{fam}|{g}|{nm}"] = {a: b for a, b in cells(pool).items() if b is not None}   # the draws share raters: (fold, rater) clusters carry all draws
L = ["# Stage 15 S15-1 — corrected latent detectors over the existing synthetic draws (post hoc; MultiPref semi-synthetic, k = 20, points or ×100 nats per rating, 95 % rater bootstrap)", "",
     "## Frequency over draws (detection: own − other direction lower bound > +1 point; ≥ 3 of 4 = detects, ≤ 1 of 4 = fails)", "",
     "| family | strength | rung | draws | DL detections | DL reading | L detections | L reading | DL own − k0 lower bound > 0 / > +1 | L own − k0 lower bound > 0 / > +1 | pooled DL own − other | pooled L own − other | pooled DL own − k0 | pooled L own − k0 |", "|---" * 14 + "|"]
for key, fr in out["frequency"].items():
    fam, g, nm = key.split("|"); po = out["pooled"][key]
    L.append(f"| {fam} | +{g} | {nm} | {fr['n_draws']} | {fr.get('DL_detect', 0)} | {fr['DL_reading']} | {fr.get('L_detect', 0)} | {fr['L_reading']} | {fr.get('DL_k0_lb0', 0)} / {fr.get('DL_k0_lb1', 0)} | {fr.get('L_k0_lb0', 0)} / {fr.get('L_k0_lb1', 0)} | {fmt(po.get('DL_dir_own-other'))} | {fmt(po.get('L_dir_own-other'))} | {fmt(po.get('DL_dir_own-k0'))} | {fmt(po.get('L_dir_own-k0'))} |")
L += ["", "Null draws: intervals that exclude 0 — " + "; ".join(f"{k_.split('|')[1]}|{k_.split('|')[2]}: DL {fr.get('DL_excl0', 0)}/{fr['n_draws']}, L {fr.get('L_excl0', 0)}/{fr['n_draws']}" for k_, fr in out["frequency"].items() if k_.startswith("null")), "",
      "## Every draw", "", "| draw | oracle gain | rung | folds | DL own − other | DL own − k0 | L own − other | L own − k0 | DFs own − other | F own − other | DL conc own − other | L conc own − other | DL − DFs LL | L − F LL | detected (DL / L) |", "|---" * 15 + "|"]
for key, c in out["draws"].items():
    p, nm = key.split("|"); g = lambda q: fmt(c.get(q)); det = " / ".join(("yes" if c[f"{m}_detect"] else "no") if f"{m}_detect" in c else "—" for m in ("DL", "L"))
    L.append(f"| {p} | {'—' if c['oracle'] is None else format(c['oracle'], '+.1f')} | {nm} | {len(c['folds'])} | {g('DL_dir_own-other')} | {g('DL_dir_own-k0')} | {g('L_dir_own-other')} | {g('L_dir_own-k0')} | {g('DFs_dir_own-other')} | {g('F_dir_own-other')} | {g('DL_conc_own-other')} | {g('L_conc_own-other')} | {g('DL_ll-DFs')} | {g('L_ll-F')} | {det} |")
json.dump(out, open(f"{R}/stage15_synth.json", "w"), indent=1); open(f"{R}/stage15_synth.md", "w").write("\n".join(L) + "\n"); print("\n".join(L[:L.index("## Every draw")]))
