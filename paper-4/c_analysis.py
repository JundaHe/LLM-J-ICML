"""Stage 2c analysis (PROTOCOL_STAGE2C.md): C1 (E1 graded: DFs vs VPL / PAL), C2 (E2 binary: style gain vanishes), C3 (VPL / PAL user latents vs DF/DFs style offsets: cross-validated R², rater bootstrap)."""
import json, glob, os, sys, collections, numpy as np
TAG = sys.argv[1] if len(sys.argv) > 1 else ""
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); rng = np.random.RandomState(7); out = {}; L = []
def load(ev): rows = []; lat = []; [ (rows.extend(d["per_rater"]), lat.extend(d["latents"])) for d in (json.load(open(f)) for f in sorted(glob.glob(f"{R}/stage2c_{ev}_f?{TAG}.json")))]; return rows, lat
def diff(rows, k, a, b, mt, den):
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k: by[(r["fold"], r["rater"])].append(r)
    q = list(by); d = np.array([np.mean([x[f"{a}_{mt}"] - x[f"{b}_{mt}"] for x in by[z]]) for z in q]); w = np.array([np.mean([x[den] for x in by[z]]) for z in q])
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], len(q)
def level(rows, k, a, mt, den):
    rr = [r for r in rows if r["k"] == k]; return sum(r[f"{a}_{mt}"] for r in rr) / sum(r[den] for r in rr)
fmt = lambda v: f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]"
for ev in ("E1", "E2"):
    rows, lat = load(ev); M = [m for m in ("Dp", "DFp", "DFsp", "VPL", "PAL2", "PAL4")]
    L += [f"## {ev} ({'graded 5-level' if ev == 'E1' else 'binary, ties dropped'})", "", "| k | " + " | ".join(f"LL {m}" for m in M) + " | " + " | ".join(f"{'dir' if ev=='E1' else 'acc'} {m}" for m in M) + " |", "|---" * (1 + 2 * len(M)) + "|"]
    for k in ((0, 5, 10, 20, 50) if any(r["k"] == 0 for r in rows) else (5, 10, 20, 50)):
        L.append(f"| {k} | " + " | ".join(f"{level(rows, k, m, 'll', 'n'):.4f}" for m in M) + " | " + " | ".join(f"{level(rows, k, m, 'dir', 'n_dir' if ev == 'E1' else 'n'):.3f}" for m in M) + " |")
    L += ["", "| k | DFsp − VPL | DFsp − PAL2 | DFsp − PAL4 | DFsp − Dp | VPL − Dp | PAL2 − Dp | acc/dir: DFsp − Dp | acc/dir: DFsp − VPL |", "|---|---|---|---|---|---|---|---|---|"]
    for k in (5, 10, 20, 50):
        cells = []
        for a, b in (("DFsp", "VPL"), ("DFsp", "PAL2"), ("DFsp", "PAL4"), ("DFsp", "Dp"), ("VPL", "Dp"), ("PAL2", "Dp")):
            v, nq = diff(rows, k, a, b, "ll", "n"); out[f"{ev}_k{k}_{a}-{b}_ll"] = v; cells.append(fmt(v))
        for a, b in (("DFsp", "Dp"), ("DFsp", "VPL")):
            v, nq = diff(rows, k, a, b, "dir", "n_dir" if ev == "E1" else "n"); out[f"{ev}_k{k}_{a}-{b}_dir"] = v; cells.append(fmt(v))
        L.append(f"| {k} | " + " | ".join(cells) + " |")
    if any(r["k"] == 0 for r in rows):                                    # own personalisation gain: method(k) − method(0), per rater (paired)
        L += ["", "| k | own gain Dp→DFsp (vs DFsp k=0) | VPL(k) − VPL(0) | PAL2(k) − PAL2(0) | PAL4(k) − PAL4(0) |", "|---|---|---|---|---|"]
        z0 = {(r["fold"], r["rater"]): r for r in rows if r["k"] == 0}
        for k in (5, 10, 20, 50):
            cells = []
            for mm in ("DFsp", "VPL", "PAL2", "PAL4"):
                by = collections.defaultdict(list)
                for r in rows:
                    if r["k"] == k and (r["fold"], r["rater"]) in z0: by[(r["fold"], r["rater"])].append(r)
                q = list(by); d = np.array([np.mean([x[f"{mm}_ll"] for x in by[z]]) / np.mean([x["n"] for x in by[z]]) * np.mean([x["n"] for x in by[z]]) - z0[z][f"{mm}_ll"] * np.mean([x["n"] for x in by[z]]) / z0[z]["n"] for z in q]); w = np.array([np.mean([x["n"] for x in by[z]]) for z in q])
                bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; v = [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
                out[f"{ev}_k{k}_{mm}_owngain"] = v; cells.append(fmt(v))
            L.append(f"| {k} | " + " | ".join(cells) + " |")
    L.append("")
    if ev == "E1":                                                        # C3: latents at k = 50, draw 0
        X = {"DFs": np.array([r["DFs"] for r in lat]), "DF": np.array([r["DF"] for r in lat])}; L += ["### C3 — how much of each user representation is response style (5-fold CV R², ridge; rater bootstrap of the CV R²)", "", "| user representation | predictors | R² [95 %] | n raters |", "|---|---|---|---|"]
        for key in ("VPL", "PAL2", "PAL4"):
            Z = np.array([r[key] for r in lat])
            if key.startswith("PAL"): Z = Z[:, :-1]                       # softmax weights: drop one redundant coordinate
            Zs = (Z - Z.mean(0)) / (Z.std(0) + 1e-9)
            from numpy.linalg import svd
            if Zs.shape[1] > 20: U, S, Vt = svd(Zs, full_matrices=False); Zs = U[:, :10] * S[:10]; Zs = (Zs - Zs.mean(0)) / Zs.std(0)      # VPL: top-10 PCs of z (variance-weighted R² over them)
            for pk, P in X.items():
                Ps = np.c_[(P - P.mean(0)) / (P.std(0) + 1e-9), np.ones(len(P))]; n_ = len(P); fold = np.arange(n_) % 5; rng.shuffle(fold); pred = np.zeros_like(Zs)
                for g in range(5):
                    tr, te = fold != g, fold == g; B = np.linalg.solve(Ps[tr].T @ Ps[tr] + 1.0 * np.eye(Ps.shape[1]), Ps[tr].T @ Zs[tr]); pred[te] = Ps[te] @ B
                res = (Zs - pred) ** 2; tot = (Zs - Zs.mean(0)) ** 2; r2 = 1 - res.sum() / tot.sum()
                bs = [1 - res[ix].sum() / tot[ix].sum() for ix in (rng.randint(0, n_, n_) for _ in range(2000))]
                out[f"C3_{key}_{pk}"] = [float(r2), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]; L.append(f"| {key}{' (top-10 PCs of z)' if key == 'VPL' else ''} | {pk} offsets | {r2:.3f} [{np.percentile(bs, 2.5):.3f}, {np.percentile(bs, 97.5):.3f}] | {n_} |")
        L.append("")
json.dump(out, open(f"{R}/stage2c_summary{TAG}.json", "w"), indent=1); open(f"{R}/stage2c_summary{TAG}.md", "w").write("# Stage 2c — VPL / PAL-B vs the style model, new raters (PROTOCOL_STAGE2C.md)\n\n" + "\n".join(L)); print("\n".join(L))
