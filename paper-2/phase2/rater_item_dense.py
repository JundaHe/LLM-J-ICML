"""R19-3 (ROUND19_PROTOCOL.md): do the rater–item models reproduce the dense-panel X, X_own, X_cross (R19-1 decomposition)?
Fits M0/M1/M2 on the full matrix with the helpers of rater_item_model.py (λ_σ as selected there), simulates 20 matrices per model,
and computes the decomposition at a ∈ {10, 20, 40}, b = 20 on observed and simulated matrices. Writes results/rater_item_dense/<panel>.json.
Usage: python rater_item_dense.py --panel bw [--sims 20 --R 5]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
panel = sys.argv[sys.argv.index("--panel") + 1]
SIMS = int(sys.argv[sys.argv.index("--sims") + 1]) if "--sims" in sys.argv else 20
R = int(sys.argv[sys.argv.index("--R") + 1]) if "--R" in sys.argv else 5
TAG = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""   # R23-2: write to <panel><tag>.json
LAM = json.load(open(f"{HERE}/results/rater_item/{panel}.json"))["lam_sigma_selected"]
src = open(f"{HERE}/rater_item_model.py").read(); src = src[:src.index("t0 = time.time(); res")]   # model definitions only
sys.argv = ["rater_item_model.py", "--panel", panel, "--lam_sigma", str(LAM)]; exec(compile(src, "rater_item_model.py", "exec"))
NAMES = ("X", "X_own", "X_cross")
def decomp(Hmat, a):
    groups = np.asarray(PAN.get("groups", np.arange(n))); acc = np.zeros(3)
    for r in range(R):
        H1, Y2 = splits(Hmat, a, 20, r); h1 = P.hist(H1); h2 = P.hist(Y2); fo = folds_for(groups, 1)
        z, t, key, stat = P.T_of(H1); q = P.exactT_q(fo, z, key, stat, h1)
        z2, t2, key2, stat2 = P.T_of(Y2); q2 = P.exactT_q(fo, z2, key2, stat2, h2); r1 = C(h1 - q)
        acc += [(r1 * C(h2 - q)).sum(1).mean() / P.NRM, (r1 * C(h2 - q2)).sum(1).mean() / P.NRM, (r1 * C(q2 - q)).sum(1).mean() / P.NRM]
    return acc / R
A_LIST = [a for a in (10, 20, 40) if a + 20 <= m]
out = dict(panel=panel, lam_sigma=LAM, sims=SIMS, R=R, observed={}, sim={}, protocol="ROUND19_PROTOCOL.md R19-3")
for a in A_LIST: out["observed"][a] = dict(zip(NAMES, map(float, decomp(H, a))))
print(panel, "observed", out["observed"], flush=True)
full = torch.ones(n, m); MODELS = [0, 1, 2] if NG > 1 else [0, 2]   # as in rater_item_model.py
for mdl in MODELS:
    par = fit(mdl, full, LAM if mdl == 2 else None); srng = np.random.RandomState(200 + mdl); vals = {a: [] for a in A_LIST}
    for s in range(SIMS):
        Hs = simulate(par, mdl, srng)
        for a in A_LIST: vals[a].append(decomp(Hs, a))
    out["sim"][f"M{mdl}"] = {a: {k: dict(mean=float(np.mean([v[i] for v in vals[a]])), range95=ci([v[i] for v in vals[a]])) for i, k in enumerate(NAMES)} for a in A_LIST}
    print(panel, f"M{mdl}", {a: {k: round(d["mean"], 5) for k, d in out["sim"][f"M{mdl}"][a].items()} for a in A_LIST}, flush=True)
amax = max(A_LIST); obs = out["observed"][amax]["X_own"]
rep = {M: (lambda r: r[0] <= obs <= r[1])(out["sim"][M][amax]["X_own"]["range95"]) for M in out["sim"]}
out["reading"] = dict(a=amax, X_own_obs=obs, reproduces_X_own=rep, thresholds_explain_beyond_location=bool(rep.get("M1", False) and not rep["M0"]) if "M1" in rep else None)
print(panel, "reading", out["reading"], flush=True)
os.makedirs(f"{HERE}/results/rater_item_dense", exist_ok=True); json.dump(out, open(f"{HERE}/results/rater_item_dense/{panel}{TAG}.json", "w"), indent=1, default=float)
