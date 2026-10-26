# Paper 2, version 2 — outline with the numbers each section rests on (2026-10-26)

Working title: **Five Raters Are Not a Distribution: What Learned Judges Can Learn from Human Disagreement, and Where to Spend the Annotation Budget**
(alternatives: *Reliable Is Not Learnable*; *Raters for Evaluation, Items for Training*)

## 1. Introduction (the four-beat story)
1. Learned judges are increasingly trained on the full histogram of human ratings (Chen et al. 2025; Singh et al. 2025; Kohli 2026), with the claim that they learn how people disagree.
2. The histogram comes from 3–9 people. We ask two questions no prior work separates: is the histogram's shape beyond its location **reproducible across raters**, and is it **predictable from the text** a judge sees? Reliable ≠ learnable.
3. Findings (one line each): (i) with 3–9 raters the shape is net noise for forecasting a new rater (A1x > 0 on all 8 small ordinal panels; 3 raters: no shape at all); (ii) the reproducible part is not decodable from a frozen LLM representation on 13 ordinal/SE panels (|G| ≤ 6e-5; multi-layer probes identical) but is on ChaosNLI (G +0.0032/+0.0043); (iii) learned judges accordingly ignore the shape (audit: perm − chen ≈ 0; no target construction moves heads by > 0.0005) while using it on ChaosNLI; (iv) a rater–item decomposition shows the ordinal structure beyond location is rater harshness, not an item property; (v) at a fixed budget, judges want items, not raters (heads 11/11; LoRA SummEval 960×1 better than 960×7; POPQUORN items-first at both budgets, with a task-dependent marginal value of a second rating).
4. Contributions: two reliabilities with estimators (split-half ρ; cross-fitted decoding G); reliability cards for 21 panels incl. 5 SE panels; the decomposition; the budget rule validated end-to-end. Companion to paper 1: raters for the test set, items for the training set.

## 2. Measuring disagreement: two reliabilities
- 2.1 Across raters: A1 = M − 2X identity, exact-T comparator, ρ = X/M (FINITE_RATER_PROTOCOL; T9). Table: reliability cards (reports/RELIABILITY_CARDS.md). Figure: ρ vs a on dense panels (ChaosNLI 5–10 raters; BW/DICES/Dorn 20–30; three Dorn languages identical).
- 2.2 Across text: the decoding estimand G = (2⟨r̂,r2⟩ − ‖r̂‖²)/n with group cross-fitting, within-T permutation control, positive control (DECODING_PROTOCOL). Figure: G per panel, ordinal vs nominal; multi-layer re-test.
- 2.3 Prior art to position against: Wong & Paritosh (k-rater reliability), Zhou et al. 2022 (Distributed NLI), Zhang et al. ICML 2025, Wan et al. 2023, Kohli 2026, Gheibi & Ghazizadeh 2026 (PRIOR_ART_CHECK).

## 3. What judges learn (audit, condensed from v1)
- Statistic-preserving donor replacement with dose certificates: heads (T2b) and LoRA (T3b/T3c): mode+mean-preserving ≈ 0, mode-only > 0; ChaosNLI pzc > 0 (T5). Gate H: 11 panels, no construction beyond ±0.0005; hard +0.003–0.010 (results/probe_shrink).
- Reading: the judge learns location + calibration; the shape it cannot see it cannot learn.

## 4. Why: a rater–item decomposition
- Ordered probit M0/M1/M2 on 13 panels (results/rater_item): ΔLL thresholds 0.05–0.16 ≫ dispersion ≤ 0.012; X_obs ≈ 0 on dense ordinal panels; SummEval's small residual unexplained by either and undecodable. Cite MFRM/HRM; present as measurement, not psychology.
- Annotation-side corollary (Gate A table): location smoothing is the gain (shr2 −0.0048; qs −0.0113); the shape coefficient collapses to the location target (shr − qT = 0).

## 5. Spending the annotation budget
- Heads at fixed budget (results/budget_heads): DICES-990 594×1 0.203 < 74×8 0.213; POPQUORN, HelpSteer2, EmoBank, SummEval same direction; small item sets (BW, DICES-350) reverse; ChaosNLI also items-first (registered prediction falsified — reported).
- LoRA SummEval (results/lora_budget/summary.md): 960×1 −0.0061 [−0.0087, −0.0035] vs full data; 144×7 +0.0211; 960×2 = 960×1. LoRA POPQUORN: items-first at both budgets; 819×1 +0.0077 vs full (second rating worth ~half the gap).
- Rule: cover items first; the marginal value of further ratings per item is task-dependent and — we hypothesise, not claim — larger where the shape is text-predictable (ChaosNLI 959×1 → ×2: −15 %).

## 6. Software-engineering panels (application section)
- Dorn (5,468 developers): the SE reliability curve; Crupi/MLCQ/Roy (3 raters): nothing beyond location exists; Scalabrino/BW/JetBrains cards. Implication for SE human studies: 3–5 raters give location only; evaluation sets need 20–30 for shape.

## 7. Limitations, honest list
One base family (Qwen2.5-7B); frozen-feature heads for breadth; linear decoders (multi-layer re-test done; non-linear not); SummEval's unexplained residual; POPQUORN position folds; falsified prediction; effect sizes in the third decimal (state next to the mode-only penalty).

## Appendices
Protocols and amendments verbatim; reliability cards; rater-quality analysis (DICES flagged raters undetectable by agreement; LLM-agreement confounded); prior-art check.

## What is NOT in this paper
Shrinkage as a training method (Gate H); the rater-mixture output head (future); paper 3's calibration results.
