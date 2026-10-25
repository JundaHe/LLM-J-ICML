# Round 4 Refinement (reframing)

## Problem Anchor
- **Bottom-line problem**: Training-side claims that an LLM judge "models human disagreement" (soft-label / distributional fine-tuning, Chen et al. NeurIPS 2025 and successors) are validated against the same pooled rating histogram they were trained on. On the small annotator panels that software-engineering benchmarks actually have (3–9 raters), we need a way to tell whether such a judge learned *which artifacts* split human raters, or merely learned a better-calibrated (smoother) score distribution plus scale-location effects.
- **Must-solve bottleneck**: The existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing; a judge can post large KL/RPS gains over point-SFT while carrying zero item-level disagreement information, and uncertainty-based downstream decisions (routing contested items to humans) inherit that ambiguity.
- **Non-goals**: Not a new judge-training method as the headline; not pairwise preference / reward-model training; not RL judges; not a new multi-rater benchmark; not claims about human populations beyond the released panels; not generation-side (DPO/best-of-n) consequences.
- **Constraints**: Released per-annotator data only (commit messages 800×6, code summarization 1,163×3, readability 200×9); 7B–14B open judges with LoRA on 4 shared RTX 6000 Ada (~22 GB free each) plus small OpenRouter budget for frontier judges as *untrained* references; single PhD student, ~3 months to submission; venue ICSE/FSE (primary) or ACL/NeurIPS Datasets & Benchmarks; parent paper's CSJE/HCA machinery is reusable and must stay consistent with it.
- **Success condition**: A protocol (target-reliability diagnostic → location-aware nulls → label-preserving attribution against held-out individual raters by consensus stratum) that, applied to Chen-style distributional judges on the three SE panels with ≥ 3 seeds and ≥ 2 model families, yields a definite, replicated verdict on whether the distributional gain is item-specific — and that a sceptical reviewer accepts as the right way to audit future "disagreement-aware judge" claims. A positive item-specific residual on some criterion/panel and a null on others is an acceptable (indeed informative) outcome.

## Anchor Check
- Original bottleneck: pooled-histogram validation cannot separate item-linked disagreement learning from global smoothing / location on small panels.
- Why the revised method still addresses it: the round-4 support audit (including the leave-one-rater-out rotations the reviewer asked for) shows that the clean separation the anchor asks for is **not non-parametrically identifiable on the commit-message panel under any rotation** (exact coverage ≤ 14 % with 5 target raters, ≤ 20 % with no exclusion), is borderline-identifiable on readability (31–51 %, 8 target raters) and impossible on 2-rater targets. The anchor's success condition explicitly admits a null/boundary verdict; the revised thesis therefore makes the *identifiability boundary* the primary result and reports what remains estimable (the calibration-symmetric Δ_soft with its REL/RES/UNC reading; the exact-support Δ_link on readability; a clearly named relaxed Δ_bin-link on commit messages as a bounded sensitivity). This is a revision of the method thesis, declared as such, not a silent drift.
- Reviewer suggestions rejected as drift: none.

## Simplicity Check
- Dominant contribution after revision: the identification analysis of training-side disagreement audits on small panels — a formal statement of when exact label-and-location-preserving target randomisation has support, a combinatorial support bound in terms of panel size and rating concentration, and its empirical support map on the three released SE panels — together with the audit of what is identifiable: Δ_soft (calibration-symmetric, excluded-rater), exact Δ_link where supported (readability), and Δ_bin-link (bounded relaxation, commit) as sensitivity.
- Components removed or merged: the drift-stratified descriptive split (cannot deconfound — removed); ten-bin decomposition sensitivity (removed); fold-exclusion rule (replaced by "include every fold; coverage κ_f is treatment intensity"); "≤ 0.002" outcome claims (replaced by estimates with CIs); the "50 % in every fold" width rule (replaced by an explicit rule with an infeasibility clause).
- Reviewer suggestions rejected as unnecessary complexity: none.
- Why the remaining mechanism is still the smallest adequate route: no new model or loss; the support audit is CPU-only and precedes every GPU run (stage-gate); the GPU matrix estimates only quantities the audit shows to be identifiable or explicitly labelled as relaxed.

## Changes Made
### 1. Estimand renamed / restored by panel (CRITICAL)
- Reviewer said: with w > 1, A_perm breaks shape and within-class location; rename the relaxed contrast or restore exact location control.
- Action: **Δ_link** is reserved for exact cells (pool, z_i, Σy) — estimated only where its support κ_f ≥ 0.30 in every fold at w = 1: readability with leave-one-rater-out rotations (8 target raters; κ = 31–51 %). **Δ_bin-link** names the relaxed contrast with cells (pool, z_i, ⌊Σy / w⌋), explicitly "the effect of breaking histogram shape together with bounded within-bin location (|drift| ≤ (w−1)/m_t)", an upper bound on the shape effect, reported as sensitivity on commit messages (LORO rotations, 5 target raters, w = 2, drift ≤ 0.2, κ = 34–65 %). Summarization: neither is identifiable (formal boundary); Δ_soft only.
### 2. Leave-one-rater-out support audit run (CRITICAL)
- Reviewer said: audit LORO support before accepting relaxation; prefer LORO rotations if exact support becomes adequate.
- Action: done (`refine-logs/SUPPORT_AUDIT.md`): commit exact coverage 1–14 % (LORO), readability 31–51 % (LORO), summarization 0 %. Consequence: LORO rotations adopted for commit and readability (they maximise support and remove the pair-fold heterogeneity); exact support is adequate only on readability.
### 3. Reframed thesis (CRITICAL)
- Reviewer said: if exact support remains inadequate, make the identifiability boundary the central result and the relaxed experiment a sensitivity analysis.
- Action: adopted (Method Thesis below). The paper's primary claims are now (C1) the identifiability result and support map; (C2) the calibration-symmetric Δ_soft audit with REL/RES/UNC on all three panels; (C3) the exact Δ_link on readability and the Δ_bin-link sensitivity on commit messages.
### 4. Width-selection rule (IMPORTANT)
- Action: w* = min{w ∈ {1, 2, 3} : κ_f ≥ 0.30 for every fold}; if no w ≤ 3 satisfies it the criterion is declared "not identifiable at the pre-declared coverage" and no relaxed contrast is run. Applied: readability w* = 1 (exact), commit w* = 2, summarization none. Drift bound (w−1)/m_t is reported with the estimate.
### 5. Fold aggregation (IMPORTANT)
- Action: every fold is included; κ_f is reported as treatment intensity; Δ_bin-link / Δ_link are intent-to-treat effects at the realised intensities (fold-level estimates and intensities shown together in Figure 1); no fold exclusion, no coverage scaling.
### 6. Outcome claims and inference (IMPORTANT)
- Action: all outcome claims are effect estimates with 95 % CIs (no "≤ 0.002" claims); the artifact bootstrap is described as conditional on the fixed trained replicas; replicate-to-replicate (training-seed) variation is shown descriptively; no equivalence procedure is claimed.
### 7. Simplifications adopted
- Drift-stratified split removed; ten-bin sensitivity removed; the GPU matrix is stage-gated on the support audit (already passed for the declared w*).

## Revised Proposal

# Research Proposal: Can Small Annotator Panels Tell Whether Soft-Label LLM Judges Learn Disagreement? An Identifiability Audit of Distributional Judge Training in Software Engineering

## Problem Anchor
(verbatim as above)

## Technical Gap
Soft-label judge training (Chen et al. 2505.12301: α·KL to the empirical histogram + (1−α)·CE to the majority label + an adversarial ℓ₂-ball term; Li et al. 2510.00263; Singh et al. 2511.14117) is scored against the *same pooled histogram* it was fitted to. Three facts make that score uninterpretable as evidence of "learned disagreement": (1) a proper score decomposes into reliability − resolution + uncertainty, and a globally calibrated point-label judge can match a soft-label judge on RPS with identical resolution — in our commit-message pilot the raw CE→KL gain (+0.004 What / +0.011 Why RPS) shrinks to +0.0008 [−0.0001, +0.0017] / +0.0018 [+0.0005, +0.0031] once the same two-parameter calibrator is fitted to both arms; (2) on bounded ordinal scales the Low-consensus stratum is predictable from the pooled median alone (AUROC .67/.80), so entropy-based "disagreement detection" is mostly location; (3) averaging a held-out-rating score over all raters *is* the pooled-histogram score plus a model-free constant, so "held-out rater" must mean held-out rater *identity*, excluded from every target and calibrator. The natural instrument — train on histograms randomly re-assigned among artifacts that share the point label and the rating sum, so that only the artifact→shape link is broken — requires two artifacts with *different* histograms in the same (label, sum) cell. Our support audit shows this almost never happens on the panels SE actually has: with m_t target raters on a 5-level scale the number of distinct histograms per cell is tiny, and the realised coverage is 1–14 % on the 6-rater commit panel (any rotation), 31–51 % on the 9-rater readability panel, and exactly 0 with 2 target raters (a ≤ b ⇒ z_i = a, b = Σy − z_i). What is missing is therefore not only the instrument but a statement of *when it can exist* — and an honest audit of what is identifiable when it cannot.

## Method Thesis
- One-sentence thesis: On the small annotator panels of released SE benchmarks, whether a soft-label judge learned item-specific disagreement is **not non-parametrically identifiable while holding label and location fixed** — exact label-and-sum-preserving target randomisation has support only on the 9-rater readability panel — and what *is* identifiable (the calibration-symmetric, excluded-rater soft-label gain Δ_soft and its reliability/resolution decomposition; the exact Δ_link where supported; a bounded relaxed contrast Δ_bin-link elsewhere) shows that the soft-label gain is mostly calibration with at most a small composite residual.
- Why this is the smallest adequate intervention: no model, no loss; a CPU support audit with a combinatorial bound, plus three training arms and one symmetric calibration step, stage-gated on the audit.
- Why this route is timely: soft-label / distributional judges and reward models are proliferating; the community needs to know which of their claims the available panels can even support.

## Contribution Focus
- Dominant contribution: the **identifiability analysis** — (i) the exact randomised target-link estimand Δ_link and its support condition (cells (pool, z_i, Σy) with ≥ 2 items and largest histogram class M ≤ N/2); (ii) a combinatorial bound on support as a function of target-panel size m_t, scale size K and rating concentration, with its empirical support map on the three SE panels under grouped and leave-one-rater-out rotations; (iii) the 2-rater impossibility result. This is what lets a reviewer judge any future "disagreement-aware judge" claim on a small panel.
- Optional supporting contribution: the audit of what is identifiable — Δ_soft (excluded-rater, symmetric calibration, five-bin REL/RES/UNC) on all three panels; exact Δ_link on readability (LORO, 8 target raters, κ ≈ 0.3–0.5); Δ_bin-link on commit messages (LORO, w = 2, drift ≤ 0.2, κ ≈ 0.35–0.65) as a named sensitivity / upper bound; the pilot's finding that ≈ 84–100 % of the Chen-style gain is calibration.
- Explicit non-contributions: no new training objective; no routing; no metric claims; no panel-size law; no population claims beyond the released panels; Δ_bin-link is not presented as identified conditional resolution.

## Proposed Method
### Complexity Budget
- Frozen / reused: Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct; verbatim single-criterion prompts; LoRA r = 16, α_LoRA = 32, dropout 0.05; parent CSJE strata code (strata from target raters).
- New trainable components: none.
- Tempting additions intentionally not used: posterior-predictive / CRPS / tie-aware arms; per-rater conditioning; RL judges; routing heads; frontier fine-tuning; non-SE benchmarks; isotonic calibration branches; drift-stratified "deconfounding"; ten-bin sensitivity.

### System Overview
```
Stage 0 (CPU, stage-gate) — support audit per panel / criterion / rotation:
   z_i = mode of target ratings (ties → level closest to target median, then lower);  cells (pool, z_i, ⌊Σy / w⌋)
   eligible cell ⇔ N ≥ 2 and largest histogram class M ≤ N/2;  κ_f = eligible training items / training items
   w* = min{w ∈ {1,2,3} : κ_f ≥ 0.30 ∀ folds};  w* = 1 ⇒ exact Δ_link;  w* > 1 ⇒ Δ_bin-link (drift ≤ (w*−1)/m_t);  none ⇒ not identifiable
   combinatorial bound: #distinct histograms with given (z, Σy) on K levels and m_t raters (enumerated) × empirical concentration ⇒ expected κ
   audited result: readability w* = 1 (κ .31–.51, LORO); commit w* = 2 (κ .34–.65, LORO); summarization none (2 target raters)
Stage 1 (GPU) — for each panel with w* ≤ 3:
   ONE immutable artifact-grouped split (seed 0): train 60 % · calibration 10 % · test 30 %
   evaluator rotation: leave-one-rater-out (commit 6 folds, readability 9 folds); summarization LOO (A_hard, A_true only)
   A_hard : CE(z_i, q);  A_true : α·KL(p_i‖q) + (1−α)·CE(z_i, q) + L_adv(p_i, q);  A_perm : same with p_π(i) in eligible cells, p_i elsewhere (full-data ITT)
   replicate seeds s ∈ {0,1,2}: LoRA init, data order, π
   symmetric arm-specific calibration C_A(q) = (1−λ_A)·softmax(log q / T_A) + λ_A·p_clim on the calibration split (target raters only)
   RPS against the excluded rater on test items;  Δ_soft = RPS(A_hard) − RPS(A_true);  Δ_link / Δ_bin-link = RPS(A_perm) − RPS(A_true);  Δ_reg = Δ_soft − Δ_(bin-)link
   secondary: five-bin REL / RES / UNC;  certification: κ_f, drift distribution, eligible cells / classes
   inference: Δ = mean over folds × replicates × families of item-level paired differences on the common test set; bootstrap over test artifacts (B = 2000), conditional on the fixed trained replicas; fold intensities κ_f and per-replicate estimates shown descriptively
```

### Core Mechanism
- Input / output: artifact + single-criterion prompt → q_A(x) ∈ Δ⁴; evaluator = a human rating whose rater identity was excluded from every target and calibrator.
- Architecture or policy: unchanged judge. The mechanism is (i) the support condition and its audit, which decide *which* contrast a panel can support; (ii) A_perm, which preserves z_i (the CE class), pool and the sum (exact) or sum bin (relaxed) for every training item and replaces the histogram shape in eligible cells; (iii) symmetric arm-specific calibration; (iv) evaluator-identity exclusion.
- Training signal / loss: exact Chen objective with (α, ε*, inner steps, optimiser) from the released configuration; L_adv by projected gradient ascent on p′ ∈ Δ⁴ ∩ B_ε*(p) (ℓ₂-ball clipping then simplex projection); identical steps, schedules, init and order across arms within a replicate.
- Why this is the main novelty: Chen/Li evaluate on the fitted histogram; Gheibi 2605.20642 shuffles globally; Kohli 2605.29797 holds out an annotator group without calibration symmetry or link randomisation; Calderon 2501.10970 is leave-one-annotator-out for point judges. None states when a label-and-location-preserving randomisation can exist, and none reports that on typical SE panels it essentially cannot.

### Optional Supporting Component
- Pre-audit diagnostics (CPU): split-half Spearman of per-item dispersion per criterion; the support map (κ by rotation, w, panel) and the combinatorial bound. Used to interpret the estimates; never a law.

### Modern Primitive Usage
- Open-weight instruction LLM judge (score-token distribution) with LoRA — the audited object; intentionally non-frontier.

### Integration into Base Generator / Downstream Pipeline
Plugs into the parent CSJE pipeline (strata from target raters). Inference = one forward pass per item per criterion; calibration = two scalars per arm.

### Training Plan
- Split: one immutable grouped split per benchmark (seed 0); replicates s ∈ {0,1,2} vary LoRA init, data order, π.
- Rotations: commit LORO (6 folds, 5 target raters); readability LORO (9 folds, 8 target raters); summarization LOO (3 folds, 2 target raters; A_hard, A_true only).
- Criteria: commit What, Why; readability (one); summarization Content Adequacy, Conciseness (Qwen only, Δ_soft only).
- Runs: commit 3 arms × 6 folds × 3 replicates × 2 families × 2 criteria = 216 (≈ 0.45 GPU-h each → 97 GPU-h); readability 3 × 9 × 3 × 2 = 162 (≈ 0.1 → 16 GPU-h); summarization 2 × 3 × 3 × 1 × 2 = 36 (≈ 0.6 → 22 GPU-h) → **414 runs ≈ 135 GPU-h** (+ ≈ 6 sensitivity); ≈ 1.4 weeks on 4 shared cards. Stage-gated: M1 (commit, Qwen, replicate 0) must reproduce the pilot's calibrated Δ_soft before the rest is launched.
- Calibration: grid T ∈ {0.5, 0.7, 0.85, 1, 1.25, 1.5, 2, 3, 4, 6} × λ ∈ {0, .05, .1, .2, .3, .5}; p_clim = target-rater level marginal over training items; objective = mean RPS over target raters on calibration items; fitted once per arm × fold × replicate × family.
- Pooling: Δ for a (benchmark, criterion) = mean over all (fold, replicate, family) cells of item-level paired differences on the common test set; bootstrap over test artifacts; per-cell estimates with κ_f in Figure 1.

### Failure Modes and Diagnostics
- A panel's w* does not exist → reported as "not identifiable at κ ≥ 0.30" (already the case for summarization).
- Δ_soft ≈ 0 after calibration everywhere → "no soft-label gain beyond calibration" (still the paper).
- Exact Δ_link on readability is null while Δ_bin-link on commit is positive → interpreted with the drift bound: an upper bound on the shape effect that may include location; stated as such.
- Residual REL after calibration → reported; conclusions scoped to the (T, λ) family.
- Readability panel: the parent alignment bug is fixed first; dispersion reliability ≈ .02 noted.

### Novelty and Elegance Argument
One estimand, one support condition with a bound, one audit map, three arms, one calibration step, one rotation. The contribution is the *identifiability* result and the disciplined audit it licenses — a measurement paper in the parent paper's lineage (CSJE/HCA → what training-side disagreement claims small panels can support), not a salami slice: new question, new instrument, new boundary.

## Claim-Driven Validation Sketch
### Claim 1 (main, CPU): Exact label-and-sum-preserving target randomisation is unsupported on the commit-message panel (κ ≤ 0.14 under every rotation), borderline on readability (κ ≈ 0.3–0.5 with 8 target raters), and impossible with 2 target raters; the combinatorial bound predicts the observed support from m_t, K and rating concentration.
- Minimal experiment: the support audit on all three panels (done for the released rotations); the bound evaluated against the empirical κ; subsampled-rater curves for readability (9 → 8 → 6 → 4 target raters) to show κ collapsing.
- Metric: κ per rotation / w; predicted vs observed κ.
- Expected evidence: as in `SUPPORT_AUDIT.md`.
### Claim 2 (supporting, GPU): For the exact Chen objective, the calibration-symmetric excluded-rater gain Δ_soft is small on all three panels (estimates with CIs; pilot: +0.0008 What, +0.0018 Why), mostly reliability (REL/RES/UNC); the exact Δ_link on readability and the relaxed Δ_bin-link on commit messages are reported as estimates with CIs and their support intensities.
- Minimal experiment: the stage-gated matrix above.
- Metric: calibrated held-out-rater RPS; Δ_soft, Δ_link / Δ_bin-link, Δ_reg; five-bin REL/RES/UNC; κ_f.
- Expected evidence: Δ_soft small everywhere; Δ_link on readability ≈ 0; Δ_bin-link on commit small and explicitly bounded by drift.

## Experiment Handoff Inputs
- Must-prove claims: C1 (support/identifiability), C2 (estimates).
- Must-run ablations: exact-Chen (α, ε) sensitivity row; certification per fold/replicate; subsampled-rater support curves (CPU).
- Critical datasets / metrics: commit (LORO), readability (direct key, LORO), summarization (LOO, Δ_soft); κ, drift; calibrated RPS; Δ's with CIs.
- Highest-risk assumptions: faithful reproduction of the adversarial term; readability alignment fix upstream; the bound's concentration model matching the empirical κ.

## Compute & Timeline Estimate
- GPU-hours: ≈ 135 (≈ 141 with the sensitivity row), stage-gated; CPU audit already complete for the released rotations.
- Data / annotation cost: none.
- Timeline: bound + support map 1 week; exact objective + permutation + rotation implementation 1 week; GPU matrix 1.5 weeks; analysis + writing 4 weeks.
