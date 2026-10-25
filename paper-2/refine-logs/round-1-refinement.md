# Round 1 Refinement

## Problem Anchor
- **Bottom-line problem**: Training-side claims that an LLM judge "models human disagreement" (soft-label / distributional fine-tuning, Chen et al. NeurIPS 2025 and successors) are validated against the same pooled rating histogram they were trained on. On the small annotator panels that software-engineering benchmarks actually have (3–9 raters), we need a way to tell whether such a judge learned *which artifacts* split human raters, or merely learned a better-calibrated (smoother) score distribution plus scale-location effects.
- **Must-solve bottleneck**: The existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing; a judge can post large KL/RPS gains over point-SFT while carrying zero item-level disagreement information, and uncertainty-based downstream decisions (routing contested items to humans) inherit that ambiguity.
- **Non-goals**: Not a new judge-training method as the headline; not pairwise preference / reward-model training; not RL judges; not a new multi-rater benchmark; not claims about human populations beyond the released panels; not generation-side (DPO/best-of-n) consequences.
- **Constraints**: Released per-annotator data only (commit messages 800×6, code summarization 1,163×3, readability 200×9); 7B–14B open judges with LoRA on 4 shared RTX 6000 Ada (~22 GB free each) plus small OpenRouter budget for frontier judges as *untrained* references; single PhD student, ~3 months to submission; venue ICSE/FSE (primary) or ACL/NeurIPS Datasets & Benchmarks; parent paper's CSJE/HCA machinery is reusable and must stay consistent with it.
- **Success condition**: A protocol (target-reliability diagnostic → location-aware nulls → label-preserving attribution against held-out individual raters by consensus stratum) that, applied to Chen-style distributional judges on the three SE panels with ≥ 3 seeds and ≥ 2 model families, yields a definite, replicated verdict on whether the distributional gain is item-specific — and that a sceptical reviewer accepts as the right way to audit future "disagreement-aware judge" claims. A positive item-specific residual on some criterion/panel and a null on others is an acceptable (indeed informative) outcome.

## Anchor Check
- Original bottleneck: pooled-histogram validation cannot separate item-specific disagreement learning from global smoothing/location on small panels.
- Why the revised method still addresses it: the revision *sharpens* the bottleneck into two formal randomised contrasts (Δ_soft = calibration-symmetric soft-vs-hard gain; Δ_link = the part of that gain that disappears when the item→histogram link is randomised while label, mean and pool are preserved), evaluated on rater identities excluded from every target and calibrator. Nothing in the revision changes the object under audit (Chen-style soft-label fine-tuning) or the population (the released SE panels).
- Reviewer suggestions rejected as drift: none. Explicitly *not* taken up (would drift): RL/DPO judges, per-rater embeddings, verbalised-probability SFT, frontier fine-tuning, non-SE benchmarks added only to target NeurIPS.

## Simplicity Check
- Dominant contribution after revision: the **randomised target-link estimand Δ_link** (with its validity conditions and failure cases) and its replicated estimate on the three SE panels, together with the calibration-symmetric Δ_soft it decomposes.
- Components removed or merged: T2 (trained tie-aware location-only arm) — removed; T3 (simplified Chen hybrid) merged into T4 (exact Chen objective); panel-size sweep, asymmetric-calibration ablation, cell-vs-identity holdout comparison, distributional skill score, entropy→Low AUROC and TOST — removed from the core (the split-panel reliability and the tie-awareness question survive only as *pre-audit diagnostics / descriptive moderators*); Claim 2 as a "law with a threshold" — removed.
- Reviewer suggestions rejected as unnecessary complexity: none; all three simplification opportunities adopted.
- Why the remaining mechanism is still the smallest adequate route: three arms (hard-median CE · exact Chen on true histograms · exact Chen on conditionally randomised histograms), one calibration family applied symmetrically, one evaluator-exclusion rotation, two contrasts. Any smaller design would lose either the calibration control or the link-randomisation control, each of which the pilot showed is necessary.

## Changes Made
### 1. Formal estimand and evaluator exclusion (Method Specificity, CRITICAL)
- Reviewer said: no single formal primary estimand; "one shared calibrator" ambiguous; rotation excluded raters only for some arms.
- Action: defined Δ_soft and Δ_link exactly (below); every arm is retrained per evaluator fold with the evaluator raters excluded from all training targets and from calibration; calibration is *symmetric arm-specific* (same family and grid, fitted separately per arm on the untouched calibration split using only non-evaluator raters).
- Reasoning: without evaluator exclusion the "held-out rater" score is the pooled-histogram score; without symmetric calibration the soft-vs-hard gain mixes reliability and resolution.
- Impact on core method: the audit is now one estimand with stated validity conditions rather than a bundle of controls.
### 2. Permutation construction specified (Method Specificity, CRITICAL)
- Reviewer said: T5 omits cell definition, sparse-cell behaviour and the algorithm.
- Action: permutation cells = (authorship pool, exact median of the m_t target raters, exact rating sum); within a cell, histograms are permuted among items (derangement where |cell| ≥ 2); singleton cells keep their own histogram and are counted; the preserved-statistics table (median, mean, pool exactly preserved by construction; dispersion and skew not) and the fraction of permutable items are reported; if < 70 % of items are permutable the median is coarsened to the rounded median (pre-declared fallback).
- Reasoning: exact preservation of sum and count preserves the mean exactly; conditioning on the exact median preserves the point-label target of the hard arm; the pilot's banker-rounded-median cells leaked mean (≈ 0.30) and pool (42–49 % cross-pool).
- Impact on core method: Δ_link now isolates dispersion/shape linkage by construction.
### 3. Three arms, exact audited objective, independent Why prompt (Contribution Quality, IMPORTANT)
- Reviewer said: five target types read as an objective comparison; Why conditioned on What.
- Action: arms reduced to A_hard (CE to the exact median of the target raters, ties broken to the lower level and reported), A_true (exact Chen objective: α·KL + (1−α)·CE with the adversarial ℓ₂-ball inner maximisation, hyper-parameters from the paper's released configuration), A_perm (A_true's objective on the randomised histograms). Why uses Zeng's single-dimension `WHY_…ZERO_SHOT_NONCOT` prompt; What uses the `WHAT_…` prompt; no cross-criterion conditioning at train or test.
- Reasoning: the question is about the published method; a faithful reproduction is the only defensible audited object.
- Impact on core method: one dominant contribution; the simplified hybrid and the tie-aware arm become footnotes.
### 4. Rater-disjoint rotation for every arm; honest compute (Feasibility, CRITICAL)
- Reviewer said: rotation policy and GPU accounting described different experiments.
- Action: three evaluator folds per benchmark — commit messages: rater pairs {1,2}, {3,4}, {5,6}; readability: triples {1,2,3}, {4,5,6}, {7,8,9}; summarization: leave-one-out over 3 raters; all targets and calibrators recomputed from the complementary identities; replicates are **three paired pipeline seeds** (seed s sets the artifact split, LoRA initialisation, data order and the permutation), not a Cartesian product. Budget recomputed below.
- Reasoning: the evaluator must be unseen by every arm for Δ to be interpretable.
- Impact on core method: none on the estimand; the run matrix is now 3 arms × 3 folds × 3 seeds × 2 model families per benchmark.
### 5. Endpoints pruned (Validation Focus, IMPORTANT)
- Reviewer said: too many arms, ablations, metrics.
- Action: primary endpoints = calibrated held-out-rater RPS per arm and the two contrasts with cluster-by-artifact and two-way (artifact × evaluator) bootstrap CIs; secondary = threshold-Brier REL/RES/UNC (predeclared: 5 and 10 equal-width forecast bins, both reported) and the permutation preserved-statistics table; pre-audit diagnostics = split-half dispersion reliability per criterion (reported descriptively as a moderator, no threshold claim); everything else dropped.
- Reasoning: only these change a reviewer's belief about Δ_link.
- Impact on core method: none.
### 6. Positioning (Venue Readiness, IMPORTANT)
- Reviewer said: novelty rests on combining known controls unless the estimand is formal.
- Action: the paper is centred on Δ_link — definition, identification assumptions (exchangeability of histograms within a cell; no leakage of evaluator ratings; calibration fitted on non-evaluator raters), validity failures (sparse cells, non-exchangeable pools), and a replicated estimate; the empirical claim is phrased as "estimating the calibration and target-link components of the soft-label gain", not as proving a reliability threshold.

## Revised Proposal

# Research Proposal: When Do Soft-Label LLM Judges Add Conditional Resolution Beyond Calibration? A Randomised Target-Link Audit on Small SE Annotator Panels

## Problem Anchor
(verbatim as above)

## Technical Gap
Soft-label judge training (Chen et al. 2505.12301: α·KL to the empirical histogram + (1−α)·CE to the majority + adversarial ε-ball; Li et al. 2510.00263; Singh et al. 2511.14117) is scored against the *same pooled histogram* it was fitted to. Three facts make that score uninterpretable as evidence of "learned disagreement": (1) a proper score decomposes into reliability − resolution + uncertainty, and a globally calibrated point-label judge can match a soft-label judge on RPS with identical resolution — in our commit-message pilot the raw CE→KL gain (+0.004 What / +0.011 Why RPS) shrinks to +0.0008 [−0.0001, +0.0017] / +0.0018 [+0.0005, +0.0031] once a temperature + climatology calibrator is applied to both arms; (2) on bounded ordinal scales the Low-consensus stratum is predictable from the pooled median alone (AUROC .67/.80), so entropy-based "disagreement detection" is mostly location; (3) averaging a held-out-rater score over all raters *is* the pooled-histogram score plus a model-free constant, so "held-out rater" must mean held-out rater *identity*, excluded from every target and calibrator. Naive fixes (more raters — unavailable; heavier Bayesian targets — over-shrink, Kohli 2605.29797 and our k = 2 pilot; ordinal losses — tie with KL; the adversarial ball — a regulariser) do not identify the item-linked component. What is missing is a randomised estimand.

## Method Thesis
- One-sentence thesis: The item-linked component of a soft-label judge's gain is identified by **Δ_link**, the loss in calibrated held-out-rater RPS incurred when the judge is trained on histograms randomly re-assigned among artifacts that share the same authorship pool, exact median and rating sum — and on small SE panels this component is small relative to the calibration component Δ_soft − Δ_link.
- Why this is the smallest adequate intervention: it adds no model and no loss; it adds one randomised training target and one symmetric calibration step to the existing pipeline.
- Why this route is timely: soft-label / distributional judges and reward models are proliferating; the community needs a way to read their numbers before adopting them as "disagreement-aware".

## Contribution Focus
- Dominant contribution: the randomised target-link estimand Δ_link (definition, identification conditions, failure modes) and its replicated estimate for the exact Chen objective on the three released multi-rater SE benchmarks (2 model families × 3 paired seeds × 3 evaluator folds).
- Optional supporting contribution: the calibration-symmetric decomposition of the soft-label gain (Δ_soft) with the threshold-Brier REL/RES/UNC reading, and split-panel dispersion reliability as a pre-audit diagnostic reported as a descriptive moderator.
- Explicit non-contributions: no new training objective; no routing; no metric claims; no panel-size law.

## Proposed Method
### Complexity Budget
- Frozen / reused: Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct (second family); verbatim single-criterion benchmark prompts; LoRA r = 16; parent CSJE strata code.
- New trainable components: none (LoRA adapters per arm only).
- Tempting additions intentionally not used: posterior-predictive / CRPS / tie-aware training arms; per-rater conditioning; RL judges; routing heads; frontier fine-tuning; extra non-SE benchmarks.

### System Overview
```
per-annotator ratings H (n × m) ── artifact-grouped split (diff / function / snippet): train 60 % · calibration 10 % · test 30 %   [seed s]
   │
   ├─ evaluator fold f: raters E_f excluded from every target and from calibration; targets from the m_t = m − |E_f| remaining raters
   ▼
targets per item i (from the m_t target raters):
   A_hard : one-hot exact median (ties → lower level)
   A_true : empirical histogram p_i                          ─┐ exact Chen objective: α·KL(p‖q) + (1−α)·CE(majority) with
   A_perm : p_{π(i)}, π a within-cell derangement,            ─┘ inner max over p' ∈ Δ ∩ B_ε(p)
            cell(i) = (pool, median_t(i), Σ ratings_t(i))
   ▼
LoRA judge → score-token distribution q_A(x) on calibration + test items
   ▼
symmetric arm-specific calibration: (T_A, λ_A) = argmin mean RPS over the m_t target raters on the calibration split; same family/grid for all arms
   ▼
scoring on test items against each evaluator rater r ∈ E_f:  RPS_r(C_A(q_A));  strata from the target raters
   ▼
Δ_soft = RPS(A_hard) − RPS(A_true);   Δ_link = RPS(A_perm) − RPS(A_true);   secondary: REL / RES / UNC; preserved-statistics table
   ▼
inference: cluster bootstrap by artifact; two-way artifact × evaluator bootstrap; seeds and families reported as replicates
```

### Core Mechanism
- Input / output: artifact + single-criterion prompt → q_A(x) ∈ Δ⁴; evaluator = a human rating whose rater identity was excluded from every target and calibrator.
- Architecture or policy: unchanged judge. The mechanism is the *design*: (i) A_perm preserves, for every item, the hard label, the mean, the pool and the item count of its cell, and changes only which histogram shape is attached to which artifact — so any RPS loss of A_perm relative to A_true is attributable to the item→shape link; (ii) symmetric arm-specific calibration removes reliability differences so that Δ_soft and Δ_link measure information, not smoothness; (iii) evaluator exclusion removes panel memorisation.
- Training signal / loss: A_hard: CE to the exact median; A_true / A_perm: the exact Chen objective with the paper's (α, ε) and optimiser; identical steps, schedules and seeds across arms.
- Why this is the main novelty: Chen/Li evaluate on the fitted histogram; Gheibi 2605.20642 shuffles globally (destroying the label); Kohli 2605.29797 holds out an annotator *group* without calibration symmetry or link randomisation; Calderon 2501.10970 is leave-one-annotator-out for point judges. None defines or estimates a label-, mean- and pool-preserving randomised link estimand against excluded rater identities.

### Optional Supporting Component
- Pre-audit diagnostics (CPU, reported in one table): split-half Spearman of per-item dispersion across disjoint rater halves (Spearman–Brown corrected) per criterion; fraction of permutable items and preserved-statistics check per fold/seed. Used to *interpret* Δ_link (e.g., a null on readability where reliability ≈ .02), never as a claimed law.
- Why it does not create sprawl: no training, one table.

### Modern Primitive Usage
- Which primitive: open-weight instruction LLM judge (score-token distribution from logits), LoRA.
- Exact role: the audited object. Intentionally non-frontier on the method side; frontier API judges appear only as untrained references in one descriptive row.

### Integration into Base Generator / Downstream Pipeline
Plugs into the parent CSJE pipeline (same strata definitions; strata now computed from target raters only). Inference = one forward pass per item per criterion; calibration = two scalars per arm.

### Training Plan
- Splits: 60/10/30 by artifact, paired seed s ∈ {0,1,2} controls split, LoRA init, data order and π.
- Evaluator folds: commit {1,2},{3,4},{5,6}; readability {1,2,3},{4,5,6},{7,8,9}; summarization LOO over 3 raters (2-rater targets; flagged low-power).
- Runs per benchmark: 3 arms × 3 folds × 3 seeds × 2 families = 54 LoRA runs (× 2 criteria for commit = 108; × 3 criteria for summarization = 162; × 1 for readability = 54).
- Per-run cost: commit ≈ 0.45 GPU-h (560 items, 2 epochs, 1k tokens); summarization ≈ 0.6 GPU-h (≈ 700 train items); readability ≈ 0.1 GPU-h.
- Total ≈ 108 × 0.45 + 162 × 0.6 + 54 × 0.1 ≈ 49 + 97 + 5 ≈ **150 GPU-h** (upper bound); summarization criteria can be reduced to Content Adequacy + Conciseness (108 runs, 65 GPU-h) if needed → ≈ 120 GPU-h, i.e. ≈ 1.3 weeks on 4 shared cards.
- Exact Chen reproduction: released hyper-parameters (α, ε, optimiser); if unavailable, the paper's ablation values with a sensitivity row.

### Failure Modes and Diagnostics
- Sparse permutation cells (< 70 % permutable): coarsen median; report; if still sparse, exclude the criterion from Δ_link.
- Δ_soft ≈ 0 everywhere after calibration: the audit's answer is "no soft-label gain beyond calibration"; still the paper.
- Δ_link > 0 but Δ_soft ≈ 0: histograms carry item information that does not produce a net gain — reported as such.
- Evaluator-fold variance large: two-way CIs will show it; no population claim beyond the panels.
- Readability: expected null (reliability ≈ .02); the parent alignment bug must be fixed first.

### Novelty and Elegance Argument
One estimand, three arms, one calibration step, one rotation. The closest works lack at least one of: label/mean/pool-preserving randomisation, calibration symmetry, evaluator-identity exclusion, or the SE small-panel setting. The paper is a measurement contribution in the parent paper's lineage (CSJE/HCA → training-side audit), not a salami slice: it asks a different question (what training learned) with a different instrument (randomised targets).

## Claim-Driven Validation Sketch
### Claim 1 (main): For the exact Chen objective on the released SE panels, the calibration-symmetric soft-label gain Δ_soft is small, and its item-linked component Δ_link is smaller still — non-zero, if anywhere, on the criterion with the highest split-panel dispersion reliability (commit Why).
- Minimal experiment: the full 3 × 3 × 3 × 2 matrix on commit messages (What, Why); report Δ_soft, Δ_link with cluster and two-way CIs per criterion and stratum.
- Baselines / ablations: none beyond the three arms; the preserved-statistics table certifies the randomisation.
- Metric: calibrated held-out-rater RPS; secondary REL/RES/UNC.
- Expected evidence: What — Δ_soft and Δ_link both ≈ 0; Why — Δ_soft ≈ 0.002, Δ_link ≈ 0.002–0.003, replicated across seeds/families.
### Claim 2 (supporting): The same picture holds on code summarization and (correctly aligned) readability, with Δ_link ≈ 0 where split-panel dispersion reliability is near zero.
- Minimal experiment: same matrix on the two other benchmarks (summarization: CA + Conciseness first).
- Metric: as above; reliability reported descriptively alongside.
- Expected evidence: null on readability; small or null on summarization.

## Experiment Handoff Inputs
- Must-prove claims: C1 (commit), C2 (breadth).
- Must-run ablations: exact-Chen hyper-parameter sensitivity row; permutation preserved-statistics certification per fold/seed; binning sensitivity (5 vs 10) for REL/RES.
- Critical datasets / metrics: commit (primary), summarization, readability (direct snippet key); calibrated RPS vs excluded raters; Δ_soft, Δ_link.
- Highest-risk assumptions: Δ of ≈ 0.002 RPS detectable with 120–350 independent artifacts per fold (power check from the pilot's CI widths: ±0.001–0.0015 per contrast per seed → pooled over 3 seeds × 3 folds adequate); faithful reproduction of the adversarial term; readability alignment fix in the parent pipeline.

## Compute & Timeline Estimate
- GPU-hours: ≈ 120–150 (upper bound) over ≈ 1.3 weeks on 4 shared cards; pilot code already implements arms A_hard / A_true (minus adversarial term) and the analysis.
- Data / annotation cost: none.
- Timeline: implementation of exact objective + permutation + rotation 1 week; commit matrix 1 week; breadth 2 weeks; analysis + writing 4 weeks.
