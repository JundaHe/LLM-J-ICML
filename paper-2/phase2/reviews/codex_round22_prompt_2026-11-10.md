You are an adversarial ICML 2027 reviewer. Below are (A) the full current submission draft (PAPER_ICML_v3.md: the 8-page ICML restructuring of PAPER_DRAFT_v2.md, main text §1–§7 plus appendices A–F) of a paper on what part of human rating histograms text-conditioned judges can learn, and (B) the protocol-and-results logs for the revisions made since your last review (ROUND21_PROTOCOL.md and ROUND22_PROTOCOL.md). Each analysis was specified before it was run; amendments made after seeing results are labelled as such.
Your previous review (round 20, verdict weak reject) said: the central interpretation of decoding as recovering a "fraction of the reproducible shape" was unresolved (G/X inherited the cross-term); the projected "bounds" were not confidence bounds; the planted experiment was not a general power calibration; R19-9's pending outcome could not support equivalence language. Rounds 21 and 22 were reviewed only by an independent Claude adversarial reviewer, because Codex was unavailable; those reviews' issues were addressed in ROUND21/22.
Since then: own-shape estimand G_own/X_own with item-cluster CLT intervals (R21-1); plant calibration with a frozen detection rule over five draws (R22-3/R22-4); a second plant construction (polarisation, R22-6) that is detected in only 3/5 draws at matched X_own, so the DICES-350 power claim is restricted to the dispersion construction; the budget question carried by the prospective POPQUORN LoRA block (R20-4); SummEval budget blocks reframed as expert dilution. A machine audit of all percentages (2026-11-07) corrected three numbers; notably the smallest NLI–ordinal margin is 18 % vs 16 % (ChaosNLI MNLI at 4 raters per half vs Dorn), not 24 % vs 16 %.

Please: (1) give the status of each of your round-20 issues (resolved / partly / not); (2) check whether the frozen readings were respected and whether all post-hoc amendments are disclosed adequately and not used to rescue claims; (3) specifically assess (a) how much the power calibration covering only the dispersion construction weakens the DICES-350 null and the paper's headline, (b) whether "every NLI lower bound exceeds every ordinal upper bound" (margin 18 % vs 16 %, intervals at different rater counts) should be kept, reworded, or dropped, (c) whether the 8-page main text makes the DICES-350 vs NLI contrast and the POPQUORN budget result clear without the appendix; (4) list new issues ranked by severity (CRITICAL/HIGH/MEDIUM/LOW), each with the concrete text or analysis change that would fix it; (5) the three most valuable remaining changes; (6) a verdict (accept / weak accept / borderline / weak reject / reject) with the main reason, and what would move it up one level. Be specific and quote the draft where it is wrong.

=============== (A) PAPER_ICML_v3.md ===============
# Five Raters Are Not a Distribution: What Learned Judges Can Learn from Human Disagreement, and Where to Spend the Annotation Budget

*ICML main-text version v3 (in progress), compressed from PAPER_DRAFT_v2.md v2.5 following COMPRESSION_PLAN.md. PAPER_DRAFT_v2.md remains the full record. Numbers are copied verbatim from v2.5 and none are recomputed.*

## Abstract
Learned judges are increasingly trained on full histograms of human ratings. We ask which part of a few-rater histogram a text-conditioned judge can learn, separating whether the shape beyond its location (mode and mean) is *reproducible across raters* from whether it is *predictable from the text*.

On rating panels from 14 datasets, a learner-free split-half analysis finds the ordinal shape poorly reproducible. Its forecasting reliability is 0.04–0.41 with 4–8 raters and below 0.3 at 40, under the ½ needed for the raw histogram to beat its own mode and mean; on NLI it reaches 0.96–0.98.

Scored against the other half's own shape, no ordinal panel shows a robustly reproducible shape beyond location. On DICES-350, the only panel where one is detectable within the rater pool, frozen representations of three LLM families recover −1 to 1 % of it (upper bounds ≤ 12 %). A planted text-predictable dispersion shape of the same magnitude is recovered at 15–33 %. On MNLI and SNLI they recover 28–38 %.

Accordingly, replacing the shape of 69–83 % of training targets while preserving mode and mean changes LoRA judges by at most ±0.0015 RPS (95 % bounds). One-hot targets are worse on 10 of 11 panels.

For the annotation budget, frozen-feature judges gain more from additional items than from additional raters on most panels. In a prospective LoRA block on POPQUORN, one rating per item costs 0.006 RPS against the full data, and a second rating recovers about half.

We release reliability cards and estimators.

## 1. Introduction

Human raters disagree. A growing line of work therefore trains learned judges, meaning language models fine-tuned to score text, on the full distribution of human ratings rather than on a single aggregated label (Chen et al., 2025; Singh et al., 2025; Kohli, 2026; Benito-Santos & Ghajari, 2025). The appeal is that a histogram records which neighbouring levels received mass and how concentrated the ratings were. A judge that reproduces it would "capture human disagreement" rather than average it away.

The data behind that appeal are thin. In most datasets the histogram is computed from three to nine people. Five ratings of a code snippet's readability are a sample from a population of possible raters. A model trained to reproduce that sample exactly is therefore partly trained to reproduce sampling noise.

We ask a question that work on learning from label variation (Uma et al., 2021; Plank, 2022) has not asked in this form: **which part of a few-rater histogram can a text-conditioned judge learn?** We split every histogram into its *location*, meaning its mode and mean, and its *shape beyond location*, meaning the residual allocation of mass once mode and mean are fixed. We then measure two properties of the shape that are usually conflated.

1. **Reproducibility across raters (§3).** If a disjoint panel rated the same items, would the shape come out the same? We estimate this without a learner, using a split-half design. An exact identity, A1 = M − 2X, links three quantities:
   - A1, the value of the raw histogram for forecasting a new rater;
   - M, the magnitude of the histogram's residual relative to an exact mode-and-mean comparator;
   - X, the agreement of that residual across the two panels.

   The ratio ρ = X/M is a split-half reliability of the shape at a given number of raters. The raw histogram beats the comparator for predicting a new rater exactly when ρ > ½.
2. **Predictability from the text (§4).** Even a reproducible shape is useless to a judge unless the text carries it. We fit a cross-fitted ridge decoder from a frozen LLM's representation to the residual of panel 1. We score it against panel 2's residual measured from *its own* mode and mean, using a proper-score gain $G_{\rm own}$. We also report the gain as the fraction $G_{\rm own}/X_{\rm own}$ of the reproducible own-shape, with item-cluster CLT intervals. Each estimate is checked against a within-cell feature-permutation control, a positive control, and planted shapes that calibrate power.

**Findings.**

*(i) The shape beyond mode and mean is poorly reproducible on ordinal scales (§3).*

- With 4–8 raters per item, its split-half reliability is 0.04–0.41, and the intervals include 0 on four of eight panels. With three raters it cannot be measured at all, because a split leaves two ratings per item, which are fixed by their own mode and mean.
- On the dense ordinal panels it stays below 0.3 up to 40 raters, so on no ordinal panel does the raw histogram forecast a new rater better than its own mode and mean. On ChaosNLI, by contrast, the forecasting reliability exceeds ½ from two to three raters.
- The reproducibility of the shape itself at 40 raters is 0.06–0.22 on the dense ordinal panels and 0.61 / 0.67 on MNLI / SNLI.

*(ii) Little of the ordinal own-shape is linearly decodable from the frozen features we tested, even where it exists (§4).* Across panels, the ordinal own-shape is:

- undetectable on SummEval's non-duplicated items, POPQUORN and DICES-990;
- on Dorn's readability panel, of the size that location and rater thresholds alone produce;
- detectable beyond location only on DICES-350, and only within its observed rater pool.

DICES-350 at 40 raters is therefore the clean ordinal case. There, frozen features of three model families recover −1 to 1 % of the own-shape (upper bounds ≤ 12 %). A planted text-predictable dispersion shape of the observed magnitude is detected in 5 of 5 draws and recovered at 15–33 % (a polarisation plant only in 3 of 5, §7), and a location-and-threshold simulation of the panel yields no own-shape at all. On MNLI and SNLI the decoder recovers 28 % [24, 33] and 38 % [33, 42]. Every NLI lower bound exceeds every ordinal upper bound.

*(iii) The judges we trained show no detectable use of the shape (§5).*

- Replacing the shape of 69–83 % of LoRA training targets while preserving each target's exact mode and mean changes held-out RPS by −0.0001 [−0.0011, +0.0011] on SummEval and +0.0000 [−0.0009, +0.0009] on POPQUORN. This null is expected, since neither panel has a detectable own-shape.
- The discriminating case is ChaosNLI, where the same intervention costs 0.005–0.017 Brier.
- Across eleven ordinal panels, one-hot targets are worse on 10 of 11.
- Beyond item location, the remaining structure is mostly rater-side. On the four panels with persistent rater identities, rater-specific cut-points improve held-out likelihood by 0.05–0.16 nats per rating, while item-specific dispersion adds −0.017 to +0.012.

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

**Learning from label variation.** Human label variation is increasingly treated as signal rather than noise (Aroyo & Welty 2015; Pavlick & Kwiatkowski 2019; Uma et al. 2021; Plank 2022). Soft-label training is reported to improve calibration and robustness (Peterson et al., 2019; Collins et al., 2022; Singh et al., 2025). Chen et al. (2025) train learned judges on human rating distributions. Kohli (2026) shows that on ChaosNLI the item-specific information in soft labels saturates around ten annotators for KL. These studies compare training targets; none separates the part of the histogram that is reproducible across raters from the part that is predictable from the input.

**Predicting disagreement.** NLI label distributions are partly predictable from text (Zhou et al. 2022). Reward models detect diverging preferences with AUROC around 0.6 (Zhang et al., 2025), and demographic information helps predict who disagrees (Wan et al., 2023). We give the matching quantity for the shape beyond mode and mean, normalised by its reproducible part.

**Reliability and rater effects.** The reliability of aggregated annotations depends on the number of raters (Wong & Paritosh, 2022). Rater severity and scale use are classical facets in many-facet Rasch measurement (Linacre, 1989; Eckes, 2011). We apply the split-half logic and the rater facet to the shape beyond location.

**Annotation budgets.** Whether to label more items or relabel existing ones is an old question in crowdsourcing (Sheng et al., 2008; Lin et al., 2014). For hard-label classifiers, labelling many items once is preferable above a worker-quality threshold (Khetan et al., 2018). On ChaosNLI, Zhang et al. (2021) find the opposite: a few hundred ten-label items beat a few thousand single-label ones in KL. Their regime has a large single-label base and evaluates the full distribution. Ours is the complementary one: every rating competes for items, and judges are trained only on the budgeted data.

## 3. Reliability across raters

**Setting.** Item $i$ has ratings on $K$ ordered levels, with empirical histogram $h_i$. We score ordinal forecasts with the ranked probability score $S(f,y)=\sum_k (F_f(k)-\mathbf 1[y\le k])^2/(K-1)$ and write $C$ for the cumulative operator. For nominal tasks (ChaosNLI), $S$ is the Brier score and $C$ is the identity.

The *location* of a histogram is its exact mode and mean; for nominal tasks it is the modal class and modal mass. To isolate the *shape beyond location* we use the exact-T comparator $q_T$: a cross-fitted forecast built from other items in the same exact mode-and-mean cell. It is KL-projected onto the cell when the cell is sparse (Appendix A). By construction $q_T$ has the same location as $h_i$ and differs from it only in shape. The residual of a histogram is $r = C(h - q_T)$.

**Split-half identity.** In each repetition, every item's ratings are split at random into disjoint panels $P_1$ (size $a$) and $P_2$. Let $r_1 = C(h_1-q_T)$ and $r_2 = C(h_2-q_T)$, with $q_T$ computed from $P_1$. The value of the raw histogram over the comparator for forecasting a rating in $P_2$ then obeys the exact identity
$$A1 = \mathbb E\big[S(h_1,y)-S(q_T,y)\big]_{y\in P_2} = M - 2X,$$
with $M=\|r_1\|^2/n$ and $X=\langle r_1,r_2\rangle/n$. Here $\langle u,v\rangle=\sum_k u_k v_k/(K-1)$. Hence $\rho = X/M$ is a *new-rater forecasting reliability*: the raw histogram beats the location-only forecast exactly when $\rho>\tfrac12$.

**Own versus cross reproducibility.** Because $r_2$ is measured against panel 1's comparator, $X$ is not purely agreement between the two panels' shapes. Writing $q_j$ for the comparator built from panel $j$, it splits as $X = X_{\rm own} + X_{\rm cross}$:

- $X_{\rm own}=\langle r_1, C(h_2-q_2)\rangle/n$ is the agreement of the two shapes, each measured beyond its own location;
- $X_{\rm cross}=\langle r_1, C(q_2-q_1)\rangle/n$ is panel 1's residual predicting the other panel's location shift.

The cross-term is not negligible. It is 31–40 % of $X$ on ChaosNLI at $a=20$, and about half or more of $X$ on the ordinal dense panels at $a\le 8$. We therefore treat $\rho$ as a forecasting quantity and use $\rho_{\rm own}=X_{\rm own}/M$ for the reproducibility of the shape itself.

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
This gain measures the shape alone. It excludes the part of the full gain that comes from predicting panel 2's location shift; the full, cross-term-inclusive ratio $G/X$ is reported in Appendix B. The headline estimand is $G_{\rm own}/X_{\rm own}$, reported where $X_{\rm own}$'s interval excludes 0.

Intervals are item-cluster CLT intervals on per-item contributions, averaged over ten cross-fitting repetitions with the predictions held fixed. Ratios get delta-method intervals. As a check fixed in advance, the interval for $\langle\hat r,s_2\rangle/n$ covers 0 in 9 of 10 null draws (Appendix A).

**Controls.** Every estimate has three controls:

1. A *within-cell permutation* of the features among items with the same exact mode and mean. Under this control $G_{\rm own}$ must be at or below zero; its null expectation is $-E\|\hat r\|^2/n$, the decoder's variance penalty.
2. A *positive control* that predicts the panel-1 mean with the same pipeline.
3. A *planted shape* used to calibrate power. Item dispersion is made log-linear in a random feature direction, with γ setting the strength, and is simulated with the panel's fitted rater cut-points. We call the plant detected when the CLT lower bound of $G_{\rm own}$ exceeds 0. For Dorn and DICES-350, the reference strength is the smallest γ whose mean planted $X_{\rm own}$ reaches the observed one; the rule prespecified for SummEval and POPQUORN compares $X$ instead (Appendix B).

**Pool bias.** Within the observed rater pool, $X_{\rm own}$ is biased downward for new raters. This happens because each item's halves are drawn without replacement from one pool of raters with different cut-points, so the rater mixes of the two halves are anti-correlated. Simulations from the fitted rater–item model locate this bias (Appendix A). It makes "no detectable own-shape" easier to declare, and we read the nulls below accordingly.

**Results (Table 2).**

*Where an own-shape is detectable at all.* The ordinal own-shape is undetectable on SummEval's non-duplicated items, POPQUORN ($a=4$) and DICES-990 ($a=20$); on these panels $G_{\rm own}$ ≈ 0. Two ordinal panels have a detectable own-shape:

- On Dorn's readability panel the decoder recovers 10 % [4, 16]. However, a pure location-and-threshold simulation of Dorn's Java panel already yields a text-decodable own-shape: over five draws its $\langle\hat r, s_2\rangle$ averages about 95 % of the value observed on the real panel. A plant matching the observed magnitude is detected in only 1 of 5 draws. Dorn's 10 % is therefore an upper bound, of the size location alone produces.
- On DICES-350 the decoder recovers −8 % [−23, 8] at 20 raters per half and 1 % [−9, 12] at 40.

*NLI.* The decoder recovers 28 % [24, 33] on MNLI and 38 % [33, 42] on SNLI. With four raters per half, ChaosNLI still gives 22 % [18, 26] and 28 % [24, 32].

*The NLI–ordinal gap.* Every NLI lower bound exceeds every ordinal upper bound; the smallest margin is 18 % vs 16 % (ChaosNLI MNLI at 4 raters per half). The gap also holds net of the variance penalty, $(G_{\rm own}-G_{\rm own,perm})/X_{\rm own}$, at 20 raters per half: at most 30 % on the ordinal panels against at least 32 % on NLI.

*DICES-350 at 40 raters, the clean ordinal case.*

- A location-and-threshold simulation of the panel yields no own-shape at all: mean $X_{\rm own}$ is −1.3·10⁻⁵, against the observed 4.9·10⁻⁵. A reproducible ordinal shape beyond location therefore exists here within the observed rater pool.
- A planted text-predictable dispersion shape of matching magnitude is detected in 5 of 5 draws and recovered at 15–33 %. A polarisation plant of matching magnitude is detected in only 3 of 5 (§7).
- Against this, the observed recovery is −1 to 1 % across the three feature families, with upper bounds ≤ 12 %.

On DICES-350, then, the shape exists within the observed rater pool, the decoder has power for a planted shape of this size and construction, and the observed shape is not decoded.

*Robustness.* Qwen3-8B and OLMo-2-7B give the same readings (MNLI 30 % and 29 %); own-shape decoding on all three families covers SummEval, MNLI and DICES-350, the other panels are Qwen2.5 only. A nonlinear random-feature decoder (SummEval and POPQUORN only), the cross-term-inclusive ratio $G/X$, and a valid-forecast version projected onto the exact cell all agree (Appendices A–B). Scored as a valid forecast, the permutation-corrected gain is ≤ 6·10⁻⁵ RPS on the ordinal panels, against 0.0065 and 0.0072 on MNLI and SNLI.

**Why the two reliabilities can come apart.** $\rho$ asks whether the shape is a property of an item's rater population, and $G_{\rm own}$ asks whether it is a property of the item's text. A shape can be reproducible yet invisible to text, for instance when it arises from how particular raters use the scale. Section 5 shows that, on the panels with persistent rater identities, most held-out likelihood structure beyond item location is associated with who rated.

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

**Where the ordinal structure beyond location lives.** We fit ordered-probit models $Y^*_{ir} = \theta_i + \sigma_i\varepsilon_{ir}$ with cut-points $c_r$ to the panels with persistent rater identities, and location-plus-dispersion models to the position panels:

- M0 has item location and common cut-points;
- M1 adds rater-specific cut-points;
- M2 adds item-specific dispersion.

Rater thresholds carry the structure. M1 improves held-out likelihood by 0.05–0.16 nats per rating, whereas item dispersion adds −0.017 to +0.012.

Simulating from the fitted models and re-running the split-half analysis at 40 + 20 raters gives a panel-dependent answer:

- On DICES-350, thresholds reproduce the observed $X_{\rm own}$ where location alone does not.
- On Buse–Weimer, location alone suffices.
- On Dorn's Java panel, only the dispersion model does.

At smaller splits, the location-only model reproduces most of the observed $X$ through $X_{\rm cross}$ (Appendix F). This is the textbook mechanism of many-facet Rasch measurement (Linacre, 1989; Eckes, 2011), which we present as measurement, not as a claim about raters' psychology. On the panels with persistent rater identities, most of the held-out likelihood structure beyond item location is associated with who rated, and a judge that sees only the text cannot learn that part. Whether the residual shape itself is rater-side is established only on DICES-350, conditional on its observed rater pool.

## 6. Annotation budget

We test the budget question directly, as an observation in its own right: hold the total number of ratings fixed and trade items for raters. We do not derive the answer from §§3–5. A registered mechanism-based prediction failed on ChaosNLI (§1).

**Frozen-feature heads** (eight ordinal and two nominal panels, thirty configurations each; Appendix F). On four of the five panels with more than 900 training items, more items with fewer ratings each wins monotonically. On DICES-990 at a budget of 594 ratings, for example, RPS rises steadily as ratings are concentrated on fewer items: 594 items × 1 rating gives 0.203, 297 × 2 gives 0.205, 148 × 4 gives 0.207, 74 × 8 gives 0.213 and 40 × 15 gives 0.219.

SummEval is flat. The direction reverses only on small item sets (60 and 210 training items), where a single rating per item is too noisy a target. The items-first order also holds on ChaosNLI (959 × 1: KL 0.226; 30 × 32: 0.323). What differs between tasks is the *marginal* value of a second rating on items already covered: −12 to −15 % on ChaosNLI against −1 to −3 % for the Qwen2.5 heads on the large ordinal panels.

**LoRA judges on POPQUORN** (Table 3). POPQUORN offensiveness has homogeneous rating positions, which makes it the clean budget case. Every arm trains for the same number of optimizer steps, and all contrasts are taken within one batch, because LoRA training on our hardware is not bit-reproducible: per-cell RPS varies by ≤ 0.0012 between identical runs. A prospective block with independent rating assignments (ROUND20 R20-4) gives:

- 819 × 1 − full = +0.0063 [+0.0030, +0.0099]: one rating per item is worse than the full data.
- 819 × 2 − 819 × 1 = −0.0031 [−0.0062, −0.0002]: a second rating recovers 49 % of that gap.
- 117 × 7 − 819 × 1 = +0.0027 [−0.0024, +0.0074]: items-first is not supported.

The earlier same-batch block gives the same three readings, with 819 × 1 − full = +0.0087 [+0.0054, +0.0122] and 62 % recovered by a second rating.

**SummEval measures dilution, not budget.** Each SummEval item carries three expert ratings and five crowd ratings, and the evaluator is always a held-out expert. Because the crowd mean is nearly uncorrelated with the expert mean (r = 0.04), a judge trained on the crowd ratings alone is +0.014 to +0.025 RPS worse than the full-data judge on every fold. There, "fewer ratings per item" changes how far two expert ratings are diluted by five crowd ratings. We report those blocks, including their Qwen2.5 and OLMo-2 replications, in Appendix C.

**Guidance, conditional on task and learner.**

- For ordinal rating tasks with more than 900 items, frozen-feature heads favour covering items first (SummEval is flat; HelpSteer2 on OLMo-2 is the exception); on ≤ 210 training items the direction reverses.
- With LoRA judges (POPQUORN), two ratings per item are a safer default than one.
- Where the rater pool mixes populations, who rates matters more than how many ratings are collected.
- Many raters per item belong where a reliable reference distribution is itself the deliverable: evaluation sets, and tasks such as NLI where the shape is in the text.

## 7. Limitations and conclusion

**Limitations.**

- *Learners and decoders.* The frozen-feature analyses use three model families, but own-shape decoding on all three covers only SummEval, MNLI and DICES-350; the other panels and the valid-forecast gain are Qwen2.5 only. The SummEval LoRA contrasts (Appendix C) replicate on OLMo-2-7B; the POPQUORN budget block and the LoRA audit are Qwen2.5 only. We test linear decoders and one non-linear probe (on SummEval and POPQUORN only), not fine-tuned probes, so "not decoded" means not decoded by these.
- *Plant scope.* The main plant is one construction: item log-dispersion linear in one feature direction. At $a=20$ (Dorn) the matched plant is detected in 1 of 5 draws, at $a=40$ (DICES-350) in 5 of 5, and there are no plants on NLI. A second construction on DICES-350, text-predictable polarisation of two fixed rater groups (ROUND22 R22-6, grid amended after a smoke run), reaches the observed own-shape magnitude at γ = 1.5. There it is detected in only 3 of 5 draws, with recovery of 1–22 %, so the DICES-350 null is informative against the dispersion construction but not against polarisation.
- *Exact cells and the rater pool.* At 20 raters the exact (mode, mean) cell pools items of different latent location, so a decodable own-shape can be location-driven. The ordinal fractions are therefore upper bounds on shape beyond location, and the NLI values may contain such a component. The pool bias of §4 makes "no detectable own-shape" slightly easier to declare.
- *SummEval data.* The released file has identical crowd annotations on 807 of 1,600 items. This is undocumented and unverified upstream. It makes SummEval's full-panel numbers artefactual and its budget contrasts dilution contrasts (Appendix C).
- *POPQUORN position folds.* A user-held-out check with real user ids, in which no evaluator contributes to any target, confirms the audit and budget conclusions.
- *Effect sizes.* The effects lie in the third decimal of RPS. They should be read against the mode-only penalty of +0.012 and the POPQUORN budget effects of 0.006–0.009.

**Conclusion.** A few-rater histogram is a noisy location plus a shape that, on ordinal scales, is barely reproducible across raters and, where it is reproducible, is not linearly decodable from the frozen features we tested. On DICES-350 we can show both halves directly. The shape exists within the rater pool, a planted shape of its size is decoded, and the real one is not.

On NLI the shape is reproducible and a quarter to two-fifths of it is decodable. Learned judges follow the same split. For the budget, frozen-feature heads on ordinal panels with more than 900 items favoured covering items first, while for LoRA judges on POPQUORN two ratings per item beat one; we report this as an observation, not as a consequence of the mechanism. Reliability cards make that check possible before rating starts.

# Appendix

Sections A–F give the full estimator definitions and the complete results behind the main text. Their text follows the long version of the paper (PAPER_DRAFT_v2.md, v2.5); the main text quotes their numbers verbatim.

## A. Estimators

**Setting and notation.** Item $i$ has ratings on $K$ ordered levels from a panel of raters; the empirical histogram is $h_i$. For ordinal scales we score forecasts with the ranked probability score, $S(f,y)=\sum_k (F_f(k)-\mathbf 1[y\le k])^2/(K-1)$, and write $C$ for the cumulative operator; for nominal tasks (ChaosNLI) $S$ is the Brier score and $C$ the identity. The **location** of a histogram is its exact mode and mean (nominal: modal class and modal mass); the **shape beyond location** is what remains once these are fixed. To isolate it we use the *exact-T comparator* $q_T$: a cross-fitted forecast built from other items in the same exact mode-and-mean cell (KL-projected onto the cell when the cell is sparse), so that $q_T$ has the same mode and mean as $h_i$ and differs from it only in shape. The residual of a histogram is $r = C(h - q_T)$.

**A.1 Reproducibility across raters (split-half reliability).** In each of $R$ repetitions the ratings of every item are split at random into disjoint panels $P_1$ (size $a$) and $P_2$. Writing $r_1 = C(h_1-q_T)$ and $r_2 = C(h_2-q_T)$, with $q_T$ computed from $P_1$, the forecasting value of the raw histogram over the comparator obeys the exact identity
$$A1 \;=\; \mathbb E\big[S(h_1,y)-S(q_T,y)\big]_{y\in P_2} \;=\; M - 2X,\qquad M=\|r_1\|^2/n,\; X=\langle r_1,r_2\rangle/n,$$
where $\langle u,v\rangle=\sum_k u_k v_k/(K-1)$ for ordinal scales (the RPS normalisation; 1 for nominal), so the identity is exact as implemented. Thus $\rho = X/M$ is a **new-rater forecasting reliability**: the raw histogram beats the location-only forecast exactly when $\rho>\tfrac12$. Because $r_2$ is taken against panel 1's comparator, $X$ is not purely shape-to-shape agreement: writing $q_j$ for the comparator built from panel $j$, $X = X_{\text{own}} + X_{\text{cross}}$ with $X_{\text{own}}=\langle r_1, C(h_2-q_2)\rangle/n$ (agreement of the two panels' shapes, each beyond its own location) and $X_{\text{cross}}=\langle r_1, C(q_2-q_1)\rangle/n$ (panel 1's residual predicting the other panel's location shift). On the dense panels we report both; the cross-term is not negligible (31–40 % of $X$ on ChaosNLI at $a=20$; about half or more of $X$ on the ordinal dense panels at $a\le 8$), so we call $\rho$ a forecasting quantity and use $\rho_{\text{own}}=X_{\text{own}}/M$ for the reproducibility of the shape itself. On the small panels the second panel is a single rating, its own comparator is that rating, and $X_{\text{own}}\equiv 0$: there $\rho$ is by construction a statement about forecasting a new rater. $\rho$ is specific to the number of raters $a$ and, as a ratio, unstable when $M$ is tiny; we report it with intervals and omit it where the residual is structurally empty (e.g. two or three ratings on a three-level scale). We also report the support of the donor-replacement intervention (the fraction of items whose histogram could be changed at all while preserving mode and mean). A smoother, response-based comparator that does not reproduce the noisy location gives larger values of $\rho$ because it also credits location reliability; we use the exact comparator throughout. Intervals are item-cluster bootstraps in which all copies of a resampled item stay in one cross-fitting fold and the comparator is refitted in every replicate. *Population.* On panels whose rating columns are positions rather than persistent people (HelpSteer2, EmoBank, CSC, ChaosNLI, Dorn and the SE panels without identities), the item bootstrap resamples an item's ratings with the item, so the intervals refer to new raters *if* the anonymous positions are filled by different people independently across items — an assumption the datasets do not document. SummEval is mixed: its three expert columns are persistent people (intervals condition on them), its five crowd columns are positions; the crowd mean is nearly uncorrelated with the expert mean (r = 0.04; Fabbri et al., 2021), and on half of the released items the five crowd annotations are identical on all four dimensions, an undocumented pattern we could not verify upstream (Appendix C, ROUND22). Where raters recur across items (Buse–Weimer, DICES-350, DICES-990, Scalabrino, POPQUORN), item-cluster intervals condition on the observed rater pool; for the three complete crossed panels we also report crossed item × rater bootstrap intervals: the ρ upper bounds stay below the ½ forecasting threshold (BW 0.39, DICES-350 0.36 at 40 raters; DICES-990 0.10 at 10 raters, the largest feasible; rounded outward) — this supports "below ½" for new raters, not the "below 0.3" of the point estimates, but ρ_own's intervals then include 0 on BW and DICES-350 ([−0.004, 0.26], [−0.02, 0.19]), so for new raters we bound the ordinal shape-to-shape reproducibility above rather than show it positive, and for POPQUORN the LoRA comparisons are additionally given under user-level clustering (Appendix D). Table 1 gives the resulting *reliability cards*; Figure 1 traces $\rho$ and $A1^x = M-2X$ (the score change of the raw histogram over the exact comparator when forecasting a held-out rating; negative means the raw histogram is better) against $a$ on the dense panels.

**A.2 Predictability from the text (decodability).** A judge sees the text, not the raters. Whether the reproducible shape is available to it is a separate question, which we answer with the representation the judges are built on: last-token hidden states of the frozen Qwen2.5-7B-Instruct (Qwen2.5-Coder for code panels) under the same rating prompt. A multi-output ridge decoder, group-cross-fitted over five item folds with a label-free PCA and a nested penalty, predicts $r_1$ from the features; it is scored on the *independent* panel $r_2$ by the covariance $V=\langle\hat r,r_2\rangle/n$ and by the proper-score gain
$$G \;=\; \big(2\langle \hat r, r_2\rangle - \|\hat r\|^2\big)/n \;=\; \mathbb E_{y\in P_2}\big[S(q_T,y) - S(q_T + C^{-1}\hat r,\,y)\big],$$
the exact reduction in score obtained by adding the decoded shape to the location-only forecast. Two controls accompany every estimate: a *within-cell permutation* of the features among items with the same exact mode and mean (which must drive $G$ to zero or below), and a *positive control* that predicts the panel-1 mean with the same pipeline (which must be clearly positive, else the representation or the alignment is broken). A third control calibrates power: we plant a known, text-predictable shape (item dispersion log-linear in a random direction of the features, with the panel's fitted locations and cut-points) and rerun the unchanged pipeline. **Own-shape decomposition (ROUND20 R20-1).** With $s_2=C(h_2-q_2)$ (panel 2's residual from its own exact cell) and $d=C(q_2-q_1)$, the gain splits as $G=G_{\rm own}+G_{\rm cross}$, with $G_{\rm own}=(2\langle\hat r,s_2\rangle-\|\hat r\|^2)/n$ and $G_{\rm cross}=2\langle\hat r,d\rangle/n$, and likewise $X=X_{\rm own}+X_{\rm cross}$ (§3). The headline estimand is $G_{\rm own}/X_{\rm own}$, reported where $X_{\rm own}$'s interval excludes 0; we call $G/X$ the *normalised forecasting gain*. Reading the planted control on this scale: with no planted shape the permutation-corrected projected gain ΔGP is zero on both panels in every draw. $G_{\rm own}$ is slightly negative, as it must be: its expectation under the null is $-E\|\hat r\|^2/n$, the decoder's variance penalty. Our frozen null check, which required its interval to cover 0, was therefore ill-posed; the uncorrected projected gain GP is positive under the null (the smoothing artefact described below). Over five simulation draws on SummEval (ROUND20 R20-2), the planted shape is detected (item-cluster CLT lower bound of G_own > 0; ROUND22 R22-4) in 0 of 5 at γ = 0, 5 of 5 at γ = 0.3 and 5 of 5 at γ = 0.6. At γ = 0.6, $X_{\rm own}$ is 0.00033–0.00047, bracketing SummEval's observed 0.00038, and the decoder recovers 38–56 % of the planted own-shape (POPQUORN, five draws: detected in 5 of 5, 6–38 %). The rule we fixed in advance compares the planted $X$ with the observed $X$. The first grid fell short (strongest plant 0.00166 against 0.00198), so we added γ = 0.8 and 1.0 (ROUND20 R20-2a/c, written after seeing that). At γ = 1.0 (mean planted X 0.00225) the plant is detected in 5 of 5 draws and recovered at 31–57 %, so at its full-panel magnitude the SummEval null would be informative under the rule; but that magnitude is carried by the duplicated crowd annotations (ROUND22), so the calibration has no reproducible SummEval shape to refer to. On POPQUORN the reference plant (γ = 0.3, X 0.00060 against the observed 0.00036) is detected in 2 of 5, so its null is uninformative. The planted own-shape saturates near 0.0004–0.0005 for γ ≥ 0.6, close to SummEval's observed 0.00038; the 7–12 % recovery under $G/X$ (one R19-2 draw) came from the cross-term in the denominator. Two features of the estimator are post hoc and disclosed. First, at γ = 0, $X_{\rm own}$ is about −1·10⁻⁴ although the halves are exchangeable ($a=b=4$). Simulations from the fitted rater–item model locate the cause (ROUND21 R21-2). Each item's two halves are drawn without replacement from one fixed pool of raters with different cut-points, so the halves' rater mixes are anti-correlated. With identical cut-points, or with raters drawn afresh for each rating, the bias vanishes (SummEval −0.000099 ± 0.000010 vs +0.000007 and +0.000018; DICES-350 −0.000015 ± 0.000003 vs ≈ 0; none on the panels fitted with one rater group). The real $X_{\rm own}$ is therefore reproducibility within the observed rater pool, biased downward for new raters. That makes "no detectable own-shape" easier to declare: corrected for the pool effect, SummEval's full-panel $X_{\rm own}$ is about 0.00048 (a correction from a rater model that cannot produce the duplicated crowd annotations, so it does not describe them), and DICES-350's interval at $a=20$ only just covers 0. Second, the item bootstrap of $G_{\rm own}$ duplicates items inside the cross-fit and is not centred on its point estimate. We therefore use item-cluster CLT intervals on the per-item contributions, averaged over ten cross-fitting repetitions with the cross-fitted predictions held fixed, so that no item is ever duplicated (ROUND21 R21-1). Ratios get delta-method intervals. As a check, fixed in advance, the interval for $\langle\hat r,s_2\rangle/n$, which has mean 0 under the no-plant null, covers 0 in 9 of 10 null draws. A nonlinear decoder (approximate Gaussian-kernel ridge, 2,048 random Fourier features on the same PCA scores; ROUND19 R19-5) does not change this. On SummEval and POPQUORN its null is calibrated. Its planted-shape recovery is no better than ridge: the lower bound at the strongest plant stays below the ridge point estimate. On the real panels its $G/X$ upper bounds are 0.2 % and 0.4 %, as for ridge. The decoded forecast $q_T + C^{-1}\hat r$ need not be a distribution in $q_T$'s cell. It has negative mass on 3–82 % of items, a changed weak mode on ≤ 6 % of ordinal items, and on nominal panels a changed modal mass. We therefore also project it onto the cell: nearest point in the RPS metric with $q\ge0$, $\sum q=1$, $q_T$'s mean and weak mode, or its modal mass for nominal panels. The projection alone gains score with no text information, because it smooths toward the interior. We correct for this by subtracting the projected gain of the within-cell-permuted forecast, which is zero under the planted null. This permutation-corrected projected gain is reported beside $G$ (ROUND19 R19-8; point estimates). Directions are symmetrised ($P_1\leftrightarrow P_2$) and bootstrapped over item clusters. Because a single layer is a weak probe, we repeat the analysis with per-layer mean- and last-token features and greedy selection of the best layers (the probing recipe of Li et al., 2026).

**A.3 Why the two can come apart.** $\rho$ asks whether the shape is a property of the item's *rater population*; $G$ asks whether it is a property of the item's *text*. A shape can be reproducible yet invisible to text — for instance when it is produced by how particular kinds of raters use the scale — and a text-predictable shape can be unreliable with few raters. Section 5 and Appendix F examine how far a rater-side account explains the first case on the ordinal panels. Nothing in §3 or §4 trains a judge; both are measurements of the data and the representation, and both are released with the reliability cards so that a dataset builder can compute them before deciding how many raters to pay for.

## B. Full decoding results and positive controls

Table B1 gives the cross-term-inclusive normalised forecasting gain $G/X$ for every panel and family. The own-shape results of the main text (Table 2) are listed here in full, together with all planted-shape calibrations, the valid-forecast gain and the ChaosNLI check at four raters per half.

*Reproducibility (long form).* (i) *The shape beyond mode and mean is poorly reproducible on ordinal scales.* Its split-half reliability is 0.04–0.41 on eight panels with 4–8 raters per item (intervals include 0 on four; on SummEval's non-duplicated items, Appendix C, it falls to 0.10 and 0.05 with intervals including 0), and with three raters its reproducibility cannot be measured (Crupi et al. (2025)'s code-summary benchmark, MLCQ, Roy et al.): a split leaves two ratings per item, and two ratings are determined by their exact mode and mean under our tie rule, although 15–75 % of the three-rating histograms share their exact cell with a different histogram. On the dense ordinal panels it stays below 0.3 up to 40 raters (Buse–Weimer 0.22, DICES 0.25 and 0.15, Dorn's Java panel 0.29), so on no ordinal panel does the raw histogram forecast a new rater better than its own mode and mean. ChaosNLI is the contrast: the NLI shape's forecasting reliability exceeds ½ from two to three raters and reaches 0.96–0.98 at 40. Part of this forecasting reliability is panel 1's residual predicting the other panel's location shift (§3); the reproducibility of the shape itself at 40 raters (ρ_own) is 0.06–0.22 on the dense ordinal panels (BW 0.13, DICES-350 0.10, DICES-990 0.06, Dorn 0.12–0.22; with rater resampling the BW and DICES-350 intervals include 0, upper bounds ≤ 0.26) and 0.61 / 0.67 on MNLI / SNLI, so the ordinal–NLI contrast holds on both measures. 

*Decoding (long form).* (ii) *No ordinal panel shows a robustly reproducible shape beyond location, and where an own-shape is detectable little of it is linearly decodable from the frozen features we tested.* A cross-fitted linear decoder on frozen features predicts panel 1's residual; we score it against panel 2's residual from *its own* mode and mean, so that the gain $G_{\rm own}$ measures the shape alone and not panel 2's location shift (§4). As a fraction of the reproducible own-shape $X_{\rm own}$ (item-cluster CLT intervals, §4; all panels and families in Table 2), it recovers:

- on the ordinal panels: 0.9 % [−0.3, 2.1] on SummEval coherence on the full panel, but on its non-duplicated items the own-shape is not detectable and the ratio (0.5 % [−4.6, 5.6]) has no reproducible shape to refer to (relevance is dropped under the prespecified rule; ROUND22); 10 % [4, 16] on Dorn; and on DICES-350, whose own-shape is now detectable, −8 % [−23, 8] at 20 raters per half and 1 % [−9, 12] at 40;
- on NLI: 28 % [24, 33] on MNLI and 38 % [33, 42] on SNLI.

Every NLI lower bound exceeds every ordinal upper bound (smallest margin: 18 % vs 16 %, ChaosNLI MNLI at 4 raters per half). The same holds for the gain net of the decoder's variance penalty, $(G_{\rm own}-G_{\rm own,perm})/X_{\rm own}$: at most 30 % on the ordinal panels against at least 32 % on NLI at 20 raters per half. With four raters per half, ChaosNLI gives 22 % [18, 26] (MNLI) and 28 % [24, 32] (SNLI), so the NLI fractions do not depend on the larger panels; no ordinal panel offers a like-for-like partner at four raters, because none has a detectable own-shape there once SummEval's duplicated items are set aside. Qwen3-8B and OLMo-2-7B features give the same readings (SummEval full panel 1.7 % and 0.7 %; MNLI 30 % and 29 %). Taken together, the ordinal own-shape is undetectable on most panels (SummEval's non-duplicated items, POPQUORN, DICES-990), detectable on DICES-350 only within its observed rater pool, and on Dorn of the size location alone produces; where it is detectable at most 16 % of it is decoded, whereas a quarter to two-fifths of NLI's reproducible shape is. DICES-350 at 40 raters is the clean ordinal case: a planted text-predictable shape whose own-shape magnitude matches the observed one is detected in 5 of 5 draws and recovered at 15–33 %, against the observed −1 to 1 % across the three feature families (upper bounds ≤ 12 %; ROUND22 R22-5), and a location-and-threshold simulation of the panel yields no own-shape at all (mean $X_{\rm own}$ −1.3·10⁻⁵ against the observed 4.9·10⁻⁵; ROUND22 R22-3), so here a reproducible ordinal shape beyond location exists within the observed rater pool and is not decoded.

Dorn's 10 % is an upper bound on decodable shape *beyond* location. At 20 raters the exact (mode, mean) cell still pools items of different latent location, and a pure location-and-threshold simulation of Dorn's Java panel already yields a text-decodable own-shape: its $\langle\hat r, s_2\rangle$ is 5.6 SE above 0, and over five such draws it averages about 95 % of the value observed on the real Java panel (ROUND21 R21-7). A planted dispersion shape whose own-shape magnitude matches the observed one is detected in only 1 of 5 draws (4 of 5 at 2.7 times that magnitude). On Dorn, then, the decodable signal is of the size that location and rater thresholds alone produce. Its 10 % neither shows decodable shape beyond location nor excludes a shape of that size, and we use it only as an upper bound. Scored as a valid forecast (projected onto its exact cell, permutation-corrected), the gain is ≤ 6·10⁻⁵ RPS on the ordinal panels (SummEval 4·10⁻⁶ and 8·10⁻⁶, Dorn 3·10⁻⁵) against 0.0065 and 0.0072 on MNLI and SNLI. This valid-forecast gain is scored against panel 2's histogram, so it also contains the cross part (text-predictable location denoising) and is not a fraction of the own-shape. On DICES-990 ($a=20$) and POPQUORN ($a=4$), $X_{\rm own}$'s interval includes 0 and $G_{\rm own}$ is ≈ 0 (≤ 5·10⁻⁶ RPS). On HelpSteer2 and EmoBank the second half has two ratings, which are fixed by their own mode and mean, so the own-shape cannot be measured at this split. On these panels the forecasting reliability is carried by the cross-term, and no own-shape is detectable to decode at the split used. A planted text-predictable shape whose own-shape magnitude matches SummEval's is detected in 5 of 5 draws and recovered at 38–56 %; at half that magnitude it is detected in 5 of 5 (item-cluster CLT intervals; ROUND22 R22-4). On POPQUORN the same plant strength is detected in 5 of 5 draws, with recovery of 6–38 %. Our prespecified informativeness rule is stated on $X$. After two added plant strengths (γ 0.8, 1.0; amendments written after the first grid fell short), the smallest plant whose $X$ reaches SummEval's observed $X$ is detected in 5 of 5 draws, so the full-panel SummEval null would be informative; but that magnitude is carried by the duplicated crowd annotations, and on the non-duplicated items there is no own-shape to calibrate against (ROUND22); on POPQUORN the matching plant is detected in 2 of 5, so its null is not. The earlier, cross-term-inclusive ratio G/X also agrees across the three families (Table B1). 

## C. SummEval: duplicated crowd annotations and expert dilution

*SummEval caveat (ROUND22).* In the released SummEval file, the five crowd annotations of 807 of the 1,600 items are identical on all four dimensions. The crowd mean is also essentially uncorrelated with the expert mean (r = 0.04 on coherence; the near-zero agreement is reported by Fabbri et al., 2021). On the 793 remaining items, $X_{\rm own}$ is −0.00013 [−0.00030, +0.00003] (coherence) and −0.00003 [−0.00016, +0.00010] (relevance). The forecasting reliability also falls: ρ is 0.35 → 0.10 [−0.13, 0.23] on coherence and 0.40 → 0.05 [−0.19, 0.25] on relevance. The full-panel SummEval reproducibility above is therefore carried by the duplicated annotations, and SummEval provides no evidence of a reproducible ordinal shape at $a=4$. Its decoding fractions, and the plant calibrated to its magnitude, should be read in that light. 

*How to read the SummEval blocks.* Each SummEval item carries three expert ratings and five crowd ratings. The crowd mean is essentially uncorrelated with the expert mean (r = 0.04; Fabbri et al., 2021), and the evaluator is always a held-out expert. A judge trained on the five crowd ratings alone predicts an almost constant score, +0.014 to +0.025 RPS worse than the full-data judge on every fold. A judge trained on the two other experts' ratings alone is 0.042 better than the full-data judge for expert 1 but no better for expert 2 (ROUND20 R20-7, descriptive; these two arms ran in a separate batch from the reference arms, and their effects of 0.014–0.042 are an order of magnitude above the ≤ 0.0012 rerun variation). On SummEval, therefore, "fewer ratings per item" changes how far two expert ratings are diluted by five crowd ratings that carry almost no expert-aligned signal. The SummEval contrasts below are contrasts between such dilutions, not evidence about rating budgets within one rater population; POPQUORN, whose rating positions are homogeneous, carries that question. On SummEval coherence, with the Chen et al. objective and the three held-out-expert folds of §5, re-run in one batch with three optimizer seeds × three folds (SHRINKAGE_PROTOCOL Amendment 6; results/lora_budget_v2/), every arm trained for the same 240 optimizer steps (effective batch 8, same schedule, no early stopping; on POPQUORN 205), so arms differ only in the number of distinct items and their repetition; budgets are matched up to rounding (144 × 7 = 1,008 ratings, which favours the many-rater arm), a judge trained on 960 items × 1 randomly chosen rating (960 ratings) is not distinguishable from the judge trained on all 960 × 7 = 6,720 ratings (−0.0027 [−0.0061, +0.0014], crossed bootstrap over seeds and test documents; in this block the three seeds share one rating assignment per fold, so the interval covers optimiser but not assignment variation — see the prospective block below); 480 × 2 even appeared better than the full data (−0.0040 [−0.0084, −0.000001], an interval excluding 0 at a seventh of the budget, which we read as a sign of how much a shared assignment can mislead; vs 960 × 1: −0.0013 [−0.0073, +0.0039]), while 144 × 7 is worse than 960 × 1 by +0.0233 [+0.0176, +0.0285] — both prespecified readings hold as worded in the protocol ("one rating per item matches the full data", operationalised as an interval that contains 0 or lies below it, i.e. without an equivalence margin; "items first"). An earlier two-seed block whose full-data reference came from a different batch had suggested that 960 × 1 *beats* the full data (−0.0061); the same-batch re-run does not support that stronger claim. (The earlier block also gave 240 × 4: +0.0162 and 960 × 2: −0.0064 vs full; these designs were not re-run.) **Prospective block (ROUND19 R19-9).** We declared a margin of δ = 0.005 RPS and three readings before running new seeds (2003–2005), with every seed × fold cell drawing its own items and ratings. Results: 960 × 1 − full = +0.0064 [+0.0045, +0.0085] (90 %: [+0.0048, +0.0082]), so equivalence (TOST) and non-inferiority both fail; 144 × 7 − 960 × 1 = +0.0102 [+0.0052, +0.0157], so items-first holds. The single-rating penalty is concentrated in three of the nine cells (+0.014 to +0.018; the other six give −0.0009 to +0.0043). One of the three is a near-collapsed run whose predicted means barely vary (SD 0.07 against 0.23–0.38 elsewhere). Single-rating training is therefore noticeably less stable across assignments, and the shared-assignment null above reflects a favourable draw. Excluding the collapsed run, the mean penalty is still +0.0052 (descriptive). An OLMo-2 replication on the same assignments (ROUND20 R20-3) gives +0.0066 [+0.0044, +0.0089], positive in all nine cells (+0.0003 to +0.0121), so the penalty does not rest on one failed run. Its largest cells overlap with Qwen2.5's in two of three (per-cell r = 0.56). On OLMo-2, 144 × 7 − 960 × 1 = +0.0060 [−0.0007, +0.0128]: items-first is not supported on that base in the prospective block. The contrasts depend on which held-out expert scores them (descriptive, ROUND21 R21-6). On Qwen2.5 the single-rating penalty is ≈ 0 when expert 0 evaluates (+0.0002) and +0.007 / +0.012 for experts 1 and 2. On OLMo-2 it is positive for all three (+0.004 to +0.010). The experts differ in location (mean ratings 2.81, 2.39, 2.05 against a crowd mean of 2.81), so 'the full data' is a crowd-dominated target scored against one expert at a time, and the budget conclusions on SummEval hold conditional on that expert/crowd mixture. Across the three prospective blocks, one rating per item costs 0.0063–0.0066 RPS against the full data. These are two independent assignment sets: SummEval's is shared by the two bases, and POPQUORN's is separate. In an earlier shared-assignment block with OLMo-2-7B on SummEval, 960 × 1 was not distinguishable from the full data (+0.0007 [−0.0056, +0.0069]) and 144 × 7 was worse than 960 × 1 by +0.0095 [+0.0022, +0.0160] (results/lora_budget_olmo/summary_vs_a1_F1.0.md); the prospective OLMo-2 block is reported above; in a prospective single-batch block on SummEval/Qwen2.5 (ROUND20 R20-5b/c; full, 960 × 1 and 960 × 2 trained together), a second rating per item helps (960 × 2 − 960 × 1 = −0.0098 [−0.0132, −0.0066]; on OLMo-2, in its own single batch (R20-6), −0.0086 [−0.0117, −0.0056]), and 960 × 2 is not worse than the full data (OLMo-2: −0.0022 [−0.0050, −0.0001]). Its interval even lies below 0 (−0.0034 [−0.0066, −0.0004]), which we do not read as two ratings being better than seven. The effect is evaluator-specific: per held-out expert, 960 × 2 − 960 × 1 is +0.003, −0.009 and −0.023, and 960 × 2 − full is +0.002, −0.002 and −0.010 (OLMo-2: +0.003, −0.002, −0.007). The advantage over the full data comes entirely from expert 2, the expert whose ratings sit lowest relative to the crowd (descriptive). 

## D. LoRA blocks: audit, budget, nondeterminism

If a judge learned the shape beyond location, destroying that shape in its training targets would hurt it. A donor-replacement audit  does exactly this with certified dose: for 69–83 % of training items the histogram is replaced by another item's histogram projected onto the recipient's exact mode and mean (mean TV 0.30–0.35 among changed items), under two learners. **End-to-end LoRA judges** (Qwen2.5-7B-Instruct, the distributional objective of Chen et al., 2025; three optimizer–assignment realisations × three held-out-rater folds) change by −0.0001 [−0.0011, +0.0011] RPS on SummEval coherence and +0.0000 [−0.0009, +0.0009] on POPQUORN offensiveness, whereas destroying the location as well (mode-only replacement) costs +0.0120 [+0.0086, +0.0155] and +0.0029 [+0.0009, +0.0050] with every seed-by-fold cell positive (POPQUORN intervals resample rating positions; resampling users instead widens them to [−0.0014, +0.0015] and [−0.0004, +0.0065]). **Frozen-feature heads** on ten ordinal panels move by −0.0024 to +0.0006. On SummEval (once the duplicated crowd annotations are set aside) and on POPQUORN no own-shape is detectable at all (§4), so there a null is the expected outcome rather than independent evidence that judges ignore a learnable shape; the discriminating case is ChaosNLI, where the shape is reproducible and decodable. On the nominal ChaosNLI panels the same kind of intervention — scrambling the allocation of mass beyond the modal class while preserving the modal mass — raises the test Brier score (the paper's nominal score) by 0.005–0.012 on MNLI and 0.008–0.017 on SNLI at every annotation count (KL 0.016–0.052), i.e. by 0.29–1.31 of the Brier gap between an oracle that uses the item's own training histogram and the exact comparator on the same test items (ROUND19 R19-7); on binary αNLI, where the replacement cannot change any target, the same contrast is a sham and averages −0.003 to +0.002 (per-configuration SD up to 0.014, since optimisation noise is not matched across arms), so only the nine-configuration averages are interpreted.

**End-to-end LoRA judges** (Table D1). *POPQUORN, the clean budget case.* On POPQUORN offensiveness, whose rating positions are homogeneous, a block re-run in one batch with three optimizer seeds × three folds (SHRINKAGE_PROTOCOL Amendment 7; 205 optimizer steps per arm) gives: extra ratings per item help — 819 × 1 is +0.0087 [+0.0054, +0.0122] worse than the full 5,733-rating data and 819 × 2 recovers 62 % of that gap (819 × 2 − 819 × 1 = −0.0054 [−0.0084, −0.0027]) — and at 819 ratings, 819 × 1 and 117 × 7 cannot be distinguished (117 × 7 − 819 × 1 = +0.0022 [−0.0029, +0.0072]); of the three prespecified readings only "a second rating helps" holds. (An earlier two-seed block with a cross-batch reference had suggested an items-first ordering here as well; it is superseded.) A prospective POPQUORN block with independent assignments (ROUND20 R20-4) reproduces all three readings: 819 × 1 − full = +0.0063 [+0.0030, +0.0099]; a second rating recovers 49 % of that gap (819 × 2 − 819 × 1 = −0.0031 [−0.0062, −0.0002]); and 117 × 7 − 819 × 1 = +0.0027 [−0.0024, +0.0074]. Two ratings per item still cost +0.0032 [+0.0016, +0.0048] on POPQUORN. 

LoRA training on our hardware is not bit-reproducible (per-cell RPS varies by ≤ 0.0012 between identical runs), so all budget contrasts are taken within one batch (the descriptive R20-7 arms excepted). Single-rating training behaves like stochastic label sampling (Gheibi & Ghazizadeh, 2026) and is consistent with the many-once-over-few-many results for hard-label classifiers (Khetan et al., 2018; Lin et al., 2014); our contribution is the demonstration with distributional targets and end-to-end LLM judges. We do not derive the budget result from §§3–5: a registered mechanism-based prediction failed on ChaosNLI (§1).

*Long-form summary of findings (iii)–(v).* (iii) *The judges we trained show no detectable use of the shape.* Replacing the shape of 69–83 % of training targets while preserving each target's exact mode and mean changes LoRA judges by −0.0001 [−0.0011, +0.0011] RPS on SummEval and +0.0000 [−0.0009, +0.0009] on POPQUORN (position-level bootstrap; user-level [−0.0014, +0.0015]), whereas destroying the location as well costs +0.012 and +0.003 (POPQUORN user-level interval [−0.0004, +0.0065]); since neither LoRA panel has a detectable own-shape, this null is expected rather than discriminating, and the discriminating case is ChaosNLI; the same intervention on ChaosNLI costs 0.005–0.017 Brier (0.016–0.052 KL). Across eleven ordinal panels and three feature families, training frozen-feature heads on the location-only comparator or on reliability-shrunk shapes changes held-out RPS by at most 0.0012 with mixed signs; other smoothing constructions move it by −0.005 to +0.009 in panel-dependent directions; one-hot targets are worse on 10 of 11 panels. A user-held-out replication on POPQUORN, where no evaluator contributes to any target, gives the same signs. (iv) *Beyond location, rating structure is mostly rater-side.* On the four panels with persistent rater identities, rater-specific cut-points improve held-out likelihood by 0.05–0.16 nats per rating while item-specific dispersion adds −0.017 to +0.012. Whether the residual shape itself is rater-side is panel-dependent: simulations at 40 raters show thresholds reproduce it where location alone does not on DICES-350, location alone suffices on Buse–Weimer, and item dispersion is needed on Dorn's Java panel. (v) *Budget.* At a fixed number of ratings, frozen-feature heads improve with more items rather than more raters per item on four of the five ordinal panels with more than 900 items and on both ChaosNLI panels (SummEval is flat; panels with ≤ 210 training items reverse). On SummEval, prospective blocks with independent rating assignments and a declared 0.005-RPS margin find LoRA judges trained on one rating per item worse than those trained on the full seven-rating data, by +0.0064 [+0.0045, +0.0085] on Qwen2.5 and +0.0066 [+0.0044, +0.0089] on OLMo-2, so equivalence and non-inferiority both fail on both bases. Because SummEval's crowd ratings are nearly uncorrelated with the held-out experts, these SummEval contrasts measure how far the expert ratings are diluted rather than the value of a rating as such (Appendix C). Earlier blocks with a shared assignment could not distinguish them. At a matched budget, 960 × 1 beats 144 × 7 on Qwen2.5 (+0.010 [+0.005, +0.016]; shared-assignment blocks 0.023 and, on OLMo-2, 0.0095), but not significantly on OLMo-2 in the prospective block (+0.006 [−0.001, +0.013]); on POPQUORN (same-batch re-run, and again in a prospective block with independent assignments) a single rating per item is worse than the full data (+0.0063 [+0.0030, +0.0099] prospectively), a second rating recovers about half of that gap (49–62 %), and items-first is not supported. A prediction we registered — that multi-rater items would pay off at fixed budget where the shape is text-predictable — was falsified on ChaosNLI; we therefore do not derive the budget result from the mechanism and report the task-dependence of the marginal value of extra ratings as an observation.

## E. Software-engineering panels

Readability, summary quality and code-smell severity are rated on the same few-rater scales, and the same questions arise for code judges. Dorn's readability study (360 snippets in Java, Python and CUDA; 161–267 developers per snippet) gives the densest ordinal panel we know of; its reliability curve matches Buse–Weimer and DICES: the shape beyond mode and mean reaches a split-half reliability of only 0.2–0.3 even with 40 developers per snippet (Figure 1). The LLM-judge validation benchmarks of the field have three raters per item — Crupi et al.'s code summaries, MLCQ's smell severities, Roy et al.'s summaries — and with three raters the split-half reliability of the shape cannot be estimated. A split leaves two ratings per item, and two ratings are fully determined by their exact mode and mean: the mode is $z$ = z_label (among tied modes the one nearest the median, then the lowest) and the mean is the rating sum, so the donor-replacement support is 0 %. The three-rating histograms themselves do carry shape. On these 4-, 5- and 11-level scales, 15–75 % of items share their exact cell with a different histogram (results/support_three.json), but whether that shape is reproducible cannot be measured from three raters. Scalabrino's nine-rater panel sits in between (Table 1). Decoding from frozen features recovers at most a small fraction of it: the own-shape fraction $G_{\rm own}/X_{\rm own}$ is 0.10 (upper bound 0.16) on Dorn's readability panel (360 snippets; normalised forecasting gain $G/X$ +0.03 [−0.03, +0.05]), with a small detectable valid-forecast gain (permutation-corrected projected gain > 0, as on HelpSteer2 and EmoBank, where it reflects within-cell location denoising rather than shape), negative on Scalabrino (G < 0, a small over-fitting penalty on 124 snippets; its X interval covers 0, so no ratio is reported), and uninformative on Buse–Weimer (+0.07 [−0.07, +0.26], 100 snippets) and JetBrains naming (+0.01 [−0.37, +0.03], 120 identifiers) (results/decoding_v2/). For SE human studies the practical reading is that with three raters per artifact the reproducibility of the shape cannot be assessed at all, that with 4–9 it is low (Table 1), and that adding raters to a few artifacts does not make the shape of developer disagreement reproducible on these readability and quality scales.

## F. Frozen-feature heads, shrinkage and the rater–item model

A stronger version of the same test asks whether *any* construction of the per-item target helps. We trained the heads on eleven ordinal panels with the raw histogram, the location-only comparator, reliability-shrunk shapes and locations, Dirichlet smoothing toward the mode prototype (the mean histogram of other-fold items with the same mode), label smoothing toward uniform and toward the marginal, and a cross-item smoothed comparator, thirty configurations each (5 seeds × 3 group-disjoint item splits × 2 annotation-position splits). The location-only comparator and reliability-shrunk shapes change held-out RPS by at most 0.0012 with mixed signs; the other smoothing constructions move it by −0.005 to +0.009 with signs that differ across panels; the one-hot target is worse on 10 of 11 panels (up to +0.010; Scalabrino −0.0013). The learner pools location across items on its own and shows no sensitivity to the per-item shape — what §4 leads one to expect for a shape that is not linearly decodable from its features. In these audits the ordinal-scale judges show no detectable sensitivity to the per-item shape beyond location, whereas on NLI the same intervention is costly, consistent with the decoding result there.

The split-half analysis says the few-rater shape is mostly noise for forecasting a new rater (ρ > 0 with an interval excluding 0 on four of the eight small panels, and on two once SummEval's duplicated items are set aside), and on the dense ordinal panels the shape-to-shape reproducibility at 40 raters is small (ρ_own 0.06–0.22 with item-only intervals; with rater resampling the BW and DICES-350 intervals include 0); the decoding analysis says little of it is in the text. What is it, then? We fit three ordered-probit models to the rating matrices of the panels with persistent rater identities (Buse–Weimer, DICES-350, Scalabrino, the SummEval experts) and location-plus-dispersion models to the position panels: $Y^*_{ir} = \theta_i + \sigma_i\,\varepsilon_{ir}$ with cut-points $c_{r}$; **M0** item location with common cut-points, **M1** adding rater-specific cut-points (harshness), **M2** adding item-specific dispersion $\sigma_i$ (the inverse of IRT discrimination). Held-out log-likelihood over random cells, five folds, with the dispersion penalty chosen on held-out data.

Rater thresholds carry the structure: M1 improves held-out likelihood by +0.111 (BW), +0.146 (DICES-350), +0.156 (Scalabrino), +0.104 / +0.047 (SummEval coherence / relevance) nats per rating; item dispersion adds −0.017 (Scalabrino) to +0.012 and over-fits on the 5–7-rating position panels. Simulating rating matrices from the fitted models and re-running the split-half analysis at the dense splits (40 + 20 raters, 20 simulations per model; ROUND19 R19-3) gives a panel-dependent answer. On DICES-350 the observed $X_{	ext{own}}$ lies within the simulation range of the threshold model M1 but not of the location-only model M0, so thresholds explain something location alone cannot. On Buse–Weimer the location-only model already reproduces it, so thresholds are not needed for the residual even though they carry the likelihood gain. On Dorn's Java panel (no rater identities) only the dispersion model M2 reproduces it. At smaller splits ($a=10$) the location-only model reproduces most of the observed $X$ through $X_{	ext{cross}}$ (BW 0.00037 of 0.00052; Dorn Java 0.00056 of 0.00068): much of the small-$a$ positive $X$ is location noise interacting with the exact comparator, not shape. SummEval retains a small residual that neither thresholds nor one-dimensional dispersion reproduce; it is carried by the items whose five crowd annotations are identical, which no rater model generates, and it disappears on the remaining items (Appendix C, ROUND22). The mechanism is the textbook one of many-facet Rasch measurement (Linacre, 1989; Eckes, 2011), and we present it as measurement, not as a claim about raters' psychology; for judges it means that, on the panels with persistent rater identities, most of the held-out likelihood structure beyond item location is associated with who rated; whether the residual shape itself is rater-side is established only on DICES-350, and only conditional on its observed rater pool (with rater resampling its $\rho_{\rm own}$ interval includes 0, §3).

The annotation side confirms the same picture from a different angle. For forecasting a new rater from an item's own ratings, shrinking both location and shape toward the mode prototype by their split-half reliabilities improves RPS by −0.0048 [−0.0052, −0.0045] over the raw histogram (eight panels, inverse-variance pooled; descriptive only — the panels share documents and annotators and the pooled interval ignores that covariance), a cross-item smoothed comparator by −0.0117 [−0.0123, −0.0112]; shrinking the *shape* alone by its reliability $\lambda=X/M$ beats the raw histogram (−0.0020 [−0.0022, −0.0019]) but is indistinguishable from the location-only comparator (inverse-variance pooled −0.000019 [−0.000039, +0.000000]; descriptive, since the panels share documents and annotators) on every panel except SummEval and EmoBank, where $\hat\lambda\approx0.4$ (on SummEval a consequence of the duplicated crowd annotations, Appendix C) (results/shrinkage/SUMMARY.md, corrected cluster bootstrap). For forecasting a new rater, what a few-rater histogram contributes beyond its location is small.

**Frozen-feature heads** (eight ordinal and two nominal panels, thirty configurations each; Table F1; CSC is excluded because its 32 conversation contexts leave fewer than the design's minimum of 20 training groups). On four of the five panels with more than 900 training items (all but SummEval), more items with fewer ratings each wins monotonically: on DICES-990 at a budget of 594 ratings, 594 items × 1 rating gives RPS 0.203, 297 × 2 0.205, 148 × 4 0.207, 74 × 8 0.213 and 40 × 15 0.219; POPQUORN, HelpSteer2 and EmoBank follow the same order, SummEval is flat. The direction reverses only on small item sets (Buse–Weimer with 60 training items, DICES-350 with 210), where a single rating per item is too noisy a target. The same items-first order holds on ChaosNLI (959 × 1: KL 0.226; 30 × 32: 0.323) — a result that falsified a prediction we had registered, namely that multi-rater items would pay off at fixed budget where the shape is text-predictable. They do not; where tasks differ is the *marginal* value of a second rating on already-covered items (ChaosNLI −12 to −15 %, Qwen2.5 heads on the large ordinal panels −1 to −3 %), which we report as an observation.

**Guidance (conditional on task and learner).** For training a judge on an ordinal rating task, many ratings for few items were the better buy only on small item sets: on the ordinal panels with more than 900 items frozen-feature heads preferred more items in every comparison except SummEval, where the orderings are flat (within 0.002), and HelpSteer2 on OLMo-2, where 1436 × 2 edges out 2870 × 1 by 0.0007, while on the panels with ≤ 210 training items (Buse–Weimer, DICES-350) the direction reverses; For LoRA judges the clean case is POPQUORN, whose rating positions are homogeneous: a single rating per item is not a free substitute for the full data (+0.006 RPS in a prospective block), a second rating recovers about half of that, and covering items first was not significantly better than seven ratings on a seventh of them (+0.0027 [−0.0024, +0.0074]). Two ratings per item is therefore the safer default than one. The SummEval LoRA contrasts (Appendix C) mix expert and crowd ratings and are not used for this guidance. Where the rater pool mixes populations, as SummEval's experts and crowd do, who rates matters more than how many ratings there are: crowd-only targets carry almost no information about the experts. Raters belong where a reliable reference distribution is itself the deliverable — evaluation sets, and tasks such as NLI where the shape is in the text.


=============== (B1) ROUND21_PROTOCOL.md ===============
# ROUND21 protocol: response to the round-21 review (reviews/claude_round21_2026-11-06.md)

Each analysis is specified here before it is run. The review was produced by a Claude subagent because Codex was unavailable.

## R21-1 Valid intervals for the decoding estimands (review N1, N10). Specified 2026-11-06 12:53, before any run
**Problem.** The percentile item bootstrap of R20-1 duplicates items inside the cross-fit while α stays fixed. It is not centred on the point estimate, and the draft quoted only its upper side.
**Primary method.** Each point-estimate repetition (R = 10, two directions) already gives every item a cross-fitted prediction and a per-item contribution: g_i to G_own, v_i = ⟨r̂_i, s2_i⟩/NRM, x_i to X_own, the projected gains, and their permuted versions. We average the contributions over repetitions and directions and take the mean over items. The SE of that mean is the item-cluster (group) CLT standard error. Ratios θ = ḡ/x̄ get delta-method intervals from the influence values (g_i − θ x_i)/x̄.
This treats the cross-fitted decoder as fixed, which is standard for cross-fitted estimators. It ignores decoder-fitting variability, which is second order under cross-fitting and partly averaged out over the R repetitions. No item is ever duplicated. Code: decode_decomp.py with `--B 0 --tag _r21`, writing results/decode_decomp/<panel>_r21.json (key "clt").
**Sensitivity.** We also report the basic interval [2θ̂ − q97.5, 2θ̂ − q2.5] from the stored R20-1 percentiles (no rerun needed), together with the shift (percentile midpoint − θ̂).
**Calibration check (fixed now).** On the ten γ 0 draws (SummEval and POPQUORN, s0–s4), V_own has mean 0 under the null because r̂ depends only on other items' panel-1 data and the features. We report how many of its CLT 95 % intervals cover 0. If ≥ 9 of 10 cover 0, the method is used for the headline. Otherwise the headline reports point estimates only, with both interval types as sensitivity.
Note: G_own itself has negative expectation under the null (−E‖r̂‖²/n), so a G_own interval below 0 at γ 0 is expected. R20-1's reading (i) was ill-posed for G_own, and the draft says so.
**Estimands reported (N10).** G_own/X_own (the proper-score gain) and (G_own − G_own,perm)/X_own (the gain net of the variance penalty the decoder would also pay on permuted features). Both are reported with one sentence on what each answers.
**Readings (fixed now).**
- (i) The ordinal–NLI contrast is re-evaluated with the CLT intervals for both estimands: every NLI lower bound must exceed every ordinal upper bound among the panels with X_own's CLT interval excluding 0. This replaces R20-1 (iii) for the headline. R20-1's percentile result stays reported as the frozen outcome of R20-1.
- (ii) Panels re-run: the 14 R20-1 runs plus the 10 γ 0 draws.

## R21-2 Source of the negative null mean of X_own (review N5). Specified 2026-11-06 12:53, before any run
**Hypothesis.** In every simulated γ 0 matrix the M = 8 positions belong to fixed raters with their own cut-points (M2 model), and each item's two halves are drawn without replacement from that one pool. If half 1 gets the lenient raters, half 2 gets the strict ones. This finite-pool negative dependence is not fully absorbed by the exact (mode, mean) cell, and it makes E[X_own] < 0. With an infinite rater population, or with no rater heterogeneity, the bias should vanish.
**Design.** x_own_null.py simulates γ 0 matrices from the panel's M2 fit under three regimes: pool (as in R20-2), common (all raters use the median cut-points) and iid (each rating's cut-points drawn with replacement from the pool). It computes X_own exactly as decode_decomp.py, with 20 simulations and R = 10. Panels: summeval_coherence8 (a = 4), popquorn_off8 (a = 4), dices (a = 20), dices990 (a = 20).
**Readings (fixed now).**
- The hypothesis is supported if the pool mean is < 0 by more than 2 SE while both common and iid lie within 2 SE of 0.
- If supported: the paper explains the null bias as a finite-rater-pool effect. It notes that the same effect operates on real panels with a fixed rater pool, so a real X_own is the shape-to-shape reproducibility *within the pool* and is biased downward relative to an infinite population of such raters. The paper reports a pool-bias-corrected X_own (observed − simulated pool mean) as a sensitivity, and the absence statements (DICES, POPQUORN) are softened accordingly.
- If not supported: the bias is reported as unexplained, and the corrected X_own is still given as a sensitivity.

## R21-3 Rater-count-matched ordinal–NLI contrast (review N4). Specified 2026-11-06 12:53, before any run
ChaosNLI MNLI and SNLI are decoded at a = b = 4, matching SummEval and POPQUORN, with decode_decomp.py at R = 10 and B = 0 (CLT intervals, R21-1) under tag _a4_r21. DICES-350 is decoded at a = 40, b = 20 (m = 104), where §1 reports item-level ρ_own > 0.
**Readings (fixed now).**
- The matched contrast holds if the a = 4 NLI lower bounds of G_own/X_own exceed the SummEval upper bounds at a = 4. The abstract states the contrast at matched a if it holds. Otherwise it states it "at the a used", per panel.
- DICES-350 at a = 40 is a headline panel if its X_own CLT interval excludes 0.

## R21-4 Plant at a = 20 (review N3). Specified 2026-11-06 12:53, before any run
A dispersion plant on dorn_java (the Dorn panel with an M2 fit) at a = 20, b = 20, γ ∈ {0, 0.6}, draws s0–s2, with R = 10 and B = 0. The real dorn_java is run at a = 20 with the same settings. This is descriptive: detection (G_own CLT lower bound > 0) and recovery, and the planted X_own against the observed X_own. It gives the a = 20 ordinal panels a reference like SummEval's. No plant is defined for the nominal ChaosNLI panels, because the dispersion construction is ordinal.
**Calibration scale (N3).** From R21 on, the calibration compares planted with observed X_own, which is the scale of the headline estimand. R20-2's X-scale rule and its outcome stay reported as frozen.

## R21-5 Other feature families for the own-shape estimand (review issue 1a). Specified 2026-11-06 12:53, before any run
Rerun decode_decomp.py (R = 10, B = 0) with `--feat_model Qwen3-8B` and `--feat_model OLMo-2-1124-7B-Instruct` on the panels whose feature files exist in all three families: summeval_coherence8 (a = 4), chaosnli_mnli (a = 20) and dices (a = 20). We report G_own/X_own with CLT intervals per family. The abstract's "frozen LLM representations" is kept only if the SummEval and MNLI values agree in their qualitative reading across families. Otherwise it is restricted to Qwen2.5.

## R21-T Text corrections (review N2, N6–N9, N11–N19, LOW)
- **Plant figures.** POPQUORN γ 0.6 is 4 of 5, 6–38 %; mean planted X at γ 0.3 is 0.00060. The misplaced parenthetical is fixed. The averaging convention of R20-2c is flagged as post hoc.
- **EmoBank** (b = 2): unmeasurable, as HS2. "EmoBank (3–4 raters)" is removed.
- **Absence wording.** "No reproducible shape to decode" and "at the rater counts available" become "no detectable shape-to-shape reproducibility at a = …". The POPQUORN null is called uninformative.
- **ΔGP.** It is reported in absolute RPS, not on the X_own scale. ΔGP > 0 with X_own ≈ 0 (HS2, EmoBank) is described as text-predictable within-cell location denoising. "Dorn the only ordinal panel …" is corrected.
- **Contribution (4), §1 (v), §5 and guidance.** Items-first in the LoRA blocks holds in 1 of 3 prospective blocks. One threshold is used consistently for the frozen heads. The penalty wording becomes "the point estimates exceed the 0.005 margin; non-inferiority fails". The prospective blocks contain two independent assignment sets. §5 leads with the prospective blocks. The superseded 480 × 2 result is described accurately (its interval excludes 0). 819 × 2 − full is reported. The SummEval one-vs-two sentence is held until R20-5.
- **SummEval population (N11).** The evaluator is a held-out expert, and 960 × 1 draws a crowd rating with probability 5/7. We report descriptively the penalty stratified by whether the sampled training rating was an expert's, if train logs or meta allow it; otherwise the confound is stated.
- **§4.** The SummEval residual is restated in X_own terms. The DICES-350 rater-side claim is made conditional on the observed pool.
- **Abstract.** "On none" is backed by upper bounds or softened. The abstract is shortened.
- **§6.** "Three to five raters fix its location and nothing else" is replaced.
- **LOW.** The header, the "35–70 % of X on ChaosNLI" figure, the (iii) caveat restored, and the null-check sentence (GP > 0 at γ 0; only ΔGP is 0).

### R21-2 results (2026-11-06 13:09; 20 simulations × R = 10; results/x_own_null/*.json)
| panel (a, b) | rater groups (cut-point SD) | pool | common | iid |
|---|---|---|---|---|
| SummEval coh. (4, 4) | 4 (0.50) | **−0.000099 ± 0.000010** | +0.000007 ± 0.000011 | +0.000018 ± 0.000010 |
| DICES-350 (20, 20) | 104 (0.73) | **−0.000015 ± 0.000003** | +0.000004 ± 0.000003 | +0.000003 ± 0.000004 |
| POPQUORN (4, 4) | 1 (0) | −0.000002 ± 0.000013 | +0.000007 ± 0.000010 | +0.000007 ± 0.000009 |
| DICES-990 (20, 20) | 1 (0) | +0.000001 ± 0.000002 | +0.000002 ± 0.000002 | +0.000003 ± 0.000002 |
**Reading (as frozen): the hypothesis is supported** on SummEval and DICES-350. There the pool mean is < 0 by 10 and 5 SE, while common and iid lie within 2 SE of 0 (SummEval iid +1.8 SE). On POPQUORN and DICES-990 the M2 fit has a single rater group, so pool and common coincide and no bias is expected; none is found. This is consistent with the hypothesis.
**Consequences.**
- (a) The negative null mean of X_own is a finite-rater-pool effect. Splitting one fixed pool of heterogeneous raters without replacement makes the two halves' rater mixes anti-correlated, and the exact cell absorbs only part of that.
- (b) On real panels with persistent heterogeneous raters, X_own is shape-to-shape reproducibility *within the pool*, biased downward relative to new raters drawn from the same population.
- (c) Sensitivity (model-based correction): SummEval coherence X_own 0.00038 → about 0.00048, and DICES-350 (a = 20) 0.000044 [−0.000018, 0.000109] → about 0.000059 [−0.000003, 0.000124], whose interval still covers 0, by a margin smaller than the correction's own uncertainty. The draft says DICES-350 at a = 20 is "not detectable, and borderline after the pool correction".

### R21-1, R21-3, R21-4, R21-5 results (2026-11-06 13:33; 36/36 runs, R = 10, CLT intervals; results/decode_decomp/*_r21*.json)
**Calibration check (as frozen): passed.** V_own's CLT interval covers 0 in 9 of 10 γ 0 draws (the exception is SummEval s0, [+6e−8, +1.3e−6]), so the CLT intervals are used for the headline.

| panel | a | X_own [95 %] | G_own/X_own [95 %] | (G_own − G_own,perm)/X_own [95 %] |
|---|---|---|---|---|
| SummEval coherence | 4 | 0.00038 [0.00025, 0.00051] | 0.009 [−0.003, 0.020] | 0.022 [0.010, 0.034] |
| SummEval relevance | 4 | 0.00031 [0.00018, 0.00043] | 0.013 [0.001, 0.025] | 0.029 [0.014, 0.044] |
| Dorn (all) | 20 | 0.00027 [0.00020, 0.00034] | 0.10 [0.04, 0.16] | 0.11 [0.07, 0.16] |
| Dorn Java | 20 | 0.00027 [0.00016, 0.00038] | 0.003 [−0.15, 0.15] | 0.11 [0.03, 0.20] |
| DICES-350 | 20 | 0.000044 [0.000005, 0.000083] | −0.08 [−0.23, 0.07] | 0.12 [−0.06, 0.29] |
| DICES-350 | 40 | 0.000049 [0.000016, 0.000082] | 0.013 [−0.09, 0.11] | 0.15 [0.03, 0.27] |
| DICES-990 | 20 | 0.000022 [−0.000002, 0.000045] | — | — |
| POPQUORN | 4 | −0.00001 [−0.00011, 0.00010] | — | — |
| MNLI | 20 | 0.0111 [0.0102, 0.0120] | 0.28 [0.25, 0.32] | 0.36 [0.33, 0.40] |
| SNLI | 20 | 0.0112 [0.0102, 0.0122] | 0.38 [0.34, 0.42] | 0.45 [0.41, 0.49] |
| MNLI | 4 | 0.0042 [0.0036, 0.0047] | 0.22 [0.19, 0.25] | 0.31 [0.27, 0.35] |
| SNLI | 4 | 0.0035 [0.0030, 0.0040] | 0.28 [0.25, 0.32] | 0.36 [0.32, 0.41] |
EmoBank and HS2 (b = 2) are unmeasurable.

**R21-1 (i), as frozen.** Ordinal panels with an X_own CLT interval excluding 0: SummEval ×2, Dorn all, Dorn Java and DICES-350 at a = 20 and 40.
- On G_own/X_own: the largest ordinal upper bound is 0.16 (Dorn all) and the smallest NLI lower bound is 0.25 (MNLI, a = 20). **The contrast holds.**
- On the net fraction: the largest ordinal upper bound is 0.29 (DICES-350 at a = 20) and the smallest NLI lower bound is 0.33. **The contrast holds**, narrowly on that measure.

**R21-3, as frozen.** At matched a = 4, the NLI lower bounds (0.19 and 0.25; net 0.27 and 0.32) exceed the SummEval upper bounds (0.020 and 0.025; net 0.034 and 0.044) by an order of magnitude, so **the matched contrast holds**. DICES-350 at a = 40 has an X_own interval excluding 0, so it is a headline panel; its G_own/X_own is 0.013 [−0.09, 0.11].
Change from R20-1: with the CLT interval, DICES-350's X_own at a = 20 also excludes 0, whereas the percentile bootstrap covered it. "No detectable own-shape" no longer applies to DICES-350; it applies only to DICES-990 and POPQUORN.

**R21-4 (descriptive).** Dorn Java plant at γ 0.6: detected 3 of 3 (G_own lower bounds 1.7e−4 to 6.1e−4), recovery 0.23–0.41. Its planted X_own (0.0020–0.0024) is about eight times the observed 0.00027, so it is not matched in magnitude.
**New finding (post hoc, descriptive):** in the γ 0 plant on Dorn Java (location and rater thresholds only, no planted dispersion), X_own is 0.00012 [0.00003, 0.00020] and V_own is +4.6e−5, 5.6 SE above 0. At a = 20 the exact (mode, mean) cell pools items of different latent location θ. The within-cell shape is a deterministic function of θ under the threshold model, and θ is text-predictable, so the decoder can learn location-driven within-cell shape. G_own therefore contains a location-driven component wherever cells are coarse relative to the location spread. On Dorn Java, the γ 0 simulation alone reproduces about 45 % of the observed X_own, and its G_own (2.3e−5) exceeds the real one (7e−7). Real Dorn's G_own/X_own of 0.10 (dorn_all) should be read as an upper bound on decodable shape beyond location. The V_own calibration check above concerned SummEval and POPQUORN at a = 4, where this component is absent (9 of 10 cover 0).

**R21-5, as frozen.** G_own/X_own by feature family:
- SummEval: Qwen2.5 0.009, Qwen3 0.017 [0.006, 0.028], OLMo-2 0.007 [−0.004, 0.018];
- MNLI: 0.28, 0.30, 0.29;
- DICES-350: −0.08, −0.004, −0.05.
The qualitative readings agree across families, so "frozen LLM representations" is kept, with the three families named.

## R21-6 (specified 14:34, 2026-11-06, before running; descriptive, post hoc, responds to N11)
Per-evaluator-fold breakdown of the existing SummEval LoRA blocks: R19-9 (results/lora_budget_r19) and R20-3 (results/lora_budget_r20_olmo). Fold f evaluates against held-out expert f.
- For each block, design and fold: mean RPS minus the full arm, averaged over seeds, plus the seed range.
- Also reported: each expert's mean rating, its SD, and its distance (mean |difference|) to the crowd-mean of the same items.
- **Reading (descriptive only, no gate):** if one fold carries the sign of the 960 × 1 or 960 × 2 contrasts, the budget claims are stated as conditional on the evaluator expert, and the expert/crowd confound is named in §5. Nothing is re-tested.

### R21-6 results (2026-11-06 14:35; results/lora_by_fold.{json,md})
- Experts (mean, SD): e0 2.81, 1.13; e1 2.39, 1.44; e2 2.05, 0.96. Crowd mean 2.81.
- 960 × 1 − full, per fold (Qwen2.5, R19-9):

  | fold | penalty |
  |---|---|
  | f0 | +0.0002 |
  | f1 | +0.0071 |
  | f2 | +0.0119 |

  On OLMo-2 (R20-3) it is +0.0044, +0.0053, +0.0101.
- 960 × 2 − full: f0 +0.0005, f1 −0.0012, **f2 −0.0114** (all three seeds −0.0106 to −0.0121). The R20-5 "two ratings beat seven" result is a fold-2 (expert 2, the lowest-rating expert) effect. It reproduces in the seed-2003 rerun (−0.0103).
- 144 × 7 − full is positive on every fold.
- **Reading:** the SummEval budget contrasts are evaluator-dependent. §5 now states them as conditional on the expert/crowd mixture (draft updated). Nothing is re-tested.

## R21-7 (specified 2026-11-06 17:31, before running): X_own-matched plant at a = 20, plus the location-only baseline (N3 follow-up)
R21-4's γ 0.6 plant on dorn_java has X_own about 8 times the observed 0.00027, so it calibrates nothing about the observed magnitude.
- **Runs.** decode_decomp.py on dorn_java, a = 20, R = 10, B = 0, tag _r21. Plants γ ∈ {0, 0.1, 0.2, 0.3, 0.4}, draws s0–s4 (γ0 s0 exists).
- **Reference plant (rule on the X_own scale, as R21 adopted).** The smallest γ whose mean planted X_own ≥ the observed 0.00027.
- **Reported.** At the reference γ: detections (CLT lower bound of G_own > 0) out of 5, and the range of G_own/X_own.
- **Reading:**
  - 4–5 of 5 detected: the dorn_java estimate (G_own/X_own 0.003 [−0.15, 0.15]) is informative at its own magnitude.
  - Fewer than 4 of 5: it is not, and is reported as such.
- **Location-only baseline (descriptive).** Over the five γ0 draws, report the mean X_own and V_own as fractions of dorn_java's observed X_own (0.00027) and V_own (4.5e−5). The draft's location-driven caveat for Dorn is then quantified from these fractions.

### R21-7 results (2026-11-06 17:45; 25 runs, 0 tracebacks)
| γ | mean X_own (range) | detected / 5 | G_own/X_own range | mean V_own |
|---|---|---|---|---|
| 0 | 0.00009 (0.00004–0.00015) | 0 | 0.04–0.75 | 4.3e−5 |
| **0.1** | **0.00030** (0.00024–0.00036) | **1** | 0.07–0.20 | 8.7e−5 |
| 0.2 | 0.00072 | 4 | 0.13–0.41 | 2.9e−4 |
| 0.3 | 0.00116 | 5 | 0.19–0.51 | 6.1e−4 |
| 0.4 | 0.00160 | 5 | 0.16–0.51 | 8.3e−4 |
- **Reference γ = 0.1** (mean X_own 0.00030 ≥ 0.00027). It is detected in 1 of 5, so **the dorn_java estimate is not informative at its own magnitude** (frozen reading). Detection reaches 4 of 5 only at about 2.7 × the observed X_own (γ 0.2).
- **Location-only baseline (γ 0).** Mean V_own is 4.3e−5, about 95 % of dorn_java's observed 4.5e−5. Mean X_own is 0.00009, about a third of the observed 0.00027.
- Reading for the paper:
  - On Dorn at a = 20, the decodable signal is of the size that location and rater thresholds alone produce. A text-predictable shape beyond location of the observed size would usually go undetected.
  - Dorn's 10 % (dorn_all, X_own 0.00027, the same magnitude) is therefore neither evidence of decodable shape beyond location nor of its absence.
  - The ordinal–NLI contrast is unaffected in direction, since 10 % is used only as an upper bound.


=============== (B2) ROUND22_PROTOCOL.md ===============
# ROUND22 protocol — SummEval crowd-annotation integrity

## Finding (2026-11-06 21:33, from R20-7 diagnostics; descriptive)
These figures are for the released file data/summeval/model_annotations.aligned.paired.scored.jsonl, restricted to the 1,600 items with 3 expert and 5 turker annotations.
- **Duplicated turker annotations.** In 807 items (50.4 %), all five turker annotation dicts are identical on all four dimensions. The rate is 0 % for systems M17, M20, M22 and M23 and 62–79 % for the other twelve.
- **Expert–crowd agreement.** The expert mean and the crowd mean correlate at r = 0.04 (coherence), 0.07 (relevance), 0.01 (consistency) and 0.05 (fluency) at the summary level. At the document level r is 0.26 for coherence; at the system level it is −0.03. On non-duplicated items only, r = 0.09.
- **Agreement within groups.** Experts correlate with each other at 0.61–0.72 and crowd positions with each other at 0.46–0.53. The latter is inflated by the duplicates.
- **R20-7 (partial).** A judge trained on the five crowd ratings predicts an almost constant mean (SD 0.03) and is +0.012 to +0.024 RPS worse than the full-data judge against each held-out expert.

**Implication.** On SummEval, the "crowd" columns carry almost no expert-aligned signal, and in half the items they are a single value repeated five times.
- Every SummEval analysis mixes three expert columns with five such columns: split-half reliability, X_own, decoding, the budget blocks and the target-construction contrasts.
- In the budget blocks, "the full data" is two expert ratings diluted by five crowd ratings. The evaluator dependence (R21-6), the second-rating benefit and the 960 × 2 ≤ full result are all consistent with this dilution.
- Whether the duplication exists in the original release, or was introduced by the "aligned/paired/scored" processing we inherited, is **unverified**. This must be checked against the upstream file before any text attributes it to SummEval.

## R22-1 (specified 21:33, before running): sensitivity of the SummEval decoding headline
- **New panels.**
  - summeval_coherence8_nodup and summeval_relevance8_nodup: the 793 items without duplicated turker annotations. Features are sliced from the existing files; the item ids are the original row indices, checked by the alignment assert.
  - Note the composition shift: these items include all 400 items from M17/M20/M22/M23.
- **Runs.** decode_decomp.py --a 4 --R 10 --B 0 --tag _r22 on both panels; CLT intervals as in R21.
- **Reading.** The headline "SummEval 1–2 %, upper bound ≤ 2.8 %" stands if the nodup upper bound for G_own/X_own is < 24 % (the smallest NLI lower bound), so that the ordinal–NLI contrast holds. Otherwise SummEval is removed from the contrast. Either way, the nodup values are reported next to the full-panel values.
- **Not addressed here** (follow-ups, to be specified separately):
  - the LoRA budget and target-construction results on SummEval, which may need an experts-only or nodup re-run;
  - the reliability card for SummEval.

### Addendum (21:34, literature check)
- **Documented upstream.** Fabbri et al. (SummEval, TACL 2021; arXiv 2007.12626) report that the averaged expert and crowd scores have a Pearson correlation close to 0, and that crowd scores were similar across dimensions. The near-zero expert–crowd agreement is therefore a documented property of SummEval and must be cited.
- **Not documented.** We found no report of the identical-annotation pattern (five identical turker dicts in 50 % of items). It stays unverified against the upstream file.
- **Draft action (once R22-1 reports).**
  - §2.1 and §5 must state that SummEval's crowd columns are essentially uncorrelated with its experts (citing Fabbri et al.).
  - The budget results on SummEval must be described as diluting two expert ratings with five crowd ratings, not as "full data vs fewer ratings of one population".

### R22-1 results (2026-11-06 21:36; results/decode_decomp/summeval_*8_nodup_r22.json; 0 tracebacks)
| panel (793 items) | X_own [95 %] | G_own/X_own | G_own_net/X_own |
|---|---|---|---|
| coherence nodup | −0.00013 [−0.00030, +0.00003] | 0.005 [−0.046, 0.056] | −0.018 [−0.064, 0.029] |
| relevance nodup | −0.00003 [−0.00016, +0.00010] | 0.32 [−1.02, 1.67] | −0.03 [−0.20, 0.15] |
- **Frozen reading.** Coherence: the upper bound 5.6 % is < 24 %, so it stays in the contrast. Relevance: the upper bound 167 % is ≥ 24 %, so it is **removed from the contrast**.
- **The substantive result (beyond the frozen reading).** Without the duplicated items, SummEval shows **no detectable own-shape reproducibility**: X_own's point estimates are negative and their intervals cover 0.
  - The full-panel X_own (coherence 0.00038) comes from items whose five crowd annotations are identical. Those make the turker part of the two halves agree trivially.
  - With X_own ≈ 0, the ratios are not interpretable, even where the frozen rule passes.
- **Consequences for the paper:**
  1. SummEval stops being the example of "reproducible but not decodable". It joins POPQUORN and DICES-990: no detectable own-shape at a = 4. The clean ordinal example of a detectable but undecoded own-shape is DICES-350 at a = 40: X_own > 0, recovery 1 % [−9, 12].
  2. SummEval's plant calibration (R20-2, R21) was matched to an X_own inflated by duplicates. It stays reported as a calibration at that magnitude, but it no longer establishes informativeness for SummEval's real shape.
  3. SummEval's split-half reliability card and every SummEval budget or target result must carry the duplication and expert–crowd facts. A full-panel versus nodup re-computation of ρ and ρ_own is to be specified next.
  4. The ordinal–NLI contrast survives in direction, but its ordinal side is now "not reproducible (SummEval, POPQUORN, DICES-990) or reproducible yet not decoded (DICES-350; Dorn's signal is location-sized)".

## R22-2 (specified 21:36, before running): the SummEval reliability card on non-duplicated items
- **Runs.** rho_own.py and rho_exact.py (R = 10, B = 200, defaults) on summeval_coherence8_nodup and summeval_relevance8_nodup.
- **Reported.** ρ, ρ_own and A1^x next to the full-panel values, at every a computed.
- **Descriptive, no gate.** The card shows both versions. The text uses nodup values for any claim about reproducibility of SummEval's shape.
- **Also (descriptive).** The expert-only split-half on SummEval is impossible (3 raters, so b = 1 or 2 and X_own ≡ 0 or unmeasurable). This is stated as such.

### R22-2 results (2026-11-06 21:38; results/rho_exact/summeval_*8_nodup.json; a = 7, leave-one-out)
| panel | full: ρ [95 %] | nodup: ρ [95 %] | full A1^x | nodup A1^x |
|---|---|---|---|---|
| coherence | 0.35 [0.24, 0.48] | **0.10 [−0.13, 0.23]** | +0.0016 | +0.0032 |
| relevance | 0.40 [0.30, 0.54] | **0.05 [−0.19, 0.25]** | +0.0008 | +0.0031 |
- On non-duplicated items, the forecasting reliability of SummEval's shape is indistinguishable from 0. A1^x > 0 with an interval excluding 0 means the raw histogram forecasts a held-out rating worse than its exact mode and mean, now clearly so.
- The duplicates inflated ρ by about 0.25–0.35.
- rho_own.py is for dense panels only (assert m > 12). SummEval's X_own comes from R22-1, so the two tracebacks are expected and are not bugs.
- **Card.** SummEval is reported with both versions. Claims use nodup. The draft range "0.04–0.41 on eight panels" is unchanged in its endpoints (0.04 is not SummEval; the 0.41 endpoint is to be re-checked against the table in R22-T).

### Provenance check (21:39)
- The file name model_annotations.aligned.paired.scored.jsonl matches the official SummEval release naming: the aligned, paired file, plus metric scores (see the 04/19/2020 update in data/summeval/README.md). It was imported unchanged on 2026-10-25 (commit 73d6323).
- Upstream verification failed from this server: the Google Drive link returns 404 and the HF datasets-server timed out. **Still unverified.**
- Until verified, the text says "in the released file as distributed with the SummEval repository's annotation link". It does not say the duplication is a defect of the original crowd collection.

## R22-T (specified 23:31, before editing): SummEval non-duplicated rows in Table 1
- Table 1 (make_tables_v2.py) gains the rows "SummEval coh./rel. (non-dup.)", from results/rho_exact/summeval_*8_nodup.json (R22-2). The full-panel rows stay. Support is "--", because no donor-replacement run exists for nodup.
- In §1 (i), the range "0.04–0.41 … (intervals include 0 on four)" is re-checked. The minimum is CSC 0.038 / POPQUORN pol. 0.037 and the maximum is EmoBank 0.412. The nodup values (0.10, 0.05) fall inside the range, so the endpoints do not change. One parenthetical is added: on SummEval's non-duplicated items, ρ is 0.10 / 0.05 and both intervals include 0. The count "four" refers to the eight released panels and stays.
- No new computation.

### Provenance check, second attempt (23:33)
- GitHub Yale-LILY/SummEval issues: no issue mentions duplicated or identical crowd annotations (searched "duplicate", "identical", "turker", "crowd").
- Issue #41 ("Identifying individual annotators", closed): the first author answered that, *within a summary*, position i is the same person across the four dimensions. They did not say whether position i is the same person across summaries. This supports the treatment of the crowd columns as positions (§2.1 Population). It does not explain the duplication: five different workers giving identical four-dimension annotations on 50 % of the items would be a strong coincidence.
- HF mirrors: davidanugraha/SummEval (1,700 rows) and mteb/summeval carry only expert scores, not the turker lists, so they cannot verify the duplication. The remaining parquet mirrors were not read, because no parquet engine is installed in the venv.
- Status: still **unverified upstream**. The draft keeps "undocumented". The nodup sensitivity (R22-1/R22-2) is the remedy in either case.

## R22-T2 (specified 23:33, before editing): carry the ROUND22 reading into §1 (iii)/(v) and §3
- §1 (v): add one sentence after the SummEval LoRA budget result. SummEval's crowd ratings are nearly uncorrelated with the held-out experts, so these contrasts measure dilution of the expert ratings (R20-7, §5). This matches the abstract and §5, which were already changed.
- §3, donor-replacement audit: add one sentence. On SummEval and POPQUORN no own-shape is detectable (R22-1, R21), so the shape-replacement null is the expected outcome there and not independent evidence that judges ignore a learnable shape. The audit's discriminating case is ChaosNLI, where the same intervention costs Brier. Text only; no new numbers.

## R22-3 (specified 2026-11-07 00:36, before running): X_own-matched plant on DICES-350 at a = 40 (round-22 review, change 3)
DICES-350 at a = 40 is the only ordinal panel whose own-shape is detectable (item-cluster CLT) and not location-sized by construction. Its G_own/X_own 1 % [−9, 12] has no power calibration.
- **Runs.** decode_decomp.py on dices, a = 40, R = 10, B = 0, tag _r22. Plants γ ∈ {0, 0.1, 0.2, 0.3, 0.4}, draws s0–s4, on the fitted dices M2 model (as R21-7). One sequential CPU Slurm job.
- **Reference plant (as R21-7).** The smallest γ whose mean planted X_own ≥ the observed 4.9·10⁻⁵. If no γ in the grid reaches it, add γ 0.6 and 0.8 and label them as an extension.
- **Reading:**
  - 4–5 of 5 detected at the reference γ: DICES-350's 1 % is informative at its own magnitude.
  - Fewer than 4: it is not, and is reported as such.
- **Location-only baseline (descriptive, as R21-7).** Mean X_own and V_own over the γ0 draws, as fractions of the observed values (X_own 4.9·10⁻⁵, V_own 4.9·10⁻⁶).

## R22-T3 (specified 2026-11-07 00:36, before editing): carry ROUND22 through the draft (round-22 review)
Text and tables only. All numbers come from existing result files.
1. **§1 (ii) list (l. 18).** Apply R22-1's frozen reading: SummEval relevance leaves the ordinal list. Coherence stays, with its no-dup ratio 0.5 % [−4.6, 5.6] beside it and the note that the no-dup X_own is not detectable.
2. **l. 21.** Relabel the a = 4 ChaosNLI result as a check that the NLI fractions do not depend on a = 20. Say that no ordinal partner at a = 4 has a detectable own-shape. The net-fraction bound "at least 32 % on NLI" becomes "at a = 20".
3. **(ii) heading and abstract.** Reframe: no ordinal panel shows a robustly reproducible own-shape. It is undetectable on most; on DICES-350 it is detectable only within the observed rater pool; on Dorn it is location-sized. Where detectable, ≤ 16 % is decoded.
4. **l. 23/49.** "So the SummEval null is informative" becomes conditional on the full-panel magnitude, which ROUND22 attributes to duplication. The corrected-X_own sentence for SummEval is marked as not applicable to duplicated annotations.
5. **l. 61, l. 63, l. 65.** Small-panel count "half" becomes "four of eight (two on SummEval's non-duplicated items)". The SummEval residual sentence is replaced. λ̂ is attributed to the duplicates.
6. **Contribution (4) and guidance (l. 25, l. 75).** Remove the SummEval budget contrasts as budget evidence. Fix the frozen-head threshold to match Table 5: SummEval prefers 480×2, POPQUORN has 819 items, and HelpSteer2/OLMo-2 is the exception.
7. **§5 (l. 73).** "+0.020 on every fold" becomes "+0.014 to +0.025". Disclose that the R20-7 arms are compared across batches: the effects are 0.01–0.04, against rerun variation ≤ 0.0012. l. 83 is fixed accordingly.
8. **§2.1 population (l. 45), §7 (l. 83).** Add the duplication / r ≈ 0.04 / unverified-provenance limitation. Replace "SummEval's small unexplained residual".
9. **Abstract.** "Prospective LoRA blocks on POPQUORN" becomes "a prospective LoRA block". Header line 3 is updated.
10. **Deferred to R22-T4 (next step).** Table 2 rebuilt on CLT G_own/X_own with no-dup rows. Table 6 rebuilt with the prospective blocks. Plant detection recomputed with CLT, if the plant JSONs store it. Duplication notes in the Table 1/2 captions.

### R22-T3 applied (2026-11-07 00:38)
All 22 replacements are applied, covering items 1–9; item 10 is deferred to R22-T4. check_consistency: 11/11 OK, 0 unmatched. The abstract is 379 words.
Correction found while editing: §5 said experts2 was "0.040 better than full" on expert 1. compare.md gives −0.0415 against a7 (−0.0395 against a2). Changed to 0.042.
Not changed: the motivating example (l. 10, SummEval coherence). It is illustrative, not evidence. It will be replaced in the next draft pass.

## R22-T4 (specified 2026-11-07 00:38, before editing): tables
- **New table, tab_own.tex.** The own-shape decoding table, built by make_tables_v2.py from results/decode_decomp/*_r21.json and *_r22.json (plant files excluded). Each row has: panel, a/b, feature family, X_own [CLT 95 %], G_own/X_own [CLT 95 %], and the net fraction (G_own − G_own,perm)/X_own [CLT 95 %].
  - A ratio is shown only when X_own's interval excludes 0; otherwise the row reads "X_own n.s.". This is the same forbidden-statement rule as Table 2.
  - SummEval rows are labelled "full panel" and "non-dup."
  - This table, not Table 2, carries the §1 (ii) headline.
- **Table 2 caption.** Add: the percentile intervals are the round-20 bootstrap, and the cross-term-inclusive G/X is kept for comparison only. The SummEval rows include the duplicated annotations.
- **Table 1 caption.** Add a sentence on the duplicated crowd annotations, pointing to the non-dup. rows.
- **Table 6 (LoRA).** Rebuilt in a separate step (R22-T5), so that it leads with the prospective blocks.

## R22-T5 (specified 2026-11-07 00:39, before editing): LoRA budget table leads with the prospective blocks
tab_budget.tex (Table 6 in the draft) is rebuilt in this order:
1. POPQUORN prospective (R20-4, lora_budget_r20_pq), the clean budget case.
2. SummEval prospective, labelled "expert dilution, §5": Qwen2.5 R19-9 (lora_budget_r19), OLMo-2 R20-3 (lora_budget_r20_olmo), and the single-batch reruns R20-5b/c (lora_budget_r20_rerun) and R20-6 (lora_budget_r206_olmo).
3. The earlier shared-assignment blocks (lora_budget_v2, lora_budget_olmo), labelled "shared assignment".

No numbers change. The rows are read from the existing summary JSONs. The §5 paragraph order (N14) is left for the next draft pass.

### R22-3 results (2026-11-07 00:50; 25 runs, 0 tracebacks; results/decode_decomp/dices_r22_plant*_s*.json)
| γ | mean X_own | mean V_own | detected (CLT lower bound of G_own > 0) | G_own/X_own per draw |
|---|---|---|---|---|
| 0 | −1.3e−5 | 4.7e−7 | 0/5 | 0.03, −0.56, 0.22, 0.10, 0.23 |
| 0.1 | −0.7e−5 | 5.7e−7 | 0/5 | 0.09, −0.28, −0.71, −0.04, 0.48 |
| 0.2 | 0.5e−5 | 2.7e−6 | 0/5 | 0.05, 0.04, 1.19, −0.07, −0.02 |
| 0.3 | 3.0e−5 | 8.8e−6 | 2/5 | 0.47, 0.08, 0.26, 0.19, 0.11 |
| **0.4** | **5.5e−5** | 2.2e−5 | **5/5** | 0.32, 0.28, 0.23, 0.33, 0.15 |

- The reference γ is **0.4**: it is the smallest γ whose mean planted X_own (5.5e−5) is at least the observed 4.9e−5.
- **Frozen reading: 5 of 5 detected, so DICES-350's G_own/X_own of 1 % [−9, 12] is informative at its own magnitude.** A planted text-predictable shape of the observed size is recovered at 15–33 %.
- Location-only baseline (γ 0), descriptive:
  - X_own is −1.3e−5, i.e. −27 % of the observed value. Location and thresholds alone do *not* produce DICES-350's own-shape, unlike Dorn (R21-7: about 95 % of V_own).
  - V_own is 4.7e−7, about 10 % of the observed 4.9e−6.
- Implication: DICES-350 at 40 raters is the one ordinal panel where a reproducible own-shape beyond location is detected (within the observed rater pool), power-calibrated, and *not* decoded. It now serves as the clean ordinal partner of the NLI contrast, at a = 40.

## R22-4 (specified 2026-11-07 01:31, before running): plant detections recounted with CLT intervals (review N1 / round-22 MEDIUM)
The SummEval and POPQUORN plant counts in the draft (R20-2/R20-2a) use the percentile bootstrap of G_own, which R21-1 abandoned for the headline. The JSONs of those runs (B = 200) store no CLT.
- **Runs.** decode_decomp.py, a = 4, R = 10, B = 0 (CLT only), tag _r22c, same plant seeds s0–s4.
  - summeval_coherence8 at γ ∈ {0.3, 0.6, 0.8, 1.0};
  - popquorn_off8 at γ ∈ {0.3, 0.6}.
  - γ 0 is already available with CLT (_r21, 0/5 detected on both).
  - Two sequential CPU jobs.
- **Reported.** Detections per γ under the CLT rule (lower bound of G_own > 0) next to the percentile counts. The point estimates (X_own, G_own/X_own) must match the earlier runs exactly; this is the pipeline check.
- **Frozen reading.** The CLT counts replace the percentile counts in the draft, whichever way they go. The reference-γ rule is unchanged (X_own scale; SummEval's full-panel reference is moot under ROUND22 and is reported for completeness).

## R22-T6 (specified 2026-11-07 01:32, before editing): §5 order (round-21 N14)
The sentences of the §5 LoRA-budget paragraph are reordered, with no new numbers:
1. POPQUORN, the clean budget case: the same-batch block, the prospective block R20-4, and "two ratings still cost".
2. The SummEval reading note.
3. The SummEval blocks, as before.
4. The cross-block summary, OLMo shared-assignment, evaluator dependence, and the batch and literature notes.

Only two wordings change: "re-run in the same way" becomes an explicit description, and "below" in the reading note points to the SummEval blocks that now follow it.

### R22-4 results (2026-11-07 02:31; 30 runs, 0 tracebacks)
Pipeline check: the point estimates (X, X_own, G, G_own) match the earlier B = 200 runs to ≤ 3·10⁻¹⁹.

| panel | γ | mean X_own | detected, percentile (old) | detected, CLT (new) | G_own/X_own range |
|---|---|---|---|---|---|
| SummEval coh. | 0 | −0.00009 | 0/5 | 0/5 (_r21) | — |
| SummEval coh. | 0.3 | 0.00017 | 4/5 | **5/5** | 0.16–0.55 |
| SummEval coh. | 0.6 | 0.00041 | 5/5 | 5/5 | 0.38–0.56 |
| SummEval coh. | 0.8 | 0.00049 | 5/5 | 5/5 | 0.33–0.50 |
| SummEval coh. | 1.0 | 0.00046 | 5/5 | 5/5 | 0.31–0.57 |
| POPQUORN off. | 0 | ≈0 | 0/5 | 0/5 (_r21) | — |
| POPQUORN off. | 0.3 | 0.00009 | 0/5 | **2/5** | −0.02–0.34 |
| POPQUORN off. | 0.6 | 0.00031 | 4/5 | **5/5** | 0.06–0.38 |

- CLT detects slightly more often than the percentile bootstrap. That is consistent with R21-1, where the percentile intervals were off-centre.
- Frozen readings: SummEval stays "informative at the full-panel magnitude", which is moot under ROUND22. The POPQUORN reference plant (γ 0.3) is detected in 2 of 5, which is below 4, so the POPQUORN null **stays uninformative**. No reading changes.
- Draft: the counts are replaced with the CLT counts (4→5, 4→5, 0→2 on POPQUORN γ 0.3).

## R22-5 (specified 2026-11-07 02:31, before running): DICES-350 at a = 40 on the other two feature families
DICES-350 at a = 40 is now the power-calibrated ordinal case (R22-3), but only Qwen2.5 features were decoded there; at a = 20, all three families were.
- **Runs.** decode_decomp.py, dices, a = 40, R = 10, B = 0, with --feat_model Qwen3-8B (tag _a40_qwen3_r22) and --feat_model OLMo-2-1124-7B-Instruct (tag _a40_olmo_r22). One CPU job.
- **Reported.** G_own/X_own and the net fraction, each with CLT 95 % intervals. X_own is the same across families, because it is learner-free.
- **Reading (descriptive).** The draft's "three LLM families recover 1 %" is kept only if both upper bounds stay below the plant recovery range (15–33 %). If either upper bound reaches 15 %, the abstract names the family-specific values instead.

### R22-5 results (2026-11-07 02:33; 2 runs, 0 tracebacks)
X_own is 4.90e−5 on all three families (learner-free, identical as expected).

| features | G_own/X_own [CLT 95 %] | net [CLT 95 %] |
|---|---|---|
| Qwen2.5 (R21) | +1.3 % [−8.8, +11.4] | +15.0 % [+2.6, +27.4] |
| Qwen3-8B | −0.6 % [−8.0, +6.8] | +9.5 % [−0.3, +19.3] |
| OLMo-2-7B | −0.0 % [−7.2, +7.2] | +6.8 % [−1.9, +15.6] |

- Reading: all three upper bounds (≤ 11.4 %) are below the plant recovery range of 15–33 %. The abstract keeps the three-family statement, with the range −1 to 1 % and upper bounds ≤ 12 % (rounded outward).

## R22-6 (specified 2026-11-07 11:31, before running): a second plant construction on DICES-350 at a = 40 (v3 self-review, limitation "one plant construction")
DICES-350's power calibration (R22-3) uses one construction: item log-dispersion linear in one feature direction. A reviewer can object that a judge-relevant ordinal shape might take another form. The obvious alternative for DICES, a dataset built to study demographic disagreement on safety, is *text-predictable polarisation*: two fixed rater groups move in opposite directions on items whose text lies along one feature direction.
- **Construction (--plant_kind polar).** Same fitted DICES M2 model (theta, rater cut-points, median σ), same random 64-dimensional feature direction sdir (standardised) per seed.
  - Each of the M rater columns gets a fixed sign g_r = ±1, exactly half each, drawn per seed.
  - Latent: y*_ir = θ_i + σ_med·ε_ir + γ·sdir_i·g_r.
  - The plant is a rater-group × item interaction predictable from text. It leaves the item mean nearly unchanged in expectation and changes the spread and bimodality.
  - The default construction (dispersion) is unchanged; --plant_kind defaults to disp.
- **Runs.** decode_decomp.py, dices, a = 40, R = 10, B = 0, tag _r22p.
  - γ ∈ {0.1, 0.2, 0.3, 0.4, 0.6}, draws s0–s4; 25 runs in one sequential CPU Slurm job.
  - γ = 0 is identical to the R22-3 γ = 0 location-only simulation (no plant term) and is not rerun.
- **Reference plant.** As R22-3: the smallest γ whose mean planted X_own ≥ the observed 4.9·10⁻⁵. If none reaches it, add γ 0.8 and 1.0, labelled as an extension.
- **Reading (frozen):**
  - Detected (CLT lower bound of G_own > 0) in 4–5 of 5 draws at the reference γ: DICES-350's −1 to 1 % is informative against this second construction too.
  - The paper then states that the clean-case power holds for two constructions, with the recovery range for each.
  - Fewer than 4 of 5: the power claim stays restricted to the dispersion construction, and the paper says the polarisation construction was not detected at the observed magnitude.
- **Not changed.** No observed-data estimate is recomputed. The draft numbers for R22-3 and R22-5 stay as they are.

### R22-6 amendment (11:33, after the smoke run, before the main run; post hoc with respect to the γ grid)
- **What the smoke run showed.**
  - The disp path reproduces R22-3 γ 0.4 s0 exactly: all 42 numeric fields are identical except run time.
  - polar at γ 0.4 s0 gives X_own −0.8e−5. It does give X +6e−5, but X_cross is +7e−5: random half-splits mix the two groups unequally, so a polarisation of this size shows up as a location shift between halves rather than as own-shape.
- **Why the grid was too weak.** The fitted DICES σ_med is 0.98 on a 3-level scale, so ±0.4 does not separate the groups.
- **New grid.** γ ∈ {0.6, 1.0, 1.5, 2.0, 3.0} × s0–s4, replacing {0.1–0.6}. Reference rule and reading are unchanged.
- **Additional reported quantity (descriptive).** X_cross/X at the reference γ, to show how much of the polarisation lands in the cross term.
- **If no γ ≤ 3.0 reaches the observed X_own:** report that this construction cannot produce an own-shape of DICES-350's magnitude at plausible strengths. The power claim then stays dispersion-only.

### R22-6 results (11:48; 25 runs, 0 tracebacks; results/decode_decomp/dices_r22p_polar*_s*.json)
| γ | mean X_own | mean X | X_cross/X | detected (CLT lower bound of G_own > 0) | G_own/X_own per draw |
|---|---|---|---|---|---|
| 0.6 | −0.3e−5 | 6.0e−5 | 1.05 | 0/5 | 0.30, 0.12, −0.24, −0.79, 0.43 |
| 1.0 | 4.4e−5 | 10.5e−5 | 0.58 | 1/5 | 0.02, 0.11, 0.10, 0.22, 0.01 |
| **1.5** | **6.3e−5** | 12.4e−5 | 0.49 | **3/5** | 0.20, 0.22, 0.11, 0.17, 0.01 |
| 2.0 | 7.1e−5 | 13.5e−5 | 0.48 | 2/5 | 0.10, 0.18, 0.01, 0.18, −0.04 |
| 3.0 | 6.3e−5 | 11.9e−5 | 0.47 | 1/5 | 0.19, 0.18, 0.04, 0.09, −0.01 |

- **Reference γ: 1.5.** It is the smallest γ whose mean X_own (6.3e−5) is at least the observed 4.9e−5.
- **Frozen reading: 3 of 5 detected, fewer than 4.** DICES-350's −1 to 1 % is *not* shown to be informative against the polarisation construction. The power claim stays restricted to the dispersion construction (R22-3: 5 of 5, 15–33 %).
- **Descriptive.**
  - At the reference γ the decoder recovers 1–22 % of the planted own-shape (point estimates). The observed −1 to 1 % lies at the bottom of that range, so it neither excludes nor matches this construction.
  - About half of the polarisation's X lands in the cross term (X_cross/X 0.47–0.58 for γ ≥ 1), and X_own saturates near 6–7e−5 for γ ≥ 1.5.
  - The decoder has less power for a shape whose own part is small relative to its location part.
- **Consequence for the paper.**
  - v3 §7 "Plant scope" and v2 §7 name the second construction and its result.
  - The DICES-350 sentence in v3 §4 is already scoped to "a planted shape of this size and construction"; v3 §1 (ii) and the abstract say "a planted text-predictable shape of the same magnitude", which is now made specific to the dispersion construction in §4 and §7 (the abstract has no room).
