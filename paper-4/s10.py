"""Stage 10 (PROTOCOL_STAGE10.md): code-readability panels. SE-1: DF − D held-out LL per rating; SE-2: within-rater pairwise concordance (points) — DL / DF own gain
(model(k) − model(0)) and own − other; rater bootstrap (seed 17); decision rules at k = 10 (Dorn) / 20 (Buse–Weimer)."""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
def rows(panel): return [r for f in sorted(glob.glob(f"{R}/stage2a_{panel}_f?.json")) for r in json.load(open(f))["per_rater"]]
def per(rs, k, key, den):
    by = collections.defaultdict(list)
    for r in rs:
        if r["k"] == k and key in r and r.get(den, 0) > 0: by[(r["fold"], r["rater"])].append(r)
    return {z: (np.mean([x[key] for x in v]), np.mean([x[den] for x in v])) for z, v in by.items()}
def boot(d, w, sc=100.0):
    rng = np.random.RandomState(17); bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]
    return [sc * d.sum() / w.sum(), sc * np.percentile(bs, 2.5), sc * np.percentile(bs, 97.5), len(d)]
def diff(rs, k1, key1, k2, key2, den):
    a, b = per(rs, k1, key1, den), per(rs, k2, key2, den); q = [z for z in a if z in b]
    return boot(np.array([a[z][0] - b[z][0] * a[z][1] / b[z][1] for z in q]), np.array([a[z][1] for z in q])) if q else None
fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}] (n = {v[3]})"
L = ["# Stage 10 — code readability, new developers (LL ×100 nats per rating; concordance in points; 95 % rater bootstrap)", "",
     "| panel | k | DF − D, LL | DL − D, LL | DL own gain, concordance | DL own − other, concordance | DF own − other, concordance | D concordance |", "|---|---|---|---|---|---|---|---|"]; out = {}
for panel, ks, kr in (("bw_raters", (5, 10, 20, 50), 20), ("dorn_raters", (5, 10), 10)):
    rs = rows(panel)
    if not rs: continue
    for k in ks:
        c = {"DF-D_ll": diff(rs, k, "DF_ll", k, "D_ll", "n"), "DL-D_ll": diff(rs, k, "DL_ll", k, "D_ll", "n"), "DL_own_conc": diff(rs, k, "DL_conc", 0, "DL_conc", "conc_den"),
             "DL_perm_conc": diff(rs, k, "DL_conc", k, "DL_perm_conc", "conc_den"), "DF_perm_conc": diff(rs, k, "DF_conc", k, "DF_perm_conc", "conc_den")}
        dc = per(rs, k, "D_conc", "conc_den"); c["D_conc"] = 100 * sum(v[0] for v in dc.values()) / max(1e-9, sum(v[1] for v in dc.values())); out[f"{panel}_k{k}"] = c
        L.append(f"| {panel} | {k} | {fmt(c['DF-D_ll'])} | {fmt(c['DL-D_ll'])} | {fmt(c['DL_own_conc'])} | {fmt(c['DL_perm_conc'])} | {fmt(c['DF_perm_conc'])} | {c['D_conc']:.1f} |")
    c = out.get(f"{panel}_k{kr}")
    if c:
        se1 = bool(c["DF-D_ll"][1] > 0); lb = max(c["DL_own_conc"][1], c["DL_perm_conc"][1]); ub = max(c["DL_own_conc"][2], c["DL_perm_conc"][2])
        se2 = "degenerate (DL switched off by validation; Am. 3)" if max(abs(x) for x in c["DL-D_ll"][:3]) < 1e-2 else ("content personalisation detected" if lb > 1 else ("ranking null" if ub < 1 else "inconclusive")); out[f"rules_{panel}"] = {"SE1": se1, "SE2": se2}
        L += ["", f"**{panel}, k = {kr}: SE-1 {'holds' if se1 else 'does not hold'} (DF − D lower bound {c['DF-D_ll'][1]:+.2f}); SE-2: {se2} (largest lower bound {lb:+.2f}, largest upper bound {ub:+.2f}).**", ""]
json.dump(out, open(f"{R}/stage10_se.json", "w"), indent=1); open(f"{R}/stage10_se.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
