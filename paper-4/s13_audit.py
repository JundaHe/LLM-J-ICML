"""Stage 13 Am. 4 (PROTOCOL_STAGE13.md): bootstrap sensitivity of endpoint A on the saved pair records — original item x user multinomial bootstrap (centre, item retention),
positive Exp(1) multipliers, prompt-group clustering, fold-level estimates, and the paired joint - position-only contrast. Usage: s13_audit.py <pairs.json> <key> [<key2>]."""
import sys, json, collections, numpy as np
P = json.load(open(sys.argv[1])); key = sys.argv[2]; key2 = sys.argv[3] if len(sys.argv) > 3 else None
val = np.array([x[key] - (x[key2] if key2 else 0.0) for x in P]); it = np.array([x["item"] for x in P]); pr = np.array([x["prompt"] for x in P]); fo = np.array([x["fold"] for x in P])
uq = np.unique([x["u"] for x in P] + [x["v"] for x in P]); ui = np.searchsorted(uq, [x["u"] for x in P]); vi = np.searchsorted(uq, [x["v"] for x in P]); iq, ii = np.unique(it, return_inverse=True)
ip = {}                                                                     # item -> prompt cluster
for a, b in zip(ii, pr): ip[a] = b
pq, pi = np.unique([ip[a] for a in range(len(iq))], return_inverse=True)
def est(wi, wu):
    w = wu[ui] * wu[vi]; num = np.bincount(ii, w * val, len(iq)); den = np.bincount(ii, w, len(iq)); m = den > 0
    return (wi[m] * num[m] / den[m]).sum() / wi[m].sum(), m
pt, _ = est(np.ones(len(iq)), np.ones(len(uq))); rng = np.random.RandomState(17); B = 1000; out = {"estimate": float(pt), "n_pairs": len(P), "n_items": len(iq), "n_users": len(uq), "n_prompts": len(pq)}
npi = np.bincount(ii, minlength=len(iq)); kept = np.zeros(len(iq)); bs = []
for _ in range(B):
    wi = np.bincount(rng.randint(0, len(iq), len(iq)), minlength=len(iq)).astype(float); wu = np.bincount(rng.randint(0, len(uq), len(uq)), minlength=len(uq)).astype(float); e, m = est(wi, wu); bs.append(e); kept += m
bs = np.array(bs); out["multinomial"] = {"ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "boot_mean": float(bs.mean()), "boot_median": float(np.median(bs))}
out["item_retention_by_pairs"] = {lab: float((kept / B)[sel].mean()) for lab, sel in (("1 pair", npi == 1), ("2-3 pairs", (npi >= 2) & (npi <= 3)), ("4-9 pairs", (npi >= 4) & (npi <= 9)), (">=10 pairs", npi >= 10)) if sel.any()}
bs = np.array([est(rng.exponential(1, len(iq)), rng.exponential(1, len(uq)))[0] for _ in range(B)]); out["exp_multiplier"] = {"ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "boot_mean": float(bs.mean())}
bs = []
for _ in range(B):
    wp = np.bincount(rng.randint(0, len(pq), len(pq)), minlength=len(pq)).astype(float)[pi]; wu = np.bincount(rng.randint(0, len(uq), len(uq)), minlength=len(uq)).astype(float); bs.append(est(wp, wu)[0])
out["prompt_cluster"] = {"ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
out["by_fold"] = {int(f): float(np.mean([np.mean(val[(fo == f) & (ii == a)]) for a in np.unique(ii[fo == f])])) for f in np.unique(fo)}
print(json.dumps(out))
