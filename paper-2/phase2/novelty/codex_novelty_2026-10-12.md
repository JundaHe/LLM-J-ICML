# Novelty assessment

**Overall: 6.5/10 — PROCEED WITH CAUTION.**

The paper has a defensible contribution, but not as “the first soft-label shuffling audit.” That broad priority claim is contradicted by direct precedents. The strongest novelty is the narrower combination of:

1. decomposing empirical ordinal histograms while preserving each recipient’s mode and exact mean;
2. measuring the realized perturbation rather than treating “permuted” as binary; and
3. applying this audit to learned judges with both ordinal and nominal panels.

## 1. C1: Is the audit design novel?

**Partly. Novelty: MEDIUM.**

### Closest direct precedent

The most important missed prior is Behrens and Zdeborová, [*Dataset Distillation for Memorized Data: Soft Labels Can Leak Held-Out Teacher Knowledge*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ff16a9219e0e6bc5f30c1ed58262addd-Abstract-Conference.html), ICLR 2026. Its supplement explicitly re-shuffles the input–soft-label assignment **within classes**. Thus it preserves the hard class stratum—and, in their fitted-teacher regimes, effectively the top class—while breaking the item-specific association with the remaining soft-label vector. It also ablates individual portions of the soft vector. This is already a training-time intervention asking whether information beyond class identity matters.

That is a serious collision with any claim of inventing “statistic-preserving soft-label randomization.” The delta is that their labels are teacher outputs used to study memorization and leakage, not empirical human histograms; they do not preserve an ordinal mean, perform recipient-specific projection, or report feasibility/dose certificates.

The closest work specifically involving annotator distributions is Gheibi and Ghazizadeh, [*Same Target, Different Basins*](https://arxiv.org/abs/2605.20642). Its shuffled-SLS control permutes annotator distributions across examples, preserving dataset-level disagreement statistics while destroying the example-to-distribution pairing. It is a full shuffle rather than a recipient-statistic-preserving intervention, but it prevents the paper from claiming that such link-breaking controls are absent from learning-from-disagreement research.

Methodologically, restricted permutation is also old: [Ojala and Garriga](https://www.jmlr.org/beta/papers/v11/ojala10a.html) permute features within classes, while conditional permutation importance permutes only within conditioning strata.

### Defensible novelty claim

The novel unit appears to be:

> A donor-replacement audit for empirical human-rating histograms that isolates residual allocation after retaining recipient-specific ordinal location—especially exact mode and mean—with explicit perturbation feasibility and realized-dose reporting.

Do not claim:

- first within-class soft-label shuffle;
- first intervention breaking item-to-distribution pairing;
- first method asking whether information beyond a hard class exists.

## 2. C2: Are the support and dose certificates novel?

**Novelty: MEDIUM.**

The underlying problem is not new. Conditional permutation importance has long recognized that increasingly fine conditioning partitions fragment the permutation space. [Debeer and Strobl](https://link.springer.com/article/10.1186/s12859-020-03622-2) explicitly show that partitions may contain only one observation, making conditional permutation impossible and producing small, random, meaningless importance values. [Strobl et al.](https://doi.org/10.1186%2F1471-2105-9-307) likewise frame conditional permutation as permutation within a conditioning grid.

Therefore:

- “A conditional permutation needs exchangeable alternatives” is standard.
- “Singleton or homogeneous cells weaken a null result” is standard.
- “Support limits interpretation” is not itself novel.

What is less standard and useful here is the operational certificate:

- heterogeneous-cell support;
- realized changed fraction;
- TV among changed items;
- TV over all items;
- zero-TV assignments;
- post-projection dose.

I did not find this exact bundle in distributional-supervision audits. It should be sold as a domain-specific reporting standard and identification discipline, not as a new statistical principle.

One important consequence of removing the commit panels is that the “3–5-rating panels leave little support” finding will rest mainly on HelpSteer2. The commit panels currently provide much of the repeated sparse-panel evidence. Additional five-rater datasets would materially strengthen C2.

## 3. C3: Is the ordinal location finding new?

**Novelty: MEDIUM, provided the claim is narrowed.**

I found no prior paper that directly performs the same controlled comparison:

\[
\text{empirical histogram}
\quad\text{vs.}\quad
\text{item-link disruption preserving exact mode and mean}.
\]

Nearby work does not anticipate that result:

- [Díaz and Marathe’s SORD](https://openaccess.thecvf.com/content_CVPR_2019/html/Diaz_Soft_Labels_for_Ordinal_Regression_CVPR_2019_paper.html) constructs ordinal soft targets from a hard class and label distances. It shows that a fixed ordinal shape can help, but does not compare that shape with residual structure in empirical annotator histograms.
- [Ordinal Label Distribution Learning](https://openaccess.thecvf.com/content/ICCV2023/html/Wen_Ordinal_Label_Distribution_Learning_ICCV_2023_paper.html) and related unimodal-target methods learn or impose ordinal distribution structure without a statistic-preserving audit.
- [Zhang and Çöltekin](https://aclanthology.org/2026.nlperspectives-1.4/) predict graded-rating distributions and disagreement structure; they do not isolate residual information after mode and mean.
- [Metric-Dependent Annotation Saturation](https://arxiv.org/abs/2605.29797) shows that ChaosNLI soft labels contain item-specific information that label smoothing cannot reproduce, but it varies annotator count rather than preserving selected statistics.
- [Distributions In, Distributions Out](https://arxiv.org/abs/2511.14117) shows soft-label advantages over majority-hard training on ChaosNLI, POPQUORN, and CIFAR-10H, without decomposing the distribution.

However, the current C3 wording overstates the evidence. “The benefit is carried by location” sounds like an identified mediation claim. The experiments establish something narrower:

> At the realized perturbation doses, mode-and-mean-preserving replacement produced little detected average degradation on the tested ordinal panels, while mode-only replacement produced a clear penalty on SummEval; this is consistent with location being sufficient for the measured ordinal benefit under these interventions.

Reasons for restraint:

- The SummEval LoRA interval is exploratory, not a prespecified equivalence result.
- Only one split and one base family receive the stronger end-to-end replication.
- The three optimizer seeds are coupled to three assignment seeds, so their contributions cannot be separated.
- Mode-only replacement changes the mean and residual allocation together; it does not independently identify the mean’s causal contribution.
- Head estimates are descriptive and not uniformly positive for mode-only replacement.
- The held-out \(G\times R\) diagnostic did not robustly validate the proposed location explanation.
- ChaosNLI differs simultaneously in dataset, label topology, task, metric, annotation regime, and pipeline. It supports a contrast, not a causal ordinal-versus-nominal conclusion.

## 4. Claim-by-claim ratings

| Claim | Novelty | Closest precedent | Defensible delta |
|---|---|---|---|
| **C1. Statistic-preserving donor-replacement audit** | **MEDIUM** | Behrens & Zdeborová’s within-class soft-label reshuffling; Gheibi & Ghazizadeh’s shuffled annotator distributions | Exact recipient mode–mean preservation, empirical human histograms, ordinal/nominal decomposition, and learned-judge application |
| **C2. Support/dose certificates** | **MEDIUM** | Conditional permutation importance, especially Debeer & Strobl’s fragmentation analysis | A concrete certificate combining support, realized changes, two TV summaries, zero-TV counts, and post-projection dose |
| **C3. Ordinal residual near-zero versus nominal residual penalty** | **MEDIUM** | SORD, ordinal LDL, graded-disagreement prediction, and ChaosNLI saturation studies | First direct residual-allocation intervention I found after preserving exact ordinal mode and mean; empirical scope remains narrow |
| **C4. Three estimands, crossed bootstrap, exact KL projection** | **LOW** | [Csiszár’s information projection](https://doi.org/10.1214/aop/1176996454) and [Owen–Eckles multiway bootstrap](https://arxiv.org/abs/1106.2125) | Careful integration and certification for this audit, but the mathematical and resampling ingredients are established |
| **C5. No two-statistic target universally dominates** | **LOW** | SORD and ordinal label-distribution-learning comparisons | Broader empirical comparison, but heterogeneous non-dominance across tasks is unsurprising and should remain a secondary negative result |

## Prior-work corrections

Two dossier descriptions should be corrected before writing related work:

- The current v2 of *Distributions In, Distributions Out* clearly compares soft with majority-hard targets; I could not verify the dossier’s claimed label-smoothing control in the current methods. Do not attribute that control without checking the final cited version.
- *Quantifying and Predicting Disagreement in Graded Human Ratings* predicts distributional variation and introduces an opposition index; it is not a clean mean-versus-full-distribution training ablation.

Chen et al.’s [distribution-alignment framework](https://arxiv.org/abs/2505.12301), NAPHA, LeWiDi, rating-indeterminacy work, and emotion-uncertainty studies remain contextual rather than novelty-destroying: they motivate distributional prediction or calibration but do not perform the proposed statistic-preserving intervention.

## 5. Recommendation and positioning

### Recommendation

**PROCEED WITH CAUTION.**

The work is publishable as an audit-method paper. At a top AI venue, the main risk is that reviewers view it as a sophisticated conditional shuffle followed by an underpowered null result. The dose certificates and positive control are therefore central, not ancillary.

### Key differentiator

The strongest one-sentence contribution is:

> Existing controls ask whether the example-to-soft-label association matters at all; this audit asks whether its predictive contribution survives after preserving recipient-specific location, and reports whether the attempted residual perturbation was actually feasible and substantial.

### Paper a reviewer will cite against you

The most damaging citation is [Behrens and Zdeborová, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ff16a9219e0e6bc5f30c1ed58262addd-Abstract-Conference.html), because it already performs within-class soft-label reassignment. In the annotator-distribution domain, expect reviewers also to cite [Gheibi and Ghazizadeh](https://arxiv.org/abs/2605.20642).

Both should be cited proactively, with the delta stated explicitly.

### Positioning that maximizes defensible novelty

- Frame the work as a **decomposition audit**, not a new training objective and not a generic permutation test.
- Make exact mode-and-mean preservation the headline; treat ordinary mode-conditioned shuffling as a baseline.
- Present dose certification as defining what a null contrast can mean.
- Say “average predictive consequence under the realized intervention,” not “intrinsic value of disagreement information.”
- Replace “location carries the benefit” with “results are consistent with location sufficiency on the tested ordinal settings.”
- Keep C4 as methodological rigor and C5 as a practical secondary result, not headline contributions.
- Do not claim equivalence without a prospectively specified margin and adequate independent training replications.

## Remaining panel sufficiency

The remaining set is **sufficient for a tightly scoped audit paper, but insufficient for a broad top-venue claim that ordinal histogram information generally reduces to location**.

Its effective breadth is smaller than six names suggest:

- SummEval is the only panel with the replicated end-to-end LoRA block and a substantial mode–mean-preserving dose.
- Scalabrino has moderate dose but only 124 items.
- HelpSteer2 changes only about 28% of targets under pmmx.
- Buse–Weimer and DICES have broad changed fractions but very small TV over all items, approximately 0.068 and 0.036.
- SummEval criteria share documents and should not be counted as independent datasets.
- ChaosNLI supplies a valuable nominal contrast, but only one nominal task.
- Removing commit removes the second application domain, the second LoRA base family, and most of the sparse-panel replication. It does remove an unresolved heads–LoRA discrepancy, making the narrative cleaner.

For a strong submission, add at least one further **end-to-end** panel selected prospectively for high support and nontrivial expected TV, rather than merely adding more frozen heads.

## Recommended additional public benchmarks

1. **POPQUORN offensiveness and politeness.** The offensiveness panel has 1,500 items with 8.7 ratings per item on average; politeness has 3,718 items with 6.7 ratings, both on five-point scales. Raw annotations and demographics are public. This is the highest-priority addition because it offers better residual support and two distinct text judgments. [Paper and dataset](https://aclanthology.org/2023.law-1.25/).

2. **EmoBank.** It contains 10,062 multi-genre sentences, each rated by five annotators on five-point valence, arousal, and dominance scales under reader and writer perspectives; individual ratings are public. Use one perspective and preregister dimensions to avoid treating correlated criteria as independent replication. [Public individual-rating repository](https://github.com/JULIELab/EmoBank).

3. **Conversational Sarcasm Corpus through LeWiDi-2025.** Approximately 7,000 context–response pairs receive 1–6 sarcasm ratings from 4–6 external observers. Use the six-observer subset to satisfy the rating-count requirement, and do not mix speaker self-ratings with observer ratings unless that mixed population is explicitly the target estimand. [LeWiDi-2025 description and public benchmark](https://aclanthology.org/2025.nlperspectives-1.16/).

These additions would restore sparse-panel evidence after removing commit, diversify beyond safety and summarization, and provide a better test of whether the SummEval result survives on ordinal tasks with genuinely usable residual-allocation dose.