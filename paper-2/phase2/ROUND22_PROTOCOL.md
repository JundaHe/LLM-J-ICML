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
