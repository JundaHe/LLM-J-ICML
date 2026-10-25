"""Post-rescaling dose certificate for the ChaosNLI pzc intervention (Codex round 13): mirrors probe_nominal's split / cell / matching / rescaling exactly (no training) and
reports, per m, the fraction of training items whose FINAL target differs from their histogram (TV > 1e-9), the final TV over all items, and the donor-level mapped fraction.
Usage: python nominal_final_dose.py -> results/nominal_final_dose.json"""
import os, sys, json, math, itertools, argparse, numpy as np
from paths import LLMJ
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import random_max_matching
from targets import nominal_zc
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", default="chaosnli_mnli"); args = ap.parse_args()
PAN = data_panels.load(args.panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]; n_ref = 50; cbin = 0.1
def hist_of(Hs): return np.stack([np.bincount(r, minlength=K) for r in Hs]) / Hs.shape[1]
out = {}
for m in (5, 10, 20, 50):
    rows = []
    for seed, isplit in itertools.product(range(3), range(3)):
        rng = np.random.RandomState(seed * 1000 + isplit)
        ids = np.random.RandomState(isplit).permutation(N); tr = ids[: int(.6 * N)]
        pos = np.random.RandomState(900 + isplit).permutation(M); P_train = pos[:m]
        Htr = H0[np.ix_(tr, P_train)]; hist = hist_of(Htr); z = hist.argmax(1); c = hist.max(1); cb = np.floor(c / cbin).astype(int)
        # the probe draws the mode-only permutation first (rng consumption order matters), then the zc one
        rec = {}
        for kind in ("mode", "zc"):
            cells = {}
            for i in range(len(tr)): cells.setdefault((int(z[i]), int(cb[i]) if kind == "zc" else 0), []).append(i)
            mp = {}
            for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(Htr[i], minlength=K)) for i in items], rng))
            T = hist.copy()
            for a, b in mp.items(): T[a] = nominal_zc(hist[b], z[a], c[a]) if kind == "zc" else hist[b]
            tvf = 0.5 * np.abs(T - hist).sum(1); tvd = np.array([0.5 * np.abs(hist[a] - hist[b]).sum() for a, b in mp.items()])
            f32 = np.any(T.astype(np.float32) != hist.astype(np.float32), axis=1)
            rec[kind] = dict(mapped=len(mp) / len(tr), donor_tv_zero=int((tvd < 1e-12).sum()), final_changed=float((tvf > 1e-9).mean()), final_changed_1e8=float((tvf > 1e-8).mean()), final_changed_1e6=float((tvf > 1e-6).mean()), final_changed_f32=float(f32.mean()),
                             final_tv_all=float(tvf.mean()), final_tv_changed=float(tvf[tvf > 1e-9].mean()) if (tvf > 1e-9).any() else 0.0)
        rows.append(rec)
    out[m] = {kind: {k: float(np.mean([r[kind][k] for r in rows])) for k in rows[0][kind]} for kind in ("mode", "zc")}
    z = out[m]['zc']; print(f"m={m}: pzc mapped {z['mapped']:.3f} | changed @f32 {z['final_changed_f32']:.3f} @1e-9 {z['final_changed']:.3f} @1e-8 {z['final_changed_1e8']:.3f} @1e-6 {z['final_changed_1e6']:.3f} | final_tv_all {z['final_tv_all']:.3f} | pmode tv_all {out[m]['mode']['final_tv_all']:.3f}", flush=True)
json.dump(out, open(f"{HERE}/results/nominal_final_dose{'' if args.panel == 'chaosnli_mnli' else '_' + args.panel}.json", "w"), indent=1)
