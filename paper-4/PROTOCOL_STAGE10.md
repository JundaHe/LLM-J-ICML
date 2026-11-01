# Paper 4 — Stage 10: new-developer personalisation on code-readability ratings (frozen before any result)
Committed 2026-11-01 at the user's request ("加 SE benchmark"), after an audit of the software-engineering panels of paper 2 for persistent rater identities (two qualify: Dorn — 5,468 developers, 360 snippets in Java / Python / CUDA, median 20 ratings each; Buse–Weimer — 121 raters × 100 Java snippets, fully crossed; Roy 2021 ships no summary text, MLCQ has 26 reviewers and no code, JetBrains ≤ 10 ratings per rater, Scalabrino 9 raters). Any change after the first result is logged under "Amendments".

## Panels
**bw_raters**: Buse–Weimer, 100 snippets × 121 raters, 1–5 readability, persistent rater IDs (the paper-2 loader's columns). **dorn_raters**: Dorn, every (snippet, participant) rating as one row (participants are the rows of the three score files, which share participant order — checked), 1–5 readability; participants with at least 10 ratings. Items are grouped by snippet. Text features: the paper-2 Qwen2.5-Coder-7B-Instruct last-token states of the CoReEval Java judge prompt for each snippet (E_last), PCA-256 as in the main tables (Buse–Weimer has only 100 snippets, so its PCA has 100 components). No rater demographics: one rater group.

## Protocol and models
`factorised_rm.py` unchanged in substance: 5 rater folds × 5 snippet-group folds; D (text-only distributional head), DF (text-independent rater category offsets — the scale-use baseline on single-response scales, as on DICES), DL (low-rank text-interacting rater latent, few-shot-tuned prior), with the permutation control; k ∈ {0, 5, 10} on Dorn (≈ 16 adaptation candidates per developer), {0, 5, 10, 20, 50} on Buse–Weimer.
**Ranking outcome for single-response ratings (new):** within-rater pairwise concordance on test snippets — over all pairs of a test rater's test ratings with different scores, the share in which the model's expected score orders the two snippets as the rater did (ties in prediction count ½). Text-independent offsets cannot change a rater's own ordering of snippets (they shift every snippet alike, up to the nonlinearity of the expected score), so concordance isolates content-dependent personalisation, as direction accuracy does for pairwise preferences.

## Outcomes and decision rules (fixed now)
**SE-1 (scale use transfers to new developers):** DF − D held-out LL per rating at k = 10 (Dorn) and k = 20 (Buse–Weimer), rater bootstrap; holds if the lower 95 % bound exceeds 0.
**SE-2 (content personalisation of developers' readability judgements):** DL's own concordance gain (DL(k) − DL(0)) and own − other at the same k. *Content personalisation detected* if either lower bound exceeds +1 point; *ranking null* if both upper bounds are below +1 point; otherwise inconclusive. Reported for DF too (expected ≈ 0 by construction).
Secondary: k-curves, RPS, the population-level learner-free agreement of two developers on the ordering of two snippets.
A code-attribute version of SAP (classical readability features — line length, identifier length, comments, nesting, blank lines, …) follows in an amendment, with its dictionary fixed before it is run.

## Amendments
