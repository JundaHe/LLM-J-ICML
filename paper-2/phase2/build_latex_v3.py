"""Build PAPER_ICML_v3.md -> latex_v3/main.pdf in an approximate ICML layout (two columns, 6.75in x 9in text block, Times), for page counting until the
official ICML 2027 style is released. Reuses build_latex_v2.py's citation and Unicode maps and make_tables_v2.py's tables (copied, with wide tables as table*).
Main-text tables: Table 1 (cards), Table 2 (own-shape), Table 3 (POPQUORN prospective budget rows); appendix: B1 (decode), D1 (all budget blocks), F1 (heads).
Usage: python build_latex_v3.py [--no-compile]"""
import os, re, shutil, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)); L2 = f"{P}/latex_v2"; L = f"{P}/latex_v3"; os.makedirs(L, exist_ok=True)
subprocess.run([sys.executable, f"{P}/make_tables_v2.py"], check=True); subprocess.run([sys.executable, f"{P}/make_figures_v2.py"], check=True)
for f in ("tab_cards", "tab_own", "tab_decode", "tab_budget", "tab_heads"):
    t = open(f"{L2}/{f}.tex").read().replace("\\begin{table}", "\\begin{table*}").replace("\\end{table}", "\\end{table*}")
    if f == "tab_budget": t = t.replace("(\\S5)", "(Appendix~C)")
    if f == "tab_own": t = re.sub(r"(\\begin\{tabular\}.*?\\end\{tabular\})", lambda m: "\\resizebox{\\textwidth}{!}{" + m.group(1) + "}", t, flags=re.S)  # 9 pt / 63 pt too wide in the ICML style
    t = t.replace("(\\S2.2)", "(\\S4)").replace("(\\S2.1)", "(\\S3)").replace("(\\S1)", "(Appendix~C)")  # v2 section numbers in make_tables_v2 captions
    open(f"{L}/{f}.tex", "w").write(t)
b = open(f"{L}/tab_budget.tex").read()
head, rest = b.split("\\midrule", 1)
rows = [l for l in b.split("\n") if l.startswith("POPQUORN, prospective")]
main = head.replace("\\label{tab:budget}", "\\label{tab:budgetmain}").replace("\\begin{table*}", "\\begin{table}").replace("\\begin{tabular}{llrrl}", "\\resizebox{\\columnwidth}{!}{\\begin{tabular}{llrrl}")
main = re.sub(r"\\caption\{.*?\}(?=\\label)", "\\\\caption{End-to-end LoRA judges on POPQUORN offensiveness at fixed rating budgets, prospective block with independent rating assignments (Qwen2.5-7B, R20-4): test RPS minus the full-data judge, 95\\\\% crossed bootstrap over optimizer seeds and test groups. All blocks, including SummEval (expert dilution), are in Table~\\\\ref{tab:budget}.}", main, flags=re.S)
open(f"{L}/tab_budget_main.tex", "w").write(main + "\\midrule\n" + "\n".join(r.replace("POPQUORN, prospective (Qwen2.5, R20-4)", "POPQUORN") for r in rows) + "\n\\bottomrule\\end{tabular}}\\end{table}\n")
open(f"{L}/tab_budget.tex", "w").write(re.sub(r"(\\begin\{tabular\}.*?\\end\{tabular\})", lambda m: "\\resizebox{\\textwidth}{!}{" + m.group(1) + "}", b, flags=re.S))  # 63 pt too wide in the ICML style
for f in ("fig_reliability.tex", "fig_reliability.pdf"): shutil.copy(f"{L2}/{f}", f"{L}/{f}")
subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--wrap=none", f"{P}/PAPER_ICML_v3.md", "-o", f"{L}/body_raw.tex"], check=True)
raw = open(f"{L}/body_raw.tex").read()
title = open(f"{P}/PAPER_ICML_v3.md").readline().lstrip("# ").strip()
raw = raw[raw.index("\\subsection{Abstract"):]
raw = re.sub(r"\\label\{[^}]*\}", "", raw); raw = re.sub(r"\\hypertarget\{[^}]*\}\{%\n", "", raw); raw = re.sub(r"(\\(?:sub)*section\{[^\n]*\})\}", r"\1", raw)
raw = re.sub(r"\\section\{Appendix\}", "\\\\onecolumn\n\\\\appendix", raw)
raw = raw.replace("\\subsection{", "\\section{")
raw = re.sub(r"\\section\{Abstract[^}]*\}\s*\n\n(.*?)\n\n\\section", lambda m: "\\begin{abstract}\n" + m.group(1) + "\n\\end{abstract}\n\n\\section", raw, count=1, flags=re.S)
raw = re.sub(r"\\section\{(?:\d+|[A-F])\.? ?", "\\\\section{", raw)
raw = raw.replace("et al.~", "et al. ")
for k, v in {"Table B1": "tab:decode", "Table D1": "tab:budget", "Table F1": "tab:heads", "Table 1": "tab:cards", "Table 2": "tab:own", "Table 3": "tab:budgetmain", "Figure 1": "fig:reliability"}.items():
    raw = raw.replace(k, "Table~\\ref{" + v + "}" if k.startswith("Table") else "Figure~\\ref{" + v + "}")
for head, tab in (("Reliability across raters", "fig_reliability"), ("Reliability across raters", "tab_cards"), ("Reliability across text", "tab_own"), ("Annotation budget", "tab_budget_main"),
                  ("Full decoding results", "tab_decode"), ("LoRA blocks", "tab_budget"), ("Frozen-feature heads, shrinkage", "tab_heads")):
    i = raw.find("\\section{" + head); assert i >= 0, head
    j = raw.index("\n", i); raw = raw[:j + 1] + "\\input{" + tab + "}\n" + raw[j + 1:]
src = open(f"{P}/build_latex_v2.py").read()
ns = {}; exec(src[src.index("src = open"):src.index("for k, v in sorted(CIT.items()")].replace('f"{P}/build_latex.py"', repr(f"{P}/build_latex.py")), ns)
for k, v in sorted(ns["CIT"].items(), key=lambda kv: -len(kv[0])): raw = raw.replace(k, v)
for k, v in ns["ns"]["M"].items(): raw = raw.replace(k, v)
for k, v in {"⁵": "$^{5}$", "≫": "$\\gg$", "↔": "$\\leftrightarrow$", "ρ": "$\\rho$", "ĥ": "$\\hat h$", "§": "\\S{}", "½": "$\\tfrac12$", "≳": "$\\gtrsim$", "γ": "$\\gamma$", "δ": "$\\delta$", "⁴": "$^{4}$", "α": "$\\alpha$", "⁷": "$^{7}$"}.items(): raw = raw.replace(k, v)
raw = raw.replace("$\\$", "$$").replace("$$-$$", "$-$")
left = sorted(set(ch for ch in raw if ord(ch) > 127)); assert not left, f"unmapped non-ascii: {left}"
pre = open(f"{P}/latex/preamble.tex").read()
pre = pre.replace("\\documentclass[10pt]{article}", "\\documentclass[10pt,twocolumn]{article}").replace("\\usepackage[margin=0.9in]{geometry}", "\\usepackage[textwidth=6.75in,textheight=9in,columnsep=0.25in,centering]{geometry}").replace("\\usepackage{lmodern}", "\\usepackage{times}")
pre = re.sub(r"\\title\{[^\n]*\}", lambda m: "\\title{" + title.replace("&", "\\&") + "}", pre)
open(f"{L}/main.tex", "w").write(pre + "\\begin{document}\\maketitle\n" + raw.replace("\\onecolumn\n\\appendix", "\\bibliographystyle{plainnat}\n\\bibliography{../references}\n\\onecolumn\n\\appendix") + "\n\\end{document}\n")
print("latex_v3/main.tex written;", len(raw.split()), "words")
# Second build with the ICML 2025 style (copied from paper-4/latex/icml2025; the 2027 style is unreleased) for a real page count: main_icml.pdf.
for f in ("icml2025.sty", "icml2025.bst", "fancyhdr.sty", "algorithm.sty", "algorithmic.sty"): shutil.copy(f"{P}/../../paper-4/latex/icml2025/{f}", f"{L}/{f}")
ipre = ("\\documentclass{article}\n\\usepackage{microtype}\\usepackage{graphicx}\\usepackage{booktabs}\\usepackage{hyperref}\\usepackage{amsmath}\\usepackage{amssymb}\\usepackage{xcolor}\n"
        "\\providecommand{\\tightlist}{\\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}\n\\usepackage{icml2025}\n\\icmltitlerunning{Five Raters Are Not a Distribution}\n\\begin{document}\n\\twocolumn[\n\\icmltitle{" + title.replace("&", "\\&") + "}\n"
        "\\begin{icmlauthorlist}\\icmlauthor{Anonymous Authors}{anon}\\end{icmlauthorlist}\n\\icmlaffiliation{anon}{Anonymous Institution}\n\\icmlcorrespondingauthor{Anonymous}{anon@example.com}\n\\vskip 0.3in]\n\\printAffiliationsAndNotice{}\n")
open(f"{L}/main_icml.tex", "w").write(ipre + raw.replace("\\onecolumn\n\\appendix", "\\bibliography{../references}\n\\bibliographystyle{icml2025}\n\\newpage\n\\appendix\n\\onecolumn") + "\n\\end{document}\n")
if "--no-compile" not in sys.argv:
    def tex(): return subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], cwd=L, capture_output=True, text=True, errors="ignore")
    r = tex(); subprocess.run(["bibtex", "main"], cwd=L, capture_output=True); r = tex(); r = tex()
    log = open(f"{L}/main.log", errors="ignore").read(); print("pdflatex exit", r.returncode, "| undefined refs/cites:", len(re.findall(r"(Citation|Reference) .* undefined", log)), "| overfull:", log.count("Overfull"))
    if r.returncode: print("\n".join(l for l in log.split("\n") if l.startswith("!"))[:800])
    print([l for l in subprocess.run(["pdfinfo", f"{L}/main.pdf"], capture_output=True, text=True).stdout.split("\n") if l.startswith("Pages")])
    def itex(): return subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main_icml.tex"], cwd=L, capture_output=True, text=True, errors="ignore")
    r = itex(); subprocess.run(["bibtex", "main_icml"], cwd=L, capture_output=True); r = itex(); r = itex()
    log = open(f"{L}/main_icml.log", errors="ignore").read(); print("ICML2025 style: exit", r.returncode, "| undefined:", len(re.findall(r"(Citation|Reference) .* undefined", log)), "| overfull:", log.count("Overfull"))
    if r.returncode: print("\n".join(l for l in log.split("\n") if l.startswith("!"))[:800])
    ref = [i + 1 for i in range(40) if subprocess.run(["pdftotext", "-f", str(i + 1), "-l", str(i + 1), f"{L}/main_icml.pdf", "-"], capture_output=True, text=True).stdout.count("\nReferences\n")]
    print("ICML2025 style: pages", [l for l in subprocess.run(["pdfinfo", f"{L}/main_icml.pdf"], capture_output=True, text=True).stdout.split("\n") if l.startswith("Pages")], "| References heading on page", ref)
