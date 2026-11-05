# Paper 2 — Round-19 analyses (frozen before any result is computed)
Committed 2026-11-05, after `reviews/codex_round19_2026-11-05.md`. Each analysis is fixed here before it is run; amendments are logged below and do not change the readings.

## R19-1 Cross-term diagnostic for X (CPU; answers review issue 1)
**Question.** `rho_exact.py` defines r1 = C(h1 − q1), r2 = C(h2 − q1), with q1 the exact mode+mean comparator of panel 1. Then r2 = C(h2 − q2) + C(q2 − q1), so X = X_own + X_cross with X_own = ⟨C(h1 − q1), C(h2 − q2)⟩/NRM (q2: the same exact-T comparator built from panel 2 itself) and X_cross = ⟨C(h1 − q1), C(q2 − q1)⟩/NRM.
**Scope.** Dense panels only (b = 20 second-panel raters; on the small leave-one-out panels b = 1, panel 2's own exact comparator equals its one-hot histogram, so X_own ≡ 0 and X is by construction a new-rater forecasting quantity — stated in the text, not estimated). Panels: every `results/rho_exact/` panel with m > 12, at every a in its existing A_LIST.
**Procedure.** Identical splits, folds (fold seed 1), R = 10 repetitions and item-cluster bootstrap (B = 200, seeds as in `rho_exact.py`) as `rho_exact.py`; additionally compute q2 = `exactT_q` on panel 2 (its own mode, sum, histogram) and report X, X_own, X_cross, M, M_own := mean ‖C(h2 − q2)‖²/NRM and ρ_own := X_own / M, each with a 95 % interval.
**Readings (fixed now).**
- *Cross-term negligible* if, at every a, the X_cross interval lies within ±25 % of |X| or within ±0.0005 absolute (whichever is larger). Then the text may describe ρ as reliability of the shape beyond location, noting the decomposition.
- Otherwise the text describes ρ only as an operational *new-rater forecasting* quantity (the identity A1 = M − 2X with NRM-normalised inner products, see R19-T) and reports X_own separately as the shape-to-shape reproducibility.
Either way, the draft adopts the narrower "forecasting" wording for the small panels.

## R19-T Text-only corrections (no new computation)
Score normalisation stated (all inner products divided by NRM = K − 1 for ordinal, 1 for nominal, as implemented); ties in "exact mode" defined as in `z_label`; abstract bound qualified by clustering; "matches" → "no difference detected (interval)"; "always" → counts; "do not use the shape" / "unlearnable" narrowed to the probes run; mechanistic budget explanation removed from §5; approximate budgets and the rounding rule stated; panel inventory table; definitions of A1^x, mode prototype, reliability-shrunk targets, CSC, the thirty configurations; "−0.0000 [−0.0000, +0.0000]" printed at more digits.

## R19-2 Planted-shape calibration of the decoding pipeline (CPU; issue 3) — specified 2026-11-05 before any planted run
**Design.** Semi-synthetic rating matrices with the panel's items, features, rater columns, item locations θ_i and rater cut-points taken from the fitted M2 model (`results/rater_item/<panel>_M2_params.npz`), and a planted, text-predictable shape: σ_i = median(σ̂) · exp(γ s_i), where s_i is the standardised projection of the item's label-free PCA-256 features on a random unit direction within the top 64 components (seed 0). Ratings y = #{cut-points < θ_i + σ_i ε}. γ ∈ {0, 0.15, 0.3, 0.6}; γ = 0 is the null (no text-predictable shape). Panels: SummEval coherence (8 raters, a = 4) and POPQUORN offensiveness (8 raters, a = 4) — the two panels with the tightest decoding nulls. The **unchanged** decoding pipeline (`decode_residual.py --plant γ`, default R = 10, B = 500, Qwen2.5 E_last) is run on each.
**Readings (fixed now).** (i) *Null calibration*: at γ = 0 the G interval covers 0 and G_perm ≤ 0 + its interval. (ii) *Detection threshold γ\**: the smallest γ whose G lower bound is > 0. (iii) *Informativeness of the real-data null*: for the panel, compare the planted X at γ\* with the observed X of the real panel; if the planted X at γ\* is ≤ the observed X, the pipeline would have detected a text-predictable shape of the observed magnitude, and the real-data null is reported as informative at that scale; otherwise the null is reported as uninformative below that magnitude. (iv) G/X at each γ is reported to show what fraction of a known, linearly planted shape the pipeline recovers (an upper reference for the real-data G/X). One simulation draw per γ; stated as a limitation.
## R19-5 Nonlinear decoder (CPU; review issue 3 / change 2) — specified 2026-11-05 after R19-2 interim point estimates (ridge recovers G/X ≈ 0.07–0.12 of a linearly planted shape), before any nonlinear run
**Decoder.** `decode_residual.py --decoder rff`: identical pipeline (splits, comparator, folds, nested α selection over the same grid, permutation and positive controls, bootstrap) except that the fold-wise PCA-64 scores are mapped to 2,048 random Fourier features of a Gaussian kernel (median-heuristic bandwidth on the training rows, seed 7) before the ridge — i.e. approximate kernel ridge regression.
**Runs.** SummEval coherence and POPQUORN offensiveness (a = 4): real data, and planted γ ∈ {0, 0.3, 0.6} (R19-2 construction, seed 0). B = 200 (stated; ridge runs used 500).
**Readings (fixed now).** (i) Null: γ = 0 G interval covers 0 or lies below it. (ii) *Decoder bottleneck* if at γ = 0.6 the RFF G lower bound exceeds the ridge G point estimate on that panel; then the real-data RFF G/X is reported alongside ridge as the decoding bound. (iii) Real data: RFF G/X with interval; if its lower bound > 0 the draft must report that a nonlinear decoder recovers reproducible shape that ridge does not.

## R19-3 Rater-model reproduction of dense-panel X (CPU; issue 4) — specified 2026-11-05, after R19-1 rows were visible on 4 of 8 panels but before any simulation at dense splits
**Panels.** Dense panels with persistent rater identities: Buse–Weimer (121 raters) and DICES-350 (104); additionally Dorn Java (no rater identities: M0 and M2 only).
**Procedure.** Refit M0, M1, M2 on the full matrix exactly as `rater_item_model.py` (same grids, λ_σ selected there; values read from `results/rater_item/<panel>.json`). Draw 20 simulated matrices per model (seed 200 + model). On each simulated and on the observed matrix compute X, X_own, X_cross (R19-1 definitions) at a ∈ {10, 20, 40} (a + 20 ≤ m), b = 20, R = 5 split repetitions, fold seed 1.
**Readings (fixed now).** At a = 40 (else the largest a), a model *reproduces* a statistic if the observed point estimate lies within the 2.5–97.5 % range of its 20 simulated values. "Thresholds explain something location alone cannot" requires M1 to reproduce observed X_own and M0 not to. If neither M1 nor M2 reproduces X_own, the draft states that the measurement models do not account for the dense-panel residual and removes the rater-side mechanism language from §4 except as a description of the likelihood gains.

## R19-4 Budget comparison with documented optimisation exposure (issue 7)
**Amendment 2026-11-05 (before any new training):** an audit of the existing run certificates (`results/lora_budget_v2/**/meta.json`, `results/lora_budget_olmo/**/meta.json`) shows that every arm of each budget block was trained for the same number of optimiser steps — 240 on SummEval (Qwen2.5 and OLMo-2), 205 on POPQUORN — with gradient accumulation 8 (1,920 / 1,640 training examples seen per run), the same learning-rate schedule and no early stopping; only the number of distinct items (and hence the repetition per item) differs. Realised ratings: SummEval 960 × 1 = 960, 480 × 2 = 960, 144 × 7 = 1,008 (rounding up favours the many-rater arm); POPQUORN 819 × 1 = 819, 117 × 7 = 819, 819 × 2 = 1,638. Optimisation exposure is therefore matched by construction and the review's confound does not apply; no rerun is needed for it. A new equivalence margin is **not** declared after the results were seen; the draft keeps "not distinguishable".

## Amendments

## Result R19-1 (2026-11-05 17:31; read by the frozen rule, no revision)
Cross-term negligible at every a: **not met** on 6 of 8 dense panels (fails at a ≤ 15–20 on BW and the three Dorn panels, at every a on both ChaosNLI panels); met on DICES-350 and DICES-990 only through the ±0.0005 absolute leg, which is uninformative there (|X| ≤ 0.0002). **Reading: ρ is described as a new-rater forecasting quantity; X_own is reported as the shape-to-shape reproducibility.**
At a = 40, X_own [95 %] and ρ_own = X_own / M: BW 0.00017 [0.00005, 0.00031], 0.13 [0.04, 0.24]; DICES-350 0.00005 [0.00001, 0.00009], 0.10 [0.02, 0.19]; DICES-990 0.00002 [−0.00000, 0.00005], 0.06 [−0.00, 0.14]; Dorn CUDA 0.22 [0.11, 0.29]; Java 0.13 [0.07, 0.26]; Python 0.13 [0.09, 0.26]; ChaosNLI MNLI 0.61 [0.58, 0.63]; SNLI 0.67 [0.64, 0.69]. At a ≤ 8 the X_own intervals of BW and all Dorn panels include 0 while X does not.

## Result R19-3 (2026-11-05 17:31; frozen rule)
At a = 40, observed X_own within the 20-simulation 95 % range of: BW — M0 yes, M1 yes, M2 no; DICES-350 — M0 no, M1 yes, M2 yes; Dorn Java (no rater identities) — M0 no, M2 yes. **"Thresholds explain something location alone cannot": met on DICES-350, not met on BW (location-only M0 already reproduces X_own); not testable on Dorn (M2, item dispersion, is needed there).** The removal clause (neither M1 nor M2 reproduces) is not triggered on any panel.
Descriptive: at a = 10 the location-only model M0 reproduces most of the observed X through X_cross (BW 0.00037 of 0.00052 observed; Dorn Java 0.00056 of 0.00068), i.e. the small-a positive X is largely produced by location noise interacting with the exact comparator.

## Note (2026-11-05, R19-2 runs): Gc is not a shape-only gain
At γ = 0 the clipped gain Gc is positive (+0.00004 / +0.00005) while G ≈ 0. `clip_gain` clips the cumulative forecast to [0, 1] and renormalises, which does not preserve the mean, so Gc mixes a location change into the score. Gc is therefore not used for any shape claim (the draft never used it); review issue 2 (validity of q_T + C⁻¹ r̂) is answered in text: G is the quadratic-score gain of the additive correction on the cumulative vector, which need not be a valid distribution; a location-preserving projection onto valid distributions is not implemented, and this is stated as a limitation.

## Result R19-2 (2026-11-05 21:45; frozen readings, no revision)
| panel | γ | G [95 %] | G_perm | planted X | G/X [95 %] |
|---|---|---|---|---|---|
| SummEval coh. | 0 | −0.00000 [−0.00001, +0.00000] | +0.00000 | −0.00008 | — |
| | 0.15 | +0.00000 [−0.00003, +0.00002] | −0.00002 | 0.00010 | — |
| | 0.3 | +0.00007 [+0.00003, +0.00013] | −0.00007 | 0.00067 | 0.11 [0.04, 0.19] |
| | 0.6 | +0.00020 [+0.00017, +0.00028] | −0.00010 | 0.00166 | 0.12 [0.11, 0.17] |
| POPQUORN off. | 0 | −0.00000 [−0.00001, +0.00000] | −0.00000 | 0.00010 | — |
| | 0.15 | −0.00000 [−0.00001, +0.00001] | −0.00000 | 0.00047 | — |
| | 0.3 | +0.00000 [−0.00003, +0.00004] | −0.00003 | 0.00063 | — |
| | 0.6 | +0.00010 [+0.00005, +0.00014] | −0.00006 | 0.00148 | 0.07 [0.03, 0.09] |
(i) Null calibration: **met** on both panels. (ii) γ*: SummEval 0.3, POPQUORN 0.6. (iii) SummEval: planted X at γ* (0.00067) ≤ observed X (0.00198) → **the real-data null is informative at the observed scale**. POPQUORN: planted X at γ* (0.00148) > observed X (0.00036) → **the real-data null is uninformative below that magnitude**. (iv) Where detected, the pipeline recovers G/X ≈ 0.07–0.12 of a linearly planted shape; real-data G/X bounds are to be read against this ceiling, not against 1. One simulation draw per γ.

## R19-5 amendment (2026-11-05 21:45, after one smoke point (SummEval γ = 0.6, R = 1, B = 2: G/X 0.114) and before any full RFF run)
Compute: the smoke run took 14 min on a loaded node; full runs use **R = 5, B = 100** (D = 2,048 unchanged). Readings unchanged.

## R19-6 Crossed item × rater uncertainty for the dense reliability rows (review issue 6) — specified 2026-11-05 23:45, before any crossed-bootstrap run
**Scope statement (text).** Item-cluster intervals condition on the observed rater pool wherever raters recur across items. On panels whose rating columns are positions rather than persistent people (SummEval, HelpSteer2, EmoBank, CSC, ChaosNLI, MultiPref, the SE panels without identities, Dorn), each item's ratings are draws from the crowd for that item and the item bootstrap already resamples them; on panels with persistent identities (Buse–Weimer, DICES-350, DICES-990, POPQUORN) item-only intervals are conditional on the pool. The draft states this in §2.1.
**Analysis.** On the three complete crossed panels (BW 100 × 121, DICES-350 350 × 104, DICES-990 990 × 60), recompute the R19-1 rows (X, X_own, ρ = X/M, ρ_own) with a crossed bootstrap: each replicate resamples item clusters (`boot_items`, as before) and, independently, the m rater columns with replacement (multiplicities w). Because P1 and P2 must be disjoint raters (a duplicated rater in both panels would create spurious agreement), each item's P1 ∪ P2 is a+b *distinct* raters drawn without replacement with probability proportional to w (Efraimidis–Spirakis keys), the first a forming P1; a replicate whose number of distinct raters is < a+b redraws the rater multiset. a ∈ {10, 20, 40} with a + 20 ≤ 0.6 m (the rule governs: BW and DICES-350 all three (DICES-350: 60 ≤ 62.4), DICES-990 a = 10 only), b = 20, 3 split repetitions per replicate, B = 200, seeds as rho_own.py. Point estimates are the existing rho_own rows. Script `rho_crossed.py`, output results/rho_crossed/<panel>.json.
**Readings (fixed now).** Report crossed intervals beside the item-only ones. The §1 claims "ρ < 0.3 at 40 raters" and "ρ_own 0.06–0.22 on the dense ordinal panels" stand as population statements if the crossed upper bound of ρ at the largest a stays < 0.5 (the forecasting threshold) on each panel; if any crossed upper bound reaches 0.5, the draft restricts that panel's claim to the observed rater pool.

### R19-6 results (2026-11-06 00:20; B = 200, results/rho_crossed/)
| panel | a | ρ | ρ crossed CI | ρ_own | ρ_own item-only CI | ρ_own crossed CI |
|---|---|---|---|---|---|---|
| BW | 40 | 0.218 | [0.033, 0.388] | 0.128 | [0.038, 0.242] | [−0.004, 0.259] |
| DICES-350 | 40 | 0.254 | [0.127, 0.351] | 0.097 | [0.019, 0.189] | [−0.022, 0.185] |
| DICES-990 | 10 | 0.061 | [0.007, 0.095] | 0.024 | [−0.020, 0.052] | [−0.026, 0.059] |
**Reading (as frozen):** the crossed upper bound of ρ stays < 0.5 on all three panels, so "the raw histogram does not forecast a new rater better than its mode and mean" stands as a population statement. **Not covered by the frozen reading, reported anyway:** with rater sampling included, ρ_own is no longer distinguishable from 0 on BW and DICES-350 at 40 raters (item-only intervals excluded 0); the ordinal shape-to-shape reproducibility is therefore bounded above (≤ 0.26) rather than shown positive for new raters. Crossed intervals for X are roughly 1.2–2× wider than item-only ones. Caveat: the distinct-rater draw uses ≈ 63 % of the pool per replicate.

## R19-7 Nominal audit under the paper's nominal scoring rule (review issue 9) — specified 2026-11-06 01:32, before any re-run
**Change.** `probe_nominal.py` additionally records `brier_ref` = mean_i ‖P_i − h_ref,i‖² against the fixed 50-annotation reference panel. Because h_ref is fixed per item, arm *differences* in brier_ref equal the differences in the expected Brier score for one new rater drawn from the reference panel (E_y‖P − e_y‖² = ‖P − h_ref‖² + const); likewise for KL vs the log score. Nothing else changes (same seeds, splits, arms, early stopping).
**Runs.** ChaosNLI MNLI, SNLI, αNLI at m ∈ {5, 10, 20, 50}; 3 seeds × 3 item splits; one GPU job (`--gres=gpu:1`), tag `_v7b`. MNLI's published table used `_v6`; the re-run uses the current code, and any KL difference from the published `_v6`/`_v7` rows is reported (reproducibility check: |ΔKL| per arm mean ≤ 0.002, else the table is regenerated from `_v7b`).
**Readings (fixed now).** (i) The donor-replacement contrast pzc − soft in Brier, with its descriptive SEM over the 9 configurations, at every m. (ii) Normalised dose: (pzc − soft) / (fidelity_zc − fidelity_soft) in Brier, i.e. the cost of scrambling the shape relative to the shape signal available to an oracle using the item's own m training ratings on the same test items. (iii) The draft's "same intervention on ChaosNLI costs …" sentence is restated in Brier (the paper's nominal score) with (ii); if pzc − soft in Brier is not positive at some m, the sentence is restricted to the m where it is.

## R19-8 Validity of the decoded forecast and a cell-preserving projection (review issue 2) — specified 2026-11-06 01:35, before any run
**Question.** G is the quadratic-score gain of the additive correction q_T + C⁻¹r̂, which need not be a valid distribution in the recipient's exact mode-and-mean cell. How often is it invalid, and what is the gain of the nearest valid forecast in that cell?
**Projection.** Per item, q* = argmin ‖C(q) − (C(q_T) + r̂)‖² (the RPS metric) subject to q ≥ 0, Σq = 1, and the cell of q_T: ordinal — mean(q) = mean(q_T) and q_z ≥ q_k for the mode z of q_T (weak inequality; ties allowed); nominal — q_z = q_T,z and q_k ≤ q_T,z. Solved by SLSQP; items whose unprojected forecast already satisfies every constraint (tolerance 1e-9) are left unchanged. G_proj = score(q_T) − score(q*) on the P2 ratings (exact RPS / Brier), symmetrised and averaged over splits exactly as G.
**Violation rates** of the unprojected forecast: fraction of items with any negative mass, with the mode of q_T no longer a (weak) mode, and with |Δmean| > 1e-6 (ordinal; per-output α makes Σr̂ ≠ 0 possible).
**Runs.** Point estimates only (R = 10, the stored ridge α are re-selected exactly as in the point estimate; no bootstrap — stated), ridge decoder, Qwen2.5 E_last, d = 64, each panel's Table 2 a: all 16 decoding_v2 panels, plus SummEval and POPQUORN planted γ ∈ {0, 0.6}. Script `decode_validity.py`, output results/decode_validity/<panel>[tag].json.
**Readings (fixed now).** (i) Null: at γ = 0, |G_proj| ≤ 0.00002 on both panels. (ii) Report violation rates and G_proj/X beside G/X. (iii) If on any ordinal panel G_proj/X exceeds that panel's published G/X upper bound, the draft's bound for that panel is replaced by max(upper bound, G_proj/X) with the reason. (iv) If on ChaosNLI G_proj/X < 0.10 (published 0.17–0.26), the ordinal–NLI contrast in decoding is restated with G_proj.

### R19-7 results (2026-11-06 01:50; results/probe_nominal/*_v7b)
Reproducibility: the re-run reproduces the published KL of every arm exactly (max |ΔKL| over arm means 0.0000 on all 12 panel × m cells), so the published `_v6`/`_v7` tables stand.

| panel | m | Brier pzc − soft (± SEM, 9 cfgs) | oracle shape gap (fidelity_zc − fidelity_soft, Brier) | normalised dose | KL pzc − soft |
|---|---|---|---|---|---|
| MNLI | 5 | +0.0120 ± 0.0007 | 0.0156 | 0.77 | +0.0285 |
| MNLI | 10 | +0.0055 ± 0.0006 | 0.0160 | 0.35 | +0.0177 |
| MNLI | 20 | +0.0053 ± 0.0009 | 0.0180 | 0.30 | +0.0173 |
| MNLI | 50 | +0.0058 ± 0.0014 | 0.0200 | 0.29 | +0.0160 |
| SNLI | 5 | +0.0168 ± 0.0011 | 0.0128 | 1.31 | +0.0525 |
| SNLI | 10 | +0.0111 ± 0.0013 | 0.0122 | 0.91 | +0.0413 |
| SNLI | 20 | +0.0103 ± 0.0010 | 0.0135 | 0.77 | +0.0355 |
| SNLI | 50 | +0.0084 ± 0.0010 | 0.0156 | 0.54 | +0.0318 |

αNLI (K = 2): the modal mass fixes the histogram, the oracle shape gap is 0 and pzc − soft is ±0.003 (no shape exists to scramble; not part of the claim).
**Reading (as frozen):** (i) Brier pzc − soft is positive at every m on MNLI and SNLI, so the draft sentence stands in Brier, unrestricted. (ii) The scramble costs 0.29–1.31 of the oracle shape gap. A ratio above 1 is possible because the oracle uses the noisy m-rating histogram of the item itself, while the head pools across items.
