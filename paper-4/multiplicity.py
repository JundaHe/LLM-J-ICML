"""Stage 11 Am. 10 (PROTOCOL_STAGE11.md): Holm-adjusted detection over the reported CA first-turn contrasts (normal approximation from 95 % intervals)."""
import json, numpy as np
from scipy.stats import norm
S8 = [("DFp own gain", -0.19, -0.36, -0.02), ("DFp own-other", 0.07, -0.08, 0.21), ("VPL own gain", 0.15, 0.03, 0.27), ("VPL own-other", 0.31, 0.20, 0.42),
      ("PAL2 own gain", -0.05, -0.19, 0.09), ("PAL2 own-other", 0.03, -0.08, 0.14), ("PAL4 own gain", -0.20, -0.38, -0.02), ("PAL4 own-other", 0.29, 0.13, 0.45),
      ("LoRe own gain", -2.34, -2.79, -1.88), ("LoRe own-other", 3.27, 2.85, 3.70), ("LoRe-reg own gain", 0.35, 0.25, 0.46), ("LoRe-reg own-other", 0.36, 0.26, 0.46)]
S8b = [("VPL own-same-country other", 0.34, 0.24, 0.45), ("PAL4 own-same-country other", 0.27, 0.11, 0.43), ("LoRe own-same-country other", 3.22, 2.83, 3.60), ("LoRe-reg own-same-country other", 0.37, 0.28, 0.46),
       ("DFp own-same-country other", 0.07, -0.05, 0.20), ("PAL2 own-same-country other", 0.07, -0.05, 0.18)]
S11 = [("S11-2 C length", 0.32, 0.25, 0.40), ("S11-2 C paragraphs (Am.1 adj.)", 0.76, 0.26, 1.35), ("S11-2 C list (Am.1 adj.)", 0.45, -0.02, 0.95),
       ("Am.3 transfer length", 0.41, 0.27, 0.55), ("Am.3 transfer paragraphs", 0.18, -0.34, 0.68), ("Am.3 transfer list", 0.12, -0.28, 0.52),
       ("S11-3 TR3 acc", 0.13, -0.28, 0.53), ("S11-3 TR3 LL", -0.0060, -0.0121, 0.0000), ("S11-3 TR3 - rank-2", -0.06, -0.36, 0.21),
       ("Am.3 shrink x0.5 acc", 0.36, 0.01, 0.71), ("Am.3 shrink x0.25 acc", 0.53, 0.23, 0.83), ("Am.3 shrink x0.25 LL", 0.0090, 0.0060, 0.0119),
       ("Am.4 TRV acc", 0.49, 0.20, 0.77), ("Am.4 TRV LL", 0.0088, 0.0061, 0.0116), ("Am.4 TRV - rank-2", 0.30, 0.04, 0.56), ("S12 smoke TRV acc 2-way", 0.49, 0.01, 0.97),
       ("S12 smoke iso acc", 0.66, 0.37, 0.95), ("S12 smoke TRV - iso", -0.17, -0.29, -0.05),
       ("S11-1a list AUC", 0.0001, -0.0017, 0.0017), ("S11-1a length acc", 1.06, 0.80, 1.33), ("S11-1b length acc", 0.45, 0.14, 0.80), ("S11-1b list acc", -0.12, -0.30, 0.04),
       ("Am.8 within-cluster length", 0.206, 0.183, 0.231), ("Am.8 own - matched other acc", 0.80, 0.45, 1.16), ("Am.8 own - matched other LL", 0.0090, 0.0055, 0.0125),
       ("Am.9 W.E length", 0.88, 0.61, 1.13), ("Am.9 W.G length", 1.08, 0.69, 1.47), ("Am.9 O.E length", 0.26, 0.02, 0.50), ("Am.9 O.G length", 0.47, 0.12, 0.85)]
def holm(rows):
    p = np.array([2 * norm.sf(abs(e) / max((h - l) / 3.92, 1e-12)) for _, e, l, h in rows]); o = np.argsort(p); m = len(p); adj = np.zeros(m); run = 0.0
    for r, i in enumerate(o): run = max(run, min(1.0, (m - r) * p[i])); adj[i] = run
    return [{"test": t, "est": e, "ci": [l, h], "p": float(pi), "p_holm": float(a), "unadjusted_sig": bool(l > 0 or h < 0), "holm_sig": bool(a < 0.05)} for (t, e, l, h), pi, a in zip(rows, p, adj)]
out = {"stage8_frozen": holm(S8), "stage8_am2": holm(S8b), "stage11_all": holm(S11)}
for k, v in out.items():
    lost = [x["test"] for x in v if x["unadjusted_sig"] and not x["holm_sig"]]; print(k, f"{sum(x['unadjusted_sig'] for x in v)}/{len(v)} unadjusted, {sum(x['holm_sig'] for x in v)} Holm; lost: {lost}")
json.dump(out, open("results/multiplicity.json", "w"), indent=1)
