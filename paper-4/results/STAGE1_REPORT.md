# Paper 4 — stage-1 result on MultiPref (overall_pref), 2026-10-27
All numbers from committed artefacts: paper-2/phase2/results/rho_exact/multipref_*.json, paper-2/phase2/results/decoding_v2/multipref_overall_d64_E_last.json, paper-4/results/rater_long_multipref_overall_tuned.json. Protocol: PROTOCOL_STAGE1.md with Amendments 1–2.

| decision-rule quantity | value | rule condition (rater-side branch) |
|---|---|---|
| ρ_exact (a = 3) | 0.253 [0.221, 0.294] (helpful 0.285, harmless 0.211) | < ½ — met |
| G/X (frozen Qwen2.5-7B, a = 3, b = 1) | 0.105 [0.057, 0.119] | ≤ 10 % — **not met** (interval straddles) |
| rater thresholds ΔLL (M2 − M0) vs item dispersion ΔLL (M4 − M2) | +0.0364 vs +0.0014 per rating (ratio 25) | ≥ 3× — met |

Controls: positive control (P1 mean → P2 mean Spearman) 0.35; within-T permutation G_perm −0.00004 [−0.00005, −0.0000]; G interval [+0.00007, +0.00013] excludes 0; V [+0.00010, +0.00015].

**Prespecified outcome: "mixed" (G/X neither ≤ 10 % nor ≥ 30 %) → report and decide with the user.**

Reading (descriptive):
- MultiPref sits between paper 2's ordinal panels (G/X upper bounds ≤ 0.4–10 %) and ChaosNLI (17–26 %): about a tenth of the reproducible preference-shape is linearly decodable from frozen text features.
- Rater-side structure is large compared with item-side dispersion, and it is almost entirely **response style** (rater scale: how often a rater says "clearly" vs "slightly", +0.031) rather than rater **position** (A/B shift, +0.005).
- The earlier statement "rater shifts do not improve held-out likelihood" (untuned fit) is withdrawn: it was an over-fitting artefact (Amendment 2).

Candidate stage-2 directions (for the user's decision):
A. Factorised RM: text → location (+ decoded residual), rater → response-style (scale/thresholds) learned from few ratings; evaluate on new-rater and few-shot personalisation against distributional and group-conditioned RMs. (Recommended: both findings point here; the decodable 10 % is kept by the text head.)
B. Evaluation paper: how much of the reproducible disagreement do distributional RMs actually capture (ceiling = G/X-style estimands), across MultiPref / HelpSteer2 / PRISM.
