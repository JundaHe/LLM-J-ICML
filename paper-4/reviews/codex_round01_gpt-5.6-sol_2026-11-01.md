Bottom line: Paper 4 is the strongest ICML candidate, Paper 2 is a credible but venue-sensitive runner-up, and Paper 3 is not yet a full ICML paper. My estimates count the supplied Stage 9 results as part of Paper 4, but not the still-running Stage 8.

## 1. Paper-by-paper assessment

### Paper 2 — *Five Raters Are Not a Distribution*

Three-line summary:

1. It separates disagreement-shape reproducibility across raters from predictability from text, using split-half reliability and cross-fitted decoding (§2).
2. Across broad ordinal panels, residual shape is weakly reproducible and barely linearly decodable, whereas ChaosNLI is a clear contrast; donor replacement and target-construction experiments show corresponding behavior in learned judges (§3–4).
3. Fixed-budget experiments suggest covering more items is usually more valuable than adding raters per item, although POPQUORN establishes that this is task-dependent (§5; limitations in §7).

**Estimated ICML acceptance probability: 34%.**

**Single biggest weakness:** it is an unusually thorough audit built around one particular mode-and-mean decomposition, but it offers neither a major new learning method nor a substantial theorem. An ICML reviewer can reasonably judge the reliability cards, donor replacement, rater decomposition and budget experiments as four related analyses rather than one sufficiently novel technical contribution. Conditioning on the exact empirical mode and mean may also be criticized as defining away much of the small-panel signal, even though the paper handles the structural-support issue honestly (§2.1, §6).

This is a strong paper, but probably a weak-accept/weak-reject paper at ICML and a more natural strong paper at an empirical NLP or software-engineering venue.

### Paper 3 — panel calibration

Three-line summary:

1. It proposes adapting an unchanged judge to a new rater pool with a small ordered-probit panel map, separating pool calibration, black-box distribution recovery and disagreement prediction (G1–G3).
2. G1 finds substantial pool shifts on some DICES-990 groups, including gaps of 0.016–0.045 RPS, with the full map recovering much of these shifts and sometimes substantially outperforming generic calibration (G1 summary v2).
3. The small-data regime remains unstable: 20–50-rating maps frequently hurt on null or small-shift rows, prompting two protocol amendments, while G2 and G3 remain unfinished (Amendments 1–2).

**Estimated ICML acceptance probability: 9%.**

**Single biggest weakness:** it does not yet have a distinct paper-level contribution. The core ordered-probit mapping is classical, only G1 has results, and Paper 4 already makes the stronger and broader “scale use rather than content” argument. The random-half controls are not uniformly reassuring either—for example, DICES-990 has a nontrivial random-half gap and map-B(50) worsens performance—so the current evidence does not yet establish a reliably sample-efficient adaptation method.

Unless G2 produces a striking result with frontier black-box judges, I would merge the best material into Paper 4 or reposition Paper 3 around a substantially different deployment problem.

### Paper 4 — personalised reward models

Three-line summary:

1. Under unseen-rater and unseen-item evaluation, a small scale-use model gains roughly 0.08–0.10 nats per rating from 20 examples across MultiPref, DICES and PRISM, matching or beating much more elaborate personalisers (§5.1–5.5).
2. Those gains are almost entirely calibration rather than ranking: binary labels remove most of the signal, real ranking improvements remain below one point, and the result extends to 41,199 native PRISM choices and even seen raters (§6, Stage 7 S7-3).
3. Positive controls localize the failure to finding preference axes, and SAP now detects injected semantic heterogeneity while remaining null on t0—but on real MultiPref its direction gain is only +0.17 [−0.19, +0.55] points (Stage 9; §5.6–5.7).

**Estimated ICML acceptance probability: 43%.**

**Single biggest weakness:** the strongest constructive evidence is still synthetic. SAP succeeds when the injected semantic axes are explicitly present in its 24-attribute dictionary, but it does not produce meaningful real-data ranking personalisation. Its real MultiPref screen selects 12 attributes while yielding only +0.17 points, making “discovery” hard to distinguish from correlated proxy selection. This leaves the paper’s main contribution as a sophisticated negative audit, with additional credibility risk because several published-method results are reimplementations whose published gains could not be reproduced (§9; Appendix B).

## 2. Most likely to be accepted

**Paper 4 is most likely.**

It has the best combination of:

- A timely, consequential question: whether personalised reward models learn preferences or merely response style.
- A memorable result: large likelihood gains can coexist with essentially no ranking gain.
- A strong evaluation design: unseen raters and items, own-versus-other permutation controls, calibration/ranking separation and native user choices (§5–6).
- Positive controls that prevent a simplistic “the methods failed, therefore heterogeneity is absent” conclusion (§5.6, Stage 7).
- A possible constructive contribution through SAP.

Paper 2 is currently more internally mature and perhaps lower variance, but Paper 4 has a sharper headline and stronger relevance to current ICML interest in reward modelling and pluralistic alignment. Paper 4’s advantage disappears if the manuscript remains as sprawling as v0.9: SAP and Stage 8 need to be integrated into a much narrower central story, with most aspect analyses, amendment history and reproduction diagnostics moved to the supplement.

## 3. Is Paper 4’s novelty sufficient?

**Borderline yes as an empirical/measurement paper; no as a conventional methods paper.**

The novel contribution is not the offset model—§2 correctly acknowledges that rater biases, thresholds and scale use are classical. Nor is Laplace-EM/ARD itself novel. The ICML-level contribution is the combination of:

1. A controlled new-rater test distinguishing calibration from ranking.
2. A permutation control that exposes apparent personalisation caused by a poor population state.
3. Method-specific positive controls and detection limits.
4. The broad empirical finding that current personalisers transfer scale use but not response ranking.

That package can clear the novelty bar, but it is vulnerable to reviewers calling it “classical annotator modelling plus many negative experiments.” The following additions would materially improve its position.

### 1. Learn the preference subspace from frozen embeddings

**Expected acceptance-odds gain if successful: approximately +8–12 percentage points.**

Build an embedding version of SAP rather than expanding the hand-written dictionary. Starting from the DFs base model:

- For every training rater, compute a cross-fitted residual preference-score vector in the 256-dimensional frozen pair-difference space.
- Estimate the between-rater covariance after subtracting estimation noise using each rater’s inverse Fisher information.
- Take the positive, low-rank eigenspace, selecting its rank using held-out training raters or a permutation null.
- Adapt a new rater by MAP only within that learned subspace.

This is feasible on CPU with the cached embeddings; randomized eigendecomposition at this scale is trivial.

**Experiment:** run t0, t5/t10, sem5/sem10 and x5/x10, but do not provide the injected features or attribute dictionary to the method. Use the same four synthetic draws and compare with DL, VPL, PAL-B, dictionary SAP and the feature-informed reference learner. Then evaluate real MultiPref and the graded PRISM panel.

**Result needed:** clean t0 behavior, plus a lower 95% bound above +1 point on the approximately +5-oracle-point panels in at least three of four draws. It should materially outperform DL/VPL/PAL-B at that strength. Recovering only the +10 panels would be useful but incremental, because PAL-B and in-span DL already approach that regime.

**Framing change:** from “existing models fail to find the axis” to “we identify why they fail and provide a noise-corrected population method that discovers transferable preference axes.” This would be a genuine method contribution even if real MultiPref remains near zero.

### 2. Finish Community Alignment and include SAP

**Expected gain: +6–10 points for a positive result; +2–4 for a tight, comprehensive null.**

Stage 8 directly addresses the most damaging external-validity objection: MultiPref contains few value conflicts, DICES is not pairwise ranking, and PRISM has limited shared comparisons. Community Alignment was designed for heterogeneous preferences.

**Experiment:** run the frozen-embedding baselines from Stage 8 and add binary/logistic SAP and, ideally, the learned-subspace method above. Preserve rater-disjoint and prompt-disjoint folds. Report both:

- own adaptation versus the method’s own \(k=0\) state; and
- own parameters versus another user’s parameters.

Given the LoRe behavior documented in §6, own-versus-other alone is not enough.

**Result needed for a strong positive contribution:** at \(k=20\), both contrasts should have lower 95% bounds above +1 choice-accuracy point, and the method should beat the strongest existing personaliser by at least roughly 0.5–1 point. The effect should not be driven by a single language or fold.

If every method instead has upper bounds below +1 point, that still produces an important replication on the dataset most favorable to the alternative hypothesis, but it strengthens the audit rather than the method novelty.

**Framing change:** with a positive result, “screen first, then personalise: content personalisation works when the dataset actually contains transferable heterogeneity.” With a null, “even a benchmark constructed for preference diversity contains little few-shot transferable ranking signal under strict new-user evaluation.”

### 3. Turn the detection limit into a calibrated statistical certificate

**Expected gain if successfully validated: +5–8 points.**

The present positive controls are scientifically valuable, but the thresholds are partly exploratory and transfer only approximately to real data (§5.6; Appendix B). Replace the current null-max selection rule with a cross-fitted variance-component test and an invertible power analysis.

**Experiment:**

- Learn attributes/subspaces only from training raters.
- Use a score test or parametric bootstrap for the between-rater variance components, with family-wise error or FDR control.
- Across held-out synthetic draws, estimate the smallest oracle ranking effect that the complete pipeline detects with 80% power at \(k=20\).
- Invert the test to place an upper confidence bound on real-data content personalisation within the declared dictionary or embedding subspace.

**Result needed:** approximately nominal false-positive control on t0, at least 80% selection/detection of the true axes on sem5 or comparable unseen injections, and 90–95% coverage of injected effects across draws. For a strong real-data statement, the resulting upper bound should be below roughly 2–3 ranking points on at least two datasets.

**Framing change:** from “we repeatedly observed a null” to “we provide a calibrated audit that certifies which forms and magnitudes of personalisation the data and method could have detected.” That is much more defensible at ICML.

## Is SAP itself sufficient?

**Not yet as a standalone method contribution. It is already a useful supporting contribution.**

The Stage 9 results are genuinely encouraging:

- The t0 control passes.
- On sem5, SAP achieves +2.69 [+1.70, +3.64] points and selects both injected semantic attributes.
- On sem10 it achieves +7.53 [+5.92, +9.10].
- The fold-0 EB variances rank the injected attributes far above the other 22, which is good diagnostic evidence.

But the current version remains a hand-crafted generalized linear mixed model with standard ARD, tested primarily on injections whose true axes are included in its dictionary. Its selection is not especially specific: t5 and sem5 select correlated proxies, sem10 selects nine attributes, and real MultiPref selects twelve while producing no meaningful ranking gain. The real-data LL gain, +0.22×10⁻² nats, is statistically detectable but too small to carry an ICML method claim.

SAP would become a sufficient method contribution if it did at least two of the following:

- Discover axes from frozen representations rather than being handed a dictionary containing them.
- Use statistically calibrated, cross-fitted selection rather than the maximum variance on one synthetic null panel.
- Produce a greater-than-one-point ranking gain on a real heterogeneous-preference dataset.
- Demonstrate reliable detection of previously hidden +5-point synthetic preferences across multiple axes and random draws.
- Generalize across at least two datasets or transfer a learned population prior from one panel to another.

My recommendation is therefore: make learned axis discovery the method contribution, use dictionary SAP as its interpretable special case, and treat Community Alignment as the decisive real-data test. That would give Paper 4 a substantially stronger ICML case than adding more backbones or more published baselines.