# Paper 4 — Stage 2b: the factorised rater model on top of a fine-tuned LLM reward model (frozen before any result)
Committed 2026-10-27, after stage 2a (results/STAGE2A_REPORT.md). Stage 2a used a frozen-feature (PCA-256 ridge) text head. Objection to answer: a stronger, fine-tuned text model might absorb what the rater offsets capture, or an LLM that sees a rater's past ratings in context might personalise better than three numbers. Any change after the first result is logged under "Amendments".

## Data and splits
MultiPref overall_pref, the same 5 rater folds × 5 prompt-group folds, validation groups and k-shot draws as stage 2a (identical seeds; the fold code is shared).

## Text head (2b-1, primary): D-LoRA
For each fold, Qwen2.5-7B-Instruct with LoRA (r = 16, all attention and MLP projections, lr 1e-4, linear warm-up/decay, accumulation 8, 1 epoch) is trained on the **training raters' ratings of the training items** (validation groups excluded): target = the histogram of the training raters' ratings of the item, loss = soft cross-entropy on the 5 score-token probabilities at the judge prompt's answer position (the stage-1 / paper-2 prompt). Test raters' ratings are never used. After training, the 5 score-token log-probabilities are computed for every item and frozen.

## Rater models on top of D-LoRA
Exactly the stage-2a distributional family with the text logits replaced: lg = a·ℓ_LoRA(x) + b (temperature a and class bias b fitted on the training cells), plus — DG: group offsets; DF: rater offset vector (5); DFs: symmetric style offsets (3); DL: low-rank text-interacting latent using the frozen PCA-256 features x for the interaction (with constant column). Penalties, adaptation (training-rater prior, primary; k-shot-tuned prior, Amendment-5 procedure, reported), k ∈ {0, 5, 10, 20, 50}, 5 draws, rater-cluster bootstrap B = 2,000: unchanged.

## In-context personalisation baseline (2b-2, folds 0–1 only for compute; stated)
RC-LoRA: the same LoRA recipe, but each training example is a (training rater, training item) pair whose prompt contains k_train = 10 other training-item ratings of the same rater (the "rater history" prompt of paper 2's rc arm), target = that rater's rating (hard cross-entropy), 1 epoch over ≈ 8k sampled pairs. At test, a new rater's prompt contains k ∈ {5, 20} of their training-item ratings (the same draws as the rater models, first draw), scored on their test-item ratings. Compared with DFs and DF on top of D-LoRA on the same raters, items and draws.

## Hypotheses (k = 20; held-out LL per rating of new raters)
- **B1** DFs(D-LoRA) − D-LoRA > 0 (interval excluding 0): the style gain survives a fine-tuned text head.
- **B2** D-LoRA − D (stage-2a frozen-feature head) > 0: the fine-tuned head is the stronger text model (otherwise B1 answers nothing new).
- **B3** DFs(D-LoRA) − RC-LoRA ≥ −0.005 (lower bound) on folds 0–1: three numbers are not worse than in-context personalisation by a fine-tuned LLM; "better" only if the lower bound > 0.
- Direction accuracy reported for all; H6-style requirement for DFs: direction accuracy not lower than D-LoRA's by more than 0.005 (lower bound).

## Forbidden statements
"LLMs cannot personalise from examples" (one recipe, one model); anything about stage 2b on DICES/PRISM.

## Amendments
**Amendment 1 (2026-10-28, after the folds 0–1 result; GPUs idle).** The B3 result rests on two folds with one training seed each and large fold-to-fold variation of the in-context gain (+0.075 vs +0.021). RC-LoRA is extended to folds 2, 3, 4 with the identical recipe and evaluation (k ∈ {5, 20}, draw 0); B3 is re-evaluated on all five folds with the same criterion, and the two-fold result is kept and reported.
