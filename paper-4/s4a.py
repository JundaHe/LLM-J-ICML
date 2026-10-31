"""Stage 4 S4-A (PROTOCOL_STAGE4.md): ceiling on trade-off personalisation. Ordinal logistic for the overall level from the annotator's own aspect levels
(helpful, truthful, harmless; centred values and absolute values). P = pooled trade-off β + rater cut-points; R = rater trade-off β + δ_r + rater cut-points.
Rater parameters fitted on k of the rater's training-item annotations (stage-2a draws), evaluated on held-out items with the rater's own aspect labels as inputs."""
import os, sys, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.join(os.path.dirname(HERE), "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels
torch.set_default_dtype(torch.float64); torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4"))); K = 5; DRAWS = 5; KS = (20, 50, "all")
LV = {"A-is-clearly-better": 0, "A-is-slightly-better": 1, "Tie": 2, "B-is-slightly-better": 3, "B-is-clearly-better": 4}
rows = [json.loads(l) for l in open(data_panels.MULTIPREF)]
ann = [(i, p, a) for i, r in enumerate(rows) for p, a in enumerate(r["normal_worker_annotations"] + r["expert_worker_annotations"])]
raters = sorted({a["evaluator"] for _, _, a in ann}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.array([i for i, _, _ in ann]); R = np.array([rid[a["evaluator"]] for _, _, a in ann]); POS = np.array([p for _, p, _ in ann])
Y = np.array([LV[a["overall_pref"]] for _, _, a in ann]); Hs = np.array([[LV[a[f"{c}_pref"]] - 2 for c in ("helpful", "truthful", "harmless")] for _, _, a in ann], float)
X = torch.tensor(np.c_[Hs, np.abs(Hs)]); Yt = torch.tensor(Y); Rt = torch.tensor(R)
sg = np.sign(Hs); CONF = (sg > 0).any(1) & (sg < 0).any(1)
# ---- folds exactly as factorised_rm.py
GRP = np.zeros(NR, int)
for j in range(len(R)): GRP[R[j]] = int(POS[j] >= 2)
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
PAN = data_panels.load("multipref_overall"); assert list(PAN["item_ids"]) == [r["comparison_id"] for r in rows]
Gp = np.asarray(PAN["groups"]); ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
def logp(beta, u, idx, dB=None, dU=None):
    rr = Rt[idx]; b = beta[None, :] + (dB[rr] if dB is not None else 0); uu = u[None, :] + (dU[rr] if dU is not None else 0)
    c = torch.cat([uu[:, :1], uu[:, :1] + torch.cumsum(torch.nn.functional.softplus(uu[:, 1:]), 1)], 1); s = (X[idx] * b).sum(1)
    cdf = torch.sigmoid(c - s[:, None]); cdf = torch.cat([torch.zeros(len(idx), 1), cdf, torch.ones(len(idx), 1)], 1); return torch.log((cdf[:, 1:] - cdf[:, :-1]).clamp_min(1e-12))
def fit(params, idx, pen, base=None):
    ii = torch.tensor(idx); [p.requires_grad_(True) for p in params.values()]; opt = torch.optim.LBFGS(list(params.values()), lr=0.5, max_iter=300, line_search_fn="strong_wolfe")
    def cl():
        opt.zero_grad(); b = params["beta"] if "beta" in params else base[0]; u = params["u"] if "u" in params else base[1]
        lp = logp(b, u, ii, params.get("dB"), params.get("dU")); loss = -lp[torch.arange(len(idx)), Yt[ii]].sum() + sum(pen[k] * (params[k] ** 2).sum() for k in pen); loss.backward(); return loss
    opt.step(cl); return {k: v.detach() for k, v in params.items()}
def metrics(lp, idx):
    ey = (lp.exp() * torch.arange(K)).sum(1).numpy(); y = Y[idx]; d = np.where(y == 2, np.nan, (np.sign(ey - 2) == np.sign(y - 2)).astype(float)); return lp[torch.arange(len(idx)), torch.tensor(y)].numpy(), d
def adapt(base, idx, variant, lc, ld):
    prm = {"dU": torch.zeros(NR, 4)} | ({"dB": torch.zeros(NR, 6)} if variant == "R" else {}); pen = {"dU": lc} | ({"dB": ld} if variant == "R" else {})
    return fit(prm, idx, pen, base)
def split_ll(base, idx, variant, lc, ld, seed):                         # penalty selection: rater-wise split of the training raters' training items
    rng = np.random.RandomState(seed); half = np.zeros(len(idx), bool)
    for r in np.unique(R[idx]):
        pos = np.where(R[idx] == r)[0]; half[rng.permutation(pos)[: len(pos) // 2]] = True
    tot = 0.0
    for a_m in (half, ~half):
        p = adapt(base, idx[a_m], variant, lc, ld); lp = logp(base[0], base[1], torch.tensor(idx[~a_m]), p.get("dB"), p["dU"]); tot += float(lp[torch.arange((~a_m).sum()), Yt[torch.tensor(idx[~a_m])]].sum())
    return tot / len(idx)
recs = []; sel = {}
for f in range(5):
    test_r = rfold == f; tr_item = ifold[I] != f; idx_tr = np.where(~test_r[R] & tr_item)[0]; pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base = fit({"beta": torch.zeros(6), "u": torch.tensor([-1.0, 0.0, 0.0, 0.0]), "dU": torch.zeros(NR, 4)}, idx_tr, {"dU": 1.0}); base = (base["beta"], base["u"])
    lc = max(((split_ll(base, idx_tr, "P", lc_, 0, 70 + f), lc_) for lc_ in (0.3, 1.0, 3.0, 10.0)))[1]
    ld = max(((split_ll(base, idx_tr, "R", lc, ld_, 80 + f), ld_) for ld_ in (0.3, 1.0, 3.0, 10.0, 30.0, 100.0)))[1]; sel[f] = (lc, ld)
    print(f"fold {f}: β = {np.round(base[0].numpy(), 2)}, λ_c {lc}, λ_δ {ld}", flush=True)
    test_raters = np.unique(R[idx_te])
    for k in KS:
        for dr in (range(DRAWS) if k != "all" else [0]):
            if k == "all": ad = pool[np.isin(R[pool], test_raters)]; keep = list(np.unique(R[ad]))
            else:
                rng = np.random.RandomState(10_000 * f + 100 * k + dr); ad = []; keep = []
                for r in test_raters:
                    pr = pool[R[pool] == r]
                    if len(pr) < k: continue
                    keep.append(r); ad.extend(rng.choice(pr, k, replace=False))
                ad = np.array(ad, int)
            te = idx_te[np.isin(R[idx_te], keep)]; tt = torch.tensor(te); out = {}
            for v in ("P", "R"):
                p = adapt(base, ad, v, lc, ld); out[v] = metrics(logp(base[0], base[1], tt, p.get("dB"), p["dU"]), te)
            for r in keep:
                m = R[te] == r
                recs.append({"fold": f, "k": str(k), "draw": dr, "rater": int(r), "n": int(m.sum()), "n_dir": int(np.isfinite(out["P"][1][m]).sum()), "n_conf_dir": int((np.isfinite(out["P"][1]) & CONF[te])[m].sum()),
                             **{f"{v}_{mt}": float(np.nansum(out[v][j][m])) for v in ("P", "R") for j, mt in ((0, "ll"), (1, "dir"))},
                             **{f"{v}_dirc": float(np.nansum(np.where(CONF[te], out[v][1], np.nan)[m])) for v in ("P", "R")}})
    # in-sample upper bound: rater parameters fitted on the test items themselves
    te = idx_te; tt = torch.tensor(te); ins = {}
    for v in ("P", "R"):
        p = adapt(base, te, v, lc, ld); ins[v] = metrics(logp(base[0], base[1], tt, p.get("dB"), p["dU"]), te)
    for r in test_raters:
        m = R[te] == r
        recs.append({"fold": f, "k": "insample", "draw": 0, "rater": int(r), "n": int(m.sum()), "n_dir": int(np.isfinite(ins["P"][1][m]).sum()), "n_conf_dir": int((np.isfinite(ins["P"][1]) & CONF[te])[m].sum()),
                     **{f"{v}_{mt}": float(np.nansum(ins[v][j][m])) for v in ("P", "R") for j, mt in ((0, "ll"), (1, "dir"))},
                     **{f"{v}_dirc": float(np.nansum(np.where(CONF[te], ins[v][1], np.nan)[m])) for v in ("P", "R")}})
    print(f"fold {f} done", flush=True)
rng = np.random.RandomState(21); L = ["# Stage 4 S4-A — ceiling on trade-off personalisation (MultiPref; rater's own aspect labels as inputs; rater cut-points in both models)", "",
     "| k | R − P direction acc. (points) | R − P LL per rating | R − P direction on conflict items (points) | conflict share of test items | raters |", "|---|---|---|---|---|---|"]; res = {}
def boot(d, w):
    bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]; return [float(d.sum() / w.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
for k in ("20", "50", "all", "insample"):
    by = collections.defaultdict(list)
    for x in recs:
        if x["k"] == k: by[(x["fold"], x["rater"])].append(x)
    q = list(by); mean = lambda z, key: np.mean([x[key] for x in by[z]])
    dd = boot(np.array([mean(z, "R_dir") - mean(z, "P_dir") for z in q]), np.array([mean(z, "n_dir") for z in q]))
    ll = boot(np.array([mean(z, "R_ll") - mean(z, "P_ll") for z in q]), np.array([mean(z, "n") for z in q]))
    qc = [z for z in q if mean(z, "n_conf_dir") > 0]; dc = boot(np.array([mean(z, "R_dirc") - mean(z, "P_dirc") for z in qc]), np.array([mean(z, "n_conf_dir") for z in qc]))
    share = sum(mean(z, "n_conf_dir") for z in q) / sum(mean(z, "n_dir") for z in q); res[k] = {"dir": dd, "ll": ll, "dir_conflict": dc, "conflict_share": share, "n": len(q)}
    L.append(f"| {k} | {100*dd[0]:+.2f} [{100*dd[1]:+.2f}, {100*dd[2]:+.2f}] | {ll[0]:+.4f} [{ll[1]:+.4f}, {ll[2]:+.4f}] | {100*dc[0]:+.2f} [{100*dc[1]:+.2f}, {100*dc[2]:+.2f}] | {100*share:.1f} % | {len(q)} |")
rule = res["all"]["dir"][1] > 0.005; L += ["", f"Penalties per fold (λ_c, λ_δ): {sel}.", f"**Decision rule (S4-B runs only if the k = all lower bound > +0.5 points): {'PASS — run S4-B' if rule else 'FAIL — S4-B not run'}.**"]
res["rule_pass"] = bool(rule); json.dump({"summary": res, "records": recs}, open(f"{HERE}/results/stage4_s4a.json", "w")); open(f"{HERE}/results/stage4_s4a.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
