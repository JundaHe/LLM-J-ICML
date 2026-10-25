"""Reproducible LaTeX build: PAPER_DRAFT.md -> latex/main.tex (pandoc + post-processing), tables via make_latex_tables.py, then pdflatex/bibtex. Usage: python build_latex.py [--no-compile]"""
import os, re, subprocess, sys
P = os.path.dirname(os.path.abspath(__file__)); L = f"{P}/latex"; os.makedirs(L, exist_ok=True)
subprocess.run([sys.executable, f"{P}/make_latex_tables.py"], check=True)
subprocess.run(["pandoc", "-f", "markdown", "-t", "latex", "--wrap=none", f"{P}/PAPER_DRAFT.md", "-o", f"{L}/body_raw.tex"], check=True)
raw = open(f"{L}/body_raw.tex").read()
raw = raw[raw.index("\\subsection{Abstract}"):] if "\\subsection{Abstract}" in raw else raw
raw = raw.replace("\\subsubsection{", "\\SUBSUB{").replace("\\subsection{", "\\section{").replace("\\SUBSUB{", "\\subsection{")
raw = re.sub(r"\\label\{[^}]*\}", "", raw); raw = re.sub(r"\\hypertarget\{[^}]*\}\{%\n", "", raw); raw = re.sub(r"(\\(?:sub)*section\{[^\n]*\})\}", r"\1", raw)
raw = re.sub(r"\\section\{Abstract\}\s*\n\n(.*?)\n\n", lambda m: "\\begin{abstract}\n" + m.group(1) + "\n\\end{abstract}\n\n", raw, count=1, flags=re.S)
i = raw.index("\\section{Figures}"); j = raw.index("\\section{1. Introduction}"); raw = raw[:i] + raw[j:]
raw = re.sub(r"\\section\{\d+[a-z]?\.? ?", "\\\\section{", raw); raw = re.sub(r"\\subsection\{\d+\.\d+ ?", "\\\\subsection{", raw)
raw = raw.replace("\\section{Appendix B. ", "\\appendix\n\\section{").replace("\\section{Appendix C. ", "\\section{")
raw = raw.replace("\\section{Results --- frozen-feature heads (Tables T2b/T2c, T4, T5)}", "\\section{Results: frozen-feature heads}\n\\input{tab_heads}")
raw = raw.replace("\\section{Results --- LoRA judges (two end-to-end blocks; T3b--T3c)}", "\\section{Results: LoRA judges}\n\\input{tab_summeval}")
raw = raw.replace("\\textbf{Nominal panels (ChaosNLI MNLI, SNLI and αNLI, T5).}", "\\input{tab_nominal}\n\\textbf{Nominal panels (ChaosNLI MNLI, SNLI and αNLI; Table~\\ref{tab:nominal}).}")
raw = raw.replace("\\subsection{Dose and support (must accompany every permutation contrast)}", "\\subsection{Dose and support}")
raw = raw.replace("et al.~", "et al. ").replace("\\&", "&")
CIT = {"Chen et al. (2025)": "\\citet{chen2025beyond}", "Chen et al. 2025": "\\citealp{chen2025beyond}", "Singh et al. (2025)": "\\citet{singh2025distributions}", "Singh et al. 2025": "\\citealp{singh2025distributions}", "Kohli (2026)": "\\citet{kohli2026metric}", "Kohli 2026": "\\citealp{kohli2026metric}", "Steindl et al. 2026": "\\citealp{steindl2026posthoc}", "Guerdan et al. (2025)": "\\citet{guerdan2025validating}", "Elangovan et al. (2025)": "\\citet{elangovan2025beyond}", "Gheibi & Ghazizadeh (2026)": "\\citet{gheibi2026same}", "Behrens & Zdeborová (2026)": "\\citet{behrens2026dataset}", "Zhang et al. 2017": "\\citealp{zhang2017understanding}", "Breiman 2001": "\\citealp{breiman2001random}", "Fisher et al. 2019": "\\citealp{fisher2019all}", "Ojala & Garriga 2010": "\\citealp{ojala2010permutation}", "Strobl et al. 2008": "\\citealp{strobl2008conditional}", "Debeer & Strobl 2020": "\\citealp{debeer2020conditional}", "Geng 2016": "\\citealp{geng2016ldl}", "Aroyo & Welty 2015": "\\citealp{aroyo2015truth}", "Pavlick & Kwiatkowski 2019": "\\citealp{pavlick2019inherent}", "Uma et al. 2021": "\\citealp{uma2021learning}", "Plank 2022": "\\citealp{plank2022problem}", "Basile et al. 2021": "\\citealp{basile2021we}", "Nie et al. 2020": "\\citealp{nie2020chaosnli}", "Zhou et al. 2022": "\\citealp{zhou2022distributed}", "Leonardelli et al. 2023": "\\citealp{leonardelli2023lewidi}", "Leonardelli et al. 2025": "\\citealp{leonardelli2025lewidi}", "Pei & Jurgens 2023": "\\citealp{pei2023popquorn}", "Buechel & Hahn 2017": "\\citealp{buechel2017emobank}", "Aroyo et al. 2023": "\\citealp{aroyo2023dices}", "Fabbri et al. 2021": "\\citealp{fabbri2021summeval}", "Wang et al. 2024": "\\citealp{wang2024helpsteer2}", "Davani et al. 2022": "\\citealp{davani2022dealing}", "Gordon et al. 2022": "\\citealp{gordon2022jury}", "Fleisig et al. 2023": "\\citealp{fleisig2023majority}", "Díaz & Marathe 2019": "\\citealp{diaz2019soft}", "Wen et al. 2023": "\\citealp{wen2023ordinal}", "Szegedy et al. 2016": "\\citealp{szegedy2016rethinking}", "Müller et al. 2019": "\\citealp{muller2019when}", "Epstein 1969": "\\citealp{epstein1969scoring}", "Gneiting & Raftery 2007": "\\citealp{gneiting2007strictly}", "Guo et al. 2017": "\\citealp{guo2017calibration}", "Lakens 2017": "\\citealp{lakens2017equivalence}", "Schuirmann 1987": "\\citealp{schuirmann1987comparison}"}
for k, v in CIT.items(): raw = raw.replace(k, v)
raw = raw.replace("&", "\\&")
M = {"−": "$-$", "±": "$\\pm$", "×": "$\\times$", "≈": "$\\approx$", "≥": "$\\geq$", "≤": "$\\leq$", "→": "$\\rightarrow$", "↔": "$\\leftrightarrow$", "α": "$\\alpha$", "λ": "$\\lambda$", "μ": "$\\mu$", "ρ": "$\\rho$", "π": "$\\pi$", "Δ": "$\\Delta$", "‖": "$\\|$", "·": "$\\cdot$", "—": "---", "–": "--", "‘": "`", "’": "'", "“": "``", "”": "''", "…": "\\ldots{}", "⁻": "$^{-}$", "⁹": "$^{9}$", "⁶": "$^{6}$", "∈": "$\\in$", "ε": "$\\varepsilon$", "σ": "$\\sigma$", "ĥ": "$\\hat{h}$", "ₑ": "$_e$", "₋": "$_-$", "ₜ": "$_t$", "ᵢ": "$_i$", "η": "$\\eta$", "ö": "\\\"o", "ü": "\\\"u", "é": "\\'e", "í": "\\'i", "á": "\\'a", "ó": "\\'o", "ú": "\\'u", "ś": "\\'s", "ń": "\\'n", "ç": "\\c{c}", "ğ": "\\u{g}", "ı": "{\\i}", "Ç": "\\c{C}", "ş": "\\c{s}", "Σ": "$\\Sigma$", "∞": "$\\infty$", "≡": "$\\equiv$", "∑": "$\\sum$", "′": "'", "\u2009": "\\,", "\u00a0": "~", "\u202f": "\\,", "\u2212": "$-$"}
for k, v in M.items(): raw = raw.replace(k, v)
raw = raw.replace("$\\$", "$$").replace("$$-$$", "$-$")   # guard double math from pandoc-escaped dollars inside math
left = sorted(set(ch for ch in raw if ord(ch) > 127)); assert not left, f"unmapped non-ascii: {left}"
figs = open(f"{P}/latex/figures_block.tex").read()
pre = open(f"{P}/latex/preamble.tex").read()
open(f"{L}/main.tex", "w").write(pre + "\\begin{document}\\maketitle\n" + figs + raw + "\n\\bibliographystyle{plainnat}\n\\bibliography{../references}\n\\end{document}\n")
print("main.tex written;", len(raw.split()), "words")
if "--no-compile" not in sys.argv:
    def tex(): return subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], cwd=L, capture_output=True, text=True, errors="ignore")
    r = tex(); subprocess.run(["bibtex", "main"], cwd=L, capture_output=True); r = tex(); r = tex()
    log = open(f"{L}/main.log", errors="ignore").read(); print("pdflatex exit", r.returncode, "| undefined citations:", log.count("Citation") and len(re.findall(r"Citation .* undefined", log)), "| overfull:", log.count("Overfull"))
    if r.returncode: print("\n".join(l for l in log.split("\n") if l.startswith("!"))[:800])
    pages = subprocess.run(["pdfinfo", f"{L}/main.pdf"], capture_output=True, text=True).stdout; print([l for l in pages.split("\n") if l.startswith("Pages")])
