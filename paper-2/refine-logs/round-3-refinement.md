# Round 3 Refinement

## Problem Anchor
- **Bottom-line problem**: Training-side claims that an LLM judge "models human disagreement" (soft-label / distributional fine-tuning, Chen et al. NeurIPS 2025 and successors) are validated against the same pooled rating histogram they were trained on. On the small annotator panels that software-engineering benchmarks actually have (3–9 raters), we need a way to tell whether such a judge learned *which artifacts* split human raters, or merely learned a better-calibrated (smoother) score distribution plus scale-location effects.
- **Must-solve bottleneck**: The existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing; a judge can post large KL/RPS gains over point-SFT while carrying zero item-level disagreement information, and uncertainty-based downstream decisions (routing contested items to humans) inherit that ambiguity.
- **Non-goals**: Not a new judge-training method as the headline; not pairwise preference / reward-model training; not RL judges; not a new multi-rater benchmark; not claims about human populations beyond the released panels; not generation-side (DPO/best-of-n) consequences.
- **Constraints**: Released per-annotator data only (commit messages 800×6, code summarization 1,163×3, readability 200×9); 7B–14B open judges with LoRA on 4 shared RTX 6000 Ada (~22 GB free each) plus small OpenRouter budget for frontier judges as *untrained* references; single PhD student, ~3 months to submission; venue ICSE/FSE (primary) or ACL/NeurIPS Datasets & Benchmarks; parent paper's CSJE/HCA machinery is reusable and must stay consistent with it.
- **Success condition**: A protocol (target-reliability diagnostic → location-aware nulls → label-preserving attribution against held-out individual raters by consensus stratum) that, applied to Chen-style distributional judges on the three SE panels with ≥ 3 seeds and ≥ 2 model families, yields a definite, replicated verdict on whether the distributional gain is item-specific — and that a sceptical reviewer accepts as the right way to audit future "disagreement-aware judge" claims. A positive item-specific residual on some criterion/panel and a null on others is an acceptable (indeed informative) outcome.

## Anchor Check
- Original bottleneck: pooled-histogram validation cannot separate item-linked disagreement learning from global smoothing / location on small panels.
- Why the revised method still addresses it: the audited object is restored to the *full-data* Chen judge (intent-to-treat randomisation on the full training set); the identification boundary discovered by the support audit ("with ≤ 4 target raters, exact control of label and sum leaves no randomisation support") is itself part of the audit's output — exactly the kind of verdict the anchor's success condition asks for ("a definite, replicated verdict … or a null").
- Reviewer suggestions rejected as drift: none.

## Simplicity Check
- Dominant contribution after revision: Δ_link as an intent-to-treat randomised target-link effect with pre-declared, audited support (coverage and bounded location drift), plus the identification-boundary result for 2-rater targets.
- Components removed or merged: per-protocol training restriction (replaced by full-data ITT); the triggered isotonic-calibration branch (removed; residual REL reported, conclusions scoped to the (T, λ) family); the 70 % rule (replaced by a pre-training support requirement); split seeds (replaced by one immutable grouped split + 3 LoRA/order/permutation seeds); A_perm on summarization (removed — Δ_link not identifiable there).
- Reviewer suggestions rejected as unnecessary complexity: none.
- Why the remaining mechanism is still the smallest adequate route: three arms on the commit and readability panels, two on summarization; one randomisation with explicit support; one calibration step; one rotation.

## Changes Made
### 1. Derangement definition and verification (CRITICAL)
- Reviewer said: "two distinct histograms" does not guarantee a derangement; need M ≤ N/2 and a verified bijection.
- Action: eligible cell ⇔ N ≥ 2 and largest histogram class M ≤ N/2; assignment = sort the cell's items by histogram class and rotate by M (every item then receives a histogram of a different class; the map is a bijection); verified programmatically per cell (no fixed histogram, permutation check). Implemented and run in the support audit (`refine-logs/SUPPORT_AUDIT.md`).
### 2. Support audit run, and its consequence: bounded relaxation of the sum (CRITICAL)
- Reviewer said: run a zero-GPU support audit before any GPU run; do not relax controls merely to manufacture variation.
- Action: audit run on the real panels. Result: under exact cells (pool, z_i, Σy) the fully derangeable coverage of the training set is **0–7 % on commit What/Why (4 target raters), 22–50 % on readability (6 target raters), 0 % on summarization (2 target raters)**. Exact location control therefore leaves essentially no support on the primary benchmark either. The relaxation adopted is pre-declared and bounded: cells (pool, z_i, ⌊Σy / w⌋), i.e. z_i (hence the CE class) exactly preserved, pool preserved, mean preserved up to |drift| ≤ (w−1)/m_t rating points; w is fixed per benchmark from the audit as the smallest width with ≥ 50 % coverage in every fold: **commit w = 3** (|drift| ≤ 0.5, mean drift ≈ 0.3; coverage 57–63 % What, 26–59 % Why — the {5,6} Why fold at 26 % is flagged low-power), **readability w = 2** (|drift| ≤ 0.17; coverage 39–78 %). The drift distribution of every realised permutation is reported in the certification table, and Δ_link is accompanied by a drift-stratified descriptive check (cells with zero drift vs positive drift).
- Reasoning: this is the reviewer's "relax the controls" option made explicit, quantified and pre-registered, instead of silently using a coarse median.
### 3. Full-data intent-to-treat randomisation (CRITICAL — scope)
- Reviewer said: per-protocol training changes the audited object; prefer full-data ITT.
- Action: all three arms train on the full training set; A_perm's targets are randomised in eligible cells and left unchanged elsewhere; coverage (fraction of training items whose histogram changed) is reported; Δ_link is the ITT effect of the feasible link-breaking intervention on the actual full-data pipeline; a coverage-scaled value is shown only descriptively; coverage < 30 % in a fold ⇒ that fold's Δ_link is reported as inconclusive.
### 4. Summarization as an identification boundary (CRITICAL)
- Reviewer said: with two target raters (z_i, Σy) determines the histogram; Δ_link cannot exist there.
- Action: formal statement in the paper (with ratings a ≤ b and the tie rule, z_i = a and b = Σy − z_i); summarization runs A_hard and A_true only → Δ_soft; Claim 2 rewritten accordingly. Matrix: commit 108 + summarization 72 + readability 54 = **234 runs ≈ 97 GPU-h** (+ ≈ 6 for the sensitivity row).
### 5. Split and aggregation (IMPORTANT)
- Reviewer said: artifact-level means averaged over different split seeds are not uniformly defined.
- Action: one immutable grouped split per benchmark (seed 0; 60/10/30 by artifact); three replicate seeds s ∈ {0,1,2} vary LoRA initialisation, data order and the permutation only; Δ := mean over folds f, replicates s and families g of item-level paired differences (each averaged over the fold's evaluators) — every replicate sees the same test artifacts, so the artifact bootstrap (B = 2000) of item-level means is well defined; per-(f, s, g) estimates descriptive.
### 6. Calibration branch removed (MINOR)
- Action: the (T, λ) family is the declared calibrator; residual REL after calibration is reported and conclusions are scoped to that family; no triggered isotonic branch.

## Revised Proposal

# Research Proposal: When Do Soft-Label LLM Judges Add Conditional Resolution Beyond Calibration? A Randomised Target-Link Audit on Small SE Annotator Panels

## Problem Anchor
(verbatim as above)

## Technical Gap
Soft-label judge training (Chen et al. 2505.12301: α·KL to the empirical histogram + (1−α)·CE to the majority label + an adversarial ℓ₂-ball term; Li et al. 2510.00263; Singh et al. 2511.14117) is scored against the *same pooled histogram* it was fitted to. Three facts make that score uninterpretable as evidence of "learned disagreement": (1) a proper score decomposes into reliability − resolution + uncertainty, and a globally calibrated point-label judge can match a soft-label judge on RPS with identical resolution — in our commit-message pilot the raw CE→KL gain (+0.004 What / +0.011 Why RPS) shrinks to +0.0008 [−0.0001, +0.0017] / +0.0018 [+0.0005, +0.0031] once the same two-parameter calibrator is fitted to both arms; (2) on bounded ordinal scales the Low-consensus stratum is predictable from the pooled median alone (AUROC .67/.80), so entropy-based "disagreement detection" is mostly location; (3) averaging a held-out-rating score over all raters *is* the pooled-histogram score plus a model-free constant, so "held-out rater" must mean held-out rater *identity*, excluded from every target and calibrator. A fourth fact, established by our support audit, bounds what any such audit can do: with ≤ 4 target raters on a 5-level scale, exact preservation of the point label and the rating sum leaves almost no two artifacts with different histograms in the same cell (0–7 % coverage on commit messages; 0 % with two target raters). Identification of the item→histogram link therefore requires a *pre-declared, bounded* relaxation of location control, and for 2-rater targets it is impossible. What is missing is a randomised estimand with explicit support.

## Method Thesis
- One-sentence thesis: The item-linked component of a soft-label judge's gain is identified, where support exists, by **Δ_link** — the loss in calibrated held-out-rater RPS when the full-data judge is trained with histograms randomly re-assigned among artifacts sharing pool, point label z_i and rating-sum bin — and on small SE panels this component is small relative to the link-independent soft-target effect Δ_reg, with 2-rater targets constituting an identification boundary.
- Why this is the smallest adequate intervention: no new model, no new loss; one randomised training target with audited support and one symmetric calibration step.
- Why this route is timely: soft-label / distributional judges and reward models are proliferating; the community needs an instrument — and its feasibility limits — before adopting them as "disagreement-aware".

## Contribution Focus
- Dominant contribution: the randomised target-link estimand Δ_link as an intent-to-treat effect with pre-declared support (eligibility M ≤ N/2, verified derangement, bounded drift, reported coverage), its identification conditions and boundary (2-rater targets), and its replicated estimate for the exact Chen objective on the commit-message and readability panels (2 families × 3 replicate seeds × 3 evaluator folds).
- Optional supporting contribution: the decomposition Δ_soft = Δ_link + Δ_reg read with five-bin REL/RES/UNC; Δ_soft on summarization as the boundary case; split-panel dispersion reliability as a pre-audit descriptive moderator.
- Explicit non-contributions: no new training objective; no routing; no metric claims; no panel-size law; no population claims beyond the released panels.

## Proposed Method
### Complexity Budget
- Frozen / reused: Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct; verbatim single-criterion prompts (Zeng WHAT / WHY zero-shot templates; Crupi per-criterion variants; CoReEval readability prompt); LoRA r = 16, α_LoRA = 32, dropout 0.05 on q/k/v/o/gate/up/down; parent CSJE strata code (strata from target raters).
- New trainable components: none.
- Tempting additions intentionally not used: posterior-predictive / CRPS / tie-aware training arms; per-rater conditioning; RL judges; routing heads; frontier fine-tuning; non-SE benchmarks; untrained frontier-judge rows; isotonic calibration branches.

### System Overview
```
per-annotator ratings H (n × m) ── ONE immutable artifact-grouped split (seed 0): train 60 % · calibration 10 % · test 30 %
   │
   ├─ evaluator fold f: raters E_f excluded from every target and from calibration; m_t = m − |E_f| target raters
   ▼
z_i = mode of target ratings (ties → level closest to the target median, then lower);  p_i = target-rater histogram
cells c(i) = (pool, z_i, ⌊Σ_r y_ir / w⌋),  w pre-declared per benchmark from the support audit (commit 3, readability 2)
eligible cells: N ≥ 2 and largest histogram class M ≤ N/2;  π = sorted-class rotation by M within eligible cells (verified bijection, every eligible item gets a different histogram); ineligible items keep p_i
coverage κ_f = fraction of training items with changed histogram (reported);  drift = |mean(p_π(i)) − mean(p_i)| ≤ (w−1)/m_t (reported)
   ▼
A_hard : CE(z_i, q)                                                       ─ all arms trained on the FULL training set (intent-to-treat)
A_true : α·KL(p_i ‖ q) + (1−α)·CE(z_i, q) + L_adv(p_i, q)
A_perm : α·KL(p_π(i) ‖ q) + (1−α)·CE(z_i, q) + L_adv(p_π(i), q)            ─ summarization: A_hard, A_true only (Δ_link not identifiable)
   ▼
LoRA judge → q_A(x) on calibration + test items;  replicate seeds s ∈ {0,1,2} vary LoRA init, data order, π
   ▼
symmetric arm-specific calibration  C_A(q) = (1−λ_A)·softmax(log q / T_A) + λ_A·p_clim ;  (T_A, λ_A) = argmin over the grid of mean RPS vs target raters on calibration items
   ▼
RPS_r(C_A(q_A)) against each evaluator r ∈ E_f on test items;  Δ_soft = RPS(A_hard) − RPS(A_true);  Δ_link = RPS(A_perm) − RPS(A_true);  Δ_reg = Δ_soft − Δ_link
secondary: five-bin REL / RES / UNC;  certification: κ_f, drift distribution, z_i / pool preserved, eligible cells & classes
   ▼
inference: Δ := mean over f, s, g of item-level paired differences (averaged over r ∈ E_f); bootstrap over test artifacts (B = 2000); per-(f, s, g) descriptive; folds with κ_f < 0.30 reported as inconclusive for Δ_link
```

### Core Mechanism
- Input / output: artifact + single-criterion prompt → q_A(x) ∈ Δ⁴; evaluator = a human rating whose rater identity was excluded from every target and calibrator.
- Architecture or policy: unchanged judge. The design is the mechanism: (i) A_perm preserves z_i (the CE class), pool and the rating-sum bin for every training item, and — where support exists — replaces the histogram shape with that of another artifact of the same cell; (ii) symmetric arm-specific calibration removes calibration differences representable by the (T, λ) family (residual REL reported); (iii) evaluator exclusion removes panel memorisation; (iv) support is audited before training and reported as part of the result.
- Training signal / loss: exact Chen objective with (α, ε*, inner steps, optimiser) from the released configuration; L_adv = inner maximisation over p′ ∈ Δ⁴ ∩ B_ε*(p) by projected gradient ascent (ℓ₂-ball clipping then Euclidean simplex projection); identical steps, schedules, LoRA init and data order across arms within a replicate.
- Why this is the main novelty: Chen/Li evaluate on the fitted histogram; Gheibi 2605.20642 shuffles globally (destroying the label); Kohli 2605.29797 holds out an annotator group without calibration symmetry or link randomisation; Calderon 2501.10970 is leave-one-annotator-out for point judges. None defines a label-preserving randomised link estimand with audited support against excluded rater identities — and none reports that such identification has a hard boundary on 2-rater targets.

### Optional Supporting Component
- Pre-audit diagnostics (CPU, one table): split-half Spearman of per-item dispersion across disjoint rater halves per criterion; the support audit (coverage, eligible cells, classes, drift) per benchmark / criterion / fold. Used to interpret Δ_link and to declare w; never a law.

### Modern Primitive Usage
- Open-weight instruction LLM judge (score-token distribution from logits) with LoRA — the audited object; intentionally non-frontier on the method side.

### Integration into Base Generator / Downstream Pipeline
Plugs into the parent CSJE pipeline (strata from target raters). Inference = one forward pass per item per criterion; calibration = two scalars per arm.

### Training Plan
- Split: one immutable grouped split per benchmark (seed 0); replicate seeds s ∈ {0, 1, 2} for LoRA init, data order, π.
- Evaluator folds: commit {1,2}, {3,4}, {5,6}; readability {1,2,3}, {4,5,6}, {7,8,9}; summarization LOO over 3 raters (A_hard, A_true only).
- Criteria: commit What, Why; summarization Content Adequacy, Conciseness; readability (one).
- Runs: commit 3 × 3 × 3 × 2 × 2 = 108; summarization 2 × 3 × 3 × 2 × 2 = 72; readability 3 × 3 × 3 × 2 = 54 → **234 LoRA runs ≈ 97 GPU-h** (commit 0.45, summarization 0.6, readability 0.1 GPU-h per run); + ≈ 6 GPU-h sensitivity row.
- Calibration: grid T ∈ {0.5, 0.7, 0.85, 1, 1.25, 1.5, 2, 3, 4, 6} × λ ∈ {0, .05, .1, .2, .3, .5}; p_clim = target-rater level marginal over training items; objective = mean RPS over target raters on calibration items; fitted once per arm × fold × replicate × family.
- Pooling rule: Δ for a (benchmark, criterion) = mean over the 18 (f, s, g) cells of item-level paired differences on the common test set; bootstrap over test artifacts; per-cell estimates in Figure 1.

### Failure Modes and Diagnostics
- Coverage κ_f < 0.30 (e.g. commit Why fold {5,6} at 26 % in the audit): fold reported as inconclusive for Δ_link; Δ_soft still reported.
- Drift confound: Δ_link shown alongside the realised drift distribution and a descriptive zero-drift vs positive-drift split of the randomised items.
- Δ_soft ≈ 0 everywhere after calibration: "no soft-label gain beyond calibration" — still the paper.
- Residual REL differences after calibration: reported; conclusions scoped to the (T, λ) family.
- Readability: expected null (dispersion reliability ≈ .02); the parent alignment bug is fixed first.

### Novelty and Elegance Argument
One estimand with audited support, three arms differing only in the distributional target, one calibration step, one rotation, and an explicit identification boundary. The closest works lack at least one of: label-preserving randomisation with a shared point label, calibration symmetry, evaluator-identity exclusion, support auditing, or the SE small-panel setting.

## Claim-Driven Validation Sketch
### Claim 1 (main): For the exact Chen objective on commit messages, Δ_soft is ≤ ≈ 0.002 RPS and the ITT Δ_link (coverage ≈ 0.3–0.6) is ≤ ≈ 0.003, replicated across replicates, families and evaluator folds; where Δ_link is non-zero it is on Why.
- Minimal experiment: the commit matrix; Δ_soft, Δ_link, Δ_reg with artifact-cluster CIs overall and per stratum; certification table (κ_f, drift, eligible cells).
- Baselines / ablations: none beyond the three arms; exact-objective sensitivity row in the appendix.
- Metric: calibrated held-out-rater RPS; secondary five-bin REL/RES/UNC.
- Expected evidence: What — both ≈ 0; Why — Δ_soft ≈ 0.002, Δ_link ≈ 0.002–0.003.
### Claim 2 (supporting): On readability the ITT Δ_link ≈ 0 (dispersion reliability ≈ .02, coverage ≈ 0.4–0.8); on summarization Δ_link is not identifiable with 2 target raters (formal boundary) and Δ_soft is ≤ ≈ 0.002.
- Minimal experiment: readability matrix (three arms); summarization matrix (two arms).
- Metric: as above.
- Expected evidence: null on readability; boundary + small Δ_soft on summarization.

## Experiment Handoff Inputs
- Must-prove claims: C1 (commit), C2 (readability null; summarization boundary + Δ_soft).
- Must-run ablations: exact-Chen (α, ε) sensitivity row; certification per fold/replicate; five- vs ten-bin decomposition sensitivity.
- Critical datasets / metrics: commit (primary), readability (direct snippet key), summarization (CA, Conciseness); calibrated RPS vs excluded raters; Δ_soft, Δ_link, Δ_reg; κ_f and drift.
- Highest-risk assumptions: coverage ≥ 0.3 per fold at the declared w; faithful reproduction of the adversarial term; detectability of ≈ 0.002 RPS with artifact-cluster CIs pooled over 18 cells; readability alignment fix upstream.

## Compute & Timeline Estimate
- GPU-hours: ≈ 97 (≈ 103 with the sensitivity row) over ≈ 1 week on 4 shared cards; the pilot harness already implements A_hard, the KL + CE core of A_true, symmetric calibration, the RPS analysis and the support audit.
- Data / annotation cost: none.
- Timeline: exact objective + permutation + rotation implementation 1 week; commit matrix 1 week; readability + summarization 1 week; analysis + writing 4 weeks.
