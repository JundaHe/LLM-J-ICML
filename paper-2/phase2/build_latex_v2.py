"""Build PAPER_DRAFT_v2.md -> latex_v2/main.pdf (pandoc + light post-processing). Reuses latex/preamble.tex (title replaced), the citation map and the Unicode map of build_latex.py.
v1 (build_latex.py / PAPER_DRAFT.md / latex/) is untouched. Usage: python build_latex_v2.py [--no-compile]"""
import os, re, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)); L = f"{P}/latex_v2"; os.makedirs(L, exist_ok=True)
subprocess.run([sys.executable, f"{P}/make_tables_v2.py"], check=True); subprocess.run([sys.executable, f"{P}/make_figures_v2.py"], check=True)
subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--wrap=none", f"{P}/PAPER_DRAFT_v2.md", "-o", f"{L}/body_raw.tex"], check=True)
raw = open(f"{L}/body_raw.tex").read()
title = open(f"{P}/PAPER_DRAFT_v2.md").readline().lstrip("# ").strip()
raw = raw[raw.index("\\subsection{Abstract"):]
raw = raw.replace("\\subsection{", "\\section{")
raw = re.sub(r"\\label\{[^}]*\}", "", raw); raw = re.sub(r"\\hypertarget\{[^}]*\}\{%\n", "", raw); raw = re.sub(r"(\\(?:sub)*section\{[^\n]*\})\}", r"\1", raw)
raw = re.sub(r"\\section\{Abstract[^}]*\}\s*\n\n(.*?)\n\n", lambda m: "\\begin{abstract}\n" + m.group(1) + "\n\\end{abstract}\n\n", raw, count=1, flags=re.S)
raw = re.sub(r"\\section\{\d+\.? ?", "\\\\section{", raw)
raw = re.sub(r"\\textbf\{(\d+\.\d+) ([^}]*)\}", r"\\subsection*{\1 \2}", raw)
raw = raw.replace("et al.~", "et al. ")
for k, v in {"Table 1": "tab:cards", "Table 2": "tab:decode", "Table 5": "tab:heads", "Table 6": "tab:budget", "Figure 1": "fig:reliability"}.items(): raw = raw.replace(k, "Table~\\ref{" + v + "}" if k.startswith("Table") else "Figure~\\ref{" + v + "}")
for head, tab in (("Two reliabilities of a disagreement histogram", "tab_cards"), ("Two reliabilities of a disagreement histogram", "fig_reliability"), ("Where the ordinal shape comes from", "tab_decode"), ("Spending the annotation budget", "tab_budget"), ("Spending the annotation budget", "tab_heads")):
    i = raw.find("\\section{" + head)
    if i >= 0: j = raw.index("\n", i); raw = raw[:j + 1] + "\\input{" + tab + "}\n" + raw[j + 1:]
src = open(f"{P}/build_latex.py").read()
ns = {}; exec(src[src.index("CIT = {"):src.index("for k, v in CIT.items()")], ns); exec(src[src.index("M = {"):src.index("for k, v in M.items()")], ns)
CIT = dict(ns["CIT"]); CIT.update({"Zhang, Gong \\& Choi (2021)": "\\citet{zhang2021learning}", "Zhang et al. (2021)": "\\citet{zhang2021learning}", "Sheng et al., 2008": "\\citealp{sheng2008get}", "Wan et al., 2023": "\\citealp{wan2023everyone}", "Zhang et al., 2025": "\\citealp{zhang2025diverging}", "Wong \\& Paritosh, 2022": "\\citealp{wong2022krater}", "Collins et al., 2022": "\\citealp{collins2022eliciting}", "Peterson et al., 2019": "\\citealp{peterson2019human}", "Chen et al. (2025)": "\\citet{chen2025beyond}", "Kohli (2026)": "\\citet{kohli2026metric}", "Chen et al., 2025": "\\citealp{chen2025beyond}", "Singh et al., 2025": "\\citealp{singh2025distributions}", "Kohli, 2026": "\\citealp{kohli2026metric}", "Benito-Santos \\& Ghajari, 2025": "\\citealp{benitosantos2025beyond}",
    "Uma et al., 2021": "\\citealp{uma2021learning}", "Plank, 2022": "\\citealp{plank2022problem}", "Crupi et al. (2025)": "\\citet{crupi2025effectiveness}", "Li et al., 2026": "\\citealp{li2026rethinking}", "Linacre, 1989": "\\citealp{linacre1989mfrm}",
    "Eckes, 2011": "\\citealp{eckes2011mfrm}", "Gheibi \\& Ghazizadeh, 2026": "\\citealp{gheibi2026same}", "Khetan et al., 2018": "\\citealp{khetan2018learning}", "Lin et al., 2014": "\\citealp{lin2014relabel}"})
for k, v in sorted(CIT.items(), key=lambda kv: -len(kv[0])): raw = raw.replace(k, v)
for k, v in ns["M"].items(): raw = raw.replace(k, v)
for k, v in {"⁵": "$^{5}$", "≫": "$\\gg$", "↔": "$\\leftrightarrow$", "ρ": "$\\rho$", "ĥ": "$\\hat h$", "§": "\\S{}", "½": "$\\tfrac12$", "≳": "$\\gtrsim$"}.items(): raw = raw.replace(k, v)
raw = raw.replace("$\\$", "$$").replace("$$-$$", "$-$")
left = sorted(set(ch for ch in raw if ord(ch) > 127)); assert not left, f"unmapped non-ascii: {left}"
pre = re.sub(r"\\title\{[^\n]*\}", lambda m: "\\title{" + title.replace("&", "\\&") + "}", open(f"{P}/latex/preamble.tex").read())
open(f"{L}/main.tex", "w").write(pre + "\\begin{document}\\maketitle\n" + raw + "\n\\bibliographystyle{plainnat}\n\\bibliography{../references}\n\\end{document}\n")
print("latex_v2/main.tex written;", len(raw.split()), "words")
if "--no-compile" not in sys.argv:
    def tex(): return subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], cwd=L, capture_output=True, text=True, errors="ignore")
    r = tex(); subprocess.run(["bibtex", "main"], cwd=L, capture_output=True); r = tex(); r = tex()
    log = open(f"{L}/main.log", errors="ignore").read(); print("pdflatex exit", r.returncode, "| undefined citations:", len(re.findall(r"Citation .* undefined", log)), "| overfull:", log.count("Overfull"))
    if r.returncode: print("\n".join(l for l in log.split("\n") if l.startswith("!"))[:800])
    print([l for l in subprocess.run(["pdfinfo", f"{L}/main.pdf"], capture_output=True, text=True).stdout.split("\n") if l.startswith("Pages")])
