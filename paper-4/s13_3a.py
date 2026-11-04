"""Stage 13 S13-3 (PROTOCOL_STAGE13.md), part a — first turns only: freeze each test-fold user's isotropic deviation δ̂_u^(1) (Stage-12 selection unchanged, k = 20 support events, draw 0).
Writes results/stage13_delta1.json: per user the fold, selected columns, τ², δ̂ (attribute units of the first turn), support conversation ids. No third-turn data are read."""
import os, json, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ["CA_PANEL"] = "ca_pairs"
exec(open(f"{HERE}/s12.py").read().split("recs, info, PAIR = ")[0])
OUT = {"users": {}, "rfold": {raters[i]: int(rfold[i]) for i in range(NR)}, "names": NAMES}
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va]); pool = np.where(test_r[R] & tr_item)[0]
    trr = np.unique(R[idx_all]); ps = set(np.random.RandomState(3 + f).choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R, list(ps))
    a_tr, a_va = idx_tr[~isp[idx_tr]], idx_va[~isp[idx_va]]; a_all = np.concatenate([a_tr, a_va]); base_s, _ = fit_base(a_tr, a_va); MUs = fit_mu(base_s, a_all)[torch.tensor(ulang)]
    lg_s = (base_s + (MUs[Rt] * A).sum(1)).numpy(); per_ps = events_of(idx_all[isp[idx_all]]); rng = np.random.RandomState(40 + f); adp, scp, kp = [], [], []
    for r, evs in per_ps.items():
        if len(evs) < KEV + 1: continue
        o = rng.permutation(len(evs)); kp.append(r); adp += [j for e in o[:KEV] for j in evs[e]]; scp += [j for e in o[KEV:] for j in evs[e]]
    adp, scp = np.array(adp, int), np.array(scp, int); vi = {}
    for nm, cols in SETS:
        for t in TAU: vi[(nm, t)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, t * np.eye(len(cols)), cols, MUs))[1].mean())
    si = max(vi, key=vi.get); cols = dict(SETS)[si[0]]
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; lg_pop = (base + (MU[Rt] * A).sum(1)).numpy()
    per_pool = events_of(pool); users = [r for r in range(NR) if test_r[r]]; ad, keep = sample_ad(per_pool, users, np.random.RandomState(10_000 * f))
    th = adapt(lg_pop, ad, keep, si[1] * np.eye(len(cols)), cols, MU); D = (th - MU).numpy(); sup = {}
    for j in ad: sup.setdefault(int(R[j]), set()).add(str(EVT[j]))
    for r in keep: OUT["users"][raters[r]] = {"fold": f, "cols": [int(c) for c in cols], "tau2": si[1], "delta": D[r, cols].tolist(), "support_conv": sorted(sup[int(r)])}
    print(f"fold {f}: iso {si}; {len(keep)} users", flush=True)
json.dump(OUT, open(f"{HERE}/results/stage13_delta1.json", "w")); print("saved", len(OUT["users"]), flush=True)
