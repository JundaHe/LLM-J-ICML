"""Stage 11 S11-2 (PROTOCOL_STAGE11.md): cross-fitted transferable heterogeneity on Community Alignment. Population model (ridge logistic on PCA-256 response
differences + per-language attribute weights μ_ℓ) cross-fitted over the five user folds; per user, events split into two halves with disjoint prompt groups;
one-step deviations z_u^h = I_u^h⁻¹ s_u^h; transferable covariance Ĉ = mean_u z^A z^Bᵀ; user bootstrap. Simulation controls on the actual design (20 replicates each)."""
import os, sys, json, collections, numpy as np, torch, torch.nn.functional as Fn
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from attr_feats import attr_G, NAMES
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
PRIM = [NAMES.index("length"), NAMES.index("paragraphs"), NAMES.index("list/heading lines")]
PAN = data_panels.load("ca_pairs"); n = len(PAN["item_ids"]); ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters); R = np.array([rid[row[0]] for row in ev])
gm = PAN["rater_group"]; glev = sorted({gm.get(r, "NA") for r in raters}); GRP = np.array([glev.index(gm.get(r, "NA")) for r in raters])   # user folds as vpl_pal.py
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
Gp = np.asarray(PAN["groups"]); EVT = np.array([s.split("|")[0] for s in PAN["item_ids"]]); LANG = np.asarray(PAN["lang"]); langs = sorted(set(LANG)); LI = np.array([langs.index(l) for l in LANG])
YB = np.asarray(PAN["yb"]).astype(float); A = attr_G(list(PAN["resp_A"]), list(PAN["resp_B"]), PAN["texts"]); J = A.shape[1]
plen = np.array([len(str(t)) for t in PAN["texts"]]); PT = np.digitize(plen, np.percentile(plen, [33.3, 66.7]))   # prompt-length tercile (misspecification control)
Fz = np.load(f"{P2}/features/ca_pairs/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fz["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
EA, EB = Fz["E_A"].astype(np.float32), Fz["E_B"].astype(np.float32); sub = np.concatenate([EA[::6], EB[::6], Fz["E_P"][::6].astype(np.float32)]); mu0 = sub.mean(0)
_, _, Vt = np.linalg.svd(sub - mu0, full_matrices=False); W256 = Vt[:256].T; del sub
XA, XB = (EA - mu0) @ W256, (EB - mu0) @ W256; del EA, EB; sd = np.concatenate([XA, XB]).std(0) + 1e-6; X = torch.tensor((XB - XA) / sd, dtype=torch.float64); del XA, XB
At = torch.tensor(A); Yt = torch.tensor(YB); Lt = torch.tensor(LI)
def nll(lg, y): return -(y * Fn.logsigmoid(lg) + (1 - y) * Fn.logsigmoid(-lg))
def fit_pop(idx, lam=100.0):
    """ridge logistic on X plus per-language attribute weights (μ_ℓ), jointly"""
    w = torch.zeros(X.shape[1], requires_grad=True); b = torch.zeros(1, requires_grad=True); th = torch.zeros(len(langs), J, requires_grad=True); ii = torch.tensor(idx)
    opt = torch.optim.LBFGS([w, b, th], lr=0.5, max_iter=400, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); lg = X[ii] @ w + b + (th[Lt[ii]] * At[ii]).sum(1); loss = nll(lg, Yt[ii]).sum() + lam * (w ** 2).sum() + 1e-3 * (th ** 2).sum(); loss.backward(); return loss
    opt.step(cl)
    with torch.no_grad(): return (X @ w + b + (th[Lt] * At).sum(1)).numpy(), th.detach().numpy()
LOGIT = np.zeros(n); MU = {}
for f in range(5):                                                         # cross-fitting over user folds
    tr = np.where(rfold[R] != f)[0]; te = np.where(rfold[R] == f)[0]; lg, th = fit_pop(tr); LOGIT[te] = lg[te]; MU[f] = th.tolist(); print(f"population model fold {f} fitted", flush=True)
# ---- per-user halves with disjoint prompt groups
rng = np.random.RandomState(5); halves = {}
byu = collections.defaultdict(list)
for j in range(n): byu[R[j]].append(j)
for u, js in byu.items():
    js = np.array(js); evs = np.unique(EVT[js])
    if len(evs) < 10: continue
    grp = np.unique(Gp[js]); side = dict(zip(grp, rng.permutation(len(grp)) % 2)); h = np.array([side[g] for g in Gp[js]])
    if h.min() == h.max(): continue
    halves[u] = (js[h == 0], js[h == 1])
users = sorted(halves); print(f"{len(users)} users with >= 10 events and two non-empty halves", flush=True)
def zvec(y, lg, js, cols):
    p = 1 / (1 + np.exp(-lg[js])); a = A[np.ix_(js, cols)]; s = a.T @ (y[js] - p); I_ = (a * (p * (1 - p))[:, None]).T @ a + 1e-3 * np.eye(len(cols)); return np.linalg.solve(I_, s)
def transfer_cov(y, lg, cols):
    ZA = np.array([zvec(y, lg, halves[u][0], cols) for u in users]); ZB = np.array([zvec(y, lg, halves[u][1], cols) for u in users]); return ZA, ZB
def summarise(ZA, ZB, B=2000, seed=17):
    C = lambda ix: 0.5 * (ZA[ix].T @ ZB[ix] + ZB[ix].T @ ZA[ix]) / len(ix)
    full = C(np.arange(len(ZA))); rg = np.random.RandomState(seed); bs = np.array([np.diag(C(rg.randint(0, len(ZA), len(ZA)))) for _ in range(B)])
    return np.diag(full), np.percentile(bs, 2.5, 0), np.percentile(bs, 97.5, 0), full
out = {"n_users": len(users), "primary": [NAMES[j] for j in PRIM]}
ZA, ZB = transfer_cov(YB, LOGIT, PRIM); d, lo, hi, full = summarise(ZA, ZB)
out["real_primary"] = {NAMES[j]: [float(d[i]), float(lo[i]), float(hi[i])] for i, j in enumerate(PRIM)}; out["real_primary_cov"] = full.tolist()
print("real (primary):", json.dumps(out["real_primary"]), flush=True)
ZA2, ZB2 = transfer_cov(YB, LOGIT, list(range(J))); d2, lo2, hi2, _ = summarise(ZA2, ZB2, B=1000)
out["real_all24"] = {NAMES[j]: [float(d2[j]), float(lo2[j]), float(hi2[j])] for j in range(J)}
# ---- in-sample random-slope variances from the frozen Stage-9 CA run (fixed-point update), mean over folds
s2 = np.mean([np.array(x["sigma2"]) for x in json.load(open(f"{HERE}/results/stage9_sapca.json"))["info"]], 0); out["insample_sigma2_primary"] = {NAMES[j]: float(s2[j]) for j in PRIM}
# ---- simulation controls on the actual design
uidx = {u: i for i, u in enumerate(users)}; sig = s2[PRIM]
def simulate(kind, rep):
    g = np.random.RandomState(1000 + rep); lg = LOGIT.copy()
    if kind in ("stable", "half"):
        dev = g.randn(NR, 3) * np.sqrt(sig * (1.0 if kind == "stable" else 0.25)); lg = lg + (dev[R] * A[:, PRIM]).sum(1)
    elif kind == "context":
        devA, devB = g.randn(NR, 3) * np.sqrt(sig), g.randn(NR, 3) * np.sqrt(sig); side = np.zeros(n, int)
        for u in users: side[halves[u][1]] = 1
        dev = np.where(side[:, None] == 0, devA[R], devB[R]); lg = lg + (dev * A[:, PRIM]).sum(1)
    elif kind == "misspec":
        lg = lg + 0.3 * (PT - 1) * A[:, PRIM[0]]
    y = (g.rand(n) < 1 / (1 + np.exp(-lg))).astype(float)
    za, zb = transfer_cov(y, LOGIT, PRIM); dd, l_, h_, _ = summarise(za, zb, B=400, seed=rep); return dd, l_, h_
sims = {}
for kind in ("stable", "half", "null", "context", "misspec"):
    res = [simulate(kind, r) for r in range(20)]; dd = np.array([x[0] for x in res]); l_ = np.array([x[1] for x in res]); h_ = np.array([x[2] for x in res])
    sims[kind] = {"mean": dd.mean(0).tolist(), "detect_rate": (l_ > 0).mean(0).tolist(), "cover0_rate": ((l_ <= 0) & (h_ >= 0)).mean(0).tolist()}
    print(kind, json.dumps(sims[kind]), flush=True)
out["sims"] = sims
cal = all(min(sims[k]["cover0_rate"]) >= 0.95 for k in ("null", "context")) and min(sims["stable"]["detect_rate"]) >= 0.8; out["calibrated"] = bool(cal)
dec = {}
for i, j in enumerate(PRIM):
    r = out["real_primary"][NAMES[j]]
    if not cal: dec[NAMES[j]] = "inconclusive (diagnostic not calibrated)"
    elif r[1] > 0: dec[NAMES[j]] = f"transferable heterogeneity (share {r[0] / sig[i]:.2f} of in-sample σ²)"
    elif r[2] < sims["half"]["mean"][i] and sims["half"]["detect_rate"][i] >= 0.8: dec[NAMES[j]] = "fitted variance lacks a corresponding transferable signal"
    else: dec[NAMES[j]] = "inconclusive"
out["decisions"] = dec; print("decisions:", json.dumps(dec), flush=True)
json.dump(out, open(f"{HERE}/results/stage11_transfer.json", "w"), indent=1)
