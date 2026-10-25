# 文献综述：模型怎样才能真正学到人类分歧？以及评委如何不只输出一个分数
**日期**：2026-09-17 · **触发**：paper-2 审计得出"软标签 KL 微调在 3–9 人面板上不含条目级分歧信息"之后，用户提出两个问题：(Q1) 最终模型怎样才能学到人类分歧；(Q2) 怎样让模型不只输出一个分数。
**检索来源**：WebSearch（5 个并行子方向代理，≥31 次查询）+ arXiv API（5 次）+ Semantic Scholar API（5 次中 2 次成功，其余 429 限速）。本地 `papers/`、`literature/` 为空（WARN: local contributed nothing）；Zotero/Obsidian 未配置。**候选 63 篇去重后经 `verify_papers.py` 三层核验：61 篇 ✅ verified（arXiv/CrossRef/S2），2 篇 … verify_pending（仅有标题、无 arXiv 号：DisCo 与 VPL，S2 暂时限速）。**

---

## 0. 一句话结论

> **凡是有条目级（item-level）证据的方法，都给了模型"标注者是谁"或"人为什么分歧"这类额外信息（rater ID / 标注者历史 / 理由）；只改训练目标或输出形式（软标签 KL、分布式奖励头、分位数头、多采样、多 persona、推理 RM）的方法，要么没测过条目级分歧，要么测了很弱。** 而且 Kohli 2026 用 100 人/条目的 ChaosNLI 直接量化了原因：KL 匹配在 ~10 个标注者就饱和，但"哪些条目有争议"（熵相关）要 20–50 个标注者才能学到——我们的 3–9 人面板处在阈值之下，零结果是意料之中。

这一条也修正了我上次的判断：我建议的 `smooth` 臂（label smoothing 对照）和"面板规模剂量曲线"，Kohli 已经在 NLI/编码器模型上做了（smoothing r≈.45–.49 vs 软标签 r=.643）。我们的版本仍有差异（见 §5），但不能再当作主要 novelty。

---

## 1. 证据地图：按"分歧信号从哪里来"分层

| 层 | 代表工作 | 条目级证据强度 | 关键数字 |
|---|---|---|---|
| **A. 只改训练目标 / 输出头**（软标签 KL、DPL、分位数、序数概率奖励、conformal 区间） | Chen 2505.12301；Siththaranjan DPL 2312.08358；Dorka 2409.10164；Chen OPRM 2602.12660；Sun PURM 2503.22480；Sheng 2509.18658 | **弱或未测** | Zhang 2410.14632（ICML'25）是唯一正面测的：KL 训练的分布式 RM 在 3–5 人面板上识别"分歧条目"AUROC 仅 .58–.65（BT/MSE ≈ .48）；Wang 2503.03064：LLM 分数分布的 std 与人类 std 的 Spearman 仅 ≈ .1–.2 |
| **B. 标注者侧信息**（per-rater 头、标注者嵌入、人口学、in-context 标注者历史、rater-specific 示例） | Davani TACL'22 2110.05719；Gordon Jury Learning CHI'22 2202.02950；DisCo ACL'23；Fleisig EMNLP'23 2305.06626；AART NAACL'24 2311.09743；DiADEM 2604.08425；Opt-ICL 2510.07105（LeWiDi-2025 双赛道第一）；PersonaJudge 2607.05742 | **最强** | Fleisig：预测条目间方差 +33%；DiADEM：与条目级分歧相关 .75（DICES）；Opt-ICL 消融：去掉 in-context 标注者示例即崩；Orlikowski 2502.20897：微调 LLM 的增益几乎全来自记住标注者 ID，而非人口学 |
| **C. 理由 / 解释**（人写的分歧理由、标注者专属 rationale） | Chen 2406.17600（Findings EMNLP'24）；Jiang LiveNLI 2304.12443；Sarumi 2604.21667；DPUA 2605.10415 | **强** | 每条目几条人类解释即可显著逼近人类判断分布；理由联合建模显著提升 per-annotator 预测；DPUA 用 GRPO 让口头不确定性对齐人类分歧 |
| **D. 从条目特征直接预测分歧** | Zhang & Çöltekin 2605.01168；Wan AAAI'23 2301.05036；Ehara 2605.12422；Hanania 2609.06646；Inoshita 2604.27345 | **中等**（文本可预测的部分有限） | 序数评分的方差回归：中等正相关，"观点对立"条目被系统低估；嵌入序数一致性信号预测评委-人分歧 AUC 优于概率信号；非文本域（笑声定位，3–5 人面板）AUC .83 |
| **E. 后处理**（熵分桶对齐、aleatoric/epistemic 分解、crowd calibration） | Steindl NAPHA 2609.01073（EMNLP'26）；Lail 2609.06444；Khurana Crowd-Calibrator COLM'24 2408.14141 | **中等** | NAPHA：先预测条目熵桶再对齐，高熵条目增益最大，oracle 熵桶增益更大；Lail：按 epistemic 不确定性排序比按总熵多去除 83% 误差（ChaosNLI） |
| **F. 多采样 / 多 persona / 辩论 / 推理型 RM** | Ni 2506.19467（EACL'26）；Kohli "Nine Judges" 2605.29800；MAJ-EVAL 2507.21028；DeepSeek-GRM 2504.02495；RM-R1 2505.02387；BoN Appetit 2510.12516 | **反映模型不确定性，不是人类分歧** | RLVR 推理**恶化**分歧建模、朴素 CoT 略帮 RLHF 模型；9 个 LLM 评委≈2 票独立信息；Best-of-N 对分歧任务无效，模型平均有效；推理 RM 只报多数票准确率 |

**共同规律**：A/F 层的"分布/展开"是**模型的**不确定性；B/C 层把"人"引入输入端，才出现**人的**分歧。D/E 层介于中间：条目特征能解释一部分，剩下的需要标注者信息。

---

## 2. 关键单篇（对我们最重要的 8 篇）

1. **Kohli 2026, *Metric-Dependent Annotation Saturation for Learning from Label Distributions*, 2605.29797** ✅ — ChaosNLI 子采样 N 个标注者微调 DeBERTa/RoBERTa：KL 在 N≈10 饱和（5 个种子 87–95% 增益），熵相关需 N≈20–50；label smoothing 五档 r≈.45–.49 vs 软标签 r=.643。**直接解释我们的零结果，并给出"无条目信息对照 = label smoothing"的先例。**（注意：我们 `FINAL_PROPOSAL.md` 把它描述成"留出标注者组"，是错的，需修正。）
2. **Zhang et al. ICML 2025, *Diverging Preferences*, 2410.14632** ✅ — MultiPref/HelpSteer2（4 / 3–5 人）上分布式 RM 找分歧条目 AUROC .58–.65。与我们最接近的 RM 侧结果：信号存在但很弱。
3. **Ni et al. EACL 2026, 2506.19467** ✅ — 60 种配置：LLM 直接输出人类标签分布仍然很差；口头化分布 > 采样展开；RLVR 推理有害。**回答 Q2 的一半：输出直方图比多采样好，但零样本仍不够。**
4. **Opt-ICL (Sorensen & Choi) 2510.07105** ✅ + **LeWiDi-2025 2510.08460** ✅ — 把该标注者过去的标注放进上下文做元学习，两赛道第一；消融证明 in-context 标注者示例是关键。**回答 Q1 最有力的正例。**
5. **Fleisig EMNLP 2023, 2305.06626** ✅ — 不用 ID，只用人口学+问卷特征就把条目方差预测提升 33%。说明标注者**特征**（不只 ID）也能携带条目级信息。
6. **Chen et al. Findings EMNLP 2024, 2406.17600** ✅ — 几条人类解释即可让 LLM 逼近 ChaosNLI 的判断分布，并警告条目级 KL 会"看起来不错但结构错"。**理由是最省标注的分歧信号。**
7. **Steindl NAPHA, EMNLP 2026, 2609.01073** ✅ — 显式的"条目熵预测 → 分桶对齐"两段式，把"哪些条目有争议"和"众数是什么"解耦。可作为我们 D/E 层的模板。
8. **Wang et al. Findings EMNLP 2025, 2503.03064** ✅ — 判断 token 分布均值优于众数；CoT 塌缩分布；LLM 分布 std 与人类 std 相关仅 .1–.2。**Q2 的反例：token 概率分布不是分歧。**

SE 领域：**没有任何工作建模或评估标注者分歧**——Wang ISSTA'25 2502.06193、SWR-Bench 2509.01494（3 专家×100）、CoReEval 2510.16579、SWE-Judge 系列都只报与平均分的相关或 pairwise kappa。空白仍在。

---

## 3. 被接受的"学到分歧"评估契约（由弱到强）

| 契约 | 出处 | 我们已有 | 备注 |
|---|---|---|---|
| 对留出条目的分布匹配（KL/JSD/Wasserstein/soft-F1） | Kurniawan CL'26 2502.01891；Wang 2503.03064 | ✅（RPS） | Kohli：N≈10 即饱和，**不能**单独支撑条目级主张；JSD 可被误导性抬高 |
| 条目级熵/方差相关（模型 vs 人） | Kohli 2605.29797；Zhang & Çöltekin 2605.01168；Davani | ❌ 未报 | **应补**：我们的 P_test.npy 现成，CPU 即可 |
| 分歧条目 vs 一致条目的判别 AUROC | Zhang 2410.14632 | ❌ | 与 CSJE 分层天然对接（Low 层 = 分歧条目） |
| 留出标注者身份（LOAO / alt-test） | Calderon 2501.10970；Orlikowski seen-vs-unseen | ✅ | 测的是可替代性，不是"知道哪里分歧" |
| "无条目信息"对照 | Kohli（label smoothing）；**我们（保众数/均值/总量的链接重排）** | ✅ | 我们的对照比 smoothing 更严格（保位置与形状边缘），这是仍然成立的差异点 |
| 熵分层报告 | NAPHA；Ni | 部分 | 应按 CSJE 层报告 Δ |

**多标注者数据集**（≥10 人/条目，核实到的）：ChaosNLI（100 人，~4.6k 条，3 类）、CIFAR-10H（~50 人，图像）、LiveNLI（10+ 人×122 条，带解释）。序数量表的都小：MultiPref（4 人，5 点）、HelpSteer2（3–5 人）、VariErr（4 人）、POPQUORN（≈6.7 人）。**SE 领域唯一的大面板是 Buse–Weimer 可读性（约 120 人×100 片段，5 点）**——从 git log 看 paper-1 最近已接入该面板（"BW panel K=121"），这是做 SE 版 Kohli 曲线的直接杠杆。

---

## 4. 回答两个问题

### Q1 模型怎样才能真正学到人类分歧？
按证据强度排序的三条路（都可在现有 SE 面板上做，第 3 条需新数据）：

1. **标注者条件化评委（rater-conditioned judge）**——把"这是标注者 r"作为输入（ID token / 标注者嵌入 / in-context 该标注者的历史评分 / 每标注者 LoRA 头），训练目标是**逐标注者**评分而不是直方图。文献里所有强证据都在这一类（Davani、DisCo、Opt-ICL、PersonaJudge）。评估：对留出条目预测每位标注者；条目级方差 = 各标注者预测的方差，与真实方差做相关；**再用我们的链接重排做对照**（重排后标注者-条目配对被打断，若模型真学到了 rater×item 交互，Δ_link 应变为正）。这同时补上了上次说的"正对照"。注意 Orlikowski 的警告：增益可能主要来自记住标注者，泛化到新标注者要单独测（seen vs unseen）。
2. **理由驱动**——用"为什么会分歧"的解释作为监督（Chen 2406.17600、Sarumi、DPUA）。我们的 SE 数据没有人类理由；可行替代是让 LLM 为 Low 层条目生成"争议点"再蒸馏，但那是弱监督，需要谨慎标注为 LLM 生成。
3. **面板规模**——Kohli 的阈值是 20–50 人。要在 SE 证明"学得到"，最现实的是 Buse–Weimer 121 人面板：子采样 K=3,5,9,20,50,121 做熵相关与 Δ_link 的剂量曲线，回答"SE 面板需要多少人才能谈分歧学习"。这是复现+扩展（序数、LLM 评委、SE 域、我们的对照），不是首创。

### Q2 怎样让模型不只输出一个分数？
文献给出的格式排序（按"展开是否真的追踪人类分歧"的证据）：

| 输出格式 | 证据 | 建议 |
|---|---|---|
| **口头化直方图**（文本里直接给 5 档比例） | Ni：优于采样展开；LeWiDi：模型平均有效 | ✅ 首选；仍需在域内微调或后处理对齐（NAPHA） |
| **理由 + 口头化不确定性，用 RL 对齐分歧**（DPUA） | 有条目级对齐证据 | ✅ 第二选；GRPO 可在我们 4×Ada 上做 7B |
| **逐标注者模拟输出**（"标注者 1–6 各会打几分"） | PersonaJudge、Opt-ICL | ✅ 与 Q1 路线 1 同一模型，天然给出分歧 |
| 分数 token 的概率分布 | Wang：与人类 std 相关 .1–.2；CoT 塌缩 | ⚠️ 只当校准信号用 |
| 多采样展开 / 多 persona 面板 / 辩论 | Ni、Kohli Nine Judges、Inoshita | ❌ 反映模型不确定性；9 评委≈2 票 |
| 推理型 RM（RM-R1/GRM 类） | Ni：RLVR 恶化分歧建模 | ❌ 不作为分歧路线 |
| conformal 区间 | 边际覆盖，宽度不随条目分歧变 | ⚠️ 仅作不确定性包装 |

一个具体的结构化输出：`{score_histogram: [p1..p5], contested: yes/no + 理由, per_rater: {r1..r6}}`，三个字段分别对应 A/E/B 层，评估用 §3 的契约。

---

## 5. 对 paper-2 下一步的修正建议

- **保留**：正对照（现在明确为"标注者条件化臂"，同时是方法贡献）；路由后果分析（CPU，免费）；补报条目级熵相关与分歧 AUROC（CPU，免费，两条被接受的契约我们还没报）。
- **降级**：`smooth` 臂 → 仍值得跑但定位为"复现 Kohli 对照 + 证明链接重排比 smoothing 更严格"，不是 novelty。
- **重定位**：面板规模曲线 → 用 Buse–Weimer 121 人做 SE 版 Kohli 曲线，主张"SE 面板的可学习阈值"，定位为复现+扩展。
- **新的主贡献候选**："在 SE 面板上，只有把标注者引入输入端才出现可归因的分歧学习"——四臂（hard / chen / rater-conditioned / rater-conditioned+perm）+ 链接重排对照 + 熵相关 + LOAO，Qwen 与 DeepSeek 两家族。约 150–200 次 LoRA 运行。
- **文档勘误（待办）**：`refine-logs/FINAL_PROPOSAL.md` 与 `IDEA_REPORT.md` 对 Kohli 2605.29797（实为标注饱和/ChaosNLI，非"留出标注者组"）和 Gheibi 2605.20642（实为 CIFAR-10H 上软标签 CE vs 硬标签多遍投递，非"全局 shuffle"）的描述需按原文修正。

---

## 6. 全部候选文献表（63 篇去重；✅ = verify_papers.py 核实；… = 待核）

| 论文 | 年份/场馆 | 方法 | 关键结果 | 与我们的关系 | 来源 | 核验 |
|---|---|---|---|---|---|---|
| Kohli — Metric-Dependent Annotation Saturation (2605.29797) | 2026 arXiv | ChaosNLI 子采样 N 人微调 | KL 饱和 N≈10；熵相关需 20–50；smoothing r≈.47 vs soft .643 | 解释我们的零；smoothing 对照先例 | web | ✅ |
| Zhang et al. — Diverging Preferences (2410.14632) | ICML 2025 | KL 分布式 RM 于 3–5 人面板 | 分歧条目 AUROC .58–.65 | 最近的 RM 侧同类结果 | web | ✅ |
| Ni et al. — Can Reasoning Help LLMs Capture Disagreement? (2506.19467) | EACL 2026 | 60 配置；口头化 vs 采样；RLVR | RLVR 恶化；口头化更好 | Q2 格式证据 | web/arXiv/S2 | ✅ |
| Chen et al. — Beyond Single-Point Judgment (2505.12301) | 2025 arXiv | KL+CE+对抗 | 无熵相关/LOAO | 我们审计的对象 | web | ✅ |
| Gheibi et al. — Same Target, Different Basins (2605.20642) | 2026 arXiv | 软 CE vs 硬标签投递（CIFAR-10H） | 少票时硬标签更好 | 支持"稀疏面板软目标≈噪声" | web | ✅ |
| Kurniawan et al. — Training & Evaluating with HLV (2502.01891) | CL 2026 | 14 方法×6 指标×6 数据集 | 软标签/去聚合最好；JSD 陷阱 | 指标契约 | web/arXiv | ✅ |
| Wang et al. — Judgment Distribution (2503.03064) | Findings EMNLP 2025 | token 分布均值/风险规避 | std 相关 .1–.2；CoT 塌缩 | Q2 反例 | web/arXiv | ✅ |
| Steindl et al. — NAPHA (2609.01073) | EMNLP 2026 | 熵分桶后处理对齐 | 高熵条目增益最大 | E 层模板 | web | ✅ |
| Lail — Decomposing LLM-Judge Uncertainty (2609.06444) | 2026 arXiv | aleatoric/epistemic 闭式分解 | epistemic 排序多去 83% 误差 | 路由/主动标注 | web | ✅ |
| Davani et al. — Dealing with Disagreements (2110.05719) | TACL 2022 | per-annotator 头 | 头间方差 ≈ 分歧 | B 层基线 | web | ✅ |
| Gordon et al. — Jury Learning (2202.02950) | CHI 2022 | 标注者条件化 + 陪审团 | 陪审团构成翻转判决 | B 层 | web | ✅ |
| Weerasooriya et al. — DisCo | Findings ACL 2023 | 标注者×条目联合嵌入 | 条目分布更准 | B 层 | web/S2 | … |
| Fleisig et al. — When the Majority is Wrong (2305.06626) | EMNLP 2023 | 人口学+问卷特征 | 方差预测 +33% | B 层（无 ID） | web/arXiv/S2 | ✅ |
| Mokhberian et al. — AART (2311.09743) | NAACL 2024 | 标注者嵌入+对比损失 | per-annotator F1 ↑ | B 层 | web | ✅ |
| Orlikowski et al. — Beyond Demographics (2502.20897) | 2025 arXiv | 微调 LLM 条件化 ID/人口学 | 增益来自 ID 记忆 | seen/unseen 契约 | web | ✅ |
| Orlikowski et al. — Ecological Fallacy (2306.11559) | ACL 2023 | 群体层 | 群体层无益 | B 层反例 | web | ✅ |
| Sun et al. — Sociodemographic Prompting Not Yet Effective (2311.09730) | NAACL 2025 | persona 提示 | 不稳定甚至有害 | persona 反例 | web | ✅ |
| Santurkar et al. — Whose Opinions (2303.17548) | ICML 2023 | OpinionQA 群体分布 | 群体级失配 | 群体级 | web | ✅ |
| Sorensen et al. — Pluralistic Alignment (2402.05070) | ICML 2024 | 框架 | 分布/陪审团多元 | 概念 | web | ✅ |
| Leonardelli et al. — LeWiDi-2025 (2510.08460) | NLPerspectives 2025 | 软标签 + perspectivist 赛道 | 标注者示例/元数据有效 | 评估契约 | web | ✅ |
| Sorensen & Choi — Opt-ICL (2510.07105) | NLPerspectives 2025 | in-context 标注者示例元学习 | 双赛道第一 | Q1 正例 | web | ✅ |
| Sawkar et al. — LPI-RIT DisCo+ (2508.08163) | NLPerspectives 2025 | 元数据嵌入+分布损失 | 一致增益 | B 层 | web | ✅ |
| Shetty et al. — DiADEM (2604.08425) | 2026 arXiv | 人口学重要性门控 | 分歧相关 .75 | B 层 | web/S2 | ✅ |
| Xu & Jurgens — Beyond Consensus survey (2601.09065) | 2026 arXiv | 综述 | 目标/指标分类 | 地图 | arXiv | ✅ |
| Zhang & Çöltekin — Graded Ratings Disagreement (2605.01168) | NLPerspectives 2026 | 序数方差回归 | 中等相关；对立被低估 | D 层（序数） | web/S2 | ✅ |
| Wan et al. — Everyone's Voice Matters (2301.05036) | AAAI 2023 | 文本+人口学预测分歧 | 人口学有益 | D 层 | web | ✅ |
| Ehara — Predicting Judge–Human Disagreement (2605.12422) | EDM 2026 | 嵌入序数一致性 | AUC > 概率信号 | D 层（序数评委） | web | ✅ |
| Hanania et al. — Laugh Localization Disagreement (2609.06646) | 2026 arXiv | 属性预测分歧 | AUC .83（3–5 人） | D 层 | web | ✅ |
| Inoshita et al. — Labels not Uncertainty (2604.27345) | 2026 arXiv | 640k 采样 vs 人类分布 | 得标签不得不确定性 | F 层反例 | web/arXiv | ✅ |
| Chen et al. — Seeing the Big through the Small (2406.17600) | Findings EMNLP 2024 | 少量解释 ICL | 显著逼近 HJD | C 层 | web | ✅ |
| Jiang et al. — LiveNLI (2304.12443) | 2023 arXiv | 122×10+ 带解释 | 数据集 | C 层 | web | ✅ |
| Sarumi et al. — Annotator-Specific Rationales (2604.21667) | NLPerspectives 2026 | 理由联合建模 | per-annotator ↑ | C 层 | web | ✅ |
| Lu et al. — DPUA (2605.10415) | 2026 arXiv | 标签+理由+不确定性，GRPO | 不确定性对齐分歧 | Q2 第二选 | web | ✅ |
| Muscato et al. — ICL for Disagreement (2506.06113) | 2025 arXiv | 检索相似/高熵示例 | few-shot 多为负 | 检索反例 | web | ✅ |
| Li et al. — Judging with Confidence (2510.00263) | 2025 arXiv | 分布匹配 SFT 于 ~10 人投票 | MSE/ECE ↓ | 无分歧排序测试 | web | ✅ |
| Siththaranjan et al. — DPL (2312.08358) | ICLR 2024 | 均值-方差/类别效用头 | 间接验证 | A 层 | web | ✅ |
| Halpern et al. — Pairwise Calibrated Rewards (2506.06298) | 2025 arXiv | 集成比例 = 标注者比例 | 构造上绑定 | A 层例外 | web | ✅ |
| Chen et al. — OPRM (2602.12660) | ICLR 2026 | 序数概率奖励 | 宽度=置信 | A 层未测 | web | ✅ |
| Dorka — Quantile RM (2409.10164) | 2024 arXiv | 分位数头 | RewardBench | A 层未测 | web/S2 | ✅ |
| Sun et al. — PURM (2503.22480) | 2025 arXiv | 高斯奖励 | 合成翻转 | A 层未测 | web | ✅ |
| Poddar et al. — VPL | NeurIPS 2024 | 用户潜变量 | per-user | 个性化 | web | … |
| Chen et al. — PAL (2406.08469) | 2024 arXiv | 理想点原型 | per-user | 个性化 | web | ✅ |
| Chakraborty et al. — MaxMin-RLHF (2402.08925) | ICML 2024 | RM 混合 | 组胜率 | 群体 | web | ✅ |
| Li et al. — DPRM (2402.09764) | 2024 arXiv | 类别分布+OT | 下游 | A 层 | arXiv/S2 | ✅ |
| Yang et al. — Bayesian RM (2402.13210) | 2024 arXiv | Laplace-LoRA | OOD | 认知不确定性 | web | ✅ |
| Khurana et al. — Crowd-Calibrator (2408.14141) | COLM 2024 | 人群分布校准弃权 | 选择性预测 | E 层 | web/S2 | ✅ |
| Sheng et al. — Conformal Judge (2509.18658) | EMNLP 2025 | conformal 区间 | 覆盖 | 边际 | arXiv | ✅ |
| Kohli et al. — Nine Judges, Two Votes (2605.29800) | 2026 arXiv | 9 评委独立票估计 | ≈2 票 | F 层反例 | web | ✅ |
| Chen et al. — Multi-Agent-as-Judge (2507.21028) | 2025 arXiv | persona 辩论 | 维度相关 | F 层 | web | ✅ |
| He et al. — PersonaJudge (2607.05742) | 2026 arXiv | 标注者专属示例 ICL | +9.9pp；推理轨迹最有用 | B 层（LLM 评委） | web | ✅ |
| Liu et al. — DeepSeek-GRM (2504.02495) | 2025 arXiv | 原则+批评+投票 | 准确率 | F 层 | web | ✅ |
| Chen et al. — RM-R1 (2505.02387) | 2025 arXiv | 推理 RM | 准确率 | F 层 | web | ✅ |
| Ruiz et al. — BoN Appetit (2510.12516) | NLPerspectives 2025 | 测试时扩展 | BoN 无效，平均有效 | Q2 | web | ✅ |
| Jin et al. — Z-Reward (2606.09076) | 2026 arXiv | 推理→分数分布蒸馏 | T2I | A/F 层 | arXiv | ✅ |
| Dong et al. — Personalized Judge? (2406.11657) | 2024 arXiv | persona 评委 | 不可靠 | persona 反例 | arXiv | ✅ |
| Guerdan et al. — Rating Indeterminacy (2503.05965) | 2025 arXiv | 多标签验证框架 | 强制单选失真 | 评估 | arXiv | ✅ |
| Calderon et al. — Alternative Annotator Test (2501.10970) | 2025 | LOAO 假设检验 | 可替代性 | 契约 | web | ✅ |
| Jha et al. — Whose Gold? (2608.15980) | 2026 arXiv | 标注池条目级差异 | 23.6% 多数标签不同 | 动机 | arXiv | ✅ |
| Wang et al. — LLM-as-Judge in SE (2502.06193) | ISSTA 2025 | 7 方法×3 任务 | Pearson .81/.69 | SE，仅均值 | arXiv | ✅ |
| SWR-Bench (2509.01494) | 2025 arXiv | 3 专家×100 评审 | kappa .7–.87 | SE，仅 kappa | web | ✅ |
| Ouedraogo et al. — CoReEval (2510.16579) | 2025 arXiv | 可读性评委 | MAE/相关 | SE，仅均值 | web | ✅ |
| Reliability without Validity (2606.19544) | 2026 arXiv | 大规模评委评估 | 64–68% vs 72–75% | 契约 | web | ✅ |
| Dogah et al. (2607.13423) | 2026 arXiv | ChaosNLI 校准缺口 | — | 契约 | web | ✅ |
| Hsiao et al. — Verbalized Confidence Shift (2609.10996) | 2026 arXiv | 口头置信 vs logprob | 2025 后模型口头更好 | Q2 | arXiv | ✅ |
| Multi-Level Annotator Modeling (2605.13801) | 2026 arXiv | N vs K 权衡 | 3–5 人面板 | 面板规模 | web | ✅ |

仅由 Semantic Scholar 列出、未再核验的补充：*Predicting Median, Disagreement and Noise Label in Ordinal Word-in-Context Data*（COLING 2025 Workshops；序数分歧预测）、*STABLEVAL: Disagreement-Aware and Stable Evaluation of AI Systems*（2605.02122）、*Learning from Annotator Disagreement via Weighted Ensemble Optimisation*（Datenbank-Spektrum 2026，无 arXiv）。

## 7. 主要来源
arXiv 摘要页（各条目 ID 见表）；LeWiDi-2025 / NLPerspectives 议程；Semantic Scholar API（2 次成功查询）。Kohli 2605.29797 的摘要由本人 WebFetch 逐字核实。
