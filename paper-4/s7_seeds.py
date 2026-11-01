"""Stage 7 S7-5 (PROTOCOL_STAGE7.md Am. 4): the in-span panels over four draws (original + seeds 11–13); DL (tuned) own − other at k = 20 / 50 and the reference
learner's own − population at k = 20; the Am. 4 rule (≥ 3 of 4 draws)."""
import json, glob, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); sys.argv = sys.argv[:1]
import s3_real as S
meta = {}
for mf in sorted(glob.glob(f"{R}/synth/synth_meta_span*.json")): meta.update(json.load(open(mf)))
fp = lambda v: None if v is None else [100 * v[0], 100 * v[1], 100 * v[2]]; fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
L = ["# Stage 7 S7-5 — in-span injection over four draws (direction accuracy, points; 95 % rater bootstrap)", "", "| panel | oracle gain | DL own − other, k = 20 | DL own − other, k = 50 | reference own − population, k = 20 |", "|---|---|---|---|---|"]; out = {}
for g in (5, 10):
    for t in [f"x{g}"] + [f"x{g}s{s}" for s in (11, 12, 13)]:
        rows = S.rows_of(f"{R}/stage2a_multipref_synth_{t}_f?.json")
        if not rows or t not in meta: continue
        ref = json.load(open(f"{R}/stage5_ref_{t}.json")) if os.path.exists(f"{R}/stage5_ref_{t}.json") else {}
        c = {"DL20": fp(S.permc(rows, "DL", 20)), "DL50": fp(S.permc(rows, "DL", 50)), "ref20": ref.get("estimated_k20_pop"), "oracle": 100 * meta[t]["oracle_gain_realised"]}; out[t] = c
        L.append(f"| {t} | +{c['oracle']:.1f} | {fmt(c['DL20'])} | {fmt(c['DL50'])} | {fmt(c['ref20'])} |")
n10 = sum(out[t]["DL20"][1] > 1.0 for t in out if t.startswith("x10")); m10 = sum(t.startswith("x10") for t in out)
n5 = sum(out[t]["DL20"][1] <= 1.0 for t in out if t.startswith("x5")); m5 = sum(t.startswith("x5") for t in out)
L += ["", f"**Am. 4 rule: DL detects +10 in {n10}/{m10} draws ({'kept' if n10 >= 3 else 'weakened'}); fails +5 in {n5}/{m5} draws ({'kept' if n5 >= 3 else 'weakened'}).**"]
out["rule"] = {"detect10": [n10, m10], "fail5": [n5, m5]}
json.dump(out, open(f"{R}/stage7_seeds.json", "w"), indent=1); open(f"{R}/stage7_seeds.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
