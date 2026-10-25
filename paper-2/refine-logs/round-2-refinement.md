# Round 2 Refinement

## Problem Anchor
- **Bottom-line problem**: Training-side claims that an LLM judge "models human disagreement" (soft-label / distributional fine-tuning, Chen et al. NeurIPS 2025 and successors) are validated against the same pooled rating histogram they were trained on. On the small annotator panels that software-engineering benchmarks actually have (3–9 raters), we need a way to tell whether such a judge learned *which artifacts* split human raters, or merely learned a better-calibrated (smoother) score distribution plus scale-location effects.
- **Must-solve bottleneck**: The existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing; a judge can post large KL/RPS gains over point-SFT while carrying zero item-level disagreement information, and uncertainty-based downstream decisions (routing contested items to humans) inherit that ambiguity.
- **Non-goals**: Not a new judge-training method as the headline; not pairwise preference / reward-model training; not RL judges; not a new multi-rater benchmark; not claims about human populations beyond the released panels; not generation-side (DPO/best-of-n) consequences.
- **Constraints**: Released per-annotator data only (commit messages 800×6, code summarization 1,163×3, readability 200×9); 7B–14B open judges with LoRA on 4 shared RTX 6000 Ada (~22 GB free each) plus small OpenRouter budget for frontier judges as *untrained* references; single PhD student, ~3 months to submission; venue ICSE/FSE (primary) or ACL/NeurIPS Datasets & Benchmarks; parent paper's CSJE/HCA machinery is reusable and must stay consistent with it.
- **Success condition**: A protocol (target-reliability diagnostic → location-aware nulls → label-preserving attribution against held-out individual raters by consensus stratum) that, applied to Chen-style distributional judges on the three SE panels with ≥ 3 seeds and ≥ 2 model families, yields a definite, replicated verdict on whether the distributional gain is item-specific — and that a sceptical reviewer accepts as the right way to audit future "disagreement-aware judge" claims. A positive item-specific residual on some criterion/panel and a null on others is an acceptable (indeed informative) outcome.

## Anchor Check
- Original bottleneck: pooled-histogram validation cannot separate item-linked disagreement learning from global smoothing / location on small panels.
- Why the revised method still addresses it: the fixes make Δ_link a cleaner intervention on exactly the item→histogram link (single point label z_i shared by all losses and permutation cells; randomisation restricted to cells where the histogram actually changes); nothing about the audited object, the panels, or the evaluator-exclusion design changes.
- Reviewer suggestions rejected as drift: none.

## Simplicity Check
- Dominant contribution after revision: Δ_link — the randomised target-link estimand — with a fully executable specification; Δ_soft and the reliability diagnostics remain supporting.
- Components removed or merged: the exact-/coarsened-median branch (replaced by one point label z_i); the untrained frontier-judge row; the conditional summarization-criterion reduction (pre-committed to Content Adequacy + Conciseness); ten-bin decomposition demoted to sensitivity.
- Reviewer suggestions rejected as unnecessary complexity: none.
- Why the remaining mechanism is still the smallest adequate route: three arms differing only in the distributional term's target (none / true / permuted), one shared point label, one calibrator family, one rotation.

## Changes Made
### 1. One point label z_i everywhere (CRITICAL)
- Reviewer said: A_hard used the median while Chen's CE term uses the majority; permutation cells conditioned on the median do not preserve the CE class, so A_perm could change both the shape and the point target.
- Action: z_i := mode of the m_t target raters' ratings (Chen's "most frequent human annotation"); tie rule: among tied modes take the level closest to the median of the target ratings, and if still tied the lower level. A_hard = CE(z_i, q); A_true = α·KL(p_i‖q) + (1−α)·CE(z_i, q) + L_adv(p_i); A_perm = α·KL(p_π(i)‖q) + (1−α)·CE(z_i, q) + L_adv(p_π(i)) — the CE class never changes under permutation. Cells = (pool, z_i, Σ_r y_ir). Stated explicitly: we follow Chen's mode-based point target verbatim; the parent paper's median-based strata are a separate, evaluation-side construct.
- Reasoning: Δ_link must differ from A_true only in the distributional target.
- Impact on core method: cleaner identification; no other change.
### 2. Sparse-cell scope and the actually-changed fraction (CRITICAL)
- Reviewer said: singleton cells keeping their histogram are "no randomisation" and attenuate Δ_link; a fallback that changes z_i or the sum is not allowed.
- Action: (i) the *training set* of every arm (A_hard, A_true, A_perm alike) is restricted to items in swappable cells — cells with ≥ 2 items and ≥ 2 distinct histograms; (ii) π is a derangement that maps every item to an item of the same cell with a *different* histogram (constructed by random cyclic shifts over the distinct-histogram classes within the cell), so the changed-histogram fraction within the training set is 100 % by construction; (iii) test and calibration sets are unrestricted; (iv) the report gives the swappable fraction of the original training pool per benchmark / criterion / fold / seed, and the estimand is explicitly scoped to judges trained on the swappable population (a per-protocol, not intent-to-treat, effect); (v) no fallback alters z_i or Σ y; if the swappable fraction is < 70 % for a criterion the criterion is reported with that caveat, and Δ_link is still defined (on the swappable population).
- Reasoning: the reviewer's two options; we take the per-protocol one, which keeps z_i and the sum intact and makes "changed" literal.
- Impact on core method: identical arms trained on identical item sets; only the distributional target differs.
### 3. Interpretation corrected (IMPORTANT)
- Reviewer said: Δ_soft − Δ_link is a link-independent soft-target / regularisation effect, not a calibration component; the two-parameter calibrator only removes calibration representable by its family.
- Action: the decomposition is now stated as Δ_soft = Δ_link + Δ_reg, with Δ_reg := RPS(A_hard) − RPS(A_perm) = the link-independent effect of training on *some* histogram of the right label and location (regularisation plus any residual reliability difference the calibrator family cannot remove); the REL term of the decomposition is used to check how much residual reliability difference remains after calibration.
- Reasoning: accuracy of claims.
- Impact on core method: wording of claims and tables only.
### 4. Aggregation and inference locked (IMPORTANT)
- Reviewer said: define Δ as an expectation over folds, seeds, permutations, families; artifact-clustered inference should be primary because the target is the fixed released panel; do not bootstrap three summarization raters as a population.
- Action: Δ (soft / link / reg) := the mean over evaluator folds f, paired seeds s (each s fixes split, init, order and π), and families g of the item-level paired RPS difference, averaged over the evaluator raters of fold f; primary inference = bootstrap over artifacts (clusters = diff / function / snippet) of the item-level paired differences already averaged over f, s, g and evaluators; fold-, seed- and family-wise estimates reported descriptively (tables / Figure 1), no rater-population bootstrap anywhere.
- Reasoning: matches the non-population claim.
- Impact on core method: none.
### 5. Executable specification completed (IMPORTANT)
- Reviewer said: state tie rule, α, ε, adversarial steps/projection, calibrator equation and grid, climatology source, pooling rule.
- Action: all given in the Revised Proposal (Core Mechanism / Training Plan).
### 6. Simplifications adopted
- Five-bin REL/RES/UNC is the declared secondary estimator (ten-bin → sensitivity); the untrained frontier-judge row is removed; summarization criteria pre-committed to Content Adequacy and Conciseness (Fluency not run).

## Revised Proposal

# Research Proposal: When Do Soft-Label LLM Judges Add Conditional Resolution Beyond Calibration? A Randomised Target-Link Audit on Small SE Annotator Panels

## Problem Anchor
(verbatim as above)

## Technical Gap
Soft-label judge training (Chen et al. 2505.12301: α·KL to the empirical histogram + (1−α)·CE to the majority label + an adversarial ℓ₂-ball term; Li et al. 2510.00263; Singh et al. 2511.14117) is scored against the *same pooled histogram* it was fitted to. Three facts make that score uninterpretable as evidence of "learned disagreement": (1) a proper score decomposes into reliability − resolution + uncertainty, and a globally calibrated point-label judge can match a soft-label judge on RPS with identical resolution — in our commit-message pilot the raw CE→KL gain (+0.004 What / +0.011 Why RPS) shrinks to +0.0008 [−0.0001, +0.0017] / +0.0018 [+0.0005, +0.0031] once the same two-parameter calibrator is fitted to both arms; (2) on bounded ordinal scales the Low-consensus stratum is predictable from the pooled median alone (AUROC .67/.80), so entropy-based "disagreement detection" is mostly location; (3) averaging a held-out-rating score over all raters *is* the pooled-histogram score plus a model-free constant, so "held-out rater" must mean held-out rater *identity*, excluded from every target and calibrator. Naive fixes (more raters — unavailable; heavier Bayesian targets — over-shrink, Kohli 2605.29797 and our k = 2 pilot; ordinal losses — tie with KL; the adversarial ball — a regulariser) do not identify the item-linked component. What is missing is a randomised estimand.

## Method Thesis
- One-sentence thesis: The item-linked component of a soft-label judge's gain is identified by **Δ_link**, the loss in calibrated held-out-rater RPS incurred when the judge is trained on histograms randomly re-assigned among artifacts that share the same authorship pool, point label z_i and rating sum — and on small SE panels this component is small relative to the link-independent soft-target effect Δ_reg.
- Why this is the smallest adequate intervention: no new model, no new loss; one randomised training target and one symmetric calibration step added to the existing pipeline.
- Why this route is timely: soft-label / distributional judges and reward models are proliferating; the community needs an instrument to read their numbers before adopting them as "disagreement-aware".

## Contribution Focus
- Dominant contribution: the randomised target-link estimand Δ_link — definition, identification conditions (within-cell exchangeability of histograms given (pool, z_i, Σy); no evaluator leakage; calibration fitted on target raters only), scope (swappable population), failure modes — and its replicated estimate for the exact Chen objective on the three released multi-rater SE benchmarks (2 families × 3 paired seeds × 3 evaluator folds).
- Optional supporting contribution: the decomposition Δ_soft = Δ_link + Δ_reg read with five-bin REL/RES/UNC; split-panel dispersion reliability as a pre-audit diagnostic reported as a descriptive moderator.
- Explicit non-contributions: no new training objective; no routing; no metric claims; no panel-size law; no population claims beyond the released panels.

## Proposed Method
### Complexity Budget
- Frozen / reused: Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct; verbatim single-criterion benchmark prompts (Zeng WHAT / WHY zero-shot templates; Crupi per-criterion variants of the three-criterion template; CoReEval readability prompt); LoRA r = 16, α_LoRA = 32, dropout 0.05 on q/k/v/o/gate/up/down; parent CSJE strata code (strata from target raters).
- New trainable components: none (LoRA adapters per arm).
- Tempting additions intentionally not used: posterior-predictive / CRPS / tie-aware training arms; per-rater conditioning; RL judges; routing heads; frontier fine-tuning; non-SE benchmarks; untrained frontier-judge rows.

### System Overview
```
per-annotator ratings H (n × m) ── artifact-grouped split (diff / function / snippet): train 60 % · calibration 10 % · test 30 %   [paired seed s]
   │
   ├─ evaluator fold f: raters E_f excluded from every target and from calibration; m_t = m − |E_f| target raters
   ▼
point label z_i = mode of target ratings (ties → level closest to the target median, then lower); histogram p_i over the 5 levels
cells c(i) = (pool, z_i, Σ_r y_ir);  swappable cells = |c| ≥ 2 with ≥ 2 distinct histograms;  training set := train items in swappable cells (ALL arms)
π = within-cell derangement over distinct-histogram classes (random cyclic shift; seed s)  ⇒  p_π(i) ≠ p_i for every training item
   ▼
A_hard : CE(z_i, q)
A_true : α·KL(p_i ‖ q) + (1−α)·CE(z_i, q) + L_adv(p_i, q)
A_perm : α·KL(p_π(i) ‖ q) + (1−α)·CE(z_i, q) + L_adv(p_π(i), q)
   ▼
LoRA judge → score-token distribution q_A(x) on calibration + test items
   ▼
symmetric arm-specific calibration  C_A(q) = (1−λ_A)·softmax(log q / T_A) + λ_A·p_clim ;  (T_A, λ_A) = argmin over the grid of mean RPS against the m_t target raters on calibration items
   ▼
scoring on test items against each evaluator rater r ∈ E_f :  RPS_r(C_A(q_A)) = Σ_{k=1}^{4} (CDF_A(k) − 1[y_r ≤ k])² / 4
   ▼
Δ_soft = RPS(A_hard) − RPS(A_true);  Δ_link = RPS(A_perm) − RPS(A_true);  Δ_reg = RPS(A_hard) − RPS(A_perm) = Δ_soft − Δ_link
secondary: five-bin threshold-Brier REL / RES / UNC;  certification: swappable fraction, changed fraction (= 100 % by construction), preserved statistics (z_i, Σy, mean, pool)
   ▼
inference: Δ := mean over f, s, g of item-level paired differences (averaged over r ∈ E_f); bootstrap over artifacts of those item-level means (primary); per-f/s/g estimates descriptive
```

### Core Mechanism
- Input / output: artifact + single-criterion prompt → q_A(x) ∈ Δ⁴; evaluator = a human rating whose rater identity was excluded from every target and calibrator.
- Architecture or policy: unchanged judge. The mechanism is the *design*: (i) A_perm preserves, for every training item, z_i (hence the CE class), Σy (hence the mean), the pool and the cell membership, and changes only which histogram shape is attached to which artifact; (ii) symmetric arm-specific calibration removes the calibration differences representable by the (T, λ) family, so the contrasts compare information rather than smoothness — residual reliability is monitored via REL; (iii) evaluator exclusion removes panel memorisation.
- Training signal / loss: as in the overview. Exact Chen hyper-parameters: (α, ε*, inner steps, learning rate, optimiser) taken from the paper's released configuration; the adversarial term L_adv is the paper's inner maximisation over p′ ∈ Δ⁴ ∩ B_ε*(p) (projected gradient ascent on p′ for the released number of steps; projection = ℓ₂-ball clipping followed by Euclidean projection onto the simplex), applied identically in A_true and A_perm; if the release lacks a value, the paper's ablation value is used and varied in the sensitivity row. Identical steps, schedules, LoRA init and data order across arms within a seed.
- Why this is the main novelty: Chen/Li evaluate on the fitted histogram; Gheibi 2605.20642 shuffles globally (destroying the label); Kohli 2605.29797 holds out an annotator *group* without calibration symmetry or link randomisation; Calderon 2501.10970 is leave-one-annotator-out for point judges. None defines or estimates a label-, mean- and pool-preserving randomised link estimand against excluded rater identities.

### Optional Supporting Component
- Pre-audit diagnostics (CPU, one table): split-half Spearman of per-item dispersion across disjoint rater halves (Spearman–Brown corrected) per criterion; swappable fraction and preserved-statistics per fold/seed. Used to *interpret* Δ_link, never as a law.

### Modern Primitive Usage
- Open-weight instruction LLM judge (score-token distribution from logits) with LoRA — the audited object; intentionally non-frontier on the method side.

### Integration into Base Generator / Downstream Pipeline
Plugs into the parent CSJE pipeline (strata from target raters; same distance conventions). Inference = one forward pass per item per criterion; calibration = two scalars per arm.

### Training Plan
- Splits: 60/10/30 by artifact; paired seed s ∈ {0, 1, 2} fixes split, LoRA init, data order and π.
- Evaluator folds: commit {1,2}, {3,4}, {5,6}; readability {1,2,3}, {4,5,6}, {7,8,9}; summarization leave-one-out over 3 raters (2-rater targets; flagged low-power).
- Criteria: commit What, Why (single-criterion prompts); summarization Content Adequacy, Conciseness (pre-committed; Fluency not run); readability (one criterion).
- Runs: 3 arms × 3 folds × 3 seeds × 2 families = 54 per benchmark-criterion → commit 108, summarization 108, readability 54 = 270 LoRA runs.
- Cost: commit ≈ 0.45 GPU-h, summarization ≈ 0.6, readability ≈ 0.1 → ≈ 49 + 65 + 5 ≈ **120 GPU-h**, ≈ 1.3 weeks on 4 shared cards (≈ 135 GPU-h with the sensitivity row).
- Calibration: grid T ∈ {0.5, 0.7, 0.85, 1, 1.25, 1.5, 2, 3, 4, 6} × λ ∈ {0, .05, .1, .2, .3, .5}; p_clim = level marginal of the target raters over training items; objective = mean RPS over target raters on calibration items; fitted once per arm × fold × seed × family.
- Pooling rule: Δ for a (benchmark, criterion) = mean over the 18 (f, s, g) cells of the item-level paired differences (each averaged over its evaluators); bootstrap over artifacts (B = 2000) of the item-level means; per-(f, s, g) estimates shown descriptively.

### Failure Modes and Diagnostics
- Swappable fraction < 70 %: report; estimand remains defined on the swappable population; no fallback that alters z_i or Σy.
- Δ_soft ≈ 0 everywhere after calibration: "no soft-label gain beyond calibration" — still the paper.
- Δ_link > 0 but Δ_soft ≈ 0: histograms carry item information without net gain — reported as such.
- Residual REL differences after calibration: reported; if large, the calibrator family is widened (isotonic per threshold) in a sensitivity row.
- Readability: expected null (reliability ≈ .02); the parent alignment bug is fixed first.

### Novelty and Elegance Argument
One estimand, three arms differing only in the distributional target, one calibration step, one rotation. The closest works lack at least one of: label/mean/pool-preserving randomisation with a shared point label, calibration symmetry, evaluator-identity exclusion, or the SE small-panel setting. A measurement contribution in the parent paper's lineage (CSJE/HCA → training-side audit), asking a different question (what training learned) with a different instrument (randomised targets).

## Claim-Driven Validation Sketch
### Claim 1 (main): For the exact Chen objective on commit messages, Δ_soft is ≤ ≈ 0.002 RPS and Δ_link is ≤ ≈ 0.003, replicated across seeds, families and evaluator folds; where Δ_link is non-zero it is on Why, the criterion with the higher split-panel dispersion reliability.
- Minimal experiment: the 3 × 3 × 3 × 2 matrix on commit messages (What, Why); Δ_soft, Δ_link, Δ_reg with artifact-cluster CIs overall and per stratum; certification table.
- Baselines / ablations: none beyond the three arms; exact-objective sensitivity row in the appendix.
- Metric: calibrated held-out-rater RPS; secondary five-bin REL/RES/UNC.
- Expected evidence: What — both contrasts ≈ 0; Why — Δ_soft ≈ 0.002, Δ_link ≈ 0.002–0.003.
### Claim 2 (supporting): The same decomposition on code summarization (CA, Conciseness) and correctly aligned readability yields Δ_link ≈ 0 where split-panel dispersion reliability is ≈ 0, and at most small elsewhere.
- Minimal experiment: same matrix on the two benchmarks.
- Metric: as above; reliability reported descriptively.
- Expected evidence: null on readability; small or null on summarization.

## Experiment Handoff Inputs
- Must-prove claims: C1 (commit), C2 (breadth).
- Must-run ablations: exact-Chen (α, ε) sensitivity row; certification per fold/seed; five- vs ten-bin decomposition sensitivity; widened calibrator sensitivity if REL residuals are large.
- Critical datasets / metrics: commit (primary), summarization (CA, Conciseness), readability (direct snippet key); calibrated RPS vs excluded raters; Δ_soft, Δ_link, Δ_reg.
- Highest-risk assumptions: swappable fraction ≥ 70 % on commit/summarization; faithful reproduction of the adversarial term; detectability of ≈ 0.002 RPS with artifact-cluster CIs pooled over 18 cells (pilot half-widths ≈ 0.001 per cell → pooled ≈ 0.0005); readability alignment fix upstream.

## Compute & Timeline Estimate
- GPU-hours: ≈ 120 (≈ 135 with sensitivity rows) over ≈ 1.3 weeks on 4 shared cards; the pilot harness already implements A_hard, the KL + CE core of A_true, symmetric calibration and the RPS analysis.
- Data / annotation cost: none.
- Timeline: exact objective + permutation + rotation implementation 1 week; commit matrix 1 week; breadth 2 weeks; analysis + writing 4 weeks.
