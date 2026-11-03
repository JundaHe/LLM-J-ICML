"""Stage 11 Am. 8 (PROTOCOL_STAGE11.md): length transfer within prompt clusters (centred within language x cluster) and task-mix-matched own - other, CA first turns."""
import os, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])  # sap_ca.py's data, folds and fits (first turns)
from sklearn.cluster import KMeans
An = A.numpy(); Yn = YB.numpy(); COL = NAMES.index("length"); a1 = An[:, COL]; GS2 = np.logspace(-3, 1, 25)
XP = (Fz["E_P"].astype(np.float32) - mu0) @ W256; CLS = {k: KMeans(k, random_state=0, n_init=4).fit_predict(XP) for k in (8, 32)}; del XP
print({k: np.bincount(v).tolist() for k, v in CLS.items()}, flush=True)
# ---- cross-fitted population logits and per-fold length sigma2 (as s11_1.py (b))
def map_dev(lg, a, y, s2):
    d = 0.0
    for _ in range(30):
        p = 1 / (1 + np.exp(-(lg + d * a))); g_ = (a * (y - p)).sum() - d / s2; h = (a * a * p * (1 - p)).sum() + 1 / s2; d += g_ / h
    return d
def sel_s2(lg, idx):
    ui = np.unique(R[idx], return_inverse=True)[1]; nu = ui.max() + 1; l0, a, y = lg[idx], a1[idx], Yn[idx]; best = None
    for s2 in GS2:
        d = np.zeros(nu)
        for _ in range(30):
            p = 1 / (1 + np.exp(-(l0 + d[ui] * a))); d += (np.bincount(ui, a * (y - p), nu) - d / s2) / (np.bincount(ui, a * a * p * (1 - p), nu) + 1 / s2)
        p = 1 / (1 + np.exp(-(l0 + d[ui] * a))); h = np.bincount(ui, a * a * p * (1 - p), nu) + 1 / s2
        lm = (y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)).sum() - (0.5 * d * d / s2 + 0.5 * np.log(s2 * h)).sum()
        if best is None or lm > best[0]: best = (lm, float(s2))
    return best[1]
lgb = np.zeros(n); SUP, TEST, S2 = {}, {}, {}
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base, _ = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); lg_f = (base + (mu[torch.tensor(ulang)][Rt] * A).sum(1)).numpy(); m_ = test_r[R]; lgb[m_] = lg_f[m_]
    s2 = sel_s2(lg_f, idx_all); per_pool = events_of(pool); per_te = collections.defaultdict(list); rng = np.random.RandomState(10_000 * f)
    for j in idx_te: per_te[R[j]].append(j)
    for u in sorted(per_te):
        evs = per_pool.get(u, [])
        if len(evs) < 16: continue
        o = rng.permutation(len(evs)); SUP[u] = [evs[e] for e in o[:16]]; TEST[u] = np.array(per_te[u]); S2[u] = s2
    print(f"fold {f}: sigma2 {s2}", flush=True)
pT = 1 / (1 + np.exp(-lgb)); OUT = {"cluster_sizes": {k: np.bincount(v).tolist() for k, v in CLS.items()}}
# ---- (1) within-task-type transfer
per = events_of(np.arange(n)); rng = np.random.RandomState(5); HALF = {}
for u in sorted(per):
    evs = per[u]
    if len(evs) < 10: continue
    g_ = np.array([Gp[e[0]] for e in evs]); ug_ = np.unique(g_); side = dict(zip(ug_, rng.permutation(len(ug_)) % 2)); h = np.array([side[x] for x in g_])
    if h.min() == h.max(): continue
    HALF[u] = (evs, h)
def zz(js):
    js = np.array(js); p = pT[js]; return (a1[js] * (Yn[js] - p)).sum() / ((a1[js] ** 2 * p * (1 - p)).sum() + 1e-3), (a1[js] ** 2 * p * (1 - p)).sum()
def boot_users(us, num, den, B=2000):
    q = np.unique(us); ix_ = {u: i for i, u in enumerate(q)}; ui = np.array([ix_[u] for u in us]); N = np.bincount(ui, num, len(q)); D = np.bincount(ui, den, len(q)); rng_ = np.random.RandomState(17)
    bs = [N[s].sum() / D[s].sum() for s in (rng_.randint(0, len(q), len(q)) for _ in range(B))]; return [float(N.sum() / D.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), int(len(q))]
for K, CL in CLS.items():
    cells = []
    for u, (evs, h) in HALF.items():
        c_ = np.array([CL[e[0]] for e in evs])
        for c in np.unique(c_):
            ea = [j for e, s_, cc in zip(evs, h, c_) if s_ == 0 and cc == c for j in e]; eb = [j for e, s_, cc in zip(evs, h, c_) if s_ == 1 and cc == c for j in e]
            if sum(1 for s_, cc in zip(h, c_) if s_ == 0 and cc == c) < 2 or sum(1 for s_, cc in zip(h, c_) if s_ == 1 and cc == c) < 2: continue
            (za, ia), (zb, ib) = zz(ea), zz(eb); cells.append((u, ulang[u], c, za, zb, ia * ib / (ia + ib)))
    U_, L_, C_, ZA, ZB, W_ = map(np.array, zip(*cells)); ZAc, ZBc = ZA.copy(), ZB.copy()
    for l in np.unique(L_):
        for c in np.unique(C_):
            m = (L_ == l) & (C_ == c)
            if m.sum(): ZAc[m] -= np.average(ZA[m], weights=W_[m]); ZBc[m] -= np.average(ZB[m], weights=W_[m])
    OUT[f"within_k{K}"] = {"centred": boot_users(U_, W_ * ZAc * ZBc, W_), "uncentred": boot_users(U_, W_ * ZA * ZB, W_), "n_cells": int(len(cells))}
    print(K, json.dumps(OUT[f"within_k{K}"]), flush=True)
us_ = sorted(HALF); pooled = []
for u in us_:
    evs, h = HALF[u]; (za, ia), (zb, ib) = zz([j for e, s_ in zip(evs, h) if s_ == 0 for j in e]), zz([j for e, s_ in zip(evs, h) if s_ == 1 for j in e]); pooled.append((u, za * zb * ia * ib / (ia + ib), ia * ib / (ia + ib)))
U_, N_, D_ = map(np.array, zip(*pooled)); OUT["pooled_1d_length"] = boot_users(U_, N_, D_); print("pooled", OUT["pooled_1d_length"], flush=True)
# ---- (2) task-mix-matched own - other at k = 16
users = sorted(SUP); D = {u: map_dev(lgb[np.concatenate(SUP[u])], a1[np.concatenate(SUP[u])], Yn[np.concatenate(SUP[u])], S2[u]) for u in users}
H = {u: np.bincount([CLS[8][e[0]] for e in SUP[u]], minlength=8) / 16 for u in users}; match, cyc = {}, {}
for l in np.unique(ulang[users]):
    g_ = [u for u in users if ulang[u] == l]; Hm = np.array([H[u] for u in g_])
    for i, u in enumerate(g_):
        dist = np.abs(Hm - Hm[i]).sum(1); dist[i] = np.inf; match[u] = g_[int(np.argmin(dist))]
    g2 = np.array(g_)[np.random.RandomState(0).permutation(len(g_))]
    for i, u in enumerate(g2): cyc[u] = g2[(i + 1) % len(g2)]
def sc(u, d):
    t = TEST[u]; lg = lgb[t] + d * a1[t]; y = Yn[t]; return ((lg > 0) == y).sum(), (y * -np.logaddexp(0, -lg) + (1 - y) * -np.logaddexp(0, lg)).sum()
nu = np.array([len(TEST[u]) for u in users]); S = {m: np.array([sc(u, d_) for u, d_ in zip(users, dd)]) for m, dd in (("pop", [0.0] * len(users)), ("own", [D[u] for u in users]), ("match", [D[match[u]] for u in users]), ("cyc", [D[cyc[u]] for u in users]))}
rng_ = np.random.RandomState(17); BS = [rng_.randint(0, len(users), len(users)) for _ in range(2000)]
for a_, b_ in (("own", "pop"), ("own", "match"), ("own", "cyc"), ("match", "cyc")):
    for k_, mt in ((0, "acc"), (1, "ll")):
        d_ = S[a_][:, k_] - S[b_][:, k_]; sc_ = 100 if mt == "acc" else 1; bs = [d_[ix].sum() / nu[ix].sum() for ix in BS]
        OUT[f"{a_}-{b_}_{mt}"] = [sc_ * d_.sum() / nu.sum(), sc_ * np.percentile(bs, 2.5), sc_ * np.percentile(bs, 97.5), len(users)]
OUT["match_L1_mean"] = float(np.mean([np.abs(H[u] - H[match[u]]).sum() for u in users])); OUT["cyc_L1_mean"] = float(np.mean([np.abs(H[u] - H[cyc[u]]).sum() for u in users]))
OUT["decision"] = {"individual_length_signal_matched_task_type": bool(OUT["within_k8"]["centred"][1] > 0 and OUT["own-match_ll"][1] > 0), "practical_gain": bool(OUT["own-pop_acc"][1] > 1.0)}
json.dump(OUT, open(f"{HERE}/results/stage11_mix.json", "w"), indent=1); print(json.dumps(OUT), flush=True)
