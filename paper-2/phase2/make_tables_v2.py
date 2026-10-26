"""LaTeX tables for PAPER_DRAFT_v2 → latex_v2/tab_*.tex: reliability cards (Table 1), cross-family decoding (Table 2), fixed-budget LoRA (Table 3)."""
import json, glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); L = f"{HERE}/latex_v2"; os.makedirs(L, exist_ok=True)
def f4(x): return ("$-$" if x < 0 else "$+$") + f"{abs(x):.4f}"
def f5(x): return ("$-$" if x < 0 else "$+$") + f"{abs(x):.5f}"
NAME = {"summeval_coherence8": "SummEval coh.", "summeval_relevance8": "SummEval rel.", "popquorn_off8": "POPQUORN off.", "popquorn_pol5": "POPQUORN pol.", "hs2_help5": "HelpSteer2", "emobank_reader_v5": "EmoBank",
        "csc6": "CSC sarcasm", "scalabrino": "Scalabrino$^{SE}$", "bw": "Buse--Weimer$^{SE}$", "dices": "DICES-350", "dices990": "DICES-990", "dorn_java": "Dorn Java$^{SE}$", "dorn_all": "Dorn (all)$^{SE}$",
        "crupi_ca": "Crupi CA$^{SE}$", "crupi_conc": "Crupi conc.$^{SE}$", "crupi_flu": "Crupi flu.$^{SE}$", "mlcq3": "MLCQ$^{SE}$", "roy_ca": "Roy CA$^{SE}$", "jb_naming": "JetBrains naming$^{SE}$",
        "chaosnli_mnli": "ChaosNLI MNLI", "chaosnli_snli": "ChaosNLI SNLI"}
# Table 1: reliability cards at a = m-1 (loo) or largest a
rows = {}
for f in glob.glob(f"{HERE}/results/finite_rater/*.json"):
    b = os.path.basename(f)[:-5]
    if b in ("summary", "moderator", "dices_raw", "dices_raw_loo", "chaosnli_alphanli"): continue
    r = json.load(open(f)); loo = b.endswith("_loo")
    for row in r["rows"]:
        k = r["panel"]
        if k not in NAME: continue
        if k not in rows or (loo and not rows[k][0]) or (loo == rows[k][0] and row["a"] > rows[k][1]["a"]): rows[k] = (loo, row, r["m"])
t = ["\\begin{table}[t]\\centering\\footnotesize", "\\caption{Disagreement reliability cards. $A1^x>0$: the raw $a$-rater histogram forecasts a new rater worse than the exact mode-and-mean comparator. $\\rho=X/M$: split-half reliability of the shape (smoothed comparator). Support: share of items whose histogram can be changed at all with mode and mean fixed. SE = software-engineering panel.}\\label{tab:cards}",
     "\\begin{tabular}{lrrrrr}\\toprule panel & raters & $a$ & $A1^x$ & $\\rho$ & support \\\\\\midrule"]
for k in sorted(rows, key=lambda k: (k.startswith("chaosnli"), rows[k][2] > 20, NAME[k])):
    loo, row, m = rows[k]; sup = row.get("A2", {}).get("changed_fraction")
    t.append(f"{NAME[k]} & {m} & {row['a']} & {f4(row['est']['A1x'])} & {row['est']['rho']:.2f} & {('%.2f' % sup) if sup is not None else '--'} \\\\")
t += ["\\bottomrule\\end{tabular}\\end{table}"]; open(f"{L}/tab_cards.tex", "w").write("\n".join(t))
# Table 2: cross-family decoding
FAM = {"": "Qwen2.5-7B", "_qwen3": "Qwen3-8B", "_olmo": "OLMo-2-7B"}; D = {}
for f in glob.glob(f"{HERE}/results/decoding/*_d64_E_last*.json"):
    m_ = re.match(r"(.+)_d64_E_last(_qwen3|_olmo)?\.json$", os.path.basename(f))
    if m_ and m_.group(1) in NAME: r = json.load(open(f)); D.setdefault(m_.group(1), {})[m_.group(2) or ""] = (r["est"]["G"], r["ci95"]["G"], r["est"]["pos_ctrl"])
t = ["\\begin{table}[t]\\centering\\footnotesize", "\\caption{Decodability of the residual beyond exact mode and mean from frozen representations of three model families: proper-score gain $G$ on an independent rater panel (95\\% item-cluster bootstrap); positive control in parentheses (Spearman of the decoded vs held-out mean).}\\label{tab:decode}",
     "\\begin{tabular}{l" + "l" * len(FAM) + "}\\toprule panel & " + " & ".join(FAM.values()) + " \\\\\\midrule"]
for k in sorted(D, key=lambda k: (k.startswith("chaosnli"), NAME[k])):
    cells = [(f"{f5(D[k][fm][0])} ({D[k][fm][2]:.2f})" if fm in D[k] else "--") for fm in FAM]
    t.append(f"{NAME[k]} & " + " & ".join(cells) + " \\\\")
t += ["\\bottomrule\\end{tabular}\\end{table}"]; open(f"{L}/tab_decode.tex", "w").write("\n".join(t))
# Table 3: LoRA fixed budget (SummEval + POPQUORN)
t = ["\\begin{table}[t]\\centering\\footnotesize", "\\caption{End-to-end LoRA judges (distributional objective; Qwen2.5-7B and, for SummEval, OLMo-2-7B) at fixed rating budgets: test RPS minus the full-data judge, 95\\% crossed bootstrap over optimizer seeds and test groups.}\\label{tab:budget}",
     "\\begin{tabular}{llrrl}\\toprule panel & design (items $\\times$ ratings) & ratings & RPS & $-$ full data \\\\\\midrule"]
for p, fn in (("SummEval (Qwen2.5)", "lora_budget/summary.json"), ("POPQUORN (Qwen2.5)", "lora_budget/summary_popquorn_off8.json"), ("SummEval (OLMo-2)", "lora_budget_olmo/summary.json")):
    S = json.load(open(f"{HERE}/results/{fn}"))
    for name, v in sorted(S.items(), key=lambda kv: (kv[1]["rating_budget"], -kv[1]["n_train"])):
        a = 7 if name.startswith("full") else int(re.match(r"a(\d+)", name).group(1)); des = f"{v['n_train']} $\\times$ {a}"
        t.append(f"{p} & {des} & {v['rating_budget']} & {v['rps']:.4f} & " + ("--" if name.startswith("full") else f"{f4(v['diff_vs_full'])} [{f4(v['ci95'][0])}, {f4(v['ci95'][1])}]") + " \\\\")
    t.append("\\midrule")
t[-1] = "\\bottomrule\\end{tabular}\\end{table}"; open(f"{L}/tab_budget.tex", "w").write("\n".join(t)); print("tables written")
