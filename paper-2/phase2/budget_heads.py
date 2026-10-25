"""
budget_heads — SHRINKAGE_PROTOCOL.md "Fixed-budget decision experiment (learner side)". Same instrument as probe_shrink.py / probe_mean2.py (group-disjoint 60/10/30 item splits,
PCA-64, MLP head, KL to the target, early stopping on validation items vs training positions, RPS on held-out positions of ALL test items).
For a fixed rating budget B = n_train_items × a, the training set is a random fraction of the training groups with a training positions per item such that n × a = B:
  a ∈ A_LIST (e.g. 1, 2, 4, 8), n = n_full × a_min / a   (budget B = n_full × a_min); a second budget B2 = n_full × a_min × 2 is run when a_max permits (sensitivity).
Target = raw histogram of the a positions (a = 1 ⇒ one-hot of a single rating); q_T as a secondary target when a ≥ 3 (exact-T comparator needs ≥ 3 ratings).
Validation items keep the same a positions; evaluation uses the held-out positions (n_eval) of the full test set, so only the training information changes.
Output: results/budget_heads/<panel>/runs.jsonl + summary.md (RPS mean ± SEM over configurations per (budget, a, n)).
Usage: python budget_heads.py --panel dices990 --n_eval_raters 24 --a_list 1,2,4,8 [--seeds 5 --item_splits 3 --rater_splits 2]
"""
import argparse, os, sys, math, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "3")
import numpy as np, pandas as pd, torch, torch.nn as nn
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--feat_key", default="E_last"); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128)
ap.add_argument("--steps", type=int, default=1500); ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2)
ap.add_argument("--n_eval_raters", type=int, required=True); ap.add_argument("--a_list", default="1,2,4,8"); ap.add_argument("--budgets", default="1,2", help="multiples of n_full × a_min")
ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); ap.add_argument("--tag", default=""); args = ap.parse_args(); DEV = args.device; torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
PAN = data_panels.load(args.panel); H0 = PAN["H"].astype(int); N, M = H0.shape; K = PAN["K"]; LV = np.arange(K, dtype=float); NOMINAL = args.panel.startswith("chaosnli"); P = Panel(K, NOMINAL)
# nominal panels (ChaosNLI): the score is the KL from the held-out-position reference histogram to the prediction (T5 instrument), reported in the same `pop_rps` column
F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F[args.feat_key].astype(np.float32); assert np.array_equal(np.asarray(PAN["item_ids"]).astype(str), F["item_ids"].astype(str))
OUT = f"{HERE}/results/budget_heads/{args.panel}{args.tag}"; os.makedirs(OUT, exist_ok=True)
A_LIST = [int(x) for x in args.a_list.split(",")]; BUDGETS = [int(x) for x in args.budgets.split(",")]; A_LIST = [a for a in A_LIST if a <= M - args.n_eval_raters]

def rps(Pm, y): cdf = np.cumsum(Pm, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def kl_ref(Pm, Hte):
    ref = np.stack([np.bincount(r, minlength=K) for r in Hte]) / Hte.shape[1]; return (ref * (np.log(ref + 1e-9) - np.log(Pm + 1e-9))).sum(1)
class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva, rng, steps):
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV)
    yv = torch.tensor(Hva.ravel(), device=DEV); xv_rep = Xv.repeat_interleave(Hva.shape[1], 0); best = (1e9, None); pat = 0; bsz = min(256, len(Xtr))
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=bsz); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            m.eval()
            with torch.no_grad(): vl = nn.functional.cross_entropy(m(xv_rep), yv).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); m.eval(); return m, best[0]
def pmf(m, X):
    with torch.no_grad(): return torch.softmax(m(torch.tensor(X, device=DEV)), -1).cpu().numpy().astype(np.float64)

def run(seed, isplit, rsplit):
    rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
    G = np.asarray(PAN.get("groups", PAN["item_ids"])); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
    g_tr_all = ug[: int(.6 * len(ug))]; g_va = set(ug[int(.6 * len(ug)): int(.7 * len(ug))]); g_tr_set = set(g_tr_all)
    tr_all = np.array([i for i in range(N) if G[i] in g_tr_set]); va = np.array([i for i in range(N) if G[i] in g_va]); te = np.array([i for i in range(N) if G[i] not in g_tr_set and G[i] not in g_va])
    rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[: args.n_eval_raters]); R_pool = rp[args.n_eval_raters:]
    dd = min(args.d, len(tr_all) // 4); mu_e = E[tr_all].mean(0); U, Sv, Vt = np.linalg.svd(E[tr_all] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr_all)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    Hte = H0[np.ix_(te, R_eval)]; n_full = len(g_tr_all); a_min = min(A_LIST); rows = []
    for bm in BUDGETS:
        for a in A_LIST:
            n_groups = int(round(n_full * a_min * bm / a))
            if n_groups > n_full or n_groups < 20: continue
            g_sub = set(np.random.RandomState(1000 * seed + 17 * isplit + 3 * rsplit + a).permutation(g_tr_all)[:n_groups]); tr = np.array([i for i in tr_all if G[i] in g_sub])
            pos = np.sort(np.random.RandomState(2000 + seed + 11 * a).permutation(R_pool)[:a])
            Htr = H0[np.ix_(tr, pos)]; Hva = H0[np.ix_(va, pos)]; h = P.hist(Htr)
            targets = {"soft": h}
            if a >= 3:
                z, t, key, stat = P.T_of(Htr); fold = folds_for(G[tr], 1 + 7 * isplit, 5); targets["qT"] = P.exactT_q(fold, z, key, stat, h)
            for name, tgt_ in targets.items():
                m_, vl = train(X[tr], tgt_, X[va], Hva, rng, args.steps); Pm = pmf(m_, X[te])
                score = kl_ref(Pm, Hte).mean() if NOMINAL else np.mean([rps(Pm, Hte[:, j]).mean() for j in range(len(R_eval))])
                row = dict(seed=seed, isplit=isplit, rsplit=rsplit, budget_mult=bm, budget=int(n_groups * a), a=a, n_groups=n_groups, n_items=len(tr), arm=name, metric=("kl_ref" if NOMINAL else "rps"),
                           pop_rps=float(score), mean_spearman=float(pd.Series(Pm @ LV).corr(pd.Series(Hte.mean(1)), method="spearman")), val_ce=vl)
                rows.append(row); print(f"  s{seed} i{isplit} r{rsplit} B×{bm} a={a:2d} n={len(tr):5d} {name:4s} popRPS {row['pop_rps']:.4f}", flush=True)
    return rows

if __name__ == "__main__":
    t0 = time.time(); rows = []
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rows += run(seed, isplit, rsplit); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows); g = df.groupby(["budget_mult", "arm", "a"]).agg(n_items=("n_items", "mean"), rps=("pop_rps", "mean"), rps_sem=("pop_rps", "sem"), spearman=("mean_spearman", "mean"), cfgs=("pop_rps", "count")).round(5)
    txt = f"# budget_heads — {args.panel} (n_eval_raters={args.n_eval_raters}): {N}x{M}, K={K}; budgets = multiples of n_full × {min(A_LIST)}\n\n```\n{g.to_string()}\n```\n"
    open(f"{OUT}/summary.md", "w").write(txt); print(txt, f"[{time.time()-t0:.0f}s]")
