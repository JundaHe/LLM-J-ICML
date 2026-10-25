# Review Summary

**Problem**: Training-side "disagreement-aware judge" claims (soft-label / distributional fine-tuning) are validated against the pooled histogram they were trained on; on 3–9-rater SE panels one cannot tell item-specific disagreement learning from calibration and scale location.
**Initial Approach**: Package A from `/idea-discovery` — learnability ceiling → held-out-rater attribution test (temperature/mixture nulls + median-matched permutation placebo) → small-panel posterior-predictive target → matched-human routing.
**Date**: 2026-08-23
**Rounds**: 5 / 5 (MAX_ROUNDS reached)
**Final Score**: 7.6 / 10
**Final Verdict**: REVISE (best current version written to `FINAL_PROPOSAL.md`)

## Problem Anchor
- Bottom-line problem: training-side claims that an LLM judge "models human disagreement" are validated against the same pooled histogram they were trained on; on 3–9-rater SE panels we need a way to tell whether the judge learned *which artifacts* split raters or merely a smoother, better-located distribution.
- Must-solve bottleneck: the existing evaluation contract cannot distinguish item-specific disagreement learning from global smoothing.
- Non-goals: no new training method as headline; no RM/RL/routing/benchmark/population claims.
- Constraints: released per-annotator data; 7B–14B LoRA on 4 shared GPUs; single PhD student; ICSE/FSE.
- Success condition: a protocol that yields a definite, replicated verdict on whether the distributional gain is item-specific — a null / boundary verdict is acceptable.

## Round-by-Round Resolution Log
| Round | Main Reviewer Concerns | What This Round Simplified / Modernized | Solved? | Remaining Risk |
|-------|-------------------------|------------------------------------------|---------|----------------|
| 1 (6.7, REVISE) | no formal estimand; ambiguous "shared calibrator"; permutation cells unspecified; rotation inconsistent; five arms + reliability "law" = sprawl; GPU accounting ≠ design | defined Δ_soft / Δ_link; symmetric arm-specific calibration; cells (pool, median, Σy); three arms; rater-disjoint rotation for every arm; endpoints pruned | yes | — |
| 2 (7.6, REVISE) | A_hard used the median while Chen's CE uses the mode → A_perm could change the CE class; sparse cells; Δ_soft − Δ_link mis-named; inference/aggregation unspecified | one point label z_i everywhere; per-protocol swappable-cell scope; Δ_reg interpretation; artifact-cluster inference; executable spec (tie rule, grid, adversarial loop) | yes | per-protocol scope narrows the object |
| 3 (7.2, REVISE) | zero support on 2-rater targets (summarization); M ≤ N/2 needed for a derangement; per-protocol = scope drift → full-data ITT; split seeds make item means ill-defined; triggered calibration branch | support audit run on the real panels (exact coverage 0–7 % on commit!); full-data ITT; pre-declared bounded Σy relaxation; summarization as boundary; one immutable split + replicate seeds | partly | relaxation breaks location |
| 4 (7.1, RETHINK) | relaxed permutation breaks shape AND within-class location → not "identified disagreement"; width rule inconsistent; LORO support must be audited first | LORO support audit (commit ≤ 14 %, readability 31–51 %, summarization 0); reframed as an identifiability audit; Δ_link exact only where supported (readability); Δ_bin-link named on commit; explicit w* rule; every fold included with κ_f as intensity; claims as estimates + CIs | yes (reframing) | pseudo-novelty of a sparsity audit |
| 5 (7.6, REVISE, final) | distinguish structural impossibility / partial positivity / adequacy threshold; Δ_bin-link is not an upper bound; "combinatorial bound" unspecified; readability universe; scope nulls; inference language | estimand Δ_link^ITT(G_f) formalised; "upper bound" removed; support result = exact enumeration + stated concentration model (proposition to be completed); readability locked to 124 keyed snippets; Δ_reg demoted; summarization GPU runs cut | mostly (wording/formalisation applied in FINAL_PROPOSAL; the formal proposition is M0 work) | general, predictive positivity result not yet written |

## Overall Evolution
- The method became more concrete: from "an audit with nulls and a placebo" to a fully specified estimand (shared point label z_i, eligible cells with M ≤ N/2, verified derangement, symmetric arm-specific calibration with a fixed grid, evaluator-identity exclusion, one immutable split, artifact-cluster inference).
- The dominant contribution became more focused — and changed: the CPU support audit showed the intended clean placebo is unsupported on the primary panel, so the paper's thesis moved from "we attribute the gain" to "here is when attribution is identifiable, and here is what remains estimable".
- Unnecessary complexity was removed: five arms → three; posterior-predictive / tie-aware / routing / reliability-law / skill-score / ten-bin / isotonic / drift-split / summarization-GPU components all cut.
- Modern leverage stayed intentionally minimal (LoRA judges with score-token distributions; no RL / DPO / frontier fine-tuning) — the reviewer agreed in every round.
- Drift was avoided: the one scope narrowing (per-protocol training) was caught in round 3 and reversed; the round-4 reframing was explicitly declared as a thesis change answering the anchored question.

## Final Status
- Anchor status: preserved (reframing answers whether the anchored claim can be tested).
- Focus status: tight (one dominant contribution; supporting audit explicitly scoped).
- Modernity status: appropriately frontier-aware / intentionally conservative.
- Strongest parts of final method: the support condition + enumeration + two-rater lemma + empirical support map; symmetric calibration with excluded-rater evaluation; honest ITT intensities.
- Remaining weaknesses: the formal, predictive positivity result is not yet written (pseudo-novelty risk); a clean positive estimate of disagreement learning may be unattainable on these panels; faithful Chen reproduction and the readability dataset fix are prerequisites; the pilot evidence rests on one model / one seed / 120 independent diffs.
