# ROUND23 protocol — response to the round-23 adversarial review of v3 (Claude subagent standing in for Codex; reviews/claude_round23_v3_2026-11-11.md)

Written 2026-11-11 14:52, before any new computation below. Items marked POST HOC respond to a review that had already seen the results.

## R23-1 — DICES-350: report V_own (POST-HOC reporting change, no new computation)

- **Finding verified from existing artefacts** (review C1).
  - On DICES-350 at a = 40 / b = 20, the linear covariance term V_own = ⟨r̂, s₂⟩/n excludes 0 in all three feature families:
    - Qwen2.5: 4.9e−6 [2.3, 7.5]e−6
    - Qwen3: 2.8e−6 [1.0, 4.6]e−6
    - OLMo-2: 2.3e−6 [0.5, 4.1]e−6
  - The five location-and-threshold (γ 0) draws give V_own 0.07–1.0e−6, mean 4.7e−7 (ROUND22 already logs "about 10 % of the observed").
  - The net-of-penalty ratio is 15 % [3, 27] on Qwen2.5, 10 % [0, 19] on Qwen3, and 7 % [−2, 16] on OLMo-2.
  - G_own/X_own stays at −1 to 1 %.
- **Consequence.** "The observed shape is not decoded" is too strong. The correct reading is that a small text-covarying component of DICES-350's own-shape is detectable, but the linear decoder gets no proper-score gain from it, because the variance penalty cancels the covariance.
- **Change.**
  - The DICES-350 sentence in the abstract, §1, §4 and §7 is rewritten.
  - V_own and the γ 0 baseline are added to the DICES-350 paragraph.
  - The NLI–ordinal contrast is stated as a contrast in proper-score gain, G_own/X_own, not in "decodability".
  - No estimate changes.

## R23-2 — DICES-350 rater-model simulation at more split repetitions (review H4)

- **Problem.** v3 §5 says rater thresholds (M1) reproduce DICES-350's X_own at 40 + 20 raters. That claim used the observed X_own at R = 5 split repetitions in rater_item_dense.py (1.79e−5). The R = 10 decoding run gives 4.9e−5. Against 4.9e−5, no model's 95 % simulation range covers the observed value:

  | Model | Upper end of 95 % simulation range |
  |---|---|
  | M0 | 1.4e−5 |
  | M1 | 2.1e−5 |
  | M2 | 2.5e−5 |

  The observed X_own is therefore unstable over split repetitions at R = 5.
- **Run.** rater_item_dense.py --panel dices --R 20 --sims 40, written to results/rater_item_dense/dices_r23.json. Only a --tag option is added to the script; the original file is untouched. Same seeds per model and the same λ_σ.
  - CPU, Slurm.
  - Bw and dorn_java are rerun in the same way, so that the §5 sentence is consistent across panels.
- **Frozen reading.** The rule is unchanged from R19-3: a model reproduces X_own iff the observed X_own at a = 40 (or the largest a) lies within its simulated 95 % range.
  - For DICES-350, the §5 sentence becomes whatever this run gives, reported as is, including "no rater model reproduces it".
  - If M1 still reproduces it at R = 20, the sentence stays, and the R = 5 vs R = 10 discrepancy is disclosed.
  - The draft's other DICES numbers are unaffected.

## R23-2 result (2026-11-11 16:17, job 15521; frozen reading, no revision)

R = 20 split repetitions, 40 simulations per model, a = 40 (+ 20) raters; values ×10⁻⁵.

| Panel | Observed X_own (R = 5 → R = 20) | M0 95 % range | M1 95 % range | M2 95 % range | Reproduces (R = 20) | Reproduced at R = 5 (R19-3) |
|---|---|---|---|---|---|---|
| DICES-350 | 1.79 → 4.83 | [−2.73, 1.69] | [−3.73, 0.03] | [−2.55, 2.24] | none | M1, M2 |
| Buse–Weimer | 10.6 → 16.8 | [0.97, 14.7] | [−0.70, 12.9] | [15.4, 30.6] | M2 only | M0, M1 |
| Dorn Java | 18.0 → 20.5 | [3.15, 12.0] | – | [20.9, 37.4] | none (between M0 and M2) | M2 |

- **Reading (as frozen).** On DICES-350 no rater model reproduces the observed X_own; the threshold model M1 generates no own-shape (mean −1.7). The §5 sentence "thresholds reproduce the observed X_own where location alone does not" is withdrawn.
- **Not anticipated by the protocol.** The readings on Buse–Weimer and Dorn Java also changed (BW: location alone no longer suffices, only the dispersion model reproduces; Dorn Java: the observed value is just below the dispersion model's range). The observed X_own moved with the number of split repetitions on all three panels, so the reproduce / does-not-reproduce reading is not stable at R = 5. The paper now reports the R = 20 readings as they are, discloses the R = 5 readings, and draws no conclusion about which rater model generates the residual shape.
- **Text changes (v3 §5, Appendix F, long-form finding (iv); v2 abstract, §4, finding (iv)).** "Whether the residual shape itself is rater-side" is now "not established on any panel" (was "established only on DICES-350"). The likelihood statement (rater cut-points +0.05–0.16 nats per rating) is unaffected and is now worded as likelihood structure. The a = 10 X_cross figures are updated to this run (BW 0.00033 of 0.00045; Dorn Java 0.00054 of 0.00080). A corrupted `\text` (a tab character) in the Appendix F formulae of both drafts is fixed.
- **Checks.** check_consistency.py passes for v3 and v2; v3 rebuilt, main text ends on page 8 (references start page 9), 0 undefined, 0 overfull.

## Deferred (need a decision; not run in this round)

- **Matched-design block** (review change 2):
  - ChaosNLI subsampled to 350 items at 20/20 raters per half;
  - an NLI plant;
  - a partial-predictability plant on DICES-350 giving a minimum detectable text-predictable fraction;
  - a nominal comparator that also fixes the runner-up class.

  This is a large new block and would be specified in its own protocol before running.
- **Text items:** H2, H3, H5, H6 and H7 (overclaiming, contribution 3, budget headline, Table 1 caption, related work). These go in the next text revision, after R23-2.
