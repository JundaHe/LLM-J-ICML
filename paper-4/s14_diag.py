"""Stage 14 Amendment 1, A1-1 (PROTOCOL_STAGE14.md): why does the pipeline's DL recover a tenth of the CF gain on seen Jester jokes? Fold 0, L1 configuration
(item-identity encoding, rating-level validation). Executes the factorised_rm.py definitions unchanged (source cut before the fold loop) and instruments the fit:
L-BFGS iterations used, penalised training objective, validation log-likelihood, size of the latent term, and seen-joke concordance own − μ at k = 20 (support
draw 0) over a grid of adaptation strengths. Exploratory, post hoc. DIAG_PART=0|1 splits the configurations over two processes.
Output: results/stage14_diag_part<p>.json"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); PART = int(os.environ.get("DIAG_PART", "0"))
sys.argv = [sys.argv[0], "--panel", "jester_raters", "--models", "D,DL,T0,L", "--folds", "0", "--val_ratings", "--seen_items", "--concord"]
src = open(f"{HERE}/factorised_rm.py").read(); cut = "# ---------------------------------------------------------------- folds"; assert src.count(cut) == 1
exec(compile(src[:src.index(cut)], "factorised_rm.py", "exec"))
# ---- fold 0 index sets, exactly as the fold loop builds them
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
f = 0; k = 20; dr = 0
test_r = rfold == f; tr_item = ifold[I] != f; is_tr_r = ~test_r[R]; va_item = np.random.RandomState(1).rand(len(I)) < 0.15
idx_tr = np.where(is_tr_r & tr_item & ~va_item)[0]; idx_va = np.where(is_tr_r & tr_item & va_item)[0]; idx_ad_pool = np.where(~is_tr_r & tr_item)[0]; idx_te = np.where(~is_tr_r & ~tr_item)[0]
rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep = []
for r in np.unique(R[idx_te]):
    pool = idx_ad_pool[R[idx_ad_pool] == r]
    if len(pool) < k: continue
    keep.append(r); ad.extend(rng.choice(pool, k, replace=False))
ad = np.array(ad, int); ts = np.setdiff1d(idx_ad_pool[np.isin(R[idx_ad_pool], keep)], ad)
def conc(ey):
    """pooled within-rater concordance on the seen cell (prediction ties count 1/2)"""
    c = d = 0.0
    for r in keep:
        sel = R[ts] == r; yy = Y[ts][sel]; e = ey[sel]; ui, uj = np.triu_indices(len(yy), 1); ok = yy[ui] != yy[uj]; sg = (np.sign(e[ui] - e[uj]) * np.sign(yy[ui] - yy[uj]))[ok]
        c += (sg > 0).sum() + 0.5 * (sg == 0).sum(); d += ok.sum()
    return 100 * c / d
CFR = [r_ for r_ in json.load(open(f"{HERE}/results/stage14_cf.json"))["per_rater"] if r_["fold"] == f and r_["k"] == k and r_["draw"] == dr]
cf_gain = 100 * (sum(r_["cf_conc"] for r_ in CFR) - sum(r_["mu_conc"] for r_ in CFR)) / sum(r_["den_s"] for r_ in CFR)
print(f"fold {f} k={k} draw {dr}: {len(keep)} test raters, {len(ts)} seen-cell ratings, {len(idx_tr)} training ratings; CF own − μ on this draw {cf_gain:+.2f}", flush=True)
def fit2(kind, lam, iters, init):
    """Model.fit with the L-BFGS state exposed; init: None = the pipeline's start, else scale of a random start for z and the loading matrix"""
    m = Model(kind, lam); keys = mdl_keys(kind)
    if init:
        g = torch.Generator().manual_seed(100); m.p["z"] = init * torch.randn(NR, args.d, generator=g); m.p["W5"] = init * torch.randn(XD, args.d * K, generator=g); m.p["W"] = init * torch.randn(XD, args.d, generator=g)
    ii = torch.tensor(I[idx_tr]); rr = torch.tensor(R[idx_tr]); yy = torch.tensor(Y[idx_tr])
    for kk in m.p: m.p[kk].requires_grad_(kk in keys)
    opt = torch.optim.LBFGS([m.p[kk] for kk in keys], lr=0.5, max_iter=iters, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); loss = -m.logp(ii, rr)[torch.arange(len(yy)), yy].sum() + m.penalty(keys); loss.backward(); return loss
    opt.step(cl); st = opt.state[opt._params[0]]; obj = float(cl())
    for kk in m.p: m.p[kk] = m.p[kk].detach()
    with torch.no_grad():
        x = X[ii]; lat = ((x @ m.p["W5"] + m.p["w0"]).view(len(ii), args.d, K) * m.p["z"][rr][:, :, None]).sum(1) if kind == "DL" else ((x @ m.p["W"] + m.p["wl0"]) * m.p["z"][rr]).sum(1)[:, None]
        lat_sd = float((lat - lat.mean(1, keepdim=True)).std()) if kind == "DL" else float(lat.std())
    return m, {"n_iter": int(st["n_iter"]), "func_evals": int(st["func_evals"]), "hit_cap": bool(st["n_iter"] >= iters), "objective": obj, "val_ll": float(m.per_rating(idx_va)[0].mean()), "latent_sd": lat_sd}
def whiten(m):
    """A1-3: z = zbar + L u with L = chol(cov of the training raters' z); the constant part goes to the text head; training-rater predictions must not change"""
    tr = torch.tensor(np.unique(R[idx_tr])); chk = idx_tr[:5000]; before = m.logp(torch.tensor(I[chk]), torch.tensor(R[chk])).clone(); d = args.d
    zb = m.p["z"][tr].mean(0); Lc = torch.linalg.cholesky(torch.cov((m.p["z"][tr] - zb).T) + 1e-10 * torch.eye(d)); u = torch.zeros_like(m.p["z"]); u[tr] = torch.linalg.solve_triangular(Lc, (m.p["z"][tr] - zb).T, upper=False).T
    if m.kind == "DL":
        W5v = m.p["W5"].view(XD, d, K); w0v = m.p["w0"].view(d, K); m.p["V"] = m.p["V"] + torch.einsum("xdk,d->xk", W5v, zb); m.p["b"] = m.p["b"] + torch.einsum("dk,d->k", w0v, zb)
        m.p["W5"] = torch.einsum("xdk,de->xek", W5v, Lc).reshape(XD, d * K); m.p["w0"] = torch.einsum("dk,de->ek", w0v, Lc).reshape(d * K)
    else:
        m.p["beta"] = m.p["beta"] + m.p["W"] @ zb; m.p["c0"] = m.p["c0"].clone(); m.p["c0"][0] -= m.p["wl0"] @ zb; m.p["W"] = m.p["W"] @ Lc; m.p["wl0"] = m.p["wl0"] @ Lc
    m.p["z"] = u; set_center(m, idx_tr); return float((m.logp(torch.tensor(I[chk]), torch.tensor(R[chk])) - before).abs().max())
WHITEN = os.environ.get("DIAG_WHITEN") == "1"
t0 = time.time(); LBsel = {}
for base in ("D", "T0"): train(base, idx_tr, idx_va); LBsel[base] = SEL[base][0]; print(f"{base}: λ_text {LBsel[base]} val LL {VAL[base]:.4f} [{time.time()-t0:.0f}s]", flush=True)
CONF = [("DL", 512, 10, 300, None), ("DL", 512, 10, 3000, None), ("DL", 32, 10, 300, None), ("DL", 32, 10, 3000, None), ("DL", 2, 10, 300, None), ("DL", 2, 10, 3000, None), ("DL", 32, 1, 3000, None), ("DL", 2, 1, 3000, None),
        ("DL", 512, 10, 3000, 0.1), ("DL", 32, 10, 3000, 0.1), ("DL", 2, 10, 3000, 0.1), ("DL", 2, 1, 3000, 0.1),
        ("L", 512, 10, 300, None), ("L", 32, 10, 300, None), ("L", 32, 10, 3000, None), ("L", 2, 10, 3000, None), ("L", 2, 1, 3000, None), ("L", 32, 10, 3000, 0.1), ("L", 2, 10, 3000, 0.1), ("L", 2, 1, 3000, 0.1)]
if WHITEN: CONF = [("DL", 512, 10, 300, None), ("L", 512, 10, 300, None), ("DL", 32, 10, 300, None), ("L", 32, 10, 300, None), ("DL", 2, 10, 300, None), ("L", 2, 10, 3000, None), ("DL", 2, 1, 3000, None)]
out = {"fold": f, "k": k, "draw": dr, "cf_gain": cf_gain, "lam_text": LBsel, "rows": []}
for j, (kind, lr, lw, iters, init) in enumerate(CONF):
    if j % 2 != PART: continue
    t1 = time.time(); m, info = fit2(kind, (LBsel["D" if kind == "DL" else "T0"], lr, lw), iters, init); set_center(m, idx_tr)
    if WHITEN: info["whiten_check"] = whiten(m)
    m0 = Model(kind, m.lam); m0.p = {kk: v.clone() for kk, v in m.p.items()}; m0.p["z"] = m.center["z"].clone(); c0 = conc(m0.per_rating(ts)[3]); gains = {}
    for la in ((0.125, 0.5, 2, 8, 32) if WHITEN else (0.5, 8, 128, 2048, 32768)):
        gains[la] = conc(adapt(m, ad, la).per_rating(ts)[3]) - c0
    row = {"kind": kind, "lam_rater": lr, "lam_W": lw, "iters": iters, "init": init, **info, "prior_conc": c0, "gain_by_adapt_strength": gains, "best_gain": max(gains.values()), "seconds": round(time.time() - t1)}
    out["rows"].append(row); print(json.dumps(row), flush=True)
    json.dump(out, open(f"{HERE}/results/stage14_diag{'_whiten' if WHITEN else ''}_part{PART}.json", "w"), indent=1)
print(f"done [{time.time()-t0:.0f}s]")
