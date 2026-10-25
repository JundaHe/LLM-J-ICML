# Verdict

Yes: make the intervention contrasts—not a “best target”—the paper’s headline. For claims about what information a training target contributes, make **raw RPS at \(T=1,\lambda=0\) primary**. Arm-specific calibrated RPS is a legitimate secondary estimand for an end-to-end deployment pipeline, but it is not a clean target comparison.

The strongest defensible conclusion is now:

> On the tested ordinal tasks, item-specific location sometimes matters, but linking residual histogram shape to the item provides no detected RPS benefit and can act as harmful complexity. On nominal ChaosNLI, the allocation of nonmodal mass is item-linked and useful.

Do not retain “mean-preserving permutation never hurts” literally, and do not yet call BW “overfitting” as an established mechanism.

## 1. Calibration

Use three explicitly named estimands:

| Estimand | Transformation | Role |
|---|---|---|
| Raw target effect | \(T=1,\lambda=0\) for every arm | **Primary target/intervention comparison** |
| Common-map sensitivity | one prespecified \(T,\lambda\) for every arm | Tests whether a common output transformation changes the conclusion |
| Arm-optimized pipeline | separately tune \(T,\lambda\) per arm | Secondary deployment estimand |

The current arm-specific result compares **target + separately selected calibrator**, not targets alone. Calling it “deployed pipeline” is valid only if independent recalibration of every candidate arm is genuinely part of deployment.

A read-only common-calibrator sensitivity on the existing outputs gives:

- Commit What, Chen − mean2:
  - raw: **+0.00046** — mean2 better;
  - common pooled calibrator: **−0.00016** — near tie/slight Chen advantage;
  - arm-specific calibrators: **−0.00070** — Chen advantage.
- SummEval folds 0–1:
  - raw: **+0.00277** — mean2 better;
  - common pooled calibrator: **+0.00059** — mean2 still better;
  - arm-specific calibrators: **−0.00126** — Chen better.

Thus the SummEval reversal is specifically produced by **arm-specific calibration selection**. On What, even a common nonlinear map can alter the ordering, so “shared calibrator” is useful sensitivity evidence but is not a neutral primary estimand either.

There is no evidence that the procedure systematically penalizes sharper targets. In fact, the raw Chen predictions have lower entropy than mean2 on both datasets, yet arm-specific calibration favors Chen. The more accurate diagnosis is that calibration rewards **calibratability against the target-rater mixture**, which is different from raw predictive quality against the evaluator.

I do not see direct evaluator leakage: calibration and test items are disjoint, and the evaluator is excluded from calibration labels. Under exchangeable raters, mean RPS against the target raters estimates expected RPS against another rater. The remaining issues are:

- Target-rater calibration versus fixed-evaluator testing creates rater-mixture shift when raters are heterogeneous.
- \(p_0\) and \(T,\lambda\) are estimated on the same calibration items. That is not test leakage, but it adds selection variance.
- Calibration is held fixed during the bootstrap, so its uncertainty is omitted.
- Mean2 hits the \(\lambda=0.5\) boundary on SummEval fold 1. Therefore this is not even necessarily each arm’s unconstrained optimum.
- Per-arm calibration is procedurally symmetric but substantively adds different post-training interventions.

Recommendation: raw primary; arm-specific calibrated secondary; common-map results in a sensitivity table. Refit calibration inside the uncertainty procedure or explicitly condition inference on the fitted calibrators.

## 2. Permutations and Buse–Weimer

“Mean-preserving permutation never hurts” does **not** survive as a universal statement. Use:

> Across the tested ordinal configurations, breaking the item–residual-shape link did not increase average RPS; on Why and BW it reduced RPS. These are descriptive non-degradation results, not a universal or equivalence claim.

Why is cleanest: with four target ratings, the 0.1 mean bin effectively matches exact attainable means, so `pmm` preserves mode and mean and improves RPS.

BW is not yet an exact mode-and-mean intervention:

- `pmm` preserves the mode but only approximately preserves the mean.
- `pmmx` preserves the mean exactly, but its exponential retilting does not constrain the original mode. I audited the constructed targets: the declared mode is strictly lost among approximately **24.5% of changed What targets, 9.7% of Why targets, and 1.8% of BW targets**.

So BW supports “permuting/shrinking target detail can improve RPS,” but not yet a pristine residual-shape attribution. Use a constrained projection satisfying both \(E[Y]=\mu_i\) and \(q_{z_i}\ge q_k\).

Do not state that BW proves the histogram “overfits.” The observations are consistent with a complexity/regularization or metric trade-off:

- Full soft has worse RPS.
- Full soft has the best disagreement recovery.
- Therefore it is not globally a bad target; it occupies a different point on an RPS–disagreement Pareto frontier.

The present shrunk-histogram control is inadequate to settle this. With \(n=97\) and \(\kappa\le8\), the maximum prototype weight is only \(8/105\approx7.6\%\). Its tie with soft merely shows that **weak shrinkage** does not explain the simpler targets’ advantage.

The correct controls are:

- shrinkage fractions spanning genuinely strong shrinkage, or \(\kappa\) scaled with \(n\);
- residual-only shrinkage while exactly retaining mode and mean;
- a training-item-count curve at fixed 97-rater targets;
- a rater-count curve at fixed training items.

Only the first two are needed immediately; the curves would identify “small-item overfitting” more convincingly.

## 3. Paper claim

Stopping the search for a best target is correct. SORDm winning What and BW but failing Why, together with calibration-sensitive Chen/mean2 rankings, makes a champion-target conclusion untenable.

Suggested ordinal statement:

> On the tested ordinal panels, removing the item link to residual target shape after retaining the mode and mean produced no detected average RPS penalty. Removing the mean link harmed performance on Why and SummEval but not on What or BW. Distributional gains therefore arise from a task-dependent combination of global regularization and item-specific ordinal location; residual shape can nevertheless improve disagreement ranking in dense panels.

Suggested nominal statement, subject to repairing the control below:

> On ChaosNLI, retaining the modal class and its mass is insufficient: the allocation of remaining probability among the two nonmodal classes is item-linked and improves both KL and residual-allocation recovery.

Avoid:

- “location suffices”;
- “residual shape is noise”;
- “two numbers are the optimal target”;
- “histograms overfit” without qualification;
- “never hurts.”

## 4. Annotation count and Kohli

The correct statement is:

> The incremental benefit of item-linked residual allocation is already detectable at \(m=5\) and shows no monotonic growth from \(m=5\) to \(50\) under the fixed-reference frozen-head protocol.

Separate that from target fidelity. The target-only soft residual correlation rises from 0.54 to 0.81, so additional annotations clearly make the empirical distribution more reliable. What remains flat is the **learned contrast** between soft and the restricted target.

This does not contradict [Kohli’s reported metric-dependent saturation](https://arxiv.org/abs/2605.29797). Kohli studies entropy correlation and KL saturation; your intervention studies the incremental value of minority-class identity after fixing modal class and mass. The refinement is:

> More annotations improve the fidelity of the target distribution, but the downstream marginal value of residual allocation may saturate much earlier than entropy recovery itself. Entropy’s slow saturation does not identify which distributional component causes it.

Do not say you have “explained Kohli.” You have decomposed one candidate component and shown that its learned marginal effect is flat under a different model/evaluation protocol.

## 5. GPU priority

Before further GPU work, repair the mode constraints and add raw/common/arm-specific calibration analysis; both are CPU-side prerequisites.

Then:

1. **Finish SummEval fold 2.** It is running and completes the external expert panel.
2. **Chain7.** Prioritize Chen/perm/perm_mode; hard next; SORDm last. This supplies the missing optimizer-seed evidence for the central intervention.
3. **Focused DeepSeek Why.** This is the highest-value architecture replication of the clearest ordinal location contrast.
4. **ChaosNLI LoRA at \(m=10\).** Valuable cross-regime confirmation, but only after implementing a truly mode-and-modal-mass-preserving `pzc`.
5. **Heads under the LoRA 5/1 protocol and calibrator.** Now mainly diagnostic; it no longer supports the headline once target rankings are demoted.
6. **SummEval SORDm ×3.** A task-specific target ranking no longer justifies the runs.

Drop **SummEval SORDm ×3** and **matched 5/1 heads**. If the matched-head run is nearly free, run it opportunistically, but do not displace the first four. I would also make SORDm the first arm removed from chain7 if time tight.

## 6. Incorrect or overstated table text

### T2b

> “cross-fitted prototypes; exact-mean permutation”

Overbroad. `soft_pmm` is only mean-binned on BW; `soft_pmmx` preserves the mean but does not guarantee preservation of the mode. State the two properties separately.

> “cond \(E[p\mid z,\mu]\)”

Not exact. The implementation uses \(E[p\mid z,\text{floor}(\mu/0.25)]\) and falls back to mean2 for small cells. Rename it “cross-fitted \(E[p\mid z,\mu\text{-bin}]\).”

> “the histogram overfits RPS yet carries disagreement information”

“Overfits” is not identified. Replace with:

> “The full histogram has worse RPS but better disagreement recovery, consistent with a complexity or metric trade-off in the 60-item regime.”

Also clarify that the current BW shrinkage is at most 7.6%, so “shrunk ties soft” is not a strong denoising result.

### T3b

> “post-calibration RPS; CI conditional on one seed”

Incomplete. These are **arm-specific** post-calibration results, and the interval is conditional on one optimizer seed, one item split, the observed evaluator folds, and fixed calibration fits. It contains no seed, evaluator-population, split, or calibration uncertainty.

> “calibration reverses the target comparison”

Accurate only if written as:

> “Arm-specific calibration reverses the comparison.”

A common pooled calibrator leaves mean2 ahead on SummEval by about 0.0006.

The raw result should be primary if this remains a target-comparison table; otherwise explicitly title the table “end-to-end arm-optimized pipeline performance.”

### T5

The most important remaining validity issue is not visible in the table: `rescale_to_c` assigns \(q_z=c\) but does not constrain every other class to be at most \(c\). In the current targets:

- `zc` makes another class strictly larger than the declared modal class for roughly **7.1%, 3.3%, 3.2%, and 2.3%** of training items at \(m=5,10,20,50\).
- `pzc` has strict violations in roughly **0%, 0%, 0.8%, and 1.6%** of mapped items, plus frequent modal ties at small \(m\).

Therefore:

> “pzc − soft”

cannot yet be interpreted as a pure residual-allocation intervention. Project onto the constrained simplex \(q_z=c,\ q_k\le c\), certify violations are zero, and rerun before making the nominal half confirmatory.

> “oracle resid \(\rho\) soft / zc”

“Oracle” is too strong. These use test-item annotations to construct target-only predictors. Rename this column:

> “test-target fidelity: \(m\)-annotation histogram / \(zc\) reconstruction.”

Finally:

> “subsample seed separate from optimiser seed”

is technically true, but the annotation subsample is tied to `isplit`, not independently crossed with item split. That is adequate for descriptive results, not for a formal annotation-count interaction.