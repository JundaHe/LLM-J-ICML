"""Figure 1 for PAPER_DRAFT_v2: split-half reliability ρ and the raw-vs-comparator contrast A1 against the number of raters a, dense panels. Writes latex_v2/fig_reliability.pdf and fig_reliability.tex."""
import json, os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); L = f"{HERE}/latex_v2"
PANELS = [("chaosnli_mnli", "ChaosNLI MNLI (nominal)", "#d62728", "-"), ("chaosnli_snli", "ChaosNLI SNLI (nominal)", "#ff9896", "-"), ("dices", "DICES-350", "#1f77b4", "--"), ("dices990", "DICES-990", "#aec7e8", "--"),
          ("bw", "Buse–Weimer (SE)", "#2ca02c", ":"), ("dorn_java", "Dorn Java (SE)", "#98df8a", ":"), ("dorn_python", "Dorn Python (SE)", "#bcbd22", ":"), ("dorn_cuda", "Dorn CUDA (SE)", "#17becf", ":")]
fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.8))
for key, lab, col, ls in PANELS:
    f = f"{HERE}/results/rho_exact/{key}.json"           # exact mode+mean comparator (§2 construct); ρ masked where the residual is structurally empty (M < 1e-5)
    if not os.path.exists(f): continue
    rows = sorted(json.load(open(f))["rows"], key=lambda r: r["a"]); ok = [r for r in rows if r["M"] > 1e-5 and r["rho_ci"][1] - r["rho_ci"][0] < 1.0]   # also drop points whose ratio interval is wider than 1 (unstable ratio at tiny M)
    ax[0].plot([r["a"] for r in ok], [r["rho"] for r in ok], ls, color=col, marker="o", ms=3, label=lab)
    ax[0].fill_between([r["a"] for r in ok], [r["rho_ci"][0] for r in ok], [r["rho_ci"][1] for r in ok], color=col, alpha=0.10, lw=0)
    a = [r["a"] for r in rows]; ax[1].plot(a, [r["A1x"] for r in rows], ls, color=col, marker="o", ms=3, label=lab)
    ax[1].fill_between(a, [r["A1x_ci"][0] for r in rows], [r["A1x_ci"][1] for r in rows], color=col, alpha=0.12, lw=0)
ax[0].axhline(0.5, color="grey", lw=0.8); ax[0].set_xscale("log"); ax[0].set_xlabel("raters per item $a$"); ax[0].set_ylabel(r"$\rho=X/M$ (exact mode+mean comparator)"); ax[0].set_ylim(-0.3, 1.05); ax[0].set_title("(a) reproducibility of the shape", fontsize=9)
ax[1].axhline(0, color="grey", lw=0.8); ax[1].set_xscale("log"); ax[1].set_yscale("symlog", linthresh=0.002); ax[1].set_xlabel("raters per item $a$"); ax[1].set_ylabel("$A1^x$ (raw $-$ mode+mean comparator)"); ax[1].set_title("(b) raw histogram worse above 0", fontsize=9)
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, fontsize=7, frameon=False, loc="lower center", ncol=4); fig.tight_layout(rect=(0, 0.12, 1, 1)); fig.savefig(f"{L}/fig_reliability.pdf")
open(f"{L}/fig_reliability.tex", "w").write("\\begin{figure}[t]\\centering\\includegraphics[width=\\linewidth]{fig_reliability.pdf}\\caption{Reliability of the shape beyond exact mode and mean against the number of raters per item, dense panels. (a) Split-half reliability $\\rho=X/M$ relative to the exact mode-and-mean comparator, with 95\\% item-cluster intervals; omitted where the residual is structurally empty or the ratio interval is wider than 1 (DICES with 2--5 ratings on a 3-level scale). The raw histogram beats the location-only forecast only above $\\tfrac12$. (b) $A1^x$: positive means the raw histogram forecasts a new rater worse than its own mode and mean.}\\label{fig:reliability}\\end{figure}\n")
print("figure written")
