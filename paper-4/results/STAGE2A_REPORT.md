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

## Stage 2b-2: in-context personalisation baseline RC-LoRA (folds 0–1; results/stage2b_B3.{json,md})
RC-LoRA = Qwen2.5-7B-Instruct + LoRA trained on prompts that contain 10 of the same rater's other ratings; at test, the prompt holds the new rater's k adaptation ratings (same draws as the rater models, draw 0). Paired with the rater models on top of D-LoRA (same base model), same raters:
| k | DFs(D-LoRA) − RC-LoRA, LL/rating | direction accuracy | raters |
|---|---|---|---|
| 5 | **+0.041 [+0.016, +0.065]** | +0.027 [+0.009, +0.046] | 90 |
| 20 | **+0.042 [+0.020, +0.065]** | +0.029 [+0.012, +0.047] | 86 |
**B3 holds, and "better" (lower bound > 0).** RC-LoRA does learn from the history (+0.048 over D-LoRA at k = 20 in LL; fold 0 +0.075, fold 1 +0.021 — one LoRA seed per fold, so fold-to-fold variation is large) but lowers direction accuracy by 3.0 points relative to the non-personalised D-LoRA, whereas the three style offsets learned from the same ratings gain more likelihood without that cost. Cost: RC-LoRA needs 4.4 GPU-hours of training per fold and several thousand prompt tokens of history at every inference; DFs needs three numbers per rater.

## Stage 2c: published personalised RMs (VPL, PAL-B) under the new-rater protocol (PROTOCOL_STAGE2C.md, Amendments 1–2; results/stage2c_summary_A2.md; first run with the collapsed VPL kept in stage2c_summary_A1.md)
Reimplemented from the official repositories as heads on frozen per-response Qwen2.5-7B embeddings; D/DF/DFs refitted on the same features (Dp/DFp/DFsp). New raters, LL per rating, k = 20:
| | E1 graded | E2 binary |
|---|---|---|
| **C1** DFsp − VPL | **+0.092 [+0.068, +0.119]** | −0.010 [−0.016, −0.003] |
| **C1** DFsp − PAL-B (K=2 / 4) | **+0.158 / +0.167** | +0.002 / +0.002 |
| own personalisation gain, model(k=20) − model(k=0): DFsp / VPL / PAL2 / PAL4 | +0.097 / +0.087 / −0.000 / +0.002 | ≈ 0 for all (≤ +0.002) |
| absolute LL: Dp / DFsp / VPL / PAL2 | −1.494 / −1.400 / −1.492 / −1.558 | −0.607 / −0.612 / −0.602 / −0.614 |
| direction (E1) / accuracy (E2): Dp / DFsp / VPL | 0.670 / 0.668 / 0.677 | 0.667 / 0.667 / 0.676 |
- **C1 holds ("better") on graded labels.** With the anti-collapse KL grid (selected KL = 0 or 0.001 in every fold), VPL's latent does carry rater information (+0.087 over its own k = 0), but its k = 0 is poor (−1.578) and its personalised likelihood only reaches the text-only Dp level; PAL-B's user weights give no gain for new raters under a validated adaptation ridge.
- **C2 holds.** On binary labels (ties dropped) no method personalises (own gains ≤ 0.002 nats; DFsp − Dp accuracy −0.0002): the response-style signal lives in the graded levels and ties, which binary preference data discard.
- **C3 fails (prediction R² > 0.5).** Cross-validated R² of VPL's z and PAL's weights on the style offsets is ≈ 0 (−0.09 … +0.04): their user representations do *not* encode response style — they miss the signal that carries most of the new-rater gain.
- Caveat: VPL's per-response reward head predicts *which* response is preferred slightly better than the multinomial head, already at k = 0 (0.677–0.678 vs 0.670), i.e. a text-head architecture effect, not personalisation; a hybrid (VPL text head + style offsets) is untested.

## Stage 2c C4 (Amendment 3): VPL + style offsets (results/stage2c_C4_A3.md)
At k = 20: (VPL+s) − VPL = **+0.088 [+0.066, +0.111]** nats per rating; (VPL+s) − DFsp = −0.004 [−0.014, +0.005] (C4's second part, lower bound ≥ −0.005, formally not met: a tie); direction accuracy (VPL+s) − DFsp = **+0.011 [+0.002, +0.020]** (VPL+s keeps VPL's 0.679). The three offsets are a plug-in for a published personalised RM: added to VPL they recover the whole style gain, and the hybrid combines DFs-level likelihood with VPL-level direction accuracy.

## Reference rows (Amendment 8; results/stage2a_reference_rows.md)
k = 20, LL per rating — MultiPref: uniform −1.609, no-text NT −1.487, text-only D −1.441, DFs −1.342, in-sample oracle DF −1.262 (DFs oracle −1.281). DICES: uniform −1.099, NT −0.766, D −0.840, DF −0.752, oracle −0.702. PRISM: uniform −1.609, NT −1.391, D −1.345, DF −1.264, oracle −1.158. A person's 20 ratings without text recover 73 % of the text model's gain over uniform on MultiPref and beat the text on DICES; DFs closes 55 % of the D-to-oracle gap on MultiPref; the in-sample oracle raises MultiPref direction accuracy only from 0.674 to 0.687.

## Stage 2b Amendment 1: RC-LoRA folds 2–3 added (4 of 5 folds; fold 4 running)
k = 20, 166 raters: DFs(D-LoRA) − RC-LoRA = +0.071 [+0.048, +0.093] LL/rating, direction +0.032; DFs(frozen) − RC-LoRA = +0.046 [+0.024, +0.069]. RC-LoRA − D-LoRA by fold: +0.075, +0.021, +0.061, −0.055 (fold 3 trained badly; one seed per fold); excluding fold 3: DFs(D-LoRA) − RC-LoRA = +0.027 [+0.006, +0.048], direction +0.027 [+0.013, +0.042]. RC-LoRA's direction accuracy is below D-LoRA's in every fold (−1.1 to −4.9 points). B3 holds ("better") with and without fold 3.

## Stage 2b: RC-LoRA on all five folds (fold 4 added; results/stage2b_B3.{json,md})
k = 20, 209 raters: DFs(D-LoRA) − RC-LoRA = **+0.062 [+0.043, +0.081]** LL/rating, direction **+0.032 [+0.019, +0.044]**; DFs(frozen) − RC-LoRA = +0.035 [+0.015, +0.054]. RC-LoRA − D-LoRA = +0.030 [−0.001, +0.061]; by fold +0.075, +0.021, +0.061, −0.055, +0.059 (one seed per fold). Excluding fold 3: DFs(D-LoRA) − RC-LoRA = +0.026 [+0.010, +0.043], direction +0.029 [+0.017, +0.041]; RC-LoRA − D-LoRA = +0.054 [+0.026, +0.083]. RC-LoRA's direction accuracy is below D-LoRA's in every fold (−1.1 to −4.9 points). **B3 holds ("better") on five folds, with and without fold 3.** The fold-3 second seed (Stage 2b Amendment 2) is running.

## Stage 2b Amendments 3–4: B3 final (three RC-LoRA seeds per fold; results/stage2b_B3_final.md)
k = 20, 209 raters. DFs(D-LoRA) − RC-LoRA, LL per rating: seed 2000 +0.062 [+0.043, +0.081], seed 3000 +0.018 [+0.005, +0.032], seed 4000 +0.042 [+0.023, +0.062], three-seed average **+0.041 [+0.027, +0.054]**; direction (average) +1.9 points [+0.9, +2.7]. Pre-specified wording rule: every lower bound > 0 → **"better"**. RC-LoRA − D-LoRA (average) +0.051 [+0.024, +0.079]; RC-LoRA direction − D-LoRA: −3.0 / −0.6 / −1.5 per seed, −1.7 [−2.6, −0.8] on average. RC gains by fold and seed (2000/3000/4000): f0 +0.075/+0.080/−0.078, f1 +0.021/+0.078/+0.085, f2 +0.061/+0.053/+0.048, f3 −0.055/+0.108/+0.125, f4 +0.059/+0.044/+0.059; the two failed runs have the two highest mean training losses (1.552, 1.545; all others ≤ 1.504). DFs on the frozen head vs RC-LoRA: +0.014 [+0.000, +0.028] on average (seed 3000: −0.008, tie).

## Note for the §5.6 LoRA block (2026-10-30)
The LoRA block of the §5.6 table uses adaptation draw 0 only (the draw the in-context model was evaluated on), 209 raters, k = 20: DFs(D-LoRA) − D-LoRA = +0.0917 [+0.0626, +0.1248] (rater bootstrap, B = 2,000, seed 7; computed from stage2a_multipref_overall_lora.json, draw 0) — hence +0.092 there against +0.100 over five draws (B1). RC-LoRA row: three-seed mean, +0.051 [+0.024, +0.079] (stage2b_B3_final.md), direction accuracy 0.671 vs D-LoRA 0.688.
