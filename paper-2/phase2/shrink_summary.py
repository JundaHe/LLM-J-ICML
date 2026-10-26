"""shrink_summary — Gate A table from results/shrinkage/*.json: per panel the contrasts vs raw and vs qT with 95 % intervals, plus the inverse-variance pooled contrast over the small ordinal
panels (SHRINKAGE_PROTOCOL Gate A (i); panels are not independent — stated). Writes results/shrinkage/SUMMARY.md."""
import glob, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ARMS = ("qT", "shr", "shr2", "loc", "dir_in", "ls_in", "lsm_in", "jsp", "qs", "shr_s")
rows = []; lines = ["# Annotation-side shrinkage (Gate A) — contrasts vs raw histogram, RPS, 95 % item-cluster bootstrap", "", "| panel | a | λ̂ | ρ_loc | " + " | ".join(ARMS) + " |", "|---|---|---|---|" + "---|" * len(ARMS)]
for f in sorted(glob.glob(f"{HERE}/results/shrinkage/*_a*.json")):
    r = json.load(open(f)); e = r["est"]["vs_raw"]; c = r["ci95"]["vs_raw"]; rows.append(r)
    lines.append(f"| {r['panel']} | {r['a']} | {r['est']['lam_hat']:.2f} | {r['est'].get('rho_loc', float('nan')):.2f} | " + " | ".join(f"{e[k]:+.4f} [{c[k][0]:+.4f}, {c[k][1]:+.4f}]" if k in e else "—" for k in ARMS) + " |")
def pooled(key, ref="vs_raw"):
    ests, ws = [], []
    for r in rows:
        if r["nominal"] or key not in r["est"][ref]: continue
        lo, hi = r["ci95"][ref][key]; se = (hi - lo) / (2 * 1.96); ests.append(r["est"][ref][key]); ws.append(1 / max(se, 1e-6) ** 2)
    ests, ws = np.array(ests), np.array(ws); m = (ests * ws).sum() / ws.sum(); se = 1 / np.sqrt(ws.sum()); return m, m - 1.96 * se, m + 1.96 * se, len(ests)
lines += ["", "## Inverse-variance pooled contrasts over the small ordinal panels (not independent: SummEval criteria share documents; POPQUORN attributes share annotators)", ""]
for ref in ("vs_raw", "vs_qT"):
    for key in ("shr", "shr2", "dir_in", "lsm_in", "qs"):
        m, lo, hi, n = pooled(key, ref); lines.append(f"- {key} {ref.replace('_', ' ')}: {m:+.4f} [{lo:+.4f}, {hi:+.4f}] over {n} panels")
txt = "\n".join(lines) + "\n"; open(f"{HERE}/results/shrinkage/SUMMARY.md", "w").write(txt); print(txt)
