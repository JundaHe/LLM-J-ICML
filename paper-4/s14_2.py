"""Stage 14 S14-2 (PROTOCOL_STAGE14.md §2): are the Stage 12 gains concentrated on contested comparisons? Executes the s12.py source with two hooks (the population
model's |logit| threshold per fold; the stratum of every test pair) and stops before the Stage 12 output is written. Contested = |lg_pop| below the 20th percentile over
that fold's training users × training items. User bootstrap (seed 17, B = 2000; primary) and prompt-group × user two-way bootstrap (B = 1000; secondary).
Usage: CA_PANEL=ca_pairs_second python s14_2.py   → results/stage14_2_<panel>.json"""
import os, json, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ.setdefault("CA_PANEL", "ca_pairs_second")
src = open(f"{HERE}/s12.py").read()
for a, b in (('lg_pop = (base + (MU[Rt] * A).sum(1)).numpy()', 'lg_pop = (base + (MU[Rt] * A).sum(1)).numpy(); THR = float(np.percentile(np.abs(lg_pop[idx_all]), 20)); THRS.append(THR)'),
             ('PAIR["te"].append(te)', 'PAIR["te"].append(te); PAIR["con"].append(np.abs(lg_pop[te]) < THR); PAIR["draw"].append(np.full(len(te), dr))')):
    assert src.count(a) == 1, a; src = src.replace(a, b)
THRS = []; exec(compile(src[:src.index('out = {"info": info}')], "s12.py", "exec"))
te = np.concatenate(PAIR["te"]); con = np.concatenate(PAIR["con"]); dr = np.concatenate(PAIR["draw"]); u = R[te]; S = {"all": np.ones(len(te), bool), "contested": con, "rest": ~con}
def per_user(v, m):
    """per test user: mean over support draws of the stratum sum of v and of the stratum count"""
    uu, ui = np.unique(u, return_inverse=True); nd = np.array([len(np.unique(dr[ui == j])) for j in range(len(uu))]); return np.bincount(ui, v * m) / nd, np.bincount(ui, m.astype(float)) / nd
def boot(v):
    D = {s: per_user(v, m) for s, m in S.items()}; n = len(D["all"][0]); rng = np.random.RandomState(17); ix = [rng.randint(0, n, n) for _ in range(2000)]; o = {}
    est = lambda s, i: D[s][0][i].sum() / max(D[s][1][i].sum(), 1e-9); A_ = np.arange(n)
    for s in S: bs = [est(s, i) for i in ix]; o[s] = [100 * est(s, A_), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)]
    bs = [est("contested", i) - est("rest", i) for i in ix]; o["contested-rest"] = [100 * (est("contested", A_) - est("rest", A_)), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)]; return o
def boot2(v, B=1000):
    uq, qi = np.unique(te, return_inverse=True); dp = np.bincount(qi, v) / np.bincount(qi); cq = np.zeros(len(uq), bool); cq[qi] = con; pu = np.unique(R[uq], return_inverse=True)[1]; pg = np.unique(Gp[uq], return_inverse=True)[1]
    M = {"all": np.ones(len(uq)), "contested": cq.astype(float), "rest": 1.0 - cq}; rng = np.random.RandomState(17); bs = collections.defaultdict(list)
    for _ in range(B):
        w = np.bincount(rng.randint(0, pu.max() + 1, pu.max() + 1), minlength=pu.max() + 1)[pu] * np.bincount(rng.randint(0, pg.max() + 1, pg.max() + 1), minlength=pg.max() + 1)[pg]
        e = {s: (w * m * dp).sum() / max((w * m).sum(), 1) for s, m in M.items()}; e["contested-rest"] = e["contested"] - e["rest"]
        for s, x in e.items(): bs[s].append(x)
    pt = {s: (m * dp).sum() / m.sum() for s, m in M.items()}; pt["contested-rest"] = pt["contested"] - pt["rest"]
    return {s: [100 * pt[s], 100 * np.percentile(bs[s], 2.5), 100 * np.percentile(bs[s], 97.5)] for s in pt}
V = lambda m_, mt: np.concatenate(PAIR[(m_, mt)])
out = {"panel": PAN["name"], "protocol": "PROTOCOL_STAGE14.md S14-2", "thresholds": THRS, "share_contested": float(con.mean()), "n_pairs": int(len(np.unique(te))), "n_users": int(len(np.unique(u))),
       "pop_acc": {s: float(100 * V("pop", "acc")[m].mean()) for s, m in S.items()}}
for a_ in ("trv", "iso"):
    for mt in ("acc", "ll"): d = V(a_, mt) - V("pop", mt); out[f"{a_}-pop_{mt}"] = boot(d); out[f"{a_}-pop_{mt}_2way"] = boot2(d)
ref = json.load(open(f"{HERE}/results/stage12_{PAN['name']}.json")); chk = {mt: [out[f"trv-pop_{mt}"]["all"][0], ref[f"trv-pop_{mt}"][0]] for mt in ("acc", "ll")}
out["sanity_stage12"] = chk; out["sanity_ok"] = bool(all(abs(a - b) < 0.005 for a, b in chk.values()))
ta, tl = out["trv-pop_acc"], out["trv-pop_ll"]
out["decisions"] = {"practically_meaningful_on_contested": bool(ta["contested"][1] > 1.0), "concentration_acc": bool(ta["contested-rest"][1] > 0), "concentration_ll": bool(tl["contested-rest"][1] > 0),
                    "concentration": bool(ta["contested-rest"][1] > 0 and tl["contested-rest"][1] > 0)}
json.dump(out, open(f"{HERE}/results/stage14_2_{PAN['name']}.json", "w"), indent=1); print(json.dumps(out), flush=True)
