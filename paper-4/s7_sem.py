"""Stage 7 S7-4 (PROTOCOL_STAGE7.md Am. 3): semantic injection axes (formatting, hedging / refusal). Own − other direction accuracy (points; rater bootstrap, as
s3_real.py) at k = 20 / 50 for DL (tuned), VPL and PAL-B (PCA-256), and the reference learner's own − population; next to the original panels t5 / t10."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); sys.argv = sys.argv[:1]
import s3_real as S
meta = {**json.load(open(f"{R}/synth/synth_meta.json")), **json.load(open(f"{R}/synth/synth_meta_sem.json"))}
fp = lambda v: None if v is None else [100 * v[0], 100 * v[1], 100 * v[2]]; fmt = lambda v: "—" if v is None else f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
L = ["# Stage 7 S7-4 — semantic injection axes vs the original injection (own − other, direction accuracy, points; 95 % rater bootstrap)", "",
     "| panel | axes | oracle gain | DL, k = 20 | VPL, k = 20 | PAL-B, k = 20 | DL, k = 50 | VPL, k = 50 | PAL-B, k = 50 | reference own − population, k = 20 |", "|---|---|---|---|---|---|---|---|---|---|"]; out = {}
for t, ax in (("t5", "length + random direction"), ("sem5", "formatting + hedging"), ("t10", "length + random direction"), ("sem10", "formatting + hedging")):
    fr, vr = S.rows_of(f"{R}/stage2a_multipref_synth_{t}_f?.json"), S.rows_of(f"{R}/stage2c_multipref_synth_{t}_E1_f?.json")
    c = {f"{m}{k}": fp(S.permc(rows, key, k)) for k in (20, 50) for m, rows, key in (("DL", fr, "DL"), ("VPL", vr, "VPL"), ("PAL", vr, "PAL2"))}
    ref = json.load(open(f"{R}/stage5_ref_{t}.json")); c["ref20"] = ref.get("estimated_k20_pop"); out[t] = c
    L.append(f"| {t} | {ax} | +{100 * meta[t]['oracle_gain_realised']:.1f} | " + " | ".join(fmt(c[k]) for k in ("DL20", "VPL20", "PAL20", "DL50", "VPL50", "PAL50", "ref20")) + " |")
det = {t: [m for m in ("DL", "VPL", "PAL") if out[t][f"{m}20"] and out[t][f"{m}20"][1] > 1.0] for t in out}
L += ["", "Detected at k = 20 (lower bound > +1 point): " + "; ".join(f"{t}: {', '.join(v) if v else 'none'}" for t, v in det.items()) + "."]
json.dump({"contrasts": out, "detected_k20": det}, open(f"{R}/stage7_sem.json", "w"), indent=1); open(f"{R}/stage7_sem.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
