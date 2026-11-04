**I would vote weak accept: 4/6 on ICML’s published 2026 scale, with a subjective acceptance probability of about 60%.** This is a credible measurement paper now, but still vulnerable on significance and the scope of its method comparisons. My assessment uses the inlined record; I could not independently inspect the implementation because the workspace tool failed to start. [ICML scoring scale](https://icml.cc/Conferences/2026/ReviewerInstructions)

**1) What changed**

The largest improvement is confidence in the evidence, rather than a stronger positive result.

- Am. 4 resolves serious concerns about event integrity, centring and bootstrap behaviour.
- The paired comparison against position-only now supports the appropriately limited conclusion: additional assignment value from attributes is unresolved.
- The revised ordering makes the distinction between identity, benefit and baseline sensitivity much easier to follow.
- S13-3 closes an outstanding question with a properly bounded result. It does not strengthen the general transport claim.

The paper now has a defensible contribution: a measurement framework, substantial evidence for text-independent rater calibration, and a controlled demonstration of user-associated choice predictability. **It still does not identify content preferences separately from position on identical items.**

**2) S13-3: the decision and placement are right**

The frozen decision is correct. Describe the split as **accuracy-positive under user clustering, likelihood-inconclusive**, rather than “LL-null.”

| Endpoint | User bootstrap | User × prompt bootstrap |
|---|---|---|
| Accuracy | +0.43 [+0.13, +0.74] points | [−0.08, +0.92] |
| Log-likelihood | +0.0015 [−0.0006, +0.0035] nats | [−0.0020, +0.0048] |

There is no contradiction here. Accuracy measures which side of a decision boundary predictions fall on; likelihood also evaluates the probabilities assigned. The results do not establish why the endpoints differ—for example, they do not establish overconfidence.

The conjunction rule requires both endpoints to clear zero. It fails, while the positive primary accuracy result remains reportable. Neither “transport works” nor “transport has no effect” is justified.

The precise scope matters: this tests **unrescaled first-turn coefficients for additional predictive value beyond a history-conditioned population model**. It does not test every way of transferring information across turns, and it does not establish preference instability.

Its current placement—after benefit and before baseline sensitivity—is appropriate. Keep it as a bounded extension of the benefit analysis. In the abstract, replace the generic negative sentence with something like:

> Frozen first-turn deviations improve third-turn accuracy under user clustering but do not meet the prespecified joint accuracy-and-likelihood criterion beyond a history-conditioned population model.

On the gate:

- **953 qualifying users exceeds 500, so the realised panel passes.**
- The earlier 2,278 was a feasibility pre-count, not a promised analysis sample.
- Am. 5 implements an exclusion already specified in Am. 3. On the recorded chronology, it is a legitimate implementation correction.
- Show the eligibility flow. The pre-count used complete-event counts, whereas final eligibility also involves support selection, disjoint conversations and complete histories. Do not attribute the entire reduction to support exclusion without checking that decomposition.

The smaller realised panel affects precision and the target population. It does not, by itself, explain the inconclusive likelihood result.

**3) Remaining reviewer attacks, ranked**

| Rank | Hardest attack | Cheapest defensible fix |
|---|---|---|
| 1 | **The strongest new identity result could reflect position-associated predictability.** Position-only is informative, and joint − position-only does not clear zero under primary inference. | Put that unresolved separation directly in the abstract and contribution statement. Retain the paired contrast prominently. A content-specific claim would require stronger evidence, such as varied presentation orders. |
| 2 | **Negative conclusions about published methods rest on modified implementations with limited detection power.** Native reproduction discrepancies remain unresolved. | Say “compressed-feature reimplementations” explicitly in the abstract/introduction or their immediate qualification. Present the full-feature sensitivity clearly. Keep conclusions about the evaluated implementations. |
| 3 | **Extensive development on previously examined data weakens confirmatory interpretation.** Freezing a later analysis does not erase earlier adaptation. | Add a compact chronology distinguishing exploratory development, frozen tests on reused data, and newly evaluated second-/third-turn outcomes. Mark intervals as conditional and nominal where appropriate. |
| 4 | **Accuracy benefit across sampled items/prompts remains fragile.** Relevant two-way intervals include zero; MultiPref benefit is unestablished. | Use one main evidence table showing both bootstrap analyses and the exact comparator. Keep “primary user-bootstrap rule met” distinct from generalisation across items. |
| 5 | **The positive controls do not exclude substantial real preferences that these learners miss.** Their conclusions depend on injected families and representations. | Replace “bound what methods could detect” with “characterise recovery for specified injected families.” Keep the power failures beside the real-data ranking null. |
| 6 | **The paper is still too sprawling, and offsets themselves are established machinery.** | Centre the contribution on evaluation and measurement. Compress SAP, covariance development and secondary domains. Remove the superseded §6 prose from the submitted PDF while preserving it in the analysis archive. |

These limitations are compatible with acceptance as an evaluation paper. They substantially weaken a paper framed as demonstrating content personalisation or explaining why published methods generally fail.

**4) Remaining errors and overclaims**

The principal Stage-13 conclusions now follow their rules. The remaining problems are mostly inconsistent claim scope, with several concrete corrections still needed.

**The introduction and §6 overgeneralise properties of symmetric offsets.**

These statements are too broad:

> “Because they are text-independent they barely change which response…”

> “they improve graded-label likelihood, not which response is preferred, and vanish under binary labels”

> “Text-independent offsets change how strongly … not which response”

Text independence alone does not imply these properties. Unrestricted offsets can change direction; your MultiPref DF and DICES results demonstrate that. Exact binary cancellation belongs to the **symmetric A/B offset construction**.

Use:

> On two-sided preference scales, symmetric offsets chiefly model intensity and ties, and cancel exactly for binary A/B labels at a fixed text head. Unrestricted offsets can also change predicted decisions.

Attach the small observed direction effect specifically to graded MultiPref.

**The §6 heading “Binary labels remove the signal on MultiPref” overclaims.**

Small gains from the evaluated learners do not establish absence of predictable user signal, especially given the positive-control failures.

Replace it with:

> Binarisation removes the symmetric scale-use term; evaluated adaptation gains on MultiPref are small.

Also replace “accuracy equals the text-only model’s (−0.0002)” with “accuracy is essentially unchanged.”

**Matching a style baseline does not identify what another model learned.**

The introduction’s statement that a model failing to exceed the offsets “has not shown that it learns more than scale use” is too categorical. Another test could establish content-associated predictability despite equal aggregate likelihood gains.

The defensible statement is:

> Likelihood gains alone do not establish content-dependent personalisation; evaluate content adaptation with rater offsets retained.

Likewise, capturing a gain with offsets supports an operational explanation in terms of text-independent calibration. It does not uniquely identify a psychological response-style mechanism.

**The MultiPref covariance interpretation conflates two comparators.**

In §6 and CLAIMS #10, distinguish:

- TRV versus isotropic: positive under the primary rater bootstrap;
- TRV versus population: improvement unestablished;
- TRV versus isotropic under two-way inference: inconclusive.

“Only because isotropic falls below μ” is too strong: isotropic’s interval includes zero. “TRV stays at μ” also suggests equivalence that has not been established.

Use:

> TRV outperforms isotropic under the primary rater bootstrap, without establishing improvement over the population model; the two-way contrast includes zero.

That preserves the frozen relative-advantage result without presenting it as beneficial adaptation over μ.

**The blanket developmental-status sentence in §6 is inaccurate.**

> “All CA analyses below were specified before their outcomes…”

That does not adequately describe the exploratory first-turn development and post-result amendments.

State separately that procedure development was exploratory, Stage-12/13 outcome rules were frozen, and the Stage-13 first-turn analysis reused previously examined data. Preserve the distinction that second- and third-turn outcomes were newly evaluated.

**The 55% sentence conflates pre-generated prompts with observed repeated identical items.**

The audit gives:

- 62,295 conversations using pre-generated prompts;
- 49,616 conversations belonging to the 2,928 observed shared identical items.

Do not use 55% as identical-item coverage without the corresponding denominator. The cheapest replacement is:

> CA contains 2,928 exact prompt–four-response items shown to at least two users, covering 49,616 first-turn conversations.

Also clarify that endpoint B’s **2,383 items** form the broader shared-item test panel, rather than the **1,116 items** contributing disagreeing pairs to endpoint A. “On all test events of these items” currently makes that relationship ambiguous.

**CLAIMS still needs these corrections:**

| Entry | Correction |
|---|---|
| #1 | “3-parameter scale-use model” does not describe every reported result. Distinguish unrestricted DF from symmetric DFs; the latter has three entries and two identifiable degrees of freedom. |
| #2 | Its blanket “frozen” status conflicts with the documented exploratory introduction of DFs. Separate the algebraic binary-cancellation property from the developmental status of the empirical result. |
| #4 | “Seeds × draws” does not describe the primary uncertainty analysis stated in §5.6. Specify rater-bootstrap intervals conditional on a synthetic panel, with separate multiple-draw sensitivity where performed. |
| #5 | Move the historical phrase “content personalisation detected” into the analysis-history/status field. The current claim should describe own − exchanged parameters and its limitations. |
| #10 | Apply the comparator correction above. |
| #12 | The substantive reading is correct. Replace “registered history filter” with “previously specified history filter,” consistent with your distinction between internal protocols and public registration. |

Two smaller but worthwhile fixes:

- Print the joint − position-only lower bound as **−0.0002**, rather than **−0.000**. Its proximity to zero matters.
- In the introduction, replace “positive controls bound what learners could detect” with the narrower injected-family wording above.

The abstract is otherwise substantially sound. Its main remaining omissions are the explicit unresolved content-versus-position distinction and the positive accuracy component of S13-3.

Outside the requested sections, two phrases also deserve correction: §7’s “training users alone” should remain “population-training procedure,” since prior estimation also differs; and §8’s claim that representations “do not encode” style is stronger than a near-zero cross-validated probe R² establishes.

**5) Ready for LaTeX? Yes, after a bounded claim-cleanup pass.**

I would require these before treating the prose as frozen:

1. Correct the offset generalisations, developmental-status language and covariance comparator interpretation.
2. Reconcile the shared-item coverage wording, endpoint populations and S13-3 eligibility flow.
3. Build one compact main-results table containing comparator, support-budget unit, primary/secondary uncertainty and developmental status.
4. Remove historical duplicate prose and decide what leaves the main body.

**No additional experimental stage is required for the appropriately scoped paper.** Another exploratory analysis is unlikely to resolve its central remaining limitations cheaply.

Begin typesetting after those corrections. The official ICML 2027 author-instructions page currently remains a placeholder, so use the 2026 template provisionally and update when the 2027 instructions appear. [ICML 2027 author instructions](https://icml.cc/Conferences/2027/AuthorInstructions), [ICML 2026 author instructions](https://icml.cc/Conferences/2026/AuthorInstructions)