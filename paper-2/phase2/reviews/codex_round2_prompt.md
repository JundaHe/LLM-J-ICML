You reviewed this project 24 hours ago (your review is in reviews/codex_direction_round1_2026-10-10.md — read it first to recall your own recommendations). We followed your advice: de-risked with frozen-feature heads on DICES first, killed the mixture-of-raters bet, and pivoted to the claim–estimand gap you identified. Now review the NEW state. Read, in this order (cwd = paper-2/phase2):
1. PROGRESS.md — hourly log; hours 1–10 contain every number.
2. PAPER_OUTLINE.md — title, claim, contributions, drafted Intro / Method / Results / Discussion / Limitations.
3. results/probe_mean/ALL_SUMMARY.md — heads hierarchy on 8 panels (paired contrasts).
4. ../idea-stage/pilot/results_v2/why/s0/analysis_v3.json, what/s0/analysis_v3.json, why/s1/analysis_v3.json — LoRA contrasts on commit; results/lora/summeval_coherence8/s0/analysis_lora_v3.json — first SummEval LoRA fold.
5. probe_mean.py, train_judge_v3.py, analysis_lora_v3.py if you need protocol details.

Summary of the claim: distributional (Chen-style) judge training gains decompose into class-conditional smoothing + item mean; the residual histogram shape is never used (mode+mean-preserving permutation inert on 8/8 heads panels and on both commit criteria with 7B LoRA); a (mode, mean) target — mode-conditional prototype exponentially tilted to the item mean — matches or beats the histogram everywhere (LoRA: commit What chen−mean2 −0.0007 [−0.0013,−0.0001]; SummEval fold 0 chen−mean2 +0.0024 [+0.0011,+0.0037]); mode-only permutation destroys mean-carried gains (commit Why +0.0033 s0, +0.0073 s1); positive controls on BW/Scalabrino show the assay detects injected shape; oracle gap shows shape beyond the mean exists only at ~100 raters on 5-level scales; Stage A: rater conditioning buys severity only.

Questions — verdict first, then reasons, be adversarial and specific:
1. Is this now an ACL/EMNLP-main paper? What is the single most likely rejection reason, and the second?
2. Novelty threats: SORD (Diaz & Marathe 2019), label-distribution learning (Geng), unimodal/ordinal soft targets, Kohli 2026, our own Phase-1 audit. For each: does it pre-empt the two-number target or the decomposition, and what exact experiment or framing neutralises it?
3. Statistics: effect sizes are 0.001–0.008 RPS. Is the item-clustered bootstrap over LORO folds (same test items across folds, one optimiser seed per split) defensible? What is the minimum replication structure a reviewer will demand (seeds × splits × families), and which of our current numbers would you not trust?
4. The protocol itself: the mean2 target uses the mode-conditional prototype estimated from training items — any leakage or asymmetry vs the soft arm? The adversarial term is applied to mean2/proto targets as well — fair? The heads use PCA-64 of frozen features — does that bias toward "mean-only" conclusions (low capacity cannot fit shape)? What control settles that?
5. What is the one experiment that would most raise acceptance probability given ~5 GPU-days (one RTX 6000 Ada), and what should we stop doing?
6. Which sentences in PAPER_OUTLINE.md over-claim relative to the evidence? Quote them and give the licensed version.
Write the answer as Markdown to stdout.
