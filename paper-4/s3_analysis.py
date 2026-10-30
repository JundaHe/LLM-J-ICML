"""Stage 3 S3-P analysis (PROTOCOL_STAGE3.md): per synthetic strength τ, each learner's own direction-accuracy gain m(k) − m(0) (paired per rater, rater bootstrap),
the τ0 sanity check and the pre-fixed power rule (some content-interacting learner with lower bound > +0.01 at k = 20)."""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); rng = np.random.RandomState(13)
meta = json.load(open(f"{R}/synth/synth_meta.json")); out = {}; L = ["# Stage 3 S3-P — semi-synthetic positive control (MultiPref structure)", ""]
def rows_of(pattern):
    rr = []
    for f in sorted(glob.glob(pattern)): rr += json.load(open(f))["per_rater"]
    return rr
def own(rows, m, k):
    by0 = {(r["fold"], r["rater"]): r for r in rows if r["k"] == 0}; byk = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k and (r["fold"], r["rater"]) in by0: byk[(r["fold"], r["rater"])].append(r)
    q = [z for z in byk if np.mean([x["n_dir"] for x in byk[z]]) > 0]
    d = np.array([np.mean([x[f"{m}_dir"] for x in byk[z]]) - by0[z][f"{m}_dir"] * np.mean([x["n_dir"] for x in byk[z]]) / max(1, by0[z]["n_dir"]) for z in q]); w = np.array([np.mean([x["n_dir"] for x in byk[z]]) for z in q])
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]
    return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], len(q)
def permc(rows, m, k):                                                    # Stage 3 Am. 1 primary: own k ratings − another test rater's k ratings (same fold, k, draw)
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k and f"{m}_perm_dir" in r: by[(r["fold"], r["rater"])].append(r)
    q = [z for z in by if np.mean([x["n_dir"] for x in by[z]]) > 0]
    d = np.array([np.mean([x[f"{m}_dir"] - x[f"{m}_perm_dir"] for x in by[z]]) for z in q]); w = np.array([np.mean([x["n_dir"] for x in by[z]]) for z in q])
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]
    return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
fmt = lambda v: f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]"
L += ["| τ panel | τ | generator-oracle gain | learner | **own − other rater, dir., k = 20 (primary)** | own − other, k = 50 | own gain k = 20 | own gain k = 50 | raters |", "|---|---|---|---|---|---|---|---|---|"]
for t in ("t0", "t2", "t5"):
    fr = rows_of(f"{R}/stage2a_multipref_synth_{t}_f?.json"); vr = rows_of(f"{R}/stage2c_multipref_synth_{t}_E1_f?.json")
    for src, rows, models in (("factorised", fr, ("DFs", "DL")), ("per-response", vr, ("DFsp", "VPL", "PAL2"))):
        if not rows: continue
        for mdl in models:
            if f"{mdl}_dir" not in rows[0]: continue
            g20, nq = own(rows, mdl, 20); g50, _ = own(rows, mdl, 50); p20 = permc(rows, mdl, 20); p50 = permc(rows, mdl, 50)
            out[f"{t}_{mdl}"] = {"perm20": p20, "perm50": p50, "own20": g20, "own50": g50, "n": nq}
            L.append(f"| {t} | {meta[t]['tau']:.3f} | {meta[t]['oracle_gain_realised']:+.4f} | {mdl} ({src}) | {fmt(p20)} | {fmt(p50)} | {fmt(g20)} | {fmt(g50)} | {nq} |")
L.append("")
content = ("DL", "VPL", "PAL2")
san = [k for k, v in out.items() if k.startswith("t0_") and not (v["perm20"][1] <= 0.005 and v["perm20"][2] >= -0.005)]
L.append(f"**Sanity (τ0, primary contrast):** every learner's k = 20 interval contains a value within ±0.005 of 0: {'yes' if not san else 'NO — ' + ', '.join(san) + ' (S3-P not usable per protocol)'}.")
for t in ("t2", "t5"):
    pw = [m for m in content if f"{t}_{m}" in out and out[f"{t}_{m}"]["perm20"][1] > 0.01]
    out[f"power_{t}"] = pw; L.append(f"**Power at {t}:** content-interacting learners with lower bound > +0.01 at k = 20: {', '.join(pw) if pw else 'none'}.")
json.dump(out, open(f"{R}/stage3_s3p.json", "w"), indent=1); open(f"{R}/stage3_s3p.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
