"""B3 (PROTOCOL_STAGE2B.md): RC-LoRA (in-context personalisation) vs DFs / DF / D on the same new raters, folds, k and draw 0 (paired rater-cluster bootstrap)."""
import json, glob, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
VAR = sys.argv[1] if len(sys.argv) > 1 else ""                           # Amendment 2: "" (primary), "s3000f3" (fold 3 = second seed), "best" (per fold, the better seed vs D-LoRA; favourable to RC)
rc = [r for f in sorted(glob.glob(f"{R}/lora_rm/multipref_overall/rc_f*/meta.json")) for r in json.load(open(f)).get("per_rater", [])]
refs = {"frozen": json.load(open(f"{R}/stage2a_multipref_overall.json"))["per_rater"], "lora": json.load(open(f"{R}/stage2a_multipref_overall_lora.json"))["per_rater"]}
if VAR:
    alt = [r for f in sorted(glob.glob(f"{R}/lora_rm/multipref_overall/rc_s3000_f*/meta.json")) for r in json.load(open(f)).get("per_rater", [])]
    def gain(rows, f):                                                    # fold-level RC − D-LoRA, LL per rating, k = 20
        lo = {(r["fold"], r["rater"]): r for r in refs["lora"] if r["k"] == 20 and r["draw"] == 0}; q = [r for r in rows if r["fold"] == f and r["k"] == 20 and (f, r["rater"]) in lo]
        return sum(r["RC_ll"] - lo[(f, r["rater"])]["D_ll"] for r in q) / sum(r["n"] for r in q)
    for f in sorted({r["fold"] for r in alt}):
        g0, g1 = gain(rc, f), gain(alt, f); print(f"fold {f}: RC − D-LoRA seed 2000 {g0:+.4f}, seed 3000 {g1:+.4f}")
        if VAR == "s3000f3" or (VAR == "best" and g1 > g0): rc = [r for r in rc if r["fold"] != f] + [r for r in alt if r["fold"] == f]
    if VAR in ("s4000", "seedavg3"):                                      # Amendment 4: (b') seed 4000 on every fold; three-seed per-rater mean
        alt4 = [r for f in sorted(glob.glob(f"{R}/lora_rm/multipref_overall/rc_s4000_f*/meta.json")) for r in json.load(open(f)).get("per_rater", [])]
        assert sorted({r["fold"] for r in alt4}) == [0, 1, 2, 3, 4] and sorted({r["fold"] for r in alt}) == [0, 1, 2, 3, 4], "seeds not complete on all folds"
        for f in range(5): print(f"fold {f}: RC − D-LoRA seeds 2000/3000/4000 {gain(rc, f):+.4f} / {gain(alt, f):+.4f} / {gain(alt4, f):+.4f}")
        if VAR == "s4000": rc = alt4
        else:
            a3, a4 = ({(r["fold"], r["k"], r["rater"]): r for r in x} for x in (alt, alt4))
            rc = [{**r, **{f"RC_{m}": (r[f"RC_{m}"] + a3[z][f"RC_{m}"] + a4[z][f"RC_{m}"]) / 3 for m in ("ll", "dir", "rps")}} for r in rc for z in [(r["fold"], r["k"], r["rater"])] if z in a3 and z in a4]
    if VAR in ("s3000", "seedavg"):                                       # Amendment 3: (b) seed 3000 on every fold; (c) per-rater mean of the two seeds' metrics
        assert sorted({r["fold"] for r in alt}) == [0, 1, 2, 3, 4], "second seed not complete on all folds"
        if VAR == "s3000": rc = alt
        else:
            a2 = {(r["fold"], r["k"], r["rater"]): r for r in alt}
            rc = [{**r, **{f"RC_{m}": 0.5 * (r[f"RC_{m}"] + a2[(r["fold"], r["k"], r["rater"])][f"RC_{m}"]) for m in ("ll", "dir", "rps")}} for r in rc if (r["fold"], r["k"], r["rater"]) in a2]
rng = np.random.RandomState(7); out = {}; lines = ["| k | head | model | RC − model, LL/rating [95 %] | RC − model, direction acc. | raters |", "|---|---|---|---|---|---|"]
for k in sorted({r["k"] for r in rc}):
    rck = {(r["fold"], r["rater"]): r for r in rc if r["k"] == k}
    for head, rows in refs.items():
        rf = {(r["fold"], r["rater"]): r for r in rows if r["k"] == k and r["draw"] == 0}
        q = sorted(set(rck) & set(rf))
        for mdl in ("DFs", "DF", "D"):
            res = []
            for mt, den in (("ll", "n"), ("dir", "n_dir")):
                d = np.array([rck[z][f"RC_{mt}"] - rf[z][f"{mdl}_{mt}"] for z in q]); w = np.array([rf[z][den] for z in q])
                bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; res.append((d.sum() / w.sum(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
            out[f"k{k}_{head}_{mdl}"] = {"ll": res[0], "dir": res[1], "n_raters": len(q)}
            lines.append(f"| {k} | {head} | {mdl} | {res[0][0]:+.4f} [{res[0][1]:+.4f}, {res[0][2]:+.4f}] | {res[1][0]:+.4f} [{res[1][1]:+.4f}, {res[1][2]:+.4f}] | {len(q)} |")
json.dump(out, open(f"{R}/stage2b_B3{VAR and "_" + VAR}.json", "w"), indent=1); open(f"{R}/stage2b_B3{VAR and "_" + VAR}.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
