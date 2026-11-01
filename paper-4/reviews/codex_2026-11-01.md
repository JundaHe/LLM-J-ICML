**My ranking as submitted today is paper 4 > paper 2 > paper 3.** Paper 4 has the clearest ICML question and the strongest potential payoff, but its headline currently outruns its evidence. SAP is promising; the screening outputs alone do not establish a method contribution.

These are subjective acceptance estimates for the supplied versions, assuming competent final presentation. I give no credit for unfinished Stages 8–9, and assess novelty against the related work described in your documents rather than an independent literature search.

## 1. Paper-by-paper assessment

### Paper 2 — *Five Raters Are Not a Distribution*

**Three-line summary**

1. Separates reproducibility across raters from predictability from text for histogram shape beyond exact mode and mean (§2).
2. Finds little useful ordinal residual shape across many panels; donor interventions, probes and training experiments broadly agree, with ChaosNLI providing a useful contrast (§§3–4).
3. Examines annotation allocation, finding strong but task-dependent reasons to cover more items before collecting many ratings per item (§5).

**Estimated ICML acceptance probability: 30%**; plausible range **20–40%**.

**Single biggest weakness: the central “shape reliability” estimand supports a narrower conclusion than the paper’s language suggests.**

The score identity in §2.1 is valid, but calling \(X/M\) a split-half reliability, calling \(M-X\) “sampling noise,” and interpreting \(G/X\) as the fraction of reproducible shape require more justification. Both residuals use a comparator constructed from panel 1; this is not the usual symmetric measurement-error decomposition. Moreover, conditioning on exact empirical mode and mean can remove meaningful disagreement information along with location.

That does **not** invalidate the audit. It means the strongest defensible finding is:

> On these panels, raw histograms offer little forecasting benefit beyond a particular exact-statistic comparator, and these learners show little benefit from the remaining information.

That is narrower than “what is reproducible is mostly not in the text” (§1), or “because there the shape is in the text” (§3). Linear probing across three families is substantial evidence about representations, not a general separation of text from rater population.

The breadth, independent-rater evaluation and reported falsifications are strengths. The budget study is useful, but its connection to the proposed mechanism weakened when ChaosNLI falsified the prediction and POPQUORN failed the LoRA items-first reading (§5). I would reduce its prominence rather than force everything into one causal story.

### Paper 3 — *Calibrating LLM judges to the people they stand in for*

**Three-line summary**

1. Fits an ordered-probit mapping from an existing judge score to a target population’s rating distribution, optionally adding individual thresholds (“The mapping used throughout”).
2. Tests pool adaptation, black-box calibration and disagreement prediction under calibration/test separation (G1–G3).
3. Initial G1 results show large gains on several substantial population shifts, but small-shift and null rows often deteriorate; the latest amended procedure lacks supplied results.

**Estimated ICML acceptance probability: 8%**; plausible range **3–15%**.

**Single biggest weakness: insufficient differentiation from established ordinal calibration and hierarchical rater models.**

The mapping itself is standard. A deployment paper could still be valuable, but the supplied evidence does not yet establish a broadly reliable decision rule for when this mapping helps.

In particular, `G1_SUMMARY_v2` supports strong gains on DICES-990 locale and some race shifts, but not the broad positive impression in the handoff. At 50 ratings, generic calibration beats the panel map on several rows; random-half and small-shift rows sometimes worsen. Amendments 1–2 are reasonable development decisions, but they mean the improved procedure needs fresh confirmation.

G2 with strong black-box judges and G3 against direct disagreement prediction are important unfinished evidence. As supplied, this is a promising study protocol with preliminary findings, not an ICML-ready contribution.

### Paper 4 — *What Personalised Reward Models Learn About a New Rater*

**Three-line summary**

1. Separates gains from text-independent scale use from gains in predicting a new rater’s preferred response under held-out-rater/item evaluation (§§4–6).
2. Finds strong graded-label calibration gains from simple offsets, while tested personalisers produce little reliable ranking improvement on MultiPref and native PRISM choices (§5.1–5.5; §6).
3. Uses synthetic injections and aspect analyses to investigate whether ranking nulls reflect weak methods, limited data, or limited opportunities for value trade-offs (§5.6–5.7).

**Estimated ICML acceptance probability: 40%**; plausible range **25–50%**.

**Single biggest weakness: the negative conclusion depends heavily on personalisation implementations whose effectiveness is not convincingly established in their native settings.**

The disclosure is commendably explicit: VPL/PAL published results are not reproduced, LoRe’s published improvement reverses, and compression and posterior collapse materially affect detectors (§9; Appendices B–C). Nevertheless, a reviewer can reasonably say:

> You have established that your evaluated implementations learn little ranking personalisation here; you have not established that the method families generally learn only scale use.

The synthetic controls improve this substantially, but they also show that the implementations miss preferences the supplied ratings would support (§5.6). That makes them less decisive instruments for ruling out real content preferences.

Two additional corrections matter:

- **Failure to detect a synthetic effect is not a formal exclusion bound on real heterogeneity.** Statements that +10 or +20 oracle-point heterogeneity is “excluded” (§5.6; Appendix B) require calibrated test inversion, power estimates and generator assumptions. The acknowledged mismatch in synthetic agreement makes the present wording particularly strong.
- **Scale use is an operational interpretation.** Symmetric offsets clearly capture tie/intensity behaviour, but free class offsets on DICES/PRISM can also absorb stable substantive differences or sampling differences. Likewise, genuine content preferences can change strength without flipping rankings. Frame ranking as an especially consequential test of content personalisation, not its exhaustive definition.

## 2. Which is most likely to be accepted?

**Paper 4.** It asks a consequential question that a broad ICML reviewer can immediately understand: *does a personalised reward model learn what I prefer, or mainly how I express a rating?*

It also has three unusually useful ingredients:

- A cheap baseline capable of changing how existing methods are evaluated.
- Native PRISM choices that move the study beyond graded-label likelihood (§6).
- Positive controls exposing the gap between available information and what current learners recover (§5.6).

Paper 2 is empirically mature but has a harder conceptual sell: reviewers must accept the exact mode-and-mean residual as the right object before the findings become compelling. Paper 4’s distinction between calibration and response selection is more immediately actionable.

**A method is not mandatory for paper 4 to succeed.** A rigorously calibrated empirical finding could suffice. A weak method appended for novelty could make it less coherent.

## 3. Is paper 4’s novelty sufficient?

**Potentially yes for an empirical analysis paper; currently borderline in execution.**

The offsets are not new (§2 correctly admits this). Held-out-user adaptation and permutation controls are not individually strong novelty claims either. The novel contribution is their combination into a convincing finding about *what reported personalisation gains represent*, supported by graded/binary comparisons and calibrated positive controls.

What currently prevents a comfortable weak accept is the unresolved combination of baseline fidelity, detector weakness and generalisation beyond the original datasets. More baselines alone will not resolve that.

These are the three highest-value additions I would prioritise within 2–4 weeks.

### 1. Turn SAP into an honest test of transferable axis discovery

**Expected acceptance gain: highest**, particularly if it succeeds on real heterogeneous preferences. Synthetic-only success would provide a smaller but useful gain.

**Experiment.** Complete SAP under an outer evaluation untouched by further method decisions. Compare, using identical content features and base predictors:

- Population attribute weights plus personalised style.
- Personalised attributes with a shared isotropic prior.
- Diagonal EB/ARD SAP.
- A regularised low-rank model given the same attributes.
- The known-axis reference learner.

Include DFs or VPL+style as the existing reference. Report own-minus-population with own style held fixed, own-minus-other, and improvement over the method’s own unpersonalised state.

Use multiple synthetic draws, correlated distractor attributes and at least one injection family whose construction did not determine the dictionary. Extend to Stage 8 if feasible.

**Result needed.**

- On sem5, reproducible recovery of a substantial part of the known-axis learner’s gain, exceeding same-feature generic baselines.
- Null behaviour consistent with the stated false-positive rate.
- Ideally, real held-out ranking improvement with a two-way interval excluding zero and a practically meaningful magnitude—around one point would be persuasive.

The dictionary already contains the exact length, formatting and hedging injection features. Recovering those is **selection among supplied candidate axes**, not discovering an unknown representation. Say so.

**New framing.**

> Generic latent personalisers miss sparse, transferable preference axes; learning which supplied attributes vary across people closes part of the gap.

If real-data SAP stays null, frame it as a stronger interpretable detector that narrows the empirical claim, not a successful real-world personalisation method.

### 2. Use Community Alignment to identify when personalisation becomes useful

**Expected acceptance gain: second**, and potentially first if SAP remains synthetic-only.

**Experiment.** Complete Stage 8, but add a carefully scoped analysis of opportunities for disagreement on identical response sets. On sufficiently shared comparisons, estimate preference variation beyond finite-rater noise and stratify by an independently defined conflict/opportunity measure.

Evaluate both aggregate performance and performance where preferences can plausibly change the selected response. Add SAP if the binary implementation is ready.

Account for the fact that three chosen-versus-other pairs come from one four-way choice. Report four-way selection performance where model scores permit it.

**Result needed.**

Either outcome can be strong:

- **Positive:** personalisation helps on disagreement-rich comparisons, with little aggregate benefit because such comparisons are uncommon.
- **Negative:** a credible detector still finds negligible gains despite demonstrable preference variation and adequate adaptation histories.

A wide interval is inconclusive. A global null without evidence that the dataset offers learnable preference differences adds much less.

**New framing.**

> Personalisation’s value depends on the availability and transferability of preference conflicts, not merely the number of users or ratings.

This would connect MultiPref’s 4% conflict finding (§5.7) to a broader empirical explanation instead of leaving it as a dataset-specific caveat.

### 3. Replace the heuristic detection limit with a calibrated sensitivity analysis

**Expected acceptance gain: third**, but the most direct repair to a vulnerable headline.

**Experiment.** Build a compact benchmark varying content-effect strength, number of adaptation ratings and axis availability. Use several seeds per condition. Compare the reference learner, strongest published implementation and SAP.

Measure recovery on a common scale—own versus population, with style fixed—and separately report the permutation contrast. Calibrate rejection thresholds under null simulations and estimate detection probabilities under alternatives.

Prioritise one generator that better matches real agreement and class frequencies; then assess sensitivity to remaining generator mismatch.

**Result needed.**

Show a stable, quantified gap between:

1. What the known-feature learner can recover.
2. What a learner selecting from a dictionary can recover.
3. What embedding-based latent models recover.

A modest, carefully estimated boundary is more valuable than a dramatic “excluded” effect size unsupported by calibrated power.

**New framing.**

> A sensitivity analysis separates information available in the ratings, representation availability and the learner’s ability to identify preference axes.

This could carry the paper even without positive real-data SAP results.

## Is SAP itself sufficient?

**Not yet.** Hierarchical logistic/ordinal modelling with dictionary features, Laplace-EM and diagonal ARD is an established methodological combination. Its ICML value would come from solving the demonstrated failure mode and establishing why screening helps.

The fold-0 outputs are encouraging diagnostics:

- t5 length variance **0.036**, versus at most **0.004** elsewhere.
- sem5 hedging and formatting **0.040/0.039**.
- Real MultiPref length highest at **0.0073**.

These show that the screening estimates respond to injected axes. They do **not** establish transferable individual prediction, superiority to simpler regularisation, or meaningful real preference heterogeneity.

Three changes would make SAP substantially more credible:

1. **Isolate its contribution.** Demonstrate that EB screening improves prediction over the same dictionary with tuned isotropic shrinkage—not merely over models deprived of explicit attributes.
2. **Validate beyond the construction.** Succeed on new draws, correlated attributes and an independently chosen real-data setting. The Stage 9 amendments are legitimate development, but cannot serve as independent confirmation.
3. **Repair selection and null calibration.** Fifteen EM iterations may leave variance rankings dependent on convergence speed, as Amendment 2 already suggests. Check convergence. Also, exceeding the maximum of five synthetic-null fold variances is a heuristic threshold, not controlled attribute discovery; real-data screening needs a null preserving its relevant structure.

Finally, **M1 is too weak as a validity criterion**: requiring a null-effect lower bound to be ≤1 point does not establish a low false-positive rate or negligible spurious gain. And because adaptation still uses every estimated variance, SAP currently performs continuous shrinkage; the “selected set” is a reporting rule, not a hard-screening mechanism.

My recommendation is to complete SAP, but make its claim conditional on held-out predictive results. The strongest attainable paper is **“separating scale use from transferable content personalisation, and showing when explicit attribute modelling recovers the latter.”** The evidence does not yet support “personalised reward models learn only scale use.”