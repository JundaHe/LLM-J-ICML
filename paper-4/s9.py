"""Stage 9 (PROTOCOL_STAGE9.md): SAP summary — own − μ and own − other (direction points, LL ×100 nats) at k = 20 / 50 per panel, null-calibrated selection (Am. 2:
σ²_j above the maximum over t0's five folds), and the decision rules M1–M3."""
import json, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
from attr_feats import NAMES
ld = lambda t: json.load(open(f"{R}/stage9_sap_{t}.json")) if os.path.exists(f"{R}/stage9_sap_{t}.json") else None
null = ld("t0"); thr = np.max([s["sigma2"] for s in null["screen"]], 0) if null else None
fmt = lambda v: f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
L = ["# Stage 9 — screened attribute personalisation (SAP)", "", "| panel | own − μ, dir, k = 20 | own − other, dir, k = 20 | own − μ, dir, k = 50 | own − μ, LL ×100, k = 20 | selected in ≥ 4/5 folds (null-calibrated) |", "|---|---|---|---|---|---|"]; out = {}
for t in ("t0", "t5", "t10", "sem5", "sem10", "x10", "real"):
    d = ld(t)
    if d is None: continue
    sel = collections.Counter(NAMES[j] for s in d["screen"] for j in range(len(NAMES)) if thr is not None and s["sigma2"][j] > thr[j]); s4 = sorted(a for a, c in sel.items() if c >= 4)
    out[t] = {k_: d[k_] for k_ in d if k_.startswith("k")}; out[t]["selected_null_cal"] = s4
    L.append(f"| {t} | {fmt(d['k20_dir_own-pop'])} | {fmt(d['k20_dir_own-other'])} | {fmt(d['k50_dir_own-pop'])} | {fmt(d['k20_ll_own-pop'])} | {', '.join(s4) if t != 't0' else '(null reference)'} |")
rules = {}
if "t0" in out: rules["M1_no_false_detection"] = bool(out["t0"]["k20_dir_own-pop"][1] <= 1.0 and out["t0"]["k20_dir_own-other"][1] <= 1.0)
if "sem5" in out and "sem10" in out:
    rules["M2_detect"] = {t: bool(out[t]["k20_dir_own-pop"][1] > 1.0) for t in ("sem5", "sem10")}
    rules["M2_select"] = {t: bool({"list/heading lines", "hedging/refusal"} <= set(out[t]["selected_null_cal"])) for t in ("sem5", "sem10")}
if "real" in out: rules["M3_real_content_personalisation"] = bool(out["real"]["k20_dir_own-pop"][1] > 1.0)
out["rules"] = rules; L += ["", "**Rules:** " + json.dumps(rules)]
if thr is not None: L += ["", "Null thresholds (max σ² over t0 folds): " + ", ".join(f"{NAMES[j]} {thr[j]:.4f}" for j in range(len(NAMES)))]
json.dump(out, open(f"{R}/stage9_sap.json", "w"), indent=1); open(f"{R}/stage9_sap.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
