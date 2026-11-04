You are reviewing the typeset ICML-format PDF (extracted with pdftotext -layout) of a paper on what gains in personalised reward modelling measure. This is round 9; round 8 asked for claim cleanup and an 8-page main text, which has been applied. Please do a submission-readiness read of the typeset text, focusing on:
1. Any number in the main text (pages 1-8) that is inconsistent with another place in the paper (main text vs tables vs appendices).
2. Any remaining overclaim, especially about S13-3 transport, positive controls, and the TRV vs isotropic comparison.
3. Typesetting defects visible in the extracted text: missing headings, broken math, garbled symbols, orphaned table fragments, undefined references (??), broken citations.
4. The three most important changes a reviewer at ICML would still ask for, ranked, and whether each is fixable without new experiments.
Be concrete: quote the offending text and give its page.

=== PAPER TEXT ===
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
095   DICES raters (Homan et al., 2024) predict individual an-               ing distribution that replicates across disjoint rater panels is
096   notators. Preference strength enters reward training as a              small (split-half reliability 0.25), and about a tenth of it is
097   margin (Touvron et al., 2023; Wang et al., 2025); ties have            decodable from text. Beyond item location, the predictable
098   classical paired-comparison models (Rao & Kupper, 1967;                structure is therefore mostly rater-side scale use, while the
099   Davidson, 1970). Personalised reward models infer a user               item-level shape that replicates across disjoint panels is
100   latent from a few examples (Poddar et al., 2024; Chen et al.,          small and only partly in the text. These two facts come from
101   2025), use a low-rank reward subspace (Bose et al., 2025),             different estimands and do not say that disagreement is “not
102   persona prompts induced from history (Ryan et al., 2025),              in the text”. The stage-1 decision rule we had written down
103   per-user embeddings (Li et al., 2024), combinations of base            returned “mixed”, because G/X was not ≤ 10 % (interval
104   rewards (Shenfeld et al., 2025; Luo et al., 2025) or neural            5.7–11.9 %); the factorised model of §4 was chosen with
105   processes (Kobalczyk et al., 2024); others personalise the             that outcome known.
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
125   offsets are text-independent: they reshape how strongly a rater is predicted to prefer, not which side.
126
127   4. A three-parameter scale-use baseline                                          5. Experiments
128
129   (Figure 2 illustrates the effect of the offsets.) Let ℓ(x) ∈ RˆK                 Protocol. 5 folds; in each, 20 % of raters (stratified by
130   be the class logits of a text-only distributional reward model                   group) and 20 % of prompt groups are held out; models are
131   for item x (K ordered rating levels). For rater r we add a text-                 trained on training raters × training items with penalties
132   independent offset vector: p(y | x, r) = softmax(ℓ(x) + b r).                    chosen on a validation split; each test rater is adapted on
133   Variants: DF (b r ∈ RˆK, free), DFs (two-sided preference                        k ∈ {0, 5, 10, 20, 50} of their ratings of training items (5
134   scales only: b r tied symmetrically, (e, s, t, s, e) — extreme,                  random draws) and evaluated on their ratings of held-out
135   slight, tie — 3 parameters, of which 2 are identifiable be-                      items. Primary metric: held-out log-likelihood per rating;
136   cause the softmax is invariant to a common shift; no A-vs-B                      also RPS and preference-direction accuracy; rater-cluster
137   position term). Rater offsets have a Gaussian prior centred                      bootstrap (B = 2,000). Because test raters share test items
138   on the training-rater mean; a new rater’s offsets are the MAP                    on MultiPref and DICES, the headline k = 20 contrasts
139   estimate from k of their ratings with the text model frozen.                     were also re-estimated with a two-way bootstrap that resam-
140   Baselines under the same protocol: D (text-only distribu-                        ples raters and prompt groups independently: on graded
141   tional RM), DG (group offsets: crowd/expert, race, region),                      labels every log-likelihood interval widens by at most 0.007
142   DL (low-rank text-interacting latent: ℓ(x) + (Wx + w0 )·z r,                     on either side and no log-likelihood conclusion changes;
143   d = 8, the personalised-RM family). An interpretable probit                      direction-accuracy differences of about a point or less (the
144   family (rater shift / log-scale on an ordered-probit text head)                  style model’s +0.5 on MultiPref, VPL’s direction advantage
145   is reported as a secondary analysis.                                             over the style model) lose significance and are marked where
146                                                                                    they appear. Text model in §5.1–5.2: frozen Qwen2.5-7B
      Training and adaptation. The text model and the train-
147                                                                                    features with a ridge head; §5.3: a LoRA-fine-tuned reward
      ing raters’ offsets are fitted jointly by penalised maximum
148                                                                                    model.
      likelihood,
149
150                                                                                    5.1. Main result (MultiPref)
             ∑︂                                          ∑︂
       min        − log p(y | xi , r) + λtext ∥V ∥2 + λr    ∥br ∥2 ,
151               (i,r,y)                                           r
152                                                                                    Figure 1 shows the gain over the text-only reward model as a
153                                                                                    function of k on all three datasets. In the table, DF/DFs/DG
      with λtext chosen on the text-only model and λr on
154                                                                                    use the training-rater prior and DL and the DFs − DL col-
      held-out items of the training raters. A new rater
                                                                                       umn use the few-shot-tuned prior (the DFs − DL contrast is
155   r∗ is adapted      from k ratings {(xj , yj )} by b̂r∗ =
156                                                                                    post hoc).
      arg minb j − log softmax(ℓ(xj )+b)yj +λr ∥b−b̄∥2 , with
                 ∑︁
157   b̄ the training-rater mean (the prior mean; b̂ = b̄ at k = 0)                    Preference-direction accuracy (D: 0.674): DFs +0.005
158   and the text model frozen — a convex problem in 3–5 param-                       [+0.001, +0.008] at k = 20 (not significant once items are
159   eters, solved in milliseconds. Any text model that outputs                       also resampled: [−0.001, +0.011]); DF −0.014 [−0.020,
160   graded log-probabilities can be used: we use a ridge head on                     −0.007]. A three-number style model gains as much as a
161   frozen LLM features (§5.1–5.2), a LoRA-fine-tuned LLM                            tuned 8-dimensional text-interacting latent (tie at k = 20)
162   reward model (§5.3) and the decoder of a published person-                       and more at k = 5, 10 and 50; fitting a rater’s A-vs-B position
163   alised reward model (§5.4).                                                      from few ratings costs direction accuracy.
164
                                                                                 3
                                                            What Do Gains in Personalised Reward Modelling Measure?

165                                    MultiPref (pairwise preference)                 DICES-350 (safety)                       PRISM (response ratings)
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
175                                    0 5 10 20                      50       0 5 10 20                      50            0 5 10 20                      50
176                                      ratings of the new rater (k)            ratings of the new rater (k)                 ratings of the new rater (k)
177
178                                style offsets, symmetric (DFs)        style offsets (DF)            low-rank latent (DL, tuned)         group offsets (DG)
179
180
181   Figure 2. New raters: gain in held-out log-likelihood per rating over the text-only distributional reward model (D), as a function of the
182   number k of the new rater’s ratings used for adaptation; 95% rater-cluster bootstrap bands, 5 folds. Text-independent rater offsets (DF;
183   symmetric three-parameter DFs on two-sided preferences) gain 0.08–0.10 nats per rating at k = 20 on all three datasets; group offsets
184   (crowd/expert, race, region) gain nothing; a low-rank text-interacting rater latent with a few-shot-tuned prior ties the three-parameter DFs
185   and beats the five-offset DF on MultiPref (DF − DL = −0.015). DF, DFs and DG use the training-rater prior; DL the few-shot-tuned prior.
186
187            k                 DF − D                      DFs − D                    DG − D         DL − D (tuned prior)          DFs − DL (tuned, post hoc)
188            5                 +0.028 [+0.012, +0.044]     +0.048 [+0.029, +0.070]    ≈0             +0.023 [−0.002, +0.047]       +0.026 [+0.016, +0.037]
189            20                +0.080 [+0.055, +0.106]     +0.100 [+0.074, +0.128]    ≈0             +0.095 [+0.069, +0.122]       +0.0045 [−0.0004, +0.0092]
190            50                +0.114 [+0.087, +0.142]     +0.128 [+0.101, +0.156]    ≈0             +0.120                        +0.007 [+0.002, +0.013]
191
192
193   Reference points. To size these gains: on MultiPref at k                                    head — and the gains of fine-tuning and of personalisation
194   = 20 a uniform forecast scores −1.609 nats per rating, a                                    add. Against in-context personalisation (a LoRA model
195   forecast that ignores the text and uses only the new rater’s 20                             given the rater’s k ratings in the prompt, three seeds per
196   ratings −1.487, the text-only model −1.441, the text model                                  fold) the offsets are better by +0.041 [+0.027, +0.054] nats
197   with the three offsets −1.342, and offsets fitted in-sample                                 and +1.9 [+0.9, +2.7] direction points (Appendix B).
198   on all of the rater’s held-out ratings (an optimistic ceiling
199   for text-independent offsets) −1.262. Twenty ratings of a                                   5.4. Published personalised reward models
200   person, without the text, recover 73 % of the text model’s
      gain over uniform; the offsets close 56 % of the gap between                                We reimplemented VPL (Poddar et al., 2024) and PAL-B
201
      the text-only model and the in-sample ceiling. On DICES                                     (Chen et al., 2025) from their official code as heads on
202
      the rater’s ratings alone predict better than the text alone                                the same frozen per-response embeddings and evaluated
203
      (−0.766 vs −0.840 at k = 20). Even the in-sample ceiling                                    them under the same new-rater protocol, refitting the text-
204
      raises MultiPref direction accuracy by only 1.3 points (0.674                               only and style models on those embeddings. On graded
205
      → 0.687), confirming that text-independent offsets cannot                                   labels, at k = 20 the style model is better than VPL by
206
      carry ranking.                                                                              +0.092 [+0.068, +0.119] nats per rating ([+0.063, +0.124]
207
                                                                                                  when prompt groups are also resampled) and than PAL-B by
208
                                                                                                  +0.158. VPL’s latent does carry rater information once its
209   5.2. Replications (k = 20)
                                                                                                  posterior collapse is prevented (KL weight selected as 0 or
210
      DF − D and DG − D use the training-rater prior, DF −                                        0.001; +0.087 over its own unpersonalised version), but only
211
      DL the few-shot-tuned prior. Direction accuracy on PRISM                                    lifts it to the level of the text-only model; PAL-B’s few-shot
212
      means good-vs-bad around the scale midpoint.                                                user weights give no gain. Their user representations are
213
                                                                                                  unrelated to response style (cross-validated R2 ≈ 0 against
214
      5.3. On a fine-tuned reward model                                                           the style offsets). On binary labels — the setting in which
215
                                                                                                  both methods were proposed — every method’s personalisa-
216   With a LoRA-fine-tuned Qwen2.5-7B reward model as                                           tion gain is at most 0.002 nats (small but nonzero for PAL-B
217   the text model, the three offsets still add +0.100 [+0.071,                                 with K = 4, and for VPL and the style model at k = 50), and
218   +0.130] nats per rating at k = 20 — as on the frozen-feature
219
                                                                                              4
                                       What Do Gains in Personalised Reward Modelling Measure?

220   dataset               DF − D                    DG − D (groups)         DF − DL (tuned prior)
221   DICES-350 (safety)    +0.089 [+0.064, +0.117]   −0.006 (race)           +0.037 [+0.022, +0.053]
222   PRISM (ratings)       +0.080 [+0.071, +0.090]   +0.003 (region)         −0.001 [−0.006, +0.003] (formally not non-inferior: bound −0.006 < −0.005)
223
224
225   VPL’s text head is the best binary model (the style model is          +1 point at k = 20; the +10 and +21 panels are exploratory.
226   0.010 nats behind it and 0.005 behind the text-only model,
227                                                                         Own minus another rater’s k = 20 ratings, direction accuracy
      differences of the size of item-sampling noise): on these
228                                                                         in points, 95 % rater bootstrap; 209 new raters, 5 folds.
      panels the largest demonstrated gains are captured by cali-
229                                                                         The low-rank latent uses the few-shot-tuned prior. k = 50
      bration of graded levels and ties, which binary preference
230                                                                         contrasts use the 180 of 209 raters with at least 50 training-
      data discard. VPL’s per-response reward head is slightly
231                                                                         item ratings. PAL-B’s own − other contrast is negative with
      better at predicting which response is preferred (0.677 vs
232                                                                         compressed features (null control −0.23, real data −0.43):
      0.668), an effect present without personalisation and not sig-
233                                                                         its per-rater adaptation adds noise there; with full features
      nificant once prompt groups are also resampled (style model
234                                                                         it is at zero (−0.04, +0.11). The injection uses one draw
      − VPL: −0.9 points [−2.7, +0.8]). The offsets are also a
235                                                                         of θ and of the labels, so seed variability of the synthetic
      plug-in: added to VPL (fitted on the same k ratings, VPL
236                                                                         panels is not in the intervals. Last column: PAL-B on the
      frozen) they improve it by +0.088 [+0.066, +0.111] nats
237                                                                         full 3,584-dimensional features instead of their PCA-256
      per rating at k = 20, tie with the style model on likelihood
238                                                                         (exploratory; τ 2 not run).
      (−0.004 [−0.014, +0.005]) and keep VPL’s direction accu-
239   racy (+1.1 points over the style model alone; rater bootstrap         No method has power at the pre-specified strengths. In
240   only).                                                                the exploratory dose-response, VPL and PAL-B detect +21-
241                                                                         point preferences but recover less than half a point of +10;
242   5.5. Summary of baselines (MultiPref, new raters, k =                 on real data they are at the null-control level, and the
243        20)                                                              low-rank latent’s +0.30 [−0.00, +0.60] is matched by the
244                                                                         text-independent offsets (+0.32). A reference learner that
245   Gains are relative to each block’s text-only model (D, Dp,            is given the two injected features recovers +0.89 [+0.40,
246   D-LoRA); the LoRA block uses adaptation draw 0 only (the              +1.37], +3.1 and +8.0 points of the +1.7, +5.2 and +10.1-
247   draw the in-context model was evaluated on), hence the                point oracle gains from 20 ratings, so twenty ratings permit
248   style model’s +0.092 here against +0.100 averaged over five           recovery in these injected families when the generating fea-
249   draws in §5.3.                                                        tures are supplied; the gap implicates representation and
250   Rows within a block share the text model and the raters;              inductive bias (probes, re-injection and semantic axes in Ap-
251   across blocks the text models differ (text-only direction             pendix B). These results characterise recovery for specified
252   accuracy 0.674 / 0.670 / 0.688). VPL’s and PAL-B’s own                injected families on panels noisier than the real data; they
253   gains over their unpersonalised versions are +0.087 and               are not formal exclusion bounds.
254   −0.000.
255                                                                         5.7. How much room is there? Conflicts among aspect
256   5.6. Could these methods have detected content                             judgements are rare
257        personalisation? A semi-synthetic positive control
258                                                                         With the rater’s own helpfulness, truthfulness and harm-
259   A ranking null is informative only if the methods would               lessness labels as inputs, a pooled trade-off gets 97.5 % of
260   detect content-dependent preferences where they exist. We             MultiPref directions right and a rater-specific one adds only
261   keep MultiPref’s raters, items, folds and k-shot draws and            +0.10 [−0.24, +0.43] points: the three aspect judgements
262   replace the labels by semi-synthetic ones: a generator                conflict in only 4.0 % of held-out comparisons (details in
263   (the text-only head plus scale-use offsets) gives each rat-           Appendix B).
264   ing a distribution, to which a rater-specific content term
265   (θr⊤ gi ) (−2, −1, 0, 1, 2) is added; gi are two response-pair        5.8. A learner that finds the axes
266   features (log length ratio and a random embedding direction
                                                                            A screened empirical-Bayes learner over 24 interpretable
267   orthogonal to consensus quality), θr ∼ N (0, τ 2 I), and τ
                                                                            attribute differences (SAP) recovers the semi-synthetic con-
268   is calibrated so that an oracle knowing θr gains +1.7, +5.2,
                                                                            tent preferences that the published learners miss, with near-
269   +10.1 or +21.1 direction points (τ = 0: null control). The
                                                                            zero effects on null panels, and abstains on real MultiPref
270   contrast is own adapted parameters minus another test
                                                                            under a prospectively specified rule (+0.28 [−0.00, +0.58]
271   rater’s (a derangement within fold, k and draw). We fixed
                                                                            points at k = 20). Details: Appendix G.
272   beforehand that the protocol has power at a strength if some
273   content-interacting method has a lower 95 % bound above
274
                                                                        5
                                         What Do Gains in Personalised Reward Modelling Measure?

275   text model                                    personalisation                                                  gain in LL per rating vs the block’s text-only
276   frozen features (joint item embedding)        group offsets (crowd / expert)                                   ≈0
277                                                 low-rank latent, tuned prior                                     +0.095 [+0.069, +0.122]
278                                                 style offsets, 3 numbers (DFs)                                   +0.100 [+0.074, +0.128]
279   frozen features (per-response embeddings)     VPL (reimplemented)                                              +0.002 [−0.008, +0.012]
280                                                 PAL-B (reimplemented)                                            −0.065 (worse)
                                                    DFs                                                              +0.094 [+0.069, +0.120]
281                                                 VPL + style offsets                                              +0.090
282   LoRA-fine-tuned Qwen2.5-7B (209 raters)       in-context rater history (RC-LoRA, mean of 3 training seeds)     +0.051 [+0.024, +0.079]
283                                                 DFs                                                              +0.092 [+0.063, +0.125]
284
285   panel                          oracle gain   low-rank latent (DL)       VPL                     PAL-B                    PAL-B, full features
286
      null control (τ = 0)           0             −0.10 [−0.38, +0.17]       −0.04 [−0.08, +0.01]    −0.23 [−0.45, +0.00]     −0.04 [−0.25, +0.17]
287
      injected, τ 2                  +1.7          −0.01 [−0.29, +0.26]       +0.01 [−0.07, +0.10]    −0.10 [−0.36, +0.15]     —
288   injected, τ 5                  +5.2          −0.02 [−0.28, +0.26]       +0.01 [+0.00, +0.03]    +0.23 [−0.04, +0.51]     +0.26 [−0.14, +0.66]
289   injected, τ 10 (exploratory)   +10.1         +0.09 [−0.18, +0.36]       +0.27 [+0.02, +0.54]    +0.42 [−0.08, +0.96]     +1.95 [+1.16, +2.74]
290   injected, τ 20 (exploratory)   +21.1         +1.47 [+0.83, +2.18]       +6.92 [+5.63, +8.30]    +4.62 [+3.47, +5.78]     +8.13 [+6.54, +9.77]
291   real MultiPref                 —             +0.30 [−0.00, +0.60]       −0.01 [−0.04, +0.02]    −0.43 [−0.72, −0.15]     +0.11 [−0.16, +0.37]
292
293
294   5.9. Developers rating code readability                                 direction accuracy on MultiPref (0.674) is already as high as
295                                                                           the agreement in direction between two human raters of the
      On two code-readability studies with persistent developer
296                                                                           same item (0.673 [0.666, 0.680]): a population model pre-
      identities (Buse–Weimer, 121 raters; Dorn, 3,393 develop-
297                                                                           dicts a new rater about as well as another person does. Seen
      ers) and Qwen2.5-Coder-7B features, scale use transfers to
298                                                                           raters. With all their training ratings (median 134), training
      new developers (offsets +0.054 [+0.036, +0.074] nats per
299                                                                           raters’ own parameters beat another rater’s by −0.11 [−0.57,
      rating at k = 20 and +0.040 [+0.031, +0.049] at k = 10),
300                                                                           +0.36] direction points for the low-rank latent (offsets +0.10,
      while content adaptation over 22 readability attributes is
301                                                                           −0.23): the ranking null is not specific to few-shot adap-
      inconclusive at the pre-set k = 20 (+0.40 [−0.25, +1.06]
302                                                                           tation (exploratory, Appendix B). Against its own k = 0
      and −0.19 [−0.81, +0.42] concordance points; Appendices
303                                                                           version, no method’s direction accuracy on MultiPref rises
      A–B).
304                                                                           by more than 0.2 points at k = 20, and every upper 95 %
305                                                                           bound stays below +0.8 points even when prompt groups are
306   6. What personalisation buys: graded-rating                             resampled together with raters (VPL +0.07 [−0.57, +0.74],
307      prediction, user signal, and small choice                            style model −0.10 [−0.69, +0.54], PAL-B −0.48 [−1.11,
308      gains                                                                +0.14]). The ranking null replicates on real users’ own
309                                                                           choices. PRISM users each saw 2–4 responses to their own
310   Binarisation removes the symmetric scale-use term; eval-                prompt, scored them and chose one; pairing the chosen re-
311   uated adaptation gains on MultiPref are small. On Multi-                sponse with every other one gives 41,199 native pairwise
312   Pref with ties dropped and labels binarised, every evaluated            choices of 1,396 users. Under the same new-user protocol
313   method’s personalisation gain is at most 0.002 nats per rat-            (5 user folds × 5 conversation folds, k of the user’s pairs
314   ing (§5.4), and the scale-use baseline’s binary accuracy is             from training conversations), we fixed before any result that
315   essentially unchanged from the text-only model’s. On these              the ranking null would be stated only if every method’s
316   graded panels the largest demonstrated gains concern graded             improvement in choice accuracy over its own k = 0 version
317   levels and ties — which binary preference data, the format              had an upper 95 % bound below one point at k = 20. It
318   in which most personalised reward models are trained and                holds for all of them (1,033 new users at k = 0; the 669
319   evaluated, discard (Community Alignment shows that bi-                  with at least 20 adaptation pairs at k = 20): VPL +0.12
320   nary choices can also carry predictable user differences, §6).          points [−0.08, +0.33], PAL-B +0.0 [−0.4, +0.4] (K = 2)
321   Ranking moves little. Symmetric offsets mainly change                   and +0.3 [−0.1, +0.7] (K = 4), the 5-offset model −0.6
322   how strongly a rater is predicted to prefer a response: on              [−1.4, +0.2]; the symmetric scale-use model is identical
323   graded MultiPref the scale-use baseline raises direction ac-            to the text-only model on binary choices, because a binary
324   curacy by only +0.005 [+0.001, +0.008] at k = 20 (about                 label carries no intensity. LoRe (Bose et al., 2025), which
325   half of it already at k = 0), while RPS drops from 0.1593 to            reports +10 points for unseen PRISM users, run here with its
326   0.1532. On single-response safety ratings the same offsets              own few-shot fit and with a validated adaptation ridge under
327   do move the safe/unsafe decision (+4.8 points on DICES),                the same pre-set rule, also fails it: own gain at k = 20 −1.5
328   because there a rater’s threshold is the decision. Text-only            [−2.5, −0.4] (regularised −0.5 [−1.2, +0.2]), own − other
329
                                                                          6
                                        What Do Gains in Personalised Reward Modelling Measure?

330   +0.2 [−0.8, +1.2]. In LoRe’s own setting (its embeddings,              Benefit over the population model. On all test events of the
331   split and pair construction) we obtain 67.4 % for the mono-            shared items in the test folds — a broader panel than the
332   lithic model and 63.6 % for LoRe (published 61.0 % and                 1,116 items that contribute disagreeing pairs to the assign-
333   71.0 %; Appendix B): the published gain is not reproduced.             ment test (2,383 items, 1,436 users; population accuracy
334   With a graded label cut from the users’ own score differ-              72.4 %) — isotropic adaptation gains +0.70 [+0.24, +1.14]
335   ences (thresholds fixed in advance), the MultiPref pattern             pairwise accuracy points and +0.018 [+0.014, +0.023]
336   returns at half the size (scale-use model +0.043 [+0.031,              nats — the pre-set user-bootstrap rule for benefit is met,
337   +0.057] nats per rating at k = 20, VPL +0.015, PAL-B 0.000;            but the user × item interval for accuracy covers 0 ([−0.07,
338   no direction gain above +0.2 points). Community Align-                 +1.43]) while log-likelihood improves under both, so an
339   ment: who chooses what on identical items, and what                    accuracy benefit that generalises across items is unresolved;
340   adaptation buys. Community Alignment (CA; first turns;                 nor is the gain shown to be below one point. Evaluated
341   2,957 new users in five countries and languages; each choice           frozen on the same users’ unanalysed second turns (pro-
342   event’s chosen response paired with each of the other three).          cedure refitted there; Stage 12), the covariance-calibrated
343   Accuracy below is pairwise winner-versus-other accuracy,               variant gains +0.38 [+0.13, +0.64] points and +0.0046 nats
344   not four-way winner selection. Status: the adaptation proce-           and isotropic +0.31 [+0.05, +0.58]; the prompt × user inter-
345   dure was developed exploratorily on first turns (Appendix              val covers 0. On MultiPref the frozen isotropic procedure
346   F); the Stage-12 and Stage-13 outcome rules were frozen                did not establish improvement (−0.28 [−0.64, +0.08] points,
347   before their outcomes; the Stage-13 first-turn analyses reuse          202 held-out annotators). On CA the estimated covariance
348   previously examined data, while the second- and third-turn             shows no advantage over isotropic shrinkage (turn 1 −0.17
349   outcomes were evaluated for the first time.                            [−0.29, −0.05], turn 2 +0.07 [−0.07, +0.22] points); on
350                                                                          MultiPref it beats isotropic under the rater bootstrap (+0.23
      Identity on identical items (Stage 13, frozen). CA contains
351                                                                          [+0.04, +0.42]) without establishing improvement over the
      2,928 exact prompt–four-response items shown to at least
352                                                                          population model (two-way includes 0; Appendix F). Val-
      two users, covering 49,616 first-turn conversations (me-
353                                                                          idated scales imply strong shrinkage, and realised gains
      dian 15 users per item, one language per item, fixed re-
354                                                                          are far below model-implied ones (+1.9 points, Gaussian
      sponse order). For two users of the same item who chose
355                                                                          event-level simulation).
      different responses a and b, the population utilities can-
356
      cel and the adapted models predict the assignment from                 Transport to later conversations (Stage 13, frozen). We
357
      S = (δu − δv )⊤ (xa − xb ), with model-implied probabil-               froze each user’s first-turn deviation and added it, with-
358
      ity σ(S). With validated isotropic adaptation over length,             out rescaling, to a third-turn population model that sees
359
      paragraphs and list/heading lines (k = 20 support events               the conversation history (the earlier prompts and the user’s
360
      on other prompts; the Stage-12 procedure unchanged), the               preferred responses). We scored it on the third turns of con-
361
      conditional assignment log score gains +0.066 [+0.034,                 versations not used for support. Of 1,901 users with a frozen
362
      +0.091] nats over chance and assignment accuracy is 62.2               first-turn deviation, 1,808 have at least five third-turn events
363
      % [58.6, 65.6] (4,608 disagreeing pairs from 1,336 users on            with a complete history and 953 have at least five outside
364
      1,116 items; item × user bootstrap). It is unchanged with              their support conversations. The result is accuracy-positive
365
      uncentred features; positive-multiplier and prompt-clustered           under user clustering and likelihood-inconclusive: accuracy
366
      intervals are [+0.046, +0.083] and [+0.036, +0.093]; every             rises by +0.43 [+0.13, +0.74] points (user × prompt inter-
367
      fold is positive. The estimand is narrow: given two dis-               val [−0.08, +0.92]), log-likelihood by +0.0015 [−0.0006,
368
      agreeing users, their support choices and the two responses            +0.0035] nats. The pre-set rule requires both lower bounds
369
      they picked, assign the responses; it conditions on the fitted         above 0, so additional predictive value of unrescaled first-
370
      deviations and population model.                                       turn coefficients beyond a history-conditioned population
371
                                                                             model is not supported for this procedure and panel.
372   Position. The four fixed positions differ systematically
                                                                             This neither shows that transport has no effect nor that pref-
373   in these attributes (label-blind check), so we refitted with
                                                                             erences are unstable, and it does not test other ways of
374   position indicators added (after the result). The attribute-
                                                                             carrying information across turns.
375   derived part of the jointly fitted scores keeps +0.060 [+0.032,
376   +0.084] nats, a position-only predictor is also informative            The measured gain depends on the population baseline. On
377   (63.8 %), and the joint model’s paired gain over position-             1,799 common users, one-dimensional length adaptation
378   only is +0.026 [−0.0002, +0.046], so additional assignment             gains +0.88 / +1.08 points (random / prompt-separated test
379   value from attributes beyond position is unresolved. With              events) against a population model fitted on low-volume
380   correlated predictors under one prior this does not separate           annotators, as in WIMHF’s protocol, and +0.26 / +0.47
381   content from position: we claim user-specific choice pre-              against one fitted on all other-fold users: the population-
382   dictability on identical alternatives, not a content preference,       procedure effect is +0.62 [+0.41, +0.81] and +0.61 [+0.30,
383   and not a psychological position habit.                                +0.93] (paired), while the prompt-split contrast is inconclu-
384
                                                                         7
                                                      What Do Gains in Personalised Reward Modelling Measure?

385
      Table 1. Choice-level results. k = 20 support choice events per user (20 binary comparisons on MultiPref); pairwise accuracy; log-
386
      likelihood per pair. First interval: user (rater) bootstrap, or item × user for the assignment rows; second: prompt- or item-group × user
387   two-way bootstrap. Nominal 95 % intervals, conditional on the fitted population models. “Reused” = data examined in earlier stages;
388   “new” = outcomes evaluated for the first time.
389   Question (comparator)                   Panel                                Accuracy, points                       Log-likelihood, nats                             Status
390   Assignment (chance)                     CA t1 identical items; 1,336 users   62.2 % [58.6, 65.6]                    +0.066 [+0.034, +0.091]                          frozen, reused
391   . . . beyond position (position-only)   same                                 —                                      +0.026 [−0.0002, +0.046]                         exploratory
      Benefit (population)                    CA t1 shared items; 1,436 users      +0.70 [+0.24, +1.14]; [−0.07, +1.43]   +0.018 [+0.014, +0.023]; [+0.010, +0.026]        frozen, reused
392   Benefit, isotropic (population)         CA t2; 1,702 users                   +0.31 [+0.05, +0.58]; [−0.13, +0.79]   +0.0038 [+0.0021, +0.0057]; [+0.0006, +0.0066]   frozen, new
393   Benefit, TRV (population)               CA t2; 1,702 users                   +0.38 [+0.13, +0.64]; [−0.04, +0.83]   +0.0046 [+0.0031, +0.0063]; [+0.0018, +0.0074]   frozen, new
      Benefit, isotropic (population)         MultiPref; 202 annotators            −0.28 [−0.64, +0.08]; [−0.92, +0.39]   −0.0004 [−0.0019, +0.0010]; [−0.0028, +0.0019]   frozen, reused
394   Transport (history-conditioned pop.)    CA t3; 953 users                     +0.43 [+0.13, +0.74]; [−0.08, +0.92]   +0.0015 [−0.0006, +0.0035]; [−0.0020, +0.0048]   frozen, new
395   Baseline procedure W − O (paired)       CA t1; 1,799 users                   +0.62 [+0.41, +0.81]                   —                                                exploratory
396
397
398   sive (+0.20 [−0.20, +0.59]). The two procedures differ in                                  new raters are largely scale use: offsets capture them, probes
399   volume, composition and prior estimation, so no mechanism                                  find near-zero R2 for them in the evaluated user represen-
400   is isolated. (Our line-count proxy is not WIMHF’s discov-                                  tations, and adding offsets to VPL recovers the whole gain
401   ered feature; with it, list/heading adaptation does not beat                               (+0.088). User-specific choice predictability is real on iden-
402   the population coefficient — a related protocol study, not a                               tical CA items (62 %), though not separated from position.
403   failed reproduction.)                                                                      Choice gains over a competent population model are small
404                                                                                              and fragile (Table 1).
      Earlier evidence. Before this test, own adapted parameters
405   beat another user’s for four of six methods (LoRe +3.27                                    Why did published models learn little about new raters
406   [+2.85, +3.70]; within-country +3.22) and length deviations                                here? Published evaluations differ in users (synthetic, or
407   reproduced across disjoint prompt sets; own − other does                                   seen in training), label formats, representations and popula-
408   not measure benefit and task mix could create it (Appendix                                 tion baselines; the last alone changes the measured gain by
409   F). The identical-item test supersedes these as evidence of                                about 0.6 points on CA. Unresolved native-reproduction dis-
410   user-specific choice predictability.                                                       crepancies prevent attributing the rest to evaluation design,
411                                                                                              and all method conclusions concern the evaluated imple-
412                                                                                              mentations.
413   7. Recommendations
414     (i) Separate three outcomes. Report graded-rating likeli-
415                                                                                              9. Limitations and analysis log
            hood (calibration and resolution), a test of user-specific
416         choice predictability, and choice or ranking gains over                              The main tables use frozen-feature text heads (a LoRA re-
417         the population model as different results; a gain on                                 ward model only in §5.3), and compressed features make
418         one does not imply the others. (ii) Test user differ-                                the published methods weaker detectors than full features.
419         ences on identical items where the data allow it (an                                 VPL, PAL and LoRe are our reimplementations as heads
420         assignment test between disagreeing users, as in §6):                                on frozen embeddings; their published numbers were not
421         own-versus-other contrasts on different prompts con-                                 reproduced in native settings (LoRe’s PRISM gain not even
422         found user differences with task mix and do not mea-                                 with its own embeddings), for reasons we could not isolate.
423         sure benefit. (iii) Report a competent population                                    The positive control injects low-dimensional preferences on
424         baseline and its training procedure. The measured                                    MultiPref only, on panels noisier than the real data. The
425         personalisation gain changed by about 0.6 points with                                aspect analyses rest on MultiPref’s concurrent aspect labels;
426         the population-training procedure (§6). (iv) Report                                  SAP’s limitations are in Appendix G. The first three datasets
427         a scale-use baseline (a few text-independent offsets                                 are English; Community Alignment spans five languages,
428         per rater) next to any personalised reward model on                                  which the phrase-based attributes cover only for English;
429         graded labels, and evaluate content adaptation with                                  and the per-rater calibration is not shown to change a down-
430         those offsets retained. (v) Evaluate on raters unseen                                stream decision. The CA analyses reuse data examined in
431         in training and on held-out prompts, with permuta-                                   earlier stages (Appendix A); the identical-item test condi-
432         tion and positive controls. (vi) Keep graded labels and                              tions on fitted models; features omit conversation history
433         ties when individual differences matter.                                             except in the third-turn test; and the identity signal is not
434                                                                                              separated from response position.
435
436   8. Discussion
437   What do personalisation gains measure? Three things
438   often reported as one come apart. Graded-rating gains for
439
                                                                                             8
                                       What Do Gains in Personalised Reward Modelling Measure?

440   Impact Statement                                                      Davidson, R. R. On extending the Bradley-Terry model
441                                                                           to accommodate ties in paired comparison experiments.
442   This paper evaluates personalised reward models, which are              Journal of the American Statistical Association, 65(329):
443   meant to let language models serve people whose prefer-                 317–328, 1970. doi: 10.1080/01621459.1970.10481082.
444   ences differ. It finds that reported personalisation gains can
445   reflect rating-scale use, user-associated choice predictability       Dawid, A. P. and Skene, A. M. Maximum likelihood esti-
446   or real improvements over a population model, and that                  mation of observer error-rates using the EM algorithm.
447   these need separate tests: gains on graded ratings were                 Journal of the Royal Statistical Society: Series C (Applied
448   largely scale use, users’ choices on identical alternatives             Statistics), 28(1):20–28, 1979.
449   were predictable from their other choices, and improvements
450   over a population model were small and dataset-dependent.             Deng, N., Zhang, X. F., Liu, S., Wu, W., Wang, L., and
451   Predicting individuals’ choices also raises privacy and ma-             Mihalcea, R. You are what you annotate: Towards better
452   nipulation concerns that a deployment would need to ad-                 models through annotator representations. In Findings of
453   dress; we report no individual-level results. The datasets are          the Association for Computational Linguistics: EMNLP
454   public, were collected with consent by their creators, and              2023, pp. 12475–12498, 2023.
455   are used under their licences; rater identifiers are used only
456   as anonymous indices.                                                 Dong, Y. R., Hu, T., Liu, Y., Üstün, A., and Collier, N. When
457                                                                           personalization meets reality: A multi-faceted analysis
458   References                                                              of personalized preference learning, 2025. URL https:
459                                                                          //arxiv.org/abs/2502.19158.
      Aroyo, L., Taylor, A. S., Dı́az, M., Homan, C. M., Parrish,
460
        A., Serapio-Garcı́a, G., Prabhakaran, V., and Wang, D.              Eckes, T. Introduction to Many-Facet Rasch Measurement:
461
        DICES dataset: Diversity in conversational AI evaluation              Analyzing and Evaluating Rater-Mediated Assessments,
462
        for safety. In Advances in Neural Information Processing              volume 22 of Language Testing and Evaluation. Peter
463
        Systems 36 (NeurIPS 2023), Datasets and Benchmarks                    Lang, Frankfurt am Main, 2011. ISBN 978-3-631-61350-
464
        Track, 2023. doi: 10.52202/075280-2321.                               4.
465
466   Baumgartner, H. and Steenkamp, J.-B. E. M. Response
467                                                                         Feng, S., Sorensen, T., Liu, Y., Fisher, J., Park, C. Y., Choi,
        styles in marketing research: A cross-national investi-
468                                                                           Y., and Tsvetkov, Y. Modular pluralism: Pluralistic align-
        gation. Journal of Marketing Research, 38(2):143–156,
469                                                                           ment via multi-LLM collaboration. In Proceedings of
        2001. doi: 10.1509/jmkr.38.2.143.18840.
470                                                                           the 2024 Conference on Empirical Methods in Natural
471   Bose, A., Xiong, Z., Chi, Y., Du, S. S., Xiao, L., and Fazel,           Language Processing, pp. 4151–4171, Miami, Florida,
472     M. LoRe: Personalizing LLMs via low-rank reward                       USA, 2024. Association for Computational Linguistics.
473     modeling, 2025. URL https://arxiv.org/abs/                            doi: 10.18653/v1/2024.emnlp-main.240.
474     2504.14439.
                                                                            Fleisig, E., Abebe, R., and Klein, D. When the majority is
475   Castricato, L., Lile, N., Rafailov, R., Fränken, J.-P.,                wrong: Modeling annotator disagreement for subjective
476     and Finn, C. PERSONA: A reproducible testbed                          tasks. In Proceedings of the 2023 Conference on Empiri-
477     for pluralistic alignment.   In Proceedings of the                    cal Methods in Natural Language Processing, pp. 6715–
478     31st International Conference on Computational Lin-                   6726, Singapore, 2023. Association for Computational
479     guistics (COLING), pp. 11348–11368, Abu Dhabi,                        Linguistics. doi: 10.18653/v1/2023.emnlp-main.415.
480     UAE, 2025. Association for Computational Linguis-
481     tics. URL https://aclanthology.org/2025.                            Gordon, M. L., Zhou, K., Patel, K., Hashimoto, T., and Bern-
482     coling-main.752/.                                                     stein, M. S. The disagreement deconvolution: Bringing
483
      Chakraborty, S., Qiu, J., Yuan, H., Koppel, A., Manocha,                machine learning performance metrics in line with reality.
484
        D., Huang, F., Bedi, A. S., and Wang, M. MaxMin-                      In Proceedings of the 2021 CHI Conference on Human
485
        RLHF: Alignment with diverse human preferences. In                   Factors in Computing Systems (CHI ’21), pp. 1–14. ACM,
486
        Proceedings of the 41st International Conference on Ma-               2021. doi: 10.1145/3411764.3445423.
487
488     chine Learning (ICML), volume 235 of Proceedings of
                                                                            Gordon, M. L., Lam, M. S., Park, J. S., Patel, K., Hancock,
489     Machine Learning Research, pp. 6116–6135, 2024.
                                                                              J. T., Hashimoto, T., and Bernstein, M. S. Jury learn-
490   Chen, D., Chen, Y., Rege, A., Wang, Z., and Vinayak, R. K.              ing: Integrating dissenting voices into machine learning
491     PAL: Sample-efficient personalized reward modeling for                models. In Proceedings of the 2022 CHI Conference on
492     pluralistic alignment. In The Thirteenth International               Human Factors in Computing Systems (CHI ’22). ACM,
493     Conference on Learning Representations (ICLR), 2025.                  2022. doi: 10.1145/3491102.3502004.
494
                                                                        9
                                      What Do Gains in Personalised Reward Modelling Measure?

495   Homan, C. M., Serapio-Garcia, G., Aroyo, L., Diaz, M.,               Li, X., Zhou, R., Lipton, Z. C., and Leqi, L. Personalized
496     Parrish, A., Prabhakaran, V., Taylor, A., and Wang, D.               language modeling from personalized human feedback,
497     Intersectionality in AI safety: Using multilevel models              2024.
498     to understand diverse perceptions of safety in conversa-
499     tional AI. In Proceedings of the 3rd Workshop on Per-              Linacre, J. M. Many-Facet Rasch Measurement. MESA
500     spectivist Approaches to NLP (NLPerspectives) @ LREC-                Press, Chicago, 1989.
501    COLING 2024, pp. 131–141, Torino, Italia, 2024. ELRA                Luo, F., Yang, R., Sun, H., Deng, C., Yao, J., Shen, J.,
502     and ICCL. URL https://aclanthology.org/                              Zhang, H., and Chen, H. Rethinking diverse human pref-
503     2024.nlperspectives-1.15/.                                           erence learning through principal component analysis.
504                                                                          In Findings of the Association for Computational Lin-
505   Hovy, D., Berg-Kirkpatrick, T., Vaswani, A., and Hovy, E.              guistics: ACL 2025, pp. 19857–19870, Vienna, Austria,
506     Learning whom to trust with MACE. In Proceedings of                  2025. Association for Computational Linguistics. doi:
507    NAACL-HLT, pp. 1120–1130, 2013.                                       10.18653/v1/2025.findings-acl.1019.
508
509   Jang, J., Kim, S., Lin, B. Y., Wang, Y., Hessel, J., Zettle-         Miranda, L. J. V., Wang, Y., Elazar, Y., Kumar, S., Pyatkin,
510     moyer, L., Hajishirzi, H., Choi, Y., and Ammanabrolu, P.            V., Brahman, F., Smith, N. A., Hajishirzi, H., and Dasigi,
511     Personalized soups: Personalized large language model               P. Hybrid preferences: Learning to route instances for hu-
512     alignment via post-hoc parameter merging, 2023.                     man vs. AI feedback. In Proceedings of the 63rd Annual
513                                                                         Meeting of the Association for Computational Linguis-
      Kim, G. and Kim, E. Swap-guided preference learning for               tics (Volume 1: Long Papers), pp. 7162–7200, Vienna,
514     personalized reinforcement learning from human feed-
515                                                                         Austria, 2025. Association for Computational Linguistics.
        back. In International Conference on Learning Represen-             doi: 10.18653/v1/2025.acl-long.355.
516     tations (ICLR), 2026. URL https://arxiv.org/
517     abs/2603.12595.                                                    Mishra, P., Rastogi, C., Pfohl, S. R., Parrish, A., Teh, T. H.,
518                                                                         Patel, R., Diaz, M., Wang, D., Paganini, M., Prabhakaran,
519   Kirk, H. R., Whitefield, A., Röttger, P., Bean, A. M., Mar-          V., Aroyo, L., and Rieser, V. Decoding safety feedback
520     gatina, K., Ciro, J., Mosquera, R., Bartolo, M., Williams,          from diverse raters: A data-driven lens on responsive-
521     A., He, H., Vidgen, B., and Hale, S. A. The PRISM                   ness to severity. Transactions on Machine Learning
522     alignment dataset: What participatory, representative and           Research, 2026. URL https://arxiv.org/abs/
523     individualised human feedback reveals about the subjec-             2503.05609.
524     tive and multicultural alignment of large language models.
525     In Advances in Neural Information Processing Systems 37            Mostafazadeh Davani, A., Dı́az, M., and Prabhakaran, V.
526     (NeurIPS 2024), Datasets and Benchmarks Track, 2024.                Dealing with disagreements: Looking beyond the major-
527     doi: 10.52202/079017-3342.                                          ity vote in subjective annotations. Transactions of the
528                                                                         Association for Computational Linguistics, 10:92–110,
529   Kobalczyk, K., Fanconi, C., Sun, H., and van der Schaar,              2022. doi: 10.1162/tacl a 00449.
530     M. Few-shot steerable alignment: Adapting rewards and
531     LLM policies with neural processes, 2024.                          Orlikowski, M., Röttger, P., Cimiano, P., and Hovy, D. The
532                                                                          ecological fallacy in annotation: Modelling human label
533   Koren, Y. and Sill, J. OrdRec: An ordinal model for predict-           variation goes beyond sociodemographics. In Proceed-
534     ing personalized item rating distributions. In Proceedings           ings of the 61st Annual Meeting of the Association for
535     of the Fifth ACM Conference on Recommender Systems                   Computational Linguistics (Volume 2: Short Papers), pp.
536     (RecSys), pp. 117–124, 2011.                                         1017–1029, Toronto, Canada, 2023. Association for Com-
537                                                                          putational Linguistics. doi: 10.18653/v1/2023.acl-short.
538   Koren, Y., Bell, R., and Volinsky, C. Matrix factorization             88.
539     techniques for recommender systems. Computer, 42(8):
        30–37, 2009.                                                       Park, C., Liu, M., Kong, D., Zhang, K., and Ozdaglar, A.
540                                                                          RLHF from heterogeneous feedback via personalization
541   Kumar, D., Kelley, P. G., Consolvo, S., Mason, J., Bursztein,          and preference aggregation, 2024.
542     E., Durumeric, Z., Thomas, K., and Bailey, M. De-
543                                                                        Plank, B. The “problem” of human label variation: On
        signing toxic content classification for a diversity of              ground truth in data, modeling and evaluation. In Pro-
544     perspectives. In Seventeenth Symposium on Usable
545                                                                          ceedings of EMNLP, pp. 10671–10682, 2022.
        Privacy and Security (SOUPS 2021), pp. 299–318.
546     USENIX Association, 2021. ISBN 978-1-939133-25-0.                  Poddar, S., Wan, Y., Ivison, H., Gupta, A., and Jaques, N.
547     URL https://www.usenix.org/conference/                               Personalizing reinforcement learning from human feed-
548     soups2021/presentation/kumar.                                        back with variational preference learning. In Advances
549
                                                                      10
                                       What Do Gains in Personalised Reward Modelling Measure?

550     in Neural Information Processing Systems 37 (NeurIPS                   Saladi, K., Schelten, A., Silva, R., Smith, E. M., Subra-
551     2024), 2024. doi: 10.52202/079017-1664.                                manian, R., Tan, X. E., Tang, B., Taylor, R., Williams,
552                                                                            A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan,
553   Rao, P. V. and Kupper, L. L. Ties in paired-comparison ex-               A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R.,
554     periments: A generalization of the Bradley-Terry model.                Edunov, S., and Scialom, T. Llama 2: Open foundation
555     Journal of the American Statistical Association, 62(317):              and fine-tuned chat models, 2023.
556     194–204, 1967. doi: 10.1080/01621459.1967.10482901.
557                                                                          Uma, A. N., Fornaciari, T., Hovy, D., Paun, S., Plank, B.,
558   Raykar, V. C., Yu, S., Zhao, L. H., Valadez, G. H., Florin, C.,         and Poesio, M. Learning from disagreement: A survey.
559     Bogoni, L., and Moy, L. Learning from crowds. Journal                 Journal of Artificial Intelligence Research, 72:1385–1470,
560     of Machine Learning Research, 11:1297–1322, 2010.                     2021.
561   Ryan, M. J., Shaikh, O., Bhagirath, A., Frees, D., Held, W.,           Wang, Z., Bukharin, A., Delalleau, O., Egert, D., Shen,
562     and Yang, D. SynthesizeMe! inducing persona-guided                    G., Zeng, J., Kuchaiev, O., and Dong, Y. HelpSteer2-
563     prompts for personalized reward models in LLMs. In                    Preference: Complementing ratings with preferences. In
564     Proceedings of the 63rd Annual Meeting of the Associ-                 The Thirteenth International Conference on Learning
565     ation for Computational Linguistics (ACL), 2025. URL                  Representations (ICLR), 2025. URL https://arxiv.
566     https://arxiv.org/abs/2506.05598.                                     org/abs/2410.01257.
567
568   Shenfeld, I., Faltings, F., Agrawal, P., and Pacchiano, A.             Zhang, L. H., Milli, S., Jusko, K., Smith, J., Amos, B.,
569     Language model personalization via reward factorization,               Bouaziz, W., Revel, M., Kussman, J., Sheynin, Y., Ti-
570     2025.                                                                  tus, L., Radharapu, B., Yu, J., Sarma, V., Rose, K., and
571                                                                            Nickel, M. Cultivating pluralism in algorithmic mono-
572   Siththaranjan, A., Laidlaw, C., and Hadfield-Menell, D.                  culture: The community alignment dataset. In The Four-
573      Distributional preference learning: Understanding and                 teenth International Conference on Learning Represen-
574      accounting for hidden context in RLHF. In The Twelfth                 tations (ICLR), 2026. URL https://arxiv.org/
575     International Conference on Learning Representations                   abs/2507.09650.
576     (ICLR), 2024. URL https://arxiv.org/abs/
577      2312.08358.                                                         Zhang, M. J. Q., Wang, Z., Hwang, J. D., Dong, Y., De-
578                                                                            lalleau, O., Choi, Y., Choi, E., Ren, X., and Pyatkin, V.
579   Sorensen, T., Moore, J., Fisher, J., Gordon, M. L.,                      Diverging preferences: When do annotators disagree and
580     Mireshghallah, N., Rytting, C. M., Ye, A., Jiang, L.,                  do models know? In Proceedings of the 42nd Interna-
581     Lu, X., Dziri, N., Althoff, T., and Choi, Y. Position:                 tional Conference on Machine Learning (ICML), volume
582     A roadmap to pluralistic alignment. In Proceedings of                  267 of Proceedings of Machine Learning Research, pp.
583     the 41st International Conference on Machine Learning                  76193–76212, 2025.
584     (ICML), volume 235 of Proceedings of Machine Learning
                                                                             Zhao, S., Dang, J., and Grover, A. Group preference
585     Research, pp. 46280–46302, 2024.
                                                                               optimization: Few-shot alignment of large language
586                                                                            models. In The Twelfth International Conference on
587   Sorensen, T., Mishra, P., Patel, R., Tessler, M. H., Bakker,
        M. A., Evans, G., Gabriel, I., Goodman, N., and Rieser, V.             Learning Representations (ICLR), 2024. URL https:
588                                                                            //arxiv.org/abs/2310.11523.
589     Value profiles for encoding human variation. In Proceed-
590     ings of the 2025 Conference on Empirical Methods in
                                                                             Zollo, T. P., Siah, A. W. T., Ye, N., Li, A., and Namkoong, H.
591     Natural Language Processing, pp. 2047–2095, Suzhou,
                                                                               PersonalLLM: Tailoring LLMs to individual preferences.
592     China, 2025. Association for Computational Linguistics.
                                                                               In The Thirteenth International Conference on Learning
593     doi: 10.18653/v1/2025.emnlp-main.106.
                                                                               Representations (ICLR), 2025. URL https://arxiv.
594   Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A.,           org/abs/2409.20296.
595     Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhos-
596     ale, S., Bikel, D., Blecher, L., Canton Ferrer, C., Chen,
597     M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W.,
598     Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn,
599     A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez,
600     V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P. S.,
601     Lachaux, M.-A., Lavril, T., Lee, J., Liskovich, D., Lu, Y.,
602     Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Moly-
603     bog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R.,
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
621   Frozen. The MultiPref data had been analysed earlier with             C3 fails (published latents do not encode style, R2 ≈ 0), C4
622   other methods.                                                        not met as a conjunction (first part holds, +0.088 over VPL;
623                                                                         second part a tie with DFs, lower bound −0.014); Stage
      All intervals are nominal and do not account for the earlier
624                                                                         3 (positive control): τ 0 control passes; power at the pre-
      adaptive development.
625                                                                         specified strengths (+1.7, +5.2 oracle points) not established
626   All analyses were specified in timestamped internal                   — no content-interacting method’s own − other gain has
627   protocols (PROTOCOL STAGE1, PROTOCOL STAGE2,                          a lower bound above +1 point; exploratory dose-response:
628   PROTOCOL STAGE2B, PROTOCOL STAGE2C, PROTO-                            VPL and PAL-B pass at +21 points, none at +10; the split-
629   COL STAGE3); stages 2b and 2c were written after the                  half content estimator (S3-C) has no power; with full fea-
630   stage-2a results. Changes after a result were logged as num-          tures (exploratory, Amendment 5) the τ 0 control passes and
631   bered amendments with the reason; the main ones: the first            PAL-B passes at +10 points (k = 20), so the PCA bottleneck
632   decoding split (a = b = 2) was structurally empty (two rat-           explains part of the detection limit. R1 (PRISM native pair-
633   ings determine their distribution) and was replaced by a = 3,         wise choices: every method’s own choice-accuracy gain at
634   b = 1; hand-set penalties in the rater–item model over-fitted         k = 20 has an upper bound < +0.01) holds (largest bound
635   and were replaced by inner cross-validation (which reversed           +0.0071, PAL-B K = 4).
636   an earlier, wrong conclusion that rater shifts do not help);
                                                                            Scale use and the shared reward model. Training the
637   penalty grids were extended when selections fell on grid
                                                                            text model jointly with rater offsets and then using the
638   edges, before any hypothesis was read; the low-rank base-
                                                                            population-mean offsets (k = 0) does not give a better
639   line lacked a constant column and was fixed in its favour; the
                                                                            consensus model than ordinary training: −0.003 [−0.010,
640   probit group model had a scale non-identifiability and was
                                                                            +0.003] nats on MultiPref (direction +0.3 points, n.s.),
641   fixed; VPL suffered posterior collapse and its KL weight
                                                                            −0.022 [−0.037, −0.008] on DICES, +0.001 on PRISM,
642   was re-selected including 0; PAL-B’s adaptation ridge was
                                                                            −0.009 [−0.016, −0.004] with the LoRA reward model.
643   re-selected by k-shot validation. Every superseded full run
                                                                            Ordinary training averages scale use out; it matters for pre-
644   is kept and reported in the supplementary results; two de-
                                                                            dicting a person, not for learning the content preference.
645   bugging smoke runs and one fold whose output was deleted
646   unread when the penalty grids were extended are not. The              What the offsets encode. In the probit family, rater scale
647   real-data aspect contrast of §5.7 was revised four times: own         matters more than rater shift on MultiPref (+0.036 [+0.020,
648   − other; with a style-only control after a first, confounded          +0.057] at k = 20), but rater shift dominates on DICES
649   +0.45 [+0.01, +0.94]; against θ = 0; and against the popu-            (−0.053) and PRISM (−0.031): leniency/strictness on
650   lation weighting, after the reference learner turned out to           single-response rating scales, intensity on two-sided prefer-
651   shrink towards 0 rather than towards the population. The              ence scales.
652   few-shot-tuned low-rank prior was selected at the top of its
                                                                            What this does and does not say about pluralism. Our
653   grid (8192) in most folds; extending the grid to 524,288
                                                                            results do not show that people agree about content: the item-
654   left every DL result unchanged in substance (real data: own
                                                                            level disagreement that replicates across rater panels is real
655   − other +0.31 vs +0.30 at k = 20, DFs − DL +0.003 vs
                                                                            (split-half reliability 0.25 on MultiPref) and about a tenth
656   +0.0045; synthetic +5/+10-point panels: +0.10 / +0.09 vs
                                                                            of it is decodable from text. They show that, for predicting
657   −0.02 / +0.09).
                                                                            an individual new rater from few ratings, that content-level
658                                                                         disagreement is a small part of what is predictable, and that
659
                                                                       12
                                       What Do Gains in Personalised Reward Modelling Measure?

660   demographic or crowd/expert groups add nothing beyond                 this ceiling concerns a small residual and is a property of
661   the text.                                                             MultiPref’s concurrent labelling.
662
      Fine-tuned and in-context reward models (§5.3, full text).            Even with the rater’s own aspect judgements and all of their
663
      With a LoRA-fine-tuned Qwen2.5-7B reward model (D-                    training ratings, a rater-specific trade-off predicts which
664
      LoRA, trained per fold on the training raters’ rating distri-         response they prefer only 0.1 points better than the popu-
665
      butions) as the text model, the three-number style model              lation’s trade-off, and even fitted in-sample only 0.4 points
666
      still adds +0.100 [+0.071, +0.130] nats per rating at k               better. The reason is that the aspects point in opposite direc-
667
      = 20 — the same as its gain on the frozen-feature head                tions in only 4.0 % of the held-out non-tie comparisons (3.5
668
      (+0.100). Fine-tuning improves the text-only model by                 % of all annotations); there individual trade-offs matter a
669
      +0.027 [+0.016, +0.039] (direction accuracy +1.4 points)              great deal (in-sample +9.7 points; among the 20 raters with
670
      and the style model by the same +0.027: the two gains                 at least ten helpfulness–harmlessness conflicts, the share
671
      add. Personalising the frozen-feature model with 20 rat-              of conflicts resolved in favour of helpfulness ranges from
672
      ings per rater gains more than fine-tuning the text model             0.00 to 0.94), but they are too rare to move overall accuracy.
673
      (+0.072 [+0.041, +0.106]). DFs keeps the direction accuracy           Individual trade-offs do change how strongly raters prefer
674
      of D-LoRA (+0.002 [−0.002, +0.006]). Against in-context               (up to +0.046 nats with all their ratings), in line with the
675
      personalisation — a separate LoRA model on the same base,             calibration-not-ranking pattern. We fixed in advance that
676
      trained with ten of the rater’s other ratings in the prompt           an aspect-weight personalised reward model would be built
677
      and evaluated with the new rater’s k ratings in the prompt            only if the lower bound of this ceiling exceeded half a point
678
      — the three offsets on D-LoRA are better at k = 20. The               with all training ratings; it does not, so we did not build one.
679
      in-context model’s result varies with its training seed (two          The learned personalisers cannot be tested on the conflict
680
      of fifteen runs failed, gaining −0.078 and −0.055 over D-             items either: the 243 held-out non-tie ratings on them give
681
      LoRA against +0.021 to +0.125 for the others; the two failed          own − other intervals wider than the achievable ceiling (k
682
      runs have the highest training loss), so it was trained with          = 20: low-rank latent +0.1 [−2.2, +2.4]). A calibrated test
683
      three seeds per fold, and we fixed in advance that “better”           on the real data. The ceiling above gives each rater’s own
684
      requires a lower bound above zero for every seed and for the          aspect labels; a deployable personaliser would know only
685
      seed average. Averaged over seeds — the expected result of            the item’s aspects. We therefore ran the reference learner
686
      one training run — the offsets are better by +0.041 [+0.027,          of §5.6 on the real labels with the item’s consensus aspect
687
      +0.054] nats per rating (209 raters; per seed +0.062, +0.018          differences from its other annotators as content features
688
      and +0.042, every lower bound at least +0.005) and more               (3-d), with a hierarchical prior centred at the population
689
      accurate on which response the rater prefers (+1.9 points             weighting (estimated on the training raters) and compared
690
      [+0.9, +2.7]). The in-context model does learn from the               each rater’s own weights with that population weighting
691
      history (+0.051 [+0.024, +0.079] over D-LoRA on average),             (style offsets kept). Individual weights transfer worse than
692
      at several thousand prompt tokens per prediction, but its             the population’s: −0.28 [−0.56, −0.06] points at k = 20
693
      direction accuracy is below D-LoRA’s (−1.7 points [−2.6,              and −0.63 [−1.01, −0.25] at k = 50. With injected aspect-
694
      −0.8] on average; −0.6 to −3.0 per seed).                             weight heterogeneity it gives +0.46 [−0.00, +0.96] at k =
695
                                                                            50 when an oracle would gain +1.4 points and +3.4 [+2.6,
696   Value conflicts (§5.7, full text). The positive control asks
                                                                            +4.3] at +5.0. The real data lie well below the +5-point
697   what the methods could detect; MultiPref also lets us ask
                                                                            panel and, at k = 50, just below the +1.4-point panel: for
698   how much there is to detect. Every MultiPref annotation
                                                                            this injection family, the real data lie below panels of one
699   carries the annotator’s own helpfulness, truthfulness and
                                                                            to two oracle points (sensitivity evidence, not a validated
700   harmlessness preferences next to the overall one, so a rater’s
                                                                            upper bound). This test is exploratory and post hoc, and its
701   way of trading these values off is observable. We fit an
                                                                            contrast was revised four times (Appendix A; no version
702   ordinal model of the overall preference from the annota-
                                                                            shows a positive transferable aspect part), the calibration
703   tor’s own aspect labels (their values and absolute values)
                                                                            strengths were chosen after seeing the real bound, it uses
704   with rater-specific cut-points (scale use) and either a pooled
                                                                            one synthetic draw on panels noisier than the real data, and
705   trade-off or a rater-specific trade-off, adapted on k of the
                                                                            it uses other annotators’ aspect labels of the test items (an
706   rater’s training-item annotations and evaluated on held-out
                                                                            aspect oracle, not a deployable model). Three caveats: the
707   items with the rater’s own aspect labels as inputs — an
                                                                            ceiling bounds personalisation of the weighting only — dis-
708   oracle for the content side. The pooled trade-off weights
                                                                            agreement about which response is more helpful or harmless
709   harmlessness most (6.1, five-fold mean), then helpfulness
                                                                            is absorbed into the inputs; it covers content preferences
710   (4.0) and truthfulness (2.0). With the rater’s own aspect
                                                                            expressible through these three aspects only; MultiPref’s
711   labels as inputs the pooled model already gets 97.5 % of
                                                                            prompt sampling determines how often values conflict; and
712   directions right (74 % on conflict items): aspect and over-
                                                                            annotators may have aligned their aspect labels with their
713   all labels are produced together by the same annotator, so
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
722   overall label, which would understate conflicts.                           the +10-point panels of the injected form at k = 20; at k = 50
723                                                                              they lie below the +5-point panel but the intervals overlap
      Code readability (Stage 10). Pre-set rules: SE-1 (offsets
724                                                                              (comparisons with synthetic panels, not formal exclusion
      transfer) holds on both panels; SE-2 with the low-rank latent:
725                                                                              bounds); the compressed features used for the main tables
      Buse–Weimer inconclusive (own gain in concordance +1.75
726                                                                              make the published methods weaker detectors than they
      [+0.68, +2.78], own − other +0.53 [−0.63, +1.72]; the
727                                                                              need to be.
      text-only model orders snippets at chance, 51.6 %), Dorn
728   degenerate (validation selects the largest penalties, the latent           Positive control (§5.6, full text). No method has power at
729   equals the text-only model). SAP-code, own − population /                  the pre-specified strengths. In the exploratory dose-response,
730   own − other: Buse–Weimer k = 20 +0.40 [−0.25, +1.06] /                     VPL and PAL-B detect content preferences worth +21 points
731   +1.57 [+0.89, +2.25], k = 50 +1.30 [+0.46, +2.18] / +2.98                  but recover less than half a point of +10; the low-rank latent,
732   [+2.00, +3.91]; Dorn k = 10 −0.19 [−0.81, +0.42] / +2.06                   whose user term interacts with a joint embedding of the
733   [+1.49, +2.62] — the rule as worded is met on Dorn through                 comparison, has a signal at +21 points that stays below the
734   own − other, which Stage 5 Am. 4 showed is not on the                      threshold, and with the untuned prior it shows nothing up to
735   oracle scale, so content personalisation is not claimed. One               +5 points either. On the real data VPL and PAL-B are at the
736   within-snippet permutation control gives own − population                  null-control level, and the low-rank latent’s marginal +0.30
737   −0.38 (Buse–Weimer) and −2.09 (Dorn).                                      [−0.00, +0.60] is matched by the text-independent offsets
738                                                                              (+0.32 [+0.06, +0.58] on the same contrast), so it reflects
739   Untuned rank-2 comparator (Stage 9 Am. 4). With only
                                                                                 scale use (which can tip a few near-tie predictions), not con-
740   its map ridge chosen on training raters’ held-out ratings
                                                                                 tent. Read together: on MultiPref, the real data lie far below
741   and z ˜ N(0, I) for new raters, the rank-2 attribute model
                                                                                 the +20-point panels for these methods, while preferences
742   gave −2.67 [−3.30, −2.07] (null), +2.20 / +7.36 (semantic),
                                                                                 worth up to about 10 points cannot be seen by them from 20
743   −0.42 (out-of-dictionary) and −2.13 [−2.73, −1.52] (real);
                                                                                 ratings, so the ranking null of §6 says nothing about those.
744   tuning its adaptation strength on pseudo-new raters (Am. 8)
                                                                                 These are comparisons with synthetic panels of one injected
745   removes the losses.
                                                                                 form, not formal exclusion bounds. On the full features
746   SAP with the pre-registered EM update (Stage 9, before                     (exploratory) VPL’s latent collapses (own − other exactly
747   Amendment 7). own − µ at k = 20: null draws −0.28                          0), while PAL-B passes the threshold at +10 points but not
748   . . . +0.05 (k = 50: down to −0.50 [−0.92, −0.09]); seman-                 at +5, and the real data stay at the null level (+0.11 [−0.16,
749   tic panels +2.26 . . . +2.79 and +7.30 . . . +8.04; out-of-                +0.37]): the real data lie below the +10-point panels of the
750   dictionary +0.41 and +0.81; real MultiPref +0.17 [−0.19,                   injected form at k = 20 but not below the +5-point panels
751   +0.55], LL +0.0022 [+0.0003, +0.0041] nats; PRISM native                   (Appendix B). How far are these methods from what the
752   choices −0.25 [−1.30, +0.83] (EM variances stayed near                     data allow? A well-specified reference learner — the injec-
753   their initial value there; with the fixed-point update +0.08               tion’s two features known, a per-rater weight vector with an
754   [−0.86, +1.02]).                                                           empirical-Bayes prior, style offsets re-fitted, the same per-
755                                                                              mutation contrast — recovers the injected preference from
756   Positive control on full features (Stage 3, Amendment 5).
                                                                                 20 ratings at every strength. On the oracle’s scale (the rater’s
757   Because the compressed features might be what limits the
                                                                                 own weights against the population state, θ = 0 here, with the
758   content-interacting methods, we re-ran VPL and PAL-B on
                                                                                 rater’s style offsets kept) it gains +0.89 [+0.40, +1.37] points
759   the full features (exploratory). The text-only fits improve (k
                                                                                 at +1.7 oracle points, +3.1 [+2.3, +4.0] at +5.2 and +8.0
760   = 0 log-likelihood: PAL-B −1.533 vs −1.558, VPL −1.495
                                                                                 at +10.1, i.e. 52–79 % of the oracle; own − other roughly
761   vs −1.574), but VPL’s latent then collapses and is unused at
                                                                                 doubles these numbers, because another rater’s weights are
762   every strength (own − other exactly 0), so this check rests
                                                                                 anti-informative, and is therefore not used for this learner.
763   on PAL-B. Its detection limit drops: it passes the threshold
                                                                                 Among the tested strengths, the reference learner crosses
764   at +10 points; at +5 points its k = 50 gain is positive (+1.05
                                                                                 the detection criterion between +1.7 and +5.2 points, well
765   [+0.37, +1.72]; real data +0.19 [−0.12, +0.48]) but meets
                                                                                 below the methods’. Is the gap in the methods’ inputs or
766   the +1-point criterion in only one of four synthetic draws.
                                                                                 in the learners? Linear probes (exploratory, Appendix B)
767   The real data stay at the null level (+0.11 [−0.16, +0.37] at
                                                                                 show the injected direction is available to VPL and PAL-B
768   k = 20). With this stronger detector, the real data lie below
                                                                                 (out-of-fold R2 0.65 compressed, 1.00 full) but not to the
769
                                                                            14
                                       What Do Gains in Personalised Reward Modelling Measure?

770   low-rank latent’s joint embedding (0.02); re-injected inside          [+5.84, +8.16] at +10.4; the reference learner is unchanged
771   that embedding, the latent detects +10 points (+1.97 [+1.31,          (own − population +2.67 and +8.33). S7-3, seen-rater
772   +2.65]; originally +0.09; 3 of 4 draws) but not +5 (+0.08;            ceiling on real MultiPref (training raters × test items, 904
773   0 of 4). With the dimension available, the best learners              rater-folds, trained parameters; derangement of training
774   thus detect between +5 and +10 oracle points, the refer-              raters): direction accuracy minus the text-only model
775   ence learner below +5: what fails is finding the dimension,           −0.51 [−0.88, −0.11] (five offsets), −0.00 [−0.20, +0.18]
776   not the number of ratings. With semantic axes (formatting,            (symmetric), −0.42 [−0.81, −0.02] (low-rank); own −
777   hedging/refusal) no method detects even +9.7 points; the              other −0.23, +0.10, −0.11 [−0.57, +0.36]; log-likelihood
778   reference learner recovers +7.4 (Appendix B). Results are             over the text-only model +0.13 nats for all three. By
779   stable over four synthetic draws, and the synthetic panels            the rule fixed beforehand, the ranking null also holds
780   are noisier than the real data, so the calibrations transfer          for seen raters. S7-4 (Amendment 3), semantic axes —
781   only approximately (Appendix B).                                      (s1) log(1 + markdown list/heading lines) of B minus A,
782                                                                         (s2) the same for a fixed list of hedging/refusal phrases
      Positive control: seed variability and realism (Stage
783                                                                         — calibrated to +4.6 and +9.7 oracle points: probes R2
      5). Over four synthetic draws (θ and labels) the reference
784                                                                         0.37–0.66 (formatting) and 0.09–0.24 (hedging); own −
      learner is stable (+2.4 to +3.1 at +5 points, +6.4 to +8.0 at
785                                                                         other at k = 20 / 50 for the low-rank latent +0.09 / +0.05
      +10), PAL-B on full features detects the +10-point panels
786                                                                         and −0.18 / −0.08, VPL −0.05 / +0.04 and +0.03 / +0.03,
      in all four (lower bounds +1.16 to +3.23) and the +5-point
787                                                                         PAL-B (compressed features) −0.24 / −0.12 and +0.27 /
      panels in none (+0.26 to +1.40), and the low-rank latent
788                                                                         +0.40 [−0.02, +0.85]; reference learner own − population
      detects neither in any draw (−0.31 to +0.15). A limitation
789                                                                         +2.57 [+1.61, +3.57] and +7.44 [+5.96, +8.91]. No method
      of all synthetic panels: they are noisier than the real data
790                                                                         detects either panel. S7-5 (Amendment 4), the in-span
      (rater-pair direction agreement 0.59 at τ = 0 against 0.673
791                                                                         panels over four draws (θ and label seeds 1, 11, 12, 13): the
      [0.666, 0.680]; Krippendorff’s α 0.11 against 0.28), and
792                                                                         low-rank latent’s own − other at k = 20 is +1.97, +2.83,
      adding item fixed effects to the generator did not close the
793                                                                         +3.14, +1.44 [+0.92, +1.96] at +9.3 to +10.9 oracle points
      gap (0.60), nor does it reproduce the small effect of style
794                                                                         (detected in 3 of 4; k = 50 +5.0 to +7.3) and +0.00 to +0.14
      offsets on direction (+0.32 real vs −0.07 at τ = 0); the cali-
795                                                                         at +4.7 to +5.5 (0 of 4); the reference learner +7.4 to +8.3
      brations transfer to the real data only approximately, with
796                                                                         and +2.6 to +2.9. Both statements are kept under the rule
      no claimed direction of bias.
797                                                                         fixed beforehand.
798   LoRe on all panels (Stage 6). Across PRISM pairs and
                                                                            Confirmatory and exploratory results. Confirmatory (rule
799   MultiPref, binary and graded labels and k ∈ {5, 20, 50},
                                                                            fixed before the result): the stage-2a hypotheses H1–H5 and
800   LoRe never improves direction or choice accuracy over its
                                                                            their replications (H6, on the symmetric offsets, was added
801   own k = 0 version or over the text-only model (own gain
                                                                            after the first results and is exploratory; its later replications
802   −6.2 to +0.1 points; the regularised version −1.1 to −0.0),
                                                                            were evaluated prospectively); B1–B3; C1–C4; R1 (PRISM
803   and its log-likelihood is below the text-only model’s every-
                                                                            native choices); the Stage-3 positive control at +1.7 and
804   where. Its own − other is positive in some cells (MultiPref
                                                                            +5.2 oracle points (no power); the Stage-4 ceiling rule (not
805   binary, k = 20: +1.3 [+0.5, +2.0]) while its own gain is neg-
                                                                            met); the Stage-6 LoRe rule (PRISM null not withdrawn).
806   ative there (−1.2 [−1.9, −0.5]): another rater’s over-fitted
                                                                            Exploratory (added or changed after a result, labelled in
807   weights are anti-informative, the scale problem discussed
                                                                            the text): the symmetric offsets DFs and their hypothesis;
808   for the reference learner, so own − other alone is not ev-
                                                                            the few-shot-tuned prior; the +10 and +21 panels and the
809   idence of personalisation for methods whose few-shot fit
                                                                            full-feature runs; the reference learner and its oracle-scale
810   over-fits.
                                                                            contrast; the calibrated real-data aspect test; the regularised
811
      Stage 7 (after the seventh review; PROTO-                             LoRe; the two-way bootstrap re-estimates.
812
      COL STAGE7.md). S7-1, cross-fitted ridge probes
813                                                                         Reproducing LoRe’s PRISM result (Stage 6, Amend-
      (prompt-group folds, out-of-fold R2 ) of the two injected
814                                                                         ments 2–3). Unseen-user binary accuracy, mean ± sd over
      features from each learner’s inputs: log length ratio 0.88
815                                                                         five random user splits, LoRe’s native setting (users with at
      (VPL/PAL-B PCA-256 x B − x A), 0.93 (full features),
816                                                                         least six dialogues split 50/50, half of each user’s conversa-
      0.73 (D/DL joint PCA-256); random direction 0.65, 1.00,
817                                                                         tions for few-shot and half for test, one chosen-vs-other pair
      0.02. By the rule fixed beforehand, S7-2 was run for
818                                                                         per conversation; 1,267 users, about three few-shot pairs per
      the low-rank latent only: the random direction re-drawn
819                                                                         unseen user):
      inside its joint embedding (orthogonal to the consensus
820
      direction), τ calibrated to oracle gains of +5.1 and +10.4.           Taking one pair per interaction instead (every turn; 20 pairs
821
      Own − other at k = 20 / 50: +0.08 [−0.18, +0.33] / +0.03              per user) gives 58.8 / 59.2 / 57.0 with our features. The
822
      [−0.29, +0.34] at +5.1; +1.97 [+1.31, +2.65] / +7.02                  remaining differences — a stronger monolithic baseline here
823
824
                                                                       15
                                          What Do Gains in Personalised Reward Modelling Measure?

825                embeddings                                         monolithic BT        LoRe, no adaptation     LoRe, few-shot fit
826                Skywork-Reward-Llama-3.1-8B-v0.2 (LoRe’s)          67.4 ± 1.1           67.3 ± 1.8              63.6 ± 3.7
827                Qwen2.5-7B-Instruct (ours)                         67.7 ± 1.5           68.7 ± 1.7              61.0 ± 2.5
828                published (Bose et al., 2025)                      61.0 ± 1.2           —                       71.0 ± 1.0
829
830
831   and a few-shot fit that helps there but hurts here — could not             the population state can improve with anyone’s ratings, the
832   be traced to any setting the LoRe paper reports. Under our                 contrast is the method adapted on the rater’s own k rat-
833   protocol (user- and conversation-disjoint folds) the Skywork               ings minus the same method given another test rater’s
834   embeddings leave the conclusion unchanged: LoRe’s own                      adapted parameters (a random derangement within fold, k
835   gain at k = 20 is −1.3 [−2.5, −0.2] points (regularised −0.5               and draw). Before the runs we fixed that the protocol has
836   [−1.3, +0.2]) and own − other +0.2 [−0.9, +1.2], as with                   power at a strength if some content-interacting method has
837   our features.                                                              a lower 95 % bound above +1 point at k = 20; the +10 and
838                                                                              +21 panels and the untuned-prior low-rank runs were added
      Positive-control details (moved from §5.6). In the ex-
839                                                                              after the first results and are exploratory.
      ploratory dose-response, VPL and PAL-B detect +21-point
840
      preferences but recover less than half a point of +10; on                  5.7 How much room is there? (full text moved from
841
      the real data they are at the null-control level, and the low-             §5). Every MultiPref annotation carries the annotator’s own
842
      rank latent’s +0.30 [−0.00, +0.60] is matched by the text-                 helpfulness, truthfulness and harmlessness preferences, so a
843
      independent offsets (+0.32), i.e. scale use. With full features            rater’s trade-off between these values is observable. With
844
      PAL-B detects +10 points but not +5. How far are these                     the rater’s own aspect labels as inputs (an oracle for the
845
      methods from what the data allow? A well-specified                         content side), a pooled trade-off already gets 97.5 % of
846
      reference learner — the two injected features known, an                    directions right, and a rater-specific trade-off fitted on all of
847
      empirical-Bayes prior on each rater’s weights, style offsets               the rater’s training ratings adds only +0.10 [−0.24, +0.43]
848
      re-fitted — recovers +0.89 [+0.40, +1.37], +3.1 [+2.3, +4.0]               points (+0.44 even in-sample). The three recorded aspect
849
      and +8.0 points of +1.7, +5.2 and +10.1-point oracle gains                 judgements point in opposite directions in only 4.0 % of
850
      from 20 ratings (own versus population weights, the oracle’s               held-out non-tie comparisons; there individual trade-offs
851
      scale). Linear probes show the injected direction is available             matter (in-sample +9.7 points), but they are too rare to move
852
      to VPL and PAL-B (out-of-fold R2 0.65 compressed, 1.00                     accuracy. A calibrated test with the item’s consensus aspects
853
      full) but not to the low-rank latent’s joint embedding (0.02);             from other annotators finds individual weights transferring
854
      re-injected inside that embedding, the latent detects +10                  worse than the population’s (−0.28 [−0.56, −0.06] at k =
855
      points (3 of 4 draws) but not +5 (0 of 4). With semantic                   20; exploratory, Appendix B).
856
      axes (formatting, hedging/refusal) no method detects even
857                                                                              5.9 Developers rating code readability (full text moved
      +9.7 points. Twenty ratings permit useful recovery in these
858                                                                              from §5). Two code-readability studies have persistent de-
      injected families when the generating features are supplied;
859                                                                              veloper identities: Buse–Weimer (121 raters × 100 Java
      the observed gap implicates feature representation and the
860                                                                              snippets) and Dorn (3,393 developers with at least ten rat-
      learners’ inductive biases. These are comparisons with syn-
861                                                                              ings of 360 Java/Python/CUDA snippets). With Qwen2.5-
      thetic panels of specific injected forms (noisier than the
862                                                                              Coder-7B features, scale use transfers to new developers:
      real data), not formal exclusion bounds; details and seed
863                                                                              offsets gain +0.054 [+0.036, +0.074] nats per rating at k
      variability in Appendix B. Generator and calibration as first
864                                                                              = 20 (Buse–Weimer) and +0.040 [+0.031, +0.049] at k
      described: We keep MultiPref’s structure (raters, items, who
865                                                                              = 10 (Dorn). For content we measure within-developer
      rated what, folds and k-shot draws) and replace the labels
866                                                                              concordance of predicted and given ratings over snippet
      by semi-synthetic ones. A generator — the text-only head
867                                                                              pairs, comparing a developer’s own weights with popula-
      plus scale-use offsets, fitted on all ratings — gives each
868                                                                              tion weights under the same offsets. SAP with 22 classical
      rating a distribution, to which a rater-specific content term
869                                                                              readability attributes (line and identifier length, indentation,
      (θr⊤ gi ) (−2, −1, 0, 1, 2) is added to the logits; gi are two fea-
870                                                                              nesting, comments, operators, . . . ) gives +0.40 [−0.25,
      tures of the response pair (the log length ratio and a random
871                                                                              +1.06] points at the pre-set k = 20 on Buse–Weimer (+1.30
      direction in the per-response embedding space, orthogonal
872                                                                              [+0.46, +2.18] at k = 50, exploratory) and −0.19 [−0.81,
      to the consensus quality direction) and θr ∼ N (0, τ 2 I).
873                                                                              +0.42] on Dorn; the low-rank latent is inconclusive on Buse–
      The scale τ is calibrated on the generator alone so that an
874                                                                              Weimer and switched off by validation on Dorn. Details,
      oracle that knows θr gains +1.7, +5.2, +10.1 or +21.1 points
875                                                                              the pre-set rule’s literal outcome on Dorn (met through the
      of direction accuracy on the test ratings; τ = 0 is a null
876                                                                              own − other contrast, which is not on the oracle scale) and
      control. Every method is then run under the paper’s proto-
877                                                                              permutation controls are in Appendices A–B.
      col. Because a method whose unpersonalised state is not
878
879
                                                                            16
                                       What Do Gains in Personalised Reward Modelling Measure?

880   C. Implementation                                                      out likelihood over random cells (every held-out rater and
881                                                                          item appears in training), and chooses all penalties by inner
882   Rater identities. All four panels carry persistent rater iden-         cross-validation.
883   tifiers (MultiPref pseudonyms, 227 evaluators, median 166
      ratings, never twice on one item; DICES rater IDs, 123                 Reproducibility. With the split-half estimator defined
884
      raters × 350 items in the release, 104 after its quality fil-          above, the reliability of the rating distribution’s shape be-
885
      ter (used throughout); PRISM user IDs, one survey record               yond its exact mode and mean is ρ = 0.25 [0.22, 0.29] on
886
      each; Community Alignment annotator IDs). Demographics                 MultiPref overall preference with three raters (helpful 0.29,
887
      never vary within an ID on DICES and in fewer than 0.3 %               harmless 0.21): the raw few-rater distribution forecasts a
888
      of IDs on Community Alignment. On MultiPref, which has                 new rater worse than its own location (ρ < 12 ). Text decod-
889
      no demographics, an evaluator’s tie rate and extreme-rating            ability. A cross-fitted ridge decoder on frozen Qwen2.5-
890
      rate in the first and second half of their ratings (by times-          7B-Instruct features, scored on an independent rater panel,
891
      tamp) correlate at 0.82 and 0.78 across evaluators, against            recovers G/X = 10.5 % [5.7 %, 11.9 %] of the reproducible
892
      −0.03 and 0.00 (largest 0.17) with evaluator labels shuf-              shape (within-cell permutation control ≤ 0; positive control
893
      fled (check rater ids.py). Shared accounts cannot                      0.35) — comparable to the upper end for ordinal quality
894
      be ruled out.                                                          ratings (upper bounds 0.4–10 %) and below NLI (17–26
895
                                                                             %). Rater vs item. A long-format ordered-probit decom-
896   Text features: last-token final-layer states of Qwen2.5-7B-            position with real rater identities and penalties tuned by
897   Instruct under a 5-point judge prompt (MultiPref, PRISM)               inner cross-validation: rater-specific thresholds improve
898   or a 3-level safety prompt (DICES), label-free PCA to 256              held-out likelihood by +0.036 nats per rating over item lo-
899   dimensions. Folds: 5 rater folds (stratified by group) × 5             cation alone, item-specific dispersion by a further +0.0014
900   prompt-group folds; validation: 15 % of training prompt                (ratio 25; 19–36 across the five folds); of the rater part, rater
901   groups. k-shot draws: 5 per k, identical across all models             scale contributes +0.031 and rater shift +0.005.
902   (RC-LoRA: draw 0 only). PRISM item folds are by conver-
903   sation. Bootstrap: rater clusters, B = 2,000. LoRA: r = 16 on
904   all attention and MLP projections, lr 10−4 , one epoch, accu-          E. Protocols and what did not hold
905   mulation 8. VPL / PAL-B: official architectures (latent 512,           All analyses are documented in an analysis log: times-
906   hidden 512; d pref 512, mlp2-gelu projectors, angle learner)           tamped internal protocols written before each stage (not
907   with an ordered-logistic link for graded labels; VPL’s KL              public registrations, so they document rather than certify
908   weight selected from {0.01 (official), 0.001, 0} and PAL-B’s           the order of decisions); changes after results are logged as
909   adaptation ridge by k-shot validation (non-official choices            amendments with reasons, and the symmetric style model
910   made to prevent collapse and over-fitting).                            DFs and its hypothesis were added after the first full result.
911
                                                                             Not supported or not robust: (i) the stage-1 decision rule
912
913
      D. Where is the predictable structure?                                 returned “mixed” (text decodability not ≤ 10 %); (ii) non-
         Estimators and results                                              inferiority of the 5-parameter DF to the low-rank latent (DF
914
                                                                             − DL ≥ −0.005) holds with the training-rater prior but not
915   Estimators. For an item with ratings on K ordered lev-                 with a few-shot-tuned prior on MultiPref (−0.015) and is
916   els, let h be the empirical rating distribution and C the              formally not met on PRISM (bound −0.006); (iii) “scale
917   cumulative operator. Split the item’s raters at random                 beats shift” holds only on MultiPref; (iv) the originally reg-
918   into disjoint panels P1 (a raters) and P2 , and let q be a             istered probit-family hypothesis is not supported (F1 − D =
919   cross-fitted location-only forecast with exactly the mode              +0.020 [−0.001, +0.041], the primary probit contrast after
920   and mean of P1 (built from other items in the same mode-               Amendment 1; homoscedastic F − D = −0.029 [−0.049,
921   and-mean cell). With r1 = C(h1 − q), r2 = C(h2 − q),                   −0.008]; superseded when the primary family was moved
922   M = ∥r1 ∥2 /n and X = ⟨r1 , r2 ⟩/n, the forecasting value              to the distributional head); (v) the prediction that published
923   of the raw distribution over its own location obeys the iden-          user latents encode style failed (R2 ≈ 0); (vi) the hybrid’s
924   tity S(h1 ) − S(q) = M − 2X under the ranked probability               non-inferiority to DFs is formally not met (bound −0.014).
925   score, so ρ = X/M is a split-half reliability of the distri-           Four baseline problems found during the study were fixed
926   bution’s shape and the raw distribution beats its location             in favour of the baselines — a missing constant column in
927   exactly when ρ > 1/2. Text decodability is the proper-                 the low-rank latent, a scale non-identifiability in the probit
928   score gain G = (2⟨r̂, r2 ⟩ − ∥r̂∥2 )/n of a residual r̂ decoded        group model, VPL’s posterior collapse, and PAL-B’s near-
929   from frozen text features, cross-fitted over prompt groups,            unregularised adaptation — and the runs before each fix are
930   reported as the fraction G/X of the reproducible shape.                reported.
931   The rater–item decomposition fits ordered-probit models
932   Yir∗ = θi + δr + σi σr ε with item locations θi , rater shifts
933   δr , rater scales σr and item dispersions σi , compares held-
934
                                                                        17
                                       What Do Gains in Personalised Reward Modelling Measure?

935   F. Community Alignment analysis log (Stages                           implies +2.8 for this learner at k = 20 (oracle +4.2; with
936      8, 11, 12)                                                         event-level simulated labels that keep one winner per choice
937                                                                         event, +1.9 and oracle +3.6 — a third lower, just inside the
938   The full sequence of analyses behind §6, in order, with the           pre-set factor-1.5 tolerance, Stage 11 Am. 6). The gap is not
939   corrections of the fifth review applied (event-level simula-          mysterious: on the evaluated split transfer from support to
940   tion as the principal achievable-gain benchmark, the pair-            test prompts is established for length (0.41 [0.27, 0.55]) but
941   level one as a consistency check; Holm as an approximate              not for paragraphs or lists (intervals cover 0), heavier-tailed
942   sensitivity analysis). Protocols: PROTOCOL STAGE8.md                  or concentrated deviations with the same covariance lower
943   (Am. 1–2), PROTOCOL STAGE11.md (Am. 1–10), PRO-                       the simulated gain of this learner to +1.6 to +0.4 (event-level:
944   TOCOL STAGE12.md.                                                     +0.9 to −0.4) (so covariance alone does not determine learn-
945   On a dataset built for preference diversity, user-specific            ability; this does not show that concentration explains the
946   signal exists; estimated choice gains remain small. Com-              real data), and the full-size prior over-adapts. With the at-
947   munity Alignment (first turns, 2,957 new users in five coun-          tribute set and prior scale chosen on pseudo-new training
948   tries, the chosen response paired with each other one; Stage          users (c = 0.125–0.25 in every fold, never “no adaptation”),
949   8): at k = 20 every method’s own gain over its own k =                transfer-calibrated adaptation gains +0.49 [+0.20, +0.77]
950   0 version has an upper bound below +0.5 points (VPL                   choice points and +0.0088 [+0.0061, +0.0116] nats on
951   +0.15 [+0.03, +0.27], LoRe-reg +0.35 [+0.25, +0.46], LoRe             the frozen test users, ahead of the tuned rank-2 model by
952   −2.34 [−2.79, −1.88]), yet a user’s own adapted parame-               +0.30 [+0.04, +0.56] points — but not of ordinary validated
953   ters beat another user’s — the frozen rule’s own − other              shrinkage: an isotropic prior over the same three attributes,
954   half, which a summary-script bug first dropped and which              its scale chosen the same way (τ 2 = 0.1 in every fold),
955   therefore literally reads “content personalisation detected”:         gains +0.66 [+0.37, +0.95] points and +0.0110 nats, and
956   LoRe +3.27 [+2.85, +3.70], LoRe-reg +0.36, VPL +0.31.                 TRV − isotropic is −0.17 [−0.29, −0.05] (not significant
957   A within-country derangement (added after the result) re-             after multiplicity adjustment). No advantage of the esti-
958   tains the contrast, so country and language do not explain            mated covariance is established; what helps is the choice of
959   it (own − same-country other +3.22 [+2.83, +3.60]; same-              attributes and strong shrinkage (light adaptation). A prompt-
960   country − any-country +0.03 [−0.12, +0.18]). A cross-                 group × user two-way bootstrap widens TRV’s interval to
961   fitted, simulation-calibrated diagnostic agrees on what the           [+0.01, +0.97]. These are below the one-point threshold, at
962   signal is: users’ deviations from the population weights on           a different budget (20 choice events, three dependent pairs
963   response length and paragraphing reproduce across disjoint            each) from Stage 8’s 20 pairs, where VPL and LoRe-reg
964   prompt sets (transferable variances 0.32 [0.25, 0.40] and             also show small positive own gains. Frozen evaluation on
965   0.72 [0.23, 1.29]; 0.33 and 0.76 [0.26, 1.35] after prompt-           new prompts (Stage 12). TRV, unchanged, on the same
966   type adjustment; exploratory, Stage 11; with 200 simulation           users’ second turns (83,238 never-analysed choices; 1,702
967   replicates the length false-detection rate is 5.0 % [2.4, 9.0]        test users at k = 20 events): +0.38 [+0.13, +0.64] choice
968   and paragraphs’ power 85 % [79, 89], so neither calibra-              points and +0.0046 [+0.0031, +0.0063] nats per pair over
969   tion target is established beyond binomial error), while no           µ; validated isotropic shrinkage +0.31 [+0.05, +0.58] and
970   method converts them into a one-point gain at k ≤ 50. Users’          +0.0038; TRV − isotropic +0.07 [−0.07, +0.22]; the tuned
971   stable prompt mixes could create such residual structure              rank-2 model selects no adaptation in three of five folds
972   without different preferences on the same tasks; as an obser-         (−0.05). By the pre-set rules the benefit is reproducible
973   vational check the length cross-covariance centred within             (both lower bounds above 0) and sub-threshold (accuracy
974   language × prompt-cluster cells is 0.206 [0.183, 0.231]               upper bound below +1), with no advantage over ordinary
975   against 0.210 uncentred, and a same-language user with                shrinkage; the prompt-group × user interval for accuracy
976   a matched task mix (cluster shares within L1 0.002) is a              covers 0 ([−0.04, +0.83]). No language reaches signifi-
977   worse predictor than the user’s own coefficient by +0.80              cance alone. The length cross-moment again reproduces
978   [+0.45, +1.16] points and +0.009 nats, though better than             across disjoint prompt halves in every fold (0.12–0.19), the
979   a random other by +0.75; the two contrasts approximately              list/heading one does not (negative in two folds). These are
980   partition the unmatched own − other (+1.54), which is not a           new prompts and turns of previously studied users, not new
981   causal decomposition, and the matched other is about 0.35             users. Multiplicity (Am. 10; an approximate, exploratory
982   points worse than the population model (Stage 11 Am. 8).              sensitivity analysis: p-values recovered from reported
983   Two annotators agree on 64.3 % of shared response pairs,              intervals by a symmetric normal approximation, ques-
984   the text-only model is right on 71.7 % of them. Using the             tionable for heavy-tailed cross-moments, then Holm at
985   transferable covariance as the prior (θ̂ u − µ = c Ĉ (I +            0.05). In Stage 8’s frozen family (six methods × two con-
986   c I u Ĉ)−1 s u over length, paragraphs and list/heading, Ĉ          trasts) the own − other contrasts of LoRe, LoRe-reg, VPL
987   estimated on training users only; S11-3) gives +0.13 [−0.28,          and PAL4 survive, and the detection is unchanged; the posi-
988   +0.53] points at c = 1, although the fitted Gaussian model            tive own gain of VPL (+0.15) and the negative own effects
989
                                                                       18
                                        What Do Gains in Personalised Reward Modelling Measure?

990    of PAL4 and DFp do not. Across a family of 29 selected                 after the pre-registered EM update was found to stall when
991    Stage-11 contrasts (not every reported contrast; e.g. AUC              raters have few ratings (EM results in Appendix B); the
992    contrasts, the k = 32 within-cluster and matched − cyclic              shared-variance column uses the same update; the rank-
993    contrasts are omitted), the length statements survive (trans-          2 model’s map ridge and adaptation strength (including
994    fer, within-cluster transfer, own − matched other, TRV and             none) are selected on held-out training raters at k = 20.
995    isotropic gains, WIMHF-style length), while paragraphs’                Exploratory: the ablations and the out-of-dictionary panels.
996    transferable variance, TRV − rank-2, TRV − isotropic and
                                                                              SAP recovers what the published learners miss and matches
997    the new-user length gain of S11-1 (b) (+0.45) do not; the
                                                                              the learner told the features; attribute-specific variances
998    first-turn evidence that isotropic shrinkage beats TRV is
                                                                              improve recovery over one shared variance under the same
999    therefore weaker, but no advantage of TRV is established
                                                                              update (which loses 60–76 % of the gain); a rank-2 subspace
1000   either. Status: the original Stage 11 diagnostic failed its
                                                                              on the same attributes, tuned with the same care, matches
1001   pre-specified calibration criterion, leaving all three primary
                                                                              SAP on the semantic panels and abstains on the null (un-
1002   outcomes inconclusive and the adaptation gate unmet; all
                                                                              tuned, it lost 2.1–2.7 points; Appendix B), while on real
1003   subsequent analyses are exploratory; the final procedure se-
                                                                              MultiPref SAP is ahead of it by +0.41 [+0.15, +0.66] points
1004   lected attributes and shrinkage on training users only, but its
                                                                              (paired, exploratory). The variance assigned to correlated
1005   candidate family was developed after inspecting test results,
                                                                              attributes means the high-variance set is a set of candidates,
1006   and the bootstrap intervals are nominal and do not account
                                                                              not independently identified preference dimensions. SAP
1007   for this adaptation. Ĉ is an uncentred cross-moment of one-
                                                                              learns transferable shrinkage over supplied axes; it does not
1008   step deviations, not a bounded share of the fitted random-
                                                                              discover new ones (outside the dictionary it recovers under
1009   slope variance; the principal achievable-gain benchmark is
                                                                              a tenth of a +10.5-point preference). With the fixed-point
1010   the event-level simulation (one winner per choice event, Am.
                                                                              update its estimated effects on the four null draws are near
1011   6); the pair-level figures are a consistency check, and both
                                                                              zero (−0.03 . . . +0.11 at k = 20 and 50; with EM it lost up
1012   are model-implied gains for specified learners, not general
                                                                              to 0.5 points at k = 50); this is not a calibrated false-positive
1013   learnability ceilings.
                                                                              rate, and forced adaptation does hurt on Community Align-
1014
                                                                              ment (below). On real MultiPref its gain over population
1015   G. Screened attribute personalisation                                  attribute weights (the rater’s offsets kept) is +0.28 [−0.00,
1016
1017
          (formerly §5.8)                                                     +0.58] direction points and +0.0028 [+0.0013, +0.0043]
                                                                              nats per rating — SAP’s achieved gain under this proto-
1018   §5.6 locates the failure: 20 ratings suffice when the con-             col, not a bound on what these attributes could offer. The
1019   tent axes are known, and the published learners do not find            decisive test was frozen before its data were embedded:
1020   them. Screened attribute personalisation (SAP) supplies                Community Alignment’s native choices (1,897 new users
1021   candidate axes and learns from the training raters which of            in five languages, k = 20 choice events, per-language popu-
1022   them people differ on. Each comparison is described by 24              lation weights, adaptation strength of every method chosen
1023   interpretable attribute differences fixed in advance (length,          on held-out training users). The fitted model assigns sub-
1024   markdown structure, hedging/refusal, code, digits, ques-               stantial training-user variation to length, paragraphs and
1025   tions, pronouns, sentence and word length, examples, dis-              formatting (prior variances 0.29–0.37 for length, 0.25–0.30
1026   claimers, summaries, evidence phrases, politeness, refusal,            for paragraphs, 0.19–0.23 for list/heading lines; one fold
1027   lexical diversity, overlap with the prompt, . . . ); a rater’s         assigns 1.37 to URLs, ≈ 0 in the others), yet adaptation
1028   content term (θr⊤ ai )(−2, . . . , 2) is added to the scale-use        from 20 choice events does not improve held-out prediction:
1029   model’s logits, with θr ∼ N (µ, diag σ 2 ), the population             validation switches SAP off in all five folds, forcing it costs
1030   weights µ and the per-attribute variances σ 2 estimated on             −0.40 [−0.87, +0.06] choice points and −0.0097 [−0.0143,
1031   the training raters by automatic relevance determination               −0.0052] nats, and the tuned low-rank model gains +0.17
1032   (Laplace approximation, MacKay’s fixed-point update); a                [−0.17, +0.51]. The pre-set rule (lower bound above +1
1033   new rater’s θr is their MAP from k ratings. The contrast is            point) is not met.
1034   the rater’s own weights against the population weights µ,
1035   with the rater’s own scale-use offsets kept (oracle scale).
1036
1037   Own minus population weights, direction accuracy at k = 20
1038   in points, 95 % rater bootstrap (ranges over four synthetic
1039   draws; VPL / PAL-B / low-rank latent: own − other on the
1040   same panels, §5.6). Rules fixed in advance: no detection
1041   on the null draws (none), detection of the semantic panels
1042   in at least three of four draws (four of four each). The
1043   SAP column uses the fixed-point variance update adopted
1044
                                                                         19
                                       What Do Gains in Personalised Reward Modelling Measure?

1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068   panel (oracle gain)                                 SAP                                         one shared variance    same attributes, rank-2 subsp
1069
1070   null, 4 draws (0)                                   −0.03 . . . +0.04                           +0.06                  0 (abstains)
       formatting + hedging (+4.6), 4 draws                +2.29 . . . +2.82                           +0.69 [+0.21, +1.18]   +2.78 [+1.84, +3.72]
1071   formatting + hedging (+9.7), 4 draws                +7.44 . . . +8.12                           +3.09 [+2.13, +4.02]   +7.75 [+6.09, +9.36]
1072   two axes outside the dictionary (+10.5)             +0.95 [+0.50, +1.39]                        —                      —
1073   real MultiPref                                      +0.28 [−0.00, +0.58]                        +0.28 [+0.04, +0.53]   −0.14 [−0.51, +0.24]
1074   real MultiPref, ratings permuted within item        −0.09 [−0.23, +0.05]                        —                      —
1075   Community Alignment, frozen, k = 20 choice events   0 (abstains); forced −0.40 [−0.87, +0.06]   −0.70 [−1.15, −0.25]   +0.17 [−0.17, +0.51] (tuned
1076
1077
1078
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
