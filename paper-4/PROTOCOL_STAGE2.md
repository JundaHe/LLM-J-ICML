# Paper 4 — Stage 2: a factorised reward model for pluralistic preferences (frozen before any result)
Committed 2026-10-27. User decision after the stage-1 "mixed" outcome (results/STAGE1_REPORT.md): direction A, factorised reward model. Any change after the first result is logged under "Amendments" with a reason.

## Motivation (from stage 1, MultiPref overall_pref)
Beyond item location, held-out rating likelihood is gained mostly from rater-side structure (rater thresholds +0.036 nats/rating vs item dispersion +0.0014), and that gain is mostly rater **response style** (rater scale, +0.031) rather than rater **position** (A/B shift, +0.005). About 10 % of the reproducible disagreement shape is linearly decodable from frozen text features (G/X 0.105 [0.057, 0.119]). Pluralistic reward models instead put the heterogeneity either in the text-conditioned output distribution (distributional RMs) or in a high-dimensional user latent (low-rank / variational personalised RMs). Stage 2 tests whether a *structured two-parameter* rater model — text decides where the item sits, the rater decides how they use the scale — predicts **new raters** from **few ratings** at least as well as those alternatives.

## Data
MultiPref (allenai/multipref, 10,461 comparisons × 4 ratings; 227 raters: 89 crowd, 138 expert, disjoint), label overall_pref on 5 ordered levels (A-clearly … B-clearly). Item representation: frozen Qwen2.5-7B-Instruct last-token features of the judge prompt (paper-2/phase2/features/multipref_overall/, the same file as stage 1), reduced by a label-free PCA to 256 components (fitted on features only). Secondary (only if the primary analysis is complete): PRISM (1–100 scores; personalisation analogue) — protocol to be amended before use.

## Models (all share the ordered-probit likelihood P(y ≤ k) = Φ((c_k − μ)/σ) with 4 common cut-points)
- **T0 text-only probit**: μ = β·x, σ = 1. Rater-agnostic.
- **D distributional RM**: rater-agnostic multinomial-logistic head (5 classes) on x — the standard "predict the rating distribution" target of distributional RMs.
- **G group-conditioned**: T0 + group offset and group log-scale (crowd / expert; group known for every rater).
- **F factorised (ours)**: μ = β·x + δ_r, σ = exp(s_r); two parameters per rater with Gaussian priors (ridge penalties λ_δ, λ_s).
- **F-shift / F-scale** (ablations): F with s_r ≡ 0 / δ_r ≡ 0.
- **L low-rank latent** (personalised-RM baseline): μ = β·x + w(x)·z_r with w(x) = Wx, z_r ∈ R^d (d = 8), Gaussian prior on z_r; σ = 1. The rater latent may interact with the text; it contains F-shift as a special case but not F-scale.
- **L+S** (sensitivity): L plus the rater log-scale s_r.

Training: on the training raters' ratings of the training items, all parameters jointly by L-BFGS; penalties (β: {1, 10, 100}; rater parameters: {8, 32, 128}; W: {1, 10, 100}) chosen on a validation split (training raters' ratings of 15 % of the training prompt groups), then refitted on all training cells.

## New-rater evaluation (primary)
5 outer folds. In fold f, raters are split 80 / 20 (stratified by crowd / expert; seed 0) and prompt groups 80 / 20 (grouped by prompt_id; seed 0). Models are trained on (training raters × training items). For each **test rater**, k adaptation ratings are drawn at random from their ratings of **training items** (k ∈ {0, 5, 10, 20, 50}; 5 draws per k, averaged; raters with fewer than k such ratings are excluded at that k and their count reported), the rater parameters (δ_r, s_r; z_r; group parameters for G are known, not adapted) are fitted by MAP with the trained prior and all text-side parameters frozen; evaluation is on the test rater's ratings of **test items**. At k = 0 every rater-level model falls back to the prior mean (F ≡ T0, L ≡ T0).
Metrics: mean held-out log-likelihood per rating (**primary**), RPS, and accuracy of the predicted preference direction (A vs B, ties excluded; the predicted direction is the sign of E[y] − 2).
Inference: rater-cluster bootstrap over test raters pooled across folds (B = 2,000) for every model difference.
Secondary: seen raters on test items (training raters' ratings of test items), where F/L use the trained rater parameters.

## Prespecified hypotheses (primary metric, k = 20)
- **H1** (rater-side structure is usable for new raters): F − T0 > 0 with a 95 % interval excluding 0.
- **H2** (individual beats group): F − G > 0 with interval excluding 0.
- **H3** (structured ≥ unstructured): F − L ≥ −0.005 nats (lower 95 % bound); "F beats L" only if the lower bound > 0. Reported also at k = 5, 10, 50.
- **H4** (which part matters): F-scale − F-shift is reported with its interval (stage 1 predicts > 0).
- **H5** (distributional RMs do not personalise): F − D > 0 with interval excluding 0.
If H1 fails, the paper does not claim a personalisation method; it reports the measurement result (stage 1) and the negative stage-2 result.

## Stage 2b (GPU; only after 2a is complete, separately amended)
The same comparison with an end-to-end LoRA reward model (Qwen2.5-7B-Instruct) in place of the frozen-feature text head, and on a second dataset.

## Forbidden statements
"Disagreement is rater-side, not text-side" (stage 1 found ~10 % decodable); any claim about raters' psychology; "F beats L" without the H3 criterion; claims about stage 2b from stage 2a.

## Amendments
**Amendment 1 (2026-10-27, after a 1-fold, 30-iteration smoke run used only to debug the code; no hypothesis was evaluated).** (i) Bugs fixed: the validation prompt groups were drawn with a re-seeded generator per group, so the validation split was empty and no penalty was actually selected; the summary's format string failed. (ii) The smoke run showed the rater-agnostic distributional head D fitting seen raters better than the single-index probit text head T0 (−1.444 vs −1.519 per rating), i.e. the probit text head cannot express text-predictable *item dispersion* (stage 1: G/X ≈ 10 %), which a fair comparison with D requires. Added **T1** (heteroscedastic probit text head: μ = β·x, log σ = γ·x) and **F1** = T1 + rater shift δ_r and rater log-scale s_r (σ = exp(γ·x + s_r)). **F1 is the primary factorised model for H1–H3 and H5** (F1 − T1, F1 − G, F1 − L, F1 − D; L and LS keep their homoscedastic text head, and F1 − LS is reported as well); F (homoscedastic) and the ablations stay reported, H4 is evaluated on F_scale − F_shift as registered. No other change.
**Amendment 2 (2026-10-27, after a second 1-fold, 30-iteration smoke run, B = 100; its numbers were seen and motivated this change, so they are not evidence and are not reported).** (i) Bug: new raters were given rater parameters 0 (k = 0) and adapted toward 0, but the jointly trained text side is calibrated to the *mean* of the training raters' parameters, so the prior mean must be that mean (F1 at k = 0 was worse than T1 although it should coincide in expectation). New raters now start at, and are shrunk toward, the training-rater mean. (ii) Even the heteroscedastic probit head (T1) fits held-out ratings much worse than the rater-agnostic distributional head D, so a comparison of rater models built on the probit head would be confounded by the text head. The **primary family is therefore built on the distributional head D**: **DG** = D + group (crowd/expert) logit offsets; **DF** = D + a rater-specific, text-independent offset vector on the 5 class logits (the rater's category-use propensities: a factorised response-style model with 5 parameters per rater, shrunk toward the training-rater mean); **DL** = D + a text-interacting low-rank rater latent (logits + (x W_k)·z_r, d = 8). Hypotheses re-mapped before any full run: **H1** DF − D > 0 (interval excluding 0); **H2** DF − DG > 0; **H3** DF − DL ≥ −0.005 (lower bound), "DF beats DL" only if the lower bound > 0; **H4** unchanged (F_scale − F_shift, probit family); the probit family (T0, T1, G, F, F1, ablations, L, LS) is reported as the interpretable secondary analysis. Everything else (folds, k, draws, penalties grid, bootstrap) unchanged; the full run uses 300 L-BFGS iterations and B = 2,000.

