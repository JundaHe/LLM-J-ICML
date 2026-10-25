"""Aggregate probe_mean2 runs: per-arm means and paired contrasts vs soft (mean ± SEM over configs)."""
import pandas as pd, numpy as np, glob, sys
pd.set_option("display.width", 250)
for d in sorted(glob.glob("results/probe_mean2/*/runs.jsonl")):
    p = d.split("/")[2]
    if p.endswith("_smoke"): continue
    df = pd.read_json(d, lines=True); key = ["seed", "isplit", "rsplit"]; n = df.groupby(key).ngroups
    cols = ["pop_rps", "kl_ref", "D_spearman", "D_partial"]; piv = df.pivot_table(index=key, columns="arm", values=cols)
    print(f"\n##### probe_mean2 {p}: {n} configs")
    print(df.groupby("arm")[cols].mean().reindex(["hard", "smooth", "sordz", "proto", "sordm", "mean2", "cond", "shrunk", "soft", "soft_pmode", "soft_pmm", "soft_pmmx"]).round(4).to_string())
    print("paired contrasts arm − soft (negative = arm better on RPS/KL; for D positive = arm better):")
    for a in ["hard", "smooth", "sordz", "proto", "sordm", "mean2", "cond", "shrunk", "soft_pmode", "soft_pmm", "soft_pmmx"]:
        if ("pop_rps", a) not in piv: continue
        s = "  " + f"{a:10s}"
        for c in cols:
            dd = piv[(c, a)] - piv[(c, "soft")]; s += f" | {c} {dd.mean():+.4f}±{dd.sem():.4f}"
        print(s)
