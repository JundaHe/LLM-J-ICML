# Five Raters Are Not a Distribution: What Learned Judges Can Learn from Human Disagreement, and Where to Spend the Annotation Budget

*ICML main-text version v3 (in progress), compressed from PAPER_DRAFT_v2.md v2.5 following COMPRESSION_PLAN.md. PAPER_DRAFT_v2.md remains the full record. Numbers are copied verbatim from v2.5 and none are recomputed.*

## Abstract
Learned judges are increasingly trained on full histograms of human ratings. We ask which part of a few-rater histogram a text-conditioned judge can learn, separating whether the shape beyond its location (mode and mean) is *reproducible across raters* from whether it is *predictable from the text*.

On rating panels from 14 datasets, a learner-free split-half analysis finds the ordinal shape poorly reproducible. Its forecasting reliability is 0.04–0.41 with 4–8 raters and below 0.3 at 40, under the ½ needed for the raw histogram to beat its own mode and mean; on NLI it reaches 0.96–0.98.

Scored against the other half's own shape, no ordinal panel shows a robustly reproducible shape beyond location. On DICES-350, the one panel where it is detectable within the rater pool, frozen representations of three LLM families recover −1 to 1 % of it (upper bounds ≤ 12 %). A planted text-predictable shape of the same magnitude is recovered at 15–33 %. On MNLI and SNLI they recover 28–38 %.

Accordingly, replacing the shape of 69–83 % of training targets while preserving mode and mean changes LoRA judges by at most ±0.0015 RPS. One-hot targets are worse on 10 of 11 panels.

For the annotation budget, frozen-feature judges gain more from additional items than from additional raters on most panels. In a prospective LoRA block on POPQUORN, one rating per item costs 0.006 RPS against the full data, and a second rating recovers about half of that loss.

We release disagreement reliability cards and the estimators.

## 1. Introduction

Human raters disagree. A growing line of work therefore trains learned judges, meaning language models fine-tuned to score text, on the full distribution of human ratings rather than on a single aggregated label (Chen et al., 2025; Singh et al., 2025; Kohli, 2026; Benito-Santos & Ghajari, 2025). The appeal is that a histogram records which neighbouring levels received mass and how concentrated the ratings were. A judge that reproduces it would "capture human disagreement" rather than average it away.

The data behind that appeal are thin. In most datasets the histogram is computed from three to nine people. Five ratings of a code snippet's readability are a sample from a population of possible raters. A model trained to reproduce that sample exactly is therefore partly trained to reproduce sampling noise.

We ask a question that work on learning from label variation (Uma et al., 2021; Plank, 2022) has not asked in this form: **which part of a few-rater histogram can a text-conditioned judge learn?** We split every histogram into its *location*, meaning its mode and mean, and its *shape beyond location*, meaning the residual allocation of mass once mode and mean are fixed. We then measure two properties of the shape that are usually conflated.

1. **Reproducibility across raters (§3).** If a disjoint panel rated the same items, would the shape come out the same? We estimate this without a learner, using a split-half design. An exact identity, A1 = M − 2X, links three quantities:
   - A1, the value of the raw histogram for forecasting a new rater;
   - M, the magnitude of the histogram's residual relative to an exact mode-and-mean comparator;
   - X, the agreement of that residual across the two panels.

   The ratio ρ = X/M is a split-half reliability of the shape at a given number of raters. The raw histogram beats the comparator for predicting a new rater exactly when ρ > ½.
2. **Predictability from the text (§4).** Even a reproducible shape is useless to a judge unless the text carries it. We fit a cross-fitted ridge decoder from a frozen LLM's representation to the residual of panel 1. We score it against panel 2's residual measured from *its own* mode and mean, using a proper-score gain $G_{\rm own}$. We also report the gain as the fraction $G_{\rm own}/X_{\rm own}$ of the reproducible own-shape, with item-cluster CLT intervals. Each estimate is checked against a within-cell feature-permutation control and against planted positive controls.

**Findings.**

*(i) The shape beyond mode and mean is poorly reproducible on ordinal scales (§3).*
- With 4–8 raters per item, its split-half reliability is 0.04–0.41, and the intervals include 0 on four of eight panels. With three raters it cannot be measured at all, because a split leaves two ratings per item, which are fixed by their own mode and mean.
- On the dense ordinal panels it stays below 0.3 up to 40 raters, so on no ordinal panel does the raw histogram forecast a new rater better than its own mode and mean. On ChaosNLI, by contrast, the forecasting reliability exceeds ½ from two to three raters.
- The reproducibility of the shape itself at 40 raters is 0.06–0.22 on the dense ordinal panels and 0.61 / 0.67 on MNLI / SNLI.

*(ii) Little of the ordinal own-shape is decodable from the text, even where it exists (§4).* Across panels, the ordinal own-shape is:
- undetectable on SummEval's non-duplicated items, POPQUORN and DICES-990;
- on Dorn's readability panel, of the size that location and rater thresholds alone produce;
- detectable only on DICES-350, and only within its observed rater pool.

DICES-350 at 40 raters is therefore the clean ordinal case. There, frozen features of three model families recover −1 to 1 % of the own-shape (upper bounds ≤ 12 %). A planted text-predictable shape of the observed magnitude is detected in 5 of 5 draws and recovered at 15–33 %, and a location-and-threshold simulation of the panel yields no own-shape at all. On MNLI and SNLI the decoder recovers 28 % [24, 33] and 38 % [33, 42]. Every NLI lower bound exceeds every ordinal upper bound.

*(iii) The judges we trained show no detectable use of the shape (§5).*
- Replacing the shape of 69–83 % of LoRA training targets while preserving each target's exact mode and mean changes held-out RPS by −0.0001 [−0.0011, +0.0011] on SummEval and +0.0000 [−0.0009, +0.0009] on POPQUORN. This null is expected, since neither panel has a detectable own-shape.
- The discriminating case is ChaosNLI, where the same intervention costs 0.005–0.017 Brier.
- Across eleven ordinal panels, one-hot targets are worse on 10 of 11.
- Beyond item location, the remaining structure is mostly rater-side. Rater-specific cut-points improve held-out likelihood by 0.05–0.16 nats per rating, while item-specific dispersion adds −0.017 to +0.012.

*(iv) Budget (§6).*
- At a fixed number of ratings, frozen-feature heads improve with more items rather than more raters per item on four of the five ordinal panels with more than 900 items, and on both ChaosNLI panels.
- In a prospective LoRA block on POPQUORN with independent rating assignments, one rating per item is worse than the full data by +0.0063 [+0.0030, +0.0099] RPS, and a second rating recovers about half of that gap.
- On SummEval, the crowd ratings are nearly uncorrelated with the held-out experts, and half the items carry five identical crowd annotations. The same contrasts there measure how far expert ratings are diluted, and we report them in Appendix C rather than as budget evidence.
- A prediction we registered was falsified on ChaosNLI: that multi-rater items would pay off at a fixed budget wherever the shape is text-predictable. We therefore report the task-dependence of the marginal value of extra ratings as an observation, not as a consequence of the mechanism.

**Contributions.**
1. Two reliabilities for disagreement, across raters and across text, with learner-free and cross-fitted estimators and calibrated positive controls.
2. Disagreement reliability cards for every panel. They tell a dataset builder whether the shape of disagreement is reproducible at the number of raters they can afford.
3. A donor-replacement audit showing that current training does not use the shape, together with a rater–item decomposition of the ordinal structure beyond location.
4. Fixed-budget evidence for frozen-feature heads in three model families, and for end-to-end LoRA judges on POPQUORN.

**What we do not claim.**
- That disagreement is noise: part of it is reproducible.
- That the text contains no residual information: we test linear decodability from three frozen model families only.
- A theoretical rater-count threshold: a two-term 1/a model was falsified.
- A causal role for rater thresholds or label structure in the ordinal–nominal difference.
- A universal budget rule: Zhang, Gong & Choi (2021) find the opposite when a large single-label base already exists (§2).

## 2. Related work

**Learning from label variation.** Human label variation is increasingly treated as signal rather than noise (Aroyo & Welty 2015; Pavlick & Kwiatkowski 2019; Uma et al. 2021; Plank 2022). Soft-label training is reported to improve calibration and robustness (Peterson et al., 2019; Collins et al., 2022; Singh et al., 2025). Chen et al. (2025) train learned judges on human rating distributions. Kohli (2026) shows that on ChaosNLI the item-specific information in soft labels saturates around ten annotators. These studies compare training targets; none separates the part of the histogram that is reproducible across raters from the part that is predictable from the input.

**Predicting disagreement.** NLI label distributions are partly predictable from text (Zhou et al. 2022). Reward models detect diverging preferences with AUROC around 0.6 (Zhang et al., 2025), and demographic information helps predict who disagrees (Wan et al., 2023). We give the matching quantity for the shape beyond mode and mean, normalised by its reproducible part.

**Reliability and rater effects.** The reliability of aggregated annotations depends on the number of raters (Wong & Paritosh, 2022). Rater severity and scale use are classical facets in many-facet Rasch measurement (Linacre, 1989; Eckes, 2011). We apply the split-half logic and the rater facet to the shape beyond location.

**Annotation budgets.** Whether to label more items or relabel existing ones is an old question in crowdsourcing (Sheng et al., 2008; Lin et al., 2014). For hard-label classifiers, labelling many items once is preferable above a worker-quality threshold (Khetan et al., 2018). On ChaosNLI, Zhang et al. (2021) find the opposite: a few hundred ten-label items beat a few thousand single-label ones in KL. Their regime has a large single-label base and evaluates the full distribution. Ours is the complementary one: every rating competes for items, and judges are trained only on the budgeted data.

## 3. Reliability across raters

**Setting.** Item $i$ has ratings on $K$ ordered levels, with empirical histogram $h_i$. We score ordinal forecasts with the ranked probability score $S(f,y)=\sum_k (F_f(k)-\mathbf 1[y\le k])^2/(K-1)$ and write $C$ for the cumulative operator. For nominal tasks (ChaosNLI), $S$ is the Brier score and $C$ is the identity.

The *location* of a histogram is its exact mode and mean; for nominal tasks it is the modal class and modal mass. To isolate the *shape beyond location* we use the exact-T comparator $q_T$: a cross-fitted forecast built from other items in the same exact mode-and-mean cell. It is KL-projected onto the cell when the cell is sparse (Appendix A). By construction $q_T$ has the same location as $h_i$ and differs from it only in shape. The residual of a histogram is $r = C(h - q_T)$.

**Split-half identity.** In each repetition, every item's ratings are split at random into disjoint panels $P_1$ (size $a$) and $P_2$. Let $r_1 = C(h_1-q_T)$ and $r_2 = C(h_2-q_T)$, with $q_T$ computed from $P_1$. The value of the raw histogram over the comparator for forecasting a rating in $P_2$ then obeys the exact identity
$$A1 = \mathbb E\big[S(h_1,y)-S(q_T,y)\big]_{y\in P_2} = M - 2X,\qquad M=\|r_1\|^2/n,\quad X=\langle r_1,r_2\rangle/n .$$
Here $\langle u,v\rangle=\sum_k u_k v_k/(K-1)$. Hence $\rho = X/M$ is a *new-rater forecasting reliability*: the raw histogram beats the location-only forecast exactly when $\rho>\tfrac12$.

**Own versus cross reproducibility.** Because $r_2$ is measured against panel 1's comparator, $X$ is not purely agreement between the two panels' shapes. Writing $q_j$ for the comparator built from panel $j$, it splits as $X = X_{\rm own} + X_{\rm cross}$:
- $X_{\rm own}=\langle r_1, C(h_2-q_2)\rangle/n$ is the agreement of the two shapes, each measured beyond its own location;
- $X_{\rm cross}=\langle r_1, C(q_2-q_1)\rangle/n$ is panel 1's residual predicting the other panel's location shift.

The cross-term is not negligible. It is 32–40 % of $X$ on ChaosNLI at $a=20$, and most of $X$ on the ordinal dense panels at $a\le 8$. We therefore treat $\rho$ as a forecasting quantity and use $\rho_{\rm own}=X_{\rm own}/M$ for the reproducibility of the shape itself.

**Intervals and population.** Intervals are item-cluster bootstraps that refit the comparator in every replicate. Where raters recur across items, these intervals condition on the observed rater pool. For the three complete crossed panels we add crossed item × rater bootstraps. Where rating columns are anonymous positions, the intervals refer to new raters only if the positions are filled independently across items (Appendix A).

**Results.** Table 1 gives the resulting *reliability cards*, and Figure 1 traces $\rho$ against $a$ on the dense panels.

*Ordinal panels.*
- With 4–8 raters per item, ρ is 0.04–0.41 on eight panels, and the intervals include 0 on four.
- On SummEval's non-duplicated items it falls to 0.10 and 0.05, with intervals including 0 (Appendix C).
- With three raters, ρ cannot be measured. A split leaves two ratings per item, and two ratings are determined by their exact mode and mean under our tie rule, although 15–75 % of the three-rating histograms share their exact cell with a different histogram.
- On the dense ordinal panels ρ stays below 0.3 up to 40 raters: Buse–Weimer 0.22, DICES 0.25 and 0.15, and Dorn's Java panel 0.29.
- Under crossed item × rater bootstraps the ρ upper bounds stay below ½ (BW 0.39, DICES-350 0.36 at 40 raters, rounded outward).

*NLI.* On ChaosNLI, ρ exceeds ½ from two to three raters and reaches 0.96–0.98 at 40.

*The shape itself.* At 40 raters, ρ_own is 0.06–0.22 on the dense ordinal panels: BW 0.13, DICES-350 0.10, DICES-990 0.06, Dorn 0.12–0.22. With rater resampling the BW and DICES-350 intervals include 0, with upper bounds ≤ 0.26. On MNLI / SNLI, ρ_own is 0.61 / 0.67.

For new raters, then, we bound the ordinal shape-to-shape reproducibility from above rather than show it to be positive. The ordinal–NLI contrast holds on both measures.

## 4. Reliability across text

**Decoder.** A judge sees the text, not the raters. We ask whether the reproducible shape is available in the representation the judges are built on: last-token hidden states of frozen Qwen2.5-7B-Instruct (Qwen2.5-Coder for code panels) under the rating prompt. Qwen3-8B and OLMo-2-7B serve as second and third families.

A multi-output ridge decoder predicts $r_1$ from the features. It is group-cross-fitted over five item folds, with a label-free PCA and a nested penalty. We score it on panel 2's residual measured from its own exact cell, $s_2 = C(h_2-q_2)$, by the proper-score gain
$$G_{\rm own} = \big(2\langle\hat r,s_2\rangle-\|\hat r\|^2\big)/n .$$
This gain measures the shape alone. It excludes the part of the full gain that comes from predicting panel 2's location shift, and that excluded part is reported in Appendix B. The headline estimand is $G_{\rm own}/X_{\rm own}$, reported where $X_{\rm own}$'s interval excludes 0.

Intervals are item-cluster CLT intervals on per-item contributions, averaged over ten cross-fitting repetitions with the predictions held fixed. Ratios get delta-method intervals. As a check fixed in advance, the interval for $\langle\hat r,s_2\rangle/n$ covers 0 in 9 of 10 null draws (Appendix A).

**Controls.** Every estimate has three controls:
1. A *within-cell permutation* of the features among items with the same exact mode and mean. Under this control $G_{\rm own}$ must be at or below zero; its null expectation is $-E\|\hat r\|^2/n$, the decoder's variance penalty.
2. A *positive control* that predicts the panel-1 mean with the same pipeline.
3. A *planted shape* used to calibrate power. Item dispersion is made log-linear in a random feature direction, with γ setting the strength, and is simulated with the panel's fitted rater cut-points. We call the plant detected when the CLT lower bound of $G_{\rm own}$ exceeds 0. The reference strength is the smallest γ whose mean planted $X_{\rm own}$ reaches the observed one.

**Pool bias.** Within the observed rater pool, $X_{\rm own}$ is biased downward for new raters. This happens because each item's halves are drawn without replacement from one pool of raters with different cut-points, so the rater mixes of the two halves are anti-correlated. Simulations from the fitted rater–item model locate this bias (Appendix A). It makes "no detectable own-shape" easier to declare, and we read the nulls below accordingly.

**Results (Table 2).**

*Where an own-shape is detectable at all.* The ordinal own-shape is undetectable on SummEval's non-duplicated items, POPQUORN ($a=4$) and DICES-990 ($a=20$); on these panels $G_{\rm own}$ ≈ 0. Two ordinal panels have a detectable own-shape:
- On Dorn's readability panel the decoder recovers 10 % [4, 16]. However, a pure location-and-threshold simulation of Dorn's Java panel already yields a text-decodable own-shape: over five draws its $\langle\hat r, s_2\rangle$ averages about 95 % of the value observed on the real panel. A plant matching the observed magnitude is detected in only 1 of 5 draws. Dorn's 10 % is therefore an upper bound, of the size location alone produces.
- On DICES-350 the decoder recovers −8 % [−23, 8] at 20 raters per half and 1 % [−9, 12] at 40.

*NLI.* The decoder recovers 28 % [24, 33] on MNLI and 38 % [33, 42] on SNLI. With four raters per half, ChaosNLI still gives 22 % [18, 26] and 28 % [24, 32].

*The NLI–ordinal gap.* Every NLI lower bound exceeds every ordinal upper bound; the smallest margin is 24 % vs 16 %. The gap also holds net of the variance penalty, $(G_{\rm own}-G_{\rm own,perm})/X_{\rm own}$, at 20 raters per half: at most 30 % on the ordinal panels against at least 32 % on NLI.

*DICES-350 at 40 raters, the clean ordinal case.*
- A location-and-threshold simulation of the panel yields no own-shape at all: mean $X_{\rm own}$ is −1.3·10⁻⁵, against the observed 4.9·10⁻⁵. A reproducible ordinal shape beyond location therefore exists here within the observed rater pool.
- A planted text-predictable shape of matching magnitude is detected in 5 of 5 draws and recovered at 15–33 %.
- Against this, the observed recovery is −1 to 1 % across the three feature families, with upper bounds ≤ 12 %.

On DICES-350, then, the shape exists, the decoder has the power to find a shape of this size, and it is not decoded.

*Robustness.* Qwen3-8B and OLMo-2-7B give the same readings (MNLI 30 % and 29 %). A nonlinear random-feature decoder, the cross-term-inclusive ratio $G/X$, and a valid-forecast version projected onto the exact cell all agree (Appendix B). Scored as a valid forecast, the permutation-corrected gain is ≤ 6·10⁻⁵ RPS on the ordinal panels, against 0.0065 and 0.0072 on MNLI and SNLI.

**Why the two reliabilities can come apart.** $\rho$ asks whether the shape is a property of an item's rater population, and $G_{\rm own}$ asks whether it is a property of the item's text. A shape can be reproducible yet invisible to text, for instance when it arises from how particular raters use the scale. Section 5 shows that on the ordinal panels the structure beyond location is mostly rater-side.

## 5. What learned judges use

**Donor-replacement audit.** If a judge learned the shape beyond location, destroying that shape in its training targets would hurt it. The audit replaces the histogram of 69–83 % of training items by another item's histogram, projected onto the recipient's exact mode and mean. Among changed items the mean total-variation distance is 0.30–0.35. We run it under two learners (Appendix D gives the full design).

*LoRA judges.* These are end-to-end judges on Qwen2.5-7B-Instruct with the distributional objective of Chen et al. (2025), trained with three optimizer–assignment realisations × three held-out-rater folds.
- Shape replacement changes held-out RPS by −0.0001 [−0.0011, +0.0011] on SummEval coherence and +0.0000 [−0.0009, +0.0009] on POPQUORN offensiveness.
- Destroying the location as well (mode-only replacement) costs +0.0120 [+0.0086, +0.0155] and +0.0029 [+0.0009, +0.0050], with every seed-by-fold cell positive.
- On POPQUORN, resampling users instead of rating positions widens these intervals to [−0.0014, +0.0015] and [−0.0004, +0.0065].

*Frozen-feature heads.* On ten ordinal panels, heads move by −0.0024 to +0.0006.

**ChaosNLI, the discriminating case.** On SummEval's non-duplicated items and on POPQUORN no own-shape is detectable (§4), so a null there is the expected outcome rather than independent evidence. On the nominal ChaosNLI panels, the shape is both reproducible and decodable. There, the same kind of intervention scrambles the allocation of mass beyond the modal class while preserving the modal mass. It raises the test Brier score at every annotation count:
- by 0.005–0.012 on MNLI and 0.008–0.017 on SNLI (KL 0.016–0.052);
- equivalently, by 0.29–1.31 of the Brier gap between an oracle that uses the item's own training histogram and the exact comparator.

On binary αNLI, where the replacement cannot change any target, the same contrast is a sham and averages −0.003 to +0.002.

**Any target construction.** We also trained heads on eleven ordinal panels with each of the following target constructions, thirty configurations each:
- the raw histogram;
- the location-only comparator;
- reliability-shrunk shapes and locations;
- Dirichlet and label smoothing;
- a cross-item smoothed comparator;
- one-hot labels.

The results:
- The location-only comparator and the reliability-shrunk shapes change held-out RPS by at most 0.0012, with mixed signs.
- The other smoothing constructions move it by −0.005 to +0.009, in directions that differ across panels.
- One-hot targets are worse on 10 of 11 panels.

The learner pools location across items on its own and shows no sensitivity to the per-item shape. That is what §4 predicts for a shape that is not decodable from its features.

**Where the ordinal structure beyond location lives.** We fit ordered-probit models $Y^*_{ir} = \theta_i + \sigma_i\varepsilon_{ir}$ with cut-points $c_r$ to the panels with persistent rater identities:
- M0 has item location and common cut-points;
- M1 adds rater-specific cut-points;
- M2 adds item-specific dispersion.

Rater thresholds carry the structure. M1 improves held-out likelihood by 0.05–0.16 nats per rating, whereas item dispersion adds −0.017 to +0.012.

Simulating from the fitted models and re-running the split-half analysis at 40 + 20 raters gives a panel-dependent answer:
- On DICES-350, thresholds reproduce the observed $X_{\rm own}$ where location alone does not.
- On Buse–Weimer, location alone suffices.
- On Dorn's Java panel, only the dispersion model does.

At smaller splits, the location-only model reproduces most of the observed $X$ through $X_{\rm cross}$ (Appendix F). This is the textbook mechanism of many-facet Rasch measurement (Linacre, 1989; Eckes, 2011), which we present as measurement, not as a claim about raters' psychology. For a judge that sees only the text, structure that follows who rated is not learnable.

## 6. Annotation budget

We test the budget question directly, as an observation in its own right: hold the total number of ratings fixed and trade items for raters. We do not derive the answer from §§3–5. A registered mechanism-based prediction failed on ChaosNLI (§1).

**Frozen-feature heads** (eight ordinal and two nominal panels, thirty configurations each; Appendix F). On four of the five panels with more than 900 training items, more items with fewer ratings each wins monotonically. On DICES-990 at a budget of 594 ratings, for example, RPS rises steadily as ratings are concentrated on fewer items:

| items × ratings | 594 × 1 | 297 × 2 | 148 × 4 | 74 × 8 | 40 × 15 |
|---|---|---|---|---|---|
| RPS | 0.203 | 0.205 | 0.207 | 0.213 | 0.219 |

SummEval is flat. The direction reverses only on small item sets (60 and 210 training items), where a single rating per item is too noisy a target. The items-first order also holds on ChaosNLI (959 × 1: KL 0.226; 30 × 32: 0.323). What differs between tasks is the *marginal* value of a second rating on items already covered: −15 % on ChaosNLI against −1 to −3 % for the ordinal heads.

**LoRA judges on POPQUORN** (Table 3). POPQUORN offensiveness has homogeneous rating positions, which makes it the clean budget case. Every arm trains for the same number of optimizer steps, and all contrasts are taken within one batch, because LoRA training on our hardware is not bit-reproducible: per-cell RPS varies by ≤ 0.0012 between identical runs. A prospective block with independent rating assignments (ROUND20 R20-4) gives:
- 819 × 1 − full = +0.0063 [+0.0030, +0.0099]: one rating per item is worse than the full data.
- 819 × 2 − 819 × 1 = −0.0031 [−0.0062, −0.0002]: a second rating recovers 49 % of that gap.
- 117 × 7 − 819 × 1 = +0.0027 [−0.0024, +0.0074]: items-first is not supported.

An earlier same-batch block reproduces all three readings, with 819 × 1 − full = +0.0087 [+0.0054, +0.0122] and 62 % recovered by a second rating.

**SummEval measures dilution, not budget.** Each SummEval item carries three expert ratings and five crowd ratings, and the evaluator is always a held-out expert. Because the crowd mean is nearly uncorrelated with the expert mean (r = 0.04), a judge trained on the crowd ratings alone is +0.014 to +0.025 RPS worse than the full-data judge on every fold. There, "fewer ratings per item" changes how far two expert ratings are diluted by five crowd ratings. We report those blocks, including their Qwen2.5 and OLMo-2 replications, in Appendix C.

**Guidance, conditional on task and learner.**
- For ordinal rating tasks with more than 900 items, frozen-feature heads favour covering items first; on ≤ 210 training items the direction reverses.
- With LoRA judges, prefer two ratings per item over one.
- Where the rater pool mixes populations, who rates matters more than how many ratings are collected.
- Many raters per item belong where a reliable reference distribution is itself the deliverable: evaluation sets, and tasks such as NLI where the shape is in the text.

## 7. Limitations and conclusion

**Limitations.**
- *Learners and decoders.* Decoding and the frozen-feature analyses use three model families. The end-to-end budget result replicates with an OLMo-2-7B LoRA judge, but the LoRA audit uses Qwen2.5 only. We test linear decoders and one non-linear probe, not fine-tuned probes, so "not decoded" means not decoded by these.
- *Plant scope.* The plant is one construction: item log-dispersion linear in one feature direction. A detected plant therefore calibrates power for that construction only. At $a=20$ (Dorn) the matched plant is detected in 1 of 5 draws, at $a=40$ (DICES-350) in 5 of 5, and there are no plants on NLI.
- *Exact cells and the rater pool.* At 20 raters the exact (mode, mean) cell pools items of different latent location, so a decodable own-shape can be location-driven. The ordinal fractions are therefore upper bounds on shape beyond location, and the NLI values may contain such a component. The pool bias of §4 makes "no detectable own-shape" slightly easier to declare.
- *SummEval data.* The released file has identical crowd annotations on 807 of 1,600 items. This is undocumented and unverified upstream. It makes SummEval's full-panel numbers artefactual and its budget contrasts dilution contrasts (Appendix C).
- *POPQUORN position folds.* A user-held-out check with real user ids, in which no evaluator contributes to any target, confirms the audit and budget conclusions.
- *Effect sizes.* The effects lie in the third decimal of RPS. They should be read against the mode-only penalty of +0.012 and the POPQUORN budget effects of 0.006–0.009.

**Conclusion.** A few-rater histogram is a noisy location plus a shape that, on ordinal scales, is barely reproducible across raters and, where it is reproducible, is not in the text. On DICES-350 we can show both halves directly. The shape exists within the rater pool, a planted shape of its size is decoded, and the real one is not.

On NLI the shape is reproducible and a quarter to two-fifths of it is decodable. Learned judges follow the same split, and spending the budget on items rather than raters is the right default where the shape is not in the text. Reliability cards make that check possible before rating starts.
