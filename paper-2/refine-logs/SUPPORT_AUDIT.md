# Zero-GPU support audit (2026-08-23) — fully derangeable coverage of training items under cells (pool, z_i, ⌊Σy/w⌋), 60 % training split, evaluator folds as in the proposal
z_i = mode of the target raters' ratings (ties → level closest to the target median, then lower). A cell is eligible iff N ≥ 2 and its largest histogram class M ≤ N/2; the assignment is the sorted-class rotation by M (verified: every item receives a different histogram; bijection). Drift = |mean(donor) − mean(item)| over target raters.

| Panel / criterion (target raters) | w = 1 (exact Σy) | w = 2 (drift ≤ 0.25) | w = 3 (drift ≤ 0.5) | w = 4 (drift ≤ 0.75) |
|---|---|---|---|---|
| Commit What (4) — folds {1,2} / {3,4} / {5,6} | 7 % / 1 % / 0 % | 25 / 37 / 18 % (mean drift .19) | 63 / 57 / 61 % (mean drift .28) | 62 / 56 / 69 % (.33) |
| Commit Why (4) | 4 / 6 / 1 % | 30 / 39 / 35 % (.15) | 59 / 39 / 26 % (.28) | 69 / 64 / 53 % (.39) |
| Readability (6) — triples | 23 / 50 / 22 % | 51 / 78 / 39 % (.10) | 91 / 91 / 76 % (.14) | — |
| Summarization (2) — LOO | 0 % (histogram determined by (z_i, Σy)) | — | — | — |
Without pool in the cell key, commit coverage changes by at most a few points (e.g. What w = 3: 65 / 50 / 65 %) — pool is kept.
Reading: exact location control leaves essentially no randomisation support on 4-rater targets; a bounded relaxation of the rating sum is unavoidable and must be pre-declared and reported with its drift. Pre-declared widths: commit w = 3 (|drift| ≤ 0.5 rating points, mean ≈ 0.3), readability w = 2 (≤ 0.17); summarization: Δ_link not identifiable.

## Leave-one-rater-out rotations (reviewer round 4), exact cells (pool, z_i, Σy), 60 % training split
| Panel / criterion (target raters) | exact coverage per LORO fold | w = 2 (drift ≤ 1/m_t) |
|---|---|---|
| Commit What (5) | 1 / 4 / 1 / 6 / 2 / 2 % (cells 2 / 1 / 2 / 4 / 2 / 3) | 42 / 44 / 42 / 44 / 65 / 43 % (drift ≤ 0.2) |
| Commit Why (5) | 8 / 14 / 13 / 9 / 6 / 6 % | 40 / 41 / 46 / 35 / 34 / 44 % |
| Commit, all 6 raters as targets (no exclusion) | What 13 %, Why 20 % | — |
| Readability (8), 124 keyed snippets | 36 / 43 / 42 / 46 / 41 / 50 / 31 / 51 / 42 % | 59 / 82 / 72 / 82 / 73 / 88 / 74 / 73 / 68 % |
| Readability (8), all 200 snippets | 45 / 55 / 61 / 53 / 42 / 59 / 36 / 61 / 58 % | — |
Reading: exact label-and-location-preserving randomisation is **not supported on the commit-message panel under any rotation** (≤ 14 % even with 5 target raters; ≤ 20 % with no exclusion), is **borderline-supported on readability** (31–51 % with 8 target raters) and **impossible on 2-rater targets**. Exact identification therefore exists only on the panel whose dispersion reliability is ≈ 0. Pre-declared selection rule (round 4): w* = min{w : κ_f ≥ 0.30 for every fold}; commit → w* = 2 (drift ≤ 0.2), readability → w* = 1 (exact), summarization → none.

## CORRECTED audit (external review round 2): hash-grouped 60 % split, randomised maximum-cardinality matching — `idea-stage/pilot/support_audit.py`, `results/support_audit.json`
The earlier tables report **full-cell derangeability** (largest class M ≤ N/2: every item in the cell changes at once) — too strict. A maximum-cardinality exact matching changes min{N, 2(N−M)} items per heterogeneous cell, and under randomised matching every item in a heterogeneous cell has positive change probability. Dose = mean total-variation distance between original and donor histogram over changed items.

| Panel / criterion (target raters) | full-cell (old κ) | **max-changed fraction** | heterogeneous-cell fraction | dose (TV) |
|---|---|---|---|---|
| Commit What (5), LORO, exact w = 1 | .01–.07 | **.25–.32** | .56–.64 | .40 |
| Commit What, w = 2 (drift ≤ 0.2) | .34–.60 | .73–.81 | .87–.92 | .25 |
| Commit Why (5), LORO, exact w = 1 | .09–.13 | **.33–.37** (≥ .30 in every fold) | .44–.53 | .40 |
| Commit Why, w = 2 | .43–.51 | .77–.81 | .90–.95 | .27 |
| Readability 124 keyed (8), LORO, exact | .31–.51 | **.47–.59** | .58–.68 | .28 |
| Summarization CA (2), LOO, exact | 0 | **0** (lemma) | 0 | — |
Consequences: exact (label-, mean- and pool-preserving) randomisation is feasible at ≈ one third of the training items on commit Why and What, and at ≈ half on readability; "exact identification only on readability" was wrong. The story is **incomplete intervention intensity**, not absence of support. The 0.30 threshold is to be replaced by MDE/power simulations that use both the changed fraction and the dose.

## M0: frozen support model — validation (2026-08-23, `idea-stage/pilot/support_model.py`, `results/support_model.json`)
Model: key frequencies (pool, z, Σy) and within-key histogram-class frequencies estimated on the complementary 40 % of artifacts; a training set of the planned size is simulated (300 draws) and its max-changed fraction computed. Validation on the 18 (split × LORO fold) commit cells and 27 readability cells:

| Panel | observed mean [min, max] | predicted mean | mean error | MAE | corr (fold-level) |
|---|---|---|---|---|---|
| Commit What | .315 [.254, .367] | .290 | −.025 | .040 | .16 |
| Commit Why | .322 [.285, .371] | .266 | −.056 | .059 | −.46 |
| Readability (124) | .549 [.459, .649] | .431 | −.118 | .123 | −.41 |

**Verdict (pre-registered rule):** the model reproduces the order of magnitude but systematically under-predicts and has no fold-level predictive power → **C1 is reported as an exact empirical support enumeration, not a general predictive bound.** The pseudo-novelty risk the reviewers flagged is therefore real: the paper's C1 must rest on the enumeration, the lemma, the dose and the subsampled-rater curves, and on the audited estimates in C2.

## M0: subsampled-rater support curves (exact cells, split 0, mean over LORO folds × 5 rater subsets)
| Panel | m_t = 8 | 6 | 5 | 4 | 3 |
|---|---|---|---|---|---|
| Commit What | — | — | .295 | .156 | .170 |
| Commit Why | — | — | .341 | .240 | .156 |
| Readability (124) | .539 | .523 | — | .212 | — |
Intensity collapses as the target panel shrinks; with 2 target raters it is exactly 0 (lemma).
