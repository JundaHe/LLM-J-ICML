## Blunt verdict

Yes—but not by adding more ablations. C–F mostly make the existing audit broader or safer; they do not fundamentally change what the paper is. The credible route to ≥7.5 is A+B, reframed as separating finite-annotation information from learner recovery.

My ranking is **A+B/G ≫ F > C > D > E**.

| Direction | Reviewer assessment |
|---|---|
| **A. Annotation-side predictive value** | **Novelty gain: medium–high. Headline: yes.** This directly answers the fatal objection: “perhaps the learner simply cannot exploit residual shape.” A clean independent-panel contrast would turn either outcome into a result: residual shape is not stable at observed \(m\), or stable information exists but judges fail to transmit it. Cost: low; repeated annotation splits and bootstrap on CPU. Collision risk: medium—[Homan et al.](https://aclanthology.org/2022.nlperspectives-1.8/) treat annotator distributions as samples, [NUTMEG](https://aclanthology.org/2025.emnlp-main.144/) separates systematic disagreement from noise, and [Kohli](https://arxiv.org/abs/2605.29797) studies annotation saturation—but none appears to combine an annotation-side statistic-preserving contrast with the corresponding learned-judge intervention. Do not call the simple plug-in comparison an “oracle.” |
| **B. Finite-rater theory** | **Gain: high jointly with A; low alone. Headline: yes.** The basic variance decomposition is textbook, so “we derived \(1/m\) sampling noise” will not impress. What could impress is an estimable RPS decomposition, predicted break-even \(m\), and out-of-sample validation across ordinal panels and ChaosNLI. Cost: medium CPU/statistical work, roughly 1–2 weeks. Collision risk: medium from Kohli, annotator-sampling work, and general noisy-label theory. Its novelty is the connection to statistic-conditioned residual shape and judge recovery, not the algebra. |
| **C. Moment ladder** | **Gain: low–medium. Headline: usually no.** A reviewer will see a larger ablation grid with unequal intervention doses. Apparent “saturation” may merely reflect projections becoming nearly identical to the original. With \(K=5\), normalization plus three raw moments leaves only one degree of freedom; with \(K=3\), mean and variance already identify the distribution. Cost: modest for heads, expensive for replicated LoRA arms. Moment-matching and ordinal LDL make collision risk medium. Kill unless A/B reveals substantial stable variance specifically attributable to dispersion. |
| **D. Annotation budget** | **Gain: low. Headline: risky.** The proposed conclusion does not follow from mode+mean sufficiency: those statistics themselves become noisy with few raters. This space is crowded by [Zhang et al.](https://aclanthology.org/2021.emnlp-main.601/), Kohli, and [Pandita et al.](https://arxiv.org/abs/2508.03663). Cost is medium for head grids and prohibitive for convincing LoRA grids. At most, make break-even \(m\) a consequence of B—not a second paper inside this one. |
| **E. Zero-shot judges** | **Gain: low. Headline: no. Kill it.** Exact-neighbour work already evaluates LLM distributions against human disagreement: *Distributional LLM-as-a-Judge*, [Can LLMs Capture Human Annotator Disagreements?](https://arxiv.org/abs/2506.19467), and [Wang et al.](https://arxiv.org/abs/2503.03064). A 7B zero-shot judge also creates prompt, verbalisation, and calibration confounds. Cost is manageable; reviewer enthusiasm will not be. |
| **F. MDE/injection** | **Gain: low novelty, medium credibility. Headline: no.** Worth doing selectively, especially because the current positive control rests on Buse–Weimer. CPU cost is low for heads, GPU cost high for LoRA. But an injection establishes power only for that injected direction in residual space. It cannot support “all real effects are below \(\delta\).” Call it an assay sensitivity curve, not a universal MDE. |
| **G. My addition: split-panel residual reliability** | **Gain: medium–high as the estimator inside A/B.** Estimate the between-item covariance of residual shape from independent rater panels, correcting the multinomial within-panel variance. Then ask whether audit effects track stable residual variance × intervention dose across panels. Cost: low–medium CPU. The ingredients are classical reliability theory, but the statistic-conditioned, score-specific application is a plausible differentiator. |

## Best plan

1. **Do A/G first.** For repeated disjoint annotation splits, compare direct held-out-panel RPS for:

   - the original \(m\)-rater histogram;
   - the exact donor-replaced target used by the audit;
   - a cross-fitted statistic-only predictor \(q_T\), where \(T=(\text{mode},\text{mean})\).

   Trace \(m\) on ChaosNLI and the dense ordinal panels; use leave-one-rater-out where identities persist. Report the annotation-side gap and learned-judge gap side by side, with joint intervals—not a ratio by default.

2. **Add B only after the empirical curves are stable.** Derive the RPS signal/noise decomposition, estimate its terms with shrinkage or a hierarchical multinomial model, predict break-even \(m\), then validate on held-out annotation counts. Finish the POPQUORN LoRA block in parallel, but add no further LoRA arms.

This makes **7.5 plausible**, provided the annotation-side curves replicate and the theory predicts them. A alone probably moves the paper only to about 7.0.

**Proposed title:** *When Do Disagreement Histograms Teach a Judge? Separating Finite-Rater Signal from Learner Recovery.*

**Contribution:** “We introduce a dose-certified finite-rater decomposition that measures whether disagreement shape beyond mode and mean predicts an independent rater panel, and then quantifies whether judge training transmits that stable information.”

## Explicit scope traps

Do not add zero-shot judges, a full moment ladder, or a large annotation-budget grid. Do not claim label topology caused the ordinal–nominal difference. Do not equate an unstable empirical residual with absence of latent human heterogeneity. Above all, do not report “percent recoverable” when the denominator crosses zero.

## Mathematical sanity check

Your proposed **“pmmx of itself” is exactly the original histogram**: it is already feasible and has KL zero to itself. That contrast is guaranteed to be zero, aside from numerical error.

Instead, compare the original histogram with either the actual donor-projected target or a separately defined \(T\)-only forecast.

For latent distribution \(p_i\), cumulative operator \(C\), and RPS,

\[
R(q\mid p_i)=\text{const}(p_i)+\|C(q-p_i)\|^2.
\]

If \(q_T=E[p_i\mid T_i]\), the population value of residual information is

\[
\Delta_\infty=E\|C(p_i-q_T)\|^2\ge 0.
\]

An \(m\)-sample histogram adds multinomial estimation error \(v/m\), giving the idealized break-even \(m^\star=v/\Delta_\infty\). But that expression assumes \(T_i\) is known and fixed. Estimating mode and mean from the same \(m\) ratings adds classification, covariance, and selection terms; those must be handled by resampling or the hierarchical model.

Finally, the direct histogram-versus-donor gap is an **annotation-side predictive contrast**, not necessarily an upper bound on model performance. A genuine recoverable-information fraction requires cross-fitted Bayes predictors \(E[Y\mid H_m]\) and \(E[Y\mid T_m]\), a positive denominator, and aligned interventions and scores.