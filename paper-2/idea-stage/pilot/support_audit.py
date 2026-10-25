"""
Support audit for exact target-link randomisation (corrected after external review round 2).
Cells: (pool, z_i, floor(sum_y / w)) over the TARGET raters of each evaluator fold; z_i = mode (ties -> closest to target median, then lower).
Quantities per fold (training items of a HASH-GROUPED 60% split):
  full    = fraction in cells where EVERY item can change at once (largest class M <= N/2)      [old, too strict]
  maxchg  = fraction changeable by a maximum-cardinality exact matching: sum_cells min(N, 2(N-M)) / n_train
  hetero  = fraction in heterogeneous cells (>= 2 distinct histograms) = items with positive change probability under randomised matching
  dose    = mean total-variation distance between original and donor histogram over changed items (one random maximum matching)
Usage: python support_audit.py  -> prints tables; writes results/support_audit.json
"""
import sys, os, json, numpy as np, pandas as pd
LLMJ = __import__("os").environ.get("LLMJ_ROOT", __import__("os").path.abspath(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "..", "..")))
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
K = 5
def z_label(r):
    vals, cnt = np.unique(r, return_counts=True); modes = vals[cnt == cnt.max()]
    if len(modes) == 1: return int(modes[0])
    med = np.median(r); d = np.abs(modes - med); return int(modes[d == d.min()].min())
def random_max_matching(items, hist, rng):
    """randomised maximum-cardinality assignment changing min(N, 2(N-M)) items: pair majority-class items with others, then derange the rest"""
    N = len(items); cls = defaultdict(list)
    for k, h in enumerate(hist): cls[h].append(k)
    if len(cls) < 2: return {}
    order = sorted(cls.values(), key=len, reverse=True); M = len(order[0])
    if M <= N / 2:                       # full derangement: random rotation over a class-sorted random order
        idx = [k for c in order for k in rng.permutation(c)]; shift = M
        return {items[idx[k]]: items[idx[(k + shift) % N]] for k in range(N) if hist[idx[k]] != hist[idx[(k + shift) % N]]}
    maj = list(rng.permutation(order[0])); rest = [k for c in order[1:] for k in rng.permutation(c)]   # |rest| = N-M < M
    m = len(rest); pairs = {}
    for a, b in zip(maj[:m], rest): pairs[items[a]] = items[b]; pairs[items[b]] = items[a]     # swap 2(N-M) items
    return pairs
def audit(H, pools, groups, folds, w=1, frac_train=0.6, seed=0):
    n, m = H.shape; rng = np.random.RandomState(seed); ug = np.unique(groups); rng.shuffle(ug)
    tr_groups = set(ug[: int(frac_train * len(ug))]); tr = np.array([g in tr_groups for g in groups])
    out = []
    for E in folds:
        T = [r for r in range(m) if r not in E]; Ht = H[:, T]; cells = defaultdict(list)
        for i in np.where(tr)[0]: cells[(pools[i], z_label(Ht[i]), int(Ht[i].sum()) // w)].append(i)
        full = maxchg = hetero = 0; doses = []; prng = np.random.RandomState(seed + 100 + len(out))
        for key, items in cells.items():
            N = len(items); hist = [tuple(np.bincount(Ht[i], minlength=K)) for i in items]; c = Counter(hist); M = max(c.values())
            if len(c) >= 2:
                hetero += N; maxchg += min(N, 2 * (N - M)); full += N if M <= N / 2 else 0
                pm = random_max_matching(items, hist, prng)
                for a, b in pm.items():
                    pa = np.bincount(Ht[a], minlength=K) / len(T); pb = np.bincount(Ht[b], minlength=K) / len(T); doses.append(0.5 * np.abs(pa - pb).sum())
        nt = tr.sum(); out.append(dict(fold=list(E), n_train=int(nt), full=full / nt, maxchg=maxchg / nt, hetero=hetero / nt, dose_tv=float(np.mean(doses)) if doses else 0.0))
    return out
if __name__ == "__main__":
    res = {}
    cm = pd.read_csv(LLMJ + "/code/commit_message/data/CM-benchmark.csv"); pools = cm.msg_type.to_numpy(); groups = pd.factorize(cm.hash)[0]
    for c in ["what", "why"]:
        H = cm[[f"{c}_{i}" for i in range(1, 7)]].to_numpy(int)
        for w in [1, 2]:
            r = audit(H, pools, groups, [(k,) for k in range(6)], w); res[f"commit_{c}_LORO_w{w}"] = r
            print(f"COMMIT {c:4s} LORO w={w}: full " + "/".join(f"{x['full']:.2f}" for x in r) + " | max-changed " + "/".join(f"{x['maxchg']:.2f}" for x in r) + " | hetero " + "/".join(f"{x['hetero']:.2f}" for x in r) + f" | dose TV {np.mean([x['dose_tv'] for x in r]):.2f}")
    M = pd.read_csv(LLMJ + "/code/code_readability/data/scalabrino/scores.csv", index_col=0); ds = pd.read_csv(LLMJ + "/code/code_readability/data/coreeval_snippets/Scalabrino_java_Code.csv")
    cols = list(M.columns); H = np.array([M.iloc[:, cols.index(f"Snippet{int(s)}")].to_numpy(int) for s in ds.snippet_id]) - 1
    r = audit(H, np.array(["rd"] * len(H)), np.arange(len(H)), [(k,) for k in range(9)], 1); res["readability124_LORO_w1"] = r
    print("READABILITY(124) LORO w=1: full " + "/".join(f"{x['full']:.2f}" for x in r) + " | max-changed " + "/".join(f"{x['maxchg']:.2f}" for x in r) + " | hetero " + "/".join(f"{x['hetero']:.2f}" for x in r) + f" | dose TV {np.mean([x['dose_tv'] for x in r]):.2f}")
    import cs_data
    for lang in ["Java"]:
        d = cs_data.load(lang); H = cs_data.H(d, "CA") - 1; groups = pd.factorize(d.target_id)[0]
        r = audit(H, np.array([lang] * len(H)), groups, [(k,) for k in range(3)], 1); res["summarization_CA_LOO_w1"] = r
        print("SUMMARIZATION CA LOO w=1: max-changed " + "/".join(f"{x['maxchg']:.2f}" for x in r))
    json.dump(res, open(LLMJ + "/paper-2/idea-stage/pilot/results/support_audit.json", "w"), indent=1)
