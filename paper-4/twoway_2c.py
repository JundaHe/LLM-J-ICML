"""Stage 2c Amendment 5: two-way (rater × prompt-group) pigeonhole bootstrap of the MultiPref k = 20 contrasts and own gains m(20) − m(0), from vpl_pal.py --dump_ratings
(tag _A2tw); reproduction check against the primary Amendment-2 per-rater rows."""
import json, glob, os, collections, numpy as np, scipy.sparse as sp
HERE = os.path.dirname(os.path.abspath(__file__)); R_ = os.path.join(HERE, "results"); B = 2000; rng = np.random.RandomState(11); out = {}
L = ["# Two-way bootstrap (Stage 2c Amendment 5) — MultiPref, k = 20", "", "Raters and prompt groups resampled independently, B = 2,000; per-rating values averaged over the 5 adaptation draws. Own gain = the same method at k = 20 minus k = 0 on the same ratings.", ""]
def boot(rk, gk, d, ok):
    key = np.stack([rk, gk], 1); u, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
    num = np.bincount(inv, np.where(ok, d, 0.0)); den = np.bincount(inv, ok.astype(float))
    ru, ri = np.unique(u[:, 0], return_inverse=True); gu, gi = np.unique(u[:, 1], return_inverse=True)
    A = sp.csr_matrix((num, (ri.ravel(), gi.ravel())), shape=(len(ru), len(gu))); N = sp.csr_matrix((den, (ri.ravel(), gi.ravel())), shape=(len(ru), len(gu)))
    bs_r, bs_2 = [], []
    for _ in range(B):
        wr = np.bincount(rng.randint(0, len(ru), len(ru)), minlength=len(ru)).astype(float); wg = np.bincount(rng.randint(0, len(gu), len(gu)), minlength=len(gu)).astype(float)
        bs_r.append((wr @ A).sum() / (wr @ N).sum()); bs_2.append((wr @ A @ wg) / (wr @ N @ wg))
    return float(A.sum() / N.sum()), np.percentile(bs_r, [2.5, 97.5]), np.percentile(bs_2, [2.5, 97.5])
def prim_contrast(rows, a, b, mt, den, k=20):
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k: by[(r["fold"], r["rater"])].append(r)
    return sum(np.mean([x[f"{a}_{mt}"] - x[f"{b}_{mt}"] for x in v]) for v in by.values()) / sum(np.mean([x[den] for x in v]) for v in by.values())
def prim_own(rows, m, mt, den):
    z0 = {(r["fold"], r["rater"]): r for r in rows if r["k"] == 0}; by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == 20 and (r["fold"], r["rater"]) in z0: by[(r["fold"], r["rater"])].append(r)
    return sum(np.mean([x[f"{m}_{mt}"] for x in v]) - z0[z][f"{m}_{mt}"] for z, v in by.items()) / sum(np.mean([x[den] for x in v]) for v in by.values())
for ev in ("E1", "E2"):
    D = [np.load(f) for f in sorted(glob.glob(f"{R_}/ratings/stage2c_{ev}_f?_A2tw.npz"))]
    if len(D) < 5: L.append(f"## {ev}: only {len(D)} folds dumped — skipped"); continue
    Z = {k: np.concatenate([d[k] for d in D]) for k in D[0].files}; M = sorted({k[:-3] for k in Z if k.endswith("_ll")})
    prim = [r for f in sorted(glob.glob(f"{R_}/stage2c_{ev}_f?_A2.json")) for r in json.load(open(f))["per_rater"]]
    rk_all = Z["fold"] * 100000 + Z["rater"]; key_all = rk_all * 10**7 + Z["item"]
    def per_rating(k, col):                                              # mean over draws for each (fold, rater, item) at this k
        s = Z["k"] == k; u, inv = np.unique(key_all[s], return_inverse=True); inv = inv.ravel(); v = Z[col][s]; ok = np.isfinite(v)
        return u, np.bincount(inv, np.where(ok, v, 0.0)) / np.maximum(np.bincount(inv, ok.astype(float)), 1), np.bincount(inv, ok.astype(float)) > 0
    s20 = Z["k"] == 20; u20 = np.unique(key_all[s20]); gmap = dict(zip(key_all[s20], np.unique(np.asarray(Z["igroup"]).astype(str), return_inverse=True)[1].ravel()[s20]))
    gk = np.array([gmap[x] for x in u20]); rk = u20 // 10**7
    acc = "direction acc." if ev == "E1" else "binary acc."; den_dir = "n_dir" if ev == "E1" else "n"
    L += [f"## {ev} ({'graded' if ev == 'E1' else 'binary'})", "", "| quantity | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |", "|---|---|---|---|---|---|"]
    rowsets = [(f"{a} − {b}", "c", a, b) for a, b in (("DFsp", "VPL"), ("DFsp", "PAL2"), ("DFsp", "Dp"), ("VPL", "Dp")) if a in M and b in M] + [(f"own gain {m}", "o", m, None) for m in ("DFp", "DFsp", "VPL", "PAL2", "PAL4") if m in M]
    for name, typ, a, b in rowsets:
        for mt in ("ll", "dir"):
            ua, va, oa = per_rating(20, f"{a}_{mt}")
            if typ == "c": ub, vb, ob = per_rating(20, f"{b}_{mt}"); pp = prim_contrast(prim, a, b, mt, "n" if mt == "ll" else den_dir)
            else: ub, vb, ob = per_rating(0, f"{a}_{mt}"); pp = prim_own(prim, a, mt, "n" if mt == "ll" else den_dir)
            ib = dict(zip(ub, range(len(ub)))); j = np.array([ib.get(x, -1) for x in ua]); ok = oa & (j >= 0) & ob[np.maximum(j, 0)]
            d = va - vb[np.maximum(j, 0)]; assert np.array_equal(ua, u20)
            pt, cr, c2 = boot(rk, gk, d, ok); out[f"{ev}_{name}_{mt}"] = {"point": pt, "primary": float(pp), "rater": cr.tolist(), "twoway": c2.tolist()}
            L.append(f"| {name} | {'LL per rating' if mt == 'll' else acc} | {pt:+.4f} | {pp:+.4f} | [{cr[0]:+.4f}, {cr[1]:+.4f}] | [{c2[0]:+.4f}, {c2[1]:+.4f}] |")
    L += ["", f"Reproduction check: |rerun − primary| ≤ 1e-3 for every {ev} row: {all(abs(v['point'] - v['primary']) <= 1e-3 for k_, v in out.items() if k_.startswith(ev))}.", ""]
json.dump(out, open(f"{R_}/stage2c_twoway.json", "w"), indent=1); open(f"{R_}/stage2c_twoway.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
