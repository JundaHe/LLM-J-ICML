**My score is 6/10: weak accept, with a subjective acceptance probability around 55%.** I would support this as an evaluation and measurement paper. TRV’s case as a method contribution is weak.

Stage 12 materially improves credibility: a procedure developed after inspecting first-turn results now produces a positive result under a frozen evaluation on previously unanalysed turns. The isotropic comparator also makes the conclusion clearer: **ordinary validated shrinkage achieves similar observed gains; the transferable covariance has no demonstrated predictive advantage.**

Your Stage-12 reading is correct:

- Both primary user-bootstrap outcomes exclude zero, satisfying the frozen predictive-benefit rule.
- The accuracy upper bound is below one point, satisfying the sub-threshold rule.
- Superiority over isotropic shrinkage is unestablished.
- Superiority over rank-2 meets the stated rule.
- Accuracy does not exclude zero under the secondary two-way bootstrap. Therefore, describe its significance as dependent on the uncertainty analysis.

The matched-task analysis strengthens the evidence for residual user signal. The 2 × 2 strengthens the population-baseline critique. Neither establishes the stronger causal interpretations currently attached to them.

I would make the central claim:

> Predicting graded ratings, detecting user-associated content structure, and improving choices over a population model are distinct achievements. Simple offsets capture substantial graded-rating gains. On Community Alignment, reproducible residual user signal supports small predictive gains from validated attribute adaptation, while estimating transferable covariance provides no demonstrated advantage over ordinary shrinkage.

The one-point threshold is your prespecified benchmark, not a universal boundary between useful and useless personalisation.

I would use the title **“Detectable User Signal, Limited Choice Gains in Personalised Reward Models”**, and this abstract, which is under 230 words:

> Gains in predicting individual ratings need not imply better prediction of individual choices. We evaluate few-shot prediction using held-out raters and prompts, population baselines, and controls that exchange users’ adapted parameters. On three preference and safety datasets, text-independent rater offsets improve graded-label log-likelihood by 0.08–0.10 nats per rating at twenty ratings. On MultiPref and native PRISM choices, the evaluated published methods’ direction or choice gains have upper 95% bounds below one percentage point at k = 20. Semi-synthetic controls show that these small gains do not exclude preferences the learners fail to recover. Community Alignment reveals user-associated length effects that transfer across prompt sets and persist under coarse task-mix controls. A common-user analysis finds larger estimated adaptation gains against a weaker population model, without a corresponding reduction from separating prompts. Following exploratory development on first turns, we freeze an attribute-adaptation procedure and evaluate it on previously unanalysed second turns of the same users. At twenty support events, pairwise choice accuracy improves by 0.38 percentage points [0.13, 0.64] and log-likelihood by 0.0046 nats per pair [0.0031, 0.0063]. Its advantage over validated isotropic shrinkage is unestablished; the prompt-and-user bootstrap accuracy interval includes zero. These results distinguish graded-rating prediction, detectable user signal, and improvements over population choices, motivating stronger population baselines and separate tests of each.

The **WIMHF 2 × 2 is useful as a descriptive comparison of evaluation procedures**. Its proposed mechanism is overstated.

| Population procedure | Random events | Held-out prompt groups |
|---|---:|---:|
| W: low-volume training users | +0.88 | +1.08 |
| O: other user folds | +0.26 | +0.47 |

The pattern is clear: changing W to O reduces the estimated gain by 0.62/0.61 points; changing E to G increases it by 0.20/0.21 points. That corrects the earlier suggestion that prompt separation explained the reduction.

The strongest defensible wording is:

> On common eligible users, changing the population-training procedure reduces the estimated length-adaptation gain by approximately 0.6 points under both splits. Separating support and test prompts does not reduce the point estimates. Population-model choice therefore substantially affects the measured personalisation gain.

You cannot yet conclude that **a common length-weight misfit among high-volume users** explains that reduction. W and O change training volume, user composition, fitted population predictions and prior estimation. Better population modelling could reduce adaptation gains through several mechanisms. A shared high-volume-user length correction would be needed to isolate the proposed common-bias mechanism.

Three further qualifications matter:

- Report **paired intervals for the factorial contrasts**, rather than inferring them from four cell intervals. Without an equivalence analysis, “prompt sharing does not inflate gains” is stronger than the evidence.
- E and G change the evaluation examples as well as support selection. They do not isolate leakage on an identical evaluation distribution.
- Verify whether W·G excludes held-out prompt groups from population and prior fitting. As written, W is reused from the unrestricted fit. If so, G establishes support–test prompt separation, rather than separation throughout the training pipeline.

Keep the WIMHF comparison explicitly qualified. The original holds high-volume annotators out of global-model training, uses a discovered SAE feature, and removes non-English data. Your line-count proxy on the multilingual panel is a related protocol study, not a failed reproduction of that feature’s published result. [WIMHF, §5.2 and Appendices D–E](https://arxiv.org/html/2510.26202v2).

The most damaging remaining weaknesses are:

- **Limited external generalisation.** Stage 12 studies previously analysed people, with twenty available support events, using features that omit conversation history. It freezes the algorithmic procedure and refits it on second-turn training data; it does not demonstrate that first-turn user coefficients transfer to second turns.
- **Preference identification remains observational.** Clusters control coarse task categories, not identical tasks, candidate-response distributions or omitted context. “User-associated length signal” is established more securely than “task-independent individual length preference.”
- **The published-method conclusions remain implementation-specific.** Compression, detector failures and unresolved native reproductions prevent attributing the results to personalised reward models generally. Your positive controls explicitly demonstrate this limitation.
- **The manuscript obscures its strongest contribution.** Section 6 has become an analysis diary. The introduction and contributions still foreground SAP and older claims rather than the final distinction among rating prediction, user signal and population-relative choice gains.

**Stop experimenting and write.** Finish the inference and consistency repairs below, but do not start another adaptation family or open another turn. A shared prompt-bank study would address identification; it belongs in subsequent work. This paper can succeed with a restricted observational claim.

The headline arithmetic is largely consistent. The exact calibration intervals check out, and your intersection–union reasoning for the “all methods below one point” conjunction is correct. The main problems are inferential and textual:

1. **The Holm analysis is an approximate sensitivity analysis, not a repaired confirmatory analysis.**  
   Recovering a standard error as interval width/3.92 assumes a symmetric normal approximation. That is particularly questionable for the heavy-tailed cross-moment estimates. Holm requires valid underlying p-values; it cannot fix their construction or retrospective selection of analyses.

   Also, 29 contrasts are not literally all reported Stage-11 contrasts. Examples absent from the table include the reported length AUC contrasts, k = 32 within-cluster result, matched-minus-cyclic contrast and top-decile contrast. Define the family accurately. Recompute retained inferential claims from unrounded underlying records using a defensible test, and label the exercise exploratory.

2. **Non-significance is repeatedly interpreted as equality.**  
   Replace “TRV and isotropic are indistinguishable” and “the estimated covariance therefore adds nothing” with **“no advantage of the estimated covariance is established.”** Stage 12’s difference interval permits effects from −0.07 to +0.22 points.

   On first turns, the nominal paired interval favours isotropic shrinkage. Losing that detection after Holm weakens the evidence; it does not establish a tie.

3. **The task-mix decomposition is not causal.**  
   The contrasts approximately partition numerically: +0.80 own-minus-matched plus +0.75 matched-minus-cyclic is approximately +1.54 own-minus-cyclic. Calling these “half task mix, half individual” exceeds what matching identifies.

   Moreover, own-minus-population is +0.45 while own-minus-matched is +0.80. Thus the matched other is approximately **0.35 points worse than the population model**. This illustrates why own-minus-other is not the magnitude of beneficial personalisation.

   The length matching result also does not remove the task-mix confound from LoRe’s separate +3.27-point contrast.

4. **“Centring removes any task-type-specific population misfit” is too strong.**  
   It removes the estimated language-by-cluster means of these one-step statistics. Nonlinear model errors, differences within clusters, and user-specific feature distributions can remain.

   The appropriate direct centring comparison is **0.206 versus 0.210**. The pooled 0.190 statistic uses a different aggregation and is not the centring ablation.

   For the matched-other intervals, verify that uncertainty accounts for donor reuse and estimation of the matching structure. A bootstrap over target users with a fixed match map need not capture all relevant dependence.

5. **The event-level simulation should replace the pair-level simulation as the principal benchmark.**  
   The ratio \(1.93/2.87 \approx 0.672\) correctly passes your numerical factor-1.5 rule. But a barely passed tolerance does not make the less realistic simulator preferable. Report +1.93 as the principal Gaussian TR3 result and place +2.87 in the consistency check.

   Call these **model-implied achievable gains for specified learners**, rather than general learnability ceilings. The oracle is a ceiling under its assumed data-generating model; TR3 is one algorithm. Monte Carlo standard errors do not cover uncertainty in the estimated covariance or generating assumptions.

6. **The covariance and shrinkage interpretation needs restraint.**  
   An uncentred cross-moment of regularised one-step estimates is not automatically a random-slope covariance. Its variance interpretation requires assumptions beyond positive cross-half association.

   Event dependence also remains relevant to the learner: \(I_u^{-1}\) is a model-based noise proxy, not an established sampling covariance for estimates from dependent winner-versus-other pairs. This provides another possible reason that additional shrinkage helps. It does not invalidate the observed Stage-12 predictive result.

   In length-only folds, TRV’s covariance is simply a scalar prior variance. Those folds offer no evidence for learning multivariate covariance structure.

7. **Keep the endpoints precise.**  
   Log-likelihood gains combine aspects of calibration and predictive resolution; they are not, by themselves, evidence of improved calibration. Revise “mostly calibration” to language about graded-rating or predictive-distribution gains unless calibration is measured directly.

   Likewise, your CA accuracy is **pairwise winner-versus-other accuracy**, not four-response winner-selection accuracy or downstream policy utility. Preserve that qualification when claiming “choice gains.”

8. **Several concrete manuscript errors remain.**
   - DFp and PAL4 have negative Stage-8 own effects. They are not “small own gains” lost after Holm.
   - Paragraph transfer loses detection in your own Holm table and is not established on the evaluated support–test split. The main text should not present it alongside length as an equally supported finding.
   - The closing statement that simulated labels “are drawn pair by pair” is stale after Amendment 6; distinguish the two simulators.
   - Smaller prior variance means **stronger shrinkage**, not “light shrinkage.” “Light adaptation” would describe the intended behaviour.
   - Explain the DICES counts of 104 quality-checked raters in §3 and 123 raters in Appendix C.
   - Keep the first-turn “S12 smoke” rows clearly separated from actual frozen Stage-12 results. The current Stage-11 Holm table says nothing directly about Stage-12 multiplicity.
   - Use unrounded interval endpoints for strict sign decisions; displayed negative zero cannot determine significance.

I could not inspect local scripts because the shell failed; this review audits the supplied artefacts and the WIMHF paper.