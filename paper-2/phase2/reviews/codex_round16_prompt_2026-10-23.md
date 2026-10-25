# Codex round 16 — second end-to-end LoRA block (POPQUORN offensiveness) is in (2026-10-23)

Read (absolute paths, read-only):
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/RESULTS_TABLES.md — new table **T3c** (POPQUORN block) directly after **T3b** (SummEval block)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/analysis_block_popquorn.py and analysis_block_summeval.py (the POPQUORN script is the frozen SummEval script with only panel, output root and resampling unit changed: POPQUORN items are their own groups)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/lora_chain_popquorn.sh, train_judge_v3.py (same flags as the SummEval chain)
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/logs/analysis_block_popquorn.log, results/lora/popquorn_off8/*/f*/*/meta.json
- /mnt/hdd2/jundahe/LLM-J/paper-2/phase2/PAPER_DRAFT.md (current manuscript; §4 covers only SummEval) and reviews/codex_round15_2026-10-13.md (your last verdict: "single-dataset LoRA block remains the dominant top-venue reviewer risk")

Result: perm − chen raw +0.0000 [−0.0009, +0.0009] (9 cells −.0017..+.0011; ±.001 equivalence by the 90 % criterion); perm_mode − chen raw +0.0029 [+0.0009, +0.0050], 9/9 cells positive; common/arm estimands agree; dose perm 68.7–71.7 % changed, TV among changed 0.295–0.301; perm_mode 100 %, TV 0.276–0.288. Mode-only penalty is ~¼ of SummEval's (+0.0120); POPQUORN offensiveness has 58 % of ratings at the floor level.

Questions (≤ 900 words):
1. Audit the block for protocol defects before anything is written into the paper: evaluator/target separation, alignment of items across arms/seeds, whether item-level resampling is the right unit here, whether the "analysis adapted before outputs existed" claim is accurate, and whether the ±.001 equivalence band is legitimately "pre-fixed" for POPQUORN (it was chosen post hoc on SummEval).
2. Does this resolve the round-15 dominant risk? What remains (one split, one base family, position-based raters rather than persistent identities on POPQUORN)?
3. Exact wording changes for PAPER_DRAFT: abstract, contribution statement, §1 findings (i)/(ii), §4 (now two blocks), §6 limitations, Fig. 3 caption (two panels or a second figure?). Give replacement sentences, not advice. Keep the claim scope honest; the comparison of mode-only penalty sizes across the two datasets must stay descriptive.
4. Verdict: go/no-go for a top-AI-venue submission of the current package (without the new A/G work), and what the A/G finite-rater analysis would add on top.
