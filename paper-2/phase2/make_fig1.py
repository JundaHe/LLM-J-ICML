"""Fig. 1 schematic: statistic-preserving donor replacement and the dose certificate (illustrative histograms only; no experimental numbers)."""
import os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
P = os.path.dirname(os.path.abspath(__file__)); OUT = f"{P}/results/figures"; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 7, "axes.spines.top": False, "axes.spines.right": False})
K = 5; lv = np.arange(1, K + 1)
recipient = np.array([0.0, 0.25, 0.5, 0.25, 0.0])          # mode 3, mean 3.0
donor_mode = np.array([0.0, 0.0, 0.5, 0.0, 0.5])           # same mode (tied allowed), mean 4.0  -> pmode
donor_mm = np.array([0.125, 0.125, 0.5, 0.125, 0.125])      # same mode and mean, different allocation -> pmm
pmmx = np.array([0.10, 0.17, 0.46, 0.17, 0.10])            # illustrative exact projection (mode 3, mean 3.0)
fig = plt.figure(figsize=(8.0, 3.4)); gs = fig.add_gridspec(2, 5, height_ratios=[1, 0.5], hspace=0.75, wspace=0.55, top=0.80, bottom=0.05, left=0.04, right=0.99)
def bar(ax, h, title, color, note=""):
    ax.bar(lv, h, color=color, width=0.7); ax.set_ylim(0, 0.65); ax.set_xticks(lv); ax.set_yticks([]); ax.set_title(title, fontsize=7); ax.text(0.5, -0.32, note, transform=ax.transAxes, ha="center", fontsize=6)
bar(fig.add_subplot(gs[0, 0]), recipient, "training item i\nhistogram h_i", "#444444", "mode 3 · mean 3.0")
ax = fig.add_subplot(gs[0, 1]); ax.axis("off"); ax.text(0.5, 0.75, "cell(i)", ha="center", fontsize=8, weight="bold"); ax.text(0.5, 0.5, "pmode: {mode}\npmm: {mode, mean-bin}", ha="center", va="center", fontsize=6.5)
ax.text(0.5, 0.1, "donor j: max-cardinality matching\non histogram classes\n(class flow deterministic;\nseed shuffles identities)", ha="center", va="center", fontsize=5.3)
ax.annotate("", xy=(1.02, 0.5), xytext=(-0.02, 0.5), xycoords="axes fraction", arrowprops=dict(arrowstyle="->", lw=0.8))
bar(fig.add_subplot(gs[0, 2]), donor_mode, "pmode target\nh_j, same mode", "#d62728", "mode 3 (tied) · mean 4.0\nlocation disrupted")
bar(fig.add_subplot(gs[0, 3]), donor_mm, "pmm target\nh_j, same mode & mean-bin", "#1f77b4", "mode 3 · mean 3.0\nresidual allocation replaced")
bar(fig.add_subplot(gs[0, 4]), pmmx, "pmmx target\nKL-projection of h_j", "#17becf", "exact mode 3 · mean 3.0\n(certified KKT projection)")
ax = fig.add_subplot(gs[1, :]); ax.axis("off")
cert = ("Certificate reported beside every contrast:  support = fraction of items in cells with ≥ 2 histogram classes (upper bound) ·  changed fraction (realised) ·  "
        "TV among changed items ·  TV over all items ·  zero-TV donor pairs (= 0 before projection) ·  post-projection dose (pmmx)\n"
        "Contrast = RPS(arm) − RPS(soft) on held-out annotation positions, same split and RNG stream; estimates the average predictive consequence of the realised replacement "
        "conditional on learner, split, realisation, assignment rule and dose — not the intrinsic value of the removed information.")
ax.text(0.0, 0.9, cert, ha="left", va="top", fontsize=6, wrap=True, bbox=dict(boxstyle="round,pad=0.4", fc="#f4f4f4", ec="#999999", lw=0.6))
fig.suptitle("Fig. 1  Statistic-preserving donor replacement (schematic; illustrative histograms)", fontsize=8, x=0.01, y=0.985, ha="left")
fig.savefig(f"{OUT}/fig1_schematic.png", dpi=200, bbox_inches="tight"); fig.savefig(f"{OUT}/fig1_schematic.pdf", bbox_inches="tight"); print("fig1 written")
