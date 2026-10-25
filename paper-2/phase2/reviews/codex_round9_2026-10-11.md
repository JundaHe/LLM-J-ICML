## A. Dose-audit handling

The proposed SummEval remedy is adequate: rerun `perm` and `perm_mode` for seeds 2000–2002 and all three folds with histogram-class matching; unaffected arms need not be retrained. The seed-2000 vector-matched runs may appear only as an implementation-audit appendix row—not as coequal evidence or a genuine dose-response study.

Before calling the audit complete:

- Report, per configuration and arm:

  1. fraction in heterogeneous matching cells;
  2. maximum/realized fraction changed;
  3. mean TV among changed items;
  4. mean TV over all training items, counting unchanged items as zero;
  5. final post-projection TV for `pmmx`/`pzc`;
  6. zero-TV count and realized mean-shift range.

  Conditional TV alone hides low exposure: commit Why has \(0.226\times0.50\approx0.113\) mean TV over all training items.

- Veto the current assertion that all four scripts have TV certificates. [`probe_nominal.py`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/probe_nominal.py:86) records only matched fraction and constraints; [`gxr_check.py`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/gxr_check.py:63) records no dose certificate; and [`probe_mean2.py`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/probe_mean2.py:110) does not record post-projection TV for `pmmx`.

- Rerun the T4 positive controls. They come from `probe_mean.py`, which still uses vector-class matching. Dense panels may make the numerical difference small, but an assay-sensitivity result cannot rest on known-buggy intervention code.

- Audit Stage A separately. [`stage_a_heads.py`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/stage_a_heads.py:76) intentionally matches rater-indexed vectors, which can be legitimate for a who-rated-what intervention, but its reported histogram TV then mixes histogram changes with pure rater-allocation changes. Report vector/Hamming and histogram doses separately or relabel that intervention. The margin-preserving 2×2 interaction scramble itself is not implicated.

For the paper, use only `_v6` heads as scientific evidence. `_v3`–`_v5` may appear in one clearly labeled audit table demonstrating stability after the fix. Do not retain the legacy T2 table or old panel rows merely with a warning; that forces reviewers to adjudicate invalid and corrected estimates. T2b presently mixes an old commit What block with corrected commit Why and must be rebuilt.

## B. Intrinsic dose

Yes. A 23–34% realized intervention materially weakens a commit-specific “inertness” claim. It does not invalidate the near-zero estimate, but it changes its interpretation from “the learner ignores residual shape” to “this low-dose intervention did not detect an average effect.”

Also, changed fraction is not the same as the proportion whose histogram is uniquely determined. For commit Why heads, a direct audit gives approximately 41% of items in heterogeneous observed \((\text{mode},\text{mean})\) cells, but the maximum bijection changes only 22.6% because of histogram-class imbalance. Therefore veto:

> Mode and mean pin down the histogram for 77% of items.

Use:

> With four training ratings on commit Why, approximately 41% of training items belonged to observed mode-and-mean cells containing multiple histogram classes, while the maximum-cardinality donor bijection changed 23% of items. The corresponding LoRA intervention changed 29–34%. These comparisons are therefore low-support, low-dose tests of residual allocation and are not interpreted as equivalence or as panel-wide evidence that residual shape is unused.

Then:

> Our principal evidence that mode-and-mean-preserving replacement causes little average degradation comes from corrected SummEval, where 81–83% of training targets change, and from the corrected dense-panel analyses. The commit results are consistency checks and evidence about the limited residual variation available at small panel sizes.

Do not say the audit is “only informative on dense panels”: commit remains informative about data geometry and the realized low-dose intervention. But yes, demote the commit null and promote corrected SummEval and dense-panel results. Do so only after the `_v6` dense-panel reruns finish.

Report commit What separately; its corrected heads dose appears still lower than commit Why—roughly 15–18% in current configurations—so “23–34% on the commit panels” is too coarse.

## C. G×R

“N​ecessary-condition account” is not acceptable.

The analysis was prespecified as a held-out test on BW, DICES, HelpSteer2, and Scalabrino, as recorded in [`PAPER_OUTLINE.md`](/mnt/hdd2/jundahe/LLM-J/paper-2/phase2/PAPER_OUTLINE.md:7). On those four panels, sign concordance is only 2/4 and Spearman \(\rho=0.20\). The reported 6/8 and \(\rho=0.62\) pool those panels with commit and SummEval, which were used to formulate the explanation. That pooled result is descriptive, not a prespecified validation.

I would write:

> On the four panels reserved for the prespecified check, the predicted sign held in two and the cross-panel Spearman correlation was 0.20. Both discordant cases had small \(G\times R\) and small RPS contrasts, but no indifference region was prespecified. Pooling these panels with the four hypothesis-generating commit and SummEval panels yielded 6/8 sign concordance and \(\rho=0.62\). Thus the results are qualitatively compatible with the proposed location account but do not validate a necessary condition or an effect-size predictor.

The “five clear effects above 0.025 versus three below 0.01” split is post hoc and outcome-defined. It can be shown descriptively but not presented as confirmation. The eight panels are also not independent: the two commit criteria and two SummEval criteria share datasets.

For commit What:

> Frozen-feature heads showed a positive mode-only permutation contrast on commit What (+0.0056 RPS, descriptive SEM 0.0007), whereas the Qwen LoRA estimate on split 0 was near zero and slightly negative (−0.0007, 95% conditional CI [−0.0019, 0.0004]). Because these pipelines also differ in target-rater count, objective, representation updating, and replication structure, this is an unresolved cross-pipeline discrepancy, not an identified model-class interaction.

## D. Vetoes and priorities

I would additionally veto:

- “The bug did not change any heads conclusion.” It preserved the commit Why point estimates, but it changed their dose, support, and evidential interpretation.
- “TV dose certificates are logged in all four scripts.” They currently are not.
- “G×R check prespecified, 6/8.” Only the four held-out panels constitute the prespecified check.
- “Mode and mean pin down 77%.” That confuses maximum simultaneous matching with heterogeneous-cell support.
- “Dense panels ≈1.0 dose” unless this refers to final post-projection targets and is demonstrated by the new certificates.
- “No corresponding location penalty on commit What” without specifying “in the LoRA experiment”; heads now disagree.
- “Clear location effect” based on descriptive SEMs over dependent configurations.
- Any headline use of the current T3b vector-matched row while the corrected block is pending.

Top three actions before drafting:

1. Complete and freeze a clean corrected-results manifest: all `_v6` ordinal heads, ChaosNLI, positive controls, corrected SummEval seed block, and final-target dose certificates with code/output hashes.

2. Rebuild the tables and outline from those artifacts only. Put dose/support beside every permutation contrast, make SummEval/dense panels the main residual-allocation evidence, and purge the many superseded “two numbers suffice,” “shape is noise,” and stale commit What statements.

3. Either run a controlled bridge for commit What using aligned item/rater splits and targets across heads and LoRA, or explicitly leave the discrepancy unresolved. Downgrade G×R to an exploratory explanatory diagnostic; the held-out result does not justify stronger wording.

## Verdict

The dose correction is a credible recovery, and the corrected SummEval plan is methodologically adequate. The paper is not yet draft-ready: the commit null must be demoted, the certificate implementation completed, and the G×R result rewritten as a weak held-out check rather than a validated necessary-condition account. Once those changes and the corrected reruns are in place, the intervention audit remains a viable top-venue empirical contribution.