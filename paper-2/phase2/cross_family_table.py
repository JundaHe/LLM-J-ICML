"""cross_family_table — Gate D decoding G (95 % CI) per panel and base family, from results/decoding/*.json. Writes reports/CROSS_FAMILY_DECODING.md."""
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); FAM = {"": "Qwen2.5-7B", "_qwen3": "Qwen3-8B", "_olmo": "OLMo-2-7B"}; T = {}
for f in glob.glob(f"{HERE}/results/decoding/*_d64_E_last*.json"):
    m = re.match(r"(.+)_d64_E_last(_qwen3|_olmo)?\.json$", os.path.basename(f))
    if not m: continue
    r = json.load(open(f)); T.setdefault(m.group(1), {})[FAM[m.group(2) or ""]] = (r["est"]["G"], r["ci95"]["G"], r["est"]["pos_ctrl"])
rows = ["| panel | " + " | ".join(FAM.values()) + " |", "|---|" + "---|" * len(FAM)]
for p in sorted(T, key=lambda k: (k.startswith("chaosnli"), k)):
    rows.append(f"| {p} | " + " | ".join((f"{T[p][fm][0]:+.5f} [{T[p][fm][1][0]:+.5f}, {T[p][fm][1][1]:+.5f}] (pos {T[p][fm][2]:.2f})" if fm in T[p] else "—") for fm in FAM.values()) + " |")
txt = "# Decoding of the residual beyond exact mode+mean (Gate D): proper-score gain G by base family\n\nG > 0 ⇔ the frozen representation linearly predicts an independent rater panel's residual; pos = positive control (Spearman of decoded vs held-out mean).\n\n" + "\n".join(rows) + "\n"
open(f"{HERE}/reports/CROSS_FAMILY_DECODING.md", "w").write(txt); print(txt)
