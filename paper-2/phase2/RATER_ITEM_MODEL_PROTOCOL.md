# Where does the reproducible disagreement live? A rater–item decomposition — protocol, frozen before any result
Committed 2026-10-26 (after Gates D and H; before any fit). CPU only. Motivation: T9 shows that the residual shape of a histogram beyond exact mode and mean is **reproducible across disjoint rater halves** (X > 0 on every panel; ρ → 1 on dense panels), yet it is **not decodable from the text representation** (DECODING_PROTOCOL, final-layer result) and **not used by learned judges** (audit). Reproducible-across-raters means it is an item property; not-decodable means the representation does not see it. This protocol asks what kind of item property it is, with a classical measurement model, so that the paper's mechanism claim is tested rather than asserted (HANDOFF §3 forbids an untested "label-structure" explanation).

## Model (graded response / ordered probit with heteroscedastic items)
Rating y_{ir} ∈ {0, …, K−1} of item i by rater r. Latent Y*_{ir} = θ_i + σ_i · ε_{ir}, ε ~ N(0, 1); y = k ⇔ c_{r,k−1} < Y* ≤ c_{r,k} with rater-specific ordered cut-points c_r (K − 1 per rater; a global set when raters are not persistent).
- **M0** (location only): θ_i, common cut-points c, σ_i ≡ 1.
- **M1** (location + rater thresholds): θ_i, c_r, σ_i ≡ 1 — "disagreement is rater harshness".
- **M2** (location + rater thresholds + item dispersion): θ_i, c_r, σ_i free — "some items polarise" (IRT: σ_i⁻¹ is the item discrimination).
Fitted by penalised maximum likelihood (ridge on θ, log σ and on c_r − c̄; torch, L-BFGS), separately per panel. Persistent-rater panels: BW (100 × 121), DICES-350 (350 × 104), SummEval experts (1,600 × 3; the 5 turker positions are not persistent and get common cut-points), Scalabrino (124 × 9). Position panels (POPQUORN, HelpSteer2, EmoBank, CSC, DICES-990, Dorn, JetBrains): M0 vs M2 only (no rater identity).

## Estimands
1. **Fit**: held-out log-likelihood of y under M0/M1/M2 with a 5-fold split over *ratings* (random cells of the item × rater matrix), item-cluster bootstrap for differences. ΔLL(M1 − M0) measures how much rater thresholds explain; ΔLL(M2 − M1) how much item-specific dispersion explains.
2. **Which component carries the reproducible residual**: simulate full rating matrices from each fitted model (parametric bootstrap, 20 draws) and run the T9(a) finite-rater analysis on the simulated matrices: X_sim(M0), X_sim(M1), X_sim(M2) versus the observed X. The model whose X_sim matches X_obs (within the bootstrap interval) is the simplest adequate description of the reproducible shape. Prediction registered here: X_sim(M0) ≈ X_sim(M1) ≈ 0 (location and thresholds are removed by the exact-T comparator), X_sim(M2) ≈ X_obs — i.e. the reproducible shape is item dispersion.
3. **Is dispersion text-predictable?** σ̂_i (from M2, cross-fitted: σ̂ for item i estimated with item i's own ratings but compared with a decoder trained on other items) decoded from the frozen features with the DECODING_PROTOCOL ridge pipeline: out-of-fold Spearman(σ̂_decoded, σ̂_i) and against the independent-panel dispersion of Amendment 2(b). Positive control: θ̂_i decoded the same way (expected Spearman ≈ the mean's 0.3–0.65).
4. **Link to the judges** (descriptive): per panel, Spearman between the heads' predicted dispersion (D_pmf of the soft head, T2b machinery) and σ̂_i; and the share of items whose σ̂_i is in the top quartile that the heads rank in their top quartile.

## Prespecified reading
- If ΔLL(M1 − M0) ≫ ΔLL(M2 − M1) and X_sim(M1) ≈ X_obs: the reproducible shape is mostly rater harshness → threshold mechanism; text cannot predict it by construction; the practical consequence is calibration, not distributional training.
- If ΔLL(M2 − M1) is material and X_sim(M2) ≈ X_obs ≫ X_sim(M1): the reproducible shape is item dispersion ("which items polarise"); whether a judge can learn it is then exactly the question of estimand 3 — the paper reports the decoded Spearman per panel and does not claim learnability or unlearnability beyond that number.
- Nominal ChaosNLI is analysed with a multinomial analogue only if time permits (not required for the ordinal claim).

## Forbidden statements
"Ordinal disagreement is caused by label structure"; "disagreement is noise" (the reproducible part is not); any statement about raters' psychology; any claim about panels without rater identity concerning thresholds.

## Amendments
(none)
