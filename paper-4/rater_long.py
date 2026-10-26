"""Long-format ordered-probit with real rater ids (paper-4 PROTOCOL_STAGE1 estimand 3 for MultiPref; reusable for POPQUORN user ids).
Y*_{ir} = θ_i + δ_r + ε, y = k ⇔ c_{k-1} < Y* ≤ c_k (M1: rater shift δ_r; M1c: rater-specific cut-points via shift + log-scale; M0: δ ≡ 0).
Held-out log-likelihood per rating over 5 random cell folds (a held-out cell's rater and item both appear in training). Also: share of rating variance explained by item vs rater (from M1 fits).
Usage: python rater_long.py --panel multipref_overall"""
import os, sys, json, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", default="multipref_overall"); ap.add_argument("--iters", type=int, default=400); args = ap.parse_args(); torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"]))
PAN = data_panels.load(args.panel); H = PAN["H"]; K = PAN["K"]; n, m = H.shape; ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}
I = torch.tensor(np.repeat(np.arange(n), m)); Rr = torch.tensor([rid[e] for row in ev for e in row]); Y = torch.tensor(H.reshape(-1)); NR = len(raters)
Phi = lambda x: 0.5 * (1 + torch.erf(x / np.sqrt(2)))
def ll(par, model, idx):
    th = par["theta"][I[idx]]; c0 = par["c0"]; cuts = torch.cat([c0[:1], c0[:1] + torch.cumsum(torch.nn.functional.softplus(c0[1:]), 0)])
    if model >= 1: th = th + par["shift"][Rr[idx]]
    sc = torch.exp(par["lscale"][Rr[idx]]) if model == 2 else torch.ones(len(idx))
    z = (cuts[None, :] - th[:, None]) / sc[:, None]; cdf = torch.cat([torch.zeros(len(idx), 1), Phi(z), torch.ones(len(idx), 1)], 1); pk = (cdf[:, 1:] - cdf[:, :-1]).clamp_min(1e-9)
    return torch.log(pk[torch.arange(len(idx)), Y[idx]])
def fit(model, tr):
    par = {"theta": torch.zeros(n, requires_grad=True), "shift": torch.zeros(NR, requires_grad=model >= 1), "lscale": torch.zeros(NR, requires_grad=model == 2), "c0": torch.tensor([-1.0] + [0.0] * (K - 2), requires_grad=True)}
    opt = torch.optim.LBFGS([p for p in par.values() if p.requires_grad], lr=0.5, max_iter=args.iters, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); loss = -ll(par, model, tr).sum() + 1e-2 * (par["theta"] ** 2).sum() + 0.5 * (par["shift"] ** 2).sum() + 2.0 * (par["lscale"] ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return par
rng = np.random.RandomState(0); fold = rng.randint(0, 5, len(Y)); out = {"panel": args.panel, "n_items": n, "n_raters": NR, "ratings": int(len(Y))}
for model in (0, 1, 2):
    vals = []
    for f in range(5):
        tr = torch.tensor(np.where(fold != f)[0]); te = torch.tensor(np.where(fold == f)[0]); par = fit(model, tr)
        with torch.no_grad(): vals.append(float(ll(par, model, te).mean()))
    out[f"heldout_ll_M{model}"] = float(np.mean(vals)); print(args.panel, f"M{model} held-out LL/rating {np.mean(vals):.4f}", flush=True)
par = fit(1, torch.arange(len(Y)))
with torch.no_grad(): out["sd_theta"] = float(par["theta"].std()); out["sd_shift"] = float(par["shift"].std())
out["dLL_shift"] = out["heldout_ll_M1"] - out["heldout_ll_M0"]; out["dLL_scale"] = out["heldout_ll_M2"] - out["heldout_ll_M1"]
os.makedirs(f"{HERE}/results", exist_ok=True); json.dump(out, open(f"{HERE}/results/rater_long_{args.panel}.json", "w"), indent=1); print(json.dumps(out))
