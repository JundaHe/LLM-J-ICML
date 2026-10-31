"""Stage 5 (PROTOCOL_STAGE5.md). `s5.py ref <tag>`: S5-1 well-specified reference learner on synthetic panel multipref_synth_<tag> (oracle and estimated base);
`s5.py stats`: S5-3 learner-free statistics of the real panel and every synthetic panel."""
import os, sys, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2); sys.argv += [""] * 3
import data_panels
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); K = 5; STEP = torch.tensor([-2., -1., 0., 1., 2.]); SYM = [0, 1, 2, 1, 0]
base = data_panels.load("multipref_overall"); Hreal = base["H"]; n, m = Hreal.shape; ev = base["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
for j in range(len(R)): GRP[R[j]] = int(POS[j] >= 2)
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
Gp = np.asarray(base["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
def panel_H(tag): return Hreal if tag in ("real", "real_aspect", "real_none") else np.load(f"{HERE}/results/synth/multipref_synth_{tag}.npz")["H"]

if sys.argv[1] == "stats":                                                # ---------------- S5-3
    import krippendorff
    def stats(H, items):
        Hs = H[items]; d = np.sign(Hs - 2); agree = [];
        for a in range(m):
            for b in range(a + 1, m):
                ok = (d[:, a] != 0) & (d[:, b] != 0); agree.append(((d[:, a] == d[:, b]) & ok).sum() / max(1, ok.sum()) * ok.sum())
        pairs = sum(((d[:, a] != 0) & (d[:, b] != 0)).sum() for a in range(m) for b in range(a + 1, m)); agr = sum(agree) / pairs
        wv = Hs.var(1).mean(); tv = Hs.var(); return agr, wv / tv
    def alpha(H):
        M = np.full((NR, n), np.nan)
        for j in range(len(R)): M[R[j], I[j]] = H.reshape(-1)[j]
        return krippendorff.alpha(reliability_data=M, level_of_measurement="ordinal")
    rng = np.random.RandomState(31); L = ["# Stage 5 S5-3 — learner-free statistics, real vs synthetic panels", "", "| panel | direction agreement of rater pairs | within-item variance share | Krippendorff α (ordinal) |", "|---|---|---|---|"]; out = {}
    real = stats(Hreal, np.arange(n)); bs = np.array([stats(Hreal, rng.randint(0, n, n)) for _ in range(400)]); lo, hi = np.percentile(bs, 2.5, 0), np.percentile(bs, 97.5, 0)
    a_real = alpha(Hreal); out["real"] = {"agree": real[0], "within": real[1], "alpha": a_real, "agree_ci": [lo[0], hi[0]], "within_ci": [lo[1], hi[1]]}
    L.append(f"| real | {real[0]:.4f} [{lo[0]:.4f}, {hi[0]:.4f}] | {real[1]:.4f} [{lo[1]:.4f}, {hi[1]:.4f}] | {a_real:.4f} |")
    import glob as _g
    for tag in [t for t in ("t0", "t2", "t5", "t10", "t20", "v2t0", "v2t5", "v2t10") if os.path.exists(f"{HERE}/results/synth/multipref_synth_{t}.npz")]:
        H = panel_H(tag); st = stats(H, np.arange(n)); al = alpha(H); inc = not (lo[0] <= st[0] <= hi[0]) or not (lo[1] <= st[1] <= hi[1])
        out[tag] = {"agree": st[0], "within": st[1], "alpha": al, "inconsistent_ci": bool(inc)}
        L.append(f"| synthetic {tag} | {st[0]:.4f} | {st[1]:.4f} | {al:.4f} |" + (" outside real 95 % (i or iii)" if inc else ""))
    L += ["", "α has no item-bootstrap interval here (one value per panel); (i) and (iii) carry the inconsistency rule of the protocol, α is reported for comparison."]
    json.dump(out, open(f"{HERE}/results/stage5_s53.json", "w"), indent=1); open(f"{HERE}/results/stage5_s53.md", "w").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit()

# ---------------- S5-1 reference learner
tag = sys.argv[2]; H = panel_H(tag); Y = H.reshape(-1); Yt = torch.tensor(Y); It, Rt = torch.tensor(I), torch.tensor(R)
F_ = np.load(f"{P2}/features/multipref_overall/Qwen2.5-7B-Instruct.npz", allow_pickle=True)
E = F_["E_last"].astype(np.float64); E -= E.mean(0); U, S, _ = np.linalg.svd(E, full_matrices=False); X = U[:, :256] * S[:256]; X /= X.std(0); X = torch.tensor(X)
# generator (identical to make_synth.py, fitted on the REAL labels) and features g
Vg = torch.zeros(256, K, requires_grad=True); bg = torch.zeros(K, requires_grad=True); Bg = torch.zeros(NR, 3, requires_grad=True); Yr = torch.tensor(Hreal.reshape(-1))
opt = torch.optim.LBFGS([Vg, bg, Bg], lr=0.5, max_iter=500, line_search_fn="strong_wolfe")
def clg():
    opt.zero_grad(); lp = torch.log_softmax(X[It] @ Vg + bg + Bg[Rt][:, SYM], 1); loss = -lp[torch.arange(len(Yr)), Yr].sum() + 300.0 * (Vg ** 2).sum() + 2.0 * (Bg ** 2).sum(); loss.backward(); return loss
opt.step(clg)
with torch.no_grad(): LPG = torch.log_softmax(X[It] @ Vg + bg + Bg[Rt][:, SYM], 1)
raw = [json.loads(l) for l in open(data_panels.MULTIPREF)]
g1 = np.log(np.array([max(1, len(str(r["completion_b"]))) for r in raw]) / np.array([max(1, len(str(r["completion_a"]))) for r in raw]))
Fp = np.load(f"{P2}/features/multipref_overall/pairs_Qwen2.5-7B-Instruct.npz"); Dd = (Fp["E_B"] - Fp["E_A"]).astype(np.float64); Dd -= Dd.mean(0); U2, S2, _ = np.linalg.svd(Dd, full_matrices=False); Z = U2[:, :256] * S2[:256]; Z /= Z.std(0)
ym = Hreal.mean(1); w = np.linalg.solve(Z.T @ Z + 1000.0 * np.eye(256), Z.T @ (ym - ym.mean())); w /= np.linalg.norm(w); u = np.random.RandomState(0).randn(256); u -= (u @ w) * w; u /= np.linalg.norm(u); g2 = Z @ u
G = torch.tensor(np.stack([(g1 - g1.mean()) / g1.std(), (g2 - g2.mean()) / g2.std()], 1)); GR = G[It]          # per-rating content features
if tag == "real_none": GR = torch.zeros(len(Y), 1, dtype=torch.float64)    # Stage 5 Am. 2: style offsets only
if tag == "real_aspect":                                                  # Stage 5 Am. 1 (A): leave-rater-out consensus aspect differences, real labels
    LVa = {"A-is-clearly-better": -2, "A-is-slightly-better": -1, "Tie": 0, "B-is-slightly-better": 1, "B-is-clearly-better": 2}
    A = np.array([[LVa[a[f"{c}_pref"]] for c in ("helpful", "truthful", "harmless")] for r_ in raw for a in r_["normal_worker_annotations"] + r_["expert_worker_annotations"]], float).reshape(n, m, 3)
    loo = (A.sum(1, keepdims=True) - A) / (m - 1); g = loo.reshape(-1, 3); g = (g - g.mean(0)) / g.std(0); GR = torch.tensor(g)
def fit_rater(lpb, idx, keys, sig2, lam_s=2.0):
    """MAP of rater params on rows idx: th (NR,2) with prior N(0, sig2 I); Bs (NR,3) ridge lam_s if 'Bs' in keys"""
    th = torch.zeros(NR, GR.shape[1], requires_grad=True); Bs = torch.zeros(NR, 3, requires_grad="Bs" in keys); ii = torch.tensor(idx); prm = [th] + ([Bs] if "Bs" in keys else [])
    opt = torch.optim.LBFGS(prm, lr=0.5, max_iter=200, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); c = (th[Rt[ii]] * GR[ii]).sum(1); lp = torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
        loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + 0.5 / sig2 * (th ** 2).sum() + lam_s * (Bs ** 2).sum(); loss.backward(); return loss
    opt.step(cl); return th.detach(), Bs.detach()
def predict(lpb, idx, th, Bs):
    ii = torch.tensor(idx); c = (th[Rt[ii]] * GR[ii]).sum(1); return torch.log_softmax(lpb[ii] + Bs[Rt[ii]][:, SYM] + c[:, None] * STEP, 1)
def dirc(lp, idx):
    ey = (lp.exp() * torch.arange(K)).sum(1).numpy(); y = Y[idx]; return np.where(y == 2, np.nan, (np.sign(ey - 2) == np.sign(y - 2)).astype(float))
recs = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold[I] != f; idx_tr = np.where(~test_r[R] & tr_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    V = torch.zeros(256, K, requires_grad=True); b = torch.zeros(K, requires_grad=True); Bt = torch.zeros(NR, 3, requires_grad=True); ii = torch.tensor(idx_tr)   # estimated base: D + DFs on training raters × training items
    opt = torch.optim.LBFGS([V, b, Bt], lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); lp = torch.log_softmax(X[It[ii]] @ V + b + Bt[Rt[ii]][:, SYM], 1); loss = -lp[torch.arange(len(idx_tr)), Yt[ii]].sum() + 300.0 * (V ** 2).sum() + 2.0 * (Bt ** 2).sum(); loss.backward(); return loss
    opt.step(cl)
    with torch.no_grad(): LPE = torch.log_softmax(X[It] @ V + b, 1)                                    # rater offsets re-fitted per rater below
    bases = {"oracle": (LPG, ()), "estimated": (LPE, ("Bs",))} if not (tag in ("real_aspect", "real_none") or tag.startswith("v2")) else {"estimated": (LPE, ("Bs",))}; sig = {}   # v2 panels: the v1 generator is not their oracle
    for bn, (lpb, keys) in bases.items():                                   # empirical-Bayes σ² on the training raters (rater-wise half split of their training items)
        best = None; rng_s = np.random.RandomState(90 + f); half = np.zeros(len(idx_tr), bool)
        for r in np.unique(R[idx_tr]):
            pos = np.where(R[idx_tr] == r)[0]; half[rng_s.permutation(pos)[: len(pos) // 2]] = True
        for s2 in (0.001, 0.01, 0.03, 0.1, 0.3, 1.0):
            th, Bs = fit_rater(lpb, idx_tr[half], keys, s2); lp = predict(lpb, idx_tr[~half], th, Bs); v = float(lp[torch.arange((~half).sum()), Yt[torch.tensor(idx_tr[~half])]].mean())
            if best is None or v > best[0]: best = (v, s2)
        sig[bn] = best[1]
    print(f"{tag} fold {f}: σ² {sig}", flush=True)
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
            res = {}
            for bn, (lpb, keys) in bases.items():
                th, Bs = fit_rater(lpb, ad, keys, sig[bn]); thp, Bsp = th.clone(), Bs.clone(); thp[tgt] = th[src]; Bsp[tgt] = Bs[src]
                res[bn] = (dirc(predict(lpb, te, th, Bs), te), dirc(predict(lpb, te, thp, Bsp), te))
            for r in keep:
                sel = R[te] == r
                recs.append({"fold": f, "k": k, "draw": dr, "rater": int(r), **{f"{bn}_{w_}": float(np.nansum(res[bn][j][sel])) for bn in bases for j, w_ in ((0, "own"), (1, "other"))}, "n_dir": int(np.isfinite(res["estimated"][0][sel]).sum())})
rng = np.random.RandomState(17); out = {}
for k in (20, 50):
    for bn in [b_ for b_ in ("oracle", "estimated") if f"{b_}_own" in recs[0]]:
        by = collections.defaultdict(list)
        for x in recs:
            if x["k"] == k: by[(x["fold"], x["rater"])].append(x)
        q = list(by); d = np.array([np.mean([x[f"{bn}_own"] - x[f"{bn}_other"] for x in by[z]]) for z in q]); wt = np.array([np.mean([x["n_dir"] for x in by[z]]) for z in q])
        bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; out[f"{bn}_k{k}"] = [100 * d.sum() / wt.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), len(q)]
import glob as _g; meta = {}
for mf in [f"{HERE}/results/synth/synth_meta.json"] + sorted(_g.glob(f"{HERE}/results/synth/synth_meta_s*.json")): meta.update(json.load(open(mf)))
meta = meta.get(tag, {}); out["oracle_gain"] = 100 * meta.get("oracle_gain_realised", float("nan"))
json.dump(out, open(f"{HERE}/results/stage5_ref_{tag}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage5_ref_{tag}_records.json", "w")); print(tag, json.dumps(out))
