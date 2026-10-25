# Codex round 17 — review the frozen finite-rater (A/G/B) protocol BEFORE results exist

Read /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/FINITE_RATER_PROTOCOL.md (committed; no result computed yet). Context: your consults reviews/codex_novelty_boost_2026-10-23.md and reviews/codex_novelty_boost2_2026-10-23.md; existing code to reuse: targets.py (ordinal_mode_mean, nominal_zc), /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot/support_audit.py (z_label, random_max_matching), probe_mean2.py (how the heads audit builds pmode/pmm/pmmx), data_panels.py.

Please check (≤ 900 words, concrete):
1. Math: is A1(a) = N(a) − Δ(a) exact as stated (S(h1) and S(q_T) each scored on held-out ratings independent of P1; q_T cross-fitted so it depends on item i only through T(h1_i))? Is N̂ (U-statistic) unbiased for both RPS (cumulative) and Brier? Is the three-panel cross-product Δ̂_x unbiased for Δ(a)? Any hidden selection term because q_T depends on T(h1)?
2. Is Δ(a) the right object for "residual information"? Note Δ(a) depends on a through the noisiness of T — is that what we want, or should we also report Δ_oracle with T taken from a large panel? Would reviewers see the break-even a* as trivial?
3. q_T construction: exact (z, sum) cells with ≥ 3 other-fold items, else the KL projection of the mode prototype. Bias concerns at small a / sparse cells? Better choice?
4. The prediction test (fit on a ∈ {20,30,40}, predict a ∈ {2,3,5,8}) — sound and non-trivial? What model for Δ(a)?
5. A2 (annotation-side pmmx) — useful or redundant given A1?
6. The polarisation moderator spec — any remaining trap; is the Bhatia–Davis normalised variance a reasonable continuous bimodality score for K = 3 / 5?
7. Anything to change BEFORE running. Give exact replacement text for the protocol where needed.
