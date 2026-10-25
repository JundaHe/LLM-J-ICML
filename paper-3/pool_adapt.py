"""
pool_adapt — PROTOCOL_CALIBRATION.md G1 (pool adaptation) with frozen-feature heads (paper-2 instrument: group-disjoint 60/10/30 item splits, PCA-64, MLP head, KL to the target).
For a panel and a pool variable: pool A = largest group, pool B = each other group (or random halves of the raters, the null shift).
  head-A       trained on pool A's ratings of the training items (soft histogram over A's ratings per item)
  arms on pool-B TEST ratings (RPS of the predicted distribution against each pool-B rating, averaged):
    none      head-A's own distribution
    map-A     panel map (ordered probit: θ = α + β·s, cut-points) fitted on pool A's CALIBRATION ratings; s = head-A expected rating
    map-B(n)  panel map fitted on n pool-B ratings sampled from the calibration items (n ∈ N_LIST, 'all')
    dir-B(n)  generic post-hoc calibration of head-A's distribution on the same n ratings: temperature T and climatology weight λ (grid, NLL)
    oracle-B  head trained on pool B's ratings of the training items
    (rater-B(n): per-rater cut-points — v2)
Usage: python pool_adapt.py --panel dices --var rater_gender [--n_list 10,20,50,100] [--seeds 5 --item_splits 3] [--min_group 10]
Output: paper-3/results/pool_adapt/<panel>__<var>/runs.jsonl + summary.md
"""
import os, sys, math, json, argparse, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np, pandas as pd, torch, torch.nn as nn
from scipy.optimize import minimize
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, HERE); sys.path.insert(0, P2)
import pools, data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--var", required=True); ap.add_argument("--n_list", default="10,20,50,100"); ap.add_argument("--min_group", type=int, default=10)
ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--device", default="cpu"); ap.add_argument("--tag", default=""); args = ap.parse_args(); DEV = args.device; torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
P = pools.LOADERS[args.panel](); K = P["K"]; LV = np.arange(K, dtype=float); R = P["ratings"]; N = len(P["items"]); PAN2 = data_panels.load(P["panel"])
F = np.load(f"{P2}/features/{P['panel']}/{PAN2['model'].split('/')[-1]}.npz", allow_pickle=True); E = F["E_last"].astype(np.float32); assert len(E) == N, (len(E), N)
G = np.asarray(PAN2.get("groups", PAN2["item_ids"])); assert len(G) == N
N_LIST = [int(x) for x in args.n_list.split(",")]
OUT = f"{HERE}/results/pool_adapt/{args.panel}__{args.var}{args.tag}"; os.makedirs(OUT, exist_ok=True)

def rps_rows(Pm_rows, y): cdf = np.cumsum(Pm_rows, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def hist_from(ratings, items_idx):
    """soft histogram per item from a ratings subset; items without ratings get NaN rows (dropped by caller)"""
    h = np.full((N, K), np.nan); g = ratings.groupby("item")
    for i, grp in g: h[i] = np.bincount(grp.y.to_numpy(), minlength=K) / len(grp)
    return h
class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train_head(Xtr, Ptr, Xva, yva_rows, rng, steps):
    """KL to the target; early stopping on validation CE against individual validation ratings (yva_rows: (item_row_index_into_Xva, y))"""
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva[yva_rows[:, 0]], device=DEV); yv = torch.tensor(yva_rows[:, 1], device=DEV)
    best = (1e9, None); pat = 0; bsz = min(256, len(Xtr))
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=bsz); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            m.eval()
            with torch.no_grad(): vl = nn.functional.cross_entropy(m(Xv), yv).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); m.eval(); return m
def pmf(m, X):
    with torch.no_grad(): return torch.softmax(m(torch.tensor(X, device=DEV)), -1).cpu().numpy().astype(np.float64)
# ---- panel map: ordered probit θ = a + b·s with cut-points
def op_probs(s, par):
    a, b = par[0], par[1]; cuts = np.concatenate([[par[2]], par[2] + np.cumsum(np.log1p(np.exp(par[3:])))]); theta = a + b * s
    cdf = norm.cdf(cuts[None, :] - theta[:, None]); cdf = np.concatenate([np.zeros((len(s), 1)), cdf, np.ones((len(s), 1))], 1); return np.clip(np.diff(cdf, axis=1), 1e-9, 1)
def fit_map(s, y, par0=None, prior=None, lam_prior=1.0):
    """s: per-rating scores (item score repeated per rating), y: ratings. With `prior` (the pool-A map), the fit is shrunk toward it: penalty lam_prior·||par − prior||² —
    so a map fitted on 10 pool-B ratings stays close to the pool-A map and moves away as pool-B evidence accumulates (protocol: implementation detail, set before any real run)."""
    def nll(par):
        v = -np.log(op_probs(s, par)[np.arange(len(y)), y]).sum()
        return v + (lam_prior * ((par - prior) ** 2).sum() if prior is not None else 0.01 * (par[1] ** 2 + (par[3:] ** 2).sum()))
    p0 = par0 if par0 is not None else np.concatenate([[0.0, 1.0, -0.5 * (K - 2) - 0.5], np.zeros(K - 2)])
    r = minimize(nll, p0, method="L-BFGS-B"); return r.x
# ---- generic calibration: temperature + climatology mixture on the head's distribution
def calib_apply(Pm, T, lam, clim): q = np.exp(np.log(np.clip(Pm, 1e-9, 1)) / T); q /= q.sum(1, keepdims=True); return (1 - lam) * q + lam * clim
def fit_calib(Pm_rows, y, clim):
    best = None
    for T in (0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
        for lam in (0.0, 0.1, 0.2, 0.3, 0.5):
            nll = -np.log(calib_apply(Pm_rows, T, lam, clim)[np.arange(len(y)), y]).sum()
            if best is None or nll < best[0]: best = (nll, T, lam)
    return best[1], best[2]

def run(seed, isplit, poolsets):
    rng = np.random.RandomState(seed * 1000 + isplit); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
    g_tr, g_ca = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
    part = np.array(["tr" if G[i] in g_tr else "ca" if G[i] in g_ca else "te" for i in range(N)]); tr, ca, te = (np.where(part == k)[0] for k in ("tr", "ca", "te"))
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    A = poolsets["A"]; RA = R[R.rater.isin(A)]; hA = hist_from(RA, None); trA = np.array([i for i in tr if not np.isnan(hA[i, 0])])
    vaA = RA[RA.item.isin(set(ca))]; pos = {i: k for k, i in enumerate(ca)}; yva = np.array([(pos[i], y) for i, y in zip(vaA.item, vaA.y)])
    headA = train_head(X[trA], hA[trA], X[ca], yva, rng, args.steps); PA_ca = pmf(headA, X[ca]); PA_te = pmf(headA, X[te]); sA_ca = PA_ca @ LV; sA_te = PA_te @ LV
    rows = []
    for bname, B in poolsets.items():
        if bname == "A": continue
        RB = R[R.rater.isin(B)]; RB_ca = RB[RB.item.isin(set(ca))]; RB_te = RB[RB.item.isin(set(te))]
        if len(RB_te) < 30 or len(RB_ca) < max(N_LIST[0], 10): continue
        pte = {i: k for k, i in enumerate(te)}; rows_te = np.array([pte[i] for i in RB_te.item]); y_te = RB_te.y.to_numpy()
        pca_ = {i: k for k, i in enumerate(ca)}
        def score(name, Pm_te_rows, extra=None):
            r = dict(seed=seed, isplit=isplit, poolA_size=len(A), poolB=bname, poolB_size=len(B), n_ratings_te=len(y_te), arm=name, rps=float(rps_rows(Pm_te_rows, y_te).mean())); r.update(extra or {}); rows.append(r)
        score("none", PA_te[rows_te])
        # map-A on pool A's calibration ratings
        RA_ca = RA[RA.item.isin(set(ca))]; parA = fit_map(sA_ca[[pca_[i] for i in RA_ca.item]], RA_ca.y.to_numpy()); score("map-A", op_probs(sA_te, parA)[rows_te])
        climA = np.bincount(RA.y.to_numpy(), minlength=K) / len(RA)
        # oracle: head trained on pool B
        hB = hist_from(RB, None); trB = np.array([i for i in tr if not np.isnan(hB[i, 0])])
        if len(trB) >= 50:
            yvb = np.array([(pos[i], y) for i, y in zip(RB_ca.item, RB_ca.y)]); headB = train_head(X[trB], hB[trB], X[ca], yvb, np.random.RandomState(seed * 7 + 1), args.steps); score("oracle-B", pmf(headB, X[te])[rows_te], {"n_train_items_B": int(len(trB))})
        # map-B(n) and dir-B(n) on n sampled pool-B calibration ratings
        for n in N_LIST + ["all"]:
            nn_ = len(RB_ca) if n == "all" else n
            if nn_ > len(RB_ca): continue
            sub = RB_ca.sample(n=nn_, random_state=seed * 100 + isplit) if n != "all" else RB_ca
            s_sub = sA_ca[[pca_[i] for i in sub.item]]; y_sub = sub.y.to_numpy()
            parB = fit_map(s_sub, y_sub, par0=parA, prior=parA); score(f"map-B({n})", op_probs(sA_te, parB)[rows_te], {"n_cal": int(nn_)})
            T, lam = fit_calib(PA_ca[[pca_[i] for i in sub.item]], y_sub, climA); score(f"dir-B({n})", calib_apply(PA_te, T, lam, climA)[rows_te], {"n_cal": int(nn_), "T": T, "lam": lam})
    return rows

if __name__ == "__main__":
    t0 = time.time(); rows = []
    for seed, isplit in itertools.product(range(args.seeds), range(args.item_splits)):
        ps = pools.pools_for(P, args.var, args.min_group, seed=seed)
        if not ps: print("no pools for", args.var); sys.exit(0)
        rows += run(seed, isplit, ps); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
        print(f"  seed {seed} split {isplit} done [{time.time()-t0:.0f}s]", flush=True)
    df = pd.DataFrame(rows); piv = df.pivot_table(index=["poolB", "seed", "isplit"], columns="arm", values="rps")
    out = []
    for b, sub in piv.groupby(level=0):
        d = sub.sub(sub["none"], axis=0); g = pd.DataFrame({"rps": sub.mean(), "vs_none": d.mean(), "vs_none_sem": d.sem()}).round(5)
        out.append(f"## {args.panel} / {args.var}: pool A (n={df.poolA_size.iloc[0]}) → {b} (n={df[df.poolB==b].poolB_size.iloc[0]}); {len(sub)} configurations\n\n```\n{g.to_string()}\n```\n")
    open(f"{OUT}/summary.md", "w").write("\n".join(out)); print("\n".join(out), f"[{time.time()-t0:.0f}s]")
