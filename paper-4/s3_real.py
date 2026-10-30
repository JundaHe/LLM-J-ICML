"""Stage 3 Amendment 4: real MultiPref with the permutation control, placed on the synthetic dose-response (τ0 … τ20): own − other direction accuracy at k = 20 / 50."""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); rng = np.random.RandomState(17)
meta = json.load(open(f"{R}/synth/synth_meta.json"))
def rows_of(pattern): return [r for f in sorted(glob.glob(pattern)) for r in json.load(open(f))["per_rater"]]
def permc(rows, m, k):
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k and f"{m}_perm_dir" in r: by[(r["fold"], r["rater"])].append(r)
    q = [z for z in by if np.mean([x["n_dir"] for x in by[z]]) > 0]
    if not q: return None
    d = np.array([np.mean([x[f"{m}_dir"] - x[f"{m}_perm_dir"] for x in by[z]]) for z in q]); w = np.array([np.mean([x["n_dir"] for x in by[z]]) for z in q])
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]
    return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), len(q), sorted({z[0] for z in q})]
SRC = [("real MultiPref", None, f"{R}/stage2a_multipref_overall_A5perm_f?.json", f"{R}/stage2c_E1_f?_perm.json")] + \
      [(f"synthetic {t}", t, f"{R}/stage2a_multipref_synth_{t}_f?.json", f"{R}/stage2c_multipref_synth_{t}_E1_f?.json") for t in ("t0", "t2", "t5", "t10", "t20") if t in meta]
fmt = lambda v: "—" if v is None else f"{100 * v[0]:+.2f} [{100 * v[1]:+.2f}, {100 * v[2]:+.2f}] (folds {v[4]})"
L = ["# Stage 3 — real data on the synthetic dose-response (own − other rater's k ratings, direction accuracy, points; rater bootstrap)", "",
     "| panel | generator-oracle gain | DL (tuned), k = 20 | VPL, k = 20 | PAL-B, k = 20 | VPL, k = 50 | PAL-B, k = 50 |", "|---|---|---|---|---|---|---|"]; out = {}
for name, t, pf, pv in SRC:
    fr, vr = rows_of(pf), rows_of(pv); c = {"DL20": permc(fr, "DL", 20), "VPL20": permc(vr, "VPL", 20), "PAL20": permc(vr, "PAL2", 20), "VPL50": permc(vr, "VPL", 50), "PAL50": permc(vr, "PAL2", 50)}
    out[name] = c; og = "—" if t is None else f"+{100 * meta[t]['oracle_gain_realised']:.1f}"
    L.append(f"| {name} | {og} | " + " | ".join(fmt(c[k]) for k in ("DL20", "VPL20", "PAL20", "VPL50", "PAL50")) + " |")
json.dump(out, open(f"{R}/stage3_real_vs_dose.json", "w"), indent=1); open(f"{R}/stage3_real_vs_dose.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
