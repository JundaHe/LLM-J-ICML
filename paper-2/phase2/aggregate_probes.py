"""Aggregate probe_mean runs across panels: paired contrasts (mean ± SEM over configs) + oracle gap. Writes results/probe_mean/ALL_SUMMARY.md"""
import pandas as pd, numpy as np, os, glob, sys
rows = []
for d in sorted(glob.glob("results/probe_mean/*/runs.jsonl")):
    p = d.split("/")[2]
    if p.endswith("_smoke"): continue
    df = pd.read_json(d, lines=True); key = ["seed", "isplit", "rsplit"]; n = df.groupby(key).ngroups
    piv = df.pivot_table(index=key, columns="arm", values=["pop_rps", "kl_ref", "D_spearman", "D_partial"])
    def c(col, a, b): dd = piv[(col, a)] - piv[(col, b)]; return dd.mean(), dd.sem()
    r = dict(panel=p, n_cfg=n, K=int(df.K.iloc[0]) if "K" in df else None,
             oracle_gap_D=piv[("D_spearman", "oracle_soft")].mean() - piv[("D_spearman", "oracle_mean2")].mean(),
             meanfit_rho=df[df.arm == "ref_meanonly_D"].D_spearman_meanfit.mean())
    for col in ("kl_ref", "D_spearman", "D_partial"):
        for a, b, nm in (("soft", "mean2", "soft-mean2"), ("mean2", "smooth", "mean2-smooth"), ("mean2", "proto", "mean2-proto"), ("soft_pmode", "soft", "pmode-soft"), ("soft_pmm", "soft", "pmm-soft"), ("soft", "hard", "soft-hard")):
            m, s = c(col, a, b); r[f"{col}:{nm}"] = f"{m:+.4f}±{s:.4f}"
    r["learnable_frac_D"] = (c("D_spearman", "soft", "mean2")[0] / r["oracle_gap_D"]) if abs(r["oracle_gap_D"]) > 0.02 else float("nan")
    rows.append(r)
T = pd.DataFrame(rows).set_index("panel")
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
with open("results/probe_mean/ALL_SUMMARY.md", "w") as f:
    f.write("# probe_mean across panels (paired contrasts, mean ± SEM over seed×item-split×rater-split configs)\n\n")
    for col in ("kl_ref", "D_spearman", "D_partial"):
        sub = T[["n_cfg", "oracle_gap_D", "meanfit_rho"] + [x for x in T.columns if x.startswith(col + ":")]].copy(); sub.columns = [x.split(":")[-1] for x in sub.columns]
        f.write(f"## {col}\n\n```\n{sub.round(3).to_string()}\n```\n\n")
    f.write(f"## learnable fraction of beyond-mean D (soft−mean2)/(oracle_soft−oracle_mean2)\n\n```\n{T[['oracle_gap_D','learnable_frac_D']].round(3).to_string()}\n```\n")
print(open("results/probe_mean/ALL_SUMMARY.md").read())
