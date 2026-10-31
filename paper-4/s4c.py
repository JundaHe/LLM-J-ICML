"""Stage 4 S4-C (PROTOCOL_STAGE4.md Amendment 2): own − other direction accuracy of the learned personalisers on conflict items (the rater's own aspect labels point in
opposite directions) vs the rest, real MultiPref, from per-rating dumps with permutation-control predictions."""
import os, sys, json, glob, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
LV = {"A-is-clearly-better": -2, "A-is-slightly-better": -1, "Tie": 0, "B-is-slightly-better": 1, "B-is-clearly-better": 2}
rows = [json.loads(l) for l in open(data_panels.MULTIPREF)]; raters = sorted({a["evaluator"] for r in rows for a in r["normal_worker_annotations"] + r["expert_worker_annotations"]}); rid = {r: j for j, r in enumerate(raters)}
CONF = {}
for i, r in enumerate(rows):
    for a in r["normal_worker_annotations"] + r["expert_worker_annotations"]:
        s = np.sign([LV[a[f"{c}_pref"]] for c in ("helpful", "truthful", "harmless")]); CONF[(i, rid[a["evaluator"]])] = bool((s > 0).any() and (s < 0).any())
s4a = json.load(open(f"{HERE}/results/stage4_s4a.json"))["summary"]; rng = np.random.RandomState(23)
def load(pattern):
    D = [np.load(f) for f in sorted(glob.glob(pattern))]
    return {k: np.concatenate([d[k] for d in D]) for k in D[0].files} if D else None
def contrast(Z, m, k, subset):
    sel = (Z["k"] == k); fo, ra, it = Z["fold"][sel], Z["rater"][sel], Z["item"][sel]; d = Z[f"{m}_dir"][sel] - Z[f"{m}_perm_dir"][sel]
    cf = np.array([CONF[(int(i), int(r))] for i, r in zip(it, ra)]); keep = np.isfinite(d) & (cf if subset == "conflict" else ~cf)
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for f_, r_, i_, v in zip(fo[keep], ra[keep], it[keep], d[keep]): by[(int(f_), int(r_))][int(i_)].append(v)     # draws averaged within rating
    q = list(by); num = np.array([sum(np.mean(v) for v in by[z].values()) for z in q]); den = np.array([len(by[z]) for z in q], float)
    bs = [num[ix].sum() / den[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]
    return [100 * num.sum() / den.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), int(den.sum())]
L = ["# Stage 4 S4-C — own − other direction accuracy (points) on conflict items vs the rest (real MultiPref, permutation control)", "",
     "| learner | k | conflict items | other items | ceiling on conflict items (S4-A, k = all / in-sample) |", "|---|---|---|---|---|"]; out = {}
for name, pat, models in (("factorised (joint features)", f"{HERE}/results/ratings/stage2a_multipref_overall_s4c_f?.npz", ("DFs", "DL")),
                          ("per-response, full features", f"{HERE}/results/ratings/stage2c_E1_f?_s4c.npz", ("DFsp", "VPL", "PAL2"))):
    Z = load(pat)
    if Z is None: L.append(f"| {name}: no dumps yet | | | | |"); continue
    for m in models:
        if f"{m}_perm_dir" not in Z: continue
        for k in (20, 50):
            c, o = contrast(Z, m, k, "conflict"), contrast(Z, m, k, "other"); out[f"{m}_k{k}"] = {"conflict": c, "other": o}
            L.append(f"| {m} ({name}) | {k} | {c[0]:+.2f} [{c[1]:+.2f}, {c[2]:+.2f}] (n = {c[3]}) | {o[0]:+.2f} [{o[1]:+.2f}, {o[2]:+.2f}] | {100*s4a['all']['dir_conflict'][0]:+.1f} / {100*s4a['insample']['dir_conflict'][0]:+.1f} |")
json.dump(out, open(f"{HERE}/results/stage4_s4c.json", "w"), indent=1); open(f"{HERE}/results/stage4_s4c.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
