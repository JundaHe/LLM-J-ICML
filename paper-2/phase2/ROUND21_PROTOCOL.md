# ROUND21 protocol: response to the round-21 review (reviews/claude_round21_2026-11-06.md)

Each analysis is specified here before it is run. The review was produced by a Claude subagent because Codex was unavailable.

## R21-1 Valid intervals for the decoding estimands (review N1, N10). Specified 2026-11-06 13:40, before any run
**Problem.** The percentile item bootstrap of R20-1 duplicates items inside the cross-fit while α stays fixed. It is not centred on the point estimate, and the draft quoted only its upper side.
**Primary method.** Each point-estimate repetition (R = 10, two directions) already gives every item a cross-fitted prediction and a per-item contribution: g_i to G_own, v_i = ⟨r̂_i, s2_i⟩/NRM, x_i to X_own, the projected gains, and their permuted versions. We average the contributions over repetitions and directions and take the mean over items. The SE of that mean is the item-cluster (group) CLT standard error. Ratios θ = ḡ/x̄ get delta-method intervals from the influence values (g_i − θ x_i)/x̄.
This treats the cross-fitted decoder as fixed, which is standard for cross-fitted estimators. It ignores decoder-fitting variability, which is second order under cross-fitting and partly averaged out over the R repetitions. No item is ever duplicated. Code: decode_decomp.py with `--B 0 --tag _r21`, writing results/decode_decomp/<panel>_r21.json (key "clt").
**Sensitivity.** We also report the basic interval [2θ̂ − q97.5, 2θ̂ − q2.5] from the stored R20-1 percentiles (no rerun needed), together with the shift (percentile midpoint − θ̂).
**Calibration check (fixed now).** On the ten γ 0 draws (SummEval and POPQUORN, s0–s4), V_own has mean 0 under the null because r̂ depends only on other items' panel-1 data and the features. We report how many of its CLT 95 % intervals cover 0. If ≥ 9 of 10 cover 0, the method is used for the headline. Otherwise the headline reports point estimates only, with both interval types as sensitivity.
Note: G_own itself has negative expectation under the null (−E‖r̂‖²/n), so a G_own interval below 0 at γ 0 is expected. R20-1's reading (i) was ill-posed for G_own, and the draft says so.
**Estimands reported (N10).** G_own/X_own (the proper-score gain) and (G_own − G_own,perm)/X_own (the gain net of the variance penalty the decoder would also pay on permuted features). Both are reported with one sentence on what each answers.
**Readings (fixed now).**
- (i) The ordinal–NLI contrast is re-evaluated with the CLT intervals for both estimands: every NLI lower bound must exceed every ordinal upper bound among the panels with X_own's CLT interval excluding 0. This replaces R20-1 (iii) for the headline. R20-1's percentile result stays reported as the frozen outcome of R20-1.
- (ii) Panels re-run: the 14 R20-1 runs plus the 10 γ 0 draws.

## R21-2 Source of the negative null mean of X_own (review N5). Specified 2026-11-06 13:40, before any run
**Hypothesis.** In every simulated γ 0 matrix the M = 8 positions belong to fixed raters with their own cut-points (M2 model), and each item's two halves are drawn without replacement from that one pool. If half 1 gets the lenient raters, half 2 gets the strict ones. This finite-pool negative dependence is not fully absorbed by the exact (mode, mean) cell, and it makes E[X_own] < 0. With an infinite rater population, or with no rater heterogeneity, the bias should vanish.
**Design.** x_own_null.py simulates γ 0 matrices from the panel's M2 fit under three regimes: pool (as in R20-2), common (all raters use the median cut-points) and iid (each rating's cut-points drawn with replacement from the pool). It computes X_own exactly as decode_decomp.py, with 20 simulations and R = 10. Panels: summeval_coherence8 (a = 4), popquorn_off8 (a = 4), dices (a = 20), dices990 (a = 20).
**Readings (fixed now).**
- The hypothesis is supported if the pool mean is < 0 by more than 2 SE while both common and iid lie within 2 SE of 0.
- If supported: the paper explains the null bias as a finite-rater-pool effect. It notes that the same effect operates on real panels with a fixed rater pool, so a real X_own is the shape-to-shape reproducibility *within the pool* and is biased downward relative to an infinite population of such raters. The paper reports a pool-bias-corrected X_own (observed − simulated pool mean) as a sensitivity, and the absence statements (DICES, POPQUORN) are softened accordingly.
- If not supported: the bias is reported as unexplained, and the corrected X_own is still given as a sensitivity.

## R21-3 Rater-count-matched ordinal–NLI contrast (review N4). Specified 2026-11-06 13:40, before any run
ChaosNLI MNLI and SNLI are decoded at a = b = 4, matching SummEval and POPQUORN, with decode_decomp.py at R = 10 and B = 0 (CLT intervals, R21-1) under tag _a4_r21. DICES-350 is decoded at a = 40, b = 20 (m = 104), where §1 reports item-level ρ_own > 0.
**Readings (fixed now).**
- The matched contrast holds if the a = 4 NLI lower bounds of G_own/X_own exceed the SummEval upper bounds at a = 4. The abstract states the contrast at matched a if it holds. Otherwise it states it "at the a used", per panel.
- DICES-350 at a = 40 is a headline panel if its X_own CLT interval excludes 0.

## R21-4 Plant at a = 20 (review N3). Specified 2026-11-06 13:40, before any run
A dispersion plant on dorn_java (the Dorn panel with an M2 fit) at a = 20, b = 20, γ ∈ {0, 0.6}, draws s0–s2, with R = 10 and B = 0. The real dorn_java is run at a = 20 with the same settings. This is descriptive: detection (G_own CLT lower bound > 0) and recovery, and the planted X_own against the observed X_own. It gives the a = 20 ordinal panels a reference like SummEval's. No plant is defined for the nominal ChaosNLI panels, because the dispersion construction is ordinal.
**Calibration scale (N3).** From R21 on, the calibration compares planted with observed X_own, which is the scale of the headline estimand. R20-2's X-scale rule and its outcome stay reported as frozen.

## R21-5 Other feature families for the own-shape estimand (review issue 1a). Specified 2026-11-06 13:40, before any run
Rerun decode_decomp.py (R = 10, B = 0) with `--feat_model Qwen3-8B` and `--feat_model OLMo-2-1124-7B-Instruct` on the panels whose feature files exist in all three families: summeval_coherence8 (a = 4), chaosnli_mnli (a = 20) and dices (a = 20). We report G_own/X_own with CLT intervals per family. The abstract's "frozen LLM representations" is kept only if the SummEval and MNLI values agree in their qualitative reading across families. Otherwise it is restricted to Qwen2.5.

## R21-T Text corrections (review N2, N6–N9, N11–N19, LOW)
- **Plant figures.** POPQUORN γ 0.6 is 4 of 5, 6–38 %; mean planted X at γ 0.3 is 0.00060. The misplaced parenthetical is fixed. The averaging convention of R20-2c is flagged as post hoc.
- **EmoBank** (b = 2): unmeasurable, as HS2. "EmoBank (3–4 raters)" is removed.
- **Absence wording.** "No reproducible shape to decode" and "at the rater counts available" become "no detectable shape-to-shape reproducibility at a = …". The POPQUORN null is called uninformative.
- **ΔGP.** It is reported in absolute RPS, not on the X_own scale. ΔGP > 0 with X_own ≈ 0 (HS2, EmoBank) is described as text-predictable within-cell location denoising. "Dorn the only ordinal panel …" is corrected.
- **Contribution (4), §1 (v), §5 and guidance.** Items-first in the LoRA blocks holds in 1 of 3 prospective blocks. One threshold is used consistently for the frozen heads. The penalty wording becomes "the point estimates exceed the 0.005 margin; non-inferiority fails". The prospective blocks contain two independent assignment sets. §5 leads with the prospective blocks. The superseded 480 × 2 result is described accurately (its interval excludes 0). 819 × 2 − full is reported. The SummEval one-vs-two sentence is held until R20-5.
- **SummEval population (N11).** The evaluator is a held-out expert, and 960 × 1 draws a crowd rating with probability 5/7. We report descriptively the penalty stratified by whether the sampled training rating was an expert's, if train logs or meta allow it; otherwise the confound is stated.
- **§4.** The SummEval residual is restated in X_own terms. The DICES-350 rater-side claim is made conditional on the observed pool.
- **Abstract.** "On none" is backed by upper bounds or softened. The abstract is shortened.
- **§6.** "Three to five raters fix its location and nothing else" is replaced.
- **LOW.** The header, the "35–70 % of X on ChaosNLI" figure, the (iii) caveat restored, and the null-check sentence (GP > 0 at γ 0; only ΔGP is 0).

### R21-2 results (2026-11-06 14:45; 20 simulations × R = 10; results/x_own_null/*.json)
| panel (a, b) | rater groups (cut-point SD) | pool | common | iid |
|---|---|---|---|---|
| SummEval coh. (4, 4) | 4 (0.50) | **−0.000099 ± 0.000010** | +0.000007 ± 0.000011 | +0.000018 ± 0.000010 |
| DICES-350 (20, 20) | 104 (0.73) | **−0.000015 ± 0.000003** | +0.000004 ± 0.000003 | +0.000003 ± 0.000004 |
| POPQUORN (4, 4) | 1 (0) | −0.000002 ± 0.000013 | +0.000007 ± 0.000010 | +0.000007 ± 0.000009 |
| DICES-990 (20, 20) | 1 (0) | +0.000001 ± 0.000002 | +0.000002 ± 0.000002 | +0.000003 ± 0.000002 |
**Reading (as frozen): the hypothesis is supported** on SummEval and DICES-350. There the pool mean is < 0 by 10 and 5 SE, while common and iid lie within 2 SE of 0 (SummEval iid +1.8 SE). On POPQUORN and DICES-990 the M2 fit has a single rater group, so pool and common coincide and no bias is expected; none is found. This is consistent with the hypothesis.
**Consequences.**
- (a) The negative null mean of X_own is a finite-rater-pool effect. Splitting one fixed pool of heterogeneous raters without replacement makes the two halves' rater mixes anti-correlated, and the exact cell absorbs only part of that.
- (b) On real panels with persistent heterogeneous raters, X_own is shape-to-shape reproducibility *within the pool*, biased downward relative to new raters drawn from the same population.
- (c) Sensitivity (model-based correction): SummEval coherence X_own 0.00038 → about 0.00048, and DICES-350 (a = 20) 0.000044 [−0.000018, 0.000109] → about 0.000059 [−0.000003, 0.000124], whose interval still covers 0, by a margin smaller than the correction's own uncertainty. The draft says DICES-350 at a = 20 is "not detectable, and borderline after the pool correction".
