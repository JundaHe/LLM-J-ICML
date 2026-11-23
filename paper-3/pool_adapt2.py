"""
pool_adapt2 — PROTOCOL_CALIBRATION.md G1 with Amendment 4 (post hoc strict re-run of pool_adapt.py's v3 sweep): 20 group-disjoint 60/10/30 item splits, one head seed
per split, item-group bootstrap intervals on paired differences, and generic calibrators fitted on the same n pool-B ratings.
Pool A = largest group of the pool variable, pool B = each other group (or random halves of the raters, redrawn per split: the null shift). Head-A = frozen-feature head
trained on pool A's ratings of the training items. Arms on pool-B TEST ratings (RPS of the predicted distribution against each pool-B rating):
  none, map-A, oracle-B, map-B(n)            as in pool_adapt.py (map-B: n < 50 → pool-A map with the offset shrunk by n/(n+50); n ≥ 50 → full map with the pool-A prior)
  dir-B(n)                                   v3's generic arm: temperature + mixture with pool A's climatology on head-A's distribution
  tmix-B(n)                                  temperature + mixture with the climatology of the n pool-B ratings
  clim-B(n), bin-B(n), qbin-B(n), refit-B(n) target only: histogram of the n ratings (judge ignored); histogram binning on head-A's rounded expected rating; the same on
                                             equal-count bins; the ordered-probit map fitted from scratch on the n ratings (no pool-A prior)
Intervals: bootstrap over item groups, one draw of group multiplicities per replicate applied to every split's pool-B test ratings; statistic = mean over splits of the
weighted mean RPS (difference). Heads and calibrators are held fixed. A contrast uses the splits in which both arms exist; the number of splits is stored.
Usage: python pool_adapt2.py --panel dices990 --var rater_race [--splits 20] [--B 1000]
Output: paper-3/results/pool_adapt_v4/<panel>__<var>/summary.json + summary.md
"""
import os, sys, math, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np, pandas as pd, torch, torch.nn as nn
from scipy.optimize import minimize
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, HERE); sys.path.insert(0, P2)
import pools, data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--var", required=True); ap.add_argument("--n_list", default="20,50,all"); ap.add_argument("--min_group", type=int, default=10)
ap.add_argument("--splits", type=int, default=20); ap.add_argument("--B", type=int, default=1000); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--device", default="cpu"); ap.add_argument("--tag", default=""); args = ap.parse_args(); DEV = args.device; torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
P = pools.LOADERS[args.panel](); K = P["K"]; LV = np.arange(K, dtype=float); R = P["ratings"]; N = len(P["items"]); PAN2 = data_panels.load(P["panel"])
F = np.load(f"{P2}/features/{P['panel']}/{PAN2['model'].split('/')[-1]}.npz", allow_pickle=True); E = F["E_last"].astype(np.float32); assert len(E) == N, (len(E), N)
G = np.asarray(PAN2.get("groups", PAN2["item_ids"])); assert len(G) == N; UG, GI = np.unique(G, return_inverse=True); NG = len(UG)
N_LIST = [x if x == "all" else int(x) for x in args.n_list.split(",")]; N0_SHRINK = 50.0
OUT = f"{HERE}/results/pool_adapt_v4/{args.panel}__{args.var}{args.tag}"; os.makedirs(OUT, exist_ok=True)

def rps_rows(Pm_rows, y): cdf = np.cumsum(Pm_rows, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def hist_from(ratings):
    """soft histogram per item from a ratings subset; items without ratings get NaN rows (dropped by caller)"""
    h = np.full((N, K), np.nan)
    for i, grp in ratings.groupby("item"): h[i] = np.bincount(grp.y.to_numpy(), minlength=K) / len(grp)
    return h
class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train_head(Xtr, Ptr, Xva, yva_rows, rng, steps):
    """KL to the target; early stopping on validation CE against individual validation ratings (as pool_adapt.py)"""
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
def op_probs(s, par):
    a, b = par[0], par[1]; cuts = np.concatenate([[par[2]], par[2] + np.cumsum(np.log1p(np.exp(par[3:])))]); theta = a + b * s
    cdf = norm.cdf(cuts[None, :] - theta[:, None]); cdf = np.concatenate([np.zeros((len(s), 1)), cdf, np.ones((len(s), 1))], 1); return np.clip(np.diff(cdf, axis=1), 1e-9, 1)
def fit_map(s, y, par0=None, prior=None, lam_prior=1.0):
    def nll(par):
        v = -np.log(op_probs(s, par)[np.arange(len(y)), y]).sum()
        return v + (lam_prior * ((par - prior) ** 2).sum() if prior is not None else 0.01 * (par[1] ** 2 + (par[3:] ** 2).sum()))
    p0 = par0 if par0 is not None else np.concatenate([[0.0, 1.0, -0.5 * (K - 2) - 0.5], np.zeros(K - 2)])
    return minimize(nll, p0, method="L-BFGS-B").x
def calib_apply(Pm, T, lam, clim): q = np.exp(np.log(np.clip(Pm, 1e-9, 1)) / T); q /= q.sum(1, keepdims=True); return (1 - lam) * q + lam * clim
def fit_calib(Pm_rows, y, clim, Ts=(0.5, 0.7, 1.0, 1.5, 2.0, 3.0), lams=(0.0, 0.1, 0.2, 0.3, 0.5)):
    best = None
    for T in Ts:
        for lam in lams:
            nll = -np.log(calib_apply(Pm_rows, T, lam, clim)[np.arange(len(y)), y]).sum()
            if best is None or nll < best[0]: best = (nll, T, lam)
    return best[1], best[2]
def clim_of(y): return (np.bincount(y, minlength=K) + 0.5) / (len(y) + 0.5 * K)
def bin_table(b_items, y, nb, clim):
    """histogram binning: per bin, the calibration ratings' histogram plus a pseudo-count of 5 ratings distributed as the climatology"""
    C = np.zeros((nb, K)); np.add.at(C, (b_items, y), 1); return (C + 5 * clim) / (C.sum(1, keepdims=True) + 5)
lev = lambda s: np.clip(np.rint(s), 0, K - 1).astype(int)

SUM, CNT, INFO = {}, {}, {}     # SUM[pool][arm][isplit] = per-group sum of per-rating RPS on the pool-B test ratings; CNT[pool][isplit] = per-group number of test ratings
def run(isplit, poolsets):
    seed = isplit; rng = np.random.RandomState(seed * 1000 + isplit); ug = UG[np.random.RandomState(isplit).permutation(NG)]
    g_tr, g_ca = set(ug[: int(.6 * NG)]), set(ug[int(.6 * NG): int(.7 * NG)])
    part = np.array(["tr" if G[i] in g_tr else "ca" if G[i] in g_ca else "te" for i in range(N)]); tr, ca, te = (np.where(part == k)[0] for k in ("tr", "ca", "te"))
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W_ = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W_).astype(np.float32)
    A = poolsets["A"]; RA = R[R.rater.isin(A)]; hA = hist_from(RA); trA = np.array([i for i in tr if not np.isnan(hA[i, 0])])
    vaA = RA[RA.item.isin(set(ca))]; pos = {i: k for k, i in enumerate(ca)}; yva = np.array([(pos[i], y) for i, y in zip(vaA.item, vaA.y)])
    headA = train_head(X[trA], hA[trA], X[ca], yva, rng, args.steps); PA = pmf(headA, X); sA = PA @ LV; LEV = lev(sA)        # head-A on every item (indexed by item row)
    RA_ca = RA[RA.item.isin(set(ca))]; parA = fit_map(sA[RA_ca.item.to_numpy()], RA_ca.y.to_numpy()); climA = np.bincount(RA.y.to_numpy(), minlength=K) / len(RA)
    for bname, B in poolsets.items():
        if bname == "A": continue
        RB = R[R.rater.isin(B)]; RB_ca = RB[RB.item.isin(set(ca))]; RB_te = RB[RB.item.isin(set(te))]
        if len(RB_te) < 30 or len(RB_ca) < 20: continue
        it_te = RB_te.item.to_numpy(); y_te = RB_te.y.to_numpy(); g_te = GI[it_te]
        CNT.setdefault(bname, {})[isplit] = np.bincount(g_te, minlength=NG).astype(float)
        INFO.setdefault(bname, []).append(dict(isplit=isplit, poolA_size=len(A), poolB_size=len(B), n_cal_ratings=int(len(RB_ca)), n_test_ratings=int(len(RB_te))))
        def add(arm, Pm_full): SUM.setdefault(bname, {}).setdefault(arm, {})[isplit] = np.bincount(g_te, weights=rps_rows(Pm_full[it_te], y_te), minlength=NG)
        add("none", PA); add("map-A", op_probs(sA, parA))
        hB = hist_from(RB); trB = np.array([i for i in tr if not np.isnan(hB[i, 0])])
        if len(trB) >= 50:
            yvb = np.array([(pos[i], y) for i, y in zip(RB_ca.item, RB_ca.y)]); headB = train_head(X[trB], hB[trB], X[ca], yvb, np.random.RandomState(seed * 7 + 1), args.steps); add("oracle-B", pmf(headB, X))
        for n in N_LIST:
            nn_ = len(RB_ca) if n == "all" else n
            if nn_ > len(RB_ca): continue
            sub = RB_ca if n == "all" else RB_ca.sample(n=nn_, random_state=1000 + isplit); it = sub.item.to_numpy(); y = sub.y.to_numpy(); s_sub = sA[it]
            if nn_ < 50:   # Amendments 1–2: offset only, shrunk toward map-A with weight n/(n + 50)
                def nll_a(a_): p_ = parA.copy(); p_[0] = a_[0]; return -np.log(op_probs(s_sub, p_)[np.arange(len(y)), y]).sum()
                a_mle = minimize(nll_a, np.array([parA[0]]), method="L-BFGS-B").x[0]; parB = parA.copy(); parB[0] = parA[0] + (nn_ / (nn_ + N0_SHRINK)) * (a_mle - parA[0])
            else: parB = fit_map(s_sub, y, par0=parA, prior=parA)
            add(f"map-B({n})", op_probs(sA, parB))
            T, lam = fit_calib(PA[it], y, climA); add(f"dir-B({n})", calib_apply(PA, T, lam, climA))
            clim = clim_of(y); add(f"clim-B({n})", np.tile(clim, (N, 1)))
            T, lam = fit_calib(PA[it], y, clim, Ts=(0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0), lams=(0.0, 0.1, 0.2, 0.3, 0.5, 0.7)); add(f"tmix-B({n})", calib_apply(PA, T, lam, clim))
            add(f"bin-B({n})", bin_table(LEV[it], y, K, clim)[LEV])
            e = np.unique(np.quantile(s_sub, [0.2, 0.4, 0.6, 0.8])); add(f"qbin-B({n})", bin_table(np.searchsorted(e, s_sub, side="right"), y, len(e) + 1, clim)[np.searchsorted(e, sA, side="right")])
            add(f"refit-B({n})", op_probs(sA, fit_map(s_sub, y)))

if __name__ == "__main__":
    t0 = time.time()
    for isplit in range(args.splits):
        ps = pools.pools_for(P, args.var, args.min_group, seed=isplit)
        if not ps: print("no pools for", args.var); sys.exit(0)
        run(isplit, ps); print(f"  split {isplit} done [{time.time()-t0:.0f}s]", flush=True)
    rng = np.random.RandomState(17); W = np.vstack([np.ones(NG), rng.multinomial(NG, np.ones(NG) / NG, size=args.B)])   # row 0 = the point estimate
    def stat(pool, arm, splits): return np.mean([(W @ SUM[pool][arm][i]) / np.maximum(W @ CNT[pool][i], 1e-12) for i in splits], axis=0)
    def ci(v, k): return [float(v[0]), float(np.nanpercentile(v[1:], 2.5)), float(np.nanpercentile(v[1:], 97.5)), int(k)]
    res = dict(panel=args.panel, var=args.var, K=K, n_items=N, n_groups=NG, splits=args.splits, B=args.B, pools={}); L = []
    for pool in SUM:
        A_ = SUM[pool]; sp = lambda *arms: sorted(set.intersection(*[set(A_[a]) for a in arms])); arms = {a: ci(stat(pool, a, sorted(A_[a])), len(A_[a])) for a in A_}; con = {}
        def diff(a, b):
            if a in A_ and b in A_ and sp(a, b): s_ = sp(a, b); con[f"{a} - {b}"] = ci(stat(pool, a, s_) - stat(pool, b, s_), len(s_))
        diff("none", "oracle-B"); diff("map-A", "none")
        for n in N_LIST:
            for b in ("none", "map-A", "clim-B", "bin-B", "qbin-B", "refit-B", "dir-B", "tmix-B", "oracle-B"): diff(f"map-B({n})", b if b in ("none", "map-A", "oracle-B") else f"{b}({n})")
            diff(f"tmix-B({n})", "none"); diff(f"refit-B({n})", "none")
            if f"map-B({n})" in A_ and "oracle-B" in A_ and sp(f"map-B({n})", "oracle-B"):   # share of the gap closed (ratio of bootstrap means)
                s_ = sp(f"map-B({n})", "oracle-B"); num = stat(pool, "none", s_) - stat(pool, f"map-B({n})", s_); den = stat(pool, "none", s_) - stat(pool, "oracle-B", s_); con[f"recovered({n})"] = ci(num / np.where(np.abs(den) > 1e-9, den, np.nan), len(s_))
        I = pd.DataFrame(INFO[pool]); res["pools"][pool] = dict(arms=arms, contrasts=con, poolA_size=float(I.poolA_size.mean()), poolB_size=float(I.poolB_size.mean()), n_cal_ratings=float(I.n_cal_ratings.mean()), n_test_ratings=float(I.n_test_ratings.mean()), n_splits=int(len(I)))
        L += [f"## {args.panel} / {args.var}: pool A ({I.poolA_size.mean():.0f} raters) → {pool} ({I.poolB_size.mean():.0f} raters); {len(I)} splits; ≈ {I.n_cal_ratings.mean():.0f} calibration and {I.n_test_ratings.mean():.0f} test ratings per split", "", "| arm | RPS | splits |", "|---|---|---|"]
        L += [f"| {a} | {v[0]:.4f} [{v[1]:.4f}, {v[2]:.4f}] | {v[3]} |" for a, v in sorted(arms.items(), key=lambda kv: kv[1][0])] + ["", "| contrast | difference | splits |", "|---|---|---|"]
        L += [f"| {a} | {v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}] | {v[3]} |" for a, v in con.items()] + [""]
    json.dump(res, open(f"{OUT}/summary.json", "w"), indent=1); open(f"{OUT}/summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L), f"\n[{time.time()-t0:.0f}s]")
