# Research Proposal: When Do Soft-Label LLM Judges Add Conditional Resolution Beyond Calibration? An Attribution Audit on Small SE Annotator Panels

## Problem Anchor
- **Bottom-line problem**: Training-side claims that an LLM judge "models human disagreement" (soft-label / distributional fine-tuning, Chen et al. NeurIPS 2025 and successors) are validated against the same pooled rating histogram they were trained on. On the small annotator panels that software-engineering benchmarks actually have (3–9 raters), we need a way to tell whether such a judge learned *which artifacts* split human raters, or merely learned a better-calibrated (smoother) score distribution plus scale-location effects.
- **Must-solve bottleneck**: The existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing; a judge can post large KL/RPS gains over point-SFT while carrying zero item-level disagreement information, and uncertainty-based downstream decisions (routing contested items to humans) inherit that ambiguity.
- **Non-goals**: Not a new judge-training method as the headline; not pairwise preference / reward-model training; not RL judges; not a new multi-rater benchmark; not claims about human populations beyond the released panels; not generation-side (DPO/best-of-n) consequences.
- **Constraints**: Released per-annotator data only (commit messages 800×6, code summarization 1,163×3, readability 200×9); 7B–14B open judges with LoRA on 4 shared RTX 6000 Ada (~22 GB free each) plus small OpenRouter budget for frontier judges as *untrained* references; single PhD student, ~3 months to submission; venue ICSE/FSE (primary) or ACL/NeurIPS Datasets & Benchmarks; parent paper's CSJE/HCA machinery is reusable and must stay consistent with it.
- **Success condition**: A protocol (target-reliability diagnostic → location-aware nulls → label-preserving attribution against held-out individual raters by consensus stratum) that, applied to Chen-style distributional judges on the three SE panels with ≥ 3 seeds and ≥ 2 model families, yields a definite, replicated verdict on whether the distributional gain is item-specific — and that a sceptical reviewer accepts as the right way to audit future "disagreement-aware judge" claims. A positive item-specific residual on some criterion/panel and a null on others is an acceptable (indeed informative) outcome.

## Technical Gap
Soft-label judge training (Chen et al. 2505.12301: KL to the empirical histogram + CE to the majority + adversarial ε-ball; Li et al. 2510.00263; Singh et al. 2511.14117) is scored by KL/accuracy against the *same pooled histogram* it was fitted to. Three things make that score uninterpretable as evidence of "learned disagreement":
1. **Calibration absorbs most of it.** A proper score (RPS/Brier) decomposes into reliability − resolution + uncertainty. A globally calibrated point-label judge can match a soft-label judge on RPS while having identical *resolution* (item-conditioned information). Our pilot (commit messages, Qwen2.5-Coder-7B LoRA, 240 test items, cluster-by-diff CIs) shows exactly this: the raw CE→KL gain (+0.004 What / +0.011 Why RPS) shrinks to +0.0008 [−0.0001, +0.0017] / +0.0018 [+0.0005, +0.0031] after one shared temperature + climatology calibrator is applied symmetrically to both arms; resolution terms are .0630 vs .0644 (What) and .0710 vs .0716 (Why).
2. **Scale location masquerades as disagreement.** On bounded ordinal scales the Low-consensus stratum is predictable from the pooled *median* alone (AUROC .67 What / .80 Why); judge-entropy "disagreement detection" collapses from .78 to ≈ .58–.64 after cross-fitted residualisation on the expected score.
3. **Small panels make the target itself unreliable.** Split-half Spearman of per-item dispersion across disjoint rater halves is .22 (What) / .36 (Why) on 6 raters and ≈ .02 on the 9-rater readability panel; nobody reports this before claiming a judge learned it. Averaging a held-out-rater score over all raters is moreover algebraically the pooled-histogram score (plus a model-free constant), so "held-out rater" evaluation must hold out *rater identities* from target construction, not just rating cells.
Naive fixes do not close the gap: more raters are unavailable; a heavier Bayesian target (Kohli 2605.29797; our k = 2 pilot) over-shrinks; ordinal losses (CRPS) tie with KL; an adversarial ε-ball is a regulariser, not an identification strategy. What is missing is an **audit** that separates calibration, location and item-conditioned resolution with label-preserving randomisation of the training target.

## Method Thesis
- **One-sentence thesis**: Soft-label fine-tuning of an LLM judge improves prediction of a new human rating mostly through global calibration; an attribution audit — symmetric validation-fitted calibration, threshold-Brier resolution, location residualisation, and training on *conditionally permuted* histograms that preserve each item's pooled label and location but break its link to the item — isolates the item-conditioned component and shows when (as a function of split-panel disagreement reliability) it is non-zero.
- **Why this is the smallest adequate intervention**: every component is a statistical control on top of the *existing* training pipeline (no new model, no new loss as a contribution); the only new training runs are placebo targets.
- **Why this route is timely in the foundation-model era**: distributional/soft-label judges and reward models are proliferating (NeurIPS 2025, ICML 2025/2026 lines); the audit is what lets the community read their numbers.

## Contribution Focus
- **Dominant contribution**: the attribution audit (estimand + controls + randomisation) and its empirical verdict on Chen-style soft-label judges across the three released multi-rater SE benchmarks with replication (2 model families × 3 seeds × several permutations, rater-identity-disjoint evaluation).
- **Optional supporting contribution**: the boundary condition — item-conditioned resolution gain as a function of split-panel disagreement reliability and panel size (k ∈ {2, 3, 5, full}).
- **Explicit non-contributions**: no new training objective is claimed (CRPS / posterior-predictive / adversarial variants appear only as audited arms); no routing system; no new metric beyond the RPS-based distributional skill score used as a reporting convenience (an HCA analogue, not advertised as novel).

## Proposed Method
### Complexity Budget
- Frozen / reused backbone: Qwen2.5-Coder-7B-Instruct and a second family (Llama-3.1-8B-Instruct or Qwen3-8B); verbatim benchmark prompts; LoRA r = 16; the parent paper's CSJE strata and HCA code.
- New trainable components: none beyond LoRA adapters per arm.
- Tempting additions intentionally not used: per-rater conditioning / annotator embeddings; RL judges; EB posterior-predictive "method"; gain-routing head; frontier API fine-tuning.

### System Overview
```
per-annotator ratings H (n × m)  ──►  split by source artifact: train / calibration / test (grouped by diff / function)
        │                                   │
        ├─ rater-identity rotation: rater r excluded from ALL targets (train+calib), used only as evaluator
        ▼
training targets per item (from the m−1 remaining raters):
   T1 hard rounded-median CE  · T2 tie-aware location-only target (two-hot adjacent levels when the median is a half-integer)
   T3 true histogram (KL + CE, Chen scaling)  · T4 exact Chen objective incl. adversarial ε-ball
   T5 conditionally permuted histograms (s permutations; within cells of (rounded median, pool, mean-bin))
        ▼
LoRA judge → score-token distribution q(x) on test items
        ▼
ONE shared calibrator (T, λ) fitted on the calibration split, applied to EVERY arm
        ▼
scoring against the excluded rater r: RPS_r, threshold-Brier REL / RES / UNC, location-residualised entropy→Low AUROC,
distributional skill (climatology = 0, (m−1)-rater panel predictive = 1); strata from the m−1 raters; inference clustered by artifact and two-way item × rater
```

### Core Mechanism
- Input / output: artifact + prompt → q(x) ∈ Δ⁴ over the Likert levels; evaluator = one human rating never used in any target.
- Architecture or policy: unchanged judge; the *experimental design* is the mechanism: symmetric calibration (removes reliability differences), conditional permutation (removes the item→dispersion link while preserving label, pool and location), rater-identity holdout (removes panel memorisation).
- Training signal / loss: T1–T5 as above; all arms share optimiser, steps, seeds; Why scored independently of What (separate prompts or same conditioning at train and test).
- Why this is the main novelty: prior distributional-judge work (Chen, Li, Zhang 2410.14632, Kohli 2605.29797, Gheibi 2605.20642) either evaluates on the fitted histogram, uses a global shuffle that destroys the label, or calibrates only the point model; none isolates item-conditioned resolution against an unseen rater.

### Optional Supporting Component
- Only include if truly necessary: panel-size sweep k ∈ {2, 3, 5, full} with identical loss construction, several rater subsets, evaluation only on identities outside the subset; regress the resolution gain on split-half reliability.
- Why it does not create contribution sprawl: same arms, same metrics; it is the x-axis of the main figure, not a new method.

### Modern Primitive Usage
- Which primitive: open-weight instruction LLM as the judge (score-token distribution read from logits); frontier API judges only as untrained references for context.
- Exact role: the audited object. No frontier primitive is central; the paper is intentionally non-frontier on the method side and says so.

### Integration into Base Generator / Downstream Pipeline
Attaches to the parent paper's CSJE pipeline: same strata, same held-out-human reference; adds the training-side audit as RQ-level machinery. Everything except LoRA adapters is frozen; inference = one forward pass per item per criterion.

### Training Plan
- Splits: 60/10/30 by diff (commit) / function (summarization) / snippet (readability), 3 split seeds.
- Arms per (benchmark, criterion, model family, seed): T1, T2, T3, T4, T5 × s = 3 permutations → 7 LoRA runs; ≈ 25 min each on a 7B at ~1k tokens.
- Rater rotation: for commit (6) and readability (9) rotate the excluded rater over all identities for T1/T3/T5 (targets recomputed per rotation); for summarization (3 raters) use leave-one-out only as a secondary analysis (2-rater targets).
- Calibration: (T, λ) by minimising mean RPS on the calibration split against the m−1 available raters; fixed thereafter.

### Failure Modes and Diagnostics
- Calibrated CE ≈ calibrated KL everywhere → the audit's main result is "no resolution gain"; still publishable as the boundary-condition paper if the reliability sweep explains it.
- Permutation leaks location (mean drift) → report preserved-statistics table for every permutation; add mean-bin conditioning; if residual drift remains, use within-cell re-sampling of raters instead of histogram swaps.
- Rater rotation too expensive on 9 raters → rotate a stratified subset of 4 identities and report rater-level CIs.
- Readability panel unreliable (split-half ≈ .02) → pre-registered expectation of a null; report as such.
- Summarization 3-rater panels → only 2-rater targets; flag as low-power.

### Novelty and Elegance Argument
Closest work: Chen 2505.12301 (method audited), Kohli 2605.29797 (small-panel Dirichlet targets; held-out annotator group; no symmetric calibration, no permutation, no rater-identity holdout, NLI classification), Gheibi 2605.20642 (global shuffle that destroys the label), Calderon 2501.10970 (leave-one-annotator-out for point judges), Zhang 2410.14632 (agreement-stratified RM evaluation without a human reference). The delta is a single coherent identification design — calibration-symmetric, label-preserving, rater-identity-disjoint, resolution-decomposed — and its application to SE judging where panels are small and the parent protocol already exists. No module pile-up; one table family answers one question.

## Claim-Driven Validation Sketch
### Claim 1 (main): On small SE panels, the held-out-rater gain of soft-label fine-tuning over point-label fine-tuning is mostly reliability; the item-conditioned resolution gain is ≤ 0.003 RPS and is non-zero only where split-panel disagreement reliability is ≥ ≈ 0.3 (commit Why).
- Minimal experiment: commit messages, 2 model families × 3 seeds, arms T1–T5, rater-identity-disjoint rotation, shared validation-fitted calibrator; report calibrated CE − KL, permuted − true, REL/RES/UNC per stratum with cluster-by-diff and two-way CIs and TOST equivalence at ± 0.002 RPS.
- Baselines / ablations: T2 (tie-aware location target) separates half-integer-median effects; T4 checks that the exact adversarial objective does not change the verdict.
- Metric: RPS against the excluded rater; resolution RES; distributional skill.
- Expected evidence: What — equivalence; Why — small positive resolution gain reproduced across seeds/families.
### Claim 2 (supporting): The resolution gain tracks split-panel disagreement reliability, not contested mass or panel size per se.
- Minimal experiment: same arms on code summarization (3 raters) and correctly aligned readability (9 raters) + panel-size sweep on commit messages.
- Baselines / ablations: location-only null; rater-subset seeds separated from model seeds.
- Metric: resolution gain vs split-half reliability (per criterion/panel), with rater-level uncertainty.
- Expected evidence: monotone relation; null on readability.

## Experiment Handoff Inputs
- Must-prove claims: C1, C2.
- Must-run ablations: T2 tie-aware target; T4 exact Chen objective; permutation count s = 3 with preserved-statistics table; symmetric vs asymmetric calibration; rater-identity-disjoint vs cell-holdout evaluation.
- Critical datasets / metrics: commit messages (primary), summarization, readability (correct key); RPS vs excluded rater, REL/RES/UNC, location-residualised AUROC, skill score.
- Highest-risk assumptions: that resolution differences of ~0.002 RPS are detectable with 120–400 independent artifacts; that the adversarial objective can be reproduced faithfully; that readability strata/scripts are corrected in the parent pipeline first.

## Compute & Timeline Estimate
- Estimated GPU-hours: commit factorial 2 families × 3 seeds × 7 arms × ~0.45 h ≈ 19 h, + rater rotations for T1/T3 (×6) ≈ 30 h, + summarization & readability ≈ 25 h, + panel-size sweep ≈ 20 h → ≈ 95 GPU-h (within 50–150 reviewer envelope; < 1 GPU-week on 4 shared cards).
- Data / annotation cost: none (released data); readability alignment fix required.
- Timeline: repairs + commit factorial 3 weeks; breadth 3 weeks; writing 3 weeks.
