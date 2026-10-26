"""g1_summary — one row per (panel, variable, pool B) from results/pool_adapt/*/runs.jsonl: the pool-shift gap (none − oracle-B), what map-B(n) and dir-B(n) recover, and map vs dir at equal n.
Paired over configurations (seed × split); ± = SEM over the 15 dependent configurations. Writes reports/G1_SUMMARY.md."""
import glob, os, pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); rows = []
for d in sorted(glob.glob(f"{HERE}/results/pool_adapt/*/runs.jsonl")):
    name = os.path.basename(os.path.dirname(d)); panel, var = name.split("__", 1); df = pd.read_json(d, lines=True)
    for b, sub in df.groupby("poolB"):
        piv = sub.pivot_table(index=["seed", "isplit"], columns="arm", values="rps")
        if "oracle-B" not in piv: continue
        gap = piv["none"] - piv["oracle-B"]
        def rec(arm):   # fraction of the gap recovered, paired per configuration (reported only when the mean gap is clearly positive)
            return (piv["none"] - piv[arm]).mean() / gap.mean() if gap.mean() > 1e-4 else np.nan
        r = dict(panel=panel, var=var, poolB=b.replace("B_", ""), nA=int(sub.poolA_size.iloc[0]), nB=int(sub.poolB_size.iloc[0]), none=piv["none"].mean(), gap=gap.mean(), gap_sem=gap.sem())
        for arm in ("map-A", "map-B(20)", "map-B(50)", "map-B(all)", "dir-B(20)", "dir-B(50)", "dir-B(all)"):
            if arm in piv: r[arm] = (piv[arm] - piv["none"]).mean()
        r["recover_map50"] = rec("map-B(50)") if "map-B(50)" in piv else np.nan; r["recover_dir50"] = rec("dir-B(50)") if "dir-B(50)" in piv else np.nan
        r["map_minus_dir_all"] = (piv["map-B(all)"] - piv["dir-B(all)"]).mean() if "map-B(all)" in piv and "dir-B(all)" in piv else np.nan
        rows.append(r)
T = pd.DataFrame(rows); pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
cols = ["panel", "var", "poolB", "nA", "nB", "none", "gap", "gap_sem", "map-B(20)", "map-B(50)", "map-B(all)", "dir-B(50)", "dir-B(all)", "recover_map50", "recover_dir50", "map_minus_dir_all"]
T = T[cols].sort_values(["panel", "var", "poolB"]); txt = "# G1 pool adaptation — summary (RPS; vs none = arm − none, negative is better; gap = none − oracle-B, positive = a pool shift the head trained on A did not capture)\n\n```\n" + T.round(4).to_string(index=False) + "\n```\n"
os.makedirs(f"{HERE}/reports", exist_ok=True); open(f"{HERE}/reports/G1_SUMMARY.md", "w").write(txt); print(txt)
