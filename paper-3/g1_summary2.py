"""G1 summary for Amendment 4 (PROTOCOL_CALIBRATION.md): reads results/pool_adapt_v4/<panel>__<var>/summary.json (pool_adapt2.py) and applies the reading fixed in the
amendment to every pool B × n ∈ {20, 50, all}, without selection:
  (i)  against no adaptation: helps if map-B(n) − none and map-B(n) − map-A both have 95 % intervals below 0; hurts if either is above 0; else no change
  (ii) against generic calibration on the same n pool-B ratings (clim-B, bin-B, qbin-B, refit-B, dir-B, tmix-B): beats if every interval is below 0; worse if any is
       above 0; else equivalent
  (iii) G1 holds iff helps and beats.  Pool shift: none − oracle-B interval above 0 (oracle in ≥ 15 splits). A verdict needs ≥ 15 splits; otherwise "n/a".
Counts separately for real pools, real pools with a shift, and the random-halves nulls. Output: reports/G1_SUMMARY_V2.md + results/pool_adapt_v4/verdicts.json"""
import json, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); RES = f"{HERE}/results/pool_adapt_v4"; NS = ("20", "50", "all"); GEN = ("clim-B", "bin-B", "qbin-B", "refit-B", "dir-B", "tmix-B"); MIN_SPLITS = 15
f4 = lambda v: "—" if v is None else f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]" + ("" if v[3] >= 20 else f" ({v[3]})")
sig = lambda v: "" if v is None else "↓" if v[2] < 0 else "↑" if v[1] > 0 else ""
rows = []
for f in sorted(glob.glob(f"{RES}/*/summary.json")):
    if os.path.basename(os.path.dirname(f)).endswith("_smoke"): continue
    S = json.load(open(f))
    for pool, D in S["pools"].items():
        C = D["contrasts"]; gap = C.get("none - oracle-B"); shift = None if gap is None or gap[3] < MIN_SPLITS else bool(gap[1] > 0)
        for n in NS:
            m = f"map-B({n})"
            if m not in D["arms"]: continue
            vn, va = C.get(f"{m} - none"), C.get(f"{m} - map-A"); g = {b: C.get(f"{m} - {b}({n})") for b in GEN}; ok = D["arms"][m][3] >= MIN_SPLITS and all(v is not None and v[3] >= MIN_SPLITS for v in [vn, va, *g.values()])
            r1 = "n/a" if not ok else "helps" if vn[2] < 0 and va[2] < 0 else "hurts" if vn[1] > 0 or va[1] > 0 else "no change"
            r2 = "n/a" if not ok else "worse" if any(v[1] > 0 for v in g.values()) else "beats" if all(v[2] < 0 for v in g.values()) else "equivalent"
            best = min(GEN, key=lambda b: D["arms"].get(f"{b}({n})", [9])[0])
            rows.append(dict(panel=S["panel"], var=S["var"], pool=pool, null=S["var"] == "random", raters=D["poolB_size"], ncal=D["n_cal_ratings"], nte=D["n_test_ratings"], n=n, gap=gap, shift=shift, vs_none=vn, vs_mapA=va, gen=g, r1=r1, r2=r2,
                             g1=(r1 == "helps" and r2 == "beats") if ok else None, best=best, rec=C.get(f"recovered({n})"), vs_oracle=C.get(f"{m} - oracle-B"), tmix_none=C.get(f"tmix-B({n}) - none"), refit_none=C.get(f"refit-B({n}) - none"), rps={a: v[0] for a, v in D["arms"].items()}))
def counts(sel, key, cats):
    c = collections.Counter(r[key] for r in sel); return " / ".join(str(c.get(k, 0)) for k in cats)
SUB = (("real pools", lambda r: not r["null"]), ("real pools with a shift", lambda r: not r["null"] and r["shift"] is True), ("real pools, no shift shown or oracle absent", lambda r: not r["null"] and r["shift"] is not True), ("random-halves nulls", lambda r: r["null"]))
L = ["# G1 (pool adaptation) under Amendment 4 — post hoc strict re-run", "",
     "20 group-disjoint item splits; RPS on pool-B test ratings (lower is better); differences are map-B(n) minus the named arm with a 95 % item-group bootstrap interval (B = 1,000, seed 17; heads and calibrators held fixed). ↓ = interval below 0 (map-B better), ↑ = interval above 0 (map-B worse). A number in parentheses after an interval is the number of splits when below 20.", "",
     "## Verdict counts", "", "| subset | n | cells | (i) helps / no change / hurts / n/a | (ii) beats / equivalent / worse / n/a | (iii) G1 holds |", "|---|---|---|---|---|---|"]
V = {}
for nm, fn in SUB:
    for n in NS:
        sel = [r for r in rows if fn(r) and r["n"] == n]; h = sum(1 for r in sel if r["g1"]); V[f"{nm}|{n}"] = dict(cells=len(sel), r1=collections.Counter(r["r1"] for r in sel), r2=collections.Counter(r["r2"] for r in sel), g1=h)
        L.append(f"| {nm} | {n} | {len(sel)} | {counts(sel, 'r1', ('helps', 'no change', 'hurts', 'n/a'))} | {counts(sel, 'r2', ('beats', 'equivalent', 'worse', 'n/a'))} | {h} |")
L += ["", "## Per generic arm: cells where map-B(n) is better / not separated / worse (descriptive; real pools, then nulls)", "", "| arm | " + " | ".join(f"real n = {n}" for n in NS) + " | " + " | ".join(f"null n = {n}" for n in NS) + " |", "|---" * 7 + "|"]
for b in GEN + ("none", "map-A"):
    cell = []
    for null in (False, True):
        for n in NS:
            vs = [(r["gen"][b] if b in GEN else r["vs_none"] if b == "none" else r["vs_mapA"]) for r in rows if r["null"] == null and r["n"] == n]; vs = [v for v in vs if v is not None]
            cell.append(f"{sum(v[2] < 0 for v in vs)} / {sum(v[1] <= 0 <= v[2] for v in vs)} / {sum(v[1] > 0 for v in vs)}")
    L.append(f"| {b} | " + " | ".join(cell) + " |")
pools_seen = {(r["panel"], r["var"], r["pool"]): r for r in rows}
L += ["", f"## Pool shift (none − oracle-B > 0): {sum(1 for r in pools_seen.values() if not r['null'] and r['shift'] is True)} of {sum(1 for r in pools_seen.values() if not r['null'])} real pools; {sum(1 for r in pools_seen.values() if r['null'] and r['shift'] is True)} of {sum(1 for r in pools_seen.values() if r['null'])} nulls", "",
      "| panel | variable | pool B | raters | cal. ratings | none − oracle-B | shift |", "|---|---|---|---|---|---|---|"]
for (p, v, b), r in pools_seen.items(): L.append(f"| {p} | {v} | {b[2:]} | {r['raters']:.0f} | {r['ncal']:.0f} | {f4(r['gap'])} | {'yes' if r['shift'] is True else 'no' if r['shift'] is False else 'n/a'} |")
L += ["", "## Every pool × n", "", "| panel | variable | pool B | n | map-B − none | − map-A | − clim-B | − bin-B | − qbin-B | − refit-B | − dir-B | − tmix-B | best generic | (i) | (ii) | G1 | share of gap closed |", "|---" * 17 + "|"]
for r in rows:
    c = lambda v: f4(v) + sig(v)
    L.append(f"| {r['panel']} | {r['var']} | {r['pool'][2:]} | {r['n']} | {c(r['vs_none'])} | {c(r['vs_mapA'])} | " + " | ".join(c(r["gen"][b]) for b in GEN) + f" | {r['best']} | {r['r1']} | {r['r2']} | {'**yes**' if r['g1'] else 'no' if r['g1'] is not None else 'n/a'} | {('%.2f [%.2f, %.2f]' % tuple(r['rec'][:3])) if r['shift'] is True and r['rec'] else '—'} |")
L += ["", "## Generic arms against no adaptation (does fitting on the n target ratings help at all?)", "", "| panel | variable | pool B | n | tmix-B − none | refit-B − none | map-B − oracle-B |", "|---|---|---|---|---|---|---|"]
for r in rows: L.append(f"| {r['panel']} | {r['var']} | {r['pool'][2:]} | {r['n']} | {f4(r['tmix_none'])}{sig(r['tmix_none'])} | {f4(r['refit_none'])}{sig(r['refit_none'])} | {f4(r['vs_oracle'])}{sig(r['vs_oracle'])} |")
if os.path.exists(f"{HERE}/reports/G1_V2_READING.md"): k = L.index("## Verdict counts"); L[k:k] = open(f"{HERE}/reports/G1_V2_READING.md").read().rstrip("\n").split("\n") + [""]   # hand-written reading, kept in its own file
os.makedirs(f"{HERE}/reports", exist_ok=True); open(f"{HERE}/reports/G1_SUMMARY_V2.md", "w").write("\n".join(L) + "\n"); json.dump(dict(counts=V, rows=rows), open(f"{RES}/verdicts.json", "w"), indent=1)
print("\n".join(L[:L.index("## Every pool × n")]))
