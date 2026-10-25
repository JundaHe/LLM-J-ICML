You are reviewing an in-progress empirical ML paper (AI top venue target) as a hostile but fair methodologist. Read-only access to /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/. Read first: RESULTS_TABLES.md (T3b = corrected SummEval block, NEW; T4/T5 regenerated from v6; T2b/T2c; T8), results/lora/summeval_coherence8/analysis_block_summeval.log, PAPER_DRAFT.md (v0, §1–§6), PROGRESS.md Hours 21–23, your previous round reviews/codex_round10_2026-10-11.md.
New since round 10:
1. Corrected SummEval block (histogram-class matching; 3 joint seed realisations × 3 expert folds; frozen analysis): perm − chen raw −0.0001 [−0.0011, +0.0011] (90 % CI inside ±.001; seeds −0.0007/+0.0007/−0.0002); perm_mode − chen raw +0.0120 [+0.0086, +0.0155], common +0.0077, arm +0.0084, positive in every seed and fold; common − raw −0.0045 [−0.0074, −0.0015]. Dose: perm 0.81, TV 0.35, zero-TV 0. Calibration grid: λ hit its maximum 0.5 in 53 % of refits (extended-grid sensitivity λ ≤ 0.9 running).
2. Finding about the matching: the class-to-class pairing in random_max_matching is deterministic given class sizes; permutation seeds randomise only within-class donor identity (dose statistics identical across seeds; donor-map hashes differ). Disclosed in draft §2.2.
3. ChaosNLI v6 (T5): pzc − soft KL +0.029 at m = 5 (was +0.015 vector-matched), +0.018 at m = 10, unchanged at 20/50; dose certified. Positive controls v6 (T4): BW pmm − soft D −0.48 (was −0.20), learnable fraction 0.79.
4. PAPER_DRAFT.md v0: §2 design/dose/estimands/pipelines, §3 heads results, §4 LoRA (SummEval now frozen; commit provisional), §5 G×R diagnostic, §6 limitations.
Questions:
A. T3b: is the wording "practically equivalent under all three estimands" acceptable given the post hoc ±.001 band (±.002 frozen after seed-2000 folds)? How to report the λ-grid boundary hits and the extended-grid sensitivity? Any veto on the T3b caption or reading?
B. Matching-seed determinism: does it change what the "3 joint seed realisations" can support? Required wording.
C. Draft §2–§3: list every sentence you would veto or rewrite (quote + replacement). In particular the headline framing of "mode-and-mean-preserving replacement is within noise everywhere tested" with the dose caveat, and the ChaosNLI/positive-control sentences.
D. Abstract: write the abstract you would accept now (≤ 200 words), given SummEval frozen, commit LoRA provisional (fixed-donor optimizer block + chen0/perm_mode0 running), heads v6 complete.
E. Top three actions before the first full draft, updated.
Write markdown with sections A–E and a short verdict.
