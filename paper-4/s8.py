"""Stage 8 (PROTOCOL_STAGE8.md): Community Alignment first-turn pairs. Per method, choice accuracy (points) at k = 20 / 50: own gain method(k) − method(0) and
own − other (permutation control); rater bootstrap (seed 17, as s6.py); decision rule at k = 20. Learner-free: annotator agreement on shared response pairs vs the
text-only model's k = 0 accuracy on the same (tested) pairs."""
import json, glob, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
from s6 import rows_of, own, pair, fmt                                    # s6 writes its own tables on import (unchanged inputs)
L = ["# Stage 8 — Community Alignment (first turn, native choice; points; 95 % rater bootstrap)", "", "| method | k | own gain | own − other | − Dp | raters |", "|---|---|---|---|---|---|"]; out = {}
for tag, ms in (("", ("DFp", "VPL", "PAL2", "PAL4")), ("_lore", ("LORE",)), ("_lorer", ("LORER",))):
    rows = rows_of(f"{R}/stage2c_ca_pairs_E2_f?{tag}.json")
    if not rows: continue
    for m in ms:
        if f"{m}_dir" not in rows[0]: continue
        for k in (20, 50):
            c = {"own": own(rows, k, m, "dir", "n"), "perm": pair(rows, k, f"{m}_dir", f"{m}_perm_dir", "n") if f"{m}_perm_dir" in rows[0] else None, "vsDp": pair(rows, k, f"{m}_dir", "Dp_dir", "n")}
            out[f"{m}_k{k}"] = c; nr = len({(r["fold"], r["rater"]) for r in rows if r["k"] == k})
            L.append(f"| {m}{tag} | {k} | {fmt(c['own'])} | {fmt(c['perm']) if c['perm'] else '—'} | {fmt(c['vsDp'])} | {nr} |")
k20 = [v for kk, v in out.items() if kk.endswith("_k20")]
ub = max(max(c["own"][2], c["perm"][2] if c["perm"] else -1e9) for c in k20); lb = max(max(c["own"][1], c["perm"][1] if c["perm"] else -1e9) for c in k20)
verdict = "CONTENT PERSONALISATION DETECTED" if lb > 1.0 else ("ranking null REPLICATES" if ub < 1.0 else "INCONCLUSIVE")
out["rule"] = {"max_upper": ub, "max_lower": lb, "verdict": verdict}
L += ["", f"**Decision rule (k = 20): largest upper bound {ub:+.2f}, largest lower bound {lb:+.2f} → {verdict}.**"]
ag = json.load(open(f"{R}/stage8_agree.json")); shared = set(ag["rows"]); hit = []
for fz in sorted(glob.glob(f"{R}/ratings/stage2c_ca_pairs_E2_f?.npz")):
    z = np.load(fz); s = (z["k"] == 0) & np.isin(z["item"], list(shared)); hit.append(z["Dp_dir"][s])
if hit:
    h = np.concatenate(hit); out["text_only_on_shared"] = [float(h.mean()), int(len(h))]
    L += ["", f"Learner-free: two annotators agree on {ag['agreement']:.3f} [{ag['ci'][0]:.3f}, {ag['ci'][1]:.3f}] of shared response pairs; the text-only model (k = 0) is right on {h.mean():.3f} of the {len(h)} tested ratings of those pairs."]
json.dump(out, open(f"{R}/stage8_ca.json", "w"), indent=1); open(f"{R}/stage8_ca.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
