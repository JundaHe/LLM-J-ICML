"""Stage 11 Am. 6 (PROTOCOL_STAGE11.md): learnability ceiling with event-level simulated labels (one winner per choice event) vs the pair-level version of Am. 3."""
import os, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])  # sap_ca.py's data, folds and fits (first turns)
PRIM = [NAMES.index("length"), NAMES.index("paragraphs"), NAMES.index("list/heading lines")]; An = A.numpy(); Yn = YB.numpy()
def sc_info(lg, a, y):
    p = 1 / (1 + np.exp(-lg)); return a.T @ (y - p), (a * (p * (1 - p))[:, None]).T @ a
def est_C(lg, idx):
    per = events_of(idx); rng = np.random.RandomState(5); ZA, ZB = [], []
    for u in sorted(per):
        evs = per[u]
        if len(evs) < 10: continue
        g_ = np.array([Gp[e[0]] for e in evs]); ug_ = np.unique(g_); side = dict(zip(ug_, rng.permutation(len(ug_)) % 2)); h = np.array([side[x] for x in g_])
        if h.min() == h.max(): continue
        z = []
        for hh in (0, 1):
            js = np.array([j for e, s_ in zip(evs, h) if s_ == hh for j in e]); s, I_ = sc_info(lg[js], An[np.ix_(js, PRIM)], Yn[js]); z.append(np.linalg.solve(I_ + 1e-3 * np.eye(3), s))
        ZA.append(z[0]); ZB.append(z[1])
    ZA, ZB = np.array(ZA), np.array(ZB); C = 0.5 * (ZA.T @ ZB + ZB.T @ ZA) / len(ZA); ev_, V_ = np.linalg.eigh(C); return (V_ * np.clip(ev_, 0, None)) @ V_.T
def event_design(evs):
    """per event: population logits and primary attributes of each response relative to the chosen one (u_c = 0)"""
    out = []
    for js in evs:
        js = np.array(js); s = 2 * Yn[js] - 1; out.append((js, s))
    return out
def sim_event(lgp, lgT, evd, g):
    """one winner per event from the multinomial logit; returns (pop logit, true logit, attrs) of winner-vs-other pairs, label 1 = winner"""
    LP, LT, AA, EV = [], [], [], []
    for k, (js, s) in enumerate(evd):
        vp = np.concatenate([[0.0], -s * lgp[js]]); vt = np.concatenate([[0.0], -s * lgT[js]]); a = np.vstack([np.zeros(3), -(s[:, None] * An[np.ix_(js, PRIM)])])
        pr = np.exp(vt - vt.max()); w = g.choice(len(vt), p=pr / pr.sum()); o = [i for i in range(len(vt)) if i != w]
        LP += list(vp[w] - vp[o]); LT += list(vt[w] - vt[o]); AA.append(a[w] - a[o]); EV += [k] * len(o)
    return np.array(LP), np.array(LT), np.vstack(AA), np.array(EV)
def adapt_vec(lg, a, y, owner, users, C):
    D = {}
    for u in users:
        m = owner == u; s, I_ = sc_info(lg[m], a[m], y[m]); D[u] = C @ np.linalg.solve(np.eye(3) + I_ @ C, s)
    return D
res = []
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; lg_pop = (base + (MU[Rt] * A).sum(1)).numpy(); C3 = est_C(lg_pop, idx_all)
    per_pool = events_of(pool); test_users = [r for r in np.unique(R[idx_te])]; ad, keep = sample_ad(per_pool, test_users, np.random.RandomState(10_000 * f)); te = idx_te[np.isin(R[idx_te], keep)]
    ad_ev = [e for evs in events_of(ad).values() for e in evs]; te_ev = [e for evs in events_of(te).values() for e in evs]
    ad_own = np.array([R[e[0]] for e in ad_ev]); te_own = np.array([R[e[0]] for e in te_ev]); evd_ad, evd_te = event_design(ad_ev), event_design(te_ev)
    g = np.random.RandomState(900 + f); Lc = np.linalg.cholesky(C3 + 1e-9 * np.eye(3))
    for dist in ("gauss", "t3", "mix10"):
        for mc in range(5):
            dl = g.randn(len(keep), 3) @ Lc.T
            if dist == "t3": dl = dl * np.sqrt(1 / 3) / np.sqrt(g.chisquare(3, (len(keep), 1)) / 3)
            if dist == "mix10": dl = dl * np.sqrt(10) * (g.rand(len(keep), 1) < 0.1)
            D_ = np.zeros((NR, 3)); D_[keep] = dl; lgT = lg_pop + (D_[R] * An[:, PRIM]).sum(1); pT = 1 / (1 + np.exp(-lgT))
            # pair-level (Am. 3): independent Bernoulli label per pair
            y = (g.rand(n) < pT).astype(float); row = {"fold": f, "dist": dist, "mc": mc}
            for c in (1.0, 0.25):
                Dh = adapt_vec(lg_pop[ad], An[np.ix_(ad, PRIM)], y[ad], R[ad], keep, c * C3); Dm = np.zeros((NR, 3))
                for u, v in Dh.items(): Dm[u] = v
                lgE = lg_pop + (Dm[R] * An[:, PRIM]).sum(1); hit = lambda lg_: np.where(lg_[te] > 0, pT[te], 1 - pT[te]).mean()
                row.update({"pair_pop": hit(lg_pop), "pair_oracle": hit(lgT), f"pair_tr3_c{c}": hit(lgE)})
            # event-level: one winner per event
            LPa, LTa, AAa, EVa = sim_event(lg_pop, lgT, evd_ad, g); LPt, LTt, AAt, EVt = sim_event(lg_pop, lgT, evd_te, g); own_a = ad_own[EVa]; own_t = te_own[EVt]
            for c in (1.0, 0.25):
                Dh = adapt_vec(LPa, AAa, np.ones(len(LPa)), own_a, keep, c * C3); Dm = np.zeros((NR, 3))
                for u, v in Dh.items(): Dm[u] = v
                lgE = LPt + (Dm[own_t] * AAt).sum(1); row.update({"ev_pop": float((LPt > 0).mean()), "ev_oracle": float((LTt > 0).mean()), f"ev_tr3_c{c}": float((lgE > 0).mean())})
            res.append(row); print(json.dumps(row), flush=True)
out = {"rows": res, "summary": {}}
for dist in ("gauss", "t3", "mix10"):
    rr = [x for x in res if x["dist"] == dist]
    out["summary"][dist] = {f"{md}_{k_}": 100 * float(np.mean([x[f"{md}_{k_}"] - x[f"{md}_pop"] for x in rr])) for md in ("pair", "ev") for k_ in ("oracle", "tr3_c1.0", "tr3_c0.25")}
g_ = out["summary"]["gauss"]; out["reading"] = {"ratio_event_to_pair_tr3": g_["ev_tr3_c1.0"] / g_["pair_tr3_c1.0"], "am3_stands": bool(abs(np.log(g_["ev_tr3_c1.0"] / g_["pair_tr3_c1.0"])) <= np.log(1.5))}
json.dump(out, open(f"{HERE}/results/stage11_ev.json", "w"), indent=1); print(json.dumps(out["summary"]), json.dumps(out["reading"]), flush=True)
