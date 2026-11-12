Round 11. Since your round-10 review the paper gained a post hoc Stage 14: (i) a Jester positive control showed the published adaptation pipeline recovered only ~10 % of a collaborative-filtering reference; (ii) the defect was diagnosed (isotropic adaptation prior on an unstandardised latent; rater-side penalties chosen by training raters' validation likelihood) and corrected ("rung a": whitened adaptation prior; "rung b": additionally selecting rater-side penalties by pseudo-new-rater concordance); (iii) the held-out-item panels (semi-synthetic MultiPref with injected preferences, real MultiPref, DICES, Dorn, PRISM) were re-run with the corrected latent models, and the main-text rows/figure for the low-rank latent (DL) were replaced by rung-a values, labelled post hoc.

Below are (A) the typeset paper (pdftotext -layout of the rebuilt PDF), (B) the Stage 14 protocol with its amendment and results sections, (C) the machine-generated result summaries (stage14_fix.md: Jester seen jokes; stage14_real.md: held-out items), (D) the claims ledger.

Please review ONLY what Stage 14 touches, as a sceptical ICML reviewer and statistician:
1. Numbers: check every Stage 14 number in the paper (A) against (B) and (C). List each mismatch with page, quoted text, and the correct value. Also check internal consistency across abstract, §5.1/5.2/5.5/5.6, Table 2, Figure 2 caption, Appendix A/B/E and the limitations section.
2. Inference: is each Stage 14 claim in the paper supported at the strength stated? In particular: (a) "the corrected pipeline detects injected +10-point preferences but not +5"; (b) "no content taste beyond scale-use offsets on MultiPref"; (c) the PRISM statement (softmax latent 0.004 nats ahead of the offsets in likelihood with no within-rater ranking gain) and its labelling under the pre-written rule as "contradicted"; (d) adopting rung a and treating rung b as a sensitivity analysis; (e) the statement that the pre-written direction clause is ill-posed on single-response panels. Say where a claim is too strong, too weak, or relies on a post hoc choice that is not disclosed clearly enough.
3. Garden of forking paths: the correction, the choice of rung, and the reading on single-response panels are all post hoc. Is the disclosure adequate in the main text (not only the appendix)? What would you require (e.g. which numbers must be shown side by side, what must be stated in the abstract/limitations)?
4. Missing controls: name at most three additional analyses that would most change your confidence in the Stage 14 conclusions, in priority order, each feasible with the existing data (no new human data).
5. One paragraph: does Stage 14 strengthen or weaken the paper's main claim (personalised reward-model gains are mostly scale use, not content taste), and how should the paper's framing change, if at all?
Be concrete and concise; quote and give page numbers.

=== (A) PAPER (typeset text) ===
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
069   jointly, and a position-only predictor is also informative             (Koren et al., 2009), user-specific ordinal thresholds predict
070   (§6). (3) Beneficial personalisation needs a competent                 personal rating distributions (Koren & Sill, 2011), and an-
071   population baseline. Own-versus-other contrasts do not                 notator models estimate rater-specific labelling behaviour
072   measure benefit; gains over the population model are small             (Dawid & Skene, 1979; Raykar et al., 2010; Hovy et al.,
073   (+0.3 to +0.7 choice points where established), not estab-             2013; Deng et al., 2023; Plank, 2022; Uma et al., 2021).
074   lished on MultiPref, and the measured gain changes by                  Our offsets are of this kind and are not new; what is new
075   about 0.6 points with the population-training procedure                is testing personalised reward models against them on new
076   alone (§6). Semi-synthetic positive controls characterise              raters and asking what these models could detect.
077   the evaluated learners’ recovery of specified injected pref-
078   erence families (§5.6); a screened attribute learner and the           3. Data, and where the predictable structure
079   covariance-calibrated procedure are reported as supporting
080   tools (Appendix G, F). Protocols, amendments and failed
                                                                                sits
081   hypotheses are in Appendices A, B, E and F.                            Data. MultiPref (Miranda et al., 2025; 10,461 comparisons;
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
129   Let ℓ(x) ∈ RK be the class logits of a text-only distributional                  Protocol. 5 paired splits; split f holds out rater fold f (20 %
130   reward model for item x (K ordered rating levels). For                           of raters, stratified by group) and prompt-group fold f (20
131   rater r we add a text-independent offset vector (Figure 1):                      % of prompt groups); models are trained on training raters
132   p(y | x, r) = softmax(ℓ(x) + br ). Variants: DF (br ∈                            × training items with penalties chosen on a validation split;
133   RK , free), DFs (two-sided preference scales only: br tied                       each test rater is adapted on k ∈ {0, 5, 10, 20, 50} of their
134   symmetrically, (e, s, t, s, e) — extreme, slight, tie — 3                        ratings of training items (5 random draws) and evaluated
135   parameters, of which 2 are identifiable because the softmax                      on their ratings of held-out items. Primary metric: held-out
136   is invariant to a common shift; no A-vs-B position term).                        log-likelihood per rating; also RPS and preference-direction
137   Rater offsets have a Gaussian prior centred on the training-                     accuracy; rater-cluster bootstrap (B = 2,000). Because test
138   rater mean; a new rater’s offsets are the MAP estimate from                      raters share test items on MultiPref and DICES, the headline
139   k of their ratings with the text model frozen. Baselines                         k = 20 contrasts were also re-estimated with a two-way boot-
140   under the same protocol: D (text-only distributional RM),                        strap that resamples raters and prompt groups independently:
141   DG (group offsets: crowd/expert, race, region), DL (low-                         on graded labels every log-likelihood interval widens by at
142   rank text-interacting latent: ℓ(x) + (W x + w0 ) · zr , d = 8,                   most 0.007 on either side and no log-likelihood conclusion
143   the personalised-RM family). An interpretable probit family                      changes; direction-accuracy differences of about a point or
144   (rater shift / log-scale on an ordered-probit text head) is                      less (the style model’s +0.5 on MultiPref, VPL’s direction
145   reported as a secondary analysis.                                                advantage over the style model) lose significance and are
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
158   and the text model frozen — a convex problem in 3–5 param-                       tuned 8-dimensional text-interacting latent at every k (dif-
159   eters, solved in milliseconds. Any text model that outputs                       ferences within 0.005 nats); fitting a rater’s A-vs-B position
160   graded log-probabilities can be used: we use a ridge head on                     from few ratings costs direction accuracy.
161   frozen LLM features (§5.1–5.2), a LoRA-fine-tuned LLM
162                                                                                    Reference points. To size these gains: on MultiPref at k
      reward model (§5.3) and the decoder of a published person-                       = 20 a uniform forecast scores −1.609 nats per rating, a
163   alised reward model (§5.4).
164
                                                                                 3
                                                                  What Do Gains in Personalised Reward Modelling Measure?

165                                              MultiPref (pairwise preference)                   DICES-350 (safety)                      PRISM (response ratings)
166         log-lik. per rating vs D
167
168                                    0.1
169
170                                    0.0
171
172
173                                    0.1
174                                              0 5 10 20                      50        0 5 10 20                      50            0 5 10 20                      50
175                                                ratings of the new rater (k)             ratings of the new rater (k)                 ratings of the new rater (k)
176
177                   style offsets, symmetric (DFs)                        style offsets (DF)          low-rank latent (DL, tuned, corrected prior)           group offsets (DG)
178
179
180   Figure 2. New raters: gain in held-out log-likelihood per rating over the text-only distributional reward model (D), as a function of the
181   number k of the new rater’s ratings used for adaptation; 95% rater-cluster bootstrap bands, 5 folds. Text-independent rater offsets (DF;
182   symmetric three-parameter DFs on two-sided preferences) gain 0.08–0.10 nats per rating at k = 20 on all three datasets; group offsets
183   (crowd/expert, race, region) gain nothing; a low-rank text-interacting rater latent with a few-shot-tuned prior ties the three-parameter DFs
184   and beats the five-offset DF on MultiPref (DF − DL = −0.020). DF, DFs and DG use the training-rater prior; DL the few-shot-tuned,
185   corrected prior (post hoc, §5.6); at k = 50 on PRISM (139 raters) tuning shrinks adaptation for offsets and latent alike (Appendix B).
186
187   Table 1. MultiPref new raters: gain in held-out log-likelihood per rating over the text-only model D, by k; 95 % rater bootstrap. DF/DFs/DG
188   use the training-rater prior; DL and DFs − DL the few-shot-tuned prior, with the latent’s adaptation prior corrected (post hoc, §5.6;
189   first-run values in Appendix A).
190                                          k   DF − D                 DFs − D                  DG − D DL − D (tuned, corrected prior) DFs − DL (tuned, post hoc)
191                                          5 +0.028 [+0.012, +0.044] +0.048 [+0.029, +0.070] ≈ 0         +0.054 [+0.038, +0.070]       −0.005 [−0.011, +0.001]
192                                          20 +0.080 [+0.055, +0.106] +0.100 [+0.074, +0.128] ≈ 0        +0.100 [+0.076, +0.128]       −0.0005 [−0.0052, +0.0049]
                                             50 +0.114 [+0.087, +0.142] +0.128 [+0.101, +0.156] ≈ 0        +0.127 [+0.100, +0.154]       +0.001 [−0.002, +0.004]
193
194
195
      forecast that ignores the text and uses only the new rater’s                                         5.3. On a fine-tuned reward model
196
      20 ratings −1.487, the text-only model −1.441, the text
197                                                                                                        With a LoRA-fine-tuned Qwen2.5-7B reward model as
      model with the three offsets −1.342, and offsets fitted in-
198                                                                                                        the text model, the three offsets still add +0.100 [+0.071,
      sample on all of the rater’s held-out ratings (an optimistic
199                                                                                                        +0.130] nats per rating at k = 20 — as on the frozen-feature
      ceiling for text-independent offsets) −1.262. Twenty rat-
200                                                                                                        head — and the gains of fine-tuning and of personalisation
      ings of a person, without the text, recover 73 % of the text
201                                                                                                        add. Against in-context personalisation (a LoRA model
      model’s gain over uniform; the offsets close about 55 %
202                                                                                                        given the rater’s k ratings in the prompt, three seeds per
      of the gap between the text-only model and the in-sample
203                                                                                                        fold) the offsets are better by +0.041 [+0.027, +0.054] nats
      ceiling. On DICES the rater’s ratings alone predict better
204                                                                                                        and +1.9 [+0.9, +2.7] direction points (Appendix B).
      than the text alone (−0.766 vs −0.840 at k = 20). Even
205
      the in-sample ceiling raises MultiPref direction accuracy
206                                                                                                        5.4. Published personalised reward models
      by only 1.3 points (0.674 → 0.687), consistent with offsets
207
      acting mainly on intensity and ties.                                                                 We reimplemented VPL (Poddar et al., 2024) and PAL-B
208
209                                                                                                        (Chen et al., 2025) from their official code as heads on
210   5.2. Replications (k = 20)                                                                           the same frozen per-response embeddings and evaluated
211                                                                                                        them under the same new-rater protocol, refitting the text-
      On DICES and PRISM the offsets gain +0.08–0.09 nats per
212                                                                                                        only and style models on those embeddings. On graded
      rating and group offsets nothing (Table 2); on PRISM the
213                                                                                                        labels, at k = 20 the style model is better than VPL by
      corrected latent is 0.004 nats ahead of the offsets, with no
214                                                                                                        +0.092 [+0.068, +0.119] nats per rating ([+0.063, +0.124]
      gain in within-rater ranking (Appendix B).
215                                                                                                        when prompt groups are also resampled) and than PAL-B by
216                                                                                                        +0.158. VPL’s latent does carry rater information once its
217                                                                                                        posterior collapse is prevented (KL weight selected as 0 or
218                                                                                                        0.001; +0.087 over its own unpersonalised version), but only
219
                                                                                                       4
                                           What Do Gains in Personalised Reward Modelling Measure?

220
      Table 2. Replications at k = 20 (nats per rating). DF − D and DG − D use the training-rater prior, DF − DL the few-shot-tuned prior with
221
      the latent’s corrected adaptation prior (post hoc, §5.6). Direction accuracy on PRISM means good-vs-bad around the scale midpoint.
222
                       dataset            DF − D                  DG − D (groups) DF − DL (tuned, corrected prior) direction acc. DF − D
223
                       DICES-350 (safety) +0.089 [+0.064, +0.117] −0.006 (race)      +0.011 [+0.005, +0.018]       +0.048 [+0.025, +0.076]
224                    PRISM (ratings)    +0.080 [+0.071, +0.090] +0.003 (region)    −0.004 [−0.007, −0.001]       +0.005 [+0.001, +0.009]
225
226
227   lifts it to the level of the text-only model; PAL-B’s few-shot                (θr⊤ gi ) (−2, −1, 0, 1, 2) is added; gi are two response-pair
228   user weights give no gain. Their user representations are                     features (log length ratio and a random embedding direction
229   unrelated to response style (cross-validated R2 ≈ 0 against                   orthogonal to consensus quality), θr ∼ N (0, τ 2 I), and τ
230   the style offsets). On binary labels — the setting in which                   is calibrated so that an oracle knowing θr gains +1.7, +5.2,
231   both methods were proposed — every method’s personalisa-                      +10.1 or +21.1 direction points (τ = 0: null control). The
232   tion gain is at most 0.002 nats (small but nonzero for PAL-B                  contrast is own adapted parameters minus another test
233   with K = 4, and for VPL and the style model at k = 50), and                   rater’s (a derangement within fold, k and draw). We fixed
234   VPL’s text head is the best binary model (the style model is                  beforehand that the protocol has power at a strength if some
235   0.010 nats behind it and 0.005 behind the text-only model,                    content-interacting method has a lower 95 % bound above
236   differences of the size of item-sampling noise): on these                     +1 point at k = 20; the +10 and +21 panels are exploratory.
237   panels the largest demonstrated gains are captured by cali-
238                                                                                 No evaluated method met the pre-specified detection cri-
      bration of graded levels and ties, which binary preference
239                                                                                 terion. In the exploratory dose-response, VPL and PAL-B
      data discard. VPL’s per-response reward head is slightly
240                                                                                 with PCA-256 features detect +21-point preferences but
      better at predicting which response is preferred (0.677 vs
241                                                                                 recover less than half a point of +10; on real data they are
      0.668), an effect present without personalisation and not
242                                                                                 at the null-control level, and the low-rank latent’s +0.30
      significant once prompt groups are also resampled (style
243                                                                                 [−0.00, +0.60] is matched by the offsets (+0.32). A later
      model − VPL: −0.9 points [−2.7, +0.8]). The offsets are
244                                                                                 real-data control (Jester; Appendix B) exposed a mis-scaled
      also a plug-in: added to VPL (fitted on the same k ratings,
245                                                                                 adaptation prior in our latent models; corrected post hoc,
      VPL frozen) they improve it by +0.088 [+0.066, +0.111]
246                                                                                 the ordinal latent detects +10 points (+2.82 [+2.02, +3.63])
      nats per rating at k = 20, come within −0.004 [−0.014,
247                                                                                 but not +5, and stays at zero on real MultiPref. A refer-
      +0.005] of the style model on likelihood (non-inferiority not
248                                                                                 ence learner that is given the two injected features recovers
      established) and keep VPL’s direction accuracy (+1.1 points
249                                                                                 +0.89 [+0.40, +1.37], +3.1 and +8.0 points of the +1.7, +5.2
      over the style model alone; rater bootstrap only).
250                                                                                 and +10.1-point oracle gains from 20 ratings, so the gap
251                                                                                 implicates representation and inductive bias (probes and
      5.5. Summary of baselines (MultiPref, new raters, k =                         re-injection in Appendix B). These results characterise re-
252        20)
253                                                                                 covery for specified injected families on panels noisier than
254   Gains are relative to each block’s text-only model (D, Dp,                    the real data; they are not formal exclusion bounds.
255   D-LoRA); the LoRA block uses adaptation draw 0 only (the
256   draw the in-context model was evaluated on), hence the                        5.7. How much room is there? Conflicts among aspect
257   style model’s +0.092 here against +0.100 averaged over five                        judgements are rare
258   draws in §5.3.
                                                                                    With the rater’s own helpfulness, truthfulness and harm-
259   Rows within a block share the text model and the raters;                      lessness labels as inputs, a pooled trade-off gets 97.5 % of
260   across blocks the text models differ (text-only direction                     MultiPref directions right and a rater-specific one fitted on
261   accuracy 0.674 / 0.670 / 0.688). VPL’s and PAL-B’s own                        all training ratings adds only +0.10 [−0.24, +0.43] points
262   gains over their unpersonalised versions are +0.087 and                       (+0.03 at k = 20): the three aspect judgements conflict in
263   −0.000.                                                                       only 4.0 % of held-out non-tie comparisons (details in Ap-
264                                                                                 pendix B).
265   5.6. Could these methods have detected content
266        personalisation? A semi-synthetic positive control                       5.8. A learner that finds the axes
267
268   A ranking null is informative only if the methods would                       A screened empirical-Bayes learner over 24 interpretable
269   detect content-dependent preferences where they exist. We                     attribute differences (SAP) recovers the semi-synthetic con-
270   keep MultiPref’s raters, items, folds and k-shot draws and                    tent preferences that the published learners miss, with near-
271   replace the labels by semi-synthetic ones: a generator                        zero effects on null panels, and abstains on real MultiPref
272   (the text-only head plus scale-use offsets) gives each rat-                   under a prospectively specified rule (+0.28 [−0.00, +0.58]
273   ing a distribution, to which a rater-specific content term                    points at k = 20). Details: Appendix G.
274
                                                                                5
                                                   What Do Gains in Personalised Reward Modelling Measure?

275
                                              Table 3. Baselines on MultiPref, new raters, k = 20, grouped by text model.
276
      text model                                   personalisation                                             gain in LL per rating vs the block’s text-only model direction accuracy
277
      frozen features (joint item embedding)    group offsets (crowd / expert)                                 ≈0                                                  0.677
278                                             low-rank latent, tuned and corrected prior                     +0.100 [+0.076, +0.128]                             0.677
279                                             style offsets, 3 numbers (DFs)                                 +0.100 [+0.074, +0.128]                             0.679
      frozen features (per-response embeddings) VPL (reimplemented)                                            +0.002 [−0.008, +0.012]                             0.677
280                                             PAL-B (reimplemented)                                          −0.065 (worse)                                      0.666
281                                             DFs                                                            +0.094 [+0.069, +0.120]                             0.668
                                                VPL + style offsets                                            +0.090                                              0.679
282   LoRA-fine-tuned Qwen2.5-7B (209 raters) in-context rater history (RC-LoRA, mean of 3 training seeds)     +0.051 [+0.024, +0.079]                             0.671
283                                             DFs                                                            +0.092 [+0.063, +0.125]                             0.689
284
285
286   Table 4. Semi-synthetic positive control (MultiPref). Own minus another rater’s k = 20 ratings, direction accuracy in points, 95 % rater
287   bootstrap; 209 new raters, 5 folds. The low-rank latent uses the few-shot-tuned prior. The injection uses one draw of θ and of the labels, so
      seed variability of the synthetic panels is not in the intervals. Last column: PAL-B on the full 3,584-dimensional features instead of their
288
      PCA-256 (exploratory; τ 2 not run). Corrected prior: the ordinal latent with a whitened adaptation prior (post hoc; τ 2 and τ 20 not run).
289
       panel                          oracle gain low-rank latent (DL)   ordinal latent, corrected prior VPL                  PAL-B                     PAL-B, full features
290
       null control (τ = 0)           0           −0.10 [−0.38, +0.17]   +0.04 [−0.11, +0.19]          −0.04 [−0.08, +0.01]   −0.23 [−0.45, +0.00]      −0.04 [−0.25, +0.17]
291    injected, τ 2                  +1.7        −0.01 [−0.29, +0.26]   —                             +0.01 [−0.07, +0.10]   −0.10 [−0.36, +0.15]      —
292    injected, τ 5                  +5.2        −0.02 [−0.28, +0.26]   +0.10 [−0.22, +0.41]          +0.01 [+0.00, +0.03]   +0.23 [−0.04, +0.51]      +0.26 [−0.14, +0.66]
       injected, τ 10 (exploratory)   +10.1       +0.09 [−0.18, +0.36]   +2.82 [+2.02, +3.63]          +0.27 [+0.02, +0.54]   +0.42 [−0.08, +0.96]      +1.95 [+1.16, +2.74]
293    injected, τ 20 (exploratory)   +21.1       +1.47 [+0.83, +2.18]   —                             +6.92 [+5.63, +8.30]   +4.62 [+3.47, +5.78]      +8.13 [+6.54, +9.77]
294    real MultiPref                 —           +0.30 [−0.00, +0.60]   −0.12 [−0.45, +0.20]          −0.01 [−0.04, +0.02]   −0.43 [−0.72, −0.15]      +0.11 [−0.16, +0.37]
295
296
297   5.9. Developers rating code readability                                                 half of it already at k = 0), while RPS drops from 0.1593 to
298                                                                                           0.1532. On single-response safety ratings the same offsets
      On two code-readability studies with persistent developer
299                                                                                           do move the safe/unsafe decision (+4.8 points on DICES),
      identities (Buse–Weimer, 121 raters, Buse & Weimer, 2010;
300                                                                                           because there a rater’s threshold is the decision. Text-only
      Dorn, 3,393 developers, Dorn, 2012) and Qwen2.5-Coder-
301                                                                                           direction accuracy on MultiPref (0.674) is already as high as
      7B features, scale use transfers to new developers (offsets
302                                                                                           the agreement in direction between two human raters of the
      +0.054 [+0.036, +0.074] nats per rating at k = 20 and +0.040
303                                                                                           same item (0.673 [0.666, 0.680]): a population model pre-
      [+0.031, +0.049] at k = 10), while content adaptation over 22
304                                                                                           dicts a new rater about as well as another person does. Seen
      readability attributes is inconclusive at the pre-set budgets
305                                                                                           raters. With all their training ratings (median 134), training
      (Buse–Weimer, k = 20: +0.40 [−0.25, +1.06]; Dorn, k =
306                                                                                           raters’ own parameters beat another rater’s by −0.11 [−0.57,
      10: −0.19 [−0.81, +0.42] concordance points; Appendices
307                                                                                           +0.36] direction points for the low-rank latent (offsets +0.10,
      A–B).
308                                                                                           −0.23): the ranking null is not specific to few-shot adap-
309                                                                                           tation (exploratory, Appendix B). Against its own k = 0
310   6. What personalisation buys: graded-rating                                             version, no method’s direction accuracy on MultiPref rises
311      prediction, user signal, and small choice                                            by more than 0.2 points at k = 20, and every upper 95 %
312      gains                                                                                bound stays below +0.8 points even when prompt groups are
313                                                                                           resampled together with raters (VPL +0.07 [−0.57, +0.74],
314   Binarisation removes the symmetric scale-use term; eval-                                style model −0.10 [−0.69, +0.54], PAL-B −0.48 [−1.11,
315   uated adaptation gains on MultiPref are small. On Multi-                                +0.14]). The ranking null replicates on real users’ own
316   Pref with ties dropped and labels binarised, every evaluated                            choices. PRISM users each saw 2–4 responses to their own
317   method’s personalisation gain is at most 0.002 nats per rat-                            prompt, scored them and chose one; pairing the chosen re-
318   ing (§5.4), and the scale-use baseline’s binary accuracy is                             sponse with every other one gives 41,199 native pairwise
319   essentially unchanged from the text-only model’s. On these                              choices of 1,396 users. Under the same new-user protocol
320   graded panels the largest demonstrated gains concern graded                             (5 paired user and conversation folds, k of the user’s pairs
321   levels and ties — which binary preference data, the format                              from training conversations), we fixed before any result that
322   in which most personalised reward models are trained and                                the ranking null would be stated only if every method’s
323   evaluated, discard (Community Alignment shows that bi-                                  improvement in choice accuracy over its own k = 0 version
324   nary choices can also carry predictable user differences, §6).                          had an upper 95 % bound below one point at k = 20. It
325   Ranking moves little. Symmetric offsets mainly change                                   holds for all of them (1,033 new users at k = 0; the 669 with
326   how strongly a rater is predicted to prefer a response: on                              at least 20 adaptation pairs at k = 20): VPL +0.12 points
327   graded MultiPref the scale-use baseline raises direction ac-                            [−0.08, +0.33], PAL-B +0.0 [−0.4, +0.4] (K = 2) and +0.3
328   curacy by only +0.005 [+0.001, +0.008] at k = 20 (about                                 [−0.1, +0.7] (K = 4), the 5-offset model −0.6 [−1.4, +0.2];
329
                                                                                          6
                                       What Do Gains in Personalised Reward Modelling Measure?

330   the symmetric scale-use model is identical to the text-only           (63.8 %), and the joint model’s paired gain over position-
331   model on binary choices, because a binary label carries no            only is +0.026 [−0.0002, +0.046], so additional assignment
332   intensity. LoRe (Bose et al., 2025), which reports +10 points         value from attributes beyond position is unresolved. With
333   for unseen PRISM users, run here with its own few-shot fit            correlated predictors under one prior this does not separate
334   and with a validated adaptation ridge under the same pre-set          content from position: we claim user-specific choice pre-
335   rule, also meets the ranking-null criterion: own gain at k =          dictability on identical alternatives, not a content preference,
336   20 −1.5 [−2.5, −0.4] (regularised −0.5 [−1.2, +0.2]), own             and not a psychological position habit.
337   − other +0.2 [−0.8, +1.2]. In LoRe’s own setting (its em-
                                                                            Benefit over the population model. On all test events of the
338   beddings, split and pair construction) we obtain 67.4 % for
                                                                            shared items in the test folds — a broader panel than the
339   the monolithic model and 63.6 % for LoRe (published 61.0
                                                                            1,116 items that contribute disagreeing pairs to the assign-
340   % and 71.0 %; Appendix B): the published gain is not repro-
                                                                            ment test (2,383 items, 1,436 users; population accuracy
341   duced. With a graded label cut from the users’ own score
                                                                            72.4 %) — isotropic adaptation gains +0.70 [+0.24, +1.14]
342   differences (thresholds fixed in advance), the MultiPref pat-
                                                                            pairwise accuracy points and +0.018 [+0.014, +0.023]
343   tern returns at half the size (scale-use model +0.043 [+0.031,
                                                                            nats — the pre-set user-bootstrap rule for benefit is met,
344   +0.057] nats per rating at k = 20, VPL +0.015, PAL-B 0.000;
                                                                            but the user × item interval for accuracy covers 0 ([−0.07,
345   no direction gain above +0.2 points). Community Align-
                                                                            +1.43]) while log-likelihood improves under both, so an
346   ment: who chooses what on identical items, and what
                                                                            accuracy benefit that generalises across items is unresolved;
347   adaptation buys. Community Alignment (CA; first turns;
                                                                            nor is the gain shown to be below one point. Evaluated
348   2,957 new users in five countries and languages; each choice
                                                                            frozen on the same users’ unanalysed second turns (proce-
349   event’s chosen response paired with each of the other three).
                                                                            dure refitted there; Stage 12), the transfer-calibrated covari-
350   Accuracy below is pairwise winner-versus-other accuracy,
                                                                            ance variant (TRV) gains +0.38 [+0.13, +0.64] points and
351   not four-way winner selection. Status: the adaptation proce-
                                                                            +0.0046 nats and isotropic +0.31 [+0.05, +0.58]; the prompt
352   dure was developed exploratorily on first turns (Appendix
                                                                            × user interval covers 0. On MultiPref the frozen isotropic
353   F); the Stage-12 and Stage-13 outcome rules were frozen
                                                                            procedure did not establish improvement (−0.28 [−0.64,
354   before their outcomes; the Stage-13 first-turn analyses reuse
                                                                            +0.08] points, 202 held-out annotators). On CA the esti-
355   previously examined data, while the second- and third-turn
                                                                            mated covariance shows no advantage over isotropic shrink-
356   outcomes were evaluated for the first time.
                                                                            age (turn 1 −0.17 [−0.29, −0.05], turn 2 +0.07 [−0.07,
357
      Identity on identical items (Stage 13, frozen). CA contains           +0.22] points); on MultiPref it beats isotropic under the rater
358
      2,928 exact prompt–four-response items shown to at least              bootstrap (+0.23 [+0.04, +0.42]) without establishing im-
359
      two users, covering 49,616 first-turn conversations (me-              provement over the population model (two-way includes
360
      dian 15 users per item, one language per item, fixed re-              0; Appendix F). Validated scales imply strong shrinkage,
361
      sponse order). For two users of the same item who chose               and realised gains are far below model-implied ones (the c
362
      different responses a and b, the population utilities can-            = 1 covariance-prior learner: +1.9 points implied under a
363
      cel and the adapted models predict the assignment from                Gaussian event-level simulation, +0.13 realised; Appendix
364
      S = (δu − δv )⊤ (xa − xb ), with model-implied probabil-              F).
365
      ity σ(S). With validated isotropic adaptation over length,
366                                                                         Transport to later conversations (Stage 13, frozen). We
      paragraphs and list/heading lines (k = 20 support events
367                                                                         froze each user’s first-turn deviation and added it, with-
      on other prompts; the Stage-12 procedure unchanged), the
368                                                                         out rescaling, to a third-turn population model that sees
      conditional assignment log score gains +0.066 [+0.034,
369                                                                         the conversation history (the earlier prompts and the user’s
      +0.091] nats over chance and assignment accuracy is 62.2
370                                                                         preferred responses). We scored it on the third turns of con-
      % [58.6, 65.6] (4,608 disagreeing pairs from 1,336 users on
371                                                                         versations not used for support. Of 1,901 users with a frozen
      1,116 items; item × user bootstrap). It is unchanged with
372                                                                         first-turn deviation, 1,808 have at least five third-turn events
      uncentred features; positive-multiplier and prompt-clustered
373                                                                         with a complete history and 953 have at least five outside
      intervals are [+0.046, +0.083] and [+0.036, +0.093]; every
374                                                                         their support conversations. The result is accuracy-positive
      fold is positive. The estimand is narrow: given two dis-
375                                                                         under user clustering and likelihood-inconclusive: accuracy
      agreeing users, their support choices and the two responses
376                                                                         rises by +0.43 [+0.13, +0.74] points (user × prompt inter-
      they picked, assign the responses; it conditions on the fitted
377                                                                         val [−0.08, +0.92]), log-likelihood by +0.0015 [−0.0006,
      deviations and population model.
378                                                                         +0.0035] nats. The pre-set rule requires both lower bounds
379   Position. The four fixed positions differ systematically              above 0, so additional predictive value of unrescaled first-
380   in these attributes (label-blind check), so we refitted with          turn coefficients beyond a history-conditioned population
381   position indicators added (after the result). The attribute-          model is not supported for this procedure and panel.
382   derived part of the jointly fitted scores keeps +0.060 [+0.032,       This neither shows that transport has no effect nor that pref-
383   +0.084] nats, a position-only predictor is also informative           erences are unstable, and it does not test other ways of
384
                                                                        7
                                                      What Do Gains in Personalised Reward Modelling Measure?

385
      Table 5. Choice-level results. k = 20 support choice events per user (20 binary comparisons on MultiPref); log-likelihood per pair. First
386
      interval: user (rater) bootstrap, or item × user for assignment; second: prompt- or item-group × user two-way bootstrap. Nominal 95 %,
387   conditional on the fitted population models. “Reused” = data examined in earlier stages; “new” = outcomes evaluated for the first time.
388   Question (comparator)                   Panel                                Accuracy (%, or gain in points)        Log-likelihood, nats                             Status
389
      Assignment (chance)                     CA t1 identical items; 1,336 users   62.2 % [58.6, 65.6]                    +0.066 [+0.034, +0.091]                          frozen, reused
390   . . . beyond position (position-only)   same                                 —                                      +0.026 [−0.0002, +0.046]                         exploratory
391   Benefit (population)                    CA t1 shared items; 1,436 users      +0.70 [+0.24, +1.14]; [−0.07, +1.43]   +0.018 [+0.014, +0.023]; [+0.010, +0.026]        frozen, reused
      Benefit, isotropic (population)         CA t2; 1,702 users                   +0.31 [+0.05, +0.58]; [−0.13, +0.79]   +0.0038 [+0.0021, +0.0057]; [+0.0006, +0.0066]   frozen, new
392   Benefit, TRV (population)               CA t2; 1,702 users                   +0.38 [+0.13, +0.64]; [−0.04, +0.83]   +0.0046 [+0.0031, +0.0063]; [+0.0018, +0.0074]   frozen, new
393   Benefit, isotropic (population)         MultiPref; 202 annotators            −0.28 [−0.64, +0.08]; [−0.92, +0.39]   −0.0004 [−0.0019, +0.0010]; [−0.0028, +0.0019]   frozen, reused
      Transport (history-conditioned pop.)    CA t3; 953 users                     +0.43 [+0.13, +0.74]; [−0.08, +0.92]   +0.0015 [−0.0006, +0.0035]; [−0.0020, +0.0048]   frozen, new
394   Baseline procedure W − O (paired)       CA t1; 1,799 users                   +0.62 [+0.41, +0.81]                   —                                                exploratory
395
396
397   carrying information across turns.                                                                 those offsets retained. (v) Evaluate on unseen raters
398                                                                                                      and held-out prompts, with permutation and posi-
      The measured gain depends on the population baseline. On
399                                                                                                      tive controls. (vi) Keep graded labels and ties when
      1,799 common users, one-dimensional length adaptation
400                                                                                                      individual differences matter.
      gains +0.88 / +1.08 points (random / prompt-separated test
401
      events) against a population model fitted on low-volume
402                                                                                               8. Discussion
      annotators, as in the WIMHF protocol (Movva et al., 2025),
403
      and +0.26 / +0.47 against one fitted on all other-fold users:                               What do personalisation gains measure? Three things
404
      the population-procedure effect is +0.62 [+0.41, +0.81] and                                 often reported as one come apart. Graded-rating gains for
405
      +0.61 [+0.30, +0.93] (paired), while the prompt-split con-                                  new raters are largely scale use: offsets capture them, probes
406
      trast is inconclusive (+0.20 [−0.20, +0.59]). The two pro-                                  find near-zero R2 for them in the evaluated user represen-
407
      cedures differ in volume, composition and prior estimation,                                 tations, and adding offsets to VPL recovers most of the
408
      so no mechanism is isolated. (Our line-count proxy is not                                   point-estimate gain (+0.088; non-inferiority not established).
409
      WIMHF’s discovered feature; with it, list/heading adapta-                                   User-specific choice predictability is real on identical CA
410
      tion does not beat the population coefficient — a related                                   items (62 %), though not separated from position. Choice
411
      protocol study, not a failed reproduction.)                                                 gains over a competent population model are small and
412
413   Earlier evidence. Before this test, own adapted parameters                                  fragile (Table 5).
414   beat another user’s for four of six methods (LoRe +3.27                                     Why did published models learn little about new raters
415   [+2.85, +3.70]; within-country +3.22) and length deviations                                 here? Published evaluations differ in users (synthetic or
416   reproduced across disjoint prompt sets; own − other does                                    seen), label formats, representations and population base-
417   not measure benefit and task mix could create it (Appendix                                  lines; the last alone changes the measured gain by about
418   F). The identical-item test supersedes these as evidence of                                 0.6 points on CA. Unresolved reproduction discrepancies
419   user-specific choice predictability.                                                        prevent attributing the rest to evaluation design; method
420                                                                                               conclusions concern the evaluated implementations.
421
      7. Recommendations
422
423     (i) Separate three outcomes. Report graded-rating likeli-                                 9. Limitations and analysis log
424         hood (calibration and resolution), a test of user-specific
                                                                                                  The main tables use frozen-feature text heads (a LoRA re-
425         choice predictability, and choice or ranking gains over
                                                                                                  ward model only in §5.3), and compressed features weaken
426         the population model as different results; a gain on
                                                                                                  PAL-B as a detector (§5.6). VPL, PAL and LoRe are our
427         one does not imply the others. (ii) Test user differ-
                                                                                                  reimplementations as heads on frozen embeddings; pub-
428         ences on identical items where the data allow it (an
                                                                                                  lished numbers were not reproduced (LoRe’s PRISM gain
429         assignment test between disagreeing users, as in §6):
                                                                                                  not even with its own embeddings). The positive control
430         own-versus-other contrasts on different prompts con-
                                                                                                  covers MultiPref only. Aspect analyses use MultiPref’s con-
431         found user differences with task mix and do not mea-
                                                                                                  current labels (SAP: Appendix G). The first three datasets
432         sure benefit. (iii) Report a competent population
                                                                                                  are English, and on CA’s five languages the phrase-based
433         baseline and its training procedure. The measured
                                                                                                  attributes cover English only; and the per-rater calibration is
434         personalisation gain changed by about 0.6 points with
                                                                                                  not shown to change a downstream decision. The CA anal-
435         the population-training procedure (§6). (iv) Report
                                                                                                  yses reuse data examined in earlier stages (Appendix A);
436         a scale-use baseline (a few text-independent offsets
                                                                                                  the identical-item test conditions on fitted models; features
437         per rater) next to any personalised reward model on
                                                                                                  omit conversation history except in the third-turn test; and
438         graded labels, and evaluate content adaptation with
                                                                                                  the identity signal is not separated from response position.
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
      over a population model were small and dataset-dependent.             Dawid, A. P. and Skene, A. M. Maximum likelihood esti-
450                                                                           mation of observer error-rates using the EM algorithm.
451   Predicting individuals’ choices also raises privacy and ma-
      nipulation concerns that a deployment would need to ad-                 Journal of the Royal Statistical Society: Series C (Applied
452                                                                           Statistics), 28(1):20–28, 1979.
453   dress; we report no individual-level results. The datasets are
454   public, were collected with consent by their creators, and            Deng, N., Zhang, X. F., Liu, S., Wu, W., Wang, L., and
455   are used under their licences; rater identifiers are used only          Mihalcea, R. You are what you annotate: Towards better
456   as anonymous indices.                                                   models through annotator representations. In Findings of
457                                                                           the Association for Computational Linguistics: EMNLP
458   References                                                              2023, pp. 12475–12498, 2023.
459
      Aroyo, L., Taylor, A. S., Dı́az, M., Homan, C. M., Parrish,           Dong, Y. R., Hu, T., Liu, Y., Üstün, A., and Collier, N. When
460
        A., Serapio-Garcı́a, G., Prabhakaran, V., and Wang, D.                personalization meets reality: A multi-faceted analysis
461
        DICES dataset: Diversity in conversational AI evaluation              of personalized preference learning, 2025. URL https:
462
        for safety. In Advances in Neural Information Processing             //arxiv.org/abs/2502.19158.
463
        Systems 36 (NeurIPS 2023), Datasets and Benchmarks
464                                                                         Dorn, J. A general software readability model. Master’s
        Track, 2023. doi: 10.52202/075280-2321.
465                                                                           thesis, University of Virginia, 2012.
466   Baumgartner, H. and Steenkamp, J.-B. E. M. Response
467                                                                         Eckes, T. Introduction to Many-Facet Rasch Measurement:
        styles in marketing research: A cross-national investi-
468                                                                           Analyzing and Evaluating Rater-Mediated Assessments,
        gation. Journal of Marketing Research, 38(2):143–156,
469                                                                           volume 22 of Language Testing and Evaluation. Peter
        2001. doi: 10.1509/jmkr.38.2.143.18840.
470                                                                           Lang, Frankfurt am Main, 2011. ISBN 978-3-631-61350-
471   Bose, A., Xiong, Z., Chi, Y., Du, S. S., Xiao, L., and Fazel,           4.
472     M. LoRe: Personalizing LLMs via low-rank reward                     Feng, S., Sorensen, T., Liu, Y., Fisher, J., Park, C. Y., Choi,
473     modeling, 2025. URL https://arxiv.org/abs/                            Y., and Tsvetkov, Y. Modular pluralism: Pluralistic align-
474     2504.14439.                                                           ment via multi-LLM collaboration. In Proceedings of
475
      Buse, R. P. L. and Weimer, W. R. Learning a metric for code             the 2024 Conference on Empirical Methods in Natural
476
        readability. IEEE Transactions on Software Engineering,               Language Processing, pp. 4151–4171, Miami, Florida,
477
        36(4):546–558, 2010.                                                  USA, 2024. Association for Computational Linguistics.
478
                                                                              doi: 10.18653/v1/2024.emnlp-main.240.
479
480   Castricato, L., Lile, N., Rafailov, R., Fränken, J.-P.,
                                                                            Fleisig, E., Abebe, R., and Klein, D. When the majority is
481     and Finn, C. PERSONA: A reproducible testbed
                                                                              wrong: Modeling annotator disagreement for subjective
482     for pluralistic alignment.   In Proceedings of the
                                                                              tasks. In Proceedings of the 2023 Conference on Empiri-
483     31st International Conference on Computational Lin-
                                                                              cal Methods in Natural Language Processing, pp. 6715–
484     guistics (COLING), pp. 11348–11368, Abu Dhabi,
                                                                              6726, Singapore, 2023. Association for Computational
485     UAE, 2025. Association for Computational Linguis-
                                                                              Linguistics. doi: 10.18653/v1/2023.emnlp-main.415.
486     tics. URL https://aclanthology.org/2025.
487     coling-main.752/.                                                   Goldberg, K., Roeder, T., Gupta, D., and Perkins, C. Eigen-
488                                                                           taste: A constant time collaborative filtering algorithm.
      Chakraborty, S., Qiu, J., Yuan, H., Koppel, A., Manocha,                Information Retrieval, 4(2):133–151, 2001.
489     D., Huang, F., Bedi, A. S., and Wang, M. MaxMin-
490     RLHF: Alignment with diverse human preferences. In                  Gordon, M. L., Zhou, K., Patel, K., Hashimoto, T., and Bern-
491     Proceedings of the 41st International Conference on Ma-               stein, M. S. The disagreement deconvolution: Bringing
492     chine Learning (ICML), volume 235 of Proceedings of                   machine learning performance metrics in line with reality.
493     Machine Learning Research, pp. 6116–6135, 2024.                       In Proceedings of the 2021 CHI Conference on Human
494
                                                                        9
                                      What Do Gains in Personalised Reward Modelling Measure?

495     Factors in Computing Systems (CHI ’21), pp. 1–14. ACM,            Kumar, D., Kelley, P. G., Consolvo, S., Mason, J., Bursztein,
496     2021. doi: 10.1145/3411764.3445423.                                 E., Durumeric, Z., Thomas, K., and Bailey, M. De-
497                                                                         signing toxic content classification for a diversity of
498   Gordon, M. L., Lam, M. S., Park, J. S., Patel, K., Hancock,           perspectives. In Seventeenth Symposium on Usable
499     J. T., Hashimoto, T., and Bernstein, M. S. Jury learn-              Privacy and Security (SOUPS 2021), pp. 299–318.
500     ing: Integrating dissenting voices into machine learning            USENIX Association, 2021. ISBN 978-1-939133-25-0.
501     models. In Proceedings of the 2022 CHI Conference on                URL https://www.usenix.org/conference/
502    Human Factors in Computing Systems (CHI ’22). ACM,                   soups2021/presentation/kumar.
503     2022. doi: 10.1145/3491102.3502004.
504                                                                       Li, X., Zhou, R., Lipton, Z. C., and Leqi, L. Personalized
      Homan, C. M., Serapio-Garcia, G., Aroyo, L., Diaz, M.,                language modeling from personalized human feedback,
505
        Parrish, A., Prabhakaran, V., Taylor, A., and Wang, D.              2024.
506
        Intersectionality in AI safety: Using multilevel models
507
        to understand diverse perceptions of safety in conversa-          Linacre, J. M. Many-Facet Rasch Measurement. MESA
508
        tional AI. In Proceedings of the 3rd Workshop on Per-               Press, Chicago, 1989.
509
        spectivist Approaches to NLP (NLPerspectives) @ LREC-
510                                                                       Luo, F., Yang, R., Sun, H., Deng, C., Yao, J., Shen, J.,
       COLING 2024, pp. 131–141, Torino, Italia, 2024. ELRA
511                                                                         Zhang, H., and Chen, H. Rethinking diverse human pref-
        and ICCL. URL https://aclanthology.org/
512                                                                         erence learning through principal component analysis.
        2024.nlperspectives-1.15/.
513                                                                         In Findings of the Association for Computational Lin-
514   Hovy, D., Berg-Kirkpatrick, T., Vaswani, A., and Hovy, E.             guistics: ACL 2025, pp. 19857–19870, Vienna, Austria,
515     Learning whom to trust with MACE. In Proceedings of                 2025. Association for Computational Linguistics. doi:
516    NAACL-HLT, pp. 1120–1130, 2013.                                      10.18653/v1/2025.findings-acl.1019.
517
518   Jang, J., Kim, S., Lin, B. Y., Wang, Y., Hessel, J., Zettle-        Miranda, L. J. V., Wang, Y., Elazar, Y., Kumar, S., Pyatkin,
519     moyer, L., Hajishirzi, H., Choi, Y., and Ammanabrolu, P.           V., Brahman, F., Smith, N. A., Hajishirzi, H., and Dasigi,
520     Personalized soups: Personalized large language model              P. Hybrid preferences: Learning to route instances for hu-
521     alignment via post-hoc parameter merging, 2023.                    man vs. AI feedback. In Proceedings of the 63rd Annual
522                                                                        Meeting of the Association for Computational Linguis-
      Kim, G. and Kim, E. Swap-guided preference learning for
523                                                                        tics (Volume 1: Long Papers), pp. 7162–7200, Vienna,
        personalized reinforcement learning from human feed-
524                                                                        Austria, 2025. Association for Computational Linguistics.
        back. In International Conference on Learning Represen-
525                                                                        doi: 10.18653/v1/2025.acl-long.355.
        tations (ICLR), 2026. URL https://arxiv.org/
526
        abs/2603.12595.
527                                                                       Mishra, P., Rastogi, C., Pfohl, S. R., Parrish, A., Teh, T. H.,
528   Kirk, H. R., Whitefield, A., Röttger, P., Bean, A. M., Mar-         Patel, R., Diaz, M., Wang, D., Paganini, M., Prabhakaran,
529     gatina, K., Ciro, J., Mosquera, R., Bartolo, M., Williams,         V., Aroyo, L., and Rieser, V. Decoding safety feedback
530     A., He, H., Vidgen, B., and Hale, S. A. The PRISM                  from diverse raters: A data-driven lens on responsive-
531     alignment dataset: What participatory, representative and          ness to severity. Transactions on Machine Learning
532     individualised human feedback reveals about the subjec-            Research, 2026. URL https://arxiv.org/abs/
533     tive and multicultural alignment of large language models.         2503.05609.
534     In Advances in Neural Information Processing Systems 37
535                                                                       Mostafazadeh Davani, A., Dı́az, M., and Prabhakaran, V.
        (NeurIPS 2024), Datasets and Benchmarks Track, 2024.
536                                                                        Dealing with disagreements: Looking beyond the major-
        doi: 10.52202/079017-3342.
537                                                                        ity vote in subjective annotations. Transactions of the
538   Kobalczyk, K., Fanconi, C., Sun, H., and van der Schaar,             Association for Computational Linguistics, 10:92–110,
539     M. Few-shot steerable alignment: Adapting rewards and              2022. doi: 10.1162/tacl a 00449.
540     LLM policies with neural processes, 2024.
541                                                                       Movva, R., Milli, S., Min, S., and Pierson, E. What’s in my
542   Koren, Y. and Sill, J. OrdRec: An ordinal model for predict-         human feedback? learning interpretable descriptions of
543     ing personalized item rating distributions. In Proceedings         preference data, 2025.
544     of the Fifth ACM Conference on Recommender Systems
        (RecSys), pp. 117–124, 2011.                                      Orlikowski, M., Röttger, P., Cimiano, P., and Hovy, D. The
545                                                                         ecological fallacy in annotation: Modelling human label
546   Koren, Y., Bell, R., and Volinsky, C. Matrix factorization            variation goes beyond sociodemographics. In Proceed-
547     techniques for recommender systems. Computer, 42(8):                ings of the 61st Annual Meeting of the Association for
548     30–37, 2009.                                                        Computational Linguistics (Volume 2: Short Papers), pp.
549
                                                                     10
                                       What Do Gains in Personalised Reward Modelling Measure?

550     1017–1029, Toronto, Canada, 2023. Association for Com-                 China, 2025. Association for Computational Linguistics.
551     putational Linguistics. doi: 10.18653/v1/2023.acl-short.               doi: 10.18653/v1/2025.emnlp-main.106.
552     88.
553                                                                          Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A.,
554   Park, C., Liu, M., Kong, D., Zhang, K., and Ozdaglar, A.                 Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhos-
555     RLHF from heterogeneous feedback via personalization                   ale, S., Bikel, D., Blecher, L., Canton Ferrer, C., Chen,
556     and preference aggregation, 2024.                                      M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W.,
557                                                                            Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn,
      Plank, B. The “problem” of human label variation: On                     A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez,
558     ground truth in data, modeling and evaluation. In Pro-
559                                                                            V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P. S.,
        ceedings of EMNLP, pp. 10671–10682, 2022.                              Lachaux, M.-A., Lavril, T., Lee, J., Liskovich, D., Lu, Y.,
560
561   Poddar, S., Wan, Y., Ivison, H., Gupta, A., and Jaques, N.               Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Moly-
562     Personalizing reinforcement learning from human feed-                  bog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R.,
563     back with variational preference learning. In Advances                 Saladi, K., Schelten, A., Silva, R., Smith, E. M., Subra-
564     in Neural Information Processing Systems 37 (NeurIPS                   manian, R., Tan, X. E., Tang, B., Taylor, R., Williams,
565     2024), 2024. doi: 10.52202/079017-1664.                                A., Kuan, J. X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan,
566                                                                            A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R.,
      Rao, P. V. and Kupper, L. L. Ties in paired-comparison ex-               Edunov, S., and Scialom, T. Llama 2: Open foundation
567
        periments: A generalization of the Bradley-Terry model.                and fine-tuned chat models, 2023.
568
        Journal of the American Statistical Association, 62(317):
569                                                                          Uma, A. N., Fornaciari, T., Hovy, D., Paun, S., Plank, B.,
        194–204, 1967. doi: 10.1080/01621459.1967.10482901.
570                                                                           and Poesio, M. Learning from disagreement: A survey.
571   Raykar, V. C., Yu, S., Zhao, L. H., Valadez, G. H., Florin, C.,         Journal of Artificial Intelligence Research, 72:1385–1470,
572     Bogoni, L., and Moy, L. Learning from crowds. Journal                 2021.
573     of Machine Learning Research, 11:1297–1322, 2010.
574                                                                          Wang, Z., Bukharin, A., Delalleau, O., Egert, D., Shen,
575   Ryan, M. J., Shaikh, O., Bhagirath, A., Frees, D., Held, W.,            G., Zeng, J., Kuchaiev, O., and Dong, Y. HelpSteer2-
576     and Yang, D. SynthesizeMe! inducing persona-guided                    Preference: Complementing ratings with preferences. In
577     prompts for personalized reward models in LLMs. In                    The Thirteenth International Conference on Learning
578     Proceedings of the 63rd Annual Meeting of the Associ-                 Representations (ICLR), 2025. URL https://arxiv.
579     ation for Computational Linguistics (ACL), 2025. URL                  org/abs/2410.01257.
580     https://arxiv.org/abs/2506.05598.
                                                                             Zhang, L. H., Milli, S., Jusko, K., Smith, J., Amos, B.,
581
      Shenfeld, I., Faltings, F., Agrawal, P., and Pacchiano, A.               Bouaziz, W., Revel, M., Kussman, J., Sheynin, Y., Ti-
582
        Language model personalization via reward factorization,               tus, L., Radharapu, B., Yu, J., Sarma, V., Rose, K., and
583
        2025.                                                                  Nickel, M. Cultivating pluralism in algorithmic mono-
584
                                                                               culture: The community alignment dataset. In The Four-
585   Siththaranjan, A., Laidlaw, C., and Hadfield-Menell, D.                  teenth International Conference on Learning Represen-
586      Distributional preference learning: Understanding and                 tations (ICLR), 2026. URL https://arxiv.org/
587      accounting for hidden context in RLHF. In The Twelfth                 abs/2507.09650.
588     International Conference on Learning Representations
589     (ICLR), 2024. URL https://arxiv.org/abs/                             Zhang, M. J. Q., Wang, Z., Hwang, J. D., Dong, Y., De-
590      2312.08358.                                                           lalleau, O., Choi, Y., Choi, E., Ren, X., and Pyatkin, V.
591                                                                            Diverging preferences: When do annotators disagree and
592   Sorensen, T., Moore, J., Fisher, J., Gordon, M. L.,                      do models know? In Proceedings of the 42nd Interna-
593     Mireshghallah, N., Rytting, C. M., Ye, A., Jiang, L.,                  tional Conference on Machine Learning (ICML), volume
594     Lu, X., Dziri, N., Althoff, T., and Choi, Y. Position:                 267 of Proceedings of Machine Learning Research, pp.
595     A roadmap to pluralistic alignment. In Proceedings of                  76193–76212, 2025.
596     the 41st International Conference on Machine Learning
597     (ICML), volume 235 of Proceedings of Machine Learning                Zhao, S., Dang, J., and Grover, A. Group preference
598     Research, pp. 46280–46302, 2024.                                       optimization: Few-shot alignment of large language
599                                                                            models. In The Twelfth International Conference on
      Sorensen, T., Mishra, P., Patel, R., Tessler, M. H., Bakker,             Learning Representations (ICLR), 2024. URL https:
600     M. A., Evans, G., Gabriel, I., Goodman, N., and Rieser, V.
601                                                                            //arxiv.org/abs/2310.11523.
        Value profiles for encoding human variation. In Proceed-
602     ings of the 2025 Conference on Empirical Methods in                  Zollo, T. P., Siah, A. W. T., Ye, N., Li, A., and Namkoong, H.
603     Natural Language Processing, pp. 2047–2095, Suzhou,                    PersonalLLM: Tailoring LLMs to individual preferences.
604
                                                                        11
                                 What Do Gains in Personalised Reward Modelling Measure?

605   In The Thirteenth International Conference on Learning    A. Protocols and amendments
606   Representations (ICLR), 2025. URL https://arxiv.
607   org/abs/2409.20296.                                       Chronology and evidential status. - Graded-label stages
608                                                             (1–2c, MultiPref, DICES, PRISM graded, code readabil-
609                                                             ity). Rules were frozen before outcomes. The symmet-
610                                                             ric offsets DFs were added after the first results and are
611                                                             exploratory. - Published methods and positive controls
612                                                             (Stages 3, 5, 6). Rules were frozen. The dose-response anal-
613                                                             yses are exploratory. - CA turn 1. - Stage 8 rule: frozen.
614                                                             - Stages 9–11: exploratory development of the adaptation
615                                                             procedure, after inspecting test results. - Stage 13 S13-1:
616                                                             frozen tests on these previously examined data. Am. 2 and
617                                                             Am. 4 were added after the result. - CA turn 2 (Stage
618                                                             12) and CA turn 3 (S13-3). Frozen procedures, evaluated
619                                                             on outcomes not previously analysed. The users are the
620                                                             same people. - MultiPref under the CA procedure (S13-
621                                                             2). Frozen. The MultiPref data had been analysed earlier
622                                                             with other methods. - Stage 14 (Jester real-data positive
623                                                             control; contested-pair stratification; corrected latent
624                                                             models). The rules for the Jester control and the stratifica-
625                                                             tion were frozen before outcomes. Amendment 1 — the
626                                                             diagnosis of the latent models’ adaptation prior, the correc-
627                                                             tion, and the re-runs with it — is post hoc; the reading rules
628                                                             for each re-run were written before it ran. The corrected
629                                                             latent rows of §5.1, §5.2, §5.5 and §5.6 are exploratory.
630                                                             All intervals are nominal and do not account for the earlier
631                                                             adaptive development.
632
633                                                             All analyses were specified in timestamped internal
634                                                             protocols (PROTOCOL STAGE1, PROTOCOL STAGE2,
635                                                             PROTOCOL STAGE2B, PROTOCOL STAGE2C, PROTO-
636                                                             COL STAGE3); stages 2b and 2c were written after the
637                                                             stage-2a results. Changes after a result were logged as num-
638                                                             bered amendments with the reason; the main ones: the first
639                                                             decoding split (a = b = 2) was structurally empty (two rat-
640                                                             ings determine their distribution) and was replaced by a = 3,
641                                                             b = 1; hand-set penalties in the rater–item model over-fitted
642                                                             and were replaced by inner cross-validation (which reversed
643                                                             an earlier, wrong conclusion that rater shifts do not help);
644                                                             penalty grids were extended when selections fell on grid
645                                                             edges, before any hypothesis was read; the low-rank base-
646                                                             line lacked a constant column and was fixed in its favour; the
647                                                             probit group model had a scale non-identifiability and was
648                                                             fixed; VPL suffered posterior collapse and its KL weight
649                                                             was re-selected including 0; PAL-B’s adaptation ridge was
650                                                             re-selected by k-shot validation. Every superseded full run
651                                                             is kept and reported in the supplementary results; two de-
652                                                             bugging smoke runs and one fold whose output was deleted
653                                                             unread when the penalty grids were extended are not. The
654                                                             real-data aspect contrast of §5.7 was revised four times: own
655                                                             − other; with a style-only control after a first, confounded
656                                                             +0.45 [+0.01, +0.94]; against θ = 0; and against the popu-
657                                                             lation weighting, after the reference learner turned out to
658                                                             shrink towards 0 rather than towards the population. The
659
                                                           12
                                       What Do Gains in Personalised Reward Modelling Measure?

660   few-shot-tuned low-rank prior was selected at the top of its           Scale use and the shared reward model. Training the
661   grid (8192) in most folds; extending the grid to 524,288               text model jointly with rater offsets and then using the
662   left every DL result unchanged in substance (real data: own            population-mean offsets (k = 0) does not give a better
663   − other +0.31 vs +0.30 at k = 20, DFs − DL +0.003 vs                   consensus model than ordinary training: −0.003 [−0.010,
664   +0.0045; synthetic +5/+10-point panels: +0.10 / +0.09 vs               +0.003] nats on MultiPref (direction +0.3 points, n.s.),
665   −0.02 / +0.09). Stage 14 showed what this selection meant:             −0.022 [−0.037, −0.008] on DICES, +0.001 on PRISM,
666   the prior was isotropic on an unstandardised latent, so the            −0.009 [−0.016, −0.004] with the LoRA reward model.
667   largest strengths (adaptation effectively off) were the best           Ordinary training averages scale use out; it matters for pre-
668   available; with the whitened prior the selected strengths              dicting a person, not for learning the content preference.
669   are interior (0.03–2), and the affected rows are re-reported
                                                                             What the offsets encode. In the probit family, rater scale
670   (Appendix B, Stage 14). First-run values replaced in the
                                                                             matters more than rater shift on MultiPref (+0.036 [+0.020,
671   main tables: MultiPref DL − D +0.023 [−0.002, +0.047],
                                                                             +0.057] at k = 20), but rater shift dominates on DICES
672   +0.095 [+0.069, +0.122], +0.120 and DFs − DL +0.026
                                                                             (−0.053) and PRISM (−0.031): leniency/strictness on
673   [+0.016, +0.037], +0.0045 [−0.0004, +0.0092], +0.007
                                                                             single-response rating scales, intensity on two-sided prefer-
674   [+0.002, +0.013] at k = 5, 20, 50 (direction accuracy 0.679
                                                                             ence scales.
675   at k = 20); DICES DF − DL +0.037 [+0.022, +0.053].
676                                                                          What this does and does not say about pluralism. Our
677   B. Hypotheses and outcomes                                             results do not show that people agree about content: the item-
678                                                                          level disagreement that replicates across rater panels is real
679   Stage 2a (MultiPref, k = 20): H1 DF > D — holds (+0.080);              (split-half reliability 0.25 on MultiPref) and about a tenth
680   H5 (probit F1 > D, the primary probit contrast after Amend-            of it is decodable from text. They show that, for predicting
681   ment 1) — not supported (+0.020 [−0.001, +0.041]; ho-                  an individual new rater from few ratings, that content-level
682   moscedastic F − D −0.029), superseded by H1 in Amend-                  disagreement is a small part of what is predictable, and that
683   ment 2; H2 DF > group — holds; H3 DF ≥ low-rank −                      demographic or crowd/expert groups add nothing beyond
684   0.005 — holds under the training-rater prior, not robust               the text.
685   under a few-shot-tuned prior (−0.015); H4 rater scale >
                                                                             Fine-tuned and in-context reward models (§5.3, full text).
686   rater shift — holds on MultiPref only; H6 symmetric style
                                                                             With a LoRA-fine-tuned Qwen2.5-7B reward model (D-
687   model gains likelihood without losing direction accuracy —
                                                                             LoRA, trained per fold on the training raters’ rating distri-
688   holds and robust. Replications: H1r, H2r hold on DICES
                                                                             butions) as the text model, the three-number style model
689   and PRISM; H3r holds on DICES (robust; +0.037 [+0.022,
                                                                             still adds +0.100 [+0.071, +0.130] nats per rating at k
690   +0.053] as first run under the tuned prior, +0.011 [+0.005,
                                                                             = 20 — the same as its gain on the frozen-feature head
691   +0.018] with the corrected prior of Stage 14) and is for-
                                                                             (+0.100). Fine-tuning improves the text-only model by
692   mally not non-inferior on PRISM under the tuned prior
                                                                             +0.027 [+0.016, +0.039] (direction accuracy +1.4 points)
693   (−0.001 [−0.006, +0.003] as first run, bound −0.006 <
                                                                             and the style model by the same +0.027: the two gains
694   −0.005; −0.004 [−0.007, −0.001] with the corrected prior,
                                                                             add. Personalising the frozen-feature model with 20 rat-
695   i.e. the latent is ahead). Stage 2b: B1, B2, B3 hold. Stage
                                                                             ings per rater gains more than fine-tuning the text model
696   2c: C1 holds (graded), C2 holds (binary: |DFs − D| ac-
                                                                             (+0.072 [+0.041, +0.106]). DFs keeps the direction accuracy
697   curacy −0.0002; all personalisation gains ≤ 0.002 nats),
                                                                             of D-LoRA (+0.002 [−0.002, +0.006]). Against in-context
698   C3 fails (published latents do not encode style, R2 ≈ 0),
                                                                             personalisation — a separate LoRA model on the same base,
699   C4 not met as a conjunction (first part holds, +0.088 over
                                                                             trained with ten of the rater’s other ratings in the prompt
700   VPL; second part, non-inferiority to DFs, not established:
                                                                             and evaluated with the new rater’s k ratings in the prompt
701   −0.004, lower bound −0.014); Stage 3 (positive control):
                                                                             — the three offsets on D-LoRA are better at k = 20. The
702   τ 0 control passes; power at the pre-specified strengths (+1.7,
                                                                             in-context model’s result varies with its training seed (two
703   +5.2 oracle points) not established — no content-interacting
                                                                             of fifteen runs failed, gaining −0.078 and −0.055 over D-
704   method’s own − other gain has a lower bound above +1
                                                                             LoRA against +0.021 to +0.125 for the others; the two failed
705   point; exploratory dose-response: VPL and PAL-B pass at
                                                                             runs have the highest training loss), so it was trained with
706   +21 points, none at +10 (as first run; corrected latent models:
                                                                             three seeds per fold, and we fixed in advance that “better”
707   Stage 14 below); the split-half content estimator (S3-C) has
                                                                             requires a lower bound above zero for every seed and for the
708   no power; with full features (exploratory, Amendment 5)
                                                                             seed average. Averaged over seeds — the expected result of
709   the τ 0 control passes and PAL-B passes at +10 points (k =
                                                                             one training run — the offsets are better by +0.041 [+0.027,
710   20), so the PCA bottleneck explains part of the detection
                                                                             +0.054] nats per rating (209 raters; per seed +0.062, +0.018
711   limit. R1 (PRISM native pairwise choices: every method’s
                                                                             and +0.042, every lower bound at least +0.005) and more
712   own choice-accuracy gain at k = 20 has an upper bound <
                                                                             accurate on which response the rater prefers (+1.9 points
713   +0.01) holds (largest bound +0.0071, PAL-B K = 4).
714
                                                                        13
                                        What Do Gains in Personalised Reward Modelling Measure?

715   [+0.9, +2.7]). The in-context model does learn from the                 each rater’s own weights with that population weighting
716   history (+0.051 [+0.024, +0.079] over D-LoRA on average),               (style offsets kept). Individual weights transfer worse than
717   at several thousand prompt tokens per prediction, but its               the population’s: −0.28 [−0.56, −0.06] points at k = 20
718   direction accuracy is below D-LoRA’s (−1.7 points [−2.6,                and −0.63 [−1.01, −0.25] at k = 50. With injected aspect-
719   −0.8] on average; −0.6 to −3.0 per seed).                               weight heterogeneity it gives +0.46 [−0.00, +0.96] at k =
720                                                                           50 when an oracle would gain +1.4 points and +3.4 [+2.6,
      Value conflicts (§5.7, full text). The positive control asks
721                                                                           +4.3] at +5.0. The real data lie well below the +5-point
      what the methods could detect; MultiPref also lets us ask
722                                                                           panel and, at k = 50, just below the +1.4-point panel: for
      how much there is to detect. Every MultiPref annotation
723                                                                           this injection family, the real data lie below panels of one
      carries the annotator’s own helpfulness, truthfulness and
724                                                                           to two oracle points (sensitivity evidence, not a validated
      harmlessness preferences next to the overall one, so a rater’s
725                                                                           upper bound). This test is exploratory and post hoc, and its
      way of trading these values off is observable. We fit an
726                                                                           contrast was revised four times (Appendix A; no version
      ordinal model of the overall preference from the annota-
727                                                                           shows a positive transferable aspect part), the calibration
      tor’s own aspect labels (their values and absolute values)
728                                                                           strengths were chosen after seeing the real bound, it uses
      with rater-specific cut-points (scale use) and either a pooled
729                                                                           one synthetic draw on panels noisier than the real data, and
      trade-off or a rater-specific trade-off, adapted on k of the
730                                                                           it uses other annotators’ aspect labels of the test items (an
      rater’s training-item annotations and evaluated on held-out
731                                                                           aspect oracle, not a deployable model). Four caveats: the
      items with the rater’s own aspect labels as inputs — an
732                                                                           ceiling bounds personalisation of the weighting only — dis-
      oracle for the content side. The pooled trade-off weights
733                                                                           agreement about which response is more helpful or harmless
      harmlessness most (6.1, five-fold mean), then helpfulness
734                                                                           is absorbed into the inputs; it covers content preferences
      (4.0) and truthfulness (2.0). With the rater’s own aspect
735                                                                           expressible through these three aspects only; MultiPref’s
      labels as inputs the pooled model already gets 97.5 % of
736                                                                           prompt sampling determines how often values conflict; and
      directions right (74 % on conflict items): aspect and over-
737                                                                           annotators may have aligned their aspect labels with their
      all labels are produced together by the same annotator, so
738                                                                           overall label, which would understate conflicts.
      this ceiling concerns a small residual and is a property of
739
      MultiPref’s concurrent labelling.                                       Code readability (Stage 10). Pre-set rules: SE-1 (offsets
740
                                                                              transfer) holds on both panels; SE-2 with the low-rank latent:
741   Even with the rater’s own aspect judgements and all of their
                                                                              Buse–Weimer inconclusive (own gain in concordance +1.75
742   training ratings, a rater-specific trade-off predicts which
                                                                              [+0.68, +2.78], own − other +0.53 [−0.63, +1.72]; the
743   response they prefer only 0.1 points better than the popu-
                                                                              text-only model orders snippets at chance, 51.6 % — by
744   lation’s trade-off, and even fitted in-sample only 0.4 points
                                                                              construction: the 99 whitened principal components of 100
745   better. The reason is that the aspects point in opposite direc-
                                                                              snippets are an item-identity encoding (Gram matrix n(I
746   tions in only 4.0 % of the held-out non-tie comparisons (3.5
                                                                              − 11⊤ /n); found without labels while designing Stage 14),
747   % of all annotations); there individual trade-offs matter a
                                                                              so on this panel neither the text head nor the latent can
748   great deal (in-sample +9.7 points; among the 20 raters with
                                                                              generalise to held-out snippets and the row does not test
749   at least ten helpfulness–harmlessness conflicts, the share
                                                                              text-mediated personalisation), Dorn degenerate (validation
750   of conflicts resolved in favour of helpfulness ranges from
                                                                              selects the largest penalties, the latent equals the text-only
751   0.00 to 0.94), but they are too rare to move overall accuracy.
                                                                              model). SAP-code, own − population / own − other: Buse–
752   Individual trade-offs do change how strongly raters prefer
                                                                              Weimer k = 20 +0.40 [−0.25, +1.06] / +1.57 [+0.89, +2.25],
753   (up to +0.046 nats with all their ratings), in line with the
                                                                              k = 50 +1.30 [+0.46, +2.18] / +2.98 [+2.00, +3.91]; Dorn
754   calibration-not-ranking pattern. We fixed in advance that
                                                                              k = 10 −0.19 [−0.81, +0.42] / +2.06 [+1.49, +2.62] —
755   an aspect-weight personalised reward model would be built
                                                                              the rule as worded is met on Dorn through own − other,
756   only if the lower bound of this ceiling exceeded half a point
                                                                              which Stage 5 Am. 4 showed is not on the oracle scale, so
757   with all training ratings; it does not, so we did not build one.
                                                                              content personalisation is not claimed. One within-snippet
758   The learned personalisers cannot be tested on the conflict
                                                                              permutation control gives own − population −0.38 (Buse–
759   items either: the 243 held-out non-tie ratings on them give
                                                                              Weimer) and −2.09 (Dorn).
760   own − other intervals wider than the achievable ceiling (k
761   = 20: low-rank latent +0.1 [−2.2, +2.4]). A calibrated test             Stage 14: a real-data positive control, contested
762   on the real data. The ceiling above gives each rater’s own              pairs and corrected latent models (PROTO-
763   aspect labels; a deployable personaliser would know only                COL STAGE14.md). Contested pairs (S14-2, frozen). Test
764   the item’s aspects. We therefore ran the reference learner              pairs were split by the population model’s margin (lowest
765   of §5.6 on the real labels with the item’s consensus aspect             fifth of |logit| = contested). TRV − population accuracy
766   differences from its other annotators as content features               on contested pairs / the rest: CA first turns +1.62 [+0.72,
767   (3-d), with a hierarchical prior centred at the population              +2.52] / +0.16 [−0.07, +0.41] points; second turns +1.62
768   weighting (estimated on the training raters) and compared               [+0.63, +2.53] / +0.05 [−0.13, +0.23]; MultiPref +0.02
769
                                                                         14
                                             What Do Gains in Personalised Reward Modelling Measure?

770   rater ratings used                       rater − pooled trade-off, direction accuracy (points)   log-likelihood per rating   on conflict items (points)
771   k = 20                                   +0.03 [−0.05, +0.12]                                    +0.011 [+0.003, +0.020]     +0.6 [−1.1, +2.4]
772   k = 50                                   +0.06 [−0.09, +0.21]                                    +0.023 [+0.011, +0.037]     +0.3 [−2.7, +3.8]
773   all training items                       +0.10 [−0.24, +0.43]                                    +0.046 [+0.028, +0.068]     +2.0 [−5.0, +9.2]
774   in-sample (fitted on the test items)     +0.44 [+0.27, +0.64]                                    +0.094 [+0.079, +0.112]     +9.7 [+5.6, +14.5]
775
776
777   [−1.38, +1.37] / −0.06. Neither pre-set rule is met on any                 over no adaptation is +0.2 to +0.8 points with intervals
778   panel (a lower bound above +1 point on contested pairs;                    that include zero, and held-out log-likelihood does not
779   concentration in both accuracy and log-likelihood): the                    exceed the scale-use model’s: the corrected pipeline’s
780   log-likelihood gain is not concentrated (contested − rest                  detection limit lies between +5 and +10 oracle points, and
781   −0.69 [−1.09, −0.29] and +0.00 [−0.24, +0.24] ×100                         detection is not yet a net ranking gain. Real MultiPref: own
782   nats on CA), so the accuracy pattern is the mechanical                     − other between −0.16 and +0.19 points across the two
783   one stated beforehand — a small logit shift changes the                    latents and rungs (upper bounds at most +0.50); DFs − DL
784   predicted choice only where the population margin is                       −0.0005 [−0.0052, +0.0049] nats and DF − DL −0.020
785   near zero. Jester (S14-1, frozen). 1,000 Jester users ×                    [−0.024, −0.016] under rung a (H3 not non-inferior, as
786   128 jokes (Goldberg et al., 2001), ratings binned to five                  before). DICES: DF − DL +0.011 [+0.005, +0.018] (as
787   levels, the paper’s folds and k-shot protocol; endpoint:                   first run +0.037). PRISM (941 raters): under rung a the
788   within-rater pairwise concordance, own adapted parameters                  softmax latent is ahead of the offsets in likelihood, DF −
789   minus the population prediction, k = 20. On jokes seen                     DL −0.0037 [−0.0065, −0.0008] nats at k = 20 (−0.003
790   in training a linear collaborative-filtering reference gains               at k = 5, −0.005 at k = 10, +0.009 [−0.002, +0.020] at
791   +1.39 [+1.12, +1.68] points (rule: lower bound above                       k = 50; as first run −0.001 [−0.006, +0.003]), about 5
792   +1; met), while our pipeline’s low-rank latent with an                     % of the offsets’ own gain; by the pre-written rule this
793   item-identity encoding gained +0.14 [+0.09, +0.19]. On                     contradicts “nothing beyond scale use” in likelihood on
794   held-out jokes no learner beat the text-predicted joke mean                PRISM. It is not a ranking gain: within-rater concordance
795   (latent −0.06 [−0.11, −0.01]; collaborative filtering on text              own − other is −0.06 [−0.26, +0.13] (latent minus offsets
796   features −0.10 [−0.34, +0.13]), so the new-item setting                    −0.01 [−0.10, +0.08]) and −0.21 [−0.37, −0.05] against
797   has no demonstrated headroom on this panel. Diagnosis                      no adaptation; the ordinal latent is 1.8 ×100 nats below
798   and correction (Amendment 1, post hoc). Ten times the                      its probit comparator, with concordance +0.01 [−0.04,
799   optimiser iterations left the gain unchanged, and the                      +0.07]. At k = 50 on PRISM (139 raters) the tuned strength
800   ordinal parametrisation was no better. Two defects were                    shrinks adaptation heavily in most folds for the offsets
801   found. The adaptation prior was isotropic on a latent                      and the latent alike (tuned DF − D +0.043 against +0.107
802   whose training-rater covariance is far from the identity, so               with the training-rater prior; corrected DL − D +0.035
803   tuning on pseudo-new raters chose the largest strengths                    [+0.010, +0.061]), which is the dip in Figure 2. Dorn:
804   (512–8192: adaptation off). And for the softmax latent                     the softmax latent is again switched off by validation; the
805   the rater-side penalties were chosen by the training raters’               ordinal latent gains +0.012 [+0.003, +0.020] nats over the
806   validation likelihood, which rewards scale use. With the                   offsets with a concordance gain of exactly zero, i.e. it is
807   prior whitened (z = z̄ + Lu, L the Cholesky factor of                      used as a rater shift. Our pre-written rule’s direction clause
808   the training raters’ latent covariance, isotropic prior on                 labels the ordinal latent on DICES and Dorn and both
809   u; rung a) the ordinal latent gains +1.68 [+1.47, +1.90]                   latents on PRISM as contradicting the scale-use reading.
810   on Jester (121 % of the reference) and the softmax latent                  On single-response panels, however, direction means above
811   +0.40; choosing the rater-side penalties and the strength by               or below the scale midpoint, which a rater shift alone moves
812   pseudo-new-rater concordance as well (rung b) brings the                   (the scale-use models gain +8.5 to +11.6 points on the same
813   softmax latent to +1.16 [+0.98, +1.34] (83 %; the +1 rule                  contrast on DICES and Dorn, +1.3 to +1.6 on PRISM),
814   narrowly unmet) and the ordinal latent to +1.67. Folds 1–4,                so we read the latent-minus-comparator and concordance
815   not used in the diagnosis, agree. Held-out items with the                  contrasts instead (post hoc). The one positive cell is the
816   corrected models (reading rules written before the runs).                  ordinal latent on DICES: concordance own − other +0.50
817   Semi-synthetic panels, own − other direction at k = 20,                    [+0.09, +0.96] (over no adaptation +0.30 [−0.04, +0.65]);
818   softmax / ordinal latent under rung a: null +0.01 / +0.04;                 with about twenty cells examined and no correction, it
819   +5.2-point panel −0.06 / +0.10 [−0.22, +0.41]; +10.1-point                 is a lead, not a finding. Under rung b the latent is below
820   panel +0.62 [+0.17, +1.06] / +2.82 [+2.02, +3.63]; rung                    its scale-use comparator in held-out log-likelihood by
821   b: +2.28 [+1.48, +3.12] / +3.35 [+2.51, +4.21] at +10.1                    0.03–1.64 nats per rating in seven of eight panel × latent
822   and at most +0.43 [−0.03, +0.88] at +5.2. The scale-use                    cells, without a concordance gain over no adaptation; the
823   models stay at zero on the same contrast. At +10.1 the gain                correction we adopt is rung a.
824
                                                                            15
                                       What Do Gains in Personalised Reward Modelling Measure?

825   Untuned rank-2 comparator (Stage 9 Am. 4). With only                   ranking null of §6 says nothing about those. These are
826   its map ridge chosen on training raters’ held-out ratings              comparisons with synthetic panels of one injected form, not
827   and z ∼ N (0, I) for new raters, the rank-2 attribute model            formal exclusion bounds. On the full features (exploratory)
828   gave −2.67 [−3.30, −2.07] (null), +2.20 / +7.36 (semantic),            VPL’s latent collapses (own − other exactly 0), while PAL-
829   −0.42 (out-of-dictionary) and −2.13 [−2.73, −1.52] (real);             B passes the threshold at +10 points but not at +5, and the
830   tuning its adaptation strength on pseudo-new raters (Am. 8)            real data stay at the null level (+0.11 [−0.16, +0.37]): the
831   removes the losses.                                                    real data lie below the +10-point panels of the injected form
832                                                                          at k = 20 but not below the +5-point panels (Appendix B).
      SAP with the pre-registered EM update (Stage 9, before
833                                                                          How far are these methods from what the data allow?
      Amendment 7). own − µ at k = 20: null draws −0.28
834                                                                          A well-specified reference learner — the injection’s two
      . . . +0.05 (k = 50: down to −0.50 [−0.92, −0.09]); seman-
835                                                                          features known, a per-rater weight vector with an empirical-
      tic panels +2.26 . . . +2.79 and +7.30 . . . +8.04; out-of-
836                                                                          Bayes prior, style offsets re-fitted, the same permutation
      dictionary +0.41 and +0.81; real MultiPref +0.17 [−0.19,
837                                                                          contrast — recovers the injected preference from 20 ratings
      +0.55], LL +0.0022 [+0.0003, +0.0041] nats; PRISM native
838                                                                          at every strength. On the oracle’s scale (the rater’s own
      choices −0.25 [−1.30, +0.83] (EM variances stayed near
839                                                                          weights against the population state, θ = 0 here, with the
      their initial value there; with the fixed-point update +0.08
840                                                                          rater’s style offsets kept) it gains +0.89 [+0.40, +1.37] points
      [−0.86, +1.02]).
841                                                                          at +1.7 oracle points, +3.1 [+2.3, +4.0] at +5.2 and +8.0
842   Positive control on full features (Stage 3, Amendment 5).              at +10.1, i.e. 52–79 % of the oracle; own − other roughly
843   Because the compressed features might be what limits the               doubles these numbers, because another rater’s weights are
844   content-interacting methods, we re-ran VPL and PAL-B on                anti-informative, and is therefore not used for this learner.
845   the full features (exploratory). The text-only fits improve (k         Among the tested strengths, the reference learner crosses
846   = 0 log-likelihood: PAL-B −1.533 vs −1.558, VPL −1.495                 the detection criterion between +1.7 and +5.2 points, well
847   vs −1.574), but VPL’s latent then collapses and is unused at           below the methods’. Is the gap in the methods’ inputs or
848   every strength (own − other exactly 0), so this check rests            in the learners? Linear probes (exploratory, Appendix B)
849   on PAL-B. Its detection limit drops: it passes the threshold           show the injected direction is available to VPL and PAL-B
850   at +10 points; at +5 points its k = 50 gain is positive (+1.05         (out-of-fold R2 0.65 compressed, 1.00 full) but not to the
851   [+0.37, +1.72]; real data +0.19 [−0.12, +0.48]) but meets              low-rank latent’s joint embedding (0.02); re-injected inside
852   the +1-point criterion in only one of four synthetic draws.            that embedding, the latent detects +10 points (+1.97 [+1.31,
853   The real data stay at the null level (+0.11 [−0.16, +0.37] at          +2.65]; originally +0.09; 3 of 4 draws) but not +5 (+0.08;
854   k = 20). With this stronger detector, the real data lie below          0 of 4). With the dimension available, the best learners
855   the +10-point panels of the injected form at k = 20; at k = 50         thus detect between +5 and +10 oracle points, the reference
856   they lie below the +5-point panel but the intervals overlap            learner below +5: in these tested settings twenty ratings
857   (comparisons with synthetic panels, not formal exclusion               sufficed once the dimension was supplied, and the evaluated
858   bounds); with the compressed features of the main tables               learners did not find it. With semantic axes (formatting,
859   PAL-B is a weaker detector than with full features (full-              hedging/refusal) no method detects even +9.7 points; the
860   feature VPL collapses).                                                reference learner recovers +7.4 (Appendix B). Results are
861                                                                          stable over four synthetic draws, and the synthetic panels
      Positive control (§5.6, full text). No evaluated method met
862                                                                          are noisier than the real data, so the calibrations transfer
      the pre-specified detection criterion. In the exploratory dose-
863                                                                          only approximately (Appendix B).
      response, VPL and PAL-B with PCA-256 features detect
864
      content preferences worth +21 points but recover less than             Positive control: seed variability and realism (Stage
865
      half a point of +10; the low-rank latent, whose user term              5). Over four synthetic draws (θ and labels) the reference
866
      interacts with a joint embedding of the comparison, has a              learner is stable (+2.4 to +3.1 at +5 points, +6.4 to +8.0 at
867
      signal at +21 points that stays below the threshold, and with          +10), PAL-B on full features detects the +10-point panels
868
      the untuned prior it shows nothing up to +5 points either. On          in all four (lower bounds +1.16 to +3.23) and the +5-point
869
      the real data VPL and PAL-B are at the null-control level,             panels in none (+0.26 to +1.40), and the low-rank latent
870
      and the low-rank latent’s marginal +0.30 [−0.00, +0.60]                detects neither in any draw (−0.31 to +0.15). A limitation
871
      is matched by the text-independent offsets (+0.32 [+0.06,              of all synthetic panels: they are noisier than the real data
872
      +0.58] on the same contrast), so its aggregate gain is matched         (rater-pair direction agreement 0.59 at τ = 0 against 0.673
873
      by scale use (which can tip a few near-tie predictions) and            [0.666, 0.680]; Krippendorff’s α 0.11 against 0.28), and
874
      does not demonstrate content adaptation. Read together: on             adding item fixed effects to the generator did not close the
875
      MultiPref, the real data lie far below the +20-point panels            gap (0.60), nor does it reproduce the small effect of style
876
      for these methods, while preferences worth up to about                 offsets on direction (+0.32 real vs −0.07 at τ = 0); the cali-
877
      10 points cannot be seen by them from 20 ratings, so the               brations transfer to the real data only approximately, with
878
879
                                                                        16
                                      What Do Gains in Personalised Reward Modelling Measure?

880   no claimed direction of bias.                                        fixed beforehand.
881
      LoRe on all panels (Stage 6). Across PRISM pairs and                 Confirmatory and exploratory results. Confirmatory (rule
882
      MultiPref, binary and graded labels and k ∈ {5, 20, 50},             fixed before the result): the stage-2a hypotheses H1–H5 and
883
      LoRe never improves direction or choice accuracy over its            their replications (H6, on the symmetric offsets, was added
884
      own k = 0 version or over the text-only model (own gain              after the first results and is exploratory; its later replications
885
      −6.2 to +0.1 points; the regularised version −1.1 to −0.0),          were evaluated prospectively); B1–B3; C1–C4; R1 (PRISM
886
      and its log-likelihood is below the text-only model’s every-         native choices); the Stage-3 positive control at +1.7 and
887
      where. Its own − other is positive in some cells (MultiPref          +5.2 oracle points (no power); the Stage-4 ceiling rule (not
888
      binary, k = 20: +1.3 [+0.5, +2.0]) while its own gain is neg-        met); the Stage-6 LoRe rule (PRISM null not withdrawn).
889
      ative there (−1.2 [−1.9, −0.5]): another rater’s over-fitted         Exploratory (added or changed after a result, labelled in
890
      weights are anti-informative, the scale problem discussed            the text): the symmetric offsets DFs and their hypothesis;
891
      for the reference learner, so own − other alone is not ev-           the few-shot-tuned prior; the +10 and +21 panels and the
892
      idence of personalisation for methods whose few-shot fit             full-feature runs; the reference learner and its oracle-scale
893
      over-fits.                                                           contrast; the calibrated real-data aspect test; the regularised
894
                                                                           LoRe; the two-way bootstrap re-estimates.
895   Stage 7 (after the seventh review; PROTO-
896   COL STAGE7.md). S7-1, cross-fitted ridge probes                      Reproducing LoRe’s PRISM result (Stage 6, Amend-
897   (prompt-group folds, out-of-fold R2 ) of the two injected            ments 2–3). Unseen-user binary accuracy, mean ± sd over
898   features from each learner’s inputs: log length ratio 0.88           five random user splits, LoRe’s native setting (users with at
899   (VPL/PAL-B PCA-256 xB − xA ), 0.93 (full features),                  least six dialogues split 50/50, half of each user’s conversa-
900   0.73 (D/DL joint PCA-256); random direction 0.65, 1.00,              tions for few-shot and half for test, one chosen-vs-other pair
901   0.02. By the rule fixed beforehand, S7-2 was run for                 per conversation; 1,267 users, about three few-shot pairs per
902   the low-rank latent only: the random direction re-drawn              unseen user):
903   inside its joint embedding (orthogonal to the consensus
                                                                           Taking one pair per interaction instead (every turn; 20 pairs
904   direction), τ calibrated to oracle gains of +5.1 and +10.4.
                                                                           per user) gives 58.8 / 59.2 / 57.0 with our features. The
905   Own − other at k = 20 / 50: +0.08 [−0.18, +0.33] / +0.03
                                                                           remaining differences — a stronger monolithic baseline here
906   [−0.29, +0.34] at +5.1; +1.97 [+1.31, +2.65] / +7.02
                                                                           and a few-shot fit that helps there but hurts here — could not
907   [+5.84, +8.16] at +10.4; the reference learner is unchanged
                                                                           be traced to any setting the LoRe paper reports. Under our
908   (own − population +2.67 and +8.33). S7-3, seen-rater
                                                                           protocol (user- and conversation-disjoint folds) the Skywork
909   ceiling on real MultiPref (training raters × test items, 904
                                                                           embeddings leave the conclusion unchanged: LoRe’s own
910   rater-folds, trained parameters; derangement of training
                                                                           gain at k = 20 is −1.3 [−2.5, −0.2] points (regularised −0.5
911   raters): direction accuracy minus the text-only model
                                                                           [−1.3, +0.2]) and own − other +0.2 [−0.9, +1.2], as with
912   −0.51 [−0.88, −0.11] (five offsets), −0.00 [−0.20, +0.18]
                                                                           our features.
913   (symmetric), −0.42 [−0.81, −0.02] (low-rank); own −
914   other −0.23, +0.10, −0.11 [−0.57, +0.36]; log-likelihood             Positive-control details (moved from §5.6). In the ex-
915   over the text-only model +0.13 nats for all three. By                ploratory dose-response, VPL and PAL-B with PCA-256
916   the rule fixed beforehand, the ranking null also holds               features detect +21-point preferences but recover less than
917   for seen raters. S7-4 (Amendment 3), semantic axes —                 half a point of +10; on the real data they are at the null-
918   (s1) log(1 + markdown list/heading lines) of B minus A,              control level, and the low-rank latent’s +0.30 [−0.00, +0.60]
919   (s2) the same for a fixed list of hedging/refusal phrases            is matched by the text-independent offsets (+0.32), i.e. by
920   — calibrated to +4.6 and +9.7 oracle points: probes R2               scale use. With full features PAL-B detects +10 points but
921   0.37–0.66 (formatting) and 0.09–0.24 (hedging); own −                not +5. PAL-B’s own − other contrast is negative with
922   other at k = 20 / 50 for the low-rank latent +0.09 / +0.05           compressed features (null control −0.23, real data −0.43):
923   and −0.18 / −0.08, VPL −0.05 / +0.04 and +0.03 / +0.03,              its per-rater adaptation adds noise there; with full features
924   PAL-B (compressed features) −0.24 / −0.12 and +0.27 /                it is at zero (−0.04, +0.11). k = 50 contrasts use the 180
925   +0.40 [−0.02, +0.85]; reference learner own − population             of 209 raters with at least 50 training-item ratings. How
926   +2.57 [+1.61, +3.57] and +7.44 [+5.96, +8.91]. No method             far are these methods from what the data allow? A
927   detects either panel. S7-5 (Amendment 4), the in-span                well-specified reference learner — the two injected features
928   panels over four draws (θ and label seeds 1, 11, 12, 13): the        known, an empirical-Bayes prior on each rater’s weights,
929   low-rank latent’s own − other at k = 20 is +1.97, +2.83,             style offsets re-fitted — recovers +0.89 [+0.40, +1.37], +3.1
930   +3.14, +1.44 [+0.92, +1.96] at +9.3 to +10.9 oracle points           [+2.3, +4.0] and +8.0 points of +1.7, +5.2 and +10.1-point
931   (detected in 3 of 4; k = 50 +5.0 to +7.3) and +0.00 to +0.14         oracle gains from 20 ratings (own versus population weights,
932   at +4.7 to +5.5 (0 of 4); the reference learner +7.4 to +8.3         the oracle’s scale). Linear probes show the injected direction
933   and +2.6 to +2.9. Both statements are kept under the rule            is available to VPL and PAL-B (out-of-fold R2 0.65 com-
934
                                                                      17
                                         What Do Gains in Personalised Reward Modelling Measure?

935               embeddings                                        monolithic BT        LoRe, no adaptation    LoRe, few-shot fit
936               Skywork-Reward-Llama-3.1-8B-v0.2 (LoRe’s)         67.4 ± 1.1           67.3 ± 1.8             63.6 ± 3.7
937               Qwen2.5-7B-Instruct (ours)                        67.7 ± 1.5           68.7 ± 1.7             61.0 ± 2.5
938               published (Bose et al., 2025)                     61.0 ± 1.2           —                      71.0 ± 1.0
939
940
941   pressed, 1.00 full) but not to the low-rank latent’s joint em-           matter (in-sample +9.7 points), but they are too rare to move
942   bedding (0.02); re-injected inside that embedding, the latent            accuracy. A calibrated test with the item’s consensus aspects
943   detects +10 points (3 of 4 draws) but not +5 (0 of 4); these             from other annotators finds individual weights transferring
944   probes predate the corrected adaptation prior, with which                worse than the population’s (−0.28 [−0.56, −0.06] at k =
945   the ordinal latent detects the original +10-point panel (Stage           20; exploratory, Appendix B).
946   14). With semantic axes (formatting, hedging/refusal) no
                                                                               5.9 Developers rating code readability (full text moved
947   method detects even +9.7 points. Twenty ratings permit use-
                                                                               from §5). Two code-readability studies have persistent de-
948   ful recovery in these injected families when the generating
                                                                               veloper identities: Buse–Weimer (121 raters × 100 Java
949   features are supplied; the observed gap implicates feature
                                                                               snippets) and Dorn (3,393 developers with at least ten rat-
950   representation and the learners’ inductive biases. These are
                                                                               ings of 360 Java/Python/CUDA snippets). With Qwen2.5-
951   comparisons with synthetic panels of specific injected forms
                                                                               Coder-7B features, scale use transfers to new developers:
952   (noisier than the real data), not formal exclusion bounds;
                                                                               offsets gain +0.054 [+0.036, +0.074] nats per rating at k
953   details and seed variability in Appendix B. Generator and
                                                                               = 20 (Buse–Weimer) and +0.040 [+0.031, +0.049] at k
954   calibration as first described: We keep MultiPref’s structure
                                                                               = 10 (Dorn). For content we measure within-developer
955   (raters, items, who rated what, folds and k-shot draws) and
                                                                               concordance of predicted and given ratings over snippet
956   replace the labels by semi-synthetic ones. A generator —
                                                                               pairs, comparing a developer’s own weights with popula-
957   the text-only head plus scale-use offsets, fitted on all ratings
                                                                               tion weights under the same offsets. SAP with 22 classical
958   — gives each rating a distribution, to which a rater-specific
                                                                               readability attributes (line and identifier length, indentation,
959   content term (θr⊤ gi ) (−2, −1, 0, 1, 2) is added to the logits;
                                                                               nesting, comments, operators, . . . ) gives +0.40 [−0.25,
960   gi are two features of the response pair (the log length ra-
                                                                               +1.06] points at the pre-set k = 20 on Buse–Weimer (+1.30
961   tio and a random direction in the per-response embedding
                                                                               [+0.46, +2.18] at k = 50, exploratory) and −0.19 [−0.81,
962   space, orthogonal to the consensus quality direction) and
                                                                               +0.42] on Dorn at its pre-set k = 10; the low-rank latent
963   θr ∼ N (0, τ 2 I). The scale τ is calibrated on the generator
                                                                               is inconclusive on Buse–Weimer and switched off by vali-
964   alone so that an oracle that knows θr gains +1.7, +5.2, +10.1
                                                                               dation on Dorn. On Buse–Weimer the whitened full-rank
965   or +21.1 points of direction accuracy on the test ratings;
                                                                               features of 100 snippets are an item-identity encoding, so
966   τ = 0 is a null control. Every method is then run under the
                                                                               the text head carries no information about held-out snippets:
967   paper’s protocol. Because a method whose unpersonalised
                                                                               the latent row there does not test text-mediated personali-
968   state is not the population state can improve with anyone’s
                                                                               sation, and the population baseline rests on offsets and the
969   ratings, the contrast is the method adapted on the rater’s
                                                                               22 attributes alone (Dorn, with 360 snippets and 256 com-
970   own k ratings minus the same method given another
                                                                               ponents, is not affected). Details, the pre-set rule’s literal
971   test rater’s adapted parameters (a random derangement
                                                                               outcome on Dorn (met through the own − other contrast,
972   within fold, k and draw). Before the runs we fixed that the
                                                                               which is not on the oracle scale) and permutation controls
973   protocol has power at a strength if some content-interacting
                                                                               are in Appendices A–B.
974   method has a lower 95 % bound above +1 point at k = 20;
975   the +10 and +21 panels and the untuned-prior low-rank runs
976   were added after the first results and are exploratory.                  C. Implementation
977
      5.7 How much room is there? (full text moved from                        Rater identities. All four panels carry persistent rater iden-
978
      §5). Every MultiPref annotation carries the annotator’s own              tifiers (MultiPref pseudonyms, 227 evaluators, median 166
979
      helpfulness, truthfulness and harmlessness preferences, so a             ratings, never twice on one item; DICES rater IDs, 123
980
      rater’s trade-off between these values is observable. With               raters × 350 items in the release, 104 after its quality fil-
981
      the rater’s own aspect labels as inputs (an oracle for the               ter (used throughout); PRISM user IDs, one survey record
982
      content side), a pooled trade-off already gets 97.5 % of                 each; Community Alignment annotator IDs). Demographics
983
      directions right, and a rater-specific trade-off fitted on all of        never vary within an ID on DICES and in fewer than 0.3 %
984
      the rater’s training ratings adds only +0.10 [−0.24, +0.43]              of IDs on Community Alignment. On MultiPref, which has
985
      points (+0.44 even in-sample). The three recorded aspect                 no demographics, an evaluator’s tie rate and extreme-rating
986
      judgements point in opposite directions in only 4.0 % of                 rate in the first and second half of their ratings (by times-
987
      held-out non-tie comparisons; there individual trade-offs                tamp) correlate at 0.82 and 0.78 across evaluators, against
988
989
                                                                          18
                                        What Do Gains in Personalised Reward Modelling Measure?

990    −0.03 and 0.00 (largest 0.17) with evaluator labels shuf-              7B-Instruct features, scored on an independent rater panel,
991    fled (check rater ids.py). Shared accounts cannot                      recovers G/X = 10.5 % [5.7 %, 11.9 %] of the reproducible
992    be ruled out.                                                          shape (within-cell permutation control ≤ 0; positive control
993                                                                           0.35) — comparable to the upper end for ordinal quality
       Text features: last-token final-layer states of Qwen2.5-7B-
994                                                                           ratings (upper bounds 0.4–10 %) and below NLI (17–26
       Instruct under a 5-point judge prompt (MultiPref, PRISM)
995                                                                           %). Rater vs item. A long-format ordered-probit decom-
       or a 3-level safety prompt (DICES), label-free PCA to 256
996                                                                           position with real rater identities and penalties tuned by
       dimensions. Folds: 5 rater folds (stratified by group) paired
997                                                                           inner cross-validation: rater-specific thresholds improve
       with 5 prompt-group folds (split f holds out rater fold f
998                                                                           held-out likelihood by +0.036 nats per rating over item lo-
       and prompt-group fold f; the other crossings are not used);
999                                                                           cation alone, item-specific dispersion by a further +0.0014
       validation: 15 % of training prompt groups. k-shot draws: 5
1000                                                                          (ratio 25; 19–36 across the five folds); of the rater part, rater
       per k, identical across all models (RC-LoRA: draw 0 only).
1001                                                                          scale contributes +0.031 and rater shift +0.005.
       PRISM item folds are by conversation. Bootstrap: rater
1002
       clusters, B = 2,000. LoRA: r = 16 on all attention and MLP
1003                                                                          E. Protocols and what did not hold
       projections, lr 10−4 , one epoch, accumulation 8. VPL / PAL-
1004
       B: official architectures (latent 512, hidden 512; dpref 512,
1005                                                                          All analyses are documented in an analysis log: times-
       mlp2-gelu projectors, angle learner) with an ordered-logistic
1006                                                                          tamped internal protocols written before each stage (not
       link for graded labels; VPL’s KL weight selected from {0.01
1007                                                                          public registrations, so they document rather than certify
       (official), 0.001, 0} and PAL-B’s adaptation ridge by k-shot
1008                                                                          the order of decisions); changes after results are logged as
       validation (non-official choices made to prevent collapse
1009                                                                          amendments with reasons, and the symmetric style model
       and over-fitting).
1010                                                                          DFs and its hypothesis were added after the first full result.
1011                                                                          Not supported or not robust: (i) the stage-1 decision rule
1012   D. Where is the predictable structure?                                 returned “mixed” (text decodability not ≤ 10 %); (ii) non-
1013      Estimators and results                                              inferiority of the 5-parameter DF to the low-rank latent (DF
1014                                                                          − DL ≥ −0.005) holds with the training-rater prior but not
1015   Estimators. For an item with ratings on K ordered lev-                 with a few-shot-tuned prior on MultiPref (−0.015; −0.020
1016   els, let h be the empirical rating distribution and C the              with the corrected prior of Stage 14) and is formally not
1017   cumulative operator. Split the item’s raters at random                 met on PRISM (bound −0.006; with the corrected prior the
1018   into disjoint panels P1 (a raters) and P2 , and let q be a             latent is 0.004 nats ahead, bound −0.007); (iii) “scale beats
1019   cross-fitted location-only forecast with exactly the mode              shift” holds only on MultiPref; (iv) the originally registered
1020   and mean of P1 (built from other items in the same mode-               probit-family hypothesis is not supported (F1 − D = +0.020
1021   and-mean cell). With r1 = C(h1 − q), r2 = C(h2 − q),                   [−0.001, +0.041], the primary probit contrast after Amend-
1022   M = ∥r1 ∥2 /n and X = ⟨r1 , r2 ⟩/n, the forecasting value              ment 1; homoscedastic F − D = −0.029 [−0.049, −0.008];
1023   of the raw distribution over its own location obeys the iden-          superseded when the primary family was moved to the distri-
1024   tity S(h1 ) − S(q) = M − 2X under the ranked probability               butional head); (v) the prediction that published user latents
1025   score, so ρ = X/M is a split-half reliability of the distri-           encode style failed (R2 ≈ 0); (vi) the hybrid’s non-inferiority
1026   bution’s shape and the raw distribution beats its location             to DFs is formally not met (bound −0.014). Five baseline
1027   exactly when ρ > 1/2. Text decodability is the proper-                 problems found during the study were fixed in favour of
1028   score gain G = (2⟨r̂, r2 ⟩ − ∥r̂∥2 )/n of a residual r̂ decoded        the baselines — a missing constant column in the low-rank
1029   from frozen text features, cross-fitted over prompt groups,            latent, a scale non-identifiability in the probit group model,
1030   reported as the fraction G/X of the reproducible shape.                VPL’s posterior collapse, PAL-B’s near-unregularised adap-
1031   The rater–item decomposition fits ordered-probit models                tation, and the latent models’ mis-scaled adaptation prior
1032   Yir∗ = θi + δr + σi σr ε with item locations θi , rater shifts         (Stage 14) — and the runs before each fix are reported.
1033   δr , rater scales σr and item dispersions σi , compares held-
1034   out likelihood over random cells (every held-out rater and
       item appears in training), and chooses all penalties by inner          F. Community Alignment analysis log (Stages
1035
1036   cross-validation.                                                         8, 11, 12, 13)
1037   Reproducibility. With the split-half estimator defined                 The full sequence of analyses behind §6, in order, with the
1038   above, the reliability of the rating distribution’s shape be-          corrections of the fifth review applied (event-level simula-
1039   yond its exact mode and mean is ρ = 0.25 [0.22, 0.29] on               tion as the principal achievable-gain benchmark, the pair-
1040   MultiPref overall preference with three raters (helpful 0.29,          level one as a consistency check; Holm as an approximate
1041   harmless 0.21): the raw few-rater distribution forecasts a             sensitivity analysis). Protocols: PROTOCOL STAGE8.md
1042   new rater worse than its own location (ρ < 12 ). Text decod-           (Am. 1–2), PROTOCOL STAGE11.md (Am. 1–10), PRO-
1043   ability. A cross-fitted ridge decoder on frozen Qwen2.5-               TOCOL STAGE12.md.
1044
                                                                         19
                                       What Do Gains in Personalised Reward Modelling Measure?

1045 On a dataset built for preference diversity, user-specific             ability; this does not show that concentration explains the
1046 signal exists; estimated choice gains remain small. Com-               real data), and the full-size prior over-adapts. With the at-
1047 munity Alignment (first turns, 2,957 new users in five coun-           tribute set and prior scale chosen on pseudo-new training
1048 tries, the chosen response paired with each other one; Stage           users (c = 0.125–0.25 in every fold, never “no adaptation”),
1049 8): at k = 20 every method’s own gain over its own k = 0               transfer-calibrated adaptation gains +0.49 [+0.20, +0.77]
1050 version has an upper bound below +0.5 points (VPL +0.15                choice points and +0.0088 [+0.0061, +0.0116] nats on
1051 [+0.03, +0.27], LoRe-reg +0.35 [+0.25, +0.46], LoRe −2.34              the frozen test users, ahead of the tuned rank-2 model by
1052 [−2.79, −1.88]), yet a user’s own adapted parameters beat              +0.30 [+0.04, +0.56] points — but not of ordinary validated
1053 another user’s — the frozen rule’s own − other half, which             shrinkage: an isotropic prior over the same three attributes,
1054 a summary-script bug first dropped and which therefore lit-            its scale chosen the same way (τ 2 = 0.1 in every fold),
1055 erally reads “content personalisation detected”: LoRe +3.27            gains +0.66 [+0.37, +0.95] points and +0.0110 nats, and
1056 [+2.85, +3.70], LoRe-reg +0.36, VPL +0.31. A within-                   TRV − isotropic is −0.17 [−0.29, −0.05] (not significant
1057 country derangement (added after the result) retains the con-          after multiplicity adjustment). No advantage of the esti-
1058 trast, so country and language do not explain it (own − same-          mated covariance is established; what helps is the choice of
1059 country other +3.22 [+2.83, +3.60]; same-country − any-                attributes and strong shrinkage (light adaptation). A prompt-
1060 country +0.03 [−0.12, +0.18]). A cross-fitted, simulation-             group × user two-way bootstrap widens TRV’s interval to
1061 calibrated diagnostic agrees on what the signal is: users’ de-         [+0.01, +0.97]. These are below the one-point threshold, at
1062 viations from the population weights on response length and            a different budget (20 choice events, three dependent pairs
1063 paragraphing reproduce across disjoint prompt sets (trans-             each) from Stage 8’s 20 pairs, where VPL and LoRe-reg
1064 ferable variances 0.32 [0.25, 0.40] and 0.72 [0.23, 1.29];             also show small positive own gains. Frozen evaluation on
1065 0.33 and 0.76 [0.26, 1.35] after prompt-type adjustment;               new prompts (Stage 12). TRV, unchanged, on the same
1066 exploratory, Stage 11; with 200 simulation replicates the              users’ second turns (83,238 never-analysed choices; 1,702
1067 length false-detection rate is 5.0 % [2.4, 9.0] and paragraphs’        test users at k = 20 events): +0.38 [+0.13, +0.64] choice
1068 power 85 % [79, 89], so neither calibration target is estab-           points and +0.0046 [+0.0031, +0.0063] nats per pair over
1069 lished beyond binomial error), while no method converts                µ; validated isotropic shrinkage +0.31 [+0.05, +0.58] and
1070 them into a one-point gain at k ≤ 50. Users’ stable prompt             +0.0038; TRV − isotropic +0.07 [−0.07, +0.22]; the tuned
1071 mixes could create such residual structure without different           rank-2 model selects no adaptation in three of five folds
1072 preferences on the same tasks; as an observational check the           (−0.05). By the pre-set rules the benefit is reproducible
1073 length cross-covariance centred within language × prompt-              (both lower bounds above 0) and sub-threshold (accuracy
1074 cluster cells is 0.206 [0.183, 0.231] against 0.210 uncentred,         upper bound below +1), with no advantage over ordinary
1075 and a same-language user with a matched task mix (clus-                shrinkage; the prompt-group × user interval for accuracy
1076 ter shares within L1 0.002) is a worse predictor than the              covers 0 ([−0.04, +0.83]). No language reaches signifi-
1077 user’s own coefficient by +0.80 [+0.45, +1.16] points and              cance alone. The length cross-moment again reproduces
1078 +0.009 nats, though better than a random other by +0.75;               across disjoint prompt halves in every fold (0.12–0.19), the
1079 the two contrasts approximately partition the unmatched                list/heading one does not (negative in two folds). These are
1080 own − other (+1.54), which is not a causal decomposition,              new prompts and turns of previously studied users, not new
1081 and the matched other is about 0.35 points worse than the              users. Multiplicity (Am. 10; an approximate, exploratory
1082 population model (Stage 11 Am. 8). Two annotators agree                sensitivity analysis: p-values recovered from reported
1083 on 64.3 % of shared response pairs, the text-only model is             intervals by a symmetric normal approximation, ques-
1084 right on 71.7 % of them. Using the transferable covari-                tionable for heavy-tailed cross-moments, then Holm at
1085 ance as the prior (θ̂u − µ = c Ĉ(I + c Iu Ĉ)−1 su over               0.05). In Stage 8’s frozen family (six methods × two con-
1086 length, paragraphs and list/heading, Ĉ estimated on training          trasts) the own − other contrasts of LoRe, LoRe-reg, VPL
1087 users only; S11-3) gives +0.13 [−0.28, +0.53] points at c              and PAL4 survive, and the detection is unchanged; the posi-
1088 = 1, although the fitted Gaussian model implies +2.8 for               tive own gain of VPL (+0.15) and the negative own effects
1089 this learner at k = 20 (oracle +4.2; with event-level sim-             of PAL4 and DFp do not. Across a family of 29 selected
1090 ulated labels that keep one winner per choice event, +1.9              Stage-11 contrasts (not every reported contrast; e.g. AUC
1091 and oracle +3.6 — a third lower, just inside the pre-set               contrasts, the k = 32 within-cluster and matched − cyclic
1092 factor-1.5 tolerance, Stage 11 Am. 6). The gap is not mys-             contrasts are omitted), the length statements survive (trans-
1093 terious: on the evaluated split transfer from support to test          fer, within-cluster transfer, own − matched other, TRV and
1094 prompts is established for length (0.41 [0.27, 0.55]) but not          isotropic gains, WIMHF-style length), while paragraphs’
1095 for paragraphs or lists (intervals cover 0), heavier-tailed or         transferable variance, TRV − rank-2, TRV − isotropic and
1096 concentrated deviations with the same covariance lower the             the new-user length gain of S11-1 (b) (+0.45) do not; the
1097 simulated gain of this learner to +1.6 to +0.4 (event-level:           first-turn evidence that isotropic shrinkage beats TRV is
1098 +0.9 to −0.4) (so covariance alone does not determine learn-           therefore weaker, but no advantage of TRV is established
1099
                                                                       20
                                           What Do Gains in Personalised Reward Modelling Measure?

1100   either. Status: the original Stage 11 diagnostic failed its                 the scale-use model’s logits, with θr ∼ N (µ, diag σ 2 ), the
1101   pre-specified calibration criterion, leaving all three primary              population weights µ and the per-attribute variances σ 2
1102   outcomes inconclusive and the adaptation gate unmet; all                    estimated on the training raters by automatic relevance de-
1103   subsequent analyses are exploratory; the final procedure se-                termination (Laplace approximation, MacKay’s fixed-point
1104   lected attributes and shrinkage on training users only, but its             update); a new rater’s θr is their MAP from k ratings. The
1105   candidate family was developed after inspecting test results,               contrast is the rater’s own weights against the population
1106   and the bootstrap intervals are nominal and do not account                  weights µ, with the rater’s own scale-use offsets kept (oracle
1107   for this adaptation. Ĉ is an uncentred cross-moment of one-                scale).
1108   step deviations, not a bounded share of the fitted random-
                                                                                   Own minus population weights, direction accuracy at k = 20
1109   slope variance; the principal achievable-gain benchmark is
                                                                                   in points, 95 % rater bootstrap (ranges over four synthetic
1110   the event-level simulation (one winner per choice event, Am.
                                                                                   draws; VPL / PAL-B / low-rank latent: own − other on the
1111   6); the pair-level figures are a consistency check, and both
                                                                                   same panels, §5.6). Rules fixed in advance: no detection
1112   are model-implied gains for specified learners, not general
                                                                                   on the null draws (none), detection of the semantic panels
1113   learnability ceilings.
                                                                                   in at least three of four draws (four of four each). The
1114
       Stage 13 methods (PROTOCOL STAGE13.md). S13-                                SAP column uses the fixed-point variance update adopted
1115
       1: an item is an exact (prompt, ordered four-response)                      after the pre-registered EM update was found to stall when
1116
       identity on CA first turns; for each pair of same-fold test                 raters have few ratings (EM results in Appendix B); the
1117
       users who chose different responses a ̸= b on an item,                      shared-variance column uses the same update; the rank-
1118
       S = (δu − δv )⊤ (xa − xb ) with δ the adapted minus popula-                 2 model’s map ridge and adaptation strength (including
1119
       tion attribute weights (population terms cancel); assignment                none) are selected on held-out training raters at k = 20.
1120
       log-score log σ(S) − log 12 , averaged over 5 support draws,                Exploratory: the ablations and the out-of-dictionary panels.
1121
       within item, then over items; two-way item × user bootstrap
1122                                                                               SAP recovers what the published learners miss and matches
       (B = 1,000). Learners: the Stage-12 isotropic procedure
1123                                                                               the learner told the features; attribute-specific variances
       (primary) and TRV, selected on pseudo-new training users;
1124                                                                               improve recovery over one shared variance under the same
       20 support events in training prompt groups. S13-2: the
1125                                                                               update (which loses 60–76 % of the gain); a rank-2 subspace
       same procedures frozen on MultiPref binary directions (ties
1126                                                                               on the same attributes, tuned with the same care, matches
       excluded), Stage-1 folds, rater and rater × prompt-group
1127                                                                               SAP on the semantic panels and abstains on the null (un-
       bootstraps. S13-3: each user’s first-turn isotropic deviation
1128                                                                               tuned, it lost 2.1–2.7 points; Appendix B), while on real
       (20 support events, draw 0) is frozen in first-turn attribute
1129                                                                               MultiPref SAP is ahead of it by +0.41 [+0.15, +0.66] points
       units and added, without rescaling or tuning, to a third-turn
1130                                                                               (paired, exploratory). The variance assigned to correlated
       population model (ridge on history-conditioned Qwen2.5-
1131                                                                               attributes means the high-variance set is a set of candidates,
       7B features of the transcript through the third prompt, trun-
1132                                                                               not independently identified preference dimensions. SAP
       cated to the last 6,000 characters, plus per-language µ) fitted
1133                                                                               learns transferable shrinkage over supplied axes; it does not
       on other users’ third turns; scored on the user’s third turns
1134                                                                               discover new ones (outside the dictionary it recovers under
       outside the support conversations (≥ 5 events; turns with
1135                                                                               a tenth of a +10.5-point preference). With the fixed-point
       incomplete history excluded, Am. 5); the pre-set rule re-
1136                                                                               update its estimated effects on the four null draws are near
       quires both accuracy and log-likelihood lower bounds above
1137                                                                               zero (−0.03 . . . +0.11 at k = 20 and 50; with EM it lost up
       0. Turn 4 was not opened.
1138                                                                               to 0.5 points at k = 50); this is not a calibrated false-positive
1139                                                                               rate, and forced adaptation does hurt on Community Align-
1140   G. Screened attribute personalisation                                       ment (below). On real MultiPref its gain over population
1141      (formerly §5.8)                                                          attribute weights (the rater’s offsets kept) is +0.28 [−0.00,
1142                                                                               +0.58] direction points and +0.0028 [+0.0013, +0.0043]
1143   In the tested settings of §5.6, 20 ratings suffice when the con-            nats per rating — SAP’s achieved gain under this proto-
1144   tent axes are supplied, and the published learners, as evalu-               col, not a bound on what these attributes could offer. The
1145   ated, do not find them. Screened attribute personalisation                  decisive test was frozen before its data were embedded:
1146   (SAP) supplies candidate axes and learns from the training                  Community Alignment’s native choices (1,897 new users
1147   raters which of them people differ on. Each comparison                      in five languages, k = 20 choice events, per-language popu-
1148   is described by 24 interpretable attribute differences fixed                lation weights, adaptation strength of every method chosen
1149   in advance (length, markdown structure, hedging/refusal,                    on held-out training users). The fitted model assigns sub-
1150   code, digits, questions, pronouns, sentence and word length,                stantial training-user variation to length, paragraphs and
1151   examples, disclaimers, summaries, evidence phrases, po-                     formatting (prior variances 0.29–0.37 for length, 0.25–0.30
1152   liteness, refusal, lexical diversity, overlap with the prompt,              for paragraphs, 0.19–0.23 for list/heading lines; one fold
1153   . . . ); a rater’s content term (θr⊤ ai )(−2, . . . , 2) is added to        assigns 1.37 to URLs, ≈ 0 in the others), yet adaptation
1154
                                                                              21
                                                    What Do Gains in Personalised Reward Modelling Measure?

1155
       Table 6. SAP: own − µ direction (CA: choice) accuracy in points, k = 20, the rater’s scale-use offsets kept. Rank-2: the same attributes in
1156
       a tuned rank-2 subspace; DL: low-rank latent; reference: learner given the generating features. Ranges over 4 synthetic draws.
1157
       panel (oracle gain)                    SAP                                         one shared variance    rank-2, same attributes VPL / PAL-B / DL reference
1158
       null, 4 draws (0)                      −0.03 . . . +0.04                           +0.06                  0 (abstains)           —                 —
1159   formatting + hedging (+4.6), 4 draws   +2.29 . . . +2.82                           +0.69 [+0.21, +1.18]   +2.78 [+1.84, +3.72]   ≤ +0.09           +2.57 [+1.61, +3.57]
1160   formatting + hedging (+9.7), 4 draws   +7.44 . . . +8.12                           +3.09 [+2.13, +4.02]   +7.75 [+6.09, +9.36]   ≤ +0.27           +7.44 [+5.96, +8.91]
       two axes outside dictionary (+10.5)    +0.95 [+0.50, +1.39]                        —                      —                      —                 —
1161   real MultiPref                         +0.28 [−0.00, +0.58]                        +0.28 [+0.04, +0.53]   −0.14 [−0.51, +0.24]   —                 —
1162   real MultiPref, permuted in item       −0.09 [−0.23, +0.05]                        —                      —                      —                 —
       CA, frozen, k = 20 events              0 (abstains); forced −0.40 [−0.87, +0.06]   −0.70 [−1.15, −0.25]   +0.17 [−0.17, +0.51]   —                 —
1163
1164
1165
       from 20 choice events does not improve held-out prediction:
1166
       validation switches SAP off in all five folds, forcing it costs
1167
       −0.40 [−0.87, +0.06] choice points and −0.0097 [−0.0143,
1168
       −0.0052] nats, and the tuned low-rank model gains +0.17
1169
       [−0.17, +0.51]. The pre-set rule (lower bound above +1
1170
       point) is not met.
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
                                                                                           22


=== (B) PROTOCOL_STAGE14.md ===
# Stage 14 protocol — a real-data positive control (Jester) and contested-item stratification

Written 2026-11-11, before any Stage 14 outcome was computed. No Jester rating value has been summarised beyond the label-blind facts in §1.2; no stratified
Stage 12 number has been looked at.

## 0. Why

The paper reports small individual gains on every real panel (SAP +0.28 / +0.08 points, TRV +0.49 / +0.38 points). Two readings are open and the paper cannot
currently separate them:

1. *Domain:* these domains carry little stable individual taste at the available history length.
2. *Method:* our pipeline cannot recover individual taste even where it exists. The existing positive controls are synthetic (planted effects).

S14-1 runs the pipeline on a text domain where strong, stable individual taste is established in the literature (joke ratings; Goldberg et al., 2001).
S14-2 asks whether the gains we do see are concentrated on the comparisons the population model itself is unsure about.

## 1. S14-1 — Jester positive control

### 1.1 A finding made while designing this stage (label-blind; disclosed because it changes the design)

`factorised_rm.py` uses whitened PCA scores with `XD = min(256, items − 1)` (Stage 10 Am. 1). When the panel has at most `XD + 1` unique items, whitened
full-rank scores are an item-identity encoding: the Gram matrix is exactly `n (I − 11ᵀ/n)`. Checked on `bw_raters` without using any rating
(100 snippets, XD 99: diagonal 99.0, every off-diagonal −1.000, sd 0.000; held-out ridge R² of the raw first PC from the whitened scores −0.048 at
λ = 0.001, 1, 100). On `dorn_raters` (360 snippets, XD 256) the encoding is not degenerate (R² 0.997 / 0.928 / 0.377).

Consequences:

- The Stage 10 Buse–Weimer D / DF / DL rows cannot test text-mediated personalisation on held-out snippets (the text head cannot generalise there by
  construction; this is consistent with the reported D concordance of 51.6 %). The paper will say so (§4).
- Jester has 128 usable jokes, so "pipeline unchanged" would be degenerate at XD = 127. The PCA dimension must be chosen (§1.4). This is a declared
  deviation from the Stage 10 pipeline, fixed here before any outcome.

### 1.2 Data (label-blind facts only)

- Source: Jester release with 59,132 users and 140 jokes with ratings (1,761,439 ratings, continuous −10…+10). The official host
  (eigentaste.berkeley.edu) was unreachable from this server; ratings and joke texts come from two third-party Hugging Face mirrors
  (sha256 prefixes `e265a78efd1aa902` ratings parquet, `06d7e50c3c9bcfe9` texts parquet). The text ↔ rating mapping was verified by matching each
  joke's sorted rating multiset between the two mirrors (140 / 140 unique matches); `prep_jester.py`.
- Terms: "Freely available for research use when acknowledged with the following reference": Goldberg, Roeder, Gupta, Perkins, *Eigentaste: A Constant
  Time Collaborative Filtering Algorithm*, Information Retrieval 4(2), 133–151, 2001. Data are not committed.
- Panel `jester_raters`: users with ≥ 120 ratings (3,238 users); jokes rated by ≥ 90 % of them (128 jokes; lowest coverage 0.947; the other 12 jokes about
  0.016); a random sample of 1,000 of these users (`RandomState(14).choice` over sorted user ids, without replacement). Ratings per sampled-population
  user on the 128 jokes: min 108, median 128, max 128. Joke length 52 / 318 / 1,326 characters (min / median / max).
- Scale: ratings binned to K = 5 at fixed cut points −6, −2, 2, 6 (bins `≤ −6`, `(−6, −2]`, `(−2, 2]`, `(2, 6]`, `> 6`), fixed without looking at the
  rating distribution.
- Features: Qwen2.5-7B-Instruct last-token state of a humour-rating judge prompt, one row per joke (panel `jester_items`), frozen.

### 1.3 Pipeline (as Stage 10 unless stated)

`factorised_rm.py --concord --adapt_tune --perm_control --models D,DF,DL`, 5 rater folds × 5 joke folds (seed 0), 15 % validation jokes (seed 1),
k ∈ {0, 5, 10, 20, 50} support ratings on training jokes, 5 support draws, d = 8, same penalty grids. Primary k = 20.

### 1.4 The three rungs

| rung | model | features | validation split | evaluation cell | question |
|---|---|---|---|---|---|
| L0 | linear CF reference (`s14_cf.py`) | joke identity | pseudo-new training raters | test raters × training jokes not in the support | does this panel carry recoverable taste at k ratings? |
| L1 | pipeline DL | item-identity encoding (XD = 127, the Stage 10 rule) | held-out *ratings* of training jokes (`--val_ratings`, 15 %, seed 1) | test raters × training jokes not in the support (`--seen_items`) | does the pipeline's latent model + adaptation recover taste when text generalisation is not needed? |
| L2 | pipeline DL | PCA dimension chosen per fold (below) | held-out jokes (as Stage 10) | test raters × held-out jokes | the paper's setting: new rater, new item |

- **PCA dimension for L2.** `--xd_grid 4,8,16,32,64`: in each fold, D is trained at every dimension (its own penalty grid) and the dimension with the
  highest validation log-likelihood (training raters × validation jokes of that fold) is used for D, DF and DL in that fold. No test rater and no test
  joke enters the choice. Limit stated in advance: the dimension is chosen for the population text head, not for DL.
- **L1b (diagnostic, no rule):** the L2 run evaluated on seen jokes — how much of the L1 gain survives the text bottleneck.
- **L0 details.** Binned scores 0–4. Training raters × training jokes; joke means μ_i; rater-centred residual matrix (missing cells = 0); rank-r SVD
  loadings v_i. New rater: ridge estimate of (b_r, u_r) from the k support ratings; prediction μ_i + b_r + u_r·v_i. Rank r ∈ {1, 2, 4, 8, 16} and ridge
  ∈ {0.1, 1, 10, 100, 1000} chosen per fold and k on pseudo-new training raters (20 % of training raters, `RandomState(3 + fold)`; loadings refit
  without them; squared error on their non-support ratings). Same folds and the same support draws (seeds) as the pipeline. Comparator μ: joke means only.
- **L2 diagnostics in `s14_cf.py` (no decision rule; multiplicity of three L2 learners stated):**
  - *CF-text:* μ_i and v_i regressed on the text PCs (ridge; dimension ∈ {4, 8, 16, 32, 64} and ridge ∈ {0.1, 1, 10, 100, 1000} chosen on validation
    jokes by squared error of training raters' ratings); new rater's u_r from the support ratings with the true loadings of the support jokes; prediction
    on held-out jokes μ̂_i + u_r·v̂_i; comparator μ̂_i.
  - *ISO:* per-rater ridge on the text PCs of the support jokes' residuals from μ_i, isotropic prior, strength chosen on pseudo-new training raters;
    prediction μ̂_i + x_i·w_r; comparator μ̂_i. Same text dimension as CF-text.

### 1.5 Endpoint and rules (k = 20)

Endpoint: within-rater pairwise concordance in points — pairs of a rater's evaluation ratings with different binned scores; a pair is concordant if the
predicted expected scores order it correctly, prediction ties count ½. Rater bootstrap over (fold, rater), seed 17, B = 2000, draws averaged within rater.

- **own − μ** = model adapted on the rater's own k ratings minus the same model at the prior mean (DL(k) − DL(0); for L1 / L1b the prior-mean model is
  evaluated on the same seen-joke cell). Preferred contrast (Stage 10 Am. 3).
- **L0 passes** if CF own − μ has lower bound > +1 point.
- **A pipeline rung (L1, L2) detects taste** if (i) DL own − μ has lower bound > +1 point and (ii) (DL own − μ) − (DF own − μ) has lower bound > 0
  (the text-interacting latent adds to what category offsets do through the softmax).
- Secondary, reported without a rule: own − other (derangement), held-out log-likelihood DL − DF and DF − D, D's concordance, L1b, k ≠ 20, the ratio
  DL gain / CF gain.

### 1.6 Readings fixed in advance

- **R1 — L0 fails.** The binned Jester panel does not show recoverable taste at k = 20 by the reference method; no conclusion about the pipeline;
  another domain is needed.
- **R2 — L0 passes, L2 detects.** The pipeline recovers known taste in the paper's setting. The small real-panel gains are then evidence about those
  domains (for the DL family), and the paper can state that gains scale with how much stable taste the domain carries.
- **R3 — L0 passes, L1 detects, L2 does not.** The latent model and adaptation work; generalising taste to unseen jokes from frozen text features is not
  shown with 128 jokes. CF-text passing (own − μ lower bound > +1) would point at DL's text-interaction map; CF-text failing would point at the features
  or the item count, and a many-item domain would be needed (amendment). The paper's DL negatives on held-out items then cannot separate domain from
  method.
- **R4 — L0 passes, L1 does not detect.** The pipeline's DL model and adaptation fail to recover known taste even on seen items. The paper's DL negatives
  cannot be read as domain properties, and the implementation must be examined before anything else.

### 1.7 Limits stated in advance

- The control covers the DL family (D / DF / DL of Stages 2–10). SAP and TRV act on attribute features of response pairs and are not exercised here.
- 128 items; one feature model; one prompt.
- Jester's interface chose which jokes each user saw; restricting to near-complete users and to jokes with ≥ 94.7 % coverage limits this.
- Third-party mirrors (§1.2). Binning discards within-bin order.
- L1 changes two things relative to L2 (features and validation split); it is the pipeline's model class and adaptation code, not the Stage 10 run
  configuration.

## 2. S14-2 — are the gains concentrated on contested comparisons?

Status: new tests on previously analysed data (as S13-1). The pooled Stage 12 results are known; the stratified ones are not.

- Code: `s14_2.py` executes the `s12.py` source unchanged except for two hooks (each pattern asserted to occur exactly once) and is cut before the
  Stage 12 output is written, so no Stage 12 file is overwritten. Output `results/stage14_2_<panel>.json`.
- Panels: `ca_pairs` (first turns), `ca_pairs_second`, `multipref_pairs`.
- **Contestedness is label-free for the test pair and fixed here:** the population model's absolute logit |lg_pop| on the pair. "Contested" = below
  the 20th percentile of |lg_pop| over that fold's training users × training items; "rest" = all other test pairs.
- Endpoints per stratum: own − μ (TRV − pop, and iso − pop) accuracy in points and log-likelihood ×100 per pair; user bootstrap (seed 17, B = 2000,
  primary) and prompt-group × user two-way bootstrap (secondary, B = 1000).
- Rules: **practically meaningful on contested pairs** if TRV − pop accuracy on the contested stratum has lower bound > +1 point; **concentration** if
  (contested − rest) has lower bound > 0 for accuracy and for log-likelihood.
- Caveat fixed in advance: a small shift in the logit changes the predicted choice only near zero margin, so accuracy gains concentrate there
  mechanically; log-likelihood is therefore co-primary for "concentration", and an accuracy-only concentration will be reported as mechanical.
- Sanity check: the pooled TRV − pop accuracy and log-likelihood from the same run must reproduce the Stage 12 values to the printed precision;
  otherwise the run is discarded.
- Also reported: share of test pairs in the contested stratum; pop accuracy per stratum.

## 3. Multiplicity

S14-1: one primary rule per rung at one k; L1b, CF-text, ISO, own − other and other k are descriptive. S14-2: three panels × two endpoints; intervals
are unadjusted 95 % and will be reported as such.

## 4. Paper changes that do not depend on the outcome

PAPER4_DRAFT.md will disclose §1.1 where the Stage 10 Buse–Weimer D / DF / DL rows are used.

## 5. Results — S14-2 (2026-11-11; job 15526; rules of §2 applied as written)

Sanity check passed on all three panels (pooled TRV − pop accuracy and log-likelihood reproduce Stage 12 to 1e-15). Intervals: user bootstrap
(primary), then the two-way bootstrap in braces. Accuracy in points, log-likelihood ×100 per pair.

| panel | share contested | pop accuracy contested / rest | TRV − pop accuracy, contested | rest | contested − rest | TRV − pop LL, contested | rest | contested − rest |
|---|---|---|---|---|---|---|---|---|
| CA first turns (36,963 pairs, 1,897 users) | 0.223 | 52.5 / 70.6 | +1.62 [+0.72, +2.52] {+0.08, +3.14} | +0.16 [−0.07, +0.41] | +1.46 [+0.56, +2.35] {−0.14, +2.98} | +0.34 [+0.09, +0.58] | +1.04 [+0.70, +1.38] | −0.69 [−1.09, −0.29] {−1.32, +0.05} |
| CA second turns (33,615 pairs, 1,702 users) | 0.214 | 53.4 / 67.7 | +1.62 [+0.63, +2.53] {−0.04, +3.31} | +0.05 [−0.13, +0.23] | +1.57 [+0.59, +2.49] {−0.07, +3.27} | +0.46 [+0.29, +0.63] | +0.46 [+0.26, +0.65] | +0.00 [−0.24, +0.24] |
| MultiPref (6,163 pairs, 202 users) | 0.193 | 55.3 / 72.0 | +0.02 [−1.38, +1.37] | −0.06 [−0.15, +0.02] | +0.08 [−1.31, +1.44] | +0.07 [−0.11, +0.23] | +0.06 [−0.04, +0.18] | +0.00 [−0.23, +0.21] |

Isotropic − pop gives the same picture (CA first turns: contested +1.88 [+0.95, +2.79], rest +0.31 [+0.08, +0.55]; second turns: contested
+1.55 [+0.63, +2.42], rest −0.02 [−0.22, +0.18]; MultiPref: contested −0.74 [−2.46, +0.97]).

Decisions by the frozen rules:

- **Practically meaningful on contested pairs (lower bound > +1 point): not met on any panel** (lower bounds +0.72, +0.63, −1.38).
- **Concentration (accuracy and log-likelihood both): not met on any panel.** On both Community Alignment panels the accuracy gain is concentrated on
  the contested fifth (contested − rest lower bound > 0 under the user bootstrap; the two-way intervals reach just below 0), but the log-likelihood
  gain is not (second turns: equal in both strata; first turns: larger on the *rest*). By the caveat fixed in §2 this is the mechanical kind of
  concentration: the adaptation shifts logits by a similar small amount everywhere, and a small shift changes the predicted choice only where the
  population margin is near zero.

What can be said (descriptive, replicated on first and second turns): on Community Alignment essentially all of TRV's accuracy gain sits on the
~22 % of comparisons where the population model is near chance (52–53 % → about 54 %); on the other ~78 % the accuracy gain is at most a few tenths
of a point. What cannot be said: that individual taste is a contested-item phenomenon, or that routing personalisation to contested items gives a
practically meaningful gain there — the gain is about +1.6 points with a lower bound below +1, and nothing on MultiPref.

## 6. Results — S14-1 (2026-11-11; pipeline job 15528, `s14_cf.py`, `s14_1.py`; rules of §1.5 applied as written)

The CF reference and the pipeline used identical support draws (seen-cell denominators identical for every fold, k, draw and rater). 1,000 raters;
991 have at least one comparable pair. PCA dimension selected for L2: 8 in every fold. Selected penalties (λ_text, λ_rater, λ_W): L1 DL
(100–300, 32–512, 10–100); L2 DL (1000–3000, 128–512, 10). Within-rater concordance in points, 95 % rater bootstrap; full tables in
`results/stage14_1.md`.

| k = 20 | estimate | rule |
|---|---|---|
| L0: CF own − μ (seen jokes; joke-mean level 66.3 %) | +1.39 [+1.12, +1.68] | **passes** (lower bound > +1) |
| L1: DL own − μ (seen jokes, item-identity encoding) | +0.14 [+0.09, +0.19] | (i) fails |
| L1: (DL own − μ) − (DF own − μ) | +0.16 [+0.13, +0.20] | (ii) met |
| L2: DL own − μ (held-out jokes; D level 60.2 %) | −0.06 [−0.11, −0.01] | (i) fails |
| L2: (DL own − μ) − (DF own − μ) | −0.00 [−0.04, +0.04] | (ii) fails |
| CF-text own − μ (held-out jokes) | −0.10 [−0.34, +0.13] | does not pass |
| ISO own − μ (held-out jokes) | −1.03 [−1.26, −0.80] | — |

**Reading R4** (L0 passes, L1 does not detect): the pipeline's DL model and adaptation recover about a tenth of the gain that a linear CF reference
obtains from the same 20 ratings on the same seen jokes (0.14 / 1.39). The DL negatives of Stages 2–10 therefore cannot be read as properties of the
domains until the implementation has been examined (Amendment 1).

Secondary (no rule): CF own − μ grows with k (+0.28, +0.73, +1.39, +2.64 at k = 5, 10, 20, 50); L1 DL own − μ +0.04, +0.08, +0.14, +0.29; L1 DL
own − other +0.31 [+0.25, +0.36]; L1b (L2 run on seen jokes) −0.00 [−0.02, +0.02]; log-likelihood ×100: L1 DL − DF +1.56 [+1.42, +1.71], L2 DL − DF
+0.92 [+0.70, +1.14], L2 DF − D +29.5 [+27.5, +31.7] (scale use dominates the likelihood, as on the paper's graded panels).

Two things the result says beyond the rule, both descriptive:

- **The "known taste" is itself modest on this endpoint.** With 20 ratings a standard CF model improves a rater's pairwise ordering of seen jokes by
  1.4 points over joke means (2.6 points with 50). Much of what makes Jester users differ is how high they rate overall, which within-rater
  concordance removes by construction.
- **No learner transferred taste to unseen jokes.** On held-out jokes all three learners (DL, CF-text, ISO) are at or below the text-predicted joke
  mean, and the text features predict joke means only weakly (60.1 % against 66.3 % for the true means). With 128 jokes and these frozen features the
  held-out-item setting has no demonstrated headroom, so L2 cannot separate domain from method here (§1.6, R3 logic), independently of the DL problem.

## Amendment 1 (2026-11-11, post hoc, after §6) — examining the DL implementation

Status: exploratory diagnosis, written before any diagnostic is run. Candidate causes read off the code, not yet tested:

1. *Optimisation.* DL is fitted by one L-BFGS call capped at 300 iterations, started at z = 0, w0 = 0 and W5 ~ 0.01·N(0, 1) — a saddle point of the
   low-rank term (the gradient with respect to W5 and w0 is zero at z = 0 and the gradient with respect to z is of order 0.01).
2. *Penalty grids.* λ_rater = 512 (the grid maximum) was selected in six of ten DL fits, and the adaptation strength chosen for new raters is 512–8192.
3. *Parametrisation.* DL puts the latent on the five category logits (softmax, 40 loadings per joke); CF puts it on the expected score.

A1-1 (fold 0, L1 configuration: identity encoding, rating-level validation; `s14_diag.py`, which executes the `factorised_rm.py` definitions unchanged
and instruments the fit):

- DL at the selected penalties and at weaker rater penalties (λ_rater ∈ {512, 32, 2}, λ_W ∈ {10, 1}), with 300 and 3000 L-BFGS iterations, and with
  a non-degenerate start (z ~ 0.1·N(0, 1), W5 ~ 0.1·N(0, 1)). Reported per fit: iterations used and whether the cap was hit, penalised training
  objective, validation log-likelihood, standard deviation of the latent term's contribution to the logits, and seen-joke concordance own − μ at
  k = 20 (support draw 0) over a grid of adaptation strengths (the best value over that grid is optimistic and is reported as such).
- The existing ordinal low-rank kind `L` (probit score x·β + (x·W + w0)·z, the CF structure) in the same configurations.
- Reference on the same fold and draw: CF own − μ.

Reading (descriptive): the cause is "optimisation" if more iterations or the non-degenerate start at the *same* penalties lower the training
objective and raise the gain materially; "grid" if only penalties outside the selected ones do; "parametrisation" if `L` recovers the gain and DL
does not under any setting; "unexplained" otherwise.

A1-2 (only if A1-1 identifies a fix): the fixed configuration becomes rung **L1-fix** and is run on all five folds through the unchanged selection
procedure and judged by the §1.5 rule. Because the fix is chosen after seeing fold 0, folds 1–4 are reported separately as the cleaner evidence, and
the whole rung is labelled post hoc. If L1-fix detects taste, the DL rows of the paper's real panels were produced by the unfixed fit and must be
re-run with the fix before they are interpreted; if no fix is found, those rows are reported as "not interpretable as domain evidence".

### A1-1 result (2026-11-11, job 15530; fold 0, k = 20, support draw 0; CF own − μ on this draw +1.33; `results/stage14_diag_part{0,1}.json`)

Gain = seen-joke concordance own − μ in points at adaptation strengths 0.5 / 8 / 128 / 2048 / 32768 (the pipeline's tuning chose 2048 in this fold).

| kind | λ_rater | λ_W | iterations (cap hit) | start | objective | val LL | latent sd | gain by adaptation strength |
|---|---|---|---|---|---|---|---|---|
| DL | 512 | 10 | 300 (yes) | pipeline | 75058.9 | −1.1306 | 1.47 | −2.01 / −1.05 / +0.38 / +0.12 / +0.07 |
| DL | 512 | 10 | 3000 (yes) | pipeline | 74662.0 | −1.1308 | 1.55 | −2.50 / −1.49 / +0.16 / +0.03 / +0.07 |
| DL | 512 | 10 | 3000 (yes) | random 0.1 | 74655.2 | −1.1311 | 1.56 | −2.47 / −1.43 / +0.20 / +0.03 / +0.06 |
| DL | 32 | 10 | 300 (yes) | pipeline | 70367.2 | −1.1461 | 1.85 | −1.80 / −0.54 / +0.67 / +0.18 / +0.03 |
| DL | 32 | 10 | 3000 (yes) | pipeline | 70318.8 | −1.1585 | 2.90 | −1.92 / −0.64 / +0.61 / +0.21 / +0.04 |
| DL | 2 | 1 | 3000 (yes) | random 0.1 | 66426.4 | −1.2515 | 4.61 | −2.01 / −0.84 / +0.86 / +0.29 / +0.02 |
| L | 512 | 10 | 300 (yes) | pipeline | 84223.4 | −1.2608 | 1.09 | −5.61 / −5.09 / −1.74 / +0.75 / +0.13 |
| L | 2 | 10 | 3000 (no, 2020) | pipeline | 78714.6 | −1.3776 | 1.67 | −5.77 / −2.92 / +0.68 / +0.15 / +0.02 |

(20 configurations in the JSON; the rows above span the range.) Reading against the three candidates:

- *Optimisation: not the cause.* The fit is not stuck at the saddle (latent term sd 1.5 logits). Ten times more iterations lower the objective by
  0.5 % at the selected penalties and do not raise the gain; the random start changes nothing.
- *Penalty grid: not sufficient.* Weaker rater penalties raise the best gain to 0.6–0.9 (optimistic: best over adaptation strengths) while making
  validation log-likelihood worse, and stay well below CF's +1.33.
- *Parametrisation: not the cause.* The ordinal CF-structured kind `L` does no better (best +0.75).
- So: **unexplained by the three candidates.** One pattern is common to every row: weak adaptation priors *lose* 1–6 points and strong ones gain
  almost nothing, with a narrow window between.

### A1-3 (written before running): is the adaptation prior misspecified?

Candidate 4, read off the code and the pattern above. `adapt()` shrinks a new rater's z isotropically toward the training-rater mean with one
strength. z is not standardised: its d = 8 directions carry both scale use (category offsets enter through the constant column w0; large
between-rater variance, strong signal per rating — DF − D is +29.5 ×100 nats) and taste (small variance, weak signal). One isotropic strength cannot
fit both: weak shrinkage overfits the low-variance directions, strong shrinkage removes them. The CF reference does not have this problem because
its loadings are scaled so that rater factors have unit variance and its intercept is unpenalised.

Test (fold 0, same draw, `DIAG_WHITEN=1 s14_diag.py`): after fitting, re-express the latent in whitened coordinates z = z̄ + L u, with L the
Cholesky factor of the training raters' covariance of z (the constant part moved into the text head; predictions for training raters unchanged —
checked numerically), then adapt u with an isotropic prior at strengths 0.125 / 0.5 / 2 / 8 / 32 (0.5 is the nominal Gaussian-prior value).
Configurations: DL (512, 10), (32, 10), (2, 10) at 300 iterations, (2, 1) at 3000; L (512, 10), (32, 10) at 300, (2, 10) at 3000.
Reading: candidate 4 is supported if the whitened prior at a strength within the grid's interior reaches at least half of the CF gain on this draw
(≥ +0.67) *and* exceeds the best unwhitened gain of the same fit; then "whitened adaptation prior" is the fix carried to A1-2.

### A1-3 result (2026-11-11, job 15532; `results/stage14_diag_whiten_part{0,1}.json`; training-rater predictions unchanged by the transform, max |Δ log p| < 1e-10)

Gain (points) by whitened adaptation strength 0.125 / 0.5 / 2 / 8 / 32; "before" = best unwhitened gain of the same fit (A1-1, coarser grid).

| kind | λ_rater | λ_W | val LL | whitened gain | before |
|---|---|---|---|---|---|
| DL | 512 | 10 | −1.1306 | +0.37 / +0.17 / +0.13 / +0.08 / +0.06 | +0.38 |
| DL | 32 | 10 | −1.1461 | +0.07 / **+0.86** / +0.61 / +0.28 / +0.12 | +0.67 |
| DL | 2 | 10 | −1.1843 | −0.64 / +0.58 / **+0.88** / +0.57 / +0.27 | +0.56 |
| DL | 2 | 1 | −1.2322 | −1.21 / −0.02 / +0.78 / +0.68 / +0.44 | +0.79 |
| L | 512 | 10 | −1.2608 | −0.84 / **+1.11** / +0.78 / +0.35 / +0.11 | +0.75 |
| L | 32 | 10 | −1.3124 | −2.52 / +0.08 / **+0.99** / +0.55 / +0.21 | +0.37 |
| L | 2 | 10 | −1.3776 | −3.77 / −1.15 / +0.72 / +0.58 / +0.27 | +0.68 |

Reading by the rule above: candidate 4 is **supported in four of seven fits** (bold: ≥ +0.67 at an interior strength and above the unwhitened best), with
gains of 0.86–1.11 points = 65–83 % of the CF gain on this draw (+1.33). It is *not* supported at the DL fit that validation log-likelihood selects
(λ_rater = 512: +0.37, at the grid edge, same as before), and the best strength is not the nominal 0.5 in every fit. Caveats: one fold, one support
draw, best-over-grid values (optimistic), and the whitened grid is finer than the unwhitened one, so part of the improvement may be grid resolution.
So the shortfall has two parts: (a) the isotropic prior on an unstandardised latent, and (b) for DL, penalties chosen by validation log-likelihood —
which rewards scale use (DL val LL −1.13 vs D −1.50) and is best at the heaviest rater penalty, where little ranking signal is left in the latent.

### A1-2 (written before running): rungs L1-fix-a and L1-fix-b, all five folds

Configuration as L1 (item-identity encoding, rating-level validation, seen jokes; same folds, support draws, k, bootstrap), models D, DF, DL, T0, L.

- **L1-fix-a** (`--whiten_adapt`): after each fit of DL / L the latent is re-expressed in whitened coordinates (A1-3); new raters are adapted with an
  isotropic prior on u. Selection unchanged: penalties by validation log-likelihood, adaptation strength by log-likelihood of pseudo-new training
  raters (the `--adapt_tune` procedure, now also for L), strength grid 2^{−5, −3, …, 7}.
- **L1-fix-b** (`--whiten_adapt --sel_conc 20`): as a, but the selection target is the endpoint. For DL / L the rater-side penalties (λ_rater, λ_W; same
  grids) are chosen by the seen-joke concordance of the pseudo-new training raters (the same 20 % inner split, `RandomState(3 + f)`; fit without them,
  whiten, adapt from 20 of their training-joke ratings, score their remaining training-joke ratings; best over the strength grid), and the adaptation
  strength of every adapted model (DF included) at each k by the same concordance. No test rater is used in any selection.

Rules, unchanged from §1.5 and applied to DL at k = 20: detects if (i) DL own − μ lower bound > +1 and (ii) (DL own − μ) − (DF own − μ) lower bound
> 0. Reported besides: L own − μ and own − other; the share of the CF gain recovered (point estimate ratio); log-likelihood DL − DF on the seen cell;
selected penalties and strengths per fold; **folds 1–4 separately** (fold 0's test raters were used in A1-1/A1-3; the choice of a criterion in b was
motivated by them).

Expectation, stated in advance: a will not move DL much in folds where validation log-likelihood picks λ_rater = 512; b should recover roughly
0.8–1.1 points (60–80 % of CF) for DL or L, which does **not** meet rule (i) as written (CF itself is +1.39 [+1.12, +1.68]).
Consequences: if a rung detects → reading R3 holds with that fix, and the DL rows of the paper's real panels must be re-run with it. If no rung
detects but b recovers at least half of the CF gain with a lower bound above zero → the paper states that the likelihood-selected pipeline
under-recovers ranking taste, reports the recovered share as the sensitivity of the corrected pipeline, and re-runs the real panels' DL rows with
rung b as a sensitivity analysis. Otherwise → the DL rows are "not interpretable as domain evidence".

### A1-2 result (2026-11-11, job 15533; `s14_fix.py` → `results/stage14_fix.{json,md}`; post hoc)

Regression check: rung a reproduces rung L1's D and DF rows exactly (max difference 0), so the code change touches only the latent models.
Seen jokes, k = 20, concordance own − μ in points [95 % rater bootstrap]; CF reference +1.39 [+1.12, +1.68] (folds 1–4: +1.48 [+1.17, +1.80]).

| rung | DL own − μ | share of CF | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF (×100) |
|---|---|---|---|---|---|---|---|---|
| L1 (original) | +0.14 [+0.09, +0.19] | 10 % | +0.16 [+0.13, +0.20] | +0.31 [+0.25, +0.36] | — | — | — | +1.56 [+1.42, +1.71] |
| L1-fix-a | +0.40 [+0.32, +0.48] | 29 % | +0.42 [+0.35, +0.50] | +0.72 [+0.63, +0.81] | +1.68 [+1.47, +1.90] | 121 % | +3.18 [+2.96, +3.42] | +2.16 [+1.94, +2.40] |
| L1-fix-b | +1.16 [+0.98, +1.34] | 83 % | +1.14 [+0.97, +1.33] | +2.44 [+2.26, +2.64] | +1.67 [+1.41, +1.94] | 120 % | +4.21 [+3.93, +4.49] | +17.33 [+15.89, +18.96] |
| folds 1–4, fix-a | +0.43 [+0.34, +0.53] | 29 % | +0.46 [+0.37, +0.54] | +0.79 [+0.68, +0.90] | +1.77 [+1.53, +2.00] | 119 % | +3.29 [+3.05, +3.54] | +2.10 [+1.85, +2.35] |
| folds 1–4, fix-b | +1.20 [+0.99, +1.39] | 81 % | +1.18 [+0.98, +1.38] | +2.52 [+2.30, +2.74] | +1.78 [+1.49, +2.08] | 120 % | +4.24 [+3.93, +4.55] | +20.95 [+19.14, +22.90] |

Other k (all folds): fix-b DL +0.43 / +0.75 / +2.08 and L +0.58 / +1.02 / +2.87 at k = 5 / 10 / 50, against CF +0.28 / +0.73 / +2.64.
Selections: validation log-likelihood chose λ_rater 32–512 for DL (rungs L1, a); pseudo-new-rater concordance chose 2–32 (rung b). Whitened
adaptation strengths 0.5–2 (interior of the grid) in every fold, against 512–2048 before.

Decisions.
- **Rule of §1.5 (DL): not met on any rung, narrowly on b** — (i) lower bound +0.98 (folds 1–4: +0.99) against the threshold +1; (ii) met on every
  rung. As pre-specified, this is "no rung detects".
- **Fallback criterion met**: rung b recovers 83 % of the CF gain with DL (lower bound well above zero), and the ordinal latent model L recovers
  about 120 % on both rungs — L's lower bound (+1.47 / +1.41) is above the +1 threshold and above CF's point estimate on rung a, i.e. under the
  *unchanged* likelihood selection. The rule was written for DL, so L is reported, not used to change the decision.
- The expectation written in advance was right for DL (a helps little; b reaches 0.8–1.1 short of the rule) and wrong for L under rung a, which I
  did not expect to exceed CF.
- **Reading: the original pipeline's failure on Jester (R4) was a property of the pipeline, not evidence about the domain.** Two defects: (1) an
  isotropic adaptation prior on an unstandardised latent — sufficient to explain L; (2) for DL, rater-side penalties chosen on *training raters'*
  validation likelihood, which is a poor proxy for adapted new raters on either endpoint: under rung b DL's new-rater log-likelihood gain over DF
  also rises from +2.2 to +17.3 ×100 nats.
- **Consequence for the paper**: every "low-rank latent adds nothing" row on the real panels used the defective configuration (selected λ_rater
  128–512 and adaptation strength 8192 = effectively switched off, on MultiPref, PRISM and DICES). Those rows are re-run with the corrected
  pipeline (A1-4) before any wording is kept.
- Limits: post hoc; fold 0's test raters informed the fixes (folds 1–4 agree); seen jokes only — the held-out-joke rung L2 is unchanged by this
  amendment (the CF-text reference found no transferable signal there); CF is one reference implementation, not a ceiling.

### A1-4 (written 2026-11-11 before running): the paper's held-out-item results with the corrected latent models

The Jester recovery is on seen jokes. The paper's statements are about held-out items, and every latent-model row there used the defective
configuration (tuned adaptation strength 8192 on MultiPref, PRISM, DICES and on the semi-synthetic positive-control panels t0 / t5 / t10; 512 on x10).
A1-4 re-runs them. Two runs per panel, five folds, `--concord --adapt_tune --perm_control`, evaluation on held-out items as in the paper:
- **a**: `--whiten_adapt` (penalties by validation log-likelihood, as in the paper);
- **b**: `--whiten_adapt --sel_conc 20` (`10` on Dorn). Because the evaluation is on held-out items, the inner fit of rung b excludes the validation
  items and the pseudo-new raters are scored on their validation-item ratings (new rater × new item); the adaptation strength of every adapted model
  is then tuned on the same cell. This cell is small (MultiPref: about 36 raters × 18 ratings); its number of informative pairs is stored and
  the rung is flagged where it is below 5,000.

**Part 1 — semi-synthetic positive control (Stage 3 panels, known injected content preferences, held-out items).** Panels `multipref_synth_t0`
(null), `_t5`, `_t10` (oracle direction gain 0 / +5.2 / +10.1 points); models D, DFs, DL, T0, F, L; k ∈ {0, 20, 50}. Endpoint as in §5.6 of the
draft: direction accuracy, own adapted parameters minus another test rater's, k = 20, rater bootstrap (seed 17, B = 2000). Stage 3's rule is kept:
a latent model **has power** at a strength if the lower bound exceeds +1 point; the null control is sound if its interval contains a value
within ±0.5 points of zero (if not, that model × rung is not used). Published DL rows: −0.10 (null), −0.02 (t5), +0.09 [−0.18, +0.36] (t10);
reference learner given the generating features: +3.1 (t5), +8.0 (t10).
- If a corrected latent model has power at t5 or t10: §5.6's "no evaluated method met the detection criterion" is restated as a property of the
  published configurations; the recovered share of the oracle gain is reported; and Part 2's MultiPref rows of that model × rung become the
  paper's informative ranking test.
- If none has power: §5.6 stands for the corrected pipeline as well, and Stage 14 is reported as "the correction recovers taste on seen items;
  transfer to unseen text remains undetected even where it is injected".

**Part 2 — real panels.** `multipref_overall` (models D, DF, DFs, DL, T0, F, L; k ∈ {0, 5, 10, 20, 50}), `prism`, `dices` (D, DF, DL, T0, F, L; same k),
`dorn_raters` (same models; k ∈ {0, 5, 10}). Buse–Weimer is left out: its features are an item-identity encoding (§0), so held-out snippets cannot
carry a text-mediated latent. Endpoints at k = 20 (Dorn: 10), same bootstrap: log-likelihood per rating, latent minus its scale-use comparator
(DL − DF; DL − DFs on MultiPref; L − F); concordance and direction accuracy, own − k = 0 and own − another rater's parameters, and the same for
the comparator.
Reading per panel, latent model and rung (all cells reported, no multiplicity correction): the paper's statement "the latent adds nothing beyond
scale-use offsets" **stands** if the log-likelihood difference has upper bound ≤ +0.5 ×100 nats (the H3 margin) and direction own − other has
upper bound < +1 point; it is **contradicted** if either has a lower bound > 0 with the latent ahead, in which case the size is reported and
"practically meaningful" requires a direction or concordance own − other lower bound > +1 point; otherwise **inconclusive**.
(Clarification, 2026-11-11, runs started but no result seen: for direction, "the latent ahead" means its own − other lower bound > 0 *and* its
own − other exceeds the comparator's own − other in point estimate; the published MultiPref row had +0.30 for DL against +0.32 for the offsets.)

Expectation, stated in advance: the corrected latent models detect t10 and possibly t5, well below the reference learner; on the real panels the
log-likelihood moves by a few hundredths of a nat at most and ranking gains stay below one point. I hold this weakly — the A1-2 expectation was
wrong for L. The original rows stay in the analysis log either way. Limits: post hoc; one synthetic draw; rung b's selection cell is small.

### A1-4 result, Part 1 and Part 2 without PRISM (2026-11-12; job 15534; `s14_real.py` → `results/stage14_real.{json,md}`; post hoc)

Run notes: 61 of 70 runs finished; nine PRISM runs were killed for memory (16 processes in 24 GB) and were resubmitted unchanged with 48 GB (job
15556); PRISM is reported separately below. `s14_real.py` reproduces the published rows from the original runs (synthetic DL −0.10 / −0.02 /
+0.09; MultiPref DL +0.30, offsets +0.32), and DF's rows are identical in the original and the rung-a runs.

**Part 1 — semi-synthetic positive control** (direction accuracy in points, own − another rater's parameters, k = 20, 209 new raters):

| panel (oracle gain) | published DL | rung a DL | rung a L | rung b DL | rung b L |
|---|---|---|---|---|---|
| null (0) | −0.10 [−0.38, +0.17] | +0.01 [−0.25, +0.27] | +0.04 [−0.11, +0.19] | +0.02 [−0.35, +0.37] | −0.22 [−0.63, +0.18] |
| t5 (+5.2) | −0.02 [−0.28, +0.26] | −0.06 [−0.29, +0.19] | +0.10 [−0.22, +0.41] | +0.15 [−0.14, +0.46] | +0.43 [−0.03, +0.88] |
| t10 (+10.1) | +0.09 [−0.18, +0.36] | +0.62 [+0.17, +1.06] | **+2.82 [+2.02, +3.63]** | **+2.28 [+1.48, +3.12]** | **+3.35 [+2.51, +4.21]** |

- Null control sound for every model × rung. **Power (lower bound > +1) at t10**: L on both rungs, DL on rung b; **no power at t5** for any model
  or rung. At k = 50 (180 raters), t10: rung a DL +1.19 [+0.51, +1.89], L +3.56; rung b DL +3.73, L +3.65; t5: at most +0.59 [+0.02, +1.14] (L, a).
- The scale-use comparators stay at zero on the same contrast (DFs −0.07 / −0.15, F +0.42 / +0.53 at t10), so the gain is content-specific.
- What the detection is worth: the reference learner given the generating features recovers +8.0 of the +10.1; the corrected latent models recover
  about 2.3–3.4 on own − other. Against **no personalisation** (the same model at the prior mean) the gain is +0.2 to +0.8 with intervals that
  include zero (rung a DL +0.34 [−0.11, +0.81], L +0.84 [−0.12, +1.80]; rung b DL +0.21, L +0.82), and the log-likelihood does not beat the
  scale-use model (rung a DL − DFs +0.26 [−0.12, +0.65], L − F −0.45 [−1.90, +0.88] ×100). So the parameters adapted from 20 ratings carry the
  rater's content preference (another rater's parameters do worse) but do not yet turn it into a net ranking gain.
- Decision under the pre-written rule: a corrected latent model has power at t10 → §5.6's "no evaluated method met the detection criterion" holds
  only at the pre-specified strengths (t2, t5) and for the published configuration at t10; the corrected rows replace the DL row; the detection
  limit of the corrected pipeline lies between an oracle gain of +5 and +10 points; Part 2's MultiPref rows are the paper's informative test.

**Part 2 — real panels** (k = 20; Dorn k = 10; ×100 nats per rating or points). Comparator: DFs on MultiPref, DF elsewhere (DL); F (L).

| panel | rung, model | LL latent − comparator | direction own − other: latent | comparator | latent − comparator | concordance own − other: latent | latent − comparator | rule |
|---|---|---|---|---|---|---|---|---|
| MultiPref | published DL | −0.45 [−0.96, +0.00] | +0.30 [−0.00, +0.60] | +0.32 | −0.02 [−0.34, +0.29] | — | — | stands |
| | a DL | +0.05 [−0.49, +0.52] | +0.19 [−0.11, +0.50] | +0.32 | −0.14 [−0.48, +0.22] | +0.13 [−0.01, +0.28] | −0.03 [−0.11, +0.06] | inconclusive (LL upper bound +0.52 against +0.5) |
| | a L | −3.05 [−4.91, −1.55] | −0.12 [−0.45, +0.20] | −0.37 | +0.25 [−0.10, +0.62] | −0.01 [−0.04, +0.02] | −0.01 | stands |
| | b DL | −12.27 [−16.02, −8.51] | −0.16 [−0.42, +0.10] | +0.14 | −0.30 [−0.58, −0.01] | +0.10 [−0.02, +0.21] | +0.01 | stands |
| | b L | −0.94 [−3.72, +1.33] | −0.16 [−0.63, +0.33] | −0.17 | +0.02 [−0.51, +0.55] | −0.01 [−0.03, +0.01] | −0.01 | inconclusive (LL upper bound) |
| DICES | a DL | −1.11 [−1.81, −0.47] | +9.44 [+7.34, +11.71] | +9.97 | −0.53 [−0.94, −0.11] | +0.06 [−0.13, +0.26] | +0.06 | inconclusive |
| | a L | −0.19 [−0.99, +0.64] | +10.01 [+7.94, +12.23] | +8.54 | +1.47 [+0.73, +2.24] | **+0.50 [+0.09, +0.96]** | +0.50 | contradicted, practically meaningful |
| | b DL | −19.30 [−26.64, −12.52] | +5.61 | +6.48 | −0.87 [−2.92, +1.17] | +0.04 [−0.07, +0.14] | +0.05 | inconclusive |
| | b L | −163.97 [−219.54, −112.69] | +6.35 | +9.97 | −3.62 [−5.10, −2.18] | +0.48 [+0.07, +0.90] | +0.48 | inconclusive |
| Dorn | published = a DL | −3.99 [−4.91, −3.06] | 0 (latent switched off by the selected penalties) | +8.70 | −8.70 | 0 | −0.09 | stands |
| | a L | +3.74 [+2.73, +4.62] | +11.24 [+10.32, +12.14] | +10.87 | +0.37 [+0.09, +0.64] | 0.00 (exactly) | 0.00 | contradicted, practically meaningful |
| | b DL | −15.16 [−16.67, −13.64] | +3.61 | +4.26 | −0.65 [−1.10, −0.19] | +0.23 [−0.14, +0.59] | +0.20 | inconclusive |
| | b L | −25.68 [−29.85, −22.26] | +7.99 | +11.61 | −3.62 [−4.33, −2.97] | +0.13 [−0.35, +0.61] | +0.13 | inconclusive |

Readings.
1. **MultiPref (the paper's primary panel): no content taste beyond scale-use offsets with the corrected models.** Own − other direction is
   between −0.16 and +0.19 points with upper bounds ≤ +0.50 for models that return +2.3 to +3.4 on the same contrast when a +10-point preference is
   injected, and the latent is never ahead of the three-number style model in likelihood (rung a DL − DFs +0.05 [−0.49, +0.52]; published −0.45).
   The two "inconclusive" labels come from likelihood upper bounds of +0.52 and +1.33 against the +0.5 margin, not from any signal.
2. **The rule's direction clause is ill-posed on single-response panels** (DICES, Dorn, PRISM): direction there is "above or below the scale
   midpoint", which a rater's shift alone moves — the scale-use comparators gain +8.5 to +11.6 points on the same contrast. This was a flaw in the
   rule I wrote, visible only after the fact; the as-written outcomes are kept in the table, and the reading below uses the latent − comparator
   column and concordance (within-rater ranking, which a shift cannot change). Post hoc.
   - Dorn, rung a L: likelihood +3.74 over F and +1.15 [+0.29, +2.04] over DF, direction +0.37 [+0.09, +0.64] over F, but concordance own − other
     is exactly zero: the selected fit uses the latent only as a rater shift. A better-regularised scale-use model, not taste.
   - DICES, L: direction +1.47 [+0.73, +2.24] over F but equal to DF's (+10.01 against +9.97), and likelihood below DF (−4.23 [−5.56, −2.96]).
     Concordance own − other +0.50 [+0.09, +0.96] on rung a and +0.48 [+0.07, +0.90] on rung b, with own − k = 0 at +0.30 [−0.04, +0.65] and
     −0.31 [−0.86, +0.18]. Half a point with a lower bound just above zero, one of some twenty cells examined without correction: recorded as a
     lead, not as a finding.
3. **Rung b is not a usable recipe on these panels.** Choosing rater-side penalties by concordance on a small new-rater × new-item cell costs
   0.12–1.64 nats per rating (MultiPref DL −12.3, DICES L −164, Dorn L −25.7 ×100) and returns no ranking gain. On Jester it improved both; there
   the selection cell had the seen-joke signal to find. The correction to carry into the paper is **rung a** (whitened adaptation prior,
   likelihood selection); rung b is reported as a sensitivity analysis whose likelihood must be shown next to its ranking numbers.
4. Sizes of rung b's selection cell: 7,000–13,000 informative pairs on MultiPref and the synthetic panels, 6,400–9,700 on DICES, 800–1,300 on Dorn
   (flagged).

### A1-4 result, Part 2: PRISM (2026-11-12; job 15557; `s14_real.py` → `results/stage14_real.{json,md}`; post hoc)

Run notes: job 15556 (48 GB) could not start while other users held the node's memory and was replaced by job 15557 (12 CPUs, 32 GB, four runs
in parallel, rung a first; commands unchanged). All ten runs finished (fold 4 of rung a came from job 15534); peak memory 29.99 GB of 32 GB, no
process killed, no traceback. 941 new raters at k = 20.

| panel | rung, model | LL latent − comparator | direction own − other: latent | comparator | latent − comparator | concordance own − other: latent | latent − comparator | rule |
|---|---|---|---|---|---|---|---|---|
| PRISM | a DL | **+0.37 [+0.08, +0.65]** | +1.59 [+1.12, +2.06] | +1.26 | +0.33 [+0.18, +0.49] | −0.06 [−0.26, +0.13] | −0.01 [−0.10, +0.08] | contradicted, practically meaningful |
| | a L | −1.81 [−2.52, −1.12] | +2.68 [+2.10, +3.30] | +1.55 | +1.13 [+0.75, +1.49] | +0.01 [−0.04, +0.07] | +0.01 | contradicted, practically meaningful |
| | b DL | −3.07 [−3.93, −2.17] | +0.30 [+0.10, +0.52] | +0.53 | −0.24 [−0.54, +0.05] | +0.16 [+0.02, +0.30] | +0.21 [+0.06, +0.36] | stands |
| | b L | −4.20 [−6.56, −1.97] | +1.31 [+0.85, +1.76] | +3.30 | −1.98 [−2.62, −1.39] | +0.35 [+0.05, +0.65] | +0.35 | inconclusive |

Against the softmax offsets DF (cross-family for L), LL ×100: a DL +0.37 [+0.08, +0.65]; a L −4.33 [−5.36, −3.26]; b DL −3.07; b L −9.27.
LL over the text-only model: a DL +8.24 [+7.16, +9.33], DF +7.87 [+6.85, +8.91]. By k (rung a, DF − DL in nats per rating, both tuned):
k = 5 −0.0031 [−0.0058, −0.0005]; k = 10 −0.0053 [−0.0083, −0.0025]; k = 20 −0.0037 [−0.0065, −0.0008]; k = 50 +0.0087 [−0.0019, +0.0201]
(139 raters). First run: k = 20 −0.0013 [−0.0060, +0.0034].

Readings.
1. **Rule as written: rung a DL contradicts "nothing beyond the scale-use offsets" in likelihood** (lower bound above zero). The size is 0.0037
   nats per rating, about 5 % of the offsets' own gain over the text-only model (+0.079), at k = 5–20; not at k = 50.
2. **It is not a ranking gain.** The "practically meaningful" labels come from the direction clause, which is ill-posed on this panel (reading 2
   of the previous section: a rater shift alone moves good-vs-bad around the midpoint; DF alone has +1.26, F +1.55). Within-rater concordance,
   which a shift cannot change, is at zero for both latents under rung a (DL own − other −0.06 [−0.26, +0.13], latent − comparator −0.01
   [−0.10, +0.08]; L +0.01 [−0.04, +0.07]) and slightly negative against no adaptation for DL (−0.21 [−0.37, −0.05]). The latent's extra
   own − other direction over its comparator (DL +0.33 [+0.18, +0.49], L +1.13 [+0.75, +1.49]) is not significant against no adaptation
   (own − k = 0: DL +0.39 [−0.04, +0.86], L +0.47 [−0.07, +1.09]). So on PRISM the corrected softmax latent buys a small, significant
   improvement in predicted rating distributions that does not show up as better ordering of a rater's responses. Post hoc reading.
3. The ordinal latent stays below its own comparator (−1.81) and below DF (−4.33) in likelihood.
4. Rung b lowers likelihood here too (DL −3.07, L −4.20 against the comparators; selection cells of 3,294–4,964 informative pairs, all under
   the 5,000 flag). Its concordance own − other is +0.16 [+0.02, +0.30] (DL) and +0.35 [+0.05, +0.65] (L), with own − k = 0 at +0.05
   [−0.11, +0.22] and −0.08 [−0.37, +0.21]: no gain over no adaptation. Across the four real panels rung b's latent is below its scale-use
   comparator in seven of eight panel × latent cells (by 0.03–1.64 nats per rating; exception: MultiPref L). Rung a remains the adopted correction.
5. Tuning at k = 50 on PRISM is unstable for every model (139 qualifying test raters): the selected strength is large in most folds (rung-a runs: DF 524288
   in two folds and 32 in one; DL 128 in three folds, in whitened units), as it already was in the first run (tuned DF − D +0.043 against +0.107 with
   the training-rater prior). Rung a DL − D at k = 50 is +0.035 [+0.010, +0.061] (first run +0.105); the like-for-like DF − DL is the +0.0087
   above.
6. Consequences for the paper: §5.2's PRISM cell becomes DF − DL = −0.004 [−0.007, −0.001] (latent ahead; H3r not non-inferior, now with an
   interval excluding zero) and DICES +0.011 [+0.005, +0.018]; the statement that the latent adds nothing beyond scale use is restricted to
   MultiPref and to ranking; Figure 1's DL series is redrawn from the rung-a runs.


=== (C1) results/stage14_fix.md ===
# Stage 14 Amendment 1, A1-2 — Jester, seen jokes: fixed rungs (post hoc; concordance own − μ in points, 95 % rater bootstrap; LL ×100 nats per rating)

Regression (rung a vs L1, D / DF rows; max |difference| in summed per-rater units): {'D_sconc': 0.0, 'DF_sconc': 0.0, 'DF_sll': 0.0, 'D_ll': 0.0, 'DF_ll': 0.0, 'sconc_den': 0.0}

## All five folds

**k = 5** — CF reference own − μ: +0.28 [+0.17, +0.38]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.04 [+0.01, +0.08] | 15 % | -0.01 [-0.03, +0.02] | +0.05 [+0.03, +0.08] | +0.15 [+0.11, +0.18] | — | — | — | +2.55 [+2.15, +2.95] |
| L1-fix-a | +0.15 [+0.11, +0.20] | 56 % | -0.01 [-0.03, +0.02] | +0.16 [+0.13, +0.20] | +0.31 [+0.26, +0.36] | +0.58 [+0.49, +0.66] | 208 % | +1.05 [+0.95, +1.15] | +3.03 [+2.50, +3.55] |
| L1-fix-b | +0.43 [+0.34, +0.53] | 157 % | +0.00 [-0.01, +0.02] | +0.43 [+0.34, +0.52] | +0.97 [+0.87, +1.07] | +0.58 [+0.47, +0.69] | 211 % | +1.36 [+1.24, +1.49] | +16.67 [+14.79, +18.61] |

**k = 10** — CF reference own − μ: +0.73 [+0.54, +0.93]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.08 [+0.04, +0.12] | 11 % | -0.02 [-0.05, +0.01] | +0.10 [+0.08, +0.13] | +0.19 [+0.14, +0.23] | — | — | — | +2.02 [+1.79, +2.27] |
| L1-fix-a | +0.24 [+0.18, +0.30] | 33 % | -0.02 [-0.05, +0.01] | +0.27 [+0.22, +0.32] | +0.46 [+0.39, +0.54] | +1.02 [+0.87, +1.16] | 139 % | +1.87 [+1.70, +2.04] | +2.58 [+2.25, +2.92] |
| L1-fix-b | +0.75 [+0.62, +0.88] | 103 % | +0.00 [-0.01, +0.02] | +0.75 [+0.62, +0.88] | +1.61 [+1.46, +1.76] | +1.02 [+0.83, +1.22] | 140 % | +2.61 [+2.39, +2.83] | +19.23 [+17.37, +21.27] |

**k = 20** — CF reference own − μ: +1.39 [+1.12, +1.68]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.14 [+0.09, +0.19] | 10 % | -0.02 [-0.06, +0.02] | +0.16 [+0.13, +0.20] | +0.31 [+0.25, +0.36] | — | — | — | +1.56 [+1.42, +1.71] |
| L1-fix-a | +0.40 [+0.32, +0.48] | 29 % | -0.02 [-0.06, +0.02] | +0.42 [+0.35, +0.50] | +0.72 [+0.63, +0.81] | +1.68 [+1.47, +1.90] | 121 % | +3.18 [+2.96, +3.42] | +2.16 [+1.94, +2.40] |
| L1-fix-b | +1.16 [+0.98, +1.34] | 83 % | +0.01 [-0.01, +0.04] | +1.14 [+0.97, +1.33] | +2.44 [+2.26, +2.64] | +1.67 [+1.41, +1.94] | 120 % | +4.21 [+3.93, +4.49] | +17.33 [+15.89, +18.96] |

**k = 50** — CF reference own − μ: +2.64 [+2.24, +3.04]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.29 [+0.22, +0.37] | 11 % | -0.05 [-0.10, -0.00] | +0.34 [+0.28, +0.40] | +0.51 [+0.43, +0.60] | — | — | — | +1.27 [+1.17, +1.38] |
| L1-fix-a | +1.00 [+0.84, +1.18] | 38 % | -0.05 [-0.10, -0.00] | +1.06 [+0.90, +1.22] | +1.83 [+1.65, +2.03] | +2.94 [+2.59, +3.27] | 111 % | +5.65 [+5.29, +6.01] | +2.40 [+2.18, +2.60] |
| L1-fix-b | +2.08 [+1.76, +2.40] | 79 % | +0.01 [-0.02, +0.04] | +2.07 [+1.75, +2.39] | +4.97 [+4.62, +5.31] | +2.87 [+2.49, +3.26] | 109 % | +6.53 [+6.14, +6.93] | +18.63 [+16.97, +20.45] |

Rules at k = 20: L1: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': False}; L1-fix-a: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': False, 'L': True}; L1-fix-b: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': True, 'L': True}

## Folds 1–4 (not used in the diagnosis)

**k = 5** — CF reference own − μ: +0.36 [+0.24, +0.47]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.04 [+0.00, +0.08] | 12 % | -0.01 [-0.04, +0.02] | +0.05 [+0.02, +0.08] | +0.15 [+0.11, +0.20] | — | — | — | +2.39 [+1.92, +2.87] |
| L1-fix-a | +0.17 [+0.12, +0.22] | 48 % | -0.01 [-0.04, +0.02] | +0.18 [+0.14, +0.23] | +0.34 [+0.28, +0.40] | +0.61 [+0.52, +0.70] | 171 % | +1.11 [+1.00, +1.21] | +2.77 [+2.19, +3.36] |
| L1-fix-b | +0.42 [+0.32, +0.53] | 118 % | +0.00 [-0.01, +0.02] | +0.42 [+0.32, +0.52] | +0.99 [+0.87, +1.09] | +0.64 [+0.52, +0.77] | 179 % | +1.58 [+1.44, +1.72] | +15.03 [+13.06, +17.06] |

**k = 10** — CF reference own − μ: +0.81 [+0.60, +1.03]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.09 [+0.04, +0.14] | 11 % | -0.02 [-0.06, +0.01] | +0.11 [+0.07, +0.14] | +0.19 [+0.14, +0.25] | — | — | — | +1.91 [+1.63, +2.19] |
| L1-fix-a | +0.27 [+0.20, +0.35] | 34 % | -0.02 [-0.06, +0.01] | +0.30 [+0.24, +0.36] | +0.51 [+0.42, +0.60] | +1.07 [+0.91, +1.22] | 131 % | +1.96 [+1.78, +2.15] | +2.43 [+2.06, +2.80] |
| L1-fix-b | +0.77 [+0.62, +0.91] | 95 % | +0.00 [-0.02, +0.03] | +0.77 [+0.62, +0.91] | +1.69 [+1.52, +1.85] | +1.11 [+0.90, +1.32] | 136 % | +2.67 [+2.43, +2.91] | +16.62 [+14.71, +18.62] |

**k = 20** — CF reference own − μ: +1.48 [+1.17, +1.80]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.15 [+0.09, +0.21] | 10 % | -0.03 [-0.07, +0.02] | +0.18 [+0.14, +0.22] | +0.33 [+0.26, +0.40] | — | — | — | +1.50 [+1.33, +1.67] |
| L1-fix-a | +0.43 [+0.34, +0.53] | 29 % | -0.03 [-0.07, +0.02] | +0.46 [+0.37, +0.54] | +0.79 [+0.68, +0.90] | +1.77 [+1.53, +2.00] | 119 % | +3.29 [+3.05, +3.54] | +2.10 [+1.85, +2.35] |
| L1-fix-b | +1.20 [+0.99, +1.39] | 81 % | +0.02 [-0.00, +0.04] | +1.18 [+0.98, +1.38] | +2.52 [+2.30, +2.74] | +1.78 [+1.49, +2.08] | 120 % | +4.24 [+3.93, +4.55] | +20.95 [+19.14, +22.90] |

**k = 50** — CF reference own − μ: +2.84 [+2.41, +3.28]

| rung | DL own − μ | share of CF | DF own − μ | DL − DF | DL own − other | L own − μ | share of CF | L own − other | LL DL − DF |
|---|---|---|---|---|---|---|---|---|---|
| L1 | +0.33 [+0.24, +0.42] | 12 % | -0.05 [-0.10, +0.01] | +0.38 [+0.31, +0.44] | +0.57 [+0.47, +0.67] | — | — | — | +1.26 [+1.14, +1.39] |
| L1-fix-a | +1.15 [+0.94, +1.35] | 41 % | -0.05 [-0.10, +0.01] | +1.20 [+1.01, +1.39] | +2.09 [+1.86, +2.31] | +3.11 [+2.72, +3.49] | 109 % | +5.89 [+5.49, +6.30] | +2.46 [+2.22, +2.71] |
| L1-fix-b | +2.21 [+1.84, +2.59] | 78 % | +0.02 [-0.02, +0.05] | +2.19 [+1.83, +2.58] | +5.33 [+4.93, +5.72] | +3.08 [+2.67, +3.51] | 108 % | +6.72 [+6.28, +7.16] | +21.83 [+19.86, +23.95] |

Rules at k = 20: L1: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': False}; L1-fix-a: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': False, 'L': True}; L1-fix-b: (i) not met, (ii) met, half of CF with lower bound > 0: {'DL': True, 'L': True}

## Selected penalties (λ_text, λ_rater, λ_W) and adaptation strength at k = 20

| rung | fold | DL | DL strength | L | L strength | DF strength |
|---|---|---|---|---|---|---|
| L1 | 0 | [100, 512, 10] | 2048 | — | — | 0.5 |
| L1 | 1 | [300, 512, 10] | 2048 | — | — | 0.5 |
| L1 | 2 | [300, 128, 10] | 512 | — | — | 0.5 |
| L1 | 3 | [300, 32, 100] | 512 | — | — | 0.5 |
| L1 | 4 | [300, 32, 100] | 512 | — | — | 0.5 |
| L1-fix-a | 0 | [100, 512, 10] | 0.5 | [10, 128, 100] | 0.5 | 0.5 |
| L1-fix-a | 1 | [300, 512, 10] | 0.5 | [300, 128, 100] | 0.5 | 0.5 |
| L1-fix-a | 2 | [300, 128, 10] | 0.5 | [1000, 128, 100] | 0.5 | 0.5 |
| L1-fix-a | 3 | [300, 32, 100] | 2 | [1000, 128, 100] | 0.5 | 0.5 |
| L1-fix-a | 4 | [300, 32, 100] | 2 | [1000, 128, 100] | 0.5 | 0.5 |
| L1-fix-b | 0 | [100, 2, 10] | 2 | [10, 32, 100] | 0.5 | 0.5 |
| L1-fix-b | 1 | [300, 2, 10] | 2 | [300, 32, 100] | 0.5 | 32 |
| L1-fix-b | 2 | [300, 8, 1] | 2 | [1000, 8, 1000] | 0.5 | 8 |
| L1-fix-b | 3 | [300, 8, 1] | 2 | [1000, 8, 1000] | 0.5 | 2 |
| L1-fix-b | 4 | [300, 32, 1] | 2 | [1000, 512, 10] | 0.5 | 8 |


=== (C2) results/stage14_real.md ===
# Stage 14 Amendment 1, A1-4 — held-out items with the corrected latent models (post hoc; points or ×100 nats per rating, 95 % rater bootstrap)

## Part 1 — semi-synthetic positive control (MultiPref; direction accuracy, own − another rater's parameters, k = 20)

| panel | oracle gain | rung | folds | DL own − other | L own − other | DFs own − other | F own − other | DL − DFs | L − F | power (DL / L) |
|---|---|---|---|---|---|---|---|---|---|---|
| t0 | +0.0 | published | 5 | -0.10 [-0.38, +0.17] | — | -0.07 [-0.34, +0.19] | — | -0.03 [-0.25, +0.18] | — | no / —; null sound: {'DL': True} |
| t0 | +0.0 | a | 5 | +0.01 [-0.25, +0.27] | +0.04 [-0.11, +0.19] | -0.07 [-0.34, +0.19] | -0.22 [-0.56, +0.13] | +0.08 [-0.13, +0.28] | +0.26 [-0.06, +0.58] | no / no; null sound: {'DL': True, 'L': True} |
| t0 | +0.0 | b | 5 | +0.02 [-0.35, +0.37] | -0.22 [-0.63, +0.18] | -0.05 [-0.33, +0.21] | -0.20 [-0.86, +0.44] | +0.07 [-0.38, +0.49] | -0.02 [-0.67, +0.60] | no / no; null sound: {'DL': True, 'L': True} |
| t5 | +5.2 | published | 5 | -0.02 [-0.28, +0.26] | — | -0.04 [-0.26, +0.19] | — | +0.02 [-0.22, +0.26] | — | no / — |
| t5 | +5.2 | a | 5 | -0.06 [-0.29, +0.19] | +0.10 [-0.22, +0.41] | -0.04 [-0.26, +0.19] | -0.04 [-0.42, +0.33] | -0.02 [-0.22, +0.17] | +0.14 [-0.24, +0.49] | no / no |
| t5 | +5.2 | b | 5 | +0.15 [-0.14, +0.46] | +0.43 [-0.03, +0.88] | +0.05 [-0.00, +0.11] | -0.01 [-0.69, +0.63] | +0.10 [-0.21, +0.42] | +0.44 [-0.31, +1.19] | no / no |
| t10 | +10.1 | published | 5 | +0.09 [-0.18, +0.36] | — | -0.07 [-0.29, +0.17] | — | +0.16 [-0.09, +0.43] | — | no / — |
| t10 | +10.1 | a | 5 | +0.62 [+0.17, +1.06] | +2.82 [+2.02, +3.63] | -0.07 [-0.29, +0.17] | +0.42 [-0.13, +0.92] | +0.69 [+0.24, +1.14] | +2.41 [+1.57, +3.25] | no / yes |
| t10 | +10.1 | b | 5 | +2.28 [+1.48, +3.12] | +3.35 [+2.51, +4.21] | -0.15 [-0.39, +0.10] | +0.53 [-0.30, +1.34] | +2.43 [+1.56, +3.35] | +2.82 [+1.75, +3.87] | yes / yes |

## Part 2 — real panels (k = 20; Dorn k = 10)

**multipref_overall**

| rung | folds | latent | LL latent − comparator | LL latent − D | LL comparator − D | direction own − other | comparator's | latent − comparator | direction own − k0 | concordance own − other | comparator's | latent − comparator | concordance own − k0 | reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| published | 5 | DL (vs DFs) | -0.45 [-0.96, +0.00] | +9.52 [+6.88, +12.34] | +9.97 [+7.37, +12.86] | +0.30 [-0.00, +0.60] | +0.32 [+0.06, +0.58] | -0.02 [-0.34, +0.29] | -0.11 [-0.51, +0.29] | — | — | — | — | stands |
| a | 5 | DL (vs DFs) | +0.05 [-0.49, +0.52] | +10.02 [+7.64, +12.76] | +9.97 [+7.37, +12.86] | +0.19 [-0.11, +0.50] | +0.32 [+0.06, +0.58] | -0.14 [-0.48, +0.22] | -0.32 [-0.69, +0.07] | +0.13 [-0.01, +0.28] | +0.16 [+0.03, +0.29] | -0.03 [-0.11, +0.06] | +0.06 [-0.06, +0.19] | inconclusive |
| a | 5 | L (vs F) | -3.05 [-4.91, -1.55] | -6.47 [-7.54, -5.29] | -3.42 [-5.39, -1.13] | -0.12 [-0.45, +0.20] | -0.37 [-0.81, +0.08] | +0.25 [-0.10, +0.62] | -0.57 [-0.93, -0.24] | -0.01 [-0.04, +0.02] | +0.00 [+0.00, +0.00] | -0.01 [-0.04, +0.02] | -0.01 [-0.04, +0.02] | stands |
| b | 5 | DL (vs DFs) | -12.27 [-16.02, -8.51] | -8.60 [-12.93, -4.08] | +3.68 [+2.21, +5.29] | -0.16 [-0.42, +0.10] | +0.14 [-0.04, +0.32] | -0.30 [-0.58, -0.01] | -0.33 [-0.64, +0.01] | +0.10 [-0.02, +0.21] | +0.09 [+0.02, +0.17] | +0.01 [-0.10, +0.11] | +0.04 [-0.06, +0.15] | stands |
| b | 5 | L (vs F) | -0.94 [-3.72, +1.33] | -6.96 [-8.11, -5.65] | -6.02 [-8.68, -2.98] | -0.16 [-0.63, +0.33] | -0.17 [-0.90, +0.54] | +0.02 [-0.51, +0.55] | -1.09 [-1.59, -0.59] | -0.01 [-0.03, +0.01] | +0.00 [+0.00, +0.00] | -0.01 [-0.03, +0.01] | +0.00 [-0.02, +0.02] | inconclusive |

Latent against the softmax scale-use offsets DF (cross-family for L), log-likelihood ×100: a DL: +2.00 [+1.60, +2.41]; a L: -14.49 [-17.04, -11.99]; b DL: -11.65 [-15.67, -7.63]; b L: -10.02 [-11.66, -8.25]

**dices**

| rung | folds | latent | LL latent − comparator | LL latent − D | LL comparator − D | direction own − other | comparator's | latent − comparator | direction own − k0 | concordance own − other | comparator's | latent − comparator | concordance own − k0 | reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | 5 | DL (vs DF) | -1.11 [-1.81, -0.47] | +7.77 [+5.05, +10.83] | +8.88 [+6.48, +11.64] | +9.44 [+7.34, +11.71] | +9.97 [+7.83, +12.22] | -0.53 [-0.94, -0.11] | +4.05 [+1.89, +6.61] | +0.06 [-0.13, +0.26] | -0.00 [-0.04, +0.03] | +0.06 [-0.12, +0.26] | +0.02 [-0.14, +0.19] | inconclusive |
| a | 5 | L (vs F) | -0.19 [-0.99, +0.64] | +4.66 [+2.56, +7.12] | +4.85 [+2.73, +7.22] | +10.01 [+7.94, +12.23] | +8.54 [+6.61, +10.69] | +1.47 [+0.73, +2.24] | +4.63 [+2.39, +7.23] | +0.50 [+0.09, +0.96] | +0.00 [+0.00, +0.00] | +0.50 [+0.09, +0.96] | +0.30 [-0.04, +0.65] | contradicted, practically meaningful |
| b | 5 | DL (vs DF) | -19.30 [-26.64, -12.52] | -13.34 [-19.79, -6.87] | +5.96 [+3.63, +8.68] | +5.61 [+3.76, +7.63] | +6.48 [+4.49, +8.72] | -0.87 [-2.92, +1.17] | +2.56 [+1.00, +4.60] | +0.04 [-0.07, +0.14] | -0.01 [-0.04, +0.02] | +0.05 [-0.06, +0.16] | +0.01 [-0.08, +0.09] | inconclusive |
| b | 5 | L (vs F) | -163.97 [-219.54, -112.69] | -165.60 [-220.09, -114.43] | -1.63 [-4.95, +1.75] | +6.35 [+4.99, +7.71] | +9.97 [+7.87, +12.27] | -3.62 [-5.10, -2.18] | +3.28 [+1.91, +4.80] | +0.48 [+0.07, +0.90] | +0.00 [+0.00, +0.00] | +0.48 [+0.07, +0.90] | -0.31 [-0.86, +0.18] | inconclusive |

Latent against the softmax scale-use offsets DF (cross-family for L), log-likelihood ×100: a DL: -1.11 [-1.81, -0.47]; a L: -4.23 [-5.56, -2.96]; b DL: -19.30 [-26.64, -12.52]; b L: -171.56 [-226.42, -119.90]

**prism**

| rung | folds | latent | LL latent − comparator | LL latent − D | LL comparator − D | direction own − other | comparator's | latent − comparator | direction own − k0 | concordance own − other | comparator's | latent − comparator | concordance own − k0 | reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | 5 | DL (vs DF) | +0.37 [+0.08, +0.65] | +8.24 [+7.16, +9.33] | +7.87 [+6.85, +8.91] | +1.59 [+1.12, +2.06] | +1.26 [+0.87, +1.70] | +0.33 [+0.18, +0.49] | +0.39 [-0.04, +0.86] | -0.06 [-0.26, +0.13] | -0.05 [-0.24, +0.15] | -0.01 [-0.10, +0.08] | -0.21 [-0.37, -0.05] | contradicted, practically meaningful |
| a | 5 | L (vs F) | -1.81 [-2.52, -1.12] | +3.54 [+2.37, +4.75] | +5.35 [+4.31, +6.43] | +2.68 [+2.10, +3.30] | +1.55 [+1.15, +1.97] | +1.13 [+0.75, +1.49] | +0.47 [-0.07, +1.09] | +0.01 [-0.04, +0.07] | -0.00 [-0.00, +0.00] | +0.01 [-0.04, +0.07] | -0.02 [-0.07, +0.04] | contradicted, practically meaningful |
| b | 5 | DL (vs DF) | -3.07 [-3.93, -2.17] | +1.80 [+0.97, +2.64] | +4.88 [+4.12, +5.67] | +0.30 [+0.10, +0.52] | +0.53 [+0.25, +0.85] | -0.24 [-0.54, +0.05] | +0.12 [-0.08, +0.34] | +0.16 [+0.02, +0.30] | -0.05 [-0.14, +0.04] | +0.21 [+0.06, +0.36] | +0.05 [-0.11, +0.22] | stands |
| b | 5 | L (vs F) | -4.20 [-6.56, -1.97] | -4.39 [-6.08, -2.66] | -0.19 [-2.29, +1.87] | +1.31 [+0.85, +1.76] | +3.30 [+2.57, +4.06] | -1.98 [-2.62, -1.39] | +0.00 [-0.41, +0.42] | +0.35 [+0.05, +0.65] | -0.00 [-0.00, +0.00] | +0.35 [+0.05, +0.65] | -0.08 [-0.37, +0.21] | inconclusive |

Latent against the softmax scale-use offsets DF (cross-family for L), log-likelihood ×100: a DL: +0.37 [+0.08, +0.65]; a L: -4.33 [-5.36, -3.26]; b DL: -3.07 [-3.93, -2.17]; b L: -9.27 [-11.08, -7.45]

**dorn_raters**

| rung | folds | latent | LL latent − comparator | LL latent − D | LL comparator − D | direction own − other | comparator's | latent − comparator | direction own − k0 | concordance own − other | comparator's | latent − comparator | concordance own − k0 | reading |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| published | 5 | DL (vs DF) | -3.99 [-4.91, -3.06] | +0.00 [-0.00, +0.00] | +3.99 [+3.06, +4.91] | +0.00 [+0.00, +0.00] | +8.70 [+7.90, +9.51] | -8.70 [-9.51, -7.90] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.09 [-0.17, +0.35] | -0.09 [-0.35, +0.17] | +0.00 [+0.00, +0.00] | stands |
| a | 5 | DL (vs DF) | -3.99 [-4.91, -3.06] | +0.00 [-0.00, +0.00] | +3.99 [+3.06, +4.91] | +0.00 [+0.00, +0.00] | +8.70 [+7.90, +9.51] | -8.70 [-9.51, -7.90] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.09 [-0.17, +0.35] | -0.09 [-0.35, +0.17] | +0.00 [+0.00, +0.00] | stands |
| a | 5 | L (vs F) | +3.74 [+2.73, +4.62] | +5.14 [+4.05, +6.23] | +1.39 [+0.00, +2.96] | +11.24 [+10.32, +12.14] | +10.87 [+9.96, +11.79] | +0.37 [+0.09, +0.64] | +3.57 [+2.53, +4.70] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | contradicted, practically meaningful |
| b | 5 | DL (vs DF) | -15.16 [-16.67, -13.64] | -11.78 [-13.38, -10.23] | +3.39 [+2.81, +3.97] | +3.61 [+3.08, +4.14] | +4.26 [+3.76, +4.81] | -0.65 [-1.10, -0.19] | +1.24 [+0.64, +1.86] | +0.23 [-0.14, +0.59] | +0.03 [-0.15, +0.22] | +0.20 [-0.23, +0.59] | -0.63 [-1.05, -0.21] | inconclusive |
| b | 5 | L (vs F) | -25.68 [-29.85, -22.26] | -34.19 [-37.77, -30.83] | -8.51 [-10.64, -6.23] | +7.99 [+7.10, +8.86] | +11.61 [+10.68, +12.55] | -3.62 [-4.33, -2.97] | +1.14 [+0.17, +2.20] | +0.13 [-0.35, +0.61] | +0.00 [+0.00, +0.00] | +0.13 [-0.35, +0.61] | -0.35 [-0.86, +0.15] | inconclusive |

Latent against the softmax scale-use offsets DF (cross-family for L), log-likelihood ×100: published DL: -3.99 [-4.91, -3.06]; a DL: -3.99 [-4.91, -3.06]; a L: +1.15 [+0.29, +2.04]; b DL: -15.16 [-16.67, -13.64]; b L: -37.58 [-41.29, -34.15]

## Selected penalties (λ_text, λ_rater, λ_W), adaptation strength at the reported k, and rung b's selection cell

| panel | rung | fold | DL | L | strengths | selection cell (raters / informative pairs) |
|---|---|---|---|---|---|---|
| multipref_synth_t0 | published | 0 | [300, 128, 100] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t0 | published | 1 | [300, 128, 10000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t0 | published | 2 | [300, 128, 1000] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_synth_t0 | published | 3 | [300, 128, 1000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t0 | published | 4 | [300, 128, 1000] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_synth_t0 | a | 0 | [300, 128, 100] | [1000, 32, 1000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 2} | — / — |
| multipref_synth_t0 | a | 1 | [300, 128, 10000] | [1000, 32, 1000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_synth_t0 | a | 2 | [300, 128, 1000] | [1000, 512, 100] | {'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_synth_t0 | a | 3 | [300, 128, 1000] | [1000, 512, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 128} | — / — |
| multipref_synth_t0 | a | 4 | [300, 128, 1000] | [1000, 512, 100] | {'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 32, 'L_20': 128} | — / — |
| multipref_synth_t0 | b | 0 | [300, 128, 10000] | [1000, 8, 100] | {'DFs_20': 0.5, 'DL_20': 0.03125, 'F_20': 0.5, 'L_20': 2} | 31 / 8275 |
| multipref_synth_t0 | b | 1 | [300, 32, 10000] | [1000, 32, 1000] | {'DFs_20': 2, 'DL_20': 0.03125, 'F_20': 0.5, 'L_20': 0.03125} | 32 / 12916 |
| multipref_synth_t0 | b | 2 | [300, 0.5, 1000] | [1000, 32, 1000] | {'DFs_20': 0.5, 'DL_20': 32, 'F_20': 0.5, 'L_20': 0.03125} | 30 / 10552 |
| multipref_synth_t0 | b | 3 | [300, 512, 1] | [1000, 2, 100] | {'DFs_20': 32, 'DL_20': 32, 'F_20': 0.5, 'L_20': 32} | 33 / 7230 |
| multipref_synth_t0 | b | 4 | [300, 0.5, 100] | [1000, 2, 10] | {'DFs_20': 0.5, 'DL_20': 32, 'F_20': 0.5, 'L_20': 128} | 34 / 9669 |
| multipref_synth_t5 | published | 0 | [300, 128, 1000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t5 | published | 1 | [300, 128, 10000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t5 | published | 2 | [300, 512, 100] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_synth_t5 | published | 3 | [300, 512, 1000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t5 | published | 4 | [300, 128, 1000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t5 | a | 0 | [300, 512, 100] | [1000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 0.5} | — / — |
| multipref_synth_t5 | a | 1 | [300, 128, 10000] | [3000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 0.5} | — / — |
| multipref_synth_t5 | a | 2 | [300, 512, 100] | [1000, 2, 10000] | {'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_synth_t5 | a | 3 | [300, 512, 10000] | [1000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 0.5} | — / — |
| multipref_synth_t5 | a | 4 | [300, 128, 1000] | [1000, 32, 1000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 8, 'L_20': 8} | — / — |
| multipref_synth_t5 | b | 0 | [300, 128, 100] | [1000, 512, 10] | {'DFs_20': 32, 'DL_20': 0.5, 'F_20': 0.5, 'L_20': 2} | 31 / 8291 |
| multipref_synth_t5 | b | 1 | [300, 128, 10] | [3000, 128, 100] | {'DFs_20': 512, 'DL_20': 0.5, 'F_20': 0.5, 'L_20': 0.125} | 32 / 13018 |
| multipref_synth_t5 | b | 2 | [300, 2, 1] | [1000, 8, 1000] | {'DFs_20': 2048, 'DL_20': 32, 'F_20': 0.5, 'L_20': 0.5} | 30 / 10616 |
| multipref_synth_t5 | b | 3 | [300, 2, 1] | [1000, 2, 10000] | {'DFs_20': 8192, 'DL_20': 32, 'F_20': 0.5, 'L_20': 0.03125} | 33 / 7360 |
| multipref_synth_t5 | b | 4 | [300, 0.5, 1000] | [1000, 0.5, 100] | {'DFs_20': 32, 'DL_20': 32, 'F_20': 0.5, 'L_20': 8} | 34 / 9764 |
| multipref_synth_t10 | published | 0 | [300, 128, 100] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t10 | published | 1 | [300, 128, 100] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t10 | published | 2 | [300, 128, 100] | None | {'DFs_20': 0.5, 'DL_20': 2048} | — / — |
| multipref_synth_t10 | published | 3 | [300, 128, 100] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t10 | published | 4 | [300, 128, 100] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_synth_t10 | a | 0 | [300, 128, 100] | [3000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 0.125} | — / — |
| multipref_synth_t10 | a | 1 | [300, 128, 100] | [3000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 32, 'L_20': 0.5} | — / — |
| multipref_synth_t10 | a | 2 | [300, 128, 100] | [1000, 2, 10000] | {'DFs_20': 0.5, 'DL_20': 0.125, 'F_20': 8, 'L_20': 0.125} | — / — |
| multipref_synth_t10 | a | 3 | [300, 128, 100] | [1000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.125} | — / — |
| multipref_synth_t10 | a | 4 | [300, 128, 100] | [3000, 2, 10000] | {'DFs_20': 2, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_synth_t10 | b | 0 | [300, 8, 1000] | [3000, 32, 1000] | {'DFs_20': 2, 'DL_20': 0.125, 'F_20': 0.5, 'L_20': 0.03125} | 31 / 8409 |
| multipref_synth_t10 | b | 1 | [300, 2, 1] | [3000, 128, 1] | {'DFs_20': 0.5, 'DL_20': 8, 'F_20': 0.5, 'L_20': 2} | 32 / 13162 |
| multipref_synth_t10 | b | 2 | [300, 0.5, 1] | [1000, 0.5, 10000] | {'DFs_20': 0.5, 'DL_20': 32, 'F_20': 0.5, 'L_20': 0.125} | 30 / 10629 |
| multipref_synth_t10 | b | 3 | [300, 0.5, 100] | [1000, 0.5, 10000] | {'DFs_20': 0.5, 'DL_20': 2, 'F_20': 0.5, 'L_20': 0.125} | 33 / 7432 |
| multipref_synth_t10 | b | 4 | [300, 8, 1000] | [3000, 2, 1000] | {'DFs_20': 2, 'DL_20': 0.03125, 'F_20': 0.5, 'L_20': 2} | 34 / 9840 |
| multipref_overall | published | 0 | [300, 128, 1000] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_overall | published | 1 | [300, 128, 100] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_overall | published | 2 | [300, 128, 100] | None | {'DFs_20': 0.5, 'DL_20': 2048} | — / — |
| multipref_overall | published | 3 | [300, 128, 1000] | None | {'DFs_20': 0.5, 'DL_20': 8192} | — / — |
| multipref_overall | published | 4 | [300, 512, 1000] | None | {'DFs_20': 2, 'DL_20': 8192} | — / — |
| multipref_overall | a | 0 | [300, 128, 1000] | [300, 32, 1000] | {'DF_20': 0.5, 'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 32} | — / — |
| multipref_overall | a | 1 | [300, 128, 100] | [1000, 32, 1000] | {'DF_20': 2, 'DFs_20': 0.5, 'DL_20': 2, 'F_20': 32, 'L_20': 2} | — / — |
| multipref_overall | a | 2 | [300, 128, 100] | [1000, 32, 1000] | {'DF_20': 0.5, 'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 2, 'L_20': 2} | — / — |
| multipref_overall | a | 3 | [300, 128, 1000] | [1000, 32, 1000] | {'DF_20': 0.5, 'DFs_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_overall | a | 4 | [300, 512, 1000] | [300, 32, 1000] | {'DF_20': 2, 'DFs_20': 2, 'DL_20': 2, 'F_20': 8, 'L_20': 0.5} | — / — |
| multipref_overall | b | 0 | [300, 128, 10] | [300, 2, 10000] | {'DF_20': 0.5, 'DFs_20': 2, 'DL_20': 8, 'F_20': 0.5, 'L_20': 2} | 31 / 7901 |
| multipref_overall | b | 1 | [300, 32, 1] | [1000, 0.5, 10000] | {'DF_20': 128, 'DFs_20': 32, 'DL_20': 8, 'F_20': 0.5, 'L_20': 8} | 32 / 13125 |
| multipref_overall | b | 2 | [300, 512, 1000] | [1000, 2, 100] | {'DF_20': 8, 'DFs_20': 0.5, 'DL_20': 0.125, 'F_20': 0.5, 'L_20': 128} | 30 / 10389 |
| multipref_overall | b | 3 | [300, 2, 1] | [1000, 512, 1000] | {'DF_20': 2048, 'DFs_20': 8192, 'DL_20': 128, 'F_20': 0.5, 'L_20': 0.03125} | 33 / 7038 |
| multipref_overall | b | 4 | [300, 32, 1] | [300, 512, 100] | {'DF_20': 8, 'DFs_20': 8192, 'DL_20': 128, 'F_20': 0.5, 'L_20': 0.125} | 34 / 9532 |
| dices | a | 0 | [3000, 128, 100] | [3000, 2, 10000] | {'DF_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.03125} | — / — |
| dices | a | 1 | [10000, 128, 10000] | [10000, 128, 1000] | {'DF_20': 0.5, 'DL_20': 0.5, 'F_20': 2, 'L_20': 0.5} | — / — |
| dices | a | 2 | [3000, 128, 100] | [3000, 128, 100] | {'DF_20': 0.5, 'DL_20': 0.125, 'F_20': 2, 'L_20': 0.125} | — / — |
| dices | a | 3 | [3000, 128, 10000] | [3000, 128, 1000] | {'DF_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 0.5} | — / — |
| dices | a | 4 | [3000, 32, 1000] | [10000, 512, 100] | {'DF_20': 0.5, 'DL_20': 0.03125, 'F_20': 2, 'L_20': 0.03125} | — / — |
| dices | b | 0 | [3000, 0.5, 100] | [3000, 32, 1] | {'DF_20': 0.5, 'DL_20': 128, 'F_20': 0.5, 'L_20': 2} | 16 / 9712 |
| dices | b | 1 | [10000, 512, 1000] | [10000, 0.5, 1] | {'DF_20': 0.5, 'DL_20': 0.125, 'F_20': 0.5, 'L_20': 0.03125} | 16 / 9063 |
| dices | b | 2 | [3000, 2, 100] | [3000, 32, 10] | {'DF_20': 32, 'DL_20': 32, 'F_20': 0.5, 'L_20': 0.5} | 16 / 8129 |
| dices | b | 3 | [3000, 512, 10] | [3000, 2, 1000] | {'DF_20': 8, 'DL_20': 0.5, 'F_20': 0.5, 'L_20': 2} | 17 / 6578 |
| dices | b | 4 | [3000, 512, 10000] | [10000, 8, 10000] | {'DF_20': 8, 'DL_20': 0.03125, 'F_20': 0.5, 'L_20': 0.03125} | 17 / 6448 |
| prism | a | 0 | [300, 512, 10] | [300, 2, 10000] | {'DF_20': 0.5, 'DL_20': 0.5, 'F_20': 8, 'L_20': 2} | — / — |
| prism | a | 1 | [300, 512, 10] | [300, 128, 100] | {'DF_20': 2, 'DL_20': 2, 'F_20': 8, 'L_20': 0.5} | — / — |
| prism | a | 2 | [300, 512, 10] | [300, 128, 100] | {'DF_20': 2, 'DL_20': 2, 'F_20': 8, 'L_20': 2} | — / — |
| prism | a | 3 | [300, 512, 10] | [300, 128, 1000] | {'DF_20': 2, 'DL_20': 2, 'F_20': 8, 'L_20': 2} | — / — |
| prism | a | 4 | [300, 512, 10] | [1000, 512, 100] | {'DF_20': 2, 'DL_20': 2, 'F_20': 8, 'L_20': 0.5} | — / — |
| prism | b | 0 | [300, 128, 1] | [300, 8, 100] | {'DF_20': 8, 'DL_20': 32, 'F_20': 0.5, 'L_20': 2} | 97 / 4828 (below 5,000: flagged) |
| prism | b | 1 | [300, 128, 1] | [300, 512, 10] | {'DF_20': 2, 'DL_20': 32, 'F_20': 0.5, 'L_20': 128} | 90 / 4333 (below 5,000: flagged) |
| prism | b | 2 | [300, 512, 100] | [300, 0.5, 10000] | {'DF_20': 2048, 'DL_20': 8, 'F_20': 0.5, 'L_20': 0.125} | 106 / 4523 (below 5,000: flagged) |
| prism | b | 3 | [300, 32, 10] | [300, 0.5, 100] | {'DF_20': 0.5, 'DL_20': 2, 'F_20': 0.5, 'L_20': 32} | 101 / 3294 (below 5,000: flagged) |
| prism | b | 4 | [300, 0.5, 100] | [1000, 2, 10] | {'DF_20': 8, 'DL_20': 128, 'F_20': 0.5, 'L_20': 32} | 87 / 4964 (below 5,000: flagged) |
| dorn_raters | published | 0 | [1000, 512, 10000] | None | {'DF_10': 0.5, 'DL_10': 0.5} | — / — |
| dorn_raters | published | 1 | [1000, 512, 10000] | None | {'DF_10': 0.5, 'DL_10': 0.5} | — / — |
| dorn_raters | published | 2 | [1000, 512, 10000] | None | {'DF_10': 0.5, 'DL_10': 0.5} | — / — |
| dorn_raters | published | 3 | [3000, 512, 10000] | None | {'DF_10': 2, 'DL_10': 0.5} | — / — |
| dorn_raters | published | 4 | [1000, 512, 10000] | None | {'DF_10': 0.5, 'DL_10': 0.5} | — / — |
| dorn_raters | a | 0 | [1000, 512, 10000] | [10000, 512, 100] | {'DF_10': 0.5, 'DL_10': 0.03125, 'F_10': 2, 'L_10': 0.5} | — / — |
| dorn_raters | a | 1 | [1000, 512, 10000] | [10000, 32, 10000] | {'DF_10': 0.5, 'DL_10': 0.03125, 'F_10': 2, 'L_10': 0.5} | — / — |
| dorn_raters | a | 2 | [1000, 512, 10000] | [10000, 32, 1000] | {'DF_10': 0.5, 'DL_10': 0.03125, 'F_10': 2, 'L_10': 0.5} | — / — |
| dorn_raters | a | 3 | [3000, 512, 10000] | [10000, 512, 100] | {'DF_10': 2, 'DL_10': 0.03125, 'F_10': 2, 'L_10': 0.5} | — / — |
| dorn_raters | a | 4 | [1000, 512, 10000] | [3000, 8, 10000] | {'DF_10': 0.5, 'DL_10': 0.03125, 'F_10': 2, 'L_10': 0.5} | — / — |
| dorn_raters | b | 0 | [1000, 512, 10000] | [10000, 0.5, 10000] | {'DF_10': 8, 'DL_10': 0.03125, 'F_10': 0.5, 'L_10': 2} | 490 / 1298 (below 5,000: flagged) |
| dorn_raters | b | 1 | [1000, 128, 1] | [10000, 512, 10] | {'DF_10': 128, 'DL_10': 128, 'F_10': 0.5, 'L_10': 8} | 474 / 932 (below 5,000: flagged) |
| dorn_raters | b | 2 | [1000, 512, 10] | [10000, 0.5, 10000] | {'DF_10': 2, 'DL_10': 8, 'F_10': 0.5, 'L_10': 32} | 497 / 1154 (below 5,000: flagged) |
| dorn_raters | b | 3 | [3000, 2, 100] | [10000, 8, 1000] | {'DF_10': 2, 'DL_10': 32, 'F_10': 0.5, 'L_10': 0.125} | 445 / 1093 (below 5,000: flagged) |
| dorn_raters | b | 4 | [1000, 128, 1] | [3000, 32, 1] | {'DF_10': 0.5, 'DL_10': 0.03125, 'F_10': 0.5, 'L_10': 8} | 433 / 802 (below 5,000: flagged) |


=== (D) CLAIMS.md ===
# Paper 4 — claim–evidence table (PROTOCOL_STAGE13.md, S13-4)
Each headline claim with its population, endpoint, baseline, implementation, uncertainty analysis and developmental status. "Frozen" = rule fixed before the outcome; "exploratory" = developed or added after inspecting results.

| # | Claim (draft wording) | Population | Endpoint | Baseline | Implementation | Uncertainty | Status |
|---|---|---|---|---|---|---|---|
| 1 | Text-independent rater offsets improve graded-label LL by 0.08–0.10 nats/rating at k = 20 (unrestricted offsets DF 0.080 on MultiPref; symmetric offsets DFs up to 0.10) | MultiPref, PRISM (graded), DICES; new raters, held-out prompts | LL per rating | text-only model (k = 0) | DF (unrestricted rater offsets) and DFs (symmetric offsets) on frozen Qwen features | rater bootstrap; prompt × rater two-way | frozen DF (Stages 1–2, replications; 0.080 on MultiPref); the symmetric-offset variant DFs (upper end 0.10) was added after first results and is exploratory |
| 2 | Symmetric offsets barely change direction on MultiPref and cancel exactly under binary labels (unrestricted offsets can change decisions, e.g. DICES) | MultiPref | direction accuracy; binary LL | text-only | as 1 | as 1 | binary cancellation is an algebraic property of the symmetric construction; the empirical DFs direction result is exploratory (DFs added after first results) |
| 3 | Evaluated published methods' own k = 20 choice/direction gains have upper bounds < 1 point | MultiPref; PRISM native choices | own − own k = 0 accuracy | each method's k = 0 | VPL, PAL-B, LoRe (compressed-feature re-implementations; LoRe native reproduction unresolved) | rater bootstrap; two-way | frozen (Stage 3; PRISM Stage 6); claims concern the evaluated implementations |
| 4 | Semi-synthetic controls: small gains do not exclude preferences the learners miss | MultiPref with injected labels | recovery of injected effects | oracle / known-feature learner | as 3 | rater bootstrap conditional on each synthetic panel; multi-seed / multi-draw sensitivity where run | frozen (Stage 5) + exploratory dose-response; the latent-model rows as first run used a mis-scaled adaptation prior (claims 14–15) |
| 5 | CA: own adapted parameters beat another user's for four of six methods (own − exchanged parameters; measures user association, not benefit, and is confounded with task mix) | CA first turns, 2,957 new users | own − other accuracy | another user's adapted parameters | LoRe, LoRe-reg, VPL, PAL | rater bootstrap; Holm sensitivity (approximate) | frozen rule (Stage 8; the rule's label was "content personalisation detected"; summary-script bug fixed); within-country control exploratory |
| 6 | Length deviations reproduce across disjoint prompt sets | CA first turns | cross-half moment of one-step deviations | 0 (null / context simulations) | S11-2 diagnostic | user bootstrap; calibration not met as specified | exploratory (Stage 11 Am. 1–5) |
| 7 | **On identical items, support histories predict which of two disagreeing users chose which response** (conditional assignment log score +0.066 nats; 62.2 %) | CA first-turn identical items, 1,336 users in 4,608 disagreeing pairs (1,436 users for the benefit endpoint) | assignment log score / accuracy over disagreeing user pairs | ½ (chance) | validated isotropic adaptation (Stage 12 procedure) | item × user two-way bootstrap | **frozen (Stage 13 S13-1)** on previously analysed data; joint attribute + position refit exploratory (Am. 2): attribute-derived scores remain predictive, position-only also informative (no content-vs-position separation) |
| 8 | Isotropic adaptation beats the population model on the identical-item panel: +0.70 points (user bootstrap; two-way covers 0), +0.018 nats (both) | as 7 | own − μ pairwise accuracy, LL | per-language population model | as 7 | user bootstrap (primary); two-way accuracy covers 0 | frozen (S13-1) |
| 9 | Frozen procedure on new turns: +0.38 [+0.13, +0.64] points, +0.0046 nats; no advantage of Ĉ over isotropic established | CA second turns of the same users | own − μ | population model | TRV / isotropic | user bootstrap; two-way accuracy covers 0 | frozen (Stage 12); procedure developed on turn 1 (exploratory) |
| 10 | The frozen isotropic procedure did not establish improvement on MultiPref (−0.28 [−0.64, +0.08]) | MultiPref, 202 held-out annotators | own − μ, binary | population model | isotropic (primary), TRV | rater bootstrap; two-way | frozen (S13-2); MultiPref analysed earlier with other methods; TRV outperforms isotropic under the primary rater bootstrap (+0.23 [+0.04, +0.42]) without establishing improvement over the population model; the two-way contrast includes 0 |
| 11 | Population-training procedure changes the measured gain by ~0.6 points (paired); prompt-split contrast inconclusive | CA first turns, 1,799 common users | own − population accuracy (length) | W vs O population models | 1-D length adaptation | paired user bootstrap | exploratory (Am. 9, 11); mechanism not isolated |
| 12 | Additional predictive value of unrescaled first-turn deviations on later, disjoint conversations beyond a history-conditioned population model is **not supported** for this procedure and panel: accuracy-positive under user clustering (+0.43 [+0.13, +0.74] points), likelihood-inconclusive (+0.0015 [−0.0006, +0.0035] nats); the rule requires both | CA third turns, 953 users (1,901 with frozen δ̂ → 1,808 with ≥ 5 complete third-turn events → 953 outside support conversations) | own − history-conditioned population | m₃ | frozen δ̂^(1) | user bootstrap; two-way (accuracy [−0.08, +0.92]) | frozen (S13-3; Am. 5 implements the previously specified history filter); not "preferences are unstable" |
| 13 | Stratifying test pairs by the population model's margin does not establish a practically meaningful gain on contested pairs (rule: lower bound > +1 point) nor concentration of the gain there (rule: accuracy and log-likelihood). CA: the accuracy gain sits on the contested ~22 % (+1.62 [+0.72, +2.52] first turns; +1.62 [+0.63, +2.53] second turns; rest +0.16 / +0.05), the log-likelihood gain does not (contested − rest −0.69 [−1.09, −0.29] / +0.00 [−0.24, +0.24] ×100) — mechanical concentration by the pre-stated caveat. MultiPref: contested +0.02 [−1.38, +1.37] | CA first and second turns; MultiPref | TRV − pop accuracy and LL per stratum (|population logit| below the 20th percentile of the fold's training pairs) | population model | TRV (isotropic: same picture) | user bootstrap (primary); two-way intervals for the CA contested accuracy reach 0 | frozen rules (Stage 14 S14-2, PROTOCOL_STAGE14.md §2, §5) on previously analysed data; intervals unadjusted |
| 14 | A real-data positive control exposed a defect in our latent models, since corrected: on Jester (seen jokes, k = 20) a linear collaborative-filtering reference gains +1.39 [+1.12, +1.68] concordance points over joke means, the pipeline's low-rank latent +0.14 [+0.09, +0.19]; with the adaptation prior whitened the ordinal latent gains +1.68 [+1.47, +1.90] and, with rater-side penalties chosen by pseudo-new-rater concordance, the softmax latent +1.16 [+0.98, +1.34]. On held-out jokes no learner beats the text-predicted joke mean | Jester, 1,000 users × 128 jokes, new raters | within-rater pairwise concordance, own − population prediction | joke means; linear CF reference | DL / L in `factorised_rm.py` (`--whiten_adapt`, `--sel_conc`); CF in `s14_cf.py` | rater bootstrap; folds 1–4 (not used in the diagnosis) reported separately | reference and first-run rules frozen (Stage 14 S14-1); diagnosis and correction post hoc (Amendment 1; rules for the corrected runs written before running; the +1 rule for the softmax latent narrowly unmet) |
| 15 | With the corrected adaptation prior the latent models detect an injected +10-point content preference on held-out items (own − other direction: ordinal latent +2.82 [+2.02, +3.63]; softmax latent +0.62 [+0.17, +1.06]) but not +5 points, without a significant gain over no adaptation (+0.84 [−0.12, +1.80]); on real MultiPref they show nothing beyond scale use (own − other −0.16 to +0.19 points, upper bounds ≤ +0.50; DFs − DL −0.0005 [−0.0052, +0.0049] nats). DICES ordinal-latent concordance +0.50 [+0.09, +0.96] is a lead only (uncorrected, about twenty cells). On PRISM the corrected softmax latent is ahead of the offsets in likelihood by 0.0037 nats per rating (DF − DL −0.0037 [−0.0065, −0.0008], about 5 % of the offsets' gain; contradicts "nothing beyond scale use" in likelihood under the pre-written rule) with no concordance gain (own − other −0.06 [−0.26, +0.13]) | MultiPref semi-synthetic panels (τ0, τ5, τ10); MultiPref, DICES, Dorn, PRISM; new raters, held-out items | own − other direction / concordance; LL latent − scale-use comparator | another rater's parameters; DFs / DF / F | as 14, rung a (likelihood selection) primary; rung b lowers held-out LL and is a sensitivity analysis | rater bootstrap; one synthetic draw per strength | post hoc (Stage 14 Amendment 1, A1-4); reading rules written before the runs; the rule's direction clause is uninformative on single-response panels (stated after the result) |
