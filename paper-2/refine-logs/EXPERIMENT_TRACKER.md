# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|--------|-----------|---------|------------------|-------|---------|----------|--------|-------|
| R000 | M0 | unit tests: AUROC ties, ordinal α, 9-rater strata, z_i tie rule, max-matching certificate | idea-stage/pilot/test_harness.py | — | pass/fail | MUST | DONE (5/5 pass) | |
| R001 | M0 | readability direct-key loader; lock the 124-snippet universe; strata re-count | rd loader | 124 snippets | 59/56/9 expected | MUST | TODO | parent scripts still use nearest-mean join (user decision) |
| R001b | M0 | support audit (randomised maximum matching, grouped split): certificates, subsampled-rater curves, frozen support model validation, MDE simulation | idea-stage/pilot/support_audit.py | all panels, LORO | full-cell / max-changed / positive-prob / dose; predicted vs observed; MDE | MUST | DONE (audit + curves; frozen model FAILED validation → C1 = empirical enumeration; MDE table in plan) | primary evidence of the paper |
| R002 | M0 | exact Chen objective (α=.8, ε=.25, 5×.05 PGA) + no-adversary variant — implementation self-check (no code released) | A_chen / A_chen0 | smoke | runs; loss decreases | MUST | DONE (self-check; parity impossible) | LoRA deviation documented |
| R003 | M0 | randomised maximum-matching generator + certification (per split / fold) | A_perm targets | commit, readability; exact cells | changed fraction, dose, z_i/mean/pool preserved, bijection | MUST | DONE (in train_judge_v2.py; certificate in meta.json: f0 changed .342, dose .40) | G seed independent of data order |
| R004 | M0 | calibration split + leakage check | all arms | 60/10/30 by diff | no evaluator ratings in targets/calibrators | MUST | TODO | |
| R005 | M0 | smoke: 2 steps, perm + chen0 arms | train_judge_v2.py | commit | runs | MUST | DONE | |
| R010–R033 | M1 | exact commit-Why gate: Qwen, split 0 | 4 arms (hard, chen0, chen, perm) × 6 LORO folds × Why | commit | calibrated RPS, Δ_soft, Δ_adv, Δ_link^ITT, intensity, dose | MUST | DONE — gate PASS (Δ_link −.0000 [−.0006, +.0005]; Δ_soft +.0008 [−.0006, +.0021]; Δ_adv −.0001) | 24 runs, 7.4 GPU-h |
| R034–R081 | M2a | Why replication: Qwen, splits 1–2 | 4 arms × 6 folds × 2 splits | commit | as above | MUST | DONE — pooled Δ_soft +.0027 [+.0015,+.0039]; Δ_adv +.0001; Δ_link −.0001 [−.0004,+.0002] | 48 runs, ≈ 15 GPU-h |
| R082–R153 | M2b-1 | What, Qwen, splits 0–2 | 4 arms × 6 folds × 3 splits | commit | as above | MUST | DONE — pooled Δ_soft +.0013 [+.0008,+.0019] (split-heterogeneous); Δ_adv ≈ 0; Δ_link −.0001 [−.0003,+.0001] | 72 runs, ≈ 22 GPU-h |
| R154–R297 | M2b-2 | second family (Llama-3.1-8B if accessible, else deepseek-coder-6.7b-instruct), both criteria, 3 splits | 4 × 6 × 6 | commit | per family | MUST | DONE — Why: Δ_soft +.0032, Δ_link −.0000; What: Δ_soft +.0036 [+.0027,+.0045], Δ_link +.0002 [−.0000,+.0005] | 144 runs, ≈ 48 GPU-h |
| R298–R321 | M2 | w = 2 sensitivity (Why, Qwen, split 0) | A_perm w=2 × 6 folds (+ reuse) | commit | Δ_bin-link | NICE | TODO | 6–24 runs |
| R322 | M2 | Block 2 protocol comparison (scoring only) | P0 / P1 / P2 | commit + readability | soft-vs-hard gain per protocol | MUST | TODO | 0 GPU |
| — | M0 | Block 3 summarization: two-rater lemma + κ = 0 table (no GPU) | — | Java+Python | κ | MUST | TODO | analytic |
| R330–R491 | M3 | Block 4 readability (direct key, exact matching, LORO, 3 outer splits) | 4 arms × 9 folds × 3 splits × 1 family (Qwen; scoped down from 2) | 124 snippets | Δ_soft, Δ_link^ITT, intensity, dose | MUST | DONE — Δ_soft −.0008 [−.0017,−.0000]; Δ_adv +.0006; Δ_link −.0002 [−.0004,−.0000] at intensity .55 | 108 runs, ≈ 33 GPU-h |
| R500–R505 | M4 | Block 5 sensitivity: (α, ε) ablation values | A_chen/A_perm | commit one LORO fold, split 0 | Δ shifts | NICE | TODO | ≈ 3 GPU-h |
| — | M4 | tables/figures: T1+F1 support quantities, dose, MDE & lemma; T2+F2 per-family estimates with intensity; T3 certification; T4 REL/RES/UNC (descriptive); T5 protocols | — | — | — | MUST | TODO | |
