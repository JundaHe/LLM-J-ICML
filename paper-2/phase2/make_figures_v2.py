"""Figure 1 for PAPER_DRAFT_v2: split-half reliability ρ and the raw-vs-comparator contrast A1 against the number of raters a, dense panels. Writes latex_v2/fig_reliability.pdf and fig_reliability.tex."""
import json, os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); L = f"{HERE}/latex_v2"
PANELS = [("chaosnli_mnli", "ChaosNLI MNLI (nominal)", "#d62728", "-"), ("chaosnli_snli", "ChaosNLI SNLI (nominal)", "#ff9896", "-"), ("dices", "DICES-350", "#1f77b4", "--"), ("dices990", "DICES-990", "#aec7e8", "--"),
          ("bw", "Buse–Weimer (SE)", "#2ca02c", ":"), ("dorn_java", "Dorn Java (SE)", "#98df8a", ":"), ("dorn_python", "Dorn Python (SE)", "#bcbd22", ":"), ("dorn_cuda", "Dorn CUDA (SE)", "#17becf", ":")]
fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.8))
for key, lab, col, ls in PANELS:
    f = f"{HERE}/results/finite_rater/{key}.json"
    if not os.path.exists(f): continue
    rows = sorted(json.load(open(f))["rows"], key=lambda r: r["a"]); a = [r["a"] for r in rows]
    ax[0].plot(a, [r["est"]["rho"] for r in rows], ls, color=col, marker="o", ms=3, label=lab)
    ax[1].plot(a, [r["est"]["A1"] for r in rows], ls, color=col, marker="o", ms=3, label=lab)
    ax[1].fill_between(a, [r["ci95"]["A1"][0] for r in rows], [r["ci95"]["A1"][1] for r in rows], color=col, alpha=0.12, lw=0)
ax[0].axhline(0.5, color="grey", lw=0.8); ax[0].set_xscale("log"); ax[0].set_xlabel("raters per item $a$"); ax[0].set_ylabel(r"split-half reliability $\rho=X/M$"); ax[0].set_title("(a) reproducibility of the shape", fontsize=9)
ax[1].axhline(0, color="grey", lw=0.8); ax[1].set_xscale("log"); ax[1].set_yscale("symlog", linthresh=0.002); ax[1].set_xlabel("raters per item $a$"); ax[1].set_ylabel("$A1$ (raw $-$ comparator score)"); ax[1].set_title("(b) raw histogram worse above 0", fontsize=9)
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, fontsize=7, frameon=False, loc="lower center", ncol=4); fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig(f"{L}/fig_reliability.pdf")
open(f"{L}/fig_reliability.tex", "w").write("\\begin{figure}[t]\\centering\\includegraphics[width=\\linewidth]{fig_reliability.pdf}\\caption{Reliability of the disagreement shape against the number of raters per item on the dense panels. (a) $\\rho=X/M$ crosses $\\tfrac12$ — where the raw histogram starts to beat a location-only forecast — at 5–10 raters on ChaosNLI, at 20–40 on Buse–Weimer and on all three languages of Dorn's developer study, and not within 40 raters on DICES. (b) $A1$ with 95\\% item-cluster intervals (symmetric-log scale).}\\label{fig:reliability}\\end{figure}\n")
print("figure written")
