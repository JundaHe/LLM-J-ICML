"""Stage 11 Am. 11 (PROTOCOL_STAGE11.md): paired intervals for the Am.-9 factorial contrasts; Am.-8 matched-other bootstrap with re-matching."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PART = sys.argv[1]
if PART == "fact":
    exec(open(f"{HERE}/s11_fact.py").read().split('ok = sorted(ok); OUT["n_users"] = len(ok)')[0]); ok = sorted(ok)
    col = NAMES.index("length"); s2W = sel_s2(LG["W"], np.where(isb)[0], col); G = {}
    for P_ in ("W", "O"):
        for S_ in ("E", "G"):
            g_, nn = [], []
            for u in ok:
                s2 = s2W if P_ == "W" else S2["O"]["length"][rfold[u]]; js = np.array([j for e in SUP[S_][u] for j in e]); d = map_dev(LG[P_][js], An[js, col], Yn[js], s2)[0]
                t = np.array(TEST[S_][u]); y = Yn[t]; lp = LG[P_][t]; lo = lp + d * An[t, col]; g_.append(((lo > 0) == y).sum() - ((lp > 0) == y).sum()); nn.append(len(t))
            G[P_ + S_] = (np.array(g_, float), np.array(nn, float))
    rng = np.random.RandomState(17); BS = [rng.randint(0, len(ok), len(ok)) for _ in range(2000)]; out = {"n_users": len(ok)}
    rate = lambda c, ix: G[c][0][ix].sum() / G[c][1][ix].sum()
    for a_, b_ in (("WE", "OE"), ("WG", "OG"), ("WG", "WE"), ("OG", "OE")):
        allx = np.arange(len(ok)); bs = [100 * (rate(a_, ix) - rate(b_, ix)) for ix in BS]; out[f"{a_}-{b_}"] = [100 * (rate(a_, allx) - rate(b_, allx)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    print(json.dumps(out), flush=True); json.dump(out, open(f"{HERE}/results/stage11_am11_fact.json", "w"), indent=1)
else:
    exec(open(f"{HERE}/s11_mix.py").read().split("# ---- (1) within-task-type transfer")[0])
    users = np.array(sorted(SUP)); D = {u: map_dev(lgb[np.concatenate(SUP[u])], a1[np.concatenate(SUP[u])], Yn[np.concatenate(SUP[u])], S2[u]) for u in users}
    H = np.array([np.bincount([CLS[8][e[0]] for e in SUP[u]], minlength=8) / 16 for u in users]); Lg = ulang[users]
    def sc(u, d):
        t = TEST[u]; lg = lgb[t] + d * a1[t]; y = Yn[t]; return ((lg > 0) == y).sum(), (y * -np.logaddexp(0, -lg) + (1 - y) * -np.logaddexp(0, lg)).sum(), len(t)
    own = np.array([sc(u, D[u]) for u in users], float); Dv = np.array([D[u] for u in users])
    def contrast(ix):
        tot = np.zeros(3); oth = np.zeros(2)
        for l in np.unique(Lg[ix]):
            m = ix[Lg[ix] == l]
            for i in m:
                dist = np.abs(H[m] - H[i]).sum(1); dist[m == i] = np.inf
                if not np.isfinite(dist).any(): continue
                j = m[int(np.argmin(dist))]; o = sc(users[i], Dv[j]); tot += own[i]; oth += o[:2]
        return 100 * (tot[0] - oth[0]) / tot[2], (tot[1] - oth[1]) / tot[2]
    allx = np.arange(len(users)); pt = contrast(allx); rng = np.random.RandomState(17); bs = []
    for b in range(300):
        ix = np.concatenate([rng.choice(np.where(Lg == l)[0], (Lg == l).sum()) for l in np.unique(Lg)]); bs.append(contrast(ix))
    bs = np.array(bs); out = {"own-match_acc": [pt[0], float(np.percentile(bs[:, 0], 2.5)), float(np.percentile(bs[:, 0], 97.5))], "own-match_ll": [pt[1], float(np.percentile(bs[:, 1], 2.5)), float(np.percentile(bs[:, 1], 97.5))], "B": 300}
    print(json.dumps(out), flush=True); json.dump(out, open(f"{HERE}/results/stage11_am11_match.json", "w"), indent=1)
