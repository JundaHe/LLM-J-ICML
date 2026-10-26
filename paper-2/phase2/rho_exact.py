"""ρ_exact = X/M with the EXACT mode+mean comparator (the construct of §2), point estimate + item-cluster bootstrap (fixed boot_items), at a = m−1 (small panels, loo) and on the dense curves.
Writes results/rho_exact/<panel>.json. Usage: python rho_exact.py --panel bw [--R 10 --B 200]"""
import os, sys, json, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "2")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits, boot_items, ci
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--R", type=int, default=10); ap.add_argument("--B", type=int, default=200); args = ap.parse_args()
PAN = data_panels.load(args.panel); H = PAN["H"].astype(int); K = PAN["K"]; n, m = H.shape; G0 = np.asarray(PAN.get("groups", np.arange(n))); NOM = args.panel.startswith("chaosnli"); P = Panel(K, NOM); C = P.C
def est(Hm, g, a, b, reps, loo, fold_seed):
    X = M = A = 0.0
    for r in reps:
        H1, Y2 = splits(Hm, a, b, r, r if loo else None); h1 = P.hist(H1); h2 = P.hist(Y2); z, t, key, stat = P.T_of(H1); q = P.exactT_q(folds_for(g, fold_seed), z, key, stat, h1)
        r1 = C(h1 - q); r2 = C(h2 - q); X += (r1 * r2).sum(1).mean() / P.NRM; M += (r1 ** 2).sum(1).mean() / P.NRM; A += (P.score(h1, Y2) - P.score(q, Y2)).mean()
    k = len(reps); return X / k, M / k, A / k
out = {"panel": args.panel, "m": int(m), "rows": []}
A_LIST = [m - 1] if m <= 12 else [a for a in (2, 3, 5, 8, 10, 15, 20, 30, 40) if a + 20 <= m]
for a in A_LIST:
    loo = m <= 12; b = 1 if loo else 20
    X, M, A = est(H, G0, a, b, range(args.R), loo, 1); brng = np.random.RandomState(11 + a); bx, br, ba = [], [], []
    for bi in range(args.B):
        idx, ng = boot_items(G0, brng); x, mm, aa = est(H[idx], ng, a, b, range(100 + 3 * bi, 103 + 3 * bi) if not loo else [bi % args.R], loo, 1000 + bi); bx.append(x); br.append(x / mm if mm > 1e-12 else np.nan); ba.append(aa)
    row = dict(a=a, X=X, M=M, rho=X / M if M > 1e-12 else float("nan"), A1x=A, X_ci=ci(bx), rho_ci=ci(br), A1x_ci=ci(ba)); out["rows"].append(row)
    print(f"{args.panel} a={a:3d}  X_exact {X:+.5f} {[round(v,5) for v in row['X_ci']]}  ρ_exact {row['rho']:+.3f} {[round(v,3) for v in row['rho_ci']]}  A1x {A:+.5f}", flush=True)
os.makedirs(f"{HERE}/results/rho_exact", exist_ok=True); json.dump(out, open(f"{HERE}/results/rho_exact/{args.panel}.json", "w"), indent=1, default=float)
