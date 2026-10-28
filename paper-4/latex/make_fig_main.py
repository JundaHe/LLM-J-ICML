"""Figure 1 of paper 4: gain in held-out log-likelihood per rating over the text-only distributional RM (D) for new raters vs number of adaptation ratings k,
three datasets as small multiples; DL uses the k-shot-tuned prior (Amendment 5); 95 % rater-cluster bootstrap bands. Palette validated (dataviz validator, light)."""
import json, os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(os.path.dirname(HERE), "results")
SER = [("DFs-D", "style offsets, symmetric (DFs)", "#2a78d6", "o"), ("DF-D", "style offsets (DF)", "#eb6834", "s"), ("DL-D", "low-rank latent (DL, tuned)", "#1baf7a", "^"), ("DG-D", "group offsets (DG)", "#eda100", "D")]
DS = [("MultiPref (pairwise preference)", "stage2a_multipref_overall"), ("DICES-350 (safety)", "stage2a_dices"), ("PRISM (response ratings)", "stage2a_prism")]
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.2), sharey=True)
for ax, (title, stem) in zip(axes, DS):
    P = json.load(open(f"{R}/{stem}.json"))["summary"]; A5 = json.load(open(f"{R}/{stem}_A5.json"))["summary"]
    ks = [k for k in ("0", "5", "10", "20", "50") if k in P]
    for key, lab, col, mk in SER:
        src = A5 if key == "DL-D" else P
        if f"{key}_ll" not in src[ks[0]]: continue
        x = [int(k) for k in ks]; y = [src[k][f"{key}_ll"][0] for k in ks]; lo = [src[k][f"{key}_ll"][1] for k in ks]; hi = [src[k][f"{key}_ll"][2] for k in ks]
        ax.fill_between(x, lo, hi, color=col, alpha=0.12, lw=0); ax.plot(x, y, color=col, lw=1.5, marker=mk, ms=4, mec="#fcfcfb", mew=0.8, label=lab)
    ax.axhline(0, color="#52514e", lw=0.6); ax.set_title(title, fontsize=8, color="#0b0b0b"); ax.set_xlabel("ratings of the new rater (k)", color="#52514e")
    ax.set_xticks([0, 5, 10, 20, 50]); ax.grid(axis="y", color="#e6e5e0", lw=0.5); ax.tick_params(colors="#52514e")
axes[0].set_ylabel("Δ log-lik. per rating vs D", color="#52514e")
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc="lower center", ncol=4, frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.06))
fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(f"{HERE}/fig_main.pdf", bbox_inches="tight"); fig.savefig(f"{HERE}/fig_main.png", dpi=160, bbox_inches="tight"); print("saved")
