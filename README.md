# LLM-J-ICML

Paper 2 of the LLM-as-a-Judge project — target venue ICML.
Working title: *Beyond Mode and Mean? What Disagreement Histograms Teach LLM Judges* (audit of distributional supervision for learned judges: statistic-preserving donor replacement with dose certificates, LoRA/heads experiments on 10 ordinal + ChaosNLI panels, and a learner-free finite-rater analysis).

Start here:
- `paper-2/phase2/SETUP_NEW_SERVER.md` — clone, data submodules, feature restore, environments, commands
- `paper-2/phase2/PAPER_DRAFT.md` → `paper-2/phase2/latex/main.pdf` — manuscript
- `paper-2/phase2/RESULTS_TABLES.md` — every result table (T2b heads, T3b/T3c LoRA, T5 ChaosNLI, T9 finite-rater)
- `paper-2/phase2/PROGRESS.md` — chronological log of decisions; `paper-2/phase2/reviews/` — external (Codex) review rounds
- `paper-2/REPORT.md`, `paper-2/lit-review/`, `paper-2/idea-stage/` — phase-1 report, literature review, idea discovery

Layout note: `code/code_readability/data` (Buse–Weimer, Scalabrino readability ratings) is shared data the panels load; paths are resolved by `paper-2/phase2/paths.py` relative to this repository root (override with `LLMJ_ROOT`).
Split off from the private working repository `JundaHe/ICSE2027-LLM-Judge` (branch `idea-discovery-2026-08-23`, commit 070876a) on 2026-10-25; history before that point lives there.
