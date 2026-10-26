# Paper 4 — Is preference disagreement in the text? Stage 1 feasibility protocol (frozen before any result)
Committed 2026-10-26 (user decision: pursue an ICML paper on pluralistic alignment in parallel with finishing paper 2). Tools reused from paper 2 (paper-2/phase2: fr_lib, decode_residual, rater_item_model); no reward model is trained in stage 1.

## Question
Pluralistic-alignment work trains distributional or group-conditioned reward models on multi-annotator preference data, assuming that disagreement is a property of the (prompt, response pair) that a text model can learn. Stage 1 measures, on public preference data, (a) how reproducible the disagreement is across disjoint raters, (b) how much of the reproducible part a frozen representation of the text can decode, and (c) how much of the rating structure is rater-side (rater offsets/thresholds) rather than item-side.

## Data
- **MultiPref** (allenai/multipref, 10,461 comparisons; 4 raters per comparison: 2 crowd + 2 expert; 227 persistent raters, median 166 ratings each). Primary label `overall_pref` mapped to a 5-level ordinal scale A-clearly < A-slightly < Tie < B-slightly < B-clearly (levels 0–4); secondary: helpful / truthful / harmless prefs. Item text = prompt + completion A + completion B.
- **PRISM** (HannahRoseKirk/prism-alignment; 1,396 users, one rater per (prompt, response) in 99 % of cases): no split-half possible; used only for the rater-side analysis (user offsets on the 1–100 score) and later for personalisation (stage 2).
- Control panels from paper 2 (SummEval, POPQUORN, DICES, ChaosNLI) are re-reported for comparison, not re-run.

## Estimands (MultiPref)
1. Split-half reliability of the shape beyond exact mode+mean, ρ = X/M (paper-2 rho_exact estimator, exact comparator, fixed bootstrap), at a = 3 (one held-out rating, position drawn per item) and with the natural split crowd-pair vs expert-pair (a = 2, |P2| = 2). Also the location reliability (Spearman of P1 mean vs P2 mean).
2. Decodability: decode_residual estimand G and G/X from frozen Qwen2.5-7B-Instruct last-token features of a judge-style prompt ("which response is better, A or B, on a 5-point scale"), a = b = 2, group-cross-fitted by prompt_id; positive control = decoding the P1 mean.
3. Rater-side structure: ordered-probit M0/M1/M2 (paper-2 rater_item_model) with persistent rater ids; ΔLL thresholds vs dispersion; X_obs vs X_sim.
4. PRISM: variance decomposition of the 1–100 score into user and item components (random-effects ANOVA on users with ≥ 10 ratings), and the out-of-sample gain of a per-user offset fitted on 5 / 10 / 20 of the user's ratings for predicting the user's held-out scores.

## Stage-1 decision rule (prespecified)
- If on MultiPref ρ_exact < ½ and G/X ≤ 10 % while rater thresholds dominate (ΔLL M1 − M0 ≥ 3× ΔLL M2 − M1): the paper's thesis is "pluralistic disagreement in preference data is mostly rater-side"; stage 2 builds and tests a factorised reward model (text location × rater offset/thresholds) against distributional and group-conditioned RMs on new-rater prediction and few-shot personalisation.
- If G/X is large (≥ 30 %): disagreement is largely in the text; stage 2 instead studies how well distributional RMs capture it (and our tools become an evaluation contribution).
- Otherwise: mixed; report and decide with the user.

## Amendments
(none)
