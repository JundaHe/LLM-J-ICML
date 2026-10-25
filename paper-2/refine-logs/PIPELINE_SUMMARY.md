# Pipeline Summary

**Problem**: Training-side "disagreement-aware judge" claims (soft-label / distributional fine-tuning of LLM judges) are validated against the pooled rating histogram they were trained on; on the 3–9-rater panels of released SE benchmarks one cannot tell item-specific disagreement learning from calibration and scale location.
**Final Method Thesis**: The exact mode-, mean- and pool-preserving target-link randomisation has limited but non-zero finite-sample intensity on released SE panels (max-changed fraction ≈ .25–.32 commit What, .33–.37 commit Why, .47–.59 readability, 0 with two target raters; dose ≈ .40 TV); we state this feasibility result with MDE/power and estimate — with symmetric calibration, excluded rater identities, a matched no-adversary control and explicit intensities — Δ_soft, Δ_adv and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability, per family.
**Final Verdict**: REVISE (7.6/10 after 5 refinement rounds) · external plan review: PROCEED WITH CAUTION (4/10 as written → ≈ 6/10 with the corrections now applied)
**Date**: 2026-08-23

## Final Deliverables
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Refinement report: `refine-logs/REFINEMENT_REPORT.md`
- Support audit (CPU evidence): `refine-logs/SUPPORT_AUDIT.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot
- Dominant contribution: the finite-sample feasibility analysis of the exact target-link intervention — the estimand Δ_link^ITT(G) with G a randomised maximum-cardinality exact matching, three support quantities (full-cell derangeability; max-changed fraction; positive-probability fraction) plus dose, the two-rater lemma, a frozen support model validated out of sample, MDE/power guidance, and the corrected support map (commit Why .33–.37, What .25–.32, readability .47–.59).
- Optional supporting contribution: the scoped audit — Δ_soft (Chen-package gain), Δ_adv (no-adversary control), exact Δ_link^ITT on commit Why (primary), What and readability, per family with CIs, split spread, intensity and dose; Δ_bin-link sensitivity; protocol comparison P0/P1/P2.
- Explicitly rejected complexity: posterior-predictive / CRPS / tie-aware arms; routing heads; per-rater conditioning; RL judges; frontier fine-tuning; non-SE benchmarks; reliability "law"; skill score; ten-bin / isotonic sensitivities; drift-stratified deconfounding; summarization GPU runs.

## Must-Prove Claims
- C1 (CPU): support quantities + dose + MDE per panel; frozen support model validated; the two-rater lemma.
- C2 (GPU, scoped): Δ_soft, Δ_adv, Δ_link^ITT (commit Why primary; What; readability) as per-family estimates with CIs, split spread, intensity and dose.

## First Runs to Launch
1. M0 (CPU): frozen support model + validation; MDE/power simulation; support certificates with subsampled-rater curves; lock the 124-snippet readability universe; exact-Chen parity with released code (+ no-adversary variant); harness unit tests.
2. M1 (GPU, 24 runs ≈ 11 GPU-h): the exact commit-Why gate — Qwen2.5-Coder-7B, split 0, 4 arms × 6 LORO folds; gate = parity / invariants / achieved MDE (never effect direction).
3. M2/M3 (GPU, ≈ 426 runs ≈ 135 GPU-h): remaining commit splits/criteria + Llama; readability 162 runs; w = 2 sensitivity; protocol comparison scoring.

## Main Risks
- The support model may not validate out of sample (pseudo-novelty risk): mitigation — freeze it before testing; if it fails, C1 is an empirical audit and the paper leans on the scoped estimates; if that is too thin, pivot to Package B.
- Partial intensity (≈ 1/3) may leave Δ_link under-powered: mitigation — MDE simulation before running; nulls never read as absence.
- Chen objective not reproducible exactly: mitigation — released configuration; sensitivity row.
- Readability dataset mis-alignment in the parent pipeline: user decision 2026-08-23 — paper already submitted, parent fix deferred; the follow-up uses its own direct-key loader (R001), so Block 4 is not blocked.

## Next Action
- Proceed to `/run-experiment` with M0 (CPU) then the M1 exact commit-Why gate, per `EXPERIMENT_TRACKER.md`; do not launch the full matrix before both gates pass.
