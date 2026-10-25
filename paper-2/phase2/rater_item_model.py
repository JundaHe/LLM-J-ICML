"""
rater_item_model — RATER_ITEM_MODEL_PROTOCOL.md estimands 1–2 (CPU, torch L-BFGS).
Ordered-probit / graded-response models of the rating matrix H (items × rater columns): Y* = θ_i + σ_i ε, y = k ⇔ c_{g(r),k-1} < Y* ≤ c_{g(r),k}
  M0  θ_i, common cut-points, σ ≡ 1          M1  + rater-specific cut-points (persistent raters only; non-persistent columns share one set)        M2  M1 + item dispersion σ_i
Estimand 1: held-out log-likelihood per rating, 5 random folds over cells.   Estimand 2: parametric-bootstrap simulation from each full-data fit → finite-rater X at a = m−1
(exact-T comparator; same construction as T9(a)) compared with the observed X.   Saves θ̂, σ̂ (M2, full data) for estimand 3 (decoding).
Usage: python rater_item_model.py --panel bw [--folds 5] [--sims 20] [--R 5]
"""
import sys, os, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, ci
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--folds", type=int, default=5); ap.add_argument("--sims", type=int, default=20); ap.add_argument("--R", type=int, default=5)
ap.add_argument("--iters", type=int, default=300); ap.add_argument("--lam_theta", type=float, default=1e-3); ap.add_argument("--lam_sigma", type=float, default=0.05); ap.add_argument("--lam_cut", type=float, default=0.1); ap.add_argument("--tag", default="")
args = ap.parse_args(); torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"])); torch.manual_seed(0)
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; n, m = H.shape; NOMINAL = args.panel.startswith("chaosnli"); assert not NOMINAL
rid = [str(x) for x in PAN["rater_ids"]]; persistent = np.array([not (r.startswith("pos") or r.startswith("turkpos")) for r in rid])
# rater groups: each persistent rater its own cut-point set; all non-persistent columns share group 0 (if any), persistent raters get 1..G
grp = np.zeros(m, int); g = 1 if (~persistent).any() else 0
for j in range(m):
    if persistent[j]: grp[j] = g; g += 1
NG = g if g > 0 else 1; P = Panel(K, False); C = P.C
Hm = torch.tensor(H); G = torch.tensor(grp)
Phi = lambda x: 0.5 * (1 + torch.erf(x / np.sqrt(2)))

LAM_SIG_GRID = (0.3, 1.0, 3.0, 10.0)          # ridge on log σ (shrinks item dispersion toward the common value); chosen by held-out LL (same folds for every model)
def unpack(par, model):
    theta = par["theta"]; logsig = 1.5 * torch.tanh(par["logsig"]) if model == 2 else torch.zeros(n)        # |log σ| ≤ 1.5 (σ ∈ [0.22, 4.5])
    a = par["a"]; b = par["b"]                                   # cut-points per group: c_0 = a_g, c_k = c_{k-1} + softplus(b_gk)
    if model == 0: a = a[:1].expand(NG); b = b[:1].expand(NG, K - 2)
    cuts = torch.cat([a[:, None], a[:, None] + torch.cumsum(torch.nn.functional.softplus(b), 1)], 1)       # NG × (K−1)
    return theta, logsig, cuts
def nll(par, model, mask, lam_sigma=None):
    lam_sigma = args.lam_sigma if lam_sigma is None else lam_sigma
    theta, logsig, cuts = unpack(par, model); sig = torch.exp(logsig)
    cu = cuts[G]                                                 # m × (K−1)
    z = (cu[None, :, :] - theta[:, None, None]) / sig[:, None, None]                  # n × m × (K−1)
    cdf = Phi(z); cdf = torch.cat([torch.zeros(n, m, 1), cdf, torch.ones(n, m, 1)], 2)
    pk = (cdf[:, :, 1:] - cdf[:, :, :-1]).clamp_min(1e-9)
    ll = torch.log(torch.gather(pk, 2, Hm[:, :, None])[:, :, 0])
    pen = args.lam_theta * (theta ** 2).sum() + lam_sigma * (logsig ** 2).sum() + (args.lam_cut * ((cuts - cuts.mean(0, keepdim=True)) ** 2).sum() if model >= 1 else 0.0)
    return -(ll * mask).sum() + pen, ll
def fit(model, mask, lam_sigma=None):
    par = {"theta": torch.zeros(n, requires_grad=True), "logsig": torch.zeros(n, requires_grad=(model == 2)),
           "a": torch.full((NG,), -1.0, requires_grad=True), "b": torch.zeros(NG, K - 2, requires_grad=True)}
    opt = torch.optim.LBFGS([p for p in par.values() if p.requires_grad], lr=0.5, max_iter=args.iters, history_size=20, line_search_fn="strong_wolfe")
    def closure():
        opt.zero_grad(); loss, _ = nll(par, model, mask, lam_sigma); loss.backward(); return loss
    opt.step(closure)
    with torch.no_grad(): return {k: v.detach().clone() for k, v in par.items()}

def finite_rater_X(Hmat, R):
    """observed/simulated residual reliability at a = m−1 with the exact-T comparator (T9(a) construction, R held-out positions drawn per item)"""
    groups = np.asarray(PAN.get("groups", np.arange(n))); Xs = []; A1x = []
    for r in range(R):
        H1, Y2 = splits(Hmat, m - 1, 1, r, loo_pos=r); h1 = P.hist(H1); h2 = P.hist(Y2); z, t, key, stat = P.T_of(H1); fold = folds_for(groups, 1)
        q = P.exactT_q(fold, z, key, stat, h1); r1 = C(h1 - q); r2 = C(h2 - q); Xs.append(((r1 * r2).sum(1) / (K - 1)).mean()); A1x.append((P.score(h1, Y2) - P.score(q, Y2)).mean())
    return float(np.mean(Xs)), float(np.mean(A1x))
def simulate(par, model, rng):
    with torch.no_grad():
        theta, logsig, cuts = unpack(par, model); sig = torch.exp(logsig); cu = cuts[G]
        ystar = theta[:, None] + sig[:, None] * torch.tensor(rng.randn(n, m), dtype=torch.float32)
        return (ystar[:, :, None] > cu[None, :, :]).sum(2).numpy().astype(int)

t0 = time.time(); res = dict(panel=args.panel, n_items=int(n), n_cols=int(m), K=K, n_rater_groups=int(NG), persistent_cols=int(persistent.sum()), protocol="RATER_ITEM_MODEL_PROTOCOL.md")
# ---- estimand 1: held-out log-likelihood over cells
rng = np.random.RandomState(0); cell_fold = rng.randint(0, args.folds, (n, m)); ll_out = {0: [], 1: [], 2: []}; ll_sig = {l: [] for l in LAM_SIG_GRID}
MODELS = [0, 1, 2] if NG > 1 else [0, 2]
for f in range(args.folds):
    mask = torch.tensor((cell_fold != f).astype(np.float32)); hold = 1 - mask
    for mdl in MODELS:
        if mdl == 2:
            for l in LAM_SIG_GRID:
                par = fit(2, mask, l); _, ll = nll(par, 2, mask, l); ll_sig[l].append(float((ll * hold).sum() / hold.sum()))
            continue
        par = fit(mdl, mask); _, ll = nll(par, mdl, mask); ll_out[mdl].append(float((ll * hold).sum() / hold.sum()))
best_lam = max(LAM_SIG_GRID, key=lambda l: np.mean(ll_sig[l])); ll_out[2] = ll_sig[best_lam]; args.lam_sigma = best_lam; res["lam_sigma_selected"] = best_lam; res["heldout_ll_M2_by_lam"] = {str(l): float(np.mean(v)) for l, v in ll_sig.items()}
res["heldout_ll_per_rating"] = {f"M{mdl}": dict(mean=float(np.mean(ll_out[mdl])), folds=ll_out[mdl]) for mdl in MODELS}
if 1 in MODELS: res["dLL_M1_M0"] = float(np.mean(ll_out[1]) - np.mean(ll_out[0])); res["dLL_M2_M1"] = float(np.mean(ll_out[2]) - np.mean(ll_out[1]))
res["dLL_M2_M0"] = float(np.mean(ll_out[2]) - np.mean(ll_out[0]))
print(f"{args.panel}: held-out LL/rating " + ", ".join(f"M{mdl} {np.mean(ll_out[mdl]):.4f}" for mdl in MODELS) + f"  [{time.time()-t0:.0f}s]", flush=True)
# ---- estimand 2: X observed vs simulated from full-data fits
full = torch.ones(n, m); X_obs, A1x_obs = finite_rater_X(H, args.R); res["X_obs"] = X_obs; res["A1x_obs"] = A1x_obs
sim = {}
for mdl in MODELS:
    par = fit(mdl, full); xs = []; a1 = []; srng = np.random.RandomState(100 + mdl)
    for s in range(args.sims):
        Hs = simulate(par, mdl, srng); x, a = finite_rater_X(Hs, max(2, args.R // 2)); xs.append(x); a1.append(a)
    sim[f"M{mdl}"] = dict(X_mean=float(np.mean(xs)), X_ci95=ci(xs), A1x_mean=float(np.mean(a1)))
    if mdl == 2:
        theta, logsig, cuts = unpack(par, 2)
        os.makedirs(f"{HERE}/results/rater_item", exist_ok=True)
        np.savez(f"{HERE}/results/rater_item/{args.panel}_M2_params.npz", theta=theta.numpy(), sigma=torch.exp(logsig).numpy(), cuts=cuts.numpy(), rater_group=grp, item_ids=np.asarray(PAN["item_ids"]))
        res["sigma_summary"] = dict(median=float(np.median(torch.exp(logsig).numpy())), q10=float(np.quantile(torch.exp(logsig).numpy(), .1)), q90=float(np.quantile(torch.exp(logsig).numpy(), .9)))
    print(f"  M{mdl}: X_sim {np.mean(xs):+.5f} {ci(xs)}  (X_obs {X_obs:+.5f}, A1x_obs {A1x_obs:+.5f})", flush=True)
res["X_sim"] = sim; res["seconds"] = round(time.time() - t0, 1)
os.makedirs(f"{HERE}/results/rater_item", exist_ok=True); json.dump(res, open(f"{HERE}/results/rater_item/{args.panel}{args.tag}.json", "w"), indent=1, default=float)
print(json.dumps({k: res[k] for k in res if k in ("dLL_M1_M0", "dLL_M2_M1", "dLL_M2_M0", "X_obs", "sigma_summary")}, default=float), flush=True)
