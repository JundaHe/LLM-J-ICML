My ranking is **paper 4 > paper 2 ≫ paper 3**. The probabilities below are subjective judgments of the supplied evidence, including the completed SAP update. I give no credit for pending Stage 8 results.

**1. Paper 2 — estimated ICML acceptance probability: approximately 35%.**

- Separates disagreement shape’s reproducibility across raters from its predictability using frozen text representations (§2).
- Finds that substantial shape replacement barely affects ordinal judges, while NLI provides a useful positive contrast (§3).
- Connects these measurements to rater thresholds and task-dependent annotation-budget results (§§4–6).

**Single biggest weakness: the explanatory story exceeds what the measurements establish.** Frozen linear nondecodability supports a statement about these representations and probes; it does not establish that reproducible disagreement is absent from text. The stronger wording in §3 and the opening explanation of §5 overreach that distinction. Moreover, the ChaosNLI prediction fails, and POPQUORN LoRA does not support the proposed items-first ordering (§5). The paper has a credible empirical audit, but its mechanism and budget findings should stand as separate, qualified contributions.

I would also ask §2.1 to justify interpreting \(X/M\) as reliability and \(M-X\) as sampling noise separately from establishing the scoring identity: the comparator depends on panel 1’s noisy location. The identity itself does not settle that interpretation.

**2. Paper 3 — estimated ICML acceptance probability: approximately 10%.**

- Maps an existing judge’s score to a target population’s ordinal rating distribution, without retraining the judge (protocol, “The mapping used throughout”).
- Shows useful adaptation on several large DICES-990 shifts, but inconsistent performance on small shifts and small calibration sets (G1 summary v2).
- Plans black-box judge calibration and disagreement prediction; the supplied evidence for those components remains preliminary (G2–G3; HANDOFF §C).

**Single biggest weakness: insufficient differentiation from standard ordinal calibration.** Ordered-probit mapping, hierarchical shrinkage and rater thresholds are established tools. The current results do not yet establish a new principle or a consistently superior deployment procedure. For example, map-B(50) worsens the DICES-990 random-halves row by 0.0032 RPS, while performing very well on some large race/locale shifts (G1 summary v2). That is potentially useful applied calibration research, but currently a thin standalone ICML contribution.

The strongest version would explain **when adaptation should be attempted and when retaining the original calibration is preferable**, with that decision validated on untouched populations.

**3. Paper 4 — estimated ICML acceptance probability: approximately 45%.**

- Tests unseen-rater personalisation against a simple scale-use baseline, separating likelihood improvements from ranking improvements (§§4–6).
- Finds substantial calibration gains but little ranking gain, including on native PRISM choices; positive controls expose limited sensitivity of the tested learners (§§5.6, 6).
- SAP now recovers semantic injections, but real MultiPref gains remain small: +0.17 direction points, CI [−0.19, +0.55], over population weights (Stage 9 update).

**Single biggest weakness: the credibility of the broad negative conclusion depends on inadequately validated baseline fidelity.** VPL, PAL and LoRe are adapted implementations, and their native published gains were not reproduced (§9; Appendix B). LoRe’s reversal—from a published improvement to deterioration even in the attempted native setting—is particularly consequential. A reviewer can reasonably attribute part of the ranking null to implementation, representation or optimisation differences.

Your transparency helps considerably. It does not resolve that alternative explanation. The defensible conclusion concerns **the tested implementations under this protocol**, with stronger generalisation requiring additional validation.

**Paper 4 is the strongest ICML candidate.**

Its question has clearer consequences for current ML practice: does personalisation learn what to show a particular person, or mainly how that person expresses a judgment? The scale-use baseline, native-choice evaluation and constructive positive controls form a coherent investigation (§§4–6).

Paper 2 is more mature, but its central tools and practical conclusions overlap more heavily with established reliability analysis, probing and annotation-budget research. Paper 4 has the stronger opportunity to change evaluation practice. SAP also supplies a constructive response to the failure it diagnoses.

The difference is modest: unresolved baseline fidelity could readily make paper 2 the safer submission.

**For paper 4, novelty is sufficient in principle for an analysis-led ICML paper, but currently borderline.**

An ICML paper does not need a new optimiser. A consequential finding established through unusually convincing experiments can suffice. Here the promising contribution is the separation of **scale use, content-dependent prediction and decision-relevant ranking**.

The individual ingredients are not strong novelty claims: rater offsets, unseen-user adaptation, permutation controls, hierarchical random coefficients and Laplace-EM/ARD all have established precedents. Your related-work section correctly acknowledges much of this (§2).

The SAP update strengthens the paper, but also requires a more precise framing:

- **The constructive result is substantial.** SAP gains +2.69 direction points on sem5 and +7.53 on sem10 over population weights, approximately reaching the known-feature reference learner’s reported performance (Stage 9 update; Appendix B, S7-4).
- **The real-data result supports a small content-dependent probability improvement.** The LL column is multiplied by 100: +0.22 means **+0.0022 nats**, CI [+0.0003, +0.0041], over population attribute weights. Thus “most improvement is scale use, with a small additional content-dependent likelihood gain” is more accurate than an exclusive calibration/content dichotomy.
- **Screening has not been isolated as the cause.** Adaptation still uses every estimated attribute variance; the null-calibrated selected set is descriptive (Stage 9, Amendments 1–2). The current result demonstrates attribute-based empirical Bayes personalisation.
- **Dictionary selection is different from discovering semantic features.** The dictionary explicitly contains the injection axes. Correlated attributes can also receive variance: the extra selections on t5 and sem5 should not be interpreted as independently identified preferences.

These are the three directions I would rank highest for the next 2–4 weeks. All can reuse frozen embeddings and rely mainly on CPU computation.

**1. Turn SAP into a demonstrably transferable, feature-matched method, with a fresh real-data test.**

This has the largest expected gain in acceptance odds.

**Experiment.** Finish Stage 8, then evaluate SAP on its native choices using an amended binary model and a dictionary fixed before inspecting the new outcomes. Compare against:

- A hierarchical attribute model with one shared shrinkage strength.
- Current SAP with attribute-specific variances.
- A strong low-rank or PAL-B comparator given the **same explicit attributes**.
- Population attribute weights with each person’s own style parameters retained.

Giving the competitors the dictionary is essential: otherwise SAP’s advantage could come from supplying useful features directly.

For an actual extension beyond current SAP, screen attributes or correlated attribute groups using **held-out few-shot adaptation gains on training raters treated as pseudo-new users**. Between-rater coefficient variance alone does not establish that an axis can be estimated from 20 ratings and transferred to new items. A transfer-based screen addresses that distinction directly.

On Community Alignment, use language-specific population controls and within-language permutations. Treat each original choice event as the sampling unit: expanding one four-way choice into three pairs does not create three independent preference elicitation events (Stage 8, “Panel”).

**Result needed.** Replicated semantic-control gains under matched inputs, with an advantage attributable to the learned prior or transfer-based screen. The strongest outcome would additionally be a real-data ranking improvement whose lower bound exceeds your existing one-point practical threshold, against population weights and the method’s own unadapted state.

A real-data null would still be useful, but would support the analysis-led contribution more strongly than a new personalisation-method claim.

**Framing change.** “A low-shot personaliser that learns which attribute differences transfer to new people, while separating scale use.”

**2. Select adaptation examples that reveal content preferences.**

This offers a concrete algorithmic contribution tied directly to the paper’s findings.

**Experiment.** Replace random adaptation examples with sequential selection from each rater’s available training-item pool. Keep labels hidden until queried.

An acquisition rule should favour examples that:

1. Distinguish plausible content-weight vectors.
2. Could change a ranking.
3. Provide information beyond what can be explained by scale-use offsets.

A feasible implementation uses the content-parameter Fisher information after accounting for the style parameters, weighted toward examples where plausible individual weights could reverse the population prediction. With 24 attributes, the required matrix operations are inexpensive.

Compare against random selection, ordinary predictive uncertainty and ordinary information-based selection. Evaluate at 5, 10 and 20 independent choice events, with identical candidate pools and held-out evaluation items.

MultiPref’s sparse value conflicts motivate this approach (§5.7). Selection must use observable item features or training-derived predictions; it cannot inspect the target rater’s unrevealed aspect judgments.

**Result needed.** A convincing improvement over the best passive method with identical features and priors—for example, ten selected examples matching twenty or fifty random examples. A real ranking gain would be especially valuable. Synthetic success should include fresh axes and draws beyond those used to design the rule.

**Framing change.** “Personalisation requires informative elicitation: a small calibration history should expose individual trade-offs.”

This would connect the diagnosis to an actionable way of collecting better preference data.

**3. Replace operational detection thresholds with a calibrated test of content personalisation.**

This has somewhat less upside than a successful real-data method, but substantially improves the scientific foundation.

**Experiment.** Develop a style-adjusted test for content interactions in a specified feature family. A feasible starting point is a variance-component score test or kernel test on cross-fitted rating residuals, accounting for the fitted style parameters.

Separate two quantities:

- **Ranking opportunity:** how much an oracle knowing the person’s content weights could improve decisions on this item distribution.
- **Recoverability:** how much of that opportunity can be identified from \(k\) observations.

Then validate the test across independent synthetic populations, different axis families, sparsity levels and disagreement levels. Include joint uncertainty over raters, prompts and synthetic draws. This should explicitly improve on the powerless split-half content estimator already reported in Appendix B.

**Result needed.** Controlled false-positive rates, demonstrated power at the claimed detection limit, and confidence statements with validated coverage under clearly stated assumptions. The current “largest null variance across five folds” rule does not establish multiplicity-controlled attribute selection.

Address negative transfer as well: SAP loses 0.50 direction points on t0 at \(k=50\), CI [−0.92, −0.09] (Stage 9 update). Passing M1 establishes absence of a declared detection on that panel; it does not establish harmless adaptation.

**Framing change.** “A calibrated framework for determining when content personalisation is identifiable and useful.”

This would make the detection-limit contribution considerably more defensible. Current positive controls establish sensitivity to particular injected families; they do not justify general exclusions of equally large but differently structured preferences (§5.6; Appendix B).

**Is SAP sufficient as the method contribution?**

**Not yet as the paper’s principal algorithmic novelty.** It is already a valuable constructive contribution to an empirical paper: it recovers preferences that the earlier learners miss and substantially narrows the unexplained gap to the reference learner.

To carry a stronger method claim, I would require:

- An advantage under matched feature access.
- An ablation establishing what attribute-specific shrinkage or screening contributes.
- Validation on fresh axes, populations or datasets.
- A precise distinction between coefficient heterogeneity, transferable probability gains and ranking gains.

A successful transfer-based screen, active elicitation rule, or calibrated statistical guarantee could supply the additional methodological substance. Real-data ranking improvement would provide the clearest empirical case.

My immediate priority would be **Stage 8 plus the matched-input SAP experiment in direction 1**. Those results will determine whether the strongest paper is a constructive personalisation paper or a rigorous measurement paper with an unusually capable diagnostic baseline.