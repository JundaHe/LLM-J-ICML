"""Build paper-4/latex/main.pdf (ICML 2025 style as a stand-in for the 2027 template) from paper-4/PAPER4_DRAFT.md: pandoc body, author-year natbib citations
mapped from references_p4.bib, pandoc longtables turned into two-column-safe table* floats, Unicode mapped to LaTeX. Anonymous submission mode."""
import re, os, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); P4 = os.path.dirname(HERE)
md = open(f"{P4}/PAPER4_DRAFT.md").read()
title = md.splitlines()[0].lstrip("# ").strip()
body = "\n".join(l for l in md.splitlines()[1:] if not l.startswith("*Draft"))
CIT = {"Siththaranjan et al., 2024": "siththaranjan2024dpl", "Kirk et al., 2024": "kirk2024prism", "Gordon et al., 2022": "gordon2022jury", "Poddar et al., 2024": "poddar2024vpl",
       "Chen et al., 2025": "chen2025pal", "Sorensen et al., 2024": "sorensen2024roadmap", "Zhang et al., 2025": "zhang2025diverging", "Miranda et al., 2025": "miranda2025hybrid",
       "Davani et al., 2022": "davani2022dealing", "Li et al., 2024": "li2024prlhf", "Orlikowski et al., 2023": "orlikowski2023ecological", "Baumgartner & Steenkamp, 2001": "baumgartner2001response",
       "Linacre, 1989": "linacre1989mfrm", "Eckes, 2011": "eckes2011mfrm", "Aroyo et al., 2023": "aroyo2023dices", "Bose et al., 2025": "bose2025lore", "Ryan et al., 2025": "ryan2025synthesizeme", "Dong et al., 2025": "dong2025personalization", "Mishra et al., 2026": "mishra2026decoding", "Kim & Kim, 2026": "kim2026swap", "Deng et al., 2023": "deng2023annotate", "Koren et al., 2009": "koren2009mf", "Koren & Sill, 2011": "koren2011ordrec", "Dawid & Skene, 1979": "dawid1979em", "Raykar et al., 2010": "raykar2010crowds", "Hovy et al., 2013": "hovy2013mace", "Plank, 2022": "plank2022problem", "Uma et al., 2021": "uma2021learning", "Kim & Kim (ICLR 2026)": None}
for k, v in sorted(CIT.items(), key=lambda kv: -len(kv[0])):
    if v: body = body.replace(k, f"@@CITE{{{v}}}@@")
body = body.replace("[companion paper, anonymised]", "a companion study (anonymised)")
open(f"{HERE}/body.md", "w").write(body)
tex = subprocess.run(["pandoc", f"{HERE}/body.md", "-f", "markdown", "-t", "latex", "--wrap=none", "--shift-heading-level-by=-1"], capture_output=True, text=True, check=True).stdout
tex = re.sub(r"@@CITE\\\{([^}]*)\\\}@@", r"\\citealp{\1}", tex); tex = re.sub(r"@@CITE\{([^}]*)\}@@", r"\\citealp{\1}", tex)
# abstract
m = re.search(r"\\section\{Abstract[^}]*\}\\label\{[^}]*\}\s*(.*?)\n\\section", tex, re.S)
abstract = m.group(1).strip(); tex = tex[:m.start()] + "\\section" + tex[m.end():]
tex = re.sub(r"\\label\{[^}]*\}", "", tex); tex = re.sub(r"\\section\{\d+\.?\s*", r"\\section{", tex); tex = re.sub(r"\\subsection\{\d+\.\d+\s*", r"\\subsection{", tex)
# longtable → table*
def tab(mm):
    t = mm.group(0); spec = re.search(r"\\begin\{longtable\}\[\]\{(.*?)\}\n", t).group(1)
    t = re.sub(r"\\begin\{longtable\}\[\]\{.*?\}\n", "\\\\begin{table*}[t]\\\\centering\\\\footnotesize\\\\begin{tabular}{" + re.sub(r"@\{\}", "", spec).replace("\\real", "") + "}\n", t, count=1)
    t = re.sub(r"\\endhead|\\endfirsthead|\\endlastfoot|\\endfoot", "", t); t = t.replace("\\bottomrule\\noalign{}", "").replace("\\bottomrule", ""); t = t.replace("\\end{longtable}", "\\bottomrule\n\\end{tabular}\\end{table*}")
    t = re.sub(r">\{\\raggedright\\arraybackslash\}p\{\(\\linewidth - \d+\\tabcolsep\) \* \\real\{[0-9.]+\}\}", "l", t)
    return t
tex = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", tab, tex, flags=re.S)
tex = re.sub(r"\\begin\{minipage\}\[b\]\{\\linewidth\}\\raggedright\s*(.*?)\s*\\end\{minipage\}", r"\1", tex, flags=re.S)
U = {"−": "$-$", "≈": "$\\approx$", "≤": "$\\leq$", "≥": "$\\geq$", "×": "$\\times$", "…": "\\ldots{}", "²": "$^2$", "₀": "$_0$", "ℓ": "$\\ell$", "ρ": "$\\rho$", "∈": "$\\in$",
     "·": "$\\cdot$", "½": "$\\tfrac12$", "§": "\\S{}", "–": "--", "—": "---", "→": "$\\to$", "θ": "$\\theta$", "τ": "$\\tau$"}
for k, v in U.items(): tex = tex.replace(k, v); abstract = abstract.replace(k, v); title = title.replace(k, v)
i_app = tex.find("\\section{Appendix A.")
if i_app >= 0: tex = tex[:i_app] + "\\appendix\n" + tex[i_app:]
tex = re.sub(r"\\section\{Appendix [A-Z]\.\s*", r"\\section{", tex)
FIG = r"""\begin{figure*}[t]\centering\includegraphics[width=\textwidth]{fig_main.pdf}
\caption{New raters: gain in held-out log-likelihood per rating over the text-only distributional reward model (D), as a function of the number k of the new rater's ratings used for adaptation; 95\% rater-cluster bootstrap bands, 5 folds. Text-independent rater offsets (DF; symmetric three-parameter DFs on two-sided preferences) gain 0.08--0.10 nats per rating at k = 20 on all three datasets; group offsets (crowd/expert, race, region) gain nothing; a low-rank text-interacting rater latent with a few-shot-tuned prior ties the three-parameter DFs and beats the five-offset DF on MultiPref (DF $-$ DL = $-$0.015). DF, DFs and DG use the training-rater prior; DL the few-shot-tuned prior.}\label{fig:main}\end{figure*}
"""
i = tex.find("\\section{Experiments}"); j = tex.index("\n", i); tex = tex[:j + 1] + FIG + tex[j + 1:]
FIG2 = r"""\begin{figure*}[t]\centering\includegraphics[width=\textwidth]{fig_styles.pdf}
\caption{What three numbers per rater change. Left: the marginal distribution of MultiPref ratings. Right: the same distribution passed through the fitted scale-use offsets (extreme, slight, tie) of three real new raters (k = 50) closest to the 90th / 10th percentile of intensity (extreme minus slight) among raters whose tie offset is at or below the median, and closest to the 90th percentile of the tie offset. The offsets are text-independent: they reshape how strongly a rater is predicted to prefer, not which side.}\label{fig:styles}\end{figure*}
"""
i2 = tex.find("\\section{A three-parameter scale-use baseline}"); j2 = tex.index("\n", i2); tex = tex[:j2 + 1] + FIG2 + tex[j2 + 1:]
left = sorted(set(c for c in tex + abstract if ord(c) > 127)); assert not left, f"unmapped: {left}"
pre = r"""\documentclass{article}
\usepackage{microtype}\usepackage{graphicx}\usepackage{booktabs}\usepackage{hyperref}\usepackage{amsmath}\usepackage{amssymb}\usepackage{longtable}\usepackage{array}\usepackage{calc}
\newcommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\real}[1]{#1}
\usepackage{icml2025}
\icmltitlerunning{What Personalised Reward Models Learn About a New Rater}
\begin{document}
\twocolumn[
\icmltitle{""" + title + r"""}
\begin{icmlauthorlist}\icmlauthor{Anonymous Authors}{anon}\end{icmlauthorlist}
\icmlaffiliation{anon}{Anonymous Institution}
\icmlcorrespondingauthor{Anonymous}{anon@example.com}
\vskip 0.3in]
\printAffiliationsAndNotice{}
\begin{abstract}
""" + abstract + "\n\\end{abstract}\n"
open(f"{HERE}/main.tex", "w").write(pre + tex + "\n\\bibliography{../references_p4}\n\\bibliographystyle{icml2025}\n\\end{document}\n")
for f in ("icml2025.sty", "icml2025.bst", "fancyhdr.sty", "algorithm.sty", "algorithmic.sty"): shutil.copy(f"{HERE}/icml2025/{f}", f"{HERE}/{f}")
run = lambda c: subprocess.run(c, cwd=HERE, capture_output=True, text=True)
run(["pdflatex", "-interaction=nonstopmode", "main.tex"]); run(["bibtex", "main"]); run(["pdflatex", "-interaction=nonstopmode", "main.tex"]); r = run(["pdflatex", "-interaction=nonstopmode", "main.tex"])
log = open(f"{HERE}/main.log", errors="ignore").read()
print("errors:", log.count("\n!"), "| undefined citations:", len(re.findall(r"Citation `[^']*' .*undefined", log)), "| pages:", re.findall(r"Output written on main.pdf \((\d+) pages", log))
