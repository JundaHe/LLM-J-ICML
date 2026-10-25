# Idea-generation bundle (read fully, then follow the instructions at the end)

You are a senior ML/SE researcher brainstorming *training-side* follow-up research ideas for the paper below. You are GPT-5.6; the executor is Claude. Think hard, be concrete, be honest.

## The paper we are following up (ICSE 2027 submission)
Abstract: Large Language Models (LLMs) are increasingly used to judge software engineering (SE) artifacts, but the standard protocol scores a judge against a single pooled human label, even though annotators often disagree on what a good artifact looks like. Prior SE judge validations stop at this single pooled score; running the analysis they omit, we find that the pooled-label protocol can misrepresent how good an LLM judge really is: it hides the human uncertainty in a benchmark, and, by scoring the judge against a denoised aggregate of all raters while scoring each human against a single peer, it can make judges look strongest exactly where humans disagree most, the alignment mirage first noted in NLP. Our goal is not to establish that this mirage exists, but to ask how good SE judges are once they are evaluated fairly, on the same footing as a human. To this end, we propose \textbf{Consensus-Sensitive Judge Evaluation (CSJE)}, a protocol that stratifies items by human agreement and scores each judge against a matched held-out human rather than the pooled label, and we trace the mirage to two measurement confounds in the standard protocol, aggregation and selection, rather than to judge behavior. Re-analyzing three released multi-annotator SE benchmarks (code summarization, commit message generation, and code readability) under CSJE, we find that the released best judges are reliable mainly on high-consensus items; on contested items we detect no advantage over a matched held-out human, and even a shortfall on clear ones. Scaling to three 2026 state-of-the-art judges (Claude Opus~4.8, Gemini~3.1~Pro, and GPT-5.5) and two multi-agent methods (CodeVisionary and SE-Jury) does not change this picture. We also introduce Human-Ceiling Agreement (HCA), an uncertainty-robust metric anchored at a held-out human ($1$) and a random labeler ($0$) that summarizes judge quality without collapsing human disagreement. SE judge evaluations should therefore report performance separately by level of human agreement, against a matched human reference rather than a single aggregate.

Summary of findings (from the Discussion section):
Discussion}sec:discussion}

Summary of Empirical Findings}

F1: Human uncertainty is not uniform across SE tasks.}
The three benchmarks occupy three regimes: code summarization is a reliable core with a small contested tail; commit-message evaluation carries a contested mass (roughly half the developer-pool Why} items are Low-consensus); and readability stays broadly low-agreement even under nine raters.

F2: The contested-item ``advantage'' is an artifact of scoring, not judging.}
The cause is asymmetric scoring: each human is measured against another raw rater, the judge against a pooled median that has already averaged rater noise away. On the commit-message Why} stratum, GPT-4's apparent Low-consensus edge all but vanishes once a held-out human is scored in the same leave-one-out position. Agreement above inter-annotator agreement is thus not better judging, only a cleaner target.

F3: The mirage can be produced without an LLM.}
In the three-rater code-summarization panel, a held-out human pushed through the identical pipeline reproduces almost the same large negative Low-stratum gap. The mirage is a protocol failure before it is a model property.

F4: Scaling the judge does not repair the measurement.}
Our frontier and multi-agent runs confirm this: the 2026 models leave the high-consensus shortfall intact while keeping the Low-consensus ``wins'' pooled-label scoring hands them for free, and multi-agent methods behave no differently.

F5: Aggregate leaderboards can be compositional artifacts.}
Readability shows it purely: the frontier judges produce no significant within-stratum mirage, yet their pooled scores still exceed human--human agreement. HCA agrees from the other side: when $S$ is small, it withholds a ranking rather than promote one the data cannot support.

Implications for SE Judge Evaluation}

Report the consensus landscape before the judge score.}
Lead not with a pooled agreement coefficient but with how items divide across High-, Partial-, and Low-consensus regimes and human-human agreement within each; the conclusion should survive an alternative cutoff or continuous sensitivity sweep, so it rests on data, not the binning rule.

Calibrate pooled-label agreement with a matched human reference.}
Pair the judge's $\alpha_{H-L}}$ with the held-out-human reference $\alpha_{ref}}$ to obtain the within-stratum diagnostic $\Delta_{\alpha}^{match}} = \alpha_{ref}} - \alpha_{H-L}}$, and treat the raw gap only as a warning sign. A three-rater panel requires the constant-quality null, whereas a larger one admits a split-panel control.

Use HCA as a calibrated summary, not a replacement for strata.}
Read HCA together with $S$ and its bootstrap CI: a small $S$ warrants an unresolved cluster rather than a ranking, and an HCA above $1$ marks a judge nearer consensus than a typical rater, not literal super-human performance.

Make claims by uncertainty regime.}
High-consensus items are reasonable targets for scalable LLM judging, whereas low-consensus items should be escalated to human review or reported separately. This also warns against tuning to the aggregate-best score, since that rewards a judge for tracking the median while it fails the cases that most need judgment.

Release annotator-level ratings.}
Publish the annotator-level matrix alongside the aggregation rule, strata, matched-human reference, HCA, discriminative power, and CIs, since no diagnostic survives collapse to a majority, mean, or median.


## Data, compute and constraints on hand
- Per-annotator Likert ratings (released benchmarks, already loaded + stratified in our code): code summarization (Crupi et al.: 1,163 items × 3 raters, 1–5, three criteria: content adequacy / conciseness / fluency; Java+Python), commit messages (Zeng et al.: 800 messages = 400 developer + 400 generated, × 6 raters, 0–4, criteria What/Why; diffs available), code readability (Scalabrino/CoReEval: 200 snippets × 9 raters, 1–5; low discriminative power S=0.14).
- Existing judge outputs: released judges (GPT-4-turbo, GPT-4, QwQ-32B, Llama-3.3-70B, Qwen2.5-72B, Mistral Large, …) and our 2026 frontier runs (Claude Opus 4.8, Gemini 3.1 Pro, GPT-5.5, 3 runs each) + CodeVisionary / SE-Jury multi-agent runs.
- Evaluation harness already implemented: consensus strata (High/Partial/Low), held-out-human reference α_ref, Δ_match, HCA with bootstrap CIs, plus distributional metrics (CRPS vs empirical rater pmf, held-out-rater NLL, entropy→Low-stratum AUROC).
- Compute: 4× RTX 6000 Ada (48 GB, but ~22 GB free each; shared machine), local Qwen2.5-Coder-7B-Instruct and Qwen3-14B (cached), conda env with torch 2.11 / transformers 5.12 / peft / trl 1.6 / vllm. A 7B judge scores 800 items in ~10 min; LoRA fine-tuning of a 7B at ~1k tokens fits. OpenRouter API for frontier models (small budget). Single PhD student; target venues ICSE/FSE/TSE or NeurIPS/ICLR/ACL.
- Smoke test: Qwen2.5-Coder-7B's next-token distribution over score tokens (0–4) is informative out of the box (e.g. item with humans [2,1,2,1,2,1] → p=[.05,.55,.38,.02,.00]).

## Literature landscape and gaps (from our three literature scouts; all arXiv IDs verified)
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



## Instructions
Generate 10–12 concrete research ideas that build on the paper's *measurement* contribution with a *training/post-training* contribution (judge fine-tuning, reward modelling, calibration training, RL judges, or downstream preference optimisation). For EACH idea give:
1. One-sentence summary
2. Core hypothesis (what you expect to find and why — what mechanism)
3. Minimum viable experiment on the data/compute above (concrete: which benchmark, which base model, which objective, which comparison, which metric; estimated GPU-hours)
4. Expected contribution type: empirical finding / new method / theoretical result / diagnostic / protocol
5. Risk: LOW / MEDIUM / HIGH
6. Estimated effort: days / weeks / months
7. Closest prior work (from the landscape) and the precise delta — one sentence each
8. A `dedup_key`: a short slug naming the hypothesis

Hard requirements:
- Must NOT be "apply Chen et al. 2025 (2505.12301) distribution-alignment to code". Each idea must differ from Chen 2025, Li 2025, Zhang 2025 (Diverging Preferences), Trust-or-Escalate, Ni 2025, PEBS in a way a reviewer would accept. Exploit the gaps: circular validation, small ordinal panels (3–9 raters), held-out-rater evaluation, ordinal transport losses, annotator conditioning with unseen-rater eval, disagreement-as-output for routing vs a matched human, RL judges with distribution rewards, downstream effects on contested items, SE specificity (what makes SE disagreement different: conciseness-vs-completeness trade-offs, developer vs student raters, What/Why floor effects).
- Prefer ideas where the result is publishable whichever way it goes (e.g. "distributional fine-tuning does/does not beat pooled SFT on the Low stratum under a held-out human" matters either way).
- At least 3 ideas must be runnable as a 1–2 GPU-hour pilot on the commit-message benchmark (richest panel).
- Include at least one idea each on: (a) the training target / loss for small ordinal panels, (b) uncertainty→routing scored against a matched human, (c) downstream DPO/best-of-n consequences, (d) RL / reasoning judges on contested items. Others are free.
- Rank your ideas at the end (1 = you would work on it first) with a one-line reason each.
Do not run any commands; just think and write. Output in markdown.
