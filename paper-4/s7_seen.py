"""Stage 7 S7-3 (PROTOCOL_STAGE7.md Am. 2): seen-rater ceiling on real MultiPref — training raters' ratings of test items with their trained parameters;
model − D and own − other (derangement of training raters), direction accuracy (points) and LL (nats per rating), rater bootstrap (seed 17)."""
import json, glob, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
rows = [r for f in sorted(glob.glob(f"{R}/stage2a_multipref_overall_seen_f?.json")) for r in json.load(open(f)).get("seen_per_rater", [])]
def boot(d, w, sc):
    rng = np.random.RandomState(17); bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]
    return [sc * d.sum() / w.sum(), sc * np.percentile(bs, 2.5), sc * np.percentile(bs, 97.5)]
fmt = lambda v: f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
nd, nn = np.array([r["n_dir"] for r in rows], float), np.array([r["n"] for r in rows], float); out = {}
L = ["# Stage 7 S7-3 — seen-rater ceiling, real MultiPref (training raters × test items; trained rater parameters)", "",
     f"{len(rows)} rater-folds, folds {sorted({r['fold'] for r in rows})}; median training ratings per rater {np.median([r['n_train'] for r in rows]):.0f}, median test-item ratings {np.median(nn):.0f}.", "",
     "| model | direction acc. | − D, direction (points) | own − other, direction (points) | − D, LL (×100 nats) | own − other, LL (×100 nats) |", "|---|---|---|---|---|---|"]
for m in ("D", "DF", "DFs", "DL"):
    if f"{m}_dir" not in rows[0]: continue
    c = {"acc": 100 * sum(r[f"{m}_dir"] for r in rows) / nd.sum()}
    if m != "D":
        c["vsD_dir"] = boot(np.array([r[f"{m}_dir"] - r["D_dir"] for r in rows]), nd, 100); c["vsD_ll"] = boot(np.array([r[f"{m}_ll"] - r["D_ll"] for r in rows]), nn, 100)
        c["perm_dir"] = boot(np.array([r[f"{m}_dir"] - r[f"{m}_perm_dir"] for r in rows]), nd, 100); c["perm_ll"] = boot(np.array([r[f"{m}_ll"] - r[f"{m}_perm_ll"] for r in rows]), nn, 100)
    out[m] = c
    L.append(f"| {m} | {c['acc']:.2f} | " + " | ".join(fmt(c[k]) if k in c else "—" for k in ("vsD_dir", "perm_dir", "vsD_ll", "perm_ll")) + " |")
rule = bool("DL" in out and out["DL"]["perm_dir"][1] > 1.0); out["rule_DL_seen_detects"] = rule
L += ["", f"**Reading (Am. 2): DL own − other direction lower bound {out['DL']['perm_dir'][1]:+.2f} points → " + ("the ranking null is specific to few-shot new-rater adaptation.**" if rule else "the ranking null also holds for seen raters with all their training ratings.**")]
json.dump(out, open(f"{R}/stage7_seen.json", "w"), indent=1); open(f"{R}/stage7_seen.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
