# ROUND22 protocol — SummEval crowd-annotation integrity

## Finding (2026-11-06 21:33, from R20-7 diagnostics; descriptive)
These figures are for the released file data/summeval/model_annotations.aligned.paired.scored.jsonl, restricted to the 1,600 items with 3 expert and 5 turker annotations.
- **Duplicated turker annotations.** In 807 items (50.4 %), all five turker annotation dicts are identical on all four dimensions. The rate is 0 % for systems M17, M20, M22 and M23 and 62–79 % for the other twelve.
- **Expert–crowd agreement.** The expert mean and the crowd mean correlate at r = 0.04 (coherence), 0.07 (relevance), 0.01 (consistency) and 0.05 (fluency) at the summary level. At the document level r is 0.26 for coherence; at the system level it is −0.03. On non-duplicated items only, r = 0.09.
- **Agreement within groups.** Experts correlate with each other at 0.61–0.72 and crowd positions with each other at 0.46–0.53. The latter is inflated by the duplicates.
- **R20-7 (partial).** A judge trained on the five crowd ratings predicts an almost constant mean (SD 0.03) and is +0.012 to +0.024 RPS worse than the full-data judge against each held-out expert.

**Implication.** On SummEval, the "crowd" columns carry almost no expert-aligned signal, and in half the items they are a single value repeated five times.
- Every SummEval analysis mixes three expert columns with five such columns: split-half reliability, X_own, decoding, the budget blocks and the target-construction contrasts.
- In the budget blocks, "the full data" is two expert ratings diluted by five crowd ratings. The evaluator dependence (R21-6), the second-rating benefit and the 960 × 2 ≤ full result are all consistent with this dilution.
- Whether the duplication exists in the original release, or was introduced by the "aligned/paired/scored" processing we inherited, is **unverified**. This must be checked against the upstream file before any text attributes it to SummEval.

## R22-1 (specified 21:33, before running): sensitivity of the SummEval decoding headline
- **New panels.**
  - summeval_coherence8_nodup and summeval_relevance8_nodup: the 793 items without duplicated turker annotations. Features are sliced from the existing files; the item ids are the original row indices, checked by the alignment assert.
  - Note the composition shift: these items include all 400 items from M17/M20/M22/M23.
- **Runs.** decode_decomp.py --a 4 --R 10 --B 0 --tag _r22 on both panels; CLT intervals as in R21.
- **Reading.** The headline "SummEval 1–2 %, upper bound ≤ 2.8 %" stands if the nodup upper bound for G_own/X_own is < 24 % (the smallest NLI lower bound), so that the ordinal–NLI contrast holds. Otherwise SummEval is removed from the contrast. Either way, the nodup values are reported next to the full-panel values.
- **Not addressed here** (follow-ups, to be specified separately):
  - the LoRA budget and target-construction results on SummEval, which may need an experts-only or nodup re-run;
  - the reliability card for SummEval.

### Addendum (21:34, literature check)
- **Documented upstream.** Fabbri et al. (SummEval, TACL 2021; arXiv 2007.12626) report that the averaged expert and crowd scores have a Pearson correlation close to 0, and that crowd scores were similar across dimensions. The near-zero expert–crowd agreement is therefore a documented property of SummEval and must be cited.
- **Not documented.** We found no report of the identical-annotation pattern (five identical turker dicts in 50 % of items). It stays unverified against the upstream file.
- **Draft action (once R22-1 reports).**
  - §2.1 and §5 must state that SummEval's crowd columns are essentially uncorrelated with its experts (citing Fabbri et al.).
  - The budget results on SummEval must be described as diluting two expert ratings with five crowd ratings, not as "full data vs fewer ratings of one population".

### R22-1 results (2026-11-06 21:36; results/decode_decomp/summeval_*8_nodup_r22.json; 0 tracebacks)
| panel (793 items) | X_own [95 %] | G_own/X_own | G_own_net/X_own |
|---|---|---|---|
| coherence nodup | −0.00013 [−0.00030, +0.00003] | 0.005 [−0.046, 0.056] | −0.018 [−0.064, 0.029] |
| relevance nodup | −0.00003 [−0.00016, +0.00010] | 0.32 [−1.02, 1.67] | −0.03 [−0.20, 0.15] |
- **Frozen reading.** Coherence: the upper bound 5.6 % is < 24 %, so it stays in the contrast. Relevance: the upper bound 167 % is ≥ 24 %, so it is **removed from the contrast**.
- **The substantive result (beyond the frozen reading).** Without the duplicated items, SummEval shows **no detectable own-shape reproducibility**: X_own's point estimates are negative and their intervals cover 0.
  - The full-panel X_own (coherence 0.00038) comes from items whose five crowd annotations are identical. Those make the turker part of the two halves agree trivially.
  - With X_own ≈ 0, the ratios are not interpretable, even where the frozen rule passes.
- **Consequences for the paper:**
  1. SummEval stops being the example of "reproducible but not decodable". It joins POPQUORN and DICES-990: no detectable own-shape at a = 4. The clean ordinal example of a detectable but undecoded own-shape is DICES-350 at a = 40: X_own > 0, recovery 1 % [−9, 12].
  2. SummEval's plant calibration (R20-2, R21) was matched to an X_own inflated by duplicates. It stays reported as a calibration at that magnitude, but it no longer establishes informativeness for SummEval's real shape.
  3. SummEval's split-half reliability card and every SummEval budget or target result must carry the duplication and expert–crowd facts. A full-panel versus nodup re-computation of ρ and ρ_own is to be specified next.
  4. The ordinal–NLI contrast survives in direction, but its ordinal side is now "not reproducible (SummEval, POPQUORN, DICES-990) or reproducible yet not decoded (DICES-350; Dorn's signal is location-sized)".

## R22-2 (specified 21:36, before running): the SummEval reliability card on non-duplicated items
- **Runs.** rho_own.py and rho_exact.py (R = 10, B = 200, defaults) on summeval_coherence8_nodup and summeval_relevance8_nodup.
- **Reported.** ρ, ρ_own and A1^x next to the full-panel values, at every a computed.
- **Descriptive, no gate.** The card shows both versions. The text uses nodup values for any claim about reproducibility of SummEval's shape.
- **Also (descriptive).** The expert-only split-half on SummEval is impossible (3 raters, so b = 1 or 2 and X_own ≡ 0 or unmeasurable). This is stated as such.

### R22-2 results (2026-11-06 21:38; results/rho_exact/summeval_*8_nodup.json; a = 7, leave-one-out)
| panel | full: ρ [95 %] | nodup: ρ [95 %] | full A1^x | nodup A1^x |
|---|---|---|---|---|
| coherence | 0.35 [0.24, 0.48] | **0.10 [−0.13, 0.23]** | +0.0016 | +0.0032 |
| relevance | 0.40 [0.30, 0.54] | **0.05 [−0.19, 0.25]** | +0.0008 | +0.0031 |
- On non-duplicated items, the forecasting reliability of SummEval's shape is indistinguishable from 0. A1^x > 0 with an interval excluding 0 means the raw histogram forecasts a held-out rating worse than its exact mode and mean, now clearly so.
- The duplicates inflated ρ by about 0.25–0.35.
- rho_own.py is for dense panels only (assert m > 12). SummEval's X_own comes from R22-1, so the two tracebacks are expected and are not bugs.
- **Card.** SummEval is reported with both versions. Claims use nodup. The draft range "0.04–0.41 on eight panels" is unchanged in its endpoints (0.04 is not SummEval; the 0.41 endpoint is to be re-checked against the table in R22-T).

### Provenance check (21:39)
- The file name model_annotations.aligned.paired.scored.jsonl matches the official SummEval release naming: the aligned, paired file, plus metric scores (see the 04/19/2020 update in data/summeval/README.md). It was imported unchanged on 2026-10-25 (commit 73d6323).
- Upstream verification failed from this server: the Google Drive link returns 404 and the HF datasets-server timed out. **Still unverified.**
- Until verified, the text says "in the released file as distributed with the SummEval repository's annotation link". It does not say the duplication is a defect of the original crowd collection.

## R22-T (specified 23:31, before editing): SummEval non-duplicated rows in Table 1
- Table 1 (make_tables_v2.py) gains the rows "SummEval coh./rel. (non-dup.)", from results/rho_exact/summeval_*8_nodup.json (R22-2). The full-panel rows stay. Support is "--", because no donor-replacement run exists for nodup.
- In §1 (i), the range "0.04–0.41 … (intervals include 0 on four)" is re-checked. The minimum is CSC 0.038 / POPQUORN pol. 0.037 and the maximum is EmoBank 0.412. The nodup values (0.10, 0.05) fall inside the range, so the endpoints do not change. One parenthetical is added: on SummEval's non-duplicated items, ρ is 0.10 / 0.05 and both intervals include 0. The count "four" refers to the eight released panels and stays.
- No new computation.

### Provenance check, second attempt (23:33)
- GitHub Yale-LILY/SummEval issues: no issue mentions duplicated or identical crowd annotations (searched "duplicate", "identical", "turker", "crowd").
- Issue #41 ("Identifying individual annotators", closed): the first author answered that, *within a summary*, position i is the same person across the four dimensions. They did not say whether position i is the same person across summaries. This supports the treatment of the crowd columns as positions (§2.1 Population). It does not explain the duplication: five different workers giving identical four-dimension annotations on 50 % of the items would be a strong coincidence.
- HF mirrors: davidanugraha/SummEval (1,700 rows) and mteb/summeval carry only expert scores, not the turker lists, so they cannot verify the duplication. The remaining parquet mirrors were not read, because no parquet engine is installed in the venv.
- Status: still **unverified upstream**. The draft keeps "undocumented". The nodup sensitivity (R22-1/R22-2) is the remedy in either case.

## R22-T2 (specified 23:33, before editing): carry the ROUND22 reading into §1 (iii)/(v) and §3
- §1 (v): add one sentence after the SummEval LoRA budget result. SummEval's crowd ratings are nearly uncorrelated with the held-out experts, so these contrasts measure dilution of the expert ratings (R20-7, §5). This matches the abstract and §5, which were already changed.
- §3, donor-replacement audit: add one sentence. On SummEval and POPQUORN no own-shape is detectable (R22-1, R21), so the shape-replacement null is the expected outcome there and not independent evidence that judges ignore a learnable shape. The audit's discriminating case is ChaosNLI, where the same intervention costs Brier. Text only; no new numbers.

## R22-3 (specified 2026-11-07 00:36, before running): X_own-matched plant on DICES-350 at a = 40 (round-22 review, change 3)
DICES-350 at a = 40 is the only ordinal panel whose own-shape is detectable (item-cluster CLT) and not location-sized by construction. Its G_own/X_own 1 % [−9, 12] has no power calibration.
- **Runs.** decode_decomp.py on dices, a = 40, R = 10, B = 0, tag _r22. Plants γ ∈ {0, 0.1, 0.2, 0.3, 0.4}, draws s0–s4, on the fitted dices M2 model (as R21-7). One sequential CPU Slurm job.
- **Reference plant (as R21-7).** The smallest γ whose mean planted X_own ≥ the observed 4.9·10⁻⁵. If no γ in the grid reaches it, add γ 0.6 and 0.8 and label them as an extension.
- **Reading:**
  - 4–5 of 5 detected at the reference γ: DICES-350's 1 % is informative at its own magnitude.
  - Fewer than 4: it is not, and is reported as such.
- **Location-only baseline (descriptive, as R21-7).** Mean X_own and V_own over the γ0 draws, as fractions of the observed values (X_own 4.9·10⁻⁵, V_own 4.9·10⁻⁶).

## R22-T3 (specified 2026-11-07 00:36, before editing): carry ROUND22 through the draft (round-22 review)
Text and tables only. All numbers come from existing result files.
1. **§1 (ii) list (l. 18).** Apply R22-1's frozen reading: SummEval relevance leaves the ordinal list. Coherence stays, with its no-dup ratio 0.5 % [−4.6, 5.6] beside it and the note that the no-dup X_own is not detectable.
2. **l. 21.** Relabel the a = 4 ChaosNLI result as a check that the NLI fractions do not depend on a = 20. Say that no ordinal partner at a = 4 has a detectable own-shape. The net-fraction bound "at least 32 % on NLI" becomes "at a = 20".
3. **(ii) heading and abstract.** Reframe: no ordinal panel shows a robustly reproducible own-shape. It is undetectable on most; on DICES-350 it is detectable only within the observed rater pool; on Dorn it is location-sized. Where detectable, ≤ 16 % is decoded.
4. **l. 23/49.** "So the SummEval null is informative" becomes conditional on the full-panel magnitude, which ROUND22 attributes to duplication. The corrected-X_own sentence for SummEval is marked as not applicable to duplicated annotations.
5. **l. 61, l. 63, l. 65.** Small-panel count "half" becomes "four of eight (two on SummEval's non-duplicated items)". The SummEval residual sentence is replaced. λ̂ is attributed to the duplicates.
6. **Contribution (4) and guidance (l. 25, l. 75).** Remove the SummEval budget contrasts as budget evidence. Fix the frozen-head threshold to match Table 5: SummEval prefers 480×2, POPQUORN has 819 items, and HelpSteer2/OLMo-2 is the exception.
7. **§5 (l. 73).** "+0.020 on every fold" becomes "+0.014 to +0.025". Disclose that the R20-7 arms are compared across batches: the effects are 0.01–0.04, against rerun variation ≤ 0.0012. l. 83 is fixed accordingly.
8. **§2.1 population (l. 45), §7 (l. 83).** Add the duplication / r ≈ 0.04 / unverified-provenance limitation. Replace "SummEval's small unexplained residual".
9. **Abstract.** "Prospective LoRA blocks on POPQUORN" becomes "a prospective LoRA block". Header line 3 is updated.
10. **Deferred to R22-T4 (next step).** Table 2 rebuilt on CLT G_own/X_own with no-dup rows. Table 6 rebuilt with the prospective blocks. Plant detection recomputed with CLT, if the plant JSONs store it. Duplication notes in the Table 1/2 captions.

### R22-T3 applied (2026-11-07 00:38)
All 22 replacements are applied, covering items 1–9; item 10 is deferred to R22-T4. check_consistency: 11/11 OK, 0 unmatched. The abstract is 379 words.
Correction found while editing: §5 said experts2 was "0.040 better than full" on expert 1. compare.md gives −0.0415 against a7 (−0.0395 against a2). Changed to 0.042.
Not changed: the motivating example (l. 10, SummEval coherence). It is illustrative, not evidence. It will be replaced in the next draft pass.

## R22-T4 (specified 2026-11-07 00:38, before editing): tables
- **New table, tab_own.tex.** The own-shape decoding table, built by make_tables_v2.py from results/decode_decomp/*_r21.json and *_r22.json (plant files excluded). Each row has: panel, a/b, feature family, X_own [CLT 95 %], G_own/X_own [CLT 95 %], and the net fraction (G_own − G_own,perm)/X_own [CLT 95 %].
  - A ratio is shown only when X_own's interval excludes 0; otherwise the row reads "X_own n.s.". This is the same forbidden-statement rule as Table 2.
  - SummEval rows are labelled "full panel" and "non-dup."
  - This table, not Table 2, carries the §1 (ii) headline.
- **Table 2 caption.** Add: the percentile intervals are the round-20 bootstrap, and the cross-term-inclusive G/X is kept for comparison only. The SummEval rows include the duplicated annotations.
- **Table 1 caption.** Add a sentence on the duplicated crowd annotations, pointing to the non-dup. rows.
- **Table 6 (LoRA).** Rebuilt in a separate step (R22-T5), so that it leads with the prospective blocks.

## R22-T5 (specified 2026-11-07 00:39, before editing): LoRA budget table leads with the prospective blocks
tab_budget.tex (Table 6 in the draft) is rebuilt in this order:
1. POPQUORN prospective (R20-4, lora_budget_r20_pq), the clean budget case.
2. SummEval prospective, labelled "expert dilution, §5": Qwen2.5 R19-9 (lora_budget_r19), OLMo-2 R20-3 (lora_budget_r20_olmo), and the single-batch reruns R20-5b/c (lora_budget_r20_rerun) and R20-6 (lora_budget_r206_olmo).
3. The earlier shared-assignment blocks (lora_budget_v2, lora_budget_olmo), labelled "shared assignment".

No numbers change. The rows are read from the existing summary JSONs. The §5 paragraph order (N14) is left for the next draft pass.

### R22-3 results (2026-11-07 00:50; 25 runs, 0 tracebacks; results/decode_decomp/dices_r22_plant*_s*.json)
| γ | mean X_own | mean V_own | detected (CLT lower bound of G_own > 0) | G_own/X_own per draw |
|---|---|---|---|---|
| 0 | −1.3e−5 | 4.7e−7 | 0/5 | 0.03, −0.56, 0.22, 0.10, 0.23 |
| 0.1 | −0.7e−5 | 5.7e−7 | 0/5 | 0.09, −0.28, −0.71, −0.04, 0.48 |
| 0.2 | 0.5e−5 | 2.7e−6 | 0/5 | 0.05, 0.04, 1.19, −0.07, −0.02 |
| 0.3 | 3.0e−5 | 8.8e−6 | 2/5 | 0.47, 0.08, 0.26, 0.19, 0.11 |
| **0.4** | **5.5e−5** | 2.2e−5 | **5/5** | 0.32, 0.28, 0.23, 0.33, 0.15 |

- The reference γ is **0.4**: it is the smallest γ whose mean planted X_own (5.5e−5) is at least the observed 4.9e−5.
- **Frozen reading: 5 of 5 detected, so DICES-350's G_own/X_own of 1 % [−9, 12] is informative at its own magnitude.** A planted text-predictable shape of the observed size is recovered at 15–33 %.
- Location-only baseline (γ 0), descriptive:
  - X_own is −1.3e−5, i.e. −27 % of the observed value. Location and thresholds alone do *not* produce DICES-350's own-shape, unlike Dorn (R21-7: about 95 % of V_own).
  - V_own is 4.7e−7, about 10 % of the observed 4.9e−6.
- Implication: DICES-350 at 40 raters is the one ordinal panel where a reproducible own-shape beyond location is detected (within the observed rater pool), power-calibrated, and *not* decoded. It now serves as the clean ordinal partner of the NLI contrast, at a = 40.

## R22-4 (specified 2026-11-07 01:31, before running): plant detections recounted with CLT intervals (review N1 / round-22 MEDIUM)
The SummEval and POPQUORN plant counts in the draft (R20-2/R20-2a) use the percentile bootstrap of G_own, which R21-1 abandoned for the headline. The JSONs of those runs (B = 200) store no CLT.
- **Runs.** decode_decomp.py, a = 4, R = 10, B = 0 (CLT only), tag _r22c, same plant seeds s0–s4.
  - summeval_coherence8 at γ ∈ {0.3, 0.6, 0.8, 1.0};
  - popquorn_off8 at γ ∈ {0.3, 0.6}.
  - γ 0 is already available with CLT (_r21, 0/5 detected on both).
  - Two sequential CPU jobs.
- **Reported.** Detections per γ under the CLT rule (lower bound of G_own > 0) next to the percentile counts. The point estimates (X_own, G_own/X_own) must match the earlier runs exactly; this is the pipeline check.
- **Frozen reading.** The CLT counts replace the percentile counts in the draft, whichever way they go. The reference-γ rule is unchanged (X_own scale; SummEval's full-panel reference is moot under ROUND22 and is reported for completeness).

## R22-T6 (specified 2026-11-07 01:32, before editing): §5 order (round-21 N14)
The sentences of the §5 LoRA-budget paragraph are reordered, with no new numbers:
1. POPQUORN, the clean budget case: the same-batch block, the prospective block R20-4, and "two ratings still cost".
2. The SummEval reading note.
3. The SummEval blocks, as before.
4. The cross-block summary, OLMo shared-assignment, evaluator dependence, and the batch and literature notes.

Only two wordings change: "re-run in the same way" becomes an explicit description, and "below" in the reading note points to the SummEval blocks that now follow it.

### R22-4 results (2026-11-07 02:31; 30 runs, 0 tracebacks)
Pipeline check: the point estimates (X, X_own, G, G_own) match the earlier B = 200 runs to ≤ 3·10⁻¹⁹.

| panel | γ | mean X_own | detected, percentile (old) | detected, CLT (new) | G_own/X_own range |
|---|---|---|---|---|---|
| SummEval coh. | 0 | −0.00009 | 0/5 | 0/5 (_r21) | — |
| SummEval coh. | 0.3 | 0.00017 | 4/5 | **5/5** | 0.16–0.55 |
| SummEval coh. | 0.6 | 0.00041 | 5/5 | 5/5 | 0.38–0.56 |
| SummEval coh. | 0.8 | 0.00049 | 5/5 | 5/5 | 0.33–0.50 |
| SummEval coh. | 1.0 | 0.00046 | 5/5 | 5/5 | 0.31–0.57 |
| POPQUORN off. | 0 | ≈0 | 0/5 | 0/5 (_r21) | — |
| POPQUORN off. | 0.3 | 0.00009 | 0/5 | **2/5** | −0.02–0.34 |
| POPQUORN off. | 0.6 | 0.00031 | 4/5 | **5/5** | 0.06–0.38 |

- CLT detects slightly more often than the percentile bootstrap. That is consistent with R21-1, where the percentile intervals were off-centre.
- Frozen readings: SummEval stays "informative at the full-panel magnitude", which is moot under ROUND22. The POPQUORN reference plant (γ 0.3) is detected in 2 of 5, which is below 4, so the POPQUORN null **stays uninformative**. No reading changes.
- Draft: the counts are replaced with the CLT counts (4→5, 4→5, 0→2 on POPQUORN γ 0.3).

## R22-5 (specified 2026-11-07 02:31, before running): DICES-350 at a = 40 on the other two feature families
DICES-350 at a = 40 is now the power-calibrated ordinal case (R22-3), but only Qwen2.5 features were decoded there; at a = 20, all three families were.
- **Runs.** decode_decomp.py, dices, a = 40, R = 10, B = 0, with --feat_model Qwen3-8B (tag _a40_qwen3_r22) and --feat_model OLMo-2-1124-7B-Instruct (tag _a40_olmo_r22). One CPU job.
- **Reported.** G_own/X_own and the net fraction, each with CLT 95 % intervals. X_own is the same across families, because it is learner-free.
- **Reading (descriptive).** The draft's "three LLM families recover 1 %" is kept only if both upper bounds stay below the plant recovery range (15–33 %). If either upper bound reaches 15 %, the abstract names the family-specific values instead.

### R22-5 results (2026-11-07 02:33; 2 runs, 0 tracebacks)
X_own is 4.90e−5 on all three families (learner-free, identical as expected).

| features | G_own/X_own [CLT 95 %] | net [CLT 95 %] |
|---|---|---|
| Qwen2.5 (R21) | +1.3 % [−8.8, +11.4] | +15.0 % [+2.6, +27.4] |
| Qwen3-8B | −0.6 % [−8.0, +6.8] | +9.5 % [−0.3, +19.3] |
| OLMo-2-7B | −0.0 % [−7.2, +7.2] | +6.8 % [−1.9, +15.6] |

- Reading: all three upper bounds (≤ 11.4 %) are below the plant recovery range of 15–33 %. The abstract keeps the three-family statement, with the range −1 to 1 % and upper bounds ≤ 12 % (rounded outward).
