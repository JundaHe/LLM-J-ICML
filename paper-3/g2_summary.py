"""G2 summary (PROTOCOL_CALIBRATION.md Amendment 3): reads results/judge_map2/*/summary.json and applies the reading fixed in the amendment. In a cell and at a given n the
panel map BEATS generic calibration if map(n) − onehot+mix(n), map(n) − bin(n), and where defined map(n) − qbin(n) and map(n) − temp+mix(n), all have 95 % intervals
below 0; it is WORSE if any of them has an interval above 0; otherwise EQUIVALENT. (temp+mix enters the rule only for judges with a distribution of their own: the
post hoc Q0 and LoRA cells.) Output: reports/G2_SUMMARY.md"""
import json, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); RES = sorted(glob.glob(f"{HERE}/results/judge_map2/*/summary.json")); NS = ("20", "50", "all")
FRONT = ("openai_gpt-5_5", "anthropic_claude-opus-4_8", "google_gemini-3_1-pro-preview")
f = lambda v: "—" if v is None else f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]"; a_ = lambda v: "—" if v is None else f"{v[0]:.4f}"
def verdict(c, n):
    ds = [c.get(f"map({n}) - {b}({n})") for b in ("onehot+mix", "bin", "qbin", "temp+mix")]; ds = [d for d in ds if d is not None]
    return "worse" if any(d[1] > 0 for d in ds) else "beats" if all(d[2] < 0 for d in ds) else "equivalent"
def block(title, cells, note):
    L = [f"## {title}", "", note, "", "| panel | judge | n | clim | onehot | onehot+mix | bin | qbin | temp+mix | map | map − onehot+mix | map − bin | map − qbin | map − temp+mix | bin − clim | reading |", "|---" * 16 + "|"]; cnt = collections.Counter()
    for r in cells:
        A, C = r["arms"], r["contrasts"]
        for n in NS:
            v = verdict(C, n); cnt[(n, v)] += 1
            L.append(f"| {r['panel']} | {os.path.basename(r['_dir']).split('__', 1)[1]} | {n} | {a_(A.get(f'clim({n})'))} | {a_(A.get('onehot'))} | {a_(A.get(f'onehot+mix({n})'))} | {a_(A.get(f'bin({n})'))} | {a_(A.get(f'qbin({n})'))} | {a_(A.get(f'temp+mix({n})'))} | {a_(A.get(f'map({n})'))} | "
                     + " | ".join(f(C.get(f"map({n}) - {b}({n})")) for b in ("onehot+mix", "bin", "qbin", "temp+mix")) + f" | {f(C.get(f'bin({n}) - clim({n})'))} | **{v}** |")
    L += ["", "Counts (cells): " + "; ".join(f"n = {n}: " + ", ".join(f"{cnt[(n, v)]} {v}" for v in ("beats", "equivalent", "worse")) for n in NS), ""]
    loo = [r for r in cells if "map+rater-offset-LOO - map(all)-LOO" in r["contrasts"]]
    if loo:
        L += ["Leave-one-rater-out (persistent raters; calibrators fitted on the other raters' calibration ratings):", "", "| panel | judge | raters | bin(all)-LOO | map(all)-LOO | map+rater-offset-LOO | rater offset − map | map − bin |", "|---" * 8 + "|"]
        L += [f"| {r['panel']} | {os.path.basename(r['_dir']).split('__', 1)[1]} | {r.get('n_loo_raters')} | {a_(r['arms']['bin(all)-LOO'])} | {a_(r['arms']['map(all)-LOO'])} | {a_(r['arms']['map+rater-offset-LOO'])} | {f(r['contrasts']['map+rater-offset-LOO - map(all)-LOO'])} | {f(r['contrasts']['map(all)-LOO - bin(all)-LOO'])} |" for r in loo] + [""]
    return L
R = []
for p in RES: r = json.load(open(p)); r["_dir"] = os.path.dirname(p); R.append(r)
fr = [r for r in R if r["judge"] in FRONT]; q0 = [r for r in R if r["judge"] == "q0"]; lo = [r for r in R if r["judge"] == "lora"]
L = ["# G2 — a black-box judge's score → the panel's rating distribution (Amendment 3)", "",
     "RPS, lower is better; differences with 95 % item-group bootstrap intervals (B = 1,000; fitted calibrators held fixed, so the intervals cover test-item sampling; calibration-set variation enters through the mean over splits). n = number of calibration ratings.", ""]
L += block("Frontier judges (paper 1's outputs) — prespecified", fr, "20 group-disjoint 30/70 splits. Crupi: integer 1–5 score, 3 rating positions (no per-rater arm). Scalabrino: mean of six runs (continuous), 9 persistent evaluators.")
L += block("Frozen Qwen2.5-7B zero-shot (Q0) — post hoc re-analysis of the first sweep", q0, "20 splits; results with 3 splits had been seen before the amendment.")
L += block("Panel-trained LoRA judge — post hoc re-analysis", lo, "One fixed split per cell (the LoRA cell's own calibration/test items).")
os.makedirs(f"{HERE}/reports", exist_ok=True); open(f"{HERE}/reports/G2_SUMMARY.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
