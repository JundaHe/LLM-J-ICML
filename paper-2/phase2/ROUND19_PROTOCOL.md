# Paper 2 — Round-19 analyses (frozen before any result is computed)
Committed 2026-11-05, after `reviews/codex_round19_2026-11-05.md`. Each analysis is fixed here before it is run; amendments are logged below and do not change the readings.

## R19-1 Cross-term diagnostic for X (CPU; answers review issue 1)
**Question.** `rho_exact.py` defines r1 = C(h1 − q1), r2 = C(h2 − q1), with q1 the exact mode+mean comparator of panel 1. Then r2 = C(h2 − q2) + C(q2 − q1), so X = X_own + X_cross with X_own = ⟨C(h1 − q1), C(h2 − q2)⟩/NRM (q2: the same exact-T comparator built from panel 2 itself) and X_cross = ⟨C(h1 − q1), C(q2 − q1)⟩/NRM.
**Scope.** Dense panels only (b = 20 second-panel raters; on the small leave-one-out panels b = 1, panel 2's own exact comparator equals its one-hot histogram, so X_own ≡ 0 and X is by construction a new-rater forecasting quantity — stated in the text, not estimated). Panels: every `results/rho_exact/` panel with m > 12, at every a in its existing A_LIST.
**Procedure.** Identical splits, folds (fold seed 1), R = 10 repetitions and item-cluster bootstrap (B = 200, seeds as in `rho_exact.py`) as `rho_exact.py`; additionally compute q2 = `exactT_q` on panel 2 (its own mode, sum, histogram) and report X, X_own, X_cross, M, M_own := mean ‖C(h2 − q2)‖²/NRM and ρ_own := X_own / M, each with a 95 % interval.
**Readings (fixed now).**
- *Cross-term negligible* if, at every a, the X_cross interval lies within ±25 % of |X| or within ±0.0005 absolute (whichever is larger). Then the text may describe ρ as reliability of the shape beyond location, noting the decomposition.
- Otherwise the text describes ρ only as an operational *new-rater forecasting* quantity (the identity A1 = M − 2X with NRM-normalised inner products, see R19-T) and reports X_own separately as the shape-to-shape reproducibility.
Either way, the draft adopts the narrower "forecasting" wording for the small panels.

## R19-T Text-only corrections (no new computation)
Score normalisation stated (all inner products divided by NRM = K − 1 for ordinal, 1 for nominal, as implemented); ties in "exact mode" defined as in `z_label`; abstract bound qualified by clustering; "matches" → "no difference detected (interval)"; "always" → counts; "do not use the shape" / "unlearnable" narrowed to the probes run; mechanistic budget explanation removed from §5; approximate budgets and the rounding rule stated; panel inventory table; definitions of A1^x, mode prototype, reliability-shrunk targets, CSC, the thirty configurations; "−0.0000 [−0.0000, +0.0000]" printed at more digits.

## R19-2 Planted-shape calibration of the decoding pipeline (CPU; issue 3) — to be specified in an amendment before running
## R19-3 Rater-model reproduction of dense-panel X (CPU; issue 4) — to be specified in an amendment before running
## R19-4 Budget comparison with documented optimisation exposure (GPU via Slurm; issue 7) — to be specified before running

## Amendments
