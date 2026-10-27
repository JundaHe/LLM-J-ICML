# Paper 4 — stage 2a result on MultiPref (overall_pref), 2026-10-27
Primary run = PROTOCOL_STAGE2.md with Amendments 1–4 (results/stage2a_multipref_overall.{json,md}); the pre-Amendment-4 run (low-rank baselines without a constant column) is kept in results/stage2a_multipref_overall_A3.*. New raters (never in training), adapted from k of their ratings on training items, evaluated on held-out prompt groups; 5 folds, 5 draws per k, rater-cluster bootstrap (B = 2,000).

## Held-out log-likelihood per rating, differences vs the rater-agnostic distributional RM D
| k | DF − D (H1) | DFs − D (H6) | DL − D | DF − DL (H3) | DF − DG (H2) | F_scale − F_shift (H4, probit) |
|---|---|---|---|---|---|---|
| 5 | +0.028 [+0.012, +0.044] | +0.048 [+0.029, +0.070] | −0.308 [−0.377, −0.242] | +0.336 | +0.028 | +0.012 [−0.001, +0.029] |
| 10 | +0.054 [+0.033, +0.078] | +0.079 [+0.054, +0.106] | −0.042 [−0.083, −0.005] | +0.096 | +0.055 | +0.029 [+0.014, +0.048] |
| 20 | +0.080 [+0.055, +0.106] | **+0.100 [+0.074, +0.128]** | +0.059 [+0.031, +0.089] | +0.021 [+0.011, +0.033] | +0.081 [+0.056, +0.106] | +0.036 [+0.020, +0.057] |
| 50 | +0.114 [+0.087, +0.142] | +0.128 [+0.101, +0.156] | +0.116 [+0.088, +0.143] | −0.001 [−0.007, +0.005] | +0.115 | +0.051 [+0.032, +0.074] |

Preference-direction accuracy (D 0.674): DF −0.014 [−0.020, −0.007] at k = 20 (worse at every k ≥ 5); **DFs +0.005 [+0.001, +0.008]** (better at every k); DL −0.011 at k = 20. RPS at k = 20: D 0.1593, DF 0.1551, **DFs 0.1532**, DL 0.1555.

## Reading against the registered hypotheses (k = 20)
- H1 (DF > D): holds. H2 (DF > DG, individual > group): holds; DG ≈ D (crowd/expert offsets add nothing for new raters).
- H3 (DF − DL ≥ −0.005): holds and DF beats DL at k ≤ 20; the two converge at k = 50. DL over-fits badly at k ≤ 10 under the training-rater prior → sensitivity with k-shot-tuned priors (Amendment 5) running.
- H4 (rater scale > rater shift, probit family): holds from k = 10.
- H6 (symmetric style model DFs: LL gain without loss in direction accuracy): holds. DFs is the best model at every k ≥ 5 in LL and RPS and the only one that also improves direction accuracy; DF − DFs < 0 at every k ≥ 5, i.e. the A-vs-B position term of DF is mostly fitted noise from few ratings.

## What this says (descriptive)
For a new rater, three numbers describing **how they use the scale** — how often they say "clearly", how often "slightly", how often "tie" — learned from 5–20 of their ratings and independent of the text, improve held-out likelihood over a distributional reward model by 0.05–0.10 nats per rating and slightly improve predicting which response they prefer; modelling *which side* they lean to, groups (crowd vs expert), or a text-interacting 8-dimensional latent does not help more at few shots. Not yet tested: end-to-end reward model (stage 2b), a second dataset, robustness to the adaptation prior (Amendment 5).
