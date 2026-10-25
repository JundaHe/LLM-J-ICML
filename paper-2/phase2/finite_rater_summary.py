"""
Summary of the finite-rater analysis (FINITE_RATER_PROTOCOL.md, amendments 1–2): writes results/finite_rater/summary.json and prints the T9 markdown blocks.
(a) a = m − 1 table per panel (A1 smoothed comparator, A1x exact-T comparator, M, X, ρ, N, Δ, A2) next to the learned-judge contrasts;
(b) prospective prediction test on dense panels: fit N = v/a and Δ = δ∞ + c/a on a ∈ {2,5,10,20,40}, predict A1 at a ∈ {3,8,15,30}, coverage by the observed 95 % intervals;
(c) dense-panel curves: crossover of A1 (raw histogram vs T-comparator) and Δ_ref with the implied reference crossover v/Δ_ref.
Usage: python finite_rater_summary.py
"""
import os, json, glob, numpy as np, pandas as pd
from scipy.optimize import nnls
P = os.path.dirname(os.path.abspath(__file__)); R = f"{P}/results/finite_rater"
ORD = [("summeval_coherence8", "SummEval coherence"), ("summeval_relevance8", "SummEval relevance"), ("popquorn_off8", "POPQUORN offensiveness"), ("popquorn_pol5", "POPQUORN politeness"),
       ("csc6", "CSC sarcasm"), ("scalabrino", "Scalabrino readability"), ("hs2_help5", "HelpSteer2 helpfulness"), ("emobank_reader_v5", "EmoBank valence"),
       ("bw", "Buse–Weimer readability"), ("dices", "DICES-350"), ("dices990", "DICES-990")]
NOM = [("chaosnli_mnli", "ChaosNLI MNLI"), ("chaosnli_snli", "ChaosNLI SNLI")]
DENSE = ["chaosnli_mnli", "chaosnli_snli", "dices", "dices990", "bw"]
TAG = {"hs2_help5": "_v7", "popquorn_off8": "_v7", "dices990": "_v7", "popquorn_pol5": "_v7", "csc6": "_v7", "emobank_reader_v5": "_v7"}
def f4(x): return f"{x:+.4f}"
def ci(c): return f"[{c[0]:+.4f}, {c[1]:+.4f}]"
def heads(key):
    p = f"{P}/results/probe_mean2/{key}{TAG.get(key, '_v6')}/runs.jsonl"
    if not os.path.exists(p): return None
    df = pd.read_json(p, lines=True); piv = df.pivot_table(index=["seed", "isplit", "rsplit"], columns="arm", values="pop_rps"); d = piv["soft_pmmx"] - piv["soft"]
    return f"{d.mean():+.4f}±{d.sem():.4f}"
LORA = {}
for key, fn in (("summeval_coherence8", "summeval_coherence8/analysis_block_summeval.json"), ("popquorn_off8", "popquorn_off8/analysis_block_popquorn.json")):
    r = {(x["contrast"], x["estimand"]): x for x in json.load(open(f"{P}/results/lora/{fn}"))["rows"]}[("perm − chen", "raw")]; LORA[key] = f"{r['est']:+.4f} {ci((r['lo'], r['hi']))}"
out = dict(loo={}, curves={}, prediction={}, ref={})
print("### (a) a = m − 1 (one held-out rating per item, position drawn per item; 20 repetitions; item-cluster bootstrap B = 500)")
print("| panel | m | A1 (smoothed T-comparator) | A1x (exact-T comparator) | M | X | ρ = X/M | N | Δ = N − A1 | A2 ITT (pmmx/pzc donor) [changed, TV] | heads pmmx − soft | LoRA perm − chen |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for key, lab in ORD + NOM:
    f = f"{R}/{key}_loo.json"
    if not os.path.exists(f): print(f"| {lab} | (pending) |"); continue
    j = json.load(open(f)); row = j["rows"][0]; e, c = row["est"], row["ci95"]; out["loo"][key] = row
    a2 = row.get("A2"); a2s = f"{a2['itt']:+.4f} {ci(a2['itt_ci95'])} [{a2['changed_fraction']:.2f}, {a2['tv_changed']:.2f}]" if a2 else "—"
    print(f"| {lab} | {j['m']} | {f4(e['A1'])} {ci(c['A1'])} | {f4(e['A1x'])} {ci(c['A1x'])} | {e['M']:.4f} | {f4(e['X'])} {ci(c['X'])} | {e['rho']:.2f} [{c['rho'][0]:.2f}, {c['rho'][1]:.2f}] | {e['N']:.4f} | {e['Delta']:.4f} | {a2s} | {heads(key) or '—'} | {LORA.get(key, '—')} |")
print("\n### (b) dense-panel curves (a ratings in P1, 20 held-out ratings in P2) and the prospective prediction test")
FIT, PRED = [2, 5, 10, 20, 40], [3, 8, 15, 30]
for key in DENSE + ["chaosnli_alphanli"]:
    f = f"{R}/{key}.json"
    if not os.path.exists(f): print(f"{key}: (pending)"); continue
    j = json.load(open(f)); rows = {r["a"]: r for r in j["rows"]}; out["curves"][key] = rows
    print(f"\n{key} (m = {j['m']}, {'nominal/Brier' if j['nominal'] else 'ordinal/RPS'})")
    print("| a | A1 [95 % CI] | A1x | ρ | N | Δ |"); print("|---|---|---|---|---|---|")
    for a in sorted(rows):
        e, c = rows[a]["est"], rows[a]["ci95"]; print(f"| {a} | {f4(e['A1'])} {ci(c['A1'])} | {f4(e['A1x'])} | {e['rho']:.2f} | {e['N']:.4f} | {e['Delta']:.4f} |")
    sgn = [(a, rows[a]["est"]["A1"]) for a in sorted(rows)]; cross = None
    for (a0, y0), (a1, y1) in zip(sgn, sgn[1:]):
        if y0 > 0 >= y1: cross = a0 + (a1 - a0) * y0 / (y0 - y1); break
    fit = [a for a in FIT if a in rows]; pred = [a for a in PRED if a in rows]
    if len(fit) >= 3 and pred:
        v = float(np.mean([a * rows[a]["est"]["N"] for a in fit]))
        Afit = np.array([[1.0, 1.0 / a] for a in fit]); yfit = np.array([rows[a]["est"]["Delta"] for a in fit]); (d_inf, cc), _ = nnls(Afit, yfit)
        res = []
        for a in pred:
            p_ = v / a - (d_inf + cc / a); lo, hi = rows[a]["ci95"]["A1"]; res.append(dict(a=a, predicted=p_, observed=rows[a]["est"]["A1"], ci=[lo, hi], covered=bool(lo <= p_ <= hi)))
        out["prediction"][key] = dict(v=v, delta_inf=float(d_inf), c=float(cc), results=res, crossover_A1=cross)
        print(f"fit on a ∈ {fit}: v = {v:.4f}, δ∞ = {d_inf:.4f}, c = {cc:.4f}; observed A1 sign change at a ≈ {('%.1f' % cross) if cross else 'none in range'}")
        for r_ in res: print(f"  a = {r_['a']:2d}: predicted {r_['predicted']:+.4f}  observed {r_['observed']:+.4f} {ci(r_['ci'])}  {'covered' if r_['covered'] else 'NOT covered'}")
    if "delta_ref" in j:
        dr = j["delta_ref"]; v = out["prediction"].get(key, {}).get("v"); out["ref"][key] = dict(dr, a_ref_cross=(v / dr["est"] if v and dr["est"] > 0 else None))
        print(f"Δ_ref (T from {dr['nref']} independent ratings) = {dr['est']:+.4f} {ci(dr['ci95'])}" + (f"; implied reference crossover v/Δ_ref ≈ {v / dr['est']:.1f} raters" if v and dr['est'] > 0 else ""))
json.dump(out, open(f"{R}/summary.json", "w"), indent=1, default=float)
