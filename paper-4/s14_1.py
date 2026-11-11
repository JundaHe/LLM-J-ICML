"""Stage 14 S14-1 summary (PROTOCOL_STAGE14.md §1.5–1.6): Jester positive control. Within-rater pairwise concordance in points, rater bootstrap over (fold, rater), seed 17,
B = 2000, support draws averaged within rater. Rungs: L0 (linear CF reference, seen jokes), L1 (pipeline DL, item-identity features, seen jokes), L1b (pipeline at the
selected PCA dimension, seen jokes), L2 (pipeline at the selected PCA dimension, held-out jokes) + CF-text and ISO diagnostics. Rules at k = 20."""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); KS = (5, 10, 20, 50); KR = 20
def rows(tag): return [r for f in sorted(glob.glob(f"{R}/stage2a_jester_raters_{tag}_f?.json")) for r in json.load(open(f))["per_rater"]]
def folds(tag): return [fo for f in sorted(glob.glob(f"{R}/stage2a_jester_raters_{tag}_f?.json")) for fo in json.load(open(f))["folds"]]
def lin(rs, terms, den, sc=100.0):
    """Σ coef · (per-rater draw-mean of key at k), every term rescaled to the first term's denominator; ratio estimator and rater bootstrap"""
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
fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
ID, XS, CF = rows("id"), rows("xs"), json.load(open(f"{R}/stage14_cf.json")); out = {"xd_selected": [fo["xd"] for fo in folds("xs")], "xd_val": [fo["xd_val"] for fo in folds("xs")], "lam_id": [fo["lam"] for fo in folds("id")], "lam_xs": [fo["lam"] for fo in folds("xs")], "cf_sel": [fo["sel"] for fo in CF["folds"]]}
# the CF reference must have used the pipeline's support draws: identical seen-cell denominators
a = {(r["fold"], r["k"], r["draw"], r["rater"]): r["sconc_den"] for r in ID if r["k"] > 0}; b = {(r["fold"], r["k"], r["draw"], r["rater"]): r["den_s"] for r in CF["per_rater"]}
out["support_draws_identical"] = bool(a == b); assert out["support_draws_identical"], "CF and pipeline support draws differ"
def seen(rs, m, k): return lin(rs, [(1, k, f"{m}_sconc"), (-1, k, f"{m}_s0conc")], "sconc_den")
def seen_dd(rs, k): return lin(rs, [(1, k, "DL_sconc"), (-1, k, "DL_s0conc"), (-1, k, "DF_sconc"), (1, k, "DF_s0conc")], "sconc_den")
def held(rs, m, k): return lin(rs, [(1, k, f"{m}_conc"), (-1, 0, f"{m}_conc")], "conc_den")
def held_dd(rs, k): return lin(rs, [(1, k, "DL_conc"), (-1, 0, "DL_conc"), (-1, k, "DF_conc"), (1, 0, "DF_conc")], "conc_den")
for k in KS:
    c = {"L0_cf_own-mu": lin(CF["per_rater"], [(1, k, "cf_conc"), (-1, k, "mu_conc")], "den_s"), "L0_mu_level": lin(CF["per_rater"], [(1, k, "mu_conc")], "den_s"),
         "L1_DL_own-mu": seen(ID, "DL", k), "L1_DF_own-mu": seen(ID, "DF", k), "L1_DL-DF": seen_dd(ID, k), "L1_DL_own-other": lin(ID, [(1, k, "DL_sconc"), (-1, k, "DL_perm_sconc")], "sconc_den"), "L1_DL_prior_level": lin(ID, [(1, k, "DL_s0conc")], "sconc_den"),
         "L1b_DL_own-mu": seen(XS, "DL", k), "L1b_DF_own-mu": seen(XS, "DF", k), "L1b_DL-DF": seen_dd(XS, k),
         "L2_DL_own-mu": held(XS, "DL", k), "L2_DF_own-mu": held(XS, "DF", k), "L2_DL-DF": held_dd(XS, k), "L2_DL_own-other": lin(XS, [(1, k, "DL_conc"), (-1, k, "DL_perm_conc")], "conc_den"), "L2_D_level": lin(XS, [(1, k, "D_conc")], "conc_den"),
         "L2_cftext_own-mu": lin(CF["per_rater"], [(1, k, "cft_conc"), (-1, k, "mut_conc")], "den_t"), "L2_iso_own-mu": lin(CF["per_rater"], [(1, k, "iso_conc"), (-1, k, "mut_conc")], "den_t"), "L2_mutext_level": lin(CF["per_rater"], [(1, k, "mut_conc")], "den_t"),
         "L2_LL_DL-DF": lin(XS, [(1, k, "DL_ll"), (-1, k, "DF_ll")], "n"), "L2_LL_DF-D": lin(XS, [(1, k, "DF_ll"), (-1, k, "D_ll")], "n"), "L1_LL_DL-DF": lin(ID, [(1, k, "DL_sll"), (-1, k, "DF_sll")], "ns")}
    out[f"k{k}"] = c
c = out[f"k{KR}"]; l0 = c["L0_cf_own-mu"][1] > 1; l1 = c["L1_DL_own-mu"][1] > 1 and c["L1_DL-DF"][1] > 0; l2 = c["L2_DL_own-mu"][1] > 1 and c["L2_DL-DF"][1] > 0
reading = "R1" if not l0 else ("R2" if l2 else ("R3" if l1 else "R4")); out["rules"] = {"L0_passes": bool(l0), "L1_detects": bool(l1), "L2_detects": bool(l2), "cftext_passes": bool(c["L2_cftext_own-mu"][1] > 1), "reading": reading,
                                                                                      "DL_gain_over_CF_gain_L1": c["L1_DL_own-mu"][0] / c["L0_cf_own-mu"][0], "DL_gain_over_CF_gain_L2": c["L2_DL_own-mu"][0] / c["L0_cf_own-mu"][0]}
L = ["# Stage 14 S14-1 — Jester positive control (within-rater concordance, points; 95 % rater bootstrap; LL ×100 nats per rating)", "",
     f"PCA dimension selected per fold (L2 run): {out['xd_selected']}; support draws identical between CF and pipeline: {out['support_draws_identical']}; raters: {c['L0_cf_own-mu'][3]}", ""]
for title, keys in (("Seen jokes (own − μ unless stated)", ("L0_cf_own-mu", "L1_DL_own-mu", "L1_DF_own-mu", "L1_DL-DF", "L1_DL_own-other", "L1b_DL_own-mu", "L1b_DL-DF")),
                    ("Held-out jokes (own − μ unless stated)", ("L2_DL_own-mu", "L2_DF_own-mu", "L2_DL-DF", "L2_DL_own-other", "L2_cftext_own-mu", "L2_iso_own-mu")),
                    ("Levels and log-likelihood", ("L0_mu_level", "L1_DL_prior_level", "L2_D_level", "L2_mutext_level", "L2_LL_DL-DF", "L2_LL_DF-D", "L1_LL_DL-DF"))):
    L += [f"**{title}**", "", "| k | " + " | ".join(keys) + " |", "|---" * (len(keys) + 1) + "|"] + [f"| {k} | " + " | ".join(fmt(out[f"k{k}"][q]) for q in keys) + " |" for k in KS] + [""]
L += [f"**Rules at k = {KR}: L0 {'passes' if l0 else 'fails'}; L1 {'detects' if l1 else 'does not detect'}; L2 {'detects' if l2 else 'does not detect'}; CF-text {'passes' if out['rules']['cftext_passes'] else 'does not pass'} → reading {reading}.**"]
json.dump(out, open(f"{R}/stage14_1.json", "w"), indent=1); open(f"{R}/stage14_1.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
