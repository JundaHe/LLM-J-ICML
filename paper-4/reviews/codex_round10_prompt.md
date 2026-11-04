Round 10 (verification). Below are (A) your round-9 review of this paper and (B) the revised typeset text (pdftotext -layout of the rebuilt PDF). Please:
1. For each item of the round-9 review, state FIXED / PARTLY / NOT FIXED, quoting the revised text and giving its page.
2. List any NEW inconsistency, overclaim or typesetting defect introduced by the revision (e.g. table numbering vs references, captions that contradict body text, citations rendering wrongly). Quote and give the page.
3. Say in one paragraph whether the main text (pages 1-8) is ready for submission apart from the 2027 template swap, and what single change would most improve it.
Be concise.

=== (A) ROUND-9 REVIEW ===
The main text is eight pages. The central CA results agree across the abstract, §6 and Table 1, and the S13-3 conclusion is now appropriately cautious. I would still make a final correction pass before submission.

I found two clear numerical-label errors and several comparisons needing clarification:

| Page | Offending text | Correction or clarification |
|---|---|---|
| **6, §5.9** | “content adaptation … is inconclusive at the pre-set **k = 20** (+0.40 … and −0.19 …)” | Appendix B, **p.14**, identifies the Dorn −0.19 result as **k = 10**. State the budgets separately: Buse–Weimer k = 20; Dorn k = 10. |
| **5, §5.7** | “conflict in only **4.0 % of held-out comparisons**” | Appendix B, **p.13**, says **4.0% of held-out non-tie comparisons**, or **3.5% of all annotations**. Add “non-tie.” Also identify the accompanying **+0.10** result as using **all training ratings**; the k = 20 result is +0.03 in the p.14 table. |
| **3, Protocol** | “**5 folds; in each**, 20 % of raters … and 20 % of prompt groups are held out” | Appendix C, **p.17**, says “**5 rater folds … × 5 prompt-group folds**”; native PRISM on **p.6** also says 5 × 5. Clarify whether the design uses five paired splits or all 25 crossed combinations, and whether this differs by experiment. |
| **7, §6** | “realised gains are far below model-implied ones (**+1.9 points**, Gaussian event-level simulation)” | Appendix F, **p.18**, attaches +1.9 to the **c = 1** learner, whose observed gain is +0.13. The subsequent validated TRV uses c = 0.125–0.25. Label the +1.9 benchmark’s configuration explicitly; the current placement invites comparison with the final validated procedures. |

A minor arithmetic query: **p.4**, “the offsets close **56 %** of the gap.” The printed likelihood reference points give \(0.099/0.179=55.3\%\), whereas the tabulated +0.100 gain gives 55.9%. This can be rounding, but derive the percentage consistently from unrounded values.

I would **not** flag the LoRA **+0.092 versus +0.100** difference: p.5 explicitly explains adaptation draw 0 versus five draws. Likewise, differences between directly reported contrasts and subtraction of rounded table entries need not be errors.

The remaining claim problems are these:

- **Categorical claims about ranking remain too strong.** Figure 1’s caption, **p.3**, says offsets reshape strength, “**not which side**”; **p.4** says the ceiling result confirms that “**text-independent offsets cannot carry ranking**.” Elsewhere the paper reports a +0.5-point direction change and a +1.3-point in-sample improvement. Replace these categorical statements with “primarily affect intensity and ties, with small observed direction changes.” Exact cancellation is established for symmetric offsets on **binary labels at a fixed head**, not arbitrary graded predictions.

- **The VPL-plus-offset result is not an established tie.** On **p.5**, “**tie with the style model on likelihood (−0.004 [−0.014, +0.005])**” conflicts with Appendix E, **p.17**, which explicitly says its non-inferiority criterion was not met. The discussion’s “**recovers the whole gain**” on **p.8** is consequently too definite. Suggested wording: “recovers most of the point-estimate gain; the remaining difference is uncertain, and non-inferiority was not established.”

- **Positive-control statements need configuration-specific language.** On **p.5**, “**VPL and PAL-B … recover less than half a point of +10**” is true for the compressed-feature runs. The **p.6** table gives full-feature PAL-B **+1.95 [+1.16, +2.74]**. Add “with PCA-256 features.” Conversely, **p.8**, “**compressed features make the published methods weaker detectors than full features**,” is too broad: Appendix B, **p.14**, reports that full-feature VPL collapses and has own−other exactly zero. The demonstrated improvement from full features is for PAL-B.

- **Prefer an observed detection result to a universal power statement.** On **p.5**, “**No method has power at the pre-specified strengths**” should read “No evaluated method met the pre-specified detection criterion on those panels.” This preserves the actual result without implying a fully estimated power curve.

- **Some appendix claims still exceed the cleaned-up main text.** On **p.14**, matching the latent’s gain with offsets is followed by “**so it reflects scale use … not content**.” Equal aggregate gains do not identify the latent’s mechanism. On **p.15**, “**what fails is finding the dimension, not the number of ratings**,” and **p.19**, “**§5.6 locates the failure**,” are also too categorical. The controls demonstrate recoverability when specified features are supplied and implicate representation or inductive bias in the tested settings.

- **The decomposition needs an explicit scope qualifier.** On **p.2**, “**the predictable structure is therefore mostly rater-side scale use**” generalises beyond the stated comparison of rater thresholds with item dispersion. Neither that comparison nor marginal distribution-shape reliability directly measures all rater-by-content interactions. “Within this decomposition” would substantially improve the claim.

- **One sentence reverses the stated decision rule.** On **p.6**, LoRe “**under the same pre-set rule, also fails it**.” Its upper bounds, −0.4 points and +0.2 for the regularised version, satisfy the preceding ranking-null criterion of being below +1 point. Write “also meets the ranking-null criterion” or “also fails to improve choice accuracy.”

For the two specifically sensitive results:

- **S13-3 is now reported correctly.** On **p.7**, accuracy is positive under user clustering, likelihood is inconclusive, and the prespecified joint criterion fails. Table 1 agrees. The text also correctly avoids inferring unstable preferences or universally unsuccessful transport.
- **The TRV-versus-isotropic conclusion is appropriately restrained.** The reported CA contrasts, −0.17 on turn 1 and +0.07 on turn 2, do not establish TRV superiority. The remaining issue is the configuration attached to the +1.9 simulation benchmark, described above.

The visible presentation defects are:

- **Swapped figure references, p.3:** §4 says “**Figure 2 illustrates the effect of the offsets**,” which should be **Figure 1**. §5.1 says “**Figure 1 shows the gain … as a function of k**,” which should be **Figure 2**.
- **Detached, uncaptioned tables:** the numerical tables on **pp.4–6** lack identifying captions/numbers. In particular, §5.2 on p.4 is separated from its table at the top of p.5. Compact captions would make these much easier to associate with their experiments.
- **Apparently clipped final table, p.20:** the last header ends “**rank-2 subsp**,” and the last cell ends “**+0.17 [−0.17, +0.51] (tuned**.” Check the rendered right edge and resize or reflow the table. It also occupies an otherwise largely empty page.
- **Missing bibliographic attribution:** “**WIMHF’s protocol**” on **p.7**, and “**WIMHF’s discovered feature**” on **p.8**, have no expansion or bibliography entry. **Buse–Weimer and Dorn**, introduced on **p.6**, likewise lack formal dataset/study citations in the supplied references.
- **Undefined acronym:** **TRV** appears in Table 1 on **p.8** without an explicit expansion in the main text.
- **Math requiring visual inspection:** “**RˆK**” on **p.3**, the figure-axis strings “**A B … B A**” on **p.3**, identical extracted upper/lower “**0.1**” ticks on **p.4**, and “**ρ < 12**” on **p.17**. These may be extraction artefacts rather than PDF defects; the last should represent \(\rho<1/2\).

I see no literal `??` references, missing numbered section headings, or visibly unresolved author–year citations. Normal two-column extraction order and line-wrapped bibliography URLs should not be treated as defects.

My three highest-priority reviewer requests, ranked, would be:

| Rank | Requested change | Fixable without new experiments? |
|---|---|---|
| **1** | **Keep method conclusions within the demonstrated sensitivity of the evaluated implementations.** Carry the compressed/full-feature distinctions and injected-family limitations through the appendices. | **Yes**, by narrowing the claims. General conclusions about published methods or exclusion of meaningful content preferences would require stronger implementation validation and controls. |
| **2** | **Align interpretation with the actual estimands and decision rules.** Remove categorical ranking/mechanism claims and the unsupported hybrid “tie”; qualify the decomposition’s scope. | **Yes.** The necessary estimates and failed criteria are already reported. |
| **3** | **Complete the reproducibility and presentation audit.** Add a Stage-13 methods block—Appendix F currently covers Stages 8, 11 and 12—resolve the fold design, correct budgets/denominators, and repair references and tables. | **Yes**, using existing code, protocols and logs, followed by a fresh PDF inspection. |
=== (B) REVISED PAPER TEXT ===
000
001
002                  What Do Gains in Personalised Reward Modelling Measure?
003
004
005
006                                                       Anonymous Authors1
007
008
009                            Abstract                                    1. Introduction
010
011                                                                        Reward models and LLM judges are trained on human
           Personalisation gains can reflect improved rat-                 ratings that disagree, and a recent line of work treats this
012        ing calibration, predictable differences between
013                                                                        disagreement as signal: distributional preference learning
           users, or better choices than a population model.               (Siththaranjan et al., 2024), jury learning (Gordon et al.,
014        We evaluate these separately using held-out
015                                                                        2022) and personalised reward models that infer a per-user
           users and prompts, few-shot adaptation, popu-                   latent from a few examples (Poddar et al., 2024; Chen et al.,
016        lation baselines and exchanged-parameter con-
017                                                                        2025), within the pluralistic-alignment agenda (Sorensen
           trols. Across three preference and safety datasets,             et al., 2024).
018        text-independent rater offsets improve graded-
019        label log-likelihood by 0.08–0.10 nats per rat-                 What these models learn about a person is rarely tested
020        ing from twenty ratings, while our compressed-                  directly. Evaluations typically use synthetic users whose
021        feature reimplementations of published methods                  preferences differ by construction, binary preference labels,
022        show small direction or choice gains on Multi-                  or users seen in training. We ask a simple question under
023        Pref and native PRISM choices. On Commu-                        a common protocol on real raters: given k ratings from
024        nity Alignment, twenty support choices from                     someone the model has never seen, how much better
025        other prompts predict which of two disagreeing                  can it predict their other ratings — in particular, which
026        users selected which response on identical four-                response they prefer — and what is it that it learns?
027        response items: assignment accuracy is 62.2 %                   We find that three outcomes usually reported together come
028        [58.6, 65.6], against 50 % chance. A predictor                  apart: the largest few-shot gains on graded ratings are cap-
029        using response positions alone is also informa-                 tured by text-independent scale-use offsets; users’ choices
030        tive, and we do not separate content from posi-                 among identical alternatives are predictable from their other
031        tion. On the shared-item panel, isotropic adap-                 choices; and improvements in choice over a competent pop-
032        tation gains 0.70 pairwise accuracy points over                 ulation model are small, dataset-dependent and sensitive to
033        the population model, although the user-by-item                 how that population model is trained. Semi-synthetic con-
034        interval includes zero; log-likelihood improves                 trols characterise which injected content-preference families
035        under both bootstrap analyses. The frozen pro-                  the evaluated methods recover.
036        cedure does not establish benefit on MultiPref,
037                                                                        Measurement theory suggests a candidate answer that re-
           and frozen first-turn deviations improve accu-                  ward modelling largely ignores: raters differ in how they
038        racy on users’ later, disjoint conversations un-
039                                                                        use the response scale — some say “clearly better” where
           der user clustering but do not meet the prespeci-               others say “slightly better”, some rarely call a tie, some
040        fied joint accuracy-and-likelihood criterion over a
041                                                                        are harsher across the board (Linacre, 1989; Baumgart-
           history-conditioned population model. Changing                  ner & Steenkamp, 2001). Such response styles are text-
042        the population-training procedure shifts measured
043                                                                        independent, cheap to estimate, and invisible to models that
           gains by about 0.6 points. These findings mo-                   condition only on content or demographics. We make them
044        tivate separate evaluations of rating calibration,
045                                                                        a reference point for calibration. On two-sided preference
           user-associated choice predictability and predic-               scales, symmetric offsets mainly model intensity and ties
046        tive benefit over a population baseline.
047                                                                        and cancel exactly for binary A/B labels at a fixed text head;
048                                                                        unrestricted offsets can also change predicted decisions.
049     1                                                                  Likelihood gains alone therefore do not establish content-
          Anonymous Institution, Anonymous City, Anonymous Region,
050   Anonymous Country. Correspondence to: Anonymous Author               dependent personalisation, and content adaptation should
051   <anon.email@domain.com>.                                             be evaluated with rater offsets retained.
052                                                                        Contributions. (1) Graded-rating gains can be scale use.
      Preliminary work. Under review by the International Conference
053   on Machine Learning (ICML). Do not distribute.                       Under a new-rater protocol (held-out raters and prompts,
054
                                                                       1
                                        What Do Gains in Personalised Reward Modelling Measure?

055   k-shot adaptation, population and exchanged-parameter con-             a decoder on value profiles of held-out raters (Sorensen
056   trols), a few text-independent rater offsets capture the largest       et al., 2025). Benchmarks often simulate users (Castricato
057   demonstrated few-shot gains on three preference and safety             et al., 2025; Zollo et al., 2025); real multi-rater data with
058   datasets and two code-readability studies; in their symmetric          diverse candidates are emerging (Zhang et al., 2026). VPL’s
059   form they chiefly improve graded-label likelihood, change              latent can collapse under sparse data (Kim & Kim, 2026),
060   direction on graded MultiPref only slightly, and cancel ex-            and methods differ widely in a multi-faceted comparison
061   actly under binary labels (§4–5). (2) User differences                 (Dong et al., 2025). Rater groups use safety severity scales
062   need their own test — ideally on identical items. On                   differently (Mishra et al., 2026); demographics are often
063   Community Alignment, where many users judged the same                  weak predictors (Orlikowski et al., 2023). Measurement
064   prompt with the same four responses, support histories pre-            theory and annotator models. Rater severity and scale
065   dict which user chooses which response among identical                 use are standard facets of many-facet Rasch measurement
066   alternatives (62 % assignment accuracy between disagree-               (Linacre, 1989; Eckes, 2011) and response styles a classical
067   ing users against 50 %); attribute-derived scores remain               survey topic (Baumgartner & Steenkamp, 2001); user and
068   predictive when attributes and response positions are fitted           item biases carry much of the gain in collaborative filtering
069   jointly, and a position-only predictor is also informative (§6).       (Koren et al., 2009), user-specific ordinal thresholds predict
070   (3) Beneficial personalisation needs a competent popula-               personal rating distributions (Koren & Sill, 2011), and an-
071   tion baseline. Own-versus-other contrasts do not measure               notator models estimate rater-specific labelling behaviour
072   benefit; gains over the population model are small (+0.3 to            (Dawid & Skene, 1979; Raykar et al., 2010; Hovy et al.,
073   +0.7 choice points where established), not established on              2013; Deng et al., 2023; Plank, 2022; Uma et al., 2021).
074   MultiPref, and the measured gain changes by ˜0.6 points                Our offsets are of this kind and are not new; what is new
075   with the population-training procedure alone (§6). Semi-               is testing personalised reward models against them on new
076   synthetic positive controls characterise the evaluated learn-          raters and asking what these models could detect.
077   ers’ recovery of specified injected preference families (§5.6);
078   a screened attribute learner and the covariance-calibrated             3. Data, and where the predictable structure
079   procedure are reported as supporting tools (Appendix G,
080   F). Protocols, amendments and failed hypotheses are in
                                                                                sits
081   Appendices A, B, E and F.                                              Data. MultiPref (Miranda et al., 2025; 10,461 comparisons;
082                                                                          4 ratings each by 2 crowd and 2 expert raters; 227 persistent
083   2. Related work                                                        raters; 5 ordered levels A-clearly . . . B-clearly). PRISM
084                                                                          (Kirk et al., 2024; 68,371 responses each rated 1–100 by
085   Pluralistic and distributional reward models. Distri-                  one of 1,396 users; binned to 5 fixed levels). DICES-350
086   butional preference learning (Siththaranjan et al., 2024),             (Aroyo et al., 2023; 350 conversations fully crossed with
087   diverging-preference detection (Zhang et al., 2025), PRISM             104 quality-checked raters; safe / unsure / unsafe).
088   (Kirk et al., 2024), MultiPref (Miranda et al., 2025) and
089   DICES (Aroyo et al., 2023) motivate modelling disagree-                A learner-free measurement (Appendix D). Before fit-
090   ment; jury learning (Gordon et al., 2022), multi-annotator             ting any personalised model we measured, on MultiPref,
091   models (Mostafazadeh Davani et al., 2022), disagreement                where held-out predictable structure sits: beyond item loca-
092   deconvolution (Gordon et al., 2021), per-rater toxicity mod-           tion, rater-specific thresholds improve held-out likelihood
093   els (Kumar et al., 2021), opinion-based prediction of unseen           about 25 times more than item-specific dispersion (+0.036
094   annotators (Fleisig et al., 2023) and multilevel models of             vs +0.0014 nats per rating), the item-level shape of the rat-
095   DICES raters (Homan et al., 2024) predict individual an-               ing distribution that replicates across disjoint rater panels
096   notators. Preference strength enters reward training as a              is small (split-half reliability 0.25), and about a tenth of it
097   margin (Touvron et al., 2023; Wang et al., 2025); ties have            is decodable from text. Within this decomposition, the pre-
098   classical paired-comparison models (Rao & Kupper, 1967;                dictable structure beyond item location is therefore mostly
099   Davidson, 1970). Personalised reward models infer a user               rater-side scale use, while the item-level shape that repli-
100   latent from a few examples (Poddar et al., 2024; Chen et al.,          cates across disjoint panels is small and only partly in the
101   2025), use a low-rank reward subspace (Bose et al., 2025),             text. These two facts come from different estimands and do
102   persona prompts induced from history (Ryan et al., 2025),              not say that disagreement is “not in the text”. The stage-1 de-
103   per-user embeddings (Li et al., 2024), combinations of base            cision rule we had written down returned “mixed”, because
104   rewards (Shenfeld et al., 2025; Luo et al., 2025) or neural            G/X was not ≤ 10 % (interval 5.7–11.9 %); the factorised
105   processes (Kobalczyk et al., 2024); others personalise the             model of §4 was chosen with that outcome known.
106   policy (Jang et al., 2023; Feng et al., 2024), adapt to groups
107   (Zhao et al., 2024; Chakraborty et al., 2024), study person-
108   alisation versus aggregation (Park et al., 2024) or condition
109
                                                                         2
                                                    What Do Gains in Personalised Reward Modelling Measure?

110                         all raters (marginal)         high intensity (90th pct.)       low intensity (10th pct.)     high tie offset (90th pct.)
111
112               0.4
113
                  0.3
      P(rating)



114
115               0.2
116
117
                  0.1
118               0.0
                        A B A>B tie B>A B A               A B A>B tie B>A B A              A B A>B tie B>A B A           A B A>B tie B>A B A
119
120
121
122   Figure 1. What three numbers per rater change. Left: the marginal distribution of MultiPref ratings. Right: the same distribution passed
123   through the fitted scale-use offsets (extreme, slight, tie) of three real new raters (k = 50) closest to the 90th / 10th percentile of intensity
124   (extreme minus slight) among raters whose tie offset is at or below the median, and closest to the 90th percentile of the tie offset. The
125   offsets are text-independent: they mainly reshape predicted intensity and ties; changes in the preferred side are small.
126
127   4. A three-parameter scale-use baseline                                          5. Experiments
128
129   (Figure 1 illustrates the effect of the offsets.) Let ℓ(x) ∈ RK                  Protocol. 5 paired splits; split f holds out rater fold f (20 %
130   be the class logits of a text-only distributional reward model                   of raters, stratified by group) and prompt-group fold f (20
131   for item x (K ordered rating levels). For rater r we add a text-                 % of prompt groups); models are trained on training raters
132   independent offset vector: p(y | x, r) = softmax(ℓ(x) + b r).                    × training items with penalties chosen on a validation split;
133   Variants: DF (b r ∈ RˆK, free), DFs (two-sided preference                        each test rater is adapted on k ∈ {0, 5, 10, 20, 50} of their
134   scales only: b r tied symmetrically, (e, s, t, s, e) — extreme,                  ratings of training items (5 random draws) and evaluated
135   slight, tie — 3 parameters, of which 2 are identifiable be-                      on their ratings of held-out items. Primary metric: held-out
136   cause the softmax is invariant to a common shift; no A-vs-B                      log-likelihood per rating; also RPS and preference-direction
137   position term). Rater offsets have a Gaussian prior centred                      accuracy; rater-cluster bootstrap (B = 2,000). Because test
138   on the training-rater mean; a new rater’s offsets are the MAP                    raters share test items on MultiPref and DICES, the headline
139   estimate from k of their ratings with the text model frozen.                     k = 20 contrasts were also re-estimated with a two-way boot-
140   Baselines under the same protocol: D (text-only distribu-                        strap that resamples raters and prompt groups independently:
141   tional RM), DG (group offsets: crowd/expert, race, region),                      on graded labels every log-likelihood interval widens by at
142   DL (low-rank text-interacting latent: ℓ(x) + (Wx + w0 )·z r,                     most 0.007 on either side and no log-likelihood conclusion
143   d = 8, the personalised-RM family). An interpretable probit                      changes; direction-accuracy differences of about a point or
144   family (rater shift / log-scale on an ordered-probit text head)                  less (the style model’s +0.5 on MultiPref, VPL’s direction
145   is reported as a secondary analysis.                                             advantage over the style model) lose significance and are
146                                                                                    marked where they appear. Text model in §5.1–5.2: frozen
      Training and adaptation. The text model and the train-
147                                                                                    Qwen2.5-7B features with a ridge head; §5.3: a LoRA-fine-
      ing raters’ offsets are fitted jointly by penalised maximum
148                                                                                    tuned reward model.
      likelihood,
149
150                                                                                    5.1. Main result (MultiPref)
             ∑︂                                          ∑︂
       min        − log p(y | xi , r) + λtext ∥V ∥2 + λr    ∥br ∥2 ,
151               (i,r,y)                                           r
152                                                                                    Figure 2 shows the gain over the text-only reward model as
153                                                                                    a function of k on all three datasets.
      with λtext chosen on the text-only model and λr on
154   held-out items of the training raters. A new rater                               Preference-direction accuracy (D: 0.674): DFs +0.005
155   r∗ is adapted      from k ratings {(xj , yj )} by b̂r∗ =                         [+0.001, +0.008] at k = 20 (not significant once items are
156   arg minb j − log softmax(ℓ(xj )+b)yj +λr ∥b−b̄∥2 , with
                 ∑︁
                                                                                       also resampled: [−0.001, +0.011]); DF −0.014 [−0.020,
157   b̄ the training-rater mean (the prior mean; b̂ = b̄ at k = 0)                    −0.007]. A three-number style model gains as much as a
158   and the text model frozen — a convex problem in 3–5 param-                       tuned 8-dimensional text-interacting latent (tie at k = 20)
159   eters, solved in milliseconds. Any text model that outputs                       and more at k = 5, 10 and 50; fitting a rater’s A-vs-B position
160   graded log-probabilities can be used: we use a ridge head on                     from few ratings costs direction accuracy.
161   frozen LLM features (§5.1–5.2), a LoRA-fine-tuned LLM
162                                                                                    Reference points. To size these gains: on MultiPref at k
      reward model (§5.3) and the decoder of a published person-                       = 20 a uniform forecast scores −1.609 nats per rating, a
163   alised reward model (§5.4).
164
                                                                                 3
                                                             What Do Gains in Personalised Reward Modelling Measure?

165                                    MultiPref (pairwise preference)                     DICES-350 (safety)                         PRISM (response ratings)
166
      log-lik. per rating vs D

167
168                              0.1
169
170
171                              0.0
172
173
174                              0.1
175                                    0 5 10 20                      50           0 5 10 20                      50              0 5 10 20                      50
176                                      ratings of the new rater (k)                ratings of the new rater (k)                   ratings of the new rater (k)
177
178                                style offsets, symmetric (DFs)           style offsets (DF)            low-rank latent (DL, tuned)              group offsets (DG)
179
180
181   Figure 2. New raters: gain in held-out log-likelihood per rating over the text-only distributional reward model (D), as a function of the
182   number k of the new rater’s ratings used for adaptation; 95% rater-cluster bootstrap bands, 5 folds. Text-independent rater offsets (DF;
183   symmetric three-parameter DFs on two-sided preferences) gain 0.08–0.10 nats per rating at k = 20 on all three datasets; group offsets
184   (crowd/expert, race, region) gain nothing; a low-rank text-interacting rater latent with a few-shot-tuned prior ties the three-parameter DFs
185   and beats the five-offset DF on MultiPref (DF − DL = −0.015). DF, DFs and DG use the training-rater prior; DL the few-shot-tuned prior.
186
187
      Table 1. MultiPref new raters: gain in held-out log-likelihood per rating over the text-only model D, by k; 95 % rater bootstrap. DF/DFs/DG
188   use the training-rater prior; DL and DFs − DL the few-shot-tuned prior (DFs − DL post hoc).
189                                        k   DF − D                 DFs − D                DG − D DL − D (tuned prior)       DFs − DL (tuned, post hoc)
190
                                           5 +0.028 [+0.012, +0.044] +0.048 [+0.029, +0.070] ≈ 0       +0.023 [−0.002, +0.047] +0.026 [+0.016, +0.037]
191                                        20 +0.080 [+0.055, +0.106] +0.100 [+0.074, +0.128] ≈ 0      +0.095 [+0.069, +0.122] +0.0045 [−0.0004, +0.0092]
192                                        50 +0.114 [+0.087, +0.142] +0.128 [+0.101, +0.156] ≈ 0      +0.120                  +0.007 [+0.002, +0.013]
193
194
195   forecast that ignores the text and uses only the new rater’s                                   add. Against in-context personalisation (a LoRA model
196   20 ratings −1.487, the text-only model −1.441, the text                                        given the rater’s k ratings in the prompt, three seeds per
197   model with the three offsets −1.342, and offsets fitted in-                                    fold) the offsets are better by +0.041 [+0.027, +0.054] nats
198   sample on all of the rater’s held-out ratings (an optimistic                                   and +1.9 [+0.9, +2.7] direction points (Appendix B).
199   ceiling for text-independent offsets) −1.262. Twenty rat-
200   ings of a person, without the text, recover 73 % of the text                                   5.4. Published personalised reward models
201   model’s gain over uniform; the offsets close about 55 %
      of the gap between the text-only model and the in-sample                                       We reimplemented VPL (Poddar et al., 2024) and PAL-B
202                                                                                                  (Chen et al., 2025) from their official code as heads on
203   ceiling. On DICES the rater’s ratings alone predict better
      than the text alone (−0.766 vs −0.840 at k = 20). Even                                         the same frozen per-response embeddings and evaluated
204                                                                                                  them under the same new-rater protocol, refitting the text-
205   the in-sample ceiling raises MultiPref direction accuracy
      by only 1.3 points (0.674 → 0.687), consistent with offsets                                    only and style models on those embeddings. On graded
206                                                                                                  labels, at k = 20 the style model is better than VPL by
207   acting mainly on intensity and ties.
                                                                                                     +0.092 [+0.068, +0.119] nats per rating ([+0.063, +0.124]
208                                                                                                  when prompt groups are also resampled) and than PAL-B by
209   5.2. Replications (k = 20)
                                                                                                     +0.158. VPL’s latent does carry rater information once its
210   On DICES and PRISM the offsets gain +0.08–0.09 nats per                                        posterior collapse is prevented (KL weight selected as 0 or
211   rating and group offsets nothing (Table 2).                                                    0.001; +0.087 over its own unpersonalised version), but only
212                                                                                                  lifts it to the level of the text-only model; PAL-B’s few-shot
213                                                                                                  user weights give no gain. Their user representations are
      5.3. On a fine-tuned reward model
214                                                                                                  unrelated to response style (cross-validated R2 ≈ 0 against
215   With a LoRA-fine-tuned Qwen2.5-7B reward model as                                              the style offsets). On binary labels — the setting in which
216   the text model, the three offsets still add +0.100 [+0.071,                                    both methods were proposed — every method’s personalisa-
217   +0.130] nats per rating at k = 20 — as on the frozen-feature                                   tion gain is at most 0.002 nats (small but nonzero for PAL-B
218   head — and the gains of fine-tuning and of personalisation
219
                                                                                                 4
                                              What Do Gains in Personalised Reward Modelling Measure?

220
      Table 2. Replications at k = 20 (nats per rating). DF − D and DG − D use the training-rater prior, DF − DL the few-shot-tuned prior.
221
      Direction accuracy on PRISM means good-vs-bad around the scale midpoint.
222
      dataset            DF − D                  DG − D (groups) DF − DL (tuned prior)                                                        direction acc. DF − D
223
      DICES-350 (safety) +0.089 [+0.064, +0.117] −0.006 (race)     +0.037 [+0.022, +0.053]                                                    +0.048 [+0.025, +0.076]
224   PRISM (ratings)    +0.080 [+0.071, +0.090] +0.003 (region)   −0.001 [−0.006, +0.003] (formally not non-inferior: bound −0.006 < −0.005) +0.005 [+0.001, +0.009]
225
226
227   with K = 4, and for VPL and the style model at k = 50), and                     rater’s (a derangement within fold, k and draw). We fixed
228   VPL’s text head is the best binary model (the style model is                    beforehand that the protocol has power at a strength if some
229   0.010 nats behind it and 0.005 behind the text-only model,                      content-interacting method has a lower 95 % bound above
230   differences of the size of item-sampling noise): on these                       +1 point at k = 20; the +10 and +21 panels are exploratory.
231   panels the largest demonstrated gains are captured by cali-
232                                                                                   No evaluated method met the pre-specified detection cri-
      bration of graded levels and ties, which binary preference
233                                                                                   terion. In the exploratory dose-response, VPL and PAL-B
      data discard. VPL’s per-response reward head is slightly
234                                                                                   with PCA-256 features detect +21-point preferences but
      better at predicting which response is preferred (0.677 vs
235                                                                                   recover less than half a point of +10; on real data they are
      0.668), an effect present without personalisation and not
236                                                                                   at the null-control level, and the low-rank latent’s +0.30
      significant once prompt groups are also resampled (style
237                                                                                   [−0.00, +0.60] is matched by the text-independent offsets
      model − VPL: −0.9 points [−2.7, +0.8]). The offsets are
238                                                                                   (+0.32). A reference learner that is given the two injected
      also a plug-in: added to VPL (fitted on the same k ratings,
239                                                                                   features recovers +0.89 [+0.40, +1.37], +3.1 and +8.0 points
      VPL frozen) they improve it by +0.088 [+0.066, +0.111]
240                                                                                   of the +1.7, +5.2 and +10.1-point oracle gains from 20 rat-
      nats per rating at k = 20, come within −0.004 [−0.014,
241                                                                                   ings, so twenty ratings permit recovery in these injected
      +0.005] of the style model on likelihood (non-inferiority not
242                                                                                   families when the generating features are supplied; the gap
      established) and keep VPL’s direction accuracy (+1.1 points
243                                                                                   implicates representation and inductive bias (probes, re-
      over the style model alone; rater bootstrap only).
244                                                                                   injection and semantic axes in Appendix B). These results
245                                                                                   characterise recovery for specified injected families on pan-
      5.5. Summary of baselines (MultiPref, new raters, k =                           els noisier than the real data; they are not formal exclusion
246        20)
247                                                                                   bounds.
248   Gains are relative to each block’s text-only model (D, Dp,
249   D-LoRA); the LoRA block uses adaptation draw 0 only (the                        5.7. How much room is there? Conflicts among aspect
250   draw the in-context model was evaluated on), hence the                               judgements are rare
251   style model’s +0.092 here against +0.100 averaged over five
                                                                                      With the rater’s own helpfulness, truthfulness and harm-
252   draws in §5.3.
                                                                                      lessness labels as inputs, a pooled trade-off gets 97.5 % of
253   Rows within a block share the text model and the raters;                        MultiPref directions right and a rater-specific one fitted on
254   across blocks the text models differ (text-only direction                       all training ratings adds only +0.10 [−0.24, +0.43] points
255   accuracy 0.674 / 0.670 / 0.688). VPL’s and PAL-B’s own                          (+0.03 at k = 20): the three aspect judgements conflict in
256   gains over their unpersonalised versions are +0.087 and                         only 4.0 % of held-out non-tie comparisons (details in Ap-
257   −0.000.                                                                         pendix B).
258
259   5.6. Could these methods have detected content                                  5.8. A learner that finds the axes
260        personalisation? A semi-synthetic positive control
261                                                                                   A screened empirical-Bayes learner over 24 interpretable
262   A ranking null is informative only if the methods would                         attribute differences (SAP) recovers the semi-synthetic con-
263   detect content-dependent preferences where they exist. We                       tent preferences that the published learners miss, with near-
264   keep MultiPref’s raters, items, folds and k-shot draws and                      zero effects on null panels, and abstains on real MultiPref
265   replace the labels by semi-synthetic ones: a generator                          under a prospectively specified rule (+0.28 [−0.00, +0.58]
266   (the text-only head plus scale-use offsets) gives each rat-                     points at k = 20). Details: Appendix G.
267   ing a distribution, to which a rater-specific content term
268   (θr⊤ gi ) (−2, −1, 0, 1, 2) is added; gi are two response-pair                  5.9. Developers rating code readability
269   features (log length ratio and a random embedding direction
270   orthogonal to consensus quality), θr ∼ N (0, τ 2 I), and τ                      On two code-readability studies with persistent developer
271   is calibrated so that an oracle knowing θr gains +1.7, +5.2,                    identities (Buse–Weimer, 121 raters, Buse & Weimer, 2010;
272   +10.1 or +21.1 direction points (τ = 0: null control). The                      Dorn, 3,393 developers, Dorn, 2012) and Qwen2.5-Coder-
273   contrast is own adapted parameters minus another test                           7B features, scale use transfers to new developers (offsets
274
                                                                                  5
                                                     What Do Gains in Personalised Reward Modelling Measure?

275
                                            Table 3. Baselines on MultiPref, new raters, k = 20, grouped by text model.
276
      text model                                     personalisation                                             gain in LL per rating vs the block’s text-only model direction accuracy
277
      frozen features (joint item embedding)    group offsets (crowd / expert)                                   ≈0                                                  0.677
278                                             low-rank latent, tuned prior                                     +0.095 [+0.069, +0.122]                             0.679
279                                             style offsets, 3 numbers (DFs)                                   +0.100 [+0.074, +0.128]                             0.679
      frozen features (per-response embeddings) VPL (reimplemented)                                              +0.002 [−0.008, +0.012]                             0.677
280                                             PAL-B (reimplemented)                                            −0.065 (worse)                                      0.666
281                                             DFs                                                              +0.094 [+0.069, +0.120]                             0.668
                                                VPL + style offsets                                              +0.090                                              0.679
282   LoRA-fine-tuned Qwen2.5-7B (209 raters) in-context rater history (RC-LoRA, mean of 3 training seeds)       +0.051 [+0.024, +0.079]                             0.671
283                                             DFs                                                              +0.092 [+0.063, +0.125]                             0.689
284
285
286   Table 4. Semi-synthetic positive control (MultiPref). Own minus another rater’s k = 20 ratings, direction accuracy in points, 95 % rater
287   bootstrap; 209 new raters, 5 folds. The low-rank latent uses the few-shot-tuned prior. k = 50 contrasts use the 180 of 209 raters with at
      least 50 training-item ratings. PAL-B’s own − other contrast is negative with compressed features (null control −0.23, real data −0.43):
288
      its per-rater adaptation adds noise there; with full features it is at zero (−0.04, +0.11). The injection uses one draw of θ and of the labels,
289   so seed variability of the synthetic panels is not in the intervals. Last column: PAL-B on the full 3,584-dimensional features instead of
290   their PCA-256 (exploratory; τ 2 not run).
291                   panel                           oracle gain low-rank latent (DL)    VPL                    PAL-B                     PAL-B, full features
292                   null control (τ = 0)            0            −0.10 [−0.38, +0.17]   −0.04 [−0.08, +0.01]   −0.23 [−0.45, +0.00]      −0.04 [−0.25, +0.17]
293                   injected, τ 2                   +1.7         −0.01 [−0.29, +0.26]   +0.01 [−0.07, +0.10]   −0.10 [−0.36, +0.15]      —
294                   injected, τ 5                   +5.2         −0.02 [−0.28, +0.26]   +0.01 [+0.00, +0.03]   +0.23 [−0.04, +0.51]      +0.26 [−0.14, +0.66]
                      injected, τ 10 (exploratory)    +10.1        +0.09 [−0.18, +0.36]   +0.27 [+0.02, +0.54]   +0.42 [−0.08, +0.96]      +1.95 [+1.16, +2.74]
295                   injected, τ 20 (exploratory)    +21.1        +1.47 [+0.83, +2.18]   +6.92 [+5.63, +8.30]   +4.62 [+3.47, +5.78]      +8.13 [+6.54, +9.77]
296                   real MultiPref                  —            +0.30 [−0.00, +0.60]   −0.01 [−0.04, +0.02]   −0.43 [−0.72, −0.15]      +0.11 [−0.16, +0.37]

297
298
299   +0.054 [+0.036, +0.074] nats per rating at k = 20 and +0.040                              direction accuracy on MultiPref (0.674) is already as high as
300   [+0.031, +0.049] at k = 10), while content adaptation over 22                             the agreement in direction between two human raters of the
301   readability attributes is inconclusive at the pre-set budgets                             same item (0.673 [0.666, 0.680]): a population model pre-
302   (Buse–Weimer, k = 20: +0.40 [−0.25, +1.06]; Dorn, k =                                     dicts a new rater about as well as another person does. Seen
303   10: −0.19 [−0.81, +0.42] concordance points; Appendices                                   raters. With all their training ratings (median 134), training
304   A–B).                                                                                     raters’ own parameters beat another rater’s by −0.11 [−0.57,
305                                                                                             +0.36] direction points for the low-rank latent (offsets +0.10,
306   6. What personalisation buys: graded-rating                                               −0.23): the ranking null is not specific to few-shot adap-
307                                                                                             tation (exploratory, Appendix B). Against its own k = 0
         prediction, user signal, and small choice                                              version, no method’s direction accuracy on MultiPref rises
308      gains
309                                                                                             by more than 0.2 points at k = 20, and every upper 95 %
310   Binarisation removes the symmetric scale-use term; eval-                                  bound stays below +0.8 points even when prompt groups are
311   uated adaptation gains on MultiPref are small. On Multi-                                  resampled together with raters (VPL +0.07 [−0.57, +0.74],
312   Pref with ties dropped and labels binarised, every evaluated                              style model −0.10 [−0.69, +0.54], PAL-B −0.48 [−1.11,
313   method’s personalisation gain is at most 0.002 nats per rat-                              +0.14]). The ranking null replicates on real users’ own
314   ing (§5.4), and the scale-use baseline’s binary accuracy is                               choices. PRISM users each saw 2–4 responses to their own
315   essentially unchanged from the text-only model’s. On these                                prompt, scored them and chose one; pairing the chosen re-
316   graded panels the largest demonstrated gains concern graded                               sponse with every other one gives 41,199 native pairwise
317   levels and ties — which binary preference data, the format                                choices of 1,396 users. Under the same new-user protocol
318   in which most personalised reward models are trained and                                  (5 paired user and conversation folds, k of the user’s pairs
319   evaluated, discard (Community Alignment shows that bi-                                    from training conversations), we fixed before any result that
320   nary choices can also carry predictable user differences, §6).                            the ranking null would be stated only if every method’s
321   Ranking moves little. Symmetric offsets mainly change                                     improvement in choice accuracy over its own k = 0 version
322   how strongly a rater is predicted to prefer a response: on                                had an upper 95 % bound below one point at k = 20. It
323   graded MultiPref the scale-use baseline raises direction ac-                              holds for all of them (1,033 new users at k = 0; the 669 with
324   curacy by only +0.005 [+0.001, +0.008] at k = 20 (about                                   at least 20 adaptation pairs at k = 20): VPL +0.12 points
325   half of it already at k = 0), while RPS drops from 0.1593 to                              [−0.08, +0.33], PAL-B +0.0 [−0.4, +0.4] (K = 2) and +0.3
326   0.1532. On single-response safety ratings the same offsets                                [−0.1, +0.7] (K = 4), the 5-offset model −0.6 [−1.4, +0.2];
327   do move the safe/unsafe decision (+4.8 points on DICES),                                  the symmetric scale-use model is identical to the text-only
328   because there a rater’s threshold is the decision. Text-only                              model on binary choices, because a binary label carries no
329
                                                                                           6
                                       What Do Gains in Personalised Reward Modelling Measure?

330   intensity. LoRe (Bose et al., 2025), which reports +10 points         value from attributes beyond position is unresolved. With
331   for unseen PRISM users, run here with its own few-shot fit            correlated predictors under one prior this does not separate
332   and with a validated adaptation ridge under the same pre-set          content from position: we claim user-specific choice pre-
333   rule, also meets the ranking-null criterion: own gain at k =          dictability on identical alternatives, not a content preference,
334   20 −1.5 [−2.5, −0.4] (regularised −0.5 [−1.2, +0.2]), own             and not a psychological position habit.
335   − other +0.2 [−0.8, +1.2]. In LoRe’s own setting (its em-
                                                                            Benefit over the population model. On all test events of the
336   beddings, split and pair construction) we obtain 67.4 % for
                                                                            shared items in the test folds — a broader panel than the
337   the monolithic model and 63.6 % for LoRe (published 61.0
                                                                            1,116 items that contribute disagreeing pairs to the assign-
338   % and 71.0 %; Appendix B): the published gain is not repro-
                                                                            ment test (2,383 items, 1,436 users; population accuracy
339   duced. With a graded label cut from the users’ own score
                                                                            72.4 %) — isotropic adaptation gains +0.70 [+0.24, +1.14]
340   differences (thresholds fixed in advance), the MultiPref pat-
                                                                            pairwise accuracy points and +0.018 [+0.014, +0.023]
341   tern returns at half the size (scale-use model +0.043 [+0.031,
                                                                            nats — the pre-set user-bootstrap rule for benefit is met,
342   +0.057] nats per rating at k = 20, VPL +0.015, PAL-B 0.000;
                                                                            but the user × item interval for accuracy covers 0 ([−0.07,
343   no direction gain above +0.2 points). Community Align-
                                                                            +1.43]) while log-likelihood improves under both, so an
344   ment: who chooses what on identical items, and what
                                                                            accuracy benefit that generalises across items is unresolved;
345   adaptation buys. Community Alignment (CA; first turns;
                                                                            nor is the gain shown to be below one point. Evaluated
346   2,957 new users in five countries and languages; each choice
                                                                            frozen on the same users’ unanalysed second turns (pro-
347   event’s chosen response paired with each of the other three).
                                                                            cedure refitted there; Stage 12), the covariance-calibrated
348   Accuracy below is pairwise winner-versus-other accuracy,
                                                                            variant gains +0.38 [+0.13, +0.64] points and +0.0046 nats
349   not four-way winner selection. Status: the adaptation proce-
                                                                            and isotropic +0.31 [+0.05, +0.58]; the prompt × user inter-
350   dure was developed exploratorily on first turns (Appendix
                                                                            val covers 0. On MultiPref the frozen isotropic procedure
351   F); the Stage-12 and Stage-13 outcome rules were frozen
                                                                            did not establish improvement (−0.28 [−0.64, +0.08] points,
352   before their outcomes; the Stage-13 first-turn analyses reuse
                                                                            202 held-out annotators). On CA the estimated covariance
353   previously examined data, while the second- and third-turn
                                                                            shows no advantage over isotropic shrinkage (turn 1 −0.17
354   outcomes were evaluated for the first time.
                                                                            [−0.29, −0.05], turn 2 +0.07 [−0.07, +0.22] points); on
355
      Identity on identical items (Stage 13, frozen). CA contains           MultiPref it beats isotropic under the rater bootstrap (+0.23
356
      2,928 exact prompt–four-response items shown to at least              [+0.04, +0.42]) without establishing improvement over the
357
      two users, covering 49,616 first-turn conversations (me-              population model (two-way includes 0; Appendix F). Vali-
358
      dian 15 users per item, one language per item, fixed re-              dated scales imply strong shrinkage, and realised gains are
359
      sponse order). For two users of the same item who chose               far below model-implied ones (the c = 1 covariance-prior
360
      different responses a and b, the population utilities can-            learner: +1.9 points implied under a Gaussian event-level
361
      cel and the adapted models predict the assignment from                simulation, +0.13 realised; Appendix F).
362
      S = (δu − δv )⊤ (xa − xb ), with model-implied probabil-
363                                                                         Transport to later conversations (Stage 13, frozen). We
      ity σ(S). With validated isotropic adaptation over length,
364                                                                         froze each user’s first-turn deviation and added it, with-
      paragraphs and list/heading lines (k = 20 support events
365                                                                         out rescaling, to a third-turn population model that sees
      on other prompts; the Stage-12 procedure unchanged), the
366                                                                         the conversation history (the earlier prompts and the user’s
      conditional assignment log score gains +0.066 [+0.034,
367                                                                         preferred responses). We scored it on the third turns of con-
      +0.091] nats over chance and assignment accuracy is 62.2
368                                                                         versations not used for support. Of 1,901 users with a frozen
      % [58.6, 65.6] (4,608 disagreeing pairs from 1,336 users on
369                                                                         first-turn deviation, 1,808 have at least five third-turn events
      1,116 items; item × user bootstrap). It is unchanged with
370                                                                         with a complete history and 953 have at least five outside
      uncentred features; positive-multiplier and prompt-clustered
371                                                                         their support conversations. The result is accuracy-positive
      intervals are [+0.046, +0.083] and [+0.036, +0.093]; every
372                                                                         under user clustering and likelihood-inconclusive: accuracy
      fold is positive. The estimand is narrow: given two dis-
373                                                                         rises by +0.43 [+0.13, +0.74] points (user × prompt inter-
      agreeing users, their support choices and the two responses
374                                                                         val [−0.08, +0.92]), log-likelihood by +0.0015 [−0.0006,
      they picked, assign the responses; it conditions on the fitted
375                                                                         +0.0035] nats. The pre-set rule requires both lower bounds
      deviations and population model.
376                                                                         above 0, so additional predictive value of unrescaled first-
377   Position. The four fixed positions differ systematically              turn coefficients beyond a history-conditioned population
378   in these attributes (label-blind check), so we refitted with          model is not supported for this procedure and panel.
379   position indicators added (after the result). The attribute-          This neither shows that transport has no effect nor that pref-
380   derived part of the jointly fitted scores keeps +0.060 [+0.032,       erences are unstable, and it does not test other ways of
381   +0.084] nats, a position-only predictor is also informative           carrying information across turns.
382   (63.8 %), and the joint model’s paired gain over position-
                                                                            The measured gain depends on the population baseline. On
383   only is +0.026 [−0.0002, +0.046], so additional assignment
384
                                                                        7
                                                  What Do Gains in Personalised Reward Modelling Measure?

385
      Table 5. Choice-level results. k = 20 support choice events per user (20 binary comparisons on MultiPref); pairwise accuracy; log-
386
      likelihood per pair. First interval: user (rater) bootstrap, or item × user for the assignment rows; second: prompt- or item-group × user
387   two-way bootstrap. Nominal 95 % intervals, conditional on the fitted population models. “Reused” = data examined in earlier stages;
388   “new” = outcomes evaluated for the first time.
389   Question (comparator)                              Panel                                Accuracy, points                       Log-likelihood, nats                             Status
390   Assignment (chance)                                CA t1 identical items; 1,336 users   62.2 % [58.6, 65.6]                    +0.066 [+0.034, +0.091]                          frozen, reused
391   . . . beyond position (position-only)              same                                 —                                      +0.026 [−0.0002, +0.046]                         exploratory
      Benefit (population)                               CA t1 shared items; 1,436 users      +0.70 [+0.24, +1.14]; [−0.07, +1.43]   +0.018 [+0.014, +0.023]; [+0.010, +0.026]        frozen, reused
392   Benefit, isotropic (population)                    CA t2; 1,702 users                   +0.31 [+0.05, +0.58]; [−0.13, +0.79]   +0.0038 [+0.0021, +0.0057]; [+0.0006, +0.0066]   frozen, new
393   Benefit, TRV, covariance-calibrated (population)   CA t2; 1,702 users                   +0.38 [+0.13, +0.64]; [−0.04, +0.83]   +0.0046 [+0.0031, +0.0063]; [+0.0018, +0.0074]   frozen, new
      Benefit, isotropic (population)                    MultiPref; 202 annotators            −0.28 [−0.64, +0.08]; [−0.92, +0.39]   −0.0004 [−0.0019, +0.0010]; [−0.0028, +0.0019]   frozen, reused
394   Transport (history-conditioned pop.)               CA t3; 953 users                     +0.43 [+0.13, +0.74]; [−0.08, +0.92]   +0.0015 [−0.0006, +0.0035]; [−0.0020, +0.0048]   frozen, new
395   Baseline procedure W − O (paired)                  CA t1; 1,799 users                   +0.62 [+0.41, +0.81]                   —                                                exploratory
396
397
398   1,799 common users, one-dimensional length adaptation                                             tive controls. (vi) Keep graded labels and ties when
399   gains +0.88 / +1.08 points (random / prompt-separated test                                        individual differences matter.
400   events) against a population model fitted on low-volume
401   annotators, as in WIMHF’s protocol (Movva et al., 2025),
                                                                                                  8. Discussion
402   and +0.26 / +0.47 against one fitted on all other-fold users:
403   the population-procedure effect is +0.62 [+0.41, +0.81] and                                 What do personalisation gains measure? Three things
404   +0.61 [+0.30, +0.93] (paired), while the prompt-split con-                                  often reported as one come apart. Graded-rating gains for
405   trast is inconclusive (+0.20 [−0.20, +0.59]). The two pro-                                  new raters are largely scale use: offsets capture them, probes
406   cedures differ in volume, composition and prior estimation,                                 find near-zero R2 for them in the evaluated user represen-
407   so no mechanism is isolated. (Our line-count proxy is not                                   tations, and adding offsets to VPL recovers most of the
408   WIMHF’s discovered feature; with it, list/heading adapta-                                   point-estimate gain (+0.088; non-inferiority not established).
409   tion does not beat the population coefficient — a related                                   User-specific choice predictability is real on identical CA
410   protocol study, not a failed reproduction.)                                                 items (62 %), though not separated from position. Choice
411                                                                                               gains over a competent population model are small and
      Earlier evidence. Before this test, own adapted parameters
412                                                                                               fragile (Table 5).
      beat another user’s for four of six methods (LoRe +3.27
413   [+2.85, +3.70]; within-country +3.22) and length deviations                                 Why did published models learn little about new raters
414   reproduced across disjoint prompt sets; own − other does                                    here? Published evaluations differ in users (synthetic or
415   not measure benefit and task mix could create it (Appendix                                  seen), label formats, representations and population base-
416   F). The identical-item test supersedes these as evidence of                                 lines; the last alone changes the measured gain by about 0.6
417   user-specific choice predictability.                                                        points on CA. Unresolved native-reproduction discrepan-
418                                                                                               cies prevent attributing the rest to evaluation design, and all
419                                                                                               method conclusions concern the evaluated implementations.
420   7. Recommendations
421    (i) Separate three outcomes. Report graded-rating likeli-
422        hood (calibration and resolution), a test of user-specific
                                                                                                  9. Limitations and analysis log
423        choice predictability, and choice or ranking gains over                                The main tables use frozen-feature text heads (a LoRA re-
424        the population model as different results; a gain on                                   ward model only in §5.3), and compressed features weaken
425        one does not imply the others. (ii) Test user differ-                                  PAL-B as a detector (§5.6). VPL, PAL and LoRe are our
426        ences on identical items where the data allow it (an                                   reimplementations as heads on frozen embeddings; pub-
427        assignment test between disagreeing users, as in §6):                                  lished numbers were not reproduced (LoRe’s PRISM gain
428        own-versus-other contrasts on different prompts con-                                   not even with its own embeddings). The positive control
429        found user differences with task mix and do not mea-                                   covers MultiPref only, on panels noisier than the real data.
430        sure benefit. (iii) Report a competent population                                      Aspect analyses use MultiPref’s concurrent labels (SAP: Ap-
431        baseline and its training procedure. The measured                                      pendix G). The first three datasets are English; Community
432        personalisation gain changed by about 0.6 points with                                  Alignment spans five languages, which the phrase-based
433        the population-training procedure (§6). (iv) Report                                    attributes cover only for English; and the per-rater calibra-
434        a scale-use baseline (a few text-independent offsets                                   tion is not shown to change a downstream decision. The CA
435        per rater) next to any personalised reward model on                                    analyses reuse data examined in earlier stages (Appendix A);
436        graded labels, and evaluate content adaptation with                                    the identical-item test conditions on fitted models; features
437        those offsets retained. (v) Evaluate on unseen raters                                  omit conversation history except in the third-turn test; and
438        and held-out prompts, with permutation and posi-                                       the identity signal is not separated from response position.
439
                                                                                              8
                                       What Do Gains in Personalised Reward Modelling Measure?

440   Impact Statement                                                      Chen, D., Chen, Y., Rege, A., Wang, Z., and Vinayak, R. K.
441                                                                           PAL: Sample-efficient personalized reward modeling for
442   This paper evaluates personalised reward models, which are              pluralistic alignment. In The Thirteenth International
443   meant to let language models serve people whose prefer-                 Conference on Learning Representations (ICLR), 2025.
444   ences differ. It finds that reported personalisation gains can
445   reflect rating-scale use, user-associated choice predictability       Davidson, R. R. On extending the Bradley-Terry model
446   or real improvements over a population model, and that                  to accommodate ties in paired comparison experiments.
447   these need separate tests: gains on graded ratings were                 Journal of the American Statistical Association, 65(329):
448   largely scale use, users’ choices on identical alternatives             317–328, 1970. doi: 10.1080/01621459.1970.10481082.
449   were predictable from their other choices, and improvements
450   over a population model were small and dataset-dependent.             Dawid, A. P. and Skene, A. M. Maximum likelihood esti-
451   Predicting individuals’ choices also raises privacy and ma-             mation of observer error-rates using the EM algorithm.
452   nipulation concerns that a deployment would need to ad-                 Journal of the Royal Statistical Society: Series C (Applied
453   dress; we report no individual-level results. The datasets are          Statistics), 28(1):20–28, 1979.
454   public, were collected with consent by their creators, and
      are used under their licences; rater identifiers are used only        Deng, N., Zhang, X. F., Liu, S., Wu, W., Wang, L., and
455
      as anonymous indices.                                                   Mihalcea, R. You are what you annotate: Towards better
456
                                                                              models through annotator representations. In Findings of
457
                                                                              the Association for Computational Linguistics: EMNLP
458   References                                                              2023, pp. 12475–12498, 2023.
459
      Aroyo, L., Taylor, A. S., Dı́az, M., Homan, C. M., Parrish,
460                                                                         Dong, Y. R., Hu, T., Liu, Y., Üstün, A., and Collier, N. When
        A., Serapio-Garcı́a, G., Prabhakaran, V., and Wang, D.
461                                                                           personalization meets reality: A multi-faceted analysis
        DICES dataset: Diversity in conversational AI evaluation
462                                                                           of personalized preference learning, 2025. URL https:
        for safety. In Advances in Neural Information Processing
463                                                                          //arxiv.org/abs/2502.19158.
        Systems 36 (NeurIPS 2023), Datasets and Benchmarks
464
        Track, 2023. doi: 10.52202/075280-2321.
465                                                                         Dorn, J. A general software readability model. Master’s
466   Baumgartner, H. and Steenkamp, J.-B. E. M. Response                     thesis, University of Virginia, 2012.
467     styles in marketing research: A cross-national investi-
468     gation. Journal of Marketing Research, 38(2):143–156,               Eckes, T. Introduction to Many-Facet Rasch Measurement:
469     2001. doi: 10.1509/jmkr.38.2.143.18840.                               Analyzing and Evaluating Rater-Mediated Assessments,
470                                                                           volume 22 of Language Testing and Evaluation. Peter
471   Bose, A., Xiong, Z., Chi, Y., Du, S. S., Xiao, L., and Fazel,           Lang, Frankfurt am Main, 2011. ISBN 978-3-631-61350-
472     M. LoRe: Personalizing LLMs via low-rank reward                       4.
473     modeling, 2025. URL https://arxiv.org/abs/
474     2504.14439.                                                         Feng, S., Sorensen, T., Liu, Y., Fisher, J., Park, C. Y., Choi,
475                                                                           Y., and Tsvetkov, Y. Modular pluralism: Pluralistic align-
476   Buse, R. P. L. and Weimer, W. R. Learning a metric for code             ment via multi-LLM collaboration. In Proceedings of
477     readability. IEEE Transactions on Software Engineering,               the 2024 Conference on Empirical Methods in Natural
478     36(4):546–558, 2010.                                                  Language Processing, pp. 4151–4171, Miami, Florida,
479                                                                           USA, 2024. Association for Computational Linguistics.
480   Castricato, L., Lile, N., Rafailov, R., Fränken, J.-P.,                doi: 10.18653/v1/2024.emnlp-main.240.
481     and Finn, C. PERSONA: A reproducible testbed
        for pluralistic alignment.   In Proceedings of the                  Fleisig, E., Abebe, R., and Klein, D. When the majority is
482
        31st International Conference on Computational Lin-                   wrong: Modeling annotator disagreement for subjective
483
        guistics (COLING), pp. 11348–11368, Abu Dhabi,                        tasks. In Proceedings of the 2023 Conference on Empiri-
484
        UAE, 2025. Association for Computational Linguis-                     cal Methods in Natural Language Processing, pp. 6715–
485
        tics. URL https://aclanthology.org/2025.                              6726, Singapore, 2023. Association for Computational
486
        coling-main.752/.                                                     Linguistics. doi: 10.18653/v1/2023.emnlp-main.415.
487
488   Chakraborty, S., Qiu, J., Yuan, H., Koppel, A., Manocha,              Gordon, M. L., Zhou, K., Patel, K., Hashimoto, T., and Bern-
489     D., Huang, F., Bedi, A. S., and Wang, M. MaxMin-                      stein, M. S. The disagreement deconvolution: Bringing
490     RLHF: Alignment with diverse human preferences. In                    machine learning performance metrics in line with reality.
491     Proceedings of the 41st International Conference on Ma-               In Proceedings of the 2021 CHI Conference on Human
492     chine Learning (ICML), volume 235 of Proceedings of                  Factors in Computing Systems (CHI ’21), pp. 1–14. ACM,
493     Machine Learning Research, pp. 6116–6135, 2024.                       2021. doi: 10.1145/3411764.3445423.
494
                                                                        9
                                      What Do Gains in Personalised Reward Modelling Measure?

495   Gordon, M. L., Lam, M. S., Park, J. S., Patel, K., Hancock,            perspectives. In Seventeenth Symposium on Usable
496     J. T., Hashimoto, T., and Bernstein, M. S. Jury learn-               Privacy and Security (SOUPS 2021), pp. 299–318.
497     ing: Integrating dissenting voices into machine learning             USENIX Association, 2021. ISBN 978-1-939133-25-0.
498     models. In Proceedings of the 2022 CHI Conference on                 URL https://www.usenix.org/conference/
499    Human Factors in Computing Systems (CHI ’22). ACM,                    soups2021/presentation/kumar.
500     2022. doi: 10.1145/3491102.3502004.
501                                                                        Li, X., Zhou, R., Lipton, Z. C., and Leqi, L. Personalized
502   Homan, C. M., Serapio-Garcia, G., Aroyo, L., Diaz, M.,                 language modeling from personalized human feedback,
503     Parrish, A., Prabhakaran, V., Taylor, A., and Wang, D.               2024.
504     Intersectionality in AI safety: Using multilevel models
505     to understand diverse perceptions of safety in conversa-           Linacre, J. M. Many-Facet Rasch Measurement. MESA
506     tional AI. In Proceedings of the 3rd Workshop on Per-                Press, Chicago, 1989.
507     spectivist Approaches to NLP (NLPerspectives) @ LREC-
       COLING 2024, pp. 131–141, Torino, Italia, 2024. ELRA                Luo, F., Yang, R., Sun, H., Deng, C., Yao, J., Shen, J.,
508                                                                          Zhang, H., and Chen, H. Rethinking diverse human pref-
509     and ICCL. URL https://aclanthology.org/
        2024.nlperspectives-1.15/.                                           erence learning through principal component analysis.
510                                                                          In Findings of the Association for Computational Lin-
511   Hovy, D., Berg-Kirkpatrick, T., Vaswani, A., and Hovy, E.              guistics: ACL 2025, pp. 19857–19870, Vienna, Austria,
512     Learning whom to trust with MACE. In Proceedings of                  2025. Association for Computational Linguistics. doi:
513    NAACL-HLT, pp. 1120–1130, 2013.                                       10.18653/v1/2025.findings-acl.1019.
514
515   Jang, J., Kim, S., Lin, B. Y., Wang, Y., Hessel, J., Zettle-         Miranda, L. J. V., Wang, Y., Elazar, Y., Kumar, S., Pyatkin,
516     moyer, L., Hajishirzi, H., Choi, Y., and Ammanabrolu, P.            V., Brahman, F., Smith, N. A., Hajishirzi, H., and Dasigi,
517     Personalized soups: Personalized large language model               P. Hybrid preferences: Learning to route instances for hu-
518     alignment via post-hoc parameter merging, 2023.                     man vs. AI feedback. In Proceedings of the 63rd Annual
519   Kim, G. and Kim, E. Swap-guided preference learning for               Meeting of the Association for Computational Linguis-
520     personalized reinforcement learning from human feed-                tics (Volume 1: Long Papers), pp. 7162–7200, Vienna,
521     back. In International Conference on Learning Represen-             Austria, 2025. Association for Computational Linguistics.
522     tations (ICLR), 2026. URL https://arxiv.org/                        doi: 10.18653/v1/2025.acl-long.355.
523     abs/2603.12595.
524                                                                        Mishra, P., Rastogi, C., Pfohl, S. R., Parrish, A., Teh, T. H.,
525   Kirk, H. R., Whitefield, A., Röttger, P., Bean, A. M., Mar-          Patel, R., Diaz, M., Wang, D., Paganini, M., Prabhakaran,
526     gatina, K., Ciro, J., Mosquera, R., Bartolo, M., Williams,          V., Aroyo, L., and Rieser, V. Decoding safety feedback
527     A., He, H., Vidgen, B., and Hale, S. A. The PRISM                   from diverse raters: A data-driven lens on responsive-
528     alignment dataset: What participatory, representative and           ness to severity. Transactions on Machine Learning
529     individualised human feedback reveals about the subjec-             Research, 2026. URL https://arxiv.org/abs/
530     tive and multicultural alignment of large language models.          2503.05609.
531     In Advances in Neural Information Processing Systems 37
532     (NeurIPS 2024), Datasets and Benchmarks Track, 2024.               Mostafazadeh Davani, A., Dı́az, M., and Prabhakaran, V.
533     doi: 10.52202/079017-3342.                                          Dealing with disagreements: Looking beyond the major-
534                                                                         ity vote in subjective annotations. Transactions of the
535   Kobalczyk, K., Fanconi, C., Sun, H., and van der Schaar,              Association for Computational Linguistics, 10:92–110,
536     M. Few-shot steerable alignment: Adapting rewards and               2022. doi: 10.1162/tacl a 00449.
537     LLM policies with neural processes, 2024.
538                                                                        Movva, R., Milli, S., Min, S., and Pierson, E. What’s in my
      Koren, Y. and Sill, J. OrdRec: An ordinal model for predict-          human feedback? learning interpretable descriptions of
539     ing personalized item rating distributions. In Proceedings
540                                                                         preference data, 2025.
        of the Fifth ACM Conference on Recommender Systems
541     (RecSys), pp. 117–124, 2011.                                       Orlikowski, M., Röttger, P., Cimiano, P., and Hovy, D. The
542                                                                          ecological fallacy in annotation: Modelling human label
543   Koren, Y., Bell, R., and Volinsky, C. Matrix factorization
        techniques for recommender systems. Computer, 42(8):                 variation goes beyond sociodemographics. In Proceed-
544                                                                          ings of the 61st Annual Meeting of the Association for
545     30–37, 2009.
                                                                             Computational Linguistics (Volume 2: Short Papers), pp.
546   Kumar, D., Kelley, P. G., Consolvo, S., Mason, J., Bursztein,          1017–1029, Toronto, Canada, 2023. Association for Com-
547     E., Durumeric, Z., Thomas, K., and Bailey, M. De-                    putational Linguistics. doi: 10.18653/v1/2023.acl-short.
548     signing toxic content classification for a diversity of              88.
549
                                                                      10
                                       What Do Gains in Personalised Reward Modelling Measure?

550   Park, C., Liu, M., Kong, D., Zhang, K., and Ozdaglar, A.               Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A.,
551     RLHF from heterogeneous feedback via personalization                   Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhos-
552     and preference aggregation, 2024.                                      ale, S., Bikel, D., Blecher, L., Canton Ferrer, C., Chen,
553                                                                            M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W.,
554   Plank, B. The “problem” of human label variation: On                     Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn,
555     ground truth in data, modeling and evaluation. In Pro-                 A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez,
556     ceedings of EMNLP, pp. 10671–10682, 2022.                              V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P. S.,
557                                                                            Lachaux, M.-A., Lavril, T., Lee, J., Liskovich, D., Lu, Y.,
558   Poddar, S., Wan, Y., Ivison, H., Gupta, A., and Jaques, N.               Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Moly-
559     Personalizing reinforcement learning from human feed-                  bog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R.,
560     back with variational preference learning. In Advances                 Saladi, K., Schelten, A., Silva, R., Smith, E. M., Subra-
561     in Neural Information Processing Systems 37 (NeurIPS                   manian, R., Tan, X. E., Tang, B., Taylor, R., Williams,
562     2024), 2024. doi: 10.52202/079017-1664.                                A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan,
563                                                                            A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R.,
      Rao, P. V. and Kupper, L. L. Ties in paired-comparison ex-
564                                                                            Edunov, S., and Scialom, T. Llama 2: Open foundation
        periments: A generalization of the Bradley-Terry model.
565                                                                            and fine-tuned chat models, 2023.
        Journal of the American Statistical Association, 62(317):
566
        194–204, 1967. doi: 10.1080/01621459.1967.10482901.                  Uma, A. N., Fornaciari, T., Hovy, D., Paun, S., Plank, B.,
567
                                                                              and Poesio, M. Learning from disagreement: A survey.
568   Raykar, V. C., Yu, S., Zhao, L. H., Valadez, G. H., Florin, C.,         Journal of Artificial Intelligence Research, 72:1385–1470,
569     Bogoni, L., and Moy, L. Learning from crowds. Journal                 2021.
570     of Machine Learning Research, 11:1297–1322, 2010.
571                                                                          Wang, Z., Bukharin, A., Delalleau, O., Egert, D., Shen,
572   Ryan, M. J., Shaikh, O., Bhagirath, A., Frees, D., Held, W.,            G., Zeng, J., Kuchaiev, O., and Dong, Y. HelpSteer2-
573     and Yang, D. SynthesizeMe! inducing persona-guided                    Preference: Complementing ratings with preferences. In
574     prompts for personalized reward models in LLMs. In                    The Thirteenth International Conference on Learning
575     Proceedings of the 63rd Annual Meeting of the Associ-                 Representations (ICLR), 2025. URL https://arxiv.
576     ation for Computational Linguistics (ACL), 2025. URL                  org/abs/2410.01257.
577     https://arxiv.org/abs/2506.05598.
578                                                                          Zhang, L. H., Milli, S., Jusko, K., Smith, J., Amos, B.,
579   Shenfeld, I., Faltings, F., Agrawal, P., and Pacchiano, A.               Bouaziz, W., Revel, M., Kussman, J., Sheynin, Y., Ti-
580     Language model personalization via reward factorization,               tus, L., Radharapu, B., Yu, J., Sarma, V., Rose, K., and
581     2025.                                                                  Nickel, M. Cultivating pluralism in algorithmic mono-
582                                                                            culture: The community alignment dataset. In The Four-
583   Siththaranjan, A., Laidlaw, C., and Hadfield-Menell, D.                  teenth International Conference on Learning Represen-
584      Distributional preference learning: Understanding and                 tations (ICLR), 2026. URL https://arxiv.org/
585      accounting for hidden context in RLHF. In The Twelfth                 abs/2507.09650.
586     International Conference on Learning Representations
                                                                             Zhang, M. J. Q., Wang, Z., Hwang, J. D., Dong, Y., De-
587     (ICLR), 2024. URL https://arxiv.org/abs/
                                                                               lalleau, O., Choi, Y., Choi, E., Ren, X., and Pyatkin, V.
588      2312.08358.
                                                                               Diverging preferences: When do annotators disagree and
589                                                                            do models know? In Proceedings of the 42nd Interna-
      Sorensen, T., Moore, J., Fisher, J., Gordon, M. L.,
590                                                                            tional Conference on Machine Learning (ICML), volume
        Mireshghallah, N., Rytting, C. M., Ye, A., Jiang, L.,
591                                                                            267 of Proceedings of Machine Learning Research, pp.
        Lu, X., Dziri, N., Althoff, T., and Choi, Y. Position:
592                                                                            76193–76212, 2025.
        A roadmap to pluralistic alignment. In Proceedings of
593
        the 41st International Conference on Machine Learning                Zhao, S., Dang, J., and Grover, A. Group preference
594
        (ICML), volume 235 of Proceedings of Machine Learning                  optimization: Few-shot alignment of large language
595
        Research, pp. 46280–46302, 2024.                                       models. In The Twelfth International Conference on
596
597                                                                            Learning Representations (ICLR), 2024. URL https:
      Sorensen, T., Mishra, P., Patel, R., Tessler, M. H., Bakker,             //arxiv.org/abs/2310.11523.
598     M. A., Evans, G., Gabriel, I., Goodman, N., and Rieser, V.
599     Value profiles for encoding human variation. In Proceed-             Zollo, T. P., Siah, A. W. T., Ye, N., Li, A., and Namkoong, H.
600     ings of the 2025 Conference on Empirical Methods in                    PersonalLLM: Tailoring LLMs to individual preferences.
601     Natural Language Processing, pp. 2047–2095, Suzhou,                    In The Thirteenth International Conference on Learning
602     China, 2025. Association for Computational Linguistics.                Representations (ICLR), 2025. URL https://arxiv.
603     doi: 10.18653/v1/2025.emnlp-main.106.                                  org/abs/2409.20296.
604
                                                                        11
                                       What Do Gains in Personalised Reward Modelling Measure?

605   A. Protocols and amendments                                           B. Hypotheses and outcomes
606
607   Chronology and evidential status. - Graded-label stages               Stage 2a (MultiPref, k = 20): H1 DF > D — holds (+0.080);
608   (1–2c, MultiPref, DICES, PRISM graded, code readabil-                 H5 (probit F1 > D, the primary probit contrast after Amend-
609   ity). Rules were frozen before outcomes. The symmet-                  ment 1) — not supported (+0.020 [−0.001, +0.041]; ho-
610   ric offsets DFs were added after the first results and are            moscedastic F − D −0.029), superseded by H1 in Amend-
611   exploratory. - Published methods and positive controls                ment 2; H2 DF > group — holds; H3 DF ≥ low-rank −
612   (Stages 3, 5, 6). Rules were frozen. The dose-response anal-          0.005 — holds under the training-rater prior, not robust
613   yses are exploratory. - CA turn 1. - Stage 8 rule: frozen.            under a few-shot-tuned prior (−0.015); H4 rater scale >
614   - Stages 9–11: exploratory development of the adaptation              rater shift — holds on MultiPref only; H6 symmetric style
615   procedure, after inspecting test results. - Stage 13 S13-1:           model gains likelihood without losing direction accuracy —
616   frozen tests on these previously examined data. Am. 2 and             holds and robust. Replications: H1r, H2r hold on DICES
617   Am. 4 were added after the result. - CA turn 2 (Stage 12)             and PRISM; H3r holds on DICES (robust) and is a tie on
618   and CA turn 3 (S13-3). Frozen procedures, evaluated on                PRISM under the tuned prior. Stage 2b: B1, B2, B3 hold.
619   outcomes not previously analysed. The users are the same              Stage 2c: C1 holds (graded), C2 holds (binary: |DFs − D|
620   people. - MultiPref under the CA procedure (S13-2).                   accuracy −0.0002; all personalisation gains ≤ 0.002 nats),
621   Frozen. The MultiPref data had been analysed earlier with             C3 fails (published latents do not encode style, R2 ≈ 0),
622   other methods.                                                        C4 not met as a conjunction (first part holds, +0.088 over
623                                                                         VPL; second part, non-inferiority to DFs, not established:
      All intervals are nominal and do not account for the earlier
624                                                                         −0.004, lower bound −0.014); Stage 3 (positive control):
      adaptive development.
625                                                                         τ 0 control passes; power at the pre-specified strengths (+1.7,
626   All analyses were specified in timestamped internal                   +5.2 oracle points) not established — no content-interacting
627   protocols (PROTOCOL STAGE1, PROTOCOL STAGE2,                          method’s own − other gain has a lower bound above +1
628   PROTOCOL STAGE2B, PROTOCOL STAGE2C, PROTO-                            point; exploratory dose-response: VPL and PAL-B pass
629   COL STAGE3); stages 2b and 2c were written after the                  at +21 points, none at +10; the split-half content estima-
630   stage-2a results. Changes after a result were logged as num-          tor (S3-C) has no power; with full features (exploratory,
631   bered amendments with the reason; the main ones: the first            Amendment 5) the τ 0 control passes and PAL-B passes at
632   decoding split (a = b = 2) was structurally empty (two rat-           +10 points (k = 20), so the PCA bottleneck explains part
633   ings determine their distribution) and was replaced by a = 3,         of the detection limit. R1 (PRISM native pairwise choices:
634   b = 1; hand-set penalties in the rater–item model over-fitted         every method’s own choice-accuracy gain at k = 20 has an
635   and were replaced by inner cross-validation (which reversed           upper bound < +0.01) holds (largest bound +0.0071, PAL-B
636   an earlier, wrong conclusion that rater shifts do not help);          K = 4).
637   penalty grids were extended when selections fell on grid
                                                                            Scale use and the shared reward model. Training the
638   edges, before any hypothesis was read; the low-rank base-
                                                                            text model jointly with rater offsets and then using the
639   line lacked a constant column and was fixed in its favour; the
                                                                            population-mean offsets (k = 0) does not give a better
640   probit group model had a scale non-identifiability and was
                                                                            consensus model than ordinary training: −0.003 [−0.010,
641   fixed; VPL suffered posterior collapse and its KL weight
                                                                            +0.003] nats on MultiPref (direction +0.3 points, n.s.),
642   was re-selected including 0; PAL-B’s adaptation ridge was
                                                                            −0.022 [−0.037, −0.008] on DICES, +0.001 on PRISM,
643   re-selected by k-shot validation. Every superseded full run
                                                                            −0.009 [−0.016, −0.004] with the LoRA reward model.
644   is kept and reported in the supplementary results; two de-
                                                                            Ordinary training averages scale use out; it matters for pre-
645   bugging smoke runs and one fold whose output was deleted
                                                                            dicting a person, not for learning the content preference.
646   unread when the penalty grids were extended are not. The
647   real-data aspect contrast of §5.7 was revised four times: own         What the offsets encode. In the probit family, rater scale
648   − other; with a style-only control after a first, confounded          matters more than rater shift on MultiPref (+0.036 [+0.020,
649   +0.45 [+0.01, +0.94]; against θ = 0; and against the popu-            +0.057] at k = 20), but rater shift dominates on DICES
650   lation weighting, after the reference learner turned out to           (−0.053) and PRISM (−0.031): leniency/strictness on
651   shrink towards 0 rather than towards the population. The              single-response rating scales, intensity on two-sided prefer-
652   few-shot-tuned low-rank prior was selected at the top of its          ence scales.
653   grid (8192) in most folds; extending the grid to 524,288
                                                                            What this does and does not say about pluralism. Our
654   left every DL result unchanged in substance (real data: own
                                                                            results do not show that people agree about content: the item-
655   − other +0.31 vs +0.30 at k = 20, DFs − DL +0.003 vs
                                                                            level disagreement that replicates across rater panels is real
656   +0.0045; synthetic +5/+10-point panels: +0.10 / +0.09 vs
                                                                            (split-half reliability 0.25 on MultiPref) and about a tenth
657   −0.02 / +0.09).
                                                                            of it is decodable from text. They show that, for predicting
658                                                                         an individual new rater from few ratings, that content-level
659
                                                                       12
                                       What Do Gains in Personalised Reward Modelling Measure?

660   disagreement is a small part of what is predictable, and that         all labels are produced together by the same annotator, so
661   demographic or crowd/expert groups add nothing beyond                 this ceiling concerns a small residual and is a property of
662   the text.                                                             MultiPref’s concurrent labelling.
663
      Fine-tuned and in-context reward models (§5.3, full text).            Even with the rater’s own aspect judgements and all of their
664
      With a LoRA-fine-tuned Qwen2.5-7B reward model (D-                    training ratings, a rater-specific trade-off predicts which
665
      LoRA, trained per fold on the training raters’ rating distri-         response they prefer only 0.1 points better than the popu-
666
      butions) as the text model, the three-number style model              lation’s trade-off, and even fitted in-sample only 0.4 points
667
      still adds +0.100 [+0.071, +0.130] nats per rating at k               better. The reason is that the aspects point in opposite direc-
668
      = 20 — the same as its gain on the frozen-feature head                tions in only 4.0 % of the held-out non-tie comparisons (3.5
669
      (+0.100). Fine-tuning improves the text-only model by                 % of all annotations); there individual trade-offs matter a
670
      +0.027 [+0.016, +0.039] (direction accuracy +1.4 points)              great deal (in-sample +9.7 points; among the 20 raters with
671
      and the style model by the same +0.027: the two gains                 at least ten helpfulness–harmlessness conflicts, the share
672
      add. Personalising the frozen-feature model with 20 rat-              of conflicts resolved in favour of helpfulness ranges from
673
      ings per rater gains more than fine-tuning the text model             0.00 to 0.94), but they are too rare to move overall accuracy.
674
      (+0.072 [+0.041, +0.106]). DFs keeps the direction accuracy           Individual trade-offs do change how strongly raters prefer
675
      of D-LoRA (+0.002 [−0.002, +0.006]). Against in-context               (up to +0.046 nats with all their ratings), in line with the
676
      personalisation — a separate LoRA model on the same base,             calibration-not-ranking pattern. We fixed in advance that
677
      trained with ten of the rater’s other ratings in the prompt           an aspect-weight personalised reward model would be built
678
      and evaluated with the new rater’s k ratings in the prompt            only if the lower bound of this ceiling exceeded half a point
679
      — the three offsets on D-LoRA are better at k = 20. The               with all training ratings; it does not, so we did not build one.
680
      in-context model’s result varies with its training seed (two          The learned personalisers cannot be tested on the conflict
681
      of fifteen runs failed, gaining −0.078 and −0.055 over D-             items either: the 243 held-out non-tie ratings on them give
682
      LoRA against +0.021 to +0.125 for the others; the two failed          own − other intervals wider than the achievable ceiling (k
683
      runs have the highest training loss), so it was trained with          = 20: low-rank latent +0.1 [−2.2, +2.4]). A calibrated test
684
      three seeds per fold, and we fixed in advance that “better”           on the real data. The ceiling above gives each rater’s own
685
      requires a lower bound above zero for every seed and for the          aspect labels; a deployable personaliser would know only
686
      seed average. Averaged over seeds — the expected result of            the item’s aspects. We therefore ran the reference learner
687
      one training run — the offsets are better by +0.041 [+0.027,          of §5.6 on the real labels with the item’s consensus aspect
688
      +0.054] nats per rating (209 raters; per seed +0.062, +0.018          differences from its other annotators as content features
689
      and +0.042, every lower bound at least +0.005) and more               (3-d), with a hierarchical prior centred at the population
690
      accurate on which response the rater prefers (+1.9 points             weighting (estimated on the training raters) and compared
691
      [+0.9, +2.7]). The in-context model does learn from the               each rater’s own weights with that population weighting
692
      history (+0.051 [+0.024, +0.079] over D-LoRA on average),             (style offsets kept). Individual weights transfer worse than
693
      at several thousand prompt tokens per prediction, but its             the population’s: −0.28 [−0.56, −0.06] points at k = 20
694
      direction accuracy is below D-LoRA’s (−1.7 points [−2.6,              and −0.63 [−1.01, −0.25] at k = 50. With injected aspect-
695
      −0.8] on average; −0.6 to −3.0 per seed).                             weight heterogeneity it gives +0.46 [−0.00, +0.96] at k =
696
                                                                            50 when an oracle would gain +1.4 points and +3.4 [+2.6,
697   Value conflicts (§5.7, full text). The positive control asks
                                                                            +4.3] at +5.0. The real data lie well below the +5-point
698   what the methods could detect; MultiPref also lets us ask
                                                                            panel and, at k = 50, just below the +1.4-point panel: for
699   how much there is to detect. Every MultiPref annotation
                                                                            this injection family, the real data lie below panels of one
700   carries the annotator’s own helpfulness, truthfulness and
                                                                            to two oracle points (sensitivity evidence, not a validated
701   harmlessness preferences next to the overall one, so a rater’s
                                                                            upper bound). This test is exploratory and post hoc, and its
702   way of trading these values off is observable. We fit an
                                                                            contrast was revised four times (Appendix A; no version
703   ordinal model of the overall preference from the annota-
                                                                            shows a positive transferable aspect part), the calibration
704   tor’s own aspect labels (their values and absolute values)
                                                                            strengths were chosen after seeing the real bound, it uses
705   with rater-specific cut-points (scale use) and either a pooled
                                                                            one synthetic draw on panels noisier than the real data, and
706   trade-off or a rater-specific trade-off, adapted on k of the
                                                                            it uses other annotators’ aspect labels of the test items (an
707   rater’s training-item annotations and evaluated on held-out
                                                                            aspect oracle, not a deployable model). Three caveats: the
708   items with the rater’s own aspect labels as inputs — an
                                                                            ceiling bounds personalisation of the weighting only — dis-
709   oracle for the content side. The pooled trade-off weights
                                                                            agreement about which response is more helpful or harmless
710   harmlessness most (6.1, five-fold mean), then helpfulness
                                                                            is absorbed into the inputs; it covers content preferences
711   (4.0) and truthfulness (2.0). With the rater’s own aspect
                                                                            expressible through these three aspects only; MultiPref’s
712   labels as inputs the pooled model already gets 97.5 % of
                                                                            prompt sampling determines how often values conflict; and
713   directions right (74 % on conflict items): aspect and over-
714
                                                                       13
                                             What Do Gains in Personalised Reward Modelling Measure?

715   rater ratings used                       rater − pooled trade-off, direction accuracy (points)   log-likelihood per rating   on conflict items (points)
716   k = 20                                   +0.03 [−0.05, +0.12]                                    +0.011 [+0.003, +0.020]     +0.6 [−1.1, +2.4]
717   k = 50                                   +0.06 [−0.09, +0.21]                                    +0.023 [+0.011, +0.037]     +0.3 [−2.7, +3.8]
718   all training items                       +0.10 [−0.24, +0.43]                                    +0.046 [+0.028, +0.068]     +2.0 [−5.0, +9.2]
719   in-sample (fitted on the test items)     +0.44 [+0.27, +0.64]                                    +0.094 [+0.079, +0.112]     +9.7 [+5.6, +14.5]
720
721
722   annotators may have aligned their aspect labels with their                 k = 20). With this stronger detector, the real data lie below
723   overall label, which would understate conflicts.                           the +10-point panels of the injected form at k = 20; at k = 50
724                                                                              they lie below the +5-point panel but the intervals overlap
      Code readability (Stage 10). Pre-set rules: SE-1 (offsets
725                                                                              (comparisons with synthetic panels, not formal exclusion
      transfer) holds on both panels; SE-2 with the low-rank latent:
726                                                                              bounds); the compressed features used for the main tables
      Buse–Weimer inconclusive (own gain in concordance +1.75
727                                                                              make the published methods weaker detectors than they
      [+0.68, +2.78], own − other +0.53 [−0.63, +1.72]; the
728                                                                              need to be.
      text-only model orders snippets at chance, 51.6 %), Dorn
729   degenerate (validation selects the largest penalties, the latent           Positive control (§5.6, full text). No evaluated method met
730   equals the text-only model). SAP-code, own − population /                  the pre-specified detection criterion. In the exploratory dose-
731   own − other: Buse–Weimer k = 20 +0.40 [−0.25, +1.06] /                     response, VPL and PAL-B with PCA-256 features detect
732   +1.57 [+0.89, +2.25], k = 50 +1.30 [+0.46, +2.18] / +2.98                  content preferences worth +21 points but recover less than
733   [+2.00, +3.91]; Dorn k = 10 −0.19 [−0.81, +0.42] / +2.06                   half a point of +10; the low-rank latent, whose user term
734   [+1.49, +2.62] — the rule as worded is met on Dorn through                 interacts with a joint embedding of the comparison, has a
735   own − other, which Stage 5 Am. 4 showed is not on the                      signal at +21 points that stays below the threshold, and with
736   oracle scale, so content personalisation is not claimed. One               the untuned prior it shows nothing up to +5 points either. On
737   within-snippet permutation control gives own − population                  the real data VPL and PAL-B are at the null-control level,
738   −0.38 (Buse–Weimer) and −2.09 (Dorn).                                      and the low-rank latent’s marginal +0.30 [−0.00, +0.60]
739                                                                              is matched by the text-independent offsets (+0.32 [+0.06,
740   Untuned rank-2 comparator (Stage 9 Am. 4). With only
                                                                                 +0.58] on the same contrast), so its aggregate gain is matched
741   its map ridge chosen on training raters’ held-out ratings
                                                                                 by scale use (which can tip a few near-tie predictions) and
742   and z ˜ N(0, I) for new raters, the rank-2 attribute model
                                                                                 does not demonstrate content adaptation. Read together: on
743   gave −2.67 [−3.30, −2.07] (null), +2.20 / +7.36 (semantic),
                                                                                 MultiPref, the real data lie far below the +20-point panels
744   −0.42 (out-of-dictionary) and −2.13 [−2.73, −1.52] (real);
                                                                                 for these methods, while preferences worth up to about
745   tuning its adaptation strength on pseudo-new raters (Am. 8)
                                                                                 10 points cannot be seen by them from 20 ratings, so the
746   removes the losses.
                                                                                 ranking null of §6 says nothing about those. These are
747   SAP with the pre-registered EM update (Stage 9, before                     comparisons with synthetic panels of one injected form, not
748   Amendment 7). own − µ at k = 20: null draws −0.28                          formal exclusion bounds. On the full features (exploratory)
749   . . . +0.05 (k = 50: down to −0.50 [−0.92, −0.09]); seman-                 VPL’s latent collapses (own − other exactly 0), while PAL-
750   tic panels +2.26 . . . +2.79 and +7.30 . . . +8.04; out-of-                B passes the threshold at +10 points but not at +5, and the
751   dictionary +0.41 and +0.81; real MultiPref +0.17 [−0.19,                   real data stay at the null level (+0.11 [−0.16, +0.37]): the
752   +0.55], LL +0.0022 [+0.0003, +0.0041] nats; PRISM native                   real data lie below the +10-point panels of the injected form
753   choices −0.25 [−1.30, +0.83] (EM variances stayed near                     at k = 20 but not below the +5-point panels (Appendix B).
754   their initial value there; with the fixed-point update +0.08               How far are these methods from what the data allow?
755   [−0.86, +1.02]).                                                           A well-specified reference learner — the injection’s two
756                                                                              features known, a per-rater weight vector with an empirical-
757   Positive control on full features (Stage 3, Amendment 5).
                                                                                 Bayes prior, style offsets re-fitted, the same permutation
758   Because the compressed features might be what limits the
                                                                                 contrast — recovers the injected preference from 20 ratings
759   content-interacting methods, we re-ran VPL and PAL-B on
                                                                                 at every strength. On the oracle’s scale (the rater’s own
760   the full features (exploratory). The text-only fits improve (k
                                                                                 weights against the population state, θ = 0 here, with the
761   = 0 log-likelihood: PAL-B −1.533 vs −1.558, VPL −1.495
                                                                                 rater’s style offsets kept) it gains +0.89 [+0.40, +1.37] points
762   vs −1.574), but VPL’s latent then collapses and is unused at
                                                                                 at +1.7 oracle points, +3.1 [+2.3, +4.0] at +5.2 and +8.0
763   every strength (own − other exactly 0), so this check rests
                                                                                 at +10.1, i.e. 52–79 % of the oracle; own − other roughly
764   on PAL-B. Its detection limit drops: it passes the threshold
                                                                                 doubles these numbers, because another rater’s weights are
765   at +10 points; at +5 points its k = 50 gain is positive (+1.05
                                                                                 anti-informative, and is therefore not used for this learner.
766   [+0.37, +1.72]; real data +0.19 [−0.12, +0.48]) but meets
                                                                                 Among the tested strengths, the reference learner crosses
767   the +1-point criterion in only one of four synthetic draws.
                                                                                 the detection criterion between +1.7 and +5.2 points, well
768   The real data stay at the null level (+0.11 [−0.16, +0.37] at
                                                                                 below the methods’. Is the gap in the methods’ inputs or
769
                                                                            14
                                       What Do Gains in Personalised Reward Modelling Measure?

770   in the learners? Linear probes (exploratory, Appendix B)               direction), τ calibrated to oracle gains of +5.1 and +10.4.
771   show the injected direction is available to VPL and PAL-B              Own − other at k = 20 / 50: +0.08 [−0.18, +0.33] / +0.03
772   (out-of-fold R2 0.65 compressed, 1.00 full) but not to the             [−0.29, +0.34] at +5.1; +1.97 [+1.31, +2.65] / +7.02
773   low-rank latent’s joint embedding (0.02); re-injected inside           [+5.84, +8.16] at +10.4; the reference learner is unchanged
774   that embedding, the latent detects +10 points (+1.97 [+1.31,           (own − population +2.67 and +8.33). S7-3, seen-rater
775   +2.65]; originally +0.09; 3 of 4 draws) but not +5 (+0.08;             ceiling on real MultiPref (training raters × test items, 904
776   0 of 4). With the dimension available, the best learners               rater-folds, trained parameters; derangement of training
777   thus detect between +5 and +10 oracle points, the reference            raters): direction accuracy minus the text-only model
778   learner below +5: in these tested settings the limitation lies         −0.51 [−0.88, −0.11] (five offsets), −0.00 [−0.20, +0.18]
779   in finding the dimension rather than in the number of ratings.         (symmetric), −0.42 [−0.81, −0.02] (low-rank); own −
780   With semantic axes (formatting, hedging/refusal) no method             other −0.23, +0.10, −0.11 [−0.57, +0.36]; log-likelihood
781   detects even +9.7 points; the reference learner recovers +7.4          over the text-only model +0.13 nats for all three. By
782   (Appendix B). Results are stable over four synthetic draws,            the rule fixed beforehand, the ranking null also holds
783   and the synthetic panels are noisier than the real data, so the        for seen raters. S7-4 (Amendment 3), semantic axes —
784   calibrations transfer only approximately (Appendix B).                 (s1) log(1 + markdown list/heading lines) of B minus A,
785                                                                          (s2) the same for a fixed list of hedging/refusal phrases
      Positive control: seed variability and realism (Stage
786                                                                          — calibrated to +4.6 and +9.7 oracle points: probes R2
      5). Over four synthetic draws (θ and labels) the reference
787                                                                          0.37–0.66 (formatting) and 0.09–0.24 (hedging); own −
      learner is stable (+2.4 to +3.1 at +5 points, +6.4 to +8.0 at
788                                                                          other at k = 20 / 50 for the low-rank latent +0.09 / +0.05
      +10), PAL-B on full features detects the +10-point panels
789                                                                          and −0.18 / −0.08, VPL −0.05 / +0.04 and +0.03 / +0.03,
      in all four (lower bounds +1.16 to +3.23) and the +5-point
790                                                                          PAL-B (compressed features) −0.24 / −0.12 and +0.27 /
      panels in none (+0.26 to +1.40), and the low-rank latent
791                                                                          +0.40 [−0.02, +0.85]; reference learner own − population
      detects neither in any draw (−0.31 to +0.15). A limitation
792                                                                          +2.57 [+1.61, +3.57] and +7.44 [+5.96, +8.91]. No method
      of all synthetic panels: they are noisier than the real data
793                                                                          detects either panel. S7-5 (Amendment 4), the in-span
      (rater-pair direction agreement 0.59 at τ = 0 against 0.673
794                                                                          panels over four draws (θ and label seeds 1, 11, 12, 13): the
      [0.666, 0.680]; Krippendorff’s α 0.11 against 0.28), and
795                                                                          low-rank latent’s own − other at k = 20 is +1.97, +2.83,
      adding item fixed effects to the generator did not close the
796                                                                          +3.14, +1.44 [+0.92, +1.96] at +9.3 to +10.9 oracle points
      gap (0.60), nor does it reproduce the small effect of style
797                                                                          (detected in 3 of 4; k = 50 +5.0 to +7.3) and +0.00 to +0.14
      offsets on direction (+0.32 real vs −0.07 at τ = 0); the cali-
798                                                                          at +4.7 to +5.5 (0 of 4); the reference learner +7.4 to +8.3
      brations transfer to the real data only approximately, with
799                                                                          and +2.6 to +2.9. Both statements are kept under the rule
      no claimed direction of bias.
800                                                                          fixed beforehand.
801   LoRe on all panels (Stage 6). Across PRISM pairs and
                                                                             Confirmatory and exploratory results. Confirmatory (rule
802   MultiPref, binary and graded labels and k ∈ {5, 20, 50},
                                                                             fixed before the result): the stage-2a hypotheses H1–H5 and
803   LoRe never improves direction or choice accuracy over its
                                                                             their replications (H6, on the symmetric offsets, was added
804   own k = 0 version or over the text-only model (own gain
                                                                             after the first results and is exploratory; its later replications
805   −6.2 to +0.1 points; the regularised version −1.1 to −0.0),
                                                                             were evaluated prospectively); B1–B3; C1–C4; R1 (PRISM
806   and its log-likelihood is below the text-only model’s every-
                                                                             native choices); the Stage-3 positive control at +1.7 and
807   where. Its own − other is positive in some cells (MultiPref
                                                                             +5.2 oracle points (no power); the Stage-4 ceiling rule (not
808   binary, k = 20: +1.3 [+0.5, +2.0]) while its own gain is neg-
                                                                             met); the Stage-6 LoRe rule (PRISM null not withdrawn).
809   ative there (−1.2 [−1.9, −0.5]): another rater’s over-fitted
                                                                             Exploratory (added or changed after a result, labelled in
810   weights are anti-informative, the scale problem discussed
                                                                             the text): the symmetric offsets DFs and their hypothesis;
811   for the reference learner, so own − other alone is not ev-
                                                                             the few-shot-tuned prior; the +10 and +21 panels and the
812   idence of personalisation for methods whose few-shot fit
                                                                             full-feature runs; the reference learner and its oracle-scale
813   over-fits.
                                                                             contrast; the calibrated real-data aspect test; the regularised
814
      Stage 7 (after the seventh review; PROTO-                              LoRe; the two-way bootstrap re-estimates.
815
      COL STAGE7.md). S7-1, cross-fitted ridge probes
816                                                                          Reproducing LoRe’s PRISM result (Stage 6, Amend-
      (prompt-group folds, out-of-fold R2 ) of the two injected
817                                                                          ments 2–3). Unseen-user binary accuracy, mean ± sd over
      features from each learner’s inputs: log length ratio 0.88
818                                                                          five random user splits, LoRe’s native setting (users with at
      (VPL/PAL-B PCA-256 x B − x A), 0.93 (full features),
819                                                                          least six dialogues split 50/50, half of each user’s conversa-
      0.73 (D/DL joint PCA-256); random direction 0.65, 1.00,
820                                                                          tions for few-shot and half for test, one chosen-vs-other pair
      0.02. By the rule fixed beforehand, S7-2 was run for
821                                                                          per conversation; 1,267 users, about three few-shot pairs per
      the low-rank latent only: the random direction re-drawn
822                                                                          unseen user):
      inside its joint embedding (orthogonal to the consensus
823
824
                                                                        15
                                       What Do Gains in Personalised Reward Modelling Measure?

825               embeddings                                      monolithic BT        LoRe, no adaptation     LoRe, few-shot fit
826               Skywork-Reward-Llama-3.1-8B-v0.2 (LoRe’s)       67.4 ± 1.1           67.3 ± 1.8              63.6 ± 3.7
827               Qwen2.5-7B-Instruct (ours)                      67.7 ± 1.5           68.7 ± 1.7              61.0 ± 2.5
828               published (Bose et al., 2025)                   61.0 ± 1.2           —                       71.0 ± 1.0
829
830
831   Taking one pair per interaction instead (every turn; 20 pairs          gains +1.7, +5.2, +10.1 or +21.1 points of direction accuracy
832   per user) gives 58.8 / 59.2 / 57.0 with our features. The              on the test ratings; τ = 0 is a null control. Every method
833   remaining differences — a stronger monolithic baseline here            is then run under the paper’s protocol. Because a method
834   and a few-shot fit that helps there but hurts here — could not         whose unpersonalised state is not the population state can
835   be traced to any setting the LoRe paper reports. Under our             improve with anyone’s ratings, the contrast is the method
836   protocol (user- and conversation-disjoint folds) the Skywork           adapted on the rater’s own k ratings minus the same
837   embeddings leave the conclusion unchanged: LoRe’s own                  method given another test rater’s adapted parameters
838   gain at k = 20 is −1.3 [−2.5, −0.2] points (regularised −0.5           (a random derangement within fold, k and draw). Before
839   [−1.3, +0.2]) and own − other +0.2 [−0.9, +1.2], as with               the runs we fixed that the protocol has power at a strength if
840   our features.                                                          some content-interacting method has a lower 95 % bound
841                                                                          above +1 point at k = 20; the +10 and +21 panels and the
      Positive-control details (moved from §5.6). In the ex-
842                                                                          untuned-prior low-rank runs were added after the first results
      ploratory dose-response, VPL and PAL-B with PCA-256
843                                                                          and are exploratory.
      features detect +21-point preferences but recover less than
844
      half a point of +10; on the real data they are at the null-            5.7 How much room is there? (full text moved from
845
      control level, and the low-rank latent’s +0.30 [−0.00, +0.60]          §5). Every MultiPref annotation carries the annotator’s own
846
      is matched by the text-independent offsets (+0.32), i.e. by            helpfulness, truthfulness and harmlessness preferences, so a
847
      scale use. With full features PAL-B detects +10 points but             rater’s trade-off between these values is observable. With
848
      not +5. How far are these methods from what the data al-               the rater’s own aspect labels as inputs (an oracle for the
849
      low? A well-specified reference learner — the two injected             content side), a pooled trade-off already gets 97.5 % of
850
      features known, an empirical-Bayes prior on each rater’s               directions right, and a rater-specific trade-off fitted on all of
851
      weights, style offsets re-fitted — recovers +0.89 [+0.40,              the rater’s training ratings adds only +0.10 [−0.24, +0.43]
852
      +1.37], +3.1 [+2.3, +4.0] and +8.0 points of +1.7, +5.2 and            points (+0.44 even in-sample). The three recorded aspect
853
      +10.1-point oracle gains from 20 ratings (own versus popu-             judgements point in opposite directions in only 4.0 % of
854
      lation weights, the oracle’s scale). Linear probes show the            held-out non-tie comparisons; there individual trade-offs
855
      injected direction is available to VPL and PAL-B (out-of-              matter (in-sample +9.7 points), but they are too rare to move
856
      fold R2 0.65 compressed, 1.00 full) but not to the low-rank            accuracy. A calibrated test with the item’s consensus aspects
857
      latent’s joint embedding (0.02); re-injected inside that em-           from other annotators finds individual weights transferring
858
      bedding, the latent detects +10 points (3 of 4 draws) but not          worse than the population’s (−0.28 [−0.56, −0.06] at k =
859
      +5 (0 of 4). With semantic axes (formatting, hedging/refusal)          20; exploratory, Appendix B).
860
      no method detects even +9.7 points. Twenty ratings permit
861                                                                          5.9 Developers rating code readability (full text moved
      useful recovery in these injected families when the gen-
862                                                                          from §5). Two code-readability studies have persistent de-
      erating features are supplied; the observed gap implicates
863                                                                          veloper identities: Buse–Weimer (121 raters × 100 Java
      feature representation and the learners’ inductive biases.
864                                                                          snippets) and Dorn (3,393 developers with at least ten rat-
      These are comparisons with synthetic panels of specific
865                                                                          ings of 360 Java/Python/CUDA snippets). With Qwen2.5-
      injected forms (noisier than the real data), not formal ex-
866                                                                          Coder-7B features, scale use transfers to new developers:
      clusion bounds; details and seed variability in Appendix B.
867                                                                          offsets gain +0.054 [+0.036, +0.074] nats per rating at k
      Generator and calibration as first described: We keep Mul-
868                                                                          = 20 (Buse–Weimer) and +0.040 [+0.031, +0.049] at k
      tiPref’s structure (raters, items, who rated what, folds and
869                                                                          = 10 (Dorn). For content we measure within-developer
      k-shot draws) and replace the labels by semi-synthetic ones.
870                                                                          concordance of predicted and given ratings over snippet
      A generator — the text-only head plus scale-use offsets,
871                                                                          pairs, comparing a developer’s own weights with popula-
      fitted on all ratings — gives each rating a distribution, to
872                                                                          tion weights under the same offsets. SAP with 22 classical
      which a rater-specific content term (θr⊤ gi ) (−2, −1, 0, 1, 2)
873                                                                          readability attributes (line and identifier length, indentation,
      is added to the logits; gi are two features of the response
874                                                                          nesting, comments, operators, . . . ) gives +0.40 [−0.25,
      pair (the log length ratio and a random direction in the per-
875                                                                          +1.06] points at the pre-set k = 20 on Buse–Weimer (+1.30
      response embedding space, orthogonal to the consensus
876                                                                          [+0.46, +2.18] at k = 50, exploratory) and −0.19 [−0.81,
      quality direction) and θr ∼ N (0, τ 2 I). The scale τ is cali-
877                                                                          +0.42] on Dorn at its pre-set k = 10; the low-rank latent is in-
      brated on the generator alone so that an oracle that knows θr
878                                                                          conclusive on Buse–Weimer and switched off by validation
879
                                                                        16
                                       What Do Gains in Personalised Reward Modelling Measure?

880   on Dorn. Details, the pre-set rule’s literal outcome on Dorn          bution’s shape and the raw distribution beats its location
881   (met through the own − other contrast, which is not on the            exactly when ρ > 1/2. Text decodability is the proper-
882   oracle scale) and permutation controls are in Appendices              score gain G = (2⟨r̂, r2 ⟩ − ∥r̂∥2 )/n of a residual r̂ decoded
883   A–B.                                                                  from frozen text features, cross-fitted over prompt groups,
884                                                                         reported as the fraction G/X of the reproducible shape.
885   C. Implementation                                                     The rater–item decomposition fits ordered-probit models
886                                                                         Yir∗ = θi + δr + σi σr ε with item locations θi , rater shifts
887   Rater identities. All four panels carry persistent rater iden-        δr , rater scales σr and item dispersions σi , compares held-
888   tifiers (MultiPref pseudonyms, 227 evaluators, median 166             out likelihood over random cells (every held-out rater and
889   ratings, never twice on one item; DICES rater IDs, 123                item appears in training), and chooses all penalties by inner
890   raters × 350 items in the release, 104 after its quality fil-         cross-validation.
891   ter (used throughout); PRISM user IDs, one survey record
                                                                            Reproducibility. With the split-half estimator defined
892   each; Community Alignment annotator IDs). Demographics
                                                                            above, the reliability of the rating distribution’s shape be-
893   never vary within an ID on DICES and in fewer than 0.3 %
                                                                            yond its exact mode and mean is ρ = 0.25 [0.22, 0.29] on
894   of IDs on Community Alignment. On MultiPref, which has
                                                                            MultiPref overall preference with three raters (helpful 0.29,
895   no demographics, an evaluator’s tie rate and extreme-rating
                                                                            harmless 0.21): the raw few-rater distribution forecasts a
896   rate in the first and second half of their ratings (by times-
                                                                            new rater worse than its own location (ρ < 12 ). Text decod-
897   tamp) correlate at 0.82 and 0.78 across evaluators, against
                                                                            ability. A cross-fitted ridge decoder on frozen Qwen2.5-
898   −0.03 and 0.00 (largest 0.17) with evaluator labels shuf-
                                                                            7B-Instruct features, scored on an independent rater panel,
899   fled (check rater ids.py). Shared accounts cannot
                                                                            recovers G/X = 10.5 % [5.7 %, 11.9 %] of the reproducible
900   be ruled out.
                                                                            shape (within-cell permutation control ≤ 0; positive control
901
      Text features: last-token final-layer states of Qwen2.5-7B-           0.35) — comparable to the upper end for ordinal quality
902
      Instruct under a 5-point judge prompt (MultiPref, PRISM)              ratings (upper bounds 0.4–10 %) and below NLI (17–26
903
      or a 3-level safety prompt (DICES), label-free PCA to 256             %). Rater vs item. A long-format ordered-probit decom-
904
      dimensions. Folds: 5 rater folds (stratified by group) paired         position with real rater identities and penalties tuned by
905
      with 5 prompt-group folds (split f holds out rater fold f             inner cross-validation: rater-specific thresholds improve
906
      and prompt-group fold f; the other crossings are not used);           held-out likelihood by +0.036 nats per rating over item lo-
907
      validation: 15 % of training prompt groups. k-shot draws: 5           cation alone, item-specific dispersion by a further +0.0014
908
      per k, identical across all models (RC-LoRA: draw 0 only).            (ratio 25; 19–36 across the five folds); of the rater part, rater
909
      PRISM item folds are by conversation. Bootstrap: rater                scale contributes +0.031 and rater shift +0.005.
910
      clusters, B = 2,000. LoRA: r = 16 on all attention and MLP
911
      projections, lr 10−4 , one epoch, accumulation 8. VPL / PAL-          E. Protocols and what did not hold
912
      B: official architectures (latent 512, hidden 512; d pref 512,
913
      mlp2-gelu projectors, angle learner) with an ordered-logistic         All analyses are documented in an analysis log: times-
914
      link for graded labels; VPL’s KL weight selected from {0.01           tamped internal protocols written before each stage (not
915
      (official), 0.001, 0} and PAL-B’s adaptation ridge by k-shot          public registrations, so they document rather than certify
916
      validation (non-official choices made to prevent collapse             the order of decisions); changes after results are logged as
917
      and over-fitting).                                                    amendments with reasons, and the symmetric style model
918
                                                                            DFs and its hypothesis were added after the first full result.
919
      D. Where is the predictable structure?                                Not supported or not robust: (i) the stage-1 decision rule
920
                                                                            returned “mixed” (text decodability not ≤ 10 %); (ii) non-
921      Estimators and results                                             inferiority of the 5-parameter DF to the low-rank latent (DF
922
      Estimators. For an item with ratings on K ordered lev-                − DL ≥ −0.005) holds with the training-rater prior but not
923
      els, let h be the empirical rating distribution and C the             with a few-shot-tuned prior on MultiPref (−0.015) and is
924
      cumulative operator. Split the item’s raters at random                formally not met on PRISM (bound −0.006); (iii) “scale
925
      into disjoint panels P1 (a raters) and P2 , and let q be a            beats shift” holds only on MultiPref; (iv) the originally reg-
926
      cross-fitted location-only forecast with exactly the mode             istered probit-family hypothesis is not supported (F1 − D =
927
      and mean of P1 (built from other items in the same mode-              +0.020 [−0.001, +0.041], the primary probit contrast after
928
      and-mean cell). With r1 = C(h1 − q), r2 = C(h2 − q),                  Amendment 1; homoscedastic F − D = −0.029 [−0.049,
929
      M = ∥r1 ∥2 /n and X = ⟨r1 , r2 ⟩/n, the forecasting value             −0.008]; superseded when the primary family was moved
930
      of the raw distribution over its own location obeys the iden-         to the distributional head); (v) the prediction that published
931
      tity S(h1 ) − S(q) = M − 2X under the ranked probability              user latents encode style failed (R2 ≈ 0); (vi) the hybrid’s
932
      score, so ρ = X/M is a split-half reliability of the distri-          non-inferiority to DFs is formally not met (bound −0.014).
933
934
                                                                       17
                                       What Do Gains in Personalised Reward Modelling Measure?

935   Four baseline problems found during the study were fixed              causal decomposition, and the matched other is about 0.35
936   in favour of the baselines — a missing constant column in             points worse than the population model (Stage 11 Am. 8).
937   the low-rank latent, a scale non-identifiability in the probit        Two annotators agree on 64.3 % of shared response pairs,
938   group model, VPL’s posterior collapse, and PAL-B’s near-              the text-only model is right on 71.7 % of them. Using the
939   unregularised adaptation — and the runs before each fix are           transferable covariance as the prior (θ̂ u − µ = c Ĉ (I +
940   reported.                                                             c I u Ĉ)−1 s u over length, paragraphs and list/heading, Ĉ
941                                                                         estimated on training users only; S11-3) gives +0.13 [−0.28,
942   F. Community Alignment analysis log (Stages                           +0.53] points at c = 1, although the fitted Gaussian model
943                                                                         implies +2.8 for this learner at k = 20 (oracle +4.2; with
944
         8, 11, 12, 13)                                                     event-level simulated labels that keep one winner per choice
945   The full sequence of analyses behind §6, in order, with the           event, +1.9 and oracle +3.6 — a third lower, just inside the
946   corrections of the fifth review applied (event-level simula-          pre-set factor-1.5 tolerance, Stage 11 Am. 6). The gap is not
947   tion as the principal achievable-gain benchmark, the pair-            mysterious: on the evaluated split transfer from support to
948   level one as a consistency check; Holm as an approximate              test prompts is established for length (0.41 [0.27, 0.55]) but
949   sensitivity analysis). Protocols: PROTOCOL STAGE8.md                  not for paragraphs or lists (intervals cover 0), heavier-tailed
950   (Am. 1–2), PROTOCOL STAGE11.md (Am. 1–10), PRO-                       or concentrated deviations with the same covariance lower
951   TOCOL STAGE12.md.                                                     the simulated gain of this learner to +1.6 to +0.4 (event-level:
952                                                                         +0.9 to −0.4) (so covariance alone does not determine learn-
953   On a dataset built for preference diversity, user-specific            ability; this does not show that concentration explains the
954   signal exists; estimated choice gains remain small. Com-              real data), and the full-size prior over-adapts. With the at-
955   munity Alignment (first turns, 2,957 new users in five coun-          tribute set and prior scale chosen on pseudo-new training
956   tries, the chosen response paired with each other one; Stage          users (c = 0.125–0.25 in every fold, never “no adaptation”),
957   8): at k = 20 every method’s own gain over its own k =                transfer-calibrated adaptation gains +0.49 [+0.20, +0.77]
958   0 version has an upper bound below +0.5 points (VPL                   choice points and +0.0088 [+0.0061, +0.0116] nats on
959   +0.15 [+0.03, +0.27], LoRe-reg +0.35 [+0.25, +0.46], LoRe             the frozen test users, ahead of the tuned rank-2 model by
960   −2.34 [−2.79, −1.88]), yet a user’s own adapted parame-               +0.30 [+0.04, +0.56] points — but not of ordinary validated
961   ters beat another user’s — the frozen rule’s own − other              shrinkage: an isotropic prior over the same three attributes,
962   half, which a summary-script bug first dropped and which              its scale chosen the same way (τ 2 = 0.1 in every fold),
963   therefore literally reads “content personalisation detected”:         gains +0.66 [+0.37, +0.95] points and +0.0110 nats, and
964   LoRe +3.27 [+2.85, +3.70], LoRe-reg +0.36, VPL +0.31.                 TRV − isotropic is −0.17 [−0.29, −0.05] (not significant
965   A within-country derangement (added after the result) re-             after multiplicity adjustment). No advantage of the esti-
966   tains the contrast, so country and language do not explain            mated covariance is established; what helps is the choice of
967   it (own − same-country other +3.22 [+2.83, +3.60]; same-              attributes and strong shrinkage (light adaptation). A prompt-
968   country − any-country +0.03 [−0.12, +0.18]). A cross-                 group × user two-way bootstrap widens TRV’s interval to
969   fitted, simulation-calibrated diagnostic agrees on what the           [+0.01, +0.97]. These are below the one-point threshold, at
970   signal is: users’ deviations from the population weights on           a different budget (20 choice events, three dependent pairs
971   response length and paragraphing reproduce across disjoint            each) from Stage 8’s 20 pairs, where VPL and LoRe-reg
972   prompt sets (transferable variances 0.32 [0.25, 0.40] and             also show small positive own gains. Frozen evaluation on
973   0.72 [0.23, 1.29]; 0.33 and 0.76 [0.26, 1.35] after prompt-           new prompts (Stage 12). TRV, unchanged, on the same
974   type adjustment; exploratory, Stage 11; with 200 simulation           users’ second turns (83,238 never-analysed choices; 1,702
975   replicates the length false-detection rate is 5.0 % [2.4, 9.0]        test users at k = 20 events): +0.38 [+0.13, +0.64] choice
976   and paragraphs’ power 85 % [79, 89], so neither calibra-              points and +0.0046 [+0.0031, +0.0063] nats per pair over
977   tion target is established beyond binomial error), while no           µ; validated isotropic shrinkage +0.31 [+0.05, +0.58] and
978   method converts them into a one-point gain at k ≤ 50. Users’          +0.0038; TRV − isotropic +0.07 [−0.07, +0.22]; the tuned
979   stable prompt mixes could create such residual structure              rank-2 model selects no adaptation in three of five folds
980   without different preferences on the same tasks; as an obser-         (−0.05). By the pre-set rules the benefit is reproducible
981   vational check the length cross-covariance centred within             (both lower bounds above 0) and sub-threshold (accuracy
982   language × prompt-cluster cells is 0.206 [0.183, 0.231]               upper bound below +1), with no advantage over ordinary
983   against 0.210 uncentred, and a same-language user with                shrinkage; the prompt-group × user interval for accuracy
984   a matched task mix (cluster shares within L1 0.002) is a              covers 0 ([−0.04, +0.83]). No language reaches signifi-
985   worse predictor than the user’s own coefficient by +0.80              cance alone. The length cross-moment again reproduces
986   [+0.45, +1.16] points and +0.009 nats, though better than             across disjoint prompt halves in every fold (0.12–0.19), the
987   a random other by +0.75; the two contrasts approximately              list/heading one does not (negative in two folds). These are
988   partition the unmatched own − other (+1.54), which is not a           new prompts and turns of previously studied users, not new
989
                                                                       18
                                        What Do Gains in Personalised Reward Modelling Measure?

990    users. Multiplicity (Am. 10; an approximate, exploratory               incomplete history excluded, Am. 5); the pre-set rule re-
991    sensitivity analysis: p-values recovered from reported                 quires both accuracy and log-likelihood lower bounds above
992    intervals by a symmetric normal approximation, ques-                   0. Turn 4 was not opened.
993    tionable for heavy-tailed cross-moments, then Holm at
994    0.05). In Stage 8’s frozen family (six methods × two con-              G. Screened attribute personalisation
995    trasts) the own − other contrasts of LoRe, LoRe-reg, VPL
996    and PAL4 survive, and the detection is unchanged; the posi-
                                                                                 (formerly §5.8)
997    tive own gain of VPL (+0.15) and the negative own effects              In the tested settings §5.6 points to where the failure lies:
998    of PAL4 and DFp do not. Across a family of 29 selected                 20 ratings suffice when the content axes are known, and the
999    Stage-11 contrasts (not every reported contrast; e.g. AUC              published learners, as evaluated, do not find them. Screened
1000   contrasts, the k = 32 within-cluster and matched − cyclic              attribute personalisation (SAP) supplies candidate axes
1001   contrasts are omitted), the length statements survive (trans-          and learns from the training raters which of them people
1002   fer, within-cluster transfer, own − matched other, TRV and             differ on. Each comparison is described by 24 interpretable
1003   isotropic gains, WIMHF-style length), while paragraphs’                attribute differences fixed in advance (length, markdown
1004   transferable variance, TRV − rank-2, TRV − isotropic and               structure, hedging/refusal, code, digits, questions, pronouns,
1005   the new-user length gain of S11-1 (b) (+0.45) do not; the              sentence and word length, examples, disclaimers, sum-
1006   first-turn evidence that isotropic shrinkage beats TRV is              maries, evidence phrases, politeness, refusal, lexical diver-
1007   therefore weaker, but no advantage of TRV is established               sity, overlap with the prompt, . . . ); a rater’s content term
1008   either. Status: the original Stage 11 diagnostic failed its            (θr⊤ ai )(−2, . . . , 2) is added to the scale-use model’s logits,
1009   pre-specified calibration criterion, leaving all three primary         with θr ∼ N (µ, diag σ 2 ), the population weights µ and the
1010   outcomes inconclusive and the adaptation gate unmet; all               per-attribute variances σ 2 estimated on the training raters
1011   subsequent analyses are exploratory; the final procedure se-           by automatic relevance determination (Laplace approxima-
1012   lected attributes and shrinkage on training users only, but its        tion, MacKay’s fixed-point update); a new rater’s θr is their
1013   candidate family was developed after inspecting test results,          MAP from k ratings. The contrast is the rater’s own weights
1014   and the bootstrap intervals are nominal and do not account             against the population weights µ, with the rater’s own scale-
1015   for this adaptation. Ĉ is an uncentred cross-moment of one-           use offsets kept (oracle scale).
1016   step deviations, not a bounded share of the fitted random-
1017   slope variance; the principal achievable-gain benchmark is             Own minus population weights, direction accuracy at k = 20
1018   the event-level simulation (one winner per choice event, Am.           in points, 95 % rater bootstrap (ranges over four synthetic
1019   6); the pair-level figures are a consistency check, and both           draws; VPL / PAL-B / low-rank latent: own − other on the
1020   are model-implied gains for specified learners, not general            same panels, §5.6). Rules fixed in advance: no detection
1021   learnability ceilings.                                                 on the null draws (none), detection of the semantic panels
1022                                                                          in at least three of four draws (four of four each). The
       Stage 13 methods (PROTOCOL STAGE13.md). S13-                           SAP column uses the fixed-point variance update adopted
1023
       1: an item is an exact (prompt, ordered four-response)                 after the pre-registered EM update was found to stall when
1024
       identity on CA first turns; for each pair of same-fold test            raters have few ratings (EM results in Appendix B); the
1025
       users who chose different responses a ̸= b on an item,                 shared-variance column uses the same update; the rank-
1026
       S = (δu − δv )⊤ (xa − xb ) with δ the adapted minus popula-            2 model’s map ridge and adaptation strength (including
1027
       tion attribute weights (population terms cancel); assignment           none) are selected on held-out training raters at k = 20.
1028
       log-score log σ(S) − log 12 , averaged over 5 support draws,           Exploratory: the ablations and the out-of-dictionary panels.
1029
       within item, then over items; two-way item × user bootstrap
1030                                                                          SAP recovers what the published learners miss and matches
       (B = 1,000). Learners: the Stage-12 isotropic procedure
1031                                                                          the learner told the features; attribute-specific variances
       (primary) and TRV, selected on pseudo-new training users;
1032                                                                          improve recovery over one shared variance under the same
       20 support events in training prompt groups. S13-2: the
1033                                                                          update (which loses 60–76 % of the gain); a rank-2 subspace
       same procedures frozen on MultiPref binary directions (ties
1034                                                                          on the same attributes, tuned with the same care, matches
       excluded), Stage-1 folds, rater and rater × prompt-group
1035                                                                          SAP on the semantic panels and abstains on the null (un-
       bootstraps. S13-3: each user’s first-turn isotropic deviation
1036                                                                          tuned, it lost 2.1–2.7 points; Appendix B), while on real
       (20 support events, draw 0) is frozen in first-turn attribute
1037                                                                          MultiPref SAP is ahead of it by +0.41 [+0.15, +0.66] points
       units and added, without rescaling or tuning, to a third-turn
1038                                                                          (paired, exploratory). The variance assigned to correlated
       population model (ridge on history-conditioned Qwen2.5-
1039                                                                          attributes means the high-variance set is a set of candidates,
       7B features of the transcript through the third prompt, trun-
1040                                                                          not independently identified preference dimensions. SAP
       cated to the last 6,000 characters, plus per-language µ) fitted
1041                                                                          learns transferable shrinkage over supplied axes; it does not
       on other users’ third turns; scored on the user’s third turns
1042                                                                          discover new ones (outside the dictionary it recovers under
       outside the support conversations (≥ 5 events; turns with
1043                                                                          a tenth of a +10.5-point preference). With the fixed-point
1044
                                                                         19
                                                 What Do Gains in Personalised Reward Modelling Measure?

1045
     Table 6. SAP: own − µ direction (CA: choice) accuracy in points, k = 20, the rater’s scale-use offsets kept. Rank-2: the same attributes in
1046
     a tuned rank-2 subspace; DL: low-rank latent; reference: learner given the generating features. Ranges over 4 synthetic draws.
1047
     panel (oracle gain)                  SAP                                       one shared variance  rank-2, same attributes VPL / PAL-B / DL reference
1048
     null, 4 draws (0)                    −0.03 . . . +0.04                         +0.06                0 (abstains)            —                —
1049 formatting + hedging (+4.6), 4 draws +2.29 . . . +2.82                         +0.69 [+0.21, +1.18] +2.78 [+1.84, +3.72]    ≤ +0.09          +2.57 [+1.61, +3.57]
1050 formatting + hedging (+9.7), 4 draws +7.44 . . . +8.12                         +3.09 [+2.13, +4.02] +7.75 [+6.09, +9.36]    ≤ +0.27          +7.44 [+5.96, +8.91]
     two axes outside dictionary (+10.5)  +0.95 [+0.50, +1.39]                      —                    —                       —                —
1051 real MultiPref                       +0.28 [−0.00, +0.58]                      +0.28 [+0.04, +0.53] −0.14 [−0.51, +0.24] —                   —
1052 real MultiPref, permuted in item     −0.09 [−0.23, +0.05]                      —                    —                       —                —
     CA, frozen, k = 20 events            0 (abstains); forced −0.40 [−0.87, +0.06] −0.70 [−1.15, −0.25] +0.17 [−0.17, +0.51] —                   —
1053
1054
1055
     update its estimated effects on the four null draws are near
1056
     zero (−0.03 . . . +0.11 at k = 20 and 50; with EM it lost up
1057
     to 0.5 points at k = 50); this is not a calibrated false-positive
1058
     rate, and forced adaptation does hurt on Community Align-
1059
     ment (below). On real MultiPref its gain over population
1060
     attribute weights (the rater’s offsets kept) is +0.28 [−0.00,
1061
     +0.58] direction points and +0.0028 [+0.0013, +0.0043]
1062
     nats per rating — SAP’s achieved gain under this proto-
1063
     col, not a bound on what these attributes could offer. The
1064
     decisive test was frozen before its data were embedded:
1065
     Community Alignment’s native choices (1,897 new users
1066
     in five languages, k = 20 choice events, per-language popu-
1067
     lation weights, adaptation strength of every method chosen
1068
     on held-out training users). The fitted model assigns sub-
1069
     stantial training-user variation to length, paragraphs and
1070
     formatting (prior variances 0.29–0.37 for length, 0.25–0.30
1071
     for paragraphs, 0.19–0.23 for list/heading lines; one fold
1072
     assigns 1.37 to URLs, ≈ 0 in the others), yet adaptation
1073
     from 20 choice events does not improve held-out prediction:
1074
     validation switches SAP off in all five folds, forcing it costs
1075
     −0.40 [−0.87, +0.06] choice points and −0.0097 [−0.0143,
1076
     −0.0052] nats, and the tuned low-rank model gains +0.17
1077
     [−0.17, +0.51]. The pre-set rule (lower bound above +1
1078
     point) is not met.
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
                                                                                    20
