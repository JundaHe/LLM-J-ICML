"""Stage 7 S7-2 (PROTOCOL_STAGE7.md Am. 1): DL (few-shot-tuned prior) and the reference learner on the in-span panels x5 / x10 (g2 in DL's joint PCA-256),
next to the original panels t5 / t10 (g2 outside DL's input space); own − other direction accuracy at k = 20, 50, rater bootstrap (as s3_real.py)."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); sys.argv = sys.argv[:1]
import s3_real as S                                                       # reuses rows_of / permc (writes the Stage-3 table as a side effect, unchanged)
meta = {**json.load(open(f"{R}/synth/synth_meta.json")), **json.load(open(f"{R}/synth/synth_meta_span.json"))}
fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
fp = lambda v: None if v is None else [100 * v[0], 100 * v[1], 100 * v[2]]
L = ["# Stage 7 S7-2 — injected g2 inside (x) vs outside (t) DL's input space (direction accuracy, points; 95 % rater bootstrap)", "",
     "| panel | g2 in DL's input | oracle gain | DL own − other, k = 20 | DL own − other, k = 50 | reference own − population, k = 20 (est. base) | reference own − other, k = 20 (est. base) |", "|---|---|---|---|---|---|---|"]; out = {}
for t, ins in (("t5", "no (R² 0.02)"), ("x5", "yes"), ("t10", "no (R² 0.02)"), ("x10", "yes")):
    rows = S.rows_of(f"{R}/stage2a_multipref_synth_{t}_f?.json"); c = {"DL20": fp(S.permc(rows, "DL", 20)), "DL50": fp(S.permc(rows, "DL", 50))}
    ref = json.load(open(f"{R}/stage5_ref_{t}.json")) if os.path.exists(f"{R}/stage5_ref_{t}.json") else {}
    c["ref20_pop"], c["ref20_other"] = ref.get("estimated_k20_pop"), ref.get("estimated_k20"); out[t] = c
    L.append(f"| {t} | {ins} | +{100 * meta[t]['oracle_gain_realised']:.1f} | {fmt(c['DL20'])} | {fmt(c['DL50'])} | {fmt(c['ref20_pop'])} | {fmt(c['ref20_other'])} |")
det = {t: bool(out[t]["DL20"] and out[t]["DL20"][1] > 1.0) for t in out}
L += ["", "Detection (lower bound > +1 point, k = 20) by DL: " + ", ".join(f"{t} {'yes' if v else 'no'}" for t, v in det.items()) + "."]
json.dump({"contrasts": out, "DL_detects": det}, open(f"{R}/stage7_span.json", "w"), indent=1); open(f"{R}/stage7_span.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
