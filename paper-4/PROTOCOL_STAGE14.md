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
