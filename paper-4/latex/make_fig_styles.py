"""Figure 2 of paper 4: how scale use changes a rater's predicted rating distribution for the same item. Base = MultiPref marginal rating distribution; three real new raters
whose fitted symmetric offsets (DFs, k = 50, stage 2c run A2, centred) lie closest to the 90th percentile of intensity (extreme − slight), the 10th percentile, and the 90th percentile of the tie offset."""
import json, glob, os, sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(os.path.dirname(HERE), "results"); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "..", "paper-2", "phase2")); import data_panels
lat = [r for f in sorted(glob.glob(f"{R}/stage2c_E1_f?_A2.json")) for r in json.load(open(f))["latents"]]
B = np.array([r["DFs"] for r in lat]); Bc = B - B.mean(0); inten = Bc[:, 0] - Bc[:, 1]
H = data_panels.load("multipref_overall")["H"]; base = np.bincount(H.reshape(-1), minlength=5) / H.size
pick = lambda v, q: int(np.abs(v - np.percentile(v, q)).argmin())
panels = [("all raters (marginal)", None), ("intense rater (90th pct.)", pick(inten, 90)), ("mild rater (10th pct.)", pick(inten, 10)), ("tie-prone rater (90th pct.)", pick(Bc[:, 2], 90))]
labels = ["A≫B", "A>B", "tie", "B>A", "B≫A"]
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 4, figsize=(6.8, 1.7), sharey=True)
for ax, (title, i) in zip(axes, panels):
    p = base if i is None else (lambda lg: np.exp(lg) / np.exp(lg).sum())(np.log(base) + Bc[i][[0, 1, 2, 1, 0]])
    ax.bar(range(5), p, color="#2a78d6" if i is not None else "#9a9993", width=0.7, edgecolor="#fcfcfb", linewidth=1.0)
    ax.set_xticks(range(5)); ax.set_xticklabels(labels, fontsize=6.5, color="#52514e"); ax.set_title(title, fontsize=7.5, color="#0b0b0b"); ax.tick_params(colors="#52514e", length=2)
    ax.grid(axis="y", color="#e6e5e0", lw=0.5); ax.set_axisbelow(True)
axes[0].set_ylabel("P(rating)", color="#52514e"); fig.tight_layout(); fig.savefig(f"{HERE}/fig_styles.pdf", bbox_inches="tight"); fig.savefig(f"{HERE}/fig_styles.png", dpi=160, bbox_inches="tight")
print({t: (None if i is None else Bc[i].round(2).tolist()) for t, i in panels})
