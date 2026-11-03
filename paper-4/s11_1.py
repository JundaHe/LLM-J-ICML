"""Stage 11 S11-1 / Am. 7 (PROTOCOL_STAGE11.md): WIMHF-style one-attribute personalisation, (a) held-out high-volume users without prompt separation, (b) our new-user protocol."""
import os, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])  # sap_ca.py's data, folds and fits (first turns)
An = A.numpy(); Yn = YB.numpy(); KS = (1, 2, 4, 8, 16); GS2 = np.logspace(-3, 1, 25); ATTRS = ("list/heading lines", "length", "paragraphs")
def map_dev(lg, a, y, s2):
    d = 0.0
    for _ in range(30):
        p = 1 / (1 + np.exp(-(lg + d * a))); g_ = (a * (y - p)).sum() - d / s2; h = (a * a * p * (1 - p)).sum() + 1 / s2; d += g_ / h
        if abs(g_ / h) < 1e-8: break
    p = 1 / (1 + np.exp(-(lg + d * a))); ll = (y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)).sum(); h = (a * a * p * (1 - p)).sum() + 1 / s2
    return d, ll - 0.5 * d * d / s2 - 0.5 * np.log(s2 * h)
def sel_s2(lg, idx, col):
    """σ² maximising the summed Laplace marginal likelihood over the users in idx (Newton vectorised over users)"""
    ui = np.unique(R[idx], return_inverse=True)[1]; nu = ui.max() + 1; l0, a, y = lg[idx], An[idx, col], Yn[idx]; best = None
    for s2 in GS2:
        d = np.zeros(nu)
        for _ in range(30):
            p = 1 / (1 + np.exp(-(l0 + d[ui] * a))); g_ = np.bincount(ui, a * (y - p), nu) - d / s2; h = np.bincount(ui, a * a * p * (1 - p), nu) + 1 / s2; d += g_ / h
        p = 1 / (1 + np.exp(-(l0 + d[ui] * a))); h = np.bincount(ui, a * a * p * (1 - p), nu) + 1 / s2
        lm = (y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)).sum() - (0.5 * d * d / s2 + 0.5 * np.log(s2 * h)).sum()
        if best is None or lm > best[0]: best = (lm, float(s2))
    return best[1]
def other_of(users):
    users = np.array(sorted(users)); o = {}; perm = np.random.RandomState(0).permutation(len(users)); users = users[perm]
    for l in np.unique(ulang[users]):
        g_ = users[ulang[users] == l]
        for i, u in enumerate(g_): o[u] = g_[(i + 1) % len(g_)]
    return o
def auc(s, y):
    r = np.argsort(np.argsort(s)) + 1.0; n1 = y.sum(); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
def evaluate(lg, col, s2, sup, test, users):
    """sup[u]: ordered list of events (lists of rows); test[u]: rows. Returns per-k pooled scores of pop / own / other."""
    oth = other_of(users); out = {}
    for k in KS:
        D = {u: map_dev(lg[np.array([j for e in sup[u][:k] for j in e])], An[np.array([j for e in sup[u][:k] for j in e]), col], Yn[np.array([j for e in sup[u][:k] for j in e])], s2[u] if isinstance(s2, dict) else s2)[0] for u in users}
        rows = {m: [] for m in ("pop", "own", "oth")}; owner = []
        for u in users:
            t = np.array(test[u]); owner += [u] * len(t)
            for m, dd in (("pop", 0.0), ("own", D[u]), ("oth", D[oth[u]])): rows[m].append(lg[t] + dd * An[t, col])
        y = Yn[np.concatenate([np.array(test[u]) for u in users])]; owner = np.array(owner); L = {m: np.concatenate(v) for m, v in rows.items()}
        uo = {u: np.where(owner == u)[0] for u in users}; rng = np.random.RandomState(17); res = {}
        for a_, b_ in (("own", "pop"), ("own", "oth")):
            pt = auc(L[a_], y) - auc(L[b_], y); bs = []
            for _ in range(1000):
                ix = np.concatenate([uo[u] for u in rng.choice(users, len(users))]); bs.append(auc(L[a_][ix], y[ix]) - auc(L[b_][ix], y[ix]))
            ha, hb = ((L[a_] > 0) == y).astype(float), ((L[b_] > 0) == y).astype(float); du = np.array([(ha[uo[u]] - hb[uo[u]]).sum() for u in users]); nu = np.array([len(uo[u]) for u in users])
            r2 = np.random.RandomState(17); ab = [du[ix].sum() / nu[ix].sum() for ix in (r2.randint(0, len(users), len(users)) for _ in range(2000))]
            res[f"{a_}-{b_}"] = {"auc": [pt, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "acc": [100 * du.sum() / nu.sum(), 100 * np.percentile(ab, 2.5), 100 * np.percentile(ab, 97.5)]}
        res["auc_pop"] = auc(L["pop"], y); res["n_users"] = len(users); res["n_test"] = int(len(y)); out[k] = res; print(k, json.dumps(res), flush=True)
    return out
OUT = {"a": {}, "b": {}}
# ---- (a) WIMHF-style: population on bottom-50 % users by event count, adapt the held-out top-50 % (prompts not separated)
nev = collections.Counter(); per_all = events_of(np.arange(n))
for u, evs in per_all.items(): nev[u] = len(evs)
order_u = sorted(nev, key=lambda u: (nev[u], u)); bottom = set(order_u[:len(order_u) // 2]); top = [u for u in order_u[len(order_u) // 2:] if nev[u] >= 17]
isb = np.isin(R, list(bottom)); ib_tr = np.where(isb & ~va_item)[0]; ib_va = np.where(isb & va_item)[0]; base_a, _ = fit_base(ib_tr, ib_va); mu_a = fit_mu(base_a, np.concatenate([ib_tr, ib_va]))
lg_a = (base_a + (mu_a[torch.tensor(ulang)][Rt] * A).sum(1)).numpy(); rng0 = np.random.RandomState(0); sup_a, test_a = {}, {}
for u in top:
    evs = per_all[u]; o = rng0.permutation(len(evs)); sup_a[u] = [evs[e] for e in o[:16]]; test_a[u] = [j for e in o[16:] for j in evs[e]]
for nm in ATTRS:
    col = NAMES.index(nm); s2 = sel_s2(lg_a, np.where(isb)[0], col); print(f"(a) {nm}: sigma2 {s2}", flush=True); OUT["a"][nm] = {"sigma2": s2, "by_k": evaluate(lg_a, col, s2, sup_a, test_a, top)}
# ---- (b) our protocol: user folds, prompt-group folds
for nm in ATTRS: OUT["b"][nm] = {"folds": []}
POOL = {nm: {"lg": [], "sup": {}, "test": {}, "users": [], "s2": []} for nm in ATTRS}
lgb = np.zeros(n)
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base, _ = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); lg_f = (base + (mu[torch.tensor(ulang)][Rt] * A).sum(1)).numpy(); m_ = test_r[R]; lgb[m_] = lg_f[m_]
    per_pool = events_of(pool); per_te = collections.defaultdict(list)
    for j in idx_te: per_te[R[j]].append(j)
    rng = np.random.RandomState(10_000 * f)
    for u in sorted(per_te):
        evs = per_pool.get(u, [])
        if len(evs) < 16: continue
        o = rng.permutation(len(evs))
        for nm in ATTRS: POOL[nm]["sup"][u] = [evs[e] for e in o[:16]]; POOL[nm]["test"][u] = per_te[u]; POOL[nm]["users"].append(u)
    for nm in ATTRS: POOL[nm]["s2"].append(sel_s2(lg_f, idx_all, NAMES.index(nm)))
for nm in ATTRS:
    # each test user gets the σ² selected on its own fold's training users
    col = NAMES.index(nm); s2u = {u: POOL[nm]["s2"][rfold[u]] for u in POOL[nm]["users"]}
    print(f"(b) {nm}: sigma2 by fold {POOL[nm]['s2']}", flush=True); OUT["b"][nm] = {"sigma2_by_fold": POOL[nm]["s2"], "by_k": evaluate(lgb, col, s2u, POOL[nm]["sup"], POOL[nm]["test"], POOL[nm]["users"])}
prim = OUT["a"]["list/heading lines"]["by_k"][16]["own-pop"]["auc"]; OUT["reading"] = {"wimhf_reproduced": bool(prim[1] > 0)}
json.dump(OUT, open(f"{HERE}/results/stage11_s111.json", "w"), indent=1); print(json.dumps(OUT["reading"]), flush=True)
