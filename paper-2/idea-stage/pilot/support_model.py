"""
M0: (a) frozen support model — predicts the max-changed fraction of an exact target-link randomisation from the
    empirical distribution of cell keys (pool, z, sum_y) and of histogram classes within keys, estimated on a
    COMPLEMENTARY item set, by simulation of a training set of the planned size; validated against the observed
    fraction on the actual grouped training sets of other splits/folds.
    (b) subsampled-rater support curves (target raters m_t -> fewer) for commit (5,4,3) and readability (8,6,4).
"""
import sys, os, json, numpy as np, pandas as pd
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support_audit import z_label
K = 5
def cells_of(Ht, pools, idx):
    c = defaultdict(list)
    for i in idx: c[(pools[i], z_label(Ht[i]), int(Ht[i].sum()))].append(tuple(np.bincount(Ht[i], minlength=K)))
    return c
def maxchg_from_cells(c):
    tot = chg = 0
    for key, hists in c.items():
        N = len(hists); cnt = Counter(hists); M = max(cnt.values()); tot += N
        if len(cnt) >= 2: chg += min(N, 2 * (N - M))
    return chg / tot
def grouped_split(groups, seed, frac=0.6):
    ug = np.unique(groups); rng = np.random.RandomState(seed); rng.shuffle(ug); tr = set(ug[: int(frac * len(ug))]); return np.array([g in tr for g in groups])
def predict(Ht, pools, est_idx, n_train, sims=300, seed=0):
    """frozen model: key frequencies and within-key class frequencies from est_idx; simulate n_train items"""
    keys = []; cls = defaultdict(list)
    for i in est_idx:
        k = (pools[i], z_label(Ht[i]), int(Ht[i].sum())); keys.append(k); cls[k].append(tuple(np.bincount(Ht[i], minlength=K)))
    kc = Counter(keys); klist = list(kc); kp = np.array([kc[k] for k in klist], float); kp /= kp.sum()
    rng = np.random.RandomState(seed); vals = []
    for _ in range(sims):
        draw = rng.choice(len(klist), n_train, p=kp); c = defaultdict(list)
        for j in draw:
            k = klist[j]; c[k].append(cls[k][rng.randint(len(cls[k]))])
        vals.append(maxchg_from_cells(c))
    return float(np.mean(vals)), float(np.std(vals))
out = {}
cm = pd.read_csv("/mnt/hdd2/jundahe/LLM-J/code/commit_message/data/CM-benchmark.csv"); pools = cm.msg_type.to_numpy(); groups = pd.factorize(cm.hash)[0]
print("=== (a) frozen support model: predicted vs observed max-changed fraction (commit, LORO, exact cells) ===")
for c in ["what", "why"]:
    H = cm[[f"{c}_{i}" for i in range(1, 7)]].to_numpy(int); rows = []
    for split in [0, 1, 2]:
        tr = grouped_split(groups, split); tr_idx = np.where(tr)[0]; est_idx = np.where(~tr)[0]     # estimate on the complementary 40 %
        for f in range(6):
            T = [r for r in range(6) if r != f]; Ht = H[:, T]
            obs = maxchg_from_cells(cells_of(Ht, pools, tr_idx)); pm, ps = predict(Ht, pools, est_idx, len(tr_idx), seed=split * 10 + f)
            rows.append(dict(split=split, fold=f, observed=obs, predicted=pm, pred_sd=ps))
    df = pd.DataFrame(rows); out[f"commit_{c}"] = rows
    err = (df.predicted - df.observed); print(f"COMMIT {c}: observed mean {df.observed.mean():.3f} [{df.observed.min():.3f},{df.observed.max():.3f}] | predicted mean {df.predicted.mean():.3f} | mean error {err.mean():+.3f}, MAE {err.abs().mean():.3f}, corr {np.corrcoef(df.predicted, df.observed)[0,1]:.2f} (18 split×fold cells)")
M = pd.read_csv("/mnt/hdd2/jundahe/LLM-J/code/code_readability/data/scalabrino/scores.csv", index_col=0); ds = pd.read_csv("/mnt/hdd2/jundahe/LLM-J/code/code_readability/data/coreeval_snippets/Scalabrino_java_Code.csv")
cols = list(M.columns); Hr = np.array([M.iloc[:, cols.index(f"Snippet{int(s)}")].to_numpy(int) for s in ds.snippet_id]) - 1; pr = np.array(["rd"] * len(Hr)); gr = np.arange(len(Hr))
rows = []
for split in [0, 1, 2]:
    tr = grouped_split(gr, split); tr_idx = np.where(tr)[0]; est_idx = np.where(~tr)[0]
    for f in range(9):
        T = [r for r in range(9) if r != f]; Ht = Hr[:, T]
        obs = maxchg_from_cells(cells_of(Ht, pr, tr_idx)); pm, ps = predict(Ht, pr, est_idx, len(tr_idx), seed=split * 10 + f); rows.append(dict(split=split, fold=f, observed=obs, predicted=pm, pred_sd=ps))
df = pd.DataFrame(rows); out["readability124"] = rows; err = df.predicted - df.observed
print(f"READABILITY(124): observed mean {df.observed.mean():.3f} [{df.observed.min():.3f},{df.observed.max():.3f}] | predicted mean {df.predicted.mean():.3f} | mean error {err.mean():+.3f}, MAE {err.abs().mean():.3f}, corr {np.corrcoef(df.predicted, df.observed)[0,1]:.2f} (27 cells)")
print("\n=== (b) subsampled-rater support curves (max-changed fraction, exact cells, split 0, mean over LORO folds and 5 rater subsets) ===")
for name, H, pl, grp, m, mts in [("commit what", cm[[f"what_{i}" for i in range(1,7)]].to_numpy(int), pools, groups, 6, [5,4,3]), ("commit why", cm[[f"why_{i}" for i in range(1,7)]].to_numpy(int), pools, groups, 6, [5,4,3]), ("readability124", Hr, pr, gr, 9, [8,6,4])]:
    tr_idx = np.where(grouped_split(grp, 0))[0]; line = []
    for mt in mts:
        vals = []
        for f in range(m):
            T = [r for r in range(m) if r != f]
            for s in range(5):
                sub = np.random.RandomState(100 * f + s).choice(T, mt, replace=False); vals.append(maxchg_from_cells(cells_of(H[:, sub], pl, tr_idx)))
        line.append(f"m_t={mt}: {np.mean(vals):.3f}"); out[f"curve_{name}_{mt}"] = float(np.mean(vals))
    print(f"{name:15s} " + " | ".join(line))
json.dump(out, open("/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/results/support_model.json", "w"), indent=1)
