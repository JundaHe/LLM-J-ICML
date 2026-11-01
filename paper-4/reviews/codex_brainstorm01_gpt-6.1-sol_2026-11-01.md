**I would prioritise a strengthened B: measure which user differences reproduce across prompts, then learn adaptation from that reproducibility.** Put explanation-based identification of preference dimensions second. These offer the best combination of scientific value, feasibility and a useful outcome if ranking gains remain small.

The paper’s main vulnerability is now the missing explanation: **why can substantial fitted heterogeneity coexist with almost no useful adaptation?** Resolving that would add more than another personaliser or dataset.

Two literature findings materially affect the novelty assessment:

- An October 2026 PRISM paper already studies stated priorities, concrete written feedback, stable feature weights and held-out choice prediction. A substantially overlaps it. If this is your group’s work, the same contribution-separation issue applies. [*Abstract Priorities, Concrete Rewards*](https://arxiv.org/abs/2610.30763)
- WIMHF already fits Gaussian-prior user coefficients over interpretable features on Community Alignment and evaluates active example selection. Its reported personalisation outcome is AUC. This is a particularly close precedent for SAP and C; a focused comparison under your protocol is important. [WIMHF, §5.2](https://arxiv.org/html/2510.26202v2#S5.SS2)

I would therefore position the extension around **transferable heterogeneity**, with SAP as an instrument for studying it. I would not assign a defensible numerical acceptance probability to the proposed additions.

Your three candidates look as follows.

**A. Stated versus revealed preferences: feasible, but currently limited headline novelty.**

The useful question is whether a user’s statement supplies **incremental information about future choices**, after accounting for the prompt and population preferences. Correlation between “importance of factuality” and factuality-related ratings is insufficient.

A clean model is

\[
\theta_u\mid s_u\sim N\!\left(\mu+B s_u,\Sigma\right),
\]

with separate representations for relative survey priorities and concrete instructions extracted from `system_string`. Learn \(B\) using training users only. Broad importance ratings should not be treated directly as signed utility weights: nearly everyone can rate every desirable attribute highly.

Evaluate population, statements alone, choices alone, and statements plus choices at \(k=0,5,20\). Keep scale-use adaptation identical across contrasts. Shuffle statements between users within language as a control.

- **Novelty:** low for the broad comparison; moderate for a calibrated conditional prior with clear prospective gains. Text summaries conditioning personalised reward models also have substantial precedent. [PLUS](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c7af751b5e0a407c62ac023e3cb381f9-Abstract-Conference.html)
- **Feasibility:** roughly 3–6 days with a small fixed extraction schema.
- **Main risks:** consensus statements, noisy attribute measurement, and profiles predicting users’ prompt selection rather than their preferences conditional on a prompt.
- **Result needed:** a meaningful zero-shot choice gain, or a substantial improvement over the same \(k\) choices without the statement. Another near-zero survey result would add little novelty.

**B. Stable versus context-dependent preferences: highest scientific value, with an identification caveat.**

Large fitted \(\sigma^2\) is compatible with several explanations:

1. Stable preferences exist, but twenty observations contain little information about them.
2. Preferences transfer within recurring contexts but poorly between contexts.
3. Population-model errors and differences in users’ item exposure inflate random-slope variance.
4. Approximate inference or plug-in MAP predictions damage an otherwise useful posterior.
5. Heterogeneity changes probabilities substantially while rarely changing the preferred response.

Your experiment should distinguish these possibilities.

The important caveat is that **a unique user-by-prompt effect cannot generally be separated from annotation noise without repeated judgments**. You can identify reproducibility across independent prompts within recurring task categories. You cannot simply estimate “contextual preference variance” at individual-prompt resolution.

Context-conditioned rewards are already well established, including explicit context supervision and context-aware routing. The novelty must be the measurement and its consequences for adaptation. [Pitis et al.](https://proceedings.neurips.cc/paper_files/paper/2024/hash/82acbbc04435f6c1e7f656b1cbe4ad82-Abstract-Conference.html), [MiCRo](https://aclanthology.org/2025.emnlp-main.882/)

- **Feasibility:** about one week for three physical attributes and a few broad contexts.
- **Main risks:** insufficient observations per user and context; different feature geometry masquerading as context dependence; another underpowered split-half null. Your unsuccessful S3-C makes a prospective power check essential.
- **Result needed:** positive transfer between different prompts within a context, weaker transfer across contexts after controlling source information, and ideally an adaptation rule that exploits this distinction. A context gap caused entirely by harmful cross-context adaptation is insufficient.

**C. Active elicitation: useful follow-up, weak standalone novelty.**

Information gain, Fisher-information design and regret-based preference elicitation have long histories. Recent LLM work also addresses Bayesian cold-start questioning directly. [Bıyık et al.](https://iliad.stanford.edu/pdfs/publications/biyik2020active.pdf), [CAPE](https://proceedings.mlr.press/v306/bose26a.html)

For your paper, the potentially distinctive acquisition objective is **information about transferable, decision-relevant preference dimensions**. Predictive entropy alone can select intrinsically ambiguous comparisons.

- **Feasibility:** 3–5 days for retrospective pool-based selection.
- **Main risks:** learning a dimension that does not transfer; optimising the wrong posterior; inadequate logged candidate pools.
- **Result needed:** active \(k=5\) or \(10\) produces a positive real choice benefit and outperforms random \(k=20\). Matching a zero-gain random baseline establishes little.
- **Evaluation constraint:** select only among comparisons whose labels genuinely exist for that user, hide unqueried labels, and keep a fixed evaluation set. LLM-generated answers to hypothetical queries would provide simulation evidence only.

I see four additional directions worth considering. The first strengthens B; the remaining three are distinct additions.

**1. Learn a transfer operator instead of using fitted variance as the adaptation prior.**

This is my top methodological choice.

In a Gaussian local approximation, suppose a history provides a noisy estimate

\[
z_H=\theta_H+\varepsilon_H.
\]

The optimal linear prediction of preferences in a query context is

\[
\widehat\theta_Q
=
\underbrace{\operatorname{Cov}(\theta_Q,z_H)}_{C_{QH}}
\operatorname{Var}(z_H)^{-1}z_H.
\]

The crucial quantity is \(C_{QH}\). A large training-user variance does not establish that this cross-prompt covariance is large.

**Concrete experiment.** Construct independent support/query episodes from training users, using disjoint prompt groups. Estimate a regularised map from support residual scores to query preferences. Start with length, paragraph structure and markdown structure—the attributes implicated by the existing CA results—and allow the map to depend on broad prompt categories.

Train the map on query prediction, with a zero-update option. Compare it against:

- population weights;
- validated SAP, including its abstention option;
- the tuned rank-2 comparator;
- feature-matched ordinary hierarchical shrinkage.

Use cross-products of independent residual-score blocks as the diagnostic. Avoid correlations between heavily shrunk MAP coefficients. This measurement has classical relatives in cross-validated second-moment estimation; covariance-based empirical Bayes is also established. The contribution would be its use to distinguish and learn transferable reward heterogeneity. [Cross-validated second moments](https://github.com/jdiedrichsen/pcm_toolbox/blob/master/pcm_estGCrossval.m), [multivariate adaptive shrinkage](https://github.com/stephenslab/mashr)

**Decisive result.** Fitted variance remains large, but reproducible covariance concentrates in particular attributes or context relationships; learning that structure improves held-out prediction over validated SAP. Preserve signed cross-context relationships: a preference can reverse systematically between contexts.

**Headline change:** *Which Individual Preferences Transfer? Measuring and Learning Cross-Prompt Personalisation.*

If the method merely abstains exactly as SAP already does, that alone is no new method result. A well-powered demonstration explaining why the fitted variance fails would still strengthen the empirical paper.

**2. Treat explanations as observations of the preference dimension being applied.**

A choice says which response won. An explanation can identify the dimension used: correctness, detail, directness, relevance, tone, or a particular interpretation of the request. This directly addresses your strongest synthetic finding: supplying the right dimensions changes learnability.

**Concrete experiment.** From training-user explanations, build a small ontology of observable response properties and scoped criteria. Use Qwen to extract structured evidence from a new user’s support explanations:

- criterion mentioned;
- direction of preference;
- whether the statement appears local to the task or general;
- extraction confidence.

Use these as noisy constraints on attribute weights or relevance, rather than an unrestricted persona summary. Evaluate future prompts without their explanations.

Compare the same support events with choices alone versus choices plus explanations. Include label-only generated summaries and matched other-user explanations that convey the same choice direction. Exact same-comparison matches are especially valuable; where unavailable, describe matching as an approximate control.

**Decisive result.** Own explanations improve future choice prediction beyond both the same labels and matched other-user explanations. That last contrast distinguishes user information from generic help understanding the response.

**Headline change:** *Explanations Identify Transferable Preference Dimensions from Sparse Feedback.*

Generic rationale-conditioned reward modelling is crowded. The stronger angle is identifying the additional information channel and testing whether it belongs to the person. Keep the population claim restricted to users who provide explanations, and do not equate annotation counts with human effort.

**3. Personalise attribute assessments separately from trade-off weights.**

Your MultiPref result suggests an underdeveloped distinction. People can disagree about **which response is more helpful or truthful**, while using a similar rule to combine their own aspect assessments.

The 97.5% oracle result concerns the combination rule conditional on contemporaneous assessments. It does not test whether those assessments themselves contain transferable user structure.

**Concrete experiment.** Fit four systems:

| Attribute assessments | Combination weights |
|---|---|
| Population | Population |
| Personalised | Population |
| Population | Personalised |
| Personalised | Personalised |

Predict test-item aspects from text and support history; never supply the target user’s test aspects to the deployable systems. Give all four systems the same available support annotations. Remove aspect-specific scale use before attributing an improvement to content.

Evaluate both future aspect judgments and overall choices.

**Decisive result.** Personalised assessment predicts held-out aspect directions and improves overall choice prediction, while personalised combination weights add little.

**Headline change:** *Personalisation Predicts How Raters Assess Responses, More Than How They Trade Off Attributes.*

This is an observational decomposition. Concurrent labels cannot establish a psychological or causal distinction between beliefs and values. Nevertheless, a transferable predictive separation would substantially sharpen the pluralistic-alignment interpretation.

**4. Eliminate symmetric scale-use offsets from content estimation by conditioning on intensity.**

This is a cheap, mathematically clean companion method.

Write the five levels as \(Y\in\{-2,-1,0,1,2\}\), with

\[
p(Y=y\mid x,u)\propto
\exp\{\ell_y(x)+b_{u,|y|}+y\,\theta_u^\top a(x)\}.
\]

Conditional on observed nonzero magnitude \(M=|Y|=m\),

\[
P(Y=+m\mid M=m,x,u)
=
\sigma\!\left(
\ell_{+m}(x)-\ell_{-m}(x)
+2m\,\theta_u^\top a(x)
\right).
\]

**The symmetric scale-use offsets cancel exactly.** Content weights can therefore be estimated from a conditional likelihood without estimating those nuisance offsets jointly.

**Concrete experiment.** Compare conditional estimation, joint SAP and binarised estimation on the same graded support events. Stress-test them under varying symmetric response styles, then evaluate real held-out choices.

**Decisive result.** Conditional estimation recovers content more reliably under scale-use variation and improves unconditional real predictions. A conditional-score gain alone would establish a narrower measurement result.

**Headline change:** *Separating Content Learning from Scale Use with Conditional Preference Likelihoods.*

Conditional likelihood and response-style separation have statistical precedents, so the new contribution would be the reward-model formulation and demonstrated consequences. [Johnson, 2014](https://journals.sagepub.com/doi/10.1177/0146621614539039) The cancellation applies to the stated symmetric-offset family; it does not eliminate arbitrary rater transformations. Test-time intensity must remain unavailable to deployment predictions.

My ranked allocation would be:

1. **First, days 1–7: transferable-heterogeneity diagnosis and transfer-trained adaptation.** Begin with a focused WIMHF comparison using its formatting concept, accounting for language, conversation budgets and AUC versus choice accuracy. Then run the three-attribute diagnosis, posterior-predictive control and transfer map. This has the highest chance of producing a coherent scientific explanation.
2. **Second, days 8–16: explanation-based dimension identification.** This has the greatest chance of producing a new real ranking result. Reuse the first experiment’s transfer evaluation and keep the ontology small enough to score once and cache.
3. **Third, days 17–24: assessment-versus-weight decomposition on MultiPref.** This offers a distinct interpretation of disagreement even if explanation gains are weak. The conditional-likelihood method is a small analytical companion to implement earlier if inexpensive.

For a two-week schedule, complete the first direction and one compact explanation experiment. I would defer broad survey modelling and active acquisition until a transferable signal has been identified.

For the top choice, I would freeze the following pre-registration. These are proposed design choices, not findings. Since CA outcomes have already informed the hypothesis, describe this as a prospectively specified new analysis of previously studied data.

**Target and estimand.** Primary population: the frozen CA cohort eligible for twenty support **choice events**, evaluated on different held-out prompt groups. Average within events, then within users, then across users; retain the original language stratification. If an event generates several pairs, keep them together throughout.

For method \(M\) and comparator \(B\),

\[
\Delta_{\mathrm{LL}}(M,B)
=
E_u E_{e\in Q_u}
\left[
\log p_M(Y_e\mid X_e,H_{u,20})
-
\log p_B(Y_e\mid X_e,H_{u,20})
\right].
\]

The main estimand is the gain from the user’s history beyond population prediction. Choice-accuracy gain is the decision-relevance endpoint.

**Frozen feature and context definitions.** Primary adaptation attributes: log length difference, paragraph structure and markdown structure. Fix normalisation using training data. The existing 24-attribute family is secondary.

Define three prompt-only categories before inspecting new outcomes: information/explanation, advice/judgment, and writing/creation. Freeze the classifier, ambiguity rules and label-blind quality checks. Fit population attribute-by-context and language effects in every comparator.

**Methods and contrasts.**

- Transfer-trained adaptation versus the population model.
- Transfer-trained adaptation versus a comparator selected on validation from SAP and rank-2, with abstention allowed.
- Same-context versus different-context support, using equal support budgets and the same target events.
- Own-history versus another user’s history as a specificity control.

Use the full \(k=20\) cohort for the main predictive comparison. For the context diagnostic, predefine an eligible subset with at least five same-context and five other-context support events. Report its coverage.

Source information must be addressed: use training-fixed Fisher normalisation and a prespecified design-matching sensitivity analysis. Different attribute variation across contexts can otherwise create a transfer gap even with stable preferences.

**Required controls.**

1. **Stable-preference positive control:** simulated stable coefficients on the actual CA observation graph and covariates, with known-feature reference inference.
2. **Context-dependent positive control:** coefficients that reproduce within broad contexts but vary between them.
3. **No-user-signal control:** labels generated without person-specific content effects.
4. **Misspecified-population control:** omitted population context interactions, testing whether they create spurious user variance.
5. **Inference control:** posterior-predictive integration versus MAP plug-in prediction.
6. **Representation control:** a small semantic formatting feature baseline, so physical counts alone cannot determine the conclusion.

A user-identity permutation should be presented as an exact test only where its required exchangeability holds. Prompt overlap does not itself establish identical comparison overlap.

**Power and uncertainty.** Freeze simulation strengths, seeds and analysis code before examining new real contrasts. Assess power on the actual sparse design, including a reference scenario with approximately one point of recoverable choice improvement. Require at least 80% simulated power before using a null to discuss absence at that strength.

Use a two-way user/prompt-group bootstrap for predictive contrasts, retaining complete events. Average adaptation draws before inference. Fix a multiplicity procedure for the primary contrasts; avoid declaring whichever attribute, context or metric happens to succeed.

**Decision rules.**

| Outcome | Permitted conclusion |
|---|---|
| Same-context transfer is positive, exceeds cross-context transfer after design controls, and calibrated controls distinguish the two | Evidence for context-dependent transfer in the tested family |
| Cross-context reproducibility is positive, but twenty-shot adaptation remains ineffective | Stable structure exists; the tested adaptation budget or inference remains inadequate |
| Both forms of reproducibility are near zero, with adequate power | Large fitted variance lacks corresponding transferable signal in the tested feature family |
| Posterior integration succeeds where MAP fails | Inference approximation explains part of the failure |
| Transfer-trained adaptation beats population and validated personalisation baselines | Evidence for the proposed method |
| Adaptation only selects zero | Successful abstention; no demonstrated methodological advance over existing SAP abstention |

For **practically meaningful ranking personalisation**, retain your existing demanding threshold: the lower confidence bound exceeds **+1 choice-accuracy point** over population prediction. For a context-dependence claim, require positive same-context transfer as well as a transfer gap. Do not interpret harmful cross-context adaptation alone as evidence that stable local preferences have been learned.