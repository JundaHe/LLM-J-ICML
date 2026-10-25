# Verdict

Do **not** make the common-map score primary for claims about what target information the model learned. Keep **raw RPS primary**, call the common map a **standardized-calibration sensitivity**, and reserve arm-specific calibration for the **arm-optimized deployment pipeline**.

Raw RPS is not “neutral,” but that is not a defect: if a training target makes the model appropriately less confident, a proper score should reward that consequence. The permutation design—not post-training calibration—is what identifies which target information matters.

## 1. Primary estimand

The pooled common calibrator has no test leakage: it is fit on calibration items and evaluated on disjoint test items. With equal item counts, each arm contributes equal weight; no arm has more probability “mass.”

It nevertheless has three important dependencies:

- It is **arm-roster dependent**. Five smooth or nearly duplicate arms exert five times the influence of one hard arm. Adding or removing an arm can change every reported contrast.
- A common \(T\) does not “remove sharpness.” It applies the same nonlinear operator to differently shaped predictions, so its effect remains arm-specific.
- The implemented map is \(T+\lambda p_0\), not merely a monotone temperature map. Mixing with climatology can change category rankings and item ordering.

Thus the three estimands answer:

| Estimand | Defensible interpretation |
|---|---|
| Raw \(T=1,\lambda=0\) | Total effect of the target intervention on the model’s native predictive distribution |
| Common map | Performance after one prespecified standardized recalibration rule |
| Arm-specific map | Performance of an independently optimized deployment pipeline |

The hard–Chen change from \(+.0073\) raw to \(+.0008\) arm-calibrated is consistent with a sharpness/calibration contribution, but it does **not** explain why `perm_mode − chen` moves from \(+.0005\) to \(+.0033\): both are smooth-target arms. That requires a direct Chen-versus-`perm_mode` diagnostic.

The honest commit-Why wording is:

> Destroying the item–location link did not measurably change native-output RPS on commit Why (\(+.0005\), 95% CI \([-.0021,+.0032]\)). The arm-optimized calibrated pipeline showed a positive contrast (\(+.0033\), \([+.0013,+.0054]\)); the common-map point estimate was also \(+.0033\), although its calibration-refitted uncertainty remains to be estimated.

Do not write “the effect exists only after calibration” yet. A nonsignificant raw estimate and significant calibrated estimate do not themselves establish that the two effects differ. Bootstrap the paired quantity

\[
(\Delta_{\text{common}}-\Delta_{\text{raw}})
\]

with calibration refitting.

## 2. Why the same target-mean displacement behaves differently

The 0.44-point target displacement is intervention dose, not evidence that the displaced information is learnable or evaluator-relevant. The main possibilities are:

1. Commit-Why text may weakly predict within-mode location.
2. Its 5-or-6-rater mean may be too noisy to predict a held-out evaluator.
3. Chen and `perm_mode` may trade resolution against raw calibration/sharpness, producing a near-zero raw net effect.
4. SummEval’s expert mean may be more reliable or more aligned with its held-out expert, even if disagreement is larger.
5. The 20% modal CE term may attenuate location learning, but because it is identical on both panels it cannot alone explain the panel interaction.

The 0–4 versus 1–5 labeling is immaterial once both are encoded as \(0,\ldots,4\).

Run this diagnostic per panel, arm, seed, fold, and estimand:

- Define truth as the target-rater mean excluding evaluator \(e\), \(\mu_{i,-e}\).
- Compute predicted mean \(\hat\mu_i=\sum_k kq_{ik}\).
- Report **within-mode** Spearman and Pearson correlation between \(\hat\mu_i\) and \(\mu_{i,-e}\), or partial correlation controlling for mode. Overall Spearman will mostly rediscover the mode.
- Estimate calibration slope/intercept and MAE of \(\hat\mu_i\) against \(\mu_{i,-e}\).
- Measure target-side relevance independently: within-mode association between \(\mu_{i,-e}\) and evaluator score \(y_{ie}\), plus split-half reliability of \(\mu_i\).
- Decompose RPS by ordinal threshold. Report the Chen-versus-`perm_mode` difference at each cumulative threshold, together with mean entropy, maximum probability, predictive variance, and fitted \(T,\lambda\).
- Bootstrap differences using the same seed/item-group draws as the main analysis.

The decisive table would contain:

\[
\rho(\hat\mu,\mu_{-e}\mid z),\quad
\rho(\mu_{-e},y_e\mid z),\quad
\text{calibration slope},\quad
H(q),\quad
\Delta\text{RPS by threshold}.
\]

If commit has target-side signal but Chen does not learn it, then an \(\alpha=1\) Chen-versus-`perm_mode` ablation is warranted. If the target-side signal itself is weak, the CE hypothesis is unnecessary.

## 3. Paper spine and abstract core

The spine remains sound after three downgrades:

- `perm − chen ≈ 0` means **no detected average degradation in the tested ordinal configurations**, not “residual shape is unused.” Formal equivalence still requires a frozen margin and permutation/training randomness.
- The location result is strong across estimands on SummEval. On commit Why it is explicitly estimand-dependent.
- Commit What is **consistent with a non-item-linked smoothing/regularization benefit**, not proven to be “smoothing only.” Hard versus smooth also changes the training objective wrapper.
- The nominal boundary belongs in the spine only after the capped `zc/pzc` rerun confirms it.

Two-sentence abstract core, assuming the corrected nominal rerun holds:

> Across the ordinal panels tested, permuting the remaining histogram while preserving each item’s mode and mean caused no detectable average increase in predictive RPS; disrupting item-specific location hurt under all three scoring estimands on SummEval, but on commit Why only after recalibration, while commit What’s gain survived location disruption and was consistent with smoothing or regularization. This pattern was not universal: on nominal NLI, scrambling residual class allocation while preserving modal class and mass degraded prediction, locating the value of full soft labels in task structure rather than distributional supervision per se.

## 4. `targets.py`

### Ordinal projection: mathematically right, operationally not certified

The optimization problem and SLSQP inequality directions in [targets.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:20) are correct. The unconstrained exponential tilt is also the correct solution when the mode inequalities are inactive.

The fallback is not correct:

- It searches only 19 arbitrary values of \(w\).
- It is not guaranteed feasible.
- Even when feasible, it is not necessarily the KL projection.
- Clipping and renormalizing after optimization can break the mean equality.
- The fallback threshold permits mode errors up to \(10^{-4}\), whereas certification rejects errors above \(10^{-6}\).
- The certificate is recorded but never asserted in [probe_mean2.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/probe_mean2.py:93).

The random failure was concrete: requested \(z=0\), but the function returned approximately

\[
q=(.4000,.0001,.0003,.0658,.5338),
\]

so class 4, not class 0, was modal.

More importantly, the running production output is already affected: the first six `commit_why_v3` configurations have **48 `soft_pmmx` mode violations total, with all 6 configurations affected**. `mean2` has zero in those six configurations, but `pmmx` does not. Thus “certified” in Hour 13 is currently false.

Required fix:

1. Before clipping, immediately return the original base if it already satisfies mode and mean. This handles many exact donor cases.
2. Obtain a genuinely feasible starting point—preferably pass the recipient empirical histogram, which is known to be feasible, or use a small `linprog` feasibility solve.
3. Accept a solver result only after checking simplex, nonnegativity, mean, and mode at one consistent tight tolerance.
4. Remove the heuristic fallback; retry with a robust convex solver or raise an exception.
5. Make every caller hard-fail on nonzero violations before training.

One violation in 500 is not acceptable when the intervention’s identifying claim is exact. Certification is useful only if it prevents the invalid target from being used.

### Nominal water filling: valid for ChaosNLI, not generally correct yet

For the actual \(K=3\) ChaosNLI setting and an empirical modal mass \(c\ge1/3\), [nominal_zc](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:44) implements the intended capped proportional allocation correctly. I found zero violations in 20,000 valid \(K=3\) cases.

The generic implementation fails for \(K\ge4\), because previously capped cells re-enter the “under-cap” set on later iterations. For example, the stress test produced 179 violations in 20,000 valid \(K=4\) cases. It also mishandles infeasible \(c<1/K\): it can return a vector whose probabilities do not sum to one, while the current certifier fails to notice because it checks neither simplex sum nor nonnegativity.

Use a persistent active set:

```text
free = all non-modal classes
remaining = 1 - c
while free:
    scale = remaining / sum(base[free])
    over = {k in free: scale * base[k] > c}
    if over is empty:
        q[free] = scale * base[free]
        break
    q[over] = c
    remaining -= c * len(over)
    free -= over
```

Reject \(c<1/K\), and add simplex/nonnegativity checks to both certifiers.

The central chain7 arms `chen/perm/perm_mode` do not use these projections, so this does not require delaying those jobs. It does require stopping or discarding the current invalid `pmmx` rerun.

## 5. Exact chain7 pooled analysis

Before launch, decide permutation randomness. My recommendation under the existing budget is to pair optimizer seeds with separately chosen permutation seeds:

```text
opt 2000 → perm 1000
opt 2001 → perm 1001
opt 2002 → perm 1002
```

Use the same permutation seed across evaluator folds for that optimizer replicate. This estimates combined optimizer-plus-permutation variability, although three paired replicates cannot decompose the two sources. If all runs retain `perm_seed=1000`, every residual-shape conclusion must say “conditional on one realized permutation.”

### Validation

For each criterion separately:

- Require exactly seeds `{2000,2001,2002}` × folds `{0,1,2}` × the required arms.
- Exclude folds 3–5 from the balanced estimate.
- Verify `split=0`, evaluator identity per fold, item IDs/order, group IDs, target raters, and prediction dimensions.
- Join losses by stable item ID rather than assuming row order.
- Refuse incomplete cells.
- Freeze the common-map roster now; use the planned balanced set `{hard, chen, perm, perm_mode, sordm}` and equal arm weights. Do not let its value change as arms arrive.

### Calibration

For each optimizer seed × evaluator fold:

- Raw: \(T=1,\lambda=0\).
- Common: fit one \(T,\lambda\) on calibration predictions pooled with equal weight over the frozen arm roster.
- Arm-specific: fit separately for every arm.
- Recompute \(p_0\) from the appropriate calibration target panel.
- Give grid ties deterministically to the map closest to identity, e.g. smallest \(|\log T|\), then smallest \(\lambda\).

This is the natural replicated extension of the existing per-fold map: calibration is shared across arms, but not across independent optimizer runs.

### Point estimator

First average items within group:

\[
d_{sfg}=\frac{1}{|g|}\sum_{i\in g}
\left[\ell(P^a_{sfi},y_{fi})-\ell(P^b_{sfi},y_{fi})\right].
\]

Then use equal seed, fixed-fold, equal-group weighting:

\[
\widehat\Delta=
\frac1{3}\sum_s\frac1{3}\sum_f\frac1G\sum_g d_{sfg}.
\]

Commit groups are effectively singleton items. Keep What and Why completely separate; do not produce a pooled “commit” effect.

### Crossed bootstrap

Use at least 10,000 draws and, for every draw:

1. Sample three optimizer-seed indices with replacement.
2. Sample calibration groups with replacement.
3. Recompute \(p_0\), refit common and arm-specific calibrators on that calibration resample, and apply them to test predictions.
4. Independently sample test item groups with replacement.
5. Use the same calibration/test draws for all arms, folds, estimands, and contrasts.
6. Average all three evaluator folds without resampling them; they are fixed evaluators.
7. Save raw, common, arm-specific, and `common − raw` contrasts.

Report:

- pooled estimate and percentile CI;
- all three seed-specific estimates;
- fold-specific estimates descriptively;
- fitted \(T,\lambda\) by cell and bootstrap boundary-hit rates;
- exact `n_seed`, `n_fold`, `n_group`;
- whether permutation randomness was varied.

For `perm − chen`, freeze an equivalence margin now. My recommendation is \(\epsilon=0.002\) normalized RPS, with a 90% bootstrap CI wholly inside \([-.002,+.002]\) for TOST. If that margin cannot be scientifically defended independently of the observed results, report sensitivity bands at `.001/.002/.003` and retain “no detected degradation” rather than claiming equivalence.

Inference should be primary for raw RPS. Common and arm-specific results get the same CIs but remain sensitivity/deployment estimands. With only three seeds, show the seed estimates prominently; the bootstrap cannot manufacture stable optimizer-population inference.

## 6. Remaining Hour-13 overclaims

Several phrases in [PROGRESS.md](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/PROGRESS.md:350) still need correction:

- **“`perm − chen ≈ 0` … estimand-robust.”** Say the point estimates are small and stable across estimands; equivalence is not established.
- **“The mean-matters effect exists only after calibration.”** This is a significance-comparison error until `calibrated − raw` has its own paired CI.
- **“Every smooth target … indistinguishable.”** The table itself gives `chen − mean2 = +.0007 [+.0001,+.0013]` raw on Why. It is tiny, but not nominally indistinguishable.
- **“Raw RPS penalises hard’s over-confident outputs.”** Currently a hypothesis. Show entropy, calibration slope, fitted \(T,\lambda\), and threshold-level RPS.
- **“The per-arm temperature removes that and exposes the location effect.”** The map includes climatology shrinkage, and “exposes” is mechanistic overreach.
- **“Monotone output map.”** False when \(\lambda>0\); even temperature is not monotone in predicted ordinal mean across arbitrary distributions.
- **“One temperature per fold.”** The implementation fits both \(T\) and \(\lambda\).
- **“Common map … does not reward over-confidence.”** Not established; it merely applies one roster-dependent transformation.
- **“SummEval location effect is robust.”** Say “stable across the three scoring estimands in the currently completed folds”; optimizer and permutation robustness are not yet established.
- **“What = smoothing.”** Use “the benefit survives location destruction and is consistent with a non-item-linked smoothing/regularization effect.”
- **“Certified constrained targets.”** False until violations hard-fail; current `pmmx_v3` outputs already contain violations.
- The common-map column needs CIs. Point estimates should not be narrated as inferentially equivalent to the raw and arm-calibrated columns.
- Replace the ambiguous SummEval header “folds 0–1 / 0” with an explicit fold count in every cell.

The strongest defensible story is now a boundary result: residual ordinal shape showed no detected predictive value under the tested interventions, location was useful in a task- and estimand-dependent way, and nominal residual allocation can matter. That is narrower than “location suffices,” but considerably harder to attack.