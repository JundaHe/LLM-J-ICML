"""R19-6 (ROUND19_PROTOCOL.md): crossed item × rater bootstrap for the R19-1 dense rows on complete crossed panels (bw, dices, dices990).
Each replicate resamples item clusters and, independently, rater columns with replacement (multiplicities w); per item, P1 ∪ P2 = a+b DISTINCT raters drawn
without replacement with probability ∝ w (Efraimidis–Spirakis keys), first a → P1. Point estimates are the rho_own rows. Writes results/rho_crossed/<panel>.json.
Usage: python rho_crossed.py --panel bw [--B 200]"""
import os, sys, json, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, boot_items, ci
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--B", type=int, default=200); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; n, m = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(n))); P = Panel(K, False); C = P.C
B_RATERS = 20
def split_w(Hm, w, a, b, rng):
    keys = np.where(w > 0, rng.rand(len(Hm), m) ** (1.0 / np.maximum(w, 1e-12)), -1.0)   # Efraimidis–Spirakis: top-(a+b) keys = weighted sample w/o replacement
    sel = np.argsort(-keys, 1)[:, :a + b]
    return np.take_along_axis(Hm, sel[:, :a], 1), np.take_along_axis(Hm, sel[:, a:], 1)
def est(Hm, g, w, a, b, seeds, fold_seed):
    acc = np.zeros(5)
    for s in seeds:
        H1, Y2 = split_w(Hm, w, a, b, np.random.RandomState(100003 * a + s)); h1 = P.hist(H1); h2 = P.hist(Y2); fo = folds_for(g, fold_seed)
        z, t, key, stat = P.T_of(H1); q = P.exactT_q(fo, z, key, stat, h1)
        z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(fo, z2, key2, stat2, h2)
        r1 = C(h1 - q)
        acc += [(r1 * C(h2 - q)).sum(1).mean() / P.NRM, (r1 * C(h2 - q2)).sum(1).mean() / P.NRM, (r1 * C(q2 - q)).sum(1).mean() / P.NRM, (r1 ** 2).sum(1).mean() / P.NRM, (C(h2 - q2) ** 2).sum(1).mean() / P.NRM]
    return acc / len(seeds)
own = {r["a"]: r for r in json.load(open(f"{HERE}/results/rho_own/{args.panel}.json"))["rows"]}
A_LIST = [a for a in (10, 20, 40) if a + B_RATERS <= 0.6 * m]
out = {"panel": args.panel, "m": int(m), "B": args.B, "protocol": "ROUND19_PROTOCOL.md R19-6", "rows": []}
for a in A_LIST:
    brng = np.random.RandomState(11 + a); bs = []; redraws = 0
    for bi in range(args.B):
        idx, ng = boot_items(G0, brng)
        while True:
            w = np.bincount(brng.randint(0, m, m), minlength=m).astype(float)
            if (w > 0).sum() >= a + B_RATERS: break
            redraws += 1
        v = est(H[idx], ng, w, a, B_RATERS, range(100 + 3 * bi, 103 + 3 * bi), 1000 + bi)
        bs.append([v[0], v[1], v[2], v[0] / v[3] if v[3] > 1e-12 else np.nan, v[1] / v[3] if v[3] > 1e-12 else np.nan])
    bs = np.array(bs); o = own[a]
    row = dict(a=a, redraws=redraws, X=o["X"], X_own=o["X_own"], rho=o["X"] / o["M"], rho_own=o["rho_own"], item_only=dict(X=o["X_ci"], X_own=o["X_own_ci"], rho_own=o["rho_own_ci"]))
    for i, k in enumerate(["X", "X_own", "X_cross", "rho", "rho_own"]): row[k + "_crossed_ci"] = ci(list(bs[:, i]))
    out["rows"].append(row)
    print(f"{args.panel} a={a:3d} rho {row['rho']:+.3f} crossed {[round(x,3) for x in row['rho_crossed_ci']]}  rho_own {row['rho_own']:+.3f} item {[round(x,3) for x in o['rho_own_ci']]} crossed {[round(x,3) for x in row['rho_own_crossed_ci']]}  X {o['X']:+.5f} item {[round(x,5) for x in o['X_ci']]} crossed {[round(x,5) for x in row['X_crossed_ci']]}  redraws {redraws}", flush=True)
amax = max(A_LIST); r = [x for x in out["rows"] if x["a"] == amax][0]
out["reading"] = dict(a=amax, rho_crossed_upper=r["rho_crossed_ci"][1], population_claim_stands=bool(r["rho_crossed_ci"][1] < 0.5))
print(args.panel, "reading", out["reading"], flush=True)
os.makedirs(f"{HERE}/results/rho_crossed", exist_ok=True); json.dump(out, open(f"{HERE}/results/rho_crossed/{args.panel}.json", "w"), indent=1, default=float)
