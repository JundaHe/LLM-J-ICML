"""Stage 10 Am. 2 (PROTOCOL_STAGE10.md): SAP on single-snippet code-readability ratings. `sap_code.py bw_raters|dorn_raters [perm]`.
Base: D head (PCA features, λ by validation) + each rater's five category offsets (DF); content term (θ_rᵀ a_i)(−2..2) with a_i the 22 code attributes of code_feats.py;
θ_r ~ N(μ, diag σ²), μ shared, σ² by Laplace-EM on the training raters (Stage 9 Am. 1). Outcome: within-rater pairwise concordance (own, other, own offsets with θ = μ)."""
import os, sys, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
from code_feats import code_G, NAMES
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); K = 5; STEP = torch.arange(5.0) - 2
panel = sys.argv[1]; PERM = len(sys.argv) > 2 and sys.argv[2] == "perm"; tag = panel + ("_perm" if PERM else "")
PAN = data_panels.load(panel); H = PAN["H"]; n, m = H.shape; ev = PAN["evaluators"] if "evaluators" in PAN else [list(PAN["rater_ids"])] * n
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); Y = H.reshape(-1).copy(); Gp = np.asarray(PAN["groups"])
rs = np.random.RandomState(0); rfold = np.zeros(NR, int); ids = np.arange(NR)[rs.permutation(NR)]; rfold[ids] = np.arange(NR) % 5          # one rater group (as factorised_rm.py)
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}; va_item = np.array([vf[g_] for g_ in Gp])[I]
snip = np.asarray(PAN["snippet_ids"]) if "snippet_ids" in PAN else np.asarray(PAN["item_ids"]).astype(str); SN = snip[I]   # snippet of every rating
if PERM:                                                                  # within-snippet permutation of the ratings across raters (null for screening)
    rp = np.random.RandomState(5)
    for s_ in np.unique(SN):
        q = np.where(SN == s_)[0]; Y[q] = Y[rp.permutation(q)]
us, first, inv_s = np.unique(snip, return_index=True, return_inverse=True)
F_ = np.load(f"{P2}/features/{panel}/Qwen2.5-Coder-7B-Instruct.npz", allow_pickle=True); Eu = F_["E_last"][first].astype(np.float64); Eu -= Eu.mean(0)
U, S, _ = np.linalg.svd(Eu, full_matrices=False); XD = min(256, len(us) - 1); Xs = U[:, :XD] * S[:XD]; Xs /= Xs.std(0)
if panel == "dorn_raters":
    code = [open(f"{data_panels.DORN}/snippets/{u.split('_')[0]}/{u.split('_')[1]}.jsnp", encoding="utf-8", errors="replace").read() for u in us]
else: code = [PAN["texts"][int(j)] for j in first]
As = code_G(code); J = As.shape[1]
row_s = inv_s                                                             # unique-snippet index of each item (features and attributes are in unique-snippet order)
X = torch.tensor(Xs[row_s][I]); AR = torch.tensor(As[row_s][I]); Yt = torch.tensor(Y); Rt = torch.tensor(R)
def fit(lpb, idx, mu, prec, Bc, lam_b=2.0, shared=False):
    """MAP: θ = μ + δ per rater (or one shared δ), prior precision prec on δ; category offsets Br per rater, ridge lam_b towards Bc"""
    d = torch.zeros(1 if shared else NR, J, requires_grad=True); Br = Bc.clone().requires_grad_(True); ii = torch.tensor(idx)
    opt = torch.optim.LBFGS([d, Br], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = mu + d; c = (AR[ii] @ th[0]) if shared else (th[Rt[ii]] * AR[ii]).sum(1); lp = torch.log_softmax(lpb[ii] + Br[Rt[ii]] + c[:, None] * STEP, 1)
        loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + 0.5 * (prec * d ** 2).sum() + lam_b * ((Br - Bc) ** 2).sum(); loss.backward(); return loss
    opt.step(cl); th = (mu + d).detach(); return (th.expand(NR, -1).clone() if shared else th), Br.detach()
def predict(lpb, idx, th, Br):
    ii = torch.tensor(idx); c = (th[Rt[ii]] * AR[ii]).sum(1); return torch.log_softmax(lpb[ii] + Br[Rt[ii]] + c[:, None] * STEP, 1)
def conc(lp, idx, sel):
    """within-rater pairwise concordance numerator and denominator for the ratings idx[sel]"""
    ey = (lp.exp() * torch.arange(K)).sum(1).numpy()[sel]; yy = Y[idx][sel]; ui, uj = np.triu_indices(len(yy), 1); ok = yy[ui] != yy[uj]
    sg = np.sign(ey[ui] - ey[uj])[ok] * np.sign(yy[ui] - yy[uj])[ok]; return float((sg > 0).sum() + 0.5 * (sg == 0).sum()), int(ok.sum())
KS = (5, 10) if panel == "dorn_raters" else (10, 20, 50); recs = []; screen = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold[I] != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    best = None
    for lam in (100.0, 300.0, 1000.0, 3000.0):                           # D head + DF offsets; λ by validation LL of training raters on validation snippets
        V = torch.zeros(XD, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); Bt = torch.zeros(NR, K, requires_grad=True); ii = torch.tensor(idx_tr)
        opt = torch.optim.LBFGS([V, b, Bt], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); lp = torch.log_softmax(X[ii] @ V + b + Bt[Rt[ii]], 1); loss = -lp[torch.arange(len(idx_tr)), Yt[ii]].sum() + lam * (V ** 2).sum() + 2.0 * (Bt ** 2).sum(); loss.backward(); return loss
        opt.step(cl)
        with torch.no_grad(): iv = torch.tensor(idx_va); v = float(torch.log_softmax(X[iv] @ V + b + Bt[Rt[iv]], 1)[torch.arange(len(idx_va)), Yt[iv]].mean())
        if best is None or v > best[0]: best = (v, lam, V.detach().clone(), b.detach().clone(), Bt.detach().clone())
    _, lam, V, b, Bt = best; idx_all = np.concatenate([idx_tr, idx_va])
    with torch.no_grad(): LPE = torch.log_softmax(X @ V + b, 1)
    Bc = Bt[torch.tensor(np.unique(R[idx_all]))].mean(0).expand(NR, -1).clone()       # population mean offsets (new raters' prior centre)
    one = torch.ones(J); zero = torch.zeros(J)
    mu, _ = fit(LPE, idx_all, zero, torch.zeros(J), Bt, shared=True); mu = mu[0]
    s2 = np.full(J, 0.1); trr = np.unique(R[idx_all])
    for it in range(15):
        thr, Brr = fit(LPE, idx_all, mu, torch.tensor(1.0 / s2), Bt)
        with torch.no_grad():
            p = predict(LPE, idx_all, thr, Brr).exp(); vs = (p * STEP ** 2).sum(1) - (p * STEP).sum(1) ** 2; acc = np.zeros(J)
            for r in trr:
                q = np.where(R[idx_all] == r)[0]; a = AR[torch.tensor(idx_all[q])]; C = np.linalg.inv(((a * vs[q][:, None]).T @ a).numpy() + np.diag(1.0 / s2)); acc += (thr[r] - mu).numpy() ** 2 + np.diag(C)
        s2 = np.maximum(acc / len(trr), 1e-6)
    screen.append({"fold": f, "lambda": lam, "mu": mu.numpy().tolist(), "sigma2": s2.tolist()})
    print(f"{tag} fold {f}: λ {lam}; σ² " + ", ".join(f"{NAMES[j]} {s2[j]:.4f}" for j in np.argsort(-s2)[:6]), flush=True)
    prec = torch.tensor(1.0 / s2); test_raters = np.unique(R[idx_te])
    for k in KS:
        for dr in range(5):
            rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep = []
            for r in test_raters:
                pr = pool[R[pool] == r]
                if len(pr) < k: continue
                keep.append(r); ad.extend(rng.choice(pr, k, replace=False))
            if len(keep) < 2: continue
            ad = np.array(ad, int); te = idx_te[np.isin(R[idx_te], keep)]
            o_ = np.random.RandomState(777 + 10_000 * f + 100 * k + dr).permutation(len(keep)); tgt = torch.tensor([int(keep[o_[i]]) for i in range(len(o_))]); src = torch.tensor([int(keep[o_[(i + 1) % len(o_)]]) for i in range(len(o_))])
            th, Br = fit(LPE, ad, mu, prec, Bc); thp, Brp = th.clone(), Br.clone(); thp[tgt] = th[src]; Brp[tgt] = Br[src]; th0 = mu.expand(NR, -1).clone()
            lps = {"own": predict(LPE, te, th, Br), "other": predict(LPE, te, thp, Brp), "pop": predict(LPE, te, th0, Br)}
            for r in keep:
                sel = R[te] == r; cs = {w: conc(lp, te, sel) for w, lp in lps.items()}
                recs.append({"fold": f, "k": k, "draw": dr, "rater": int(r), "conc_den": cs["own"][1], **{f"{w}_conc": cs[w][0] for w in lps},
                             **{f"{w}_ll": float(lp[torch.arange(len(te)), Yt[torch.tensor(te)]].numpy()[sel].sum()) for w, lp in lps.items()}, "n": int(sel.sum())})
out = {"tag": tag, "screen": screen}
for k in KS:
    by = collections.defaultdict(list)
    for x in recs:
        if x["k"] == k: by[(x["fold"], x["rater"])].append(x)
    q = list(by)
    for mt, den in (("conc", "conc_den"), ("ll", "n")):
        wt = np.array([np.mean([x[den] for x in by[z]]) for z in q]); ok = wt > 0
        for ref_ in ("other", "pop"):
            d = np.array([np.mean([x[f"own_{mt}"] - x[f"{ref_}_{mt}"] for x in by[z]]) for z in q])[ok]; w = wt[ok]; rng = np.random.RandomState(17)
            bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]; out[f"k{k}_{mt}_own-{ref_}"] = [100 * d.sum() / w.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), int(ok.sum())]
json.dump(out, open(f"{HERE}/results/stage10_sapcode_{tag}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage10_sapcode_{tag}_records.json", "w"))
print(tag, json.dumps({k_: v for k_, v in out.items() if k_ != "screen"}), flush=True)
