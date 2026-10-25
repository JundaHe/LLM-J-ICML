# Verdict

**Net stronger, but still not yet ACL/EMNLP-main ready.** ChaosNLI turns the ordinal null into a credible boundary rather than a failed universal claim, and it acts as a natural positive control for the intervention. However, the proposed claim and title remain too broad. Today I would call this a **strong Findings paper / borderline-to-weak-reject main paper**.

The principal remaining rejection risk is:

> The paper turns heterogeneous, partly exploratory results into the universal conclusion that “location suffices,” although SORD is metric- and task-dependent, the LoRA target ordering changes under calibration, and the central residual-shape null lacks optimizer/permutation replication and equivalence inference.

The second risk is the dependence structure: most intervals remain conditional on one optimizer seed, one split, and one permutation mapping.

## 1. ChaosNLI: stronger or weaker?

**Stronger as an attribution paper; weaker only if you insist on the current universal headline.**

ChaosNLI does three valuable things:

- It shows the intervention can detect naturally occurring item-linked information, not merely injected PCA-1 signal.
- It rules out the facile explanation that every null is caused by low-capacity heads.
- At \(m=5\), it shows that annotation count alone does not explain the ordinal result.

But do not claim that you have isolated “ordinality” causally. Ordinal versus nominal is confounded with task, domain, representation and label semantics. The conclusion should be “consistent with a structural distinction,” not “proves that ordinal shape is noise.”

The working title is now misleading. “Location, Not Shape” is false without qualification. Better:

> **Location for Ordinal Ratings, Allocation for Nominal Labels: What Distributional Judge Training Uses**

or:

> **Auditing What Distributional Judges Learn from Human Rating Histograms**

A defensible abstract core is:

> Distributional supervision is often interpreted as teaching models which items elicit human disagreement, but its gains may arise from lower-dimensional statistics of the annotation histogram. We introduce nested link interventions that separately disrupt associations with ordinal location and residual distributional shape, evaluating predictions against held-out annotations. Across tested small-panel ordinal rating tasks, breaking the item–mean association degrades performance, whereas mean-preserving shape permutations cause no detectable average degradation; mean-centred parametric targets are often competitive with empirical histograms, although the preferred target depends on metric and adaptation regime. In contrast, on ChaosNLI, preserving the modal class and its mass while permuting allocation among nonmodal classes increases KL by 0.011–0.020 with 5–50 annotations, and empirical histograms outperform two-statistic targets by 0.010–0.017. These findings identify location-dominated learning in the tested ordinal regimes and item-linked residual allocation in nominal classification.

The phrases “no detectable average degradation” and “tested regimes” are necessary until you have equivalence tests and replicated LoRA permutations.

## 2. Does SORD-at-the-mean constitute a contribution?

**Not as a new target method. Yes as a diagnostic control supporting a new empirical attribution result.**

Your `sordm` is directly within Díaz and Marathe’s construction:

\[
q_k \propto \exp[-\phi(\mu,k)],
\qquad
\phi(\mu,k)=\frac{(k-\mu)^2}{2\sigma^2}.
\]

SORD already permits task-defined distances and soft ordinal vectors; substituting a fractional multi-rater mean for a hard rank is an obvious application, not a substantial algorithmic invention. See the original [Díaz & Marathe CVPR paper](https://openaccess.thecvf.com/content_CVPR_2019/papers/Diaz_Soft_Labels_for_Ordinal_Regression_CVPR_2019_paper.pdf).

What is new is:

> Using a fixed-shape SORD target centred on a multi-rater location estimate as an information-restricted control, together with nested link randomizations, to determine whether empirical item-specific residual histogram shape contributes predictive information.

That is an attribution contribution, not “we invented SORD-mean.”

Do not currently say “SORD-at-the-mean is the right target”:

- On What, `sordm` is best on RPS, but `sordz` is slightly better on KL: −0.042 versus −0.039 relative to soft.
- `sordm` is already worse in the partial Why result.
- Mean2 loses on RPS but wins on KL.
- Therefore there is no metric-independent or panel-independent “right target.”

There is also a technical naming issue. Your discrete Gaussian is **parameter-centred** at \(\mu\), but its actual expectation is not constrained to \(\mu\), particularly near scale boundaries. In the What configurations, I calculate an average absolute target-mean drift of about 0.075 score points. Rename it “SORD with location parameter \(\mu\),” or solve for the Gaussian location parameter that makes \(E_q[Y]=\mu\).

The licensed contribution is:

> On commit What with frozen-feature heads, a one-item-statistic target—empirical mean plus a globally tuned width—outperforms the noisy histogram on RPS, while nested permutations attribute the useful item link to location rather than residual shape.

It becomes “SORD works” if you lead with target performance. It remains novel if SORD is explicitly presented as the strongest restricted-information control in the attribution audit.

## 3. LoRA What versus heads What

**Run `sordm`, but first acknowledge that the apparent disagreement is presently caused partly by calibration and objective mismatch.**

The most important protocol finding is this:

| What, Qwen LoRA | Chen | mean2 | proto |
|---|---:|---:|---:|
| Raw RPS | 0.10151 | **0.10105** | 0.10132 |
| Post-calibration RPS | **0.09972** | 0.10042 | 0.10062 |

Thus mean2 beats Chen before calibration by about 0.00046, but Chen beats mean2 after calibration by about 0.00070. Proto also changes from slightly better than Chen raw to worse after calibration.

The “heads versus LoRA” disagreement therefore does **not** currently establish a LoRA-specific target-shape regularization effect. It is at least partly a raw-versus-calibrated estimand difference. The analyzer independently tunes temperature and climatology shrinkage for each arm in [analysis_lora_v3.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_lora_v3.py:10).

Other mismatches are substantial:

- Heads use direct cross-entropy against each target. LoRA’s Chen, mean2, proto and permutation arms all receive adversarial perturbation plus a 20% hard-label term in [train_judge_v3.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/train_judge_v3.py:135).
- Heads use 4 training and 2 reference raters on commit; LoRA uses 5 training and 1 evaluator per fold.
- LoRA mean2 prototypes are not leave-one-item-out; revised heads prototypes are.
- Heads have validation-based early stopping; LoRA uses fixed training length and subsequent calibration.
- The frozen-head and LoRA representations/capacities differ.

Recommended adjudication:

1. Report both raw and calibrated LoRA results, with one declared primary estimand. Calibrated performance is valid for the deployed pipeline, but it cannot support the story that Chen’s histogram target intrinsically trained a better model when the raw ordering is opposite.
2. Run `sordm` under exactly the same Chen-style wrapper as the other constructed LoRA targets.
3. If affordable, also run a direct SORD arm with \(\alpha=1\), no adversarial perturbation and no hard term. Otherwise it is not a clean reproduction of the heads/Díaz objective.
4. Cross-fit the LoRA prototype before interpreting sub-0.001 differences.
5. Cheaply rerun the heads under the LoRA 5/1 rater protocol and apply the same calibration. This will distinguish architecture from evaluation-pipeline effects.

## 4. Correct pooled analysis for chain7

Use the balanced **3 optimizer seeds × 3 evaluator folds** block as the primary analysis. Do not count the nine cells as nine independent observations, and do not combine folds 3–5—which only have seed 2000—into the primary balanced estimate.

For each contrast, first compute paired test-item or source-document loss differences within every seed–fold cell. Estimate:

\[
\hat\Delta=
\frac{1}{3}\sum_s
\frac{1}{3}\sum_f
\frac{1}{G}\sum_g d_{sfg}.
\]

Then:

- Treat evaluator folds as fixed if the claim concerns these observed raters. Three folds are too few for credible rater-population inference.
- Propagate both test-group and optimizer-seed uncertainty, for example with a crossed product bootstrap over seeds and item/document clusters. With only three seeds, also show all three seed-specific estimates.
- If you model folds as random, use a crossed hierarchical model with item/document, optimizer seed and evaluator effects, but be explicit that three levels give weak variance estimation.
- Refit calibration within resampled calibration groups, or report calibration uncertainty as omitted.
- Analyze What and Why separately. Do not manufacture a single pooled task effect.
- Freeze the metric, contrasts, SORD width and equivalence margin before opening chain7 outputs.

The current analyzer keys results only by fold and averages folds before its item bootstrap; it does not account for seed variation in [analysis_lora_v3.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_lora_v3.py:21). It needs a seed dimension.

If preregistered now, chain7 can confirm—**conditional on Qwen, split 0 and the fixed evaluator set**:

- `perm_mode − chen > 0` on Why: item-specific ordinal location matters.
- `hard − chen > 0`: the Chen-style distributional pipeline improves RPS.
- Chen versus mean2 and Chen versus SORDm target comparisons under optimizer replication.

It cannot confirm:

- **Residual shape is inert.** Chain7 omits `perm`, the mean-preserving intervention.
- Equivalence of `perm` and Chen.
- Robustness to permutation mapping: `perm_seed` remains fixed at 1000 when only `opt_seed` changes.
- Item-split, model-family or rater-population generalization.
- “SORDm is the right ordinal target.”

The central headline is about residual shape, so omitting `perm` from the replication set is a design error. Add it, or replace a secondary arm with it. For a null claim, specify a smallest effect of interest and test \(|\Delta_{\text{link}}|<\epsilon\); a CI containing zero is not enough.

## 5. GPU priority

Ranked by expected acceptance gain per GPU-day:

1. **(i) Finish SummEval folds 1–2.** A one-expert result is not publishable as the main external LoRA result, and the jobs are already running.
2. **(v) SORDm LoRA on SummEval.** It is cheap relative to a new sweep and directly tests the proposed constructive conclusion on the strongest external panel.
3. **(ii) Seed replication, redesigned.** Include `perm`; keep optimizer and permutation seeds separate. If necessary, prioritize Chen/perm/perm_mode/SORDm rather than replicating every secondary baseline.
4. **(iii) Focused DeepSeek-family replication.** Use only the central contrasts on Why and/or SummEval. This is more valuable than another full Qwen panel once optimizer stability is known.
5. **(iv) ChaosNLI LoRA.** Scientifically attractive and would align the ordinal/nominal halves under one adaptation regime, but the frozen-head result already establishes the boundary directionally.
6. **(vi) HelpSteer2 LoRA.** It adds another sparse ordinal panel without resolving calibration, seed uncertainty, target choice or model-family generalization.

If there is time for only the first three, stop there.

## 6. Problems in `RESULTS_TABLES.md`

The arithmetic is mostly correct. The presentation and inferential labels need several fixes.

1. **“± = SEM over configs” is not adequate inference.**

   The 30 head configurations reuse five seeds, three item splits and two rater splits; the nine Chaos configurations reuse three splits and three annotation/optimizer seeds. Replace the header with:

   > “± denotes descriptive SEM over pipeline configurations; confirmatory intervals use paired crossed/hierarchical inference over optimizer seeds, item groups and evaluator folds.”

2. **T1’s rater column silently describes heads but not LoRA.**

   > “commit … 6 (4 / 2)”  
   > “SummEval … 8 (6 / 2)”

   Fix the header to “heads train/reference ratings,” with a footnote that LoRA LORO uses 5/1 for commit and 7/1 for SummEval.

3. **The ChaosNLI entry is in the wrong column.**

   Its residual Spearman values appear under “oracle D advantage of histogram over mean2,” which is an ordinal quantity. Put `—` there and add a separate nominal residual-recovery column or footnote.

4. **T2 is a legacy exploratory table.**

   Its prototypes are not cross-fitted and some dense-panel `pmm` interventions preserve only a mean bin. Label it accordingly; do not use T2 as exact-mean or confirmatory evidence.

5. **“sordm (Gaussian at mean)” is technically imprecise.**

   Replace with:

   > “SORD Gaussian with location parameter set to empirical mean; globally tuned \(\sigma\)”

   The target’s actual expectation is not exactly the empirical mean near boundaries.

6. **The claim that `pmmx` settles the binning issue on commit What is overstated.**

   With four training ratings, possible means are spaced by 0.25, while the permutation bin is 0.1. Consequently `pmm` already matches only equal means on this panel; `pmmx` is essentially the same target plus numerical smoothing. The two independently trained arms are not an additional exact-mean experiment. Run `pmmx` on BW/DICES, where the original concern actually exists.

7. **T3 must identify calibration as outcome-changing.**

   Add “arm-specific post-calibration RPS” to the title and report raw sensitivity. On What the raw order has mean2 and proto ahead of Chen, while calibration reverses that conclusion. Without this, “Chen better” is easily misread as a training-target result.

8. **T3/T3b confidence intervals are conditional.**

   T3 uses one optimizer seed; T3b uses one evaluator fold and one optimizer seed. Label them “test-item/document bootstrap CIs conditional on trained models,” not general uncertainty intervals. Replace “inert” with “not detectably different in this conditional analysis.”

9. **T5’s \(m\)-trend does not use a fixed reference panel.**

   The code uses `P_ref = pos[m:m+50]`, so the 50-reference panel changes as \(m\) changes in [probe_nominal.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/probe_nominal.py:64). Use a common split such as training positions `pos[:m]` and reference positions `pos[50:100]` for every \(m\). Also separate annotation-subsample seed from optimizer seed. Until then, “the margin grows with \(m\)” is descriptive, not a tested dose response.

10. **T6’s final comparison is ambiguous and “oracle” is misleading.**

   > “interactive − additive +0.0017±0.0012”

   That is approximately the \(k=64\) contrast. The population-RPS contrast is only about \(+0.00054\pm0.00094\). Label the metric explicitly. Rename “seen-ID oracle” to “seen-rater ID ceiling”; it is a learned model evaluated on the training-rater population, unlike the unseen-rater methods, so its 0.197 is not directly comparable.

Finally, the central claim should be weakened from “dispersion beyond the mean is unused” to:

> **In the tested ordinal regimes, we find no detectable average benefit from linking an item to residual histogram shape beyond its location; in nominal NLI, the corresponding residual class allocation is detectably item-linked and useful.**

That claim survives all the current results.