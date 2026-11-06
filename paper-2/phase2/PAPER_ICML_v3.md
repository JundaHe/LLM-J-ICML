# Five Raters Are Not a Distribution: What Learned Judges Can Learn from Human Disagreement, and Where to Spend the Annotation Budget

*ICML main-text version v3 (in progress), compressed from PAPER_DRAFT_v2.md v2.5 following COMPRESSION_PLAN.md. PAPER_DRAFT_v2.md remains the full record. Numbers are copied verbatim from v2.5 and none are recomputed.*

## Abstract
Learned judges are increasingly trained on full histograms of human ratings. We ask which part of a few-rater histogram a text-conditioned judge can learn, separating whether the shape beyond its location (mode and mean) is *reproducible across raters* from whether it is *predictable from the text*.

On rating panels from 14 datasets, a learner-free split-half analysis finds the ordinal shape poorly reproducible. Its forecasting reliability is 0.04–0.41 with 4–8 raters and below 0.3 at 40, under the ½ needed for the raw histogram to beat its own mode and mean; on NLI it reaches 0.96–0.98.

Scored against the other half's own shape, no ordinal panel shows a robustly reproducible shape beyond location. On DICES-350, the one panel where it is detectable within the rater pool, frozen representations of three LLM families recover −1 to 1 % of it (upper bounds ≤ 12 %). A planted text-predictable shape of the same magnitude is recovered at 15–33 %. On MNLI and SNLI they recover 28–38 %.

Accordingly, replacing the shape of 69–83 % of training targets while preserving mode and mean changes LoRA judges by at most ±0.0015 RPS. One-hot targets are worse on 10 of 11 panels.

For the annotation budget, frozen-feature judges gain more from additional items than from additional raters on most panels. In a prospective LoRA block on POPQUORN, one rating per item costs 0.006 RPS against the full data, and a second rating recovers about half of that loss.

We release disagreement reliability cards and the estimators.

## 1. Introduction

Human raters disagree. A growing line of work therefore trains learned judges, meaning language models fine-tuned to score text, on the full distribution of human ratings rather than on a single aggregated label (Chen et al., 2025; Singh et al., 2025; Kohli, 2026; Benito-Santos & Ghajari, 2025). The appeal is that a histogram records which neighbouring levels received mass and how concentrated the ratings were. A judge that reproduces it would "capture human disagreement" rather than average it away.

The data behind that appeal are thin. In most datasets the histogram is computed from three to nine people. Five ratings of a code snippet's readability are a sample from a population of possible raters. A model trained to reproduce that sample exactly is therefore partly trained to reproduce sampling noise.

We ask a question that work on learning from label variation (Uma et al., 2021; Plank, 2022) has not asked in this form: **which part of a few-rater histogram can a text-conditioned judge learn?** We split every histogram into its *location*, meaning its mode and mean, and its *shape beyond location*, meaning the residual allocation of mass once mode and mean are fixed. We then measure two properties of the shape that are usually conflated.

1. **Reproducibility across raters (§3).** If a disjoint panel rated the same items, would the shape come out the same? We estimate this without a learner, using a split-half design. An exact identity, A1 = M − 2X, links three quantities:
   - A1, the value of the raw histogram for forecasting a new rater;
   - M, the magnitude of the histogram's residual relative to an exact mode-and-mean comparator;
   - X, the agreement of that residual across the two panels.

   The ratio ρ = X/M is a split-half reliability of the shape at a given number of raters. The raw histogram beats the comparator for predicting a new rater exactly when ρ > ½.
2. **Predictability from the text (§4).** Even a reproducible shape is useless to a judge unless the text carries it. We fit a cross-fitted ridge decoder from a frozen LLM's representation to the residual of panel 1. We score it against panel 2's residual measured from *its own* mode and mean, using a proper-score gain $G_{\rm own}$. We also report the gain as the fraction $G_{\rm own}/X_{\rm own}$ of the reproducible own-shape, with item-cluster CLT intervals. Each estimate is checked against a within-cell feature-permutation control and against planted positive controls.

**Findings.**

*(i) The shape beyond mode and mean is poorly reproducible on ordinal scales (§3).*
- With 4–8 raters per item, its split-half reliability is 0.04–0.41, and the intervals include 0 on four of eight panels. With three raters it cannot be measured at all, because a split leaves two ratings per item, which are fixed by their own mode and mean.
- On the dense ordinal panels it stays below 0.3 up to 40 raters, so on no ordinal panel does the raw histogram forecast a new rater better than its own mode and mean. On ChaosNLI, by contrast, the forecasting reliability exceeds ½ from two to three raters.
- The reproducibility of the shape itself at 40 raters is 0.06–0.22 on the dense ordinal panels and 0.61 / 0.67 on MNLI / SNLI.

*(ii) Little of the ordinal own-shape is decodable from the text, even where it exists (§4).* Across panels, the ordinal own-shape is:
- undetectable on SummEval's non-duplicated items, POPQUORN and DICES-990;
- on Dorn's readability panel, of the size that location and rater thresholds alone produce;
- detectable only on DICES-350, and only within its observed rater pool.

DICES-350 at 40 raters is therefore the clean ordinal case. There, frozen features of three model families recover −1 to 1 % of the own-shape (upper bounds ≤ 12 %). A planted text-predictable shape of the observed magnitude is detected in 5 of 5 draws and recovered at 15–33 %, and a location-and-threshold simulation of the panel yields no own-shape at all. On MNLI and SNLI the decoder recovers 28 % [24, 33] and 38 % [33, 42]. Every NLI lower bound exceeds every ordinal upper bound.

*(iii) The judges we trained show no detectable use of the shape (§5).*
- Replacing the shape of 69–83 % of LoRA training targets while preserving each target's exact mode and mean changes held-out RPS by −0.0001 [−0.0011, +0.0011] on SummEval and +0.0000 [−0.0009, +0.0009] on POPQUORN. This null is expected, since neither panel has a detectable own-shape.
- The discriminating case is ChaosNLI, where the same intervention costs 0.005–0.017 Brier.
- Across eleven ordinal panels, one-hot targets are worse on 10 of 11.
- Beyond item location, the remaining structure is mostly rater-side. Rater-specific cut-points improve held-out likelihood by 0.05–0.16 nats per rating, while item-specific dispersion adds −0.017 to +0.012.

*(iv) Budget (§6).*
- At a fixed number of ratings, frozen-feature heads improve with more items rather than more raters per item on four of the five ordinal panels with more than 900 items, and on both ChaosNLI panels.
- In a prospective LoRA block on POPQUORN with independent rating assignments, one rating per item is worse than the full data by +0.0063 [+0.0030, +0.0099] RPS, and a second rating recovers about half of that gap.
- On SummEval, the crowd ratings are nearly uncorrelated with the held-out experts, and half the items carry five identical crowd annotations. The same contrasts there measure how far expert ratings are diluted, and we report them in Appendix C rather than as budget evidence.
- A prediction we registered was falsified on ChaosNLI: that multi-rater items would pay off at a fixed budget wherever the shape is text-predictable. We therefore report the task-dependence of the marginal value of extra ratings as an observation, not as a consequence of the mechanism.

**Contributions.**
1. Two reliabilities for disagreement, across raters and across text, with learner-free and cross-fitted estimators and calibrated positive controls.
2. Disagreement reliability cards for every panel. They tell a dataset builder whether the shape of disagreement is reproducible at the number of raters they can afford.
3. A donor-replacement audit showing that current training does not use the shape, together with a rater–item decomposition of the ordinal structure beyond location.
4. Fixed-budget evidence for frozen-feature heads in three model families, and for end-to-end LoRA judges on POPQUORN.

**What we do not claim.**
- That disagreement is noise: part of it is reproducible.
- That the text contains no residual information: we test linear decodability from three frozen model families only.
- A theoretical rater-count threshold: a two-term 1/a model was falsified.
- A causal role for rater thresholds or label structure in the ordinal–nominal difference.
- A universal budget rule: Zhang, Gong & Choi (2021) find the opposite when a large single-label base already exists (§2).
