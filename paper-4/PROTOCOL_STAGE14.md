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
