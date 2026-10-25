# Research review brief — follow-up idea after /idea-discovery (read everything it points to before judging)

You are a senior reviewer (NeurIPS/ICML/ACL level, with SE/ICSE sensibility). Start from the assumption that the work is broken somewhere; find where. Trust nothing stated here — verify against the files.

## Files to inspect (absolute paths)
- Canonical report (landscape, 48 ranked ideas, novelty verdict, pilot results): /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/IDEA_REPORT.md
- Pilot code: /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/train_judge.py (LoRA judge trainer, objectives), /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/csje_eval.py (strata/HCA/CRPS), /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/pilot_a_analysis.py (attribution nulls, RPS, bootstrap), /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/pilot_c_routing.py
- Raw pilot outputs: /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/results/pilot_a_report.json and /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/results/*/results.json, *pilot_c_routing.json
- Parent paper (for context): /mnt/hdd2/jundahe/LLM-J/paper-1/icse-2027/sections/discussion.tex, /mnt/hdd2/jundahe/LLM-J/paper-1/icse-2027/sections/result_rq4.tex
- Novelty dossier + verdict: /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/NOVELTY_DOSSIER.md (verdict is in IDEA_REPORT.md#novelty-verification)

## The proposed paper (as revised after novelty check + pilots)
**Working title:** "Do Distributional LLM Judges Learn Human Disagreement? An Attribution Audit with Small Annotator Panels."
**Thesis:** Better distributional scores are not evidence that a judge learned human disagreement. On small (3–9-rater) SE annotator panels, (i) per-item disagreement is only weakly reliable and is strongly confounded with scale location; (ii) the held-out-rater gain of Chen-style soft-label fine-tuning (KL to the empirical histogram) is fully reproduced by a non-item-specific smoother (cross-fitted temperature + climatology mixture on a point-SFT judge) and is statistically indistinguishable from training on median-matched *permuted* histograms; (iii) a small-panel Bayesian target and a matched-human routing head do not rescue this.
**Claimed contributions:** (C1) a three-part identification contract for training-side disagreement claims — target reliability (split-half dispersion reliability), location-aware nulls, label-preserving attribution (median-matched permutation + gain-reproduction ratio), all against held-out individual raters by consensus stratum; (C2) the empirical audit of Chen-style distributional judges on SE panels (negative result, tiny Why residual); (C3, secondary/appendix) negative results for the EB posterior-predictive target (k=2) and for gain-based routing vs entropy.
**Data/compute:** three released multi-rater SE benchmarks (commit messages 800×6; code summarization 1,163×3; readability 200×9); Qwen2.5-Coder-7B LoRA on 4 shared RTX 6000 Ada (~22 GB free each); single PhD student; target ICSE/FSE or NeurIPS/ACL.

## Known weaknesses (be harsher than this list)
- One benchmark, one 7B model family, one seed, 240 test items; Why-criterion floor effects; the KL arm used a ½ CE mixture (Chen-style hybrid) while the k=2 arm used pure KL; N1 is cross-fitted on the test set (2-fold), not fitted on train; strata for per-rater scoring use the 5-rater Range rule; the point-SFT target is the *rounded* 6-rater median, so contested items (half-integer medians) get a systematically "noisier" label — possibly why CE/KL/permuted judges share the same entropy→Low signal; no replication on summarization/readability yet; the "learnability ceiling" is a reliability diagnostic, not a formal bound; K4 pilot used α fitted by LORO marginal likelihood which selected heavy shrinkage (α=2 at k=2).

## Questions
1. Logical gaps / unjustified claims in the thesis and in the attribution logic (is the gain-reproduction ratio + permutation placebo a valid identification argument? what confounds remain? is N1 "too strong" or "too weak" a null?).
2. Missing experiments that would make the negative result convincing to a top venue (replication, seeds, model families incl. a frontier API judge, the other two benchmarks, panel-size sweep, the half-integer-median confound, alternative distributional objectives such as Chen's adversarial term, Li's verbalized-probability SFT, per-rater conditioning) — give the *minimal* package with highest acceptance lift per GPU-week given our compute.
3. Narrative: is "attribution audit / negative result" a top-venue paper? What framing would make it one (and which venue)? Does it risk being "Kohli 2605.29797 + Gheibi 2605.20642 on SE data"?
4. Results-to-claims matrix: what claim is allowed under each plausible outcome of the replication package (e.g., residual appears on summarization but not commit; frontier judge differs; half-integer confound explains the entropy signal).
5. A mock review (Summary, Strengths, Weaknesses, Questions, Score 1–10, Confidence, What would move toward accept).
Be brutally honest and specific; cite file/line evidence where you can.
