## Novelty Check Report — 2026-10-12 (web search + Codex gpt-5.6-sol xhigh cross-check; traces in .aris/traces/novelty-check/2026-10-12_run01)

### Proposed Method
A support- and dose-certified donor-replacement audit of distributional judge training: each training histogram is replaced by a donor histogram that retains the recipient's mode (pmode) or exact mode and mean (pmmx, certified KL projection); the raw proper-score contrast vs. held-out annotations measures the average predictive consequence of disrupting the item↔histogram link beyond the retained statistics. Applied to frozen heads (ordinal + nominal panels) and LoRA judges (SummEval).

### Core Claims
1. Statistic-preserving donor-replacement audit (C1) — Novelty: **MEDIUM** — Closest: Gheibi & Ghazizadeh 2026 (shuffled-SLS control; VERIFIED) and Behrens & Zdeborová ICLR 2026 (within-class soft-label reshuffling in the supplement per Codex; abstract VERIFIED, the supplement claim UNVERIFIED); Ojala & Garriga 2010 (within-class permutation, methodological precedent).
2. Support / changed-fraction / TV dose certificates (C2) — Novelty: **MEDIUM** — Closest: conditional permutation importance (Strobl et al. 2008; Debeer & Strobl 2020 on fragmented conditioning cells) [UNVERIFIED in this session]; the operational bundle for supervision audits appears new.
3. Ordinal: little detected degradation after retaining exact mode+mean, mode-only penalty on SummEval; nominal ChaosNLI residual allocation penalised (C3) — Novelty: **MEDIUM** (narrowed wording) — Closest: SORD (Díaz & Marathe 2019), ordinal LDL (Wen et al. 2023), Metric-Dependent Annotation Saturation (2605.29797; VERIFIED), Distributions In/Out (2511.14117; VERIFIED — note: its label-smoothing control could NOT be verified in the current version), Zhang & Çöltekin 2026 (VERIFIED).
4. Three estimands + crossed bootstrap + certified KL projection (C4) — Novelty: **LOW** — Csiszár I-projection; Owen–Eckles multiway bootstrap [UNVERIFIED].
5. No two-statistic target dominates (C5) — Novelty: **LOW** — SORD / ordinal LDL comparisons.

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|---|---|---|---|---|
| Gheibi & Ghazizadeh, "Same Target, Different Basins: Hard vs. Soft Labels for Annotator Distributions" (arXiv 2605.20642) [VERIFIED] | 2026 | arXiv | shuffled-SLS control breaks the example→distribution match | full shuffle; no recipient-statistic preservation, no dose certificates, CIFAR-10H only |
| Behrens & Zdeborová, "Dataset Distillation for Memorized Data: Soft Labels Can Leak Held-Out Teacher Knowledge" [VERIFIED title/abstract; within-class reshuffle = supplement claim UNVERIFIED] | 2026 | ICLR | within-class reassignment of soft labels (teacher outputs) | teacher soft labels for memorisation/leakage, not human histograms; no ordinal mean preservation or projection |
| Chen et al., "Beyond Single-Point Judgment: Distribution Alignment for LLM-as-a-Judge" (arXiv 2505.12301) [VERIFIED via search] | 2025 | NeurIPS | the objective we audit | no analysis of which histogram statistics are used |
| "Metric-Dependent Annotation Saturation for Learning from Label Distributions" (arXiv 2605.29797) [VERIFIED] | 2026 | arXiv | ChaosNLI annotation-count sweep; soft vs smoothing; "item-specific signal" | intervenes by subsampling, not by statistic-preserving replacement |
| "Distributions In, Distributions Out: The Case for Soft-Label Training" (arXiv 2511.14117) [VERIFIED] | 2025 | arXiv | soft vs hard on ChaosNLI/POPQUORN/CIFAR-10H; entropy correlation | no decomposition of the distribution |
| Ojala & Garriga, "Permutation Tests for Studying Classifier Performance" (JMLR 11) [VERIFIED via search] | 2010 | JMLR | within-class permutation test | features permuted, not training targets; evaluation-time significance test |
| Díaz & Marathe, "Soft Labels for Ordinal Regression" [VERIFIED via search] | 2019 | CVPR | constructed ordinal soft targets | no comparison with residual structure of empirical histograms |
| Zhang & Çöltekin, "Quantifying and Predicting Disagreement in Graded Human Ratings" [VERIFIED] | 2026 | NLPerspectives | graded-rating disagreement prediction, Opposition Index | not a mean-vs-distribution training ablation |
| NAPHA post-hoc alignment (arXiv 2609.01073) [VERIFIED] | 2026 | arXiv | entropy-aware alignment of judge distributions | post hoc; no supervision audit |

### Overall Novelty Assessment
- Score: 6.5/10 (Codex) / 6/10 (own search)
- Recommendation: **PROCEED WITH CAUTION**
- Key differentiator: existing controls ask whether the example→soft-label association matters at all; this audit asks whether its predictive contribution survives after preserving recipient-specific location (exact mode+mean), and certifies whether the attempted residual perturbation was feasible and substantial (support, changed fraction, TV, post-projection dose).
- Risk: reviewers cite Behrens & Zdeborová (within-class soft-label reshuffle) and Gheibi & Ghazizadeh (shuffled annotator distributions); "a sophisticated conditional shuffle followed by an underpowered null" — the dose certificates and the semi-synthetic positive control are therefore central.
- Do NOT claim: first within-class soft-label shuffle; first link-breaking control; "location carries the benefit" (say "consistent with location sufficiency on the tested ordinal settings at the realised doses"); equivalence.

### Suggested Positioning
Decomposition audit of distributional supervision, headline = exact mode-and-mean preservation with dose certification; mode-conditioned shuffling as the baseline; C4 as rigor, C5 as secondary. Cite both colliding papers proactively with the delta. After removing commit: add POPQUORN offensiveness/politeness (in progress), EmoBank reader valence (5 raters, public individual ratings; obtained), CSC via LeWiDi-2025 (6-observer subset; access pending), and at least one further END-TO-END LoRA panel chosen prospectively for high support and non-trivial TV (POPQUORN offensiveness is the candidate).

### Refresh — 2026-10-23 (web search, after the POPQUORN LoRA block)
New/relevant since the 2026-10-12 check (none performs a statistic-preserving supervision audit):
- Benito-Santos & Ghajari, "Beyond Averages: Learning with Annotator Disagreement in STS", EMNLP 2025 (aclanthology 2025.emnlp-main.1800) — full ordinal distribution beats the averaged score on STS, esp. ambiguous pairs. **Must cite and discuss**: their baseline is a point/mean target, not a mode+mean-matched distribution, so their gain is compatible with our location-sufficiency finding (cf. our mean2/pmmx arms).
- Pavlovic, Paun & Poesio, "An Assessment of Human vs. Model Uncertainty in Soft-Label Learning and Calibration" (arXiv 2605.18648, rev. 2026-10-05) — human soft labels act mainly as calibration regularisers on hard samples (MNIST re-annotation). Supports our "calibration + location" reading; cite.
- Chen, Hong, Zhang, Roth, Korhonen & Plank, "Human Label Variation as Stable Signal" (arXiv 2605.28802) — annotator-specific explanation behaviour is weak per annotation but detectable after aggregation. Relevant to the planned A/G finite-rater reliability analysis; cite there.
- Kurniawan et al., "Training and Evaluating with Human Label Variation: An Empirical Study" (Computational Linguistics; arXiv 2502.01891) — 14 training methods × 6 datasets; no decomposition. Cite in related work.
- JudgeMoE (arXiv 2610.07109) aggregates judge score distributions at inference — not training on human distributions; no collision.
