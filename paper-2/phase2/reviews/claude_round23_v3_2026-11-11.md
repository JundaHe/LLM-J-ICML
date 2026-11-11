**Claude-subagent adversarial review (round 23, PAPER_ICML_v3.md), standing in for the external Codex review, which is unavailable until later. It follows reviews/codex_round22_prompt_2026-11-10.md items 1–6, plus the authors' proposed per-matched-rater-count reporting of the NLI–ordinal margin.**

Date: 2026-11-11. Inputs: PAPER_ICML_v3.md (as embedded in the prompt), ROUND21/ROUND22_PROTOCOL.md, PROGRESS.md, reviews/codex_round20_2026-11-06.md, reviews/percent_audit_v3_2026-11-07.md, latex_v3/tab_*.tex, and the artefacts under results/. Every number in the "verified" table at the end was recomputed with /scratch/jundahe/venvs/llmj/bin/python from results/. No file other than this one was modified.

---

## Verdict (summary)

**Weak reject.** The audit trail is exemplary, and most of the round-20 estimand problems are repaired. However, the paper's flagship "clean ordinal case" claim, that on DICES-350 "the real one is not [decoded]", is contradicted by the paper's own prespecified, null-calibrated statistic. ⟨r̂, s₂⟩/n (V_own) is significantly positive on DICES-350 at a = 40 for **all three** feature families. It is about 10× its location-only null, and the main text never reports it. Two further problems compound this. The headline ratio G_own/X_own recovers only 15–33 % even of a planted shape that is an exact linear function of the decoder's inputs, so it is not a "fraction of the shape that is in the text" and cannot be compared across panels with different n and SNR. And the nominal "shape beyond location" (the split of mass among non-modal classes) is a different kind of object from the ordinal one (dispersion at fixed mean), which confounds the headline NLI–ordinal contrast by construction. The proposed "25 % vs 16 % / 19 % vs 3 %" matched-count reporting is **not acceptable as written**; see §3b.

---

## 1. Status of the round-20 issues

| # | Round-20 issue | Status | Evidence / what remains |
|---|---|---|---|
| 1 | CRITICAL: decoding inherits the cross-term (G/X is not a shape fraction) | **Largely resolved; a new, deeper problem is exposed** | G_own/X_own with s₂ = C(h₂ − q₂) removes the cross-term from both numerator and denominator (§4, Appendix A.2). But the ratio is still read as "the fraction … of the reproducible own-shape" (§1, §4) and "a quarter to two-fifths of it is decodable" (Conclusion). The DICES plant shows that a shape that is *entirely* a linear function of the decoder's features is recovered at only 15–33 %. The ratio is therefore an attenuated, n- and SNR-dependent estimator output, not a fraction of the shape that is predictable from the text. See new issue C2. |
| 2 | HIGH: the "bounds" mixed estimands and had no coverage | **Mostly resolved** | Item-cluster CLT intervals with delta-method ratios (R21-1) replace the max-of-two-estimands construction. Residuals: (a) the coverage check is 9 of 10 null draws, which a 70–80 %-coverage procedure also passes with probability 0.15–0.38, and the draws are only at a = 4 on SummEval/POPQUORN, not in the a = 40 or NLI regimes where the headline lives. (b) The CLT treats the cross-fitted decoder as fixed. (c) The valid-forecast gain in §4 *Robustness* ("≤ 6·10⁻⁵ RPS … against 0.0065 and 0.0072") is still a point estimate without an interval and is Qwen2.5-only; say so in the sentence. |
| 3 | HIGH: inconsistent rater population | **Partly** | SummEval is now explicitly mixed, crossed bootstraps are given for BW/DICES-350, and the pool bias is explained (R21-2). But the consequence is under-stated: with rater resampling, ρ_own for DICES-350 includes 0 ([−0.02, 0.19]). The "clean case" own-shape therefore exists only for these 104 people, and every DICES-350 decoding interval also conditions on them. DICES-990's crossed interval is still only at a = 10, and its *item-level* ρ_own interval at 40 already includes 0 ([−0.002, 0.139]), which §3's "with rater resampling the BW and DICES-350 intervals include 0" omits. |
| 4 | HIGH: the plant is not a general power calibration | **Partly** | There are now 5 draws, X_own-matched references, a frozen detection rule, and a second construction whose adverse result was reported honestly. Still: one random direction that lies *in the decoder's own PCA input space* (the most favourable alternative a linear decoder can face); no plant in which only *part* of the shape is text-predictable; no NLI plant; and 5/5 vs 3/5 detections are statistically indistinguishable (Clopper–Pearson 95 % lower bound for 5/5 is 0.48; the 3/5 interval is [0.15, 0.95]). See §3a. |
| 5 | MEDIUM: αNLI sham contrast | **Partly (disclosed, not fixed)** | Now attributed to unmatched optimisation noise (per-config SD up to 0.014), with only nine-configuration averages interpreted. A matched-initialisation rerun was not done. Acceptable for an appendix. |
| 6 | MEDIUM: nonlinear limitation contradicted the analysis | **Resolved in wording, but the analysis is pointless where it was run** | §7 now says "one non-linear probe (on SummEval and POPQUORN only)". After ROUND22, neither panel has a detectable own-shape (SummEval non-dup X_own n.s.; POPQUORN n.s.). The nonlinear probe was therefore tested only where there is nothing to find. Run it on DICES-350 (a = 40) and Dorn. |
| 7 | MEDIUM/LOW: inventory and numbers | **Mostly resolved** | The percentage audit fixed six mismatches; MultiPref is gone from the paper; the Dorn range is 0.12–0.22. Remaining: "+0.0000 [−0.0009, +0.0009]" is still printed (§1 iii, §5); results/ file paths appear in the paper ("results/support_three.json", "results/decoding_v2/" in App. E); internal protocol IDs appear in the main text (see C/H list); and a Table 1 caption error (H6). |
| 8 | (round-20 #8) Structural-zero claims lacked scale/tie definitions | **Partly; still contradicted in Table 1** | The tie rule is now in App. E. But the Table 1 caption still says "Three-rater panels: the mode-and-mean cell determines the histogram (support 0)", and the rows say "-- (no shape)". Both are false for three ratings: §3 itself says "15–75 % of the three-rating histograms share their exact cell with a different histogram". It is the *two-rating half* that is determined. |

---

## 2. Were the frozen readings respected? Are post-hoc amendments disclosed and not used to rescue claims?

**At the protocol level, yes, and admirably.** R21-7 (Dorn uninformative, 1/5), R22-1 (relevance removed from the contrast), R22-4 (POPQUORN stays uninformative) and R22-6 (polarisation 3/5, so the power claim is restricted) are all adverse readings applied as frozen. The R22-6 grid amendment after the smoke run is labelled, it strengthened the plant rather than the claim, and PROGRESS explicitly refuses extra draws after seeing 3/5. That is the right call.

**At the manuscript level, three things undercut this:**

1. **Selective estimand reporting on the flagship panel (see C1).** R21-1 prespecified V_own = ⟨r̂, s₂⟩/n as *the* null-calibrated statistic ("V_own has mean 0 under the null … If ≥ 9 of 10 cover 0, the method is used for the headline"), and the draft uses it to argue Dorn is location-driven. On DICES-350 the same statistic is positive with an interval excluding 0 on every family, and the draft is silent about it. Whatever the intent, the effect is a rescue of "not decoded".
2. **The abstract and Conclusion do not carry the R22-6 restriction.** PROGRESS says "the abstract has no room". Yet the abstract spends a sentence on the plant that worked ("A planted text-predictable dispersion shape of the same magnitude is recovered at 15–33 %"). The Conclusion says, without any construction qualifier, "a planted shape of its size is decoded, and the real one is not". A frozen adverse reading that is reported in §7 but omitted wherever the favourable reading is quoted is not adequately disclosed.
3. **The proposed matched-count reporting of the margin (§3b)** rounds 24.6 % to "25 %" against the paper's own outward-rounding convention. It also resurrects the SummEval full panel, which ROUND22 demoted, as the a = 4 partner. Both choices move in the direction that makes the claim look stronger.

Also note: the abstract's "Accordingly, replacing the shape … changes LoRA judges by at most ±0.0015 RPS" presents as a *consequence* an audit that §5 itself calls "expected rather than discriminating" ("neither panel has a detectable own-shape"). This is not a frozen-reading violation, but it is a framing that the protocol log does not license.

---

## 3. Specific assessments

### 3a. How much does a dispersion-only power calibration weaken the DICES-350 null and the headline?

Substantially, for four reasons. The first and second are, in my view, more serious than the polarisation result itself.

1. **The ratio is attenuated even under the most favourable alternative.** The dispersion plant is an exact log-linear function of a random direction *in the decoder's own 64-dimensional PCA input*. Even so, the decoder recovers only 15–33 % (mean 26 %) of the planted own-shape at the matched magnitude (dd/dices_r22_plant0.4_s*). Calibrated against that ceiling, the observed DICES-350 values become:
   - Qwen2.5: 1.3/26 ≈ 5 %, upper bound 11.4/26 ≈ **44 %**;
   - Qwen3 and OLMo-2: upper bounds ≈ **26–27 %**.

   So "upper bounds ≤ 12 %" in the abstract invites the reading "at most 12 % of the shape is text-predictable", whereas the data exclude only shapes that are mostly (≳ 30–45 %) linear-text-predictable. A null that is informative only against "the entire own-shape is a linear dispersion effect along one feature direction" is a narrow null.
2. **Text signal is in fact detected (C1).** V_own on DICES-350 at a = 40 is 4.9·10⁻⁶ [2.3, 7.5]·10⁻⁶ (Qwen2.5), 2.8·10⁻⁶ [1.0, 4.6]·10⁻⁶ (Qwen3) and 2.3·10⁻⁶ [0.5, 4.1]·10⁻⁶ (OLMo-2). The location-and-threshold simulation gives a mean of 4.7·10⁻⁷ (max 1.05·10⁻⁶ over five draws), and the planted shape gives 2.2·10⁻⁵ on average. The observed covariance is therefore about **23 % of the fully-predictable plant's**. The net-of-penalty ratio tells the same story: 15.0 % [2.6, 27.4] for Qwen2.5 against a plant mean of 59 %, i.e. about 25 %. The correct reading is: *a small, detectable part of DICES-350's own-shape covaries with the text, but a ridge decoder on 350 items cannot turn it into a proper-score gain.* That reading is very different from "the real one is not decoded".
3. **The failed construction is the one the dataset was designed for.** DICES exists to study demographic disagreement on safety, and group polarisation is its natural ordinal shape. The construction that *does* calibrate (item dispersion) is the less domain-relevant one. Polarisation at matched X_own is detected in 3/5 with recovery of 1–22 %, and the observed −1 to 1 % sits at the bottom of that range. Against the most plausible alternative, the paper cannot distinguish "no text-predictable shape" from "polarisation shape of the observed size".
4. **The detection counts carry little statistical weight.** 5/5 means power ≥ 0.48 at 95 % confidence; 3/5 means [0.15, 0.95]. The matched dispersion plant also sits slightly above the observed magnitude (5.5 vs 4.9·10⁻⁵), on a steep power curve (γ = 0.3, at 61 % of the observed X_own, gives 2/5). "5 of 5" is a point on a cliff edge, not a power guarantee.

**Effect on the headline.** The DICES-350 "clean case" should be demoted from "shape exists, power is calibrated, shape not decoded" to: "shape exists within the observed pool; a small text-covarying component is detectable (V_own > 0, three families); the decoder recovers no proper-score gain; and the null excludes only a shape that is largely linear-text-predictable in the dispersion construction." The abstract's DICES sentence and the Conclusion's "we can show both halves directly" must go. **Fix:** (i) report V_own and the net ratio for DICES-350 in §4 and Table 2; (ii) add a *partial-predictability* plant: plant a text-predictable fraction π ∈ {0.25, 0.5, 0.75} of the matched X_own, with the remainder rater-side, and report the minimum detectable π at ≥ 80 % power with ≥ 20 draws; (iii) report plant-normalised ("calibrated") recovery beside the raw ratio. All of these should be prespecified as R23 items.

### 3b. "Every NLI lower bound exceeds every ordinal upper bound" (18 % vs 16 %), and the proposed per-matched-count reporting

**Recommendation: drop it as a headline sentence and replace it with matched-a difference estimates. The authors' proposed matched-count numbers are not acceptable as written.**

Recomputed from dd/*_r21.json:

| raters/half | smallest NLI lower bound | largest ordinal upper bound (X_own detectable) | comment |
|---|---|---|---|
| 20 | MNLI Qwen2.5 **24.64 %** → 24 (outward), not 25 | Dorn (all) 15.86 → 16; Dorn Java 15.45; DICES-350 7.05 | Dorn is the binding partner, and the paper says its *decodable* signal is location-sized (V_own ≈ 96 % of the location-only simulation) |
| 4 | MNLI **18.65 %** → 18 (outward), not 19 | only SummEval **full panel** (coh. 2.00, rel. 2.50 → "3") | the paper's own App. B says "no ordinal panel offers a like-for-like partner at four raters … once SummEval's duplicated items are set aside" |
| 40 | **no NLI run** | DICES-350 11.4 (three-family max) | the flagship ordinal panel has no matched NLI partner |

Specific objections to "25 % vs 16 % at 20 and 19 % vs 3 % at 4":

- **Rounding.** The paper rounds every interval outward (percent audit; Table 2 prints "28 % [24, 33]"). Printing 25 and 19 breaks that convention in the claim's favour and contradicts the "[24, 33]" two lines away. Use 24 and 18.
- **The a = 4 ordinal partner is the artefact ROUND22 removed.** SummEval's full-panel X_own "is carried by the duplicated annotations" (App. C). Reinstating it as the ordinal side of a matched contrast directly contradicts App. B's "no ordinal panel offers a like-for-like partner at four raters". At a = 4 the correct entry is "no ordinal partner (SummEval non-dup., POPQUORN: X_own n.s.)". The a = 4 NLI values are a robustness check that the NLI fractions do not need 20 raters, which is how App. B already describes them.
- **No matched partner at 40.** DICES-350, the clean case, is at a = 40/20; ChaosNLI (≈ 100 raters) was decoded only at 20/20 and 4/4. ChaosNLI at 40/20 is a cheap CPU run and should be prespecified.
- **Bound non-overlap is the wrong statistic.** Non-overlap of two marginal intervals is neither a test nor an effect size, and the "smallest margin" is dominated by whichever panel has the widest interval. Report the matched-a difference with its interval (the panels are independent, so the variances add). At a = 20: MNLI − Dorn (all) = **18.2 pp [11.4, 25.0]**; MNLI − DICES-350 = **36.3 pp [20.8, 51.8]**. These are compelling and need no "every … every" rhetoric. With difference estimates, the 18-vs-16 question disappears.

**Is per-matched-count reporting acceptable as a labelled post-hoc reporting change?** Yes, *in principle*. It changes presentation, not data or tests, and matched-a is the scientifically correct comparison (R21-3 already prespecified matched-a = 4 reporting). It is acceptable **only if** (i) R21-1(i)'s frozen pooled reading is kept in the appendix verbatim; (ii) the outward-rounding convention is applied (24, 18); (iii) the a = 4 row says "no valid ordinal partner" rather than citing the SummEval full panel; (iv) the a = 40 gap is acknowledged, or filled by a prespecified run; and (v) it is labelled "post-hoc reporting change made after the percentage audit narrowed the pooled margin". As proposed, it fails (ii) and (iii) and would read as a rescue.

**A deeper problem with the contrast (H1):** the nominal and ordinal "shapes" are different objects. See H1 below.

### 3c. Is the 8-page main text self-contained for the DICES-350 vs NLI contrast and the POPQUORN budget result?

**Partly.** POPQUORN is the clearer of the two: Table 3 is in the main text and §6 states the three contrasts. The DICES-350 vs NLI contrast is not self-contained:

- **No panel inventory in the main text.** "14 datasets" (abstract) are never listed. DICES-350 vs DICES-990, Dorn, Buse–Weimer, POPQUORN, Scalabrino and CSC appear by name only, with no item count, scale, rater count or construction. A reader cannot tell that DICES-350 is a 3-level scale with 104 persistent raters. That fact matters: on a 3-level scale, "shape beyond mode and mean" has one degree of freedom, namely dispersion.
- **The plant evidence that carries "power" is text only.** Detections, γ, matched X_own and recovery ranges for both constructions should be a small table, or a column of Table 2.
- **The comparator is deferred** ("KL-projected onto the cell when the cell is sparse (Appendix A)"). The headline estimand depends on q_T, so one sentence on cell sparsity and the projection is needed in §3.
- **Internal protocol IDs in the main text.** "(ROUND20 R20-4)" (§6) and "(ROUND22 R22-6, grid amended after a smoke run)" (§7) mean nothing to a reviewer. Neither do "registered" and "prospective" ("A prediction we registered was falsified", §1, §6): registered where? Replace them with a one-paragraph "Analysis protocol" statement (timestamped internal protocol files, released with hashes in the supplement; amendments labelled) and an appendix table mapping each claim to its protocol entry.
- **Effect scale.** RPS differences of 0.006 mean nothing without a baseline. Give the full-data RPS (0.1215) so readers see ≈ 5 % relative.
- **The NLI "location" definition** (modal class and modal mass) is a single clause in §3, and its consequence for what "shape" means on NLI is never discussed (H1).

---

## 4. Issues ranked by severity

### CRITICAL

**C1. The flagship "not decoded" claim on DICES-350 is contradicted by the paper's own prespecified null-calibrated statistic, which the main text omits.**
- Draft: "On DICES-350, then, the shape exists within the observed rater pool, the decoder has power … and the observed shape is not decoded" (§4); "The shape exists within the rater pool, a planted shape of its size is decoded, and the real one is not" (Conclusion).
- Data (dd/dices_a40_*): V_own = ⟨r̂, s₂⟩/n excludes 0 on all three families. Qwen2.5 4.9 [2.3, 7.5]·10⁻⁶; Qwen3 2.8 [1.0, 4.6]·10⁻⁶; OLMo-2 2.3 [0.5, 4.1]·10⁻⁶. At a = 20 it also excludes 0 for Qwen2.5 and Qwen3. Location-only null (R22-3): mean 4.7·10⁻⁷. The net ratio is 15.0 % [2.6, 27.4] (Qwen2.5) and 9.5 % [−0.3, 19.3] (Qwen3).
- G_own ≈ 0 because the decoder's variance penalty ‖r̂‖²/n (G_own,perm = −6.7·10⁻⁶) cancels a genuine covariance, not because the text carries nothing.
- **Fix:** report V_own (and the net ratio) for every panel in Table 2. Rewrite the DICES-350 conclusion as "a small text-covarying component is detectable, but the decoder obtains no proper-score gain from it", and remove "the real one is not [decoded]" from the abstract, §1, §4 and the Conclusion. Note that DICES-990 also has V_own > 0 ([0.8, 2.6]·10⁻⁶) with X_own n.s.

**C2. G_own/X_own is not a "fraction of the shape that is decodable", and is not comparable across panels.**
- Draft: "As a fraction of the reproducible own-shape" (App. B); "a quarter to two-fifths of it is decodable" (Conclusion); the headline compares 1 % (DICES, 350 items, X_own 4.9·10⁻⁵) with 28–38 % (ChaosNLI, ≈ 1,500 items, X_own 1.1·10⁻², 230× larger).
- A shape that is exactly linear in the decoder's inputs is recovered at 15–33 % on DICES-350, and at 38–56 % on SummEval at its magnitude. Recovery is a finite-sample, SNR-dependent attenuation, so part of the ordinal–NLI gap is mechanically produced by n and X_own.
- **Fix:** (i) call the ratio "the decoder's normalised own-shape gain", never "fraction decodable"; (ii) add an NLI plant, for example a Dirichlet-mixture plant whose non-modal split is linear in a feature direction, matched to the NLI X_own, so both sides have a ceiling; (iii) report plant-normalised recovery for every panel with a plant; (iv) subsample ChaosNLI to 350 items at a = 20 and a = 40 and re-decode, to show that the gap survives matched n. This is the single analysis that would make the headline contrast credible.

### HIGH

**H1. The nominal and ordinal "shape beyond location" are different constructs, which confounds the headline contrast by design.**
- Ordinal location = (mode, mean). On DICES's 3-level scale this leaves a single degree of freedom, the *spread*, because the mean already fixes which side of the mode receives mass.
- Nominal location = (modal class, modal mass). For a 3-class NLI item this leaves *which* non-modal class receives the minority mass. That is directional, semantic information ("neutral vs contradiction"), the analogue of what the mean already absorbs on ordinal scales.
- It is unsurprising that direction is text-predictable and spread is not; Jiang & de Marneffe (2022, TACL) catalogue exactly such text-based reasons for NLI disagreement.
- "We do not claim a causal role for … label structure" (§1) does not cure this, because the confound is in the estimand, not the explanation.
- **Fix:** add a nominal comparator that also conditions on the runner-up class (modal class, modal mass, second class), so the NLI residual is spread-like, and report G_own/X_own and ρ_own under it. Otherwise restate the contrast as "the directional allocation of minority mass on NLI vs dispersion on ordinal scales".

**H2. Abstract and §1 overclaim relative to the evidence.**
- (a) "no ordinal panel shows a robustly reproducible shape beyond location". Dorn's own-shape is *not* location-sized: location-only simulations give X_own ≈ 35 % of the observed (dd/dorn_java_r21_plant0_s*: mean 9.4·10⁻⁵ vs 2.69·10⁻⁴, observed lower bound 1.55·10⁻⁴ above all five draws). At 40 + 20, only M2 dispersion reproduces Dorn Java (results/rater_item_dense/dorn_java.json: observed X_own 1.8·10⁻⁴, outside the M0 range [1.9·10⁻⁵, 1.3·10⁻⁴]); ρ_own for Dorn CUDA is 0.22 [0.11, 0.29]. What is location-sized on Dorn is the *decodable covariance* V_own (≈ 96 %), not the own-shape. The §1 bullet "on Dorn's readability panel, of the size that location and rater thresholds alone produce" is therefore wrong as written; it should say "Dorn has a reproducible own-shape beyond location (item-level intervals), whose decodable part is location-sized, and the decoder has no power at its magnitude (1/5)".
- (b) "A planted text-predictable dispersion shape … is recovered at 15–33 %" in the abstract, without the polarisation 3/5, and the Conclusion's "a planted shape of its size is decoded" with no construction at all.
- (c) "Accordingly, replacing the shape … changes LoRA judges by at most ±0.0015". Both LoRA panels have no detectable own-shape, so the null is non-discriminating (§5 says so), and on POPQUORN the location-destroying *positive* control is itself not detected under user-level resampling ([−0.0004, +0.0065]). The audit has no demonstrated sensitivity on POPQUORN under the conservative clustering.
- (d) "Its forecasting reliability is 0.04–0.41 … under the ½ needed". These are point estimates; EmoBank's and Scalabrino's upper bounds are 0.55, and EmoBank's A1^x interval includes 0. Say "point estimates 0.04–0.41; no interval lies above ½".
- **Fix:** rewrite the abstract along the lines of C1, H1 and H2a–d. Drop "Accordingly"; replace the LoRA sentence with the ChaosNLI discriminating case; add "(a polarisation plant: 3/5)" or drop the plant sentence.

**H3. §1(iii) and Contribution 3 say the opposite of the paper's discriminating evidence.**
- "*The judges we trained show no detectable use of the shape*" (§1 iii heading) and "A donor-replacement audit showing that current training does not use the shape" (Contribution 3). The only discriminating case, ChaosNLI, shows frozen-feature heads *do* use the shape (+0.005–0.017 Brier). On SummEval and POPQUORN there is no shape to use.
- The supported conclusion is: "judges use the shape where it is reproducible and decodable (NLI) and are insensitive to it where none is detectable". **Fix:** reword the heading and the contribution accordingly; the LoRA audit is a sanity check, not a finding.

**H4. §4 and §5 contradict each other on DICES-350's rater-side origin.**
- §4: "A location-and-threshold simulation of the panel yields no own-shape at all: mean X_own is −1.3·10⁻⁵, against the observed 4.9·10⁻⁵."
- §5: "On DICES-350, thresholds reproduce the observed X_own where location alone does not."
- The §5 claim comes from R19-3 (results/rater_item_dense/dices.json), whose "observed" a = 40 X_own is **1.79·10⁻⁵** (R = 5), against 4.75–4.9·10⁻⁵ in rho_own and decode_decomp. M1's simulation range [−4.9, 2.1]·10⁻⁵ covers 1.79·10⁻⁵ but not 4.9·10⁻⁵. Under the headline estimate, *no* fitted rater model reproduces DICES-350's own-shape.
- The same quantity also differs by 2.7× across split repetitions, which suggests that split-randomness variance is not fully captured.
- **Fix:** rerun R19-3 for DICES-350 at R = 10 with the decode_decomp split, and report which models' ranges cover the headline 4.9·10⁻⁵. Then remove whichever of the two sentences fails. Delete "Whether the residual shape itself is rater-side is established only on DICES-350" unless it survives.

**H5. The budget headline is not a fixed-budget result, and its fixed-budget LoRA comparison is null.**
- Abstract: "one rating per item costs 0.006 RPS against the full data, and a second rating recovers about half". The "full data" has 7× the ratings.
- The one fixed-budget LoRA contrast (117 × 7 vs 819 × 1) is +0.0027 [−0.0024, +0.0074], which is not mentioned in the abstract, although the title promises "Where to Spend the Annotation Budget".
- "About half" has an interval of roughly 3–98 % (−0.0031 [−0.0062, −0.0002] over 0.0063).
- Intervals rest on three seed clusters × three folds; with three assignment clusters, bootstrap tail calibration is weak, as round 20 already noted.
- **Fix:** in the abstract, state the fixed-budget contrast first ("at a fixed budget, items-first and raters-first LoRA judges are indistinguishable on POPQUORN"). Report "a second rating helps (−0.0031 [−0.0062, −0.0002])" rather than "recovers about half". Add more independent assignments (≥ 6) if the budget claim stays in the title.

**H6. Table 1 caption and rows are false for the three-rater panels** (round-20 #8, still open).
- Caption: "Three-rater panels: the mode-and-mean cell determines the histogram (support 0)"; rows: "-- (no shape)".
- §3 and App. E: "15–75 % of the three-rating histograms share their exact cell with a different histogram".
- **Fix:** "Three-rater panels: a split leaves two ratings, which the cell determines; ρ is unmeasurable (not zero). Support is computed at two ratings." Replace "no shape" with "unmeasurable".

**H7. Novelty and positioning are insufficient for ICML as written.**
- The identity A1 = M − 2X is the standard quadratic-score expansion E‖h₁ − y‖² − E‖q − y‖² = ‖h₁ − q‖² − 2⟨h₁ − q, y − q⟩. ρ is a split-half reliability in the Spearman–Brown / generalizability-theory tradition. The decoder is a ridge probe.
- The contribution is therefore empirical and conceptual: separating the reproducibility of the shape beyond location from its predictability from the text. That is a reasonable but modest ICML contribution, and §2 undersells how close prior work is. Missing, and in my view necessary:
  - Gordon et al. (CHI 2021, "The Disagreement Deconvolution"): separates annotator inconsistency from disagreement via repeated labels, and is the closest precedent for "reproducible across raters";
  - Davani, Díaz & Prabhakaran (TACL 2022): multi-annotator models;
  - Jiang & de Marneffe (TACL 2022): reasons for NLI disagreement; directly relevant to H1;
  - Baan et al. (EMNLP 2022, "Stop Measuring Calibration When Humans Disagree");
  - the DICES dataset paper (Aroyo et al., 2023) and group-level disagreement analyses on DICES (e.g. Prabhakaran et al.'s GRASP, NAACL 2024; Homan et al.'s multilevel models). These bear directly on the polarisation construction;
  - LeWiDi shared tasks (Leonardelli et al., 2023);
  - Sucholutsky et al. (UAI 2023, "On the informativeness of supervision signals"): the cost–benefit of soft labels vs more items, directly on the budget question;
  - Elangovan et al. (2025): LLM-judge evaluation stratified by human uncertainty;
  - generalizability theory (Brennan, 2001) for ρ.

  Please verify these citations before adding them; I list them from memory.
- §2's "none separates the part of the histogram that is reproducible across raters from the part that is predictable from the input" must be argued against Gordon et al. and Davani et al.
- **Fix:** expand §2 by about 0.3 page, and sharpen Contribution 1 to the location-vs-shape decomposition plus the own-shape estimand and its calibration. Consider whether a datasets-and-benchmarks or TACL venue fits the "reliability cards" contribution better.

### MEDIUM

- **M1. The CLT calibration check is weak and out of regime.** Nine of ten coverage passes with probability 0.38 under 80 % coverage. The draws are at a = 4 on SummEval/POPQUORN only. Add ≥ 50 null draws at DICES-350 a = 40 and an NLI-like null; report empirical coverage of V_own and of G_own,net (the latter has a known nonzero null mean, so check its centring).
- **M2. The within-pool caveat is under-weighted in the headline.** With rater resampling, DICES-350's ρ_own includes 0, so for new raters the "clean case" shape is not shown to exist. The abstract's "the only panel where one is detectable within the rater pool" is accurate, but the Conclusion drops "within the pool" from "On DICES-350 we can show both halves directly".
- **M3. The nonlinear probe was run only on panels with no own-shape** (round-20 #6 above). Run RFF on DICES-350 (a = 40) and Dorn; given C1, a nonlinear decoder with better variance control may turn V_own > 0 into G_own > 0.
- **M4. "Pool bias makes 'no detectable own-shape' easier to declare".** Quantify it for DICES-990 and POPQUORN (both one-group fits, bias ≈ 0) and say so explicitly. The sentence currently reads as a general caveat that applies to all nulls.
- **M5. Frozen-head budget orderings are mean-only.** DICES-990 594 × 1 vs 297 × 2 differ by 0.0014 RPS with per-configuration SD ≈ 0.006–0.007 (budget_heads/dices990/runs.jsonl). "Wins monotonically" needs paired intervals across the 30 configurations.
- **M6. SummEval provenance.** The duplication is still unverified upstream. Any SummEval number in the main text (§6 dilution, Table 1 full-panel rows) should carry the "released file" qualifier; consider dropping SummEval from the main text entirely.

### LOW

- "+0.0000 [−0.0009, +0.0009]" → give five decimals or "< 0.0001".
- Remove results/… file paths from App. E and elsewhere; they read as unanonymised artefacts.
- "exceeds ½ from two to three raters" (§1, §3) is ambiguous: ρ is 0.45 at a = 2 and 0.63 at a = 3 on MNLI. Write "from three raters".
- "about 95 %" → "about 96 %" (95.7 %).
- App. F has a LaTeX escape bug: "$X_{	ext{own}}$" (a tab character where "\t" should be), twice.
- Header line 10 of the draft ("Numbers are copied verbatim from v2.5 and none are recomputed") is false after the percentage audit and should be removed before submission.

---

## 5. The three most valuable changes

1. **Report V_own and the net ratio for every panel, and rewrite the DICES-350 story around them (C1, H2, H4).** On DICES-350 a small text-covarying component of the own-shape *is* detected on all three families. The decoder simply cannot convert it into a proper-score gain. That makes the paper's story more honest and arguably more interesting ("detectable, but too weak to help a judge"). It requires no new compute beyond rerunning R19-3 at R = 10, and it removes the claim most likely to be caught by a careful reviewer who opens the JSONs.
2. **Make the cross-panel contrast estimand-matched and ceiling-calibrated (C2, H1, §3b).** Prespecify an R23 block with:
   - (a) ChaosNLI at a = 40/20 and at n = 350 (subsampled);
   - (b) an NLI plant matched to the NLI X_own;
   - (c) a partial-predictability plant on DICES-350 giving a minimum detectable text-predictable fraction;
   - (d) a nominal comparator that also fixes the runner-up class.

   Then report matched-a *differences* with intervals, and plant-normalised recovery, in place of "every NLI lower bound exceeds every ordinal upper bound". This is the change that decides whether the headline contrast is about disagreement or about the estimator.
3. **Rewrite the abstract, §1(iii), Contribution 3 and the Conclusion to match what the evidence supports (H2, H3, H5).**
   - State the ChaosNLI discriminating case instead of the non-discriminating LoRA null.
   - Lead the budget sentence with the null fixed-budget LoRA contrast.
   - Carry the polarisation 3/5 and "within the observed rater pool" wherever the dispersion plant and the DICES-350 shape are cited.
   - Replace internal protocol IDs in the main text with a short analysis-protocol paragraph.
   - Add the missing related work (Gordon et al. 2021; Davani et al. 2022; Jiang & de Marneffe 2022; Sucholutsky et al. 2023) and position the contribution against it.

---

## 6. Verdict

**Weak reject.** The paper's measurement framework (location vs shape beyond location, own vs cross reproducibility, decodability with permutation, positive and planted controls) is careful, and the protocol discipline is unusually good. The SE-panel and budget observations are useful. But the central empirical claim, "on DICES-350 a reproducible shape exists and is not decoded, while on NLI a quarter to two-fifths is", rests on three things that do not hold up:
- a proper-score ratio that ignores the paper's own significant covariance statistic (C1);
- a ratio whose ceiling depends on n and SNR and is uncalibrated on the NLI side (C2);
- a nominal/ordinal estimand mismatch (H1).

The ICML contribution beyond careful measurement is also modest relative to the uncited prior work (H7).

**To move to borderline:** do change 1 (V_own/net ratio reporting and the DICES rewrite), fix H2–H6 in text, and implement the §3b reporting conditions; all of this is text plus one CPU rerun. **To move to weak accept:** in addition, run the R23 block of change 2 and show that the ordinal–NLI gap survives at matched n, a matched rater count of 40, a calibrated ceiling, and a spread-only nominal comparator.

---

## Appendix: numbers spot-checked against results/ (all recomputed with /scratch/jundahe/venvs/llmj/bin/python)

| Draft claim | Recomputed | Source | Verdict |
|---|---|---|---|
| DICES-350 a = 40: "−1 to 1 % … upper bounds ≤ 12 %" | 1.30 [−8.77, 11.37]; −0.56 [−7.96, 6.84]; −0.03 [−7.22, 7.16] | dd/dices_a40_r21, _qwen3_r22, _olmo_r22 | MATCH |
| Dispersion plant "5 of 5 … 15–33 %" | 5/5; 0.319, 0.278, 0.227, 0.326, 0.153; mean X_own 5.46e−5 | dd/dices_r22_plant0.4_s0–4 | MATCH |
| Polarisation plant "3 of 5 … 1–22 %" | 3/5; 0.196, 0.224, 0.115, 0.165, 0.013; mean X_own 6.30e−5 | dd/dices_r22p_polar1.5_s0–4 | MATCH |
| Location-only DICES "mean X_own −1.3·10⁻⁵" | −1.29e−5; 0/5 detected | dd/dices_r22_plant0_s0–4 | MATCH |
| MNLI / SNLI a = 20 "28 % [24, 33]", "38 % [33, 42]" | 28.34 [24.64, 32.04]; 37.80 [33.95, 41.64] | dd/chaosnli_*_r21 | MATCH |
| MNLI a = 4 "22 % [18, 26]" | 22.01 [18.65, 25.38] → authors' proposed "19 %" violates outward rounding | dd/chaosnli_mnli_a4_r21 | MATCH; proposed 19 is wrong |
| Dorn "10 % [4, 16]" | 10.15 [4.44, 15.86] | dd/dorn_all_r21 | MATCH |
| Dorn location-only "≈ 95 % of ⟨r̂, s₂⟩" | V_own ratio 95.7 %; **X_own ratio 34.9 %** (not stated in §1) | dd/dorn_java_r21_plant0_s* | MATCH for V; §1 bullet mischaracterises X_own |
| ρ_own at 40 "BW 0.13, DICES-350 0.10, DICES-990 0.06, Dorn 0.12–0.22, MNLI/SNLI 0.61/0.67" | 0.128, 0.097, 0.058 [−0.002, 0.139], 0.125/0.134/0.221, 0.611/0.674 | results/rho_own/*.json | MATCH (DICES-990 item-level CI includes 0, not mentioned) |
| EmoBank ρ "0.41" (range endpoint) | 0.412 [0.272, 0.555] | rho_exact/emobank_reader_v5.json | MATCH (upper bound > ½) |
| POPQUORN LoRA "819 × 1 − full = +0.0063 [+0.0030, +0.0099]", "49 %" | +0.00628 [0.00305, 0.00994]; (0.00628 − 0.00322)/0.00628 = 48.7 % | lora_budget_r20_pq/summary_popquorn_off8.json | MATCH |
| DICES-990 heads "0.203, 0.205, 0.207, 0.213, 0.219" | 0.2032, 0.2046, 0.2071, 0.2134, 0.2185 (SD 0.006–0.008 per config) | budget_heads/dices990/runs.jsonl | MATCH |
| **Not in the draft:** DICES-350 V_own a = 40 | 4.94e−6 [2.34e−6, 7.54e−6] (Qwen2.5); 2.81e−6 [1.04e−6, 4.58e−6] (Qwen3); 2.33e−6 [0.55e−6, 4.11e−6] (OLMo-2) | dd/dices_a40_* (clt.V_own) | basis of C1 |
| **Not in the draft:** R19-3 DICES "observed" X_own at 40 | 1.79e−5 (vs 4.9e−5 in decode_decomp, 4.75e−5 in rho_own) | rater_item_dense/dices.json | basis of H4 |
