"""Stage 15 S15-3 (PROTOCOL_STAGE15.md): two-way (rater × item-cluster) pigeonhole bootstrap of the corrected real-panel contrasts and a declared multiplicity
family, from the per-rating dumps of the `_s15` runs (factorised_rm.py --dump_ratings --decomp, rung a). Family A (Stage 14 contrasts): LL latent − scale-use
comparator, direction own − other, concordance own − other. Family B (Stage 15): LL staged − base, LL and concordance own − other on the interaction (own offsets).
Raters and item clusters resampled independently, B = 2000, seed 9; adaptation draws averaged within rating (pairs for concordance, weight w_r·w_g(i)·w_g(j), or
w_r·w_g inside one cluster). p from the normal approximation with the two-way standard error; Holm within each family and over both. Reproduction check: the
family-A points against the Stage 14 `_wa` per-rater runs (|difference| ≤ 1e-3 per rating). Post hoc. Output: results/stage15_twoway.json / .md"""
import json, glob, os, collections, numpy as np, scipy.sparse as sp
from scipy.stats import norm
HERE = os.path.dirname(os.path.abspath(__file__)); R_ = os.path.join(HERE, "results"); B = 2000; TAG = "_s15"
PANELS = {"multipref_overall": 20, "dices": 20, "prism": 20, "dorn_raters": 10}
COMP = lambda panel, m: ("F" if m == "L" else "DFs" if panel.startswith("multipref") else "DF")
def primary(panel, k, a, b, mt):
    """Stage 14 rung-a point (per-rater runs): pooled Σ(a − b) / Σ denominator, draws averaged within rater"""
    den = {"ll": "n", "dir": "n_dir", "conc": "conc_den"}[mt]; by = collections.defaultdict(list)
    for f in sorted(glob.glob(f"{R_}/stage2a_{panel}_wa_f?.json")):
        for r in json.load(open(f))["per_rater"]:
            if r["k"] == k and f"{a}_{mt}" in r and f"{b}_{mt}" in r: by[(r["fold"], r["rater"])].append(r)
    return (sum(np.mean([x[f"{a}_{mt}"] - x[f"{b}_{mt}"] for x in v]) for v in by.values()) / sum(np.mean([x[den] for x in v]) for v in by.values())) if by else None
rows = []; meta = {}
for panel, k in PANELS.items():
    D = [np.load(f, allow_pickle=True) for f in sorted(glob.glob(f"{R_}/ratings/stage2a_{panel}{TAG}_f?.npz"))]
    if not D: continue
    Z = {key: np.concatenate([d[key] for d in D]) for key in D[0].files}; sel = Z["k"] == k; rng = np.random.RandomState(9)
    rt = Z["fold"][sel] * 100000 + Z["rater"][sel]; key = np.stack([rt, Z["item"][sel]], 1); u, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel(); cnt = np.bincount(inv)
    gl = np.asarray(Z["igroup"][sel]).astype(str); gi = np.unique(gl, return_inverse=True)[1].ravel(); ig = np.zeros(len(u), int); ig[inv] = gi   # cluster of every (rater, item) cell
    ru, ri = np.unique(u[:, 0], return_inverse=True); ri = ri.ravel(); NRr, NGg = len(ru), ig.max() + 1; yc = np.zeros(len(u)); yc[inv] = Z["y"][sel]
    dr = Z["draw"][sel].astype(int); ND = dr.max() + 1; assert (cnt == ND).all()
    WR = np.stack([np.bincount(rng.randint(0, NRr, NRr), minlength=NRr) for _ in range(B)]).astype(float); WG = np.stack([np.bincount(rng.randint(0, NGg, NGg), minlength=NGg) for _ in range(B)]).astype(float)
    pr, pi_, pj = [], [], []                                                  # informative pairs (different ratings) within rater, as cell indices
    for r in range(NRr):
        c = np.where(ri == r)[0]; a_, b_ = np.triu_indices(len(c), 1); ok = yc[c[a_]] != yc[c[b_]]; pr.append(np.full(ok.sum(), r)); pi_.append(c[a_][ok]); pj.append(c[b_][ok])
    pr, pi_, pj = np.concatenate(pr), np.concatenate(pi_), np.concatenate(pj); sy = np.sign(yc[pi_] - yc[pj]); same = ig[pi_] == ig[pj]
    def cellmat(name):
        E = np.zeros((len(u), ND)); E[inv, dr] = Z[name][sel]; return E
    def conc(name):
        """per informative pair: concordance score of the expected scores (ties 1/2), averaged over the adaptation draws"""
        E = cellmat(name); sg = np.sign(E[pi_] - E[pj]) * sy[:, None]; return ((sg > 0) + 0.5 * (sg == 0)).mean(1)
    def boot(a, b, mt):
        if mt == "conc":
            d = conc(f"{a}_ey") - conc(f"{b}_ey"); pt = d.mean(); bs_r, bs_2 = np.zeros(B), np.zeros(B); cr = np.bincount(pr, d, minlength=NRr); nr = np.bincount(pr, minlength=NRr).astype(float)
            for t in range(B):
                w = WR[t][pr] * np.where(same, WG[t][ig[pi_]], WG[t][ig[pi_]] * WG[t][ig[pj]]); bs_2[t] = (w * d).sum() / max(w.sum(), 1e-12); bs_r[t] = (WR[t] @ cr) / (WR[t] @ nr)
        else:
            d = Z[f"{a}_{mt}"][sel] - Z[f"{b}_{mt}"][sel]; ok = np.isfinite(d); d = np.where(ok, d, 0.0); num = np.bincount(inv, d) / cnt; den = np.bincount(inv, ok.astype(float)) / cnt
            A = sp.csr_matrix((num, (ri, ig)), shape=(NRr, NGg)); N = sp.csr_matrix((den, (ri, ig)), shape=(NRr, NGg)); pt = A.sum() / N.sum()
            AR, NRm = np.asarray(A.sum(1)).ravel(), np.asarray(N.sum(1)).ravel(); bs_r = (WR @ AR) / (WR @ NRm); bs_2 = np.einsum("bg,bg->b", WR @ A, WG) / np.einsum("bg,bg->b", WR @ N, WG)
        return float(pt), np.percentile(bs_r, [2.5, 97.5]).tolist(), np.percentile(bs_2, [2.5, 97.5]).tolist(), float(np.std(bs_2))
    meta[panel] = {"k": k, "folds": sorted(set(Z["fold"].tolist())), "n_raters": int(NRr), "n_clusters": int(NGg), "n_pairs": int(len(pr))}
    for M, S, Bm in (("DL", "DFL", "DF"), ("L", "FL", "F")):
        Q = COMP(panel, M)
        for fam, lab, a, b, mt in (("A", f"LL {M} − {Q}", M, Q, "ll"), ("A", f"direction {M} own − other", M, f"{M}_perm", "dir"), ("A", f"concordance {M} own − other", M, f"{M}_perm", "conc"),
                                   ("B", f"LL {S} − {Bm}", S, Bm, "ll"), ("B", f"LL {S} own − other latent", S, f"{S}_perm", "ll"), ("B", f"concordance {S} own − other latent", S, f"{S}_perm", "conc"),
                                   ("–", f"LL {M} own − (other's interaction)", M, f"{M}_xi", "ll"), ("–", f"LL {M} own − (other's shift)", M, f"{M}_xs", "ll"), ("–", f"concordance {M} own − (other's interaction)", M, f"{M}_xi", "conc")):
            if f"{a}_ll" not in Z or f"{b}_ll" not in Z: continue
            pt, cr_, c2, se = boot(a, b, mt); prim = primary(panel, k, a, b, mt) if fam == "A" else None
            rows.append({"panel": panel, "family": fam, "contrast": lab, "point": pt, "rater": cr_, "twoway": c2, "se2": se, "p": float(2 * norm.sf(abs(pt) / max(se, 1e-12))), "primary": prim})
def holm(ix):
    p = np.array([rows[i]["p"] for i in ix]); o = np.argsort(p); adj = np.zeros(len(p)); run = 0.0
    for r, i in enumerate(o): run = max(run, min(1.0, (len(p) - r) * p[i])); adj[i] = run
    return dict(zip(ix, adj))
hA = holm([i for i, r in enumerate(rows) if r["family"] == "A"]); hB = holm([i for i, r in enumerate(rows) if r["family"] == "B"]); hU = holm([i for i, r in enumerate(rows) if r["family"] in "AB"])
for i, r in enumerate(rows): r["p_holm_family"] = float({**hA, **hB}.get(i, np.nan)); r["p_holm_union"] = float(hU.get(i, np.nan)); r["nominal_sig"] = bool(r["twoway"][0] > 0 or r["twoway"][1] < 0)
chk = [abs(r["point"] - r["primary"]) for r in rows if r["primary"] is not None]; repro = bool(chk and max(chk) <= 1e-3)
sc = lambda v: 100 * v; f3 = lambda r, q: f"[{sc(r[q][0]):+.2f}, {sc(r[q][1]):+.2f}]"
L = ["# Stage 15 S15-3 — two-way intervals and multiplicity for the corrected real-panel contrasts (post hoc; rung a; k = 20, Dorn k = 10; ×100 nats or points per rating)", "",
     f"Reproduction of the Stage 14 rung-a points by the rerun (family A, |difference| ≤ 1e-3 per rating): {repro} (max {max(chk) if chk else float('nan'):.2e}, {len(chk)} contrasts). Panels: {meta}", "",
     "| panel | family | contrast | point | Stage 14 point | rater-only 95 % | two-way 95 % | p (two-way, normal) | Holm in family | Holm over A ∪ B | nominal | after Holm (family / union) |", "|---" * 12 + "|"]
for r in rows:
    hf, hu = r["p_holm_family"], r["p_holm_union"]
    L.append(f"| {r['panel']} | {r['family']} | {r['contrast']} | {sc(r['point']):+.2f} | {'—' if r['primary'] is None else format(sc(r['primary']), '+.2f')} | {f3(r, 'rater')} | {f3(r, 'twoway')} | {r['p']:.4f} | {'—' if np.isnan(hf) else format(hf, '.4f')} | {'—' if np.isnan(hu) else format(hu, '.4f')} | {'yes' if r['nominal_sig'] else 'no'} | {'—' if np.isnan(hf) else ('yes' if hf < 0.05 else 'no') + ' / ' + ('yes' if hu < 0.05 else 'no')} |")
for fam in "AB":
    fr = [r for r in rows if r["family"] == fam]
    if fr: L += ["", f"Family {fam}: {len(fr)} contrasts; nominal (two-way interval excludes 0) {sum(r['nominal_sig'] for r in fr)}; Holm within family {sum(r['p_holm_family'] < 0.05 for r in fr)}; Holm over the union {sum(r['p_holm_union'] < 0.05 for r in fr)}."]
json.dump({"rows": rows, "meta": meta, "reproduced": repro}, open(f"{R_}/stage15_twoway.json", "w"), indent=1); open(f"{R_}/stage15_twoway.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
