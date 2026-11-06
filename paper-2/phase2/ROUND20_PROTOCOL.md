# ROUND20 protocol — response to Codex round 20 (reviews/codex_round20_2026-11-06.md)
Every analysis below is specified before it is run. Amendments made after seeing results are labelled as such. Post-hoc changes of an estimand are called amendments that *change the estimand*, never "readings as frozen" (review §2 on R19-8a).

## R20-1 Decoding against the other panel's own shape (review issue 1, CRITICAL) — specified 2026-11-06 02:54, before any run
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

## R20-2 Planted control: more draws and directions (review issue 4) — specified 2026-11-06 02:54, before any run
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

### R20-1 interim results (2026-11-06 04:32; 9 of 14 runs final, B = 200)
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

### R20-1 readings (2026-11-06 05:32; 13 of 14 runs final, HS2 re-running after a ci() crash)
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

## R20-3 OLMo-2 replication of the prospective LoRA block (specified 2026-11-06 06:34, after R19-9's results, before any run)
**Why.** R19-9 overturned the shared-assignment null: 960 × 1 − full = +0.0064 [+0.0045, +0.0085] on Qwen2.5, carried by three of nine cells. We need to know whether the penalty is base-specific and whether the bad cells come from the *rating assignment* (shared across bases) or from optimisation.
**Design.** As R19-9 (SummEval coherence, Chen objective, 240 steps, folds 0–2, split 0, designs full / 960 × 1 / 144 × 7, seeds 2003–2005), but with base allenai/OLMo-2-1124-7B-Instruct. The budget seeds are the **same** as R19-9 (6000 + 100·(seed − 2003) + fold), so every cell sees R19-9's items and ratings. Output: results/lora_budget_r20_olmo/summeval_coherence8/.
**Readings (fixed now).** (i)–(iii) as R19-9 with δ = 0.005, via `analysis_budget_lora.py --root lora_budget_r20_olmo --seeds 2003,2004,2005 --B 2000` (and `--ref a1_F1.0`). (iv) Descriptive only: the per-cell 960 × 1 − full penalties are compared across bases (Pearson r over the nine cells). If the three R19-9 outlier cells are also the three largest here, the outliers are attributed to the assignment, not to optimisation.
The draft reports both bases. No claim is upgraded on one base alone.

### R20-2 results, SummEval coherence (2026-11-06 07:31; draws s0 from R20-1 plus s1–s4)
| γ | draws | detected (G_own lower bound > 0) | planted X | planted X_own | G_own/X_own |
|---|---|---|---|---|---|
| 0 | 5 | 0 of 5 (ΔGP covers 0 in 5 of 5) | −0.00017 to +0.00006 | −0.00014 to −0.00005 | — |
| 0.3 | 4 (s1–s4; no s0) | 3 of 4 | 0.00040–0.00064 | 0.00012–0.00022 | 0.16–0.55 |
| 0.6 | 5 | 5 of 5 | 0.00133–0.00166 | 0.00033–0.00047 | 0.38–0.56 |
Observed: X = 0.00198, X_own = 0.00038.

**Reading as frozen (on X): not met.** No γ has planted X at or above the observed X, because the strongest plant reaches 0.00166. The frozen rule therefore cannot certify the SummEval null as informative.
**Post hoc, on the X_own scale used by the R20-1 headline:** the γ0.6 draws bracket the observed X_own (0.00033–0.00047 vs 0.00038) and are detected 5 of 5. γ0.3, at about half the observed X_own, is detected 3 of 4.
The draft states the frozen outcome first, then the X_own reading labelled post hoc. The monotonicity argument (a stronger plant would be detected at least as often) is reasoning, not a test. POPQUORN plant draws are still running.

### R20-2a Stronger plant so the frozen X-scale rule can be evaluated (amendment, specified 2026-11-06 07:32 after seeing R20-2's SummEval results)
**Why.** The R20-2 rule requires a γ whose planted X is at or above the observed X (0.00198). The γ grid {0, 0.3, 0.6} tops out at X = 0.00166.
**Design.** Add γ = 0.8 on SummEval coherence, draws s0–s4, a = 4, with otherwise identical settings (R = 10, B = 200, R_boot = 3).
**Reading.** The R20-2 rule is applied unchanged to the grid {0.3, 0.6, 0.8}. If γ 0.8 still falls short of the observed X, the rule is reported as not evaluable. This is an amendment written after the results it addresses and is labelled as such in the draft.

### R20-1 final panel (HS2) and a note on ΔGP (2026-11-06 08:31)
**HS2 (a = 3, b = 2):** X_own = 0 exactly in the point estimate and in all 200 resamples. Two ratings are determined by their exact (mode, mean) cell (z_label tie rule), so s2 ≡ 0. HS2's own-shape is therefore *structurally unmeasurable* at b = 2, not "not detected". G_own = −‖r̂‖²/n = −4.6e−6 is the decoder's variance penalty. Under (ii), HS2 is reported as unmeasurable.
**ΔGP is not an own-shape quantity (post hoc).** HS2 has ΔGP = +1.5e−5 [+1.2e−5, +3.1e−5], and EmoBank has +7.5e−6 [+1.7e−6, +1.5e−5], both with X_own ≈ 0. The projected-forecast gain is scored against h2 itself, so it includes the cross part: panel 2's within-cell location shift predicted from text. ΔGP/X_own is therefore a valid-forecast gain on the X_own scale, not a fraction of the own-shape, and can exceed 1. The draft labels it that way. The ordinal–NLI contrast (iii) rests on G_own/X_own alone.
**R20-2 POPQUORN (interim).** γ0: 0 of 5 detected, ΔGP covers 0 in 5 of 5. Observed X = 0.00036, so the rule's reference is γ0.3 (planted X 0.00073). So far 1 draw, not detected on G_own (lower bound −1.1e−5), ΔGP > 0.

### R20-2 POPQUORN readings (2026-11-06 09:31)
| γ | draws | detected | planted X | G_own/X_own |
|---|---|---|---|---|
| 0 | 5 | 0 of 5 (ΔGP covers 0 in 5 of 5) | 0.00010–0.00030 | — |
| 0.3 | 4 (s1–s4) | **0 of 4** | 0.00037–0.00074 | −0.02 to 0.30 |
| 0.6 | 2 so far | 2 of 2 | 0.00148–0.00190 | 0.25–0.36 |
Observed X = 0.00036. The reference γ under the rule is 0.3, and it is detected 0 of 4, so **the POPQUORN null is uninformative** (as frozen).
*Protocol defect (recorded):* R20-2 specified seeds 1–4, plus the R20-1 s0 draws, which exist only at γ 0 and 0.6. γ 0.3 therefore has 4 draws, and "≥ 4 of 5" is read as "≥ 4 of the available draws". This changes nothing here (0 of 4; SummEval 3 of 4 at γ 0.3, where γ 0.3 is not the reference).

## R20-4 POPQUORN prospective LoRA block with independent assignments (specified 2026-11-06 09:31, before any run)
**Why.** R19-9 showed that SummEval's shared-assignment block understated the single-rating penalty. POPQUORN's three budget readings (SHRINKAGE Amendment 7) also come from a block whose seeds share one assignment per fold.
**Design.** As Amendment 7 (popquorn_off8, Qwen2.5-7B-Instruct, Chen objective, 2 epochs / 205 steps, folds 0–2, split 0). Designs: full, 819 × 1, 819 × 2, 117 × 7. Seeds 2003–2005, `--budget_seed 7000 + 100·(seed − 2003) + fold`. Output: results/lora_budget_r20_pq/popquorn_off8/.
**Readings (fixed now).** Crossed bootstrap B = 2000 (`analysis_budget_lora.py --panel popquorn_off8 --root lora_budget_r20_pq --seeds 2003,2004,2005`, plus `--ref a1_F1.0`):
(i) a single rating is worse: 819 × 1 − full has a 95 % lower bound > 0;
(ii) a second rating helps: 819 × 2 − 819 × 1 has a 95 % upper bound < 0;
(iii) items first: 117 × 7 − 819 × 1 has a 95 % lower bound > 0.
Each reading is reported as it comes out. Where it differs from Amendment 7, the prospective block is the one the draft states, and the shared-assignment block is described as such.

### R20-3 results (2026-11-06 10:31; 27/27; results/lora_budget_r20_olmo/summary*.json)
| contrast (OLMo-2) | point | 90 % | 95 % | Qwen2.5 (R19-9) |
|---|---|---|---|---|
| 960 × 1 − full | **+0.0066** | [+0.0049, +0.0084] | [+0.0044, +0.0089] | +0.0064 [+0.0045, +0.0085] |
| 144 × 7 − full | +0.0126 | — | [+0.0058, +0.0197] | +0.0166 |
| 144 × 7 − 960 × 1 | +0.0060 | — | [−0.0007, +0.0128] | +0.0102 [+0.0052, +0.0157] |
(i) Equivalence fails. (ii) Non-inferiority fails, so the single-rating penalty replicates on a second base at almost the same size. (iii) Items-first **does not hold** on OLMo-2 (the interval covers 0, with the point favouring items). It holds on Qwen2.5.
(iv) Per-cell 960 × 1 − full across bases: Pearson r = 0.56 over 9 cells. The three largest cells overlap in 2 of 3 (s2003 f1 and s2004 f2 are shared), so per the rule the outliers are **not** attributed to the assignment alone. On OLMo-2 the penalty is positive in all 9 cells (+0.0003 to +0.0121), so the result does not rest on the collapsed Qwen run.
Draft consequence: "one rating per item is worse than the full data by about 0.006 RPS on both bases". The items-first statement at matched budget is restricted to "on Qwen2.5; on OLMo-2 the direction agrees but the interval covers 0". The earlier shared-assignment OLMo block (+0.0095 [+0.0022, +0.0160]) is described as such.

### R20-2b Completing the γ 0.3 draws (2026-11-06 10:32, amendment after R20-2 results)
Run s0 at γ 0.3 on SummEval coherence and POPQUORN, so that every γ has the five draws R20-2 intended. The rule is unchanged. The outcome cannot reverse POPQUORN (0 of 4 already), and on SummEval γ 0.3 is not the reference γ, so this completes the record without changing any reading.

### R20-4 results (2026-11-06 11:32; 36/36; results/lora_budget_r20_pq/summary*.json)
| contrast (POPQUORN, Qwen2.5) | prospective [95 %] | Amendment 7 (shared assignment) |
|---|---|---|
| 819 × 1 − full | +0.0063 [+0.0030, +0.0099] | +0.0087 [+0.0054, +0.0122] |
| 819 × 2 − 819 × 1 | −0.0031 [−0.0062, −0.0002] | −0.0054 [−0.0084, −0.0027] |
| 117 × 7 − 819 × 1 | +0.0027 [−0.0024, +0.0074] | +0.0022 [−0.0029, +0.0072] |
(i) **Holds.** (ii) **Holds**: a second rating recovers 49 % of the single-rating gap (62 % before). (iii) **Does not hold.** All three readings agree with Amendment 7.
Across the three prospective blocks, the single-rating penalty is +0.0063 to +0.0066 RPS (SummEval Qwen2.5 and OLMo-2, POPQUORN Qwen2.5). Items-first at matched budget holds in one of three (SummEval Qwen2.5).

### R20-2a reading (γ 0.8, SummEval; 2026-11-06 11:32)
Detected in 5 of 5 draws (G_own lower bound 0.00008–0.00022, G_own/X_own 0.33–0.50). The planted X is 0.00176–0.00222, with mean 0.001976 against the observed 0.001984 (0.4 % short; 2 of 5 draws above). Strictly, the mean does not reach the observed X, so the rule is applied once more with γ 1.0 (R20-2c, below). The draft states "met in substance at γ 0.8" only together with this detail.

### R20-2c γ 1.0 (amendment, 2026-11-06 11:32)
SummEval coherence, γ 1.0, s0–s4, otherwise as R20-2. Reading: the R20-2 rule on the grid {0.3, 0.6, 0.8, 1.0}, reference = the smallest γ whose mean planted X ≥ the observed X. No further γ will be added. If γ 1.0 also falls short, the rule is reported as not met.

## R20-5 SummEval prospective 960 × 2 (specified 2026-11-06 11:32, before any run)
**Why.** The guidance's "a second rating is worth nothing on SummEval" rests on shared-assignment blocks. The prospective blocks show a single-rating penalty of 0.006.
**Design.** As R19-9 (Qwen2.5, the same seeds 2003–2005 and budget seeds 6000 + 100·(seed − 2003) + fold, folds 0–2), design 960 × 2 (`--train_pos 2 --train_frac 1.0`). Output goes into results/lora_budget_r19/summeval_coherence8/a2_F1.0/, so the full and 960 × 1 cells of R19-9 serve as references.
**Readings (fixed now).** (i) A second rating helps: 960 × 2 − 960 × 1 has a 95 % upper bound < 0. (ii) Two ratings suffice within the margin: 960 × 2 − full has a 95 % upper bound < 0.005. Both are reported as they come out.

### R20-2 final readings (2026-11-06 12:31; R20-2a/b/c complete)
| panel | γ | draws | detected | mean planted X | G_own/X_own |
|---|---|---|---|---|---|
| SummEval | 0 | 5 | 0 of 5 | −0.00008 | — |
| SummEval | 0.3 | 5 | 4 of 5 | 0.00055 | 0.16–0.55 |
| SummEval | 0.6 | 5 | 5 of 5 | 0.00147 | 0.38–0.56 |
| SummEval | 0.8 | 5 | 5 of 5 | 0.00198 (−0.4 %) | 0.33–0.50 |
| SummEval | **1.0** | 5 | **5 of 5** | **0.00225** | 0.31–0.57 |
| POPQUORN | 0 | 5 | 0 of 5 | 0.00019 | — |
| POPQUORN | **0.3** | 5 | **0 of 5** | 0.00062 | −0.02 to 0.34 |
| POPQUORN | 0.6 | 2 | 2 of 2 | 0.00169 | 0.25–0.36 |
**Readings.**
- **SummEval:** the reference γ (the smallest with mean planted X ≥ observed 0.00198) is 1.0, detected 5 of 5, so the SummEval null **is informative** under the rule, with the amendments R20-2a/c disclosed.
- **POPQUORN:** the reference γ is 0.3, detected 0 of 5, so its null is **uninformative**.
- **Descriptive:** planted X_own saturates at about 0.0004–0.0005 from γ 0.6 to 1.0, while the planted X grows through its cross part. The plant raises dispersion symmetrically and so also moves the location cells. The γ 1.0 plant's own-shape magnitude (0.00041–0.00050) is close to SummEval's observed 0.00038.

### R20-5 results (2026-11-06 13:35; 9/9 runs; results/lora_budget_r19/summary*.json now include a2_F1.0)
| contrast (SummEval, Qwen2.5, R19-9 assignments) | point [95 %] |
|---|---|
| 960 × 2 − 960 × 1 | −0.0105 [−0.0143, −0.0068] |
| 960 × 2 − full | **−0.0040 [−0.0078, −0.0003]** |
- (i) A second rating helps: **holds**.
- (ii) Two ratings suffice within the margin: **holds**. The upper bound is −0.0003, so the point estimate *favours two ratings over seven*.
**Caution.** This is implausible on its face, and the three blocks that have run a two-ratings arm all point this way: the earliest 960 × 2 (−0.0064, cross-batch), the shared-assignment 480 × 2 (−0.0040) and this one (−0.0040). The a2 arm ran about 6 h after the full arm, with the same code, hardware, settings and budget seeds.
**Descriptive checks:**
- the mean predicted SD is 0.94–0.96 in every arm, so sharpness does not explain it;
- experts and crowd differ in location (mean rating 2.41 vs 2.81) and in within-group SD (0.60 vs 0.39);
- the evaluator is a held-out expert, and every design has the same expected expert share, so the mixture alone does not explain a2 < full in expectation.
**R20-5a (specified now, before running): batch reproducibility.** Rerun the full arm for seed 2003, folds 0–2, now, into results/lora_budget_r20_rerun/. If P_test matches R19-9 to within 1e−4 RPS per cell, batch effects are excluded and the result stands as observed. Otherwise the cross-batch comparison is reported as unreliable, and full and a2 are rerun in one batch before any claim.
R20-5a addendum (13:35, before running): the a2 arm for seed 2003 is also rerun on the second GPU (same rule, same output root).

### R20-5a results (2026-11-06 14:33; seed 2003, both arms rerun, 6/6 cells)
- **Frozen criterion: fails.** Items are identical, but P_test differs from the R19-9/R20-5 cells by up to 0.05–0.11 in probability per item. Training on this GPU is not bit-reproducible (nondeterministic kernels), so the 1e−4 threshold was unattainable. *Post hoc:* that threshold was mis-set. A tolerance at the scale of run-to-run noise should have been specified.
- Descriptive (not a frozen reading):
  - Per-cell mean RPS moves by −0.0011 to +0.0002 (full) and −0.0012 to 0.0000 (a2) between batches.
  - Within one batch, a2 − full per fold:

    | | f0 | f1 | f2 |
    |---|---|---|---|
    | original | +0.0047 | +0.0059 | −0.0106 |
    | rerun | +0.0048 | +0.0045 | −0.0103 |

  - So the seed-2003 contrast reproduces to ≤ 0.0014 per cell, and its sign pattern is fold-specific. Fold 2 (evaluator expert 2) is where two ratings beat seven.
- Per the frozen rule, the cross-batch comparison is reported as unreliable, and the claim waits for a single-batch rerun.

**R20-5b (specified now, before running): single-batch rerun.** Rerun the full and a2 arms for seeds 2004 and 2005, folds 0–2, into results/lora_budget_r20_rerun/ (one GPU per arm, both submitted together). Analysis: analysis_budget_lora.py --root lora_budget_r20_rerun --seeds 2003,2004,2005 (reference = the in-root full arm), B = 2000. Readings: the frozen R20-5 readings (i) and (ii), unchanged. R20-5 is reported only from this single-batch set. Descriptive add-on: the a2 − full contrast per evaluator fold, because fold 2 drives the sign (relevant to N11, expert heterogeneity).

### R20-5b results (2026-11-06 15:46; 18/18 cells, results/lora_budget_r20_rerun/summary.json)
- 960 × 2 − full (same batch) = **−0.0034 [−0.0066, −0.0004]**. Reading (ii), two ratings suffice within the margin, **holds**. As in R20-5, the interval lies below 0.
- Per fold: f0 +0.0019, f1 −0.0020, **f2 −0.0099** (the three seeds span −0.0103 to −0.0094). The advantage of two ratings is an expert-2-evaluator effect (R21-6) and is not a batch artefact.
- Reading (i), 960 × 2 vs 960 × 1, cannot be read from a single batch yet, because the a1 arm was not rerun.

**R20-5c (specified now, before running): a1 arm in the same batch.** Rerun 960 × 1 (budget seeds as in R19-9) for seeds 2003–2005, folds 0–2, into results/lora_budget_r20_rerun/. Run analysis_budget_lora.py --root lora_budget_r20_rerun --seeds 2003,2004,2005 --ref a1_F1.0. Reading (i) as frozen in R20-5: a second rating helps if the 95 % upper bound of a2 − a1 is < 0. Reported per fold as well.

### R20-5c results (2026-11-06 16:58; single batch, 27 cells: full, a1 and a2 × seeds 2003–2005 × folds 0–2)
| contrast (same batch) | point [95 %] |
|---|---|
| 960 × 1 − full | +0.0064 [+0.0045, +0.0086] (R19-9 cross-batch: +0.0064 [+0.0045, +0.0085]) |
| 960 × 2 − 960 × 1 | **−0.0098 [−0.0132, −0.0066]** |
| 960 × 2 − full | −0.0034 [−0.0066, −0.0004] |
- (i) A second rating helps: **holds**.
- (ii) Two ratings suffice within the margin: **holds** (see R20-5b).
- Per fold:

  | contrast | f0 | f1 | f2 |
  |---|---|---|---|
  | a1 − full | −0.0013 | +0.0070 | +0.0135 |
  | a2 − full | +0.0019 | −0.0020 | −0.0099 |
  | a2 − a1 (by subtraction) | +0.0032 | −0.0090 | −0.0234 |

- Evaluator expert 0 (mean 2.81, equal to the crowd mean) sees no budget effect. Experts 1 and 2 see a single-rating penalty that a second rating more than removes.
- Final R20-5 statement, as reported: on SummEval/Qwen2.5 a second rating helps, and two ratings are not worse than seven. Both are carried by the two experts whose location differs from the crowd's. The cross-batch R20-5 values (−0.0105, −0.0040) agree with the single-batch values to within 0.0007.
