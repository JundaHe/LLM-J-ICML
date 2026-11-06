"""ROUND20 R20-7: per-fold comparison of rater-subset arms (results/lora_budget_r207) with the R20-5c single batch (results/lora_budget_r20_rerun). Descriptive. Usage: python r207_compare.py"""
import os, sys, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
P = data_panels.load("summeval_coherence8"); H = P["H"]; K = P["K"]; LV = np.arange(K)
def rps(path, f):
    Pm = np.load(f"{path}/P_test.npy"); rows = pd.read_csv(f"{path}/items_test.csv")["row"].to_numpy(); cdf = np.cumsum(Pm, 1)
    return float((((cdf - (LV[None] >= H[rows, f][:, None])) ** 2).sum(1) / (K - 1)).mean())
A = f"{HERE}/results/lora_budget_r207/summeval_coherence8"; B = f"{HERE}/results/lora_budget_r20_rerun/summeval_coherence8"
pairs = [("experts2", "a2_F1.0"), ("experts2", "a7_F1.0"), ("crowd5", "a7_F1.0"), ("crowd5", "a2_F1.0")]; out = {}; lines = ["| arm − reference | f0 | f1 | f2 | mean | cells |", "|---|---|---|---|---|---|"]
for arm, ref in pairs:
    per = {}
    for f in range(3):
        d = [rps(f"{A}/{arm}/s{s}/f{f}/chen", f) - rps(f"{B}/{ref}/s{s}/f{f}/chen", f) for s in (2003, 2004, 2005) if os.path.exists(f"{A}/{arm}/s{s}/f{f}/chen/P_test.npy")]
        if d: per[f] = d
    if not per: continue
    out[f"{arm}-{ref}"] = per; allv = [x for v in per.values() for x in v]
    lines.append(f"| {arm} − {ref} | " + " | ".join(f"{np.mean(per[f]):+.4f} [{min(per[f]):+.4f}, {max(per[f]):+.4f}]" if f in per else "–" for f in range(3)) + f" | {np.mean(allv):+.4f} | {len(allv)} |")
json.dump(out, open(f"{HERE}/results/lora_budget_r207/compare.json", "w"), indent=1); open(f"{HERE}/results/lora_budget_r207/compare.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
