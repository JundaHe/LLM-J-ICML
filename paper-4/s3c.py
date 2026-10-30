"""Stage 3 S3-C (PROTOCOL_STAGE3.md): transferable rater-specific direction signal. Per fold, D head (joint-item PCA-256, λ = 300) trained on training raters × training items;
for each test rater, per-rater content weights w_r on the top-32 PCs of (E_B − E_A) (logit offset (w_r·z_i)·[−2,−1,0,1,2], ridge λ_c chosen on the training raters by the same
split-half procedure) are fitted on a random half of the rater's test-item ratings and evaluated on the other half (10 splits): direction-accuracy gain over D, rater bootstrap.
Run on the real panel and on the τ0/τ2/τ5 synthetic panels (calibration)."""
import os, sys, json, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); K = 5; STEP = torch.tensor([-2., -1., 0., 1., 2.]); SPLITS = 10
base = data_panels.load("multipref_overall"); n, m = base["H"].shape; ev = base["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
for i in range(len(R)): GRP[R[i]] = int(POS[i] >= 2)
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
Gp = np.asarray(base["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
F_ = np.load(f"{P2}/features/multipref_overall/Qwen2.5-7B-Instruct.npz", allow_pickle=True)
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, _ = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0); X = torch.tensor(X)
Fp = np.load(f"{P2}/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz"); Dd = (Fp["E_B"] - Fp["E_A"]).astype(np.float64); Dd -= Dd.mean(0)
U2, S2, _ = np.linalg.svd(Dd, full_matrices=False); Zc = U2[:, :32] * S2[:32]; Zc /= Zc.std(0); Zc = torch.tensor(Zc)
def fit_D(idx, Y):
    V = torch.zeros(256, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); ii = torch.tensor(I[idx]); yy = torch.tensor(Y[idx])
    opt = torch.optim.LBFGS([V, b], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); loss = -torch.log_softmax(X[ii] @ V + b, 1)[torch.arange(len(idx)), yy].sum() + 300.0 * (V ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return V.detach(), b.detach()
def fit_w(lpD, rix, zz, yy, nr, lam):
    """per-rater content weights, all raters jointly (separable): lpD (N,K) base log-probs, rix rater index 0..nr-1"""
    W = torch.zeros(nr, 32, requires_grad=True); opt = torch.optim.LBFGS([W], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); c = (W[rix] * zz).sum(1); loss = -torch.log_softmax(lpD + c[:, None] * STEP, 1)[torch.arange(len(yy)), yy].sum() + lam * (W ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return W.detach()
def dirc(lp, y):
    ey = (lp.exp() * torch.arange(K)).sum(1).numpy(); return np.where(y == 2, np.nan, (np.sign(ey - 2) == np.sign(y - 2)).astype(float))
def split_half(idx, Y, lpD_all, lam, seed, splits=SPLITS):
    """mean over SPLITS of per-rater (sum of dir gains on half B, n_dir on half B); returns dict rater -> [gain_sum, n] and the held-out LL gain"""
    rr = np.unique(R[idx]); rmap = {r: j for j, r in enumerate(rr)}; acc = {r: [0.0, 0.0] for r in rr}; llg = [0.0, 0]
    rng = np.random.RandomState(seed)
    for s in range(splits):
        half = np.zeros(len(idx), bool)
        for r in rr:
            pos = np.where(R[idx] == r)[0]; half[rng.permutation(pos)[: len(pos) // 2]] = True
        for a_mask in (half, ~half):
            a, bq = idx[a_mask], idx[~a_mask]
            W = fit_w(lpD_all[a_mask], torch.tensor([rmap[r] for r in R[a]]), Zc[I[a]], torch.tensor(Y[a]), len(rr), lam)
            c = (W[torch.tensor([rmap[r] for r in R[bq]])] * Zc[I[bq]]).sum(1); lpB = lpD_all[~a_mask]; lpW = torch.log_softmax(lpB + c[:, None] * STEP, 1)
            g = dirc(lpW, Y[bq]) - dirc(lpB, Y[bq]); yb = torch.tensor(Y[bq]); llg[0] += float((lpW[torch.arange(len(bq)), yb] - lpB[torch.arange(len(bq)), yb]).sum()); llg[1] += len(bq)
            for j, r in enumerate(R[bq]):
                if np.isfinite(g[j]): acc[r][0] += g[j]; acc[r][1] += 1
    return acc, llg[0] / llg[1]
out = {}; L = ["# Stage 3 S3-C — transferable rater-specific direction signal (split-half, per-rater content weights on top-32 PCs of E_B − E_A)", "",
              "| panel | λ_c | direction gain over D on the held-out half [95 %] | LL gain per rating | raters |", "|---|---|---|---|---|"]
for panel in ("multipref_overall", "multipref_synth_t0", "multipref_synth_t2", "multipref_synth_t5"):
    Y = data_panels.load(panel)["H"].reshape(-1); per = {}; llgs = []; lam_sel = []
    for f in range(5):
        test_r = rfold == f; tr_item = ifold[I] != f; idx_tr = np.where(~test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
        V, b = fit_D(idx_tr, Y)
        with torch.no_grad(): lp_tr = torch.log_softmax(X[I[idx_tr]] @ V + b, 1); lp_te = torch.log_softmax(X[I[idx_te]] @ V + b, 1)
        best = None
        for lam in (1.0, 3.0, 10.0, 30.0, 100.0, 300.0):                  # penalty on the training raters' training items, same split-half procedure, held-out LL
            _, llg = split_half(idx_tr, Y, lp_tr, lam, seed=50 + f, splits=2)
            if best is None or llg > best[0]: best = (llg, lam)
        lam_sel.append(best[1]); acc, llg = split_half(idx_te, Y, lp_te, best[1], seed=2 + f); llgs.append(llg)
        for r, v in acc.items(): per[(f, r)] = v
        print(panel, "fold", f, "λ_c", best[1], "LL gain %.4f" % llg, flush=True)
    q = [z for z in per if per[z][1] > 0]; d = np.array([per[z][0] for z in q]); w = np.array([per[z][1] for z in q]); rng = np.random.RandomState(9)
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; v = [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    out[panel] = {"dir_gain": v, "ll_gain": float(np.mean(llgs)), "lam_c": lam_sel, "n_raters": len(q)}
    L.append(f"| {panel} | {lam_sel} | {v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}] | {np.mean(llgs):+.4f} | {len(q)} |")
json.dump(out, open(f"{HERE}/results/stage3_s3c.json", "w"), indent=1); open(f"{HERE}/results/stage3_s3c.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
