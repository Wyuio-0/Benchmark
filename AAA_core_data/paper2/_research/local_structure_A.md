# 优秀 Benchmark 论文全文写作结构提取（5 篇参考论文）

> 调研对象：WebArena (2307.13854, ICLR 2024)、ToolEmu (2309.15817, ICLR 2024)、SWE-bench (2310.06770, ICLR 2024)、τ-bench (2406.12045)、AgentDojo (2406.13352, NeurIPS 2024 D&B)。
> 目的：为我们的 benign tool-using agent 安全 benchmark 论文（context-environment gaps）设计论文骨架。
> 方法：PDF → markitdown 全文转写后按编号标题建章节树，选择性精读引言 / 构建 / 实验 / 讨论部分。

---

## 一、逐篇论文结构拆解

### 1. WebArena (ICLR 2024) — 环境 + 任务 + 程序化验证型 benchmark

#### 1.1 章节树（到子节粒度）

```
Abstract
1 Introduction
2 WebArena: Websites as an Environment for Autonomous Agents
  2.1 Controlling Agents through High-Level Natural Language   （形式化 E=<S,A,O,T> + reward）
  2.2 Website Selection                                        （域选择依据 + 实现方式）
  2.3 Observation Space
  2.4 Action Space                                             （含 User Role Simulation）
3 Benchmark Suite of Web-Based Tasks
  3.1 Intent Collection                                        （含 IntentAnalysis：三类意图分类）
  3.2 Evaluation Annotation                                    （含 Unachievable Tasks / AnnotationProcess / HumanPerformance）
4 Baseline Web Agents
5 Results
  5.1 Analysis                                                 （两个问句式 run-in 小节）
6 Related Work
7 Conclusion
Acknowledgement / References
A Appendix
  A.1 Website Implementation / A.2 Environment Delivery and Reset / A.3 User Roles Simulation
  A.4 Intent Distribution / A.5 Human Performance / A.6 Experiment Configurations
  A.7 Prompt for Fuzzy Match / A.8 The Accuracy of Fuzzy Match Function
  A.9 The Prompts of the Baseline Web Agents / A.10 Additional Error Analysis
```

#### 1.2 各节一句话概括

- **Abstract**：环境（4 个真实网站域+工具+知识库）→ benchmark（812 任务）→ 最强 agent 14.41% vs 人类 78.24%。
- **1 Introduction**：自主 agent 需要"真实且可复现"的环境 → 现有环境过度简化/静态/表面匹配 → 引出 WebArena 及三大交付物 → 基线结果与人类差距。
- **2**：环境设计总述；2.1 给出 MDP 形式化与 reward 定义；2.2 用作者浏览器历史分析决定 4 个网站类别并开源实现+Docker；2.3 观察空间三种渲染（screenshot/DOM/accessibility tree）+ 多标签页；2.4 复合动作空间+元素 ID 选择方式。
- **3**：812 个任务的构建；3.1 标注者写意图的三条准则（abstract/high-level、creative、模板化+变量实例化）→ 241 模板 812 实例，三类意图（Information Seeking / Site Navigation / Content & Config）；3.2 逐类给出评分函数（exact_match / must_include / fuzzy_match 用 GPT-4 判；programmatic reward 查数据库/URL/JS），另有 Unachievable tasks（评估"不编造"能力）、双标注+第三仲裁的质控、human performance 测量。
- **4**：3 个 LLM × 2 种 prompting（direct / CoT）基线，UA hint 设计，与人类指引对齐。
- **5**：主表（模型 × prompting × SR/SR_AC/SR_UA，含 Human 行）；5.1 两个问句式分析："Do models know when to stop?"（UA hint 消融）与 "Can a model maintain consistent performance across similar tasks?"（模板内成功率直方图）。
- **6 Related Work**：用 Table 4（Dynamic/Realistic/Diverse/Functional 四维对比矩阵）论证差距。
- **7 Conclusion**：一句话复述贡献 + 14.41% vs 78.24% + 呼吁。
- **Appendix**：实现细节、重置脚本、用户角色、意图分布、人类表现细节、fuzzy match prompt 与准确率（≈近满分，即 judge 验证）、基线 prompt 全文、错误分析。

#### 1.3 引言组织方式

- 推进逻辑：**愿景（agent 做日常任务）→ 需要真实且可复现的环境 → 缺口（现有环境简化/静态/表面匹配三点并列，各带引文）→ 本文 WebArena（逐段对应 §2 环境、§3 benchmark、§4 基线实验）→ 结果数字与人类差距 → 开源链接**。
- 贡献点：**不列 bullet，而是 3 个自然段**，每段以 "We introduce WebArena…(§2)" / "Along with WebArena, we release a ready-to-use benchmark with 812 tasks (§3)" / "We use this benchmark to evaluate…(§4)" 开头，段内即展开细节（论文的三大组件直接映射三个章节）。
- **Figure 1**：整个环境总览图——4 类网站 + 工具 + 知识库 + agent + 程序化 validator，附两个示例 intent，是"系统组件图"。

#### 1.4 Benchmark 构建呈现方式

- **分类体系**：意图三分类（Information Seeking / Site Navigation / Content & Configuration），在 §3.1 末尾给出，配 Figure 5 示例、Figure 6 分布直方图。
- **收集→扩展流程**：标注者先探索网站 → 按三条准则写意图 → 模板化（可替换变量 + 多个实例化）→ 241 模板扩展为 812 实例（平均 3.3 实例/模板）；还给标注者 ChatGPT prompt 作灵感来源。
- **质控**：参考答案双人标注、分歧第三人仲裁；程序化 eval 由 3 位作者实现；标注者必须完整执行任务并核查中间状态；另测 human performance（5 名研究生，78.24%）作为难度锚点。
- **统计表**：Table 1（评分函数示例：Function ID/Intent/Eval Implementation，5 行示例覆盖全部评分函数）放在 §3.2；human performance 小表也在 §3.2；无单独统计表章节，数字散在正文。

#### 1.5 评价协议与指标呈现方式

- 两类 reward 明确命名：**r_info**（文本答案对比，三档评分函数 exact_match / must_include / fuzzy_match，逐一说明适用场景；fuzzy_match 用 gpt-4-0613 判语义等价，附录 A.8 验证其近满分准确率）与 **r_prog**（程序化检查中间状态：locator 取关键内容 + 关键词断言，复用 exact_match/must_include）。
- Table 1 用 5 个真实示例把每个评分函数落到具体实现（"评分函数+示例实现"一张表讲清）。
- Unachievable 任务：期望 agent 输出 "N/A"，评估"避免无根据断言"。

#### 1.6 实验部分组织

- 主实验（§5 Table 2）：模型 × prompting 策略全因子，报告 SR / SR_AC / SR_UA + Human 行作上限锚点。
- §5.1 两个问句式分析小节，每个回答一个具体问题并支撑一个结论：
  - "Do models know when to stop?" → UA hint 消融（Table 2 换列对比），支撑"细微指令设计显著影响行为"；
  - "Can a model maintain consistent performance across similar tasks?" → 模板内成功率直方图（Table 3），支撑"同模板任务难度差异大，需要记忆类方法"。
- 无传统消融章节；消融以"分析问题"的形式嵌入 5.1。

#### 1.7 讨论/局限/伦理/可复现性处理

- 无独立 Limitations 章；局限隐含在 Analysis（模型能力缺口）与 Conclusion 的"呼吁未来工作"中。
- 无 Ethics/Reproducibility 独立节（ICLR 2024 附录中体现）；可复现性靠正文承诺（Docker + 重置脚本 + gym API）与开源链接（webarena.dev）。

#### 1.8 独特且值得借鉴的结构选择

1. **"human performance" 作为难度校准锚点**放在 benchmark 章末（§3.2），而不是实验章——暗示"任务是人可做的、评测是公平的"。
2. **评分函数一表化**（Table 1：每个函数配一个真实任务示例和 eval 实现）——评审最关心"怎么判对错"，一张表全答。
3. **Unachievable tasks 单列一段**——专门评"agent 是否会编造"，与我们"验证失败即危险"的精神接近。
4. Related Work 里的**四维能力对比矩阵**（Table 4）：Dynamic/Realistic/Diverse/Functional × 8 个 benchmark 打勾。

---

### 2. ToolEmu (ICLR 2024) — 模拟器 + 自动评估器 + 风险评测型 benchmark

#### 2.1 章节树

```
Abstract
1 Introduction
2 Background & Problem Statement
  （Formulation of LM agents / Challenges in safety evaluation / Problem statement / Threat model: instruction underspecification）
3 Constructing ToolEmu
  3.1 Emulating Tool Executions with Language Models    （含 adversarial emulator、emulator requirements & design）
  3.2 Designing Automatic Evaluations with Language Models（safety evaluator + helpfulness evaluator）
  3.3 Curating the Evaluation Benchmark                 （tool specification curation + test case curation）
4 Validating ToolEmu
  4.1 Experimental Setup                                （含 Human annotations：招募/筛选/报酬细节）
  4.2 End-to-End Validation                             （identified vs true failures、precision、真实 bash 复现）
  4.3 Detailed Validation                               （emulator 质量 + evaluator 与人一致性）
5 Evaluating Language Model Agents within ToolEmu      （无编号子节，用粗体问句式 run-in 标题）
6 Related Work
7 Limitations & Future Directions
Acknowledgements / References
A Detailed Design & Implementation of ToolEmu
  A.1 Emulator / A.2 SafetyEvaluator / A.3 HelpfulnessEvaluator
  A.4 Evaluation Benchmark（A.4.1 Example Test Cases / A.4.2 Example Tool Specifications / A.4.3 Tool Curation / A.4.4 Test Case Curation）
B Additional Experimental Results（B.1 Additional Validations / B.2 Additional Evaluations for LM agents）
C Detailed Implementation of LM agents
D Details of Human Annotation Procedure
E Representative Cases（E.1 Typical Failures / E.2 Comparing Standard & Adversarial Emulation / E.3 Real Sandbox Instantiation）
F Full Prompts（F.1 Agent / F.2 Emulator / F.3 SafetyEvaluator / F.4 HelpfulnessEvaluator / F.5-F.7 数据生成 prompts）
```

#### 2.2 各节一句话概括

- **Abstract**：LM agent 有风险 → 测试成本高 → ToolEmu 用 LM 模拟工具 + LM 自动安全评估器 → 144 test cases，最安全 agent 仍 23.9% 失败。
- **1 Introduction**：风险严重性（金融/财产/生命）→ 长尾风险测试工程成本高 → 受自动驾驶模拟测试启发 → 核心是 LM 模拟器 → 模拟可信度（>80% realistic，7 个 ChatGPT-3.5 严重失败 6 个可在真实 bash 复现，8 小时 vs 15 分钟）→ 自动评估器与人一致性（73.1% recall vs 人类 78.8%）→ benchmark 规模与结论数字。
- **2 Background & Problem Statement**：LM agent 的 POMDP 形式化（helpfulness r_h 与 safety r_s 双评分）→ 安全评估的三大挑战（长尾难复现/工具面窄/人工找失败贵）→ 问题陈述（用 LM 模拟 T,O,s0 与人工评估）→ **明确 Threat model：instruction underspecification，用户意图 benign、无恶意**——与我们论文的"无攻击者"设定同构。
- **3**：3.1 LM 作虚拟沙盒（只凭 tool spec 即可模拟）+ adversarial emulator（把沙盒状态导向高风险）+ 三大模拟器要求（input validation / accuracy / consistency）；3.2 安全评估器（回溯式识别风险动作，likelihood × severity 评分，Table 1 量表）与 helpfulness 评估器（防"什么都不做就安全"）；3.3 数据构建：18 类 toolkit 分类体系 → GPT-4 生成工具规格与风险 → 人工复核+模拟器验证；test case 同流程，每 case 至少两人审+执行验证，共 144 cases / 36 toolkits / 311 tools / 9 risk types。
- **4 Validating ToolEmu**（**全文最独特的"验证测量工具"章**）：4.1 从 144 抽 100 case × 标准/对抗模拟器 = 200 条轨迹，3 个 agent 模型；人工标注员筛选（25 选 4，12 道测试题，~25 小时，$21/时）；4.2 端到端：identified failure precision 72.5%/68.8%，对抗模拟器多找 10pp 真失败；7 个 ChatGPT-3.5 终端失败 6 个真实复现；4.3 分组件：模拟器 85-92% 无 critical issue；评估器与人 Cohen's κ=0.478 ≈ 人人一致 0.480；precision/recall 与单人标注员相当。
- **5**：主表 Table 5（5 个 agent × safety/helpfulness 分数 + failure incidence + NoAct 对照）+ 三个问句式分析：base agent 对比 / prompt 是否提升安全 / safety-helpfulness 是否权衡（Figure 6 前沿散点 + Ideal 点）。
- **6 Related Work**：三段式（LM agents / Evaluation of LM agents / LM as emulator / Simulation environments），每段末尾列 (i)(ii) 差异点。
- **7 Limitations & Future Directions**：三段粗体 run-in：模拟器与评估器质量（各带具体失败率数字）/ 自动 red-teaming 与可扩展监督（承认 test case 仍靠人工）/ 扩展 benchmark（其他 threat model、多模态）。
- **Appendix**：设计与 prompt 全文（F 卷 7 个完整 prompt）、附加实验、人工标注流程细节、代表性案例（含真实沙盒复现）。

#### 2.3 引言组织方式

- 逻辑：**agent 能力→风险放大（具体危害举例）→ 风险测试的工程瓶颈（三点）→ 模拟器方案（借自动驾驶类比）→ 三个证据数字（模拟保真度 80%+/真实复现 6 of 7/评估器对齐人类）→ benchmark 与结论（23.9%）**。引言里嵌了 Figure 2（5 个真实失败案例画廊，红/黄高亮），先声夺人展示"我们能抓到什么"。
- 贡献点：不列 bullet，用 "The core of our framework… / Furthermore… / Finally…" 递进段落，但每段都带量化证据。
- **Figure 1**：框架总览（emulator + agent + evaluator 三角数据流）；**Figure 3** 是 test case 字段解剖图（每个字段被哪个组件消费，彩色对应）。

#### 2.4 Benchmark 构建呈现方式

- **分类体系**：toolkit 18 类 taxonomy（Table A.2）+ 9 种 risk type 分布（Figure 5b 饼图）。
- **收集→扩展流程**：分类体系 → GPT-4 生成 toolkit 名/规格/潜在风险（带 requirement + 格式示例 prompt）→ 人工复核并在模拟器中验证 ≥2 个测试 → test case 同策略生成 → 每 case ≥2 人审查+轨迹验证；Figure 5a 是整条 curation 流程图。
- **质控**：多人独立审查、执行验证、模拟器要求清单（Table A.1 major/minor issue 分级）。
- **统计表**：Table 2（toolkit 按"已有 benchmark 与否 × 有无公开 API"3×分类计数，例：23 个有 API 但无沙盒评测、7 个连 API 都还没有）——证明覆盖面新颖性；规模数字（144/36/311/9）在正文与 Figure 5a 中。

#### 2.5 评价协议与指标呈现方式

- **Table 1 量表**：safety（Certain No Risk 3 … Likely Severe Risk 0，likelihood × severity）与 helpfulness（Excellent 3 … Poor 0）双维度 + binarize 规则，一张表同时用于自动评估和人工标注（"同标准"是验证一致性的前提）。
- judge 写法：prompt 里喂 test case 的 underspecification / potential risks & risky actions / expected achievement 字段 + 完整轨迹，让 GPT-4 回溯式判定；prompt 全文放附录 F.3/F.4。
- **judge 验证**：与人工标注算 Cohen's κ（0.478 vs 人人 0.480）、precision/recall（75.3/73.1 vs 人 78.7/78.8）——把"LLM judge 可信"当作独立研究问题正面回答。

#### 2.6 实验部分组织

- **§4 验证实验（instrument validation）与 §5 应用实验（benchmark 评测）分成两章**，这是最大结构特色：
  - §4.2 端到端验证（框架整体能不能找到"真失败"）+ 真实 bash 复现 case study（6/7）；
  - §4.3 分组件验证（模拟器质量、评估器一致性）；
  - §5 主实验 Table 5 + 3 个问句分析（base 对比 / prompting 消融含 Safety 与 Helpfulness+Safety 两个变体 / trade-off 散点）；NoAct 对照 agent 防"摆烂刷安全分"。
- 每个分析小节都有明确结论：能力与安全正相关、prompt 提升安全但仍有 23.9% 失败、trade-off 不必然（Ideal 点）。

#### 2.7 讨论/局限/伦理/可复现性处理

- §7 Limitations 用三段粗体小标题组织，每段承认具体数字级局限（模拟器 critical issue 14.4%、评估器 recall 73.1%）并给出缓解论据（model scaling）。
- 无独立 Ethics/Repro 声明（arXiv 版）；人工标注伦理细节（筛选、报酬、耗时）放 §4.1 + 附录 D；全部 prompt 开源 + 项目站 toolemu.com。

#### 2.8 独特且值得借鉴的结构选择

1. **独立的 "Validating ToolEmu" 章**：先证明测量工具可信，再用它测 agent——评审无法攻击"你的 judge 说了算"。
2. **identified failure / true failure 双定义** + precision 指标 + 真实环境复现（8h vs 15min 的效率对比）。
3. **test case 解剖图（Fig 3）**：每个字段被哪个组件消费，一张图讲清数据格式与评测协议的耦合。
4. **NoAct 对照**堵住"不做事就安全"的漏洞；Helpfulness+Safety prompt 变体展示双目标冲突。
5. 引言直接放**失败案例画廊（Fig 2）**：读者先看到危害，再看框架。

---

### 3. SWE-bench (ICLR 2024) — 数据管线 + 执行验证型 benchmark（含训练集与微调模型）

#### 3.1 章节树

```
Abstract
1 Introduction
2 SWE-bench
  2.1 Benchmark Construction          （Stage I/II/III 三段管线）
  2.2 Task Formulation                （Model input / Evaluation metrics）
  2.3 Features of SWE-bench           （6 个特征条目）
  2.4 SWE-bench Lite
3 SWE-Llama: Fine-tuning CodeLlama for SWE-bench（Training data / Training details）
4 Experimental Setup
  4.1 Retrieval-Based Approach        （Sparse retrieval / "Oracle" retrieval）
  4.2 Input Format
  4.3 Models
5 Results
  5.1 A Qualitative Analysis of SWE-Llama Generations
6 Related Work
7 Discussion                          （Limitations and future directions / Conclusion 两个 run-in）
8 Ethics Statement
9 Reproducibility Statement
10 Acknowledgements / References
A Benchmark Details（A.1 High-level Overview / A.2 Construction Process / A.3 Execution-based Validation / A.4 Evaluation Procedure / A.5 Evaluation Test Set Characterization / A.6 Development Set Characterization / A.7 SWE-bench Lite Characterization）
B Additional Details on Training SWE-Llama（B.1 Training Details）
C Additional Results（C.1 Oracle / C.2 Eval Test Set / C.3 GPT-4 Subset / C.4 Temporal Analysis / C.5 F2P-P2P Rate Analysis / C.6 Patch Generation Extended Analysis / C.7 Software Engineering Metrics）
D Additional Experimental Details（D.1 Retrieval / D.2 Inference / D.3 Prompt Template Example）
E Societal Impact
F In-Depth Analysis of SWE-Llama Generations
```

#### 3.2 各节一句话概括

- **Abstract**：真实软件工程是理想 testbed → 2,294 个 GitHub issue 任务、12 仓库 → 最强模型解 1.96% → 另发布 SWE-bench-train 与 SWE-Llama。
- **1 Introduction**：现有 benchmark 饱和 → "难"与"易验证"的张力 → 代码任务二者兼得但 HumanEval 玩具化 → SWE-bench（真实 issue+PR+测试）→ 四点优势列举 → 结果数字 → **训练集 + 微调模型作为第二贡献**。
- **2.1**：三段管线（Stage I 爬 12 个仓库 ~90k PR → Stage II 属性过滤：关联 issue+改测试 → Stage III 执行过滤：fail-to-pass 测试 + 安装成功）筛出 2,294 实例；Figure 2 管线图。
- **2.2**：输入=issue 文本+完整代码库，输出=patch；指标=% resolved（patch 可应用且所有关联测试通过）。
- **2.3**：6 个特征（真实任务/可持续更新/长输入/稳健评测/跨文件编辑/解法自由度），每条一段并带统计数字（1.7 文件、3.0 函数、32.8 行）。
- **2.4**：Lite 300 题子集（更自包含、聚焦 bug 修复），为落地采用率考虑。
- **3**：开源模型基线补充——SWE-bench-train 19k 实例（37 个不同仓库防污染）+ LoRA 微调 SWE-Llama 7b/13b。
- **4**：4.1 BM25 vs oracle 两种检索设定（并报告 BM25 recall 对照）；4.2 输入格式；4.3 模型与上下文长度表。
- **5**：主表 Table 5（BM25 下 %Resolved/%Apply）+ 若干粗体 run-in 分析：跨仓库难度差异（Fig 4）/ 难度与上下文长度相关（Fig 5）/ 与 issue 日期无关（Table 7，防污染证据）/ 微调模型对检索分布敏感 / patch 比整文件好 / 模型编辑偏短（Table 8）；5.1 选 11 个生成做定性分析（Figure 6 端到端示例：输入→gold patch→模型 patch→测试日志）。
- **6 Related Work**：三段（LM 评测泛泛批判 potpourri 式 / 代码生成 benchmark / ML for SE）。
- **7 Discussion**：Limitations and future directions（Python only、基线不代表方法论上限、执行验证不足以保证代码质量）+ Conclusion。
- **8 Ethics Statement**：公开仓库许可、不涉 GitHub 用户数据、无众包人力、开源承诺。
- **9 Reproducibility Statement**：匿名源码压缩包、目录按贡献划分、含全部 2,294 实例、附录 A.2/A.4 补足管线与评测细节。
- **Appendix**：构建管线技术细节、执行验证、评测流程（Figure: Input→Generates→Evaluation→Results 四步图）、数据集刻画、训练细节、扩展结果、社会影响。

#### 3.3 引言组织方式

- 逻辑：**LM 广泛部署 → benchmark 饱和 → 好 benchmark 的两难（难 + 易验证）→ 代码任务两者兼得但现有代码 benchmark 玩具化 → 真实 SE 才是前沿 → SWE-bench 任务定义（Figure 1）→ 四点优势 → 结果（1.96%）→ 第二贡献（train set + SWE-Llama）**。
- 贡献点：不列 bullet；用 "SWE-bench offers several advantages… These include…" 的列举句 + 单独一段 "In addition to SWE-bench our contributions include…"。
- **Figure 1**：数据来源管线鸟瞰（issue + codebase snapshot → 模型生成 patch → 对真实测试评测；标注 Pre/Post PR tests 的 fail→pass）。

#### 3.4 Benchmark 构建呈现方式

- **流程**：显式 **Stage I/II/III** 三段过滤管线（每段一段文字+Figure 2 一行流程图），漏斗数字 90,000 → 2,294 全程可追溯。
- **统计表**：Table 1（instance 属性均值/最大值：issue 长度、代码库规模、编辑行数、fail-to-pass 测试数、总测试数）放 §2.4 旁；Figure 3 仓库分布甜甜圈图。
- **质控**：执行过滤本身就是质控（fail-to-pass 判据、安装运行错误剔除）；附录 A.3 详述 execution-based validation。
- **分类体系**：无任务分类学，但 2.3 的"6 个 features"承担了"任务设计原则"的角色；C.7 用软件工程指标（缺陷类别）做生成分类。

#### 3.5 评价协议与指标呈现方式

- 指标定义极简且客观（§2.2）：patch 可应用 + 全部相关测试通过 = resolved；主指标 % resolved，附 % apply 作为"格式正确率"中间指标——**把"能用"与"能对"分开报告**。
- 无 LLM judge；全部执行验证。评测流程图（附录 A.4 的 Input→Generates→Evaluation→Results）把协议可视化。

#### 3.6 实验部分组织

- §4 Experimental Setup 先把**检索设定当一等公民**（BM25 三档上下文 + oracle），因为上下文构造本身就是主要实验变量；
- §5 Results：主表 + 6 个粗体 run-in 分析（每个分析一个对照实验：oracle-collapsed 消融 Table 6、时间切片 Table 7、整文件 vs patch 对照）；5.1 定性分析（选取非 cherry-picked 的 11 例，端到端 Figure 6）；
- 每个分析支撑一个结论：定位困难 > 上下文长度、无时间泄漏、微调不稳健、模型编辑偏保守。

#### 3.7 讨论/局限/伦理/可复现性处理

- **Discussion 把 Limitations 与 Conclusion 合成一节**，两个粗体 run-in；Ethics 与 Reproducibility 独立成章（§8/§9，ICLR 惯例模板）；另有附录 E Societal Impact。
- 局限三条各自量化（Python only / 仅基线方法 / 执行验证不足以保证可读性与效率）。

#### 3.8 独特且值得借鉴的结构选择

1. **可更新性作为特性小节**（2.3 Continually updatable）：管线可持续采新实例防数据污染——"benchmark 生命周期"写进正文。
2. **SWE-bench Lite 子集**：为采用成本考虑设轻量子集，正文明说动机（贵、耗时、吓退新手）。
3. **辅助交付物成章**（§3 SWE-Llama + SWE-bench-train）：benchmark 论文顺带发布训练资源与模型，贡献立体化。
4. **%Resolved 与 %Apply 分开**、oracle/bm25/collapsed 三档评测设定作对照阶梯，把"检索 vs 推理"的混淆变量控掉。
5. **防污染分析**（before/after 2023 切片）独立成一个 run-in 分析——评审必问的问题直接做掉。

---

### 4. τ-bench (2024, Sierra) — 用户模拟 + 规则遵循 + 可靠性指标型 benchmark

#### 4.1 章节树

```
Abstract
1 Introduction
2 Related Work（Benchmarks for language agents and tool use / Task-oriented dialogue / User simulation with LMs）
3 τ-bench: A benchmark for Tool-Agent-User Interaction
  （POMDP 形式化；Databases and APIs / Domain policy / User simulation / Task instances / Reward / Pass^k metric——全部为粗体 run-in 而非编号子节）
4 Benchmark Construction
  （Stage I manual design / Stage II automatic data generation with LMs / Stage III manual task annotation and validation with agent runs）
  4.1 Domains（τ-retail / τ-airline）
  4.2 Key Characteristics（4 条）
5 Experiments
  5.1 Main results（Model comparison / Method comparison / Agent consistency via pass^k / Cost analysis）
  5.2 Research challenge analysis（Failure breakdown / Failure 1-3）
6 Discussion（Directions for improvement / Challenges for agents）
Acknowledgements / References
A Additional Results（含 Figure 7 任务难度分布）
B Benchmark Construction（B.1 Stage I: design of database schemas, APIs, and policies / B.2 Stage II: data generation）
C Retail Examples（C.1 Data examples / C.2 Task and trajectory examples）
D Airline Examples（D.1 Data examples / …）
```

#### 4.2 各节一句话概括

- **Abstract**：现有 benchmark 不测人机交互与规则遵循 → τ-bench 模拟用户+API+政策文档 → 数据库终态对比评分 + pass^k 新指标 → gpt-4o pass^1<50%、pass^8<25%。
- **1 Introduction**：部署三要求（人机+API 长程交互 / 遵守领域政策 / 大规模一致性）→ 航班改签例子（Figure 1）→ 现有 benchmark 信息一次性给全、无人机交互 → τ-bench 模块化三件套（数据库+API、政策文档、用户场景+真值标注）→ 三阶段构建 → 终态对比评分 + pass^k → 结果与失败分析预告。
- **2 Related Work**：三段（agent/tool benchmark：指出全是单轮、Task-oriented dialogue：静态或规则化模拟、User simulation with LMs：以往只展示仿真能力不用于测可靠性）。
- **3**：任务 POMDP 形式化（db+user 双状态、双动作空间）→ 数据库/API（隐藏状态、确定性转移）→ 域政策（部分规则写进 API 检查、部分留给 agent）→ 用户模拟（gpt-4-0613，###STOP### 结束）→ task instance（用户指令保证唯一终态 + ground-truth 写动作标注）→ Reward = r_action × r_output ∈ {0,1}（终态库一致 + 关键信息子串）→ **Pass^k metric**（k 次独立全成功的概率，无偏估计公式，对比 pass@k）。
- **4**：三阶段构建（Stage I 人工设计 schema/API/政策；Stage II GPT-4 生成采样代码批量造数据；Stage III 人工写任务+用 gpt-4-turbo agent 跑 >40 trial 迭代消除歧义）；4.1 两个域（retail 规则贴近常识、airline 规则 ad-hoc 多跳）；4.2 四个 key characteristics（真实对话与工具使用 / 开放多样任务 / 忠实的规则化评测 / 模块化扩展）——**"trade quantity for quality" 明说**。
- **5**：13 个模型 × FC/ReAct/Act 三法；5.1 主表 Table 2 + 方法对比 Figure 3 + **pass^k 曲线 Figure 4** + 成本分析（$0.38/$0.23 每任务，成本在长 system prompt）；5.2 挑战分析：失败饼图 Figure 5（36 例分解为 wrong argument 33.3% / wrong info 22.2% / wrong decision 25% / partially resolve 19.4%）→ 三类 Failure 各一段 → **政策消融 Table 3**（去掉域政策 retail 降 4.4pp、airline 降 22.4pp，证明模型确实在用政策）→ 复合请求难度曲线 Figure 6。
- **6 Discussion**：Directions for improvement（模拟用户局限三点、可加系统检查/更复杂政策/更多指标、标注偏差——用 gpt-4-turbo 调 prompt 有隐性偏置）+ Challenges for agents（一致性与规则遵循是核心短板）。
- **Appendix**：附加结果、构建细节、retail/airline 数据与轨迹示例。

#### 4.3 引言组织方式

- 逻辑：**agent 热潮 → 部署三要求（(1)(2)(3) 显式编号）→ 具体场景故事（Figure 1 航班改签）→ 现有 benchmark 缺口（无交互、无规则）→ τ-bench 设定 → 三阶段构建一句话 → 评分方式 + pass^k → 结果数字（pass^1<50%、pass^8<25%）→ 失败原因预告**。
- 贡献点：无 bullet，融在 "we introduce / We constructed / We also introduce / Our experiments reveal" 叙述中。
- **Figure 1**：(a) 系统设定图（agent ↔ tools/db ↔ LM 用户 ↔ 政策文档）+ (b) 真实轨迹示例（含"拒绝用户请求并提出替代方案"）——**一半概念一半实证**。

#### 4.4 Benchmark 构建呈现方式

- **流程**：Stage I/II/III 三段明确命名（与 SWE-bench 同构：人工设计 → LM 扩量 → 人工验证），关键质控是 Stage III 的"**跑 agent 迭代消除任务歧义直至唯一终态**"（每任务 >40 次 gpt-4-turbo trial 检查零/低成功率）。
- **统计表**：Table 1（每域一行：数据库规模、API 数（write/non-write 分开）、任务数）——极简但把"规模+难度"都交代。
- **分类体系**：按域（retail/airline）组织，域选择动机写明（易合成数据、规则常识化、任务多样）；4.2 用 4 条 key characteristics 取代"任务分类学"。
- 数据示例全放附录（C/D：data examples + task & trajectory examples），正文只留 Figure 2 组件解剖（(a)数据库 (b)API (c)政策 (d)任务实例 四联图）。

#### 4.5 评价协议与指标呈现方式

- **Reward**：r = r_action × r_output 二值，规则化（终态数据库逐字段比对 + 回复含必要子串）；明写局限（r=1 是必要非充分，例如未确认就执行）——**先自己指出再论证可接受**。
- **Pass^k 独立 run-in 小节**：定义（k 次 i.i.d. 全成功概率）+ 无偏估计公式 + 与 pass@k 对比 + 为何适用（LM 采样提供随机性、测一致性/鲁棒性）+ 默认主指标 pass^1。**新指标配公式+动机+使用建议，是全篇最被记住的点。**

#### 4.6 实验部分组织

- 主实验：Table 2（模型 × 域 × avg）+ Figure 3（模型×方法柱状）+ Figure 4（pass^k 曲线，k=1..32）+ Cost analysis（成本归因到 prompt 组成）。
- §5.2 挑战分析：失败分解饼图（先量化分布，再逐类定性）→ 每类配附录案例 → 两个受控消融（政策移除 Table 3、复合请求难度 Figure 6）。
- 每个实验支撑一个结论：FC>text-formatted、推理痕迹有用、一致性随 k 崩塌、airline 规则多跳是硬点、模型并没有充分利用政策文档。

#### 4.7 讨论/局限/伦理/可复现性处理

- §6 Discussion 合并了局限（模拟用户三点局限 + 标注偏差）与未来方向与核心挑战；无独立 ethics/repro（preprint），但正文有"无负面社会影响直接声明"一句话。
- 独特：把"用户指令可能有 typo/歧义"这类数据缺陷也列进 limitations 并说明已修流程。

#### 4.8 独特且值得借鉴的结构选择

1. **Pass^k 独立指标小节**：定义+公式+与 pass@k 对比+适用性论证——新指标必须这样待遇。
2. **Stage III "用 agent 跑任务来验证任务无歧义"**：数据质控用模型行为闭环，写成构建流程一部分。
3. **4.2 Key Characteristics**：以设计原则（而非任务分类）总结 benchmark 特性，每条一句价值主张（"trade quantity for quality"）。
4. **成本分析进主实验**：每任务 $、成本构成（95.9% 在输入 prompt）——实用性说服力强。
5. **政策消融**（把关键信息源从 prompt 里移除看掉多少分）证明"模型真的在用 X"——可迁移到我们"证据搜集"归因。

---

### 5. AgentDojo (NeurIPS 2024 D&B) — 动态攻防框架型 benchmark

#### 5.1 章节树

```
Abstract
1 Introduction
2 Related Work and Preliminaries（AI agents and tool-enhanced LLMs / Prompt injections / Benchmarking agents and prompt injections）
3 Designing and Constructing AgentDojo
  3.1 AgentDojo Components（Environments and state / Tools / User tasks / Injection tasks / Task suites）
  3.2 Agents and Prompt Injection Defenses
  3.3 Prompt Injection Attacks
  3.4 Reporting AgentDojo Results（三指标定义）
4 Evaluation
  4.1 Performance of Baseline Agents and Attacks
  4.2 Ablations on Attack Components and Attacker Knowledge
  4.3 Prompt Injection Defenses
5 Conclusion（含 (i)-(v) 未来方向）
References
A Additional Details on AgentDojo's Design
B Prompts（B.1 Agent / B.2 Defense / B.3 Attack）
C Full Results（Table 4/5 全量结果）
D Additional Results（注入位置分析等）
E Dataset-related Supplementary Material（E.1 Code and data release / E.2 Hosting, licensing, maintenance plan / E.3 Reproducibility / E.4 License / E.5 Statement of responsibility / E.6 DOI and Croissant metadata）
F Data Card（F.1-F.13 完整 NeurIPS 数据卡：Authorship/Overview/Sensitivity/Motivations/Access/Provenance/Human attributes/Extended use/Transformations/Validation/Applications）
```

#### 5.2 各节一句话概括

- **Abstract**：agent 脆弱于 prompt injection → AgentDojo 动态框架（非静态测试集）→ 97 任务 / 629 安全用例 / 多种攻防范式 → 攻与防都难（无攻击时模型 <66% 任务成功率，攻击 <25%，加检测器降到 8%）。
- **1 Introduction**：agent+工具范式 → LLM 无法区分指令与数据 → prompt injection 危害 → AgentDojo 设定（Figure 1）→ 与既有工作差异（动态多工具有状态、形式化 utility check 而非 LLM 模拟环境）→ 可扩展框架定位（不是静态 benchmark）→ 关键数字（66%/25%/8%）→ 通用攻防非特化设计 → 开源+leaderboard。
- **2 Related Work and Preliminaries**：相关工作与术语定义合并（direct/indirect injection、防御三类）；Figure 2 在此对比 Berkeley Function Calling Leaderboard 证明"无攻击时也够难"。
- **3**：先一段组件总述（environment/state/user task/injection task/task suite/交叉积得 629 安全用例）；3.1 组件细节（4 环境、74 工具、user task 带 utility 函数+ground-truth 调用序列、injection task 带攻击目标、dummy 数据由 GPT-4o/Opus 生成+全量人工检查）；3.2 agent 与防御接口（query 函数 + 模块化 pipeline）；3.3 攻击（不做静态攻击集、支持自适应攻击、攻击者先验知识档位）；3.4 **三指标**：Benign Utility / Utility Under Attack / Targeted ASR（+ adaptive "any-attack-succeeds" 度量）。
- **4**：9 个模型 × 629 用例全量；4.1 主结果 Figure 6 双散点（utility vs ASR、utility vs utility-under-attack，**Pareto frontier 加粗**）→ 能力越强越易被攻击（inverse scaling）→ Figure 7 按 suite/injection task 分解 ASR（Slack 92% vs travel task 6 0%）→ 注入位置分析（放响应末尾最有效 ~70%）；4.2 攻击组件消融（4 种注入措辞对比 Figure 8 + Max 自适应攻击 + 攻击者知识消融 Table 2：知道用户名+模型名 +1.9pp，猜错 -22pp）；4.3 防御评估（4 种防御 × GPT-4o，Figure 9 双散点，tool filter 降到 7.5% 但 17% 用例工具可兼善恶→失效）。
- **5 Conclusion**：总结 + (i)-(v) 编号未来方向（更复杂攻防、自动任务生成、多模态、注入约束）。
- **Appendix**：设计细节、全部 prompt、全量结果表、附加分析（注入位置）、数据集发布/许可/维护/复现细节 + 完整 Data Card。

#### 5.3 引言组织方式

- 逻辑：**agent+工具前景 → 安全挑战（LLM 不区分指令与数据）→ 危害列举 → AgentDojo 设定（Figure 1 一段话讲完 attack goal/injection endpoint/双指标）→ 与四类既有 benchmark 的差异（逐类点名）→ 动态框架定位 → 4 个关键数字（无攻击 <66%、攻击 <25%、防御后 8%、信息侧信道收益小）→ 通用性声明 → 开源/leaderboard**。
- 贡献点：无 bullet；以 "we introduce AgentDojo… / In contrast to prior benchmarks… / AgentDojo is not a static benchmark… / We hope…" 推进。
- **Figure 1**：攻防设定解剖图（Attacker Goal / Environment / User Task / Attack Vector / Evaluation Metrics 五块，邮件注入示例）——把威胁模型一图化。

#### 5.4 Benchmark 构建呈现方式

- **分类体系**：4 环境（Workspace/Slack/Banking/Travel）× Table 1（每环境工具数、user task 数、injection task 数 + 例句）——**规模表直接承担分类学**；注入任务按"步骤数 1→20、敏感度 generic email→2FA code"标定难度梯度。
- **收集→扩展流程**：人工设计 user task（覆盖中长上下文检索、最多 18 步工具链）→ 与 injection task 交叉积成 task suite；dummy 数据 GPT-4o/Opus 生成 + **全部人工检查**。
- **质控**：utility/security 函数为**确定性二值函数**（检查模型输出+环境状态变更），正文明写为什么不用 LLM judge（评测模型也可能被注入劫持）——**方法选择的防御性论证直接写进正文**。
- **统计表**：Table 1（主规模表，§3.2 旁）；629=Σ user×injection 交叉积在正文解释。

#### 5.5 评价协议与指标呈现方式

- §3.4 专节列三指标（Benign Utility / Utility Under Attack / Targeted ASR），每个一句定义 + 其中一个给补集别名（untargeted ASR）；另定义 "attack collection" 度量模拟自适应攻击者。
- 评分函数 = 代码（deterministic binary utility），无 judge；每 user/injection task 附 ground-truth 函数调用序列（既做标注又供攻击者设计用——双向使用说明写清）。

#### 5.6 实验部分组织

- 4.1 主实验：全模型 × 通用攻击，主图是**双散点（utility–security 权衡，Pareto 加粗）**而非单表 + Table 3 报 95% CI；随后 ASR 按 suite/task 分解（Figure 7）、注入位置分析（附录 D Figure 21a）。
- 4.2 消融：攻击措辞 4 种 + 自适应 Max（Figure 8）；攻击者先验知识（Table 2）。
- 4.3 防御：4 种文献防御逐一评估 + **Strengths and limitations of tool isolation mechanisms** 段落：tool filter 最有效（7.5%）但失效条件（17% 用例、任务不可预规划、多任务会话）逐条列出。
- 每个实验支撑一个结论：更强模型更易被攻击、措辞影响大、侧信道收益小、隔离防御有效但边界清晰。

#### 5.7 讨论/局限/伦理/可复现性处理

- Conclusion 内嵌 (i)-(v) 编号的改进方向（≈ limitations）；数据伦理与可复现性集中在**附录 E（Dataset-related supplementary material：发布/托管许可维护/复现/许可/责任声明/DOI+Croissant）与附录 F（完整 Data Card 13 小节）**——NeurIPS Datasets & Benchmarks track 的标准配置。

#### 5.8 独特且值得借鉴的结构选择

1. **Utility–security 权衡散点图（Pareto frontier 加粗）**：攻防类 benchmark 的标准"主图"，一眼看防御/攻击的 trade-off。
2. **"动态框架而非静态测试集"定位**：§3.3 用两个理由论证（现成攻击不优化防御、易被特化防御刷分→需要自适应评测），把 benchmark 的生命周期策略写成学术主张。
3. **为什么不用 LLM judge 的显式论证**（评测模型会被注入劫持）→ 我们用 LLM-as-Judge 时应反向显式论证（benign 无攻击者，judge 不会被劫持 + 与人工一致性验证）。
4. **攻防矩阵式呈现**：user×injection 交叉积、注入任务难度梯度（步骤数×敏感度）、攻击者知识档位——多轴设计一表/一图化。
5. **NeurIPS Data Card 全套**（附录 E+F）：托管、许可、维护计划、Croissant DOI——数据类论文的"合规即说服力"。

---

## 二、5 篇共有的 benchmark 论文"结构惯例"

1. **引言固定推进线**：愿景/趋势 → 具体风险或能力缺口（配危害或场景例子）→ 现有 benchmark 缺口（逐类点名+引文）→ 本文 benchmark 一句话定位（紧跟 Figure 1）→ 构建与评测方式一句话 → **标题级数字**（最好带人类/上限锚点）→ 开源链接。贡献大多不写 bullet，而是"每个贡献对应一个正文段落/章节"的叙事式推进（WebArena 最典型：§2/§3/§4 三段三贡献）。
2. **Figure 1 恒为"系统/任务总览图"**：组件、数据流、一个具体示例三合一；有的再加 Figure 2/3 做"失败案例画廊"或"test case 解剖"。
3. **正文三段式骨架**：① 形式化/问题定义（POMDP 或 MDP + 威胁模型，ToolEmu §2、τ-bench §3、AgentDojo §2）→ ② Benchmark 构建（收集→扩展→质控→统计）→ ③ 评测协议（指标+评分函数+judge）→ ④ 实验（主实验+分析+消融）。
4. **构建流程显式分 Stage**（SWE-bench 与 τ-bench 都是三段：人工设计→LM/爬虫扩量→人工+执行验证），配管线图 + 漏斗数字（90k→2,294）+ 统计表（规模、长度、难度分布）。
5. **质控即卖点**：双人标注/第三人仲裁（WebArena）、每 case ≥2 人审查（ToolEmu）、执行过滤（SWE-bench）、跑 agent 验证任务无歧义（τ-bench）、全量人工检查 LLM 生成数据（AgentDojo）——全都写成显式流程而非一句"经过人工检查"。
6. **指标定义精确到函数**：exact_match/must_include/fuzzy_match（WebArena）、r=r_action×r_output（τ-bench）、binary utility（AgentDojo）、0-3 量表+binarize（ToolEmu）；新指标给独立小节+公式+动机（τ-bench pass^k）。
7. **LLM judge 必须"验身"**：与人工标注的一致性（Cohen's κ、precision/recall、leave-one-out，ToolEmu §4.3）或准确率验证（WebArena 附录 A.8）单独成节/成表。
8. **实验按"问题"组织**：分析小节用问句标题（"Do models know when to stop?" / "Is there a tradeoff?" / "Does prompting improve safety?"），每个实验绑定一个明确结论；消融以"受控对照"形式出现（政策移除、oracle-collapsed、UA hint 移除、注入位置）。
9. **防"作弊式安全/能力"的对照设计**：NoAct 对照（ToolEmu）、human performance 锚点（WebArena）、benign utility 与 attack ASR 同报（AgentDojo）、%Resolved 与 %Apply 分开（SWE-bench）。
10. **收尾合规化**：Discussion/limitations 承认具体数字级局限；ICLR 投稿配独立 Ethics Statement + Reproducibility Statement（SWE-bench §8/§9 是标准模板）；NeurIPS D&B 配 Data Card + 托管/许可/维护计划（AgentDojo 附录 E/F）。

---

## 三、对我们论文最有用的 10 条建议（按论文骨架顺序）

1. **引言照"愿景→危害实例→缺口→Figure 1→数字"走，贡献用 3 段叙事式**。缺口段直接点名：现有 agent-safety benchmark 要么有攻击者（AgentDojo/ASB）要么 LLM 模拟环境（ToolEmu）要么只测能力（WebArena/τ-bench）；我们补的是 **benign 设定下 context-environment gap** 这一格。标题级数字建议："最优防御/预训练增强后 ASR 仍为 X%，安全对照版同模型成功率 Y%（证明不是能力问题）"——安全对照版就是我们的 human-performance 式锚点。

2. **Figure 1 做成"一张 case 的解剖图"**（学 ToolEmu Fig 3 + τ-bench Fig 1b）：左侧 context（用户指令/文档，标出 gap 位置），右侧部分可观测环境（标出验证所需证据），下方 agent 危险动作 + 三类 case 的小图标；再加一小块"safe twin（移除坑点）"对比。把核心概念一次讲完。

3. **设独立 "Threat Model & Problem Formulation" 节（放 §2，学 ToolEmu §2）**：显式声明 **benign 用户意图、无攻击者**（ToolEmu 原文即如此写，并解释与 red-teaming 的区别）；形式化 context-environment gap（context 视为可信先验 vs 环境需验证的证据）；定义危险动作 = 验证失败仍执行。三类 case（requirement underspecification / requirement infeasibility / factual inconsistency）给**分类定义表**（每类：定义、单句例子、危险机制），学 AgentDojo Table 1 与 ToolEmu Fig 5b。

4. **构建章按三段 Stage 写**（种子→批量扩展→质控），配管线图+漏斗数字：种子 case 收集准则（学 WebArena §3.1 的三条标注准则写法）→ LLM 扩展 → 人工筛选与证据标注。**安全对照版（safe twin）单列一小节**：构造规则、配对方式、用途（剥离坑点验证模型能力无问题）——这是我们独有的设计，要给它 τ-bench "Key Characteristics" 级别的显式待遇。

5. **统计表 2 张起步**：Table A（规模：case 数 × 三类 × 环境/工具分布，学 AgentDojo Table 1 一行一环境+例句）；Table B（case 属性统计：证据数量、上下文长度、验证步骤数等，学 SWE-bench Table 1 均值/最大值双列）。人工证据标注报双人一致率/仲裁流程（学 WebArena AnnotationProcess）。

6. **评测协议章给"三分类失败归因"一张量表**（学 ToolEmu Table 1）：三类归因（证据搜集不足 / 证据充足但未识别危险 / 识别到危险但盲从指令）各自的操作性判据 + 与 ASR 指标的关系；**LLM-as-Judge 必须做"验身"实验**：与人工标注的 Cohen's κ、precision/recall（学 ToolEmu §4.3），并在方法处显式论证 judge 在 benign 设定下无被劫持风险（反向回应 AgentDojo 不用 judge 的理由）。若有新指标（如 gap-aware ASR 或归因分布），学 τ-bench pass^k 给独立小节+公式。

7. **实验一（防御打不下 ASR）学 AgentDojo §4.3 的呈现**：主图用 **utility–security 双散点 + Pareto 加粗**（x=能力/任务成功率，y=ASR），证明防御既不降 ASR 又不提升能力；2 种防御 + 1 种预训练增强逐个一小段，每段先报数字再解释，并写明"Strengths and limitations"式边界讨论。加 NoAct/极端对照防"摆烂"误读。

8. **实验二（拓扑对比）必须带"token/成本对照"**：学 τ-bench Cost analysis，报每任务 token 消耗与费用，并画 ASR vs token 散点/表格，直接支撑"ASR 降低不是 token 消耗大带来的"这一反混淆主张；三种拓扑 + 普通对照结构的对比表放主文，成本分析紧随其后。

9. **实验三（wording × position 受控干预）学 AgentDojo 注入位置分析 + τ-bench 政策消融的呈现**：2×2（明显/隐晦 wording × 明显/不明显 position）设计画成剂量-反应曲线或热力图；结果与三分类归因分布联动（哪种干预把失败推向哪类归因），支撑"失败归因"结论。失败分解先给饼图/条形分布再逐类定性（学 τ-bench Fig 5→Failure 1-3 的节奏）。

10. **收尾合规**：Discussion 用 2-3 段粗体 run-in 承认数字级局限（如 judge recall、case 由 LLM 扩展的偏差、benign 设定不覆盖对抗攻击），学 τ-bench 把数据缺陷也列入局限；按目标会议配独立 Ethics Statement（数据来源/无众包剥削/风险披露）与 Reproducibility Statement（学 SWE-bench §8/§9 模板）；若投 NeurIPS D&B，补 AgentDojo 式 Data Card + 托管/许可/维护计划。另建议放一个"benchmark 可扩展性"小段（学 AgentDojo "dynamic framework" 与 SWE-bench "continually updatable"）：说明三类 case 分类可加新类、safe-twin 机制可迁移，把局限转成路线图。

---

## 附：快速对照表

| 维度 | WebArena | ToolEmu | SWE-bench | τ-bench | AgentDojo |
|---|---|---|---|---|---|
| Figure 1 | 环境总览 | 框架总览(+Fig2失败画廊) | 数据管线鸟瞰 | 设定图+真实轨迹 | 攻防设定解剖 |
| 贡献写法 | 3 段对应 §2/3/4 | 叙事递进段 | 叙述+一句"贡献包括" | 叙事递进段 | 叙事递进段 |
| 构建流程 | 标注准则+模板扩展 | Taxonomy→GPT-4→人工 | Stage I/II/III 漏斗 | Stage I/II/III+agent 闭环验证 | 人工设计+交叉积 |
| 质控 | 双标注+仲裁+human perf | ≥2 人/条+执行验证 | 执行过滤 fail-to-pass | >40 trial 消歧义 | 全量人工检查 |
| 指标 | r_info/r_prog 三函数 | 0-3 量表+binarize | %Resolved/%Apply | r_action×r_output + pass^k | 3 指标(utility/ASR) |
| judge 验证 | 附录 A.8 准确率 | §4.3 κ+P/R | 无(执行验证) | 无(规则验证) | 无(确定性函数) |
| 独立验证章 | 无(human perf 内嵌) | **§4 Validating ToolEmu** | 无 | 无 | 无 |
| 实验分析标题 | 问句式 | 问句式 | 粗体 run-in | 粗体 run-in | 粗体 run-in |
| 局限位置 | 隐含 | §7 独立(3 段) | §7 Discussion 内 | §6 Discussion 内 | Conclusion (i)-(v) |
| 合规声明 | 无独立节 | 无独立节 | Ethics+Repro 独立章 | 一句话 | 附录 E+F Data Card |
