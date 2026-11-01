"""Stage 9 (PROTOCOL_STAGE9.md): screened attribute personalisation (SAP) on MultiPref-structured panels. `sap.py <tag>`, tag = real | t0 | t5 | t10 | sem5 | sem10 | x10 ...
Estimated base (D head + DFs offsets on training raters × training items) + rater content term (θ_rᵀ a_i)(−2..2), a_i = the 24 attribute differences of attr_feats.py;
θ_r ~ N(μ, diag σ²), μ shared on training raters, σ² by Laplace-EM (ARD) on the training raters (Am. 1); selected = σ²_j > 1e-3."""
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
recs = []; screen = []
for f in range(NF):
    test_r = rfold == f; tr_item = ifold[I] != f; idx_tr = np.where(~test_r[R] & tr_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    V = torch.zeros(256, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); Bt = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx_tr)
    opt = torch.optim.LBFGS([V, b, Bt], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); lp = torch.log_softmax(X[It[ii]] @ V + b + Bt[Rt[ii]][:, SYM], 1); loss = -lp[torch.arange(len(idx_tr)), Yt[ii]].sum() + 300.0 * (V ** 2).sum() + 2.0 * (Bt ** 2).sum(); loss.backward(); return loss
    opt.step(cl)
    with torch.no_grad(): LPE = torch.log_softmax(X[It] @ V + b, 1)
    one = torch.ones(J); zero = torch.zeros(J)
    mu, _ = fit(LPE, idx_tr, zero, torch.zeros(J), one, shared=True); mu = mu[0]                         # population weights μ
    s2 = np.full(J, 0.1); trr = np.unique(R[idx_tr])                                               # Am. 1: Laplace-EM (ARD) for diag σ² on the training raters
    MK = os.environ.get("SAP_EM", "em") == "mackay"                          # Stage 9 Am. 7: MacKay fixed-point update (robustness)
    for it in range(40 if MK else NIT):
        thr, Bsr = fit(LPE, idx_tr, mu, torch.tensor(1.0 / s2), one)
        with torch.no_grad():
            p = predict(LPE, idx_tr, thr, Bsr).exp(); vs = (p * STEP ** 2).sum(1) - (p * STEP).sum(1) ** 2; acc = np.zeros(J); cc = np.zeros(J)
            for r in trr:
                q = np.where(R[idx_tr] == r)[0]; a = AR[torch.tensor(idx_tr[q])]; C = np.linalg.inv(((a * vs[q][:, None]).T @ a).numpy() + np.diag(1.0 / s2))
                acc += (thr[r] - mu).numpy() ** 2 + (0 if MK else np.diag(C)); cc += np.diag(C)
        if ISO and MK: s2 = np.full(J, float(np.clip(acc.sum() / max(1e-9, len(trr) * J - (cc / s2).sum()), 1e-6, 10.0)))   # Am. 8: scalar MacKay update for SAP-iso
        else: s2 = (np.clip(acc / np.clip(len(trr) - cc / s2, 1e-6, None), 1e-6, 10.0) if MK else np.maximum(acc / len(trr), 1e-6)) if not ISO else np.full(J, max(float(np.mean(acc / len(trr))), 1e-6))
    print(f"{tag} fold {f}: σ² " + ", ".join(f"{NAMES[j]} {s2[j]:.4f}" for j in np.argsort(-s2)[:6]), flush=True)
    mask = one; prec = torch.tensor(1.0 / s2)
    screen.append({"fold": f, "mu": mu.numpy().tolist(), "sigma2": s2.tolist(), "selected": [NAMES[j] for j in range(J) if s2[j] > 1e-3]})
    print(f"{tag} fold {f}: selected {screen[-1]['selected']}", flush=True)
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
            th, Bs = fit(LPE, ad, mu, prec, mask); thp, Bsp = th.clone(), Bs.clone(); thp[tgt] = th[src]; Bsp[tgt] = Bs[src]; th0 = mu.expand(NR, -1).clone()
            lps = {"own": predict(LPE, te, th, Bs), "other": predict(LPE, te, thp, Bsp), "pop": predict(LPE, te, th0, Bs)}
            for r in keep:
                sel = R[te] == r
                recs.append({"fold": f, "k": k, "draw": dr, "rater": int(r), **{f"{w}_dir": float(np.nansum(dirc(lp, te)[sel])) for w, lp in lps.items()},
                             **{f"{w}_ll": float(ll(lp, te)[sel].sum()) for w, lp in lps.items()}, "n_dir": int(np.isfinite(dirc(lps["own"], te)[sel]).sum()), "n": int(sel.sum())})
out = {"tag": tag, "screen": screen}
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
cnt = collections.Counter(a for s in screen for a in s["selected"]); out["selected_4of5"] = sorted(a for a, c in cnt.items() if c >= 4)
sfx = ("" if NIT == 15 else f"_em{NIT}") + ("_mackay" if os.environ.get("SAP_EM", "em") == "mackay" else "")
json.dump(out, open(f"{HERE}/results/stage9_sap_{tag}{sfx}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage9_sap_{tag}{sfx}_records.json", "w"))
print(tag, json.dumps({k_: v for k_, v in out.items() if k_ != "screen"}), flush=True)
