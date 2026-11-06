# Compression plan: draft v2.5 (about 8,900 words, 15 pages) → ICML main body (8 pages) + appendix

Written 2026-11-07 04:31. PAPER_DRAFT_v2.md stays the full record and the source for check_consistency.py. The new file PAPER_ICML_v3.md is the 8-page main text plus an appendix. Numbers are copied verbatim from v2.5; none are recomputed.

## Main body (target about 5,000 words of text + 3 tables + 1 figure)
| § | content | words | float |
|---|---|---|---|
| Abstract | ≤ 250 words | 250 | |
| 1 Introduction | motivation; two questions; four findings (reproducibility, decodability with DICES-350 vs NLI as the clean contrast, judges, budget on POPQUORN); contributions; non-claims | 900 | |
| 2 Related work | label variation, distributional judges, annotation budget, rater models | 300 | |
| 3 Reliability across raters | ρ = X/M and the identity A1 = M − 2X; X_own; population; results | 850 | Table 1 (cards), Fig. 1 |
| 4 Reliability across text | cross-fitted decoder; G_own/X_own and CLT; plants; DICES-350 vs NLI; Dorn location-sized; the rest undetectable | 950 | Table 2b (own-shape) |
| 5 What judges use | donor-replacement audit (LoRA + heads), ChaosNLI as the discriminating case; rater–item decomposition (short) | 650 | |
| 6 Annotation budget | frozen heads at a fixed budget; POPQUORN prospective LoRA; SummEval as dilution (2 sentences, pointer to App.) | 550 | Table 6 (prospective rows only) |
| 7 Limitations and conclusion | the 5 limitations, condensed; SummEval data caveat; conclusion | 500 | |

## Appendix
- A. Estimators: the identity, X_cross, the CLT interval and its calibration (R21-1), the null bias (R21-2), population/crossed bootstrap.
- B. Full decoding results: Table 2 (cross-term-inclusive G/X), valid-forecast gain, all plants (R20-2, R21-7, R22-3, R22-4), and the a = 4 ChaosNLI check.
- C. SummEval data: duplication finding, no-dup results (R22-1/2), expert dilution (R20-7), provenance.
- D. LoRA blocks: all blocks (shared-assignment, prospective, reruns, OLMo), evaluator dependence, nondeterminism.
- E. Software-engineering panels (v2 §6), three-rater support.
- F. Frozen-feature budget heads (Table 5), shrinkage for annotation (v2 §4 end), rater–item model details.

## Order of work
1. Abstract + §1 (this step)
2. §3 + §4
3. §5 + §6 + §7
4. Appendix
5. Build: a check_consistency run on v3 (with check_consistency pointed at v3), then LaTeX.
