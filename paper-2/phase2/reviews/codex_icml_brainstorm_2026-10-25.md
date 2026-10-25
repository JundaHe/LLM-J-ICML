## Part 1 — Literature check (≈390 words)

Important omissions from the refresh:

- [Kurniawan et al., *Training and Evaluating with Human Label Variation* (CL 2026)](https://aclanthology.org/2026.cl-1.3/): 14 methods × 6 datasets; the broadest baseline suite and an obvious reviewer citation.
- [Tao et al., *Confidence Calibration under Ambiguous Ground Truth* (2026)](https://arxiv.org/abs/2603.22879): reports that one randomly sampled annotation can sometimes match full-distribution calibration. This directly complicates claims about the value of collecting histograms.
- [Wu et al., *SHALA-LLM* (2026)](https://arxiv.org/abs/2606.05376): a positive LLM method trained from annotator distributions, including ChaosNLI.
- [Wang & Chau, *Epistemic Learning from Imprecise Annotation* (2026)](https://arxiv.org/abs/2609.34285): treats sparse empirical distributions as imprecise sets rather than exact targets—the closest conceptual alternative to shrinkage.
- [Wang et al., *Learning Label Distribution with Dirichlet Process Mixture Model* (AAAI 2026)](https://ojs.aaai.org/index.php/AAAI/article/view/39846): explicitly models heterogeneous latent annotation patterns.
- [Chen et al., *Human Label Variation as Stable Signal* (EMNLP 2026)](https://arxiv.org/abs/2605.28802): weak single-annotation signals become detectable after aggregation, supporting your reliability framing.
- **Uncertain:** *When Annotators Disagree: A Principled Approach to Learning with Noisy Labels*. The available 2026 metadata appears to conflate it with a 2023 inter-rater-agreement paper. Do not cite until its DOI and text are verified.

The biggest acceptance threat is [Gheibi & Ghazizadeh, *Same Target, Different Basins*](https://arxiv.org/abs/2605.20642), because it already owns “sparse empirical soft labels can be worse, and breaking the item–distribution association diagnoses this.” Neutralise it experimentally: include SLS/multipass as baselines on your datasets, then show that reliability shrinkage—not simply hard-label delivery—wins at equal annotation budget across ordinal and nominal tasks and multiple LLM families.

Is \(\lambda^*=X/M\) already known? **The algebra is; the proposed package probably is not.** Minimising \(\lambda^2M-2\lambda X\) is an elementary projection/forecast-combination coefficient. James–Stein multinomial estimators already shrink empirical proportions toward a target; [Hausser–Strimmer](https://jmlr.org/papers/v10/hausser09a.html) is mandatory prior art. Dirichlet posterior means shrink toward a prior mean using pseudo-count concentration. Dawid–Skene estimates latent labels and rater confusion. Label smoothing mixes with a fixed generic target. None of these, in the search I could verify, combines a recipient-specific statistic-preserving comparator with independently measured cross-panel residual agreement.

Do not claim the ratio itself as novel. Claim the comparator, estimand, cross-fitting, and supervision application. Technically, a shared coefficient is  
\[
\lambda^*=\mathrm{clip}\{\mathbb E[X]/\mathbb E[M],0,1\},
\]
and a covariate-dependent one uses conditional expectations—not noisy per-item \(X_i/M_i\).

## Part 2 — The paper that gets in (≈1,170 words)

Blunt verdict: do not spend 13 weeks merely enlarging the audit. The ICML paper needs to become a positive method-and-decision paper, with the audit as motivation.

1. **Residual decoding**

   - **Impact:** High if positive, roughly +8–12 acceptance points. SummEval has annotation-side A2 \(=+0.0044\) while the learned LoRA contrast is approximately zero. Showing positive independent-panel decoding would locate the failure between representation and supervision.
   - **Cost:** 2–4 CPU wall-days including nested CV and bootstrap refitting; negligible GPU.
   - **Failure:** Write only that residuals were not linearly decodable from these frozen features. Do not say text lacks the information. A null is informative but not an ICML centerpiece.

2. **Reliability-shrunk targets**

   - **Impact:** Highest, potentially +15–25 points. The key positive fact is stronger than the current \(1/2\) threshold: raw residuals beat \(q_T\) only when \(X/M>1/2\), but optimally shrunken residuals improve on \(q_T\) whenever \(X>0\). That converts the audit’s apparent negative result into a usable method.
   - **Cost:** Approximately one CPU week for cross-fitted annotation/heads experiments, then 2–5 aggregate GPU-days for LoRA and replications.
   - **Required baselines:** raw soft labels, \(q_T\), fixed/CV-tuned \(\lambda\), Dirichlet/James–Stein shrinkage, label smoothing, SLS/multipass, and the existing `shrunk_res`.
   - **Failure:** If it improves annotation forecasts but not trained models, say the learner is insensitive to this target correction. Keep it as analysis, not as a successful training method. Per-item \(\lambda\) must be secondary unless it beats the global/panel coefficient out of sample.

3. **Additional base families**

   - **Impact:** Moderate, +5–8 points; defensive rather than novel. One Qwen family is currently an easy rejection argument.
   - **Cost:** Llama-3.1-8B-Instruct plus Gemma-2-9B-it, with a minimal four-arm roster, should cost about 2–5 GPU-days and one engineering week.
   - **Failure:** Report family heterogeneity and abandon universal wording. One-family success is insufficient for a method headline.

4. **Rater-aware POPQUORN**

   - **Impact:** Mandatory hygiene. It prevents a serious reviewer objection rather than adding novelty.
   - **Cost:** 3–5 engineering days and under one GPU-day. Construct folds from real `user_id`s, ensure target raters and evaluation raters are disjoint, and audit the induced missingness.
   - **Failure:** If the mode-only or method result collapses, POPQUORN is no longer a replication. Report it and make SummEval primary; do not hide behind the conservative bootstrap.

5. **Theory**

   - **Impact:** Moderate only when attached to the method. The failed \(1/a\) prediction does not invalidate the exact quadratic-risk result.
   - **Cost:** 1–2 researcher-weeks.
   - **Publishable content:** Under exchangeable target-population raters, cross-fitting, and bounded RPS/Brier residuals, prove the risk curve, clipped optimal coefficient, conditional-covariate version, and an oracle inequality for estimating \(\lambda\). Explicitly distinguish global \(\mathbb E X/\mathbb E M\) from per-item ratios.
   - **Failure:** If the bound is vacuous, retain the exact proposition and empirical estimator in the appendix. An identity plus the failed parametric crossover model is not an ICML theory contribution.

6. **Larger dense-panel study/new benchmark**

   - **Impact:** Low-to-moderate for another dataset; potentially high for an excellent benchmark, but 13 weeks is unrealistic.
   - **Cost:** Existing-data extension: 1–3 weeks. New human benchmark: too risky, with recruitment, ethics, population definition, and quality control.
   - **Failure:** “Another heterogeneous panel” does not change the story. Do not collect a rushed benchmark. Commit-message panels remain excluded.

7. **Better addition: fixed-budget decision experiment**

   - **Impact:** High and practical. On dense panels, hold total annotations fixed and compare more items × fewer raters against fewer items × deeper panels, using raw, \(q_T\), and reliability-shrunk supervision.
   - **Cost:** About one CPU week; add 1–2 GPU-days only after the method passes.
   - **Failure:** If no universal frontier appears, ship a task-specific diagnostic rather than a universal annotation-count threshold. This directly respects the failed \(1/a\) result.

### Thirteen-week plan

- **Week 1:** Freeze protocols, estimands, primary panels, baselines, multiplicity treatment, and gates. Implement residual decoding.
- **Week 2 — Gate D:** Continue the mechanistic story only if proper-score gain is positive on SummEval coherence, directionally replicates on relevance, and disappears under within-\(T\) feature permutation. This gate does not kill the method.
- **Weeks 2–4:** Implement global and covariate-conditional shrinkage with nested cross-fitting. Run annotation-side panels and classical baselines.
- **Gate A:** Proceed only if estimated shrinkage beats both endpoints out of sample on the prespecified pooled ordinal test and on both ChaosNLI panels, without material primary-panel harm. Otherwise kill the method immediately.
- **Weeks 4–5:** Run all heads plus the fixed-budget frontier.
- **Gate H:** Require shrinkage to beat the best generic shrinkage baseline, not merely raw soft labels, on both ordinal and nominal families.
- **Weeks 5–7:** Qwen LoRA on SummEval and genuinely user-held-out POPQUORN.
- **Gate L:** Require improvement over raw soft and \(q_T\) on SummEval and a compatible user-aware POPQUORN result. If only one succeeds, the claim becomes dataset-conditional.
- **Weeks 7–9:** Llama and Gemma replication. Require the primary direction in at least two of three base families.
- **Weeks 9–10:** Finish the finite-sample theory; do not revive the \(1/a\) extrapolation.
- **Weeks 10–12:** Write the method paper, main figures, ablations, and limitations; run independent consistency review.
- **Week 13:** Reproduction pass, artifact, and buffer. No new scientific branch after week 10.

**Title:** *When Should Disagreement Histograms Teach? Reliability-Adaptive Distributional Supervision for Learned Judges*

**One-sentence contribution:** We identify cross-rater-replicable residual variation beyond task statistics as the learnable component of empirical disagreement, derive a cross-fitted reliability shrinkage rule that minimises new-rater proper-score risk, and validate when it improves distributional supervision across ordinal and nominal panels and multiple open LLM families.

### Probabilities and fallbacks

- Current package: **25% ICML acceptance**.
- All gates pass: **65%**.
- Method fails but decoding and the cleaned audit survive: **30%**; about **20%** if decoding also fails.

If only decoding fails, continue to ICML as a method paper. If Gate A or H fails, stop the ICML-method push and submit the audit/finite-rater paper to **ACL or EMNLP**, with **TMLR** as the stronger home for a comprehensive negative result. If rater-aware POPQUORN or cross-family replication fails, report the heterogeneity and prefer ACL/EMNLP or TMLR over making a universal ICML claim.