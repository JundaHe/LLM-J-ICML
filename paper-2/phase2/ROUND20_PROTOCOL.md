# ROUND20 protocol — response to Codex round 20 (reviews/codex_round20_2026-11-06.md)
Every analysis below is specified before it is run. Amendments made after seeing results are labelled as such. Post-hoc changes of an estimand are called amendments that *change the estimand*, never "readings as frozen" (review §2 on R19-8a).

## R20-1 Decoding against the other panel's own shape (review issue 1, CRITICAL) — specified 2026-11-06 02:55, before any run
**Estimands.** In each direction, q1 is panel 1's exact comparator (as now), q2 is panel 2's own exact comparator (same folds), s2 = C(h2 − q2) and d = C(q2 − q1). The decoded residual r̂ (unchanged ridge pipeline) gives:
- G = G_own + G_cross,
- G_own = (2⟨r̂, s2⟩ − ‖r̂‖²)/n, the gain against the other panel's own shape,
- G_cross = 2⟨r̂, d⟩/n,
- with X_own and X_cross as in R19-1.

All inner products are NRM-normalised. The *shape-recovery fraction* is G_own/X_own. G/X is renamed the "normalised forecasting gain".
**Valid forecasts, separately (replaces the R19-8a max-combination).** Two quantities, each with its own paired interval:
- GP = score(q1) − score(q*), the gain of the cell-projected valid forecast over the comparator (R19-8 projection);
- ΔGP = GP − GP_perm, the projected real forecast against the projected within-cell-permuted forecast (R19-8a).

The draft's "bounds" become the 95 % upper bounds of one named estimand. No maximum over different estimands is taken.
**Uncertainty.** The item-cluster bootstrap of decode_residual.py: B = 200, R_boot = 3, α fixed at the point-estimate choice, all quantities computed on the same replicates (paired). Point estimates use R = 10.
**Panels.** Qwen2.5 E_last, d = 64, each panel's Table 2 a. The eight informative ordinal panels: SummEval coherence and relevance, POPQUORN offensiveness, EmoBank, DICES-350, DICES-990, Dorn, HS2. Plus ChaosNLI MNLI and SNLI. Plus the planted SummEval and POPQUORN γ ∈ {0, 0.6} (seed 0) as null and positive checks.
**Readings (fixed now).**
(i) Null: at γ = 0 the intervals of G_own and ΔGP cover 0.
(ii) Where the X_own interval excludes 0, G_own/X_own with its interval is the headline decoding estimand. Elsewhere G_own is reported in absolute units only and the panel is described as having no detectable shape-to-shape reproducibility at that a.
(iii) The ordinal–NLI contrast is stated on G_own/X_own: it holds if each NLI lower bound exceeds every ordinal upper bound among the panels in (ii). Otherwise the contrast is reported per panel, without a summary claim.
(iv) Abstract and §1 numbers are replaced by the (ii)/(iii) quantities and the 95 % upper bounds of ΔGP/X_own (labelled as valid-forecast contrasts). The R19-8a maximum rule is withdrawn.
Script `decode_decomp.py`; output results/decode_decomp/<panel>[tag].json.

## R20-2 Planted control: more draws and directions (review issue 4) — specified 2026-11-06 02:55, before any run
The R19-2 construction plants log-dispersion linear in one feature direction. It is renamed a *dispersion plant* everywhere; "known linear shape" and "ceiling" are withdrawn.
**Runs.** SummEval and POPQUORN, γ ∈ {0, 0.3, 0.6}, plant seeds 1–4, each giving an independent direction and simulation, ridge decoder, R = 10, B = 200. Seed 0 already exists. A run uses decode_decomp.py so that G_own is available.
**Readings (fixed now).** Across the five seeds, report the range of G_own/X_own at γ 0.6 and the number of seeds with G_own lower bound > 0 at each γ. The detection threshold is stated as "detected in k of 5 draws". The real-data null on a panel is called informative at its observed X only if, at the γ whose planted X is closest to (and not below) the observed X, ≥ 4 of 5 draws detect.

## R20-T Text-only corrections (review issues 3, 5, 6, 8, 10 and new 3, 5, 6, 7)
- Remove or qualify: "matches" / "equally good" / "tie" (until R19-9), "never the better buy", "mostly not in the text", "learn location and calibration", and "small but non-zero" for the dense panels.
- §7: state the nonlinear probe's actual scope.
- Rater-population statement per panel. SummEval mixes persistent experts with anonymous crowd positions; Scalabrino; the assumption behind "new raters".
- R19-6's frozen threshold supports only "below the ½ forecasting threshold". It does not support "< 0.3".
- Structural-zero statement with scale and tie rule (z_label), §6.
- Inventory: MultiPref status, Dorn's ρ_own lower endpoint, outward rounding of upper bounds, "−0.0000", draft date.
- The αNLI sham contrast: report the optimisation variation it reveals.
- Disclose R19-8's failed control and R19-8a's post-hoc status in §2.2.

### R20-T note on the αNLI sham (2026-11-06; descriptive)
With K = 2 the donor replacement cannot change any target, so pzc − soft on αNLI is a pure sham contrast. Its mean over the 9 configurations is +0.0001 / −0.0033 / +0.0015 / +0.0005 Brier at m = 5 / 10 / 20 / 50, i.e. within about one SEM of 0. The per-configuration SD is 0.005–0.014.
The reason: every arm draws its own initialisation and minibatch order from the run's RNG stream, so optimisation noise is not matched across arms. The sham shows the size of that unmatched noise. The MNLI / SNLI contrasts (+0.005 to +0.017, SEM 0.0006–0.0014) are averages over the same 9 configurations and exceed their SEMs by 4–15×, but single configurations should not be compared.

### R20-1 interim results (2026-11-06 04:45; 9 of 14 runs final, B = 200)
| run | a | X_own [95 %] | G_own/X_own [95 %] | ΔGP/X_own upper |
|---|---|---|---|---|
| SummEval coherence | 4 | 0.00038 [0.00022, 0.00050] | 0.009 [−0.026, 0.022] | 0.051 |
| SummEval relevance | 4 | 0.00031 [0.00019, 0.00044] | 0.013 [−0.098, 0.011] | 0.128 |
| DICES-350 | 20 | 0.00004 [−0.00002, 0.00011] | — (X_own covers 0) | — |
| DICES-990 | 20 | 0.00002 [−0.00001, 0.00005] | — | — |
| POPQUORN off. | 4 | −0.00001 [−0.00017, 0.00009] | — | — |
| plant γ0.6 SummEval | 4 | 0.00040 [0.00030, 0.00058] | 0.56 [0.39, 0.72] | — |
| plant γ0.6 POPQUORN | 4 | 0.00033 [0.00021, 0.00048] | 0.36 [0.15, 0.47] | — |

Reading (i): ΔGP covers 0 at γ 0 on both panels. G_own covers 0 on SummEval [−8.2e−6, +2.1e−8], but on POPQUORN its interval [−9.4e−6, −1.9e−8] misses 0 by 2e−8, on the conservative (negative) side. Strictly, (i) fails for POPQUORN G_own. The failure is negligible in size and in the direction that cannot manufacture a positive decoding gain.
Reading (ii): only SummEval coherence and relevance qualify so far. DICES-350, DICES-990 and POPQUORN are reported as G_own in absolute units, each "no detectable shape-to-shape reproducibility at that a". Dorn, EmoBank, HS2, MNLI and SNLI are pending (point estimates: Dorn 0.10, MNLI 0.28, EmoBank and HS2 X_own ≈ 0).

**Post-hoc observations (not frozen; reported as such).**
1. *Null bias of X_own.* At γ 0, X_own is −0.00011 [−0.00019, −0.00002] on SummEval and −0.00010 [−0.00020, +0.00003] on POPQUORN. Each half's residual is taken against its own cross-fitted (mode, mean) cell. With a ≠ b, the two halves' conditional-mean errors need not have the same sign, so E[X_own] is not 0 even when the shape is fully cell-determined. Consequences:
   - the real SummEval X_own (0.00038) is understated rather than inflated;
   - the "X_own covers 0" readings are, if anything, conservative about absence.
2. *The G_own bootstrap is not centred on the point estimate* (corrected 05:40: the direction is not uniformly downward — EmoBank's point −4.3e−6 lies below its interval [−3.1e−6, −1.8e−6]). Original text: Point estimates sit near or above the upper percentile (SummEval relevance 4.0e−6 vs an upper bound of 3.4e−6). Item resampling keeps duplicates in one fold, which reduces the number of distinct items while α stays fixed at its rep-0 value. The decoder's prediction variance rises, so −‖r̂‖² rises. The percentile interval therefore has a downward-shifted centre. It stays the frozen interval; for G_own and ratios built on G_own, the paper uses the point estimate and the upper bound only.

### R20-1 readings (2026-11-06 05:40; 13 of 14 runs final, HS2 re-running after a ci() crash)
Crash: on HS2 (a = 3) X_own ≤ 1e−9 in every bootstrap resample, so all ratios were NaN and fr_lib.ci received an empty list. ci now returns NaN for an empty list. The fix does not change any other result.

| panel | a | X_own [95 %] | G_own/X_own pt (upper) | ΔGP/X_own [95 %] |
|---|---|---|---|---|
| SummEval coherence | 4 | 0.00038 [0.00022, 0.00050] | 0.009 (0.022) | 0.012 [−0.009, 0.051] |
| SummEval relevance | 4 | 0.00031 [0.00019, 0.00044] | 0.013 (0.011) | 0.027 [−0.042, 0.128] |
| Dorn (all) | 20 | 0.00027 [0.00014, 0.00033] | 0.10 (0.18) | 0.11 [0.005, 0.27] |
| ChaosNLI MNLI | 20 | 0.0111 [0.0102, 0.0122] | 0.28 [0.20, 0.30] | 0.59 [0.49, 0.65] |
| ChaosNLI SNLI | 20 | 0.0112 [0.0100, 0.0122] | 0.38 [0.30, 0.40] | 0.65 [0.56, 0.70] |
| EmoBank | 3 | 2.3e−6 [−5e−7, 7.8e−6] | — | G_own −4e−6, ΔGP 7.5e−6 [1.7e−6, 1.5e−5] |
| DICES-350 / DICES-990 / POPQUORN | 20 / 20 / 4 | cover 0 | — | G_own ≤ 5e−6 in absolute terms |

(ii) Headline panels: SummEval ×2, Dorn, MNLI, SNLI. The others: no detectable shape-to-shape reproducibility at that a.
(iii) The ordinal–NLI contrast **holds**: the NLI lower bounds (0.199, 0.296) exceed every ordinal upper bound (0.022, 0.011, 0.181). The margin is narrow on Dorn (0.199 vs 0.181). With the bootstrap-centring caveat (post-hoc note 2), this is reported as a frozen-rule pass, not as a robust separation.
(iv) The text quantities are the G_own/X_own points and upper bounds above, plus ΔGP/X_own upper bounds of 0.05 / 0.13 / 0.27 (ordinal) vs 0.65 / 0.70 (NLI). Dorn's ΔGP lower bound is > 0, a small detectable valid-forecast gain. The R19-8a max rule is withdrawn from the text.
Panels not run in R20-1 (BW, CSC, Scalabrino, HS2 until it finishes) keep only their R19 G values, labelled as G/X with the cross-term caveat.

## R20-3 OLMo-2 replication of the prospective LoRA block (specified 2026-11-06 07:00, after R19-9's results, before any run)
**Why.** R19-9 overturned the shared-assignment null: 960 × 1 − full = +0.0064 [+0.0045, +0.0085] on Qwen2.5, carried by three of nine cells. We need to know whether the penalty is base-specific and whether the bad cells come from the *rating assignment* (shared across bases) or from optimisation.
**Design.** As R19-9 (SummEval coherence, Chen objective, 240 steps, folds 0–2, split 0, designs full / 960 × 1 / 144 × 7, seeds 2003–2005), but with base allenai/OLMo-2-1124-7B-Instruct. The budget seeds are the **same** as R19-9 (6000 + 100·(seed − 2003) + fold), so every cell sees R19-9's items and ratings. Output: results/lora_budget_r20_olmo/summeval_coherence8/.
**Readings (fixed now).** (i)–(iii) as R19-9 with δ = 0.005, via `analysis_budget_lora.py --root lora_budget_r20_olmo --seeds 2003,2004,2005 --B 2000` (and `--ref a1_F1.0`). (iv) Descriptive only: the per-cell 960 × 1 − full penalties are compared across bases (Pearson r over the nine cells). If the three R19-9 outlier cells are also the three largest here, the outliers are attributed to the assignment, not to optimisation.
The draft reports both bases. No claim is upgraded on one base alone.

### R20-2 results, SummEval coherence (2026-11-06 07:40; draws s0 from R20-1 plus s1–s4)
| γ | draws | detected (G_own lower bound > 0) | planted X | planted X_own | G_own/X_own |
|---|---|---|---|---|---|
| 0 | 5 | 0 of 5 (ΔGP covers 0 in 5 of 5) | −0.00017 to +0.00006 | −0.00014 to −0.00005 | — |
| 0.3 | 4 (s1–s4; no s0) | 3 of 4 | 0.00040–0.00064 | 0.00012–0.00022 | 0.16–0.55 |
| 0.6 | 5 | 5 of 5 | 0.00133–0.00166 | 0.00033–0.00047 | 0.38–0.56 |
Observed: X = 0.00198, X_own = 0.00038.

**Reading as frozen (on X): not met.** No γ has planted X at or above the observed X, because the strongest plant reaches 0.00166. The frozen rule therefore cannot certify the SummEval null as informative.
**Post hoc, on the X_own scale used by the R20-1 headline:** the γ0.6 draws bracket the observed X_own (0.00033–0.00047 vs 0.00038) and are detected 5 of 5. γ0.3, at about half the observed X_own, is detected 3 of 4.
The draft states the frozen outcome first, then the X_own reading labelled post hoc. The monotonicity argument (a stronger plant would be detected at least as often) is reasoning, not a test. POPQUORN plant draws are still running.
