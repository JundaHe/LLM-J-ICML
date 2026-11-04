**A 7/10 version is realistically reachable. An 8/10 version needs a stronger empirical result, not simply more validation runs.** The best route is an evaluation paper that establishes predictable differences between users on identical tasks, while separately measuring whether exploiting those differences improves choices.

**The single biggest lever is the CA shared-item subset.** That new fact changes my round-5 recommendation. A credible shared-item study could replace the paper’s weakest observational argument with its strongest experiment. Another adaptation family would not.

I would authorise four work items, with firm stopping rules. The numerical thresholds below are proposed design choices, not forecasts.

1. **Make CA’s shared items the main identification study.**

   **Design.** Begin with a label-blind exposure audit, before examining new performance contrasts. Establish:
   
   - Whether the same response texts occur with the **same prompt, visible context, complete four-response set and presentation conditions**.
   - Which users rated these items, their support availability, and the user–item overlap graph within language/country and user fold.
   - How much of the eligible panel consists of a small number of prolific users or repeated prompts.

   Start from complete response-set exposures, rather than the extracted winner-versus-other rows. **The existing shared-pair count is outcome-selected:** a pair appears in that extraction only when one of its members wins. Two losers provide no observed preference between them. Different surrounding candidates can also change the meaning of an otherwise identical pair.

   Use **first turns** for the primary study, avoiding the conversation-history problem. Define the primary item by exact prompt and response-set identity; handle original response positions explicitly. Do not treat near-duplicate text or embedding matches as identical items.

   The draft’s statement that CA has no shared prompt bank must already be removed: its documentation explicitly describes prompt overlap. That documentation does not establish identical candidate sets; your audit must establish that. [CA dataset documentation](https://huggingface.co/datasets/facebook/community-alignment-dataset/blob/main/README.md)

   Freeze the Stage-12 **validated isotropic procedure as the primary learner**; retain TRV as a secondary comparator. Each evaluated user receives twenty support events from disjoint prompt groups and conversations. Refit every population model, prior and validation choice using eligible training users and prompts. Reuse embeddings, **not fitted predictions or priors that incorporated the new test items**.

   Run two distinct tests:

   **Identity signal on identical items.** Compare assigning users their own adapted parameters with exchanging parameters between eligible raters of the same item, within the same evaluation fold and language/country stratum. For two users \(u,v\) who choose different responses \(a,b\) from the identical set, the assignment score is

   \[
   S=s_u(a)+s_v(b)-s_u(b)-s_v(a).
   \]

   The common population response scores cancel. Evaluate whether the model predicts the actual assignment better than the swapped assignment, using the conditional probability \(\sigma(S)\) and its log score against the \(1/2\) baseline. This directly tests **whether histories predict who makes which choice on the same item**. It is a conditional disagreement diagnostic, not ordinary choice accuracy.

   **Beneficial personalisation.** On **all eligible shared-item events**, compare own adaptation with the population model using pairwise winner-versus-other accuracy and log-likelihood. Do not restrict this evaluation to disagreements.

   Average the identity diagnostic within item before pooling so heavily rated items do not dominate. Use crossed user/prompt inference that accounts for users appearing as both targets and donors; a fixed donor-map target-user bootstrap is insufficient.

   **Pre-set decisions and paper wording.**
   
   - Positive conditional-assignment log-score lower bound: “Support histories predict differences between users choosing among identical displayed alternatives.”
   - That result plus positive accuracy and log-likelihood gains over the population model: “Those differences support beneficial personalisation on the shared-item panel.”
   - Identity signal positive, population-relative gain unestablished: “Individual differences are predictable, but exploiting them has not established a choice benefit.”
   - A sufficiently precise accuracy upper bound below one point: retain the procedure-specific sub-threshold statement.
   - Null or wide identity intervals: no stronger identification claim. This does **not** establish absence of individual preferences.
   - Insufficient identical exposures or overlap: declare the design infeasible. Do not progressively relax “identical” until something works.

   Even success identifies persistent, user-specific **choice predictability**, not an intrinsic causal “length preference.” Attention, position sensitivity and unmeasured user characteristics remain possible explanations.

   **Cost:** roughly half a day for the audit; another one to two analysis days plus CPU jobs if cached first-turn features are usable. No new embeddings should be necessary. The 147,939 ratings do not establish effective sample size or power.

2. **Run one bounded external evaluation of the frozen TRV/isotropic procedures.**

   **Design.** I would choose **MultiPref**, using its existing features and twenty non-tie comparison events per support set. Fix the tie-exclusion rule, user/prompt folds and five support draws before results. Evaluate native preference direction as binary choice; retain the existing graded-rating results separately.

   Freeze both procedures’ candidate attributes, grids and selection algorithms exactly. Refit population models and priors only on external training folds. This transfers the **procedure**, not CA’s fitted numerical coefficients. Use isotropic adaptation as the primary benefit test and TRV-minus-isotropic as the predeclared covariance comparison.

   This is worthwhile because it is cheap and tests another population and annotation setting. But be precise: **MultiPref participants are external to CA; they are not untouched by this research project.** Fresh folds cannot erase prior benchmark inspection.

   PRISM is a reasonable alternative if chosen in advance. I prefer MultiPref here because the support unit is straightforward. The existing PRISM count of users with twenty pairs does not establish eligibility for twenty choice events. Do not run both datasets and promote whichever produces the better story.

   **Pre-set decisions and paper wording.**
   
   - Accuracy and log-likelihood lower bounds above zero under primary crossed inference: evidence that the frozen procedure benefits held-out users in another dataset.
   - Accuracy upper bound below one point: a bounded, procedure-specific small-gain result in that setting.
   - Otherwise: inconclusive external benefit, or harm if supported.
   - TRV-minus-isotropic lower bound above zero: evidence of covariance advantage in this setting. Otherwise, that advantage remains unestablished.

   A precise small-gain result would strengthen the measurement paper. A wide interval would add little. Neither outcome licenses “personalisation generally cannot help.”

   **Cost:** approximately half to one working day, mostly CPU, assuming the required cached features exist. No new representation search.

3. **Use turn 3 only for direct coefficient transport; leave turn 4 unopened.**

   Another Stage-12-style refit on later turns has low marginal value. **The useful new question is whether fixed first-turn user coefficients predict later choices.**

   **Design.** Freeze each user’s first-turn deviation \(\hat\delta_u^{(1)}\), estimated from twenty support events. Evaluate third turns from different conversations, with support–test prompt separation. Do not estimate any user coefficient from third-turn labels.

   Fit a competent third-turn population model on other users, then compare

   \[
   m_3(x)
   \quad\text{with}\quad
   m_3(x)+a_3(x)^\top\hat\delta_u^{(1)}.
   \]

   Preserve the first-turn attribute units and fitted adaptation strength. No third-turn rescaling, attribute selection or shrinkage tuning for the transported deviations. Make isotropic deviations primary.

   Include the **full visible conversation history** in the third-turn population features, using a fixed serialization and context-length rule. Otherwise, the study repeats a known weakness. Exclude post-choice explanations and other information unavailable when predicting the choice.

   This is a new transport study, not an unchanged replication of Stage 12. The third-turn population baseline can be refitted; the user deviations cannot.

   **Pre-set decisions and paper wording.**
   
   - Positive accuracy and log-likelihood lower bounds: “First-turn user deviations improve prediction in later, disjoint conversations beyond a history-conditioned population model.”
   - Identity-swapping evidence alone: association transfers, but beneficial coefficient transport is unestablished.
   - Null or harm: coefficient transfer is unsupported for this procedure and panel. Do not infer that people’s preferences are unstable.
   - Insufficient eligible users or excessive embedding cost: skip this arm **before examining outcomes**, and retain the limitation.

   This still studies previously analysed people. It addresses coefficient transport and omitted history, not generalisation to untouched participants. Report later-turn attrition explicitly.

   **Cost:** one implementation day plus one embedding pass. Use the supplied eight-hours-per-400k-texts rate only as a reference; longer histories can cost more. Count eligible texts first and cap this arm at roughly one GPU day. **Do not then open turn 4 to rescue the result.**

4. **Rewrite around the measurement contribution and reduce the published-method claims.**

   **Design.** Start this immediately. Build a claim–evidence table recording each headline’s population, endpoint, baseline, implementation, uncertainty analysis and developmental status.

   Reduce the contributions to three:
   
   - Graded-rating improvement can arise from text-independent scale use.
   - Predictable user differences require a separate test, ideally on identical items.
   - Beneficial choice personalisation requires improvement over a competent population model; own-versus-other does not measure that benefit.

   Move SAP’s development history, covariance simulations and most Stage-11 amendments to the supplement. Keep a compact positive-control result because detector failure materially limits the negative conclusions.

   **Do not spend another week debugging LoRe.** Describe compressed-feature implementations as such. Keep unresolved native reproductions in the appendix. WIMHF’s discovered SAE feature and your line-count proxy are different implementations; the latter cannot refute the former. [WIMHF, §5.2 and Appendices D–E](https://arxiv.org/html/2510.26202v2)

   Repair inference from underlying records, including paired factorial contrasts and donor dependence. Retrospective multiplicity corrections remain exploratory; they do not turn the development history into confirmatory evidence.

   **Pre-set editorial rule.** A claim about a published method in its native setting requires a verified native implementation and matched evaluation. Otherwise, the claim explicitly concerns the evaluated implementation. Passing a synthetic detector control still does not justify a universal negative conclusion.

   **Cost:** two to three concentrated writing/audit days; no GPU requirement.

The title-level story should be **“What Do Gains in Personalised Reward Modelling Measure?”**

If the shared-item study succeeds, the central statement becomes:

> Histories predict which users choose which responses on identical tasks, but identifying those differences and improving choices over a population model are separate achievements. Graded-rating gains, user discrimination and net choice gains therefore require separate evaluations.

That is stronger than “our methods mostly fail.” If the shared-item study finds a substantial gain, revise the “limited choice gains” headline accordingly. A positive result would strengthen this conceptual contribution rather than spoil it.

Cut the method-paper framing around SAP/TRV, the analysis diary in Section 6, human-agreement comparisons presented as ceilings, and general statements that predictable individual differences mostly concern scale use. DICES already shows why endpoint qualifications matter: a safety threshold can change a decision.

The main risks are concrete:

- **The shared subset may be unsuitable.** Exact contexts, candidate sets, eligible users and overlap matter more than the headline count.
- **Its population may be narrow.** A curated prompt bank rated by prolific annotators does not represent all CA conversations.
- **More data can expose a different result.** Strong shared-item gains would narrow the current small-gain claim; negative coefficient transport would narrow the persistence claim.
- **New protocols cannot undo previous exposure.** Label these analyses according to their actual developmental history.
- **Three new experiments create more opportunities for selective emphasis.** Freeze the whole plan’s primary claims, weighting, inference families, feasibility gates and stopping rules before outcomes. Compute tests from underlying records; do not recover p-values from interval widths.

**Items 1 and 4 are essential. Item 2 is a cheap supporting check; item 3 earns its cost only as the narrowly frozen transport test above.** If the shared-item design is infeasible or inconclusive, I would not expect additional turn refits and amendments to manufacture a clear accept.