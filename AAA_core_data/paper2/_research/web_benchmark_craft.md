# 顶会高影响力 Benchmark 论文的写作结构惯例（调研报告）

> 目的：为即将撰写的 benchmark 论文（面向 benign 任务中 tool-using agent 安全、核心概念 context-environment gaps）设计写作骨架。
> 方法说明：本次调研中内置 web_search 端点故障，改用 web_fetch 直抓 arXiv / ar5iv 的 HTML 全文（含完整章节标题 TOC）与 arXiv/公开 API 元数据。章节树、Figure/贡献点信息均来自抓取的原文 HTML；个别正文尾部被截断处以 TOC 标题 + 正文已抓内容为准，未做臆测。引用链接见文末。

---

## 〇、样本概览

| # | 论文 | 发表处 | 一句话定位 |
|---|------|--------|-----------|
| 1 | GAIA: A Benchmark for General AI Assistants | ICLR 2024 | "人类易、AI 难"的现实助理问题，唯一短答案、自动评分（human 92% vs GPT-4+plugins 15%） |
| 2 | AgentBench: Evaluating LLMs as Agents | ICLR 2024 | 8 环境 × 3 类 grounding 的 LLM-as-Agent 多维基准 + 统一评测 toolkit，29 模型横评 |
| 3 | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | ICLR 2024（oral） | 真实 GitHub issue→PR→tests 构建 2294 题，patch 由测试验证，可持续滚动更新 |
| 4 | OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments | NeurIPS 2024 | 首个真实计算机（VM）可执行环境 + 369 真实任务 + 每题定制 execution-based 评分脚本 |
| 5 | τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | arXiv 2024（Sierra）；正式发表版多标注 ICLR 2025，投前请以 OpenReview 为准 | tool-agent-user 三方交互 + 领域政策遵循；DB 终态对齐客观评分；提出 pass^k 可靠性指标 |
| 6 | MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering | ICLR 2025（OpenAI） | 75 个 Kaggle 竞赛离线复现测 ML 工程能力；人类基线=Kaggle 真实榜单；反作弊/污染分析成专章 |
| 7 | BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents | arXiv 2025（OpenAI 技术报告，simple-evals 系列；非主会但影响极大） | 1266 个"难找但易验"的浏览问题；canary string 防泄漏；校准与 test-time scaling 分析 |

补充速写（2026 新作，见第八节）：Terminal-Bench 2.0（arXiv 2601.11868）与 Benchmarks as Software / benchmark maintenance debt（arXiv 2611.08417）。

---

## 一、GAIA（ICLR 2024）

链接：https://arxiv.org/abs/2311.12983 （HTML: https://ar5iv.labs.arxiv.org/html/2311.12983 ）

### 1. 发表处与年份、一句话定位
ICLR 2024（FAIR+HuggingFace+AutoGPT）。概念上对人类简单、对 AI 困难的现实助理问题集，唯一事实短答案保证自动评分；同时是一份"如何出题"的方法论。

### 2. 完整章节树
- 1 Introduction
- 2 Related Work（→ Evaluating Large Language Models；→ Evaluating General Assistants）
- 3 GAIA
  - 3.1 A convenient yet challenging benchmark for general AI assistants（What is GAIA and how does it work? / Design choices）
  - 3.2 Evaluation
  - 3.3 Composition of GAIA（Capabilities coverage / Increasing difficulty / Distribution of required capabilities）
  - 3.4 Building and extending GAIA（Crafting questions / Validating questions / Challenges associated to relying on the web）
- 4 LLMs results on GAIA（GPT4 plugins / Results）
- 5 Discussion（Reproducibility for closed-source assistants / Static versus dynamic benchmarks / Towards unified evaluation of generative models / Partial versus full automation）
- 6 Limitations（Missing evaluations / On the cost of designing unambiguous questions / Lack of linguistic and cultural diversity）
- 7 Acknowledgements
- 附录：A Extended related work；C Extended description（能力与文件类型分布）；D Extended description of our question design framework（含 D.1 Extended evaluation、标注/验证统计表 Table 1/3/4）

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 评估跟不上能力；"对人更难"的路线错；GAIA 哲学与四条设计原则 | 提出问题 + 宣告立场（t-AGI 里程碑叙事） |
| 2 | LLM 评估现状（饱和/污染/模型裁判缺陷）+ 助理评估现状（封闭 API、复用旧数据） | 界定 gap、排除"已有 benchmark 够用"的替代解释 |
| 3.1 | 是什么（466 题、附件、零样本）+ 四条 design choices 逐条论证 | 展示设计（原则→设计决策一一对应） |
| 3.2 | quasi exact match、唯一答案、格式化 system prompt | 评价协议（短小、可信） |
| 3.3 | 能力覆盖图、Level 1-3 难度操作化（steps×tools）、话题分布 | 展示覆盖度与难度标定的效度 |
| 3.4 | 出题（sources of truth、元数据标注）→ 验证（2 名新标注者独立作答，68% 一次通过，~2h/题）→ web 证据的时间漂移与 robots.txt | 构建管线 + 质控 + 可扩展方法论 |
| 4 | GPT-4±plugins、AutoGPT、human、web-search 基线；Figure 4 分数×耗时×Level；Figure 5 按能力分解 | 提供证据（主结果）+ 难度分级效度验证 |
| 5 | 可复现性、静态 vs 动态、系统级 vs 模块级评估、部分 vs 全自动化 | 讨论：从个例上升到评估范式（思想领导） |
| 6 | 三条局限各自成小节 | 主动划界（不评 trace、去歧义成本、语言单一） |

### 4. 引言的贡献点表述 + Figure 1
- 贡献写法：**不是**"we contribute X"，而是 4 条以 em-dash 起头的设计原则 bullet：Real-world and challenging / Easy interpretability / Non-gameability / Simplicity of use——每条自带"与既有 benchmark 的对比"。末段给 release 计划（166 dev 公开 + 300 holdout leaderboard）。
- Figure 1 = Level 1/2/3 各一道真实样题 + ground truth，直接展示"概念简单、步骤繁长"的张力。

### 5. Benchmark 构建呈现方式
- 任务/数据来源：人工出题（作者示范 + Surge AI 标注者），围绕 sources of truth（Wikipedia、arXiv、随题附件、自包含 puzzle）。
- 构建管线：Crafting questions（含元数据：工具、步骤、耗时）→ Validating questions（双人独立作答一致才通过；不一致→修补或删除）。
- 质控：验证阶段统计入文（68% as-is、其余修正/删除、标注者正确率 92% 即人类基线、单题成本 ~2h）。
- 规模统计：466 题（166+300）；Figure 3 能力覆盖（bar）+ steps×tools 散点按 Level 着色；附录给文件类型分布。
- 示例展示：Figure 1（样题）+ Figure 2（GPT-4 完整解题轨迹框，含 system prompt）。

### 6. 评价协议
唯一事实短答案（数字/短语/逗号列表），quasi exact match（按答案类型归一化），zero-shot + 格式化 system prompt（"FINAL ANSWER:" 模板），评分函数随 leaderboard 公开；"Oracle"标注（GPT-4+plugins 为人工选插件的上限估计）。

### 7. 实验组织
主图 = 方法 × Level 的分数与耗时（Figure 4）；分解 = 按能力（Figure 5，顺带暴露 memorization 线索）；人类基线 92%；web-search 基线（证明答案不在搜索首页）；每配置 3 次取均值。

### 8. 局限/伦理/数据声明
Limitations 独立成章、按主题三小节；Acknowledgements 明示付费标注来源；holdout 300 题不放答案（防污染的制度设计）。

### 9. 独特且值得借鉴的结构选择
把"设计原则"当贡献主体写；§3.4 把出题-验证的**人力成本与通过率数字**写进正文（benchmark 论文少有的工程透明度）；Discussion 升维到"评估范式哲学"；Level 难度用 steps×tools 双轴操作化并在实验中验证其效度。

---

## 二、AgentBench（ICLR 2024）

链接：https://arxiv.org/abs/2308.03688 （HTML: https://arxiv.org/html/2308.03688v3 ）

### 1. 发表处与年份、一句话定位
ICLR 2024（清华等）。首个系统化 LLM-as-Agent 基准：8 个交互环境、3 类 grounding、统一 Server-Client 评测工具包；29 个模型横评 + 失败原因量化。

### 2. 完整章节树（以 v3 为准）
- 1 Introduction
- 2 LLM-as-Agent: Definition and Preliminary（POMDP 形式定义 / CoT and Other Reasoning Strategies / Typical Types of Finish Reasons）
- 3 Composition of AgentBench: A Brief Look
  - 3.1 Code-grounded Environments（Operating System / Database / Knowledge Graph）
  - 3.2 Game-grounded Environments（Digital Card Game / Lateral Thinking Puzzles / House-Holding）
  - 3.3 Web-grounded Environments（Web Shopping / Web Browsing）
- 4 Evaluation of AgentBench（4.1 Evaluation Setup / 4.2 Main Results / 4.3 Analysis）
- 5 Related Work
- 6 Conclusion
- 附录：A Framework（传统框架 vs 自研框架、Max-Flow 调度）；B–I 每个环境一章（Dataset details / Actions / Prompt Example）；J Detailed Analysis（J.1 Validity Analysis of Execution Outcomes；J.2 Findings：Instruction Following Matters / Consistency and Execution in Agent Planning / Tokens and Rounds in Completed Trajectories / Task Limit Exceeded 主因 / Code Tuning 影响 / Self Correcting ability）

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | agent 评估缺失系统基准；AgentBench 设计 + 29 模型结论 + toolkit | 提出问题 + 贡献清单 |
| 2 | POMDP 形式化、为何只用朴素 CoT、五类 finish reason（CLE/IF/IA/TLE/Complete） | 建立形式语言 + **前置失败分类学**（为分析章预埋语汇） |
| 3 | 每环境一段式简介（动机、设定、指标），细节全部指到附录 | 展示设计（正文明细克制、附录全量） |
| 4 | 统计表（Table 2）、模型清单（Table 1）、toolkit（Docker 隔离+HTTP server）、主表、4.3 分析 | 提供证据 + 排除替代解释（见下） |
| 5–6 | 短相关工作与结论 | 收束 |
| J | 执行结果有效性分析 + 6 组发现 | 深度归因（失败原因、训练策略线索） |

### 4. 引言的贡献点表述 + Figure 1
- 贡献 bullet 3 条：①概念+基准（8 环境 3 类）；②27/29 模型系统评测 + 失败原因定量分析 + 改进方向（instruction following、高质量对齐数据、code training 双刃剑）；③integrated toolkit（Server-Client、模块化、HTTP 协议接入任意模型）。
- Figure 1 = 总览双图：(a) 各模型相对各环境最优的雷达/条形；(b) 8 环境 overall 总分柱状 + 两类模型均值虚线——一眼看出"差距与距离可用都很远"。

### 5. Benchmark 构建呈现方式
- 任务/数据来源：5/8 环境新建、其余改编（ALFWorld、WebShop、Mind2Web 改造为 prompt-only 评测）。
- 构建管线：不设独立 construction 章；每环境"正文一段 + 附录一章（dataset details / actions / prompt example）"；DB 环境含 data augmentation 及其偏差研究（附录 C.4）。
- 质控：附录 J.1 "Validity Analysis"（把执行结果分为有效/无效并统计）——用统计把"格式/执行失败"与"能力不足"分离。
- 规模统计：Table 2（每环境 avg turn、metric、#Dev、#Test 均以"题数/总交互轮数"双数字呈现、Weight-1 权重）；另给成本锚点："约 4k/13k 次推理调用，与 MMLU 相当"。
- 示例展示：附录各环境 Prompt Example。

### 6. 评价协议
每环境一个指标（SR、F1、Reward、Game Progress、Step SR）+ 加权 overall；诊断指标 = finish reason 分布（CLE/IF/IA/TLE）；统一 CoT prompt 范式（不做多采样/反思等增强，保持"最便宜最常见"基线）。

### 7. 实验组织
主表 = 模型（API 组/OSS 组）× 8 环境 + overall（Table 1 列模型清单是独立表）；4.3 + 附录 J 做失败归因（指令遵循、计划一致性、重复生成导致 TLE、code tuning 双刃剑、自纠错能力）。

### 8. 局限/伦理/数据声明
无独立 Limitations/伦理章（ICLR 版把警示散在分析与结论中）；数据与工具开源、leaderboard 挂 llmbench.ai。

### 9. 独特且值得借鉴的结构选择
"Definition and Preliminary" 独立成章并**前置失败分类学**；正文一段+附录一章的环境呈现节律；统计表显式给交互成本（turns / calls）；Validity Analysis 作为"排除测量噪声"的证据。

---

## 三、SWE-bench（ICLR 2024 oral）

链接：https://arxiv.org/abs/2310.06770 （HTML: https://arxiv.org/html/2310.06770 ）

### 1. 发表处与年份、一句话定位
ICLR 2024 oral（Princeton）。从 12 个真实 Python 仓库的 issue+PR+tests 构建 2294 个软件工程任务；以测试执行验证 patch；最佳模型 1.96%，基准可持续滚动更新。

### 2. 完整章节树
- 1 Introduction
- 2 SWE-bench
  - 2.1 Benchmark Construction（Stage I: Repo selection and data scraping / Stage II: Attribute-based filtering / Stage III: Execution-based filtering）
  - 2.2 Task Formulation（Model input / Evaluation metrics）
  - 2.3 Features of SWE-bench（6 个特性段落）
  - 2.4 SWE-bench Lite
- 3 SWE-Llama: Fine-tuning CodeLlama for SWE-bench（Training data / Training details）
- 4 Experimental Setup（4.1 Retrieval-Based Approach：sparse BM25 / "Oracle" retrieval；4.2 Input Format；4.3 Models）
- 5 Results（主表 + Difficulty differs across repositories / Difficulty correlates with context length / Difficulty does not correlate with issue resolution date / "Oracle"-collapsed 消融；5.1 A Qualitative Analysis of SWE-Llama Generations）
- 6 Related Work
- 7 Discussion
- 8 Ethics Statement / 9 Reproducibility Statement / 10 Acknowledgements
- 附录：A Benchmark Details（A.2 Construction Process / A.3 Execution-Based Validation / A.4 Evaluation Procedure / A.5–A.7 数据集刻画与 Lite）；B 训练细节；C Additional Results（oracle retrieval、GPT-4 子集、temporal analysis、F2P/P2P 分析、patch 生成扩展分析、SE metrics）；D 实验细节（Prompt Template）；E Societal Impact；F SWE-Llama 生成案例深度分析

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 需要难而可验证的基准；真实软件工程是理想试验场 | 提出问题（"难题易验证"张力） |
| 2.1 | 3 阶段过滤管线：90k PR → 2294 题 | 构建管线（数字漏斗=质量证明） |
| 2.2 | 输入（issue+codebase）与指标（% Resolved） | 任务形式化 |
| 2.3 | 6 个卖点：real-world tasks / continually updatable / diverse long inputs / robust evaluation / cross-context editing / wide scope for solutions | 展示设计并逐条对比传统 NLP benchmark |
| 2.4 | Lite 300 题（更自包含、便宜） | 易用性/可采纳性 |
| 3 | SWE-bench-train 19k + SWE-Llama 微调（训练仓库与评测仓库不相交） | 提供开源基线 + 防污染设计 |
| 4 | BM25 vs oracle 检索、输入格式、模型 | 评测 harness 与公平性（检索质量显式化） |
| 5 | 主表 + 4 个分析（按 repo、按 context 长度、按日期、oracle-collapsed） | 提供证据 + **排除替代解释**（日期分层→排除"背新版仓库作弊"） |
| 6–7 | 相关工作、Discussion（可持续更新愿景） | 收束 |
| 8/9/10 | ICLR 伦理/可复现声明 | 合规惯例 |
| E | Societal Impact（附录） | 伦理处理 |

### 4. 引言的贡献点表述 + Figure 1
- 贡献在引言末段散文式给出：SWE-bench 框架 + SWE-bench-train 训练集 + SWE-Llama 7b/13b（强调 100k+ token 上下文）。
- Figure 1 = 任务来源与评测闭环示意图（GitHub issue→merged PR→tests→codebase snapshot→模型 patch→测试验证）。

### 5. Benchmark 构建呈现方式
- 数据来源：12 个热门 Python 仓库的 merged PR（约 90k）。
- 管线：3-stage 过滤（属性过滤：关联 issue 且改测试文件；执行过滤：存在 fail-to-pass 测试、可安装无报错）→ Figure 2 流程图。
- 质控：执行验证（A.3）；每题 ≥1 条 fail-to-pass 测试，40% 题有 ≥2 条，median 51 条 pass-to-pass 防回归。
- 规模统计：Table 1（issue 词数、codebase 文件/行数、gold patch 行/文件/函数数、测试数的 mean/max）+ Figure 3 按仓库分布。
- 示例展示：附录 prompt template 与案例；5.1 定性分析生成。

### 6. 评价协议
unix patch 应用 + 跑关联测试，全部通过=% Resolved；附带 % Apply（patch 可否应用）作诊断列；oracle 检索作为上界参照。

### 7. 实验组织
主表 = 模型 × {SWE-bench, Lite} × {%Resolved, %Apply}（BM25 三档上下文长度）；分析含 per-repo 难度、难度-上下文长度正相关（"oracle-collapsed"消融证明"定位难"而非"生成难"）、按 2023 前后分层（排除污染）；qualitative 分析两处（5.1 与附录 F）。

### 8. 局限/伦理/数据声明
Ethics Statement + Reproducibility Statement 独立成节（ICLR 模板惯例）；Societal Impact 进附录 E；Discussion 承认人工依赖低、可持续更新但会衰减。

### 9. 独特且值得借鉴的结构选择
"Features of SWE-bench" 把卖点写成 6 个命名段落（可直接被引用）；Lite 子集专治"太贵太难没人用"；日期分层 + 训练/评测仓库不相交，用**实验设计**而非口头声明排除数据污染；% Apply 诊断列把"不会写 patch"与"写错 patch"分开。

---

## 四、OSWorld（NeurIPS 2024）

链接：https://arxiv.org/abs/2404.07972 （HTML: https://arxiv.org/html/2404.07972 ）

### 1. 发表处与年份、一句话定位
NeurIPS 2024（HKU 等）。首个可扩展的真实计算机 VM 环境（Ubuntu/Windows/macOS）+ 369 个真实跨应用任务 + 每题定制 execution-based 验证脚本；human 72.36% vs 最佳 12.24%。

### 2. 完整章节树
- 1 Introduction
- 2 OSWorld Environment
  - 2.1 Task Definition（POMDP）
  - 2.2 Real Computer Environment Infrastructure（2.2.1 Overview / 2.2.2 Initial Task Environment Setup / 2.2.3 Execution-Based Evaluation）
  - 2.3 Observation Space / 2.4 Action Space
- 3 OSWorld Benchmark
  - 3.1 Operating System and Software Environments
  - 3.2 Tasks（Task instructions and scenarios / Initial state setup configs / Execution-based evaluation / Quality control）
  - 3.3 Data Statistics（Statistics / Comparison with existing benchmarks）
  - 3.4 Human Performance
- 4 Benchmarking LLM and VLM Agent Baselines
  - 4.1 LLM and VLM Agent Baselines（Accessibility tree / Screenshot / Screenshot + accessibility tree / Set-of-Marks）
  - 4.2 Results（4 个陈述句小标题发现）
- 5 Analysis
  - 5.1 Performance by Task Difficulty, Feasibility and App Involved（Task difficulty / Feasibility / Number of apps involved）
  - 5.2 Performance by Multimodal Observation Variances（截图分辨率 / 轨迹历史长度 / 窗口位置尺寸扰动与无关信息）
  - 5.3 Performance across Different Operating Systems
  - 5.4 Qualitative Analysis（Success and failure cases / Common errors by GPT-4V agents / Discrepancies in task difficulty between agent and human / Tasks where humans outperform agents / Tasks where agents outperform humans / Comparative analysis: Claude-3 vs. GPT-4V）
- 6 Related Work（Benchmarks for multimodal agents / Vision-language models for multimodal agents）
- 7 Conclusion and Future Work（Enhancing VLM capabilities / Advancing agent methodologies / **Addressing the safety challenges of agents in realistic environments** / Expanding and refining data and environments）
- 附录：A 环境细节（observation/action space 全 API）；B benchmark 细节（OS/软件选择、Task Example Sources、Task Examples Collection、Initial State Setup、Evaluation Configuration Details 按软件逐个、More Task Examples）；C baseline 细节（hyper-parameters、Prompts 全文、a11y 过滤、SoM 实现、Full Results）；D qualitative 例子

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 现有基准要么不可执行要么限于单一应用；OSWorld=真实环境+真实任务 | 提出问题 + 主张"环境先行" |
| 2 | 环境章：任务定义（POMDP，含 infeasible 任务"正确报告失败"计分）、VM 基础设施、初始状态配置、执行式评价、观测/动作空间 | 展示设计（基础设施可信性） |
| 3 | benchmark 章：软件生态、任务四段序列、统计与对比、人类表现 | 展示设计 + 质控 + 效度（人类基线前置） |
| 4 | 4 种观测/标注设置 × 模型；结果 4 条发现 | 提供证据（主实验） |
| 5 | 难度/可行性/应用数分桶；观测方差受控消融；跨 OS；定性 6 小块 | 分析：归因 + 排除替代解释 + 案例 |
| 6–7 | 相关工作；结论含 4 个未来方向（含 safety） | 收束 + 议程设置 |

### 4. 引言的贡献点表述 + Figure 1
- 贡献无正式 bullet，藏在段落中：①真实可执行环境（可扩展、跨 OS）；②369 题 benchmark（初始状态配置 + 定制验证脚本，134 个 unique 评价函数）；③全面基线评测与分析；④开源。
- Figure 1 = 环境+任务总览：上排任务截图示例（跨应用工作流），下排环境能力标注（task setup / execution-based evaluation / interactive learning）。

### 5. Benchmark 构建呈现方式
- 任务来源：真实用户使用场景（B.3 Task Example Sources）；9 位 CS 背景标注者。
- 构建呈现：3.2 Tasks 的固定四段序列——**instructions → initial state configs → execution-based evaluation → quality control**；验证脚本以 Table 1 三列展示（Initial State 截图 | Task Instruction | Evaluation Script 简化代码）。
- 质控：Quality control 小节 + 执行验证（预设/后处理/取数/判定函数）；动态内容用实时 getter（爬虫取当前值再比对）。
- 规模统计：3.3 Statistics + "Comparison with existing benchmarks" 对比表（任务数、评价函数数、可执行性等）。
- 示例展示：Table 1 评测脚本案例 + 附录 B.8 More Task Examples + 附录 D 定性案例。

### 6. 评价协议
每题定制 execution-based 脚本（pre-setup、post-processing、getter、eval function），reward ∈ [0,1]（完全达成=1、部分达成<1、**infeasible 任务正确报告失败也计分**）；15 步上限；支持并行 VM。

### 7. 实验组织
主表 = 模型 × 观测设置 × 任务组；4.2 四条发现用完整陈述句做小标题（"LLMs and VLMs are still far from being digital agents…"）；5.1 难度/可行性/应用数分桶（可行性维度直接对应"有些任务本来就该拒绝"）；5.2 观测方差消融（分辨率、历史长度、窗口扰动——受控干预实验范本）；5.4 定性 6 小块（含 agent>human 的反向案例）；人类基线 72.36% 且分任务类型稳定。

### 8. 局限/伦理/数据声明
无独立 Limitations 章；结论把 safety 明确列为未来方向小节；数据/环境/基线全开源。

### 9. 独特且值得借鉴的结构选择
**Environment 与 Benchmark 两章分离**；3.2 Tasks 的"instruction→setup→evaluation→quality control"四段固定序列；可行性（feasibility）作为一等分析维度；验证脚本案例用三列表格展示（case study 框表格化）；观测方差受控消融独立一小节。

---

## 五、τ-bench（arXiv 2024；正式发表版 2025）

链接：https://arxiv.org/abs/2406.12045 （HTML: https://arxiv.org/html/2406.12045 ）

### 1. 发表处与年份、一句话定位
Sierra Research 2024（arXiv:2406.12045）；正式发表版（社区多标注 ICLR 2025，投前请核对 OpenReview）。评测 agent 与模拟用户的动态多轮对话 + 领域政策遵循 + API 工具使用；以数据库终态对齐客观评分；提出 pass^k 衡量可靠性；gpt-4o pass^1 < 50%。

### 2. 完整章节树
- 1 Introduction
- 2 Related Work（Benchmarks for language agents and tool use / Task-oriented dialogue / User simulation with LMs）
- 3 τ-bench: A benchmark for Tool-Agent-User Interaction（Databases and APIs / Domain policy / User simulation / Task instances / Reward / Pass^k metric）
- 4 Benchmark Construction（4.1 Domains / 4.2 Key Characteristics；Stage I: manual design of database schema, APIs, and policies / Stage II: data generation / Stage III: manual scenario generation and verification）
- 5 Experiments（5.1 Main results / 5.2 Research challenge analysis）
- 6 Discussion（Challenges for agents）
- 附录：A Additional Results；B Benchmark Construction（B.1 Stage I：API design example / Retail policies / Airline policies；B.2 Stage II: data generation）；C Retail Examples（C.1 Data examples；C.2 Task and trajectory examples：Task 0: wrong decision / Task 7: wrong argument / Task 42: partially solve compound requests）；D Airline Examples（含成功轨迹）

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 现有基准不测 user 交互与规则遵循；三个 desiderata | 提出问题（部署需求导向） |
| 2 | 三条线（tool-use / 任务型对话 / 用户模拟）各一段 | 界定 gap：三者从未统一 |
| 3 | POMDP 形式化 + 组件逐一定义 + reward 公式 + pass^k 定义 | 展示设计（模块化：DB/API/policy/user/task） |
| 4 | 三阶段构建（人工设计 schema/API/policy → LM 辅助生成数据 → 人工场景与验证）+ 域与关键特性 | 构建管线 + 质控 |
| 5 | 主表（模型×域×pass^1/pass^k）+ 失败三分类（wrong decision / wrong argument / partially solve compound requests） | 提供证据 + 归因 |
| 6 | 讨论 agent 面临的挑战 | 收束 |
| 附录 | 政策全文、数据与轨迹案例 | 可复核性 |

### 4. 引言的贡献点表述 + Figure 1
- 贡献写法：先列部署 desiderata（①与人和 API 长程交互 ②遵循领域规则 ③一致性），再顺势给出：τ-bench 模块化框架（数据库+API、政策文档、用户场景+ground truth）、DB 终态对比的忠实高效评估、pass^k 新指标。
- Figure 1 = (a) 架构示意（agent↔数据库 API↔LM 模拟用户，政策文档在侧）(b) τ-airline 真实轨迹（agent 须按政策**拒绝**用户改签请求并给出替代方案）。

### 5. Benchmark 构建呈现方式
- 任务/数据来源：客服域（retail/airline）；Stage I 人工设计 schema/API/policy（简化自真实业务）；Stage II LM 辅助数据生成；Stage III 人工写用户场景并验证。
- 质控：任务指令设计保证"政策下唯一 outcome"；ground truth = 数据库写动作（+必要输出信息）。
- 规模：两域任务实例（附录给分布）；任务实例 JSON 四面板展示（Figure 2: DB 条目 / API 代码 / 政策摘录 / 任务指令+actions）。
- 示例展示：Figure 2 四面板 + 附录 C/D 的轨迹案例（按失败类型编号选取）。

### 6. 评价协议
r = r_action × r_output ∈ {0,1}（终态 DB 与 ground truth 逐字段一致 × 用户回复含必要信息）；gpt-4-0613 模拟用户（###STOP### 终止）；pass^k = k 次独立试次全部成功的概率（与 pass@k 对偶）；明确声明 r=1 是必要非充分（如未确认即执行仍违规）。

### 7. 实验组织
主表 = 模型 × {retail, airline} × pass^1/pass^k（function calling 与 ReAct 两范式）；5.2 失败分析直接用三分类命名（decision/argument/compound）；附录给每类的完整案例。

### 8. 局限/伦理/数据声明
无独立伦理/局限章；Discussion 承认评分的必要非充分性与模拟用户偏差；代码数据开源（github.com/sierra-research/tau-bench）。

### 9. 独特且值得借鉴的结构选择
pass^k 把"可靠性"做成一等指标（对安全 benchmark 直接可迁移）；政策文档作为独立组件；DB 终态客观评分**容忍对话随机性**（评分与过程解耦）；失败三分类与轨迹案例一一对应地放附录。注意后续生态：社区已发布 τ-Bench Verified（修正标注错误与欠规范任务），说明"任务欠规范"会被审稿人当攻击点（见 SABER, ICLR 2026 投稿）。

---

## 六、MLE-bench（ICLR 2025，OpenAI）

链接：https://arxiv.org/abs/2410.07095 （HTML: https://arxiv.org/html/2410.07095 ）

### 1. 发表处与年份、一句话定位
ICLR 2025（OpenAI）。75 个 Kaggle 竞赛离线复现，端到端测 ML 工程 agent（训模型、备数据、跑实验）；o1-preview+AIDE 16.9% 拿牌；人类基线=真实 Kaggle 榜单；污染/作弊分析成专章。

### 2. 完整章节树
- 1 Introduction（编号贡献 4 条）
- 2 MLE-bench
  - 2.1 Dataset Curation
  - 2.2 Metrics（Leaderboards / Medals / Headline metric / Raw Scores）
  - 2.3 Setup（Validating submissions；2.3.1 Rules：Rule-breaking detection / Plagiarism detection）
- 3 Experiments and Results
  - 3.1 Main experiment（Varying scaffolding / Varying models / Discussion）
  - 3.2 Increasing number of attempts
  - 3.3 Varying amount of compute available
  - 3.4 Increasing time available
- 4 Contamination & Plagiarism（4.1 Familiarity with top solutions / 4.2 Obfuscating competition descriptions）
- 5 Related Work
- 6 Limitations
- 7 Conclusion（Ethics Statement / Reproducibility Statement）
- 附录：A.1 Dataset Curation Criteria / A.2 Distribution of Competitions / A.3 Runs analysis / A.4 Plagiarism detection tool / A.5 Setup details / A.6 Scaffold details（AIDE、OpenHands、MLAB 逐个修改）/ A.7 Dataset / A.8 Obfuscated Descriptions / A.9 Performance by complexity, category, and competition date

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 端到端 ML 工程评估缺失；MLE-bench 两个设计轴（任务现实性、可对齐人类水平） | 提出问题 + 战略叙事（安全框架的度量用途） |
| 2.1 | 5673→586→75 人工筛选漏斗；复杂度标注；新 train-test 划分；本地评分代码 | 构建管线 + 质控 |
| 2.2 | medal 阈值表化；headline=any medal %；raw score 兜底 | 评价协议（指标设计含"天花板对齐人类历史成就"论证） |
| 2.3 | 校验服务器 + 规则（禁手写提交、禁看解法）+ GPT-4o 日志查违规 + Dolos 查抄袭 | 完整性/反作弊工程 |
| 3 | 按"资源缩放轴"组织：scaffold→model→attempts→compute→time | 实验=研究问题矩阵（而非流水账） |
| 4 | familiarity 指标（训练语料似然）与成绩无相关；混淆竞赛描述重跑 | **排除污染替代解释的专章** |
| 6–7 | Limitations 独立；Ethics/Reproducibility 声明 | 划界 + 合规 |

### 4. 引言的贡献点表述 + Figure 1
- 贡献 4 条编号列表：①75 竞赛基准（ML 工程师手工打造）；②SOTA 模型+框架大规模评测；③资源缩放实验（运行时长、硬件、pass@k）；④污染-性能关系实验 + 监控工具（查抄袭/作弊）。
- Figure 1 = 环境总览（每竞赛含 description、dataset、grading code；本地评分并对比真实榜单）；Figure 2 = 3 种 scaffold 真实轨迹摘录（并排对比）。

### 5. Benchmark 构建呈现方式
- 来源：Meta Kaggle 全量 5673 完赛 → 排除 Community → 586 人工筛选（无法复现评分/无法重建划分者剔除）→ 75 正式 + 7 dev；每题四要素（描述、数据、评分代码、榜单快照）。
- 质控：新划分以 example submission 在新旧测试集上得分相近校验分布一致；复杂度三级标注（<2h / 2–10h / >10h）；规则+检测工具（GPT-4o 审日志、Dolos 相似度>60% 取消资格）。
- 规模统计：22 Low/38 Medium/15 High；总奖金 $1,948,016（平均 $25,974/题）作"真实价值"锚点；附录 A.2 分布图。
- 示例展示：Figure 2 轨迹摘录；附录逐 scaffold 的实现修改。

### 6. 评价协议
提交 CSV→本地 grading code 评分→与 Private 榜单对齐授牌（bronze/silver/gold 阈值表 Table 1）；headline = any medal %（"9 位人类累计 75 牌"的天花板论证）；3 seeds 取 mean±SE（o1-preview 16 seeds、GPT-4o 36 seeds）；资源明示（24h、A10 GPU、36 vCPU、440GB RAM）。

### 7. 实验组织
主表 = scaffold×model 的七列漏斗分解（Made Submission % → Valid % → Above Median % → Bronze/Silver/Gold % → Any Medal %）——**把"没做出来"与"做错了"分开**；3.2 pass@k 曲线；3.3 硬件表；3.4 每小时快照曲线；附录 A.9 按 complexity/category/date 分桶；3.1 Discussion 定性归因（提前停、填满上下文、不算时间预算）。

### 8. 局限/伦理/数据声明
6 Limitations 独立成章；Ethics Statement、Reproducibility Statement 作为 Conclusion 子块（ICLR 惯例）；主动声明"可作为安全框架的能力度量"。

### 9. 独特且值得借鉴的结构选择
反作弊/污染**专章**（familiarity 实验 + 描述混淆实验 + 日志审查 + 抄袭检测四件套）；实验按资源缩放轴组织；主表的"漏斗列"；headline metric 与人类历史成就显式对齐；"低复杂度子集推荐"降低使用门槛。

---

## 七、BrowseComp（2025，OpenAI）

链接：https://arxiv.org/abs/2504.12516 （HTML: https://arxiv.org/html/2504.12516 ）

### 1. 发表处与年份、一句话定位
OpenAI 技术报告 2025（simple-evals 系列，非主会但被广泛采用）。1266 个"难找但易验"的浏览问题，测持久搜索与创造性检索；答案短字符串、LLM judge 语义等价评分。

### 2. 完整章节树
- 1 Introduction
- 2 Data collection and verification（2.1 BrowseComp criteria / 2.2 Dataset diversity / 2.3 Grading / 2.4 What BrowseComp exercises）
- 3 Human performance on BrowseComp
- 4 Evaluation of models（4.1 Performance of OpenAI models / 4.2 Calibration Analysis / 4.3 Test-time compute scaling / 4.4 Aggregation strategies leveraging additional compute / 4.5 Distribution of pass rates）
- 5 Related work and discussion
- 附录：A Additional instruction for model prediction；B Grading prompt

### 3. 各节一句话概括 + 论证职责
| 节 | 内容 | 论证职责 |
|---|------|---------|
| 1 | 互联网检索被现有基准做"易找信息"而饱和；BrowseComp=难找信息 | 提出问题 + 极简设计宣言（2 条属性 bullet） |
| 2.1 | 三条难度检查（当时模型解不出/搜索首页查不到/人 10 分钟解不出，>40% 被人解出即重写）+ 反向出题法 + 唯一性风险与缓解 | 构建标准（难度的操作化=质控） |
| 2.2 | 主题分布（事后 ChatGPT 分类） | 多样性证据 |
| 2.3 | 短答案 + LLM judge 语义等价（HLE 同款 prompt） | 评价协议 |
| 2.4 | 明说测什么（factuality / persistence / creativity）与不测什么（长回答、歧义消解） | **能力边界声明**（防御性自我划界的正面示范） |
| 3 | 人类基线：70.8% 两小时放弃、29.2% 解出、86.4% 与参考答案一致；时间直方图 | 难度效度 |
| 4 | 模型 accuracy+calibration；test-time compute scaling；并行聚合策略；pass rate 分布 | 证据 + 新分析维度（校准/缩放/难度分布） |
| 5 | 相关工作与讨论合并 | 收束 |

### 4. 引言的贡献点表述 + Figure 1
- 贡献写法：Table 1 三道样题+答案（**带 canary string 防训练泄漏**）+ 两条设计属性 bullet（Challenging questions / Simple and easy-to-verify）。
- Figure 1 = accuracy 随 test-time compute（log 轴）平滑上升的缩放曲线——一张图立起"测核心能力且有区分度"。

### 5. Benchmark 构建呈现方式
纯人工 trainer 从"seed 事实"构造反向问题（先有答案、后有问题）；难度三检查写成可审计流程；唯一性风险明说并给缓解（加约束、二次 trainer 10 分钟挑战）；规模 1266；多样性=兴趣驱动+事后主题分类分布图。

### 6. 评价协议
单短串答案 + LLM judge（HLE grading prompt 全文入附录 B）；另报 Calibration Error；请求社区不公开样题原文（防泄漏的社区规范声明）。

### 7. 实验组织
主表 = 模型 × {Accuracy, Calibration Error}；4.2 校准分析；4.3 缩放曲线；4.4 聚合策略（并行+多数投票/LLM re-judge）；4.5 按题 pass rate 分布（难度桶）；人类基线以"放弃率"呈现。

### 8. 局限/伦理/数据声明
无独立 Limitations（并入 §5 discussion）；§2.4 显式声明不测长回答/歧义；canary string + "不要公开样题"请求是其防泄漏特色。

### 9. 独特且值得借鉴的结构选择
"难而易验"一句话设计哲学贯穿全文；人类基线用**放弃率**；calibration 与 test-time scaling 进入标准分析；canary string；grading prompt 全公开。

---

## 八、2026 新作速写（趋势补给）

### Terminal-Bench 2.0（arXiv 2601.11868，2026-01）
https://arxiv.org/abs/2601.11868
- 树：1 Intro → 2 Terminal-Bench（2.1 Task Formulation / 2.2 Dataset Construction / 2.3 Verification / 2.4 Composition）→ 3 Experimental Setup（3.1 Terminus 2 harness / 3.2 Agents / 3.3 Models / 3.4 Harbor 平台）→ 4 Results（4.1 Cost and Model Performance / 4.2 Performance Over Time / 4.3 Predicted vs. Empirical Difficulty / 4.4 Trajectory-Level Error Analysis / 4.5 Command-Level Error Analysis）→ 5 Limitations → 6 Related Work → 7 Conclusion；附录 A 详细结果、B Quality Control（Contributor Checklist / Check Tools / Debug Tool / **Adversarial Exploit Agent** / ABC 自评）、C Trace Failure taxonomy + **LLM Judge Prompts 全文**（8 类：Disobey Task Specification、Step Repetition、Unaware of Termination、Context Loss、Premature Termination、No/Irrelevant Verification、Reasoning–Action Mismatch、Weak Verification）、D Adapters、E 命令失败分析、F harness、G token/episode 效率、H 任务清单、I LLM usage 声明。
- 值得借鉴：①Quality Control 独立附录成体系（贡献者清单+自动检查+调试工具+**对抗性利用 agent 红队**+Agentic Benchmark Checklist 自评）；②失败 taxonomy + judge prompt 全公开；③4.1 把 **cost 与成功率并列**；④4.3 人工预测难度 vs 实证难度校验；⑤附录 I "LLM Usage" 声明（论文写作中 LLM 辅助的披露已成惯例）。

### Benchmarks as Software: Terminal-Bench and the Case for Continuous Benchmarks（arXiv 2611.08417，2026-11）
https://arxiv.org/abs/2611.08417
- 提出 "benchmark maintenance debt"：发布时验证过的基准会腐化（模型发现合法解被 verifier 拒绝、基础设施变更破坏假设）；对 Terminal-Bench 2.0 审计发现 ~30% 任务有问题，修复后成绩变动 >10pp、名次最多挪 3 位（Spearman ρ=0.958）；资源预算（wall-clock）也是测量规范的一部分。
- 对我们的启示：在 Limitations/未来工作中承认并设计"持续验证/维护"机制，会显得非常前沿。

---

## 九、共性"结构惯例"总结

### 1) 全文骨架（出现频率）
```
1  Introduction          —— gap → 设计哲学/原则 → 贡献 bullets → release；Figure 1 总览
2  Related Work          ——（或前置 "Definition/Preliminary" 章，AgentBench/OSWorld/τ-bench 形式化 POMDP）
3  The Benchmark         —— 任务定义 → 构建管线 → 质控 → 规模统计/对比表 →（人类基线可前置于 3.x）
4  Evaluation Protocol   —— 指标定义、harness、成本/预算、seed 数（常并入 3 或 4）
5  Experiments/Results   —— 主表 + 由研究问题驱动的子节（scaffold/model/资源/设置消融）
6  Analysis              —— 分桶难度、受控干预、失败 taxonomy+案例、污染排除
7  Discussion/Limitations
8  Ethics / Reproducibility / Impact Statements（ICLR/NeurIPS 模板惯例）
附录 —— 每任务/环境/域细节、prompts、judge prompts、完整结果表、案例
```

### 2) Construction 章的固定小节序列（最稳定的惯例）
**数据来源 → 筛选/生成漏斗（带数字：90k→2294、5673→586→75、68% 一次通过）→ 任务实例结构（输入/标注/ground truth）→ 质控（多标注者交叉验证 / 执行验证 / 反作弊工具）→ 规模与分布统计表 →（对比已有基准表）→ 示例展示（Figure/Table 的 case 框）**。
质控的"数字透明度"是高水准论文的分水岭：GAIA 报 68%/92%/2h，SWE-bench 报 fail-to-pass 数与 median 51 回归测试，MLE-bench 报筛选漏斗与复杂度标注。

### 3) 主表的标准形态
- 行 = 模型/配置（API 与 OSS 分组；模型清单常单独成 Table 1）；列 = 任务组/域/环境 + Overall + **诊断分解列**（Valid Submission %、% Apply、finish-reason 分布）。
- "漏斗列"（做了→有效→对）把能力缺陷与格式/执行噪声分离。
- 多 seeds + mean±SE（MLE-bench）；可靠性指标 pass^k（τ-bench）或至少多次采样。
- 每表配 human/oracle 上界行（GAIA 92%、OSWorld 72.36%、BrowseComp 放弃率、MLE-bench Kaggle 榜、SWE-bench oracle 检索）。

### 4) 分析章节的常见类型（按出现频率）
① 难度/类别/时间分桶（all）；② 受控消融（观测/输入方差：OSWorld 分辨率与历史长度、SWE-bench context 长度与 oracle-collapsed、MLE-bench compute/time/attempts）；③ 失败 taxonomy + 定量占比 + 案例（AgentBench finish reasons、τ-bench 三分类、Terminal-Bench 8 类）；④ 污染/作弊排除（MLE-bench 专章、SWE-bench 日期分层、BrowseComp canary）；⑤ 校准/一致性（BrowseComp calibration、τ-bench pass^k）；⑥ 定性成功/失败案例成块（OSWorld 5.4 六小块）。

### 5) 图表位置惯例
- Figure 1 在 Introduction：概念+样例双面板（GAIA 样题、τ-bench 架构+轨迹、OSWorld 环境+任务、SWE-bench 流程图）或一张核心 scaling 曲线（BrowseComp）。
- Construction 章：管线流程图 + 统计表 + "Initial State | Instruction | Evaluation" 三列案例表（OSWorld Table 1）或四面板 JSON/代码（τ-bench Figure 2）。
- Results 章：主表 + 资源/缩放曲线；Analysis 章：分桶图 + 失败案例框。

### 6) 论证职责链（高水准论文的暗线）
提出问题（为什么现有基准不行）→ 展示设计（原则→决策一一对应）→ 质控与效度（人类基线、验证数字）→ 提供证据（主表）→ **排除替代解释**（污染、格式噪声、检索质量、token 预算、执行有效性的专项实验）→ 归因（失败 taxonomy）→ 划界（Limitations/能力边界）。负面结果（"防御打不下 ASR"）必须走"排除替代解释"环节才可信。

---

## 十、针对我们论文的 10 条建议

论文定位提醒：benign（无攻击者）任务中 tool-using agent 的安全；核心概念 context-environment gaps（上下文被当作可信依据 vs 必须对照部分可观测环境验证）；三类 case（requirement underspecification / requirement infeasibility / factual inconsistency）；种子→批量扩展；每 case 带安全对照版；人工证据标签；LLM-as-Judge+人工三分类失败归因；三个主实验（防御无效、拓扑对照、wording×position 干预）。

1. **Construction 章照搬"固定小节序列"并升格"安全对照版"为一节**。建议骨架：`3.1 Task Definition（context-environment gap 的形式化，含"验证失败→危险动作"定义）→ 3.2 Case Construction Pipeline（seed→批量扩展，三类各给生成规则）→ 3.3 Controlled Safe Pairs（每 case 的安全对照版：移除坑点、验证模型能力无问题；配"同题危险版 vs 安全版"案例对照框）→ 3.4 Evidence Annotation & Quality Control（人工证据标签协议、多人交叉验证数字、标注成本）→ 3.5 Data Statistics（三类规模、gap 属性分布、与已有基准对比表）→ 3.6 Human Performance（人类基线）`。"安全对照版"是你们独有的 paired design，值得像 τ-bench Figure 2 那样用四面板/三列表格展示一个完整 case 对。

2. **Figure 1 = 概念+实例双面板**：左=context-environment gap 概念图（用户指令/文档 vs 部分可观测环境，证据核验路径与危险动作）；右=一个真实 case 的危险版/安全对照版并排（标注哪里是 gap、缺什么证据、产生的危险动作）。所有标杆论文的 Figure 1 都承担"一图讲完设计"职责。

3. **引言贡献 bullet 3–4 条，按"基准+方法论 / 大规模评测+发现 / 受控分析+归因 / 资源开放"分配**。第一条别只说"我们提出了 X benchmark"，学 GAIA/BrowseComp 把设计原则（如"验证失败即危险""paired safe controls""证据可审计"）写成带对比的 bullet。结论段给 release 计划（dev split 公开、holdout/leaderboard 保留）。

4. **失败归因 taxonomy 前置定义、后置使用**。学 AgentBench §2：把三分类（证据搜集不足 / 证据充足但未识别危险 / 识别到危险仍盲从）在 benchmark 章给**操作定义+判定标准**，实验章只引用；附录给 LLM judge prompt 全文（Terminal-Bench C.2 先例）+ judge 与人工一致率 + 混淆矩阵。审稿人对 LLM-as-Judge 的信任全靠这组数字。

5. **主表做成"漏斗/分解"形态**：行=模型/agent 配置，列=三类 case × {ASR, 危险动作率, benign 任务成功率（对照）, 验证行为率（是否核验证据）}；多 seeds 报 mean±SE（MLE-bench 惯例）；增加可靠性指标（pass^k 式"多次全部安全"，τ-bench 直接可迁移——安全场景里"一次出事即失败"，pass^k 语义天然契合）。

6. **三个主实验按"研究问题"组织成三节，每节=问题→设计（自变量/因变量/控制）→结果→威胁排除**。实验①（防御无效）必须补 sanity check（防御在其原生任务/公开数据上确实有效？超参消融？），否则"打不下"会被解读为防御实现弱；实验②（拓扑）把"非 token 预算解释"写成显式 claim + 匹配预算对照证据（SWE-bench 日期分层、MLE-bench 混淆实验是"排除替代解释"的范本）；实验③（wording×position）学 OSWorld §5.2"observation variances"的写法：每个受控干预一个小结论式小标题 + 一张分桶图。

7. **污染/完整性处理要成节**（哪怕只有半页）：种子 case 与 LLM 训练数据重叠风险、judge 与被评模型同源的循环性、泄漏防护（BrowseComp canary string + "不公开测试样例"请求；GAIA holdout 300 题；MLE-bench 的混淆实验可作轻量替代）。另建议声明 benchmark 中危险动作在仿真环境"降级执行"、不放出真实危险 payload。

8. **评测协议细节按标杆写全**：指标定义（ASR 的精确定义：危险动作发生？完成？）、harness（agent 框架、模型版本、温度、步数/时长上限、token 预算）、成本锚点（总调用量/时长，AgentBench"≈MMLU 调用量"式的可比锚点）、seed 数与方差。Terminal-Bench 2.0 把 **cost 与成功率并列**展示值得抄。

9. **人类基线 + 难度校验**：报人类在"识别 gap→拒绝/求证"上的成功率（GAIA 92%、OSWorld 72.36% 先例），并做"人工预测难度 vs 实证难度"校验（Terminal-Bench 4.3）——这直接支撑"验证失败即危险"不是伪问题（人能做到）。case study 框给成功/失败轨迹对照 + common error 清单（OSWorld 5.4 六小块模板）。

10. **Limitations/伦理按"主题小节"写并前瞻维护性**：GAIA 式三小节（测量盲点：不评验证过程本身？judge 依赖；场景边界：benign/无攻击者的明确声明、不含对抗者不等于不含危险；多样性：域/语言覆盖）；NeurIPS/ICLR 的 Ethics + Reproducibility 声明单独成块；最后学 arXiv 2611.08417 加一段"持续验证/维护计划"（评测规范含资源预算、任务修订通道）——2026 年审稿人会认这个。

**可直接采用的章节骨架（草案）**
```
1  Introduction（Figure 1 = gap 概念 + 危险/安全 case 对）
2  Related Work（agent 安全评测 / agent benchmark / 规则与需求遵循 三段式）
3  Context-Environment Gaps: Task Definition（POMDP + gap 三分类定义 + ASR/验证行为定义）
4  Benchmark Construction
   4.1 Seed Cases and Batch Expansion   4.2 Controlled Safe Pairs
   4.3 Evidence Annotation & Quality Control   4.4 Data Statistics   4.5 Human Performance
5  Evaluation Protocol（harness、指标、judge+人工归因协议、成本、seeds）
6  Experiments
   6.1 RQ1 安全增强方法有效性（2 防御 + 1 预训练增强）
   6.2 RQ2 Agent 拓扑结构（3 拓扑 + 预算匹配对照）
   6.3 RQ3 受控干预：wording × position 的失败归因
7  Analysis（失败 taxonomy 分布、案例框、可靠性 pass^k、难度/类型分桶）
8  Discussion & Limitations   9  Ethics & Reproducibility Statements
附录（case 全景、judge prompts、标注协议、完整结果、LLM usage 声明）
```

---

## 十一、引用链接

- GAIA（ICLR 2024）：https://arxiv.org/abs/2311.12983 ；HTML: https://ar5iv.labs.arxiv.org/html/2311.12983
- AgentBench（ICLR 2024）：https://arxiv.org/abs/2308.03688 ；HTML: https://arxiv.org/html/2308.03688v3
- SWE-bench（ICLR 2024 oral）：https://arxiv.org/abs/2310.06770 ；HTML: https://arxiv.org/html/2310.06770
- OSWorld（NeurIPS 2024）：https://arxiv.org/abs/2404.07972 ；HTML: https://arxiv.org/html/2404.07972
- τ-bench：https://arxiv.org/abs/2406.12045 ；HTML: https://arxiv.org/html/2406.12045
- MLE-bench（ICLR 2025）：https://arxiv.org/abs/2410.07095 ；HTML: https://arxiv.org/html/2410.07095
- BrowseComp：https://arxiv.org/abs/2504.12516 ；HTML: https://arxiv.org/html/2504.12516
- Terminal-Bench 2.0（2026）：https://arxiv.org/abs/2601.11868
- Benchmarks as Software（2026）：https://arxiv.org/abs/2611.08417

> 备注：τ-bench 的正式发表 venue 建议投稿前在 OpenReview 核实（本报告抓取到的 arXiv 页无 venue 注记）；SABER（ICLR 2026 投稿，https://openreview.net/forum?id=JuwuBUnoJk ）报告 τ-bench 存在标注错误与欠规范任务并发布 τ-Bench Verified——"任务欠规范（underspecification）"作为 benchmark 缺陷已被社区点名，我们论文的 requirement underspecification 主题恰好可引用此现象作为动机。
