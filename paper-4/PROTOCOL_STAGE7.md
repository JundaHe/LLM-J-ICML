# Paper 4 — Stage 7: is the injected content dimension inside the learners' input space? (frozen before any result)
Committed 2026-11-01, after the seventh ICML-style review (4/10). Objection (checked in `make_synth.py`): the injected feature g2 is a random direction in the *whitened* top-256 PCs of the pair-difference embedding E_B − E_A, while VPL / PAL-B see a different PCA-256 basis over per-response embeddings and D / DL see PCA-256 of a joint (prompt, A, B) embedding; g1 (log length ratio) need not be linear in any of them. The detection limit of §5.6 may therefore mix representation mismatch with statistical difficulty. Any change after the first result is logged under "Amendments".

## S7-1: linear-probe availability of g1 and g2 (diagnostic)
For each learner input space, a cross-fitted ridge probe predicts the standardised g1 and g2 (exactly as `make_synth.py` computes them) on all MultiPref items: 5 folds by prompt group (the paper's item folds), ridge penalty chosen per outer fold by inner 5-fold CV over {10⁻², 10⁻¹, …, 10⁵}, out-of-fold R². Input spaces:
(a) VPL / PAL-B, PCA-256: [x_A, x_B, x_P] (768-d) as `vpl_pal.py` builds them, and the difference x_B − x_A (256-d), which is all a linear reward on responses can use for a pair;
(b) VPL / PAL-B, full features: x_B − x_A on the standardised 3,584-d embeddings;
(c) D / DL / DFs: the joint-embedding PCA-256 X of `factorised_rm.py`.
Positive reference: the 256-d whitened pair-difference basis Z of the generator itself (R²(g2) = 1 by construction).

**Reading (fixed now).** A component is called *available* to a learner if its probe R² ≥ 0.5, and *largely unavailable* if R² < 0.2. If g2 is largely unavailable to a learner, that learner's §5.6 detection limit is reported as partly a representation limit, not a statistical one, and S7-2 is run. The abstract's "the bottleneck is finding the content dimension, not the number of ratings" is softened in either case (the reference learner is given the features; that comparison does not separate the two).

## S7-2 (conditional on S7-1): in-span injection
If S7-1 finds g2 largely unavailable to any learner, τ5 and τ10 panels are regenerated with g2 replaced by a random unit direction in the span of that learner's pair-difference input (x_B − x_A, PCA-256 of `vpl_pal.py`; same seed rule, same calibration of τ to generator-oracle gains), and PAL-B (full features), VPL and the reference learner are re-run with the §5.6 outcome (own − other at k = 20, 50; detection = lower bound > +1 point). Exploratory; reported next to the original panels.

## Amendments
