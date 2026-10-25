# Verdict

**No—not yet.** The project now has a plausible ACL/EMNLP-main contribution, but the current manuscript is still a **weak reject at main and a credible Findings paper**. The attribution hierarchy is substantially stronger than yesterday’s paper. The constructive “two-number target” claim and the inference are not yet sound enough.

There is also a consequential sign error in the current interpretation:

> Commit *What*: `chen − mean2 = −0.0007 [−0.0013, −0.0001]`

Because lower RPS is better, this means **Chen beats mean2 by 0.0007**, not the reverse. The raw means confirm it:

| arm | RPS, *What* s0 |
|---|---:|
| chen | **0.099720** |
| perm | 0.099853 |
| perm_mode | 0.100256 |
| mean2 | 0.100421 |
| proto | 0.100619 |
| hard | 0.101354 |

Likewise, `chen − proto = −0.0009` means Chen beats proto. Thus the sentence “the histogram never beats its (mode, mean) summary” is false in the current central LoRA table. See [the actual analysis JSON](/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/results_v2/what/s0/analysis_v3.json).

The supported interpretation is more interesting but narrower:

> On *What*, item identity of the residual shape is not needed—permuting shape conditional on mode and mean is inert—but the particular exponentially tilted mean2 target does not reproduce the full histogram’s benefit. Some item-independent or randomly assigned target-shape effect remains.

That is not the proposed smoothing + mean decomposition unless you add a third component: **marginal/random target-shape regularisation**.

## 1. Main-track verdict and rejection reasons

### Most likely rejection reason

**The headline is stronger than the identified result.**

Your interventions support:

> No detectable average use of the link between an item and its residual histogram shape, under the realized interventions and model classes.

They do not support:

> Residual shape is never used, shape is noise, or a particular two-number target always substitutes for the histogram.

The *What* LoRA result directly contradicts the last statement. In addition:

- Null CIs are not equivalence tests.
- `soft_pmm` preserves mean only approximately on BW and DICES.
- The “~100 raters” threshold is inferred from different datasets rather than a within-dataset panel-size curve.
- The positive control injects an especially easy signal along PCA-1.
- Most natural panels contain little reliable residual-shape signal, so invariance is unsurprising.

### Second most likely rejection reason

**The uncertainty intervals condition on nearly all important training randomness.**

The bootstrap captures test-item sampling conditional on one trained model per arm, one optimizer seed, one permutation, one item split, and one calibration fit. Effects of \(7\times10^{-4}\) to \(3\times10^{-3}\) are exactly where optimizer, split, calibration, and permutation variation can reverse conclusions.

The six LORO folds do not provide six optimizer replications: they are six related training/evaluation problems on the same test items. SummEval fold 0 is one evaluator, one split, one seed.

Novelty would be my third concern, but it is survivable if you sell the work as an **attribution audit**, not as the invention of a new ordinal target.

# 2. Novelty threats

| Threat | What it pre-empts | What it does not pre-empt | Required neutralisation |
|---|---|---|---|
| **SORD, Díaz & Marathe 2019** | Target-side ordinal softening, KL/cross-entropy against an exponentially shaped ordinal distribution, and the idea that a full soft vector can be generated from a small number of label-side parameters. [SORD](https://openaccess.thecvf.com/content_CVPR_2019/html/Diaz_Soft_Labels_for_Ordinal_Regression_CVPR_2019_paper.html) | It starts from a hard ordinal label and a fixed distance function. It does not condition on an empirical panel mean, audit human-histogram links, or decompose smoothing/mean/residual shape. | Add tuned `SORD-mode` and the obvious `SORD-mean` adaptation, plus a discrete Gaussian centered at the empirical mean. If they tie mean2, stop presenting mean2 as a method contribution. Frame it as an information-preserving control. |
| **Geng’s label-distribution learning** | Learning full label distributions with distributional losses; broad claims that soft-label/KL training itself is new. Geng explicitly includes distributions aggregated from multiple labeling sources. [LDL](https://arxiv.org/abs/1408.6027) | It does not give your constrained link randomizations or ask which sufficient statistics of an annotator histogram drive downstream gains. | Cite LDL as the parent paradigm. Compare against a standard Gaussian/LDL target and an empirical-Bayes-shrunk histogram. Claim novelty only for attribution and the empirical sufficient-information question. |
| **Unimodal/adaptive ordinal targets** | “A compact parametric distribution is enough for ordinal prediction” and much of the two-parameter-target rhetoric. Prior work uses Poisson/binomial, beta, Gaussian, learned mean/variance, and adaptive unimodal distributions. [Beckham & Pal](https://proceedings.mlr.press/v70/beckham17a.html), [Li et al.](https://openaccess.thecvf.com/content/CVPR2022/html/Li_Unimodal-Concentrated_Loss_Fully_Adaptive_Label_Distribution_Learning_for_Ordinal_Regression_CVPR_2022_paper.html) | These methods do not demonstrate that empirical human residual shape is unused, nor separate item-linked information from regularisation. | Benchmark SORD, discrete Gaussian, binomial/Poisson, scalar mean regression with calibrated ordinal likelihood, and mean2. Include a dense-panel/bimodal stratum where unimodality is genuinely wrong. |
| **Kohli 2026** | Smoothing versus item-specific soft-label information, annotation-count saturation, dense-panel evaluation, and the practical annotation-budget story. Kohli already uses five model seeds, five annotation subsamples, three splits, and two architectures. [Kohli](https://arxiv.org/html/2605.29797v1) | It does not perform your constrained target-link randomization or ordinal mode/mean decomposition. | Do not say you “explain Kohli” without testing ChaosNLI. Run the nominal analogue: mode + majority probability versus residual allocation among minority classes. |
| **Your Phase-1 audit** | The mode+mean-preserving permutation, certificates, LORO evaluation, and the basic “distributional gain need not mean disagreement learning” argument. | The mode-only arm, explicit mean control, cross-domain extension, and constructive target are new relative to Phase 1. | If Phase 1 is unpublished, merge the papers. If published/submitted, treat its permutation as prior work, not contribution 1. Lead with the new nested intervention and the corrected decomposition. Avoid counting the same commit cells twice as independent evidence. |

The mean2 construction itself is a standard information projection/exponential tilt of a base distribution under a moment constraint. Its mathematical form should not be sold as algorithmic novelty.

# 3. Statistics and replication

## Is the current bootstrap defensible?

**Only as a conditional test-item CI.**

Averaging the per-item differences over LORO folds and then resampling item/source-document clusters is sensible for the fixed-panel estimand, because it keeps the same item’s six evaluator outcomes together. This handles the “same test items across folds” issue better than treating folds as independent.

It does not cover:

- optimizer initialization and minibatch order;
- item-split variability;
- permutation-draw variability;
- evaluator/rater-population variability;
- calibration-set and calibration-grid uncertainty;
- model-family variability.

Calibration should be refit inside a nested bootstrap or cross-fitted. If you want to generalize beyond the six observed raters, use a crossed item × rater bootstrap, while acknowledging that six raters give weak rater-population inference.

For null claims, preregister a smallest effect of interest and conduct equivalence tests. “CI includes zero” does not license “inert” or “costs nothing.”

## Minimum replication

The minimum I would submit for the primary LoRA claims is:

- **3 optimizer seeds × 3 grouped item splits × 2 genuinely different model families**, with families reported separately;
- all available evaluator folds;
- **at least 3 independent permutation mappings** for each permutation contrast, crossed with optimizer seed rather than tied to split;
- one prespecified primary metric and contrast.

Given the sub-0.001 *What* effects, **5 seeds × 3 splits × 2 families** is safer and matches the replication standard set by Kohli more closely.

Currently, `split` determines item partition, optimizer seed, and permutation seed simultaneously. Those factors need to be orthogonal.

## Numbers I would and would not trust

I would trust directionally:

- Why `perm_mode − chen > 0` on s0 and s1;
- the repeated near-zero pmm pattern as descriptive evidence;
- the large injected positive-control effects, but only as an easy pipeline unit test;
- mean2/proto differences in the heads when they are large.

I would not treat as confirmatory:

- either CI for `chen − mean2` on commit s0;
- the SummEval fold-0 CI;
- precise “14% learned fraction” ratios;
- the `~100 raters` threshold;
- SEMs over the heads’ 30 configurations as if those were 30 independent replicates;
- the general Stage-A “no interactions” conclusion;
- any “8/8” claim as formal equivalence.

The head configurations reuse three item splits and two rater splits; their SEMs substantially overstate the effective replication count.

# 4. Protocol audit

## Mean2 construction

There is **no test leakage** in the normal sense:

- the evaluator rater is excluded;
- prototypes are estimated from `tr_idx`;
- only training-item targets are optimized.

But there are four concerns.

1. **Self-inclusion.** Each training item contributes its own histogram to its mode prototype. This is not leakage, but the target is not strictly a function of only that item’s \((z,\mu)\) plus independently estimated population information. Use leave-one-item-out or cross-fitted prototypes.

2. **Unequal denoising.** Mean2 receives pooled empirical-Bayes-like shrinkage; soft receives the raw noisy histogram. Therefore mean2 beating soft could mean “shrinkage helps,” not “mean is sufficient.” Add a matched shrunk-full-histogram arm:
   \[
   \tilde p_i=\frac{n p_i+\kappa \bar p_{z_i}}{n+\kappa},
   \]
   with \(\kappa\) tuned on validation data.

3. **The tilt need not preserve the mode.** In a split-0 audit, the mean2 distribution’s argmax differed from the empirical mode for about **11.9% of commit What** and **11.7% of BW** training items. The target is determined by \((z,\mu)\), but it does not necessarily possess mode \(z\). Either rename it a “\((z,\mu)\)-constructed target” or solve the constrained projection with both \(E[Y]=\mu\) and \(p_z\ge p_k\).

4. **The chosen target is arbitrary.** The natural optimal two-number baseline under cross-entropy is a cross-fitted estimate of
   \[
   E[p_i\mid z_i,\mu_i],
   \]
   not necessarily “tilt \(E[p_i\mid z_i]\).” This conditional prototype is especially feasible for small panels, where means lie on a discrete grid. It may fix the *What* failure.

## Adversarial term

Applying the same adversarial operator to soft, mean2, and proto is fair if the question is:

> Which base target works best inside our reconstruction of Chen’s complete objective?

It is not clean for the information decomposition. The adversarial target depends on the item-specific model prediction \(q_\theta(x_i)\), so a proto or mean2 arm can acquire item-specific residual shape during training even though its human-derived base target lacks it.

Run the target × adversary factorial:

- `soft0`, `mean2_0`, `proto0`;
- `soft_adv`, `mean2_adv`, `proto_adv`.

Your current `chen0` result only establishes that the adversary is small for the soft target, not that its interaction with mean2/proto is negligible.

## Permutation fidelity

For the sparse panels, \(\tau=.1\) generally implies exact means because possible means are farther apart. On BW and DICES, it does not:

- BW pmm average mean shift is about **0.033**;
- DICES about **0.031**.

Call these mean-binned, not mean-preserving. For the positive control, an observed pmm effect on BW could partly reflect mean perturbation. Either match exact sums, or swap residuals and then project them back to the recipient’s exact mean and mode.

## PCA-64 heads

Yes, this biases the study toward mean-only conclusions. Mean/location is typically easier to predict than higher-order distribution shape, and unsupervised PCA preserves feature variance rather than shape-predictive directions.

The current positive control does not settle this because the injected label is explicitly keyed to PCA-1—the easiest possible signal for that representation.

The decisive capacity control is:

- full-dimensional frozen features;
- head-width/rank sweep: 64, 256, 1024, full;
- a supervised residual-shape probe on the dense natural panel;
- ideally end-to-end training on a dense panel where the independent-rater oracle gap is nonzero.

If a full-capacity probe predicts held-out residual shape but soft-label training remains pmm-invariant, the mechanistic conclusion becomes much stronger.

# 5. Highest-value experiment for five GPU-days

Run a **direct, replicated extension of Kohli on ChaosNLI**, using the nominal analogue of your decomposition.

For three classes, decompose each histogram into:

1. modal class \(z_i\);
2. modal probability \(c_i=p_i(z_i)\);
3. allocation of the remaining mass between the two nonmodal classes.

Then compare:

- hard;
- class-conditional prototype;
- a cross-fitted \((z,c)\) target;
- full histogram;
- mode-only permutation;
- mode+\(c\)-preserving permutation.

Use independent training/evaluation rater panels from the 100 annotations, and subsample \(m\in\{5,10,20,50\}\). Evaluate distributional fit, entropy ranking, and recovery of the minority-allocation residual.

Replication:

- three item splits;
- three optimizer seeds;
- two architectures matching Kohli if feasible;
- independent permutation seeds.

This experiment does four things simultaneously:

- directly neutralizes the closest prior work;
- supplies a dense natural NLP panel;
- tests whether “two numbers” generalizes beyond ordinal scales;
- reveals whether Kohli’s slow entropy saturation comes from majority mass or genuine residual shape.

If residual allocation matters, narrow the paper honestly to ordinal panels. If it does not, you have a genuinely strong main-track result.

Finish the already-running three SummEval folds, but stop spending time on:

- more sparse SE panels;
- further PCA-head panels;
- Stage-A rater conditioning or demographic variants;
- additional single-seed model-family checks;
- dose-response refinements before the central result has orthogonal seed/split replication.

# 6. Overclaims in `PAPER_OUTLINE.md`

The following need revision.

| Current sentence | Licensed version |
|---|---|
| “the item-level information a soft label transmits is its **mean**” | “When we detect item-linked information beyond the mode, it is largely associated with the empirical mean; we detect no average benefit from linking residual shape to the correct item.” |
| “permuting histograms across items while preserving mode and mean costs nothing” | “We detect no degradation under the realized mode-and-mean-conditioned permutations; equivalence remains to be established over training and permutation randomness.” |
| “permuting while preserving only the mode destroys the soft-label gain and makes soft labels worse than hard labels” | “This occurs on commit *Why* in two split-seed configurations; on *What*, the gain survives mode-only permutation and is therefore not item-linked.” |
| “a target built from (mode, mean) alone matches the histogram everywhere” | “The target matches the histogram on *Why* and beats it in SummEval fold 0, but is worse than Chen on commit *What* by 0.0007 RPS.” |
| “shape beyond the mean only becomes recoverable at ~100 raters” | “A substantial independent-panel residual-shape advantage appears on the one 121-rater five-level panel; the available datasets do not identify a rater-count threshold.” |
| “The results reinterpret Kohli et al. … KL saturates … because the mean does” | “Our ordinal results suggest a possible location-versus-shape account of differential saturation; testing that account on Kohli’s nominal ChaosNLI setting remains future work.” |
| “soft-label gains are mean-carried” in Contribution 2 | “Gains are class-conditional-smoothing-carried on some tasks and mean-associated on others; item-linked residual shape has no detected benefit.” |
| “mean2 … beats tuned label smoothing — so the gain is item-specific information” | “Mean2 beats uniform smoothing in the heads, but the mode-conditional prototype and permutation arms are required to determine whether the gain is item-specific.” |
| “soft_pmm − soft ≈ 0 ⇔ residual shape is not used” | “A sufficiently powered pmm null is consistent with no average use of the item–residual-shape link; it is not an iff identification result.” |
| “with ≤6 raters the moves are infeasible, i.e. there is no shape to carry” | “Our particular pair-move injection is often infeasible with ≤6 ratings; this does not prove that distinct histograms with the same mode and mean do not exist.” |
| “the histogram's best-case advantage” | “the observed cross-panel advantage of the raw training-rater histogram over the chosen mean2 estimator.” “Oracle” is misleading because both are noisy estimators. |
| “on a 3-level scale … disagreement is a deterministic function of the mean” | “On DICES, disagreement is empirically almost determined by the mean.” It is not true by construction: \(p=(0,1,0)\) and \(p=(.5,0,.5)\) both have mean 1 but different pairwise disagreement. |
| “proto beats Chen’s histogram target” in R1 | “Chen beats proto by 0.0009 RPS on *What*.” This is a sign correction. |
| “the item-specific part of the histogram is noise that costs ≈0.0008” | “The correct item–shape link is unnecessary under pmm, but the chosen deterministic proto/mean2 targets underperform Chen; the difference may reflect marginal target shape, shrinkage, or optimization.” |
| “three raters per item already pin the mean well enough” | “In the examined three-rater HelpSteer subset, mean2 and soft are similar; a within-dataset annotation-count experiment is needed for a budget recommendation.” |
| “Spending the budget on more items rather than more raters per item is the better trade” | “Our results motivate testing this allocation trade-off; they do not evaluate it.” |
| “Any claim … should (i) survive a mode-and-mean-preserving permutation” | “Any claim of residual-shape learning should show a prespecified degradation under a mode-and-mean-preserving permutation; invariance rules that claim out.” |
| “Identity buys severity, not item-specific disagreement.” | “With frozen-feature heads on DICES and BW, the tested interaction model provides no detectable benefit beyond an additive severity component.” |

I would also change the title until the *What* contradiction is resolved. A defensible current title is:

> **What Distributional Judge Training Uses: Separating Smoothing, Item Means, and Residual Shape**

The paper’s strongest result is now the nested attribution audit. Make the two-number target a tested consequence, not the premise.