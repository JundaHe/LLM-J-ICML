# Verdict

The empirical spine is now substantially stronger, but I would veto two phrases as written:

1. Commit Why has shown robustness across partitions and a preliminary second-family check—not “three/four independent replications.”
2. `ordinal_mode_mean` is not yet an exact KL projection. The KKT derivation is correct, but the three fallback cases are genuine suboptimal solutions, not harmless numerical ties.

The central LoRA permutation results remain intact; the solver problem affects solver-dependent `mean2`/`pmmx` heads claims.

## 1. Commit Why language

Recommended paper wording:

> On commit Why, disrupting item-specific location while retaining the modal label increased raw RPS in two follow-up Qwen partitions: +0.0061 [0.0020, 0.0101] and +0.0091 [0.0057, 0.0128]. The corresponding estimate in the original partition was near zero, +0.0005 [−0.0021, 0.0032]. A preliminary run with DeepSeek-Coder on the original partition was concordant, +0.0060 [0.0016, 0.0102], although only two of six evaluator folds were complete. These are robustness checks across three overlapping Qwen item partitions and a second base-model family, with one optimizer-seed setting and one realized permutation per model–partition cell; they are not independent replications.

For calibration:

> Arm-specific calibrated contrasts were positive, with conditional intervals excluding zero, in all three Qwen partitions; calibration therefore changes the split-0 conclusion and is reported as a distinct secondary estimand.

Do not call split 0 an “outlier.” Call this **partition sensitivity** or **between-partition variation**. You can report it without cherry-picking precisely because you show the original result first, show all follow-up partitions, and do not discard it. “Heterogeneity” is defensible descriptively, but a formal heterogeneity claim would require a contrast-of-effects analysis accounting for overlapping items. A standard independent-study heterogeneity test would be invalid here.

Also avoid “the location effect replicated in a second family” until DeepSeek reaches 6/6 folds. For now: “a preliminary concordant second-family result.”

## 2. `ordinal_mode_mean`

The interior KKT derivation is correct:

- Untied classes have \(q_k=s\,b_k e^{\lambda k}\).
- A tied set containing \(z\) shares \(c=sG(\lambda)\), with \(G\) the geometric mean of the tied tilted bases.
- The stated mean equation is correct.
- The KKT inequalities are correctly oriented: untied \(b_ke^{\lambda k}\le G\), tied \(j\ne z\) require \(b_je^{\lambda j}\ge G\).

But the implementation’s fallback is not exact. The three `projected_minkl` cases are all the boundary case \(K=5,z=2,\mu=3\). For one observed base,

\[
b=(.05997,.06751,.42366,.16359,.28527),
\]

the code returns approximately

\[
q=(0,0,\tfrac13,\tfrac13,\tfrac13),\qquad KL=0.20923.
\]

A lower-KL feasible solution is

\[
q=(0,0,.40476,.19047,.40476),\qquad KL=0.15212.
\]

The latter is the optimum with active tie set \(\{2,4\}\). It occurs at the asymptotic boundary \(\lambda\to+\infty\). Because `R(-200)` and `R(200)` have the same numerical sign, the correct active set is discarded by the bracket test. The other two fallback cases have KL gaps of approximately 0.434 and 0.509.

Required fix:

- Handle roots attained at \(\lambda=\pm\infty\), either by constructing the analytic limiting distribution or accepting a sufficiently accurate endpoint after checking the mean and KKT residuals.
- Delete the non-KKT minimum-feasible fallback. If no KKT candidate remains, hard-fail.
- Add these three cases as regression tests with objective-value assertions.
- Regenerate every v4 target and compare it with the fixed solver’s target. Rerun training only where targets differ.
- Log `projected_minkl`/boundary counts per actual panel, not only constraint violations.

The 9,000-case test established feasibility, not optimality. The random brute-force test was unlikely to find optima on lower-dimensional boundary faces, so it did not cover this failure.

Even after fixing it, the most precise label is:

> deterministic KKT active-set KL projection, constraint- and optimality-certified to numerical tolerance, relative to the \(10^{-9}\)-floored base distribution.

Literal “exact KL projection onto the original base” is also complicated by clipping zero base probabilities and accepting equality within `TOL`.

## 3. Abstract core

> Distributional supervision is often interpreted as teaching an LLM judge how people disagree. We audit that interpretation by replacing each training histogram with a donor histogram while preserving selected item-level statistics. Across the ordinal panels tested, mode-and-mean-preserving donor replacement produced near-zero average RPS contrasts in the evaluated LoRA configurations and frozen-feature heads, indicating little measurable predictive value from residual histogram allocation under these designs. Disrupting location while retaining the mode degraded prediction under all three scoring pipelines on SummEval and in two of three overlapping Qwen partitions on commit Why; the original partition was null in raw predictions, while calibrated estimates were positive across all three. No corresponding location penalty was detected for commit What, whose soft-label gain was consistent with non-item-linked smoothing or regularization. In a separate nominal NLI study, constraint-certified scrambling of residual class allocation while preserving modal class and mass degraded prediction. Thus soft-label training did not uniformly recover the full disagreement distribution: useful information depended on task and label geometry, and no single constructed target dominated across panels and scoring estimands.

Do not say location “destroyed the gain” on commit Why: under raw RPS, `perm_mode` often remained better than hard. It explains part of the Chen advantage, not necessarily all of it.

## 4. DeepSeek versus chain7

Start chain7 now. Stop DeepSeek after the currently near-complete fold, if abandoning that fold would waste little time; otherwise preempt f2–5.

The remaining DeepSeek folds add evaluator coverage under the same partition and optimizer seed. The SummEval chain7 block attacks the more damaging weakness: optimizer/permutation randomness in the cleanest headline experiment. Resume DeepSeek afterward and keep its current partial row out of the main evidentiary claim until 6/6.

One terminology correction: the paired mappings `2000→1000`, `2001→2501`, `2002→2502` are independent **joint seed realizations**, not orthogonal or crossed optimizer/permutation factors. Their effects cannot be separated.

Also, the current [analysis_chain7.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_chain7.py:1) is commit-specific. Freeze a SummEval version before inspecting chain7 output: balanced seeds × expert folds, document-clustered test resampling, calibration-document resampling with refitting, and the same three-arm common-calibrator roster for every seed.

## 5. Hour 16 / T3 vetoes

Beyond the solver claim, I would change five things:

- Replace “replicates” in the Hour 16 heading with “reappears across follow-up partitions and a preliminary second-family run.”
- Replace “split-0 feature/outlier” with “partition sensitivity.”
- Replace “the null holds in 4/4” with “the estimated mode-and-mean-preserving contrasts were near zero in all completed configurations.” No prespecified equivalence claim is available.
- The T3 header says six folds per split, but the DeepSeek `perm_mode` contrast has 2/6. Put “preliminary; 2/6 folds” prominently in the caption, or omit that row until complete.
- Show the conditional CIs for the headline `perm − chen` contrast; omitting them while claiming a near-zero contrast invites criticism. They are reassuring: approximately [−.00027,.00044] for What s0; [−.00072,.00031], [−.00080,.00030], and [−.00044,.00048] for Qwen Why s0–s2; and [−.00125,.00035] for preliminary DeepSeek.

Two technical table notes also matter:

- Arm-calibrated intervals in T3 condition on fixed fitted calibration maps, just as T3b now states.
- The “common map” is fitted over all arms present. Because s0 has more arms than s1/s2, its calibrator roster changes across rows. Recompute it using a fixed intersection roster—preferably `{hard, chen, perm, perm_mode}`—before comparing common-map estimates across partitions.

With those changes and the solver boundary fix, I would accept the revised spine.