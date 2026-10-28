"""Stage 2c Amendment 4 analysis (PROTOCOL_STAGE2C.md): PRISM pairs. R1 (primary): each method's own improvement in the new user's binary choice accuracy, method(k) − method(0),
paired per user, rater-cluster bootstrap; the ranking null is stated only if every method's k = 20 upper 95 % bound is below +0.01. Graded-label (E1) LL and direction reported alongside."""
import json, glob, os, sys, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); rng = np.random.RandomState(7); out = {}; L = []
TAG = sys.argv[1] if len(sys.argv) > 1 else ""
fmt = lambda v: f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]"
def load(ev):
    fs = sorted(glob.glob(f"{R}/stage2c_prism_pairs_{ev}_f?{TAG}.json")); rows = []
    for f in fs: rows.extend(json.load(open(f))["per_rater"])
    return rows, [int(f.split("_f")[-1][0]) for f in fs]
def boot(d, w):
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]; return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
def per_user(rows, k, key, den):                                           # per-user mean over draws of (sum of metric, sum of denominator)
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k: by[(r["fold"], r["rater"])].append(r)
    return {z: (np.mean([x[key] for x in v]), np.mean([x[den] for x in v])) for z, v in by.items()}
def own_gain(rows, k, m, mt, den):                                         # m(k) − m(0) on the same user's test items, rate scale
    a, b = per_user(rows, k, f"{m}_{mt}", den), per_user(rows, 0, f"{m}_{mt}", den); q = [z for z in a if z in b and a[z][1] > 0]
    d = np.array([a[z][0] - b[z][0] * a[z][1] / b[z][1] for z in q]); w = np.array([a[z][1] for z in q]); return boot(d, w)
def contrast(rows, k, m1, m2, mt, den):
    a, b = per_user(rows, k, f"{m1}_{mt}", den), per_user(rows, k, f"{m2}_{mt}", den); q = [z for z in a if a[z][1] > 0]
    return boot(np.array([a[z][0] - b[z][0] for z in q]), np.array([a[z][1] for z in q]))
def level(rows, k, m, mt, den): rr = [r for r in rows if r["k"] == k]; return sum(r[f"{m}_{mt}"] for r in rr) / max(1, sum(r[den] for r in rr))
for ev in ("E2", "E1"):
    rows, folds = load(ev)
    if not rows: continue
    M = [m for m in ("Dp", "DFp", "DFsp", "VPL", "VPLs", "PAL2", "PAL4") if f"{m}_ll" in rows[0]]; den = "n" if ev == "E2" else "n_dir"; acc = "acc" if ev == "E2" else "dir"
    KS = sorted(set(r["k"] for r in rows)); nu = len({(r["fold"], r["rater"]) for r in rows})
    L += [f"## {ev} ({'binary: the user’s native choice' if ev == 'E2' else 'graded 5-level score-difference label'}) — folds {folds}, {nu} new users", "",
          "| k | " + " | ".join(f"LL {m}" for m in M) + " | " + " | ".join(f"{acc} {m}" for m in M) + " |", "|---" * (1 + 2 * len(M)) + "|"]
    for k in KS: L.append(f"| {k} | " + " | ".join(f"{level(rows, k, m, 'll', 'n'):.4f}" for m in M) + " | " + " | ".join(f"{level(rows, k, m, 'dir', den):.4f}" for m in M) + " |")
    L += ["", f"**Own personalisation gain, method(k) − method(0)** — {acc} (R1 for E2) and LL per rating", "", "| k | " + " | ".join(f"{acc} {m}" for m in M if m != "Dp") + " | " + " | ".join(f"LL {m}" for m in M if m != "Dp") + " |", "|---" * (1 + 2 * (len(M) - 1)) + "|"]
    for k in [k for k in KS if k > 0]:
        cells = []
        for mt, dn in (("dir", den), ("ll", "n")):
            for m in M:
                if m == "Dp": continue
                v = own_gain(rows, k, m, mt, dn); out[f"{ev}_k{k}_{m}_own_{mt}"] = v; cells.append(fmt(v))
        L.append(f"| {k} | " + " | ".join(cells) + " |")
    L += ["", "**Contrasts at the same k**", "", "| k | LL DFsp − VPL | LL DFsp − PAL2 | LL DFsp − Dp | LL VPL − Dp | " + f"{acc} DFsp − Dp | {acc} VPL − Dp | {acc} PAL2 − Dp |", "|---|---|---|---|---|---|---|---|"]
    for k in [k for k in KS if k > 0]:
        cells = []
        for (a, b, mt, dn) in (("DFsp", "VPL", "ll", "n"), ("DFsp", "PAL2", "ll", "n"), ("DFsp", "Dp", "ll", "n"), ("VPL", "Dp", "ll", "n"), ("DFsp", "Dp", "dir", den), ("VPL", "Dp", "dir", den), ("PAL2", "Dp", "dir", den)):
            v = contrast(rows, k, a, b, mt, dn); out[f"{ev}_k{k}_{a}-{b}_{mt}"] = v; cells.append(fmt(v))
        L.append(f"| {k} | " + " | ".join(cells) + " |")
    if ev == "E2" and 20 in KS:
        ub = {m: out[f"E2_k20_{m}_own_dir"][2] for m in M if m != "Dp"}; ok = all(u < 0.01 for u in ub.values())
        L += ["", f"**R1 (k = 20):** upper 95 % bounds of the own accuracy gain: " + ", ".join(f"{m} {u:+.4f}" for m, u in ub.items()) + f" → ranking null {'HOLDS' if ok else 'NOT supported'} on PRISM" + ("" if len(folds) == 5 else f" (INTERIM: folds {folds} only; the criterion applies to all 5 folds)") + "."]
        out["R1_holds"] = ok; out["R1_folds"] = folds
    L.append("")
json.dump(out, open(f"{R}/stage2c_prism_pairs_summary{TAG}.json", "w"), indent=1)
open(f"{R}/stage2c_prism_pairs_summary{TAG}.md", "w").write("# Stage 2c Amendment 4 — PRISM pairs (PROTOCOL_STAGE2C.md)\n\n" + "\n".join(L)); print("\n".join(L))
