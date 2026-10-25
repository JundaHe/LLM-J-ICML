"""Figures 2–4 from the frozen artefacts (no numbers typed by hand). Output: results/figures/fig{2,3,4}.{png,pdf}."""
import os, json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
P = os.path.dirname(os.path.abspath(__file__)); OUT = f"{P}/results/figures"; os.makedirs(OUT, exist_ok=True)
TAG = {"hs2_help5": "_v7", "popquorn_off8": "_v7", "dices990": "_v7", "popquorn_pol5": "_v7", "csc6": "_v7", "emobank_reader_v5": "_v7"}
def tag(key): return TAG.get(key, "_v6")
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False})
# ---------------- Fig 2: heads contrasts per panel with dose annotations
PANELS = [("hs2_help5", "HelpSteer2"), ("popquorn_pol5", "POPQUORN pol."), ("popquorn_off8", "POPQUORN off."), ("dices990", "DICES-990"), ("csc6", "CSC sarcasm"), ("emobank_reader_v5", "EmoBank val."), ("scalabrino", "Scalabrino"), ("summeval_coherence8", "SummEval coh."), ("bw", "Buse–Weimer"), ("dices", "DICES")]
ARMS = [("soft_pmmx", "mode+mean-preserving (pmmx)", "#1f77b4"), ("soft_pmode", "mode-only (pmode)", "#d62728"), ("hard", "one-hot (hard)", "#7f7f7f")]
fig, ax = plt.subplots(figsize=(9.8, 3.4)); x = np.arange(len(PANELS)); w = 0.26
for j, (arm, lab, col) in enumerate(ARMS):
    means, sems = [], []
    for key, _ in PANELS:
        df = pd.read_json(f"{P}/results/probe_mean2/{key}{tag(key)}/runs.jsonl", lines=True); piv = df.pivot_table(index=["seed", "isplit", "rsplit"], columns="arm", values="pop_rps"); d = piv[arm] - piv["soft"]; means.append(d.mean()); sems.append(d.sem())
    ax.bar(x + (j - 1) * w, means, w, yerr=sems, color=col, label=lab, error_kw=dict(lw=0.8, capsize=2))
DA = pd.read_csv(f"{P}/results/dose_audit_summary.csv")   # offline certificates incl. POST-PROJECTION pmmx dose
for i, (key, _) in enumerate(PANELS):
    rx = DA[(DA.panel == key) & (DA.arm == "soft_pmmx")].iloc[0]; rm = DA[(DA.panel == key) & (DA.arm == "soft_pmode")].iloc[0]
    ax.text(x[i], -0.0040, f"{rx.changed:.3f} / {rx.tv_chg:.3f}", ha="center", va="top", fontsize=5.5, color="#1f77b4")
    ax.text(x[i], -0.0060, f"{rm.changed:.3f} / {rm.tv_chg:.3f}", ha="center", va="top", fontsize=5.5, color="#d62728")
ax.axhline(0, color="k", lw=0.6); ax.set_xticks(x); ax.set_xticklabels([l for _, l in PANELS], rotation=20, ha="right"); ax.set_ylabel("RPS contrast vs. soft (arm − soft)\n[mean ± descriptive SEM over 30 dependent cfgs]")
ax.set_ylim(-0.010, 0.016); ax.legend(frameon=False, loc="upper left", fontsize=7); ax.text(0.995, 0.02, "text rows: pmmx (blue) and pmode (red) — changed fraction / TV among changed items", transform=ax.transAxes, ha="right", fontsize=6); ax.set_title("Fig. 2  Frozen-feature heads (ordinal panels): observed contrasts (descriptive) and realised dose", fontsize=8, loc="left")
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_heads_contrasts.png", dpi=200); fig.savefig(f"{OUT}/fig2_heads_contrasts.pdf"); plt.close(fig)
# ---------------- Fig 3: both LoRA blocks (SummEval T3b, POPQUORN T3c) — seed × fold cells (raw)
import sys; sys.path.insert(0, P); import data_panels
def rps_k(Pm, y, K): LVk = np.arange(K); cdf = np.cumsum(Pm, 1); step = (LVk[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
BLOCKS = [("summeval_coherence8", "SummEval coherence", "analysis_block_summeval.json", "expert", "chg 80.5–82.6 %, TV .335–.351", "chg 100 %, TV .296–.319"),
          ("popquorn_off8", "POPQUORN offensiveness", "analysis_block_popquorn.json", "position", "chg 68.7–71.7 %, TV .295–.301", "chg 100 %, TV .276–.288")]
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), sharey=False); cols = {2000: "C0", 2001: "C1", 2002: "C2"}
for bi, (key, label, jf, unit, dose_pc, dose_pm) in enumerate(BLOCKS):
    PAN = data_panels.load(key); H = PAN["H"]; K = PAN["K"]; R = f"{P}/results/lora/{key}"
    rows = {(r["contrast"], r["estimand"]): r for r in json.load(open(f"{R}/{jf}"))["rows"]}; cells = {}
    for seed in (2000, 2001, 2002):
        for fold in (0, 1, 2):
            base = f"{R}/{'s0' if seed == 2000 else f's0_seed{seed}'}/f{fold}"; it = pd.read_csv(f"{base}/chen/items_test.csv").row.to_numpy(); y = H[it, fold]
            Lx = {a: rps_k(np.load(f"{base}/{a}/P_test.npy"), y, K).mean() for a in ("chen", "perm", "perm_mode")}
            cells[(seed, fold)] = (Lx["perm"] - Lx["chen"], Lx["perm_mode"] - Lx["chen"])
    x0 = 4 * bi
    for ax, idx, ckey, dose in ((axes[0], 0, ("perm − chen", "raw"), dose_pc), (axes[1], 1, ("perm_mode − chen", "raw"), dose_pm)):
        for si, seed in enumerate((2000, 2001, 2002)):
            ax.scatter([x0 + f + (si - 1) * 0.12 for f in (0, 1, 2)], [cells[(seed, f)][idx] for f in (0, 1, 2)], color=cols[seed], label=f"seed {seed}" if bi == 0 else None, s=16, zorder=3)
        r = rows[ckey]; ax.fill_between([x0 - 0.4, x0 + 2.4], r["lo"], r["hi"], color="0.85", zorder=0); ax.plot([x0 - 0.4, x0 + 2.4], [r["est"]] * 2, color="k", lw=0.8)
        ax.text(x0 + 1, 1.0, f"{label}\n{r['est']:+.4f} [{r['lo']:+.4f}, {r['hi']:+.4f}]\n{dose}", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=5.2)
for ax, name in ((axes[0], "perm − chen (mode+mean-preserving)"), (axes[1], "perm_mode − chen (mode-only)")):
    ax.axhline(0, color="k", lw=0.4, ls=":"); ax.set_xticks([0, 1, 2, 4, 5, 6]); ax.set_xticklabels(["exp 0", "exp 1", "exp 2", "pos 0", "pos 1", "pos 2"], fontsize=6.5)
    ax.set_ylabel("raw RPS contrast", fontsize=7); ax.set_xlabel(name, fontsize=7.5)
fig.legend(*axes[0].get_legend_handles_labels(), frameon=False, fontsize=6, loc="upper right", ncol=3, bbox_to_anchor=(0.99, 0.95))
fig.suptitle("Fig. 3  Two LoRA blocks: raw RPS contrast per seed × fold; band = 95% crossed-bootstrap CI of the pooled contrast\n(the two panels use different vertical scales)", fontsize=7, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.84)); fig.savefig(f"{OUT}/fig3_summeval_block.png", dpi=200); fig.savefig(f"{OUT}/fig3_summeval_block.pdf"); plt.close(fig)
# ---------------- Fig 4: ChaosNLI m-sweeps (one subplot per nominal panel)
NOM = [("chaosnli_mnli", "MNLI", "_v6", f"{P}/results/nominal_final_dose.json"), ("chaosnli_snli", "SNLI", "_v7", f"{P}/results/nominal_final_dose_chaosnli_snli.json"), ("chaosnli_alphanli", "αNLI (K=2)", "_v7", f"{P}/results/nominal_final_dose_chaosnli_alphanli.json")]
NOM = [t for t in NOM if all(os.path.exists(f"{P}/results/probe_nominal/{t[0]}_m{mm}{t[2]}/runs.jsonl") for mm in (5, 10, 20, 50))]
fig, axes = plt.subplots(1, len(NOM), figsize=(4.0 * len(NOM), 3.0), squeeze=False); ms = (5, 10, 20, 50)
for ax, (pkey, plab, ptag, fdp) in zip(axes[0], NOM):
    series = {("soft_pzc", "soft", "pzc − soft (residual allocation scrambled)"): [], ("soft_pmode", "soft", "pmode − soft (mode-only donor)"): [], ("zc", "soft", "zc − soft (two-statistic target)"): []}; doses = []; tvf = {}
    for mm in ms:
        df = pd.read_json(f"{P}/results/probe_nominal/{pkey}_m{mm}{ptag}/runs.jsonl", lines=True); kl = df.pivot_table(index=["seed", "isplit"], columns="arm", values="kl_ref")
        for (a, b, _), lst in series.items(): d = kl[a] - kl[b]; lst.append((d.mean(), d.sem()))
        doses.append(df[df.arm == "soft_pzc"].changed_fraction.mean()); tvf[mm] = (df[df.arm == "soft_pzc"].dose_tv_final_all.mean(), df[df.arm == "soft_pmode"].dose_tv_final_all.mean())
    for (a, b, lab), lst in series.items(): ax.errorbar(ms, [v for v, _ in lst], yerr=[s for _, s in lst], marker="o", ms=3, lw=1, capsize=2, label=lab)
    FD = json.load(open(fdp)) if os.path.exists(fdp) else {}
    tab = "m   mapped  eff.chg  TV-all pzc/pmode\n" + "\n".join(f"{mm:<3d} {dz:.3f}   {FD.get(str(mm), {}).get('zc', {}).get('final_changed_1e6', float('nan')):.3f}    {tvf[mm][0]:.3f} / {tvf[mm][1]:.3f}" for mm, dz in zip(ms, doses))
    ax.text(0.98, 0.26, tab, transform=ax.transAxes, ha="right", va="top", fontsize=5, family="monospace", color="C0")
    ax.axhline(0, color="k", lw=0.5); ax.set_xscale("log"); ax.set_xticks(ms); ax.set_xticklabels([str(mm) for mm in ms]); ax.set_xlabel("training annotations per item (m)"); ax.set_title(f"ChaosNLI {plab}", fontsize=8)
axes[0][0].set_ylabel("KL contrast vs. soft (nats)\n[mean ± descriptive SEM, 9 dependent cfgs]"); axes[0][0].legend(frameon=False, fontsize=6)
fig.suptitle("Fig. 4  Nominal panels: KL contrasts vs. soft across annotation counts", fontsize=8, x=0.02, ha="left"); fig.tight_layout(); fig.savefig(f"{OUT}/fig4_chaosnli.png", dpi=200); fig.savefig(f"{OUT}/fig4_chaosnli.pdf"); plt.close(fig)
print("figures written:", sorted(os.listdir(OUT)))
