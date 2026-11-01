You are an experienced ICML area chair. Below are the full texts of research documents by one PhD student on LLM-as-judge, human disagreement and pluralistic alignment (paper 1 lives in another repository and is not included). Do NOT run any shell commands; everything you need is in this message. Papers: paper 2 (draft), paper 3 (early stage: protocol + first results), paper 4 (draft v0.9 + protocols of its running stages: Stage 8 = Community Alignment dataset, running; Stage 9 = a new method SAP, screened attribute personalisation, running — first fold-0 screening outputs: on synthetic panel t5 the injected length axis gets EB prior variance 0.036 vs ≤0.004 for the other 23 attributes; on sem5 hedging/refusal 0.040 and formatting 0.039; on real MultiPref length is top at 0.0073).
Answer candidly and specifically, citing sections:
(1) For each paper, a 3-line summary, your estimated probability of acceptance at the ICML main track as it stands, and its single biggest weakness.
(2) Which paper is most likely to be accepted at ICML, and why.
(3) For paper 4: is the novelty sufficient for ICML? Give the 3 most promising, concrete ways to increase its novelty that are feasible in about 2-4 weeks with frozen-embedding methods, CPU and at most one GPU, ranked by expected gain in acceptance odds; for each: what experiment would show it, what result would be needed, and how it changes the paper's framing. Also say whether SAP (Stage 9) is a sufficient method contribution, and what would make it one.


===== FILE: README.md =====
# LLM-J-ICML

Paper 2 of the LLM-as-a-Judge project — target venue ICML.
Working title: *Beyond Mode and Mean? What Disagreement Histograms Teach LLM Judges* (audit of distributional supervision for learned judges: statistic-preserving donor replacement with dose certificates, LoRA/heads experiments on 10 ordinal + ChaosNLI panels, and a learner-free finite-rater analysis).

Start here:
- `paper-2/phase2/SETUP_NEW_SERVER.md` — clone, data submodules, feature restore, environments, commands
- `paper-2/phase2/PAPER_DRAFT.md` → `paper-2/phase2/latex/main.pdf` — manuscript
- `paper-2/phase2/RESULTS_TABLES.md` — every result table (T2b heads, T3b/T3c LoRA, T5 ChaosNLI, T9 finite-rater)
- `paper-2/phase2/PROGRESS.md` — chronological log of decisions; `paper-2/phase2/reviews/` — external (Codex) review rounds
- `paper-2/REPORT.md`, `paper-2/lit-review/`, `paper-2/idea-stage/` — phase-1 report, literature review, idea discovery

Layout note: `code/code_readability/data` (Buse–Weimer, Scalabrino readability ratings) is shared data the panels load; paths are resolved by `paper-2/phase2/paths.py` relative to this repository root (override with `LLMJ_ROOT`).
Split off from the private working repository `JundaHe/ICSE2027-LLM-Judge` (branch `idea-discovery-2026-08-23`, commit 070876a) on 2026-10-25; history before that point lives there.


===== FILE: HANDOFF.md =====
# Paper 2 交接文档（HANDOFF）

> **2026-10-26 更新（新服务器 `/scratch/jundahe/LLM-J-ICML`，一天的密集实验之后）。** 下面第 0–9 节是 10-25 的原文；本节总结之后发生的事。细节以 `paper-2/phase2/PROGRESS.md`（逐条带时间）、`paper-2/phase2/reports/STORY_2026-10-26.md`、`reports/PRIOR_ART_CHECK_2026-10-26.md`、`reports/RELIABILITY_CARDS.md` 为准。
>
> **A. 关卡结果。** Gate D（残差从冻结表征解码）在 13 个有序/SE 面板上失败（|G| ≤ 6e-5；多层探针复检同样 ≈ 0），在 2 个名义面板 ChaosNLI 上通过（G = +0.0032 / +0.0043）。Gate H（heads 上的目标构造）失败：11 个面板上任何收缩/平滑目标相对原始直方图都在 ±0.0005 内、正负不定。Gate A（标注侧）：位置+形状收缩 shr2 相对原始直方图 −0.0048 [−0.0051, −0.0044]、相对纯位置目标 −0.0028；纯形状收缩相对纯位置目标 = 0（除 SummEval 外 λ̂ 只有 0.04–0.13）。机制分解（ordered-probit，13 面板）：位置之外主要是标注者阈值（ΔLL 0.05–0.16 / 评分），密集有序面板在精确众数均值之外没有可复现形状。固定预算：heads 11/11、LoRA 2/2（SummEval、POPQUORN）都是"固定预算下样本优先"；第二个标注者的边际价值因任务而异（SummEval ≈ 0，POPQUORN 约为差距一半）。一个登记的预测被证伪（ChaosNLI 上多标注者并未在固定预算下胜出）。
>
> **B. 论文故事（修订）。** judge 只能学到由文本决定的那部分分歧；有序打分任务上那部分只有位置，NLI 上包括形状。两个信度（跨标注者可复现 vs 跨文本可预测）、阈值机制、预算规则。它是 analysis + 决策规则论文，不是新方法论文；用户的决定：**ICML 路线 A 保留但 FSE/ACL 更匹配，由用户定；不做视觉 benchmark；SE 作为重点应用域**。新增 SE 面板：Dorn（360 × 161–267 人）、Crupi 2025（1,163 × 3）、JetBrains 2024（120 × 11–31）、Roy 2021、MLCQ（见 `data/SE_PANELS_SOURCE.md`）。
>
> **C. Paper 3（`paper-3/`，用户 10-26 批准）。** 实用方向 "Calibrating LLM judges to the people they stand in for"：G1 换标注者群体只重估阈值映射（DICES-990 种族/地区偏移 0.008–0.045，≥ 50 条评分追回 87–100%，优于通用校准 2–3 倍）；G2 黑盒 judge 分数 → 人类分布（零样本 judge 上映射胜过温度+混合 6/6；在本面板训练的 judge 上三者打平，但每人偏移仍有 0.005–0.015 收益）；G3 争议预测（映射推出的离散度 ≈ 直接问 LLM ≫ judge 自信度）。协议 `paper-3/PROTOCOL_CALIBRATION.md`（两次修订）。**等用户提供 paper 1 的前沿 judge 输出**做真正的黑盒 G2。
>
> **D. 基础设施（重要）。** 非 Slurm 进程被 cgroup 限在 4 核；一切重计算走 Slurm（`paper-2/phase2/slurm/run_cpu.sh`；normal QOS 每用户 16 核 / 64 GB；GPU 2 × RTX PRO 5000 72 GB；`--gres=gpu:1`）。BLAS 线程要限。LoRA adapter 权重已 ignore（`results/lora_budget/**/lora/`）。Codex CLI 已装未登录（需用户 `codex login`），本日所有审阅都没有 Codex 参与——这是下一步最该补的。
>
> **E. 未完成。** paper 2 的写作（§1–§3 按新故事重写、信度卡和预算图进正文）；Codex 审；G1/G3 第三轮结果；Dorn 经验列未解码（`experience.csv` 无表头，第 1 列疑为编程年限，未核实）；JetBrains 曲线、Roy conc/flu 信度在跑。

写于 2026-10-25，从旧服务器（`/mnt/hdd2/jundahe/LLM-J`）迁到本仓库 `JundaHe/LLM-J-ICML` 时。
**目标会议：ICML 2027**（截稿预计 2027 年 1 月下旬）。
本文档覆盖：做了什么、结果是什么、论文现在什么状态、下一步做什么、怎么在新服务器上接着做、有哪些规则和坑。

---

## 0. 一句话现状

审计实验（heads + 两个端到端 LoRA 数据集）和不训练模型的"有限标注者"分析（A+G）都已完成，论文能编译成 12 页。
Codex 的最新评估：新颖性约 7/10，ICML borderline（偏 weak reject）。
要冲 ICML，还差两件事，都在等用户拍板：

1. 解码实验：文本特征能否预测分歧形状；
2. 由分析推出的新方法：按可靠度收缩分布形状。

---

## 1. 研究故事线

**起点（paper 1，ICSE 2027 投稿）。** 在人类有分歧时，用"合并后的标签"评估 LLM judge 会产生假象（alignment mirage）。paper 1 管评估侧。

**paper 2 的问题（训练侧）。** Chen et al. (NeurIPS 2025) 等工作用人类的完整打分分布训练 judge，并把效果提升解读为"学会了人类分歧"。我们要问的是：这个提升到底来自分布里的哪部分？

**方法（审计，不是新训练方法）：保留统计量的供体替换。** 训练时，把每个样本的打分直方图换成另一个样本（供体）的直方图，同时保留接收样本的统计量。有三档：

| 档位 | 代码里的名字 | 做法 |
|---|---|---|
| 只保留众数 | `pmode`，LoRA 里叫 `perm_mode` | 只在众数相同的样本之间换 |
| 保留众数 + 均值区间 | `pmm`，LoRA 里叫 `perm` | 众数相同、均值在同一区间内的样本之间换 |
| 精确保留众数 + 均值 | `pmmx` | 换完后用 KL 投影回接收者的精确众数和均值 |

替换后 judge 变差 → 被换掉的那部分信息有用；不变 → 没用。
每个对比都附**剂量证书**：可替换比例、实际改动比例、被改动样本的 TV、全体样本的 TV、"换了等于没换"的配对数。
暂定方法名：**Transplant**（donor/recipient 的"移植"），还没最终确定。

**阶段转折（按时间）：**

1. **8 月 · phase 1**：在 SE 数据（commit message、可读性）上做，结果是 0 效果。
2. **10 月初 · phase 2 第一个赌注**：在输入里加标注者身份，看能否学到分歧。失败（Stage A，表 T6）。
3. **转向**：论文主线改为"用分布训练时 judge 实际只用到众数和均值"，并扩展到 10 个有序数据集和 3 个 ChaosNLI 类别数据集。
4. **10-12 · 用户决定删掉 commit 数据集**：理由是"大家标注得好不好不是我们的问题"。**以后永远不要再加回 commit。**
5. **10-23 · 第二个端到端数据集**：POPQUORN LoRA 跑完，复现了 SummEval 的结论。
6. **10-23 · A+G 有限标注者分析**：回答"0 效果是数据里没信号，还是模型没学会"。

---

## 2. 当前结果（论文里用的数字）

### 2.1 冻结特征 heads（表 T2b）
- Qwen2.5-7B 特征 + 小分类头，10 个有序数据集。
- `pmmx − soft` 的 RPS 变化在 −0.0024 到 +0.0006 之间，都接近 0。
- 只保留众数时，在若干数据集上变差，但不是每个都变差。
- 阳性对照（人为注入形状，看方法能否测出来）只在 Buse–Weimer 上成立（表 T4）。

### 2.2 端到端 LoRA judge（Qwen2.5-7B-Instruct，Chen 目标；表 T3b、T3c）

| 数据集 | perm − chen（保留众数 + 均值） | perm_mode − chen（只保留众数） | 替换剂量 |
|---|---|---|---|
| SummEval coherence（3 位专家依次留出） | −0.0001 [−0.0011, +0.0011] | +0.0120 [+0.0086, +0.0155]，9/9 格为正 | 改动 80.5–82.6%，TV 0.34–0.35 |
| POPQUORN offensiveness（3 个标注位置依次留出） | +0.0000 [−0.0009, +0.0009] | +0.0029 [+0.0009, +0.0050]，9/9 格为正 | 改动 69–72%，TV 0.30 |

- 设计：3 个优化器种子（各配一个替换种子）× 3 个 fold，交叉 bootstrap。
- **POPQUORN 的重要限制：** 数据加载器丢掉了标注者 ID，所以留出的是"一个打分位置"，不是"一个人"，测试评估者 100% 也出现在训练目标里。
  - 这不算泄露，因为模型看不到身份；但区间只对这批标注者成立。
  - 同时重抽样本和标注者后（`sensitivity_popquorn_users.py`）：perm − chen 区间是 [−0.0014, +0.0015]；perm_mode − chen 是 [−0.0004, +0.0065]，95% 区间含 0。
  - 论文第 4、6 节已经如实写明。

### 2.3 ChaosNLI 类别任务（表 T5）
- 打乱剩余形状（保留众数类和众数占比）会让 KL 变差：MNLI +0.016–0.029，SNLI +0.032–0.052。
- αNLI 只有 2 个类别，替换剂量为 0，作为实现检查。
- 和有序任务的差异只作描述，**不能**说成是标签结构导致的。

### 2.4 A+G 有限标注者分析（表 T9；不训练模型）
- 方案：`FINITE_RATER_PROTOCOL.md`，先冻结再跑，有 2 次修订，修订原因都写在文件里。
- 核心量 A1 = S(原始直方图) − S(只用众数、均值的对照)，用留出标注者打分；为负说明形状有用。
- 精确恒等式 A1 = M − 2X（X 是两组独立标注者之间形状的一致程度）：ρ = X/M > 1/2 时形状才有用。
- 两种对照：平滑对照 A1（预先指定的主指标）和精确保留众数、均值的对照 A1x（回答"众数、均值之外的形状"这个问题的主要证据）。

结果：
- **标注人少的有序数据集（5–9 人，8 个）：** A1x 全部为正（+0.0004 到 +0.0052）。原始直方图比"只用精确众数、均值"更差，ρ = 0.06–0.58。
- **标注人多的有序数据集（60–121 人）：** A1x ≈ 0。
- **ChaosNLI：** A1x ≈ −0.02，形状有用。
- **标注人数曲线：**
  - ChaosNLI 在 MNLI 8–10 人、SNLI 5–8 人时开始占优；
  - DICES-350、DICES-990 到 40 人都没有交叉点；
  - Buse–Weimer 在 20–30 人之间，从 20 人起区间就包含 0；
  - 参考组推算的交叉点：ChaosNLI 约 14–15 人，DICES 约 37–44 人。这只是模型推算的参考值。
- **预测检验（N = v/a, Δ = δ∞ + c/a）被证伪：** ChaosNLI 1/4、DICES 2/4、BW 3/4 被覆盖。论文**不能**声称理论临界人数。
- **A2（标注侧的供体替换）：**
  - SummEval coh/rel +0.0044/+0.0034，HelpSteer2 +0.0016，EmoBank +0.0018 为正，但训练出来的 judge 对同样替换约为 0。
  - 结论只能说"标注侧有信号，judge 没有表现出用上了它"，区分不了"从文本预测不出来"和"模型没学会"。解码实验就是用来区分这一点的。
- **两极分化调节分析（预先指定的次要分析）：** 零结果。有序合并 β = +0.00019 [−0.00131, +0.00169]；类别合并 β = +0.00288 [−0.00050, +0.00626]。

---

## 3. 论文现状

- **源文件和输出：** `paper-2/phase2/PAPER_DRAFT.md`，用 `build_latex.py` 生成 `latex/main.pdf`（12 页）。
- **已写进论文的：** POPQUORN 和 Codex 第 16 轮的措辞（含标注者限制、±0.001 等价区间是在 SummEval 上事后选的、全文不声称等价）。
- **还没写进论文的：** A+G（表 T9）和 Codex 第 18 轮建议的改写，都等用户同意：
  - 标题；
  - 摘要；
  - 正文放一张标注人数曲线图和一张"标注侧 vs judge"对照小表；
  - 完整 T9 放附录；
  - 正文写明预测检验失败。
- **标题候选：**
  - *Beyond Mode and Mean? What Disagreement Histograms Teach LLM Judges*（Claude 推荐）
  - *When Do Disagreement Histograms Teach Learned Judges? A Finite-Rater, Statistic-Preserving Audit*（Codex 建议）
  - 现在的标题：*Auditing Distributional Supervision for Learned Judges with Statistic-Preserving Label Randomization*
- **绝对不能声称的：**
  - 形状信息不存在 / 两种训练方式等价；
  - 从文本学不到形状；
  - 理论验证了临界人数；
  - 有序和类别的差异由标签结构造成；
  - 两极分化不重要；
  - "第一个在类内打乱软标签"（Behrens & Zdeborová 2026 已做过）；
  - "location carries the benefit"。
- **必须引用并讨论的相近工作**（详见 `novelty/NOVELTY_REPORT.md`）：
  - Gheibi & Ghazizadeh 2026；Behrens & Zdeborová ICLR 2026；Chen et al. 2025；Kohli 2026；Singh et al. 2025；
  - **Beyond Averages (EMNLP 2025)**：审稿人最可能拿它来问；
  - Pavlovic et al. 2026；Chen et al. 2026 "Stable Signal"；Kurniawan et al. CL 2025。

---

## 4. 下一步

需要用户点头的事项：

| 优先级 | 事项 | 资源 / 时间 | 说明 |
|---|---|---|---|
| 1 | **解码实验** | CPU，约半天 | 用冻结特征做交叉拟合的 ridge 回归，预测第一组标注者的形状残差（相对精确众数、均值对照），在独立的第二组标注者上评分（协方差，以及 2⟨r̂, r2⟩ − ‖r̂‖² 这个真实评分增益）；两组对称交换，在分组 bootstrap 里重新拟合，再做"同一众数、均值格子内打乱特征"的对照。先做 SummEval coh/rel。结果为正 → 信息在表示里、是训练没学到，这是论文缺的一环，Codex 认为有机会到 ICML weak accept。为负 → 只能说"这些特征线性解码不出来"。 |
| 2 | **新方法：按可靠度收缩形状** | 步骤 0–2 用 CPU，步骤 3 用 GPU | 训练目标 = q_T + λ·(h − q_T)，最优 λ* = X/M，由 A1 = M − 2X 直接推出，改善量为 X²/M。步骤：0 文献 + Codex 新颖性检查；1 标注侧验证；2 在 heads 上加一个对照组；3 有提升再跑 LoRA。风险：judge 本来就对形状不敏感，judge 侧的提升可能很小。 |
| 3 | 按 Codex 第 18 轮改写论文 | 约半天 | 等第 1、2 项有结果再一起改更省事 |
| 4 | SE 方向小实验（另一篇论文用） | CPU，1–2 天 | 用静态分析特征（职责覆盖、复杂度等）检验两件事：能否在 judge 分数之外更准地预测人类均分，能否预测共识层级。不属于 paper 2 |

其他事项：
- arXiv 版 paper 1 仓库（旧服务器 `paper-1/LLM-as-a-Judge-arxiv`）还有 2 个提交没 push，属于 paper 1，由用户决定。
- **建议顺序：** 1 → 2（步骤 0–2）→ 视结果决定 2（步骤 3）→ 3。

---

## 5. 在新服务器上开始

### 5.1 准备

```bash
git clone --recurse-submodules git@github.com:JundaHe/LLM-J-ICML.git
cd LLM-J-ICML
bash paper-2/phase2/restore_features.sh      # 拼回两个超过 100MB 而被拆分的特征文件
```

- **路径：** 由 `paper-2/phase2/paths.py` 自动推断仓库根目录，不用改代码。只有把 `paper-2/` 挪出仓库时，才需要设置 `LLMJ_ROOT`。
- **环境：** 详见 `paper-2/phase2/SETUP_NEW_SERVER.md`。
  - GPU / 训练 / 分析：`pip install -r paper-2/phase2/requirements-gpu.txt`（Python 3.12，torch 2.8，transformers 4.57.3，peft 0.19.1）。模型 `Qwen/Qwen2.5-7B-Instruct` 从 HF 下载。
  - 作图、表格、编译：`pip install -r paper-2/phase2/requirements-cpu.txt`，另外需要 `pandoc`、`pdflatex`、`bibtex`。
- **自检**（旧服务器上，在全新克隆里验证通过）：

```bash
cd paper-2/phase2
python check_consistency.py      # 应当 11/11 OK，0 unmatched
```

### 5.2 资源参考（旧服务器，A6000 级 46GB 显卡）
- POPQUORN 一个 LoRA 任务约 7.5–8 分钟，显存 16GB，27 个任务一张卡约 3.5 小时。
- SummEval 一个任务约 18 分钟。
- heads 和 A+G 只用 CPU；A+G 最慢的是 Buse–Weimer 曲线，约 4 小时。

### 5.3 常用命令（在 `paper-2/phase2/` 下运行）

```bash
python make_latex_tables.py && python make_figures.py && python build_latex.py   # 重建表格、图、PDF
python check_consistency.py                                                       # 正文数字 ↔ 实验结果
python manifest.py                                                                # 结果文件哈希清单
python finite_rater.py --panel <panel> [--ref | --loo --a2]                       # A+G
python finite_rater_summary.py                                                    # 生成 T9
PY=$(which python) bash lora_chain_popquorn.sh <gpu> 2000 2001 2002               # 重训 POPQUORN LoRA
python analysis_block_popquorn.py; python sensitivity_popquorn_users.py
```

### 5.4 没有放进仓库的
- **LoRA adapter 权重：** 每个约 150MB，可以重训；论文用到的预测结果都在仓库里。
- **`logs/` 和 `*.log`：** 例外是 LoRA 的 `train.log`，它在仓库里。
- **commit 数据集的特征和 pilot 大文件：** commit 已从论文删除。

---

## 6. 文件地图（`paper-2/phase2/`）

| 文件 | 内容 |
|---|---|
| `PAPER_DRAFT.md`、`latex/` | 论文 |
| `RESULTS_TABLES.md` | 所有结果表：T1 数据集；T2b heads；T3b/T3c LoRA；T4 阳性对照；T5 ChaosNLI；T6 Stage A；T7 G×R；T9 A+G |
| `PROGRESS.md` | 按时间顺序的完整工作日志和每个决定的原因（最权威的历史记录） |
| `reviews/` | Codex 第 1–18 轮审阅（prompt + 回复），以及新颖性咨询 |
| `novelty/NOVELTY_REPORT.md` | 新颖性检查（6.5/10）和 10-23 的文献补查 |
| `FINITE_RATER_PROTOCOL.md` | A+G 方案和 2 次修订 |
| `data_panels.py`、`targets.py`、`paths.py` | 数据加载、目标构造（KL 投影）、路径 |
| `train_judge_v3.py`、`lora_chain_*.sh` | LoRA 训练 |
| `probe_mean2.py`、`probe_nominal.py` | heads（有序 / 类别） |
| `analysis_block_*.py`、`sensitivity_popquorn_users.py` | LoRA 的冻结分析 |
| `finite_rater*.py` | A+G |
| `check_consistency.py`、`manifest.py` | 一致性检查、哈希清单 |
| `../idea-stage/`、`../lit-review/`、`../REPORT.md` | phase 1、文献综述（63 篇）、早期报告 |

---

## 7. 工作规则（用户的偏好和长期约定，请继续遵守）

1. **每完成一个原子步骤就 commit**，并 push 到 `origin main`。新结果都要提交，adapter 权重和日志除外。
2. **每个里程碑都发给 Codex 审**，用 CLI，不要用 MCP（旧的 token 已失效）。审阅存进 `reviews/`，并按意见修改。
   ```bash
   codex exec --model gpt-5.6-sol -c model_reasoning_effort=xhigh --sandbox read-only --skip-git-repo-check -o <绝对路径输出> - < <绝对路径prompt>
   ```
   prompt 文件写到 `reviews/codex_roundNN_prompt_<日期>.md`，在后台运行。
3. **先固定方案再看结果：** 新分析先写 protocol 并提交；看到结果后要改，只能在 protocol 末尾记修订，写明原因。
4. **如实汇报：** 结果不好也照实说。不夸大，不声称第 3 节列出的那些结论。
5. **永远不要重新加入 commit 数据集。**
6. **不要把 API key、token 写进任何文件。** GitGuardian 之前的告警已查过，是数据集文本里的 "password" 等误报，历史扫描为 0 个真实问题。
7. **GPU：** 旧服务器上要用别人或别的项目的卡，必须先得到用户明确同意。新服务器同理，先确认哪些卡可以用。
8. 用户用中文交流，汇报要简洁。

---

## 8. 已知问题和历史 bug（避免重犯）

- **向量匹配 bug（已修）：** 替换时曾按"评分向量"配对，导致 18–23% 的配对直方图其实相同。现在一律按"直方图类别"配对，并断言 `n_tv_zero = 0`。
- **阳性对照的注入方式（已修）：** 曾经在整行标注上注入，导致训练和评估子集里的众数、均值不再保持。现在按子集分别注入（`_v8`），只在 Buse–Weimer 上有效。
- **A+G 两次修订：**
  - Δ 一开始被误当成"形状信息"；
  - 在 loo 模式下所有样本留出同一个位置，让对照预测学到了那个标注者的偏好。
  - 两处都已修正并写进 protocol。
- **POPQUORN 的标注者身份问题：** 见第 2.2 节。以后用 POPQUORN 时，最好按真实 user_id 留出标注者，数据加载器可以重放随机种子来恢复 ID（见 `sensitivity_popquorn_users.py`）。
- **两个环境的包不同：** `finite_rater*.py` 在 GPU 环境下能跑（没用到 krippendorff）；作图需要 matplotlib（CPU 环境）。新服务器上也可以合并成一个环境，但要重新验证。

---

## 9. 给新服务器上 Claude 的起始提示（可直接复制）

> 你在继续 paper 2（目标 ICML 2027）。先读 `HANDOFF.md`，再读 `paper-2/phase2/PROGRESS.md` 的最后 40 行、`paper-2/phase2/RESULTS_TABLES.md` 的表 T3b/T3c/T9，以及 `paper-2/phase2/reviews/codex_round18_2026-10-23.md`。按 `HANDOFF.md` 第 5 节准备好环境，并运行 `check_consistency.py` 自检。遵守第 7 节的工作规则。然后用中文告诉我现状，并按第 4 节的优先级建议下一步；我同意之后再开始。


===== FILE: paper-2/phase2/PAPER_DRAFT_v2.md =====
# Five Raters Are Not a Distribution: What Learned Judges Can Learn from Human Disagreement, and Where to Spend the Annotation Budget

*Draft v2.2, 2026-10-27 — revised after the internal review and a numbers audit (all claims checked against results/; corrections logged in PROGRESS.md) (reviews/internal_review_v2_2026-10-26.md). All numbers previously marked [v2-pending] are now filled from the re-runs triggered by that review (decoding with the corrected bootstrap, results/decoding_v2/; same-batch LoRA budget block, results/lora_budget_v2/).*

## Abstract (draft)
Learned judges are increasingly trained on the full histogram of human ratings rather than on a single label, with the stated aim of learning how people disagree. We ask what part of such a histogram a text-conditioned judge can learn. We separate two properties that prior work conflates: whether the histogram's shape beyond its location (mode and mean) is *reproducible across raters*, and whether it is *predictable from the text*. On rating panels from 14 datasets — summarisation, offensiveness, politeness, helpfulness, sarcasm, valence, conversational safety, NLI, and seven software-engineering datasets including a 5,468-developer code-readability study — a learner-free split-half analysis finds the shape beyond mode and mean poorly reproducible on every ordinal panel: its split-half reliability stays between 0.04 and 0.41 with 4–8 raters and below 0.3 even with 40 raters on the dense panels, so the raw histogram never forecasts a new rater better than its own mode and mean. A cross-fitted decoding analysis finds that the frozen representations of three model families recover at most a few percent of the reproducible ordinal shape (upper 95 % bounds below 5 % on six of the eight ordinal panels with an informative interval — X distinguishable from zero and the G/X interval narrower than 20 points — and at most 10.2 % on all eight) but 17–26 % of the NLI shape. Learned judges behave accordingly: statistic-preserving replacement of the shape of 69–83 % of training targets changes LoRA judges by less than ±0.0011 RPS on two datasets, and alternative constructions of the per-item target change frozen-feature heads by at most a few thousandths of RPS in inconsistent directions, whereas discarding the distribution (one-hot targets) is worse on 10 of 11 panels. A rater–item decomposition of the panels with persistent rater identities shows that, beyond item location, rater-specific thresholds account for most of the held-out likelihood gain, while item-specific dispersion adds little. At a fixed number of ratings, frozen-feature judges improve with more items rather than more raters per item on most panels, and on SummEval end-to-end LoRA judges trained on one rating per item match those trained on seven (two base-model families) and beat judges trained on seven ratings for a seventh of the items, whereas on POPQUORN extra ratings per item help; the marginal value of further ratings on covered items is task-dependent. We release per-dataset disagreement reliability cards and the estimators.

## 1. Introduction

Human raters disagree, and a growing line of work trains learned judges — language models fine-tuned to score text — on the full distribution of human ratings rather than on a single aggregated label (Chen et al., 2025; Singh et al., 2025; Kohli, 2026; Benito-Santos & Ghajari, 2025). The appeal is clear: a histogram records which neighbouring levels received mass and how concentrated the ratings were, and a judge that reproduces it would "capture human disagreement" rather than average it away. The data behind that appeal are thin. In most datasets the histogram is computed from three to nine people. Five ratings of a summary's coherence are a sample from a population of possible raters, and a model trained to reproduce the sample exactly is, in part, trained to reproduce sampling noise.

This paper asks a question that the literature on learning from label variation (Uma et al., 2021; Plank, 2022) has not asked in this form: **which part of a few-rater histogram can a text-conditioned judge learn?** We decompose every histogram into its *location* (mode and mean) and the *shape beyond location* (the residual allocation of mass once mode and mean are fixed), and we measure two properties of the shape that are usually conflated:

1. **Reproducibility across raters.** If the same items were rated by a disjoint panel, would the shape come out the same? We estimate this learner-free with a split-half design: an exact identity, A1 = M − 2X, relates the forecasting value of the raw histogram to the magnitude M of its residual relative to an exact mode-and-mean comparator and the cross-panel agreement X of that residual; the ratio ρ = X/M is a split-half reliability of the shape at a given number of raters, and the raw histogram beats the comparator for predicting a new rater exactly when ρ > ½.
2. **Predictability from the text.** Even a reproducible shape is useless to a judge unless the text carries it. We fit a cross-fitted ridge decoder from a frozen LLM's representation to the panel-1 residual and score it on an independent panel-2 residual with a proper-score gain G, reported also as the fraction G/X of the reproducible shape, against a within-cell feature-permutation control and a positive control.

**Findings.** (i) *The shape beyond mode and mean is poorly reproducible on ordinal scales.* Its split-half reliability is 0.04–0.41 on eight panels with 4–8 raters per item (intervals include 0 on four), and with three raters the mode-and-mean cell determines the histogram outright (Crupi et al. (2025)'s code-summary benchmark, MLCQ, Roy et al.). On the dense ordinal panels it stays below 0.3 up to 40 raters (Buse–Weimer 0.22, DICES 0.25 and 0.15, Dorn's Java panel 0.29), so on no ordinal panel does the raw histogram forecast a new rater better than its own mode and mean. ChaosNLI is the contrast: the NLI shape's reliability exceeds ½ from two to three raters and reaches 0.96–0.98 at 40. (ii) *What is reproducible is mostly not in the text.* A cross-fitted linear decoder on frozen features, scored against an independent rater panel, recovers a fraction G/X of the reproducible shape whose upper 95 % bound is 0.2–0.4 % on SummEval, ≤ 0.4 % on POPQUORN offensiveness, ≤ 2 % on EmoBank and DICES-350, ≤ 4.6 % on DICES-990, ≤ 5.4 % on Dorn and ≤ 10.2 % on HelpSteer2 (CSC's G is ≈ 0 but its X interval covers 0, so no ratio is reported); on the six panels run in all three families (Qwen2.5-7B, Qwen3-8B, OLMo-2-7B) the families agree; on ChaosNLI MNLI it recovers 17–18 % in all three families (intervals [0.11, 0.19]) and 26 % on SNLI (Table 2). (iii) *Learned judges do not use the shape.* Replacing the shape of 69–83 % of training targets while preserving each target's exact mode and mean changes LoRA judges by −0.0001 [−0.0011, +0.0011] RPS on SummEval and +0.0000 [−0.0009, +0.0009] on POPQUORN (position-level bootstrap; user-level [−0.0014, +0.0015]), whereas destroying the location as well costs +0.012 and +0.003 (POPQUORN user-level interval [−0.0004, +0.0065]); the same intervention on ChaosNLI costs 0.016–0.052 KL. Across eleven ordinal panels and three feature families, training frozen-feature heads on the location-only comparator or on reliability-shrunk shapes changes held-out RPS by at most 0.0012 with mixed signs; other smoothing constructions move it by −0.005 to +0.009 in panel-dependent directions; one-hot targets are worse on 10 of 11 panels. A user-held-out replication on POPQUORN, where no evaluator contributes to any target, gives the same signs. (iv) *Beyond location, rating structure is mostly rater-side.* On the four panels with persistent rater identities, rater-specific cut-points improve held-out likelihood by 0.05–0.16 nats per rating while item-specific dispersion adds −0.017 to +0.012. This is consistent with — though it does not by itself prove — the reading that, on these panels, the shape a judge is asked to learn is largely a property of who rated. (v) *Budget.* At a fixed number of ratings, frozen-feature heads improve with more items rather than more raters per item on four of the five ordinal panels with more than 900 items and on both ChaosNLI panels (SummEval is flat; panels with ≤ 210 training items reverse). End-to-end LoRA judges trained on one rating per item match judges trained on all seven on SummEval (Qwen2.5, same batch, 3 seeds: −0.0027 [−0.0061, +0.0014]; OLMo-2: +0.0007 [−0.0056, +0.0069]) and beat judges trained on 144 × 7 by 0.023 / 0.0095 RPS; on POPQUORN (same-batch re-run) a single rating per item is worse than the full data, a second rating recovers about 60 % of that gap, and items-first is not supported. A prediction we registered — that multi-rater items would pay off at fixed budget where the shape is text-predictable — was falsified on ChaosNLI; we therefore do not derive the budget result from the mechanism and report the task-dependence of the marginal value of extra ratings as an observation.

**Contributions.** (1) Two reliabilities for disagreement — across raters and across text — with learner-free, cross-fitted estimators. (2) Disagreement reliability cards for every panel, telling a dataset builder whether the shape of disagreement is reproducible at the number of raters they can afford. (3) A rater–item decomposition of the ordinal structure beyond location. (4) Fixed-budget evidence, with frozen-feature heads in three model families and end-to-end LoRA judges, that covering items matters more than adding raters for training. The donor-replacement audit (§3) is the evidence that current training does not use the shape; shrinkage of the histogram survives as a tool for forecasting a new rater, not as a training method.

**What we do not claim.** That disagreement is noise (part of it is reproducible); that the text contains no residual information (we test linear decodability from three frozen model families); a theoretical rater-count threshold (a two-term 1/a model was falsified); a causal role of rater thresholds or of label structure in the ordinal–nominal difference; or a universal budget rule (Zhang, Gong & Choi (2021) find the opposite when a large single-label base already exists; see §5).

## 1b. Related work

**Learning from label variation.** Human label variation is increasingly treated as signal rather than noise (Aroyo & Welty 2015; Pavlick & Kwiatkowski 2019; Uma et al. 2021; Plank 2022), and soft-label training is reported to improve calibration and robustness (Peterson et al., 2019; Collins et al., 2022; Singh et al., 2025). For learned judges, Chen et al. (2025) train on human rating distributions; Kohli (2026) shows that on ChaosNLI the item-specific information in soft labels saturates around ten annotators for KL. These studies compare training targets; none separates the part of the histogram that is reproducible across raters from the part that is predictable from the input, which is the distinction our results turn on.

**Predicting disagreement.** Disagreement is partly predictable from text: NLI label distributions can be predicted to a degree (Zhou et al. 2022), reward models detect diverging preferences with AUROC around 0.6 (Zhang et al., 2025), and demographic information helps predict who disagrees (Wan et al., 2023). Our decoding analysis gives the matching quantity for the shape beyond mode and mean, normalised by its reproducible part, and finds the NLI and ordinal cases on opposite sides.

**Reliability of aggregates and rater effects.** Reliability of aggregated annotations depends on the number of raters (Wong & Paritosh, 2022); rater severity and scale use are classical facets in many-facet Rasch measurement (Linacre, 1989; Eckes, 2011). We use the split-half logic and the rater facet, but apply them to the shape beyond location and connect them to what a text-conditioned judge can learn.

**Annotation budgets.** Whether to label more items or relabel existing ones is an old question in crowdsourcing (Sheng et al., 2008; Lin et al., 2014); for hard-label classifiers, labelling many items once is preferable above a worker-quality threshold (Khetan et al., 2018). In NLP, Zhang et al. (2021) find the opposite on ChaosNLI: replacing a few thousand single-label items by a few hundred ten-label items reduces KL — in a regime where a large single-label base already exists and the evaluation targets the full distribution. Our budget results concern the complementary regime (every rating competes for items, ordinal quality ratings, judges trained only on the budgeted data), and on ChaosNLI we also observe a larger marginal value of a second rating than on ordinal panels; the two findings are consistent once the regime is stated.

## 2. Two reliabilities of a disagreement histogram

**Setting and notation.** Item $i$ has ratings on $K$ ordered levels from a panel of raters; the empirical histogram is $h_i$. For ordinal scales we score forecasts with the ranked probability score, $S(f,y)=\sum_k (F_f(k)-\mathbf 1[y\le k])^2/(K-1)$, and write $C$ for the cumulative operator; for nominal tasks (ChaosNLI) $S$ is the Brier score and $C$ the identity. The **location** of a histogram is its exact mode and mean (nominal: modal class and modal mass); the **shape beyond location** is what remains once these are fixed. To isolate it we use the *exact-T comparator* $q_T$ (Appendix A): a cross-fitted forecast built from other items in the same exact mode-and-mean cell (KL-projected onto the cell when the cell is sparse), so that $q_T$ has the same mode and mean as $h_i$ and differs from it only in shape. The residual of a histogram is $r = C(h - q_T)$.

**2.1 Reproducibility across raters (split-half reliability).** In each of $R$ repetitions the ratings of every item are split at random into disjoint panels $P_1$ (size $a$) and $P_2$. Writing $r_1 = C(h_1-q_T)$ and $r_2 = C(h_2-q_T)$, with $q_T$ computed from $P_1$, the forecasting value of the raw histogram over the comparator obeys the exact identity
$$A1 \;=\; \mathbb E\big[S(h_1,y)-S(q_T,y)\big]_{y\in P_2} \;=\; M - 2X,\qquad M=\|r_1\|^2/n,\; X=\langle r_1,r_2\rangle/n,$$
so $\rho = X/M$ is a split-half reliability of the shape and the raw histogram beats the location-only forecast exactly when $\rho>\tfrac12$. $M$ is the observed magnitude of the shape, $X$ its agreement with an independent panel's shape; $M-X$ is sampling noise. $\rho$ is specific to the number of raters $a$ and, as a ratio, unstable when $M$ is tiny; we report it with intervals and omit it where the residual is structurally empty (e.g. two or three ratings on a three-level scale). We also report the support of the donor-replacement intervention (the fraction of items whose histogram could be changed at all while preserving mode and mean). A smoother, response-based comparator that does not reproduce the noisy location gives larger values of $\rho$ because it also credits location reliability; we use the exact comparator throughout. Intervals are item-cluster bootstraps in which all copies of a resampled item stay in one cross-fitting fold and the comparator is refitted in every replicate. Table 1 gives the resulting *reliability cards*; Figure 1 traces $\rho$ and $A1^x$ against $a$ on the dense panels.

**2.2 Predictability from the text (decodability).** A judge sees the text, not the raters. Whether the reproducible shape is available to it is a separate question, which we answer with the representation the judges are built on: last-token hidden states of the frozen Qwen2.5-7B-Instruct (Qwen2.5-Coder for code panels) under the same rating prompt. A multi-output ridge decoder, group-cross-fitted over five item folds with a label-free PCA and a nested penalty, predicts $r_1$ from the features; it is scored on the *independent* panel $r_2$ by the covariance $V=\langle\hat r,r_2\rangle/n$ and by the proper-score gain
$$G \;=\; \big(2\langle \hat r, r_2\rangle - \|\hat r\|^2\big)/n \;=\; \mathbb E_{y\in P_2}\big[S(q_T,y) - S(q_T + C^{-1}\hat r,\,y)\big],$$
the exact reduction in score obtained by adding the decoded shape to the location-only forecast. Two controls accompany every estimate: a *within-cell permutation* of the features among items with the same exact mode and mean (which must drive $G$ to zero or below), and a *positive control* that predicts the panel-1 mean with the same pipeline (which must be clearly positive, else the representation or the alignment is broken). Directions are symmetrised ($P_1\leftrightarrow P_2$) and bootstrapped over item clusters. Because a single layer is a weak probe, we repeat the analysis with per-layer mean- and last-token features and greedy selection of the best layers (the probing recipe of Li et al., 2026).

**2.3 Why the two can come apart.** $\rho$ asks whether the shape is a property of the item's *rater population*; $G$ asks whether it is a property of the item's *text*. A shape can be reproducible yet invisible to text — for instance when it is produced by how particular kinds of raters use the scale — and a text-predictable shape can be unreliable with few raters. Section 4 shows that the first case is the ordinal norm. Nothing in §2.1 or §2.2 trains a judge; both are measurements of the data and the representation, and both are released with the reliability cards so that a dataset builder can compute them before deciding how many raters to pay for.

## 3. What learned judges use: the audit, condensed

If a judge learned the shape beyond location, destroying that shape in its training targets would hurt it. A donor-replacement audit (Appendix A gives the full design and tables) does exactly this with certified dose: for 69–83 % of training items the histogram is replaced by another item's histogram projected onto the recipient's exact mode and mean (mean TV 0.30–0.35 among changed items), under two learners. **End-to-end LoRA judges** (Qwen2.5-7B-Instruct, the distributional objective of Chen et al., 2025; three optimizer–assignment realisations × three held-out-rater folds) change by −0.0001 [−0.0011, +0.0011] RPS on SummEval coherence and +0.0000 [−0.0009, +0.0009] on POPQUORN offensiveness, whereas destroying the location as well (mode-only replacement) costs +0.0120 [+0.0086, +0.0155] and +0.0029 [+0.0009, +0.0050] with every seed-by-fold cell positive (POPQUORN intervals resample rating positions; resampling users instead widens them to [−0.0014, +0.0015] and [−0.0004, +0.0065]). **Frozen-feature heads** on ten ordinal panels move by −0.0024 to +0.0006. On the nominal ChaosNLI panels the same kind of intervention — scrambling the allocation of mass beyond the modal class while preserving the modal mass — raises test KL by 0.016–0.052 at every annotation count.

A stronger version of the same test asks whether *any* construction of the per-item target helps. We trained the heads on eleven ordinal panels with the raw histogram, the location-only comparator, reliability-shrunk shapes and locations, Dirichlet smoothing toward the mode prototype, label smoothing toward uniform and toward the marginal, and a cross-item smoothed comparator, thirty configurations each. The location-only comparator and reliability-shrunk shapes change held-out RPS by at most 0.0012 with mixed signs; the other smoothing constructions move it by −0.005 to +0.009 with signs that differ across panels; the one-hot target is worse on 10 of 11 panels (up to +0.010; Scalabrino −0.0013). The learner pools location across items on its own and shows no sensitivity to the per-item shape — what §2.2 leads one to expect for a shape that is not linearly decodable from its features. Learned judges on ordinal scales learn location and calibration; on NLI they also learn shape, because there the shape is in the text.

## 4. Where the ordinal shape comes from: a rater–item decomposition

The split-half analysis says the few-rater shape is mostly noise but not entirely (ρ > 0 with an interval excluding 0 on half of the small panels and on all dense panels at 40 raters); the decoding analysis says the reproducible part is not in the text. What is it, then? We fit three ordered-probit models to the rating matrices of the panels with persistent rater identities (Buse–Weimer, DICES-350, Scalabrino, the SummEval experts) and location-plus-dispersion models to the position panels: $Y^*_{ir} = \theta_i + \sigma_i\,\varepsilon_{ir}$ with cut-points $c_{r}$; **M0** item location with common cut-points, **M1** adding rater-specific cut-points (harshness), **M2** adding item-specific dispersion $\sigma_i$ (the inverse of IRT discrimination). Held-out log-likelihood over random cells, five folds, with the dispersion penalty chosen on held-out data.

Rater thresholds carry the structure: M1 improves held-out likelihood by +0.111 (BW), +0.146 (DICES-350), +0.156 (Scalabrino), +0.104 / +0.047 (SummEval coherence / relevance) nats per rating; item dispersion adds −0.017 (Scalabrino) to +0.012 and over-fits on the 5–7-rating position panels. Simulating rating matrices from the fitted models and re-running the split-half analysis closes the loop: at the split used for this check, the observed exact-T residual agreement on the dense ordinal panels is X ≈ 0 (BW −0.0001, DICES-350 +0.00003, DICES-990 +0.00002) and every model reproduces it; with 40 raters a small reproducible shape does remain (ρ = 0.22 [0.06, 0.35] on BW, 0.25 [0.19, 0.35] on DICES-350; Table 1), and we have not tested whether the threshold model reproduces it at that size. SummEval retains a small residual (X = +0.0018 / +0.0016) that neither thresholds nor one-dimensional dispersion reproduce, and it is precisely this residual that the decoder of §2.2 cannot read from the text. The mechanism is the textbook one of many-facet Rasch measurement (Linacre, 1989; Eckes, 2011), and we present it as measurement, not as a claim about raters' psychology; its consequence for judges is new: on the panels with persistent rater identities, most of the structure beyond location that a text-conditioned model is asked to learn is associated with who rated — information that is not in the item text.

The annotation side confirms the same picture from a different angle. For forecasting a new rater from an item's own ratings, shrinking both location and shape toward the mode prototype by their split-half reliabilities improves RPS by −0.0048 [−0.0052, −0.0045] over the raw histogram (eight panels, inverse-variance pooled; panels are not independent), a cross-item smoothed comparator by −0.0117 [−0.0123, −0.0112]; shrinking the *shape* alone by its reliability $\lambda=X/M$ beats the raw histogram (−0.0020 [−0.0022, −0.0019]) but is indistinguishable from the location-only comparator (pooled −0.0000 [−0.0000, +0.0000]) on every panel except SummEval and EmoBank, where $\hat\lambda\approx0.4$ (results/shrinkage/SUMMARY.md, corrected cluster bootstrap). For forecasting a new rater, what a few-rater histogram contributes beyond its location is small.

## 5. Spending the annotation budget

If the shape is unlearnable and the location is what the judge learns, then every rating after the first on the same item buys at most a less noisy location, while a rating on a new item buys a new point for the regression the judge is implicitly fitting. We tested this directly by holding the total number of ratings fixed and trading items for raters.

**Frozen-feature heads** (eight ordinal and two nominal panels, thirty configurations each; Table 5; CSC is excluded because its 32 conversation contexts leave fewer than the design's minimum of 20 training groups). On every panel with more than about 300 training items except SummEval, more items with fewer ratings each wins monotonically: on DICES-990 at a budget of 594 ratings, 594 items × 1 rating gives RPS 0.203, 297 × 2 0.205, 148 × 4 0.207, 74 × 8 0.213 and 40 × 15 0.219; POPQUORN, HelpSteer2 and EmoBank follow the same order, SummEval is flat. The direction reverses only on small item sets (Buse–Weimer with 60 training items, DICES-350 with 210), where a single rating per item is too noisy a target. The same items-first order holds on ChaosNLI (959 × 1: KL 0.226; 30 × 32: 0.323) — a result that falsified a prediction we had registered, namely that multi-rater items would pay off at fixed budget where the shape is text-predictable. They do not; where tasks differ is the *marginal* value of a second rating on already-covered items (ChaosNLI −15 %, ordinal heads −1 to −3 %), which we report as an observation.

**End-to-end LoRA judges** (Table 6). On SummEval coherence, with the Chen et al. objective and the three held-out-expert folds of §3, re-run in one batch with three optimizer seeds × three folds (SHRINKAGE_PROTOCOL Amendment 6; results/lora_budget_v2/), a judge trained on 960 items × 1 randomly chosen rating (960 ratings) matches the judge trained on all 960 × 7 = 6,720 ratings (−0.0027 [−0.0061, +0.0014], crossed bootstrap over seeds and test documents); 480 × 2 is equally good (−0.0040 [−0.0084, −0.0000]; vs 960 × 1: −0.0013 [−0.0073, +0.0039]), while 144 × 7 is worse than 960 × 1 by +0.0233 [+0.0176, +0.0285] — both prespecified readings ("one rating per item matches the full data", "items first") hold. An earlier two-seed block whose full-data reference came from a different batch had suggested that 960 × 1 *beats* the full data (−0.0061); the same-batch re-run does not support that stronger claim. (The earlier block also gave 240 × 4: +0.0162 and 960 × 2: −0.0064 vs full; these designs were not re-run.) On POPQUORN offensiveness, re-run in the same way (one batch, three seeds × three folds; SHRINKAGE_PROTOCOL Amendment 7), the picture differs: extra ratings per item help — 819 × 1 is +0.0087 [+0.0054, +0.0122] worse than the full 5,733-rating data and 819 × 2 recovers 62 % of that gap (819 × 2 − 819 × 1 = −0.0054 [−0.0084, −0.0027]) — and at 819 ratings, 819 × 1 and 117 × 7 cannot be distinguished (117 × 7 − 819 × 1 = +0.0022 [−0.0029, +0.0072]); of the three prespecified readings only "a second rating helps" holds. (An earlier two-seed block with a cross-batch reference had suggested an items-first ordering here as well; it is superseded.) The decisive part replicates on a non-Qwen base: with OLMo-2-7B on SummEval, 960 × 1 matches the full data (+0.0007 [−0.0056, +0.0069]) and 144 × 7 is worse than 960 × 1 by +0.0095 [+0.0022, +0.0160] (results/lora_budget_olmo/summary_vs_a1_F1.0.md); one versus two ratings per item is a tie on both bases. Single-rating training behaves like stochastic label sampling (Gheibi & Ghazizadeh, 2026) and is consistent with the many-once-over-few-many results for hard-label classifiers (Khetan et al., 2018; Lin et al., 2014); our contribution is the demonstration with distributional targets and end-to-end LLM judges, and the explanation of §§2–4 for why the raters' side of the budget buys so little.

**Rule.** For training a judge on an ordinal rating task, do not buy many ratings for few items: on large item sets frozen-feature heads always and LoRA judges on SummEval preferred more items, and nowhere did seven ratings on a seventh of the items beat one rating on all of them; a second rating per item is worth between nothing (SummEval) and about 60 % of the single-rating gap (POPQUORN, where covering items first was not better than seven ratings on a seventh of them), and further ratings less. Raters belong where a reliable reference distribution is itself the deliverable — evaluation sets, and tasks such as NLI where the shape is in the text.

## 6. Software-engineering panels

Readability, summary quality and code-smell severity are rated on the same few-rater scales, and the same questions arise for code judges. Dorn's readability study (360 snippets in Java, Python and CUDA; 161–267 developers per snippet) gives the densest ordinal panel we know of; its reliability curve matches Buse–Weimer and DICES: the shape beyond mode and mean reaches a split-half reliability of only 0.2–0.3 even with 40 developers per snippet (Figure 1). The LLM-judge validation benchmarks of the field have three raters per item — Crupi et al.'s code summaries, MLCQ's smell severities, Roy et al.'s summaries — and with three raters the mode-and-mean cell determines the histogram: there is no shape to learn or to evaluate (support 0 %). Scalabrino's nine-rater panel sits in between (Table 1). Decoding from frozen features recovers none of it at a precision that matters: G/X is +0.03 [−0.03, +0.05] on Dorn's readability panel (360 snippets), negative on Scalabrino (G < 0, a small over-fitting penalty on 124 snippets; its X interval covers 0, so no ratio is reported), and uninformative on Buse–Weimer (+0.07 [−0.07, +0.26], 100 snippets) and JetBrains naming (+0.01 [−0.37, +0.03], 120 identifiers) (results/decoding_v2/). For SE human studies the practical reading is that three to five raters per artifact fix its location and nothing else, and that adding raters to a few artifacts does not make the shape of developer disagreement reproducible on these readability and quality scales.

## 7. Limitations

Base models: all frozen-feature results (decoding, target construction, fixed budget) replicate on Qwen3-8B and on the non-Qwen OLMo-2-7B (Table 2: ordinal G/X intervals include 0 on all six three-family panels with upper bounds ≤ 10.2 %, ChaosNLI MNLI G/X 0.17 / 0.18 / 0.18 in Qwen2.5 / Qwen3 / OLMo-2; budget orderings agree except HelpSteer2 on OLMo-2, where 1436 × 2 edges out 2870 × 1 by 0.0007; target-construction contrasts agree in sign except one-hot, whose cost differs by up to 0.009 across families), and the end-to-end budget result replicates with an OLMo-2-7B LoRA judge on SummEval (the audit's LoRA blocks remain Qwen2.5-only); frozen-feature heads for breadth, end-to-end judges on two datasets; linear decoders — we re-tested with per-layer features and greedy layer selection, not with non-linear or fine-tuned probes; SummEval's small unexplained residual; POPQUORN's position folds (a user-held-out check with real user ids, evaluators never in any target, confirms the four conclusions on offensiveness and politeness: mode+mean-preserving replacement −0.00004 / +0.00024 (the latter three SEMs above zero, but two orders of magnitude below the mode-only cost), mode-only +0.0022 / +0.0029, one-hot +0.0042 / +0.0050, 4 ratings on a quarter of the items +0.0042 / +0.0030 worse than 1 rating on all); one registered prediction falsified and reported; effect sizes in the third decimal of RPS, to be read against the mode-only penalty of +0.012 and the budget effects of +0.02. We make no claim that disagreement is noise, that text contains no residual information, that a theoretical rater count exists, or that label structure causes the ordinal–nominal difference.


===== FILE: paper-3/PROTOCOL_CALIBRATION.md =====
# Paper 3 — Calibrating LLM judges to the people they stand in for: protocol (frozen before any result)
Committed 2026-10-26 after the user's go-ahead ("好，那我们先这么做吧"). Builds on paper 2's findings (paper-2/phase2/reports/STORY_2026-10-26.md): on ordinal rating tasks a text-conditioned judge learns the item's location; the structure beyond location is mostly rater thresholds (harshness), a property of the people, not the text. Scope: deployment-level questions, no new training objective, no theory beyond the ordered-probit mapping. SE framing (review-team standards) with NLP panels as replication. Rules of HANDOFF §7 apply (protocol before results, honest reporting, atomic commits).

## The mapping used throughout
A judge produces a continuous score s(x) for item x (a head's expected rating; a black-box judge's score; an LLM's expected score from its token distribution). A **panel map** turns s into the rating distribution of a target pool P of raters: ordered probit with location θ = α_P + β_P · s and pool cut-points c_P (K − 1 increasing; per-rater cut-points c_r shrunk toward c_P when the rater has ≥ 5 ratings). Fitted by penalised maximum likelihood on the ratings of pool P on **calibration items** (never test items). The map has K + 1 parameters per pool; the judge is untouched. Implementation detail fixed before any real run (after a 1-configuration smoke test showed 4-parameter maps over-fitting 10–20 ratings): a pool-B map is shrunk toward the pool-A map with a quadratic penalty (weight 1 in parameter units), so with little pool-B data it stays near the pool-A map and moves as evidence accumulates; the generic calibration baseline keeps its grid search.

## G1 — pool adaptation (does a judge trained on pool A need retraining for pool B?)
Panels (rater identity + metadata available): DICES-350 (gender, race, age, education), DICES-990 (+ locale), POPQUORN offensiveness/politeness (gender, race, age, education, occupation), SummEval coherence (3 persistent experts vs the crowd positions), Buse–Weimer (no metadata: random rater halves as the null pool shift), MLCQ (26 reviewers: individual reviewers as pools), Dorn (experience groups once the experience columns are decoded; otherwise omitted).
Pools: for each metadata variable with ≥ 2 groups of ≥ 10 raters, pool A = the largest group, pool B = each other group; plus the random-halves null on every panel.
Design per (panel, A → B): group-disjoint item split 60/10/30 (train/calib/test, 3 splits) × 5 seeds. The judge = frozen-feature head (probe_shrink.py machinery) trained on pool A's ratings of the training items (soft target over pool A's raters). Arms evaluated on pool B's ratings of the test items (RPS to each rater, averaged; and RPS of the predicted distribution to the pool-B histogram):
- **none**: the head's own distribution;
- **map-A**: panel map fitted on pool A's calibration ratings (controls for the map itself);
- **map-B(n)**: panel map fitted on n ∈ {10, 20, 50, 100, all} pool-B ratings drawn from the calibration items;
- **dir-B(n)**: generic post-hoc calibration of the head's distribution on the same n pool-B ratings (temperature + Dirichlet/climatology mixture, the T2b calibration map) — the fair generic baseline;
- **oracle-B**: head trained on pool B's ratings of the training items (upper reference);
- **rater-B(n)**: per-rater cut-points for pool-B raters with ≥ 5 calibration ratings (individual prediction).
Prespecified reading: a *pool shift* exists when none − oracle-B > 0 with a 95 % interval (crossed bootstrap over seeds and test groups) excluding 0; **adaptation works** when map-B(n) closes ≥ 50 % of that gap at n ≤ 50 and beats dir-B(n) at the same n. The random-halves null must show no shift (none ≈ oracle) — otherwise the instrument is biased. Report every panel/group; no selection.

## G2 — black-box judge → human distribution
Judges: (a) the frozen model's zero-shot score distribution Q0 (features/<panel>/*.npz; weak judge available on every panel); (b) paper 1's released judge scores on Crupi and Scalabrino (GPT-5.5, Claude Opus 4.8, Gemini 3.1 Pro, Mistral Large, GPT-4-turbo) once copied; (c) the paper-2 LoRA judges on SummEval/POPQUORN (chen, full data) as "trained judge" references. s = expected score (a, c) or the reported score (b).
Arms (fitted on calibration items' ratings, evaluated on test items vs held-out raters, leave-one-rater-out where identities persist, as in paper 1's CSJE): judge's own distribution (a, c only); temperature scaling; Dirichlet/climatology mixture; **panel map**; panel map + per-rater cut-points. Metric: RPS (ordinal) against held-out ratings; also the HCA-style human-ceiling comparison of paper 1 for the SE panels. Prespecified reading: the panel map must beat temperature scaling and the Dirichlet mixture at equal calibration data to be claimed; otherwise it is reported as equivalent.

## G3 — which items will people disagree on?
Targets: observed dispersion of the held-out raters' ratings per test item (variance; and the "contested" indicator = range ≥ 2 on a 5-point scale, as paper 1's Low stratum). Predictors, each a single number per item: (i) judge confidence (entropy / max-prob of the judge's own distribution); (ii) **map-implied dispersion** (variance of the panel-map distribution at s(x) — large when θ sits between cut-points); (iii) a direct LLM question ("how much would annotators disagree about this item?", 1–5; frozen Qwen2.5-7B-Instruct zero-shot, GPU via Slurm; and one frontier judge if paper 1's outputs include it); (iv) paper 2's decoded residual dispersion (ridge from features; Amendment 2(b)). Metrics: Spearman with observed dispersion; AUROC for the contested indicator; item-cluster bootstrap. Prespecified reading: (ii) ≥ (i) is the hypothesis; (iii) is the practitioner's default to beat; no claim beyond the per-panel numbers.

## Deliverables
paper-3/pools.py (identity-preserving long-format loaders with metadata), paper-3/pool_adapt.py (G1), paper-3/judge_map.py (G2), paper-3/contested.py (G3), results in paper-3/results/, reports in paper-3/reports/. Every result committed with its protocol version; amendments appended below with reasons.

## Forbidden statements
"Raters of group X are harsher" as a social claim (report threshold estimates as panel properties of this dataset's raters only); any claim that adaptation makes judges "fair"; any use of demographic groups other than as pre-registered pool-shift instances; no commit-message datasets.

## Amendments
**Amendment 1 (2026-10-26 10:40, after the first full G1 sweep; reports/G1_SUMMARY.md).** Observed: with n = 20 pool-B ratings the 4-parameter map over-fits on most rows (+0.004 … +0.019 RPS vs none) even with the quadratic prior, while with n ≥ 50 it recovers 65–100 % of the large shifts (DICES-990 race/locale) and beats generic calibration by 0.006–0.028. Change: for n < 50 only the location offset α is re-estimated (1 parameter; slope and cut-points inherited from map-A); for n ≥ 50 the full map with the prior, as before. Also recorded: for small pools (n_B ≤ 30 raters) the oracle head trained on pool B is often worse than the pool-A head, so "gap" is undefined there and the arms are compared against `none` only. The sweep is re-run with the amended rule; the first-sweep results are kept in results/pool_adapt_v1/.
**Amendment 2 (2026-10-26 12:30, after the v2 sweep).** Observed: offset-only maps at n = 20 still cost 0.002–0.009 on null/small-shift rows. Change: the small-n offset is shrunk toward map-A's offset with weight n/(n + 50) (empirical-Bayes prior strength n0 = 50 ratings; fixed, not tuned). v2 results kept in results/pool_adapt_v2/. G3: a second 'contested' indicator (dispersion in the top quartile of the split's test items) is added because range ≥ 2 is ~always true on 60–121-rater panels; the direct-LLM question (Qwen2.5-7B-Instruct, decoding-free expected value) is included as predictor (iii).


===== FILE: paper-3/reports/G1_SUMMARY_v2.md =====
# G1 pool adaptation — summary (RPS; vs none = arm − none, negative is better; gap = none − oracle-B, positive = a pool shift the head trained on A did not capture)

```
        panel             var                                      poolB  nA  nB   none     gap  gap_sem  map-B(20)  map-B(50)  map-B(all)  dir-B(50)  dir-B(all)  recover_map50  recover_dir50  map_minus_dir_all
           bw           group                                      cs101  43  10 0.1716  0.0072   0.0014     0.0039    -0.0012     -0.0019    -0.0029     -0.0032         0.1650         0.4081             0.0013
           bw           group                        cs216-Prog_Data_Rep  43  22 0.1607 -0.0058   0.0013     0.0070     0.0057      0.0037    -0.0006     -0.0000            NaN            NaN             0.0037
           bw           group                                   cs414-OS  43  18 0.1621 -0.0013   0.0008     0.0042     0.0039      0.0035    -0.0005     -0.0008            NaN            NaN             0.0043
           bw           group                       cs445-Intro_Graphics  43  13 0.1627  0.0003   0.0010     0.0082     0.0024      0.0021    -0.0004     -0.0009        -7.0538         1.1209             0.0030
           bw          random                                     random  60  61 0.1656 -0.0013   0.0010     0.0063     0.0025      0.0012     0.0003     -0.0022            NaN            NaN             0.0034
        dices          random                                     random  52  52 0.2227  0.0021   0.0012     0.0056     0.0012     -0.0035    -0.0001     -0.0038        -0.5929         0.0283             0.0003
        dices       rater_age                                     gen x+  49  27 0.2306 -0.0002   0.0013     0.0042    -0.0012     -0.0035    -0.0037     -0.0042            NaN            NaN             0.0007
        dices       rater_age                                  millenial  49  28 0.2160 -0.0003   0.0010     0.0207     0.0073     -0.0006     0.0021     -0.0010            NaN            NaN             0.0004
        dices rater_education                       High school or below  64  33 0.2303 -0.0008   0.0018     0.0110     0.0014     -0.0030    -0.0016     -0.0024            NaN            NaN            -0.0007
        dices    rater_gender                                        Man  57  47 0.2210  0.0000   0.0007     0.0116     0.0013     -0.0027    -0.0013     -0.0030            NaN            NaN             0.0003
        dices      rater_race                   Asian/Asian subcontinent  25  21 0.2364  0.0045   0.0015     0.0061    -0.0035     -0.0080    -0.0054     -0.0081         0.7631         1.1957             0.0000
        dices      rater_race                     Black/African American  25  23 0.2207  0.0018   0.0009     0.0056     0.0005     -0.0040    -0.0007     -0.0039        -0.2727         0.3742            -0.0001
        dices      rater_race LatinX, Latino, Hispanic or Spanish Origin  25  22 0.2273  0.0079   0.0013     0.0051     0.0007     -0.0052     0.0009     -0.0015        -0.0837        -0.1091            -0.0037
        dices      rater_race                                Multiracial  25  13 0.2622  0.0179   0.0009    -0.0123    -0.0191     -0.0234    -0.0161     -0.0185         1.0649         0.8995            -0.0049
     dices990          random                                     random  86  86 0.1933  0.0025   0.0007     0.0023     0.0032     -0.0021     0.0025     -0.0008        -1.2972        -1.0286            -0.0013
     dices990       rater_age                                     gen x+  98  43 0.1788  0.0005   0.0004     0.0042     0.0041      0.0013     0.0023      0.0006        -8.6270        -4.7616             0.0006
     dices990       rater_age                                      gen z  98  31 0.2083  0.0011   0.0004     0.0044     0.0019     -0.0024     0.0016      0.0000        -1.8321        -1.5437            -0.0024
     dices990 rater_education                       High school or below 152  20 0.1717  0.0029   0.0005     0.0145     0.0015     -0.0017    -0.0002     -0.0011        -0.5369         0.0856            -0.0006
     dices990    rater_gender                                        Man  88  82 0.1952  0.0004   0.0002     0.0088     0.0065     -0.0002     0.0029     -0.0006       -14.9626        -6.7391             0.0004
     dices990    rater_locale                                         US  92  80 0.1824  0.0160   0.0007    -0.0122    -0.0105     -0.0154    -0.0046     -0.0098         0.6527         0.2863            -0.0055
     dices990      rater_race                   Asian/Asian subcontinent  65  53 0.2030  0.0082   0.0003     0.0026    -0.0043     -0.0079    -0.0037     -0.0060         0.5233         0.4513            -0.0019
     dices990      rater_race                     Black/African American  65  11 0.2210  0.0104   0.0003    -0.0017    -0.0054     -0.0119    -0.0060     -0.0093         0.5228         0.5766            -0.0026
     dices990      rater_race LatinX, Latino, Hispanic or Spanish Origin  65  16 0.1708  0.0446   0.0018    -0.0401    -0.0430     -0.0452    -0.0133     -0.0171         0.9637         0.2988            -0.0281
     dices990      rater_race                                      White  65  27 0.1752  0.0352   0.0006    -0.0254    -0.0306     -0.0352    -0.0110     -0.0150         0.8693         0.3119            -0.0202
popquorn_off8             age                                      18-24  36  31 0.1301  0.0081   0.0009     0.0075    -0.0014     -0.0040     0.0041      0.0041         0.1778        -0.5073            -0.0081
popquorn_off8             age                                      25-29  36  25 0.1205  0.0058   0.0010     0.0029    -0.0060     -0.0062     0.0005     -0.0008         1.0288        -0.0876            -0.0054
popquorn_off8             age                                      30-34  36  30 0.1314  0.0035   0.0010    -0.0021    -0.0076     -0.0102    -0.0060     -0.0072         2.2050         1.7199            -0.0030
popquorn_off8             age                                      35-39  36  31 0.1267  0.0069   0.0013    -0.0011    -0.0092     -0.0109     0.0016     -0.0023         1.3416        -0.2334            -0.0086
popquorn_off8             age                                      40-44  36  23 0.1422 -0.0039   0.0008     0.0021     0.0004     -0.0017    -0.0006     -0.0010            NaN            NaN            -0.0007
popquorn_off8             age                                      45-49  36  22 0.1278 -0.0070   0.0010     0.0046    -0.0002     -0.0028     0.0017     -0.0009            NaN            NaN            -0.0019
popquorn_off8             age                                      50-54  36  20 0.1328 -0.0112   0.0022     0.0060     0.0033      0.0027     0.0031      0.0034            NaN            NaN            -0.0007
popquorn_off8             age                                      60-64  36  15 0.1570 -0.0063   0.0018     0.0046    -0.0021     -0.0030     0.0006      0.0013            NaN            NaN            -0.0042
popquorn_off8             age                                        >65  36  29 0.1466 -0.0032   0.0013     0.0045     0.0007     -0.0011     0.0051      0.0039            NaN            NaN            -0.0050
popquorn_off8       education                            Graduate degree 121  50 0.1495 -0.0022   0.0008     0.0021     0.0004     -0.0010     0.0020      0.0009            NaN            NaN            -0.0019
popquorn_off8       education          High school diploma or equivalent 121  80 0.1253  0.0008   0.0005     0.0054     0.0022     -0.0008     0.0021      0.0002        -2.7088        -2.6452            -0.0011
popquorn_off8          gender                                        Man 131 124 0.1307 -0.0011   0.0002     0.0045     0.0038      0.0002     0.0037      0.0007            NaN            NaN            -0.0005
popquorn_off8      occupation                                  Homemaker 127  12 0.1275 -0.0064   0.0012     0.0026     0.0049      0.0031     0.0036      0.0019            NaN            NaN             0.0012
popquorn_off8      occupation                                    Retired 127  29 0.1338 -0.0052   0.0008     0.0018     0.0001     -0.0024     0.0045      0.0012            NaN            NaN            -0.0037
popquorn_off8      occupation                              Self-employed 127  34 0.1304 -0.0053   0.0007     0.0024     0.0024     -0.0007     0.0008     -0.0003            NaN            NaN            -0.0004
popquorn_off8      occupation                                    Student 127  20 0.1252 -0.0090   0.0007     0.0038     0.0027      0.0013     0.0027      0.0011            NaN            NaN             0.0002
popquorn_off8      occupation                                 Unemployed 127  34 0.1190 -0.0048   0.0009     0.0022     0.0031     -0.0001     0.0005      0.0009            NaN            NaN            -0.0010
popquorn_off8          random                                     random 131 131 0.1300  0.0005   0.0003     0.0068     0.0030      0.0001     0.0036      0.0007        -6.2932        -7.7473            -0.0006
popquorn_pol5       education                            Graduate degree 237  97 0.1378 -0.0041   0.0007     0.0032     0.0026      0.0001     0.0021      0.0011            NaN            NaN            -0.0011
popquorn_pol5       education          High school diploma or equivalent 237 151 0.1333 -0.0005   0.0004     0.0022     0.0014     -0.0019     0.0018      0.0003            NaN            NaN            -0.0022
popquorn_pol5       education                                      Other 237  11 0.1083 -0.0310   0.0013     0.0044     0.0051      0.0030     0.0006     -0.0002            NaN            NaN             0.0032
popquorn_pol5          gender                                        Man 254 236 0.1355  0.0013   0.0003     0.0068     0.0005     -0.0021    -0.0000     -0.0013        -0.3519         0.0217            -0.0008
popquorn_pol5          gender                                 Non-binary 254  13 0.1282 -0.0200   0.0016     0.0015    -0.0014     -0.0024     0.0008     -0.0002            NaN            NaN            -0.0022
popquorn_pol5          random                                     random 253 253 0.1321 -0.0000   0.0002     0.0007     0.0024     -0.0006     0.0011      0.0001            NaN            NaN            -0.0006
```


===== FILE: paper-4/PAPER4_DRAFT.md =====
# What Personalised Reward Models Learn About a New Rater: Scale Use, and a Detection Limit for Content Preferences

*Draft v0.9, 2026-11-01 — paper 4 (ICML target). Every number is copied from a committed artefact (paper-4/results/STAGE1_REPORT.md, STAGE2A_REPORT.md and the files they cite); protocols (incl. PROTOCOL_STAGE7.md): PROTOCOL_STAGE1.md (Amendments 1–2), PROTOCOL_STAGE2.md (Amendments 1–10), PROTOCOL_STAGE2B.md (Amendments 1–4), PROTOCOL_STAGE2C.md (Amendments 1–5), PROTOCOL_STAGE3.md (Amendments 1–5), PROTOCOL_STAGE4.md (Amendments 1–2), PROTOCOL_STAGE5.md (Amendments 1–3). Revised after an external-style review and two independent numbers audits and a second review (positive control added).*

## Abstract (draft)
Personalised reward models are meant to learn how individual people judge model outputs. We test what they learn about raters they have never seen, with one protocol on three multi-rater datasets (MultiPref, DICES, PRISM): k of a new rater's ratings for adaptation, held-out items for evaluation, and a permutation control that compares a rater's own adapted parameters with another rater's. Across group-conditioned, low-rank, published (VPL, PAL, LoRe), in-context and fine-tuned personalisation, what transfers to a new rater is scale use: a text-independent baseline with two identifiable offsets per rater gains 0.08–0.10 nats per rating at k = 20 on all three datasets, is matched only by a tuned low-rank latent, and loses its gain on binary labels, as do all methods (at most 0.002 nats). No method improves which response a new rater prefers: on MultiPref and on 41,199 native PRISM choices, every method's gain over its unpersonalised version has an upper 95 % bound below one point. The null also holds for raters seen in training with all their ratings. A semi-synthetic positive control bounds what it can mean: with the injected content direction inside their inputs, the best of these methods detect a preference worth +10 points of direction accuracy to an oracle but not one worth +5, whereas a learner told the content features recovers about 60 % of the +5-point preference from the same 20 ratings, so the ratings suffice and finding the dimension is what fails. We recommend graded labels, a permutation control, separate calibration and ranking metrics, and a scale-use baseline.

## 1. Introduction
Reward models and LLM judges are trained on human ratings that disagree. A recent line of work treats this disagreement as signal to be modelled rather than noise to be averaged: distributional preference learning estimates a distribution over each alternative's utility rather than a point score (Siththaranjan et al., 2024); jury learning predicts individual annotators from content, annotator and demographic-group embeddings (Gordon et al., 2022), and large datasets such as PRISM are analysed by sociodemographic group (Kirk et al., 2024); personalised reward models learn a per-user latent, inferred for a new user from a few examples (Poddar et al., 2024; Chen et al., 2025). The pluralistic-alignment agenda (Sorensen et al., 2024) makes the representation of individual and group differences a first-class goal.

What these models learn about a person is rarely tested directly. Evaluations typically use synthetic users whose preferences differ by construction, binary preference labels, or users seen in training. We ask a simple question under a common protocol on real raters: **given k ratings from someone the model has never seen, how much better can it predict their other ratings — in particular, which response they prefer — and what is it that it learns?** The answer we find is that the methods learn calibration, not ranking — and a semi-synthetic positive control shows how strong a rater's content preferences would have to be before they learn ranking.

Measurement theory suggests a candidate answer that reward modelling largely ignores: raters differ in **how they use the response scale** — some say "clearly better" where others say "slightly better", some rarely call a tie, some are harsher across the board (Linacre, 1989; Baumgartner & Steenkamp, 2001). Such response styles are text-independent, cheap to estimate, and invisible to models that condition only on content or demographics. We make them a reference point for calibration. Because they are text-independent they barely change which response a rater is predicted to prefer (only through asymmetric "clearly"/"slightly" mass); a personalised reward model that learns content preferences should therefore show its value in ranking, and a model whose likelihood gain does not exceed the scale-use offsets has not shown that it learns more than scale use.

**Contributions.** (1) A new-rater evaluation protocol for personalised reward models — held-out raters and items, k-shot adaptation, a permutation control (own versus another rater's adapted parameters) — and a scale-use baseline (a few text-independent offsets per rater; two identifiable on two-sided preferences) that plugs into any graded reward model (§4–5). (2) A systematic test on three datasets of group-conditioned, low-rank, published (VPL, PAL, LoRe), in-context and fine-tuned personalisation: what transfers is scale use, which is calibration rather than ranking and disappears on binary labels (§5–6). (3) A detection-limit analysis: a semi-synthetic positive control with a well-specified reference learner and linear probes of each method's inputs show how strong a content preference must be for these methods to find it, and that the limit lies in finding the content dimension rather than in the number of ratings; on MultiPref, annotators' own aspect labels show that value conflicts — where individual trade-offs could change a ranking — occur in 4 % of comparisons (§5.6–5.7). Supporting measurements of where the predictable structure sits are in §3 and Appendix D; protocols, amendments and failed hypotheses in Appendices A, B and E.

## 2. Related work
**Pluralistic and distributional reward models.** Distributional preference learning (Siththaranjan et al., 2024), diverging-preference detection (Zhang et al., 2025), PRISM (Kirk et al., 2024), MultiPref (Miranda et al., 2025) and DICES (Aroyo et al., 2023) motivate modelling disagreement; jury learning (Gordon et al., 2022) and multi-annotator models (Davani et al., 2022) predict individual annotators, as do disagreement deconvolution (Gordon et al., 2021), per-rater toxicity models (Kumar et al., 2021), demographic and opinion-based prediction of unseen annotators (Fleisig et al., 2023) and multilevel models of DICES raters (Homan et al., 2024). Graded preference strength enters reward training as a margin (Touvron et al., 2023; Wang et al., 2025), and ties have classical paired-comparison models (Rao & Kupper, 1967; Davidson, 1970). **Personalised reward models** infer a user latent from a few examples (Poddar et al., 2024; Chen et al., 2025), represent users in a low-rank reward subspace (Bose et al., 2025), induce persona prompts from a user's history (Ryan et al., 2025, who also release a benchmark of PRISM and Chatbot Arena users), learn per-user embeddings jointly with the reward model (Li et al., 2024), fit a new user as a combination of shared base rewards (Shenfeld et al., 2025; Luo et al., 2025), or infer the user with neural processes (Kobalczyk et al., 2024); related work personalises the policy (Jang et al., 2023; Feng et al., 2024), adapts to groups (Zhao et al., 2024; Chakraborty et al., 2024) or studies personalisation versus aggregation (Park et al., 2024). Value profiles condition a rating decoder on a rater's demonstrations and are tested on held-out raters (Sorensen et al., 2025). Benchmarks often simulate users by personas or mixtures of reward models (Castricato et al., 2025; Zollo et al., 2025); real multi-rater data with deliberately diverse candidates are emerging (Zhang et al., 2026). VPL's latent can collapse under sparse preference data (Kim & Kim, 2026). A multi-faceted comparison of personalisation methods (Dong et al., 2025) reports large differences between methods and safety costs. Annotator embeddings (Deng et al., 2023) and per-annotator heads (Davani et al., 2022) are close relatives of our offsets; our contribution is not the offset model but the new-rater test and what it shows. Rater groups have been found to use safety severity scales differently (Mishra et al., 2026), which is consistent with the leniency component we find on DICES. **Annotator demographics** as predictors of labels have been found weak in several studies (e.g. Orlikowski et al., 2023). **Measurement theory**: rater severity and scale use are standard facets in many-facet Rasch measurement (Linacre, 1989; Eckes, 2011) and response styles are a classical survey-methods topic (Baumgartner & Steenkamp, 2001). We connect the last line to the first: for new-rater prediction, the measurement-theory rater facet is what the reward model is missing. **Collaborative filtering and annotator models.** User and item bias terms carry much of the predictive gain in collaborative filtering (Koren et al., 2009), and user-specific ordinal thresholds predict personal rating distributions (Koren & Sill, 2011); annotator models estimate rater-specific labelling behaviour (Dawid & Skene, 1979; Raykar et al., 2010; Hovy et al., 2013), and the label-variation literature argues for modelling it (Plank, 2022; Uma et al., 2021). Our offsets are of this kind and are not new; what is new is testing personalised reward models against them on new raters, and measuring what content personalisation these models could detect at all.

## 3. Data, and where the predictable structure sits
**Data.** MultiPref (Miranda et al., 2025; 10,461 comparisons; 4 ratings each by 2 crowd and 2 expert raters; 227 persistent raters; 5 ordered levels A-clearly … B-clearly). PRISM (Kirk et al., 2024; 68,371 responses each rated 1–100 by one of 1,396 users; binned to 5 fixed levels). DICES-350 (Aroyo et al., 2023; 350 conversations fully crossed with 104 quality-checked raters; safe / unsure / unsafe).

**A learner-free measurement (Appendix D).** Before fitting any personalised model we measured, on MultiPref, where held-out predictable structure sits: beyond item location, rater-specific thresholds improve held-out likelihood about 25 times more than item-specific dispersion (+0.036 vs +0.0014 nats per rating), the item-level shape of the rating distribution that replicates across disjoint rater panels is small (split-half reliability 0.25), and about a tenth of it is decodable from text. Beyond item location, the predictable structure is therefore mostly rater-side scale use, while the item-level shape that replicates across disjoint panels is small and only partly in the text. These two facts come from different estimands and do not say that disagreement is "not in the text". The stage-1 decision rule we had written down returned **"mixed"**, because G/X was not ≤ 10 % (interval 5.7–11.9 %); the factorised model of §4 was chosen with that outcome known.

## 4. A three-parameter scale-use baseline
(Figure 2 illustrates the effect of the offsets.) Let ℓ(x) ∈ R^K be the class logits of a text-only distributional reward model for item x (K ordered rating levels). For rater r we add a text-independent offset vector: p(y | x, r) = softmax(ℓ(x) + b_r). Variants: **DF** (b_r ∈ R^K, free), **DFs** (two-sided preference scales only: b_r tied symmetrically, (e, s, t, s, e) — extreme, slight, tie — 3 parameters, of which 2 are identifiable because the softmax is invariant to a common shift; no A-vs-B position term). Rater offsets have a Gaussian prior centred on the training-rater mean; a new rater's offsets are the MAP estimate from k of their ratings with the text model frozen. Baselines under the same protocol: **D** (text-only distributional RM), **DG** (group offsets: crowd/expert, race, region), **DL** (low-rank text-interacting latent: ℓ(x) + (Wx + w₀)·z_r, d = 8, the personalised-RM family). An interpretable probit family (rater shift / log-scale on an ordered-probit text head) is reported as a secondary analysis.

**Training and adaptation.** The text model and the training raters' offsets are fitted jointly by penalised maximum likelihood,
$$\min \sum_{(i,r,y)} -\log p(y \mid x_i, r) + \lambda_{\text{text}} \|V\|^2 + \lambda_r \sum_r \|b_r\|^2,$$
with $\lambda_{\text{text}}$ chosen on the text-only model and $\lambda_r$ on held-out items of the training raters. A new rater $r^*$ is adapted from $k$ ratings $\{(x_j, y_j)\}$ by $\hat b_{r^*} = \arg\min_b \sum_j -\log \mathrm{softmax}(\ell(x_j) + b)_{y_j} + \lambda_r \|b - \bar b\|^2$, with $\bar b$ the training-rater mean (the prior mean; $\hat b = \bar b$ at $k = 0$) and the text model frozen — a convex problem in 3–5 parameters, solved in milliseconds. Any text model that outputs graded log-probabilities can be used: we use a ridge head on frozen LLM features (§5.1–5.2), a LoRA-fine-tuned LLM reward model (§5.3) and the decoder of a published personalised reward model (§5.4).

## 5. Experiments
**Protocol.** 5 folds; in each, 20 % of raters (stratified by group) and 20 % of prompt groups are held out; models are trained on training raters × training items with penalties chosen on a validation split; each test rater is adapted on k ∈ {0, 5, 10, 20, 50} of their ratings of *training* items (5 random draws) and evaluated on their ratings of *held-out* items. Primary metric: held-out log-likelihood per rating; also RPS and preference-direction accuracy; rater-cluster bootstrap (B = 2,000). Because test raters share test items on MultiPref and DICES, the headline k = 20 contrasts were also re-estimated with a two-way bootstrap that resamples raters and prompt groups independently: on graded labels every log-likelihood interval widens by at most 0.007 on either side and no log-likelihood conclusion changes; direction-accuracy differences of about a point or less (the style model's +0.5 on MultiPref, VPL's direction advantage over the style model) lose significance and are marked where they appear. Text model in §5.1–5.2: frozen Qwen2.5-7B features with a ridge head; §5.3: a LoRA-fine-tuned reward model.

### 5.1 Main result (MultiPref)
Figure 1 shows the gain over the text-only reward model as a function of k on all three datasets. In the table, DF/DFs/DG use the training-rater prior and DL and the DFs − DL column use the few-shot-tuned prior (the DFs − DL contrast is post hoc).

| k | DF − D | DFs − D | DG − D | DL − D (tuned prior) | DFs − DL (tuned, post hoc) |
|---|---|---|---|---|---|
| 5 | +0.028 [+0.012, +0.044] | +0.048 [+0.029, +0.070] | ≈ 0 | +0.023 [−0.002, +0.047] | +0.026 [+0.016, +0.037] |
| 20 | +0.080 [+0.055, +0.106] | **+0.100 [+0.074, +0.128]** | ≈ 0 | +0.095 [+0.069, +0.122] | +0.0045 [−0.0004, +0.0092] |
| 50 | +0.114 [+0.087, +0.142] | +0.128 [+0.101, +0.156] | ≈ 0 | +0.120 | +0.007 [+0.002, +0.013] |

Preference-direction accuracy (D: 0.674): DFs +0.005 [+0.001, +0.008] at k = 20 (not significant once items are also resampled: [−0.001, +0.011]); DF −0.014 [−0.020, −0.007]. A three-number style model gains as much as a tuned 8-dimensional text-interacting latent (tie at k = 20) and more at k = 5, 10 and 50; fitting a rater's A-vs-B position from few ratings costs direction accuracy.

**Reference points.** To size these gains: on MultiPref at k = 20 a uniform forecast scores −1.609 nats per rating, a forecast that ignores the text and uses only the new rater's 20 ratings −1.487, the text-only model −1.441, the text model with the three offsets −1.342, and offsets fitted in-sample on all of the rater's held-out ratings (an optimistic ceiling for text-independent offsets) −1.262. Twenty ratings of a person, without the text, recover 73 % of the text model's gain over uniform; the offsets close 56 % of the gap between the text-only model and the in-sample ceiling. On DICES the rater's ratings alone predict better than the text alone (−0.766 vs −0.840 at k = 20). Even the in-sample ceiling raises MultiPref direction accuracy by only 1.3 points (0.674 → 0.687), confirming that text-independent offsets cannot carry ranking.

### 5.2 Replications (k = 20)
DF − D and DG − D use the training-rater prior, DF − DL the few-shot-tuned prior. Direction accuracy on PRISM means good-vs-bad around the scale midpoint.

| dataset | DF − D | DG − D (groups) | DF − DL (tuned prior) | direction acc. DF − D |
|---|---|---|---|---|
| DICES-350 (safety) | +0.089 [+0.064, +0.117] | −0.006 (race) | +0.037 [+0.022, +0.053] | +0.048 [+0.025, +0.076] |
| PRISM (ratings) | +0.080 [+0.071, +0.090] | +0.003 (region) | −0.001 [−0.006, +0.003] (formally not non-inferior: bound −0.006 < −0.005) | +0.005 [+0.001, +0.009] |

### 5.3 On a fine-tuned reward model
With a LoRA-fine-tuned Qwen2.5-7B reward model (D-LoRA, trained per fold on the training raters' rating distributions) as the text model, the three-number style model still adds +0.100 [+0.071, +0.130] nats per rating at k = 20 — the same as its gain on the frozen-feature head (+0.100). Fine-tuning improves the text-only model by +0.027 [+0.016, +0.039] (direction accuracy +1.4 points) and the style model by the same +0.027: the two gains add. Personalising the frozen-feature model with 20 ratings per rater gains more than fine-tuning the text model (+0.072 [+0.041, +0.106]). DFs keeps the direction accuracy of D-LoRA (+0.002 [−0.002, +0.006]). Against in-context personalisation — a separate LoRA model on the same base, trained with ten of the rater's other ratings in the prompt and evaluated with the new rater's k ratings in the prompt — the three offsets on D-LoRA are better at k = 20. The in-context model's result varies with its training seed (two of fifteen runs failed, gaining −0.078 and −0.055 over D-LoRA against +0.021 to +0.125 for the others; the two failed runs have the highest training loss), so it was trained with three seeds per fold, and we fixed in advance that "better" requires a lower bound above zero for every seed and for the seed average. Averaged over seeds — the expected result of one training run — the offsets are better by +0.041 [+0.027, +0.054] nats per rating (209 raters; per seed +0.062, +0.018 and +0.042, every lower bound at least +0.005) and more accurate on which response the rater prefers (+1.9 points [+0.9, +2.7]). The in-context model does learn from the history (+0.051 [+0.024, +0.079] over D-LoRA on average), at several thousand prompt tokens per prediction, but its direction accuracy is below D-LoRA's (−1.7 points [−2.6, −0.8] on average; −0.6 to −3.0 per seed).

### 5.4 Published personalised reward models
We reimplemented VPL (Poddar et al., 2024) and PAL-B (Chen et al., 2025) from their official code as heads on the same frozen per-response embeddings and evaluated them under the same new-rater protocol, refitting the text-only and style models on those embeddings. On graded labels, at k = 20 the style model is better than VPL by +0.092 [+0.068, +0.119] nats per rating ([+0.063, +0.124] when prompt groups are also resampled) and than PAL-B by +0.158. VPL's latent does carry rater information once its posterior collapse is prevented (KL weight selected as 0 or 0.001; +0.087 over its own unpersonalised version), but only lifts it to the level of the text-only model; PAL-B's few-shot user weights give no gain. Their user representations are unrelated to response style (cross-validated R² ≈ 0 against the style offsets). On binary labels — the setting in which both methods were proposed — every method's personalisation gain is at most 0.002 nats (small but nonzero for PAL-B with K = 4, and for VPL and the style model at k = 50), and VPL's text head is the best binary model (the style model is 0.010 nats behind it and 0.005 behind the text-only model, differences of the size of item-sampling noise): the individual differences that are predictable for new raters live in the graded levels and ties that binary preference data discard. VPL's per-response reward head is slightly better at predicting *which* response is preferred (0.677 vs 0.668), an effect present without personalisation and not significant once prompt groups are also resampled (style model − VPL: −0.9 points [−2.7, +0.8]). The offsets are also a plug-in: added to VPL (fitted on the same k ratings, VPL frozen) they improve it by +0.088 [+0.066, +0.111] nats per rating at k = 20, tie with the style model on likelihood (−0.004 [−0.014, +0.005]) and keep VPL's direction accuracy (+1.1 points over the style model alone; rater bootstrap only).

### 5.5 Summary of baselines (MultiPref, new raters, k = 20)
Gains are relative to each block's text-only model (D, Dp, D-LoRA); the LoRA block uses adaptation draw 0 only (the draw the in-context model was evaluated on), hence the style model's +0.092 here against +0.100 averaged over five draws in §5.3.

| text model | personalisation | gain in LL per rating vs the block's text-only model | direction accuracy |
|---|---|---|---|
| frozen features (joint item embedding) | group offsets (crowd / expert) | ≈ 0 | 0.677 |
| | low-rank latent, tuned prior | +0.095 [+0.069, +0.122] | 0.679 |
| | **style offsets, 3 numbers (DFs)** | **+0.100 [+0.074, +0.128]** | **0.679** |
| frozen features (per-response embeddings) | VPL (reimplemented) | +0.002 [−0.008, +0.012] | 0.677 |
| | PAL-B (reimplemented) | −0.065 (worse) | 0.666 |
| | **DFs** | **+0.094 [+0.069, +0.120]** | 0.668 |
| | VPL + style offsets | +0.090 | 0.679 |
| LoRA-fine-tuned Qwen2.5-7B (209 raters) | in-context rater history (RC-LoRA, mean of 3 training seeds) | +0.051 [+0.024, +0.079] | 0.671 |
| | **DFs** | **+0.092 [+0.063, +0.125]** | 0.689 |

Rows within a block share the text model and the raters; across blocks the text models differ (text-only direction accuracy 0.674 / 0.670 / 0.688). VPL's and PAL-B's own gains over their unpersonalised versions are +0.087 and −0.000.

### 5.6 Could these methods have detected content personalisation? A semi-synthetic positive control
A ranking null is informative only if the methods would detect content-dependent preferences where they exist. We keep MultiPref's structure (raters, items, who rated what, folds and k-shot draws) and replace the labels by semi-synthetic ones. A generator — the text-only head plus scale-use offsets, fitted on all ratings — gives each rating a distribution, to which a rater-specific content term $(\theta_r^\top g_i)\,(-2,-1,0,1,2)$ is added to the logits; $g_i$ are two features of the response pair (the log length ratio and a random direction in the per-response embedding space, orthogonal to the consensus quality direction) and $\theta_r \sim N(0, \tau^2 I)$. The scale $\tau$ is calibrated on the generator alone so that an oracle that knows $\theta_r$ gains +1.7, +5.2, +10.1 or +21.1 points of direction accuracy on the test ratings; $\tau = 0$ is a null control. Every method is then run under the paper's protocol. Because a method whose unpersonalised state is not the population state can improve with anyone's ratings, the contrast is **the method adapted on the rater's own k ratings minus the same method given another test rater's adapted parameters** (a random derangement within fold, k and draw). Before the runs we fixed that the protocol has power at a strength if some content-interacting method has a lower 95 % bound above +1 point at k = 20; the +10 and +21 panels and the untuned-prior low-rank runs were added after the first results and are exploratory.

| panel | oracle gain | low-rank latent (DL) | VPL | PAL-B | PAL-B, full features |
|---|---|---|---|---|---|
| null control (τ = 0) | 0 | −0.10 [−0.38, +0.17] | −0.04 [−0.08, +0.01] | −0.23 [−0.45, +0.00] | −0.04 [−0.25, +0.17] |
| injected, τ2 | +1.7 | −0.01 [−0.29, +0.26] | +0.01 [−0.07, +0.10] | −0.10 [−0.36, +0.15] | — |
| injected, τ5 | +5.2 | −0.02 [−0.28, +0.26] | +0.01 [+0.00, +0.03] | +0.23 [−0.04, +0.51] | +0.26 [−0.14, +0.66] |
| injected, τ10 (exploratory) | +10.1 | +0.09 [−0.18, +0.36] | +0.27 [+0.02, +0.54] | +0.42 [−0.08, +0.96] | +1.95 [+1.16, +2.74] |
| injected, τ20 (exploratory) | +21.1 | +1.47 [+0.83, +2.18] | +6.92 [+5.63, +8.30] | +4.62 [+3.47, +5.78] | +8.13 [+6.54, +9.77] |
| real MultiPref | — | +0.30 [−0.00, +0.60] | −0.01 [−0.04, +0.02] | −0.43 [−0.72, −0.15] | +0.11 [−0.16, +0.37] |

Own minus another rater's k = 20 ratings, direction accuracy in points, 95 % rater bootstrap; 209 new raters, 5 folds. The low-rank latent uses the few-shot-tuned prior. k = 50 contrasts use the 180 of 209 raters with at least 50 training-item ratings. PAL-B's own − other contrast is negative with compressed features (null control −0.23, real data −0.43): its per-rater adaptation adds noise there; with full features it is at zero (−0.04, +0.11). The injection uses one draw of θ and of the labels, so seed variability of the synthetic panels is not in the intervals. Last column: PAL-B on the full 3,584-dimensional features instead of their PCA-256 (exploratory; τ2 not run).

No method has power at the pre-specified strengths. In the exploratory dose-response, VPL and PAL-B detect content preferences worth +21 points but recover less than half a point of +10; the low-rank latent, whose user term interacts with a joint embedding of the comparison, has a signal at +21 points that stays below the threshold, and with the untuned prior it shows nothing up to +5 points either. On the real data VPL and PAL-B are at the null-control level, and the low-rank latent's marginal +0.30 [−0.00, +0.60] is matched by the text-independent offsets (+0.32 [+0.06, +0.58] on the same contrast), so it reflects scale use (which can tip a few near-tie predictions), not content. Read together: on MultiPref, content-level heterogeneity strong enough for an oracle to gain about 20 points of direction accuracy is excluded; heterogeneity worth up to about 10 points cannot be seen by these methods from 20 ratings, so the ranking null of §6 says nothing about it. On the full features (exploratory) VPL's latent collapses (own − other exactly 0), while PAL-B passes the threshold at +10 points but not at +5, and the real data stay at the null level (+0.11 [−0.16, +0.37]): content heterogeneity of the injected form worth about 10 oracle points is excluded at k = 20, about 5 is not (Appendix B). **How far are these methods from what the data allow?** A well-specified reference learner — the injection's two features known, a per-rater weight vector with an empirical-Bayes prior, style offsets re-fitted, the same permutation contrast — recovers the injected preference from 20 ratings at every strength. On the oracle's scale (the rater's own weights against the population state, θ = 0 here, with the rater's style offsets kept) it gains +0.89 [+0.40, +1.37] points at +1.7 oracle points, +3.1 [+2.3, +4.0] at +5.2 and +8.0 at +10.1, i.e. 52–79 % of the oracle; own − other roughly doubles these numbers, because another rater's weights are anti-informative, and is therefore not used for this learner. The statistical detection limit is therefore between +1.7 and +5.2 points, well below the methods'. Is the gap in the methods' inputs or in the learners? Linear probes (exploratory, Appendix B) show the injected direction is available to VPL and PAL-B (out-of-fold R² 0.65 compressed, 1.00 full) but not to the low-rank latent's joint embedding (0.02); re-injected inside that embedding, the latent detects +10 points (+1.97 [+1.31, +2.65]; originally +0.09; 3 of 4 draws) but not +5 (+0.08; 0 of 4). With the dimension available, the best learners thus detect between +5 and +10 oracle points, the reference learner below +5: what fails is finding the dimension, not the number of ratings. With semantic axes (formatting, hedging/refusal) no method detects even +9.7 points; the reference learner recovers +7.4 (Appendix B). Results are stable over four synthetic draws, and the synthetic panels are noisier than the real data, so the calibrations transfer only approximately (Appendix B).

### 5.7 How much room is there? Value conflicts are rare
The positive control asks what the methods could detect; MultiPref also lets us ask how much there is to detect. Every MultiPref annotation carries the annotator's own helpfulness, truthfulness and harmlessness preferences next to the overall one, so a rater's way of trading these values off is observable. We fit an ordinal model of the overall preference from the annotator's own aspect labels (their values and absolute values) with rater-specific cut-points (scale use) and either a pooled trade-off or a rater-specific trade-off, adapted on k of the rater's training-item annotations and evaluated on held-out items **with the rater's own aspect labels as inputs** — an oracle for the content side. The pooled trade-off weights harmlessness most (6.1, five-fold mean), then helpfulness (4.0) and truthfulness (2.0). With the rater's own aspect labels as inputs the pooled model already gets 97.5 % of directions right (74 % on conflict items): aspect and overall labels are produced together by the same annotator, so this ceiling concerns a small residual and is a property of MultiPref's concurrent labelling.

| rater ratings used | rater − pooled trade-off, direction accuracy (points) | log-likelihood per rating | on conflict items (points) |
|---|---|---|---|
| k = 20 | +0.03 [−0.05, +0.12] | +0.011 [+0.003, +0.020] | +0.6 [−1.1, +2.4] |
| k = 50 | +0.06 [−0.09, +0.21] | +0.023 [+0.011, +0.037] | +0.3 [−2.7, +3.8] |
| all training items | +0.10 [−0.24, +0.43] | +0.046 [+0.028, +0.068] | +2.0 [−5.0, +9.2] |
| in-sample (fitted on the test items) | +0.44 [+0.27, +0.64] | +0.094 [+0.079, +0.112] | +9.7 [+5.6, +14.5] |

Even with the rater's own aspect judgements and all of their training ratings, a rater-specific trade-off predicts which response they prefer only 0.1 points better than the population's trade-off, and even fitted in-sample only 0.4 points better. The reason is that the aspects point in opposite directions in only 4.0 % of the held-out non-tie comparisons (3.5 % of all annotations); there individual trade-offs matter a great deal (in-sample +9.7 points; among the 20 raters with at least ten helpfulness–harmlessness conflicts, the share of conflicts resolved in favour of helpfulness ranges from 0.00 to 0.94), but they are too rare to move overall accuracy. Individual trade-offs do change how strongly raters prefer (up to +0.046 nats with all their ratings), in line with the calibration-not-ranking pattern. We fixed in advance that an aspect-weight personalised reward model would be built only if the lower bound of this ceiling exceeded half a point with all training ratings; it does not, so we did not build one. The learned personalisers cannot be tested on the conflict items either: the 243 held-out non-tie ratings on them give own − other intervals wider than the achievable ceiling (k = 20: low-rank latent +0.1 [−2.2, +2.4]). **A calibrated test on the real data.** The ceiling above gives each rater's own aspect labels; a deployable personaliser would know only the item's aspects. We therefore ran the reference learner of §5.6 on the real labels with the item's consensus aspect differences from its *other* annotators as content features (3-d), with a hierarchical prior centred at the population weighting (estimated on the training raters) and compared each rater's own weights with that population weighting (style offsets kept). Individual weights transfer *worse* than the population's: −0.28 [−0.56, −0.06] points at k = 20 and −0.63 [−1.01, −0.25] at k = 50. With injected aspect-weight heterogeneity it gives +0.46 [−0.00, +0.96] at k = 50 when an oracle would gain +1.4 points and +3.4 [+2.6, +4.3] at +5.0. The real data lie well below the +5-point panel and, at k = 50, just below the +1.4-point panel: transferable heterogeneity in how raters weigh these three values is at most of the order of one to two oracle points on MultiPref. This test is exploratory and post hoc, and its contrast was revised four times (Appendix A; no version shows a positive transferable aspect part), the calibration strengths were chosen after seeing the real bound, it uses one synthetic draw on panels noisier than the real data, and it uses other annotators' aspect labels of the test items (an aspect oracle, not a deployable model). Three caveats: the ceiling bounds personalisation of the *weighting* only — disagreement about which response is more helpful or harmless is absorbed into the inputs; it covers content preferences expressible through these three aspects only; MultiPref's prompt sampling determines how often values conflict; and annotators may have aligned their aspect labels with their overall label, which would understate conflicts.

## 6. What personalisation buys: calibration, not ranking
**Binary labels remove the signal.** On MultiPref with ties dropped and labels binarised, every method's personalisation gain is at most 0.002 nats per rating (§5.4), and the scale-use baseline's binary accuracy equals the text-only model's (−0.0002). The individual differences that are predictable for new raters live in the graded levels and in ties — exactly what binary preference data discard, and the format in which most personalised reward models are trained and evaluated.
**Ranking moves little.** Text-independent offsets change how strongly a rater is predicted to prefer a response, not which response: on MultiPref the scale-use baseline raises direction accuracy by only +0.005 [+0.001, +0.008] at k = 20 (about half of it already at k = 0), while RPS drops from 0.1593 to 0.1532. On single-response safety ratings the same offsets do move the safe/unsafe decision (+4.8 points on DICES), because there a rater's threshold *is* the decision. Content-interacting personalisation does not do better on ranking: VPL's advantage in direction accuracy is present without personalisation (k = 0), comes from its text head, and is within item-sampling noise. Text-only direction accuracy on MultiPref (0.674) is already as high as the agreement in direction between two human raters of the same item (0.673 [0.666, 0.680]): a population model predicts a new rater about as well as another person does. **Seen raters.** With all their training ratings (median 134), training raters' own parameters beat another rater's by −0.11 [−0.57, +0.36] direction points for the low-rank latent (offsets +0.10, −0.23): the ranking null is not specific to few-shot adaptation (exploratory, Appendix B). Against its own k = 0 version, no method's direction accuracy on MultiPref rises by more than 0.2 points at k = 20, and every upper 95 % bound stays below +0.8 points even when prompt groups are resampled together with raters (VPL +0.07 [−0.57, +0.74], style model −0.10 [−0.69, +0.54], PAL-B −0.48 [−1.11, +0.14]).
**The ranking null replicates on real users' own choices.** PRISM users each saw 2–4 responses to their own prompt, scored them and chose one; pairing the chosen response with every other one gives 41,199 native pairwise choices of 1,396 users. Under the same new-user protocol (5 user folds × 5 conversation folds, k of the user's pairs from training conversations), we fixed before any result that the ranking null would be stated only if every method's improvement in choice accuracy over its own k = 0 version had an upper 95 % bound below one point at k = 20. It holds for all of them (1,033 new users at k = 0; the 669 with at least 20 adaptation pairs at k = 20): VPL +0.12 points [−0.08, +0.33], PAL-B +0.0 [−0.4, +0.4] (K = 2) and +0.3 [−0.1, +0.7] (K = 4), the 5-offset model −0.6 [−1.4, +0.2]; the symmetric scale-use model is identical to the text-only model on binary choices, because a binary label carries no intensity. LoRe (Bose et al., 2025), which reports +10 points for unseen PRISM users, run here with its own few-shot fit and with a validated adaptation ridge under the same pre-set rule, also fails it: own gain at k = 20 −1.5 [−2.5, −0.4] (regularised −0.5 [−1.2, +0.2]), own − other +0.2 [−0.8, +1.2]. In LoRe's own setting (its embeddings, split and pair construction) we obtain 67.4 % for the monolithic model and 63.6 % for LoRe (published 61.0 % and 71.0 %; Appendix B): the published gain is not reproduced. With a graded label cut from the users' own score differences (thresholds fixed in advance), the MultiPref pattern returns at half the size: at k = 20 the scale-use model gains +0.043 [+0.031, +0.057] nats per rating over its k = 0 version, VPL +0.015 [+0.005, +0.027], PAL-B 0.000; the scale-use model is ahead of VPL by +0.045 [+0.030, +0.062]; and no method's own direction-accuracy gain exceeds +0.2 points (the 5-offset model loses 1.7).


## 7. Recommendations
(i) Collect and keep graded labels (and ties) when individual differences matter; binary preferences erase most of what is predictable about a new rater. Sample comparisons for value conflicts (for example, pairs on which aspect ratings disagree): in MultiPref only 4 % of comparisons involve one, and they are where individual trade-offs matter. (ii) Report a scale-use calibration baseline (a few text-independent offsets per rater) next to any personalised reward model. Beating it on likelihood is necessary but not sufficient evidence of content personalisation; a method that learns content preferences should show it in ranking or choice outcomes, where the offsets cannot help by construction. (iii) Evaluate on raters unseen in training, adapted from k of their own ratings, and on held-out items, and compare each method with itself given another rater's ratings (a permutation control): a poor unpersonalised state inflates gains measured against k = 0. (iv) Report calibration (log-likelihood, RPS) and ranking (direction accuracy) separately: they answer different questions — how strongly someone prefers, and what to show them. (v) Check what a learned user representation encodes (here unrelated to scale use, R² ≈ 0).

## 8. Discussion
**Why did published personalised models learn little about new raters here?** Their evaluations differ from ours in three ways that each favour content-dependent personalisation: synthetic users whose preferences differ in content by construction, binary labels that remove scale use, and users seen during training. On real raters, graded labels and unseen users, the structure that transfers from k ratings to new items is mostly how the rater uses the scale, which neither VPL's latent nor PAL-B's prototypes represent (R² ≈ 0). Adding the offsets to VPL recovers the whole gain (+0.088): the two are complementary, and a content-personalising method should be shown to beat VPL plus offsets.



## 9. Limitations and analysis log
Protocols, amendments and failed hypotheses: Appendices A, B, E. The main tables use frozen-feature text heads (a LoRA reward model only in §5.3), and compressed features make the published methods weaker detectors than full features. Our VPL, PAL and LoRe are reimplementations as heads on frozen embeddings; VPL's and PAL's published numbers were not reproduced in their native settings, and LoRe's PRISM gain is not reproduced even in its own setting with its embeddings, for reasons we could not isolate. The positive control injects low-dimensional preferences on MultiPref only, and its panels are noisier than the real data, so detection limits transfer only approximately. The aspect analyses rest on MultiPref's concurrent aspect labels. All datasets are English, and the per-rater calibration is not shown to change a downstream decision.

## Impact Statement
This paper evaluates personalised reward models, which are meant to let language models serve people whose preferences differ. Its main finding — that what such models learn about a new rater from few ratings is mostly how that rater uses the rating scale — bears on claims that current methods represent individual or minority values: reported personalisation gains can reflect scale use rather than content preferences, and evaluations on synthetic users, binary labels or seen users can overstate what is learned. We see no direct negative use of the protocol. The datasets are public, were collected with consent by their creators, and are used under their licences; we use rater identifiers only as anonymous indices and report no individual-level results.

## Appendix A. Protocols and amendments
All analyses were specified in timestamped internal protocols (PROTOCOL_STAGE1, PROTOCOL_STAGE2, PROTOCOL_STAGE2B, PROTOCOL_STAGE2C, PROTOCOL_STAGE3); stages 2b and 2c were written after the stage-2a results. Changes after a result were logged as numbered amendments with the reason; the main ones: the first decoding split (a = b = 2) was structurally empty (two ratings determine their distribution) and was replaced by a = 3, b = 1; hand-set penalties in the rater–item model over-fitted and were replaced by inner cross-validation (which reversed an earlier, wrong conclusion that rater shifts do not help); penalty grids were extended when selections fell on grid edges, before any hypothesis was read; the low-rank baseline lacked a constant column and was fixed in its favour; the probit group model had a scale non-identifiability and was fixed; VPL suffered posterior collapse and its KL weight was re-selected including 0; PAL-B's adaptation ridge was re-selected by k-shot validation. Every superseded full run is kept and reported in the supplementary results; two debugging smoke runs and one fold whose output was deleted unread when the penalty grids were extended are not. The real-data aspect contrast of §5.7 was revised four times: own − other; with a style-only control after a first, confounded +0.45 [+0.01, +0.94]; against θ = 0; and against the population weighting, after the reference learner turned out to shrink towards 0 rather than towards the population. The few-shot-tuned low-rank prior was selected at the top of its grid (8192) in most folds; extending the grid to 524,288 left every DL result unchanged in substance (real data: own − other +0.31 vs +0.30 at k = 20, DFs − DL +0.003 vs +0.0045; synthetic +5/+10-point panels: +0.10 / +0.09 vs −0.02 / +0.09).

## Appendix B. Hypotheses and outcomes
Stage 2a (MultiPref, k = 20): H1 DF > D — holds (+0.080); H5 (probit F1 > D, the primary probit contrast after Amendment 1) — not supported (+0.020 [−0.001, +0.041]; homoscedastic F − D −0.029), superseded by H1 in Amendment 2; H2 DF > group — holds; H3 DF ≥ low-rank − 0.005 — holds under the training-rater prior, not robust under a few-shot-tuned prior (−0.015); H4 rater scale > rater shift — holds on MultiPref only; H6 symmetric style model gains likelihood without losing direction accuracy — holds and robust. Replications: H1r, H2r hold on DICES and PRISM; H3r holds on DICES (robust) and is a tie on PRISM under the tuned prior. Stage 2b: B1, B2, B3 hold. Stage 2c: C1 holds (graded), C2 holds (binary: |DFs − D| accuracy −0.0002; all personalisation gains ≤ 0.002 nats), C3 fails (published latents do not encode style, R² ≈ 0), C4 not met as a conjunction (first part holds, +0.088 over VPL; second part a tie with DFs, lower bound −0.014); Stage 3 (positive control): τ0 control passes; power at the pre-specified strengths (+1.7, +5.2 oracle points) not established — no content-interacting method's own − other gain has a lower bound above +1 point; exploratory dose-response: VPL and PAL-B pass at +21 points, none at +10; the split-half content estimator (S3-C) has no power; with full features (exploratory, Amendment 5) the τ0 control passes and PAL-B passes at +10 points (k = 20), so the PCA bottleneck explains part of the detection limit. R1 (PRISM native pairwise choices: every method's own choice-accuracy gain at k = 20 has an upper bound < +0.01) holds (largest bound +0.0071, PAL-B K = 4).

**Scale use and the shared reward model.** Training the text model jointly with rater offsets and then using the population-mean offsets (k = 0) does not give a better consensus model than ordinary training: −0.003 [−0.010, +0.003] nats on MultiPref (direction +0.3 points, n.s.), −0.022 [−0.037, −0.008] on DICES, +0.001 on PRISM, −0.009 [−0.016, −0.004] with the LoRA reward model. Ordinary training averages scale use out; it matters for predicting a person, not for learning the content preference.

**What the offsets encode.** In the probit family, rater *scale* matters more than rater *shift* on MultiPref (+0.036 [+0.020, +0.057] at k = 20), but rater *shift* dominates on DICES (−0.053) and PRISM (−0.031): leniency/strictness on single-response rating scales, intensity on two-sided preference scales.

**What this does and does not say about pluralism.** Our results do not show that people agree about content: the item-level disagreement that replicates across rater panels is real (split-half reliability 0.25 on MultiPref) and about a tenth of it is decodable from text. They show that, for predicting an individual new rater from few ratings, that content-level disagreement is a small part of what is predictable, and that demographic or crowd/expert groups add nothing beyond the text.

**Positive control on full features (Stage 3, Amendment 5).** Because the compressed features might be what limits the content-interacting methods, we re-ran VPL and PAL-B on the full features (exploratory). The text-only fits improve (k = 0 log-likelihood: PAL-B −1.533 vs −1.558, VPL −1.495 vs −1.574), but VPL's latent then collapses and is unused at every strength (own − other exactly 0), so this check rests on PAL-B. Its detection limit drops: it passes the threshold at +10 points; at +5 points its k = 50 gain is positive (+1.05 [+0.37, +1.72]; real data +0.19 [−0.12, +0.48]) but meets the +1-point criterion in only one of four synthetic draws. The real data stay at the null level (+0.11 [−0.16, +0.37] at k = 20). With this stronger detector, content heterogeneity of the injected form worth about 10 oracle points of direction accuracy is excluded at k = 20; at k = 50 the real data lie below the +5-point panel but the intervals overlap, so about 5 points is not excluded; the compressed features used for the main tables make the published methods weaker detectors than they need to be.

**Positive control: seed variability and realism (Stage 5).** Over four synthetic draws (θ and labels) the reference learner is stable (+2.4 to +3.1 at +5 points, +6.4 to +8.0 at +10), PAL-B on full features detects the +10-point panels in all four (lower bounds +1.16 to +3.23) and the +5-point panels in none (+0.26 to +1.40), and the low-rank latent detects neither in any draw (−0.31 to +0.15). A limitation of all synthetic panels: they are noisier than the real data (rater-pair direction agreement 0.59 at τ = 0 against 0.673 [0.666, 0.680]; Krippendorff's α 0.11 against 0.28), and adding item fixed effects to the generator did not close the gap (0.60), nor does it reproduce the small effect of style offsets on direction (+0.32 real vs −0.07 at τ = 0); the calibrations transfer to the real data only approximately, with no claimed direction of bias.

**LoRe on all panels (Stage 6).** Across PRISM pairs and MultiPref, binary and graded labels and k ∈ {5, 20, 50}, LoRe never improves direction or choice accuracy over its own k = 0 version or over the text-only model (own gain −6.2 to +0.1 points; the regularised version −1.1 to −0.0), and its log-likelihood is below the text-only model's everywhere. Its own − other is positive in some cells (MultiPref binary, k = 20: +1.3 [+0.5, +2.0]) while its own gain is negative there (−1.2 [−1.9, −0.5]): another rater's over-fitted weights are anti-informative, the scale problem discussed for the reference learner, so own − other alone is not evidence of personalisation for methods whose few-shot fit over-fits.

**Stage 7 (after the seventh review; PROTOCOL_STAGE7.md).** S7-1, cross-fitted ridge probes (prompt-group folds, out-of-fold R²) of the two injected features from each learner's inputs: log length ratio 0.88 (VPL/PAL-B PCA-256 x_B − x_A), 0.93 (full features), 0.73 (D/DL joint PCA-256); random direction 0.65, 1.00, 0.02. By the rule fixed beforehand, S7-2 was run for the low-rank latent only: the random direction re-drawn inside its joint embedding (orthogonal to the consensus direction), τ calibrated to oracle gains of +5.1 and +10.4. Own − other at k = 20 / 50: +0.08 [−0.18, +0.33] / +0.03 [−0.29, +0.34] at +5.1; +1.97 [+1.31, +2.65] / +7.02 [+5.84, +8.16] at +10.4; the reference learner is unchanged (own − population +2.67 and +8.33). S7-3, seen-rater ceiling on real MultiPref (training raters × test items, 904 rater-folds, trained parameters; derangement of training raters): direction accuracy minus the text-only model −0.51 [−0.88, −0.11] (five offsets), −0.00 [−0.20, +0.18] (symmetric), −0.42 [−0.81, −0.02] (low-rank); own − other −0.23, +0.10, −0.11 [−0.57, +0.36]; log-likelihood over the text-only model +0.13 nats for all three. By the rule fixed beforehand, the ranking null also holds for seen raters. S7-4 (Amendment 3), semantic axes — (s1) log(1 + markdown list/heading lines) of B minus A, (s2) the same for a fixed list of hedging/refusal phrases — calibrated to +4.6 and +9.7 oracle points: probes R² 0.37–0.66 (formatting) and 0.09–0.24 (hedging); own − other at k = 20 / 50 for the low-rank latent +0.09 / +0.05 and −0.18 / −0.08, VPL −0.05 / +0.04 and +0.03 / +0.03, PAL-B (compressed features) −0.24 / −0.12 and +0.27 / +0.40 [−0.02, +0.85]; reference learner own − population +2.57 [+1.61, +3.57] and +7.44 [+5.96, +8.91]. No method detects either panel. S7-5 (Amendment 4), the in-span panels over four draws (θ and label seeds 1, 11, 12, 13): the low-rank latent's own − other at k = 20 is +1.97, +2.83, +3.14, +1.44 [+0.92, +1.96] at +9.3 to +10.9 oracle points (detected in 3 of 4; k = 50 +5.0 to +7.3) and +0.00 to +0.14 at +4.7 to +5.5 (0 of 4); the reference learner +7.4 to +8.3 and +2.6 to +2.9. Both statements are kept under the rule fixed beforehand.

**Confirmatory and exploratory results.** Confirmatory (rule fixed before the result): the stage-2a hypotheses H1–H6 and their replications; B1–B3; C1–C4; R1 (PRISM native choices); the Stage-3 positive control at +1.7 and +5.2 oracle points (no power); the Stage-4 ceiling rule (not met); the Stage-6 LoRe rule (PRISM null not withdrawn). Exploratory (added or changed after a result, labelled in the text): the symmetric offsets DFs and their hypothesis; the few-shot-tuned prior; the +10 and +21 panels and the full-feature runs; the reference learner and its oracle-scale contrast; the calibrated real-data aspect test; the regularised LoRe; the two-way bootstrap re-estimates.

**Reproducing LoRe's PRISM result (Stage 6, Amendments 2–3).** Unseen-user binary accuracy, mean ± sd over five random user splits, LoRe's native setting (users with at least six dialogues split 50/50, half of each user's conversations for few-shot and half for test, one chosen-vs-other pair per conversation; 1,267 users, about three few-shot pairs per unseen user):

| embeddings | monolithic BT | LoRe, no adaptation | LoRe, few-shot fit |
|---|---|---|---|
| Skywork-Reward-Llama-3.1-8B-v0.2 (LoRe's) | 67.4 ± 1.1 | 67.3 ± 1.8 | 63.6 ± 3.7 |
| Qwen2.5-7B-Instruct (ours) | 67.7 ± 1.5 | 68.7 ± 1.7 | 61.0 ± 2.5 |
| published (Bose et al., 2025) | 61.0 ± 1.2 | — | 71.0 ± 1.0 |

Taking one pair per interaction instead (every turn; 20 pairs per user) gives 58.8 / 59.2 / 57.0 with our features. The remaining differences — a stronger monolithic baseline here and a few-shot fit that helps there but hurts here — could not be traced to any setting the LoRe paper reports. Under our protocol (user- and conversation-disjoint folds) the Skywork embeddings leave the conclusion unchanged: LoRe's own gain at k = 20 is −1.3 [−2.5, −0.2] points (regularised −0.5 [−1.3, +0.2]) and own − other +0.2 [−0.9, +1.2], as with our features.

## Appendix C. Implementation
Text features: last-token final-layer states of Qwen2.5-7B-Instruct under a 5-point judge prompt (MultiPref, PRISM) or a 3-level safety prompt (DICES), label-free PCA to 256 dimensions. Folds: 5 rater folds (stratified by group) × 5 prompt-group folds; validation: 15 % of training prompt groups. k-shot draws: 5 per k, identical across all models (RC-LoRA: draw 0 only). PRISM item folds are by conversation. Bootstrap: rater clusters, B = 2,000. LoRA: r = 16 on all attention and MLP projections, lr $10^{-4}$, one epoch, accumulation 8. VPL / PAL-B: official architectures (latent 512, hidden 512; d_pref 512, mlp2-gelu projectors, angle learner) with an ordered-logistic link for graded labels; VPL's KL weight selected from {0.01 (official), 0.001, 0} and PAL-B's adaptation ridge by k-shot validation (non-official choices made to prevent collapse and over-fitting).

## Appendix D. Where is the predictable structure? Estimators and results
**Estimators.** For an item with ratings on $K$ ordered levels, let $h$ be the empirical rating distribution and $C$ the cumulative operator. Split the item's raters at random into disjoint panels $P_1$ ($a$ raters) and $P_2$, and let $q$ be a cross-fitted *location-only* forecast with exactly the mode and mean of $P_1$ (built from other items in the same mode-and-mean cell). With $r_1 = C(h_1 - q)$, $r_2 = C(h_2 - q)$, $M = \|r_1\|^2/n$ and $X = \langle r_1, r_2\rangle/n$, the forecasting value of the raw distribution over its own location obeys the identity $S(h_1) - S(q) = M - 2X$ under the ranked probability score, so $\rho = X/M$ is a split-half reliability of the distribution's *shape* and the raw distribution beats its location exactly when $\rho > 1/2$. Text decodability is the proper-score gain $G = (2\langle \hat r, r_2\rangle - \|\hat r\|^2)/n$ of a residual $\hat r$ decoded from frozen text features, cross-fitted over prompt groups, reported as the fraction $G/X$ of the reproducible shape. The rater–item decomposition fits ordered-probit models $Y^*_{ir} = \theta_i + \delta_r + \sigma_i\sigma_r\varepsilon$ with item locations $\theta_i$, rater shifts $\delta_r$, rater scales $\sigma_r$ and item dispersions $\sigma_i$, compares held-out likelihood over random cells (every held-out rater and item appears in training), and chooses all penalties by inner cross-validation.

**Reproducibility.** With the split-half estimator defined above, the reliability of the rating distribution's shape beyond its exact mode and mean is ρ = 0.25 [0.22, 0.29] on MultiPref overall preference with three raters (helpful 0.29, harmless 0.21): the raw few-rater distribution forecasts a new rater worse than its own location (ρ < ½).
**Text decodability.** A cross-fitted ridge decoder on frozen Qwen2.5-7B-Instruct features, scored on an independent rater panel, recovers G/X = 10.5 % [5.7 %, 11.9 %] of the reproducible shape (within-cell permutation control ≤ 0; positive control 0.35) — comparable to the upper end for ordinal quality ratings (upper bounds 0.4–10 %) and below NLI (17–26 %).
**Rater vs item.** A long-format ordered-probit decomposition with real rater identities and penalties tuned by inner cross-validation: rater-specific thresholds improve held-out likelihood by +0.036 nats per rating over item location alone, item-specific dispersion by a further +0.0014 (ratio 25; 19–36 across the five folds); of the rater part, rater scale contributes +0.031 and rater shift +0.005.

## Appendix E. Protocols and what did not hold
All analyses are documented in an analysis log: timestamped internal protocols written before each stage (not public registrations, so they document rather than certify the order of decisions); changes after results are logged as amendments with reasons, and the symmetric style model DFs and its hypothesis were added after the first full result. Not supported or not robust: (i) the stage-1 decision rule returned "mixed" (text decodability not ≤ 10 %); (ii) non-inferiority of the 5-parameter DF to the low-rank latent (DF − DL ≥ −0.005) holds with the training-rater prior but not with a few-shot-tuned prior on MultiPref (−0.015) and is formally not met on PRISM (bound −0.006); (iii) "scale beats shift"  holds only on MultiPref; (iv) the originally registered probit-family hypothesis is not supported (F1 − D = +0.020 [−0.001, +0.041], the primary probit contrast after Amendment 1; homoscedastic F − D = −0.029 [−0.049, −0.008]; superseded when the primary family was moved to the distributional head); (v) the prediction that published user latents encode style  failed (R² ≈ 0); (vi) the hybrid's non-inferiority to DFs  is formally not met (bound −0.014). Four baseline problems found during the study were fixed in favour of the baselines — a missing constant column in the low-rank latent, a scale non-identifiability in the probit group model, VPL's posterior collapse, and PAL-B's near-unregularised adaptation — and the runs before each fix are reported.


===== FILE: paper-4/PROTOCOL_STAGE7.md =====
# Paper 4 — Stage 7: is the injected content dimension inside the learners' input space? (frozen before any result)
Committed 2026-11-01, after the seventh ICML-style review (4/10). Objection (checked in `make_synth.py`): the injected feature g2 is a random direction in the *whitened* top-256 PCs of the pair-difference embedding E_B − E_A, while VPL / PAL-B see a different PCA-256 basis over per-response embeddings and D / DL see PCA-256 of a joint (prompt, A, B) embedding; g1 (log length ratio) need not be linear in any of them. The detection limit of §5.6 may therefore mix representation mismatch with statistical difficulty. Any change after the first result is logged under "Amendments".

## S7-1: linear-probe availability of g1 and g2 (diagnostic)
For each learner input space, a cross-fitted ridge probe predicts the standardised g1 and g2 (exactly as `make_synth.py` computes them) on all MultiPref items: 5 folds by prompt group (the paper's item folds), ridge penalty chosen per outer fold by inner 5-fold CV over {10⁻², 10⁻¹, …, 10⁵}, out-of-fold R². Input spaces:
(a) VPL / PAL-B, PCA-256: [x_A, x_B, x_P] (768-d) as `vpl_pal.py` builds them, and the difference x_B − x_A (256-d), which is all a linear reward on responses can use for a pair;
(b) VPL / PAL-B, full features: x_B − x_A on the standardised 3,584-d embeddings;
(c) D / DL / DFs: the joint-embedding PCA-256 X of `factorised_rm.py`.
Positive reference: the 256-d whitened pair-difference basis Z of the generator itself (R²(g2) = 1 by construction).

**Reading (fixed now).** A component is called *available* to a learner if its probe R² ≥ 0.5, and *largely unavailable* if R² < 0.2. If g2 is largely unavailable to a learner, that learner's §5.6 detection limit is reported as partly a representation limit, not a statistical one, and S7-2 is run. The abstract's "the bottleneck is finding the content dimension, not the number of ratings" is softened in either case (the reference learner is given the features; that comparison does not separate the two).

## S7-2 (conditional on S7-1): in-span injection
If S7-1 finds g2 largely unavailable to any learner, τ5 and τ10 panels are regenerated with g2 replaced by a random unit direction in the span of that learner's pair-difference input (x_B − x_A, PCA-256 of `vpl_pal.py`; same seed rule, same calibration of τ to generator-oracle gains), and PAL-B (full features), VPL and the reference learner are re-run with the §5.6 outcome (own − other at k = 20, 50; detection = lower bound > +1 point). Exploratory; reported next to the original panels.

## Amendments

**Amendment 1 (2026-11-01 06:35, after the S7-1 result; before any S7-2 run).** S7-1 (`results/stage7_probe.md`): g1 is available to every learner (R² 0.73–0.93); g2 is available to VPL / PAL-B (PCA-256 x_B − x_A 0.65, full features 1.00) but largely unavailable to D / DL / DFs (joint PCA-256, R² 0.022). By the reading rule, the §5.6 limits of VPL and PAL-B are not a representation mismatch for this injection, while DL's is partly one, so S7-2 is run for **DL** (not VPL / PAL-B, for which g2 is available). The protocol text above said "in the span of x_B − x_A of `vpl_pal.py`", which is the wrong space for DL; S7-2 is therefore defined as: g2 replaced by a random unit direction (seed 0, as before) in DL's own input X (joint-embedding PCA-256, unit-variance columns, as `factorised_rm.py`), orthogonalised against the ridge consensus direction in X (λ = 1000, as before); g1 unchanged; same generator, θ seed 1, label seed 2, τ calibrated to generator-oracle gains of +5 and +10 points (tags `x5`, `x10`, `make_synth.py span`). Learners: DL with the few-shot-tuned prior (`--adapt_tune --perm_control`, k = 0, 20, 50, 5 folds) and the reference learner (`s5.py ref`, features known). Outcome as §5.6 (own − other at k = 20, 50; detection = lower bound > +1 point); reference learner on the oracle scale (own − population). Exploratory; reported next to the original panels. Reading: if DL detects the +10-point in-span panel, its §5.6 limit is attributed mainly to representation; if not, to the learner.
Also fixed in `make_synth.py` (no effect on existing panels): the `if ASP … else` target selection overrode the `seed` and `v2` targets; it was introduced at 14:52 on 2026-10-31, after those panels were generated (12:52, 13:57), and is now an `elif` chain.

**Amendment 2 (2026-11-01 06:51, before any run below; S7-2 results not yet seen).** **S7-3, seen-rater ceiling** (seventh review, Q2: is the ranking null specific to few-shot adaptation of *new* raters?). On real MultiPref (E1), for every fold, the models already trained on training raters × training items (D, DF, DFs, DL with the paper's selected penalties) are evaluated on the **training raters' ratings of the test items** (`idx_seen`, already used for the Stage-2 secondary LL): direction accuracy and LL per rating, each model minus D, and for DF, DFs, DL **own − other** (the trained rater parameters of a random derangement of the training raters within fold, seed 777 + fold). Each training rater contributes all of their training-item ratings (≈ 145 on MultiPref), so this is the many-ratings ceiling for the same model class. Rater bootstrap (seed 17), 5 folds. Reading (fixed now): if DL's own − other direction accuracy on seen raters has a lower bound above +1 point, the ranking null is stated as specific to few-shot new-rater adaptation; otherwise the paper states that it also holds for seen raters with all their ratings. Exploratory secondary: the same for PAL-B if its per-user weights for training users can be evaluated without code changes to training.

**Amendment 3 (2026-11-01 08:51, before any run below).** **S7-4, semantic injection axes** (seventh review W2: "semantically meaningful directions (verbosity, refusal, formality)"). The two injected features are replaced by observable style/content axes of the response pair, defined now (`sem_feats.py`): (s1) **formatting**: log(1 + number of lines of B that start with a markdown list or heading marker, regex `^\s*([-*+•]|\d+[.)]|#+)\s`) − the same for A; (s2) **hedging / refusal**: log(1 + count in B of a fixed case-insensitive phrase list: "i'm sorry", "i am sorry", "i apologize", "i cannot", "i can't", "i'm not able", "i am not able", "as an ai", "i don't have", "however", "it's important to", "it is important to", "please consult", "it depends", "may vary") − the same for A; each standardised. (Length, the third axis named by the review, is g1 of the original panels.) Same generator, θ seed 1, label seed 2, τ calibrated to oracle gains +5 and +10 (tags `sem5`, `sem10`, `make_synth.py sem`). Learners: reference learner (features known), DL (tuned prior), VPL and PAL-B (K = 2) on PCA-256 (E1, CPU), all with the permutation control at k = 20, 50, 5 folds; S7-1 probes of s1, s2 from each learner's inputs. Outcome and detection criterion as §5.6. Exploratory.

**Amendment 4 (2026-11-01 11:21, after S7-2 and S7-4; before any run below).** S7-2 rests on one draw. **S7-5:** the in-span panels are re-drawn with θ and label seeds 11, 12, 13 (as Stage 5 S5-2; same in-span g2, τ re-calibrated per seed to +5 and +10; tags `x5s{s}`, `x10s{s}`, `make_synth.py span <s>`), and DL (tuned prior) and the reference learner are re-run. The S7-2 statement "with g2 in its input, DL detects +10 points at k = 20" is kept only if it holds (lower bound > +1) in at least three of the four draws, and "does not detect +5" only if it fails in at least three of four; otherwise both are weakened to the range over draws.


===== FILE: paper-4/PROTOCOL_STAGE8.md =====
# Paper 4 — Stage 8: the ranking null on a dataset built for preference heterogeneity (frozen before any result)
Committed 2026-11-01, after the seventh ICML-style review (W3: MultiPref follows guidelines, DICES rates single responses, PRISM has few shared items; "add at least one dataset built for heterogeneous preferences"). Dataset: **Community Alignment** v1.1 (Zhang et al., 2026; Hugging Face `facebook/community-alignment-dataset`, CC-BY-4.0; 90,256 conversations, 3,603 annotators in five countries and languages; candidate responses sampled to be diverse). The data are not committed. Any change after the first result is logged under "Amendments".

## Panel
**First turn only** (later turns depend on the conversation so far). A conversation enters if its first turn has four responses and a preferred response. **Pairs:** the chosen response against each of the three others (A/B side randomised, seed 0); label = native choice (binary; the dataset has no graded strength, so scale use cannot help and only ranking is tested). Items are grouped by **first-turn prompt text**, so a pre-generated prompt shown to many annotators is in a single item fold. User-initiated and pre-generated prompts are both used.
**Features:** Qwen2.5-7B-Instruct, last-layer state at the final token of the chat-formatted (prompt, response) for each response (E_A, E_B; truncated at 4,000 characters each) and of the prompt alone (E_P). Texts are used in their original language. (PRISM used a judge-prompt embedding of each response; the difference is stated.)

## Protocol and methods
As PRISM pairs (Stage 2c Amendment 4): 5 annotator folds × 5 prompt-group folds, k ∈ {0, 5, 20, 50} adaptation pairs from training items, 5 draws, permutation control (own vs another test annotator's adapted parameters), rater bootstrap. Methods (`vpl_pal.py`, PCA-256 features as in the main tables): Dp (text-only), DFp, VPL, PAL-B (K = 2, 4), LoRe and LoRe-reg (Stage 6, unchanged hyper-parameter grids).

## Outcomes and decision rule (fixed now)
Primary, k = 20, choice accuracy in points: each method's own gain (method(k) − method(0)) and own − other.
- **Ranking null replicates on Community Alignment** if, for every method, both upper 95 % bounds are below +1 point.
- **Content personalisation detected** if any method's own gain or own − other has a lower 95 % bound above +1 point; the paper's ranking-null claims are then restricted to the three original datasets and the abstract is rewritten.
- Otherwise **inconclusive**, reported as such.
Secondary: the same at k = 50; log-likelihood; per assigned language. Learner-free: on response pairs rated by at least two annotators (pre-generated prompts, identical response texts), the rate at which two annotators make the same choice, against the text-only model's accuracy on the same pairs (is a population model already as good as another person?).

## Forbidden statements
Any statement about later turns, or about countries/languages beyond the per-language secondary analysis.

## Amendments


===== FILE: paper-4/PROTOCOL_STAGE9.md =====
# Paper 4 — Stage 9: a constructive method — screened attribute personalisation (SAP) (frozen before any result)
Committed 2026-11-01, after the user chose ICML and asked for more novelty, and after Stage 7 showed (i) that 20 ratings suffice statistically when the content axes are known (reference learner) and (ii) that the published learners fail because they do not find the axis (in-span and semantic injections; hedging/refusal is barely linear in the embeddings). The seventh review asked for a learner that must *discover* the axes from the training raters. SAP is that learner. Any change after the first result is logged under "Amendments".

## Method
**Attribute dictionary.** J = 24 interpretable, text-computable attribute differences a_i = attr(B) − attr(A) of each response pair, fixed now (`attr_feats.py`; each standardised over items): (1) log length ratio; (2) markdown list/heading lines; (3) hedging/refusal phrases (Stage 7 list); (4) code blocks; (5) bold/italic markup; (6) digits; (7) question marks; (8) exclamation marks; (9) first-person singular pronouns; (10) second-person pronouns; (11) mean sentence length; (12) mean word length; (13) paragraphs; (14) URLs; (15) example markers ("for example", "e.g.", "for instance", "such as"); (16) safety/disclaimer phrases ("consult", "professional", "not a substitute", "seek medical", "seek help", "disclaimer"); (17) summary markers ("in summary", "in conclusion", "overall", "to summarize", "in short"); (18) emojis; (19) evidence phrases ("according to", "studies", "research", "evidence", "source"); (20) politeness ("please", "thank", "glad", "happy to", "great question"); (21) strict refusal ("i cannot", "i can't", "i won't", "unable to", "not able to"); (22) type–token ratio; (23) word overlap with the prompt (fraction of the response's word types that occur in the prompt); (24) headings only (lines starting with #). Counts enter as log(1 + count); ratios as differences. The dictionary contains the two Stage-7 semantic axes (2, 3) among 22 others and the log length ratio (1); it does not contain the random embedding direction of the original panels.
**Model.** Estimated base log P̂ (text head D + rater style offsets DFs, fitted on training raters × training items, as the S5-1 reference learner) plus a rater content term (θ_rᵀ a_i)(−2, −1, 0, 1, 2) on the logits; θ_r ~ N(μ, diag(σ²_1 … σ²_J)).
**Screening (empirical Bayes on training raters only).** μ = one shared θ fitted on all training ratings (style offsets per rater). Each training rater's θ̂_r is fitted on all of their training ratings by MAP (weak prior N(μ, 10·I), style offsets refitted); its sampling variance v_rj is the diagonal of the inverse observed information Σ_i Var_i(step) a_i a_iᵀ + I/10. Then σ²_j = max(0, Var_r(θ̂_rj) − mean_r(v_rj)) (method of moments). Attributes with σ²_j = 0 are screened out (their weight is fixed at μ_j). **Adaptation of a new rater:** MAP of θ_r (and the rater's style offsets, ridge as S5-1) on the k adaptation ratings under this prior.
**Outputs:** per fold, the screened set and σ²_j (which attributes raters differ on, transferably), μ.

## Panels and protocol
MultiPref structure, the paper's folds, k = 20 and 50, five draws, permutation control (another test rater's θ and offsets) and the population contrast own − μ (own style offsets kept), rater bootstrap (seed 17) — identical to the S5-1 reference learner. Panels: real MultiPref; synthetic t0 (null), t5, t10 (original injection: length + random direction), sem5, sem10 (Stage 7 semantic injection), x10 (in-span). PRISM pairs and Community Alignment (binary) follow in an amendment with a logistic base.

## Outcomes and decision rules (fixed now)
**M1 (validity, null):** on t0, SAP's own − other and own − μ lower bounds at k = 20 are ≤ +1 point (no false detection).
**M2 (discovery):** on sem5 and sem10, SAP's own − μ lower bound at k = 20 exceeds +1 point (it finds axes that VPL, PAL-B and DL miss; Stage 7 S7-4); and the screened set contains attributes 2 and 3 in at least four of five folds. Reported against the reference learner told the features (an upper bound) and against the published learners.
**M3 (real data, primary):** on real MultiPref, if SAP's own − μ (direction accuracy, k = 20) has a lower bound above +1 point, the paper reports content personalisation along interpretable axes, and its abstract leads with it; otherwise the upper bound is reported as the bound on transferable individual weighting of these 24 axes, and the screened attributes (σ²_j > 0 in ≥ 4 of 5 folds) are reported as where raters' differences lie. Secondary: log-likelihood of SAP − the scale-use baseline DFs (same base), own − other, k = 50.
**Forbidden:** describing SAP as detecting content heterogeneity outside the dictionary; claims about other datasets before their amendment.

## Amendments

**Amendment 1 (2026-11-01 14:23, after SAP on real, t0, t5 selected no attribute in any fold; sem5 / sem10 / t10 / x10 runs cancelled unseen).** Diagnosis (t5, fold 0): the screening MAP fits with a weak N(μ, 10·I) prior over 24 attributes per rater (≈ 110 training ratings each) over-fit, so predictions become near-deterministic, the observed information collapses, and the estimated sampling variances (e.g. 0.81 for length) exceed the spread of the estimates; the method-of-moments σ² is then 0 everywhere — even for the injected length axis, whose one-dimensional between-rater s.d. is 0.26. The screening step is replaced by **Laplace-EM (automatic relevance determination)**: start at σ²_j = 0.1; iterate 15 times: MAP θ̂_r of every training rater under N(μ, diag σ²) (style offsets refitted), Laplace posterior covariance C_r = (Σ_i Var_i(step) a_i a_iᵀ + diag(1/σ²))⁻¹, update σ²_j = mean_r[(θ̂_rj − μ_j)² + C_r,jj], floored at 10⁻⁶. Adaptation of new raters uses the final diag σ² for all attributes; an attribute counts as **selected** if σ²_j > 10⁻³ (s.d. > 0.03 on the standardised attribute). M1–M3 unchanged; all seven panels re-run.

**Amendment 2 (2026-11-01 14:25, after fold-0 screening of t5, sem5 and real; before any t0, sem10, t10, x10 output and before any detection result).** The EM σ² ranks the injected axes first by an order of magnitude (t5: length 0.036; sem5: hedging/refusal 0.040, list/heading lines 0.039; all others ≤ 0.004), but the 10⁻³ "selected" threshold of Am. 1 is passed by nearly every attribute, because EM shrinks rarely-active attributes (emojis, URLs, code blocks) slowly — so M2's selection clause would be vacuous. **Selection is redefined with a null calibration:** attribute j is selected on a panel and fold if its σ²_j exceeds the largest σ²_j over the five folds of the null panel t0 (no rater content heterogeneity). The M2 selection clause and the M3 "where raters differ" report use this rule; the detection outcomes of M1–M3 are unchanged, and SAP's adaptation still uses all σ² as estimated.


===== UPDATE (Stage 9 results, after the documents above were written) =====
# Stage 9 — screened attribute personalisation (SAP)

| panel | own − μ, dir, k = 20 | own − other, dir, k = 20 | own − μ, dir, k = 50 | own − μ, LL ×100, k = 20 | selected in ≥ 4/5 folds (null-calibrated) |
|---|---|---|---|---|---|
| t0 | -0.19 [-0.50, +0.14] | +0.06 [-0.26, +0.39] | -0.50 [-0.92, -0.09] | -0.10 [-0.18, -0.01] | (null reference) |
| t5 | +1.36 [+0.73, +1.98] | +2.54 [+1.88, +3.24] | +1.41 [+0.59, +2.26] | +1.45 [+0.99, +1.97] | length, prompt overlap, second person, type-token ratio |
| t10 | +3.89 [+2.74, +5.04] | +6.19 [+5.06, +7.39] | +4.14 [+2.94, +5.54] | +3.76 [+2.74, +4.90] | code blocks, length, list/heading lines, paragraphs, prompt overlap, type-token ratio |
| sem5 | +2.69 [+1.70, +3.64] | +5.00 [+4.03, +5.99] | +3.98 [+2.70, +5.22] | +2.78 [+2.00, +3.60] | digits, hedging/refusal, list/heading lines, prompt overlap |
| sem10 | +7.53 [+5.92, +9.10] | +12.23 [+10.63, +13.82] | +9.35 [+7.60, +11.05] | +8.73 [+6.97, +10.57] | digits, evidence phrases, headings, hedging/refusal, length, list/heading lines, prompt overlap, safety/disclaimer, second person |
| real | +0.17 [-0.19, +0.55] | +0.45 [+0.03, +0.86] | +0.13 [-0.45, +0.63] | +0.22 [+0.03, +0.41] | bold/italic, code blocks, digits, first person, headings, hedging/refusal, length, paragraphs, prompt overlap, safety/disclaimer, second person, type-token ratio |

**Rules:** {"M1_no_false_detection": true, "M2_detect": {"sem5": true, "sem10": true}, "M2_select": {"sem5": true, "sem10": true}, "M3_real_content_personalisation": false}

Null thresholds (max σ² over t0 folds): length 0.0021, list/heading lines 0.0022, hedging/refusal 0.0018, code blocks 0.0023, bold/italic 0.0019, digits 0.0016, question marks 0.0018, exclamation marks 0.0018, first person 0.0013, second person 0.0015, sentence length 0.0028, word length 0.0016, paragraphs 0.0020, URLs 0.0036, examples 0.0016, safety/disclaimer 0.0016, summary markers 0.0015, emojis 0.0058, evidence phrases 0.0016, politeness 0.0016, strict refusal 0.0018, type-token ratio 0.0021, prompt overlap 0.0014, headings 0.0015
