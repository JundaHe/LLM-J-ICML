# Experiment Plan

**Problem**: Soft-label / distributional fine-tuning of LLM judges is validated against the pooled histogram it was trained on; on 3–9-rater SE panels we cannot tell item-linked disagreement learning from global calibration and scale location — and the support audit shows the clean attribution is mostly not available on these panels.
**Method Thesis**: The exact mode-, mean- and pool-preserving target-link randomisation has limited but non-zero finite-sample intensity on released SE panels (max-changed fraction ≈ .25–.32 commit What, .33–.37 commit Why, .47–.59 readability, 0 with two target raters; dose ≈ .40 TV); we state this feasibility result with MDE/power, and estimate — with symmetric calibration, excluded rater identities, a matched no-adversary control and explicit intensities — the Chen-package gain Δ_soft, the adversarial-term effect Δ_adv and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability, per family, reading what they license from a results-conditioned claim matrix.
**Date**: 2026-08-23

## Claim Map
| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|-------|-----------------|-----------------------------|---------------|
| C1 (primary, CPU): under randomised maximum-cardinality exact matching on the hash-grouped split, the intervention can change .25–.32 (commit What), .33–.37 (commit Why), .47–.59 (readability) of training artifacts with dose ≈ .40 TV, and 0 with two target raters (lemma); a frozen support model validated on held-out grouped splits / synthetic panels predicts these intensities (else C1 is the empirical audit); MDE/power simulations give the minimum detectable Δ_link per panel | Tells reviewers what this intervention can support on a given panel and at what power | Support script + certificates; full-cell / max-changed / positive-probability fractions and dose per panel / criterion / rotation; subsampled-rater curves; predicted vs observed; MDE table | B0 |
| C2 (supporting, GPU): for the exact Chen objective with a matched no-adversary control, Δ_soft, Δ_adv and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability are reported per family as estimates with artifact-bootstrap CIs per outer split, split-level replication spread, intensities and dose; Δ_bin-link (w = 2) sensitivity only | Positive Δ_link = item-linked histogram information beyond mode and mean at the realised intensity; a null at partial intensity is not evidence of absence | Estimates + CIs per (panel, criterion, family), three outer splits, certification, five-bin REL/RES/UNC (descriptive), protocol comparison | B1, B2, B4 |
| Anti-claims to rule out | (a) the gain is an artefact of asymmetric / transductive calibration; (b) A_perm changes the CE class, the mean or the pool; (c) Why results are driven by What conditioning; (d) the simplified hybrid, not Chen's objective, was audited; (e) effects are single-seed / single-family noise; (f) Δ_soft is an objective-package contrast (loss weighting / adversarial term); (g) G is a fixed rotation confounded with artifact order | (a) symmetric arm-specific calibration on an untouched split (readability: 15 % split, coarse grid); (b) shared point label z_i in all losses and cells; certification (z_i, mean, pool exact at w = 1; max-changed fraction; dose); (c) single-criterion prompts; (d) exact objective parity-tested against released code + sensitivity row; (e) 3 hash-grouped outer splits × independent optimiser and permutation seeds × 2 families reported separately; (f) A_chen0 no-adversary arm must-run on commit; (g) G drawn as a randomised maximum matching, permutation seed independent of data order | B0, B1, B2 |

## Paper Storyline
- Main paper must prove: C1 (Table 1 + Figure 1: full-cell / max-changed / positive-probability fractions and dose by panel / rotation; subsampled-rater curves; predicted vs observed; MDE table; the two-rater lemma), C2 (Table 2: Δ_soft, Δ_adv, exact Δ_link^ITT on commit Why / What / readability per family with CIs, split spread, intensity and dose; Figure 2: per-(fold, split) estimates), the certification table (Table 3) and the five-bin REL/RES/UNC reading (Table 4, descriptive). Δ_reg and Δ_bin-link are appendix.
- Appendix can support: exact-objective hyper-parameter sensitivity; pre-audit split-half reliability and location-null diagnostics; the pilot's superseded analyses (as a cautionary tale); Δ_reg as an algebraic residual.
- Experiments intentionally cut: panel-size sweep as a law; posterior-predictive / CRPS / tie-aware training arms; routing / gain heads; per-rater conditioning; RL judges; non-SE benchmarks; skill-score and entropy-AUROC metrics (the pilot's location-residualisation claim is dropped); untrained frontier-judge rows; summarization GPU runs (the two-rater boundary is analytic); ten-bin and isotonic sensitivities; drift-stratified "deconfounding".

## Experiment Blocks
### Block 0: Support enumeration + sanity — the CPU result that is the paper's primary evidence
- Claim tested: C1 (support map, two-rater lemma, predicted vs observed κ) and anti-claims (a)–(d); correctness of the harness.
- Why this block exists: the round-1 external review found five metric/data bugs and an unfair null; every later number depends on these being fixed.
- Dataset / split / task: all three panels; hash-grouped (commit) / snippet (readability) 60/10/30 outer splits × 3; readability universe locked to the 124 keyed CoReEval snippets (direct key; the 76 snippets without code excluded and documented; its keyed-subset dispersion reliability ≈ −0.04 is reported); commit LORO (6 folds), readability LORO (9 folds); subsampled-rater support curves (readability 8 → 6 → 4; commit 5 → 4 → 3).
- Compared systems: none (checks).
- Metrics: per panel / criterion / rotation: full-cell derangeability, max-changed fraction Σ min{N, 2(N−M)}/n, positive-probability fraction, dose (TV) under randomised maximum matching on the grouped split (`idea-stage/pilot/support_audit.py`, certificates to `results/support_audit.json`); frozen support model predictions vs observed on held-out grouped splits and synthetic panels; the two-rater lemma; MDE/power simulation from pilot variance × intensity × dose; unit tests for AUROC ties, ordinal α, 9-rater strata, z_i tie rule; calibration-split leakage check; exact-Chen parity against released code incl. the adversarial inner loop. Corrected audit already run: commit Why max-changed .33–.37 (dose .40), What .25–.32, readability .47–.59 (dose .28), summarization 0.
- Setup details: CPU + one 7B smoke run per arm (≤ 3 steps).
- Success criterion: support script and certificates released; frozen support model validated (or downgraded to empirical audit); MDE table produced; parity and invariant checks pass. No outcome-contingent gate.
- Failure interpretation: if the support model mis-predicts out of sample, C1 is the empirical audit only; if MDE exceeds plausible effects on a panel, that panel's Δ_link is reported as under-powered and not run.
- Table / figure target: Table 1, Figure 1, Table 3.
- Priority: MUST-RUN (zero GPU; the paper's primary evidence)

### Block 1: GPU audit on commit messages — Δ_soft, Δ_adv and the exact Δ_link^ITT(G) (Why primary)
- Claim tested: C2 (commit part).
- Why this block exists: the primary estimate — exact randomisation is feasible at ≈ one third intensity on commit Why, the criterion with reproducible item-level disagreement.
- Dataset / split / task: commit messages, criteria Why (primary) and What (single-criterion prompts); three hash-grouped 60/10/30 outer splits; leave-one-rater-out evaluator rotation (6 folds, 5 target raters).
- Compared systems: A_hard (CE to z_i); A_chen0 (α·KL + (1−α)·CE, no adversary — matched control); A_chen (exact Chen incl. adversarial term, parity-tested); A_perm (exact Chen with histograms re-assigned by a randomised maximum-cardinality exact matching within heterogeneous cells (pool, z_i, Σy), identity elsewhere; full-data ITT); all arms on the full training set; w = 2 sensitivity arm on Why, Qwen, split 0 only.
- Metrics: calibrated held-out-rater RPS per arm (primary); Δ_soft = hard − chen, Δ_adv = chen0 − chen, Δ_link^ITT = perm − chen overall and per stratum (strata from target raters), each with the split's max-changed fraction and dose; five-bin REL/RES/UNC (descriptive); Δ_reg, Δ_bin-link appendix.
- Setup details: Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct (reported separately); LoRA r = 16, α = 32, lr 1e-4, 2 epochs, accum 8; per outer split an independent optimiser/data-order seed and an independent permutation draw; symmetric arm-specific (T, λ) calibration on the 10 % calibration split using target raters, refitting uncertainty by bootstrapping the calibration set; 4 arms × 6 folds × 3 splits × 2 families × 2 criteria = 288 runs (≈ 130 GPU-h); stage-gated by M1 = exact commit-Why gate (4 arms × 6 folds, Qwen, split 0 = 24 runs ≈ 11 GPU-h) checked for parity, invariants and achieved MDE — never for effect direction.
- Success criterion: per-family estimates with artifact-bootstrap CIs per split and split-level spread, reported with intensity and dose; claims read from the results-conditioned matrix; no pre-asserted direction, no equivalence claim.
- Failure interpretation: positive Δ_link^ITT → item-linked histogram information beyond mode and mean at the realised intensity; null → not evidence of absence (intensity ≈ 1/3); Δ_adv ≠ 0 → the adversarial term, not soft labels, carries part of the package gain; family disagreement → report both, no general claim.
- Table / figure target: Table 2, Figure 2.
- Priority: MUST-RUN

### Block 2: Novelty isolation — the randomised-link estimand vs the naive protocols
- Claim tested: that the excluded-rater, calibration-symmetric protocol says something the existing protocols cannot (instrument novelty).
- Why this block exists: reviewers will ask why not just report KL-to-histogram or a held-out annotator group.
- Dataset / split / task: Block 1 and Block 4 runs re-scored under three protocols: (P0) KL/RPS against the fitted pooled histogram (Chen's protocol); (P1) held-out annotator group without evaluator exclusion from calibration (Kohli-style); (P2) ours.
- Compared systems: same three arms.
- Metrics: the soft-vs-hard "gain" each protocol reports, side by side; P0's gain vs P2's calibration-symmetric Δ_soft.
- Setup details: no new training; scoring only.
- Success criterion: P0 reports a large gain that P2 shrinks to a small calibration-symmetric Δ_soft; P1 sits in between.
- Failure interpretation: if all protocols agree, the instrument adds nothing — report honestly, the paper shrinks to the empirical verdict.
- Table / figure target: Table 5 (protocol comparison).
- Priority: MUST-RUN (zero GPU)

### Block 3: Code summarization — analytic boundary only (no GPU runs)
- Claim tested: C1 (two-rater lemma).
- Why this block exists: 3-rater panels are the most common SE regime; with LOO evaluation they leave 2 target raters, for which (z_i, Σy) determines the histogram, so no link randomisation exists.
- Dataset / split / task: Crupi et al. Java + Python (3 raters); the lemma (a ≤ b ⇒ z_i = a, b = Σy − z_i) and the empirical κ = 0 table; no training (the 36 summarization GPU runs were cut on reviewer advice — breadth, not evidence for the dominant contribution).
- Compared systems: none.
- Metrics: κ (= 0) per LOO fold; the lemma.
- Setup details: CPU only.
- Success criterion: the lemma and the enumeration agree (κ = 0).
- Failure interpretation: none (analytic).
- Table / figure target: Table 1 (boundary row).
- Priority: MUST-RUN (zero GPU)

### Block 4: GPU audit on readability — exact Δ_link^ITT at ≈ 0.5 intensity on a low-reliability panel
- Claim tested: C2 (readability part).
- Why this block exists: the highest exact intensity (max-changed .47–.59) but an unreliable disagreement target (keyed-subset split-half ≈ −0.04) and only ≈ 37 test snippets — reported with explicit scoping.
- Dataset / split / task: the locked universe of 124 keyed CoReEval snippets (direct key); three outer splits (60/15/25 to give ≈ 19 calibration snippets); leave-one-rater-out rotation (9 folds, 8 target raters); strata by median agreement; exact matching.
- Compared systems: three arms.
- Metrics: calibrated RPS (coarse calibration grid); Δ_soft and Δ_link^ITT(G) with intensity and dose; five-bin REL/RES/UNC descriptive; wide CIs expected.
- Setup details: 3 arms (A_chen0 nice-to-have) × 9 folds × 3 splits × 2 families = 162 runs × ≈ 0.1 GPU-h ≈ 16 GPU-h.
- Success criterion: estimates with CIs, intensity and dose reported; a positive Δ_link^ITT is evidence of item-linked information; a null is uninformative (unreliable target, small n).
- Failure interpretation: a clear positive Δ_link^ITT despite reliability ≈ −0.04 would show split-half reliability is not a ceiling — reported.
- Table / figure target: Table 2, Figure 2.
- Priority: MUST-RUN (cheap)

### Block 5: Failure analysis / robustness
- Claim tested: robustness of C1 to the audited objective's hyper-parameters and to the decomposition estimator.
- Why this block exists: to pre-empt "you mis-tuned Chen" and "binning artefacts".
- Dataset / split / task: commit messages, one LORO fold, replicate 0, Qwen.
- Compared systems: A_chen / A_perm with (α, ε) at the paper's ablation values; the w = 2 sensitivity arm.
- Metrics: Δ_soft, Δ_bin-link shift.
- Setup details: ≈ 6 extra runs.
- Success criterion: conclusions unchanged in sign and magnitude class.
- Failure interpretation: sensitivity → report the range; if Δ_bin-link depends on ε, the adversarial term interacts with the randomisation and must be discussed.
- Table / figure target: appendix.
- Priority: NICE-TO-HAVE

## Run Order and Milestones
| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|-----------|------|------|---------------|------|------|
| M0 | Block 0: support script + certificates; frozen support model validated; two-rater lemma; subsampled-rater curves; MDE/power simulation; harness fixes; exact objective parity with released code; readability universe locked | CPU + 3 smoke runs | correctness/power gate: certificates, model validation, MDE table, parity and invariant checks | 0.5 GPU-h, 1.5 weeks | adversarial term parity; support model may not validate |
| M1 | Exact commit-Why gate: Block 1, Qwen, split 0, 4 arms × 6 LORO folds | 24 runs | parity (loss values vs reference), invariants (no leakage; certification), achieved MDE vs simulation, resource use — not effect direction | 11 GPU-h | calibration split too small → widen to 15 % |
| M2 | Block 1 complete (What; splits 1–2; Llama) + Block 2 scoring + w = 2 sensitivity | 264 + 24 runs | per-family estimates with CIs, split spread, intensity, dose | 130 GPU-h | family disagreement → report both |
| M3 | Block 4 readability (exact Δ_link^ITT) | 162 runs | estimates with CIs, intensity, dose | 16 GPU-h | small n; wide CIs; unreliable target |
| M4 | Block 5 sensitivity + paper tables/figures | ≈ 6 runs | no sign flips | 3 GPU-h | — |

## Compute and Data Budget
- Total estimated GPU-hours: ≈ 146 (450 LoRA runs) + ≈ 17 sensitivity ≈ 163; ≈ 1.6 weeks on 4 shared RTX 6000 Ada at ~22 GB free each; stage-gated on M0 (correctness/power) and M1 (exact commit-Why gate).
- Data preparation needs: single-criterion prompts (Zeng WHAT/WHY templates; CoReEval readability prompt); readability direct-key loader with the 124-snippet universe locked; support-enumeration + permutation generator with certification; one immutable grouped split per panel; calibration split.
- Human evaluation needs: none.
- Biggest bottleneck: the frozen support model and MDE simulation; parity of Chen's adversarial objective with the released code; the readability alignment fix upstream in the parent pipeline.


## M0 outputs so far (2026-08-23)
- Chen et al. hyper-parameters (from the paper; **no code released**, so the "parity with released code" gate becomes an implementation self-check): α = 0.8 (search grid {0,…,1}), ε = 0.25 (grid {0,…,0.25}), 5 PGA steps of size 0.05 on the target distribution, AdamW 5e-5, 2 epochs, full fine-tuning of Qwen2.5-7B / LLaMA3.1-8B. We use LoRA (r = 16, lr 1e-4) — a documented deviation.
- MDE from pilot variance (diff-clustered SD of the item-level paired RPS difference CE − KL): What SD = .0105 (n = 120 diffs) → 80 %-power MDE ≈ .0027 per split, ≈ .0016 over three splits; Why SD = .0173 → MDE ≈ .0044 per split, ≈ .0026 over three splits. With the exact intervention changing ≈ 0.35 of training items, a full-intensity shape effect of the pilot's size (≈ .003) maps to an ITT effect of roughly .001 — **below the MDE on the commit panel**. Consequences: (i) the M1 gate reports the achieved CI width; (ii) to gain clusters, the design should move from one 60/10/30 split to grouped cross-validation so that every diff is a test item once (400 clusters; MDE ≈ .0024 per replicate on Why), at ≈ 2.5× the run count; (iii) larger multi-rater panels (the user proposes additional datasets) are the real lever — note that sparse-rater datasets (e.g. ≈ 2.7 random raters per item) cannot support rater-identity rotation or exact link randomisation and would serve Δ_soft-type audits only.
- Corrected support audit: see `refine-logs/SUPPORT_AUDIT.md` (commit Why max-changed .33–.37, dose .40).
- Frozen support model: validated and **failed** as a fold-level predictor (commit Why corr −.46, under-prediction −.056; readability −.118) → C1 is the exact empirical enumeration + lemma + dose + subsampled-rater curves (commit Why .34 → .24 → .16 for 5 → 4 → 3 target raters; readability .54 → .52 → .21 for 8 → 6 → 4), not a general bound.
- M1 gate launched 2026-08-23 12:28 (24 runs, Why, split 0, Qwen): `idea-stage/pilot/run_m1.sh`, results under `idea-stage/pilot/results_v2/why/s0/`; analysis `analysis_v2.py`.


## M1 gate result (2026-08-23 14:40) — PASS (correctness / power)
Why · split 0 · Qwen2.5-Coder-7B · 4 arms × 6 LORO folds (24 runs, ≈ 7.4 GPU-h). Invariants: evaluator excluded from targets and calibration (asserted), certificates changed .33–.37 / dose .40, calibration on the untouched split (T = 1.25–2, λ = 0–.05), losses decreased, 120 steps each, 17.4 GB. Calibrated RPS vs the excluded rater: hard .1068 / chen0 .1059 / chen .1061 / perm .1060.
| Contrast | estimate | 95 % CI (diff-clustered, 120 diffs) | per-fold range |
|---|---|---|---|
| Δ_soft = hard − chen | +0.0008 | [−0.0006, +0.0021] | −0.0041 … +0.0024 |
| Δ_adv = chen0 − chen | −0.0001 | [−0.0004, +0.0001] | −0.0006 … +0.0004 |
| Δ_link^ITT = perm − chen (intensity .34, dose .40) | −0.0000 | [−0.0006, +0.0005] | −0.0008 … +0.0009 |
Achieved precision: Δ_link SE ≈ .0003 → MDE(80 %) ≈ .0008 at ITT level, ≈ .0023 at full intensity — an order of magnitude better than the pilot-based MDE, because perm and chen share targets on 66 % of items. Results-conditioned reading (one split, one family): calibrated hard ≈ chen and perm ≈ chen → the Chen-package gain on this panel is small and not attributable to item-linked histogram information beyond mode and mean, at the power available; the adversarial term is inert. Next: replicate on splits 1–2 (Why, Qwen), then What, Llama, readability.


## M2a result (2026-08-23 20:20) — Why replication on three hash-grouped outer splits (Qwen, 72 runs, ≈ 22 GPU-h)
| split | intensity | Δ_soft = hard − chen | Δ_adv = chen0 − chen | Δ_link^ITT = perm − chen |
|---|---|---|---|---|
| 0 | .34 | +0.0008 [−0.0006, +0.0021] | −0.0001 [−0.0004, +0.0001] | −0.0000 [−0.0006, +0.0005] |
| 1 | .31 | +0.0029 [+0.0005, +0.0052] | +0.0003 [−0.0002, +0.0008] | −0.0002 [−0.0008, +0.0003] |
| 2 | .32 | +0.0043 [+0.0020, +0.0066] | +0.0001 [−0.0002, +0.0005] | −0.0001 [−0.0005, +0.0003] |
| pooled (3 splits, independent test diffs) | — | **+0.0027 [+0.0015, +0.0039]** (SD .0018) | +0.0001 [−0.0001, +0.0003] | **−0.0001 [−0.0004, +0.0002]** (SD .0001) |
Results-conditioned reading (claim matrix row "KL > CE but true ≈ permuted"): after symmetric calibration the Chen package beats hard-label CE by ≈ 0.003 RPS on commit Why, the adversarial term is inert, and the exact mode-/mean-/pool-preserving link randomisation on ≈ 32 % of training items costs nothing detectable (MDE ≈ .0005 at ITT level) — the gain is a soft-target regularisation effect, not item-linked histogram information beyond mode and mean. Caveats: one model family so far; ITT at ≈ 1/3 intensity (full-intensity bound ≈ 3× the CI, i.e. |Δ_link| ≲ .0012 RPS); commit panel only.

## M3 readability implementation note (2026-08-23)
Panel = 124 keyed CoReEval snippets (direct key), 9-rater LORO, grouped split 60/15/25, tokens "1"–"5" ↔ levels 0–4. Prompt = CoReEval senior zero-shot Java template **with the scale changed from 0–20 to 1–5** (so the score-token distribution matches the 5-level human target) — a documented deviation from verbatim. Queued (4 arms × 9 folds × 3 splits = 108 runs, Qwen) after the DeepSeek commit runs.


## M2b-1 result (2026-08-24 04:10) — What, Qwen, three outer splits (72 runs, ≈ 22 GPU-h)
| split | intensity | Δ_soft | Δ_adv | Δ_link^ITT |
|---|---|---|---|---|
| 0 | .30 | +0.0016 [+0.0010, +0.0023] | +0.0002 | +0.0001 [−0.0002, +0.0004] |
| 1 | .32 | +0.0034 [+0.0023, +0.0046] | +0.0004 | +0.0001 [−0.0003, +0.0005] |
| 2 | .33 | −0.0011 [−0.0020, −0.0001] | −0.0005 | −0.0004 [−0.0008, −0.0001] |
| pooled | — | **+0.0013 [+0.0008, +0.0019]** (SD .0023 — split-heterogeneous) | −0.0000 | **−0.0001 [−0.0003, +0.0001]** |
Same picture as Why: no detectable item-linked component at ≈ 1/3 intensity; the soft-target effect is small and varies by split (split 2 negative). DeepSeek-Coder-6.7B (second family) queues running; readability chained after.


## M2b-2 partial result (2026-08-24 13:25) — Why, DeepSeek-Coder-6.7B (second family), three outer splits (72 runs)
| split | Δ_soft | Δ_adv | Δ_link^ITT |
|---|---|---|---|
| 0 | +0.0025 [+0.0011, +0.0039] | +0.0005 | −0.0001 [−0.0007, +0.0005] |
| 1 | +0.0049 [+0.0024, +0.0076] | −0.0005 | −0.0006 [−0.0010, −0.0001] |
| 2 | +0.0023 [−0.0007, +0.0050] | −0.0011 | +0.0006 [−0.0001, +0.0013] |
| pooled | **+0.0032 [+0.0019, +0.0046]** | −0.0004 [−0.0008, +0.0000] | **−0.0000 [−0.0004, +0.0003]** |
RPS levels ≈ .137–.140 (weaker judge than Qwen's ≈ .106). The second family replicates the Qwen pattern: a small real soft-target (Chen-package) gain, an inert (here marginally harmful) adversarial term, and no detectable item-linked component at ≈ 1/3 intensity. What (DeepSeek) running; readability queued.


## M2b-2 complete (2026-08-24 22:10) — What, DeepSeek-Coder-6.7B, three outer splits (72 runs; family total 144)
| split | Δ_soft | Δ_adv | Δ_link^ITT |
|---|---|---|---|
| 0 | +0.0034 [+0.0022, +0.0047] | −0.0000 | −0.0001 [−0.0004, +0.0002] |
| 1 | +0.0051 [+0.0034, +0.0070] | −0.0003 | +0.0000 [−0.0004, +0.0005] |
| 2 | +0.0022 [+0.0006, +0.0037] | −0.0000 | +0.0008 [+0.0003, +0.0013] |
| pooled | **+0.0036 [+0.0027, +0.0045]** | −0.0001 [−0.0003, +0.0001] | **+0.0002 [−0.0000, +0.0005]** |
Pooled Δ_link remains compatible with 0; the split-2 cell is the single nominally-positive cell among the 12 commit (criterion × family × split) cells — consistent with chance at the 5 % level and reported without over-reading. **Commit-panel matrix now complete: Δ_soft positive and replicated in all four (criterion × family) cells (+0.0013 … +0.0036); Δ_adv ≈ 0 in all four; Δ_link^ITT ≈ 0 in all four (pooled CIs within ±0.0005).**


## M3 complete (2026-08-24 23:20) — readability, Qwen2.5-Coder-7B, 9 LORO folds × 3 splits (108 runs)
| split | changed | Δ_soft | Δ_adv | Δ_link^ITT |
|---|---|---|---|---|
| 0 | .539 | +0.0008 [−0.0010, +0.0024] | +0.0012 [+0.0005, +0.0019] | +0.0000 [−0.0002, +0.0003] |
| 1 | .581 | −0.0002 [−0.0011, +0.0006] | +0.0009 [+0.0005, +0.0013] | +0.0000 [−0.0001, +0.0002] |
| 2 | .526 | −0.0030 [−0.0042, −0.0017] | −0.0004 [−0.0008, +0.0000] | −0.0006 [−0.0010, −0.0002] |
| pooled | .55 | **−0.0008 [−0.0017, −0.0000]** | +0.0006 [+0.0002, +0.0009] | **−0.0002 [−0.0004, −0.0000]** |
RPS: hard .1533 / chen0 .1547 / chen .1541 / perm .1539. Pooled over 3 snippet-hash splits, snippet-clustered bootstrap (B = 2000); `results_v2/readability/pooled.json`.
Reading: on the **highest-intensity cell** (exact matching changes .53–.58 of training histograms) the link randomisation costs nothing — Δ_link is ≈ 0 (marginally negative, i.e. the permuted-histogram model is indistinguishable from the true one). Moreover the Chen package itself gives **no gain at all** here (Δ_soft marginally negative, split-heterogeneous: split 2 −0.0030). Δ_adv is the one cell with a nominally positive adversary effect (+0.0006) — trivial in magnitude. Pre-registered scoping applies: keyed-subset dispersion reliability ≈ −0.04, so the readability nulls are reported as intensity-qualified nulls on an unreliable panel, never as "judges cannot learn disagreement".

## Final six-cell results matrix (all pooled over 3 outer splits; 2026-08-24)
| cell (panel × criterion × family) | intensity | Δ_soft = hard−chen | Δ_adv = chen0−chen | Δ_link^ITT = perm−chen |
|---|---|---|---|---|
| commit Why × Qwen2.5-Coder-7B | .33 | **+0.0027 [+0.0015, +0.0039]** | +0.0001 [−0.0001, +0.0003] | −0.0001 [−0.0004, +0.0002] |
| commit What × Qwen2.5-Coder-7B | .30 | **+0.0013 [+0.0008, +0.0019]** | −0.0000 | −0.0001 [−0.0003, +0.0001] |
| commit Why × DeepSeek-Coder-6.7B | .33 | **+0.0032 [+0.0019, +0.0046]** | −0.0004 [−0.0008, +0.0000] | −0.0000 [−0.0004, +0.0003] |
| commit What × DeepSeek-Coder-6.7B | .32 | **+0.0036 [+0.0027, +0.0045]** | −0.0001 [−0.0003, +0.0001] | +0.0002 [−0.0000, +0.0005] |
| readability × Qwen2.5-Coder-7B | **.55** | −0.0008 [−0.0017, −0.0000] | +0.0006 [+0.0002, +0.0009] | −0.0002 [−0.0004, −0.0000] |
| (2-rater panels, e.g. summarization 3-rater LORO) | 0 | — | — | identified 0 by the two-rater lemma |

**Results-conditioned claim (claim-matrix row "KL > CE on commit, but true ≈ permuted everywhere"):**
1. Δ_soft is real, positive and cross-family-replicated on the commit panel (4/4 cells, +0.0013 … +0.0036 RPS) — but it vanishes (marginally reverses) on readability.
2. Δ_adv ≈ 0 in 5/6 cells (readability +0.0006 the exception, trivial): the adversarial term of the Chen objective is inert at these scales.
3. Δ_link^ITT ≈ 0 in every cell, including the .55-intensity readability cell (per-split |Δ| ≤ 0.0008; the one nominally-positive commit cell is 1 of 12 at the 5 % level). At the achieved intensities, **none of the soft-label gain is attributable to item-linked histogram information beyond mode and mean** — what the KL objective buys is soft-target regularisation, and even that is panel-dependent.
4. Licensing: the paper may claim (a) the feasibility/identifiability analysis (support map, two-rater lemma, MDE), and (b) "on released SE panels, distributional fine-tuning gains are calibration/regularisation effects; we detect no item-linked disagreement learning at intensity .3–.55 with MDE ≈ .0005" — with the readability cell scoped by its ≈ −0.04 dispersion reliability. It may NOT claim disagreement learning is impossible, nor extrapolate beyond the achieved intensity/dose.

## Risks and Mitigations
- Partial intervention intensity (≈ 1/3 on commit): reported as treatment intensity with dose; MDE computed before running; nulls never read as absence; Δ_bin-link only as a bounded-confounding sensitivity (never an upper bound).
- Δ_soft is an objective-package contrast: the no-adversary arm A_chen0 separates the adversarial term (must-run on commit).
- Randomisation distribution: G is a randomised maximum matching with its own seed, independent of data order; one draw per outer split.
- Effects of ≈ 0.002 RPS below detectability: MDE simulation first; artifact-bootstrap CIs per split, split-level spread as replication uncertainty, families separate; no equivalence claims; no rater-population inference.
- Chen objective not reproducible exactly: document deviations; sensitivity row (Block 5).
- Summarization 2-rater targets degenerate: report as boundary; Block 3 interpretation limited.
- Parent-paper overlap: the contribution is the feasibility result (estimand, support quantities, dose, frozen support model, two-rater lemma, MDE) and the scoped audit; CSJE reused only as plumbing.
- Pseudo-novelty (matching conditions are standard; the lemma is simple): the general, validated support model and the MDE-based guidance must carry the novelty — M0 deliverable; if they fail, pivot to Package B (offline best-of-n on the fully rated summary pools).

## Final Checklist
- [ ] Main paper tables are covered (Tables 1–5, Figure 1)
- [ ] Novelty is isolated (Block 0 support result; Block 2 protocol comparison)
- [ ] Simplicity is defended (three arms; every cut component listed as "intentionally cut")
- [ ] Frontier contribution is justified or explicitly not claimed (explicitly not claimed)
- [ ] Nice-to-have runs are separated from must-run runs
