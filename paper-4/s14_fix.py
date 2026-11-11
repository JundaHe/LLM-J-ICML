"""Stage 14 Amendment 1, A1-2 summary (PROTOCOL_STAGE14.md): rungs L1-fix-a (whitened adaptation prior, selection by log-likelihood) and L1-fix-b (whitened prior,
rater-side penalties and adaptation strength by pseudo-new-rater concordance) against the CF reference L0 and the original rung L1, on seen jokes. Within-rater
pairwise concordance in points, rater bootstrap over (fold, rater), seed 17, B = 2000, support draws averaged within rater; all folds and folds 1–4 (fold 0's test
raters were used in the diagnosis). Rules of §1.5 at k = 20. Post hoc. Output: results/stage14_fix.json / .md"""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); KS = (5, 10, 20, 50); KR = 20
def load(tag): return [json.load(open(f)) for f in sorted(glob.glob(f"{R}/stage2a_jester_raters_{tag}_f?.json"))]
def lin(rs, terms, den, sc=100.0):
    """Σ coef · (per-rater draw-mean of key at k), every term rescaled to the first term's denominator; ratio estimator and rater bootstrap (as s14_1.py)"""
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rs: by[(r["fold"], r["rater"])][r["k"]].append(r)
    d, w = [], []
    for z, kk in by.items():
        if any(k not in kk or key not in kk[k][0] for _, k, key in terms): continue
        w0 = np.mean([x[den] for x in kk[terms[0][1]]])
        if w0 <= 0: continue
        d.append(sum(c * np.mean([x[key] for x in kk[k]]) * w0 / np.mean([x[den] for x in kk[k]]) for c, k, key in terms)); w.append(w0)
    d, w = np.array(d), np.array(w); rng = np.random.RandomState(17); bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]
    return [sc * d.sum() / w.sum(), sc * np.percentile(bs, 2.5), sc * np.percentile(bs, 97.5), len(d)]
fmt = lambda v: f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
RUN = {t: load(t) for t in ("id", "ida", "idb")}; assert all(len(v) == 5 for v in RUN.values()), {t: len(v) for t, v in RUN.items()}
ROWS = {t: [r for o in v for r in o["per_rater"]] for t, v in RUN.items()}; CF = json.load(open(f"{R}/stage14_cf.json"))["per_rater"]
out = {"selected": {t: [{"fold": fo["fold"], "lam": fo["lam"], "lam_adapt": fo["lam_adapt"], "sel_conc": fo.get("sel_conc", {})} for o in v for fo in o["folds"]] for t, v in RUN.items()}}
# regression: whitening leaves D and DF untouched, so rung a must reproduce rung L1's D / DF rows
key = lambda r: (r["fold"], r["k"], r["draw"], r["rater"]); a = {key(r): r for r in ROWS["id"]}; b = {key(r): r for r in ROWS["ida"]}; assert a.keys() == b.keys()
out["regression_max_abs_diff"] = {q: float(max(abs(a[z][q] - b[z][q]) for z in a if q in a[z])) for q in ("D_sconc", "DF_sconc", "DF_sll", "D_ll", "DF_ll", "sconc_den")}
def block(folds):
    res = {}; cf = [r for r in CF if r["fold"] in folds]
    for k in KS:
        c = {"L0_cf_own-mu": lin(cf, [(1, k, "cf_conc"), (-1, k, "mu_conc")], "den_s")}
        for t, nm in (("id", "L1"), ("ida", "L1-fix-a"), ("idb", "L1-fix-b")):
            rs = [r for r in ROWS[t] if r["fold"] in folds]
            for m in ("DL", "DF", "L"):
                if f"{m}_sconc" in rs[0] or any(f"{m}_sconc" in r for r in rs): c[f"{nm}_{m}_own-mu"] = lin(rs, [(1, k, f"{m}_sconc"), (-1, k, f"{m}_s0conc")], "sconc_den")
            c[f"{nm}_DL-DF"] = lin(rs, [(1, k, "DL_sconc"), (-1, k, "DL_s0conc"), (-1, k, "DF_sconc"), (1, k, "DF_s0conc")], "sconc_den")
            for m in ("DL", "L"):
                if f"{nm}_{m}_own-mu" in c: c[f"{nm}_{m}_own-other"] = lin(rs, [(1, k, f"{m}_sconc"), (-1, k, f"{m}_perm_sconc")], "sconc_den"); c[f"{nm}_{m}_share_of_cf"] = c[f"{nm}_{m}_own-mu"][0] / c["L0_cf_own-mu"][0]
            c[f"{nm}_LL_DL-DF"] = lin(rs, [(1, k, "DL_sll"), (-1, k, "DF_sll")], "ns")
        res[f"k{k}"] = c
    c = res[f"k{KR}"]; res["rules"] = {nm: {"i_DL_own-mu_lb>1": bool(c[f"{nm}_DL_own-mu"][1] > 1), "ii_DL-DF_lb>0": bool(c[f"{nm}_DL-DF"][1] > 0), "detects": bool(c[f"{nm}_DL_own-mu"][1] > 1 and c[f"{nm}_DL-DF"][1] > 0),
                                             "half_of_cf": {m: bool(c[f"{nm}_{m}_share_of_cf"] >= 0.5 and c[f"{nm}_{m}_own-mu"][1] > 0) for m in ("DL", "L") if f"{nm}_{m}_own-mu" in c}} for nm in ("L1", "L1-fix-a", "L1-fix-b")}
    return res
out["all_folds"] = block((0, 1, 2, 3, 4)); out["folds_1_4"] = block((1, 2, 3, 4))
L = ["# Stage 14 Amendment 1, A1-2 — Jester, seen jokes: fixed rungs (post hoc; concordance own − μ in points, 95 % rater bootstrap; LL ×100 nats per rating)", "",
     f"Regression (rung a vs L1, D / DF rows; max |difference| in summed per-rater units): {out['regression_max_abs_diff']}", ""]
for ttl, bk in (("All five folds", "all_folds"), ("Folds 1–4 (not used in the diagnosis)", "folds_1_4")):
    L += [f"## {ttl}", ""]
    for k in KS:
        c = out[bk][f"k{k}"]; L += [f"**k = {k}** — CF reference own − μ: {fmt(c['L0_cf_own-mu'])}", "", "| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |", "|---" * 10 + "|"]
        for nm in ("L1", "L1-fix-a", "L1-fix-b"):
            g = lambda q: fmt(c[f"{nm}_{q}"]) if f"{nm}_{q}" in c else "—"; sh = lambda m: f"{100 * c[f'{nm}_{m}_share_of_cf']:.0f} %" if f"{nm}_{m}_share_of_cf" in c else "—"
            L.append(f"| {nm} | {g('DL_own-mu')} | {sh('DL')} | {g('DF_own-mu')} | {g('DL-DF')} | {g('DL_own-other')} | {g('L_own-mu')} | {sh('L')} | {g('L_own-other')} | {g('LL_DL-DF')} |")
        L.append("")
    L += [f"Rules at k = {KR}: " + "; ".join(f"{nm}: (i) {'met' if v['i_DL_own-mu_lb>1'] else 'not met'}, (ii) {'met' if v['ii_DL-DF_lb>0'] else 'not met'}, half of CF with lower bound > 0: {v['half_of_cf']}" for nm, v in out[bk]["rules"].items()), ""]
L += ["## Selected penalties (λ_text, λ_rater, λ_W) and adaptation strength at k = 20", "", "| rung | fold | DL | DL strength | L | L strength | DF strength |", "|---" * 7 + "|"]
for t, nm in (("id", "L1"), ("ida", "L1-fix-a"), ("idb", "L1-fix-b")):
    for s in out["selected"][t]: L.append(f"| {nm} | {s['fold']} | {s['lam'].get('DL')} | {s['lam_adapt'].get('DL_20')} | {s['lam'].get('L', '—')} | {s['lam_adapt'].get('L_20', '—')} | {s['lam_adapt'].get('DF_20')} |")
json.dump(out, open(f"{R}/stage14_fix.json", "w"), indent=1); open(f"{R}/stage14_fix.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
