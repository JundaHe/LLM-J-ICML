"""Stage 11 S11-3 (PROTOCOL_STAGE11.md Am. 2, exploratory): transfer-trained empirical-Bayes adaptation on the frozen CA split of Stage 9 Am. 6.
Per fold, the transferable covariance Ĉ is estimated on training users (cross-half, disjoint prompt groups); a new user's deviation is
θ̂_u − μ = Ĉ (I + I_u Ĉ)⁻¹ s_u from k = 20 support events. Also a learnability ceiling with labels simulated from δ_u ~ N(0, Ĉ)."""
import os, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])  # sap_ca.py's data, folds, base/μ fits and samplers (its evaluation loop is not run)
PRIM = [NAMES.index("length"), NAMES.index("paragraphs"), NAMES.index("list/heading lines")]
SEC7 = [NAMES.index(x) for x in ("length", "list/heading lines", "bold/italic", "digits", "paragraphs", "type-token ratio", "headings")]
An = A.numpy()
def sc_info(lg, js, cols):
    p = 1 / (1 + np.exp(-lg[js])); a = An[np.ix_(js, cols)]; return a.T @ (YB.numpy()[js] - p), (a * (p * (1 - p))[:, None]).T @ a
def est_C(lg, idx, cols, min_ev=10, trim=0.0):
    per = events_of(idx); rng = np.random.RandomState(5); ZA, ZB = [], []
    for u in sorted(per):
        evs = per[u]
        if len(evs) < min_ev: continue
        g_ = np.array([Gp[e[0]] for e in evs]); ug_ = np.unique(g_); side = dict(zip(ug_, rng.permutation(len(ug_)) % 2)); h = np.array([side[x] for x in g_])
        if h.min() == h.max(): continue
        z = []
        for hh in (0, 1):
            js = np.array([j for e, s_ in zip(evs, h) if s_ == hh for j in e]); s, I_ = sc_info(lg, js, cols); z.append(np.linalg.solve(I_ + 1e-3 * np.eye(len(cols)), s))
        ZA.append(z[0]); ZB.append(z[1])
    ZA, ZB = np.array(ZA), np.array(ZB); P = ZA * ZB
    if trim > 0:
        keep = (np.abs(P) <= np.quantile(np.abs(P), 1 - trim, axis=0)).all(1); ZA, ZB = ZA[keep], ZB[keep]
    C = 0.5 * (ZA.T @ ZB + ZB.T @ ZA) / len(ZA); ev_, V_ = np.linalg.eigh(C); return (V_ * np.clip(ev_, 0, None)) @ V_.T, len(ZA), np.diag(C)
def adapt(lg, ad, keep, C, cols, MU):
    th = MU.clone().numpy(); per = collections.defaultdict(list)
    for j in ad: per[R[j]].append(j)
    for u in keep:
        s, I_ = sc_info(lg, np.array(per[u]), cols); th[u, cols] += C @ np.linalg.solve(np.eye(len(cols)) + I_ @ C, s)
    return torch.tensor(th)
AM3 = os.environ.get("S113_AM3") == "1"                                   # Amendment 3: diagnosing the ceiling-vs-realised gap
ZS, ZT = [], []; AM4 = os.environ.get("S113_AM4") == "1"                 # Amendment 4: validated attribute set and prior scale
L1 = [NAMES.index("length")]; GRID = (1.0, 0.5, 0.25, 0.125, 0.0625, 0.0)
old = {(x["fold"], x["draw"], x["rater"]): x for x in json.load(open(f"{HERE}/results/stage9_sapca_records.json"))}
recs, info, ceil = [], [], []; MIS = [0.0, 0]                                   # pop-prediction disagreement with the Stage-9 rerun
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]
    lg_pop = (base + (MU[Rt] * A).sum(1)).numpy()
    C3, nu, d3 = est_C(lg_pop, idx_all, PRIM); C7, _, d7 = est_C(lg_pop, idx_all, SEC7); C7 = np.diag(np.clip(d7, 0, None))
    C3t = est_C(lg_pop, idx_all, PRIM, trim=0.01)[0]; rob = {"min30": est_C(lg_pop, idx_all, PRIM, min_ev=30)[2].tolist(), "trim1": np.diag(C3t).tolist()}
    info.append({"fold": f, "n_train_users": nu, "C3": C3.tolist(), "C3_diag_raw": d3.tolist(), "C7_diag": np.diag(C7).tolist(), "robust": rob})
    print(f"fold {f}: {nu} training users; Ĉ diag " + ", ".join(f"{NAMES[j]} {d3[i]:.3f}" for i, j in enumerate(PRIM)) + f"; robust {json.dumps(rob)}", flush=True)
    if AM4:
        trr = np.unique(R[idx_all]); ps = set(np.random.RandomState(3 + f).choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R, list(ps))
        a_tr, a_va = idx_tr[~isp[idx_tr]], idx_va[~isp[idx_va]]; a_all = np.concatenate([a_tr, a_va]); base_s, _ = fit_base(a_tr, a_va); MUs = fit_mu(base_s, a_all)[torch.tensor(ulang)]
        lg_s = (base_s + (MUs[Rt] * A).sum(1)).numpy(); per_ps = events_of(idx_all[isp[idx_all]]); rng = np.random.RandomState(40 + f); adp, scp, kp = [], [], []
        for r, evs in per_ps.items():
            if len(evs) < KEV + 1: continue
            o = rng.permutation(len(evs)); kp.append(r); adp += [j for e in o[:KEV] for j in evs[e]]; scp += [j for e in o[KEV:] for j in evs[e]]
        adp, scp = np.array(adp, int), np.array(scp, int); val = {}
        for nm, cols in (("len", L1), ("prim3", PRIM)):
            Cs = est_C(lg_s, a_all, cols)[0]
            for c in GRID: val[(nm, c)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, c * Cs, cols, MUs))[1].mean())
        sel = max(val, key=val.get); info[-1]["am4_val"] = {f"{k_[0]}_{k_[1]}": v for k_, v in val.items()}; info[-1]["am4_sel"] = list(sel)
        Csel = sel[1] * (est_C(lg_pop, idx_all, L1)[0] if sel[0] == "len" else C3); cols_sel = L1 if sel[0] == "len" else PRIM
        print(f"fold {f}: AM4 selected {sel} on {len(kp)} pseudo-new users", flush=True)
    per_pool = events_of(pool); test_users = [r for r in np.unique(R[idx_te])]
    for dr in range(5):
        ad, keep = sample_ad(per_pool, test_users, np.random.RandomState(10_000 * f + dr)); te = idx_te[np.isin(R[idx_te], keep)]
        if AM4: th = {"pop": MU, "tr3": adapt(lg_pop, ad, keep, C3, PRIM, MU), "trv": adapt(lg_pop, ad, keep, Csel, cols_sel, MU)}
        elif AM3: th = {"pop": MU, "tr3": adapt(lg_pop, ad, keep, C3, PRIM, MU), "tr3s50": adapt(lg_pop, ad, keep, 0.5 * C3, PRIM, MU), "tr3s25": adapt(lg_pop, ad, keep, 0.25 * C3, PRIM, MU)}
        else: th = {"pop": MU, "tr3": adapt(lg_pop, ad, keep, C3, PRIM, MU), "tr3d": adapt(lg_pop, ad, keep, np.diag(np.diag(C3)), PRIM, MU), "tr7": adapt(lg_pop, ad, keep, C7, SEC7, MU)}
        shift = np.linalg.norm((th["tr3"] - MU).numpy()[:, PRIM], axis=1)
        if AM3 and dr == 0:                                               # 1. support -> test transfer on the evaluated users
            pa = collections.defaultdict(list); pt = collections.defaultdict(list)
            for j in ad: pa[R[j]].append(j)
            for j in te: pt[R[j]].append(j)
            for u in keep:
                z_ = []
                for js in (pa[u], pt[u]): s_, I_ = sc_info(lg_pop, np.array(js), PRIM); z_.append(np.linalg.solve(I_ + 1e-3 * np.eye(3), s_))
                ZS.append(z_[0]); ZT.append(z_[1])
        sc = {m_: scores(base, te, t_) for m_, t_ in th.items()}
        for r in keep:
            sel = R[te] == r; o = old[(f, dr, int(r))]
            recs.append({"fold": f, "draw": dr, "rater": int(r), "lang": langs[ulang[r]], "n": int(sel.sum()), **{f"{m_}_acc": float(sc[m_][0][sel].sum()) for m_ in sc}, **{f"{m_}_ll": float(sc[m_][1][sel].sum()) for m_ in sc},
                         **{f"{m_}_{mt}": o[f"{m_}_{mt}"] for m_ in ("sap", "lr") for mt in ("acc", "ll")}, "shift": float(shift[r])})
            assert o["n"] == recs[-1]["n"], "records do not align with Stage 9 Am. 6"; MIS[0] += abs(o["pop_acc"] - recs[-1]["pop_acc"]); MIS[1] += o["n"]
        if dr == 0 and not AM4:                                           # learnability ceiling on this draw's design
            g = np.random.RandomState(900 + f); ui = {u: i for i, u in enumerate(keep)}; Lc = np.linalg.cholesky(C3 + 1e-9 * np.eye(3))
            for mc, (dist, Cg) in enumerate([("gauss", C3)] * 5 if not AM3 else [(d_, C_) for d_, C_ in (("gauss", C3), ("gauss_trim", C3t), ("t3", C3), ("mix10", C3)) for _ in range(5)]):
                Lc = np.linalg.cholesky(Cg + 1e-9 * np.eye(3)); dl = g.randn(len(keep), 3) @ Lc.T
                if dist == "t3": dl = dl * np.sqrt(1 / 3) / np.sqrt(g.chisquare(3, (len(keep), 1)) / 3)
                if dist == "mix10": dl = dl * np.sqrt(10) * (g.rand(len(keep), 1) < 0.1)
                D_ = np.zeros((NR, 3)); D_[keep] = dl; lgT = lg_pop + (D_[R] * An[:, PRIM]).sum(1); pT = 1 / (1 + np.exp(-lgT))
                ysim = (g.rand(n) < pT).astype(float); Ysave = YB.clone(); YB[:] = torch.tensor(ysim); thE = adapt(lg_pop, ad, keep, Cg, PRIM, MU); YB[:] = Ysave
                lgE = (base + (thE[Rt] * A).sum(1)).numpy(); hit = lambda lg_: np.where(lg_[te] > 0, pT[te], 1 - pT[te]).mean()
                ceil.append({"fold": f, "mc": mc, "dist": dist, "pop": float(hit(lg_pop)), "oracle": float(hit(lgT)), "tr3": float(hit(lgE))})
            print(f"fold {f} ceiling: " + json.dumps({k_: float(np.mean([c[k_] for c in ceil if c['fold'] == f])) for k_ in ("pop", "oracle", "tr3")}), flush=True)
def boot(key_a, key_b, mt, users=None):
    by = collections.defaultdict(list)
    for x in recs:
        if users is None or (x["fold"], x["rater"]) in users: by[(x["fold"], x["rater"])].append(x)
    q = list(by); wt = np.array([np.mean([x["n"] for x in by[z]]) for z in q]); d = np.array([np.mean([x[f"{key_a}_{mt}"] - x[f"{key_b}_{mt}"] for x in by[z]]) for z in q]); rng = np.random.RandomState(17)
    bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; return [100 * d.sum() / wt.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), len(q)]
out = {"info": info, "pop_mismatch_rate": MIS[0] / max(1, MIS[1]), "ceiling": {k_: 100 * float(np.mean([c[k_] - c["pop"] for c in ceil])) for k_ in ("oracle", "tr3")}}
if AM4:
    for mt in ("acc", "ll"): out[f"trv-pop_{mt}"] = boot("trv", "pop", mt); out[f"trv-lr_{mt}"] = boot("trv", "lr", mt)
    out["selected"] = [x.get("am4_sel") for x in info]; out["rule"] = bool(out["trv-pop_acc"][1] > 1.0); del out["ceiling"]
    json.dump(out, open(f"{HERE}/results/stage11_s113_am4.json", "w"), indent=1); print(json.dumps({k_: v for k_, v in out.items() if k_ != "info"}), flush=True); raise SystemExit
if AM3:
    out["ceiling_by_dist"] = {d_: {k_: 100 * float(np.mean([c[k_] - c["pop"] for c in ceil if c["dist"] == d_])) for k_ in ("oracle", "tr3")} for d_ in ("gauss", "gauss_trim", "t3", "mix10")}
    ZS, ZT = np.array(ZS), np.array(ZT); P_ = ZS * ZT; rg = np.random.RandomState(17); bs = np.array([P_[rg.randint(0, len(P_), len(P_))].mean(0) for _ in range(2000)])
    out["transfer_test_users"] = {NAMES[j]: [float(P_[:, i].mean()), float(np.percentile(bs[:, i], 2.5)), float(np.percentile(bs[:, i], 97.5))] for i, j in enumerate(PRIM)}
    ms = collections.defaultdict(list)
    for x in recs: ms[(x["fold"], x["rater"])].append(x["shift"])
    ms = {z: np.mean(v) for z, v in ms.items()}; thr = np.percentile(list(ms.values()), 90); top = {z for z, v in ms.items() if v >= thr}
    out["concentration"] = {"top10_acc": boot("tr3", "pop", "acc", top), "rest_acc": boot("tr3", "pop", "acc", set(ms) - top)}
    for a_ in ("tr3", "tr3s50", "tr3s25"): out[f"{a_}-pop_acc"] = boot(a_, "pop", "acc"); out[f"{a_}-pop_ll"] = boot(a_, "pop", "ll")
    json.dump(out, open(f"{HERE}/results/stage11_s113_am3.json", "w"), indent=1); print(json.dumps({k_: v for k_, v in out.items() if k_ != "info"}), flush=True); raise SystemExit
for mt in ("acc", "ll"):
    for a_, b_ in (("tr3", "pop"), ("tr3d", "pop"), ("tr7", "pop"), ("tr3", "sap"), ("tr3", "lr")): out[f"{a_}-{b_}_{mt}"] = boot(a_, b_, mt)
out["rule"] = bool(out["tr3-pop_acc"][1] > 1.0)
json.dump(out, open(f"{HERE}/results/stage11_s113.json", "w"), indent=1); print(json.dumps({k_: v for k_, v in out.items() if k_ != "info"}), flush=True)
