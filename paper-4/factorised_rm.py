"""Stage 2a (PROTOCOL_STAGE2.md): factorised reward model vs text-only, distributional, group-conditioned and low-rank personalised baselines on MultiPref,
evaluated on NEW raters adapted from k of their ratings. Frozen Qwen2.5-7B features (label-free PCA-256) as the text representation.
Usage: python factorised_rm.py [--folds 0,1,2,3,4] [--draws 5]   → results/stage2a_<panel>.json (per-rating predictions summarised per rater) and a bootstrap summary"""
import os, sys, json, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "4")
import numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", default="multipref_overall"); ap.add_argument("--folds", default="0,1,2,3,4"); ap.add_argument("--draws", type=int, default=5)
ap.add_argument("--ks", default="0,5,10,20,50"); ap.add_argument("--d", type=int, default=8); ap.add_argument("--iters", type=int, default=300); ap.add_argument("--B", type=int, default=2000); ap.add_argument("--tag", default=""); ap.add_argument("--merge", default="", help="comma-separated tags of per-fold runs to merge and summarise (no training)"); args = ap.parse_args()
torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"])); torch.set_default_dtype(torch.float64)
KS = [int(k) for k in args.ks.split(",")]; MODELS = ("D", "DG", "DF", "DFs", "DL", "T0", "T1", "G", "F", "F1", "F_shift", "F_scale", "L", "LS")   # T1/F1: Amendment 1; DG/DF/DL (distributional text head + group / rater category offsets / low-rank latent): Amendment 2

# ---------------------------------------------------------------- data (long format)
PAN = data_panels.load(args.panel); H = PAN["H"]; K = PAN["K"]; n, m = H.shape; ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); Y = H.reshape(-1); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
for i in range(len(R)): GRP[R[i]] = int(POS[i] >= 2)                     # 0 = crowd (positions 0,1), 1 = expert (2,3); disjoint sets (checked)
F_ = np.load(f"{P2}/features/{args.panel}/Qwen2.5-7B-Instruct.npz", allow_pickle=True); assert np.array_equal(F_["item_ids"].astype(str), np.asarray(PAN["item_ids"]).astype(str))
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, Vt = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0)   # label-free PCA-256, unit-variance scores
X = torch.tensor(X); Gp = np.asarray(PAN["groups"])

Phi = lambda z: 0.5 * (1 + torch.erf(z / np.sqrt(2)))
def cuts_of(c0): return torch.cat([c0[:1], c0[:1] + torch.cumsum(torch.nn.functional.softplus(c0[1:]), 0)])
def probit_pk(mu, sig, c0):
    z = (cuts_of(c0)[None, :] - mu[:, None]) / sig[:, None]; cdf = torch.cat([torch.zeros(len(mu), 1), Phi(z), torch.ones(len(mu), 1)], 1); return (cdf[:, 1:] - cdf[:, :-1]).clamp_min(1e-12)

class Model:
    """parameters: text side (beta, c0, W, V/bias for D, group params) and rater side (delta, s, z) indexed by global rater id"""
    def __init__(s, kind, lam):
        s.kind, s.lam = kind, lam; d = args.d
        s.p = {"beta": torch.zeros(256), "c0": torch.tensor([-1.0] + [0.0] * (K - 2)), "delta": torch.zeros(NR), "s": torch.zeros(NR), "z": torch.zeros(NR, d),
               "W": torch.randn(256, d, generator=torch.Generator().manual_seed(0)) * 0.01, "V": torch.zeros(256, K), "b": torch.zeros(K), "gd": torch.zeros(2), "gs": torch.zeros(2), "gam": torch.zeros(256), "gb": torch.zeros(2, K), "Br": torch.zeros(NR, K), "W5": torch.randn(256, d * K, generator=torch.Generator().manual_seed(1)) * 0.01, "w0": torch.zeros(d * K), "wl0": torch.zeros(d), "Bs": torch.zeros(NR, 3)}   # w0/wl0: unpenalised constant column of the low-rank map (Amendment 4: L ⊇ F_shift, DL ⊇ DF)
        s.center = {}
    def text_keys(s):
        return {"D": ["V", "b"], "DG": ["V", "b", "gb"], "DF": ["V", "b"], "DFs": ["V", "b"], "DL": ["V", "b", "W5", "w0"], "G": ["beta", "c0", "gd", "gs"], "L": ["beta", "c0", "W", "wl0"], "LS": ["beta", "c0", "W", "wl0"], "T1": ["beta", "c0", "gam"], "F1": ["beta", "c0", "gam"]}.get(s.kind, ["beta", "c0"])
    def rater_keys(s):
        return {"DF": ["Br"], "DFs": ["Bs"], "DL": ["z"], "F": ["delta", "s"], "F1": ["delta", "s"], "F_shift": ["delta"], "F_scale": ["s"], "L": ["z"], "LS": ["z", "s"]}.get(s.kind, [])
    def logp(s, ii, rr):
        p = s.p; x = X[ii]
        if s.kind in ("D", "DG", "DF", "DFs", "DL"):
            lg = x @ p["V"] + p["b"]
            if s.kind == "DG": lg = lg + p["gb"][torch.tensor(GRP[rr])]
            if s.kind == "DF": lg = lg + p["Br"][rr]
            if s.kind == "DFs": lg = lg + p["Bs"][rr][:, [0, 1, 2, 1, 0]]   # symmetric style offsets: extreme / slight / tie (no A-vs-B position term; Amendment 4)
            if s.kind == "DL": lg = lg + ((x @ p["W5"] + p["w0"]).view(len(ii), args.d, K) * p["z"][rr][:, :, None]).sum(1)
            return torch.log_softmax(lg, 1)
        mu = x @ p["beta"]; ls = torch.zeros(len(ii))
        if s.kind == "G": g = torch.tensor(GRP[rr]); mu = mu + p["gd"][g]; ls = ls + p["gs"][g]
        if s.kind in ("T1", "F1"): ls = ls + x @ p["gam"]
        if s.kind in ("F", "F1", "F_shift"): mu = mu + p["delta"][rr]
        if s.kind in ("F", "F1", "F_scale", "LS"): ls = ls + p["s"][rr]
        if s.kind in ("L", "LS"): mu = mu + ((x @ p["W"] + p["wl0"]) * p["z"][rr]).sum(1)
        return torch.log(probit_pk(mu, torch.exp(ls), p["c0"]))
    def penalty(s, keys):
        lb, lr, lw = s.lam; p = s.p; out = 0.0
        for k in keys:
            w = {"beta": lb, "V": lb, "gam": lb, "W": lw, "W5": lw, "delta": lr, "s": lr, "z": lr, "Br": lr, "Bs": lr, "gd": 1.0, "gs": 1.0, "gb": 1.0}.get(k, 0.0)
            out = out + w * ((p[k] - s.center[k]) ** 2).sum() if k in s.center else out + w * (p[k] ** 2).sum()   # adaptation shrinks toward the training-rater mean (Amendment 2)
        return out
    def fit(s, idx, keys):
        ii = torch.tensor(I[idx]); rr = torch.tensor(R[idx]); yy = torch.tensor(Y[idx])
        for k in s.p: s.p[k].requires_grad_(k in keys)
        opt = torch.optim.LBFGS([s.p[k] for k in keys], lr=0.5, max_iter=args.iters, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); loss = -s.logp(ii, rr)[torch.arange(len(yy)), yy].sum() + s.penalty(keys); loss.backward(); return loss
        opt.step(cl)
        for k in s.p: s.p[k] = s.p[k].detach()
        return s
    def per_rating(s, idx):
        """log-lik, RPS and direction-correctness of every rating in idx"""
        with torch.no_grad():
            lp = s.logp(torch.tensor(I[idx]), torch.tensor(R[idx])); pk = lp.exp(); yy = Y[idx]
            ll = lp[torch.arange(len(idx)), torch.tensor(yy)].numpy()
            cdf = torch.cumsum(pk, 1).numpy(); step = (np.arange(K)[None, :] >= yy[:, None]).astype(float); rps = ((cdf - step) ** 2).sum(1) / (K - 1)
            ey = (pk.numpy() * np.arange(K)).sum(1); dirc = np.where(yy == 2, np.nan, (np.sign(ey - 2) == np.sign(yy - 2)).astype(float))
        return ll, rps, dirc

def set_center(mdl, idx):
    """population mean of the rater-side parameters over the raters seen in training (prior mean for new raters)"""
    tr = torch.tensor(np.unique(R[idx]))
    for k in mdl.rater_keys(): mdl.center[k] = mdl.p[k][tr].mean(0).expand_as(mdl.p[k]).clone()
    return mdl
# Amendment 3: coordinate-wise selection on extended grids. The text penalty λβ is chosen on the rater-agnostic base model of each family (D for DG/DF/DL; T0 for G/F/F_shift/F_scale/L/LS; T1 for F1)
# and then held fixed while the rater-side penalties are chosen.
LB, LR, LW = (10, 100, 300, 1000, 3000, 10000), (0.5, 2, 8, 32, 128, 512), (1, 10, 100, 1000, 10000)
BASE = {"DG": "D", "DF": "D", "DFs": "D", "DL": "D", "G": "T0", "F": "T0", "F_shift": "T0", "F_scale": "T0", "L": "T0", "LS": "T0", "F1": "T1"}
SEL = {}
def grid(kind):
    if kind in ("D", "T0", "T1"): return [(lb, 0, 0) for lb in LB]
    lb = SEL[BASE[kind]][0]
    if kind in ("DG", "G"): return [(lb, 0, 0)]
    if kind in ("DL", "L", "LS"): return [(lb, lr, lw) for lr in LR for lw in LW]
    return [(lb, lr, 0) for lr in LR]
def train(kind, idx_tr, idx_va):
    best = None
    for lam in grid(kind):
        mdl = Model(kind, lam).fit(idx_tr, mdl_keys(kind))
        va = mdl.per_rating(idx_va)[0].mean()
        if best is None or va > best[0]: best = (va, lam)
    SEL[kind] = best[1]
    full = np.concatenate([idx_tr, idx_va]); return set_center(Model(kind, best[1]).fit(full, mdl_keys(kind)), full), best[1]
def mdl_keys(kind): m_ = Model(kind, (1, 1, 1)); return m_.text_keys() + m_.rater_keys()

def adapt(mdl, idx_ad):
    """MAP of the rater-side parameters of the test raters in idx_ad, text side frozen; returns a copy"""
    keys = mdl.rater_keys()
    if not keys or len(idx_ad) == 0: return mdl
    c = Model(mdl.kind, mdl.lam); c.p = {k: v.clone() for k, v in mdl.p.items()}; c.center = dict(mdl.center)
    te = torch.tensor(np.unique(R[idx_ad]))
    for k in keys: c.p[k][te] = c.center[k][te]                       # start new raters at the prior mean
    return c.fit(idx_ad, keys)

# ---------------------------------------------------------------- folds
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in (0, 1):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}                              # validation prompt groups (15 %) inside training items
out = {"panel": args.panel, "protocol": "PROTOCOL_STAGE2.md", "n_raters": NR, "ks": KS, "folds": [], "per_rater": []}
t0 = time.time()
if args.merge:
    for tg in args.merge.split(","):
        o_ = json.load(open(f"{HERE}/results/stage2a_{args.panel}{tg}.json")); out["folds"] += o_["folds"]; out["per_rater"] += o_["per_rater"]
for f in ([] if args.merge else [int(x) for x in args.folds.split(",")]):
    test_r = rfold == f; tr_item = ifold[I] != f; is_tr_r = ~test_r[R]
    va_item = np.array([vf[g_] for g_ in Gp])[I]
    idx_tr = np.where(is_tr_r & tr_item & ~va_item)[0]; idx_va = np.where(is_tr_r & tr_item & va_item)[0]
    idx_ad_pool = np.where(~is_tr_r & tr_item)[0]; idx_te = np.where(~is_tr_r & ~tr_item)[0]; idx_seen = np.where(is_tr_r & ~tr_item)[0]
    fits = {}; lam_sel = {}
    for kind in MODELS: fits[kind], lam_sel[kind] = train(kind, idx_tr, idx_va); print(f"fold {f} trained {kind} λ={lam_sel[kind]} [{time.time()-t0:.0f}s]", flush=True)
    out["folds"].append({"fold": f, "lam": lam_sel, "n_train": int(len(idx_tr) + len(idx_va)), "n_test": int(len(idx_te)), "n_test_raters": int(test_r.sum())})
    test_raters = np.unique(R[idx_te])
    for k in KS:
        for dr in range(args.draws if k > 0 else 1):
            rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep = []
            for r in test_raters:
                pool = idx_ad_pool[R[idx_ad_pool] == r]
                if len(pool) < k: continue
                keep.append(r); ad.extend(rng.choice(pool, k, replace=False) if k > 0 else [])
            ad = np.array(ad, int); te = idx_te[np.isin(R[idx_te], keep)]
            res = {}
            for kind in MODELS:
                mdl = adapt(fits[kind], ad) if k > 0 else fits[kind]
                if k == 0 and mdl.rater_keys():                                    # unseen raters: prior (training-rater) mean
                    mdl = Model(kind, mdl.lam); mdl.p = {kk: v.clone() for kk, v in fits[kind].p.items()}; mdl.center = dict(fits[kind].center)
                    for kk in mdl.rater_keys(): mdl.p[kk] = mdl.center[kk].clone()
                res[kind] = mdl.per_rating(te)
            for r in keep:
                sel = R[te] == r
                out["per_rater"].append({"fold": f, "k": k, "draw": dr, "rater": int(r), "group": int(GRP[r]), "n": int(sel.sum()),
                                         **{f"{kind}_{mt}": float(np.nansum(res[kind][j][sel])) for kind in MODELS for j, mt in enumerate(("ll", "rps", "dir"))},
                                         "n_dir": int(np.isfinite(res["T0"][2][sel]).sum())})
        print(f"fold {f} k={k} done [{time.time()-t0:.0f}s]", flush=True)
    seen = {kind: fits[kind].per_rating(idx_seen)[0].mean() for kind in MODELS}; out["folds"][-1]["seen_ll"] = seen; print("seen-rater LL", {k_: round(v, 4) for k_, v in seen.items()}, flush=True)
    os.makedirs(f"{HERE}/results", exist_ok=True); json.dump(out, open(f"{HERE}/results/stage2a_{args.panel}{args.tag}.json", "w"))

# ---------------------------------------------------------------- summary: per k, mean metric per rating; rater-cluster bootstrap of differences (raters pooled over folds; draws averaged within rater)
import collections
summ = {}
rng = np.random.RandomState(7)
for k in KS:
    rows = [r for r in out["per_rater"] if r["k"] == k]; by = collections.defaultdict(list)
    for r in rows: by[(r["fold"], r["rater"])].append(r)
    keys_ = list(by); agg = {mt: {kind: np.array([np.mean([x[f"{kind}_{mt}"] for x in by[q]]) for q in keys_]) for kind in MODELS} for mt in ("ll", "rps", "dir")}
    nn_ = np.array([np.mean([x["n"] for x in by[q]]) for q in keys_]); nd = np.array([np.mean([x["n_dir"] for x in by[q]]) for q in keys_])
    den = {"ll": nn_, "rps": nn_, "dir": nd}; s_k = {"n_raters": len(keys_), "n_ratings": float(nn_.sum())}
    for mt in ("ll", "rps", "dir"): s_k[mt] = {kind: float(agg[mt][kind].sum() / den[mt].sum()) for kind in MODELS}
    bidx = [rng.randint(0, len(keys_), len(keys_)) for _ in range(args.B)]
    for a, b in (("DFs", "D"), ("DF", "DFs"), ("DF", "D"), ("DF", "DG"), ("DF", "DL"), ("DL", "D"), ("DG", "D"), ("F1", "DF"), ("F", "T0"), ("F", "G"), ("F", "L"), ("F", "D"), ("F_scale", "F_shift"), ("F", "LS"), ("G", "T0"), ("L", "T0"), ("F1", "T1"), ("F1", "G"), ("F1", "L"), ("F1", "LS"), ("F1", "D"), ("T1", "D")):
        for mt in ("ll", "rps", "dir"):
            d = agg[mt][a] - agg[mt][b]; pt = d.sum() / den[mt].sum(); bs = [d[ix].sum() / den[mt][ix].sum() for ix in bidx]
            s_k[f"{a}-{b}_{mt}"] = [float(pt), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    summ[k] = s_k
out["summary"] = summ; json.dump(out, open(f"{HERE}/results/stage2a_{args.panel}{args.tag}.json", "w"))
lines = [f"# Stage 2a — {args.panel}: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)", "", "| k | raters | " + " | ".join(f"LL {m_}" for m_ in MODELS) + " |", "|---" * (2 + len(MODELS)) + "|"]
for k in KS: lines.append(f"| {k} | {summ[k]['n_raters']} | " + " | ".join(f"{summ[k]['ll'][m_]:.4f}" for m_ in MODELS) + " |")
lines += ["", "| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |", "|---|---|---|---|---|---|---|---|---|"]
fmt = lambda v: f"{v[0]:+.4f} [{v[1]:+.4f}, {v[2]:+.4f}]"
for k in KS: lines.append(f"| {k} | " + " | ".join(fmt(summ[k][f"{p}_ll"]) for p in ("DF-D", "DF-DG", "DF-DL", "F_scale-F_shift", "DFs-D", "DF-DFs", "F1-T1", "DL-D")) + " |")
lines += ["", "| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |", "|---|---|---|---|---|---|---|"] + [f"| {k} | " + " | ".join(f"{summ[k]['dir'][m_]:.3f}" for m_ in ("D", "DF", "DFs", "DL")) + " | " + " | ".join(fmt(summ[k][f"{p}_dir"]) for p in ("DF-D", "DFs-D")) + " |" for k in KS]
lines += ["", "Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 %% rater-cluster bootstrap (B = %d). RPS and direction accuracy in the JSON." % args.B]
open(f"{HERE}/results/stage2a_{args.panel}{args.tag}.md", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
