# Refinement Report

**Problem**: Training-side "disagreement-aware judge" claims (soft-label / distributional fine-tuning of LLM judges) are validated against the pooled rating histogram they were trained on; on the 3–9-rater panels of released SE benchmarks one cannot tell item-specific disagreement learning from calibration and scale location.
**Initial Approach**: Package A from `/idea-discovery` (learnability ceiling → held-out-rater attribution test with temperature/mixture nulls and a median-matched permutation placebo → small-panel posterior-predictive target → matched-human routing), revised after the novelty check and the round-1 external review into an "attribution audit".
**Date**: 2026-08-23
**Rounds**: 5 / 5
**Final Score**: 7.6 / 10
**Final Verdict**: REVISE (MAX_ROUNDS reached; best current version in `FINAL_PROPOSAL.md`)

## Problem Anchor
See `PROBLEM_ANCHOR.md` (verbatim in every round file).

## Output Files
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Final proposal: `refine-logs/FINAL_PROPOSAL.md`
- Support audit (CPU evidence): `refine-logs/SUPPORT_AUDIT.md`
- Rounds: `round-0-initial-proposal.md`, `round-{1..5}-review.md`, `round-{1..4}-refinement.md`, `score-history.md`
- Reviewer traces: `.aris/traces/research-refine/2026-08-23_run01/` (thread `01a02b0b-40c2-7c60-8526-1ce3cf8263a0`)

## Score Evolution
| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict |
|-------|------------------|--------------------|----------------------|-------------------|-------------|------------------|-----------------|---------|---------|
| 1     | 9 | 6 | 6 | 8 | 6 | 5 | 6 | 6.7 | REVISE |
| 2     | 9 | 6 | 8 | 8 | 8 | 8 | 7 | 7.6 | REVISE |
| 3     | 8 | 6 | 8 | 8 | 6 | 7 | 7 | 7.2 | REVISE |
| 4     | 8 | 6 | 7 | 8 | 8 | 7 | 6 | 7.1 | RETHINK |
| 5     | 9 | 7 | 7 | 8 | 8 | 8 | 7 | 7.6 | REVISE (final) |

## Round-by-Round Review Record
| Round | Main Reviewer Concerns | What Was Changed | Result |
|-------|-------------------------|------------------|--------|
| 1 | no formal estimand; calibrator ambiguity; permutation unspecified; five arms; rotation/budget mismatch | Δ_soft / Δ_link; symmetric arm-specific calibration; three arms; rater-disjoint folds for all arms; endpoints pruned | resolved |
| 2 | median vs mode point target; sparse cells; Δ_reg naming; inference | shared z_i; swappable-cell scope; Δ_reg; artifact-cluster inference; executable spec | resolved (scope issue introduced) |
| 3 | zero support with 2 target raters; M ≤ N/2; per-protocol scope drift; split seeds; triggered calibration | support audit run; full-data ITT; bounded Σy relaxation; summarization boundary; immutable split | partially (relaxation confounds location) |
| 4 | relaxed contrast is composite; width rule inconsistent; audit LORO first | LORO audit; reframed as identifiability audit; Δ_link exact only on readability; Δ_bin-link named; w* rule; intensities | resolved by reframing |
| 5 | formalise Δ_link^ITT(G_f); distinguish impossibility / positivity / adequacy; no "upper bound"; specify or downgrade the bound; lock readability universe; scope nulls | applied in FINAL_PROPOSAL (wording, scope, estimand); formal proposition scheduled as M0 deliverable | mostly; formal result pending |

## Final Proposal Snapshot
- Canonical clean version lives in `refine-logs/FINAL_PROPOSAL.md`.
- Thesis (after the external round-2 correction): the exact target-link intervention has limited but non-zero intensity (max-changed .25–.32 commit What, .33–.37 commit Why, .47–.59 readability, 0 with two target raters); feasibility + MDE stated, scoped estimates per family.
- Dominant contribution: the finite-sample feasibility analysis (Δ_link^ITT(G) with randomised maximum matching; support quantities and dose; frozen support model; lemma; MDE).
- Supporting: scoped audit — Δ_soft, Δ_adv (no-adversary control), exact Δ_link^ITT on commit Why / What / readability; Δ_bin-link sensitivity.
- Compute: 450 LoRA runs ≈ 146 GPU-h (+ sensitivities), stage-gated on correctness/power gates (M0, M1 exact commit-Why gate).

## Method Evolution Highlights
1. Most important simplification: five training targets and four diagnostic families → three arms, one estimand, one calibration step, one rotation.
2. Most important mechanism upgrade: the support audit (rounds 3–4, corrected by the external review's round 2 to randomised maximum matching on the grouped split) — it replaced an assumed clean placebo by a quantified intervention with intensity and dose, and changed the thesis from attribution to feasibility + scoped audit.
3. Most important justification for staying simple: every round's reviewer stated "Modernization: NONE" — RL/DPO/per-rater embeddings/frontier fine-tuning would weaken identification.

## Pushback / Drift Log
| Round | Reviewer Said | Author Response | Outcome |
|-------|---------------|-----------------|---------|
| 3 | per-protocol training narrows the audited object | accepted: full-data ITT adopted | accepted |
| 4 | relaxed permutation ≠ identified disagreement; audit LORO before relaxing | accepted: LORO audit run; reframed | accepted |
| 5 | κ ≥ 0.30 is an adequacy criterion, not identifiability; Δ_bin-link is not an upper bound; bound unspecified | accepted: wording and estimand corrected; formal result scheduled | accepted |
| — | (no pushback was warranted; every reviewer objection survived verification) | — | — |

## Remaining Weaknesses
- The frozen, out-of-sample-validated support model and the MDE simulation are not yet written; without them the contribution risks reading as an empirical sparsity audit (pseudo-novelty).
- Δ_link may be under-powered: the exact intervention has ≈ one-third intensity on commit (corrected audit), ≈ one-half on readability (unreliable target, ≈ 37 test snippets), and zero on summarization; MDE simulations precede any GPU run.
- Faithful reproduction of Chen's adversarial objective (released hyper-parameters) is a prerequisite; the readability dataset must be fixed upstream (parent-paper scripts mis-align 81.5 % of snippets).
- Pilot evidence is one model, one seed, 120 independent diffs; the Δ_soft estimate must be replicated before it is quoted.
- Parent-paper overlap: the audit reuses CSJE/HCA plumbing; the identifiability result must carry the paper.

## Raw Reviewer Responses
<details><summary>Rounds 1–5</summary>
Condensed copies in `round-N-review.md`; full prompt/response pairs in `.aris/traces/research-refine/2026-08-23_run01/00{1..5}-round-N-review.*`.
</details>

## Next Steps
- REVISE: write the formal positivity proposition and the concentration model (M0), then `/run-experiment` on the stage-gated plan (`EXPERIMENT_PLAN.md`, `EXPERIMENT_TRACKER.md`); re-run `/research-refine` only if M0 changes the estimand.
