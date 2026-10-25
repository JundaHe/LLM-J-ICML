# Bottom line

Do not submit the current package unchanged to ACL/EMNLP main. My forecast is weak reject at main, plausible Findings, and a poor fit for NeurIPS/ICLR unless you add either a genuinely general theory or a new disagreement-learning method. The audit is careful and useful; the present headline is broader than the estimand, the empirical scope is narrow, and Kohli makes the small-panel null substantially less surprising.

## 1. Is the current paper publishable as is?

### Verdict: not at ACL/EMNLP main, in its current form

The strongest rejection would be:

> The intervention only tests whether the model uses residual histogram shape beyond the item’s mode and mean, on 30–55% of training items, in two small SE panels—one of which has essentially no reliable item-level dispersion. A null under that intervention does not establish that the observed soft-label gain is global calibration or regularisation.

That is a claim–estimand mismatch, not merely an external-validity complaint.

Your current permutation preserves the empirical mean. Consequently, a soft-label model could exploit an item-specific shift in expected score relative to the mode and still be unaffected by your permutation. That is item-linked information, even if one does not want to call it “disagreement shape.” The licensed conclusion is therefore:

> We detect no use of item-linked histogram shape beyond mode and empirical mean under the realised partial intervention.

The current conclusion—

> the gain is a global calibration/regularisation effect and is unrelated to which histogram belongs to which item

—is not identified. A mode-only permutation, a class-conditional prototype target, or another intervention that breaks the item–mean association is needed for that claim.

Other likely main-track objections:

- **The “identifiability” contribution is currently an intervention-support result.** Maximum matching feasibility and the two-rater lemma characterize positivity for one particular randomization. They do not characterize statistical identifiability of human disagreement from anonymous, crossed, or sparse panels. Since the frozen support predictor failed out of sample, the remaining contribution is an exact empirical enumeration plus a simple boundary lemma.
- **The evidence base is effectively one useful dataset.** The commit panel supplies the four substantive positive/negative cells. Scalabrino has negative split-half dispersion reliability and only one model family. The nominal “sixth cell” is an analytic two-rater boundary, not a trained experimental cell. Calling this “six empirical cells” or saying the null occurred “in all six cells” is misleading.
- **No assay-sensitivity result.** A reviewer can reasonably ask whether this training setup would produce nonzero \(\Delta_{\text{link}}\) even when item-linked shape information is known to be learnable. MDE is not a substitute for a positive control.
- **No direct disagreement outcome.** RPS against an excluded rating is valuable, but the paper does not yet show whether the models rank items by disagreement, recover ordinal dispersion, or identify contested items.
- **Conditional rather than full uncertainty.** Each split uses one optimizer seed and one permutation draw, with split, initialization, and permutation variation confounded. Random 60/10/30 splits also have overlapping test items; they are not independent replicates. Unless the pooled analysis clusters the same item across every split in which it appears, the pooled CIs are too narrow. The current per-split implementation only bootstraps test items conditional on the fitted calibrator and trained model. See [analysis_v2.py](/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/analysis_v2.py:53).
- **Calibration uncertainty is not propagated.** The code fits the calibrator once and bootstraps only test differences. It also constructs the climatology from the calibration set, whereas the written protocol says training items. See [analysis_v2.py](/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/analysis_v2.py:37). This matters especially for the roughly 19-item readability calibration sets.
- **This is Chen-style, not an exact Chen reproduction.** Chen et al. used full fine-tuning and reported that their components improved KL; you use LoRA, a different learning rate, and a reconstructed adversarial implementation because code was unavailable. That is defensible, but “the adversarial term is inert” must be scoped to your implementation and regimes. [Chen et al. 2025](https://arxiv.org/abs/2505.12301)

MDE should also not be used rhetorically as equivalence. “MDE ≈ .0005” means the procedure had a certain power under its simulation assumptions; it does not imply that the effect is smaller than .0005. If you want a bounded-null claim, preregister a smallest effect of interest and conduct an equivalence or non-inferiority analysis with training and permutation randomness included.

### Does Kohli scoop you?

**Kohli scoops the empirical explanation and two proposed extensions, but not the exact audit.**

[Kohli, *Metric-Dependent Annotation Saturation for Learning from Label Distributions*](https://arxiv.org/abs/2605.29797) already provides:

- the distinction between distributional fit and identifying which items are disputed;
- an annotation-count curve;
- the result that KL saturates earlier than entropy correlation;
- label smoothing as the no-item-specific-information comparator;
- positive evidence that sufficiently dense soft labels contain item-specific information that smoothing cannot reproduce.

Therefore:

- Your proposed smoothing arm is a replication/control, not novelty.
- A Buse-Weimer panel-size curve is an ordinal/LLM/SE extension, not a new question.
- “Small panels do not yield item-level disagreement learning” is now an expected domain replication rather than a surprising discovery.

What Kohli does **not** scoop is:

- label- and location-preserving link randomization;
- explicit treatment intensity and intervention support;
- identity-excluded evaluation with symmetric calibration;
- a causal attribution protocol distinguishing true item links from marginal target shape.

So the instrument survives. The empirical headline does not.

Kohli also exposes an inconsistency in the literature-review conclusion. It is no longer correct to say that every method with item-level evidence puts rater identity, history, or rationales into the input. Kohli reports entropy correlation \(r=.643\) from ordinary soft-label training with dense panels, versus roughly .45–.49 for smoothing. The defensible statement is:

> Rater- or rationale-conditioned methods currently provide the strongest evidence, especially under sparse panels; dense anonymous histograms can also carry item-specific signal.

## 2. Which proposed additions matter?

| Addition | Verdict | Effect on venue outcome |
|---|---|---|
| **(a) Label-smoothing arm** | Necessary baseline, not a contribution | Little by itself. It is needed if you retain the “regularisation” explanation. Use tuned smoothing and a class-conditional empirical prototype, not one arbitrary \(\epsilon\). |
| **(b) Entropy correlation and disagreement AUROC** | Mandatory reporting, not novelty | Improves reviewability but does not change the tier. On ordinal ratings, also report expected pairwise distance or variance; entropy ignores how far ratings are apart. |
| **(c) Semi-synthetic known-signal experiment** | Essential validation of the instrument | Materially improves credibility. It will not by itself turn this into a main-track paper, but its absence leaves the core null vulnerable. |
| **(d) Annotator-conditioned judge** | The only listed addition with clear venue-changing potential | Yes, if upgraded beyond plain ID embeddings and coupled to an attribution design. Plain rater embeddings are old and incompatible with strict LOAO. |
| **(e) SE panel-size curve** | Mostly filler as a headline | Useful as supporting evidence for a theory or method; otherwise it is Kohli-in-SE. Do not spend dozens of LoRA runs making this the centrepiece. |
| **(f) \(\Delta_{\text{link}}\) dose response** | Important for an audit paper | Strong supporting evidence, particularly when combined with the synthetic positive control. It becomes substantive only if you separate intervention coverage from donor distance and estimate across multiple randomizations. |

### How I would implement the controls

For the target-side audit, use a hierarchy rather than only `chen` versus `perm`:

1. **Hard mode:** one-hot \(z_i\).
2. **Tuned label smoothing:** global smoothing around \(z_i\).
3. **Mode-conditional prototype:** the average training histogram among items with mode \(z_i\).
4. **Mode-only permutation:** shuffle full histograms within mode, breaking item-specific mean and shape.
5. **Mode+mean permutation:** your current arm, breaking residual shape only.
6. **True soft histogram.**

This decomposes three different sources:

- global/class-conditional smoothing;
- item-specific expected-score information beyond the mode;
- residual histogram shape beyond mode and mean.

Without the mode-only intervention, you cannot attribute the entire \(\Delta_{\text{soft}}\) to global regularisation.

For dose response, vary two axes separately:

- changed fraction \(\rho\);
- donor distance, such as histogram TV or ordinal Wasserstein distance.

Use several independent matchings at each setting. A single quantity such as mean TV among changed items conflates treatment coverage and treatment magnitude.

For the semi-synthetic control, use two levels:

- an explicit learnable marker as a pipeline unit test;
- a less trivial feature-defined partition of real items, with two histograms chosen to have identical mode and mean but different dispersion.

The audit should recover a monotone \(\Delta_{\text{link}}\) curve as the injected effect and randomized fraction increase.

### What a reviewer will still demand

1. **A large-panel dataset with independent evaluation raters.** DICES-350 should be primary; Buse-Weimer should be the SE replication. DICES is fully crossed and was explicitly constructed for demographic and distributional analyses. Use the 104 quality-filtered raters as primary and all 123 only as sensitivity. [DICES](https://proceedings.neurips.cc/paper_files/paper/2023/hash/a74b697bce4cac6c91896372abaa8863-Abstract-Datasets_and_Benchmarks.html)

2. **Separate training-rater and evaluation-rater panels.** With large crossed panels, train on \(m\) raters and evaluate the learned item distribution against 20–50 entirely unused raters. That directly separates noisy training histograms from a substantially more reliable reference distribution.

3. **Direct, reliability-aware disagreement metrics.** At minimum:

   - Spearman correlation of predicted and reference disagreement;
   - AUROC for a preregistered high-disagreement threshold;
   - ordinal pairwise disagreement  
     \[
     D_i=\mathbb E\left[|Y_i-Y_i'|\right]/(K-1),
     \]
     estimated from distinct rater pairs;
   - performance conditional on mode or mean, so location is not doing the work.

4. **Orthogonal replication factors.** Fix an item split and vary optimizer seeds; fix a model and vary permutation draws; then repeat across item folds. Do not bind split 0 to seed 0 to permutation 0.

5. **Inference that matches the training pipeline.** Use non-overlapping item cross-validation or cluster repeated appearances by item across splits. Nest calibration fitting inside the bootstrap, or cross-fit calibration.

6. **A practical consequence.** For example: at a fixed human-review budget, does the disagreement-aware judge retrieve genuinely contested items better than mean score, model entropy, and hard-model uncertainty? A tiny RPS difference alone will be viewed as technically correct but operationally immaterial.

## 3. Ranked contributions that could support a strong paper

### 1. History-conditioned population-of-raters judge with two-way attribution

**Claim.** Human judgment distributions should be generated by marginalizing rater-conditional predictions,
\[
p(y\mid x)=\int p(y\mid x,h_r)\,dP(r),
\]
where \(h_r\) is inferred from a short rating history or demographics. Two separate interventions establish whether gains come from the item–distribution link or from genuine rater-by-item interactions.

**What would be new.** The basic rater-conditioned architecture is not new. Davani et al. use annotator-specific tasks, Gordon et al. model individual jurors, and DisCo operates on annotator–item pairs. [Davani et al.](https://aclanthology.org/2022.tacl-1.6/), [Gordon et al.](https://arxiv.org/abs/2202.02950), [DisCo](https://aclanthology.org/2023.findings-acl.287/)

History conditioning is also no longer novel by itself: [Opt-ICL](https://arxiv.org/abs/2510.07105) shows that rater demonstrations are crucial, while [DiADEM](https://arxiv.org/abs/2604.08425) explicitly models demographic interactions and reports strong DICES disagreement correlation.

The new contribution would need to be the combination of:

- cold-start generalization to unseen raters from a bounded support history;
- population marginalization over a declared target rater population;
- two-axis, margin-preserving attribution:
  - reassign response vectors across items to break the item link;
  - scramble rater–item interactions while preserving item histograms and rater marginals;
- a four-quadrant evaluation: seen/unseen items × seen/unseen raters.

**Minimal experiment.** DICES-350 and Buse-Weimer. Compare:

- item-only judge;
- history-only/rater-severity baseline;
- additive item+rater model;
- interactive history-conditioned model;
- oracle seen-ID model as a ceiling.

Evaluate per-rater RPS and item-level ordinal disagreement against unused raters. Repeat under both link interventions.

**Main risk.** The apparent gain may be almost entirely a rater intercept or severity effect. If the additive baseline matches the interaction model, you have not learned who disagrees about which item. Also, 100 Buse items may be too few for item generalization.

**Important protocol correction.** Plain rater embeddings and LOAO are incompatible: an excluded rater has no learned embedding. You must distinguish:

- held-out items for known raters;
- unseen raters with a support history or demographics;
- unseen raters with no information, for whom only a population prior is possible.

### 2. A real theory of disagreement learnability under panel design

**Claim.** Which disagreement object can be learned depends jointly on:

- whether ratings are anonymous or identity-linked;
- whether the item–rater graph is fully crossed, connected sparse, or disjoint;
- panel size;
- the target functional: mean, distributional score, entropy, ordinal dispersion, or individual response.

The theory should provide identification conditions and finite-sample lower or upper bounds, with link randomization as an empirical specification test.

**What would be new.** Kohli supplies an empirical saturation curve for anonymous NLI panels. Chen supplies a learning objective. Jury learning and multi-annotator work assume particular identity-rich designs. The perspectivist literature emphasizes preserving variation but does not give a unified design-dependent learnability result; see [Uma et al.’s survey](https://doi.org/10.1613/JAIR.1.12752) and [Plank 2022](https://aclanthology.org/2022.emnlp-main.731/).

A useful theory would distinguish:

- population disagreement \(p(y\mid x)\);
- fixed-panel disagreement;
- rater main effects;
- item-by-rater interaction;
- what each observation design identifies.

**Minimal experiment.** Validate predicted reliability and power curves by subsampling DICES, Buse-Weimer, and ChaosNLI. Always reserve a large independent rater panel as the reference. Compare predicted learnability thresholds with observed performance for hard, KL, and rater-conditioned models.

**Main risk.** Much of the mathematics may reduce to standard multinomial estimation, entropy bias, generalized linear mixed models, or graph connectivity. The current matching formula and two-rater lemma are not sufficient. The theory must yield a non-obvious design recommendation that is empirically correct.

### 3. Noise-corrected direct learning of ordinal disagreement

**Claim.** Instead of asking KL training to incidentally learn disagreement, train a separate head on a low-bias estimand such as expected pairwise ordinal distance or a hierarchical posterior over it. This should recover item-level disagreement rankings from panels of 3–9 raters more efficiently than plug-in entropy.

**What would be new.** Kohli diagnoses metric-dependent saturation but does not provide a sparse-panel estimator. NAPHA predicts entropy strata post hoc, while DiADEM directly penalizes variance error. Thus novelty cannot be “we add an entropy/variance head.” It would need to be:

- an unbiased or bias-corrected target for ordinal panels;
- finite-panel uncertainty weighting;
- a sample-complexity argument;
- integration with a distributional LLM judge.

**Minimal experiment.** From DICES and Buse-Weimer, sample training panels of 3, 5, and 9 raters and retain at least 40–50 raters as reference. Compare hard training, KL, entropy regression, variance regression, and the pairwise ordinal objective. Evaluate correlation, conditional AUROC, and RPS.

**Main risk.** Pairwise disagreement may improve ranking but discard important distributional structure. It may also fail to outperform a simple empirical-Bayes shrinkage baseline.

### 4. Disagreement-aware annotation budgeting

**Claim.** Jointly choose the next item and rater to maximize expected reduction in error of the item-level disagreement map—or the power of a future link-sensitivity test—rather than majority-label accuracy.

**What would be new.** This space is already occupied. ACTOR reports disagreement-aware multi-head active learning with large budget savings; DAAL chooses items based on the discrepancy between model and expected human entropy; ACAL explicitly selects annotators. [ACTOR](https://aclanthology.org/2023.emnlp-main.126/), [DAAL](https://aclanthology.org/2023.findings-acl.658/), [ACAL](https://aclanthology.org/2024.emnlp-main.1031/)

A new contribution would need to jointly optimize:

- which item;
- which rater or demographic group;
- whether to add another label to an existing item;
- a link-sensitive or population-disagreement objective.

**Minimal experiment.** Sequentially reveal entries from the fully observed DICES and Buse matrices. At 5%, 10%, and 20% of the full annotation budget, compare uniform allocation, uncertainty sampling, DAAL-style item selection, ACAL-style annotator selection, and your joint policy.

**Main risk.** This is a crowded area, and retrospective replay on a fixed fully crossed matrix can look artificial. It is probably a separate paper rather than an extension of the current audit.

### 5. Link sensitivity as an evaluation contract and benchmark

**Claim.** Distributional-score improvement alone should never license “learned disagreement.” A valid claim requires:

- an independent-rater target;
- direct item-level disagreement metrics;
- a no-item-link control;
- an assay-sensitivity positive control;
- intervention intensity and dose;
- uncertainty over training and intervention randomness.

**What would be new.** Kohli supplies label smoothing, but not your conditional link intervention. Chen evaluates distributional fit. Davani, Gordon, DisCo, and related methods evaluate predictions without this causal attribution contract. Your contribution would be a common protocol across anonymous-histogram and identity-conditioned methods.

**Minimal experiment.** At least five or six genuinely different datasets, including ChaosNLI, DICES, Buse-Weimer, the commit panel, and a preference/reward-model dataset; at least four method classes and two model families.

**Main risk.** With only the current SE panels, this is an ablation checklist, not a benchmark contribution. It becomes credible only through breadth, released tooling, positive controls, and at least one finding that changes method rankings.

### Where the original five ideas rank

For this project, after the required upgrades:

1. **Mixture/history-of-raters plus two-way attribution**
2. **True panel-design learnability theory**
3. **Disagreement-aware budgeting**
4. **Link-sensitivity benchmark contract**
5. **Rationale-conditioned judge**

Rationale conditioning is last because you do not possess human rationales, and the closest conceptual contribution already exists: Chen et al. show that a few explanations improve approximation of human judgment distributions, while LiveNLI was explicitly built around label variation and explanations. [Chen et al. 2024](https://aclanthology.org/2024.findings-emnlp.842/), [LiveNLI](https://arxiv.org/abs/2304.12443)

LLM-generated rationales would be circular evidence: the model would generate the purported disagreement mechanism and then be credited for learning it. Rationale conditioning becomes attractive only if you collect paired human rationales from people who actually disagree.

## 4. My single bet for 2027

### Bet: a history-conditioned population judge with factorial item/rater attribution

The paper should not be “soft labels fail.” It should be:

> Anonymous histograms confound global smoothing, item-linked distributions, and panel composition. Modeling a population through rater-conditional predictions can recover genuine disagreement—but only when evaluated under crossed item/rater holdouts and interventions that separately break item links and rater interactions.

That gives you:

- a method;
- a mechanism claim;
- a strong negative baseline;
- a positive control for your audit;
- a bridge between LLM-as-a-judge and perspectivist learning;
- direct use of your unusual fully crossed datasets.

### First de-risking experiment

Run DICES-350 first, using frozen LLM representations and small heads—not hundreds of LoRA runs.

Use the 104 quality-filtered raters:

- 80 meta-training raters;
- 24 completely unseen evaluation raters;
- item split approximately 250/50/50 for train/validation/test;
- for each unseen rater, expose 0, 4, 16, or 64 support ratings from training items;
- evaluate that rater on untouched test items.

Compare:

1. item-only population model;
2. history-only rater-prior model;
3. additive item + inferred-rater model;
4. interactive item × inferred-rater model;
5. seen-rater ID model as an oracle ceiling.

Report:

- per-rater log loss or RPS;
- population RPS after marginalizing over the 24 unseen raters;
- correlation with reference ordinal disagreement;
- disagreement AUROC conditional on item mean;
- performance after item-link randomization;
- performance after a constrained interaction scramble preserving item histograms and rater marginals.

The go/no-go criterion should be mechanistic, not merely significant:

- the interactive model must beat both the item-only and additive baselines on unseen-rater query ratings;
- aggregation over unseen raters must improve item-level disagreement recovery;
- item-link and rater-interaction interventions must damage the corresponding outcomes in the predicted directions.

If it only learns stable harshness/leniency, or if its aggregate distribution is no better than the item-only model, stop. In that case, the rater-conditioned direction is another personalization result, not a disagreement-learning paper.

If it passes on DICES, replicate on Buse-Weimer and then use your LoRA budget. That package has a credible ACL/EMNLP-main story. With a formal treatment of the two-way randomizations and panel-design identification, it could also become a plausible NeurIPS submission.