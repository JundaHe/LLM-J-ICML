"""R19-1 (ROUND19_PROTOCOL.md): X = X_own + X_cross decomposition on the dense panels, otherwise identical to rho_exact.py.
Original doc: ρ_exact = X/M with the EXACT mode+mean comparator (the construct of §2), point estimate + item-cluster bootstrap (fixed boot_items), at a = m−1 (small panels, loo) and on the dense curves.
Writes results/rho_own/<panel>.json. Usage: python rho_exact.py --panel bw [--R 10 --B 200]"""
import os, sys, json, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, boot_items, ci
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--R", type=int, default=10); ap.add_argument("--B", type=int, default=200); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; n, m = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(n))); NOM = args.panel.startswith("chaosnli"); P = Panel(K, NOM); C = P.C
def est(Hm, g, a, b, reps, loo, fold_seed):
    acc = np.zeros(5)
    for r in reps:
        H1, Y2 = splits(Hm, a, b, r, r if loo else None); h1 = P.hist(H1); h2 = P.hist(Y2); fo = folds_for(g, fold_seed)
        z, t, key, stat = P.T_of(H1); q = P.exactT_q(fo, z, key, stat, h1)
        z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(fo, z2, key2, stat2, h2)
        r1 = C(h1 - q); r2 = C(h2 - q); r2o = C(h2 - q2); rc = C(q2 - q)
        acc += [(r1 * r2).sum(1).mean() / P.NRM, (r1 * r2o).sum(1).mean() / P.NRM, (r1 * rc).sum(1).mean() / P.NRM, (r1 ** 2).sum(1).mean() / P.NRM, (r2o ** 2).sum(1).mean() / P.NRM]
    return acc / len(reps)
out = {"panel": args.panel, "m": int(m), "rows": []}
A_LIST = [a for a in (2, 3, 5, 8, 10, 15, 20, 30, 40) if a + 20 <= m]
assert m > 12
NAMES = ["X", "X_own", "X_cross", "M", "M_own"]
for a in A_LIST:
    loo = False; b = 20
    pt = est(H, G0, a, b, range(args.R), loo, 1); brng = np.random.RandomState(11 + a); bs = []
    for bi in range(args.B):
        idx, ng = boot_items(G0, brng); v = est(H[idx], ng, a, b, range(100 + 3 * bi, 103 + 3 * bi), loo, 1000 + bi); bs.append(np.r_[v, v[1] / v[3] if v[3] > 1e-12 else np.nan])
    bs = np.array(bs); row = dict(a=a, **{k: float(pt[i]) for i, k in enumerate(NAMES)}, rho_own=float(pt[1] / pt[3]) if pt[3] > 1e-12 else float("nan"))
    for i, k in enumerate(NAMES + ["rho_own"]): row[k + "_ci"] = ci(list(bs[:, i]))
    out["rows"].append(row)
    print(f"{args.panel} a={a:3d}  X {pt[0]:+.5f} {[round(v,5) for v in row['X_ci']]}  X_own {pt[1]:+.5f} {[round(v,5) for v in row['X_own_ci']]}  X_cross {pt[2]:+.5f} {[round(v,5) for v in row['X_cross_ci']]}  rho_own {row['rho_own']:+.3f}", flush=True)
os.makedirs(f"{HERE}/results/rho_own", exist_ok=True); json.dump(out, open(f"{HERE}/results/rho_own/{args.panel}.json", "w"), indent=1, default=float)
