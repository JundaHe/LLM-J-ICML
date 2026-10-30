"""Stage 3 S3-P (PROTOCOL_STAGE3.md): semi-synthetic MultiPref panels with injected content-dependent rater preferences.
Generator = D head + DFs offsets fitted on all ratings; synthetic y ~ softmax(log P + θ_r·g_i · [−2,−1,0,1,2]); τ calibrated on the generator alone
so that the generator-oracle direction accuracy gain on the test ratings is 0, +2 and +5 points. Writes results/synth/multipref_synth_t{0,2,5}.npz."""
import os, sys, json, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
PAN = data_panels.load("multipref_overall"); H = PAN["H"]; K = 5; n, m = H.shape; ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); Y = H.reshape(-1); POS = np.tile(np.arange(m), n)
# ---- folds exactly as factorised_rm.py (test ratings = test-fold raters × test-fold items)
GRP = np.zeros(NR, int)
for i in range(len(R)): GRP[R[i]] = int(POS[i] >= 2)
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
Gp = np.asarray(PAN["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
TEST = rfold[R] == ifold[I]
# ---- generator: D head (joint-item PCA-256 features, as factorised_rm.py) + symmetric style offsets, all ratings
F_ = np.load(f"{P2}/features/multipref_overall/Qwen2.5-7B-Instruct.npz", allow_pickle=True); assert np.array_equal(F_["item_ids"].astype(str), np.asarray(PAN["item_ids"]).astype(str))
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, Vt = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0); X = torch.tensor(X)
V = torch.zeros(256, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); Bs = torch.zeros(NR, 3, requires_grad=True)
It, Rt, Yt = torch.tensor(I), torch.tensor(R), torch.tensor(Y); SYM = [0, 1, 2, 1, 0]
opt = torch.optim.LBFGS([V, b, Bs], lr=0.5, max_iter=500, line_search_fn="strong_wolfe")
def cl():
    opt.zero_grad(); lp = torch.log_softmax(X[It] @ V + b + Bs[Rt][:, SYM], 1); loss = -lp[torch.arange(len(Y)), Yt].sum() + 300.0 * (V ** 2).sum() + 2.0 * (Bs ** 2).sum(); loss.backward(); return loss
opt.step(cl)
with torch.no_grad(): LP = torch.log_softmax(X[It] @ V + b + Bs[Rt][:, SYM], 1).numpy()
print("generator fitted; mean LL on real labels %.4f" % LP[np.arange(len(Y)), Y].mean(), flush=True)
# ---- content features of the response pair
raw = [json.loads(l) for l in open(data_panels.MULTIPREF)]; assert [r["comparison_id"] for r in raw] == list(PAN["item_ids"])
g1 = np.log(np.array([max(1, len(str(r["completion_b"]))) for r in raw]) / np.array([max(1, len(str(r["completion_a"]))) for r in raw]))
Fp = np.load(f"{P2}/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fp["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
Dd = (Fp["E_B"] - Fp["E_A"]).astype(np.float64); Dd -= Dd.mean(0); U2, S2, _ = np.linalg.svd(Dd, full_matrices=False); Z = U2[:, :256] * S2[:256]; Z /= Z.std(0)
ymean = H.mean(1); w = np.linalg.solve(Z.T @ Z + 1000.0 * np.eye(256), Z.T @ (ymean - ymean.mean())); w /= np.linalg.norm(w)
u = np.random.RandomState(0).randn(256); u -= (u @ w) * w; u /= np.linalg.norm(u); g2 = Z @ u
G = np.stack([(g1 - g1.mean()) / g1.std(), (g2 - g2.mean()) / g2.std()], 1)                     # (n, 2)
print("corr(g1, g2) %.3f; corr(g2, item mean rating) %.3f" % (np.corrcoef(G[:, 0], G[:, 1])[0, 1], np.corrcoef(G[:, 1], ymean)[0, 1]), flush=True)
TH0 = np.random.RandomState(1).randn(NR, 2)                                                       # θ_r = τ · TH0_r
STEP = np.array([-2, -1, 0, 1, 2], float)
def sample(lp, seed):                                                                             # Gumbel-max with fixed noise per seed (panels coupled across τ)
    gmb = -np.log(-np.log(np.random.RandomState(seed).rand(*lp.shape))); return np.argmax(lp + gmb, 1)
def dir_acc(lp, y, mask):
    pk = np.exp(lp); ey = (pk * np.arange(K)).sum(1); ok = mask & (y != 2); return float((np.sign(ey[ok] - 2) == np.sign(y[ok] - 2)).mean())
def oracle_gain(tau, seeds=range(100, 105)):
    c = tau * (TH0[R] * G[I]).sum(1); lpc = LP + c[:, None] * STEP[None, :]; lpc -= np.logaddexp.reduce(lpc, 1, keepdims=True)
    return float(np.mean([dir_acc(lpc, y, TEST) - dir_acc(LP, y, TEST) for y in (sample(lpc, s) for s in seeds)]))
out = {}
TARGETS = ((0.0, "t0"), (0.02, "t2"), (0.05, "t5")) if len(sys.argv) < 2 else ((0.10, "t10"), (0.20, "t20"))   # Stage 3 Am. 3: `make_synth.py dose` adds τ10, τ20
for target, tag in TARGETS:
    if target == 0: tau = 0.0
    else:
        lo, hi = 0.0, 5.0
        for _ in range(25):
            mid = 0.5 * (lo + hi); (lo, hi) = (mid, hi) if oracle_gain(mid) < target else (lo, mid)
        tau = 0.5 * (lo + hi)
    c = tau * (TH0[R] * G[I]).sum(1); lpc = LP + c[:, None] * STEP[None, :]; lpc -= np.logaddexp.reduce(lpc, 1, keepdims=True)
    y = sample(lpc, 2); Hs = y.reshape(n, m); og = dir_acc(lpc, y, TEST) - dir_acc(LP, y, TEST)
    os.makedirs(f"{HERE}/results/synth", exist_ok=True); np.savez_compressed(f"{HERE}/results/synth/multipref_synth_{tag}.npz", H=Hs, tau=tau, item_ids=np.asarray(PAN["item_ids"]).astype(str))
    out[tag] = {"tau": tau, "target_gain": target, "oracle_gain_calibration": oracle_gain(tau), "oracle_gain_realised": og, "label_dist": np.bincount(y, minlength=K).tolist()}
    print(tag, out[tag], flush=True)
mp = f"{HERE}/results/synth/synth_meta.json"; old = json.load(open(mp)) if (len(sys.argv) > 1 and os.path.exists(mp)) else {}; old.update(out); json.dump(old, open(mp, "w"), indent=1)
