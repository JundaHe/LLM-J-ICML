**1) My assessment is now borderline weak accept: 4/6, with roughly a 45–55% subjective acceptance probability after the claim corrections below.** Submitted literally as written, the draft would still receive a weak reject from me because several central statements contradict its latest results. This probability is a reviewer judgment, not a calibrated forecast.

The scientific story has improved:

- The corrected Stage 8 result provides a substantive counterexample to a blanket ranking null. The negative own gain makes it especially useful for distinguishing **user information from beneficial adaptation**.
- Stage 11 supplies evidence of transferable residual structure and a small positive adaptation result. The paper can now explain why detecting heterogeneity and exploiting it are separate problems.
- The amendments preserve failed outcomes and withdraw the unsupported order-of-magnitude claim. That strengthens credibility.

The liabilities have also grown: the final method emerged through repeated inspection of the same test outcomes, the diagnostic’s interpretation remains fragile, and the positive predecessors have not been adequately resolved.

I would sell this as an empirical measurement paper. Its strongest contribution is separating three quantities that personalisation papers often conflate: **predicting scale use, detecting user-specific content signal, and improving choices**.

**2) Stage 11’s forking paths are acceptable as exploratory research. Their current presentation still overstates what was validated.**

| Analysis | Evidential status | Defensible interpretation |
|---|---|---|
| Corrected frozen Stage 8 rule | Prospectively specified rule, with a corrected implementation | The rule detects through LoRe’s own−other contrast; report the harmful own gain alongside it |
| Within-country derangement | Exploratory control specified after the initial result | Country differences do not explain the large contrast |
| Original Stage 11 diagnostic | Failed its specified calibration gate | All three primary outcomes remain inconclusive; the original S11-3 gate was not triggered |
| Amendments 1–3 | Exploratory diagnostic and method development | Evidence motivating revised hypotheses and a better adaptation procedure |
| Amendment 4 | Training-user selection within an adaptively developed procedure | Useful exploratory performance evidence; its test set was already involved in method development |

Amendment 4 prevents directly choosing the final shrinkage value on test users. It does **not** erase the fact that test outcomes motivated the shrinkage grid, attribute-set comparison and revised procedure. Cross-fitting addresses training separation; it does not address researcher adaptation.

I would put this paragraph beside the Stage 11 results, not only in the appendix:

> The original Stage 11 diagnostic failed its pre-specified calibration criterion, leaving all three primary outcomes inconclusive and the adaptation gate unmet. All subsequent analyses were exploratory. The final procedure selected attributes and shrinkage using training users only, but its candidate family was developed after inspecting test results. Reported bootstrap intervals are nominal and do not account for this analysis adaptation.

The amendments themselves need slightly different conclusions:

- **Amendment 1:** Reasonable repairs, but changing calibration criteria after failure requires retaining the original failure prominently.
- **Amendment 2:** Supports exploratory length and paragraph findings under the amended simulation criterion. It does not establish that Ĉ measures a well-calibrated amount of latent preference variance.
- **Amendment 3:** Successfully undermines the proposed order-of-magnitude conclusion. A hypothetical concentration mixture shows that covariance alone cannot determine learnability; it does not establish that concentration explains the real data.
- **Amendment 4:** Your strongest adaptation result, but still an exploratory result from a test-informed procedure.

There is no categorical prohibition against exploratory findings in an abstract. I would allow the **explicitly labelled exploratory point estimates** below. Before making any of these unqualified abstract claims, however, I require a fresh frozen evaluation:

1. “We establish transferable individual length preferences.”
2. “Our diagnostic is simulation-calibrated.”
3. “Our method reliably improves new-user prediction.”
4. “Transfer-calibrated adaptation outperforms competing methods.”

Freeze the entire procedure—including eligibility, event counting, preprocessing, covariance estimation, PSD projection, selection grid, population baseline, estimand and uncertainty calculation—before that evaluation.

PRISM or MultiPref would provide useful external evidence, but rerunning their previously examined test panels is not a pristine replication. Use genuinely untouched users/prompts or a new collection where possible. Otherwise describe it accurately as a frozen cross-dataset evaluation on previously studied data.

**3) Yes: change the title, abstract and central claim.**

My proposed title is:

**Detectable Preferences, Limited Choice Gains: Evaluating Personalised Reward Models for New Raters**

Proposed abstract, under 230 words:

> Personalised reward models aim to predict individual judgements from a few ratings, but detectable user information need not yield better choices. We evaluate adaptation to previously unseen raters on held-out prompts, using population, shuffled-rater and scale-use controls. Text-independent rater offsets improve predictive log-likelihood by 0.08–0.10 nats per rating at twenty ratings on three preference and safety datasets. On MultiPref and native PRISM choices, evaluated methods’ own adaptation gains have upper 95% bounds below one percentage point at this budget. Semi-synthetic controls show that published learners can miss preferences recoverable when their generating attributes are supplied. On Community Alignment, LoRe’s own adapted parameters outperform shuffled users’ parameters by 3.27 percentage points, although adaptation reduces accuracy relative to its unadapted state by 2.34 points. An exploratory within-country control retains this contrast. Further exploratory analyses, developed after examining test results, find that residual length effects reproduce across disjoint prompt sets. At twenty choice events, covariance-based adaptation with attributes and shrinkage selected on training users yields gains of 0.49 choice points and 0.0088 nats per pair, below the pre-specified one-point accuracy threshold. These results distinguish scale-use prediction, detectable user-specific content signal and useful adaptation, while leaving the exploratory gains for independent confirmation.

The central claim should be:

> Across the studied graded-rating tasks, scale-use offsets provide substantial predictive gains. User-specific content signal is detectable on Community Alignment, but the evaluated adaptation procedures deliver limited average choice gains at the tested budgets.

Four immediate textual corrections:

- Replace **“individual signal exists but does not pay”** with **“individual signal exists; estimated choice gains remain small.”** A positive half-point gain may have value. Your one-point threshold is a research criterion, not a universal utility threshold.
- Restrict **“binary labels remove the signal”** to the tested MultiPref construction. CA now demonstrates predictable individual structure using binary choices.
- Delete **“the only validated content gain on Community Alignment.”** Stage 8 already reports positive own gains and positive within-country own−other contrasts for VPL and LoRe-reg. The budgets, cohorts and baselines differ, so compare them explicitly.
- Replace **“paragraphs/list parts do not transfer”** with **“transfer was not established for paragraphs or lists on the evaluated support→test split.”** Intervals covering zero do not establish absence.

The introduction, contributions, discussion and impact statement need the same qualification. The old abstract’s final CA example is now an incomplete account of your own evidence.

**4) The greatest remaining weaknesses are test-informed method development, incomplete separation of preference from task mix, and unresolved baseline fidelity. These determine my next three experiments, in this order.**

**First: independently evaluate the complete Amendment-4 procedure.**

Choose the target dataset and untouched evaluation population before examining outcomes. Freeze the existing procedure rather than adding another adaptation family. Include population weights, abstention, the tuned rank-2 comparator, and a comparably validated simple attribute-prior baseline. This last comparator determines whether transferable-covariance estimation adds value beyond supplying attributes and tuning shrinkage.

Use twenty **choice events** as the primary CA-like budget. Retain the same person-specific scale offsets in graded-data comparisons. Report user and prompt uncertainty, with a declared weighting over users and events.

Pre-set decisions:

- A reproducible predictive benefit requires positive lower bounds for both own−population accuracy and log-likelihood.
- A practically meaningful choice-gain claim requires the accuracy lower bound above **+1 point**.
- An upper bound below +1 supports a sub-threshold conclusion for this procedure and population.
- A methodological advantage over ordinary validated shrinkage requires a positive paired accuracy contrast against that baseline.
- Any outcome failing these conditions is reported without further test-driven revisions.

This experiment would most directly improve the paper’s acceptance prospects.

**Second: test length transfer on a shared, balanced prompt bank.**

Give users within each language a common distribution of prompts, with disjoint support and test prompts. Balance response length and formatting variation across task types; randomise presentation. Include the population model and an own-versus-other comparison matched within language and support information.

This addresses the major identification problem: users’ stable prompt distributions can create stable residual coefficients without different preferences conditional on the same tasks.

Pre-set decisions:

- Make length the single primary attribute.
- Require a positive support→test cross-covariance and a positive own−matched-other prediction contrast on the balanced bank before claiming reproducible individual length-related preference signal.
- Apply the existing +1-point rule separately to practical adaptation.
- If the signal disappears after balancing task exposure, restrict the original finding to user-associated residual structure under CA’s observed task mix.

The within-country derangement and eight-cluster adjustment do not resolve this issue.

**Third: complete a faithful predecessor comparison at matched budgets.**

Finish S11-1 and report every specified outcome. Use WIMHF’s actual feature or representation alongside your list/heading proxy. Resolve LoRe’s native reproduction as far as possible using its official implementation and documented settings. Then evaluate the faithful implementations under your prompt-disjoint protocol.

There is an important correction here: WIMHF trains its global model on low-volume annotators and adapts high-volume annotators excluded from that population-model training. Calling its personalisation evaluation simply **“seen users” is misleading**. The pertinent differences include feature discovery, annotator selection and prompt separation. [WIMHF, §5.2](https://arxiv.org/html/2510.26202v1#S5.SS2)

Pre-set decisions:

- Apply S11-1’s existing reproduction criterion: positive lower bound for the k = 16 AUC gain.
- Report accuracy and own−other independently; an AUC result cannot establish a one-point choice benefit.
- Change protocol components separately to identify which changes affect the result.
- If native reproduction remains unresolved, restrict conclusions to your implementations and evaluation settings. Do not attribute the discrepancy to evaluation design alone.

**5) These are the statistical and logical issues I would fix before submission.**

- **Positive own−other with negative own gain is coherent.** On the same Stage 8 records, the reported numbers imply other−k₀ = −2.34 − 3.27 = **−5.61 points**. Own parameters are considerably less harmful than another user’s parameters. Under appropriate exchangeability controls, that is evidence of user-linked predictive information; it is not a +3.27-point adaptation benefit. Preserve the frozen rule’s literal outcome, then explain its estimand. Also reconcile the appendix’s claim that own−other alone is “not evidence of personalisation” with the CA interpretation: the consistent distinction is between information and benefit.

- **Within-country permutation does not establish irreducibly individual preference.** It removes country as the explanation for the large contrast. Within-country demographics, task mix, response exposure and support informativeness remain possible explanations. “A within-country user-specific contrast” is warranted. “Individual, not linguistic or national” is too categorical.

- **Ĉ is an uncentred cross-moment as defined.** In general,
  \[
  E[z^A(z^B)^\top]
  =\operatorname{Cov}(z^A,z^B)+E[z^A]E[z^B]^\top.
  \]
  Calling it covariance requires a justified zero-mean condition or appropriate centring. Shared population-model misspecification can generate nonzero means and user-dependent biases. Report half-specific means and centred cross-covariances, including within-language calculations. Cross-fitting users does not automatically remove these biases.

- **Ĉ exceeding fitted σ² is not a mathematical contradiction.** They are different estimators, potentially fitting different effective models. One-step nonlinearity, ill-conditioning, regularisation, correlated attributes, misspecification and heavy tails can all contribute. A ratio of 2.7 does not specifically diagnose heavy tails. Calling the ratio a **“transferable share”** suggests a bounded decomposition that has not been established. Use “cross-moment relative to fitted random-slope variance,” or justify the decomposition and propagate uncertainty in both quantities.

- **The covariance-to-EB step makes stronger assumptions than the diagnostic’s detection test.** The rewrite \(C(I+IC)^{-1}s\) is algebraically correct. However, treating \(I^{-1}\) as the noise covariance requires the relevant information identity. Three chosen-versus-other pairs from one choice event are dependent. If the fitting criterion is a composite Bernoulli likelihood, its curvature need not equal score variance. An event-cluster sandwich variance or a coherent choice likelihood deserves examination. Shrinkage of 0.125–0.25 could compensate for likelihood misspecification as well as an oversized prior; it does not uniquely identify the explanation.

- **Simulation calibration must preserve the choice-event mechanism.** Verify whether simulated labels respect a common winner among four candidates. Independently redrawing pair labels would not preserve that dependence structure. Also verify which controls refit the complete population model, rather than treating estimated probabilities as known. The stated protocol does not establish these implementation details.

- **Your criticism of the original 20-replicate coverage rule is numerically correct, but incomplete.** Under true 95% coverage, observing at most 18 covered intervals out of 20 has probability approximately **0.264**. Nevertheless, the original failure also included stable-control detection rates of 0.70 and 0.30. It cannot all be dismissed as a noisy coverage criterion. List/heading detection remains only 109/200 under the amended experiment.

- **Passing 10/200 does not establish a false-detection probability of at most 5%.** Length passes the criterion you wrote. But the exact two-sided 95% binomial interval for 10/200 is approximately **2.4–9.0%**. A positive lower endpoint of a nominal two-sided 95% interval ordinarily corresponds to a 2.5% upper-tail test, so distinguish nominal size from your 5% acceptance tolerance. Likewise, 169/200 stable detections passes the point-estimate power rule, but its exact 95% interval extends below 80%. Future calibration should use explicitly declared Monte Carlo precision and report uncertainty around error rates and power. [Morris, White and Crowther](https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/)

- **Multiplicity remains under-addressed.** Stage 8 detects if any method passes either contrast; Stage 11 tests three primaries and numerous later variants. Holm correction only across the 24 secondary attributes does not cover those families. The large LoRe contrast is unlikely to hinge on this, but report an adjusted detection analysis. Keep the frozen literal outcomes unchanged. The “all methods below threshold” conjunction has a different testing structure from “any method detected”; do not mechanically apply the same multiplicity argument to both.

- **The trimming results demonstrate sensitivity, not robustness of the variance magnitude.** Length appears more stable than paragraphs and lists, but the quoted trimmed ranges are point estimates without uncertainty. Trimming can remove genuine concentrated heterogeneity as well as numerical artefacts. Recompute uncertainty for a frozen robust estimator, and distinguish a robust positive sign from a robust covariance magnitude. “Trimming halves it” also does not accurately describe every attribute.

- **The simulated learner gain is not a learnability ceiling.** The oracle is an upper benchmark under the assumed generative model. TR3’s +2.81 is the simulated performance of one learner. The concentration-mixture result, +0.38, falls within a factor of three of +0.13; the shrink-only result +0.53 remains about **5.3 times** below +2.81. Thus the recorded rule supports withdrawing the order-of-magnitude claim. It does not establish that a concentrated non-Gaussian prior explains CA. The concentration analysis on real users was uninformative, and five Monte Carlo draws per fold need uncertainty before supporting a ratio boundary.

- **Paragraph transfer remains unresolved.** The half-split and support→test paragraph intervals overlap. Their difference cannot be inferred from one being significant and the other not. The diagnostic and adaptation cohorts also differ in eligibility and support construction. Estimate the paired difference on a common cohort before claiming a loss of transfer.

- **Likelihood improvement is not specifically a calibration improvement.** Log score measures overall probabilistic prediction quality; improvements can involve calibration and discriminatory resolution. Call +0.0088 a **predictive log-likelihood gain** unless you separately demonstrate improved calibration. [Gneiting and Raftery](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf)

- **The JSON’s likelihood conversion is correct; its baseline accounting needs reconciliation.** Dividing 0.884181… and its bounds by 100 gives +0.00884 [0.00612, 0.01158] nats. However, the accuracy contrasts imply rank-2−population = 0.4885967 − 0.2975949 = **+0.1910 points**, rather than the earlier +0.17. Recompute every comparison from the same keyed records, weights and population predictions. If `pop_mismatch_rate` measures hard-decision disagreement, its small value does not bound differences in log-likelihood.

- **Twenty pairs and twenty events are different budgets.** Stage 8 uses twenty adaptation pairs; Stage 11 uses twenty choice events, each furnishing three dependent pairs. They also evaluate different user cohorts. Make these distinctions visible wherever gains are compared.

Finally, repair the four-versus-five-fold entries and NaNs in Stage 8, and report the missing S11-1 outcomes. Human–human agreement below model accuracy is a useful reference point, but provides no ceiling on predictable personalisation.