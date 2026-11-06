# Round-21 adversarial review (Claude subagent, 2026-11-06)

Codex was unavailable because of its usage limit, until 2026-11-11 21:45. This review was produced by an independent Claude subagent from the same prompt (reviews/codex_round21_prompt_2026-11-06.md). The reviewer could read the result JSONs and checked the numbers against them. The text below is a faithful condensation of the review, kept issue by issue. The author's verification notes are in [brackets].

**Verdict: weak reject (close to borderline).**
The estimand is right now, and the budget results are prospective, with the frozen readings followed honestly. But the headline decoding claim (about 1 %, "95 % upper bounds ≤ 2.2 %") rests on a percentile bootstrap that the authors themselves show is off-centre, and it reports only the side that favours the claims. The X_own null-bias explanation does not apply (a = b = 4), and it draws the wrong conclusion about which readings are conservative. The ordinal–NLI contrast compares a = 4 with a = 20. Some of the plant evidence is stale.
- **To borderline:** a valid interval, a diagnosed or corrected null bias, and the text fixes.
- **To weak accept:** additionally, an a-matched ChaosNLI decoding that still separates from the ordinal panels.

## Status of the round-20 issues
1. Cross-term: **partly resolved.** The own-shape estimand is computed only on Qwen2.5 last-token features, while Table 2, the layer probe and the RFF probe still report G/X. BW, Scalabrino, CSC and JetBrains are G/X only. The bootstrap is invalid (N1).
2. Max rule: **partly resolved.** It is withdrawn, but ΔGP/X_own upper bounds are now contrasted on both sides (N9).
3. Population: **mostly resolved**, but the abstract's "on none of these panels" rests on point estimates.
4. Plant: **partly resolved.** The rule is on X, which is 81 % cross-term on SummEval (N3); the POPQUORN γ 0.6 figures are stale (N2); there is one construction and no plant at a = 20.
5. αNLI sham: resolved as disclosure.
6. Nonlinear: resolved in the text. The RFF result is still quoted on G/X.
7. Inventory: **partly resolved**, with new stale items.

## Frozen readings and amendments
- R19-9, R20-3, R20-4: respected, and the numbers match the JSONs.
- R20-1 (i): G_own's interval excludes 0 from below in 6 of 10 γ 0 draws, not only POPQUORN s0. Also, "the projected gain is zero" is false: GP > 0 at γ 0 and only ΔGP is 0. [Author: correct as a description of the draft. But E[G_own] < 0 under the null by construction (the −‖r̂‖²/n term), so a negative null G_own is expected and is not by itself evidence of bootstrap shift. Reading (i) was ill-posed for G_own; the clean null quantity is ⟨r̂, s2⟩/n.]
- R20-1 (ii): wording exceeded. "There is no reproducible shape to decode" and "at the rater counts available" go beyond "no detectable … at that a".
- R20-1 (iii): the protocol's caveat "a frozen-rule pass, not a robust separation" was dropped from the draft.
- R20-2: **not respected for POPQUORN.** All five γ 0.6 draws exist: 4 of 5 detected, G_own/X_own 0.06–0.38 (0.361, 0.252, 0.064, 0.382, 0.323), mean X 0.00134. The draft says "2 of 2, 25–36 %". [Verified.]
- R20-2a/b/c: adequately disclosed and not a rescue in substance. However, the "mean planted X" convention was fixed post hoc.
- X_own null-bias note: the mechanism is wrong (a = b = 4 for SummEval and POPQUORN), and the sign argument is backwards. A downward-biased X_own makes "covers 0" more likely, which is anti-conservative for the absence claims. [Verified.]
- Bootstrap-centring note: the remedy keeps the upper bound, which is the side the shift biases in the authors' favour.
- HS2 logic not applied to EmoBank (b = 2). [Verified: emobank_reader_v5 has a = 3, b = 2.]

## New issues
- **N1 CRITICAL.** The headline "95 % upper bounds" are not valid. On relevance the upper bound sits below the point, and the point sits near the top of the percentile interval on Dorn, MNLI and SNLI. A basic-interval sensitivity check gives ordinal upper bounds of about 4.3 % / 12.4 % / 23 % and NLI lower bounds of about 27 % / 36 %. Fix: a bootstrap without duplicates inside the cross-fit (m-out-of-n subsampling; or re-selecting α and deduplicating), or at least stored replicates with BC/BCa/basic intervals. Until then, drop "95 % upper bounds" from the abstract.
- **N2 HIGH.** The POPQUORN plant figures are stale in the abstract, §1 and §2.2, and one parenthetical is misplaced (the γ 0.6 numbers are attached to "half that magnitude").
- **N3 HIGH.** The informativeness rule's scale (X) does not match the estimand (X_own). Make the X_own-matched comparison the primary calibration (labelled post hoc). Add plants at a = 20 (Dorn) and on ChaosNLI.
- **N4 HIGH.** The ordinal–NLI contrast confounds task with a (4 vs 20). Decode ChaosNLI at a = 4 and 8, and DICES-350 / BW at a = 40.
- **N5 HIGH.** The X_own null bias of about −1e−4 is unexplained. Diagnose it (simulation with the true cell mean; permutation of panel 2), report a corrected X_own, and soften the absence claims.
- **N6 HIGH.** Contribution (4) and the guidance overclaim items-first. It holds in 1 of 3 prospective LoRA blocks, and three different thresholds for the frozen heads appear across §1 (v), §5 and the guidance.
- **N7 HIGH.** EmoBank should be classed as unmeasurable at b = 2. "EmoBank (3–4 raters)" is wrong.
- **N8 MEDIUM.** "Dorn the only ordinal panel with a detectable valid-forecast gain" is false: HS2 and EmoBank have ΔGP > 0. Interpret ΔGP > 0 with X_own ≈ 0 as text-predictable location denoising.
- **N9 MEDIUM.** ΔGP/X_own is on an inappropriate scale (it can exceed 1; EmoBank 3.28), and upper bounds are contrasted with upper bounds. Report ΔGP in absolute RPS.
- **N10 MEDIUM.** The permutation correction is applied to GP but not to G_own. The corrected fractions would be about 2.2 / 2.9 / 11.4 / 36 / 45 %. Report both.
- **N11 MEDIUM.** Possible expert/crowd confound in the SummEval single-rating penalty: the evaluator is a held-out expert, and 960 × 1 draws a crowd rating with probability 5/7. Stratify or add arms.
- **N12 MEDIUM.** "More than the 0.005 margin" overstates: the lower bounds are 0.0045 and 0.0044. Say that the point estimates exceed δ and that non-inferiority fails.
- **N13 MEDIUM.** The three prospective blocks contain only two independent assignment sets (R20-3 reuses R19-9's).
- **N14 MEDIUM.** §5 opens with the superseded shared-assignment pass. "480 × 2 is not worse either (−0.0040 [−0.0084, −0.000001])" hides that the interval excludes 0, i.e. it beats the full data, which is implausible.
- **N15 MEDIUM.** "One versus two ratings per item is not distinguishable on either base" is asserted while R20-5 is running. Also report 819 × 2 − full = +0.0032 [+0.0016, +0.0048].
- **N16 MEDIUM.** §4's SummEval residual sentence uses X, not X_own.
- **N17 MEDIUM.** The §4 DICES-350 rater-side claim holds only conditional on the observed pool.
- **N18 MEDIUM.** The abstract's "on none" rests on point estimates.
- **N19 MEDIUM.** §6's "three to five raters per artifact fix its location and nothing else" is unsupported.
- **LOW.**
  - The header says "HS2 pending".
  - "35–70 % of X on ChaosNLI": at a = 20 it is 40 % / 32 %.
  - POPQUORN γ 0.3 mean planted X is 0.00060, not 0.00062.
  - The abstract is about 450 words.
  - The (iii) pass hinges on the third decimal.
  - The OLMo 90 % interval is [+0.0006, +0.0115].

## Three most valuable changes
1. A valid decoding interval plus diagnosis and correction of the null bias, then recompute the headline bounds (N1, N5).
2. A like-for-like ordinal–NLI contrast: matched a, plants at a = 20, the X_own-matched calibration as primary, and other feature families (N3, N4).
3. Text aligned with the results (N2, N6–N9, N14, N15).
