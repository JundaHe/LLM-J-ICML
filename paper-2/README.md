# paper-2 — 后续研究：软标签 LLM 评委的分歧归因审计

Follow-up to paper-1 (the ICSE 2027 "Illusion of Alignment" submission), fully separated from it.
Working title: *"Can Small Annotator Panels Tell Whether Soft-Label LLM Judges Learn Disagreement?"*

**Start here → [`REPORT.md`](REPORT.md)** — motivation, protocol, the final six-cell results matrix, and what the results license the paper to claim.

| Path | What |
|---|---|
| `REPORT.md` | The consolidated experiment report (read this first). |
| `idea-stage/` | ARIS Workflow-1 output: landscape, 48 ranked ideas, novelty check, external reviews, pilots (`IDEA_REPORT.md`). |
| `idea-stage/pilot/` | All code: 4-arm LoRA trainer, calibrated LORO analysis, support audit, unit tests. |
| `idea-stage/pilot/results_v2/` | Raw final-protocol outputs (per-run probability matrices + permutation certificates + per-split analyses). |
| `refine-logs/` | 5-round proposal refinement + external review rounds, final proposal, experiment plan/tracker with all per-milestone result tables. |
| `lit-review/` | Literature review (2026-09-17): how judges can actually learn item-level disagreement and output more than a score; 63 papers, verified. |

Depends on `code/commit_message/` and `code/code_readability/` for data only (own direct-key readability loader; never edits parent scripts).
