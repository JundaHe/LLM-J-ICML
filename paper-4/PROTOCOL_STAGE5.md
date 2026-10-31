# Paper 4 — Stage 5: making the positive control informative about the data (frozen before any result)
Committed 2026-10-31, after the fourth ICML-style review (4/10, soundness 3). Objection: the Stage-3 positive control measures how weak the learners are, not how much content heterogeneity the data contain — no well-specified reference learner, one θ/label draw, one injection form, no check that the synthetic panels resemble the real data. Any change after the first result is logged under "Amendments".

## S5-1: a well-specified reference learner (what 20 ratings can reveal at best)
On each synthetic panel (τ0 … τ20), for each test rater, fit θ_r (2-d) by MAP on the rater's k adaptation ratings with the **true injection form**: y ~ softmax(log P̂ + (θ_rᵀg_i)(−2, −1, 0, 1, 2)), g_i the two known features, prior θ_r ~ N(0, σ²I) with σ² estimated by marginal-likelihood-free empirical Bayes on the training raters (σ² chosen from a grid by held-out LL of training raters' half-split adaptation). Two base distributions log P̂: (a) **oracle base** = the generator itself (an upper bound); (b) **estimated base** = D head + DFs offsets fitted on training raters × training items (realistic). Outcome: own − other direction accuracy at k = 20 and 50 (same permutation control, folds, draws, bootstrap as Stage 3). Reported per τ, with the fraction of the generator-oracle gain recovered. The **statistical detection limit** is the smallest τ at which the estimated-base reference learner's own − other lower bound exceeds +1 point at k = 20.

## S5-2: seed variability
Three further synthetic draws (θ seed and label seed 11, 12, 13; same features, same τ calibration procedure, which is re-run per seed) for τ5 and τ10. Learners: reference learner (S5-1), PAL-B on full features, DL (few-shot-tuned). Reported: own − other at k = 20 and 50 for every seed, and mean and range over the four seeds (original + three). The Stage-3 statement "PAL-B on full features detects τ10 at k = 20" is kept only if it holds (lower bound > +1 point) in at least three of the four seeds; otherwise it is weakened.

## S5-3: learner-free comparison of the synthetic panels with the real data
Statistics computed identically on the real panel and every synthetic panel, all raters, all items: (i) agreement in direction between two raters of the same item (non-tie pairs); (ii) Krippendorff's α (ordinal); (iii) the share of an item's rating variance that is between raters within item. Item bootstrap (B = 2,000) on the real data. A synthetic panel is called **inconsistent with the real data, learner-free,** if any of (i)–(iii) lies outside the real data's 95 % interval. Reported; used to qualify which τ the real data could plausibly be.

## S5-4: an aspect-based injection (more realistic structure)
A second injection family in which content preferences act through observable value dimensions: g_i = the item's consensus aspect differences (mean helpfulness, truthfulness and harmlessness level of B over A across the item's annotators, standardised; 3-d), θ_r ~ N(0, τ²I), calibrated as in Stage 3 to generator-oracle gains of +5 and +10 points (one seed). Learners: reference learner (with g_i known), PAL-B (full features), DL. Same outcomes. (The learners do not see the aspect labels; whether text predicts them is part of what is tested.)

## Forbidden statements
Any S5 statement about datasets other than MultiPref; "the real data contain no content heterogeneity".

## Amendments
