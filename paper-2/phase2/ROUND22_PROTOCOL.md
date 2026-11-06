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
