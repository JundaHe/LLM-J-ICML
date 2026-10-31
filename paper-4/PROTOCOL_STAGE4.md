# Paper 4 — Stage 4: how much room is there for content personalisation? Aspect trade-offs as observable content preferences (frozen before any result)
Committed 2026-10-31, after the third ICML-style review (4/10; W1: no estimate of the size of real content heterogeneity) and the user's request to increase novelty. Every MultiPref annotation also carries the annotator's own helpfulness, truthfulness and harmlessness preferences (5 levels each). Descriptives seen before this protocol (no hypothesis quantity): all 41,844 annotations have the three aspects; aspects point in opposite directions in 3.5 % of annotations; when helpfulness and harmlessness conflict and the overall label is not a tie (912 annotations), the overall label sides with helpfulness in 22 %; among the 20 raters with ≥ 10 such conflicts, that share ranges from 0.00 to 0.94 (sd 0.22). Any change after the first result is logged under "Amendments".

## S4-A: a data-grounded ceiling on trade-off personalisation (learner-free with respect to text)
**Question.** If we knew, for every new-rater rating, that rater's own three aspect judgements, how much better could a rater-specific way of combining them into the overall preference predict the overall preference than the population's way of combining them? This bounds the ranking gain available to any personalised reward model whose content dependence acts through these aspects, given perfect knowledge of the aspects.

**Model.** Ordinal logistic for the overall level y ∈ {0, …, 4}: latent s = βᵀh, h = the annotator's three aspect levels centred at 0 (−2 … 2), plus each aspect's absolute value (3 more columns; lets "tie on harmlessness" differ from a strong harmlessness preference), cut-points c. Two variants, both with **rater-specific cut-points** (scale use, so that the contrast isolates the trade-off):
- **P (pooled trade-off):** β shared, c_r per rater (shrunk to the pooled c);
- **R (rater trade-off):** β_r = β + δ_r per rater (ridge on δ_r, λ chosen once on the training raters by splitting their training items in half), c_r as in P.

**Splits.** The stage-2a folds (5 rater folds × 5 prompt-group folds). Population parameters (β, c, penalties) on training raters × training items. For each test rater, the rater parameters (c_r for P; c_r and δ_r for R) are fitted on k of that rater's training-item annotations (k ∈ {20, 50}, the stage-2a draws; and k = all) and evaluated on the rater's test-item annotations, using the rater's own aspect labels on those items as inputs (oracle access to the aspects).

**Outcomes.** R − P at each k: direction accuracy on held-out items (ties excluded), log-likelihood per rating; also on the subset of held-out annotations whose three aspects do not all point the same way ("conflict items") and the share of such items. Rater bootstrap B = 2,000; also an in-sample version (δ_r fitted on the rater's test items) as an absolute upper bound.

**Decision rule (fixed now).** S4-B (an aspect-weight personalised reward model from text) is run only if the k = all ceiling R − P in direction accuracy has a lower 95 % bound above +0.5 points. Otherwise the paper reports the ceiling as the explanation of the ranking null (the room for trade-off personalisation is too small) and S4-B is not run.

## S4-B (conditional; specified now, run only if the S4-A rule passes)
**Aspect-weight personalised reward model (AW).** Text → three aspect heads (5-level distributions of the training raters' aspect labels per item; full-feature per-response embeddings; ridge, penalties on validation) → expected aspect scores μ_a(x) and their absolute values; overall model: ordinal logistic with s = β_rᵀ[μ(x), |μ(x)|] + rater style offsets; new rater's β_r and offsets fitted on k overall ratings (no aspect labels of the new rater at adaptation or test). Compared with DFs, DL, VPL, PAL-B (full features) under the permutation control: own − other direction accuracy and LL at k ∈ {20, 50}, on all items and on predicted-conflict items. Success criterion: AW's own − other direction gain at k = 50 with lower bound > 0 **and** AW's LL not below DFs by more than 0.005.

## Forbidden statements
"Raters do not differ in their values"; anything about datasets other than MultiPref from Stage 4.

## Amendments

**Amendment 1 (2026-10-31 05:00, AFTER the first S4-A result, which is kept as results/stage4_s4a_grid0.*).** The cut-point penalty λ_c was selected at the lower edge of its grid (0.3) in every fold. Following the grid-edge rule used throughout, the grid is extended downward to {0.01, 0.03, 0.1, 0.3, 1, 3, 10} and S4-A is re-run; nothing else changes. The decision rule is applied to the re-run; both runs are reported.
