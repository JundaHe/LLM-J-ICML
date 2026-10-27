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

## Amendment 5 sensitivity (adaptation prior tuned per model and k by k-shot validation on held-out training raters; results/stage2a_multipref_overall_A5.*)
| k | DF − D | DFs − D | DL − D | DF − DL (H3) | DFs − DL (post hoc) | dir: DFs − D | dir: DFs − DL |
|---|---|---|---|---|---|---|---|
| 5 | +0.035 [+0.026, +0.043] | +0.049 [+0.032, +0.067] | +0.023 [−0.002, +0.047] | +0.012 [−0.007, +0.031] | +0.026 [+0.016, +0.037] | +0.003 [+0.000, +0.006] | −0.001 [−0.005, +0.002] |
| 10 | +0.058 | +0.077 | +0.068 | −0.009 [−0.024, +0.004] | +0.010 [+0.003, +0.017] | +0.003 | −0.000 |
| 20 | +0.080 | **+0.100 [+0.074, +0.128]** | +0.095 [+0.069, +0.122] | **−0.015 [−0.021, −0.009]** | +0.0045 [−0.0004, +0.0092] | +0.005 [+0.001, +0.008] | −0.000 [−0.004, +0.003] |
| 50 | +0.114 | +0.128 | +0.120 | −0.006 [−0.012, −0.000] | +0.007 [+0.002, +0.013] | +0.004 | +0.010 [+0.004, +0.015] |

Selected adaptation priors: DF/DFs λ_ad ∈ {0.5, 2} (close to the training choice); DL λ_ad = 8192 (grid top) at k ≤ 20 in most folds — with the unpenalised constant column w₀ the scale of z is not identified, so a large λ on z does not pin the effective rater offsets to zero.

**Reading against the prespecified robustness criterion (k = 20):**
- **H3 is NOT robust.** With a few-shot-tuned prior the low-rank latent model DL catches up and beats the 5-parameter DF (−0.015 [−0.021, −0.009]); the primary-run advantage of DF over DL came from DL's under-regularised few-shot adaptation.
- **H6 is robust.** DFs − D is unchanged (+0.100 nats/rating; direction accuracy +0.005 [+0.001, +0.008]).
- Post hoc (not registered; flagged as such): the 3-parameter symmetric style model DFs is **at least as good as the tuned 8-dimensional text-interacting latent DL at every k** — better at k = 5, 10 and 50, tied at k = 20 (+0.0045 [−0.0004, +0.0092]) — with equal direction accuracy at k ≤ 20. DF's deficit relative to DL is its A-vs-B position term.

**Revised one-line claim:** for new raters, three text-independent numbers describing how a rater uses a two-sided preference scale (extreme / slight / tie) capture essentially all the few-shot personalisation gain that an 8-dimensional text-interacting rater latent achieves, and more of it at very few shots; position (A/B) propensities and demographic/crowd-vs-expert groups add nothing or hurt.

## Replication 1: DICES-350 (Amendment 6; conversational safety, 3 levels; 104 raters × 350 conversations; DG/G = rater race, 5 groups)
results/stage2a_dices.{json,md} (training-rater prior) and stage2a_dices_A5.* (k-shot-tuned prior). Held-out LL per rating of new raters, k = 20:
| | primary | Amendment-5 prior |
|---|---|---|
| H1r DF − D | **+0.089 [+0.064, +0.117]** | +0.089 [+0.064, +0.117] |
| H2r DF − DG (race) | **+0.095 [+0.069, +0.122]** | +0.095 |
| H3r DF − DL | **+0.028 [+0.017, +0.040]** | **+0.037 [+0.022, +0.053]** |
| DL − D | +0.061 [+0.031, +0.093] | +0.052 [+0.015, +0.086] |
| F_scale − F_shift (H4) | **−0.053 [−0.070, −0.036]** | same |
| direction accuracy (safe vs unsafe), DF − D | +0.048 [+0.025, +0.076] (0.649 → 0.697) | same |

- H1r, H2r, H3r hold, and H3r is robust to the tuned prior here (unlike MultiPref, where tuned DL caught up with DF). The race-group model DG is slightly *worse* than the text-only D for new raters (−0.006).
- **H4 reverses on DICES**: rater *shift* (how strict a rater is about "unsafe") matters more than rater *scale*, the opposite of MultiPref (where expressiveness — clearly vs slightly — dominated). "Response style" is task-specific: strictness for safety ratings, intensity for two-sided preferences; the text-independent offset model DF captures both.
- Personalising also improves *which side* a new rater falls on by 4.8 points (unlike MultiPref, where only the symmetric model helped direction), consistent with strictness being a threshold shift.
- The secondary probit group model G was mis-specified (common-scale escape, Amendment 7); its DICES numbers are superseded by the rerun (stage2a_dices_A7_*). No primary-family number is affected.

## Replication 2: PRISM (Amendment 6; 1–100 response ratings binned to 5 levels; 1,013 new users evaluated; DG/G = user's special_region, 9 groups)
results/stage2a_prism.{json,md} (primary) and stage2a_prism_A5.* (k-shot-tuned prior). k = 20:
| | primary | Amendment-5 prior |
|---|---|---|
| H1r DF − D | **+0.080 [+0.071, +0.090]** | +0.079 [+0.068, +0.089] |
| H2r DF − DG (region) | **+0.078 [+0.068, +0.087]** | +0.076 |
| H3r DF − DL | +0.049 [+0.038, +0.060] | **−0.001 [−0.006, +0.003]** (tie; misses the −0.005 non-inferiority bound by 0.001) |
| F_scale − F_shift (H4) | −0.031 [−0.042, −0.020] | same |
| direction accuracy DF − D | +0.005 [+0.001, +0.009] | +0.003 [−0.001, +0.008] |
- H1r, H2r hold; region groups add +0.003 over text-only. H3r holds under the training-rater prior; under the tuned prior DF and DL are tied (formally not robust: lower bound −0.006 vs −0.005).
- H4 reverses as on DICES: on single-response rating scales the rater *shift* (lenient vs harsh) dominates; scale > shift is specific to the two-sided preference scale of MultiPref.
- Note: at k = 50 the tuned prior is unreliable (only 139 users have ≥ 50 adaptation ratings, so the inner k-shot validation set is tiny; DF under the tuned prior is worse than under the training prior there).

DICES G after the Amendment-7 fix (stage2a_dices_A7.*): −0.854 nats at every k (≈ T0 −0.842); no other DICES number changed.

## Cross-dataset summary (k = 20, LL per rating vs the text-only distributional RM D)
| dataset | rater-offset model DF | group model DG | tuned low-rank DL | DF − DL (tuned) |
|---|---|---|---|---|
| MultiPref (pairwise preference) | +0.080 (DFs +0.100) | ≈ 0 (crowd/expert) | +0.095 | −0.015 (DFs − DL +0.005, tie) |
| DICES-350 (safety) | +0.089 | −0.006 (race) | +0.052 | +0.037 |
| PRISM (response ratings) | +0.079 | +0.003 (region) | +0.080 | −0.001 (tie) |
Text-independent rater offsets learned from 20 ratings give +0.08–0.10 nats per rating on all three datasets; demographic or crowd/expert groups give ≈ 0; a tuned 8-dimensional text-interacting latent is at best equal. What the offsets encode is task-specific (strictness on ratings, intensity on two-sided preferences).

## Stage 2b-1: rater models on a fine-tuned LoRA reward model (PROTOCOL_STAGE2B.md; 5 folds; results/stage2a_multipref_overall_lora.*)
D-LoRA = Qwen2.5-7B-Instruct + LoRA trained per fold on the training raters' rating distributions of the training items; its 5 score-token log-probs are the frozen text head (lg = a·ℓ + b + rater terms). New raters, k = 20, LL per rating (paired rater-cluster bootstrap against the frozen-feature run on the same raters and draws):
| | value |
|---|---|
| **B1** DFs(D-LoRA) − D-LoRA | **+0.100 [+0.071, +0.130]** (frozen head: +0.100) |
| DF(D-LoRA) − D-LoRA | +0.081 [+0.056, +0.109] |
| **B2** D-LoRA − D(frozen) | **+0.027 [+0.016, +0.039]**; direction accuracy +0.014 [+0.003, +0.024] (0.674 → 0.688) |
| DFs(D-LoRA) − DFs(frozen) | +0.027 [+0.017, +0.038] — the text and rater gains add |
| DFs(frozen, 20 ratings) − D-LoRA | +0.072 [+0.041, +0.106] — three numbers per rater gain more than fine-tuning the text model |
| DFs direction accuracy − D-LoRA | +0.002 [−0.002, +0.006] (requirement: lower bound ≥ −0.005: met) |
| DL(D-LoRA) − D-LoRA | −0.301 at k = 5, +0.057 at k = 20 (training-rater prior; under-regularised as in stage 2a) |
B1 and B2 hold. The style gain is not absorbed by a stronger text model; it is additive to it. B3 (in-context personalisation, RC-LoRA, folds 0–1) is running.
