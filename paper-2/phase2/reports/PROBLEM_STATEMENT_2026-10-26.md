# Problem statement for the ICML version (2026-10-26)

Written after the user asked for the limitation of the problem and of existing methods to be stated clearly. All experiments and the §1 of the paper are to be checked against this document. Scope decision (user, 2026-10-26): the paper stays in the NLP / LLM-judge setting (no vision benchmarks); software-engineering panels (Buse–Weimer, Scalabrino code readability) remain as one application domain among others, not as the framing.

## The task
Train a judge (an LLM fine-tuned to score text, or a head on frozen features) to predict the **distribution** of human ratings for an item, not a single label. Supervision: for each item, the ratings of m annotators — m = 3–9 in most datasets (SummEval 8, POPQUORN 5–8, HelpSteer2 5, EmoBank 5, CSC 6, Scalabrino 9), m = 60–121 in a few (DICES, Buse–Weimer, ChaosNLI 100). Existing methods (Chen et al. NeurIPS 2025; Singh et al. 2025; Kohli 2026; Benito-Santos & Ghajari 2025; the LeWiDi line) use the **empirical histogram h of the m ratings as the target** and fit it with KL / CE.

## Limitation of existing methods: a finite-sample histogram is treated as the population distribution
h is an m-sample estimate of the latent rating distribution p. With m ≈ 5, the part of h beyond its location (mode, mean) is dominated by multinomial sampling noise. Existing methods have no mechanism for this:
1. the target is h whether m is 5 or 100;
2. no quantity tells the practitioner how much of a dataset's histogram shape is reproducible across annotators;
3. evaluation is against the same kind of pooled histogram (KL to h), so **fitting noise and learning the population distribution are indistinguishable in the reported metrics**.

Evidence already in hand (RESULTS_TABLES.md):
- T9: on the eight ordinal panels with 5–9 raters, the residual of the raw histogram beyond exact mode and mean agrees with an independent panel's residual at ρ = X/M = **0.06–0.58 < ½**; consequently the raw histogram predicts a new rater **worse** than the exact mode-and-mean comparator (A1x = +0.0004 … +0.0052 RPS). On 60–121-rater panels A1x ≈ 0; only on ChaosNLI (100 raters, nominal) the raw histogram wins (≈ −0.02 Brier).
- T2b / T3b / T3c: replacing the shape of 70–80 % of training targets while preserving mode and mean leaves judges unchanged (LoRA −0.0001 [−0.0011, +0.0011] and +0.0000 [−0.0009, +0.0009]); the gain of distributional over point-label training reported in the literature is reproduced by location-matched targets. **The claimed "learning of human disagreement" is, in the audited settings, learning of location and calibration.**
- T9 A2 > 0 on SummEval coherence/relevance, HelpSteer2 and EmoBank: annotation-side residual signal beyond mode and mean **exists**, but the corresponding learned-judge contrasts are ≈ 0. Existing methods absorb the noise and do not demonstrably transmit the signal.

## Why the available alternatives do not solve it
| alternative | problem |
|---|---|
| hard / majority label | discards the whole distribution; worse than soft by +0.004 … +0.011 RPS in our heads (T2b) |
| label smoothing | shrinks toward uniform, independent of item or dataset reliability; does not preserve location |
| Dirichlet / James–Stein shrinkage (Hausser & Strimmer 2009) | shrinks toward a prior with a tuned concentration; shrinks location (reliable) and shape (unreliable) together |
| Dawid–Skene-type annotator models | assume a latent true label; the premise fails for subjective tasks (offensiveness, politeness, readability) |
| per-annotator / perspectivist models | need persistent annotator identities (most datasets lack them) and mostly memorise annotators |
| collect more raters (Kohli 2026; Gheibi & Ghazizadeh 2026 observe the sparse-label problem) | say that few raters are insufficient; give neither a decision rule for how many nor a fix when few are available |

Common gap: **no method uses the cross-annotator reproducibility of the residual shape to decide how much of the histogram to trust while keeping the reliable location statistics fixed.**

## What the paper solves (one sentence)
> Distributional supervision targets are estimated from a handful of annotators; existing methods neither know how much of the target is noise nor can keep only the reliable part. We give a data-estimable reliability ρ = X/M (from the exact identity A1 = M − 2X) that (a) diagnoses, without training a model, whether a dataset's histogram shape is worth learning and at roughly what annotation count, (b) yields a statistic-preserving, reliability-shrunk target q_T + λ*(h − q_T) with λ* = X/M that is never worse in expected proper score than either the raw histogram or the location-only target, and (c) turns into a fixed-budget rule for spending annotations on more items vs. more raters.

Three contributions in that order: **diagnosis** (learner-free), **method** (target + finite-sample guarantee), **decision** (annotation budget). The donor-replacement audit becomes motivation: it shows that current training does not use the shape.

## Our own limitations (what reviewers will attack; what the plan must answer)
1. The diagnosis exists; the method is not yet validated — Gates A (annotation side) and H (heads) in SHRINKAGE_PROTOCOL.md.
2. Learned judges are already insensitive to the shape, so learner-side gains may be small; report them honestly next to the mode-only penalty (+0.012 / +0.003 RPS) rather than as a headline.
3. One 2024 base family (Qwen2.5-7B) and small absolute effects — base-model refresh and a second family are in step 3 of the plan (GPU, pending approval).
4. ICML fit: the problem must be presented as a general learning-from-crowds problem with LLM judges as the setting; no vision benchmarks (user decision).

## Forbidden framings (inherit HANDOFF §3)
No equivalence claims; no "text lacks the information"; no theoretical break-even rater count; no causal ordinal–nominal explanation; no "first within-class shuffle"; no polarisation wording; no commit-message panels.
