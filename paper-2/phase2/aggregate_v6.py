"""Build the T2b markdown (heads hierarchy, _v6 runs only) with realised-dose columns from results/probe_mean2/<panel>_v6/runs.jsonl. Usage: python aggregate_v6.py > results/t2b_v6.md"""
import os, sys, numpy as np, pandas as pd
TAG = {"commit_why": "_v7", "commit_what": "_v7", "hs2_help5": "_v7", "popquorn_off8": "_v7", "dices990": "_v7", "popquorn_pol5": "_v7", "csc6": "_v7", "emobank_reader_v5": "_v7"}   # group-disjoint reruns (Codex round 13); others _v6
def tag(key): return TAG.get(key, "_v6")
HERE = os.path.dirname(os.path.abspath(__file__)); PANELS = [("summeval_coherence8", "SummEval coherence"), ("bw", "Buse–Weimer"), ("dices", "DICES Q_overall"), ("scalabrino", "Scalabrino"), ("hs2_help5", "HelpSteer2 helpfulness"), ("popquorn_off8", "POPQUORN offensiveness"), ("dices990", "DICES-990"), ("popquorn_pol5", "POPQUORN politeness"), ("csc6", "CSC sarcasm"), ("emobank_reader_v5", "EmoBank reader valence")]
ARMS = ["hard", "smooth", "sordz", "proto", "sordm", "mean2", "cond", "shrunk", "shrunk_strong", "shrunk_res", "soft_pmode", "soft_pmm", "soft_pmmx"]
def fmt(d): return f"{d.mean():+.4f}±{d.sem():.4f}"
def fmt3(d): return f"{d.mean():+.3f}±{d.sem():.3f}"
out = []
for key, label in PANELS:
    f = f"{HERE}/results/probe_mean2/{key}{tag(key)}/runs.jsonl"
    if not os.path.exists(f): out.append(f"**{label}** — pending.\n"); continue
    df = pd.read_json(f, lines=True); idx = ["seed", "isplit", "rsplit"]; n = df.groupby(idx).ngroups
    piv = {m: df.pivot_table(index=idx, columns="arm", values=m, dropna=False) for m in ("pop_rps", "kl_ref", "D_partial")}   # dropna=False: D-partial is undefined (NaN) when a single annotation position is held out
    dose = {}
    for a in ("soft_pmode", "soft_pmm", "soft_pmmx"):
        d = df[df.arm == a]; dose[a] = dict(ch=d.changed_fraction.mean(), tv=d.dose_tv.mean() if "dose_tv" in d and d.dose_tv.notna().any() else np.nan, chp=d.changed_after_projection.mean() if "changed_after_projection" in d and d.changed_after_projection.notna().any() else np.nan)
    soft = df[df.arm == "soft"].pop_rps.mean()
    DA = pd.read_csv(f"{HERE}/results/dose_audit_summary.csv"); rx = DA[(DA.panel == key) & (DA.arm == "soft_pmmx")]
    pmmx_line = f"pmmx post-projection (T2c rule, TV > 1e-9): changed {rx.changed.iloc[0]:.3f} / TV {rx.tv_chg.iloc[0]:.3f} / TV-all {rx.tv_all.iloc[0]:.3f}" if len(rx) else "pmmx dose: see T2c"
    out.append(f"**{label}** (`{tag(key)}`, {n} cfgs; soft RPS {soft:.4f}). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode {dose['soft_pmode']['ch']:.3f} / {dose['soft_pmode']['tv']:.2f} / {dose['soft_pmode']['ch']*dose['soft_pmode']['tv']:.3f}; "
               f"pmm {dose['soft_pmm']['ch']:.3f} / {dose['soft_pmm']['tv']:.2f} / {dose['soft_pmm']['ch']*dose['soft_pmm']['tv']:.3f}; {pmmx_line}.\n")
    out.append("| arm − soft | RPS | KL | D partial |\n|---|---|---|---|")
    for a in ARMS:
        if a not in piv["pop_rps"].columns: continue
        out.append(f"| {a} | {fmt(piv['pop_rps'][a] - piv['pop_rps']['soft'])} | {fmt3(piv['kl_ref'][a] - piv['kl_ref']['soft'])} | {fmt3(piv['D_partial'][a] - piv['D_partial']['soft'])} |")
    out.append("")
print("\n".join(out))
