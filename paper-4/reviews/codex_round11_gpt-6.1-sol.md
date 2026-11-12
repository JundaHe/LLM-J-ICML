Stage 14 strengthens the descriptive scale-use result, but does not establish an absence of content taste. The main problems are inconsistent model-version labelling, overstatement of null results, and insufficient main-text disclosure of the post hoc choices. Page numbers below are the printed pages.

**1. Numerical audit**

The corrected \(k=20\) likelihood entries are consistent with C2:

- MultiPref DL − D: **0.1002 [0.0764, 0.1276]**, matching Tables 1 and 3.
- MultiPref DFs − DL: **−0.0005 [−0.0052, 0.0049]**, matching Table 1 and Appendix B.
- DICES DF − DL: **0.0111 [0.0047, 0.0181]**, matching Table 2.
- PRISM DF − DL: **−0.0037 [−0.0065, −0.0008]**, matching Table 2’s rounding.
- The Jester estimates, recovery percentages, contested-pair results, and corrected ordinal column of Table 4 match B/C.

The offset rows using the training-rater prior need not equal C2’s few-shot-tuned offset rows; that difference is disclosed.

**Table 4 retains original DL values without clearly identifying that column as uncorrected.** These are valid historical numbers, but inconsistent with the corrected DL identity used elsewhere:

| Location and quoted DL entry | Correct rung-a DL entry |
|---|---|
| p. 6, Table 4, null: “−0.10 [−0.38, +0.17]” | **+0.01 [−0.25, +0.27]** |
| p. 6, injected +5.2: “−0.02 [−0.28, +0.26]” | **−0.06 [−0.29, +0.19]** |
| p. 6, injected +10.1: “+0.09 [−0.18, +0.36]” | **+0.62 [+0.17, +1.06]** |
| p. 6, real MultiPref: “+0.30 [−0.00, +0.60]” | **+0.19 [−0.11, +0.50]** |

Either replace these cells or label the column **“original DL, unwhitened prior”** and add corrected DL alongside it. The +1.7 and +21.1 rows were not rerun and must remain explicitly historical. The unqualified original “+0.30” in §5.6, p. 5, and its repetitions on pp. 16–17 need the same treatment.

Two archived confidence intervals also differ from C2’s recomputation:

| Location and quotation | Value from C2 |
|---|---|
| p. 13, Appendix A: first-run DL − D “+0.095 [+0.069, +0.122]” | **+0.0952 [+0.0688, +0.1234]**, or **+0.095 [+0.069, +0.123]** |
| p. 13, Appendix A: first-run DFs − DL “+0.0045 [−0.0004, +0.0092]” | **+0.0045 [approximately 0, +0.0096]** |

Different bootstrap realizations could explain these discrepancies. If these are deliberately preserved archival intervals, say so and identify the recomputation; do not imply exact numerical reproduction.

Further corrections or clarifications:

- **p. 13:** “selected strengths are interior (0.03–2)” is false as a general statement. Rung-a DL selects the **0.03125 lower grid boundary** on DICES and Dorn; PRISM at \(k=50\) selects the **128 upper boundary** in three folds.
- **p. 16:** “preferences worth up to about 10 points cannot be seen by them from 20 ratings” needs an explicit **original-configuration** qualifier. Corrected L detects the +10.1 panel under both rungs; corrected DL does so under rung b.
- **p. 8, limitations:** “The positive control covers MultiPref only” is now inaccurate. The **injection controls** cover MultiPref; the **real-data control** covers Jester, with successful corrected recovery demonstrated on seen jokes.
- **p. 15:** “+0.012 [+0.003, +0.020] nats over the offsets” on Dorn is correct **against DF**: C2 gives +0.0115 [0.0029, 0.0204]. Against L’s designated comparator **F**, the value is **+0.0374 [0.0273, 0.0462]**. Name DF explicitly.
- **Ledger #13:** the first-turn contested-accuracy two-way interval is **[+0.08, +3.14]**, which excludes zero. Both CA two-way **contested-minus-rest accuracy** intervals reach zero; those are different contrasts.

The supplied B/C summaries do not independently establish Table 1’s corrected \(k=5/50\) rows, Table 3’s absolute DL accuracy **0.677**, or Figure 2’s plotted coordinates. Those remain unverified from this packet.

**2. Inferential strength**

**(a) “Detects +10 but not +5”: supported only with precise qualification.** On one synthetic draw, at \(k=20\), using the stipulated own-minus-other criterion:

| Model | Rung a | Rung b |
|---|---|---|
| Softmax DL | **Does not pass** at +10: lower bound +0.17 | Passes: lower bound +1.48 |
| Ordinal L | Passes: lower bound +2.02 | Passes: lower bound +2.51 |

None passes at +5.2. Ledger #15’s wording risks implying that rung-a DL’s **+0.62** passes; it does not.

A suitable statement is: **“In the tested injection family and draw, corrected ordinal L passes the detection criterion at +10.1 but not +5.2 points.”** Calling this a general “detection limit between +5 and +10” (p. 15) is too strong: one realization at two strengths does not estimate statistical power or establish a general threshold.

Also bring the no-adaptation comparison into §5.6: ordinal L’s **+0.84 [−0.12, +1.80]** does not establish net ranking benefit. Own-minus-other demonstrates user-associated information here; it is a different estimand from the oracle’s gain over population weights.

**(b) “No content taste beyond offsets on MultiPref”: too strong.** “Stays at zero” (§5.6, p. 5) should become **“shows no established additional direction gain.”** The small own-minus-other upper bounds constrain these fitted learners, conditional on the protocol; they do not bound all content preferences in the population.

Moreover, rung-a DL is **inconclusive under the written likelihood rule**: its upper bound is 0.0052 nats against the 0.005 margin. Rung-b L is also inconclusive. The manuscript should retain those outcomes rather than replace them with a universal “nothing beyond scale use.”

Relatedly, §5.1’s “gains as much” (p. 3) and Figure 2’s “ties” (p. 4) overstate the comparison. Table 1 does not establish 0.005-nat non-inferiority at \(k=5\) or \(20\). Say **“similar point estimates.”**

**(c) PRISM: the numerical statement and likelihood contradiction are supported.** The extra **0.0037 [0.0008, 0.0065] nats** is approximately **4.7%** of the tuned offsets’ gain. Under the written rule, it contradicts the literal claim of no additional likelihood improvement. It does not contradict **“mostly scale use.”**

“No ranking gain” should mean **no demonstrated ranking advantage**: own-minus-other concordance is −0.06 [−0.26, +0.13], and the contrast against offsets is −0.01 [−0.10, +0.08]. Against its own \(k=0\), concordance actually decreases by **−0.21 [−0.37, −0.05]**.

The likelihood evidence is nominal and exploratory; family-adjusted significance is unknown. Also, the rule’s “stands” margin and “contradicted” exact-zero test are not complementary hypotheses and should be distinguished.

**(d) Adopting rung a is defensible for the original likelihood objective, but remains a post hoc choice.** It preserves the selection target and avoids rung b’s substantial likelihood losses. However, it fixes only one of the two diagnosed problems: **rung-a DL recovers 29% of CF on Jester and fails the +10 detection criterion.** Ordinal L’s success cannot validate softmax DL automatically.

Describe rung a as the adopted exploratory correction, with rung b as a fully reported sensitivity analysis—not as a uniquely validated repair. Rung b’s failure does not prove that concordance selection generally fails, or that small selection cells caused its failure.

**(e) The direction clause is inappropriate for identifying content taste on single-response panels, although mathematically well-defined.** Midpoint classification is a legitimate endpoint; it is simply changed by scale shifts. Revising its interpretation is reasonable, provided the original labels remain visible and the replacement interpretation is explicitly exploratory.

Two qualifications matter:

- On p. 15, “concordance gain of exactly zero, i.e. it is used as a rater shift” is not established by concordance alone. Unchanged finite-sample ordering does not prove that the text-interacting term is constant. Show the coefficients or an ablation.
- “The one positive cell” must specify **under rung a**. Rung b also has nominal positive own-minus-other concordance for DICES L and both PRISM latents. None establishes improvement over no adaptation.

**3. Disclosure and forking paths**

Appendices A/B/E provide a useful chronology, including the original failed rule. The main text is not adequate at its present claim strength: “corrected prior, post hoc” does not communicate the original control failure, the remaining weakness of rung-a DL, or the outcome-informed adoption of rung a.

I would require:

- A compact main-text comparison showing **CF 1.39; original DL 0.14; rung-a DL 0.40; rung-b DL 1.16; ordinal L 1.68/1.67**, with uncertainty. State that **no DL rung passed the original Jester rule**.
- Corrected synthetic results labelled by **model × rung**, alongside real MultiPref results, including **own-minus-other, own-minus-\(k=0\), and likelihood versus the matched scale-use comparator**.
- Side-by-side rung-a/b likelihood and ranking results. For example, PRISM DL changes from **+0.0037** to **−0.0307 nats versus DF**. State that all eight rung-b likelihood point estimates are negative; seven intervals exclude zero.
- An abstract sentence acknowledging the **post hoc latent correction and limited injection recovery**. The limitations must mention the original pipeline failure, adaptive rung/interpretation choices, single corrected synthetic draw, and absence of demonstrated corrected transfer to unseen Jester jokes.

The p. 3 statement that two-way bootstrapping changes no likelihood conclusion must also be restricted to the original analyses unless repeated for the corrected fits. Earlier bootstrap checks cannot automatically validate replacement rows.

**4. Three additional analyses, in priority order**

1. **Recalibrate the corrected detectors across existing synthetic draws and injection families.** Repeat the corrected null/+5/+10 and semantic-axis panels with the existing seeds, reporting detection frequency and both own-minus-other and own-minus-\(k=0\). This most directly tests whether the new sensitivity claim generalizes.
2. **Separate scale use from the latent interaction explicitly.** Retain the same rater offsets in both models and compare offsets alone with offsets plus content interaction; ablate the latent’s item-independent component. This would clarify PRISM’s likelihood gain and test the Dorn “rater shift” explanation.
3. **Recompute uncertainty for the corrected real-panel contrasts.** Use appropriate item/conversation × rater resampling and a declared multiplicity family, reporting nominal and adjusted results with rung choices frozen. This particularly affects PRISM’s small likelihood advantage and the DICES concordance lead.

**5. Framing**

Stage 14 strengthens confidence that offsets capture most demonstrated graded-rating gains, but weakens the broader inference that small latent gains reveal little content taste in these domains. The original negative control exposed a methodological failure; the repair provides useful, narrowly calibrated sensitivity evidence, rather than a general absence test. PRISM’s additional likelihood gain is small enough to preserve “mostly,” while ruling out an unqualified “nothing beyond scale use.” Frame the paper around what these implementations predict from short histories, the strong performance of scale-use baselines, and the need to distinguish likelihood, user association, and net ranking benefit. Content preferences outside the validated injection family remain unresolved.