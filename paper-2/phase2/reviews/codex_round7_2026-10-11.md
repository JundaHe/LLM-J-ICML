# Verdict

**The SummEval result licenses a strong location-versus-residual-allocation statement, but not a formally prespecified equivalence claim.** The overall package is submission-worthy as a carefully scoped audit once chain7, DeepSeek, and the v4 target checks finish. Its largest remaining scientific weakness is that the cleanest SummEval LoRA result still conditions on one optimizer seed, one item split, and one permutation draw.

There is also an immediate implementation discrepancy: the current `targets.py` still does **not** require `res.success`.

## 1. SummEval and equivalence

The abstract may now say:

> On SummEval, disrupting the item-specific location link increased native-output RPS, whereas randomizing residual histogram allocation while preserving mode and mean produced a near-zero contrast.

A more numerical Results statement is:

> Mode-and-mean-preserving link randomization changed native-output RPS by −0.0006 (document-bootstrap CI [−0.0012, +0.0001]), while disrupting item-specific location increased RPS by +0.0112 [+0.0083, +0.0143]. The location contrast was positive under the raw, common-map, and arm-specific estimands.

Do **not** write simply “the two arms were equivalent at \(\epsilon=.002\).” Use:

> The interval was contained within a post hoc practical-equivalence band of ±.002, but not ±.001.

Two reasons:

1. The margin was outcome-informed. More seriously, the progress chronology indicates that \(\epsilon=.002\) was frozen after SummEval folds 0–1 had already been inspected, not solely after an independent commit result. It is therefore a sensitivity threshold, not a prespecified SummEval margin.
2. The exact endpoints in T3b come from `2.5/97.5` bootstrap percentiles in [analysis_lora_v3.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_lora_v3.py:45), so they are currently a **95% CI**, not a 90% CI. A 95% interval inside ±.002 is numerically stronger, but it must be labelled correctly.

The \(.002\) band is substantively plausible—it is about 11% of the raw hard–Chen gain and 18% of the location-disruption effect—but that justification should accompany a `.001/.002/.003` sensitivity display. Future replication can treat `.002` as prospectively frozen.

## 2. Chen–mean2 reversal

This is primarily a documented **estimand dependence**, especially because `mean2` is now only a projection control and this SummEval version is the old unconstrained tilt. Report all three estimates and make no “better target” claim.

A direct paired CI is worthwhile only if the prose says calibration *reverses* or *changes* the comparison. The relevant statistic is not merely common-minus-raw; it is chiefly

\[
(\text{chen}-\text{mean2})_{\text{arm}}
-
(\text{chen}-\text{mean2})_{\text{raw}}
\approx -0.0046.
\]

I would report paired CIs for arm-minus-raw, common-minus-raw, and arm-minus-common in an appendix. Resample calibration documents and test documents jointly and refit every calibration map inside each replicate.

The current `analysis_lora_v3.py` holds fitted calibration maps fixed during the bootstrap, so it does not yet implement that inference. Until the direct CI exists, say:

> Arm-specific calibration changed the estimated ordering.

Do not say it “proved Chen better” or “caused the reversal.”

## 3. Licensed BW statement

Use:

> In the 60-training-item × 97-training-rater Buse–Weimer regime, restricted or regularized targets yielded lower held-out RPS than empirical-histogram supervision, whereas the histogram-trained model best ranked held-out disagreement conditional on location. Strong shrinkage improved RPS by 0.0024 and residual-only shrinkage by 0.0007, consistent with a finite-item regularization or bias–variance trade-off, but not identifying overfitting or annotation noise.

The important interpretation is that 97 raters estimate each item’s distribution well, but they do not solve the problem of learning a text-to-five-bin mapping from only 60 training items. The histogram can contain useful disagreement-ranking information while being a worse target for average proper-score generalization.

Keep these BW numbers provisional until v4 regeneration establishes that the v2 fallback was never used.

## 4. DICES SORDm

**Keep SORDm.** Excluding a prespecified comparator only on the dataset where it fails would look selective.

But do not call this “a failure of parametric targets on short scales.” The licensed statement is narrower:

> Mean-centered SORD degraded RPS by 0.0425 on DICES. Its unimodal discrete-Gaussian shape is badly mismatched to this three-level, near-binary endpoint-mass distribution.

A flexible parametric target need not fail on three levels; this specific Gaussian family does. If table space is tight, move all parametric comparators to the appendix by a dataset-independent rule rather than removing only the DICES result.

## 5. Is the evidence base enough?

**Yes, enough to submit a scoped audit paper; not enough to advertise the LoRA result as fully replicated or confirmatory.** The breadth is now respectable: multiple domains, ordinal and nominal geometries, heads and LoRA, held-out raters, direct disagreement metrics, constrained interventions, and positive controls.

The single most damaging remaining scientific gap is:

> The headline SummEval LoRA result has no orthogonal optimizer/permutation replication and no independent item split.

The three expert folds are evaluator coverage, not three training replications. Chain7 addresses optimizer/permutation randomness on commit, and DeepSeek addresses family dependence on Why, but neither directly replicates the clean SummEval result.

If one additional GPU block is possible, the highest-value block is SummEval `chen/perm/perm_mode` under two additional paired optimizer/permutation seeds; a new document split would strengthen it further. Otherwise scope the abstract explicitly to “one Qwen training realization and document split” and retain the conditional language.

## 6. Wording and implementation vetoes

### Immediate code veto

[targets.py](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/targets.py:82) accepts `res.x` whenever it is feasible, without checking `res.success`. Thus Hour 14b’s statement that optimizer success is required is currently false. Add the equivalent of:

```python
if not res.success:
    continue
```

before considering `res.x`. Also, the bundled self-test catches failures and continues, so it should assert the requested case count and `STATUS["failed"] == 0`. Until then, “converged KL projection” and “all fixed” are not licensed.

### PROGRESS.md Hour 15

Veto or revise:

- “**Certified heads, BW … v2 targets code — fallback possible**”: internally contradictory. Delete “Certified.”
- “The mode+mean-binned permutation is **inert**”: replace with “produced a near-zero contrast” or the post hoc-band wording above.
- “The nominal half is now **confirmed**”: use “the constraint-corrected rerun reproduced the nominal result.”
- “SORDm is **catastrophic … a Gaussian cannot represent a 3-point near-binary histogram**”: use the narrower misspecification wording above.
- “The two anchor results are complete and certified”: use “completed under the current design; the nominal intervention is constraint-certified.” SummEval is not replication-certified.
- Replace the literal `q = …` placeholder with the actual vector or remove it.

### RESULTS_TABLES.md T3b

Revise the table to:

- label the displayed intervals as 95%, unless recalculated;
- state conditioning on one optimizer seed, one item split, one permutation draw, and the three observed experts;
- state that the arm-specific intervals currently condition on fixed fitted calibration maps;
- label the `.002` band post hoc and show `.001/.002/.003` sensitivity;
- remove “Earlier partial numbers” and fold-0 archaeology from the consolidated results table;
- either add a common-map CI or make explicit that it is a point estimate only.

### RESULTS_TABLES.md T5

Replace the legacy table with the exact capped results instead of saying they agree “within ±.001.” In particular, the header reports capped `zc` fidelity ending at `.51`, while the table ends at `.49`. Also specify what `±` denotes across the nine configurations.

Use “constraint-certified `zc/pzc` targets” rather than allowing “CERTIFIED” to modify the entire empirical conclusion.