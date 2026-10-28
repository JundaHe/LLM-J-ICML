"""Stage 2 Amendment 9: two-way (rater × item-cluster) pigeonhole bootstrap of the k = 20 headline contrasts, from the per-rating dumps of factorised_rm.py --dump_ratings.
Also checks that the rerun reproduces the primary per-rater-run point estimates. Usage: twoway_boot.py <panel> <primary-tag>"""
import json, glob, os, sys, collections, numpy as np, scipy.sparse as sp
HERE = os.path.dirname(os.path.abspath(__file__)); R_ = os.path.join(HERE, "results"); panel, ptag = sys.argv[1], sys.argv[2]; B = 2000; rng = np.random.RandomState(9)
D = [np.load(f) for f in sorted(glob.glob(f"{R_}/ratings/stage2a_{panel}_tw_f?.npz"))]; Z = {k: np.concatenate([d[k] for d in D]) for k in D[0].files}
MODELS = sorted({k[:-3] for k in Z if k.endswith("_ll")}); folds = sorted(set(Z["fold"].tolist()))
prim = json.load(open(f"{R_}/stage2a_{panel}{ptag}.json"))["per_rater"]
def rate_from_rows(rows, k, a, b, mt, den):                              # primary-style estimate: per-rater mean over draws, pooled
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k and r["fold"] in folds: by[(r["fold"], r["rater"])].append(r)
    return sum(np.mean([x[f"{a}_{mt}"] - x[f"{b}_{mt}"] for x in v]) for v in by.values()) / sum(np.mean([x[den] for x in v]) for v in by.values())
L = [f"# Two-way bootstrap (Stage 2 Amendment 9) — {panel}, k = 20, folds {folds}", "", "Raters and item clusters (prompt groups) resampled independently (pigeonhole bootstrap), B = 2,000. Per-rating differences are averaged over the 5 adaptation draws within each rating.", "",
     "| contrast | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |", "|---|---|---|---|---|---|"]; out = {}
sel = Z["k"] == 20
for a, b in [(a, b) for a, b in (("DF", "D"), ("DFs", "D"), ("DG", "D"), ("DF", "DG"), ("DFs", "DG")) if a in MODELS and b in MODELS]:
    for mt in ("ll", "dir"):
        d = Z[f"{a}_{mt}"][sel] - Z[f"{b}_{mt}"][sel]; ok = np.isfinite(d); d = np.where(ok, d, 0.0)
        rt = Z["fold"][sel] * 100000 + Z["rater"][sel]; key = np.stack([rt, Z["item"][sel]], 1)             # average draws within (rater, item)
        u, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel(); cnt = np.bincount(inv); num = np.bincount(inv, d) / cnt; den = np.bincount(inv, ok.astype(float)) / cnt
        gl = np.asarray(Z["igroup"][sel]).astype(str); gi = np.unique(gl, return_inverse=True)[1].ravel(); ig = np.zeros(len(u), int); ig[inv] = gi
        ru, ri = np.unique(u[:, 0], return_inverse=True); ri = ri.ravel(); NRr, NGg = len(ru), ig.max() + 1
        A = sp.csr_matrix((num, (ri, ig)), shape=(NRr, NGg)); N = sp.csr_matrix((den, (ri, ig)), shape=(NRr, NGg))
        pt = A.sum() / N.sum(); prim_pt = rate_from_rows(prim, 20, a, b, mt, "n" if mt == "ll" else "n_dir")
        bs_r, bs_2 = [], []
        for _ in range(B):
            wr = np.bincount(rng.randint(0, NRr, NRr), minlength=NRr).astype(float); wg = np.bincount(rng.randint(0, NGg, NGg), minlength=NGg).astype(float)
            bs_r.append((wr @ A).sum() / (wr @ N).sum()); bs_2.append((wr @ A @ wg) / (wr @ N @ wg))
        ci_r, ci_2 = np.percentile(bs_r, [2.5, 97.5]), np.percentile(bs_2, [2.5, 97.5])
        out[f"{a}-{b}_{mt}"] = {"point": float(pt), "primary": float(prim_pt), "rater": ci_r.tolist(), "twoway": ci_2.tolist()}
        L.append(f"| {a} − {b} | {'LL per rating' if mt == 'll' else 'direction acc.'} | {pt:+.4f} | {prim_pt:+.4f} | [{ci_r[0]:+.4f}, {ci_r[1]:+.4f}] | [{ci_2[0]:+.4f}, {ci_2[1]:+.4f}] |")
L += ["", f"n raters (fold-specific) = {NRr}, item clusters = {NGg}. Reproduction check (Am. 9): |rerun − primary| ≤ 1e-3 for every row: {all(abs(v['point'] - v['primary']) <= 1e-3 for v in out.values())}."]
json.dump(out, open(f"{R_}/stage2a_twoway_{panel}.json", "w"), indent=1); open(f"{R_}/stage2a_twoway_{panel}.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
