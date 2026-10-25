# NOVELTY DOSSIER — cross-model verification (read fully; answer the questions at the end)

You are an independent senior reviewer (NeurIPS/ICLR/ACL + ICSE/FSE). Judge the novelty of the proposed follow-up work below, brutally honestly. Do not run commands except reading files named here.

## Parent paper (ICSE 2027 submission, ours)
"LLMs are Bad Judges? The Illusion of Alignment in SE": pooled-label judge validation hides annotator disagreement; CSJE protocol (consensus strata + matched held-out-human reference) and HCA metric. Three multi-rater SE benchmarks (code summarization 3 raters; commit messages 6 raters; readability 9 raters).

## Proposed follow-up (Package A as revised after pilots): "Learning disagreement or learning smoothing? A training-time evaluation contract for distributional LLM judges on small annotator panels"
Components and claims:
- (K1) **Learnability ceiling before training**: split-half reliability of *per-item dispersion* across disjoint rater halves (Spearman–Brown corrected) as the upper bound on any judge's ability to predict which items are contested; plus a *location-controlled* disagreement metric (entropy→Low AUROC within predicted-level bins / residualised on predicted level), because on bounded ordinal scales the Low stratum is strongly predictable from scale location alone.
- (K2) **Attribution protocol for trained distributional judges**: every judge (point-SFT to pooled median; KL/soft-label to the empirical histogram à la Chen et al. NeurIPS 2025) is scored against each *held-out individual rater* (leave-one-rater-out) with the ranked probability score by consensus stratum; item-independent nulls (cross-fitted global temperature + criterion-marginal mixture on the point judge; location-conditional human pmf; climatology) and a *median-matched histogram-permutation placebo* (preserves the label and the marginal dispersion, destroys the artifact–dispersion link); report the **smoothing share** = (gain reproduced by the item-independent null)/(total gain) and the true-vs-permuted gap.
- (K3) **Distributional skill score** anchored at climatology (=0) and the (k−1)-rater panel predictive (=1) — the distributional analogue of HCA.
- (K4) **Small-panel ordinal target**: Dirichlet-multinomial posterior-predictive target with *empirical-Bayes* concentration (fit by leave-one-rater-out marginal likelihood on training items; shrinkage ∝ 1/k) trained with a bounded ordinal proper score (RPS/CRPS); hypothesis that Chen et al.'s adversarial ε-ball is a small-k artefact. (Pilot pending.)
- (K5) **Operational consequence**: whether the judge's predicted distribution improves a human-routing decision scored against a matched held-out rater (gain-first vs entropy-first routing).

## Pilot evidence so far (commit-message benchmark, 6 raters, Qwen2.5-Coder-7B LoRA, 240 test items, leave-one-rater-out)
# CPU diagnostics (2026-08-23) — split-half reliability of per-item disagreement & location-only null
| panel | split-half r of per-item std (SB-corrected) | location-only AUROC for Low (|median−centre|) | half-panel std → other-half Low AUROC |
|---|---|---|---|
| CM What (800, 6 raters) | +0.22 (0.36) | 0.67 | 0.61 |
| CM Why (800) | +0.36 (0.53) | 0.80 | 0.65 |
| Readability (200, 9 raters) | +0.02 (0.04) | 0.64 | 0.60 |
| CS (3 raters) | n/a (1-vs-2 mechanically confounded) | CA 0.65/0.73, Conc 0.89/0.82, Flu 0.82/0.71 (Java/Python) | — |
Reading: item-level disagreement is a real but moderate item property on commit messages (Why > What); on readability it is essentially NOT an item property (r≈0.02) → unlearnable by any judge. The Low stratum is strongly predictable from scale LOCATION alone (floor/ceiling items are mechanically peaked), more so than from the other half-panel's dispersion → any "entropy predicts disagreement" claim must beat this location null.
# Zero-shot Qwen2.5-Coder-7B on CM test split (240 items): What HCA High .77 / Partial .89 / Low 1.17 (Δmatch −.24 = mirage shape); Why overall HCA .12, High −.49 (floor effect: model predicts 2–3 where humans give 0), entropy→Low AUROC .55.
# Location-controlled entropy test, zero-shot Qwen2.5-Coder-7B, CM test split (240 items)
| crit | entropy→Low AUROC raw | human-location null | entropy within predicted-level bins | entropy residual (level-adjusted) | Spearman(entropy, human std) |
|---|---|---|---|---|---|
| What | 0.615 | 0.610 | 0.594 | 0.590 | +0.21 |
| Why | 0.551 | 0.732 | 0.499 | 0.500 | +0.13 |
Reading: the untrained judge's uncertainty carries at most weak (What) or zero (Why) item-level disagreement information once scale location is controlled; entropy is dominated by predicted level (ρ=−0.63 with |level−2| on What). Any routing-by-entropy scheme on these data would be routing by location.
# Pilot A partial (zero-shot / ce_median / kl_soft(+½CE); 240 test items; held-out-rater RPS normalised, strata from other 5 raters)
What: RPS zero-shot .114 | ce_median .103 | kl_soft .098 | N1 temp+mix(ce) .098 | N2 loc-cond .106 | climatology .159 | 5-rater panel .095. Δ(ce−kl)=+.0041 [.0023,.0059]; Δ(ce−N1)=+.0042 [.0023,.0062]; Δ(N1−kl)=−.0001 [−.0013,+.0012]; Low: −.0002 [−.0021,+.0018]; smoothing share 1.02. ent→Low AUROC level-adjusted: ce .616, kl .640. skill: ce .879, kl .943, N1 .945.
Why: RPS zero-shot .322 | ce .123 | kl .112 | N1 .109 | N2 .133 | clim .175 | panel .100. Δ(ce−kl)=+.0112 [.0086,.0140]; Δ(ce−N1)=+.0139 [.0090,.0188]; Δ(N1−kl)=−.0027 [−.0051,−.0001] (KL WORSE than smoother); Low: −.0076 [−.0113,−.0039]; smoothing share 1.24. ent→Low level-adjusted: ce .765, kl .762. skill: ce .700, kl .850, N1 .886.
Pre-registered verdict: SMOOTHING EXPLANATION SUCCEEDS (≥70% reproduced; item-specific residual ≈ 0 or negative). Mirage shape persists after training on What (Low HCA 1.22, Δmatch −.42/−.45).
# Pilot C on trained judges (ce_median, kl_soft): gain-head AUROC(g>0) .53–.67 vs entropy-first .56–.77 (entropy better on Why); 20% budget ΔMAE(gain−entropy) +.013 [−.009,+.039] (ce What), +.013 [−.010,+.035] (ce Why), +.014 [−.014,+.041] (kl What), −.000 (kl Why); 50%: +.034 [+.002,+.064] (kl What) only marginal. Oracle headroom large (.55→.47, .61→.51). Judge-only MAE (.55) < human-only (.63) on What after training. VERDICT: FAIL pre-registered criteria; entropy routing is not "backwards" here.


## Closest prior work — full-text details of the three main competitors
# Full-text details of the three closest competitors (fetched 2026-08-23)
## Chen et al. 2025, Distributional LLM-as-a-Judge (NeurIPS 2025, 2505.12301)
- Loss: L = α·KL(p_human || q_θ over score tokens) + (1−α)·CE to majority label; adversarial inner max over p' in simplex ∩ ℓ2-ball(ε*) around empirical p.
- Data: SNLI/MNLI (5 raters, 3-way), SummEval (1–5 Likert, experts+crowd), MT-Bench (A/Tie/B, ≥1 rater). No code/SE data.
- Models: Qwen2.5-7B, LLaMA3.1-8B fine-tuned; GPT-4o(-mini) untuned.
- Eval: KL to the SAME pooled empirical distribution + accuracy vs majority; 8:2 split; NO held-out annotator, NO leave-one-annotator-out, NO agreement stratification.
- Numbers: MNLI KL 0.74(SFT)→0.23, acc 89.2→89.0; SummEval KL 0.74→0.52, acc 45.8→46.6.
- No ordinal/EMD/CRPS loss, no annotator identity, no disagreement prediction.
## Li et al. 2025, Judging with Confidence (2510.00263)
- SFT: MLE on sequences containing verbalised probability targets; RL: GRPO with Brier / clipped log proper-scoring reward. Pairwise binary only.
- Data: JudgeLM prompts; annotations from Gemini-2.5-Flash persona sampling (synthetic "annotators"), 10 per item. Models: Gemma-2-9B, Qwen2.5-7B full FT.
- Eval: ECE, Brier, MSE vs population mean; no per-annotator, no agreement strata; OOD on PandaLM/JudgeBench. No ordinal, no SE.
## Zhang et al. 2024/ICML 2025, Diverging Preferences (2410.14632)
- RMs: Mean-Var RM (μ, σ², KL over tie/slight/significant labels), 5-way Likert classification RM (KL) on HelpSteer2 (12K pairs, 3–5 raters, 1–5 Likert) and MultiPref (10K pairs, 4 raters).
- Findings: BT RMs give P(chosen>rejected)≈0.84 on diverging AND high-agreement pairs; LLM-judge decisiveness 73.8% vs 73.1%; comply-vs-refuse bias 68%.
- Eval: 500 held-out examples stratified High-Agreement Prefs / Ties / Diverging (All/Substantial); Preference accuracy + Diverging-ID AUROC. NO held-out annotator reference. No downstream policy/BoN. No code/SE.


## Novelty searches (three independent multi-source scouts; all arXiv IDs verified by retrieval)
# Novelty search A — "learned disagreement vs learned smoothing" (contradiction#1). 10 arxiv queries, 18 web, 23 abs fetches; all IDs verified.
| # | Title | First author, year | Venue | arXiv | Claims | Overlap | Key difference |
|---|---|---|---|---|---|---|---|
| NA1 | Same Target, Different Basins: Hard vs Soft Labels for Annotator Distributions | Gheibi 2026-05 | EIML@ICML 2026 | 2605.20642 | C1 | "Shuffled SLS": global permutation of annotator dists, preserves marginal disagreement; label-smoothing & majority baselines | CIFAR-10H categorical; global shuffle also destroys the label (sanity check, not attribution); no median-matched permutation, no gain-share, no held-out annotators, no temperature null |
| NA2 | Metric-Dependent Annotation Saturation for Learning from Label Distributions | Kohli 2026-05 | arXiv cs.CL | 2605.29797 | C3,C2,C5 | soft labels vs 5 label-smoothing α on per-item entropy correlation (r .643 vs .45–.49); 80/20 annotator split; TS fairness control; annotator-count saturation curves | categorical NLI, DeBERTa; held-out annotator GROUP not individual LORO; no permutation placebo, no smoothing share, no split-half ceiling, no location confound. MOST LIKELY "already shown" citation |
| NA3 | Temperature Scaling Is Not Enough: Calibration Gaps Under Human Label Distributions | Dogah 2026-07 | arXiv | 2607.13423 | C3 | TS on hard labels vs oracle soft-fit gap | post-hoc only; supports our framing |
| NA4 | Confidence Calibration under Ambiguous Ground Truth | Tao 2026-03 | arXiv cs.LG | 2603.22879 | C3 | TS underestimates annotator uncertainty; Dirichlet-Soft / MC-TS / LS-TS calibrators | their methods ≈ our nulls, used as solutions; no judges/ordinal/held-out rater |
| NA5 | Human vs Model Uncertainty in Soft-Label Learning and Calibration | Pavlovic 2026-05 | arXiv | 2605.18648 | C3 | soft labels mainly a regularizer | MNIST only |
| NA6 | LLMs Capture Emotion Labels, Not Emotion Uncertainty | Inoshita 2026-04 | arXiv | 2604.27345 | C2,C4 | entropy correspondence; calibration reduces JSD | hard-label FT; no location control |
| NA7 | Semantic Entropy as a Signal for Human-AI Disagreement (AI grading) | Iyer 2025-08 | arXiv | 2508.04105 | C4 | rationale semantic entropy predicts rater disagreement, AUROC .82 (ASAP ordinal) | no score-location control; no FT |
| NA8 | The Alternative Annotator Test for LLM-as-a-Judge | Calderon 2025 | ACL 2025 | 2501.10970 | C2 | leave-one-annotator-out comparison of LLM vs excluded human | point judges, no FT, no distributions |
| NA9 | Seeing the Big through the Small: LLM-approximated human judgment distributions (NLI) | Chen 2024 | EMNLP-F 2024 | 2406.17600 | C2,C3 | instance-level vs global-shape distances | no nulls/attribution |
| NA10 | DPRM | Li 2024 | arXiv | 2402.09764 | C2 | OT loss to population pref dist | population-level |
| NA11 | Pairwise Calibrated Rewards | Halpern 2025 | arXiv | 2506.06298 | C2 | ensemble share matches annotator fraction | no item-specific vs marginal test |
| NA12 | Variance-aware RM with Anchor Guidance | Fang 2026-05 | arXiv | 2605.11865 | C2 | per-item mean+variance RM | no held-out rater, no nulls |
Also: Ni 2506.19467; Inoshita cSG-MCMC 2605.24773; Opt-ICL 2510.07105; CAPO 2605.28802; Ehara 2605.12422; Xu&Jurgens 2601.09065; Z-Reward 2606.09076.
## Per-claim: C1 permuted placebo MEDIUM (NA1 has global shuffle; median-matched + smoothing share not done; none on judges/ordinal) · C2 held-out individual rater for distributional judges MED-HIGH (Alt-Test = point judges; NA2 = held-out group) · C3 "soft labels = smoothing" MEDIUM (crowded qualitatively; no quantitative decomposition of FT gains, none ordinal) · C4 location confound HIGH · C5 split-half dispersion ceiling HIGH.
## Already-done risk: none single; NA2+NA1 combination → reviewer frames as "NA2 re-run on SE Likert with fancier permutation". Defence: NA1 global shuffle destroys label; NA2/3/4 compare methods, no smoothing share; ordinal scales make C4/C5 load-bearing; individual-rater CRPS stricter. Lead with C4+C5+attribution share. Secondary risk: Chen 2505.12301 already trains distributional judges → position as "does the gain mean what it claims".
## Last 6 months: 2603.22879, 2604.27345, 2605.01168, 2605.11865, 2605.18648, 2605.20642, 2605.24773, 2605.28802, 2605.29797, 2607.08493, 2607.13423. Nothing Jun–Aug closes the gap further.


# Novelty search B — small-panel posterior-predictive target (method-transfer#1). 12 arxiv queries, 16 web, ~20 fetches; all IDs verified.
| # | Title | First author, year | Venue | arXiv | Claims | Overlap | Key difference |
|---|---|---|---|---|---|---|---|
| NB1 | Metric-Dependent Annotation Saturation for Learning from Label Distributions | Kohli 2026-05-28 | arXiv | 2605.29797 | C2,C5 | DIRECT HIT on mechanism: ChaosNLI subsampled to N∈{3,5,10,100}; symmetric Dirichlet-multinomial posterior mean (α∈{1/K,.5,1}) as target; at N=10 α=1/K closes 99% of KL gap; heavier priors hurt at small N | fixed α (no EB); nominal NLI; DeBERTa; no RPS; eval vs N=100 histogram not held-out rater; no skill score |
| NB2 | Crowd-Informed Machine Annotation (Dirichlet posteriors as objective) | Klugmann 2024 | arXiv cs.HC | 2409.00048 | C2,C3 | CNN predicts Dirichlet posterior over soft labels from 5–20 crowd labels; motivated by fewer labelers | uniform prior fixed; Bhattacharyya loss; vision; no held-out rater |
| NB3 | Same Target, Different Basins | Gheibi 2026-05 | arXiv | 2605.20642 | C5 | few votes → soft-CE to sparse histogram worse than hard-label delivery | fix is label delivery not shrinkage |
| NB4 | How many labelers do you have? | Cheng, Asi & Duchi 2022/24 | arXiv math.ST | 2206.12041 | C5 | theory: calibration needs raw per-labeler labels; labeler-count trade-offs | pure theory |
| NB5 | OPRM: Learning Ordinal Probabilistic Reward from Preferences | Chen 2026 | ICLR 2026 | 2602.12660 | C1 | RM outputs distribution over ordinal ratings; Region Flooding Tuning | from preference pairs, no histograms, no RPS |
| NB6 | Reward Modeling with Ordinal Feedback: Wisdom of the Crowd | Liu 2025 | ICML 2025 | 2411.12843 | C1 | ordinal pairwise feedback as crowd preference probability | pairwise; BT NLL |
| NB7 | Beyond Binary Preferences: RM with Ordinal Feedback | Afsharrad 2026-02 | arXiv | 2603.02232 | C1 | cumulative-link ordinal RM | single-label targets |
| NB8 | Alternative Annotator Test | Calderon 2025 | ACL 2025 | 2501.10970 | C3,C4 | leave-one-annotator-out LLM vs excluded human | hard-label test; no distributional score/skill |
| NB9 | Diagnosing LLM-as-a-Judge via IRT | Choi 2026 | arXiv | 2602.00521 | C4 | graded-response IRT; Wasserstein LLM vs human dists | diagnostic only |
| NB10 | Training and Evaluating with Human Label Variation | Kurniawan 2025 | Computational Linguistics | 2502.01891 | C4,C5 | 14 HLV methods × 6 metrics × 6 datasets | no shrunk target, no RPS, no panel sweep |
| NB11 | Do We Still Need Humans in the Loop? | Hakimi 2026-04 | arXiv | 2604.13899 | C2,C3 | evaluates vs Beta-Binomial / Dawid-Skene posteriors with 3–6 annotators | evaluation-side, binary |
| NB12 | DPUA: Aligning LLM Uncertainty with Human Disagreement | Lu 2026-05 | arXiv | 2605.10415 | C1 | GRPO reward: expressed confidence matches disagreement dists | nominal; not proper ordinal score |
Also: 2605.24773; 2607.08493; 2604.27345; 2605.13801 (bootstrap of annotator behaviour, items-vs-responses trade-off); 2212.09409 (Wright & Augenstein aggregators); 2202.02950; 2507.00736 (balanced DRPS metric); 2606.24959 (RPS nonconformity ordinal CP); Rizzi NLPerspectives 2024.
## Per-claim: C1 RPS/CRPS training of LLM judges to Likert histograms MEDIUM (ingredients in print; "swap KL for RPS" reads as ablation unless small-k/propriety is headline) · C2 Dirichlet/EB shrinkage LOW–MED (Kohli, Klugmann) · C3 posterior-predictive / next-rater framing MEDIUM · C4 climatology/panel-anchored distributional skill score HIGH (metric; incremental vs our own HCA) · C5 panel-size effects LOW–MED (ε-ball-is-small-k-artefact unclaimed).
## Already-done: if abstract leads with "Bayesian shrinkage fixes small-panel soft targets" → scooped by Kohli (May 28 2026) + Klugmann 2024. Not found: LLM judge trained with RPS/CRPS to EB-smoothed ordinal target; soft-label judges evaluated vs held-out individual rater with climatology-anchored skill. Defensible = conjunction, positioned against NB1/NB2. Dense May-2026 cluster; timing matters.


# Novelty search C — "route by matched-human gain" (training-signal#3). 6 arxiv queries, 19 web, 30 fetches; all IDs verified.
| # | Title | First author, year | Venue | arXiv | Claims | Overlap | Key difference |
|---|---|---|---|---|---|---|---|
| NC1 | Flexible Routing via Uncertainty Decomposition | Peale 2026-05 | arXiv cs.LG | 2605.07805 | C2,C3 | CLOSEST: reducible vs irreducible uncertainty from multi-annotation calibration set; route to oracle when reducible high, abstain when irreducible high; baselines: total-uncertainty routing, supervised XGBoost router predicting reducible loss, oracle | oracle = noise-free Bayes conditional (mean of 47 CIFAR-10H labels), classification (CIFAR-10H, SNLI, ChaosNLI); no single noisy human target, no judge features, no SE, no MAE/CRPS |
| NC2 | HyPER: Learning to Route Instances for Human vs AI Feedback | Miranda 2024 | arXiv | 2410.19133 | C2 | per-instance gain Δ = PPM(v_n)−PPM(v_0); route to humans if Δ>0 | gain = downstream RM accuracy, not agreement with a human; tag features |
| NC3 | Trust or Escalate | Jung 2024 | ICLR 2025 | 2407.18370 | C1,C3 | selective eval w/ human-agreement guarantee, confidence routing | target = majority; routes by confidence |
| NC4 | AURA: Adaptive Uncertainty-aware Refinement for LLM-as-a-Judge Auditing | Zhang 2026-06 | arXiv stat.ML | 2606.19714 | C2,C3 | prioritises uncertain comparisons for human review | pure uncertainty prioritisation, pairwise |
| NC5 | Augmenting Human Evaluation with LLM Judges: How Many Human Reviews? | Kim 2026-05 | arXiv cs.LG | 2605.16354 | C4,C1 | two-stage design, doubly-robust estimator; more human ratings where LLM predictability low; per-rater partially observed | design-level, population estimate target |
| NC6 | LECODU: Learning to Complement and Defer to Multiple Users | Zhang 2024 | ECCV 2024 | 2407.07003 | C5 | L2D w/ noisy users, optimal number of users per instance | latent true label target |
| NC7 | CL2DC: coverage-constrained cooperation with multiple experts | Zhang 2024 | arXiv | 2411.11976 | C5 | trains from noisy annotations w/o clean labels | latent correct label |
| NC8 | Learning to Defer to a Population | Tailor 2024 | AISTATS 2024 | 2403.02683 | C5 | defer to unseen experts via meta-learning | accuracy target |
| NC9 | EA-L2D: Identity-Free Deferral for Unseen Experts | Strong 2025 | ICLR 2026 | 2502.10533 | C5 | Bayesian competence profiles | classification |
| NC10 | To Ask or Not to Ask: Learning to Require Human Feedback | Pugnana 2025 | arXiv | 2510.08314 | C2 | optimal when-to-query strategy | ground-truth loss target |
| NC11 | Venire | Koshy 2024 | arXiv cs.HC | 2410.23448 | C3 | predicts moderator disagreement → escalates contested | the opposite policy; baseline to beat |
| NC12 | Collaborative Content Moderation w/ conformalized disagreement | Villate-Castillo 2024 | Neurocomputing 2025 | 2411.04090 | C3,C5 | disagreement prediction triggers human review | majority target, no Pareto |
Also: alt-test 2501.10970; Ask-a-Strong-Judge 2510.20369 (NeurIPS 2025); multi-expert L2D 2210.16955, 2310.14774, 2602.17144, 2509.12573, 2510.26706, 2510.19351; SANT 2405.12081; Gruber 2507.02593; Lu 2605.10415; Stopping and Routing LLM Judge Panels 2608.19802 (Aug 2026, routes among judges by validation gain); Share the Judge 2607.27984; When to Screen 2603.13870; Metric Match 2606.15029; SE judge audits 2502.06193 / 2604.16790.
## Per-claim: C1 held-out individual rater as routing target HIGH (for routing; alt-test framing exists) · C2 learned expected-gain head MED-LOW (HyPER, Peale's XGBoost router, Pugnana) · C3 "uncertainty routing sends the wrong items" MED-LOW (Peale states/demonstrates it) · C4 SE hybrid Pareto MED-HIGH · C5 L2D with disagreement LOW-MED (crowded).
## Already-done risk: Peale 2605.07805 is the paper to worry about (same conceptual pivot; noise-free oracle, classification, no judge, no SE). Survives only if led by the matched-NOISY-human target (g_i can be negative on contested items) with Peale as direct baseline. Combination (judge features + gain head + matched rater + Likert + SE + strata) is open but an instantiation novelty. Vocabulary converging (2608.19802) → submit soon.


## Questions (answer each explicitly, in markdown)
1. For each component K1–K5: is it novel? Name the single closest prior work and state the delta in one sentence. Rate HIGH / MEDIUM / LOW.
2. Overall: what is the closest prior work to the *package* and what is the delta? Would a reviewer say "already done"? Which paper(s) would they cite?
3. Given the pilot evidence (Chen-style KL gains fully reproduced by an item-independent smoother; gain-routing not beating entropy), what is the strongest *honest* framing of the contribution, and which components should be dropped, merged, or repositioned (e.g. the negative result as the headline; K4 conditional on Pilot B; K5 as appendix)?
4. Output the structured block:
```
## Novelty Check Report
### Proposed Method
### Core Claims  (K1..K5 — Novelty: HIGH/MEDIUM/LOW — Closest: [paper])
### Closest Prior Work  | Paper | Year | Venue | Overlap | Key Difference |
### Overall Novelty Assessment  - Score: X/10  - Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON  - Key differentiator  - Risk
### Suggested Positioning
```
