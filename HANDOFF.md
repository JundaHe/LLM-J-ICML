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
