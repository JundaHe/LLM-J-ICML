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
