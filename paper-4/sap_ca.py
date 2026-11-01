"""Stage 9 Am. 6 (PROTOCOL_STAGE9.md): frozen Community Alignment evaluation of SAP. Adaptation unit = choice event (a first-turn conversation, its three
chosen-vs-other pairs kept together), k = 20 events; population weights μ per assigned language; comparators SAP-iso and ATTR-LR-bin (rank 2) with adaptation
strength (incl. none) and W-ridge selected on pseudo-new training users (20 %) adapted on k = 20 events; same selection for SAP's {no adaptation, SAP}.
Outcomes: own − μ choice accuracy and LL per method; paired SAP − selected ATTR-LR-bin; rater bootstrap (seed 17)."""
import os, sys, json, collections, numpy as np, torch, torch.nn.functional as Fn
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from attr_feats import attr_G, NAMES
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); KEV = 20
PAN = data_panels.load("ca_pairs"); n = len(PAN["item_ids"]); ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters); R = np.array([rid[row[0]] for row in ev])
gm = PAN["rater_group"]; glev = sorted({gm.get(r, "NA") for r in raters}); GRP = np.array([glev.index(gm.get(r, "NA")) for r in raters])   # folds as vpl_pal.py
Gp = np.asarray(PAN["groups"]); rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}; va_item = np.array([vf[g_] for g_ in Gp])
EVT = np.array([s.split("|")[0] for s in PAN["item_ids"]]); LANG = np.asarray(PAN["lang"]); langs = sorted(set(LANG)); LI = np.array([langs.index(l) for l in LANG])
ulang = np.zeros(NR, int)
for j in range(n): ulang[R[j]] = LI[j]
YB = torch.tensor(np.asarray(PAN["yb"]).astype(float)); A = torch.tensor(attr_G(list(PAN["resp_A"]), list(PAN["resp_B"]), PAN["texts"])); J = A.shape[1]
Fz = np.load(f"{P2}/features/ca_pairs/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fz["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
EA, EB = Fz["E_A"].astype(np.float32), Fz["E_B"].astype(np.float32); sub = np.concatenate([EA[::6], EB[::6], Fz["E_P"][::6].astype(np.float32)]); mu0 = sub.mean(0)
_, _, Vt = np.linalg.svd(sub - mu0, full_matrices=False); W256 = Vt[:256].T; del sub                                  # PCA-256 basis on a label-free subsample
XA, XB = (EA - mu0) @ W256, (EB - mu0) @ W256; del EA, EB; sd = np.concatenate([XA, XB]).std(0) + 1e-6; X = torch.tensor((XB - XA) / sd); Rt = torch.tensor(R); Lt = torch.tensor(LI)
def nll(lg, y): return -(y * Fn.logsigmoid(lg) + (1 - y) * Fn.logsigmoid(-lg))
def fit_base(idx, idx_va):
    best = None
    for lam in (1.0, 10.0, 100.0, 1000.0):
        w = torch.zeros(X.shape[1], requires_grad=True); b = torch.zeros(1, requires_grad=True); ii = torch.tensor(idx); opt = torch.optim.LBFGS([w, b], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); loss = nll(X[ii] @ w + b, YB[ii]).sum() + lam * (w ** 2).sum(); loss.backward(); return loss
        opt.step(cl)
        with torch.no_grad(): iv = torch.tensor(idx_va); v = -float(nll(X[iv] @ w + b, YB[iv]).mean())
        if best is None or v > best[0]: best = (v, lam, w.detach(), b.detach())
    with torch.no_grad(): return X @ best[2] + best[3], best[1]
def fit_mu(base, idx):
    """population attribute weights per language (one shared θ per language)"""
    th = torch.zeros(len(langs), J, requires_grad=True); ii = torch.tensor(idx); opt = torch.optim.LBFGS([th], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); loss = nll(base[ii] + (th[Lt[ii]] * A[ii]).sum(1), YB[ii]).sum() + 1e-3 * (th ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return th.detach()
def fit_sap(base, idx, MU, prec):
    d = torch.zeros(NR, J, requires_grad=True); ii = torch.tensor(idx); opt = torch.optim.LBFGS([d], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = MU + d; loss = nll(base[ii] + (th[Rt[ii]] * A[ii]).sum(1), YB[ii]).sum() + 0.5 * (prec * d ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return (MU + d).detach()
def em(base, idx, MU, iso=False, nit=15):
    s2 = np.full(J, 0.1); us_ = np.unique(R[idx]); Ri = R[idx]
    for _ in range(nit):
        th = fit_sap(base, idx, MU, torch.tensor(1.0 / s2))
        with torch.no_grad():
            it_ = torch.tensor(idx); p = torch.sigmoid(base[it_] + (th[Rt[it_]] * A[it_]).sum(1)); vs = p * (1 - p); acc = np.zeros(J)
            for r in us_:
                q = np.where(Ri == r)[0]; a = A[torch.tensor(idx[q])]; C = np.linalg.inv(((a * vs[q][:, None]).T @ a).numpy() + np.diag(1.0 / s2)); acc += (th[r] - MU[r]).numpy() ** 2 + np.diag(C)
        s2 = np.maximum(acc / len(us_), 1e-6); s2 = np.full(J, max(float(s2.mean()), 1e-6)) if iso else s2
    return s2
def fit_lr(base, idx, MU, Wm, zprec, lamW=None):
    z = torch.zeros(NR, 2, requires_grad=True); ii = torch.tensor(idx); Wv = Wm.clone().requires_grad_(lamW is not None); prm = [z] + ([Wv] if lamW is not None else [])
    opt = torch.optim.LBFGS(prm, lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = MU + z @ Wv.T; loss = nll(base[ii] + (th[Rt[ii]] * A[ii]).sum(1), YB[ii]).sum() + 0.5 * zprec * (z ** 2).sum() + ((lamW or 0.0) * (Wv ** 2).sum()); loss.backward(); return loss
    opt.step(cl); return (MU + z @ Wv.T).detach(), Wv.detach()
def scores(base, idx, th):
    with torch.no_grad():
        it_ = torch.tensor(idx); lg = base[it_] + (th[Rt[it_]] * A[it_]).sum(1); y = YB[it_]; return ((lg > 0).double() == y).double().numpy(), -nll(lg, y).numpy()
def events_of(rows):
    by = collections.defaultdict(list)
    for j in rows: by[(R[j], EVT[j])].append(j)
    per = collections.defaultdict(list)
    for (r, e), js in by.items(): per[r].append(js)
    return per
def sample_ad(per_pool, users, rng):
    ad = []; keep = []
    for r in users:
        evs = per_pool.get(r, [])
        if len(evs) < KEV: continue
        keep.append(r); ad.extend(j for e in rng.choice(len(evs), KEV, replace=False) for j in evs[e])
    return np.array(ad, int), keep
recs = []; info = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    # ---- selection on pseudo-new training users (20 %): everything refitted without them
    trr = np.unique(R[idx_all]); ps = set(np.random.RandomState(3 + f).choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R, list(ps))
    a_tr, a_va = idx_tr[~isp[idx_tr]], idx_va[~isp[idx_va]]; a_all = np.concatenate([a_tr, a_va]); base_s, _ = fit_base(a_tr, a_va); mus = fit_mu(base_s, a_all); MUs = mus[torch.tensor(ulang)]
    per_ps = events_of(idx_all[isp[idx_all]]); rng = np.random.RandomState(40 + f); ad_ps, keep_ps = [], []
    for r, evs in per_ps.items():
        if len(evs) < KEV + 1: continue
        o = rng.permutation(len(evs)); keep_ps.append(r); ad_ps.append([j for e in o[:KEV] for j in evs[e]]); ad_ps[-1] = (ad_ps[-1], [j for e in o[KEV:] for j in evs[e]])
    adp = np.array([j for a_, _ in ad_ps for j in a_], int); scp = np.array([j for _, s_ in ad_ps for j in s_], int)
    s2s = em(base_s, a_all, MUs); ll_none = scores(base_s, scp, MUs)[1].mean(); ll_sap = scores(base_s, scp, fit_sap(base_s, adp, MUs, torch.tensor(1.0 / s2s)))[1].mean()
    sap_on = bool(ll_sap > ll_none); best_lr = (ll_none, 1.0, 0.0)
    W0 = torch.randn(J, 2, generator=torch.Generator().manual_seed(f)) * 0.01
    for lw in (1.0, 10.0, 100.0):
        _, Wf = fit_lr(base_s, a_all, MUs, W0, 1.0, lamW=lw)
        for c in (0.1, 1.0, 10.0):
            v = scores(base_s, scp, fit_lr(base_s, adp, MUs, Wf, 1.0 / c)[0])[1].mean()
            if v > best_lr[0]: best_lr = (v, lw, c)
    info.append({"fold": f, "pseudo_users": len(keep_ps), "sap_on": sap_on, "ll_none": float(ll_none), "ll_sap": float(ll_sap), "lr_sel": {"ll": float(best_lr[0]), "lamW": best_lr[1], "c": best_lr[2]}})
    print(f"fold {f}: pseudo-new {len(keep_ps)} users; SAP on {sap_on}; ATTR-LR-bin selected {info[-1]['lr_sel']}", flush=True)
    # ---- final fits on all training users
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; s2 = em(base, idx_all, MU); s2i = em(base, idx_all, MU, iso=True)
    if best_lr[2] > 0: _, Wf = fit_lr(base, idx_all, MU, W0, 1.0, lamW=best_lr[1])
    info[-1].update({"lambda": lam, "mu": mu.numpy().tolist(), "sigma2": s2.tolist(), "sigma2_iso": float(s2i[0])})
    print(f"fold {f}: σ² top " + ", ".join(f"{NAMES[j]} {s2[j]:.4f}" for j in np.argsort(-s2)[:6]), flush=True)
    per_pool = events_of(pool); test_users = [r for r in np.unique(R[idx_te])]
    for dr in range(5):
        ad, keep = sample_ad(per_pool, test_users, np.random.RandomState(10_000 * f + dr)); te = idx_te[np.isin(R[idx_te], keep)]
        th = {"pop": MU, "sap": fit_sap(base, ad, MU, torch.tensor(1.0 / s2)) if sap_on else MU, "sap_forced": fit_sap(base, ad, MU, torch.tensor(1.0 / s2)),
              "iso": fit_sap(base, ad, MU, torch.tensor(1.0 / s2i)), "lr": fit_lr(base, ad, MU, Wf, 1.0 / best_lr[2])[0] if best_lr[2] > 0 else MU}
        sc = {m_: scores(base, te, t_) for m_, t_ in th.items()}
        for r in keep:
            sel = R[te] == r
            recs.append({"fold": f, "draw": dr, "rater": int(r), "lang": langs[ulang[r]], "n": int(sel.sum()), **{f"{m_}_acc": float(sc[m_][0][sel].sum()) for m_ in sc}, **{f"{m_}_ll": float(sc[m_][1][sel].sum()) for m_ in sc}})
out = {"info": info}
def boot(key_a, key_b, mt, flt=None):
    by = collections.defaultdict(list)
    for x in recs:
        if flt is None or x["lang"] == flt: by[(x["fold"], x["rater"])].append(x)
    q = list(by); wt = np.array([np.mean([x["n"] for x in by[z]]) for z in q]); d = np.array([np.mean([x[f"{key_a}_{mt}"] - x[f"{key_b}_{mt}"] for x in by[z]]) for z in q]); rng = np.random.RandomState(17)
    bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; return [100 * d.sum() / wt.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), len(q)]
for mt in ("acc", "ll"):
    for a_, b_ in (("sap", "pop"), ("sap_forced", "pop"), ("iso", "pop"), ("lr", "pop"), ("sap", "lr")): out[f"{a_}-{b_}_{mt}"] = boot(a_, b_, mt)
for l_ in langs: out[f"sap-pop_acc_{l_}"] = boot("sap", "pop", "acc", l_)
out["rule"] = bool(out["sap-pop_acc"][1] > 1.0 and out["sap-lr_acc"][1] > 0.0)
json.dump(out, open(f"{HERE}/results/stage9_sapca.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage9_sapca_records.json", "w"))
print(json.dumps({k_: v for k_, v in out.items() if k_ != "info"}), flush=True)
