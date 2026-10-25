# Codex consult — can paper 2's novelty be raised? (2026-10-23)

You are a senior ML reviewer (NeurIPS/ICML/ICLR area chair level). Be blunt. Read these files first (absolute paths, read-only):
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/PAPER_DRAFT.md  (current manuscript text)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/RESULTS_TABLES.md (all numbers)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/novelty/NOVELTY_REPORT.md (earlier novelty check: 6.5/10, "proceed with caution"; closest prior work Gheibi & Ghazizadeh 2026 shuffled-SLS control; Behrens & Zdeborová ICLR 2026 within-class soft-label reshuffle; Kohli 2026 soft labels on ChaosNLI; Singh et al. 2025; Chen et al. 2025 distributional judge training)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/reviews/codex_round15_2026-10-13.md (your last verdict)

## Current state
Contribution today = a dose-certified, statistic-preserving donor-replacement AUDIT of distributional supervision for learned judges, plus the finding that on ordinal panels mode+mean-preserving replacement changes RPS by ~0 (heads: −.0024..+.0006 on 10 panels; SummEval LoRA −.0001 [−.0011, +.0011]) while mode-only replacement hurts (SummEval +.0120), and on nominal ChaosNLI residual scrambling hurts (KL +.016..+.052). A second end-to-end LoRA dataset (POPQUORN offensiveness, 27 runs) is running now; seed-2000 interim perm−chen ≈ −.0002, perm_mode−chen f0 +.0037.
Weaknesses we know: core result is a null (reviewers will say "underpowered" or "your learner just can't use the shape"); novelty is medium (decomposition audit of a known control family); positive control valid only on Buse–Weimer.

## The question
The user asks: can we materially INCREASE the novelty / significance of this paper? Constraints: 1 GPU (A6000-class, 46 GB) for ~days, CPU plenty, existing frozen features (Qwen2.5-7B) for all panels, ChaosNLI has ~100 annotations/item, POPQUORN/DICES/EmoBank/CSC/SummEval/HelpSteer2/readability panels available; no paid API budget assumed. Timeline: weeks, not months.

## Candidate directions (mine — critique, rank, kill, or improve them; add your own)
A. **Data-side ceiling vs learner-side recovery ("is the information there?")**. With no learning at all, score a held-out rater against (i) the other raters' empirical histogram, (ii) its mode+mean projection (pmmx of itself), (iii) donor-replaced targets — i.e. the *oracle* value of residual shape for predicting a new rater. Then the learned-judge contrast can be read as a fraction of the oracle gap. If the oracle gap is ~0 on ordinal panels with m=3–8 raters, the null is a data property (residual shape is mostly sampling noise at small m), not learner weakness; on ChaosNLI (m≈100 subsampled) we can trace the oracle gap vs m. This would turn the null into an identification statement: "learner recovers X% of what is recoverable".
B. **Signal-to-noise theory of residual shape vs number of annotators m.** Under a multinomial sampling model per item, derive the expected predictive value of the residual (beyond mode/mean) for a new rater as a function of m and of the between-item variance of the true residual; estimate it per panel; give a predicted "break-even m". Validate on ChaosNLI by subsampling m and on the heads.
C. **Statistic ladder.** Generalise preserve-{mode} / {mode,mean} to {mode,mean,variance} and {mode,mean,variance,skew} via the same exact KL projection, giving a "how many moments does a judge use" profile per panel (where does the contrast saturate?).
D. **Annotation-budget consequence.** If mode+mean suffice on ordinal tasks, then for a fixed rating budget, more items × fewer raters should beat fewer items × more raters for judge training. Simulate by subsampling raters/items on panels with enough raters (ChaosNLI, DICES m=60, EmoBank) → a practical design rule.
E. **Extend the audit to frontier/zero-shot judges.** Elicit verbalised or token-probability distributions from an open LLM (no training) and test whether their residual shape tracks human residual shape beyond mode/mean (zero-shot "do LLM judges model disagreement?").
F. **Minimum-detectable-effect / power.** Inject residual-shape signal of controlled strength on high-dose panels and report the MDE of the audit per panel, so every null becomes "effect < δ with power 0.8".

## What I want back (≤ 1,200 words)
1. For each of A–F (and any of yours): novelty gain (low/med/high) relative to the cited prior work, how a top-venue reviewer would see it, cost on our resources, risk that it is already done (name papers if you know any), and whether it changes the paper's *headline claim*.
2. Your single best plan (which 1–2 directions, in what order) to move the novelty score from ~6.5 to ≥ 7.5, and the reframed one-sentence contribution/title that plan would support.
3. What to explicitly NOT do (scope traps).
4. A quick sanity check: is anything in A or B mathematically trivial or wrong (e.g. is the oracle gap for a held-out rater guaranteed ≈ 0 by construction under pmmx, and if so how should the oracle be defined so it is informative)?
