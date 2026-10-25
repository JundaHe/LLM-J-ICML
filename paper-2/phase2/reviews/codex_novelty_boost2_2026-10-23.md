## 1. Novelty and pre-specification

H is a genuine but secondary gain only if it tests a moderator that G does not already encode.

- G measures the magnitude/reliability of residual shape.
- H must concern its organization: conditional on residual reliability and intervention dose, does replicable bimodality predict a larger annotation-side or learner contrast?

If “polarised” simply means large, stable residual variance, reviewers will correctly call it discretized G. Prefer a continuous, pre-defined shape score and test a `shape × reliability` interaction; use the three types only for visualization.

Also avoid “two camps.” Replication of a two-label histogram does not establish stable rater factions without persistent identities and cross-item rater clustering. Call it “replicable bimodality” for ordinal labels and “replicable two-label concentration” for nominal labels. These are not the same construct, so do not pool them or claim that their differing prevalence explains the ordinal–nominal result.

The broad idea of disagreement taxonomies is not novel—there are already analyses of disagreement causes in [NLI](https://aclanthology.org/2022.tacl-1.78/), [subjective annotation](https://aclanthology.org/2023.eacl-main.178/), and systematic rater disagreement [metrics](https://aclanthology.org/2026.nlperspectives-1.6/). The potentially novel piece is connecting independently replicated distributional shape to a statistic-preserving supervision audit.

Freeze, before computing stratified effects:

- Exact mathematical scores/cutoffs, minimum cell sizes, exclusions, primary datasets and one primary interaction.
- Annotation-side outcome and model-side outcome separately.
- Covariates: residual-reliability magnitude, mode/mean cell, entropy, and realized TV dose.
- One ordinal prediction and one nominal prediction; no cross-topology causal claim.
- A timestamped protocol. Because H arose after aggregate results were known, call it a “prospectively specified secondary analysis,” not confirmatory preregistration.

## 2. Statistical traps and fixes

Use three disjoint annotation panels:

1. type/shape estimation;
2. replication or stability assessment;
3. outcome evaluation.

Using panel 2 both to require stability and to estimate A/G selects positive noise and exaggerates effects. DICES and ChaosNLI can support three-way repeated splits; POPQUORN \(m=8\) cannot and should be exploratory only. Repeated cross-fitting improves efficiency but does not cure reuse of the same ratings for selection and evaluation.

Better still, estimate posterior type probabilities with a hierarchical multinomial model and weight items probabilistically rather than hard-classifying them. Report the cross-panel transition matrix; do not discard “unstable” items.

For power and multiplicity:

- Make a continuous interaction the primary test; partial-pool type effects.
- Use an omnibus interaction rather than three separate significance tests.
- Bootstrap items/documents while repeating the rater split and type assignment.
- Predefine a minimum effective subgroup size and report simultaneous intervals.
- Report changed fraction and TV within every type; otherwise “polarised” effects may merely reflect stronger interventions.

Restricting existing judges to independently typed test items is valid as test-side effect heterogeneity, even though training used all types. It does **not** show that polarised training items supply the useful signal. That stronger claim requires type-targeted training interventions or retraining with only one type perturbed. Keep existing LoRA stratification explicitly exploratory.

## 3. Qualitative analysis

Worth appendix space, not a standalone contribution. Use one compact figure or table: 2–3 mechanically selected examples per type, their two independent histograms, and brief rubric-based interpretation. Do not cherry-pick compelling cases or infer causes from ratings alone.

A real content analysis would require a coding scheme, multiple coders, agreement, and enough sampling to estimate category prevalence. That is a second study. Earlier SE examples would increase scope drift; mention them only as motivation, not evidence for these datasets.

## 4. Recommendation

Fold H into A/G as a pre-specified secondary moderator analysis—not a new headline and not a replacement for continuous G. Run it confirmatorily only on dense DICES and ChaosNLI panels; treat POPQUORN and existing LoRA subgroup results as exploratory. Promote it to the main text only if shape predicts outcomes after controlling for reliability and dose with adequate subgroup support. Otherwise retain one appendix figure or drop it.