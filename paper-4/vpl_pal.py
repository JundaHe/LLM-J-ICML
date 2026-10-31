"""Stage 2c (PROTOCOL_STAGE2C.md + Amendment 1): VPL (Poddar et al., NeurIPS 2024) and PAL-B (Chen et al., ICLR 2025) reimplemented as heads on frozen
per-response embeddings, against D / DF / DFs refitted on the same features, under the stage-2a new-rater protocol (same folds, k-shot draws, metrics).
E1 = graded 5-level labels (ordered-logistic link on the methods' scalar score); E2 = binary labels (ties dropped; native logistic / Bradley-Terry loss).
Usage: python vpl_pal.py --fold 0 [--eval E1|E2]   → results/stage2c_<eval>_f<fold>.json"""
import os, sys, json, time, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np, torch, torch.nn as nn, torch.nn.functional as Fn
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--fold", type=int, required=True); ap.add_argument("--eval", default="E1", choices=("E1", "E2")); ap.add_argument("--draws", type=int, default=5)
ap.add_argument("--ks", default="0,5,10,20,50"); ap.add_argument("--max_epochs", type=int, default=20); ap.add_argument("--models", default="Dp,DFp,DFsp,VPL,PAL2,PAL4"); ap.add_argument("--feat", default=""); ap.add_argument("--tag", default=""); ap.add_argument("--panel", default="multipref_overall"); ap.add_argument("--dump_ratings", action="store_true"); ap.add_argument("--perm_control", action="store_true"); ap.add_argument("--pca", type=int, default=256, help="0 = full standardised features (Stage 3 Am. 5)"); args = ap.parse_args()
torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"])); torch.manual_seed(0); f = args.fold; KS = [int(k) for k in args.ks.split(",")]; MODELS = args.models.split(",")
DEV = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------------------------------------------------------- data, folds (identical to factorised_rm.py / lora_rm.py)
PAN = data_panels.load(args.panel); H = PAN["H"]; K = PAN["K"]; n, m = H.shape; ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); Y = H.reshape(-1); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
if args.panel.startswith("multipref"):
    for i in range(len(R)): GRP[R[i]] = int(POS[i] >= 2)
else:                                                                     # Amendment 4 (PRISM pairs): user region
    gm = PAN["rater_group"]; glev = sorted({gm.get(r, "NA") for r in raters}); GRP = np.array([glev.index(gm.get(r, "NA")) for r in raters])
Gp = np.asarray(PAN["groups"])
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}
test_r = rfold == f; tr_item = ifold[I] != f; is_tr_r = ~test_r[R]; va_item = np.array([vf[g_] for g_ in Gp])[I]
idx_tr = np.where(is_tr_r & tr_item & ~va_item)[0]; idx_va = np.where(is_tr_r & tr_item & va_item)[0]
idx_ad_pool = np.where(~is_tr_r & tr_item)[0]; idx_te = np.where(~is_tr_r & ~tr_item)[0]
if args.panel == "multipref_overall":
    ref = json.load(open(f"{HERE}/results/stage2a_multipref_overall_f{f}.json"))["folds"][0]
    assert ref["n_train"] == len(idx_tr) + len(idx_va) and ref["n_test"] == len(idx_te), "fold mismatch with stage 2a"
BIN = args.eval == "E2"
NATIVE = "yb" in PAN                                                       # PRISM pairs: native binary choice for every pair (no ties to drop)
if BIN and not NATIVE:                                                    # E2: drop ties everywhere (training, adaptation contexts, evaluation)
    keep = Y != 2; idx_tr, idx_va, idx_ad_pool, idx_te = (a[keep[a]] for a in (idx_tr, idx_va, idx_ad_pool, idx_te))
YB = (np.repeat(PAN["yb"], m) if NATIVE else (Y >= 3)).astype(np.float32)  # 1 = B preferred / chosen

# ---------------------------------------------------------------- features: label-free PCA-256 over all per-response embeddings
Fz = np.load(args.feat or f"{P2}/features/{args.panel}/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fz["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
EA, EB, EP = (Fz[k].astype(np.float32) for k in ("E_A", "E_B", "E_P")); allE = np.concatenate([EA, EB, EP]); mu = allE.mean(0)
if args.pca > 0: U, S, Vt = np.linalg.svd(allE[::3] - mu, full_matrices=False); W = Vt[:args.pca].T   # PCA basis fitted on a 1/3 subsample of all rows (label-free)
else: W = np.eye(allE.shape[1], dtype=np.float32)                          # Stage 3 Am. 5: full features, standardised below
def proj(E): Z = (E - mu) @ W; return Z
XA, XB, XP = proj(EA), proj(EB), proj(EP); sd = np.concatenate([XA, XB, XP]).std(0) + 1e-6; XA, XB, XP = (torch.tensor(x / sd, dtype=torch.float32, device=DEV) for x in (XA, XB, XP))
XC = torch.cat([XA, XB, XP], 1); FD = XA.shape[1]                         # 3·FD inputs for the D-family (768 with PCA-256)
It = torch.tensor(I, device=DEV); Rt = torch.tensor(R, device=DEV); Yt = torch.tensor(Y, device=DEV); YBt = torch.tensor(YB, device=DEV)

def ordinal_logp(s, cuts):
    """s: score for B over A (n,); P(y ≤ k) = σ(c_k − s); returns log-probs (n, K)"""
    c = torch.cat([cuts[:1], cuts[:1] + torch.cumsum(Fn.softplus(cuts[1:]), 0)])
    cdf = torch.sigmoid(c[None, :] - s[:, None]); cdf = torch.cat([torch.zeros_like(s)[:, None], cdf, torch.ones_like(s)[:, None]], 1)
    return torch.log((cdf[:, 1:] - cdf[:, :-1]).clamp_min(1e-9))
def metrics(lp, idx):
    """per-rating (ll, rps, dir) for graded log-probs lp (n, K) or binary log P(B) (n,) in E2"""
    y = Y[idx]
    if BIN:
        pB = lp.exp().cpu().numpy(); yb = YB[idx]; ll = np.log(np.where(yb == 1, pB, 1 - pB) + 1e-9); return ll, np.zeros_like(ll), ((pB > 0.5) == (yb == 1)).astype(float)
    pk = lp.exp().cpu().numpy(); ll = lp.cpu().numpy()[np.arange(len(idx)), y]; cdf = np.cumsum(pk, 1); st = (np.arange(K)[None, :] >= y[:, None]).astype(float)
    ey = (pk * np.arange(K)).sum(1); dirc = np.where(y == 2, np.nan, (np.sign(ey - 2) == np.sign(y - 2)).astype(float))
    return ll, ((cdf - st) ** 2).sum(1) / (K - 1), dirc
def to_binary(lp5):
    """graded log-probs → log P(B | not tie)"""
    p = lp5.exp(); return torch.log((p[:, 3] + p[:, 4]) / (p[:, 0] + p[:, 1] + p[:, 3] + p[:, 4]) + 1e-9)

# ---------------------------------------------------------------- D-family on the pair features (multinomial head + text-independent rater offsets)
class DFam:
    def __init__(s, kind, lb, lr):
        s.kind, s.lb, s.lr = kind, lb, lr; s.V = torch.zeros(3 * FD, K, device=DEV); s.b = torch.zeros(K, device=DEV); s.B = torch.zeros(NR, K, device=DEV); s.Bs = torch.zeros(NR, 3, device=DEV); s.cB = None
    def rk(s): return {"Dp": [], "DFp": ["B"], "DFsp": ["Bs"]}[s.kind]
    def logits(s, idx):
        lg = XC[It[idx]] @ s.V + s.b
        if s.kind == "DFp": lg = lg + s.B[Rt[idx]]
        if s.kind == "DFsp": lg = lg + s.Bs[Rt[idx]][:, [0, 1, 2, 1, 0]]
        return torch.log_softmax(lg, 1)
    def logp(s, idx): lp = s.logits(idx); return to_binary(lp) if BIN else lp
    def nll(s, idx):
        if BIN: lp = s.logp(idx); return -torch.where(YBt[idx] == 1, lp, torch.log1p(-lp.exp() + 1e-9)).sum()
        return -s.logits(idx)[torch.arange(len(idx)), Yt[idx]].sum()
    def fit(s, idx, keys, center=None):
        ps = [getattr(s, k) for k in keys]; [p.requires_grad_(True) for p in ps]; ii = torch.tensor(idx, device=DEV)
        opt = torch.optim.LBFGS(ps, lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); pen = 0.0
            for k in keys:
                w = s.lb if k in ("V",) else (s.lr if k in ("B", "Bs") else 0.0); c = center[k] if (center and k in center) else 0.0
                pen = pen + w * ((getattr(s, k) - c) ** 2).sum()
            loss = s.nll(ii) + pen; loss.backward(); return loss
        opt.step(cl); [setattr(s, k, getattr(s, k).detach()) for k in keys]; return s
def train_D(kind):
    best = None
    for lb in ((100, 300, 1000) if args.pca > 0 else (100, 300, 1000, 3000, 10000, 30000, 100000)):
        for lr in ((0.5, 2, 8) if kind != "Dp" else (0,)):
            mdl = DFam(kind, lb, lr).fit(idx_tr, ["V", "b"] + DFam(kind, 1, 1).rk()); v = metrics(mdl.logp(torch.tensor(idx_va, device=DEV)), idx_va)[0].mean()
            if best is None or v > best[0]: best = (v, lb, lr)
    mdl = DFam(kind, best[1], best[2]).fit(np.concatenate([idx_tr, idx_va]), ["V", "b"] + DFam(kind, 1, 1).rk())
    seen = np.unique(R[np.concatenate([idx_tr, idx_va])]); mdl.cB = {k: getattr(mdl, k)[torch.tensor(seen, device=DEV)].mean(0).expand_as(getattr(mdl, k)).clone() for k in mdl.rk()}
    return mdl, {"lb": best[1], "lr": best[2]}
def adapt_D(mdl, ad, te):
    c = DFam(mdl.kind, mdl.lb, mdl.lr); c.V, c.b = mdl.V, mdl.b; c.B, c.Bs = mdl.B.clone(), mdl.Bs.clone()
    for k in mdl.rk(): setattr(c, k, mdl.cB[k].clone())
    if mdl.rk() and len(ad): c.fit(ad, mdl.rk(), mdl.cB)
    return c.logp(torch.tensor(te, device=DEV)), c

# ---------------------------------------------------------------- VPL (pair encoder → attention pooling → z; decoder MLP([x; z]) → reward)
class VPL(nn.Module):
    def __init__(s, d=None, hid=512, lat=512):
        d = d or FD
        super().__init__(); cin = 2 * d + (0 if BIN else K)
        s.pair = nn.Sequential(nn.Linear(cin, hid), nn.LeakyReLU(0.2), nn.Linear(hid, hid), nn.LeakyReLU(0.2), nn.Linear(hid, lat))
        s.wq, s.wk, s.wv = nn.Linear(lat, lat), nn.Linear(lat, lat), nn.Linear(lat, lat); s.mean, s.logv = nn.Linear(lat, lat), nn.Linear(lat, lat)
        s.dec = nn.Sequential(nn.Linear(d + lat, hid), nn.LeakyReLU(0.2), nn.Linear(hid, hid), nn.LeakyReLU(0.2), nn.Linear(hid, 1)); s.cuts = nn.Parameter(torch.tensor([-1.5, -0.5, 0.5, 1.5]))
    def ctx_in(s, cidx):
        a, b = XA[It[cidx]], XB[It[cidx]]
        if BIN: ch = YBt[cidx][:, None] == 1; return torch.cat([torch.where(ch, b, a), torch.where(ch, a, b)], 1)     # (chosen, rejected), as in the official code
        return torch.cat([a, b, Fn.one_hot(Yt[cidx], K).float()], 1)
    def encode(s, ctx_list):
        out = []
        for cidx in ctx_list:
            h = s.pair(s.ctx_in(cidx)); att = torch.softmax(s.wq(h) @ s.wk(h).T / h.shape[-1] ** 0.5, -1); out.append((att @ s.wv(h)).mean(0))
        o = torch.stack(out); return torch.clamp(s.mean(o), -1, 1), torch.clamp(s.logv(o), -1, 1)
    def score(s, tidx, z): return (s.dec(torch.cat([XB[It[tidx]], z], 1)) - s.dec(torch.cat([XA[It[tidx]], z], 1)))[:, 0]
    def logp(s, tidx, z):
        sc = s.score(tidx, z); return Fn.logsigmoid(sc) if BIN else ordinal_logp(sc, s.cuts)
def vpl_contexts(targets, pool_by_r, rng, C=8):
    ctx = []
    for t in targets:
        p = [j for j in pool_by_r[int(R[t])] if j != t]; ctx.append(torch.tensor(rng.choice(p, min(C, len(p)), replace=False), device=DEV))
    return ctx
def vpl_nll(mdl, tidx, z):
    lp = mdl.logp(tidx, z)
    return -torch.where(YBt[tidx] == 1, lp, torch.log1p(-lp.exp() + 1e-9)).sum() if BIN else -lp[torch.arange(len(tidx)), Yt[tidx]].sum()
def train_vpl():
    pool_tr = {}
    for j in idx_tr: pool_tr.setdefault(int(R[j]), []).append(int(j))
    tr = np.array([j for j in idx_tr if len(pool_tr[int(R[j])]) > 8]); va = idx_va[np.isin(R[idx_va], list(pool_tr))]
    best = None
    for lr, klw in [(lr_, kw_) for lr_ in (3e-4, 1e-3) for kw_ in (0.01, 0.001, 0.0)]:          # Amendment 2: KL weight 0.01 (official) / 0.001 / 0 against posterior collapse
        torch.manual_seed(0); mdl = VPL().to(DEV); opt = torch.optim.Adam(mdl.parameters(), lr=lr); rng = np.random.RandomState(0); hist = []; best_state = None; bad = 0
        for ep in range(args.max_epochs):
            mdl.train()
            for b0 in range(0, len(tr), 64):
                t = tr[rng.permutation(len(tr))[:64]]
                mean, logv = mdl.encode(vpl_contexts(t, pool_tr, rng)); z = mean + torch.exp(0.5 * logv) * torch.randn_like(mean); z = Fn.normalize(z, dim=-1) * z.shape[-1] ** 0.5
                kl = -0.5 * (1 + logv - mean ** 2 - logv.exp()).sum(1).mean(); loss = vpl_nll(mdl, torch.tensor(t, device=DEV), z) / len(t) + klw * kl
                opt.zero_grad(); loss.backward(); opt.step()
                if b0 >= 64 * 200: break                                  # 200 minibatches per epoch
            mdl.eval()
            with torch.no_grad():
                vr = np.random.RandomState(1); mean, _ = mdl.encode(vpl_contexts(va, pool_tr, vr)); v = metrics(mdl.logp(torch.tensor(va, device=DEV), mean), va)[0].mean()
            hist.append(float(v))
            if best_state is None or v > max(hist[:-1] + [-1e9]): best_state = {k: x.clone() for k, x in mdl.state_dict().items()}; bad = 0
            else: bad += 1
            if bad >= 3: break
        out_hp.setdefault("VPL_grid", []).append({"lr": lr, "kl": klw, "val_ll": max(hist), "epochs": len(hist)})
        if best is None or max(hist) > best[0]: best = (max(hist), (lr, klw), best_state, len(hist))
    mdl = VPL().to(DEV); mdl.load_state_dict(best[2]); mdl.eval(); return mdl, {"lr": best[1][0], "kl": best[1][1], "epochs_run": best[3], "val_ll": best[0]}

# ---------------------------------------------------------------- PAL-B (K prototype projectors of the prompt; user = softmax mixture; angle learner)
def mlp2(d_in, d): return nn.Sequential(nn.Linear(d_in, 512), nn.GELU(), nn.Linear(512, d))
class PAL(nn.Module):
    def __init__(s, k, d=None, dp=512):
        d = d or FD
        super().__init__(); s.k = k; s.g = nn.ModuleList([mlp2(d, dp) for _ in range(k)]); s.fi = mlp2(d, dp); s.W = nn.Parameter(torch.randn(NR, k) * 1.0)
        s.logit_scale = nn.Parameter(torch.tensor(np.log(10.0), dtype=torch.float32)); s.cuts = nn.Parameter(torch.tensor([-1.5, -0.5, 0.5, 1.5]))
    def score(s, tidx, W=None):
        w = torch.softmax((s.W if W is None else W)[Rt[tidx]], 1); u = sum(w[:, j:j + 1] * s.g[j](XP[It[tidx]]) for j in range(s.k)); u = Fn.normalize(u, dim=-1)
        fa, fb = Fn.normalize(s.fi(XA[It[tidx]]), dim=-1), Fn.normalize(s.fi(XB[It[tidx]]), dim=-1); sc = torch.clamp(s.logit_scale.exp(), max=100)
        return ((fb * u).sum(1) - (fa * u).sum(1)) * sc
    def logp(s, tidx, W=None):
        sc = s.score(tidx, W); return Fn.logsigmoid(sc) if BIN else ordinal_logp(sc, s.cuts)
def pal_nll(mdl, tidx, W=None):
    lp = mdl.logp(tidx, W)
    return -torch.where(YBt[tidx] == 1, lp, torch.log1p(-lp.exp() + 1e-9)).sum() if BIN else -lp[torch.arange(len(tidx)), Yt[tidx]].sum()
def train_pal(k):
    best = None
    for lr in (3e-4, 1e-3):
        torch.manual_seed(0); mdl = PAL(k).to(DEV); opt = torch.optim.Adam([{"params": [p for n_, p in mdl.named_parameters() if n_ != "W"], "lr": lr}, {"params": [mdl.W], "lr": 5e-3}])
        rng = np.random.RandomState(0); hist = []; best_state = None; bad = 0
        for ep in range(args.max_epochs):
            mdl.train(); order = rng.permutation(idx_tr)
            for b0 in range(0, len(order), 256):
                t = torch.tensor(order[b0:b0 + 256], device=DEV); loss = pal_nll(mdl, t) / len(t); opt.zero_grad(); loss.backward(); opt.step()
            mdl.eval()
            with torch.no_grad(): v = metrics(mdl.logp(torch.tensor(idx_va, device=DEV)), idx_va)[0].mean()
            hist.append(float(v))
            if best_state is None or v > max(hist[:-1] + [-1e9]): best_state = {k_: x.clone() for k_, x in mdl.state_dict().items()}; bad = 0
            else: bad += 1
            if bad >= 3: break
        if best is None or max(hist) > best[0]: best = (max(hist), lr, best_state, len(hist))
    mdl = PAL(k).to(DEV); mdl.load_state_dict(best[2]); mdl.eval()
    seen = torch.tensor(np.unique(R[np.concatenate([idx_tr, idx_va])]), device=DEV); w0 = mdl.W.detach()[seen].mean(0)
    return mdl, {"lr": best[1], "epochs_run": best[3], "val_ll": best[0]}, w0
def adapt_pal(mdl, w0, ad, te, lam=1e-3):
    Wn = mdl.W.detach().clone(); test = torch.tensor(np.unique(R[te]), device=DEV); Wn[test] = w0
    if len(ad):
        Wp = Wn.clone().requires_grad_(True); ii = torch.tensor(ad, device=DEV); opt = torch.optim.LBFGS([Wp], lr=0.5, max_iter=100, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); loss = pal_nll(mdl, ii, Wp) + lam * ((Wp[test] - w0) ** 2).sum(); loss.backward(); return loss
        opt.step(cl); Wn = Wp.detach()
    with torch.no_grad(): return mdl.logp(torch.tensor(te, device=DEV), Wn), Wn

# ---------------------------------------------------------------- run
out_hp = {}
def tune_pal_lambda(k_, hp):
    """Amendment 2: adaptation ridge for PAL chosen per k by k-shot validation on 20 % held-out training raters (PAL refit without them)"""
    global idx_tr, idx_va
    tr_r = np.unique(R[np.concatenate([idx_tr, idx_va])]); vr = set(np.random.RandomState(3 + f).choice(tr_r, len(tr_r) // 5, replace=False)); inv = np.isin(R, list(vr))
    keep_tr, keep_va = idx_tr, idx_va; idx_tr, idx_va = keep_tr[~inv[keep_tr]], keep_va[~inv[keep_va]]
    m5, _, w05 = train_pal(k_); idx_tr, idx_va = keep_tr, keep_va
    pool5, sc5 = keep_tr[inv[keep_tr]], keep_va[inv[keep_va]]; lam_k = {}
    for k in [k for k in KS if k > 0]:
        best = None
        for lam in (1e-3, 0.1, 1.0, 10.0):
            rng5 = np.random.RandomState(60_000 + k); ad = []; kr = []
            for r in vr:
                pl = pool5[R[pool5] == r]
                if len(pl) >= k: kr.append(r); ad.extend(rng5.choice(pl, k, replace=False))
            sc = sc5[np.isin(R[sc5], kr)]; lp, _ = adapt_pal(m5, w05, np.array(ad, int), sc, lam); v = metrics(lp, sc)[0].mean()
            if best is None or v > best[0]: best = (v, lam)
        lam_k[k] = best[1]
    return lam_k
t0 = time.time(); DUMP = []; out = {"fold": f, "eval": args.eval, "protocol": "PROTOCOL_STAGE2C.md", "models": MODELS, "hp": {}, "per_rater": [], "latents": []}
fits = {}
for mname in MODELS:
    if mname in ("Dp", "DFp", "DFsp"): fits[mname] = train_D(mname); out["hp"][mname] = fits[mname][1]
    elif mname == "VPLs": continue                                       # uses the trained VPL
    elif mname == "VPL": fits[mname] = train_vpl(); out["hp"][mname] = fits[mname][1]
    else: mdl_, hp_, w0_ = train_pal(int(mname[3:])); hp_["lam_adapt"] = tune_pal_lambda(int(mname[3:]), hp_); fits[mname] = (mdl_, w0_, hp_["lam_adapt"]); out["hp"][mname] = hp_
    print(f"fold {f} {args.eval} trained {mname} {out['hp'][mname]} [{time.time()-t0:.0f}s]", flush=True)
test_raters = np.unique(R[idx_te])
for k in KS:
    for dr in range(args.draws if k > 0 else 1):
        rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep_r = []
        for r in test_raters:                                             # same draw sequence as stage 2a (pool restricted to non-ties in E2)
            pool = idx_ad_pool[R[idx_ad_pool] == r]
            if len(pool) < k: continue
            keep_r.append(r); ad.extend(rng.choice(pool, k, replace=False))
        ad = np.array(ad, int); te = idx_te[np.isin(R[idx_te], keep_r)]; res = {}; lat = {}; resP = {}
        PERM = args.perm_control and k > 0
        if PERM:                                                          # Stage 3 Amendment 1: derangement of the test raters' adapted parameters
            o_ = np.random.RandomState(777 + 10_000 * f + 100 * k + dr).permutation(len(keep_r)); SRC = {int(keep_r[o_[i]]): int(keep_r[o_[(i + 1) % len(o_)]]) for i in range(len(o_))}
            tgt_ = torch.tensor(list(SRC.keys()), device=DEV); src_ = torch.tensor(list(SRC.values()), device=DEV)
        for mname in MODELS:
            if mname == "VPLs": continue
            if mname in ("Dp", "DFp", "DFsp"):
                lp, c = adapt_D(fits[mname][0], ad, te); res[mname] = metrics(lp, te)
                if PERM:
                    sv = {kk: getattr(c, kk) for kk in c.rk()}
                    for kk, v in sv.items(): vp = v.clone(); vp[tgt_] = v[src_]; setattr(c, kk, vp)
                    with torch.no_grad(): resP[mname] = metrics(c.logp(torch.tensor(te, device=DEV)), te)
                    for kk, v in sv.items(): setattr(c, kk, v)
                if mname == "DFsp": lat["DFs"] = c.Bs
                if mname == "DFp": lat["DF"] = c.B
            elif mname == "VPL":
                mdl = fits[mname][0]
                with torch.no_grad():
                    if k > 0: ctx = [torch.tensor(ad[R[ad] == r], device=DEV) for r in keep_r]; mean, _ = mdl.encode(ctx)
                    else: mean = torch.zeros(len(keep_r), 512, device=DEV)            # k = 0: prior mean of z
                    zmap = dict(zip(keep_r, mean))
                    z = torch.stack([zmap[int(r)] for r in R[te]]); lpv = mdl.logp(torch.tensor(te, device=DEV), z); res[mname] = metrics(lpv, te); lat["VPL"] = zmap
                    if PERM: resP[mname] = metrics(mdl.logp(torch.tensor(te, device=DEV), torch.stack([zmap[SRC[int(r)]] for r in R[te]])), te)
                if "VPLs" in MODELS and not BIN:                          # Amendment 3: VPL + symmetric style offsets fitted on the same k ratings (VPL frozen)
                    if k > 0:
                        with torch.no_grad(): za = torch.stack([zmap[int(r)] for r in R[ad]]); lpa = mdl.logp(torch.tensor(ad, device=DEV), za)
                        rix = {int(r): j for j, r in enumerate(keep_r)}; ra = torch.tensor([rix[int(r)] for r in R[ad]], device=DEV); ya = Yt[torch.tensor(ad, device=DEV)]
                        Bs = torch.zeros(len(keep_r), 3, device=DEV, requires_grad=True); opt_s = torch.optim.LBFGS([Bs], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
                        def cl_s():
                            opt_s.zero_grad(); l2 = torch.log_softmax(lpa + Bs[ra][:, [0, 1, 2, 1, 0]], 1); loss = -l2[torch.arange(len(ad)), ya].sum() + 2.0 * (Bs ** 2).sum(); loss.backward(); return loss
                        opt_s.step(cl_s); rt = torch.tensor([rix[int(r)] for r in R[te]], device=DEV)
                        with torch.no_grad(): res["VPLs"] = metrics(torch.log_softmax(lpv + Bs.detach()[rt][:, [0, 1, 2, 1, 0]], 1), te)
                    else: res["VPLs"] = res[mname]
            else:
                lp, Wn = adapt_pal(fits[mname][0], fits[mname][1], ad, te, fits[mname][2].get(k, 1e-3)); res[mname] = metrics(lp, te); lat[mname] = torch.softmax(Wn, 1)
                if PERM:
                    WnP = Wn.clone(); WnP[tgt_] = Wn[src_]
                    with torch.no_grad(): resP[mname] = metrics(fits[mname][0].logp(torch.tensor(te, device=DEV), WnP), te)
        if args.dump_ratings: DUMP.append({"fold": np.full(len(te), f), "k": np.full(len(te), k), "draw": np.full(len(te), dr), "rater": R[te], "item": I[te], "igroup": np.asarray(Gp)[I[te]],
                                           **{f"{mn}_{mt}": np.asarray(res[mn][j]) for mn in res for j, mt in ((0, "ll"), (2, "dir"))}, **{f"{mn}_perm_{mt}": np.asarray(resP[mn][j]) for mn in resP for j, mt in ((0, "ll"), (2, "dir"))}})
        for r in keep_r:
            sel = R[te] == r
            out["per_rater"].append({"fold": f, "k": k, "draw": dr, "rater": int(r), "n": int(sel.sum()), "n_dir": int(np.isfinite(res[MODELS[0]][2][sel]).sum()),
                                     **{f"{mn}_{mt}": float(np.nansum(res[mn][j][sel])) for mn in res for j, mt in enumerate(("ll", "rps", "dir"))},
                                     **{f"{mn}_perm_{mt}": float(np.nansum(resP[mn][j][sel])) for mn in resP for j, mt in enumerate(("ll", "rps", "dir"))}})
            if k == max(KS) and dr == 0:                                  # C3: per-rater latents at the largest k, draw 0
                row = {"fold": f, "rater": int(r)}
                for key, v in lat.items(): row[key] = (v[int(r)] if isinstance(v, dict) else v[int(r)]).detach().cpu().numpy().tolist()
                out["latents"].append(row)
    print(f"fold {f} {args.eval} k={k} done [{time.time()-t0:.0f}s]", flush=True)
os.makedirs(f"{HERE}/results", exist_ok=True); out["hp"]["grids"] = out_hp; pfx = "" if args.panel == "multipref_overall" else f"{args.panel}_"; json.dump(out, open(f"{HERE}/results/stage2c_{pfx}{args.eval}_f{f}{args.tag}.json", "w")); 
if args.dump_ratings: os.makedirs(f"{HERE}/results/ratings", exist_ok=True); np.savez_compressed(f"{HERE}/results/ratings/stage2c_{pfx}{args.eval}_f{f}{args.tag}.npz", **{key: np.concatenate([d[key] if key in d else np.full(len(d["fold"]), np.nan) for d in DUMP]) for key in sorted(set().union(*DUMP))})
print("done", flush=True)
