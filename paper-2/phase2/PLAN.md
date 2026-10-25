# paper-2 Phase 2 — can disagreement be learned when the annotator enters the input?

Started 2026-10-10 (user: "直接开始做吧", hourly progress loop). Target venue: AI top venue (ACL/EMNLP main or NeurIPS/ICLR), not SE.

## Hypothesis (from REPORT.md §3 + lit-review §0/§5)
Phase 1 showed that on 3–9-rater SE panels, soft-label (Chen et al. 2025) gains are global calibration: permuting
histograms across mode/mean-matched items (Δ_link) costs nothing. Every method in the literature with item-level
evidence puts annotator identity/history into the INPUT. Hypothesis: **Δ_link becomes negative only for a
rater-conditioned judge, and only on panels large enough** — the null of Phase 1 is a necessary-condition result.

## De-risk experiment (this phase, step 1)
Panels (fully crossed, persistent rater IDs):
- `bw`    Buse–Weimer readability, 100 Java snippets × 121 raters (local), K=5, Qwen2.5-Coder-7B-Instruct
- `dices` DICES-350 safety, 350 conversations × 123 raters (downloaded to phase2/data/dices), degree_of_harm K=4, Qwen2.5-7B-Instruct

Arms (train_judge_v3.py): hard, chen, perm (histogram-level, as Phase 1 but relaxed cells: mode exact, |Δmean| ≤ τ=0.1),
rc (rater history k=4 in prompt, CE on that rater's label), rc_perm (rc with full rating vectors swapped by the same G).
LOAO: evaluator rater excluded from targets and calibration; 12 seeded evaluators per panel; split 0 first.
Evaluation: symmetric per-arm calibration (T, λ) on calib vs target raters; RPS vs evaluator on test;
rc arms scored as the panel mixture over 24 target raters (same information as chen) and, separately, evaluator-conditioned.

Estimands
- Δ_soft = hard − chen (replicates Phase 1 on a large panel)
- Δ_link = perm − chen (histogram link; Phase 1 said ≈ 0)
- Δ_rc = chen − rc (does identity in the input beat the histogram objective as a panel-distribution predictor?)
- **Δ_link_rc = rc_perm − rc** (the de-risk quantity; the hypothesis predicts it is negative, i.e. breaking the item↔who-disagrees link hurts)
- Δ_person = rc_mixture − rc_evalcond (personalisation gain from 4 of the evaluator's own ratings)
- contracts: entropy correlation (pred entropy vs held-out panel entropy), disagreement AUROC — both still unreported from Phase 1

Decision rule: if Δ_link_rc is not negative on DICES (the most favourable panel), the direction is dead; stop and
write Phase 1 up as an audit paper for an SE venue / TOSEM. If negative on DICES, run bw, then scale.

## Schedule
1. dry runs + 1 smoke run (bw fold 0, rc, max_steps 20) on GPU 0
2. bw split 0: folds 0–5 × {hard, chen, perm, rc, rc_perm}  (hist arms ≈ 10 min, rc arms ≈ 1 h each)
3. dices split 0: folds 0–5 × same arms (GPU 1–3 when the user's vLLM servers free up)
4. analysis_v3.py: Δs with item-clustered bootstrap, contracts, per-fold table → PROGRESS.md every hour
5. cheap Phase-1 add-ons in parallel on CPU: entropy correlation + AUROC on results_v2; label-smoothing arm later

## Open risks
- bw has 60 train / 10 calib / 30 test items: CIs will be wide; dices (210/35/105) is the real test
- rc prompts are long (snippet + 4 history snippets); watch max_prompt_tokens and memory
- rater history from 60 items may not identify a rater's taste; try k=8 if rc ≈ chen
- DICES is non-SE; it is the positive-control domain, not the paper's main domain
