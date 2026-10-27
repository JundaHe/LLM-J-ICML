"""B3 (PROTOCOL_STAGE2B.md): RC-LoRA (in-context personalisation) vs DFs / DF / D on the same new raters, folds, k and draw 0 (paired rater-cluster bootstrap)."""
import json, glob, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
rc = [r for f in sorted(glob.glob(f"{R}/lora_rm/multipref_overall/rc_f*/meta.json")) for r in json.load(open(f)).get("per_rater", [])]
refs = {"frozen": json.load(open(f"{R}/stage2a_multipref_overall.json"))["per_rater"], "lora": json.load(open(f"{R}/stage2a_multipref_overall_lora.json"))["per_rater"]}
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
json.dump(out, open(f"{R}/stage2b_B3.json", "w"), indent=1); open(f"{R}/stage2b_B3.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
