"""LaTeX tables from the frozen artefacts (same sources as RESULTS_TABLES): latex/tab_heads.tex (T2b compact), latex/tab_summeval.tex (T3b + T3c LoRA blocks), latex/tab_nominal.tex (T5 MNLI+SNLI)."""
import os, json, numpy as np, pandas as pd
P = os.path.dirname(os.path.abspath(__file__)); L = f"{P}/latex"; os.makedirs(L, exist_ok=True)
TAG = {"hs2_help5": "_v7", "popquorn_off8": "_v7", "dices990": "_v7", "popquorn_pol5": "_v7", "csc6": "_v7", "emobank_reader_v5": "_v7"}
PANELS = [("summeval_coherence8", "SummEval coherence", 8), ("popquorn_off8", "POPQUORN offensiveness", 8), ("csc6", "CSC sarcasm (K=6)", 6), ("scalabrino", "Scalabrino readability", 9), ("popquorn_pol5", "POPQUORN politeness", 5), ("hs2_help5", "HelpSteer2 helpfulness", 5), ("emobank_reader_v5", "EmoBank valence", 5), ("bw", "Buse--Weimer readability", 121), ("dices", "DICES-350", 104), ("dices990", "DICES-990", 60)]
DA = pd.read_csv(f"{P}/results/dose_audit_summary.csv")
def pm(d, nd=4): return f"${d.mean():+.{nd}f}\\pm{d.sem():.{nd}f}$"
rows = []
for key, lab, nr in PANELS:
    df = pd.read_json(f"{P}/results/probe_mean2/{key}{TAG.get(key, '_v6')}/runs.jsonl", lines=True); idx = ["seed", "isplit", "rsplit"]
    piv = df.pivot_table(index=idx, columns="arm", values="pop_rps", dropna=False); rx = DA[(DA.panel == key) & (DA.arm == "soft_pmmx")].iloc[0]
    c = lambda a: pm(piv[a] - piv["soft"])
    rows.append(f"{lab} & {nr} & {rx.changed:.2f} & {rx.tv_all:.2f} & {c('soft_pmmx')} & {c('soft_pmode')} & {c('hard')} & {c('sordm')} & {c('cond')} \\\\")
tab = r"""\begin{table*}[t]\centering\footnotesize\setlength{\tabcolsep}{3.5pt}
\caption{Frozen-feature heads on ten ordinal panels: observed RPS contrasts (arm $-$ soft; mean $\pm$ descriptive SEM over 30 dependent configurations, not inferential intervals). Columns pmmx/pmode/hard/sordm/cond give arm $-$ soft. Dose = realised post-projection changed fraction of training targets under exact mode-and-mean-preserving replacement (pmmx; changed = TV $>10^{-9}$) and the resulting TV averaged over all training items. pmode = mode-only replacement; sordm = SORD Gaussian at the item mean; cond = cross-fitted conditional reference.}
\label{tab:heads}
\resizebox{\textwidth}{!}{\begin{tabular}{lrrrrrrrr}\toprule
panel & $n_r$ & changed & TV-all & pmmx & pmode & hard & sordm & cond \\ \midrule
""" + "\n".join(rows) + "\n" + r"""\bottomrule\end{tabular}}\end{table*}
"""
open(f"{L}/tab_heads.tex", "w").write(tab)
# ---- LoRA blocks (SummEval T3b + POPQUORN T3c)
def load_rows(f): return {(r["contrast"], r["estimand"]): r for r in json.load(open(f))["rows"]}
RS = load_rows(f"{P}/results/lora/summeval_coherence8/analysis_block_summeval.json"); RP = load_rows(f"{P}/results/lora/popquorn_off8/analysis_block_popquorn.json")
def cell(R, k): r = R[k]; return f"${r['est']:+.4f}$ [{r['lo']:+.4f}, {r['hi']:+.4f}]"
def seeds(R, k): return " / ".join(f"{v:+.4f}" for v in R[k]["per_seed"].values())
CONS = (("perm $-$ chen (mode+mean preserved)", "perm − chen"), ("perm\\_mode $-$ chen (mode only)", "perm_mode − chen"), ("perm\\_mode $-$ perm", "perm_mode − perm"))
body = ""
for title, R in (("SummEval coherence (3 persistent experts held out; document-level inference)", RS), ("POPQUORN offensiveness (3 annotation positions held out; item-level inference conditional on the rater panel)", RP)):
    body += f"\\multicolumn{{4}}{{l}}{{\\emph{{{title}}}}} \\\\\n" + "\n".join(f"{name} & {cell(R, (c,'raw'))} & {cell(R, (c,'common'))} & {cell(R, (c,'arm'))} \\\\" for name, c in CONS) + "\n\\midrule\n"
body = body[: -len("\\midrule\n")]
tab2 = (r"""\begin{table}[t]\centering\footnotesize\setlength{\tabcolsep}{3pt}
\caption{LoRA judges (Qwen2.5-7B-Instruct; three optimizer seeds, each paired with one item-assignment seed; three held-out folds; split 0). Raw RPS contrasts with 95\% crossed-bootstrap intervals over the three joint seed clusters and test documents (SummEval) or test items (POPQUORN); calibrated sensitivities resample calibration units and refit maps. Seed-marginal raw means, perm $-$ chen: SummEval SPC, POPQUORN PPC; perm\_mode $-$ chen: SummEval SPM, POPQUORN PPM. Dose: SummEval perm changed 80.5--82.6\% of targets (TV among changed 0.335--0.351), POPQUORN 68.7--71.7\% (0.295--0.301); perm\_mode changed 100\%. POPQUORN position folds hold out ratings, not persons; a rater-aware (item $\times$ user) bootstrap widens its intervals (Section~4).}
\label{tab:summeval}
\resizebox{\columnwidth}{!}{\begin{tabular}{llll}\toprule
contrast & raw & common map & arm-specific \\ \midrule
""" + body + r"""\bottomrule\end{tabular}}\end{table}
""").replace("SPC", seeds(RS, ("perm − chen","raw"))).replace("PPC", seeds(RP, ("perm − chen","raw"))).replace("SPM", seeds(RS, ("perm_mode − chen","raw"))).replace("PPM", seeds(RP, ("perm_mode − chen","raw")))
open(f"{L}/tab_summeval.tex", "w").write(tab2)
# ---- nominal
rows3 = []
for pkey, plab, ptag, fds in (("chaosnli_mnli", "MNLI", "_v6", ""), ("chaosnli_snli", "SNLI", "_v7", "_chaosnli_snli")):
    for m in (5, 10, 20, 50):
        df = pd.read_json(f"{P}/results/probe_nominal/{pkey}_m{m}{ptag}/runs.jsonl", lines=True); kl = df.pivot_table(index=["seed", "isplit"], columns="arm", values="kl_ref"); dz = df[df.arm == "soft_pzc"]
        rows3.append(f"{plab} & {m} & {dz.changed_fraction.mean():.3f} & {dz.dose_tv_final_all.mean():.3f} & {pm(kl['soft_pzc']-kl['soft'],3)} & {pm(kl['soft_pmode']-kl['soft'],3)} & {pm(kl['zc']-kl['soft'],3)} & {pm(kl['cond']-kl['soft'],3)} \\\\")
tab3 = r"""\begin{table}[t]\centering\footnotesize\setlength{\tabcolsep}{3pt}
\caption{Nominal ChaosNLI panels (frozen-feature heads): mean test KL to a fixed 50-annotation reference panel, contrasts vs.\ training on the $m$-annotation histogram (mean $\pm$ descriptive SEM over nine dependent configurations). Columns pzc/pmode/zc/cond give arm $-$ soft in KL. pzc scrambles residual class allocation while retaining the modal class and its mass; dose = donor-mapped fraction and final TV over all training items. Binary $\alpha$NLI (zero-dose limit) is reported in the text.}
\label{tab:nominal}
\begin{tabular}{llrrllll}\toprule
panel & $m$ & mapped & TV-all & pzc & pmode & zc & cond \\ \midrule
""" + "\n".join(rows3) + "\n" + r"""\bottomrule\end{tabular}\end{table}
"""
open(f"{L}/tab_nominal.tex", "w").write(tab3); print("latex tables written")
