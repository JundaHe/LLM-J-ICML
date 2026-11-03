"""Stage 12 (PROTOCOL_STAGE12.md): frozen evaluation of transfer-calibrated adaptation (TRV, Stage 11 Am. 4, unchanged) on Community Alignment second turns.
Comparators with strength selected on the same pseudo-new training users: μ, a validated isotropic attribute prior (τ² I), the tuned rank-2 model (sap_ca.py).
User bootstrap (primary) and prompt-group × user two-way bootstrap (secondary); half-specific means and centred cross-covariances of the one-step deviations."""
import os, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ.setdefault("CA_PANEL", "ca_pairs_second")
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])  # sap_ca.py's data, folds, base/μ/rank-2 fits and samplers (its evaluation loop is not run)
PRIM = [NAMES.index("length"), NAMES.index("paragraphs"), NAMES.index("list/heading lines")]; L1 = [NAMES.index("length")]; SETS = (("len", L1), ("prim3", PRIM))
GRID = (1.0, 0.5, 0.25, 0.125, 0.0625, 0.0); TAU = (0.01, 0.03, 0.1, 0.3, 1.0, 0.0); An = A.numpy(); Yn = YB.numpy()
def sc_info(lg, js, cols):
    p = 1 / (1 + np.exp(-lg[js])); a = An[np.ix_(js, cols)]; return a.T @ (Yn[js] - p), (a * (p * (1 - p))[:, None]).T @ a
def halves_z(lg, idx, cols):
    per = events_of(idx); rng = np.random.RandomState(5); ZA, ZB, U = [], [], []
    for u in sorted(per):
        evs = per[u]
        if len(evs) < 10: continue
        g_ = np.array([Gp[e[0]] for e in evs]); ug_ = np.unique(g_); side = dict(zip(ug_, rng.permutation(len(ug_)) % 2)); h = np.array([side[x] for x in g_])
        if h.min() == h.max(): continue
        z = []
        for hh in (0, 1):
            js = np.array([j for e, s_ in zip(evs, h) if s_ == hh for j in e]); s, I_ = sc_info(lg, js, cols); z.append(np.linalg.solve(I_ + 1e-3 * np.eye(len(cols)), s))
        ZA.append(z[0]); ZB.append(z[1]); U.append(u)
    return np.array(ZA), np.array(ZB), np.array(U)
def est_C(lg, idx, cols):
    ZA, ZB, _ = halves_z(lg, idx, cols); C = 0.5 * (ZA.T @ ZB + ZB.T @ ZA) / len(ZA); ev_, V_ = np.linalg.eigh(C); return (V_ * np.clip(ev_, 0, None)) @ V_.T
def adapt(lg, ad, keep, C, cols, MU):
    th = MU.clone().numpy(); per = collections.defaultdict(list)
    for j in ad: per[R[j]].append(j)
    for u in keep:
        s, I_ = sc_info(lg, np.array(per[u]), cols); th[u, cols] += C @ np.linalg.solve(np.eye(len(cols)) + I_ @ C, s)
    return torch.tensor(th)
recs, info, PAIR = [], [], collections.defaultdict(list)
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    # ---- selection on pseudo-new training users (Stage 9 Am. 6 / Stage 11 Am. 4)
    trr = np.unique(R[idx_all]); ps = set(np.random.RandomState(3 + f).choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R, list(ps))
    a_tr, a_va = idx_tr[~isp[idx_tr]], idx_va[~isp[idx_va]]; a_all = np.concatenate([a_tr, a_va]); base_s, _ = fit_base(a_tr, a_va); MUs = fit_mu(base_s, a_all)[torch.tensor(ulang)]
    lg_s = (base_s + (MUs[Rt] * A).sum(1)).numpy(); per_ps = events_of(idx_all[isp[idx_all]]); rng = np.random.RandomState(40 + f); adp, scp, kp = [], [], []
    for r, evs in per_ps.items():
        if len(evs) < KEV + 1: continue
        o = rng.permutation(len(evs)); kp.append(r); adp += [j for e in o[:KEV] for j in evs[e]]; scp += [j for e in o[KEV:] for j in evs[e]]
    adp, scp = np.array(adp, int), np.array(scp, int); vt, vi = {}, {}
    for nm, cols in SETS:
        Cs = est_C(lg_s, a_all, cols)
        for c in GRID: vt[(nm, c)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, c * Cs, cols, MUs))[1].mean())
        for t in TAU: vi[(nm, t)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, t * np.eye(len(cols)), cols, MUs))[1].mean())
    st, si = max(vt, key=vt.get), max(vi, key=vi.get)
    ll_none = float(scores(base_s, scp, MUs)[1].mean()); best_lr = (ll_none, 1.0, 0.0); W0 = torch.randn(J, 2, generator=torch.Generator().manual_seed(f)) * 0.01
    for lw in (1.0, 10.0, 100.0):
        _, Wf = fit_lr(base_s, a_all, MUs, W0, 1.0, lamW=lw)
        for c in (0.1, 1.0, 10.0):
            v = scores(base_s, scp, fit_lr(base_s, adp, MUs, Wf, 1.0 / c)[0])[1].mean()
            if v > best_lr[0]: best_lr = (float(v), lw, c)
    print(f"fold {f}: {len(kp)} pseudo-new users; TRV {st}; iso {si}; rank-2 {best_lr}", flush=True)
    # ---- final fits on all training users
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; lg_pop = (base + (MU[Rt] * A).sum(1)).numpy()
    colsT = dict(SETS)[st[0]]; CT = st[1] * est_C(lg_pop, idx_all, colsT); colsI = dict(SETS)[si[0]]; CI = si[1] * np.eye(len(colsI))
    if best_lr[2] > 0: _, Wf = fit_lr(base, idx_all, MU, W0, 1.0, lamW=best_lr[1])
    ZA, ZB, U = halves_z(lg_pop, idx_all, PRIM); Ul = ulang[U]
    diag = {"mean_A": ZA.mean(0).tolist(), "mean_B": ZB.mean(0).tolist(), "uncentred": np.mean(ZA * ZB, 0).tolist(), "centred": np.mean((ZA - ZA.mean(0)) * (ZB - ZB.mean(0)), 0).tolist(),
            "centred_within_lang": np.mean(np.concatenate([(ZA[Ul == l] - ZA[Ul == l].mean(0)) * (ZB[Ul == l] - ZB[Ul == l].mean(0)) for l in np.unique(Ul)]), 0).tolist(), "n_users": int(len(U))}
    info.append({"fold": f, "pseudo_users": len(kp), "trv_val": {f"{k_[0]}_{k_[1]}": v for k_, v in vt.items()}, "iso_val": {f"{k_[0]}_{k_[1]}": v for k_, v in vi.items()}, "trv_sel": list(st), "iso_sel": list(si),
                 "lr_sel": {"ll": best_lr[0], "lamW": best_lr[1], "c": best_lr[2]}, "lambda": lam, "C_sel": CT.tolist(), "diag_prim3": diag})
    print(f"fold {f}: half means / centred cross-cov (length, paragraphs, list) {json.dumps(diag)}", flush=True)
    per_pool = events_of(pool); test_users = [r for r in np.unique(R[idx_te])]
    for dr in range(5):
        ad, keep = sample_ad(per_pool, test_users, np.random.RandomState(10_000 * f + dr)); te = idx_te[np.isin(R[idx_te], keep)]
        th = {"pop": MU, "trv": adapt(lg_pop, ad, keep, CT, colsT, MU), "iso": adapt(lg_pop, ad, keep, CI, colsI, MU), "lr": fit_lr(base, ad, MU, Wf, 1.0 / best_lr[2])[0] if best_lr[2] > 0 else MU}
        sc = {m_: scores(base, te, t_) for m_, t_ in th.items()}
        for m_ in sc:
            for mt, j_ in (("acc", 0), ("ll", 1)): PAIR[(m_, mt)].append(sc[m_][j_])
        PAIR["te"].append(te)
        for r in keep:
            sel = R[te] == r
            recs.append({"fold": f, "draw": dr, "rater": int(r), "lang": langs[ulang[r]], "n": int(sel.sum()), **{f"{m_}_acc": float(sc[m_][0][sel].sum()) for m_ in sc}, **{f"{m_}_ll": float(sc[m_][1][sel].sum()) for m_ in sc}})
def boot(key_a, key_b, mt, flt=None):
    by = collections.defaultdict(list)
    for x in recs:
        if flt is None or x["lang"] == flt: by[(x["fold"], x["rater"])].append(x)
    q = list(by); wt = np.array([np.mean([x["n"] for x in by[z]]) for z in q]); d = np.array([np.mean([x[f"{key_a}_{mt}"] - x[f"{key_b}_{mt}"] for x in by[z]]) for z in q]); rng = np.random.RandomState(17)
    bs = [d[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; return [100 * d.sum() / wt.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5), len(q)]
def boot2(key_a, key_b, mt, B=1000):
    """prompt-group × user two-way bootstrap over test pairs (each pair's difference averaged over the 5 support draws)"""
    te = np.concatenate(PAIR["te"]); d = np.concatenate(PAIR[(key_a, mt)]) - np.concatenate(PAIR[(key_b, mt)]); uq, ui = np.unique(te, return_inverse=True)
    dp = np.bincount(ui, d) / np.bincount(ui); pu = np.unique(R[uq], return_inverse=True)[1]; pg = np.unique(Gp[uq], return_inverse=True)[1]; rng = np.random.RandomState(17); bs = []
    for _ in range(B):
        wu = np.bincount(rng.randint(0, pu.max() + 1, pu.max() + 1), minlength=pu.max() + 1); wg = np.bincount(rng.randint(0, pg.max() + 1, pg.max() + 1), minlength=pg.max() + 1); w = wu[pu] * wg[pg]
        bs.append((w * dp).sum() / max(w.sum(), 1))
    return [100 * dp.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)]
out = {"info": info}
for mt in ("acc", "ll"):
    for a_, b_ in (("trv", "pop"), ("iso", "pop"), ("lr", "pop"), ("trv", "iso"), ("trv", "lr")): out[f"{a_}-{b_}_{mt}"] = boot(a_, b_, mt); out[f"{a_}-{b_}_{mt}_2way"] = boot2(a_, b_, mt)
for l_ in langs: out[f"trv-pop_acc_{l_}"] = boot("trv", "pop", "acc", l_)
acc, ll = out["trv-pop_acc"], out["trv-pop_ll"]
out["decisions"] = {"reproducible_predictive_benefit": bool(acc[1] > 0 and ll[1] > 0), "practically_meaningful_choice_gain": bool(acc[1] > 1.0), "sub_threshold": bool(acc[2] < 1.0),
                    "advantage_over_isotropic": bool(out["trv-iso_acc"][1] > 0), "advantage_over_rank2": bool(out["trv-lr_acc"][1] > 0)}
json.dump(out, open(f"{HERE}/results/stage12_{PAN["name"]}.json", "w"), indent=1); json.dump(recs, open(f"{HERE}/results/stage12_{PAN["name"]}_records.json", "w"))
print(json.dumps({k_: v for k_, v in out.items() if k_ != "info"}), flush=True)
