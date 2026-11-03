"""Stage 11 Am. 9 (PROTOCOL_STAGE11.md): population model (W: bottom-50 % users / O: other-fold users) x split (E: random events / G: held-out prompt groups) on common high-volume users."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{HERE}/s11_1.py").read().split('OUT = {"a": {}, "b": {}}')[0])   # s11_1.py's data, helpers (map_dev, sel_s2, evaluate) and sap_ca.py fits
KS = (16,); OUT = {}
nev = collections.Counter(); per_all = events_of(np.arange(n))
for u, evs in per_all.items(): nev[u] = len(evs)
order_u = sorted(nev, key=lambda u: (nev[u], u)); bottom = set(order_u[:len(order_u) // 2]); top = set(u for u in order_u[len(order_u) // 2:] if nev[u] >= 17)
isb = np.isin(R, list(bottom)); ib_tr = np.where(isb & ~va_item)[0]; ib_va = np.where(isb & va_item)[0]; base_a, _ = fit_base(ib_tr, ib_va); mu_a = fit_mu(base_a, np.concatenate([ib_tr, ib_va]))
LG = {"W": (base_a + (mu_a[torch.tensor(ulang)][Rt] * A).sum(1)).numpy(), "O": np.zeros(n)}; S2 = {"O": {nm: {} for nm in ("length", "list/heading lines")}}
SUP = {"E": {}, "G": {}}; TEST = {"E": {}, "G": {}}; rng0 = np.random.RandomState(0); ok = []
for u in sorted(top):
    evs = per_all[u]; o = rng0.permutation(len(evs)); SUP["E"][u] = [evs[e] for e in o[:16]]; TEST["E"][u] = [j for e in o[16:] for j in evs[e]]
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item)[0]
    base, _ = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); lg_f = (base + (mu[torch.tensor(ulang)][Rt] * A).sum(1)).numpy(); m_ = test_r[R]; LG["O"][m_] = lg_f[m_]
    for nm in S2["O"]: S2["O"][nm][f] = sel_s2(lg_f, idx_all, NAMES.index(nm))
    per_pool = events_of(pool); per_te = collections.defaultdict(list); rng = np.random.RandomState(10_000 * f)
    for j in idx_te: per_te[R[j]].append(j)
    for u in sorted(per_te):
        evs = per_pool.get(u, [])
        if len(evs) < 16: continue
        o = rng.permutation(len(evs)); SUP["G"][u] = [evs[e] for e in o[:16]]; TEST["G"][u] = per_te[u]
        if u in top: ok.append(u)
    print(f"fold {f} done; sigma2 {[S2['O'][nm][f] for nm in S2['O']]}", flush=True)
ok = sorted(ok); OUT["n_users"] = len(ok)
for nm in ("length", "list/heading lines"):
    col = NAMES.index(nm); s2W = sel_s2(LG["W"], np.where(isb)[0], col); OUT[nm] = {"sigma2_W": s2W, "sigma2_O": S2["O"][nm]}
    for P_ in ("W", "O"):
        s2 = s2W if P_ == "W" else {u: S2["O"][nm][rfold[u]] for u in ok}
        for S_ in ("E", "G"):
            print(nm, P_, S_, flush=True); OUT[nm][P_ + S_] = evaluate(LG[P_], col, s2, SUP[S_], TEST[S_], ok)[16]
json.dump(OUT, open(f"{HERE}/results/stage11_fact.json", "w"), indent=1)
for nm in ("length", "list/heading lines"): print(nm, {c: (round(OUT[nm][c]["auc_pop"], 4), [round(x, 4) for x in OUT[nm][c]["own-pop"]["auc"]], [round(x, 2) for x in OUT[nm][c]["own-pop"]["acc"]]) for c in ("WE", "WG", "OE", "OG")}, flush=True)
