# Finite-rater annotation-side analysis (A/G/B) — protocol, frozen before any result is computed
Committed 2026-10-23 (user go-ahead "那你开始做吧"); follows Codex consults reviews/codex_novelty_boost_2026-10-23.md and _boost2_. CPU only; no model is trained.
Any change after the first result is computed is logged below under "Amendments" with a reason.

## Question
The learned-judge audit found ≈ 0 predictive value of residual shape (beyond mode and mean) on ordinal panels. Is that because
(a) at the observed number of raters the residual shape of an empirical histogram does not predict a NEW rater (an annotation-side, learner-free fact), or
(b) the residual shape is predictive but the judges do not transmit it?

## Notation
Item i has latent rating distribution p_i over K levels; we observe exchangeable ratings (panel columns). For each repetition r (R = 20 seeds) and each item, panel positions are randomly permuted and split into disjoint subsets
P1 (size a: the "training" histogram h1), P2 (held-out ratings used for scoring), and on dense panels P3 (a second independent subset for cross-products).
Scoring: ordinal panels — RPS, S(f, y) = Σ_k (F_f(k) − 1[y ≤ k])² / (K − 1) with C = cumulative operator; nominal panels — Brier score with C = identity.
For any forecast f that does not depend on the held-out ratings, E_y[S(f, y)] = c(p_i) + ‖C(f − p_i)‖² / n (n = K−1 for RPS, 1 for Brier).
T = retained statistics, computed from P1 only: ordinal T = (mode z by the audit's z_label rule, exact mean of the a ratings); nominal T = (modal class z, modal count).
q_T: a T-only forecast, cross-fitted over 5 item folds (grouped by PAN["groups"]): the mean of h1 over other-fold items in the same exact T cell when that cell has ≥ 3 items; otherwise the
mode-and-mean KL projection (targets.ordinal_mode_mean) of the other-fold mode-z prototype (nominal: targets.nominal_zc to the modal mass), so q_T always satisfies T exactly.

## Primary estimands (per panel, per a)
A1(a) = E[S(h1, y)] − E[S(q_T, y)], y ∈ P2: the annotation-side value of the residual shape of an a-rater histogram for predicting a new rater. A1 < 0 ⇔ residual shape helps.
A2(a) = E[S(d, y)] − E[S(h1, y)]: the annotation-side analogue of the learned audit, d = the audit's exact donor replacement applied to the P1 histograms
(ordinal: random_max_matching on histogram classes within (z, floor(mean/0.1)) cells, then ordinal_mode_mean projection = pmmx; nominal: donor within z cell rescaled with nominal_zc = pzc). Dose (changed fraction, TV) reported.

## Decomposition (B) — exact identity, no approximation
A1(a) = N(a) − Δ(a), with N(a) = E‖C(h1 − p)‖²/n = E[Σ_k F_k(1 − F_k)]/(a·n) (multinomial sampling noise of the a-rater histogram; for Brier F_k → p_k)
and Δ(a) = E‖C(p − q_T(a))‖²/n (predictive value of the latent distribution beyond the a-rater T-forecast).
Estimators: N̂(a) — unbiased U-statistic from P1 (F̂_k(1−F̂_k)·a/(a−1)); Δ̂(a) two ways: (i) Δ̂_id = N̂ − Â1; (ii) on dense panels Δ̂_x = mean_i ⟨C(h2 − q_T), C(h3 − q_T)⟩/n from two further disjoint subsets P2, P3 (unbiased because P2, P3 are independent of P1 and of each other given p_i).
Agreement of (i) and (ii) is an internal validity check. Break-even: residual shape is worth learning from a raters iff Δ(a) > N(a); report â* where the fitted N(a) and Δ(a) curves cross, and
v̂ = a·N̂(a), Δ̂ at the largest a. Prediction test (dense panels): fit v and Δ(a) on a ∈ {20, 30, 40} (where available), predict A1 at a ∈ {2, 3, 5, 8} and compare with the observed A1 (out-of-sample in a).

## Panels and sizes
Dense (curves): ChaosNLI MNLI, SNLI (m = 100, nominal K = 3), DICES-350 (m = 104, K = 3), DICES-990 (m = 60, K = 3), Buse–Weimer (m = 121, K = 5, 100 items — small n).
a ∈ {2, 3, 5, 8, 10, 15, 20, 30, 40}; |P2| = |P3| = 20 (|P2| = 10 for DICES-990 at a = 40 if needed; all subsets disjoint).
Small (one point each, a = m − 1, |P2| = 1, all m leave-one-out choices): SummEval coherence/relevance (8), POPQUORN off (8) / pol (5), Scalabrino (9), HelpSteer2 (5), EmoBank (5), CSC (6).
Also at a = m − 1 on the dense panels for comparability with the heads audit.
Negative control: ChaosNLI αNLI (K = 2): T determines the histogram, so Δ ≡ 0 and A1 = N − 0 ≥ 0 by construction (implementation check).

## Inference
Item-cluster bootstrap (PAN groups; B = 2,000) of the means over items, with the R split repetitions averaged inside each item first. Rater identity: panels with persistent raters (BW, DICES, Scalabrino, SummEval experts) — intervals are conditional on the rater pool; secondary sensitivity with a rater-aware pigeonhole bootstrap on DICES-350 and BW.

## Link to the learned judges (descriptive)
Table: per panel, A1 and A2 at a = m − 1 next to the heads pmmx − soft contrast (T2b) and, for SummEval and POPQUORN, the LoRA perm − chen contrast (T3b/T3c), with doses. No ratio ("% recovered") is reported when the denominator's interval crosses 0.

## Secondary, prospectively specified moderator (polarisation) — dense panels only
Four disjoint subsets per item: P0 (size 10) defines the shape score, P1 (size 10) defines T and q_T, P2 and P3 (size 10 each) give the per-item cross-product δ_i = ⟨C(h2 − q_T), C(h3 − q_T)⟩/n.
Ordinal shape score: normalised variance (Bhatia–Davis) Pol_i = Var_0 / (μ_0 (K − 1 − μ_0)) ∈ [0, 1] (0 if μ_0 at a bound). Nominal: two-label concentration TLC_i = mass of the second class / non-modal mass, from P0.
Model: δ_i ~ β·score_i + γ1·N̂_i + γ2·entropy_0,i + mean-bin fixed effects; primary test = β, one for ordinal (DICES-350, DICES-990, BW combined by inverse-variance weighting of per-panel β) and one for nominal (MNLI + SNLI). Item bootstrap with the subset assignment re-drawn (R = 20). Visualisation by tertiles only. Report regardless of sign. POPQUORN and the LoRA cells are exploratory only.
"Polarised" wording is forbidden; use "replicable bimodality" (ordinal) / "replicable two-label concentration" (nominal).

## Amendments
**Amendment 1 (2026-10-23, before any real-panel result; only a 3-split smoke run on the αNLI negative control had been computed).** Triggered by that negative control and by Codex round 17 (reviews/codex_round17_2026-10-23.md). Supersedes the corresponding text above.
1. Ratings within an item are treated as conditionally i.i.d. draws from p_i; for persistent-rater panels the estimands are rater-pool-specific (rater-aware sensitivity on DICES-350 and BW).
2. N̂_i(a) = (1/n) Σ_k F̂_ik(1 − F̂_ik)/(a − 1) (Brier: p̂ in place of F̂) — the earlier text omitted the 1/a.
3. Δ(a) is renamed: it is the score-metric error of the prospectively specified, cross-fitted T(h1)-only comparator, and −A1(a) = Δ(a) − N(a) is the predictive advantage of the raw residual-bearing histogram over that comparator. Neither is a Bayes residual-information quantity. The crossover is called the "raw-histogram / T-comparator crossover".
4. Second exact decomposition, reported alongside: with r1 = h1 − q_T and r2 = h2 − q_T (h2 = histogram of the held-out ratings), A1 = M − 2X per item, where M = ‖C r1‖²/n (observed residual magnitude) and X = ⟨C r1, C r2⟩/n (cross-panel agreement of the residual). The raw histogram beats the comparator iff ρ = X/M > 1/2.
5. Primary comparator q_T (response-based, smoothed): for other-fold items j, predictors are T(P1_j) and responses are their P2 histograms h2_j (never their own P1). Within mode z: q(z, t) = (Σ_j w_j h2_j + λ π_z)/(Σ_j w_j + λ), w_j = exp(−(t_j − t)²/(2 bw²)) over the location coordinate t (ordinal: mean of P1; nominal: modal share of P1), π_z = mean h2_j over other-fold items with mode z. (bw, λ) ∈ {0.05, 0.1, 0.2, 0.4} × {0, 1, 5, 20} chosen by 4-fold inner grouped cross-validation within the other folds, using the panel's scoring rule against held-out ratings. q is not forced to reproduce the noisy empirical T. Secondary, audit-aligned comparator: the original exact-T cell mean of P1 histograms with the KL-projection fallback ("exact-T").
6. Reference-panel comparator (dense panels): T estimated from an independent reference subset (40 ratings; 30 on DICES-990) gives q_ref with the same smoother; Δ_ref = E⟨C(h2 − q_ref), C(h3 − q_ref)⟩/n from two further disjoint subsets (20 each; 15 on DICES-990). Called "reference-panel", not "oracle". It separates noisy-T effects from stable shape variation beyond T.
7. Prediction test replaced: on dense panels fit N(a) = v/a and Δ(a) = δ∞ + c/a (δ∞, c ≥ 0) on a ∈ {2, 5, 10, 20, 40}; prospectively predict A1 = N − Δ at a ∈ {3, 8, 15, 30} and report coverage by the observed intervals. Lack of fit counts against the two-term approximation.
8. A2 is secondary (bridge to the learned-judge intervention): report intention-to-treat (all items) and changed-item effects, changed fraction and TV.
9. Bootstrap: B = 500 replicates; each resamples groups, re-assigns the 5 outer folds, refits q_T with the (bw, λ) selected on the full data, re-draws R = 5 splits and reruns donor matching/projection (A2: B = 200, R = 2). Re-selecting (bw, λ) inside every replicate is a sensitivity on one panel.
10. Moderator score replaced: ordinal B_i = max_{v − u ≥ 2} 4 h0_iu h0_iv; nominal B_i = max_{u < v} 4 h0_iu h0_iv (balanced mass on two separated levels / two labels), standardised within panel before combining. Outcome δ_i = X-type cross-product ⟨C(h2 − q_T), C(h3 − q_T)⟩/n with q_T from P1.
11. Negative control corrected: for binary ratings T determines h1, so the exact-T comparator equals h1: A1 = 0, M = X = 0 and Δ = N (not Δ = 0). For the smoothed primary comparator A1 need not be 0; the exact-T result is the implementation check.
**Amendment 2 (2026-10-23 21:15; bug fix after the first a = m − 1 outputs had been printed for ChaosNLI MNLI/SNLI, DICES-350/990 and SummEval coherence).** In "loo" mode every item held out the SAME position r in a repetition. On persistent-rater panels (DICES, SummEval, Scalabrino, BW…) the response-based comparator q is then trained on rater r's ratings of other items and learns that rater's bias, so it is no longer a T-only forecast (symptom: Δ = N − A1 < 0 on DICES-350 and SummEval, impossible for a valid comparator). Fix: at a = m − 1, |P2| = 1, the held-out position is drawn independently per item in each of R = 20 repetitions (as the curve runs already did through per-item permutations). All a = m − 1 runs were discarded and rerun; the curve runs were unaffected.
