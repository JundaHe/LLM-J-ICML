"""Stage 9 Am. 5 (PROTOCOL_STAGE9.md): SAP on native binary choices. `sap_bin.py prism_pairs|ca_pairs`.
Base: ridge logistic regression of the choice on the PCA-256 difference x_B − x_A (vpl_pal.py features); content term θ_uᵀa_i on the logit (a_i: attr_feats.py, 24 attribute
differences); θ_u ~ N(μ, diag σ²), μ shared, σ² by Laplace-EM on training users; new users adapted on k pairs; own − μ and own − other in choice accuracy and LL."""
import os, sys, json, collections, numpy as np, pandas as pd, torch, torch.nn.functional as Fn
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
from attr_feats import attr_G, NAMES
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
panel = sys.argv[1]; PAN = data_panels.load(panel); n = len(PAN["item_ids"]); ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters); R = np.array([rid[row[0]] for row in ev])
gm = PAN["rater_group"]; glev = sorted({gm.get(r, "NA") for r in raters}); GRP = np.array([glev.index(gm.get(r, "NA")) for r in raters])   # folds exactly as vpl_pal.py
Gp = np.asarray(PAN["groups"]); rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}; va_item = np.array([vf[g_] for g_ in Gp])
YB = torch.tensor(np.asarray(PAN["yb"]).astype(float))
if panel == "prism_pairs":
    u = pd.read_json(f"{data_panels.PRISM_DIR}/utterances.jsonl", lines=True); txt = dict(zip(u.utterance_id.astype(str), u.model_response.astype(str)))
    TA, TB = [txt[str(x)] for x in PAN["utt_A"]], [txt[str(x)] for x in PAN["utt_B"]]
else: TA, TB = list(PAN["resp_A"]), list(PAN["resp_B"])
A = torch.tensor(attr_G(TA, TB, PAN["texts"])); J = A.shape[1]
Fz = np.load(f"{P2}/features/{panel}/pairs_Qwen2.5-7B-Instruct.npz"); assert np.array_equal(Fz["item_ids"], np.asarray(PAN["item_ids"]).astype(str))
EA, EB = Fz["E_A"].astype(np.float32), Fz["E_B"].astype(np.float32); allE = np.concatenate([EA, EB, Fz["E_P"].astype(np.float32)]); mu0 = allE.mean(0)
_, _, Vt = np.linalg.svd(allE[::3] - mu0, full_matrices=False); W = Vt[:256].T; del allE                      # vpl_pal.py --pca 256
XA, XB = (EA - mu0) @ W, (EB - mu0) @ W; sd = np.concatenate([XA, XB]).std(0) + 1e-6; X = torch.tensor((XB - XA) / sd, dtype=torch.float64); Rt = torch.tensor(R)
def nll(logit, y): return -(y * Fn.logsigmoid(logit) + (1 - y) * Fn.logsigmoid(-logit))
def fit(base, idx, mu, prec, shared=False):
    d = torch.zeros(1 if shared else NR, J, requires_grad=True); ii = torch.tensor(idx); opt = torch.optim.LBFGS([d], lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); th = mu + d; c = (A[ii] @ th[0]) if shared else (th[Rt[ii]] * A[ii]).sum(1); loss = nll(base[ii] + c, YB[ii]).sum() + 0.5 * (prec * d ** 2).sum(); loss.backward(); return loss
    opt.step(cl); th = (mu + d).detach(); return th.expand(NR, -1).clone() if shared else th
def logit_of(base, idx, th): ii = torch.tensor(idx); return base[ii] + (th[Rt[ii]] * A[ii]).sum(1)
KS = (5, 20, 50) if panel == "ca_pairs" else (5, 20); recs = []; screen = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    best = None
    for lam in (1.0, 10.0, 100.0, 1000.0):
        w = torch.zeros(X.shape[1], requires_grad=True); b = torch.zeros(1, requires_grad=True); ii = torch.tensor(idx_tr); opt = torch.optim.LBFGS([w, b], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
        def cl():
            opt.zero_grad(); loss = nll(X[ii] @ w + b, YB[ii]).sum() + lam * (w ** 2).sum(); loss.backward(); return loss
        opt.step(cl)
        with torch.no_grad(): iv = torch.tensor(idx_va); v = -float(nll(X[iv] @ w + b, YB[iv]).mean())
        if best is None or v > best[0]: best = (v, lam, w.detach().clone(), b.detach().clone())
    _, lam, w, b = best; idx_all = np.concatenate([idx_tr, idx_va])
    with torch.no_grad(): base = X @ w + b
    zero = torch.zeros(J); mu = fit(base, idx_all, zero, torch.zeros(J), shared=True)[0]
    s2 = np.full(J, 0.1); trr = np.unique(R[idx_all])
    for it in range(15):
        th = fit(base, idx_all, mu, torch.tensor(1.0 / s2))
        with torch.no_grad():
            p = torch.sigmoid(logit_of(base, idx_all, th)); vs = p * (1 - p); acc = np.zeros(J); Ra = R[idx_all]
            for r in trr:
                q = np.where(Ra == r)[0]; a = A[torch.tensor(idx_all[q])]; C = np.linalg.inv(((a * vs[q][:, None]).T @ a).numpy() + np.diag(1.0 / s2)); acc += (th[r] - mu).numpy() ** 2 + np.diag(C)
        s2 = np.maximum(acc / len(trr), 1e-6)
    screen.append({"fold": f, "lambda": lam, "mu": mu.numpy().tolist(), "sigma2": s2.tolist()})
    print(f"{panel} fold {f}: λ {lam}; σ² " + ", ".join(f"{NAMES[j]} {s2[j]:.4f}" for j in np.argsort(-s2)[:6]), flush=True)
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
            th = fit(base, ad, mu, prec); thp = th.clone(); thp[tgt] = th[src]; th0 = mu.expand(NR, -1).clone()
            with torch.no_grad():
                lg = {"own": logit_of(base, te, th), "other": logit_of(base, te, thp), "pop": logit_of(base, te, th0)}; yt = YB[torch.tensor(te)]
                accs = {w_: ((v > 0).double() == yt).double().numpy() for w_, v in lg.items()}; lls = {w_: -nll(v, yt).numpy() for w_, v in lg.items()}
            for r in keep:
                sel = R[te] == r
                recs.append({"fold": f, "k": k, "draw": dr, "rater": int(r), "n": int(sel.sum()), **{f"{w_}_acc": float(accs[w_][sel].sum()) for w_ in lg}, **{f"{w_}_ll": float(lls[w_][sel].sum()) for w_ in lg},
                             **({"lang": str(PAN["lang"][te[sel][0]])} if "lang" in PAN else {})})
out = {"panel": panel, "screen": screen}
for k in KS:
    by = collections.defaultdict(list)
    for x in recs:
        if x["k"] == k: by[(x["fold"], x["rater"])].append(x)
    q = list(by); wt = np.array([np.mean([x["n"] for x in by[z]]) for z in q])
    for mt in ("acc", "ll"):
        for ref_ in ("other", "pop"):
            d = np.array([np.mean([x[f"own_{mt}"] - x[f"{ref_}_{mt}"] for x in by[z]]) for z in q]); rng = np.random.RandomState(17)
            bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; out[f"k{k}_{mt}_own-{ref_}"] = [100 * d.sum() / wt.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), len(q)]
r20 = out.get("k20_acc_own-pop"); out["rule_content_personalisation"] = bool(r20 and r20[1] > 1.0)
json.dump(out, open(f"{HERE}/results/stage9_sapbin_{panel}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage9_sapbin_{panel}_records.json", "w"))
print(panel, json.dumps({k_: v for k_, v in out.items() if k_ != "screen"}), flush=True)
