# Codex 补充文献的核实结果 + 两点交叉检查（2026-10-26，旧服务器 session）

这是对 `reviews/codex_icml_brainstorm_2026-10-25.md` 第 1 部分的核实，以及对 `SHRINKAGE_PROTOCOL.md` 的两点补充。新服务器上的计划和 protocol 不作任何改动。

## 1. Codex 新增的 6 篇文献：都存在，其中 2 篇的描述需要更正
核实方式：逐篇在 arXiv / ACL Anthology / AAAI OJS 上读摘要。正文还没读。

| 论文 | 结果 | 备注 |
|---|---|---|
| Kurniawan, Mistica, Baldwin, Lau. *Training and Evaluating with Human Label Variation: An Empirical Study*. Computational Linguistics 52(1), 2026 (2026.cl-1.3) | ✅ | 14 种方法 × 6 个数据集；结论是 disaggregated 或 soft 训练最好。必须引用，并正面讨论 |
| Tao, Luo, Dong, Xu. *Confidence Calibration under Ambiguous Ground Truth*. arXiv 2603.22879 | ✅ ⚠️ | 摘要讲的是 ambiguity-aware 的事后校准（Dirichlet-Soft、MC-TS、LS-TS）。Codex 说的"一个随机标注有时就能达到完整分布的校准效果"在摘要里没有，引用前要读正文核实 |
| Wu, Wang, Ong, Liang, Picard. *SHALA-LLM: Smartly Handling Ambiguous Labels in Aligning LLMs*. arXiv 2606.05376 | ✅ | 用 RL 从标注分布训练 LLM，覆盖 NLI 和情绪识别任务 |
| Wang & Chau. *Epistemic Learning from Imprecise Annotation*. arXiv 2609.34285 | ✅ | 用 credal set 作监督，是收缩方法在概念上最近的替代方案 |
| Wang, Li, Lu, Jia. *Learning Label Distribution with Dirichlet Process Mixture Model*. AAAI-26 | ✅ | 显式建模潜在标注模式的异质性 |
| Chen, Hong, Zhang, Roth, Korhonen, Plank. *Human Label Variation as Stable Signal: Learning Annotator-Specific Explanation Behavior via Cross-Annotator Preference Optimization*. arXiv 2605.28802 | ✅ ⚠️ | **Codex 的描述不准确**。这篇研究的是学习某个标注者的 free-text explanation 风格，不是"单个标注者的弱信号在聚合后可以被检测到"。只能作为"HLV 是稳定信号"的旁证 |
| *When Annotators Disagree: A Principled Approach…* | ❌ | 元数据混乱，不引用 |

## 2. 对 SHRINKAGE_PROTOCOL 的两点交叉检查（只是提醒，不修改 protocol）

**(a) 现有 heads 中的 `shrunk_res` 已经是一种收缩，而且在 SummEval coherence 上不如完全收缩的端点。**
- `probe_mean2.py:130` 定义了 `shrunk_res`：w ∈ {0.25, 0.5, 0.75, 0.9}，收缩方向是 mean2。
- T2b 中 SummEval coherence 的结果（arm − soft，RPS）：

  | arm | RPS |
  |---|---|
  | shrunk_res | −0.0016±0.0003 |
  | mean2（w = 1） | −0.0021±0.0003 |

- 结论：至少在这个 learner 上，保留哪怕 10% 的残差也是负收益。
- 对 Gate H 是一个先验预警：shrunk-λ̂ 想赢过 min(shrunk, shrunk_res, …)，λ̂ 在 heads 上很可能要接近 0。
- protocol 已经把 shrunk_res 列为 baseline，这里只是提前记下这个预期。

**(b) T9(a) 里的 X、ρ 是相对平滑 comparator 计算的，不能直接拿来估算方法的增益。**
- 按平滑 comparator 算，所有 13 个面板的 X 都 > 0（CI 不含 0）。BW、DICES 的 ρ ≈ 1，但这里面主要是位置效应。
- 与构念对齐的增益是基于 exact-T comparator 的 Xx²/Mx，目前还没有数。
- SHRINKAGE_PROTOCOL 已经把 exact-T comparator 定为主 comparator，这一点是对的。
- 写论文时不要用 T9(a) 的 X²/M 来报"预期增益"。
