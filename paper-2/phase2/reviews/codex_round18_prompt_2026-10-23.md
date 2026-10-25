# Codex round 18 — interpret the finite-rater (A/G/B) results and decide what goes into the paper (2026-10-23)

Read (absolute paths, read-only): /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/FINITE_RATER_PROTOCOL.md (amendments 1–2), finite_rater.py, finite_rater_summary.py, finite_rater_moderator.py,
RESULTS_TABLES.md section **T9** (end of file), results/finite_rater/*.json, PAPER_DRAFT.md (current manuscript), and your earlier consults reviews/codex_novelty_boost_2026-10-23.md, reviews/codex_round17_2026-10-23.md.
(The Buse–Weimer curve is still running; everything else in T9 is final.)

Key observations (check them against the files):
1. Small ordinal panels at a = m − 1 (5–9 ratings): A1x > 0 on all eight (raw histogram scores worse than the exact mode+mean comparator, +0.0004 … +0.0052), ρ = 0.06–0.58. Dense ordinal panels at a = m − 1 (60–121 ratings): A1x ≈ 0 (BW +0.0007 [−0.0004, +0.0011], DICES ±0.0002), while the smoothed comparator gives A1 < 0 with ρ ≈ 0.8–1.0. ChaosNLI (nominal) A1x ≈ −0.02 and A1 ≈ −0.02.
2. Dense curves: ChaosNLI raw histogram beats the smoothed comparator from a ≈ 9 (MNLI) / 5.5 (SNLI); exact-T comparator from a = 3. DICES-350/990 never within a ≤ 40; reference-panel crossover v/Δ_ref ≈ 44 / 37 raters vs ≈ 15 / 14 on ChaosNLI.
3. Prediction test (N = v/a, Δ = δ∞ + c/a fitted on a ∈ {2,5,10,20,40}): 2/4 predicted points covered per dense panel; systematic misses at a = 8 and 30.
4. A2 (annotation-side donor replacement, ITT): positive on SummEval coh/rel (+0.0044/+0.0034), HelpSteer2 (+0.0016), EmoBank (+0.0018, 14 % changed); ≈ 0 on POPQUORN off/pol, CSC, Scalabrino and the dense ordinal panels; +0.03–0.04 on ChaosNLI. Learned contrasts (heads pmmx − soft, LoRA perm − chen) are ≈ 0 on every ordinal panel. My reading: A2 ≈ 2 × (between-item residual signal variance) × dose, so A2 > 0 only says the targets contain item-specific residual signal; whether that signal is predictable from text is untested.
5. Moderator: pooled ordinal β +0.00019 [−0.00131, +0.00169], nominal +0.00288 [−0.00050, +0.00626] — null.

Questions (≤ 1,000 words, concrete):
A. Is my reading of A1 vs A1x right — at large a the smoothed comparator loses location precision, so A1 < 0 there reflects location, not residual; and A1x is the residual-only contrast? Which of A1/A1x should be the headline for the paper's question, given your round-17 advice to make the smoothed comparator primary?
B. A2 > 0 with learned ≈ 0: what exactly can be concluded? Propose the cheapest decisive follow-up to separate "residual not predictable from text" from "learner fails to transmit it" (we have frozen Qwen2.5-7B features for every panel: e.g. cross-fitted ridge prediction of the panel-1 residual from text features, scored by its covariance with an independent panel-2 residual). Is that sound?
C. The 1/a model's lack of fit: how to report; does it sink claim B (break-even), or do we keep only the empirical crossovers + Δ_ref?
D. How the paper changes: new headline, title, abstract sentence(s), where T9 goes (main text vs appendix), and what must NOT be claimed. Give replacement text.
E. Updated novelty / venue verdict with this added (ICML?).
