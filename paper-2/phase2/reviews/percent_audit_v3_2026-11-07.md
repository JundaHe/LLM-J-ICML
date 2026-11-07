# Percentage audit of PAPER_ICML_v3.md (2026-11-07)

Scope: every percentage in `PAPER_ICML_v3.md` except confidence levels ("95 %", "90 %"). Each value was recomputed from the artefacts under `results/`. The script is `/scratch/jundahe/tmp/claude-1009/-scratch-jundahe/37e80840-40ff-46af-af94-89c1d6cafae4/scratchpad/percent_audit.py` and it only reads files.

Conventions:
- `dd/` stands for `results/decode_decomp/`. Ratios are `est` and `clt.ci95` of `G_own/X_own`. "Net" is `G_own_net/X_own`.
- Intervals in the paper are **rounded outward** (floor for the lower bound, ceil for the upper), as ROUND22 states. A value that matches under that convention is marked MATCH.
- ROUNDING-ONLY means the stated number is off from the nearest rounding but the claim stands. MISMATCH means the number, or the range the sentence attaches to it, is wrong.

| # | line | quoted fragment | claimed quantity | recomputed | source | verdict |
|---|---|---|---|---|---|---|
| 1 | 10 | "recover −1 to 1 % of it" | DICES-350 a=40 G_own/X_own, 3 families | Qwen2.5 1.30, Qwen3 −0.56, OLMo −0.03 → −1…1 | dd/dices_a40_r21, dices_a40_qwen3_r22, dices_a40_olmo_r22 | MATCH |
| 2 | 10 | "(upper bounds ≤ 12 %)" | same, CLT upper bounds | 11.37, 6.84, 7.16 | same | MATCH |
| 3 | 10 | "recovered at 15–33 %" | DICES dispersion plant γ=0.4, 5 draws | 15.3, 22.7, 27.8, 31.9, 32.6 (5/5 detected) | dd/dices_r22_plant0.4_s0–4 | MATCH |
| 4 | 10 | "MNLI and SNLI they recover 28–38 %" | ChaosNLI a=20 G_own/X_own | 28.34, 37.80 | dd/chaosnli_{mnli,snli}_r21 | MATCH |
| 5 | 12 | "shape of 69–83 % of training targets" | LoRA perm changed fraction | POPQUORN 68.7–71.7, SummEval 80.5–82.6 | results/lora/*/s0{,_seed2001,_seed2002}/f*/perm/meta.json (vecmatch excluded); RESULTS_TABLES T3b/T3c | MATCH |
| 6 | 48 | "recover −1 to 1 % of the own-shape" | as #1 | as #1 | as #1 | MATCH |
| 7 | 48 | "(upper bounds ≤ 12 %)" | as #2 | as #2 | as #2 | MATCH |
| 8 | 48 | "detected in 5 of 5 draws and recovered at 15–33 %" | as #3 | as #3 | as #3 | MATCH |
| 9 | 48 | "28 % [24, 33]" | MNLI a=20 | 28.34 [24.64, 32.04] | dd/chaosnli_mnli_r21 | MATCH (outward) |
| 10 | 48 | "38 % [33, 42]" | SNLI a=20 | 37.80 [33.95, 41.64] | dd/chaosnli_snli_r21 | MATCH (outward) |
| 11 | 52 | "shape of 69–83 % of LoRA training targets" | as #5 | as #5 | as #5 | MATCH |
| 12 | 104 | "It is 32–40 % of X on ChaosNLI at a=20" | X_cross/X at a=20 | rho_own: MNLI 40.4, **SNLI 31.4** → 31–40; decode_decomp: 40.2, 31.7 → 32–40 | results/rho_own/chaosnli_{mnli,snli}.json (the R19-1 / §3 artefact); dd/chaosnli_*_r21 | MISMATCH (minor, 1 pp; source-dependent) |
| 13 | 114 | "15–75 % of the three-rating histograms share their exact cell" | support_3 over the 7 three-rater panels | 15.1 (crupi_flu) … 74.6 (roy_ca) | results/support_three.json | MATCH |
| 14 | 146 | "recovers 10 % [4, 16]" | Dorn (all) G_own/X_own | 10.15 [4.44, 15.86] | dd/dorn_all_r21 | MATCH |
| 15 | 146 | "averages about 95 % of the value observed" | mean V_own of 5 location-only simulations / observed V_own (Dorn Java) | 95.7 % | dd/dorn_java_r21_plant0_s0–4 vs dd/dorn_java_r21 (clt.V_own); PROGRESS R21-7 | ROUNDING-ONLY ("about 96 %") |
| 16 | 146 | "Dorn's 10 % is therefore an upper bound" | as #14 | 10.15 | as #14 | MATCH |
| 17 | 147 | "−8 % [−23, 8] at 20 raters per half" | DICES-350 a=20 Qwen2.5 | −7.96 [−22.97, 7.05] | dd/dices_r21 | MATCH (outward; nearest rounding would give 7) |
| 18 | 147 | "1 % [−9, 12] at 40" | DICES-350 a=40 Qwen2.5 | 1.30 [−8.77, 11.37] | dd/dices_a40_r21 | MATCH (outward) |
| 19 | 149 | "28 % [24, 33] on MNLI" | as #9 | as #9 | as #9 | MATCH |
| 20 | 149 | "38 % [33, 42] on SNLI" | as #10 | as #10 | as #10 | MATCH |
| 21 | 149 | "ChaosNLI still gives 22 % [18, 26]" | MNLI a=4/half | 22.01 [18.65, 25.38] | dd/chaosnli_mnli_a4_r21 | MATCH |
| 22 | 149 | "and 28 % [24, 32]" | SNLI a=4/half | 28.39 [24.84, 31.93] | dd/chaosnli_snli_a4_r21 | MATCH |
| 23 | 151 | "the smallest margin is 24 % vs 16 %" | min NLI lower bound vs max ordinal upper bound | 24 vs 16 holds only for the a=20 Qwen2.5 intervals. The a=4/half NLI intervals reported one sentence earlier (#21) have lower bound **18.65 → 18** | dd/chaosnli_mnli_a4_r21, dd/dorn_all_r21 | MISMATCH (scope: across all reported NLI intervals the margin is 18 % vs 16 %) |
| 24 | 151 | "at most 30 % on the ordinal panels" | net ratio, ordinal, 20/half, upper bounds | max upper 29.37 (DICES-350 Qwen2.5); others 19.4–27.4 | dd/dices*_r21, dices990_r21, dorn_*_r21, dices_a40_r21 | MATCH |
| 25 | 151 | "at least 32 % on NLI" | net ratio, NLI, 20/half, lower bounds | min lower 32.77 (MNLI Qwen2.5) | dd/chaosnli_*_r21 (3 families) | MATCH |
| 26 | 156 | "recovered at 15–33 %" | as #3 | as #3 | as #3 | MATCH |
| 27 | 157 | "observed recovery is −1 to 1 %" | as #1 | as #1 | as #1 | MATCH |
| 28 | 157 | "upper bounds ≤ 12 %" | as #2 | as #2 | as #2 | MATCH |
| 29 | 161 | "(MNLI 30 % and 29 %)" | MNLI a=20, Qwen3 / OLMo | 30.22, 28.94 | dd/chaosnli_mnli_{qwen3,olmo}_r21 | MATCH |
| 30 | 167 | "histogram of 69–83 % of training items" | as #5 | as #5 | as #5 | MATCH |
| 31 | 223 | "−15 % on ChaosNLI" | relative KL change from a second rating on the same items (n×2 vs n×1, soft arm, largest n) | MNLI −14.9, **SNLI −12.0** | results/budget_heads/chaosnli_{mnli,snli}/runs.jsonl; PROGRESS 2026-10-26 05:52 (MNLI only) | MISMATCH (range: ChaosNLI is −12 to −15 %; −15 % is MNLI only) |
| 32 | 223 | "against −1 to −3 % for the ordinal heads" | same, RPS, ordinal | Qwen2.5 panels with >900 items: HS2 −0.8, EmoBank −1.3, SummEval −2.2, POPQUORN −2.8, DICES-990 −3.1. Not covered: BW −9.0, DICES-350 −12.5, Dorn −1.7; POPQUORN Qwen3/OLMo −4.4/−4.8 | results/budget_heads/*/runs.jsonl | ROUNDING-ONLY (−0.8 → "−1"; holds only for Qwen2.5 on the large ordinal panels) |
| 33 | 228 | "a second rating recovers 49 % of that gap" | (a1−full − (a2−full)) / (a1−full), POPQUORN prospective | 48.7 % | results/lora_budget_r20_pq/summary_popquorn_off8.json | MATCH |
| 34 | 231 | "62 % recovered by a second rating" | same, same-batch block | 62.3 % | results/lora_budget_v2/summary_popquorn_off8.json | MATCH |
| 35 | 247 | "with recovery of 1–22 %" | DICES polarisation γ=1.5, 5 draws | 1.3, 11.5, 16.5, 19.6, 22.4 (3/5 detected) | dd/dices_r22p_polar1.5_s0–4 | MATCH |
| 36 | 267 | "(32–40 % of X on ChaosNLI at a=20 …)" | as #12 | as #12 | as #12 | MISMATCH (minor; same as #12) |
| 37 | 271 | "recovers 38–56 % of the planted own-shape" | SummEval γ=0.6, 5 draws | 37.6, 48.7, 51.3, 51.4, 56.4 (5/5) | dd/summeval_coherence8_r22c_plant0.6_s0–4 | MATCH |
| 38 | 271 | "(POPQUORN … detected in 5 of 5, 6–38 %)" | POPQUORN γ=0.6, 5 draws | 6.4, 25.2, 32.3, 36.1, 38.2 (5/5 under the R22-4 CLT rule) | dd/popquorn_off8_r22c_plant0.6_s0–4 | MATCH |
| 39 | 271 | "recovered at 31–57 %" | SummEval γ=1.0, 5 draws | 30.8, 32.6, 46.8, 50.8, 57.4 (5/5; mean X 0.00225) | dd/summeval_coherence8_r22c_plant1_s0–4 | MATCH |
| 40 | 271 | "the 7–12 % recovery under G/X" | R19-2 G/X at γ=0.6, draw s0, POPQUORN / SummEval | 6.9, 11.8 | dd/{popquorn_off8,summeval_coherence8}_plant0.6_s0; ROUND19 R19-2; PROGRESS 1399/1477 | MATCH (see note: over the 5 draws, G/X at γ=0.6 is 1.6–6.9 on POPQUORN and 11.2–16.8 on SummEval) |
| 41 | 271 | "G/X upper bounds are 0.2 % and 0.4 %" | RFF G/X upper bound, SummEval / POPQUORN | 0.15, 0.36 | results/decoding_v2/{summeval_coherence8,popquorn_off8}_d64_E_last_rff.json | MATCH ("as for ridge": ridge uppers 0.23 / 0.03) |
| 42 | 271 | "negative mass on 3–82 % of items" | decode_validity `neg`, real panels | 3.4 (DICES) … 82.0 (CSC) | results/decode_validity/*.json; ROUND19 R19-8 | MATCH |
| 43 | 271 | "changed weak mode on ≤ 6 % of ordinal items" | decode_validity `mode`, ordinal | max 5.96 (SummEval relevance) | same | MATCH |
| 44 | 279 | "15–75 % of the three-rating histograms" | as #13 | as #13 | as #13 | MATCH |
| 45 | 283 | "0.9 % [−0.3, 2.1] on SummEval coherence" | SummEval coherence full panel, Qwen2.5 | 0.86 [−0.28, 2.00] | dd/summeval_coherence8_r21 | MATCH (outward) |
| 46 | 283 | "the ratio (0.5 % [−4.6, 5.6])" | SummEval non-duplicated items | 0.50 [−4.59, 5.58] | dd/summeval_coherence8_nodup_r22 | MATCH (outward) |
| 47 | 283 | "10 % [4, 16] on Dorn" | as #14 | as #14 | as #14 | MATCH |
| 48 | 283 | "−8 % [−23, 8] at 20 raters per half" | as #17 | as #17 | as #17 | MATCH (outward) |
| 49 | 283 | "1 % [−9, 12] at 40" | as #18 | as #18 | as #18 | MATCH |
| 50 | 284 | "28 % [24, 33] on MNLI" | as #9 | as #9 | as #9 | MATCH |
| 51 | 284 | "38 % [33, 42] on SNLI" | as #10 | as #10 | as #10 | MATCH |
| 52 | 286 | "(smallest margin: 24 % vs 16 %)" | as #23 (the a=4 NLI intervals follow two sentences later in the same paragraph) | 18 vs 16 if those are included | as #23 | MISMATCH (scope; same as #23) |
| 53 | 286 | "at most 30 % on the ordinal panels" | as #24 | as #24 | as #24 | MATCH |
| 54 | 286 | "at least 32 % on NLI" | as #25 | as #25 | as #25 | MATCH |
| 55 | 286 | "ChaosNLI gives 22 % [18, 26] (MNLI)" | as #21 | as #21 | as #21 | MATCH |
| 56 | 286 | "and 28 % [24, 32] (SNLI)" | as #22 | as #22 | as #22 | MATCH |
| 57 | 286 | "SummEval full panel 1.7 % and 0.7 %" | SummEval coherence, Qwen3 / OLMo | 1.71, 0.70 | dd/summeval_coherence8_{qwen3,olmo}_r21 | MATCH |
| 58 | 286 | "MNLI 30 % and 29 %" | as #29 | as #29 | as #29 | MATCH |
| 59 | 286 | "at most 16 % of it is decoded" | max upper bound where X_own is detectable | 15.86 (Dorn) | dd/dorn_all_r21 | MATCH |
| 60 | 286 | "recovered at 15–33 %" | as #3 | as #3 | as #3 | MATCH |
| 61 | 286 | "observed −1 to 1 % across the three feature families" | as #1 | as #1 | as #1 | MATCH |
| 62 | 286 | "(upper bounds ≤ 12 %; ROUND22 R22-5)" | as #2 | as #2 | as #2 | MATCH |
| 63 | 288 | "Dorn's 10 % is an upper bound" | as #14 | as #14 | as #14 | MATCH |
| 64 | 288 | "averages about 95 % of the value observed" | as #15 | 95.7 % | as #15 | ROUNDING-ONLY |
| 65 | 288 | "Its 10 % neither shows …" | as #14 | as #14 | as #14 | MATCH |
| 66 | 288 | "recovered at 38–56 %" | as #37 | as #37 | as #37 | MATCH |
| 67 | 288 | "with recovery of 6–38 %" | as #38 | as #38 | as #38 | MATCH |
| 68 | 298 | "for 69–83 % of training items" | as #5 | as #5 | as #5 | MATCH |
| 69 | 300 | "819 × 2 recovers 62 % of that gap" | as #34 | 62.3 | as #34 | MATCH |
| 70 | 300 | "a second rating recovers 49 % of that gap" | as #33 | 48.7 | as #33 | MATCH |
| 71 | 304 | "Replacing the shape of 69–83 %" | as #5 | as #5 | as #5 | MATCH |
| 72 | 304 | "about half of that gap (49–62 %)" | #33 and #34 | 48.7, 62.3 | as #33/#34 | MATCH |
| 73 | 308 | "donor-replacement support is 0 %" | support_2 on the three-rater panels | 0.0 on all 7 | results/support_three.json | MATCH |
| 74 | 308 | "15–75 % of items share their exact cell" | as #13 | as #13 | as #13 | MATCH |
| 75 | 320 | "(ChaosNLI −15 %, …)" | as #31 | MNLI −14.9, SNLI −12.0 | as #31 | MISMATCH (same as #31) |
| 76 | 320 | "ordinal heads −1 to −3 %" | as #32 | as #32 | as #32 | ROUNDING-ONLY (scope caveat as #32) |

Skipped as confidence levels: "95 %" on lines 12, 25 and 294 (and every "[95 %]" bracket), and "90 %" on line 294.

**Totals (76 percentage instances):** MATCH 66 · ROUNDING-ONLY 4 · MISMATCH 6 (three distinct issues, each appearing twice) · NO-SOURCE-FOUND 0.

## Mismatches

1. **Lines 104 and 267, "32–40 % of X on ChaosNLI at a=20".** The ρ artefact that §3 cites is `results/rho_own/chaosnli_snli.json` (ROUND19 R19-1). There, X_cross/X at a=20 is 31.4 % for SNLI and 40.4 % for MNLI, so the range is **31–40 %**. `dd/chaosnli_snli_r21.json` (a single split) gives 31.7 %, which does round to 32. Fix: write "31–40 %", or say that the range comes from the decode_decomp split.
2. **Lines 151 and 286, "smallest margin 24 % vs 16 %".** This holds only for the a=20, Qwen2.5 NLI intervals. Both passages also report the ChaosNLI 4-per-half intervals (MNLI 22 % [18, 26]), and "every NLI lower bound" then includes 18.65 % → 18. "Every NLI lower bound exceeds every ordinal upper bound" is still true. Fix: write "smallest margin 18 % vs 16 %", or qualify the sentence with "at 20 raters per half".
3. **Lines 223 and 320, "−15 % on ChaosNLI".** The relative KL gain from a second rating is −14.9 % on MNLI but **−12.0 %** on SNLI (`results/budget_heads/chaosnli_snli/runs.jsonl`). The −15 % figure was taken from the MNLI-only note in PROGRESS. Fix: write "−12 to −15 %", or "−15 % on ChaosNLI-MNLI".

## Rounding-only and coverage notes (not errors)

- **Lines 146 and 288, "about 95 %".** The recomputed value is 95.7 %, which would round to 96 %.
- **Lines 223 and 320, "−1 to −3 % for the ordinal heads".** The recomputed range is −0.8 to −3.1 %, and it covers only the Qwen2.5 heads on the large ordinal panels. Values outside it: BW −9.0 %, DICES-350 −12.5 % (these are the small panels whose direction already reverses), and POPQUORN on Qwen3 −4.4 % and OLMo −4.8 %. Stating "Qwen2.5" would make the claim exact.
- **Line 271, "7–12 % recovery under G/X".** This is the single R19-2 draw (s0). Over the five R22c draws at γ=0.6, G/X is 1.6–6.9 % on POPQUORN and 11.2–16.8 % on SummEval. The sentence still holds as historical context.
- **Lines 147 and 283, "−8 % [−23, 8]".** The upper bound is 7.05, which rounds to 8 only under the outward convention. That convention is applied consistently to every interval in the paper.

## Related non-percentage observations

- **Line 308, Dorn "0.10 (upper bound 0.18)".** Every other mention of Dorn, and `dd/dorn_all_r21.json`, gives an upper bound of 0.1586 (→ 16 %). No current artefact gives 0.18; it looks like a stale value.
- **Lines 104 and 267, "most of X on the ordinal dense panels at a ≤ 8".** In rho_own, X_cross/X on DICES-350 is 49 % at a=8, and at a=5 X is near zero (ratio −2059 %). "Most" therefore fails on DICES-350 at a=8.
- **Lines 271 and 288, POPQUORN γ=0.6 "detected in 5 of 5".** ROUND21 and PROGRESS 1555 say 4 of 5. Under the R22-4 CLT rule (`*_r22c_*`), all five lower bounds of G_own are above 0, so 5 of 5 is the current result.
