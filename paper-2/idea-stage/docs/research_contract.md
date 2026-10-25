# Research Contract: Identifiability Audit of Soft-Label LLM-Judge Training on Small SE Annotator Panels

> **A focused working document for the currently selected idea.** Created when an idea is chosen from `IDEA_REPORT.md`, updated throughout implementation and training. This is what the LLM reads on session recovery — not the full IDEA_REPORT with all 48 candidates.

## Selected Idea

- **Description**: Soft-label / distributional fine-tuning of LLM judges (Chen et al. NeurIPS 2025 and successors) is validated against the pooled rating histogram it was trained on. On the 3–9-rater panels of released SE benchmarks, we (i) state the finite-sample feasibility of the clean attribution instrument — training on histograms re-assigned by a randomised maximum-cardinality exact matching among artifacts that share pool, point label z_i and rating sum, so only the artifact→shape link is broken — with three support quantities and the dose (corrected audit: max-changed fraction .25–.32 commit What, .33–.37 commit Why, .47–.59 readability, 0 with two target raters; dose ≈ .40 TV), a frozen support model, the two-rater lemma and MDE/power guidance; and (ii) audit what the panels can support: the excluded-rater, symmetrically calibrated Chen-package gain Δ_soft, its no-adversary decomposition Δ_adv, and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability, per family, with Δ_bin-link (w = 2) as a sensitivity.
- **Source**: `idea-stage/IDEA_REPORT.md`, Package A (contradiction#1 + scaling#4 + method-transfer#1 + training-signal#3) as reframed by the novelty check, the external review and 5 refinement rounds; `refine-logs/FINAL_PROPOSAL.md`.
- **Selection rationale**: Codex-ranked #1 of 48 candidates; pilot evidence that the Chen-style gain is mostly calibration (calibrated CE − KL = +0.0008 [−0.0001, +0.0017] What / +0.0018 [+0.0005, +0.0031] Why); the alternatives (Bayesian small-panel target, gain routing) failed their pre-registered pilots and are near-scooped (Kohli 2605.29797, Peale 2605.07805); the support audit turned the attribution idea into a feasibility-plus-scoped-audit paper; the external plan review (PROCEED WITH CAUTION) corrected the support definition and made exact commit-Why the primary experiment.

## Core Claims

1. **C1 (feasibility, CPU)**: Under randomised maximum-cardinality exact matching on the hash-grouped split the intervention can change .25–.32 (commit What), .33–.37 (commit Why), .47–.59 (readability) of training artifacts at dose ≈ .40 TV, and 0 with two target raters (lemma); a frozen support model validated out of sample predicts these intensities (else C1 is the empirical audit); MDE/power simulations give the minimum detectable Δ_link per panel.
2. **C2 (scoped audit, GPU)**: For the exact Chen objective with a matched no-adversary control, Δ_soft, Δ_adv and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability are per-family estimates with artifact-bootstrap CIs, split-level spread, intensity and dose; a positive Δ_link^ITT is evidence of item-linked histogram information beyond mode and mean; a null at partial intensity does not establish absence.
3. **Scope/limitation claim**: no new training objective; Δ_bin-link is neither an upper bound nor identified conditional resolution; no population claims beyond the released panels; results conditional on the fixed split and trained replicas.

## Method Summary

Stage 0 (CPU, primary evidence; `idea-stage/pilot/support_audit.py`): for each panel, criterion and evaluator rotation on hash-grouped outer splits, compute z_i (mode; ties → closest to the target median, then lower), exact cells (pool, z_i, Σy), the randomised maximum-cardinality matching G (changes min{N, 2(N−M)} items per heterogeneous cell), full-cell / max-changed / positive-probability fractions and the TV dose; freeze a support model (cell occupancy × histogram-class frequencies × key) and validate it on held-out splits / synthetic panels; state the two-rater lemma; run MDE/power simulations from pilot variance × intensity × dose; w = 2 only as a sensitivity.

Stage 1 (GPU): three hash-grouped 60/10/30 outer splits per panel (readability 60/15/25), each with independent optimiser and permutation seeds; leave-one-rater-out rotation (commit 6 folds, readability 9); evaluator raters excluded from every target and from calibration. Four arms on the full training set (commit; three on readability): A_hard = CE(z_i, q); A_chen0 = α·KL + (1−α)·CE(z_i) (no adversary); A_chen = exact Chen objective incl. the adversarial term (parity-tested vs released code); A_perm = A_chen with histograms re-assigned by G in heterogeneous cells (identity elsewhere). Symmetric arm-specific calibration C_A(q) = (1−λ_A)·softmax(log q/T_A) + λ_A·p_clim fitted per arm on the calibration split using target raters only (coarse grid on readability; refitting uncertainty bootstrapped). Score every arm against the excluded rater with RPS; Δ_soft = hard − chen; Δ_adv = chen0 − chen; Δ_link^ITT = perm − chen (exact), Δ_bin-link at w = 2 sensitivity; five-bin REL/RES/UNC descriptive. Inference: per family, per outer split an artifact bootstrap (B = 2000) of item-level paired differences averaged over the split's folds; split-level spread as replication uncertainty; intensities and dose reported with every estimate.

## Experiment Design

- **Datasets**: commit messages (Zeng et al.; 800 × 6 raters; What, Why; single-criterion prompts); readability (CoReEval/Scalabrino; the 124 keyed snippets × 9 raters; direct `snippet_id ↔ SnippetN` key via our own loader; the parent scripts' fix is deferred by user decision); code summarization (Crupi et al.; 3 raters) — analytic boundary only.
- **Baselines**: A_hard (point-label SFT), A_chen0 (no adversary), A_chen (exact Chen); protocols P0 (Chen's pooled-histogram scoring) and P1 (Kohli-style held-out annotator group) re-scored on the same runs.
- **Metrics**: full-cell / max-changed / positive-probability fractions, dose and MDE per panel (primary for C1); calibrated held-out-rater RPS, Δ_soft, Δ_adv, Δ_link^ITT with CIs, split spread, intensity and dose per family (primary for C2); five-bin REL/RES/UNC (descriptive).
- **Key hyperparameters**: LoRA r = 16, α = 32, dropout 0.05, lr 1e-4, 2 epochs, accum 8; Chen (α, ε*, steps) from the released configuration; calibration grid T ∈ {0.5 … 6} × λ ∈ {0 … 0.5} (coarse on readability); exact cells (w = 1); B = 2000.
- **Compute budget**: 450 LoRA runs ≈ 146 GPU-h (+ ≈ 17 sensitivities) on 4 shared RTX 6000 Ada (~22 GB free each), stage-gated on M0 (correctness/power) and the M1 exact commit-Why gate (24 runs).

## Baselines

| Method | Dataset | Metric | Score | Source |
|--------|---------|--------|-------|--------|
| zero-shot Qwen2.5-Coder-7B | commit (240-item test split, all 6 raters) | held-out-rater RPS What / Why | .114 / .322 | pilot (`idea-stage/pilot/results/base_zeroshot`) |
| CE to pooled median (A_hard-like) | commit | RPS What / Why (raw; calibrated) | .103 / .123 (.099 / .109) | pilot (`ce_median_s0`) |
| KL + ½ CE (Chen-style core, no adversarial term) | commit | RPS What / Why (raw; calibrated) | .098 / .112 (.098 / .107) | pilot (`kl_soft_s0`) |
| KL on median-matched permuted histograms | commit | RPS What / Why (raw; calibrated) | .099 / .113 (.099 / .110) | pilot (`kl_soft_permuted_s0`) |
| climatology / 5-rater panel predictive | commit | RPS What / Why | .159 / .175 and .095 / .100 | pilot |

## Current Results

> Pilot-stage only (one model, one seed, 120 independent diffs; not the final protocol — rater identities were not excluded from targets).

| Method | Dataset | Metric | Score | Notes |
|--------|---------|--------|-------|-------|
| calibrated CE − KL | commit What | RPS Δ | +0.0008 [−0.0001, +0.0017] | cluster-by-diff CI; RES .0630 vs .0644 |
| calibrated CE − KL | commit Why | RPS Δ | +0.0018 [+0.0005, +0.0031] | RES .0710 vs .0716 |
| calibrated permuted − true KL | commit Why | RPS Δ | +0.0030 [+0.0016, +0.0045] | small histogram-specific component |
| max-changed fraction (exact cells, randomised max matching, grouped split) | commit What / Why, LORO | intensity | .25–.32 / .33–.37 (dose .40) | `refine-logs/SUPPORT_AUDIT.md`, `idea-stage/pilot/results/support_audit.json` |
| max-changed fraction | readability (124 keyed), LORO | intensity | .47–.59 (dose .28) | |
| max-changed fraction | summarization, LOO | intensity | 0 (lemma) | |

| **M1 gate (final protocol)**: Δ_link^ITT = perm − chen | commit Why, split 0, Qwen, 6 LORO folds | RPS Δ | −0.0000 [−0.0006, +0.0005] | intensity .34, dose .40; gate PASS |
| M1: Δ_soft = hard − chen | same | RPS Δ | +0.0008 [−0.0006, +0.0021] | |
| M1: Δ_adv = chen0 − chen | same | RPS Δ | −0.0001 [−0.0004, +0.0001] | adversarial term inert |
| **M2a pooled (3 outer splits)**: Δ_soft | commit Why, Qwen | RPS Δ | +0.0027 [+0.0015, +0.0039] | small real Chen-package gain |
| M2a pooled: Δ_adv | same | RPS Δ | +0.0001 [−0.0001, +0.0003] | inert |
| M2a pooled: Δ_link^ITT (intensity .31–.34) | same | RPS Δ | −0.0001 [−0.0004, +0.0002] | no item-linked information beyond mode & mean detectable |
| **M2b-1 pooled (What, Qwen, 3 splits)**: Δ_soft | commit What | RPS Δ | +0.0013 [+0.0008, +0.0019] | split-heterogeneous (split 2 negative) |
| M2b-1 pooled: Δ_link^ITT (intensity ≈ .32) | same | RPS Δ | −0.0001 [−0.0003, +0.0001] | replicates the Why null |
| **M2b-2 pooled (Why, DeepSeek, 3 splits)**: Δ_soft | commit Why | RPS Δ | +0.0032 [+0.0019, +0.0046] | second family, same pattern |
| M2b-2 pooled: Δ_link^ITT | same | RPS Δ | −0.0000 [−0.0004, +0.0003] | cross-family replication of the null |
| **M2b-2 pooled (What, DeepSeek, 3 splits)**: Δ_soft | commit What | RPS Δ | +0.0036 [+0.0027, +0.0045] | strongest soft-target gain |
| M2b-2 pooled: Δ_link^ITT | same | RPS Δ | +0.0002 [−0.0000, +0.0005] | split-2 cell +0.0008 nominally positive (1 of 12 cells; chance-consistent) |
| **M3 pooled (readability, Qwen, 3 splits, intensity .55)**: Δ_soft | readability | RPS Δ | −0.0008 [−0.0017, −0.0000] | no Chen-package gain on this panel |
| M3 pooled: Δ_adv | same | RPS Δ | +0.0006 [+0.0002, +0.0009] | only nominally-positive adversary cell; trivial |
| M3 pooled: Δ_link^ITT | same | RPS Δ | −0.0002 [−0.0004, −0.0000] | highest-intensity cell; true ≈ permuted; scoped by panel reliability ≈ −0.04 |

## Key Decisions

- Reframed from "attribution audit" to "feasibility + scoped audit" after the support audits: the external plan review corrected the support notion (maximum matching, not full-cell derangeability) — exact randomisation is feasible at ≈ 1/3 intensity on commit Why, which is therefore the primary experiment; the paper states feasibility, dose and MDE, and reports scoped estimates.
- Four arms on commit (hard, no-adversary control, exact Chen, permuted); single point label z_i everywhere; full-data intent-to-treat randomisation with a randomised maximum matching whose seed is independent of data order; every fold included with intensity and dose; families reported separately; no "upper bound" language for Δ_bin-link; gates test correctness and power, never effect direction.
- Evaluator-identity exclusion (LORO) and symmetric arm-specific calibration on an untouched split — the two fixes the round-1 external review required.
- Summarization: no GPU runs (two-rater impossibility is analytic); readability universe locked to the 124 keyed snippets (dispersion reliability ≈ −0.04 there; small n).
- Known risks: the frozen support model may not validate (pseudo-novelty); Chen parity; upstream readability fix; Δ_link possibly under-powered at ≈ 1/3 intensity (MDE first); pivot option = Package B (offline best-of-n on fully rated summary pools).

## Status

- [x] Idea selected
- [x] Pilot baselines reproduced (commit messages, one seed)
- [x] Baseline reproduced under the final protocol (M1 gate PASS, 2026-08-23)
- [x] Main method implemented (exact Chen objective + no-adversary variant, randomised maximum matching with certificates, LORO rotation, calibration split) — `idea-stage/pilot/train_judge_v2.py`
- [x] Representative dataset results (commit Why, Qwen, 3 splits) — What and second family running
- [x] Full dataset results: SIX-CELL MATRIX COMPLETE — commit (2 criteria × 2 families) + readability + two-rater lemma; final matrix in EXPERIMENT_PLAN.md
- [ ] Ablation studies (sensitivity row; protocol comparison)
- [ ] Paper draft
