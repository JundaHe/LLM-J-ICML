## Verdict

The paper’s strongest contribution is now the intervention audit, not a universal two-number target. The results are coherent and interesting, but three code issues should be fixed before freezing claims:

1. `targets.py` still does not guarantee a KL projection.
2. `diag_location.py` does not actually control categorically for mode.
3. `analysis_chain7.py` does not yet implement the promised grouped estimator/bootstrap or enforce a complete balanced block.

These do not overturn the substantive pattern, but they affect the words “certified,” “mechanism,” and the eventual chain7 confidence intervals.

## 1. Inert RPS/KL but better disagreement ranking

Yes, this makes sense. RPS/KL assess average probabilistic accuracy; partial Spearman of predicted disagreement assesses the ranking of a nonlinear functional of the prediction. An intervention can leave proper scores essentially unchanged while improving that ranking.

The lower-entropy artefact has a precise answer:

- For `soft_pmm`, the matching is bijective within cells, so the multiset of training histograms—and therefore its entropy distribution—is preserved exactly. Systematically lower target entropy cannot explain its `+0.017` result.
- `soft_pmmx` is not literally a permutation: donor histograms are projected onto the recipient’s mode-and-mean constraints. That projection can change entropy, support, and dispersion.
- The fact that `soft_pmm`, `soft_pmmx`, and `shrunk_res` all improve D-partial by roughly `+.014–.017` is good triangulation for a denoising interpretation, but it is not proof.

Recommended wording:

> Replacing item-specific residual allocation while retaining location did not detectably change average RPS or KL, but improved the secondary ranking of held-out disagreement by about 0.017 in commit Why heads. Together with the residual-shrinkage result, this is consistent with residual allocation estimated from four training raters acting as noisy supervision for dispersion ranking.

Do not say “residual shape is sampling noise.” Say “consistent with noisy residual-shape supervision in this four-rater setting.” Also call `pmmx` a “mode-and-mean-preserving donor replacement,” not an “exact permutation.”

Before publication, record for every target arm:

- mean entropy, target disagreement, max probability and support size;
- actual TV from the recipient and donor;
- fraction actually changed after projection, not merely matched;
- the same entropy/disagreement summaries for model predictions.

### Remaining `targets.py` defect

The claimed v2 contract is not implemented:

- [`targets.py:72`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:72) still returns the feasible starting histogram when optimization fails. The certificate does not flag this, so affected `pmmx` items may silently remain unchanged.
- `res.success` is never checked at [`targets.py:68`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:68).
- The advertised single `1e-6` tolerance still uses `1e-4` for the mean at [`targets.py:30`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:30) and [`targets.py:78`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:78).

Thus “0 violations” currently certifies feasibility under those tolerances, not successful KL projection. Remove the fallback, require optimizer success, return projection-status metadata, and report actual post-projection treatment dose. Existing v3 outputs need not be rerun if deterministic regeneration shows zero fallbacks and identical targets.

## 2. Does mean2’s loss kill the constructive contribution?

It kills the strong constructive claim, not the information audit.

`cond` should become the main two-statistic reference, described precisely as:

> a cross-fitted conditional-shape reference indexed by mode and a prespecified mean bin.

But `cond` is not yet a clean deployable “collect only two numbers” recipe:

- It estimates its conditional shapes from full training histograms.
- It preserves a mean bin, not necessarily the exact item mean.
- Its sparse-cell fallback at [`probe_mean2.py:91`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/probe_mean2.py:91) uses an unconstrained tilt.

Therefore:

- Keep `cond` in the main audit table.
- Move `mean2` out of the headline and into the full hierarchy/appendix, but do not hide it; the constrained baseline’s failure is scientifically informative.
- Describe `mean2` as a projection control, not the proposed method.
- Drop “two-number target” as a constructive contribution unless a prespecified `cond_exact`—conditional cell prototype projected to exact mode and mean—replicates across panels.

The defensible conclusion is: “Some tested predictions obtainable from mode and location matched the histogram on particular panels,” not “two numbers are sufficient” or “we provide a better target.”

## 3. Location mechanism

It is presently a post-hoc candidate explanation, not a confirmed mechanism.

There is also a methodological bug: [`diag_location.py:31-33`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/diag_location.py:31) residualizes against the numeric rank of `z`. That controls only a linear ordinal trend, not categorical mode. Replace it with mode dummy fixed effects or rank/center separately within each mode stratum. The script also computes but does not report the intercept, and arm comparisons should use identical completed folds.

After fixing that, the commit/SummEval contrast is useful descriptive evidence. But the literal product of two Spearman correlations has no identified relationship to RPS magnitude.

A stronger prespecified check would be:

\[
G=\rho(\hat\mu_{\text{soft}},\mu_{\text{train}}\mid z)
-\rho(\hat\mu_{\text{pmode}},\mu_{\text{train}}\mid z),
\qquad
R=\rho(\mu_{\text{train}},y_{\text{eval}}\mid z),
\]

then predict the sign and rank of raw `pmode − soft` RPS using \(G\times R\).

Use diagnostics measured on validation items to predict effects on separate test items, freeze the formula and expected signs beforehand, and evaluate new seeds/splits. BW/DICES/HelpSteer2/Scalabrino can provide triangulation, but because their effects have already been inspected, they are not pristine confirmatory panels. With only four panels, report sign concordance and leave-one-panel-out behavior rather than a significant regression.

Also weaken:

> “Raw hard is worse mainly through sharpness.”

to:

> “Hard predictions are substantially sharper, and the attenuation after arm-specific calibration is consistent with a substantial calibration component.”

Entropy alone does not causally decompose the RPS gap.

## 4. `analysis_chain7.py`

The calibration logic, fixed-fold averaging, common-map tie ordering, three estimands, paired `common − raw` contrast, seed resampling, per-seed estimates and raw equivalence-CI check are present. The following changes are needed before using its output.

### Material issues

- The promised group estimator is absent. Lines [`67`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_chain7.py:67) and [`79`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_chain7.py:79) average individual rows. Commit hashes contain paired developer/generated rows, so calibration and test resampling must sample hashes and include every row in the sampled hash.
- The script silently drops incomplete cells unless `--require_all` is supplied, then still labels the result “balanced.” Complete `3×3×roster` should be the default hard requirement.
- One positional `cal_idx`/`test_idx` is reused across all seeds and folds, which is correct only if every cell has globally identical item ordering. Alignment is checked only within a seed-fold at [`analysis_chain7.py:42-44`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_chain7.py:42). Assert hashes, row IDs, and ordering across every seed and fold.
- Validate `meta["opt_seed"]`, arm, criterion, expected permutation seed, array lengths, finiteness, and probability simplex—not merely evaluator and split.
- The roster is supposedly frozen but remains freely overrideable. Either hard-code it or reject noncanonical rosters for the primary analysis.

### Missing promised reporting

Add:

- fold-specific estimates;
- `n_seed`, `n_fold`, and `n_group`;
- calibration-grid boundary-hit frequencies across bootstrap refits;
- explicit statement that optimizer and permutation randomness are jointly resampled and cannot be separated;
- at least 10,000 final bootstrap draws rather than the current default 2,000.

The 90% CI containment rule is fine, but call it “equivalence by the CI/TOST criterion,” not a computed TOST p-value.

Finally, chain7 covers one outer item split and one base family. Call it an “optimizer/permutation replication block,” not the overall replication standard; it does not satisfy the earlier three-split/two-family standard.

## 5. Suggested header wording

**Title**

> *What Distributional Judge Training Uses from Human Rating Histograms: A Link-Randomization Audit*

This is safer than foregrounding a universal ordinal/nominal distinction based on the current panels.

**Estimands**

> Native-output RPS (\(T=1,\lambda=0\)) is the prespecified primary estimand for target-information contrasts. We additionally report a standardised-calibration sensitivity using one map fitted jointly with equal arm weights over the frozen roster, and an arm-specific calibrated deployment estimand. Calibration is refit inside the bootstrap; equivalence testing is reserved for the primary raw contrast with prespecified margins. The common-map result is roster-dependent.

**Abstract core**

> Distributional judge training is often interpreted as learning human disagreement. We audit that interpretation by randomizing the item–histogram link while preserving successively the modal label and item location, with native-output RPS against held-out raters as the primary estimand. Across the ordinal panels tested, replacing residual histogram allocation while retaining mode and mean did not measurably worsen RPS. Breaking item-specific location harmed prediction on SummEval and in frozen-feature heads on commit Why; the LoRA effect on commit Why was sensitive to recalibration, while commit What’s gain survived location disruption. On nominal NLI, conditional on the capped replication, preserving modal class and modal mass was insufficient: scrambling residual class allocation degraded prediction. These results locate the useful information in soft labels more narrowly than “human disagreement,” while showing that it depends on task and label geometry.

Do not say “under all three estimands on SummEval” until fold 2 completes for `perm_mode`.

**Mechanism**

Rename this block “Exploratory explanation”:

> Panels with a larger intervention-induced loss of within-mode location tracking and stronger held-out relevance of target location showed larger costs from location disruption. This pattern motivates a prespecified held-out-panel test; it is not presently a causal mediation result.

Add to “Do not write”:

- “exact permutation” for projected `pmmx`;
- “the location mechanism explains the effect”;
- “the hard-label gap is a calibration gap”;
- “cond requires only two-number annotations”;
- a causal ordinal-versus-nominal generalization;
- “confirmatory LoRA replication” for chain7 alone.

## 6. What to add or remove now

Do not add another GPU arm to chain7. Keep the frozen roster, including `sordm`; removing an unfavorable prespecified comparator now would be harder to defend than reporting it as secondary.

Priorities:

1. Fix `targets.py`, `diag_location.py`, and `analysis_chain7.py` before interpreting new output.
2. On SummEval fold 2, prioritize `perm` and `perm_mode`. The old unconstrained `mean2` is no longer central or directly comparable.
3. Add only CPU-side audits: target entropy/dispersion/dose, projection-status counts, balanced-fold location diagnostics, and chain7 bootstrap validation.
4. Do not add more target families or tune a new mechanism after seeing the remaining panels.
5. After chain7, either scope LoRA conclusions explicitly to Qwen/split 0 or later meet the already stated item-split and model-family replication standard.

The most defensible paper is now a careful boundary result: residual ordinal allocation showed no detectable proper-score value under the tested interventions; item location mattered heterogeneously; nominal residual allocation could matter; and no single compact target dominated.