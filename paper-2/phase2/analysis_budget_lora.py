"""
analysis_budget_lora — fixed-budget LoRA block (SHRINKAGE_PROTOCOL.md Amendment 3): raw test RPS against the held-out expert per design, and contrasts design − full-data chen,
with a crossed bootstrap over optimizer-seed clusters and test DOCUMENTS (SummEval groups), B replicates. Uses whatever cells exist (reports the count).
Usage: python analysis_budget_lora.py [--B 2000]
"""
import os, sys, glob, re, json, argparse, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--panel", default="summeval_coherence8"); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"]; G = np.asarray(PAN.get("groups", PAN["item_ids"])); K = PAN["K"]; LV = np.arange(K)
def rps(Pm, y): cdf = np.cumsum(Pm, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def load_cell(path, fold):
    Pm = np.load(f"{path}/P_test.npy"); rows = pd.read_csv(f"{path}/items_test.csv")["row"].to_numpy(); return rows, rps(Pm, H[rows, fold])
SEEDS = (2000, 2001); FULL = {2000: "s0", 2001: "s0_seed2001"}
cells = {}                                                     # design -> {(seed, fold): (rows, rps per item)}
for s in SEEDS:
    for f in range(3): cells.setdefault("full_a7_F1", {})[(s, f)] = load_cell(f"{HERE}/results/lora/{args.panel}/{FULL[s]}/f{f}/chen", f)
meta = {}
for d in sorted(glob.glob(f"{HERE}/results/lora_budget/{args.panel}/*")):
    name = os.path.basename(d)
    for p in glob.glob(f"{d}/s*/f*/chen"):
        if not os.path.exists(f"{p}/P_test.npy"): continue
        m = re.search(r"/s(\d+)/f(\d)/chen$", p); s, f = int(m.group(1)), int(m.group(2))
        if s in SEEDS: cells.setdefault(name, {})[(s, f)] = load_cell(p, f)
        meta.setdefault(name, json.load(open(f"{p}/meta.json")))
def mean_rps(cellset, seeds, doc_weights=None):
    """mean over cells (seed × fold) of the document-weighted mean item RPS"""
    vals = []
    for (s, f), (rows, r) in cellset.items():
        if s not in seeds: continue
        w = np.ones(len(rows)) if doc_weights is None else np.array([doc_weights.get(g, 0.0) for g in G[rows]])
        vals.append((r * w).sum() / max(w.sum(), 1e-12))
    return float(np.mean(vals)) if vals else np.nan
docs = np.unique(G[[i for i in range(len(G)) if i in set(np.concatenate([rows for (rows, _) in cells["full_a7_F1"].values()]))]])
rng = np.random.RandomState(7); out = {}; lines = [f"# Fixed-budget LoRA block — {args.panel} (analysis_budget_lora.py)", "", "| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |", "|---|---|---|---|---|---|"]
for name, cs in cells.items():
    pt = mean_rps(cs, SEEDS); ref = mean_rps(cells["full_a7_F1"], SEEDS); diff = pt - ref; bs = []
    folds_present = sorted({f for (_, f) in cs})
    for b in range(args.B):
        seeds_b = tuple(rng.choice(SEEDS, len(SEEDS), replace=True)); dw = {}
        for g in rng.choice(docs, len(docs), replace=True): dw[g] = dw.get(g, 0.0) + 1.0
        bs.append(mean_rps(cs, seeds_b, dw) - mean_rps(cells["full_a7_F1"], seeds_b, dw))
    ci = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    md = meta.get(name, {}); n_full = int(json.load(open(f"{HERE}/results/lora/{args.panel}/{FULL[2000]}/f0/chen/meta.json"))["parts"]["train"])
    out[name] = dict(rps=pt, diff_vs_full=diff, ci95=ci, n_cells=len(cs), folds=folds_present, rating_budget=md.get("rating_budget", n_full * (H.shape[1] - 1)), n_train=md.get("n_train_used", n_full))
    lines.append(f"| {name} | {out[name]['rating_budget']} | {out[name]['n_train']} | {len(cs)} | {pt:.4f} | {diff:+.4f} [{ci[0]:+.4f}, {ci[1]:+.4f}] |")
lines += ["", "Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test groups (B = %d). Full-data chen = the T3b/T3c runs restricted to the same seeds." % args.B]
os.makedirs(f"{HERE}/results/lora_budget", exist_ok=True); sfx = "" if args.panel == "summeval_coherence8" else "_" + args.panel; json.dump(out, open(f"{HERE}/results/lora_budget/summary{sfx}.json", "w"), indent=1); open(f"{HERE}/results/lora_budget/summary{sfx}.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
