# Codex consult — literature check + brainstorm: how does paper 2 get ACCEPTED at ICML 2027? (2026-10-25)

You are an experienced ICML area chair. Be blunt and concrete. Read (absolute paths, read-only):
- /mnt/hdd2/jundahe/LLM-J-ICML/HANDOFF.md (full project state, results, rules)
- /mnt/hdd2/jundahe/LLM-J-ICML/paper-2/phase2/reports/LIT_REVIEW_2026-10-25.md (today's literature refresh)
- /mnt/hdd2/jundahe/LLM-J-ICML/paper-2/phase2/PAPER_DRAFT.md and RESULTS_TABLES.md (esp. T2b, T3b, T3c, T5, T9)
- /mnt/hdd2/jundahe/LLM-J-ICML/paper-2/phase2/reviews/codex_round18_2026-10-23.md (your last verdict: novelty ~7/10, ICML borderline / weak reject)
- /mnt/hdd2/jundahe/LLM-J-ICML/paper-2/phase2/FINITE_RATER_PROTOCOL.md

Constraints: deadline ≈ late January 2027 (≈ 13 weeks). Compute: a new server (assume 1–4 A100/A6000-class GPUs, plenty of CPU); open-weight models only (no paid API budget assumed). Commit-message panels are permanently excluded. Honesty rules in HANDOFF §3/§7 apply (no overclaiming).

Part 1 — Literature (≤ 400 words): which important 2025–2026 papers are missing from the review (name them; mark uncertain ones), and which single paper is the biggest threat to acceptance and how to neutralise it. Specifically: is "reliability-weighted shrinkage of empirical label distributions toward a statistic-preserving comparator, λ* = X/M from cross-panel residual agreement" already known (empirical Bayes / James–Stein for multinomials, Dirichlet smoothing, Dawid–Skene, label smoothing theory)?

Part 2 — Brainstorm (≤ 1,200 words): the paper that gets in. For each candidate below give (a) acceptance impact, (b) cost on our resources, (c) failure mode and what we write if it fails; then propose your best 13-week plan with milestones and go/no-go gates, and the one-sentence contribution + title of the resulting paper.
 1. Residual decoding experiment (frozen features → panel-1 residual, scored on independent panel-2 residual).
 2. Reliability-shrunk targets method (q_T + λ(h − q_T), λ* = X/M; per-item λ via covariates) — annotation side, heads, LoRA.
 3. Second/third base family for LoRA (e.g., Llama-3.1-8B, Mistral/Gemma) on SummEval + POPQUORN.
 4. Rater-aware POPQUORN rerun (hold out real user_ids).
 5. Theory: finite-sample decomposition of soft-label training risk (location vs residual, sampling noise), with conditions under which residual supervision helps — and whether it is publishable at ICML given the failed 1/a prediction.
 6. A larger dense-panel study (more datasets with many raters per item) or a new benchmark.
 7. Anything better you see — including reframing the paper (e.g., "when should you collect distributions?" annotation-budget guidance; or a positive method paper with the audit as motivation).
End with: probability estimates (rough) of ICML acceptance for (i) current package, (ii) your plan if all gates pass, (iii) your plan if the method fails; and what to submit where if a gate fails.
