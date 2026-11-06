"""ROUND21 R21-6: per-evaluator-fold breakdown of LoRA budget contrasts (descriptive). Usage: python lora_by_fold.py <root> [<root> ...]"""
import os, sys, glob, re, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
P = data_panels.load("summeval_coherence8"); H = P["H"]; K = P["K"]; LV = np.arange(K)
def rps(path, f):
    Pm = np.load(f"{path}/P_test.npy"); rows = pd.read_csv(f"{path}/items_test.csv")["row"].to_numpy(); cdf = np.cumsum(Pm, 1)
    return float((((cdf - (LV[None] >= H[rows, f][:, None])) ** 2).sum(1) / (K - 1)).mean())
out = {"experts": {}}; crowd = H[:, 3:].mean(1)
for e in range(3): out["experts"][e] = dict(mean=float(H[:, e].mean()), sd=float(H[:, e].std()), mad_to_crowd_mean=float(np.abs(H[:, e] - crowd).mean()))
lines = ["# R21-6 per-fold LoRA contrasts (lora_by_fold.py)", "", "experts (mean, SD, mean |e − crowd mean|): " + "; ".join(f"e{e} {v['mean']:.2f}, {v['sd']:.2f}, {v['mad_to_crowd_mean']:.2f}" for e, v in out["experts"].items()), "", "| root | design | fold | mean Δ vs full | seed range | seeds |", "|---|---|---|---|---|---|"]
for root in sys.argv[1:]:
    base = f"{HERE}/results/{root}/summeval_coherence8"; out[root] = {}
    for d in sorted(os.path.basename(x) for x in glob.glob(f"{base}/*") if not x.endswith("a7_F1.0")):
        for f in range(3):
            ds = []
            for p in glob.glob(f"{base}/{d}/s*/f{f}/chen/P_test.npy"):
                s = re.search(r"/s(\d+)/", p).group(1); ref = f"{base}/a7_F1.0/s{s}/f{f}/chen"
                if os.path.exists(f"{ref}/P_test.npy"): ds.append(rps(os.path.dirname(p), f) - rps(ref, f))
            if ds: out[root][f"{d}/f{f}"] = ds; lines.append(f"| {root} | {d} | {f} | {np.mean(ds):+.4f} | [{min(ds):+.4f}, {max(ds):+.4f}] | {len(ds)} |")
json.dump(out, open(f"{HERE}/results/lora_by_fold.json", "w"), indent=1); open(f"{HERE}/results/lora_by_fold.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
