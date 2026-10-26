"""
probe_shrink — SHRINKAGE_PROTOCOL.md step 2 (frozen-feature heads; Gate H). Same instrument as probe_mean2.py (group-disjoint 60/10/30 item splits × annotation-position
splits, PCA-64 on training items, MLP head, KL to the target, early stopping on validation items vs TRAINING positions, RPS against HELD-OUT positions), with the training
target set to each of:
  soft     raw histogram of the training positions                       hard   one-hot at the mode
  qT       exact-T comparator (fr_lib.exactT_q, cross-fitted over training items)        [≈ mean2 / cond of T2b]
  shr      qT + λ̂ (soft − qT)                      λ̂ from the training items' TRAINING positions only (inner leave-one-rating-out, as shrink_targets.py)
  loc      location-shrunk prototype (ρ_loc)         shr2  loc + λ̂ (soft − qT)                                  [two-reliability target]
  dir_in   Dirichlet toward the mode prototype, κ by the same inner loo      ls_in  label smoothing, ε by the same inner loo
  dir_val  Dirichlet with κ tuned on VALIDATION items vs training positions (= T2b `shrunk`; ceiling)
  qs       response-based smoothed comparator fitted on a split of the training positions (predictor half → response half; other-fold items)   shr_s  qs + λ̂ (soft − qT)
Output: results/probe_shrink/<panel>/runs.jsonl + summary.md (mean ± SEM over configurations, as T2b). CPU or GPU.
Usage: python probe_shrink.py --panel summeval_coherence8 --n_eval_raters 2 [--seeds 5 --item_splits 3 --rater_splits 2 --d 64]
"""
import argparse, os, sys, math, itertools, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np, pandas as pd, torch, torch.nn as nn
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for
from support_audit import z_label
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--feat_key", default="E_last"); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128)
ap.add_argument("--steps", type=int, default=1500); ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2)
ap.add_argument("--n_eval_raters", type=int, required=True); ap.add_argument("--R_in", type=int, default=3); ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); ap.add_argument("--feat_model", default=None, help="feature file model tag (default: the panel model, e.g. Qwen2.5-7B-Instruct); e.g. Qwen3-8B"); ap.add_argument("--tag", default="")
args = ap.parse_args(); DEV = args.device; torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
PAN = data_panels.load(args.panel); H0 = PAN["H"].astype(int); N, M = H0.shape; K = PAN["K"]; LV = np.arange(K, dtype=float); NOMINAL = args.panel.startswith("chaosnli"); P = Panel(K, NOMINAL); C = P.C
F = np.load(f"{HERE}/features/{args.panel}/{args.feat_model or PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F[args.feat_key].astype(np.float32)
assert np.array_equal(np.asarray(PAN["item_ids"]).astype(str), F["item_ids"].astype(str))
OUT = f"{HERE}/results/probe_shrink/{args.panel}{args.tag}"; os.makedirs(OUT, exist_ok=True)
KAPPA_GRID = (0.5, 1, 2, 4, 8, 16); EPS_GRID = (0.02, 0.05, 0.1, 0.2, 0.3)

def rps(Pm, y): cdf = np.cumsum(Pm, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def loc(h): return h @ LV if not NOMINAL else h.max(1)
def protos(fold, z, h):
    out = np.zeros_like(h)
    for f in np.unique(fold):
        oth = fold != f
        for zz in range(K):
            sel = oth & (z == zz); out[(fold == f) & (z == zz)] = h[sel].mean(0) if sel.any() else np.full(K, 1 / K)
    return out
def tilt_vec(base, mu):
    base = np.clip(base, 1e-9, None); lo = np.full(len(base), -40.0); hi = np.full(len(base), 40.0)
    for _ in range(80):
        lam = (lo + hi) / 2; q = base * np.exp(lam[:, None] * LV); q /= q.sum(1, keepdims=True); m = q @ LV
        lo = np.where(m < mu, lam, lo); hi = np.where(m < mu, hi, lam)
    lam = (lo + hi) / 2; q = base * np.exp(lam[:, None] * LV); return q / q.sum(1, keepdims=True)
def loc_target(pi, z, loc_t):
    if not NOMINAL: return tilt_vec(pi, np.clip(loc_t, 0, K - 1))
    import targets as tgt
    return np.stack([tgt.nominal_zc(pi[i], int(z[i]), float(np.clip(loc_t[i], 1 / K + 1e-6, 1))) for i in range(len(pi))])
def inner_estimates(Htr, groups, rng):
    """λ̂, κ_in, ε_in, ρ_loc from the training items' training positions only (inner leave-one-rating-out + inner 5-fold exact-T comparator)"""
    n, a = Htr.shape; sx = sm = lx = lm = 0.0; sk = {k_: 0.0 for k_ in KAPPA_GRID}; se = {e_: 0.0 for e_ in EPS_GRID}; sg = {e_: 0.0 for e_ in EPS_GRID}
    for r in range(args.R_in):
        hp = rng.randint(0, a, n); keep = np.ones((n, a), bool); keep[np.arange(n), hp] = False
        Hm1 = Htr[keep].reshape(n, a - 1); y = Htr[np.arange(n), hp][:, None]
        hm1 = P.hist(Hm1); z, t, key, stat = P.T_of(Hm1); fi = folds_for(groups, 5000 + r, 5); q = P.exactT_q(fi, z, key, stat, hm1); pin = protos(fi, z, hm1); marg = hm1.mean(0)
        r1 = C(hm1 - q); r2 = C(np.eye(K)[y[:, 0]] - q); sx += (r1 * r2).sum(); sm += (r1 ** 2).sum()
        d1 = loc(hm1) - loc(pin); d2 = loc(np.eye(K)[y[:, 0]]) - loc(pin); lx += (d1 * d2).sum(); lm += (d1 ** 2).sum()
        for k_ in KAPPA_GRID: sk[k_] += P.score(((a - 1) * hm1 + k_ * pin) / (a - 1 + k_), y).sum()
        for e_ in EPS_GRID: se[e_] += P.score((1 - e_) * hm1 + e_ / K, y).sum(); sg[e_] += P.score((1 - e_) * hm1 + e_ * marg, y).sum()
    lam = float(np.clip(sx / sm, 0, 1)) if sm > 1e-12 else 0.0; rho_loc = float(np.clip(lx / lm, 0, 1)) if lm > 1e-12 else 0.0
    return lam, min(sk, key=sk.get), min(se, key=se.get), rho_loc, min(sg, key=sg.get)

class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva, rng, steps):
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4 if Xtr.shape[1] <= 256 else 1e-3)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV)
    yv = torch.tensor(Hva.ravel(), device=DEV); xv_rep = Xv.repeat_interleave(Hva.shape[1], 0); best = (1e9, None); pat = 0
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=256); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
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
    g_tr, g_va = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
    tr = np.array([i for i in range(N) if G[i] in g_tr]); va = np.array([i for i in range(N) if G[i] in g_va]); te = np.array([i for i in range(N) if G[i] not in g_tr and G[i] not in g_va])
    rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[: args.n_eval_raters]); R_train = np.sort(rp[args.n_eval_raters:])
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    Htr = H0[np.ix_(tr, R_train)]; Hva = H0[np.ix_(va, R_train)]; Hte = H0[np.ix_(te, R_eval)]; n_r = len(R_train); assert n_r >= 3, "need >= 3 training positions for the inner leave-one-rating-out"
    h = P.hist(Htr); z, t, key, stat = P.T_of(Htr); fold = folds_for(G[tr], 1 + 7 * isplit, 5); qT = P.exactT_q(fold, z, key, stat, h); pi = protos(fold, z, h)
    lam, k_in, e_in, rho_loc, em_in = inner_estimates(Htr, G[tr], np.random.RandomState(99 + seed))
    marg = np.zeros_like(h)
    for f_ in np.unique(fold): marg[fold == f_] = h[fold != f_].mean(0)          # other-fold marginal (climatology) for the marginal-smoothing arm
    T = {"soft": h, "hard": np.eye(K)[z], "qT": qT, "shr": qT + lam * (h - qT), "dir_in": (n_r * h + k_in * pi) / (n_r + k_in), "ls_in": (1 - e_in) * h + e_in / K, "lsm_in": (1 - em_in) * h + em_in * marg}
    locq = loc_target(pi, z, loc(pi) + rho_loc * (loc(h) - loc(pi))); T["loc"] = locq; T["shr2"] = locq + lam * (h - qT)
    # response-based smoothed comparator from a split of the TRAINING positions (predictor half -> response half), fitted on other-fold items
    if n_r >= 4:
        half = n_r // 2; Hp, Hr = Htr[:, :half], Htr[:, half:]; zp, tp, _, _ = P.T_of(Hp); hr = P.hist(Hr); bw, lam_s = P.select_bw_lam(G[tr], zp, tp, hr, Hr); qs = P.fit_q(fold, zp, tp, hr, bw, lam_s)
        T["qs"] = qs; T["shr_s"] = qs + lam * (h - qT)
    rows = []; meta = dict(seed=seed, isplit=isplit, rsplit=rsplit, lam_hat=lam, rho_loc=rho_loc, kappa_in=k_in, eps_in=e_in, eps_marg_in=em_in, n_train_pos=n_r)
    def score(name, Pm, extra=None):
        Pm = np.clip(Pm, 1e-9, None); Pm = Pm / Pm.sum(1, keepdims=True)
        row = dict(meta, arm=name, pop_rps=float(np.mean([rps(Pm, Hte[:, j]).mean() for j in range(len(R_eval))])), mean_spearman=float(pd.Series(Pm @ LV).corr(pd.Series(Hte.mean(1)), method="spearman")))
        if extra: row.update(extra)
        rows.append(row); print(f"  s{seed} i{isplit} r{rsplit} {name:7s} popRPS {row['pop_rps']:.4f}" + (f"  {extra}" if extra else ""), flush=True)
    for name, tgt_ in T.items():
        tgt_ = np.clip(tgt_, 0, None); tgt_ = tgt_ / tgt_.sum(1, keepdims=True); m_, vl = train(X[tr], tgt_, X[va], Hva, rng, args.steps); score(name, pmf(m_, X[te]))
    best = None
    for kap in KAPPA_GRID:
        m_, vl = train(X[tr], (n_r * h + kap * pi) / (n_r + kap), X[va], Hva, rng, args.steps)
        if best is None or vl < best[0]: best = (vl, kap, m_)
    score("dir_val", pmf(best[2], X[te]), {"param": best[1]})
    return rows

if __name__ == "__main__":
    t0 = time.time(); rows = []
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rows += run(seed, isplit, rsplit); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows); g = df.groupby("arm")["pop_rps"].agg(["mean", "sem", "count"]); soft = g.loc["soft", "mean"]; g["vs_soft"] = g["mean"] - soft
    # paired contrast vs soft per configuration (SEM over the dependent configurations, as T2b)
    piv = df.pivot_table(index=["seed", "isplit", "rsplit"], columns="arm", values="pop_rps"); d = piv.sub(piv["soft"], axis=0); g["vs_soft_sem"] = d.sem()
    g = g.sort_values("mean").round(5); lam = df.lam_hat.mean(); rl = df.rho_loc.mean()
    txt = f"# probe_shrink — {args.panel} (d={args.d}, n_eval_raters={args.n_eval_raters}): {N}x{M}, K={K}; mean λ̂ {lam:.3f}, mean ρ_loc {rl:.3f}; {len(piv)} configurations\n\n```\n{g.to_string()}\n```\n"
    open(f"{OUT}/summary.md", "w").write(txt); print(txt, f"[{time.time()-t0:.0f}s]")
