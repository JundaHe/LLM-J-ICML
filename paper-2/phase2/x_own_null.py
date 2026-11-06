"""R21-2 (ROUND21_PROTOCOL.md): source of the negative null mean of X_own. Simulates γ = 0 matrices from the panel's fitted M2 model
(item location θ, median dispersion, rater cut-points) under three rater regimes and computes X_own exactly as decode_decomp.py
(random per-item split into a + b positions, exact-T comparator with the same 5 cross-fitting folds):
  pool   — fixed rater per position (as the R20-2 plant): the two halves are drawn without replacement from one finite rater pool;
  common — every rater gets the median cut-points (no rater heterogeneity);
  iid    — each rating's cut-points drawn independently, with replacement, from the rater pool (an infinite population of such raters).
Writes results/x_own_null/<panel>.json. Usage: python x_own_null.py --panel summeval_coherence8 --a 4 [--sims 20 --R 10]"""
import sys, os, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data_panels
from fr_lib import Panel, folds_for, splits
ap = argparse.ArgumentParser(); ap.add_argument("--panel", required=True); ap.add_argument("--a", type=int, required=True); ap.add_argument("--b", type=int, default=None)
ap.add_argument("--sims", type=int, default=20); ap.add_argument("--R", type=int, default=10); args = ap.parse_args()
PAN = data_panels.load(args.panel); K = PAN["K"]; NI, M = PAN["H"].shape; G0 = np.asarray(PAN.get("groups", np.arange(NI)))
b = args.b if args.b is not None else (M - args.a if M <= 12 else min(20, M - args.a))
P = Panel(K, False); C = P.C; NRM = P.NRM
prm = np.load(f"{HERE}/results/rater_item/{args.panel}_M2_params.npz"); cuts = prm["cuts"][prm["rater_group"]]          # M × (K−1)
sig = np.median(prm["sigma"]); med = np.median(cuts, 0)
def simulate(regime, rng):
    ystar = prm["theta"][:, None] + sig * rng.randn(NI, M)
    cu = {"pool": np.broadcast_to(cuts, (NI, M, K - 1)), "common": np.broadcast_to(med, (NI, M, K - 1)),
          "iid": cuts[rng.randint(0, M, (NI, M))]}[regime]
    return (ystar[:, :, None] > cu).sum(2).astype(int)
def x_own(H):
    fo = folds_for(G0, 1); v = []
    for r in range(args.R):
        H1, Y2 = splits(H, args.a, b, r); h1, h2 = P.hist(H1), P.hist(Y2)
        z, t, key, stat = P.T_of(H1); q1 = P.exactT_q(fo, z, key, stat, h1); z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(fo, z2, key2, stat2, h2)
        v.append(float(np.mean((C(h1 - q1) * C(h2 - q2)).sum(1) / NRM)))
    return float(np.mean(v))
out = dict(panel=args.panel, a=args.a, b=b, sims=args.sims, R=args.R, protocol="ROUND21_PROTOCOL.md R21-2", regimes={})
for k, regime in enumerate(("pool", "common", "iid")):
    rng = np.random.RandomState(9000 + k); vals = [x_own(simulate(regime, rng)) for _ in range(args.sims)]
    se = float(np.std(vals, ddof=1) / np.sqrt(len(vals)))
    out["regimes"][regime] = dict(mean=float(np.mean(vals)), se=se, values=vals)
    print(f"{args.panel} a{args.a} b{b} {regime:6s} X_own mean {np.mean(vals):+.6f} ± {se:.6f}", flush=True)
os.makedirs(f"{HERE}/results/x_own_null", exist_ok=True); json.dump(out, open(f"{HERE}/results/x_own_null/{args.panel}.json", "w"), indent=1)
