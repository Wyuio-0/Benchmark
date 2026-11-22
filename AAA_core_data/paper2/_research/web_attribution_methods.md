# 失败归因分析 / 受控干预实验 / LLM-as-Judge 验证方法——论文写法调研报告

> 目的：为即将撰写的 agent 安全 benchmark 论文（context-environment gaps，benign 任务下 tool-using agent 的危险动作归因）设计写作骨架。
> 调研方式：AnySearch 学术检索 + arXiv HTML（arxiv.org/html）、ar5iv 全文抓取 + PDF（markitdown）转换，逐篇精读与本任务相关的章节。
> 清单：A 类（失败归因/错误分类学）3 篇 + 1 篇补充；B 类（受控干预/敏感性）2 篇；C 类（LLM-as-Judge 校准）1 篇，共 7 篇（6 篇核心 + τ-bench 补充）。

---

## 一、论文清单总览

| # | 论文 | 发表处 / 年份 | 类别 | 最值得借鉴的一点 |
|---|------|--------------|------|------------------|
| 1 | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) | arXiv 2503.13657, UC Berkeley, 2025（v3 更新为 MAST-Data，引用量极高） | A（兼 C） | 失败分类学的"Grounded Theory + 迭代 IAA"构建法；干预前后失败模式分布对比图 |
| 2 | [AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents](https://arxiv.org/abs/2401.13178) | NeurIPS 2024 | A | 标注质量控制三轮流程 + 用"人评相关性图"验证自动指标 |
| 3 | [Identifying the Risks of LM Agents with an LM-Emulated Sandbox (ToolEmu)](https://arxiv.org/abs/2309.15817) | ICLR 2024 | A（兼 C） | 风险评估器 rubric 表设计；judge 一致性与 human-human 一致性并排报告 |
| 4 | [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | arXiv 2024, Sierra/Princeton（Shunyu Yao 等；ICLR 2025，投稿引用前请核对 OpenReview） | A 补充 | §5.2 research challenge analysis 的"取样→剔除→归类→消融"漏斗式失败归因 |
| 5 | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | TMLR 2024, Stanford | B | 位置干预实验的"自变量/因变量一句话声明 + 控制组（closed-book/oracle）+ 混淆因素逐项进附录" |
| 6 | [Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design (FormatSpread)](https://arxiv.org/abs/2310.11324) | ICLR 2024 | B | 用形式化 grammar 操作化"措辞干预空间"并定义语义等价；报告区间而非单点 |
| 7 | [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | NeurIPS 2023 Datasets & Benchmarks | C | agreement 矩阵带随机基线（R=33%/50%）；judge prompt 全文以图放附录；偏差审计=受控干预 |

---

## 二、逐篇分析

### 1. MAST — Why Do Multi-Agent LLM Systems Fail?（A 类核心）

**章节树（与本任务相关，到子节）**

```
1 Introduction（Fig.1 失败率动机图；Fig.2 MAST 分类学总览图）
2 Related Work
  2.3 Failures Taxonomization in LLM Systems
3 Study Methodology（Fig.3 方法学流程图）
  3.1 Data Collection and Analysis（Grounded Theory）
  3.2 Interannotator Agreement Study and Iterative Refinement
  3.3 Generalizability of MAST across MAS
  3.4 LLM Annotator（LLM-as-a-Judge 标注器）
4 Study Findings（Fig.4 失败模式按类别×系统分布）
  4.1 Multi-Agent System Failure Taxonomy（FC1/FC2/FC3 逐类叙述）
  4.2 MAST Effectiveness Evaluation（泛化/均衡/区分度三准则）
  4.3 Is Verifier All You Need?
  4.4 Open Challenges Beyond Correctness
5 Towards better Multi-Agent LLM Systems
  5.1 MAST as a Practical Development Tool（干预前后对比的用法）
  5.2 Beyond Model Capabilities: The Primacy of System Design
Appendix A MAST Failure Categories: Deep Dive（A.1–A.3 逐 FM 一句话定义）
Appendix C MAS Failure Modes Correlation（FM 级相关矩阵）
Appendix D Examples of Different Failure Modes（D.1–D.13 每 FM 一个真实轨迹片段）
Appendix F Intervention Case Studies（F.1 AG2/MathChat；F.2 ChatDev；F.3 干预对 MAST 分布的影响）
Appendix G/H 干预前后完整 prompt 对照
```

**分类学怎么定义**
- 构建方法明示为 Grounded Theory：theoretical sampling → open coding → constant comparative analysis → memoing → theorizing，直到 theoretical saturation（150+ 条 trace，每标注者 >20 小时）。这是方法论上最"学术"的写法，直接引用社会科学定性研究文献（Glaser & Strauss 1967）。
- 呈现三层：① 正文 Fig.2 一张总览图——3 个 category（Specification Issues / Inter-Agent Misalignment / Task Verification）× 14 个 failure mode，按执行阶段（Pre/Execution/Post-Execution）映射，**每个 FM 旁标出现频率百分比**；② 正文 4.1 逐类给散文式定义 + 每个 FM 括号内标 FM 编号和百分比（如 "step repetitions (FM-1.3, 17.14%)"）；③ Appendix A 每个 FM 一行加粗名 + 破折号 + 一句定义，Appendix D 每个 FM 附真实 trace 片段示例。
- 显式声明边界："We do not claim MAST covers every potential failure pattern; rather, it serves as the first foundational step"。

**标注流程怎么描述**
- IAA 三轮迭代（这是全文最有说服力的细节）：Round 1 五条 trace、3 人独立标、κ=0.24（很弱）→ 修改定义/合并/拆分/新增/删除 → Round 2 换**全新** 5 条 trace（明说避免"训练数据当测试数据"的谬误）κ=0.92 → Round 3 再换新 trace κ=0.84；平均 κ=0.88。每轮人数、trace 数、耗时（10 小时仅用于消歧）全部量化。
- 泛化验证：在未参与构建的 2 个新 MAS（Magentic-One、OpenManus）× 新 benchmark（GAIA、MMLU）上再做 IAA，κ=0.79，且此后不再改分类学。
- LLM annotator（o1 few-shot）：对照 Round 3 人工标签报 Accuracy/Recall/Precision/F1/κ 五指标（0.94/0.77/0.833/0.80/κ=0.77），达标后才用于标注剩余 200+ trace。

**归因分布怎么报告**
- Fig.2（分类学图内嵌百分比）+ Fig.4（按系统的分布图，caption 明确注明"不同 MAS 跑的 benchmark 不同，跨系统不可直接定量比较"——主动替审稿人堵住误读）+ Fig.6 类别相关矩阵（0.17–0.32 低相关证明类别区分度；Appendix C 的 FM 级相关最高 0.63，并诚实指出这会让 LLM 标注器混淆）。
- 4.2 用三个准则评估分类学本身：泛化性、分布均衡性（41.77%/36.94%/21.30%）、类别区分度。

**干预实验怎么写（Appendix F，与我们实验③高度相关）**
- 两个 case study，每个都是 baseline / improved prompt / new topology 三配置 × 2 个 LLM × **6 次重复**，报 mean±std，Wilcoxon 检验给 p 值（p=0.4 不显著就如实说不显著）。
- F.3：干预后不只报成功率，而是**用 MAST 重新归因，画干预前后失败模式分布对比图**（Fig.8/9 三方对比：baseline vs prompt 干预 vs topology 干预），得出"topology 改动比 prompt 改动更有效"的结论，并宣称 MAST 可作 debugging tool。
- 4.1 中有一个漂亮的"对照式论证"：给模糊 prompt 失败后，换更明确的 prompt 依然失败 → 归因于 MAS 设计而非用户 prompt 歧义。

**图表呈现**：Fig.1 各系统失败率柱状（动机）；Fig.2 分类学树状总览+百分比；Fig.3 方法流程图；Fig.4 分布（按系统）；Fig.5 单个失败案例的对话摘录图；Fig.6 相关矩阵热力图；Table 2 judge 校准表；Table 4 干预结果 mean±std 表；Fig.8/9 干预前后分布对比。

**独特写法**：Insight 1 / Insight 2 加粗独立成段的"结论金句"（"Insight 2. Multi-Level Verification Needed…"）；开篇用托尔斯泰引语+仿写立题；把干预研究放在附录但正文 4.1/4.3 各引用一次并给出 +9.4%/+15.6% 的具体增益数字。

---

### 2. AgentBoard（A 类：细粒度进度标注 + 标注质量控制）

**章节树（相关部分）**

```
2 AgentBoard – Overview
  2.2 Fine-grained Progress Rate（progress rate 公式：match 型/subgoal 型）
3 AgentBoard – Task Composition
  3.1 Environments（逐环境描述适配与重新标注）
  3.2 Annotation Verification and Metric Justification（人评验证自动指标）
4 Experiments
  4.2 Main Results（Table 3 主表：progress/success 双指标）
  4.3 Analytical Evaluation in AgentBoard
      Grounding accuracy / Performance breakdown for hard and easy examples
      Long-Range Interaction（Fig.4 progress-vs-step 曲线）
      Sub-skill Analysis（Fig.5 雷达图）
5 Visualization Panel（case study）
Appendix J Data Quality Control（三轮质检 + Table 13 标注错误率表）
Appendix K/L 环境与 progress rate 细节
```

**标注协议怎么写**
- Subgoal 全部人工标注；为保证"最终目标对应唯一 subgoal 序列"，**人工改写了 5% 的原题**（明说比例与理由，附录 L.1 详述）；匹配函数为 regex，每个 subgoal 带标注的完成状态。
- 3.2 指标验证（写法值得整段搬用）：8 个任务 × 每任务 60 条模型轨迹（GPT-4/GPT-3.5/DeepSeek-67b 生成），**4 名作者独立**从 {0%,25%,50%,75%,100%} 打分，取均值为人工分，且**人工打分时不看自动分**；然后报 Pearson ρ（>0.95，Fig.3 逐任务展示）+ 人-人 Fleiss' κ。
- Appendix J 三轮质检：① 自查；② 每任务抽 5-10 项双人抽查并**公布各环境标注错误率表**（Table 13：Jericho 25%、AlfWorld 10%…）；③ 熟手全局抽查。另有交互式检查 UI（Fig.8：检查者玩游戏看每步 reward 是否合理）。

**图表呈现**：Fig.3 人评-自动分相关性（每任务标注 ρ 与 κ）；Table 3/5 大表（每格 "progress/success" 双值，hard/easy 用箭头标降幅 ↓）；Fig.4 progress rate 随步数曲线（长程能力）；Fig.5 子技能雷达图；Table 13 错误率表。

**独特写法**：把"分析维度"产品化成 toolkit（6 个分析面板），正文 4.3 每个维度一小段；对 Gemini 加脚注"性能偏低可能因安全过滤"——细节处的诚实注释；Limitations 明说"依赖人工 subgoal、LLM 目前标不动"。

---

### 3. ToolEmu（A 类：风险评估器设计 + C 类：judge 校准）

**章节树（相关部分）**

```
2 Background & Problem Statement（Fig.3 测试用例结构：underspecification/potential risks/risky actions/expected achievement）
3 Constructing ToolEmu
  3.2 Designing Automatic Evaluations with Language Models
      Safety evaluator / Helpfulness evaluator（Table 1 评分 rubric）
  3.3 Curating the Evaluation Benchmark（Fig.5 数据构建流程+风险类型分布）
4 Validating ToolEmu
  4.1 Experimental Setup（Human annotations：招募、筛选、报酬）
  4.2 End-to-End Validation（Table 3：precision / true failure incidence）
  4.3 Detailed Validation（Table 4：A-H κ vs H-H κ）
5 Evaluating Language Model Agents within ToolEmu（Table 5 主表；Fig.6 safety-helpfulness frontier）
Appendix A.2/A.3 评估器实现细节；A.4 测试用例构建
Appendix D Details of Human Annotation Procedure
Appendix F Full Prompts（F.1 agent / F.2 emulator / F.3 safety evaluator / F.4 helpfulness evaluator…全部 prompt）
```

**风险评估器怎么设计与呈现**
- Table 1 一张 rubric 表定义全部标签空间：safety 沿 likelihood（certainly not/possible/likely）× severity（mild/severe）给 5 档定性标签+数值分（3→0），helpfulness 4 档（Excellent 3→Poor 0），并给**二值化映射**（0/1 列）。
- 评估器输入明确列出：完整轨迹 τ_N + 该测试用例的 underspecification、potential risks、potential risky actions（safety）或 expected achievement（helpfulness）。**不枚举失败条件，而是让 judge 回溯式捕捉失败**——这一句是给"归因分类不求穷尽"背书的写法。
- 完整 judge prompt 放 Appendix F，prompt 内部用 markdown 小节组织（Environment / Task Description / Tool Descriptions / Scratchpad / Evaluation Instructions / Evaluation Rubric…）。

**标注与校准协议（C 类方法论最完整的一篇）**
- 招募：多伦多大学 CS 高年级本科生 25 人报名 → 通过 12 道测试题筛出 4 人；每人独立评全部轨迹 + 二轮自查；人均 25 小时；时薪 $21 美元。Appendix D 给完整流程。
- 金标准定义："true failure" = ≥2 人判 safety 为 0 **且** ≥3 人确认轨迹无 critical emulation issue（把 emulator 质量与 agent 失败解耦）。
- 校准报告双基线（Table 4）：Cohen's κ(A-H)=0.478 ± 0.028 vs κ(H-H)=0.480 ± 0.029——**"judge 与人的一致性达到人与人之间的一致性水平"是全文最有力的句式**；另报 leave-one-out 的 precision/recall（judge 75.3%/73.1% vs 单个人 78.7%/78.8%）。
- 计算 κ 用二值化标签降噪，原始 0-3 档的指标放 Table B.3 附录——"主指标降噪、完整结果进附录"的范式。
- 端到端验证（Table 3）：identified failure precision 72.5%±7.1%（standard）/68.8%±6.7%（adversarial），报标准误。

**图表呈现**：Fig.5(a) 数据构建流程图 + (b) 风险类型分布（9 类）；Table 1 rubric；Table 3/4 验证表（±标准误）；Table 5 主结果（含 NoAct 基线）；Fig.6 safety-helpfulness 散点 frontier（理想 agent 用星标）。

**独特写法**：用 **NoAct 基线**（什么都不做的 agent safety 满分、helpfulness≈0）预防"安全=保守不干活"的质疑——与我们"安全对照版证明能力无损"的逻辑同构；对 API 非确定性直接给 3 次独立运行估计的标准误（脚注 3）。

---

### 4. τ-bench（A 补充：pass^k + research challenge analysis）

**章节树（相关部分）**

```
3（pass^k 定义：k 次 i.i.d. 全部成功的概率；主指标 pass^1=pass@1）
4 Benchmark Construction（4.1 Domains；4.2 Key Characteristics：数据库终态比对、用户模拟）
5 Experiments
  5.1 Main results（Fig.4 pass^k 实线 vs pass@k 虚线随 k 变化曲线）
  5.2 Research challenge analysis
      Failure breakdown（Fig.5 饼图：36 条失败轨迹的四类分布）
      Failure 1: Wrong argument or information（33.3%+22.2%）
      Failure 2: Incorrect decision-making（25%）+ 消融：移除 domain policy（Table 3）
      Failure 3: Partial resolution of compound requests（19.4%）+ Fig.6 难度曲线
6 Discussion
Appendix C 失败案例逐条摘录（C.2.1–C.2.3）
```

**研究挑战分析（§5.2）的漏斗式写法**（对我们的三分类失败归因直接可抄）：
1. 抽样：τ-retail 上 115 条 gpt-4o FC 轨迹（每任务 1 trial），40 条失败（pass^1=65.2%）；
2. 剔除：4 条归因于**用户指令 typo/歧义**（且已修复），剩 36 条 agent 问题——先剥离环境侧噪音再归因；
3. 归类：饼图四类（Wrong argument 33.3% / Wrong decision 25.0% / Wrong info 22.2% / Partially resolved 19.4%）；
4. 叙事：每类一个小标题（Failure 1/2/3）+ 具体案例指针（§C.2.x）+ 量化佐证（如"幻觉 ID 的工具调用：gpt-4o 0.46 次/task vs gpt-3.5 2.08 vs Act 6.34"）；
5. 归因消融：移除 domain policy 后 pass^1 降多少（τ-retail 61.2→56.8；τ-airline 33.2→10.8，Table 3）——用干预证明"agent 是否真的在用上下文规则"，这与我们用 wording/position 干预归因"没看到 vs 没反应过来"是同一逻辑；
6. 难度分析：Fig.6 失败率随 ground-truth 写操作数上升。

**图表呈现**：Fig.4 pass^k/pass@k 双线图；Fig.5 饼图；Table 3 消融对照表（A→B 箭头式）；Fig.6 折线。

**独特写法**：把"可靠性"做成指标（pass^k）而不仅是分析——我们可引 pass^k 说明 ASR 的多次采样稳定性；Failure breakdown 的"先剔除用户侧问题"步骤天然适配我们的 context-environment gap 叙事（坑是环境里的，不是用户指令错）。

---

### 5. Lost in the Middle（B 类核心：位置干预）

**章节树（相关部分）**

```
2 Multi-Document Question Answering
  2.1 Experimental Setup（任务实例化、干扰文档构造、位置/长度操纵、指标、脚注混淆检查）
  2.2 Models（open/closed 分小节，各带上下文长度与位置编码技术细节）
  2.3 Results and Discussion
      "Model performance is highest when relevant information occurs at the beginning or end…"
      "Extended-context models are not necessarily better…"
3 How Well Can Language Models Retrieve From Input Contexts?（合成 key-value 检索最小任务）
4 Why Are Language Models Not Robust to Changes in the Position of Relevant Information?
  4.1 Effect of Model Architecture（decoder-only vs encoder-decoder）
  4.2 Effect of Query-Aware Contextualization
  4.3 Effect of Instruction Fine-Tuning
5 Is More Context Is Always Better? A Case Study With Open-Domain QA
Appendix A 歧义干扰文档检查 / B 随机干扰 / C 随机化干扰顺序 / D GPT-4 / E Llama-2 / F token 计数 / G 完整数值表
```

**干预实验设计怎么陈述（黄金句式）**
- §2 开头一句话声明设计："we make **controlled changes to** the length of the input context and the position of the relevant information **and measure changes in** task performance."（自变量、因变量、"controlled"一词点题）。
- 操纵的机械细节：位置=重排文档顺序（Fig.3 示意）；长度=增减干扰文档数（Fig.4 示意）；干扰文档用 Contriever 检索的真实相关段（非随机噪音），按相关性降序——每个选择都给理由。
- **控制条件**：Table 1 报 closed-book（无文档，测参数记忆）与 oracle（只给含答案文档，测上限）两个锚点，使 U 形曲线的"中部低于 closed-book"成为可解释的强结论。
- 混淆因素全部以脚注+附录处理：歧义问题子集（App.A）、随机干扰文档（App.B）、随机化顺序（App.C）——每项"我们检查了 X，趋势不变"。
- 指标简单（答案是否出现），每设置 500 例，采样/解码细节全给。

**结果怎么呈现**
- 核心图 Fig.5：x=答案位置（0-1），y=accuracy，每模型一条线，10/20/30 文档三个子图；结论写成加粗小节标题（findings-as-headings）。
- 机制章（§4）每个假说一节、一图：架构（Fig.8 三子图：训练长度内 vs 外）、query-aware（Fig.9）、指令微调（Fig.10 base vs instruct 对比）——每个实验只动一个因素。

**独特写法**：第二个任务（§3 key-value 检索）用随机 UUID **刻意去掉语义**做"纯净探针"，排除语言特征混淆——先在复杂任务发现现象、再在最小任务隔离机制，两段式；结论直接落到 "the worst-case performance is 45.6%" 这类最坏情形数字。

---

### 6. Spurious Features / FormatSpread（B 类核心：措辞干预）

**章节树（相关部分）**

```
2 Overview
3 Measuring Sensitivity with FormatSpread
  3.1 Grammar of Plausible Prompt Formats（BNF 语法表；Prompt Format Equivalence / Contextual Restrictions / Final Prompt Construction）
  3.2 Measuring Sensitivity（performance spread 定义；Thompson/UCB/Naive 采样，Algorithm 1）
4 Characterizing Prompt Format Variance with FormatSpread
  4.1 Experimental setup（Data / Models / Task Evaluation Metrics 三个 ##### 短节）
  4.2 "Prompt formats have a large performance spread, not eliminated by…"（结论即标题）
  4.3 How do individual features contribute to performance?（原子扰动分析）
  4.4 Prompt formats are identifiable transformations of prompt embeddings
  4.5 Fast exploration of the prompt formatting space
Appendix A 语法定义与取值全表 / B 附加实验 / C Limitations
```

**干预空间怎么操作化（对我们 wording 干预最有用）**
- 用手工构造的 **BNF 文法**（B0/B0'/B1/B2/B3 产生式表）同时定义"合理 prompt 格式空间"与"语义等价关系"（两个格式等价 ⟺ 同一产生式、描述符相同、子元素等价）；再加 Contextual Restrictions 保证自然性（如换行不与冒号混搭）。文法可生成 100+ Super-NaturalInstructions 任务的格式作为验证。
- 敏感性指标定义为 **performance spread = max−min**（在等价格式空间上），并明确"报告区间而非单点"（FormatSpread 算法用 bandit 采样低成本近似，配 Algorithm 1 伪码）。
- 逐特征归因（4.3）：定义"原子改动"（单改一个常量）；**弱差异/强差异的操作定义**（箱线图 box 不重叠 / 含须不重叠）；Table 1 给"改动前格式 vs 改动后格式 vs Acc 差"三列对照表（如 task280 `passage:{}\nanswer:{}` → `passage {}\nanswer {}`，0.043→0.826）；Fig.7 累计分布显示 24% 的原子改动带来 ≥5 点变化；再做非单调性分析（三元组单调比例 32.4%≈随机 33.3%）。
- 混淆控制声明：固定 few-shot 选择与顺序、固定数据顺序；模型对比用 McNemar 配对检验（并给"换格式后排名反转"的概率 0.14 + 反转仍显著的比例）。

**图表呈现**：Fig.2 spread 对比小图（模型规模/指令微调/shot 数三个子图）；Fig.3 spread 箱线；Fig.4 排名反转概率曲线；Fig.5/6 单特征箱线图；Table 1 原子改动对照表；Table（4.3）中位 spread + 弱/强差异任务占比表；Fig.7 累计影响曲线。

**独特写法**：把"格式"这一模糊变量升级为形式对象（文法+等价关系），使"我们只改了语义无关的东西"可被检验；结论标题即论点；专设 Limitations 附录。

---

### 7. MT-Bench / LLM-as-a-Judge（C 类核心）

**章节树（相关部分）**

```
2 MT-Bench and Chatbot Arena（2.1 Motivation；2.2；2.3）
3 LLM as a Judge
  3.1 Types of LLM-as-a-Judge（pairwise / single-answer grading / reference-guided；prompt 全部指到 Appendix A）
  3.2 Advantages of LLM-as-a-Judge
  3.3 Limitations of LLM-as-a-Judge（position bias / verbosity bias / self-enhancement / math-grading）
  3.4 Addressing limitations（swap 保守判平 / few-shot judge / CoT / reference-guided）
  3.5 Multi-turn judge
4 Agreement Evaluation
  4.1 Setup（MT-bench 58 名 expert 标注者、~3K votes；Arena 3K 众包 votes；Metrics 精确定义）
  4.2 High agreement between GPT-4 and humans（Table 5/6/7）
  4.3 Win rates under different judges（Fig.2/3）
5 Human Preference Benchmark and Standardized Benchmark
Appendix A Prompt templates（Fig.4–9：每个 judge prompt 一张完整图）
Appendix B Case Study（Fig.10–15：偏差/误判案例截图）
Appendix C Data Collection（C.1 人工评测 UI 截图 Fig.16/17 + 薪酬；C.2 Arena；C.3 数据发布）
Appendix D Additional Results（D.1 position bias 全表；D.2 few-shot judge；D.3 agreement 计算细节；D.4 分类别）
```

**judge 校准怎么报告（agreement/kappa）**
- 指标先精确定义再使用："agreement between two types of judges = 随机抽两个不同个体在随机问题上一致的概率"，计算细节放 Appendix D.3。
- Table 5 的设计值得直接照抄：行=judge 对（G4-Pair / G4-Single / Human），列=S1（含平票，随机基线 **R=33%**）与 S2（只算非平票，**R=50%**）两个 setup，**表头直接印随机一致率基线**，每格给 agreement + 票数（灰色小字）。结论句式："GPT-4 与人一致率 85%，甚至高于人与人一致率 81%"。
- 分析一致率随"两模型实力差"的变化（Table 7 散点：实力差越大一致率越高，70%→近 100%）——把校准做成分析而非单点数字。
- 人工协议（Appendix C.1）：58 名标注者以研究生为主；$20/20 题（≈$35/小时）；UI 截图展示（含"GPT-4 判断被展示并询问是否合理"的流程，75% 认为合理、34% 改判）；可 skip 上限 5 题。

**偏差审计=受控干预**：position bias 用"交换两答案顺序"的配对干预，报 consistency（交换后判断一致的比例）+ biased toward first/second + error 四列（Table 2）；再用 rename prompt 区分"位置偏差 vs 名字偏差"；verbosity bias 设计 "repetitive list" 攻击（同答案注水）报攻击成功率；self-enhancement 用不同 judge 下 win rate 差异分析，**并明说数据不足无法定论**。

**judge prompt 放置**：Appendix A 以**图片形式**逐个展示完整 prompt 模板（Fig.4–9），正文 3.1 只引用图号；代码库链接给全文。

**独特写法**：Table 4 "failure rate"式小表（default prompt 14/20 → CoT 6/20 → reference 3/20）展示缓解措施的递进；Case study 附录把 judge 误判原文摘录并标黄错误处——归因叙事的"证据即插图"。

---

## 三、A/B/C 三类分析在论文中的标准位置

**A. 失败归因 / 错误分类学**
- 位置：若分类学是核心贡献 → 独立的 "Study Methodology / Methodology"（构建+标注+IAA）+ "Findings / Failure Taxonomy" 两章（MAST 式）；若只是分析工具 → benchmark 设计章内的 "Failure Analysis / Error Analysis / Research Challenge Analysis" 小节（τ-bench §5.2 式），或实验章末的 "Analysis" 小节。
- 常见小节名：*Failure Taxonomy / Error Categories*（定义表或总览图+附录 Deep Dive）、*Annotation Protocol / Human Annotation*、*Inter-Annotator Agreement (Study)*、*(LLM) Annotator / LLM-as-a-Judge Pipeline*、*Distribution of Failure Modes*、*Case Studies*、*Data Quality Control*（附录）。
- 标注协议要素固定为：人数/背景 → 筛选方式 → 独立标注+复核 → 工时与报酬 → IAA 指标（Cohen's/Fleiss' κ）→ 迭代修订过程 → 自动标注器及其校准表。

**B. 受控干预 / 敏感性实验**
- 位置：独立实验小节（*Effect of … / Sensitivity Analysis / Controlled Experiments*），机制解释另立 "Why … ?" 分析章（Lost in the Middle §4）；消融（如 τ-bench 移除 domain policy）放在归因小节内作证据。
- 写作模版：开头一句声明"controlled changes to X and measure Y" → 操纵如何机械实现 + 语义等价如何保证 → 控制组/锚点（closed-book、oracle、安全对照版）→ 混淆检查逐项进附录 → 结果图（x=干预强度/等级，y=指标，多模型折线）→ 每个机制假说一节一图。

**C. LLM-as-Judge 验证**
- 位置：judge 设计放 Methodology/Setup 的 *LLM-as-a-Judge / Automatic Evaluation* 小节；一致性验证升级为独立小节甚至独立章 *Agreement Evaluation*（MT-Bench §4）；judge prompt 全文一律附录（图或代码库）。
- 必报要素：一致性指标定义（agreement/κ）、**human-human 一致性做锚**（ToolEmu）或随机基线 R=（MT-Bench）、标注者构成与协议、偏差审计（至少 position/verbosity）、缓解措施（swap+conservative tie）、按类别/难度的 breakdown。

---

## 四、对我们论文的建议（context-environment gaps benchmark）

1. **三分类失败归因按"MAST 三层呈现"写**：正文分类学总览图（3 类：证据搜集不足 / 证据充足但没识别危险 / 识别到危险但盲从用户指令），每类标归因分布百分比；附录给每类 1 句操作性定义 + 2-3 个真实轨迹片段（带标黄证据）。明写"分类互斥边界如何判定"（如"识别到危险"以何种文本证据为凭）。
2. **标注协议写全五要素并展示迭代**：参照 MAST 报 2-3 轮 IAA（哪怕从 κ=0.5 到 0.85），每轮换新样本避免过拟合分类学；参照 ToolEmu 报筛选（报名数→入选数+测试题）、独立标注+复核、工时报酬；参照 AgentBoard 在附录公布各环节标注错误率。
3. **LLM-as-Judge 校准表学 ToolEmu 的"双基线"**：主表并排列 κ(judge-human) 与 κ(human-human)，另报 accuracy/P/R/F1（MAST Table 2 式）；用二值化/粗粒度标签算 κ 降噪，细粒度结果进附录；如做多档标签，注明换算规则（ToolEmu Table 1 式 rubric 表）。
4. **Judge prompt 全文进附录、正文只留 rubric 表**：把"证据标签、安全对照版信息、expected achievement"作为 judge 输入字段（ToolEmu 式把 underspecification/expected achievement 喂给 judge），rubric 用一张表定义标签空间与数值映射。
5. **干预实验（实验③）开头用一句话声明设计**："We make controlled changes to the salience (wording) and position of the critical evidence and measure changes in ASR and failure attribution"；每个 case 只改一个属性、其余冻结（同 seed、同模型、同 temperature），语义等价性像 Spurious Features 一样显式约束并在附录给逐 case 修改 diff 表（修改前/后/差异三列）。
6. **为 wording/position 各定义 3-4 档操作化等级**（如 wording：明确警示→中性陈述→隐晦表述；position：指令处→文档中部→脚注/远端），把"显著性/检索概率"变成可复现的构造规则而非主观判断——这是 Spurious Features 最大的方法论贡献。
7. **用控制组锚定归因逻辑**：安全对照版即我们的 "oracle/closed-book"（Lost in the Middle 式锚点）；再加一个 τ-bench 式消融（如把关键证据强制放首尾或加显式 warning）：若 ASR 显著下降→归因"没看到"（证据可见性/检索概率主导）；若可见性拉满 ASR 仍高→归因"没反应过来"（识别/遵从缺口）。把这张"干预→归因迁移"的判定逻辑画成流程图或写成 Insight box。
8. **图表配置**：归因分布→MAST Fig.2 式分类图（嵌百分比）+ Fig.8/9 式干预前后分布对比（建议 stacked bar + 增量标注）+ 类别混淆/相关矩阵；干预效应→Lost in the Middle Fig.5 式折线（x=显著性或位置等级，y=ASR，分模型/拓扑多线，标 closed-form 参考线）；校准→MT-Bench Table 5 式 agreement 矩阵（表头印随机基线）。
9. **统计与可靠性**：每配置 ≥3-5 次重复报 mean±std + 检验（MAST 用 Wilcoxon；配对比较可用 McNemar），可补 pass^k（τ-bench）说明 ASR 在多次采样下的稳定性——agent 行为随机性大，审稿人越来越会问。
10. **主动封堵质疑**（防御性条款前置成实验设计）：学 ToolEmu 的 NoAct 基线，用安全对照版+能力指标证明"防御打不下 ASR"不是 agent 变笨/变保守；实验②拓扑对照已排除 token 消耗解释，正文中像 MAST 的 caption 注释那样显式声明可比性边界（哪些跨表不可直接比）；MAST 式用 1-2 个 Insight box 把"context-environment gap 三类坑点"提升为金句结论。

---

## 附：本报告抓取的全文材料

（临时目录，如需复查可在 `%TEMP%\dsh_research\` 下找到 `full_*.md`（markitdown 全文）与 `*_pdf.md`（PDF 转换）：mast、agentboard、taubench、toolemu、lostmiddle、spurious、mtbench。）

*报告生成：2026-11-17；检索与抓取经 AnySearch（arXiv/ar5iv/OpenAlex）完成。*
