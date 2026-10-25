# Idea Discovery Report

**Direction**: Training-side follow-ups to *"LLMs are Bad Judges? The Illusion of Alignment in Software Engineering"* (CSJE protocol + HCA metric): post-training LLM judges / reward models to model human disagreement instead of averaging it away — disagreement-aware (distributional) judge fine-tuning, uncertainty-calibrated judges that predict annotator disagreement and route contested items, pluralistic reward modeling for SE artifacts, downstream effects of pooled-label vs disagreement-aware rewards, and reasoning-RL judges on contested items.
**Date**: 2026-08-23
**Run id**: `disagreement-aware-judge-training-2026-08-23` (state: `.aris/runs/`)
**Pipeline**: research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline
**Executor / reviewer**: Claude Fable 5 (executor) · Codex GPT-5.6 (cross-family reviewer)

## Executive Summary

**Best idea (after 5 refinement rounds): an identifiability audit of soft-label ("distributional") LLM-judge training on small SE annotator panels.** The pipeline started from the user's direction (train judges that model disagreement), found that the naive follow-up is already published (Chen et al., NeurIPS 2025), and ran a 48-idea brainstorm whose Codex-ranked winner was an attribution test: does distributional fine-tuning learn *which* artifacts split raters, or only a smoother score distribution? Pilots on the commit-message benchmark (Qwen2.5-Coder-7B LoRA, leave-one-rater-out scoring, ≈ 3.7 GPU-h) showed the Chen-style gain is mostly calibration — after one shared calibrator is fitted symmetrically, CE − KL is +0.0008 [−0.0001, +0.0017] RPS on What and +0.0018 [+0.0005, +0.0031] on Why, with only a small histogram-specific component on Why — and that the two "treatment" ideas (a Bayesian small-panel target; matched-human routing) fail their pre-registered criteria. An adversarial Codex-ultra review (3/10 for the pilot as a paper) caught real identification flaws and five harness bugs — and, for the parent paper, a **readability snippet↔rating mis-alignment in the released scripts (18.5 % correct) that needs the user's decision**. The refinement's support audit showed the clean placebo is impossible on 2-rater targets and has only partial intensity elsewhere; the external review's second round then corrected the support definition (randomised maximum matching): exact randomisation can change ≈ one-third of training artifacts on commit Why, so the recommended paper is a **feasibility result (support quantities, dose, a validated support model, MDE) plus a scoped audit** with exact commit-Why as the primary experiment (refinement 7.6/10 REVISE; plan review PROCEED WITH CAUTION, ≈ 6/10 with the corrections applied; plan: 450 stage-gated LoRA runs ≈ 146 GPU-h). **Recommended next step**: the user decides on the readability fix; then M0 (support model + MDE, CPU) and the M1 exact commit-Why gate (24 runs) via `/run-experiment` — not the full matrix.

## Literature Landscape

**Sources.** arXiv API helper (`arxiv_fetch.py`, ≥27 distinct queries across three scouts; frequent HTTP 429 rate-limits, gaps covered by `arxiv.org/abs` fetches) + WebSearch (≈69 searches) + full-text reads of the three closest competitors. Zotero / Obsidian MCP and Gemini (MCP or CLI) are not configured on this machine → skipped. `WARN: local contributed nothing — no PDFs found in papers/, literature/, or a configured paper library` (the three benchmark-source PDFs under `icse-2027/` are already cited by the paper). **Verification** (`verify_papers.py`, 3-layer arXiv→CrossRef→S2): scope A 93/94 verified (Skywork-Critic: model card only, no paper), scope C 92/93 (cDPO: Mitchell 2023 tech note, no arXiv), scope B 72/72 verified. Raw candidate lists: `.aris/verify-papers/candidates_{A,B,C}.json`, verdicts in `verified_{A,B,C}.json`.

### 1. Map of the area (five sub-directions)

**(S1) Training judges on rating *distributions* instead of point labels.** The mainstream judge-training line — JudgeLM (2310.17631, ICLR 2025), Prometheus 2 (2405.01535), CompassJudger-2 (2507.09104), Self-Taught Evaluator (2408.02666), REAL regression-aware RL (2603.17145) — fits a single distilled or gold label; Huang et al. (2403.02839) show such judges behave like task-specific classifiers. Two 2025 papers already move to distributions: **Chen et al., NeurIPS 2025 "Distributional LLM-as-a-Judge" (2505.12301)** fine-tunes Qwen2.5-7B / Llama-3.1-8B with `α·KL(p_human‖q_θ) + (1−α)·CE(majority)` plus an adversarial ℓ₂-ball perturbation of the empirical distribution, on SNLI/MNLI (5 raters), SummEval (1–5 Likert) and MT-Bench, and reports KL to the pooled distribution falling from 0.74 (point-label SFT) to 0.52 (SummEval) at unchanged majority accuracy. **Li et al. "Judging with Confidence" (2510.00263)** matches verbalized probabilities to a *population* preference distribution (SFT on soft targets; GRPO with Brier/log proper-scoring rewards on binary labels), but its "annotators" are Gemini-2.5-Flash personas. Soft-label training in general (Singh et al. 2511.14117; LeWiDi-2025 2510.08460; survey 2601.09065) and per-annotator modelling (jury learning 2202.02950; Orlikowski et al. ACL 2025 2502.20897 — per-annotator fine-tunes mostly *memorise* annotators and generalise poorly; DiADEM 2604.08425) come from perspectivist NLP. **None of these touch SE artifacts, none uses an ordinal distance (EMD/CRPS/Wasserstein) for Likert scales, and — critically — every one of them is evaluated against the *same pooled distribution* it was trained on** (KL / accuracy vs majority, 8:2 split). No held-out-rater, no consensus stratification.

**(S2) Uncertainty-aware judges, disagreement prediction, and selective judging.** Inference-only: judgment-token distributions predict pairwise human disagreement (Wang/Zhang/Choi, EMNLP-F 2025, 2503.03064); judges are over-confident (2508.06225); ordinal conformal intervals for Likert judges (2509.18658, EMNLP 2025; Gupta 2026 2604.15302 proposes set width as a human-review trigger); linear probes give cheap calibrated confidence (2512.22245). Routing with guarantees: **Trust-or-Escalate (ICLR 2025 oral, 2407.18370)** — provable human-agreement level with abstention and a cheap→strong cascade; **SCOPE (ICML 2026, 2602.13110)** conformal risk control for pairwise judging; **HyPAC (2602.02550)** fast-LLM → reasoning-LLM → human routing with PAC error bounds (−78 % cost); PPI-style debiasing (2403.07008, 2408.15204; limits by Dorner et al. ICLR 2025 2410.13341). Disagreement prediction exists only for NLP (ordinal "opposition index" 2605.01168; CEFR judge–human disagreement 2605.12422; emotion: LLMs match majority labels but not uncertainty 2604.27345). Calibration training — RLCR (2507.16806), ConfTuner (NeurIPS 2025, 2508.18847), and the "confidence reward hacking" caution of Tan et al. (2607.04332) — calibrates P(my answer is correct) for single-truth tasks. Panels of frontier judges are a weak disagreement proxy ("Nine Judges" 2605.29800: 9 judges ≈ 2 independent votes; "Judge Knows When It Knows" 2608.07517: vote-margin abstention at 49 % coverage). **Every routing guarantee is defined against one gold/majority label — exactly the target our paper shows is unreliable on contested items — and no work validates a judge's per-item spread against per-item annotator dispersion on held-out raters.**

**(S3) Distributional / pluralistic reward modelling.** DPL hidden-context (ICLR 2024, 2312.08358), MaxMin-RLHF (ICML 2024, 2402.08925), VPL (NeurIPS 2024, 2408.10075), PAL (ICLR 2025, 2406.08469), QRM quantile RMs (2409.10164), DPRM optimal-transport RM (2402.09764), Pairwise-Calibrated Rewards (2506.06298), variance-aware RM with anchors (2605.11865), PEBS per-rater empirical-Bayes calibration (ICML 2026 wkshp, 2606.27578: pooling confounds rater scale with reward, −8.6 % held-out RMSE), RM ensembles (2310.02743, 2312.09244). **Zhang et al. "Diverging Preferences" (ICML 2025, 2410.14632)** is the closest RM-side template: Mean-Var and 5-way KL-classification RMs trained on per-annotator Likert (HelpSteer2, 3–5 raters; MultiPref, 4 raters), evaluated on 500 held-out items *stratified by agreement* (High-Agreement / Diverging) with a Diverging-ID AUROC; it shows BT RMs and LLM judges are equally decisive on divisive and consensual pairs (73.8 % vs 73.1 %). **Artificial Hivemind** (NeurIPS 2025 D&B oral, 2510.22954; 25 ratings/item) documents that RMs and judges are mis-calibrated precisely where annotators diverge. All of this is general chat/safety data; none compares to a matched held-out annotator; none has a downstream policy experiment.

**(S4) Downstream consequences of pooled / noisy preference signals.** Theory and synthetic-group evidence that KL-regularised RLHF amplifies the majority and collapses minority preferences (Xiao et al., JASA, 2405.16455; Soft Preference Learning, ICLR 2025, 2511.08594; PA-RLHF 2608.10126; Kirk et al. 2310.06452); soft-label / noise-robust optimisers — GAPO (NeurIPS 2024, 2409.06691), cDPO (Mitchell 2023), rDPO (ICML 2024, 2403.00409), ROPO (2404.04102), Dr.DPO (ICLR 2025, 2407.07880), RA-DPO weighting DPO by annotator agreement (2608.12330, classification only); best-of-n with imperfect rewards (HedgeTune, NeurIPS 2025, 2506.19248; 2503.21878; 2604.04648). Noise-robust PO models disagreement as a scalar flip rate, conflating plurality with noise; **no study measures generation quality separately on contested vs. uncontested items after DPO/BoN with pooled vs. distributional rewards, and none in SE.**

**(S5) Reasoning / RL-trained judges on contested items.** RM-R1 (ICLR 2026, 2505.02387), DeepSeek-GRM/SPCT (2504.02495), J1 (2505.10320), JudgeLRM (2504.00050), RRM (2505.14674), Think-J (AAAI 2026, 2505.14268), J4R, TIR-Judge all use binary verifiable rewards; J1 explicitly *manufactures* verifiability for subjective prompts by synthesising degraded pairs. **The only evidence about reasoning models on human disagreement is negative: Ni et al. (EACL 2026, 2506.19467; 60 configurations) find RLVR-style reasoning degrades disagreement modelling while plain CoT helps RLHF models** — but on NLP classification, not Likert quality judging, and without RM-R1/J1/GRM-class judges. No paper trains a judge with RL against a distribution-matching or proper-scoring reward over annotator distributions.

**(S-SE) Software-engineering instances.** SE judges — CodeJudge (2410.02184), CodeVisionary, SE-Jury (2505.20854), AXIOM, CriterAlign (2605.19665), Themis code RMs (2605.00754), CoRAL code-review RM (2506.04464) — and SE preference data — CodeUltraFeedback (TOSEM, 2403.09032; GPT-3.5 ratings), CodeFavor/CodePrefBench (2410.03837), BigCodeArena (2510.08697), "Learning to Align Human Code Preferences" (2507.20109) — use a single LLM judge or one human per pair. The multi-rater SE datasets that exist — Crupi et al. TSE 2025 (2507.16587; 3 raters), Zeng et al. 2025 (2507.10906; 6 raters), CoReEval/Scalabrino (9 raters), Mokhova et al. 2026 (2605.25296; 73 engineers, LLM Likert distributions polarised vs humans) — are all **averaged before use**. SE judge surveys (2510.24367, 2502.06193) name rating indeterminacy as an open gap without offering a method.

### 2. Closest prior work (the papers a reviewer will cite)

| Paper | Venue | What it does | What it does *not* do (our opening) | Status |
|---|---|---|---|---|
| Chen et al., Distributional LLM-as-a-Judge (2505.12301) | NeurIPS 2025 | KL+CE(+adversarial) fine-tune of 7–8B judge to human score distributions; SummEval KL 0.74→0.52 | Pooled target; evaluated on the *same* pooled distribution; no held-out rater, no strata; no SE; no ordinal loss; no annotator identity | ✅ verified (arxiv) |
| Li et al., Judging with Confidence (2510.00263) | arXiv 2025 | Verbalized-probability calibration to population preference dist (SFT + GRPO-Brier) | Pairwise only; synthetic persona annotators; no per-annotator, no strata, no SE | ✅ verified |
| Zhang et al., Diverging Preferences (2410.14632) | ICML 2025 | Mean-Var / KL-classification RMs on per-annotator Likert; agreement-stratified eval; Diverging-ID AUROC | No matched held-out-human reference; no downstream policy/BoN; no SE; scalar RM not generative judge | ✅ verified |
| Jung et al., Trust or Escalate (2407.18370) | ICLR 2025 oral | Selective judging with provable agreement; cascade | Guarantee vs pooled label; escalates to a stronger LLM, not a human; no training; no SE | ✅ verified |
| Ni et al., Can Reasoning Help… Disagreement? (2506.19467) | EACL 2026 | RLVR reasoning hurts disagreement modelling | NLP classification only; no judge training; no Likert SE | ✅ verified |
| Guerdan et al., Rating Indeterminacy (2503.05965) | NeurIPS 2025 | Validation framework for multi-valid ratings | Validation only; no trained judge | ✅ verified |
| Orlikowski et al., Beyond Demographics (2502.20897) | ACL 2025 | Per-annotator fine-tuning memorises annotators | Negative result to design around; no judge task | ✅ verified |
| PEBS (2606.27578) / Pairwise-Calibrated Rewards (2506.06298) / GAPO (2409.06691) | ICML-26 wkshp / arXiv / NeurIPS 2024 | Per-rater calibration / disagreement-matched reward ensembles / soft-label PO | No strata, no SE, soft labels synthetic, no contested-vs-uncontested downstream split | ✅ verified |
| HyPAC (2602.02550) / SCOPE (2602.13110) / Gupta conformal (2604.15302) | arXiv / ICML 2026 / arXiv | Uncertainty-thresholded routing with PAC/conformal guarantees | Post-hoc thresholds vs one gold label; no learned disagreement; no SE Pareto vs matched human | ✅ verified |
| Artificial Hivemind (2510.22954) | NeurIPS 2025 D&B | Judges/RMs fail where annotators diverge (25 ratings/item) | Diagnostic; no trained judge; no SE; dense panels | ✅ verified |
| SE-Jury (2505.20854) / Crupi et al. (2507.16587) / Zeng et al. (2507.10906) | arXiv / TSE 2025 / arXiv | SE judges & multi-rater SE benchmarks | Pool labels; no training on disaggregated ratings | ✅ verified |

### 3. Structural gaps (consolidated from the three scouts)

1. **Circular validation of distributional judges.** Chen 2025 / Li 2025 train *and* test on the same pooled distribution, so "learned the disagreement structure" is indistinguishable from "learned the pooled mean plus a global smoothing". A matched held-out-rater, consensus-stratified protocol (CSJE/HCA) has never been applied to a trained distributional judge — the mirage may survive inside their own numbers.
2. **No SE judge or reward model has ever been trained on disaggregated ratings**, although three multi-rater SE benchmarks (3/6/9 raters) exist; every SE judge line pools.
3. **Small-panel regime (3–9 raters) is untreated.** Existing methods assume dense crowds (25 ratings/item) or add ad-hoc adversarial smoothing; principled targets (leave-one-rater-out proper scoring, Dirichlet/ordinal priors) are open, and identifiability of per-item variance from few raters is flagged as open by the variance-aware-RM line.
4. **Ordinal-aware distribution losses (EMD/CRPS/Wasserstein on 0–4 / 1–5) have not been tried for judges**; CRPS appears only for LLM regression (2605.20740).
5. **Per-item disagreement prediction as a judge output, validated against held-out raters, does not exist** — routing guarantees (Trust-or-Escalate, SCOPE, HyPAC) are all relative to one gold label, and there is no SE cost–quality Pareto against a matched human.
6. **RL/reasoning judges are trained only with hard verifiable rewards**; the single data point on contested items (Ni 2025) is negative but narrow; whether RM-R1/J1/GRM-class judges inherit the degradation on Likert SE tasks is unmeasured, and no one has trained a judge with a distribution-matching reward.
7. **Downstream: "pooled reward ⇒ median-seeking policy" is theorised and shown on synthetic groups, never measured on real multi-rater data split by contested vs. uncontested items**, and never in SE generation (commit messages, summaries).
8. **Per-annotator fine-tuning memorises rather than generalises (Orlikowski 2025)** — any annotator-conditioned SE judge must be evaluated on unseen raters, which the 6- and 9-rater panels make possible.

### 4. Take-away for idea generation

The naive follow-up — "fine-tune a judge to match rating distributions" — is already published at NeurIPS 2025 in general NLP. A publishable SE contribution must therefore (a) change the *evaluation contract* (held-out rater + strata, i.e. settle "smoothing vs. disagreement"), (b) change the *training target* for small ordinal panels (leave-one-rater-out proper scoring, ordinal transport, annotator conditioning with unseen-rater evaluation), (c) turn the judge's spread into an operational *routing* signal scored against a matched human, or (d) measure what the pooled signal does *downstream* on contested items. Ideas that merely transplant Chen 2025 to code will be killed at novelty check.

## Ranked Ideas

**Generation.** 12 ideas from Codex GPT-5.6 (xhigh, cross-model seed; trace `.aris/traces/idea-creator/2026-08-23_run01/001-ideation`) + 36 from six parallel Claude lens generators (method-transfer · contradiction · untested-assumption · scaling-regime · diagnostic · training-signal) = **48 candidates**, mechanically clustered into nine themes (no same-family quality filtering; all 48 passed the objective budget gate: < 1 week GPU, data on hand). **Quality verdict** = Codex GPT-5.6 devil's-advocate triage over all 48 (trace `…/002-triage-devils-advocate`). Full candidate texts: `idea-stage/triage/lens_candidates.json`, `idea-stage/triage/codex_ideas.md`.

### Clusters (theme → members)
| # | Theme | Members | Reviewer's surviving formulation |
|---|---|---|---|
| C1 | Smoothing vs item-level disagreement attribution | codex#1, contradiction#1, diagnostic#2, untested#2, scaling#4, untested#6, method-transfer#4 | **contradiction#1** + nulls of diagnostic#2 + split-half ceiling of scaling#4 |
| C2 | Pooled-label SFT manufactures the mirage | untested#1, diagnostic#1 | diagnostic#1 (supporting RQ only; near-tautological alone) |
| C3 | Training targets / output heads for 3–9-rater ordinal panels | codex#2, codex#3, codex#9, codex#12, method-transfer#1, method-transfer#3, untested#3, scaling#1, scaling#3 | **method-transfer#1** + rater-count curve of untested#3 |
| C4 | Uncertainty → routing scored against a matched human | codex#4, training-signal#3, method-transfer#6 | **training-signal#3** (+ rater-exchangeable coverage mirage of method-transfer#6 as baseline) |
| C5 | Rater structure / unseen-rater personalisation | codex#5, contradiction#3, training-signal#5, method-transfer#2, diagnostic#5, contradiction#4, contradiction#6, diagnostic#6 | contradiction#3 (affine severity as the hypothesis) |
| C6 | Downstream best-of-n / DPO on real multi-rater SE data | codex#6, codex#7, contradiction#5, diagnostic#4, training-signal#1, training-signal#2, scaling#5, method-transfer#5 | **training-signal#1** + mirage gap (diagnostic#4) + CVaR rules (method-transfer#5) |
| C7 | RL / reasoning judges with distribution rewards | codex#8, contradiction#2, diagnostic#3, training-signal#4 | contradiction#2 (reward × reasoning factorial) — *after* an SFT-level signal exists |
| C8 | Validation regimes (rater-disjoint splits, authorship transfer, test-time sampling, size-vs-training) | untested#5, untested#4, scaling#2, scaling#6, codex#11 | untested#5 (both-disjoint split) |
| C9 | Annotation-budget allocation | codex#10, training-signal#6 | training-signal#6 (protocol appendix) |

### Reviewer's top 12 (authoritative ranking)
| Rank | Id | Idea | Risk | Effort | Why it ranks |
|---|---|---|---|---|---|
| 1 | contradiction#1 | **Learned disagreement or learned smoothing?** Re-train the distribution-alignment objective on the 6-rater commit-message panel; score against a matched held-out rater by stratum with explicit item-independent nulls (temperature + criterion-marginal mixture; location-conditional pmf) and a histogram-permutation placebo; report the "smoothing share" | LOW | 1–2 w | The make-or-break falsification of the NeurIPS-2025 distributional-judge claim; credible nulls + unseen-rater outcome |
| 2 | method-transfer#1 | **Small-panel ordinal posterior-predictive target + RPS**: Dirichlet-multinomial posterior predictive with empirical-Bayes concentration (shrinkage ∝ 1/k), bounded ordinal proper score, climatology/panel-anchored distributional skill score; show Chen's ε-ball is a small-k artefact | LOW–MED | 2–3 w | The strongest *treatment*: principled small-panel target, held-out-rater validation, human-anchored skill score |
| 3 | training-signal#3 | **Route by matched-human gain, not entropy**: learned gain head g=|J−Y_ref|−|Y_h−Y_ref|; cost–quality Pareto vs entropy/contested-first/conformal/random/oracle | LOW | days–1 w | Clearest operational consequence of CSJE; existing routing work targets a pooled label |
| 4 | training-signal#1 | Offline best-of-n on the fully rated 6-candidate summary pools and dev/gen commit pairs: selection rule (mean / quantile / P(≥4)) vs matched-human selector, by pool contestedness | LOW | days–1 w | Fully offline, real multi-rater outcomes, no surrogate judge |
| 5 | untested#5 | Rater-disjoint validation contract (item-only vs rater-only vs both-disjoint) + panel-specificity index | MEDIUM | 2 w | Establishes whether distributional gains are panel-specific |
| 6 | untested#3 | Rater-count identifiability curve: raw vs shrunk targets as k=1…m−1; target noise floor | MEDIUM | 2–3 w | Actionable rater-count guidance before any method |
| 7 | scaling#4 | Split-half learnability ceiling per criterion (is per-item disagreement an item property?) | LOW | 1–2 w (CPU) | Cheap prerequisite that can stop a doomed training project |
| 8 | contradiction#5 | Disagreement-as-noise (rDPO/ROPO) vs disagreement-as-signal (soft DPO) on real 6-rater commit pairs; policy calibration on contested pairs | MEDIUM | 2–3 w | Strongest real-data downstream test (policy calibration only, no generation claims) |
| 9 | contradiction#2 | GRPO judge: {CoT on/off} × {hard median-match / proper-scoring reward}; resolves Ni 2025 vs RM-R1/J1 | MED–HIGH | 3–5 w | Timely; high execution risk; not the first investment |
| 10 | untested#2 | Entropy = location, not disagreement: location-controlled disagreement metric for ordinal scales | LOW–MED | 1–2 w | Undermines the premise of all uncertainty-routing schemes |
| 11 | contradiction#3 | Leniency vs taste: per-rater affine calibration as the hypothesis; unseen-rater k-shot | LOW–MED | 1–3 w | Defensible perspectivist study for small panels |
| 12 | method-transfer#6 | Rater-exchangeable conformal coverage ("coverage mirage") + set width as escalation trigger | MEDIUM | 2–3 w | Concrete protocol result; training part needs validity care |

### Paper-shaped packages (reviewer's synthesis)
- **Package A — "Learning disagreement rather than smoothing"** = scaling#4 → contradiction#1 → method-transfer#1 → training-signal#3. *Thesis:* a distributional judge counts as disagreement-aware only when (i) the benchmark has reproducible item-level dispersion, (ii) the trained judge beats item-independent smoothing on an unseen rater, and (iii) its predicted distribution improves a matched-human routing decision. *Dominant contribution:* a training + validation contract for small-panel distributional judges with a concrete ordinal method. Coherent under negative results. **← selected for pilots and refinement.**
- **Package B — "The downstream cost of median optimisation"** = diagnostic#1 → training-signal#1 → contradiction#5. Offline best-of-n on fully rated pools as primary evidence; DPO secondary unless fresh human ratings are collected.

### Pre-registered pilots (Codex-specified; ≤ 2 GPU-h each on the commit-message benchmark)
| Pilot | Idea(s) | Design | Success criterion |
|---|---|---|---|
| A | contradiction#1 (+diagnostic#2, scaling#4) | Qwen2.5-Coder-7B LoRA; arms: zero-shot, CE-to-median, KL-to-histogram (+½ CE, Chen-style), KL with histograms permuted within median bins (placebo); nulls: cross-fitted temperature+climatology mixture on the point judge, location-conditional pmf, climatology; leave-one-rater-out RPS by stratum | *Item-specific learning* iff true KL beats the strongest item-independent null **and** the permuted model by ≥ 0.01 RPS (paired item-bootstrap CI excl. 0) **and** level-adjusted entropy→Low AUROC > 0.60; *smoothing* iff ≥ 70 % of the KL-vs-CE gain is reproduced by the null and true ≈ permuted within ± 0.005 |
| B | method-transfer#1 (+untested#3) | Training raters subsampled to k = 2 and k = 6; objectives: raw KL, CRPS to raw histogram, empirical-Bayes posterior-predictive + CRPS; held-out-rater RPS by stratum; skill vs climatology (0) and 5-rater panel (1) | At k = 2 the posterior-predictive target improves Low/Partial RPS by ≥ 0.01 over the best of raw KL / raw CRPS (CI excl. 0), High not worse by > 0.005, skill CI > 0; gain larger at k = 2 than k = 6 |
| C | training-signal#3 | Cross-fitted GBM gain head on judge-side features; policies gain-first / entropy-first / predicted-Low-first / random / oracle; hybrid MAE vs matched reference rater at 10–50 % human budget | Positive-gain AUROC ≥ 0.60 and ≥ 0.05 above entropy; at 20 % budget MAE reduction ≥ 0.05 vs entropy-first (CI excl. 0); High-stratum MAE not worse by > 0.02 |

Pilot scripts: `idea-stage/pilot/{csje_eval.py, cm_data.py, cs_data.py, train_judge.py, pilot_a_analysis.py, pilot_reanalysis.py, pilot_c_routing.py}` (the latter three incorporate the round-1 review fixes).

## Novelty Verification

**Protocol.** Three independent multi-source scouts (arXiv API + WebSearch + abstract fetches; every ID verified by retrieval and by `verify_papers.py` — `verified_novelty_{A,B,C}.json`, 36/36 verified) on the three reviewer-selected ideas, followed by a cross-model verdict from Codex GPT-5.6 (xhigh) on the full dossier `idea-stage/NOVELTY_DOSSIER.md` (trace `.aris/traces/novelty-check/2026-08-23_run01/001-novelty-verdict`, thread `01a02adb-1cdf-7382-b2a0-b1ddc57d2fff`).

### Closest prior work (the papers a reviewer would cite)
| Paper | Year | Venue | Overlap | Key difference |
|---|---|---|---|---|
| Kohli, *Metric-Dependent Annotation Saturation for Learning from Label Distributions* (2605.29797) | 2026-05 | arXiv | Small-panel soft labels, Dirichlet-multinomial targets (fixed α), held-out annotator *group*, temperature control, per-item entropy correlation | No individual-rater LORO, no ordinal location control, no split-half dispersion reliability, no median-matched placebo, no gain attribution; categorical NLI, not judges |
| Gheibi, *Same Target, Different Basins* (2605.20642) | 2026-05 | EIML@ICML | Shuffled soft-label control, label-smoothing baselines | Global shuffle also destroys the pooled label; CIFAR-10H |
| Chen et al., *Distributional LLM-as-a-Judge* (2505.12301) | 2025 | NeurIPS | The training method under audit | Scores against the same pooled histogram; cannot establish prediction of a new human rating |
| Peale, *Flexible Routing via Uncertainty Decomposition* (2605.07805) | 2026-05 | arXiv | Learned reducible-loss routing vs total-uncertainty routing | Noise-free Bayes oracle target, classification; not a matched noisy human |
| Calderon, *Alternative Annotator Test* (2501.10970) | 2025 | ACL | Leave-one-annotator-out judge evaluation | Point judgments only; no distributional scoring / attribution |
| Klugmann, *Crowd-Informed Machine Annotation* (2409.00048) | 2024 | arXiv | Dirichlet posteriors as training objective | Fixed uniform prior; vision; no held-out rater |
| Li et al. (2510.00263); Zhang et al. (2410.14632); Trust-or-Escalate (2407.18370); HyPER (2410.19133); multi-expert L2D (2407.07003, 2411.11976, 2403.02683, 2502.10533) | 2024–26 | various | see Literature Landscape | pooled/synthetic targets, classification, no SE |

### Per-component verdict (Codex GPT-5.6)
| Component | Novelty | Closest | Delta |
|---|---|---|---|
| K1 learnability (split-half dispersion reliability) + location-controlled disagreement metric | **HIGH** | Kohli 2605.29797 | Kohli studies annotator-count saturation; no split-half dispersion reliability, no ordinal scale-location confound |
| K2 attribution protocol (LORO RPS by stratum; global-smoothing nulls; median-matched histogram-permutation placebo; gain-reproduction ratio) | **MEDIUM** | Gheibi 2605.20642 | Label-preserving permutation + held-out individual raters + quantified gain reproduction |
| K3 climatology/panel-anchored distributional skill score | LOW | our HCA | straightforward skill-score analogue — report as evaluation detail |
| K4 EB posterior-predictive ordinal target + RPS | LOW | Kohli 2605.29797 | EB concentration, ordinal RPS, LLM-judge setting are incremental refinements; **conditional on Pilot B beating the histogram, Chen's ε-ball and Kohli-style fixed priors** |
| K5 matched-human gain routing | MEDIUM | Peale 2605.07805 | only genuine distinction = optimisation against a noisy matched rater; **pilot failed → appendix / secondary negative result** |

**Overall: 6/10 — PROCEED WITH CAUTION.** Key differentiator: a label-preserving attribution test showing that improved held-out-rater proper scores need not imply learning item-specific disagreement. Risk: ingredients are individually established; a sceptical reviewer can frame the package as "Kohli's small-panel analysis + Gheibi's shuffle control applied to Chen-style judges on SE Likert data with an Alternative-Annotator-Test evaluation"; the negative result rests on one model / one benchmark / 240 items until replicated.

**Reviewer's positioning.** Lead with *"better distributional scores are not evidence that a judge learned human disagreement"*: merge K1+K2 into a three-part identification contract (target reliability → location-aware nulls → label-preserving attribution, all against held-out individual raters); fold K3 into evaluation; keep K4 only if Pilot B clearly wins; move K5 to an appendix; rename "smoothing share" → *gain-reproduction ratio* (values > 1 mean the smoother beats the trained judge); soften "unlearnable" → "not reliably measurable with this panel". Suggested title: **"Do Distributional LLM Judges Learn Human Disagreement? An Attribution Audit with Small Annotator Panels."**

**Eliminated at this stage:** the headline versions of method-transfer#1 (scooped in spirit by Kohli 2026-05 / Klugmann 2024 unless Pilot B shows a clear win) and training-signal#3 (Peale 2026-05 + failed pilot).

## External Critical Review

**Round 1 — Codex GPT-5.6, reasoning `ultra`, adversarial brief `idea-stage/RESEARCH_REVIEW_REQUEST.md`; the reviewer independently re-ran the code and checked raw outputs** (trace `.aris/traces/research-review/2026-08-23_run01/001-round-1-review`, thread `01a02af0-4e5e-7460-8740-45036b668097`). **Verdict: 3/10 — strong reject in the pilot's current form (4/10 for ICSE/FSE); the central empirical observation is real, the identification claim is not.**

### What the reviewer verified and what it broke
| Finding | Status after our re-analysis |
|---|---|
| Averaging the held-out-rater RPS over all six raters is algebraically identical (for model contrasts) to scoring against the pooled empirical histogram; rater identities are never unseen | **Accepted.** The pilot's "held-out-rater" evaluation is proper-score evaluation on held-out *items*, not an escape from pooled targets. The experiment plan makes rater-identity-disjoint target construction (one rater excluded from all targets, then evaluated) the primary design |
| N1 was transductive (per-rater 2-fold on test labels), asymmetric (only CE calibrated), and not item-independent | **Fixed in re-analysis:** one shared (T, λ) calibrator, fitted by diff-grouped cross-fitting on all six raters and applied identically to every arm; renamed *global-smoothing null*; the plan moves it to an untouched validation split |
| Median-matched permutation preserves only the banker-rounded median (exact median 72 %, mean shifts ≈ 0.30, 42–49 % cross developer/generated pools); one permutation, one seed; "statistically indistinguishable" was false on Why | **Accepted.** Re-analysis reports the Why placebo gap as significant; plan: several permutations conditioned on (median, pool, mean bin) with tighter location preservation |
| Gain-reproduction ratio is not identification; needs reliability–resolution decomposition | **Fixed:** threshold-Brier REL/RES/UNC decomposition added; the estimand becomes *item-conditioned resolution beyond calibration* |
| Not Chen's full objective (no adversarial term; KL:CE = 2:1); Why conditioned on ground-truth What at train vs predicted What at test | **Accepted** → plan: exact objective incl. adversarial ε-ball; Why scored independently of What |
| Bugs: AUROC ignores ties; ordinal Krippendorff α doubled D_o (all Δ_match magnitudes inflated); 9-rater strata used modal frequency instead of median agreement; bootstrap not clustered by diff (120 independent diffs, not 240 rows); routing KFold leaked companion messages; stale `pilot_a_report.json`; `--eval_only` adapter bug; k = 2 arms evaluated on the two raters used to build their targets | **Fixed** (`csje_eval.py`, `pilot_reanalysis.py`, `pilot_c_routing.py`); re-analysis below |
| **Parent-paper readability scripts align rating columns by nearest mean (18.5 % correct) instead of the direct `snippet_id ↔ SnippetN` key** | **Verified independently** (correct strata 59/56/9 vs 40/65/19 used in the paper); recorded in memory; *user decision pending* |
| Location adjustment by argmax bins inadequate; continuous residualisation removes most of the Why entropy→Low signal | **Accepted:** cross-fitted cubic residualisation on expected score implemented |
| Parent-paper overlap ("salami-sliced ablation" risk); novelty evidence is bibliographic only | Positioning narrowed to the calibration / conditional-resolution audit + target randomisation |

### Re-analysis with the fixes (commit messages; cluster-by-diff 95 % CIs; shared symmetric calibration)
| Contrast (RPS, + = second better) | What | Why |
|---|---|---|
| CE − KL, raw | +0.0041 [+0.0022, +0.0061] | +0.0112 [+0.0081, +0.0144] |
| CE − KL, **both calibrated** | +0.0008 [−0.0001, +0.0017] | **+0.0018 [+0.0005, +0.0031]** |
| CE − permuted-KL, both calibrated | −0.0002 [−0.0010, +0.0007] | −0.0013 [−0.0025, −0.0000] |
| permuted-KL − true KL, both calibrated | +0.0009 [+0.0000, +0.0018] | **+0.0030 [+0.0016, +0.0045]** |
| Resolution (RES, calibrated): CE / KL / permuted | .0630 / .0644 / .0629 | .0710 / .0716 / .0684 |
| Location-controlled entropy→Low AUROC (CE / KL / perm) vs location-only | .58 / .61 / .62 vs .61–.63 | .64 / .58 / .60 vs .79 |
| k = 2 raw-KL RPS on the four *unseen* raters vs k = 6 KL | .1088 vs .0971 | .1127 vs .1120 |

**Corrected reading.** On *What*, the soft-label gain is entirely reliability (calibration): after symmetric calibration CE ≈ KL ≈ permuted-KL and the resolution terms coincide. On *Why*, ≈ 84 % of the raw gain is calibration, but a small, significant item-conditioned and histogram-specific component remains (+0.0018 RPS over calibrated CE; +0.0030 over the permuted target; RES .0716 vs .0684). The k = 2 "advantage" was seen-rater leakage; the posterior-predictive target remains worst. Routing with diff-grouped CV: CE/Why @ 20 % budget gain-head beats entropy by 0.025 [0.001, 0.053] MAE (significant, below the pre-registered 0.05), null elsewhere. *The honest thesis is therefore the reviewer's: soft-label fine-tuning improves prediction of a new rating mostly through calibration; whether and when it adds conditional resolution is the question, and on these panels the answer is "barely, and only where item-level disagreement is reliable (Why)".*

### Reviewer's minimal package (highest acceptance lift per GPU-week; 50–150 GPU-h)
1. Zero-GPU repairs: estimand (fixed panel vs new raters), diff-grouped train/calibration/test, shared validation-fitted calibrator applied symmetrically, REL/RES/UNC decomposition, "split-panel reliability diagnostic" (not "ceiling"), clustered + two-way item×rater inference, TOST equivalence margins, immutable manifest.
2. Commit-message factorial: 2 open model families × 3 seeds; arms = hard median CE · tie-aware location-only target · true histogram · exact Chen objective (adversarial) · several conditioned permutations · symmetric calibration of all arms; Why independent of What; rater-identity-disjoint rotations; separate model / rater-subset / permutation seeds; integer vs half-integer medians.
3. Breadth: code summarization (grouped by function), correctly aligned readability; for NeurIPS/ACL one non-SE multi-rater replication and a formal conditional-resolution estimand.
4. Panel-size k ∈ {2, 3, 5, full} with identical loss construction, evaluated only on unseen identities; test whether resolution tracks split-panel reliability.
Deprioritised: frontier API judges, Li-style verbalized-probability SFT, EB refinements, per-rater conditioning, routing.

### Results-to-claims matrix (reviewer's)
| Outcome of the replication package | Claim licensed |
|---|---|
| calibrated CE ≈ calibrated KL and true ≈ permuted across models/datasets | in small-panel settings, soft-label gains are explainable by calibration / target regularisation |
| KL > calibrated CE and true > permuted | distributional training adds item-conditioned resolution (negative thesis false) |
| KL > CE but true ≈ permuted | soft-target regularisation helps, the item→histogram mapping is not responsible |
| true > permuted but calibrated CE ties true | histograms carry item signal without net proper-score advantage |
| residual only on summarization / high-reliability panels | soft labels help only where disagreement is reproducible — boundary-condition paper |
| exact adversarial objective succeeds, hybrid does not | only the simplified implementation failed |
| validation-fitted calibrator no longer ties KL | pilot result was driven by transductive calibration |
| half-integer control removes entropy signal but not RPS result | drop disagreement-detection claims; keep the calibration attribution |
| seed / rater uncertainty swamps the gaps | pilot underpowered; no population-level claim |
| routing succeeds after grouping | separate selective-prediction result |

### Round 2 — the revised research plan (Codex GPT-5.6 `ultra`, same thread; trace `.aris/traces/research-review/2026-08-23_run01/002-round-2-plan-review`)
**Verdict: PROCEED WITH CAUTION** — likelihood that the plan as written yields an ICSE/FSE-acceptable paper 4/10 (≈ 6/10 with the changes below), confidence 5/5; "redo M0 and run a small exact commit-Why gate — not launch all 378 runs".

The reviewer found the refinement's primary claim wrong in exactly the place it mattered: the support condition M ≤ N/2 characterises *full-cell* derangeability, whereas a maximum-cardinality exact matching changes min{N, 2(N−M)} items per heterogeneous cell, and under randomised matching every item in a heterogeneous cell has positive change probability. Our support audit had also used an ungrouped row shuffle instead of the hash-grouped split. Re-run correctly (`idea-stage/pilot/support_audit.py`, hash-grouped split, randomised maximum matching), the **max-changed fraction is .25–.32 on commit What, .33–.37 on commit Why (≥ .30 in every LORO fold at exact w = 1), .47–.59 on readability, 0 on summarization; dose (TV between original and donor histogram) ≈ .40 (exact) vs ≈ .25 (w = 2)**. "Exact identification exists only on readability" was therefore false: exact randomisation is feasible at ≈ one-third intensity on the criterion with reproducible disagreement, and the story is *incomplete intervention intensity*, not absence of support.

Other corrections adopted (all now in `refine-logs/FINAL_PROPOSAL.md`, `EXPERIMENT_PLAN.md`, `EXPERIMENT_TRACKER.md`, `idea-stage/docs/research_contract.md`): C1 narrowed to the finite-sample feasibility of *this* intervention (no general non-identifiability claim; the two-rater lemma proves determination under the stated tie rule only); the "predictive concentration model" must be frozen and validated on held-out splits / synthetic panels or be called an empirical audit; the 0.30 threshold replaced by MDE/power simulations using intensity and dose; Δ_soft is an objective-package contrast until a matched no-adversary arm (A_chen0, must-run) separates the adversarial term; the randomisation distribution G must be specified (randomised maximum matching, permutation seed independent of data order); three hash-grouped outer splits with independent optimiser and permutation seeds instead of three initialisation seeds on one split; families reported separately, never pooled; readability calibration split raised to 15 % with a coarse grid (≈ 12 calibration / 37 test snippets); REL/RES/UNC descriptive only (five-bin remainder ≈ .001 is comparable to the residual); the M1 gate must test parity / invariants / MDE, never effect direction; no pre-asserted "mostly calibration" language — a results-conditioned claim matrix; the pilot's location-residualisation claim is dropped (a quartic fit removes it); routing stays cut; the keyed 124-snippet readability subset has split-half dispersion reliability ≈ −0.04 (the +0.02 was on all 200).

Status of the round-1 objections: pooled-histogram equivalence and unseen rater identities — closed in design; asymmetric calibration — closed in the plan (the re-analysis remains transductive); permutation leakage — partially closed (exact w = 1 fixes pool, label and mean; G now specified); not-Chen's-objective — open until parity-tested against the released code; effective sample size — partially closed. Is this the right next paper? "Only conditionally": corrected M0 plus the exact commit-Why gate first, time-boxed; if the support result cannot become a general, reusable audit, pivot to offline best-of-n on the fully rated summary pools (Package B); noise-vs-signal DPO third.

**Framing adopted (reviewer's):** *"Soft-label fine-tuning can improve prediction of a new rating without necessarily adding conditional resolution beyond a globally calibrated point-label judge; we introduce an audit that separates calibration, score location and item-conditioned resolution, and study when each appears as panel reliability changes."* Working title: **When Do Soft-Label LLM Judges Add Conditional Resolution Beyond Calibration?** Venue: ICSE/FSE after the repair package (NeurIPS/ACL would additionally need a formal estimand and a non-SE replication). The refined proposal and its round-2 verdict are summarised above and in the Refined Proposal section.

## Eliminated Ideas

Killed or demoted at each phase (Codex GPT-5.6 triage verdict, novelty check, or pilot evidence). Full texts remain in `idea-stage/triage/`.

| Idea | Phase | Reason |
|---|---|---|
| codex#1 counterfactual anti-smoothing test (alone) | triage | Too narrow on its own; absorbed into contradiction#1 as the placebo arm |
| untested#6 disagreement from artifact features | triage | Generic feature study; panel-derived cross-criterion features leak human labels |
| method-transfer#4 label-noise dynamics (AUM) | triage | Shaky premise: the pooled median is not "noise" w.r.t. the objective optimised |
| untested#1 pooled-SFT amplifies median tracking / diagnostic#1 | triage | Near-tautological ("training to the median tracks the median"); supporting RQ only |
| codex#2 hierarchical ordinal next-rater head | triage | Assumes unimodal cumulative-link family before establishing that SE disagreement is unimodal |
| codex#3 mean-matched contrastive; codex#12 human-ceiling-weighted CE; codex#9 joint trade-off mixture | triage | Noisy pairwise dispersion targets / down-weights plurality / three rating vectors too weak for a multivariate mixture |
| scaling#1 iso-budget grid; scaling#3 output-head dof | triage | Over-gridded (192 correlated subsample runs from six raters); engineering comparison |
| codex#4 binary "safe" router | triage | Binarising a noisy continuous gain wastes information (superseded by training-signal#3) |
| training-signal#5 anchor-conditioned judge; codex#5; method-transfer#2 rater-channel Rasch; diagnostic#5; diagnostic#6 | triage | Four training raters cannot define a rater population; ≈ PEBS + many-facet Rasch; descriptive; restates the parent paper |
| codex#7 best-of-two escalation; scaling#5 in-benchmark BoN; training-signal#2 median-seeking collapse | triage | Leaves the 6-candidate summary pools unused / duplicate of training-signal#1 / needs fresh human evaluation |
| codex#8 proper-scoring RL; diagnostic#3; training-signal#4 (as standalone) | triage | Li et al. already do proper-scoring GRPO; GRPO instability; "not the first investment until an SFT-level disagreement signal exists" |
| scaling#6 size-vs-training Pareto; codex#11 cross-task transfer; scaling#2 test-time sampling | triage | Restates parent paper's F4 / uninterpretable multi-factor shift / secondary |
| codex#10 active-acquisition value head; training-signal#6 | triage | Protocol appendix at best; mature active-annotation area |
| **method-transfer#1 small-panel EB posterior-predictive target (K4)** | novelty + Pilot B | Scooped in spirit by Kohli 2605.29797 (Dirichlet-smoothed few-annotator targets, May 2026) and Klugmann 2409.00048; pilot: posterior-predictive + CRPS *worse* than raw KL at k = 2 (over-shrinkage). Kept only as an ablation / negative result |
| **training-signal#3 matched-human gain routing (K5)** | novelty + Pilot C | Peale 2605.07805 (route on reducible uncertainty) is the same pivot with a noise-free oracle; pilot: gain head never beats entropy routing (AUROC 0.53–0.67 vs 0.56–0.77; ΔMAE CI includes 0). Appendix negative result |
| Package B (downstream cost of median optimisation) | triage ranking | Strong but secondary; fixed candidate pools show selection, not generator behaviour; DPO arm needs fresh human ratings. Recommended as the *next* paper |

## Pilot Experiment Results

**Setup (all pilots).** Commit-message benchmark (Zeng et al.; 800 messages = 400 developer + 400 generated, 6 raters, What/Why on 0–4). Item-level 70/30 split grouped by diff (560 train / 240 test). Judge = Qwen2.5-Coder-7B-Instruct, LoRA r=16 on the verbatim Zeng prompt, score read from the next-token distribution over the five score tokens; 2 epochs, lr 1e-4, single seed (0). Every judge and null is scored against **each held-out individual rater** (leave-one-rater-out) with the ranked probability score RPS = Σ_k(CDF_q(k) − 1[Y_r ≤ k])²/4; strata (High/Partial/Low) come from the five raters other than the held-out one; paired item-bootstrap 95 % CIs (B = 1000). Scripts and raw outputs: `idea-stage/pilot/` (`train_judge.py`, `pilot_a_analysis.py`, `pilot_c_routing.py`, `results/*/results.json`, `results/pilot_a_report.json`). GPU cost so far ≈ 3.5 GPU-h (budget 8).

### CPU diagnostics (learnability ceiling, location confound) — scaling#4 / untested#2
| Panel | Split-half Spearman of per-item dispersion (Spearman–Brown to full panel) | Location-only AUROC for Low (|median − centre|) | Half-panel std → other-half Low AUROC |
|---|---|---|---|
| Commit What (800 × 6) | +0.22 (0.36) | 0.67 | 0.61 |
| Commit Why (800 × 6) | +0.36 (0.53) | 0.80 | 0.65 |
| Readability (200 × 9) | **+0.02 (0.04)** | 0.64 | 0.60 |
| Code summarization (3 raters) | n/a (1-vs-2 splits are mechanically confounded) | CA 0.65/0.73 · Conciseness 0.89/0.82 · Fluency 0.82/0.71 (Java/Python) | — |

*Reading.* Per-item disagreement is a moderately reliable item property on commit messages (Why > What) and **not reliably measurable at all on the readability panel** (r ≈ 0.02, consistent with the paper's S = 0.14). On bounded ordinal scales the Low stratum is strongly predictable from scale *location* alone — more so than from the other half-panel's dispersion — so any "entropy predicts disagreement" claim must beat a location null. Zero-shot judge entropy carries ≤ weak item-level information once level is controlled (What 0.59, Why 0.50 AUROC).

### Pilot A — learned disagreement or learned smoothing? (contradiction#1 + diagnostic#2 nulls) — **verdict: MOSTLY CALIBRATION (see External Critical Review for the corrected analysis)**
Held-out-rater RPS (lower is better); skill = 1 − (RPS − RPS_panel)/(RPS_clim − RPS_panel); level-adjusted entropy→Low AUROC in the last column.

| Judge / null | What RPS (High/Partial/Low) | skill | ent→Low adj. | Why RPS (High/Partial/Low) | skill | ent→Low adj. |
|---|---|---|---|---|---|---|
| zero-shot | .114 (.081/.111/.127) | .71 | .59 | .322 (.369/.326/.295) | −1.97 | .50 |
| CE to pooled median (point SFT) | .103 (.048/.104/.118) | .88 | .62 | .123 (.031/.114/.177) | .70 | .77 |
| KL to empirical histogram + ½ CE (Chen-style) | .098 (.052/.099/.112) | .94 | .64 | .112 (.031/.107/.158) | .85 | .76 |
| KL to **median-matched permuted** histograms (placebo) | .099 (.053/.099/.112) | .94 | .61 | .113 (.031/.107/.161) | .83 | .78 |
| N1 cross-fitted temperature + climatology mixture on the point judge | .098 (.056/.098/.112) | .95 | — | .109 (.036/.107/.149) | .89 | — |
| N2 location-conditional human pmf (by judge's predicted level) | .106 | .83 | .15 | .133 | .57 | .31 |
| N3 climatology (criterion marginal) | .159 | 0 | — | .175 | 0 | — |
| 5-rater panel predictive (human ceiling) | .095 (.056/.096/.104) | 1 | — | .100 (.033/.100/.137) | 1 | — |

Paired contrasts (RPS, + = second is better):
| Contrast | What | Why |
|---|---|---|
| CE − KL (total gain of distributional training) | +0.0041 [+0.0023, +0.0059] | +0.0112 [+0.0083, +0.0143] |
| CE − N1 (gain reproduced by the non-item-specific smoother) | +0.0042 [+0.0023, +0.0062] | +0.0139 [+0.0095, +0.0187] |
| N1 − KL (item-specific residual) | −0.0001 [−0.0013, +0.0012] | **−0.0027 [−0.0051, −0.0002]** (KL *worse* than the smoother) |
| N1 − KL, Low stratum | −0.0002 [−0.0021, +0.0018] | **−0.0076 [−0.0114, −0.0039]** |
| permuted − true KL (placebo gap) | +0.0002 [−0.0009, +0.0012] | +0.0018 [+0.0003, +0.0034]; Low +0.0037 [+0.0010, +0.0068] |
| gain-reproduction ratio (CE−N1)/(CE−KL) | 1.02 | 1.24 |

*Pre-registered interpretation (superseded by the re-analysis in the review section; kept for the record).* "Smoothing explanation" criteria met on both criteria (≥ 70 % of the KL-vs-CE gain reproduced by a non-item-specific smoother; true ≈ permuted within the ± 0.005 equivalence margin). Nuance worth reporting: on Why the true histogram beats the permuted one by a small but significant margin (≈ 0.002–0.004 RPS, concentrated in the Low stratum), i.e. a *detectable but practically negligible* item-specific component, still smaller than what a global temperature + mixture on the point judge delivers. Second finding: the level-adjusted entropy→Low AUROC (≈ 0.76–0.78 on Why) is identical for CE, KL and *permuted*-KL judges — whatever item-level disagreement signal the trained judges carry comes from point-label training (half-integer medians of contested items), not from the distributional target. The mirage shape survives training on What (Low HCA 1.22, Δ_match −0.42/−0.45).
 *Half-integer-median check (post-hoc).* Restricted to integer-median items the raw entropy→Low AUROC is unchanged (0.67–0.70 What, 0.79–0.80 Why for all trained judges), so rounding is not the source of the signal — but the reviewer's continuous location residualisation (cubic on expected score, cross-fitted) reduces it to 0.58–0.64, i.e. the entropy signal is mostly scale location; no claim of a learned disagreement detector is made.

### Pilot B — small-panel ordinal posterior-predictive target (method-transfer#1) — **verdict: FAIL (so far)**
Training targets built from k = 2 randomly chosen raters or all k = 6 (evaluation unchanged: all 6 held-out rotations).
| Target (k = 2 training raters) | What RPS (High/Partial/Low) | skill | Why RPS (High/Partial/Low) | skill |
|---|---|---|---|---|
| raw KL to 2-rater histogram | .105 (.064/.108/.114) | .84 | .108 (.041/.110/.143) | .90 |
| CRPS to 2-rater histogram | .108 (.069/.111/.117) | .79 | .108 (.039/.112/.143) | .90 |
| EB Dirichlet-multinomial posterior predictive (α = 2) + CRPS | .121 (.122/.121/.121) | .60 | .133 (.079/.143/.156) | .56 |
| CRPS to 6-rater histogram (k = 6) | .098 (.054/.099/.110) | .96 | .110 (.030/.107/.156) | .86 |
| EB posterior predictive (α = 2) + CRPS, k = 6 | .099 (.068/.098/.110) | .93 | .112 (.037/.112/.152) | .85 |
| (reference) KL + ½ CE, k = 6 | .098 (.052/.099/.112) | .94 | .112 (.031/.107/.158) | .85 |
| (reference) N1 smoother on the point judge | .098 (.056/.098/.112) | .95 | .109 (.036/.107/.149) | .89 |

*Reading.* **Verdict: FAIL.** The posterior-predictive target **hurts** at k = 2 (over-shrinkage toward the marginal flattens High-consensus items: High RPS .122 vs .064), failing the pre-registered criterion by a wide margin — consistent with Kohli (2605.29797): heavy priors hurt at small N. At k = 6 every distributional objective (KL, CRPS, posterior-predictive + CRPS) lands on the same RPS as the item-independent smoother N1 (.098–.099 vs .098 on What; .110–.112 vs .109 on Why); the expected k-interaction (larger gain at small k) is absent or reversed. Raw KL and raw CRPS tie; a 2-rater histogram is as good as the 6-rater one (Why: .108 vs .112). The ordinal bounded score changes nothing. K4 is demoted to an ablation / negative result: on this panel no training target extracts item-level disagreement beyond what a point judge plus global smoothing already gives.

### Pilot C — route by matched-human gain, not entropy (training-signal#3) — **verdict: FAIL**
Cross-fitted gradient-boosted gain head on judge-side features; hybrid MAE vs the matched reference rater (averaged over all ordered rater pairs).
| Judge | crit | judge-only MAE / human-only MAE | AUROC(g>0): gain-head / entropy / pred-Low / random | ΔMAE gain − entropy @20 % budget | @50 % |
|---|---|---|---|---|---|
| zero-shot | What | .650 / .632 | .45 / .54 / .52 / .49 | −0.012 [−0.040, +0.017] | +0.006 |
| CE-median | What | .554 / .632 | .55 / .58 / .56 / .49 | +0.013 [−0.009, +0.039] | +0.022 |
| CE-median | Why | .617 / .669 | .67 / **.77** / .77 / .48 | +0.013 [−0.010, +0.035] | +0.016 |
| KL-soft | What | .558 / .632 | .53 / .56 / .58 / .49 | +0.014 [−0.014, +0.041] | +0.034 [+0.002, +0.064] |
| KL-soft | Why | .611 / .669 | .58 / .76 / .74 / .47 | −0.000 [−0.028, +0.027] | −0.022 |

*Reading.* The learned gain head never beats entropy-first routing on AUROC and yields no significant MAE reduction at 20 % budget; entropy routing is *not* backwards here (AUROC 0.77 on Why). The oracle gap is large (e.g. .55 → .47) but not recoverable from judge-side features. After training, the judge alone is better than a single human on What (.55 vs .63), so routing has little to buy. K5 → appendix negative result.

### GPU / budget
| Run | GPU | Wall time | Status |
|---|---|---|---|
| zero-shot eval | 1 | 6 min | done |
| CE-median · KL-soft · permuted-KL · raw-KL k2 · CRPS k2 · PP-CRPS k2 | 0–3 | ≈ 25 min each | done |
| CRPS k6 · PP-CRPS k6 | 2–3 | ≈ 25 min each | done |
Total ≈ 3.7 GPU-h of the 8 GPU-h pilot budget (9 LoRA runs + evaluations).

## Refined Proposal

`/research-refine-pipeline` ran 5 Codex GPT-5.6 (xhigh) rounds on the selected package (trace `.aris/traces/research-refine/2026-08-23_run01/`, thread `01a02b0b-40c2-7c60-8526-1ce3cf8263a0`). Scores 6.7 → 7.6 → 7.2 → 7.1 (RETHINK) → **7.6 REVISE (final, MAX_ROUNDS)**. The decisive event was the reviewer-requested **zero-GPU support audit** (`refine-logs/SUPPORT_AUDIT.md`): under the refinement's (too strict) full-cell criterion the clean placebo — training on histograms re-assigned among artifacts with the same point label and rating sum — looked unsupported on commit messages, and the proposal was reframed from "attribution audit" to **identifiability audit**. The external review's round 2 then corrected the support notion (randomised maximum-cardinality matching on the hash-grouped split): the intervention can change .25–.32 (commit What), **.33–.37 (commit Why)**, .47–.59 (readability) of training artifacts and 0 with two target raters, so the final design is a **feasibility result + scoped audit** with exact commit-Why as the primary experiment.

- **Proposal**: `refine-logs/FINAL_PROPOSAL.md` — *"Can Small Annotator Panels Tell Whether Soft-Label LLM Judges Learn Disagreement? An Identifiability Audit of Distributional Judge Training in SE."* Thesis: the exact mode-, mean- and pool-preserving target-link randomisation has limited but non-zero finite-sample intensity on released SE panels; we state this feasibility result with MDE/power, and estimate — with symmetric calibration, excluded rater identities, a matched no-adversary control and explicit intensities — the Chen-package gain Δ_soft, the adversarial-term effect Δ_adv and the exact Δ_link^ITT(G) on commit Why (primary), commit What and readability, per family, reading what they license from a results-conditioned claim matrix. Dominant contribution: the estimand Δ_link^ITT(G) with a randomised maximum matching, three support quantities + dose, a frozen out-of-sample-validated support model, the two-rater lemma and MDE guidance.
- **Experiment plan**: `refine-logs/EXPERIMENT_PLAN.md` — Block 0 (CPU, primary evidence: support certificates, frozen support model, lemma, MDE), Block 1 (commit, 4 arms incl. no-adversary control, 288 runs), Block 2 (protocol comparison, scoring only), Block 3 (summarization, analytic boundary), Block 4 (readability, 162 runs), Block 5 (sensitivity); 450 LoRA runs ≈ 146 GPU-h, stage-gated on M0 (correctness/power) and the M1 exact commit-Why gate (24 runs ≈ 11 GPU-h; parity / invariants / MDE, never effect direction).
- **Tracker**: `refine-logs/EXPERIMENT_TRACKER.md`; review history `refine-logs/REVIEW_SUMMARY.md`, `refine-logs/REFINEMENT_REPORT.md`; one-page `refine-logs/PIPELINE_SUMMARY.md`.
- **Remaining weaknesses (both reviewers)**: the frozen support model may not validate out of sample (then C1 is an empirical audit — pseudo-novelty risk); Δ_link may be under-powered at ≈ one-third intensity (MDE first); Chen parity with the released code is unverified; the readability dataset must be fixed upstream and is tiny; the pilot rests on one model / one seed / 120 independent diffs and its numbers are hypotheses for the final protocol, not conclusions.

## Next Steps

- [x] **Parent paper's readability alignment bug** (`code_readability/scripts/*.py` nearest-mean join, 18.5 % correct): decision 2026-08-23 — paper already submitted, fix deferred to rebuttal / camera-ready; the follow-up uses its own direct-key loader (tracker R001). Memory note `readability-alignment-bug`.
- [ ] M0 (CPU, ~1.5 weeks): freeze and validate the support model; MDE/power simulation; release the support certificates (`idea-stage/pilot/support_audit.py`) with subsampled-rater curves; lock the 124-snippet readability universe; parity-test Chen's exact objective (+ no-adversary variant) against the released code; add harness unit tests.
- [x] M1 (GPU, 24 runs, 7.4 GPU-h) — **gate PASS** (2026-08-23): Why, split 0, Qwen; Δ_link^ITT = −0.0000 [−0.0006, +0.0005] at intensity .34; Δ_soft = +0.0008 [−0.0006, +0.0021]; Δ_adv = −0.0001; achieved MDE ≈ .0008 (ITT) — details in `refine-logs/EXPERIMENT_PLAN.md` § M1 gate result.
- [x] M2a — Why replicated on 3 outer splits (Qwen): pooled Δ_soft +0.0027 [+0.0015, +0.0039], Δ_adv +0.0001, **Δ_link^ITT −0.0001 [−0.0004, +0.0002]** at intensity ≈ .32 → the Chen-package gain is soft-target regularisation, not item-linked histogram information (details: `refine-logs/EXPERIMENT_PLAN.md` § M2a result).
- [x] M2b-1 — What replicated on 3 outer splits (Qwen): pooled Δ_soft +0.0013 [+0.0008, +0.0019] (split-heterogeneous), Δ_adv ≈ 0, Δ_link^ITT −0.0001 [−0.0003, +0.0001] — the Why null replicates on the second criterion.
- [x] M2b-2 — DeepSeek-Coder-6.7B complete: the commit matrix (2 criteria × 2 families × 3 splits) is done — **Δ_soft positive in all four cells (+0.0013 … +0.0036 RPS), Δ_adv ≈ 0 in all four, Δ_link^ITT ≈ 0 in all four** (one chance-consistent cell at +0.0008); details in `refine-logs/EXPERIMENT_PLAN.md`.
- [x] M3 — readability complete (108 runs). **Final six-cell matrix (pooled, RPS):** commit Δ_soft positive in all four cells (+0.0013 … +0.0036), readability Δ_soft −0.0008 [−0.0017, −0.0000]; Δ_adv ≈ 0 (readability +0.0006 the trivial exception); **Δ_link^ITT ≈ 0 in every cell — including the .55-intensity readability cell** (−0.0002 [−0.0004, −0.0000]). Results-conditioned claim: soft-label gains on these panels are soft-target regularisation, not item-linked disagreement information; full matrix + licensing in `refine-logs/EXPERIMENT_PLAN.md`.
- [ ] M2–M4 per `refine-logs/EXPERIMENT_TRACKER.md`; then `/auto-review-loop` on the draft.
- [ ] Backup paper (Package B): offline best-of-n on the fully rated 6-candidate summary pools + noise-vs-signal DPO — no training needed for the first half.
- [ ] Or invoke `/research-pipeline` for the complete end-to-end flow.

<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:START -->
## Evidence Gate
**Status:** PASS

All required stage records, review receipts, artifacts, and report sections are present.
<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:END -->
