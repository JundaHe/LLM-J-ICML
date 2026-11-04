"""Stage 13 S13-1 (PROTOCOL_STAGE13.md): identity on identical CA first-turn items (endpoint A) and benefit on the same panel (endpoint B); learners frozen from Stage 12 (isotropic primary, TRV secondary)."""
import os, json, collections, numpy as np, torch, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ["CA_PANEL"] = "ca_pairs"
exec(open(f"{HERE}/s12.py").read().split("recs, info, PAIR = ")[0])  # s12.py: sap_ca.py's data and fits, halves_z / est_C / adapt, SETS, GRID, TAU (unchanged)
# ---- identical items (label-blind: prompt and the four ordered responses only)
d = pd.read_csv(data_panels.CA_CSV, usecols=["conversation_id", "first_turn_prompt"] + [f"first_turn_response_{x}" for x in "abcd"]).dropna()
d["okey"] = list(zip(d.first_turn_prompt, *[d[f"first_turn_response_{x}"] for x in "abcd"])); d["skey"] = [(k[0],) + tuple(sorted(k[1:])) for k in d.okey]
nord = d.groupby("skey").okey.nunique(); d = d[d.skey.map(nord) == 1]; ids = {k: i for i, k in enumerate(sorted(set(d.okey), key=str))}; ITEM_OF = dict(zip(d.conversation_id.astype(str), d.okey.map(ids)))
ITEM = np.array([ITEM_OF.get(e, -1) for e in EVT]); LET = np.array([s.split("|")[1] for s in PAN["item_ids"]])
nu_item = collections.Counter(); seen = set()
for j in range(n):
    if ITEM[j] >= 0 and (ITEM[j], R[j]) not in seen: seen.add((ITEM[j], R[j])); nu_item[ITEM[j]] += 1
SH = np.array([ITEM[j] >= 0 and nu_item[ITEM[j]] >= 2 for j in range(n)])
POSRUN = os.environ.get("S13POS") == "1"
if POSRUN:                                                                 # Am. 2: position-difference columns (B minus A; positions b, c, d one-hot, a = reference)
    chosen = {}
    for e_, l_ in zip(EVT, LET): chosen.setdefault(e_, set("abcd")).discard(l_)
    CH = np.array([next(iter(chosen[e_])) for e_ in EVT]); Yb = np.asarray(PAN["yb"]); posB = np.where(Yb == 1, CH, LET); posA = np.where(Yb == 1, LET, CH)
    oh = lambda P_: np.stack([(P_ == x).astype(float) for x in "bcd"], 1); A = torch.cat([A, torch.tensor(oh(posB) - oh(posA))], 1); J = A.shape[1]
    POS = [J - 3, J - 2, J - 1]; SETS = (("pos", POS), ("lenpos", L1 + POS), ("prim3pos", PRIM + POS)); ISO_SETS = SETS; TRV_SETS = ()
else: ISO_SETS = SETS; TRV_SETS = SETS
An = A.numpy(); Yn = YB.numpy(); G_ = (2 * Yn - 1)[:, None] * An   # G_ = x_chosen - x_other
ATTRC = np.arange(J - 3) if POSRUN else None
print(f"identical items with >= 2 users: {sum(1 for v in nu_item.values() if v >= 2)}; shared pairs {SH.sum()}", flush=True)
recs, A_rows, gate = [], [], {}
for f in range(5):
    test_r = rfold == f; tr_item = ifold != f; is_tr = ~test_r[R]
    idx_tr = np.where(is_tr & tr_item & ~va_item)[0]; idx_va = np.where(is_tr & tr_item & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    pool = np.where(test_r[R] & tr_item)[0]; idx_te = np.where(test_r[R] & ~tr_item & SH)[0]
    per_pool = events_of(pool); test_users = [r for r in np.unique(R[idx_te]) if len(per_pool.get(r, [])) >= KEV]
    it_users = collections.defaultdict(set)
    for j in idx_te:
        if R[j] in set(test_users): it_users[ITEM[j]].add(R[j])
    gate[f] = sum(1 for v in it_users.values() if len(v) >= 2); print(f"fold {f}: {len(test_users)} test users; items with >= 2 test users {gate[f]}", flush=True)
    if f == 4 and sum(gate.values()) < 300: raise SystemExit("S13-1 infeasible by the pre-set gate")
    # ---- selection on pseudo-new training users: exactly s12.py
    trr = np.unique(R[idx_all]); ps = set(np.random.RandomState(3 + f).choice(trr, len(trr) // 5, replace=False)); isp = np.isin(R, list(ps))
    a_tr, a_va = idx_tr[~isp[idx_tr]], idx_va[~isp[idx_va]]; a_all = np.concatenate([a_tr, a_va]); base_s, _ = fit_base(a_tr, a_va); MUs = fit_mu(base_s, a_all)[torch.tensor(ulang)]
    lg_s = (base_s + (MUs[Rt] * A).sum(1)).numpy(); per_ps = events_of(idx_all[isp[idx_all]]); rng = np.random.RandomState(40 + f); adp, scp, kp = [], [], []
    for r, evs in per_ps.items():
        if len(evs) < KEV + 1: continue
        o = rng.permutation(len(evs)); kp.append(r); adp += [j for e in o[:KEV] for j in evs[e]]; scp += [j for e in o[KEV:] for j in evs[e]]
    adp, scp = np.array(adp, int), np.array(scp, int); vt, vi = {}, {}
    for nm, cols in TRV_SETS:
        Cs = est_C(lg_s, a_all, cols)
        for c in GRID: vt[(nm, c)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, c * Cs, cols, MUs))[1].mean())
    for nm, cols in ISO_SETS:
        for t in TAU: vi[(nm, t)] = float(scores(base_s, scp, adapt(lg_s, adp, kp, t * np.eye(len(cols)), cols, MUs))[1].mean())
    if POSRUN:
        vj = {k_: v for k_, v in vi.items() if k_[0] != "pos"}; vp = {k_: v for k_, v in vi.items() if k_[0] == "pos"}; si, st = max(vj, key=vj.get), max(vp, key=vp.get)   # "trv" slot = position-only learner
    else: st, si = max(vt, key=vt.get), max(vi, key=vi.get)
    print(f"fold {f}: TRV/pos-only {st}; iso {si}", flush=True)
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; lg_pop = (base + (MU[Rt] * A).sum(1)).numpy()
    colsI = dict(SETS)[si[0]]; CI = si[1] * np.eye(len(colsI)); colsT = dict(SETS)[st[0]]; CT = st[1] * (np.eye(len(colsT)) if POSRUN else est_C(lg_pop, idx_all, colsT))
    te_by = collections.defaultdict(dict); first_conv = {}                 # item -> user -> {other letter: row}; a user who saw an item twice: first conversation only
    for j in idx_te:
        if R[j] not in set(test_users): continue
        k_ = (ITEM[j], R[j]); first_conv.setdefault(k_, EVT[j])
        if EVT[j] == first_conv[k_]: te_by[ITEM[j]].setdefault(R[j], {})[LET[j]] = j
    DEL = {m_: [] for m_ in ("iso", "trv")}
    for dr in range(5):
        ad, keep = sample_ad(per_pool, test_users, np.random.RandomState(10_000 * f + dr)); te = idx_te[np.isin(R[idx_te], keep)]
        th = {"pop": MU, "iso": adapt(lg_pop, ad, keep, CI, colsI, MU), "trv": adapt(lg_pop, ad, keep, CT, colsT, MU)}
        for m_ in ("iso", "trv"): DEL[m_].append((th[m_] - MU).numpy())
        sc = {m_: scores(base, te, t_) for m_, t_ in th.items()}
        for r in keep:
            sel = R[te] == r
            recs.append({"fold": f, "draw": dr, "rater": int(r), "n": int(sel.sum()), **{f"{m_}_acc": float(sc[m_][0][sel].sum()) for m_ in sc}, **{f"{m_}_ll": float(sc[m_][1][sel].sum()) for m_ in sc},
                         "items": [int(x) for x in ITEM[te[sel]]], **{f"{m_}_acc_rows": sc[m_][0][sel].tolist() for m_ in sc}, **{f"{m_}_ll_rows": sc[m_][1][sel].tolist() for m_ in sc}})
    # ---- endpoint A: pairs of test users of the same item choosing different responses
    for it, us in te_by.items():
        us = [u for u in us if u in set(test_users)]
        for i in range(len(us)):
            for k in range(i + 1, len(us)):
                u, v = us[i], us[k]; rows_u, rows_v = te_by[it][u], te_by[it][v]
                if len(rows_u) < 3 or len(rows_v) < 3: continue
                cu = ({"a", "b", "c", "d"} - set(rows_u)).pop(); cv = ({"a", "b", "c", "d"} - set(rows_v)).pop()   # chosen = the letter without an "other" row
                if cu == cv: continue
                g = G_[rows_u[cv]]                                         # x_{a} - x_{b}, a = u's choice, b = v's choice
                out = {"item": int(it), "u": int(u), "v": int(v), "fold": f}
                parts = [("iso", "iso", None), ("trv", "trv", None)] + ([("iso_attr", "iso", ATTRC), ("iso_pos", "iso", POS)] if POSRUN else [])
                for nm_, m_, cc in parts:
                    S = np.array([((D_[u] - D_[v]) * g)[cc].sum() if cc is not None else ((D_[u] - D_[v]) * g).sum() for D_ in DEL[m_]]); out[f"{nm_}_ls"] = float(np.mean(-np.logaddexp(0, -S) + np.log(2))); out[f"{nm_}_acc"] = float(np.mean((S > 0) + 0.5 * (S == 0)))
                A_rows.append(out)
    print(f"fold {f}: {len(A_rows)} disagreeing pairs so far", flush=True)
# ---- inference
def twoway_A(key, B=1000):
    it = np.array([x["item"] for x in A_rows]); uu = np.array([x["u"] for x in A_rows]); vv = np.array([x["v"] for x in A_rows]); val = np.array([x[key] for x in A_rows])
    iq, ii = np.unique(it, return_inverse=True); uq = np.unique(np.concatenate([uu, vv])); ui = np.searchsorted(uq, uu); vi_ = np.searchsorted(uq, vv)
    def est(wi, wu):
        w = wu[ui] * wu[vi_]; num = np.bincount(ii, w * val, len(iq)); den = np.bincount(ii, w, len(iq)); m = den > 0
        return (wi[m] * num[m] / den[m]).sum() / wi[m].sum()
    pt = est(np.ones(len(iq)), np.ones(len(uq))); rng = np.random.RandomState(17); bs = []
    for _ in range(B): bs.append(est(np.bincount(rng.randint(0, len(iq), len(iq)), minlength=len(iq)).astype(float), np.bincount(rng.randint(0, len(uq), len(uq)), minlength=len(uq)).astype(float)))
    return [float(pt), float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5)), int(len(iq)), int(len(A_rows))]
def boot(a_, b_, mt):
    by = collections.defaultdict(list)
    for x in recs: by[(x["fold"], x["rater"])].append(x)
    q = list(by); wt = np.array([np.mean([x["n"] for x in by[z]]) for z in q]); dd = np.array([np.mean([x[f"{a_}_{mt}"] - x[f"{b_}_{mt}"] for x in by[z]]) for z in q]); rng = np.random.RandomState(17)
    bs = [dd[ix].sum() / wt[ix].sum() for ix in (rng.randint(0, len(q), len(q)) for _ in range(2000))]; sc_ = 100 if mt == "acc" else 1
    return [sc_ * dd.sum() / wt.sum(), sc_ * np.percentile(bs, 2.5), sc_ * np.percentile(bs, 97.5), len(q)]
def boot2(a_, b_, mt, B=1000):
    """user x item two-way over test pairs (each pair's difference averaged over draws)"""
    pr = collections.defaultdict(list)
    for x in recs:
        for k_, (it, ra, rb) in enumerate(zip(x["items"], x[f"{a_}_{mt}_rows"], x[f"{b_}_{mt}_rows"])): pr[(x["rater"], it, k_)].append(ra - rb)
    keys = list(pr); dp = np.array([np.mean(pr[k_]) for k_ in keys]); uq, ui = np.unique([k_[0] for k_ in keys], return_inverse=True); iq, ii = np.unique([k_[1] for k_ in keys], return_inverse=True)
    rng = np.random.RandomState(17); bs = []; sc_ = 100 if mt == "acc" else 1
    for _ in range(B):
        w = np.bincount(rng.randint(0, len(uq), len(uq)), minlength=len(uq))[ui] * np.bincount(rng.randint(0, len(iq), len(iq)), minlength=len(iq))[ii]; bs.append((w * dp).sum() / max(w.sum(), 1))
    return [sc_ * dp.mean(), sc_ * np.percentile(bs, 2.5), sc_ * np.percentile(bs, 97.5)]
out = {"gate_items_by_fold": gate, "A": {m_: {"logscore": twoway_A(f"{m_}_ls"), "acc": twoway_A(f"{m_}_acc")} for m_ in (("iso", "trv", "iso_attr", "iso_pos") if POSRUN else ("iso", "trv"))}}
dA = [x["trv_ls"] - x["iso_ls"] for x in A_rows]
for x, v in zip(A_rows, dA): x["d_ls"] = v
out["A"]["trv-iso_logscore"] = twoway_A("d_ls")
for mt in ("acc", "ll"):
    for a_, b_ in (("iso", "pop"), ("trv", "pop"), ("trv", "iso")): out[f"B_{a_}-{b_}_{mt}"] = boot(a_, b_, mt); out[f"B_{a_}-{b_}_{mt}_2way"] = boot2(a_, b_, mt)
A1 = out["A"]["iso"]["logscore"]; Bacc, Bll = out["B_iso-pop_acc"], out["B_iso-pop_ll"]
out["decisions"] = {"identity_on_identical_items": bool(A1[1] > 0), "beneficial_on_shared_panel": bool(A1[1] > 0 and Bacc[1] > 0 and Bll[1] > 0), "sub_threshold": bool(Bacc[2] < 1.0),
                    "trv_advantage_A": bool(out["A"]["trv-iso_logscore"][1] > 0), "trv_advantage_B": bool(out["B_trv-iso_acc"][1] > 0)}
TAG = "_pos" if POSRUN else ""
if POSRUN: out["decisions"]["identity_not_position"] = bool(out["A"]["iso_attr"]["logscore"][1] > 0)
json.dump(out, open(f"{HERE}/results/stage13_s1{TAG}.json", "w"), indent=1); json.dump(A_rows, open(f"{HERE}/results/stage13_s1{TAG}_pairs.json", "w")); print(json.dumps(out), flush=True)
