"""Stage 9 Am. 4 (PROTOCOL_STAGE9.md): matched-feature comparator and transfer-based screen. `sap_ext.py lr <tag>`: ATTR-LR, θ_r = μ + W z_r with W (24 × 2)
learned on the training raters (ridge on W by half-split), z_r ~ N(0, I); `sap_ext.py tr <tag>`: SAP-T, SAP whose attributes are kept only if deleting their prior
variance lowers held-out LL of pseudo-new training raters adapted on k = 20. Same base, dictionary, folds, draws and contrasts as sap.py (shared code below is copied from it)."""
import sys; MODE = sys.argv.pop(1); assert MODE in ("lr", "tr", "lr2")   # lr2: Stage 9 Am. 6/8 — W ridge and adaptation strength (incl. none) chosen on pseudo-new raters at k = 20
import os, sys, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
from attr_feats import multipref_G, NAMES
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); K = 5; STEP = torch.tensor([-2., -1., 0., 1., 2.]); SYM = [0, 1, 2, 1, 0]
base = data_panels.load("multipref_overall"); Hreal = base["H"]; n, m = Hreal.shape; ev = base["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
for j in range(len(R)): GRP[R[j]] = int(POS[j] >= 2)
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
Gp = np.asarray(base["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])   # folds exactly as s5.py
tag = sys.argv[1]; ISO = tag.endswith("_iso"); ptag = tag[:-4] if ISO else tag                     # Am. 3 (a): "_iso" = one shared prior variance
if ptag == "real": H = Hreal
elif ptag == "real_perm":                                                  # Am. 3 (d): each item's ratings permuted across its raters
    rp = np.random.RandomState(5); H = np.array([row[rp.permutation(m)] for row in Hreal])
else: H = np.load(f"{HERE}/results/synth/multipref_synth_{ptag}.npz")["H"]
Y = H.reshape(-1); Yt = torch.tensor(Y); It, Rt = torch.tensor(I), torch.tensor(R)
F_ = np.load(f"{P2}/features/multipref_overall/Qwen2.5-7B-Instruct.npz", allow_pickle=True)
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, _ = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0); X = torch.tensor(X)
raw = [json.loads(l) for l in open(data_panels.MULTIPREF)]; A = torch.tensor(multipref_G(raw)); J = A.shape[1]; AR = A[It]
def fit(lpb, idx, mu, prec, mask, lam_s=2.0, shared=False):
    """MAP on rows idx: θ = μ + mask ⊙ δ per rater (or one shared θ if shared), prior precision prec (J,) on δ; style offsets Bs per rater, ridge lam_s"""
    d = torch.zeros(1 if shared else NR, J, requires_grad=True); Bs = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx)
    opt = torch.optim.LBFGS([d, Bs], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = mu + mask * d; c = (AR[ii] @ th[0]) if shared else (th[Rt[ii]] * AR[ii]).sum(1); lp = torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
        loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + 0.5 * (prec * d ** 2).sum() + lam_s * (Bs ** 2).sum(); loss.backward(); return loss
    opt.step(cl); th = (mu + mask * d).detach(); return (th.expand(NR, -1).clone() if shared else th), Bs.detach()
def predict(lpb, idx, th, Bs):
    ii = torch.tensor(idx); c = (th[Rt[ii]] * AR[ii]).sum(1); return torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
def dirc(lp, idx):
    ey = (lp.exp() * torch.arange(K)).sum(1).numpy(); y = Y[idx]; return np.where(y == 2, np.nan, (np.sign(ey - 2) == np.sign(y - 2)).astype(float))
def ll(lp, idx): return lp[torch.arange(len(idx)), Yt[torch.tensor(idx)]].numpy()
NIT = int(os.environ.get("SAP_EM_ITERS", "15")); NF = int(os.environ.get("SAP_FOLDS", "5"))   # Am. 3 (e): convergence check uses 50 iterations on fold 0

def em(rows, nit=15):
    """Laplace-EM (ARD) prior variances on the raters of rows (as sap.py Am. 1)"""
    s2 = np.full(J, 0.1); rr_ = np.unique(R[rows])
    for it in range(nit):
        thr, Bsr = fit(LPE, rows, mu, torch.tensor(1.0 / s2), one)
        with torch.no_grad():
            p = predict(LPE, rows, thr, Bsr).exp(); vs = (p * STEP ** 2).sum(1) - (p * STEP).sum(1) ** 2; acc = np.zeros(J)
            for r in rr_:
                q = np.where(R[rows] == r)[0]; a = AR[torch.tensor(rows[q])]; C = np.linalg.inv(((a * vs[q][:, None]).T @ a).numpy() + np.diag(1.0 / s2)); acc += (thr[r] - mu).numpy() ** 2 + np.diag(C)
        s2 = np.maximum(acc / len(rr_), 1e-6)
    return s2
def fit_lr(lpb, idx, W, lam_W=None, lam_s=2.0):
    """MAP of z_r (NR × 2) and style offsets on rows idx, θ_r = μ + W z_r, z_r ~ N(0, I); if lam_W is given W is learned jointly with ridge lam_W"""
    z = torch.zeros(NR, 2, requires_grad=True); Bs = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx); Wv = W.clone().requires_grad_(lam_W is not None)
    prm = [z, Bs] + ([Wv] if lam_W is not None else []); opt = torch.optim.LBFGS(prm, lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = mu + z @ Wv.T; c = (th[Rt[ii]] * AR[ii]).sum(1); lp = torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
        loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + 0.5 * (z ** 2).sum() + lam_s * (Bs ** 2).sum() + ((lam_W or 0.0) * (Wv ** 2).sum()); loss.backward(); return loss
    opt.step(cl); return (mu + z @ Wv.T).detach(), Bs.detach(), Wv.detach()
def fit_lr_c(lpb, idx, W, zprec, lam_s=2.0):
    """new-rater fit with W fixed and prior precision zprec on z"""
    z = torch.zeros(NR, 2, requires_grad=True); Bs = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx); opt = torch.optim.LBFGS([z, Bs], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = mu + z @ W.T; c = (th[Rt[ii]] * AR[ii]).sum(1); lp = torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
        loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + 0.5 * zprec * (z ** 2).sum() + lam_s * (Bs ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return (mu + z @ W.T).detach(), Bs.detach()
recs = []; screen = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold[I] != f; idx_tr = np.where(~test_r[R] & tr_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    V = torch.zeros(256, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); Bt = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx_tr)
    opt = torch.optim.LBFGS([V, b, Bt], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); lp = torch.log_softmax(X[It[ii]] @ V + b + Bt[Rt[ii]][:, SYM], 1); loss = -lp[torch.arange(len(idx_tr)), Yt[ii]].sum() + 300.0 * (V ** 2).sum() + 2.0 * (Bt ** 2).sum(); loss.backward(); return loss
    opt.step(cl)
    with torch.no_grad(): LPE = torch.log_softmax(X[It] @ V + b, 1)
    one = torch.ones(J); zero = torch.zeros(J)
    mu, _ = fit(LPE, idx_tr, zero, torch.zeros(J), one, shared=True); mu = mu[0]
    trr = np.unique(R[idx_tr]); rng_s = np.random.RandomState(90 + f); half = np.zeros(len(idx_tr), bool)
    for r in trr:
        pos = np.where(R[idx_tr] == r)[0]; half[rng_s.permutation(pos)[: len(pos) // 2]] = True
    if MODE == "lr2":
        pr_ = np.random.RandomState(3 + f); pseudo = set(pr_.choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R[idx_tr], list(pseudo)); rest = idx_tr[~isp]
        ad_p, sc_p = [], []; rk = np.random.RandomState(60 + f)
        for r in pseudo:
            q = idx_tr[R[idx_tr] == r]
            if len(q) < 30: continue
            q = rk.permutation(q); ad_p.extend(q[:20]); sc_p.extend(q[20:])
        ad_p, sc_p = np.array(ad_p, int), np.array(sc_p, int); W0 = torch.randn(J, 2, generator=torch.Generator().manual_seed(f)) * 0.01
        _, Bs0 = fit(LPE, ad_p, mu, torch.full((J,), 1e6), one); best = (float(ll(predict(LPE, sc_p, mu.expand(NR, -1).clone(), Bs0), sc_p).mean()), 1.0, 0.0)   # no content adaptation (offsets only)
        for lw in (1.0, 10.0, 100.0):
            _, _, Wr = fit_lr(LPE, rest, W0, lam_W=lw)
            for c in (0.1, 1.0, 10.0):
                th_c, Bs_c = fit_lr_c(LPE, ad_p, Wr, 1.0 / c); v = float(ll(predict(LPE, sc_p, th_c, Bs_c), sc_p).mean())
                if v > best[0]: best = (v, lw, c)
        CSEL = best[2]; W = fit_lr(LPE, idx_tr, W0, lam_W=best[1])[2] if CSEL > 0 else W0
        screen.append({"fold": f, "lam_W": best[1], "c": CSEL}); print(f"lr2 {tag} fold {f}: selected λ_W {best[1]}, c {CSEL}", flush=True)
    elif MODE == "lr":
        W0 = torch.randn(J, 2, generator=torch.Generator().manual_seed(f)) * 0.01; best = None
        for lw in (1.0, 10.0, 100.0):
            th_h, Bs_h, _ = fit_lr(LPE, idx_tr[half], W0, lam_W=lw); v = float(ll(predict(LPE, idx_tr[~half], th_h, Bs_h), idx_tr[~half]).mean())
            if best is None or v > best[0]: best = (v, lw)
        _, _, W = fit_lr(LPE, idx_tr, W0, lam_W=best[1]); screen.append({"fold": f, "lam_W": best[1], "W": W.numpy().tolist()})
        print(f"lr {tag} fold {f}: λ_W {best[1]}; |W| rows top: " + ", ".join(NAMES[j] for j in np.argsort(-W.norm(dim=1).numpy())[:5]), flush=True)
    else:
        pr_ = np.random.RandomState(3 + f); pseudo = set(pr_.choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R[idx_tr], list(pseudo)); rest = idx_tr[~isp]
        s2r = em(rest); ad_p, sc_p = [], []; rk = np.random.RandomState(60 + f)
        for r in pseudo:
            q = idx_tr[R[idx_tr] == r]
            if len(q) < 30: continue
            q = rk.permutation(q); ad_p.extend(q[:20]); sc_p.extend(q[20:])
        ad_p, sc_p = np.array(ad_p, int), np.array(sc_p, int)
        def hold(s2v):
            th, Bs = fit(LPE, ad_p, mu, torch.tensor(1.0 / s2v), one); return float(ll(predict(LPE, sc_p, th, Bs), sc_p).mean())
        base_ll = hold(s2r); keepj = []
        for j in range(J):
            s2d = s2r.copy(); s2d[j] = 1e-6
            if hold(s2d) < base_ll: keepj.append(j)
        s2 = em(idx_tr); s2[[j for j in range(J) if j not in keepj]] = 1e-6
        screen.append({"fold": f, "kept": [NAMES[j] for j in keepj], "sigma2": s2.tolist()}); print(f"tr {tag} fold {f}: kept {screen[-1]['kept']}", flush=True)
    test_raters = np.unique(R[idx_te])
    for k in (20, 50):
        for dr in range(5):
            rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep = []
            for r in test_raters:
                pr = pool[R[pool] == r]
                if len(pr) < k: continue
                keep.append(r); ad.extend(rng.choice(pr, k, replace=False))
            ad = np.array(ad, int); te = idx_te[np.isin(R[idx_te], keep)]
            o_ = np.random.RandomState(777 + 10_000 * f + 100 * k + dr).permutation(len(keep)); tgt = torch.tensor([int(keep[o_[i]]) for i in range(len(o_))]); src = torch.tensor([int(keep[o_[(i + 1) % len(o_)]]) for i in range(len(o_))])
            if MODE == "lr2": th, Bs = (fit(LPE, ad, mu, torch.full((J,), 1e6), one) if CSEL == 0 else fit_lr_c(LPE, ad, W, 1.0 / CSEL)[:2])
            elif MODE == "lr": th, Bs, _ = fit_lr(LPE, ad, W)
            else: th, Bs = fit(LPE, ad, mu, torch.tensor(1.0 / s2), one)
            thp, Bsp = th.clone(), Bs.clone(); thp[tgt] = th[src]; Bsp[tgt] = Bs[src]; th0 = mu.expand(NR, -1).clone()
            lps = {"own": predict(LPE, te, th, Bs), "other": predict(LPE, te, thp, Bsp), "pop": predict(LPE, te, th0, Bs)}
            for r in keep:
                sel = R[te] == r
                recs.append({"fold": f, "k": k, "draw": dr, "rater": int(r), **{f"{w}_dir": float(np.nansum(dirc(lp, te)[sel])) for w, lp in lps.items()},
                             **{f"{w}_ll": float(ll(lp, te)[sel].sum()) for w, lp in lps.items()}, "n_dir": int(np.isfinite(dirc(lps["own"], te)[sel]).sum()), "n": int(sel.sum())})
out = {"tag": tag, "mode": MODE, "screen": screen}
for k in (20, 50):
    by = collections.defaultdict(list)
    for x in recs:
        if x["k"] == k: by[(x["fold"], x["rater"])].append(x)
    q = list(by)
    for mt, den, sc in (("dir", "n_dir", 100), ("ll", "n", 100)):
        wt = np.array([np.mean([x[den] for x in by[z]]) for z in q])
        for ref_ in ("other", "pop"):
            rng = np.random.RandomState(17); d = np.array([np.mean([x[f"own_{mt}"] - x[f"{ref_}_{mt}"] for x in by[z]]) for z in q])
            bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; out[f"k{k}_{mt}_own-{ref_}"] = [sc * d.sum() / wt.sum(), sc * np.percentile(bs, 2.5), sc * np.percentile(bs, 97.5), len(q)]
json.dump(out, open(f"{HERE}/results/stage9_{MODE}_{tag}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage9_{MODE}_{tag}_records.json", "w"))
print(MODE, tag, json.dumps({k_: v for k_, v in out.items() if k_ not in ("screen",)}), flush=True)
