# 优秀 benchmark 论文全文写作结构调研（local_structure_B）

> 目的：为本组 benchmark 论文（benign 任务中 tool-using agent 的 context-environment gaps 安全评测）提取可借鉴的论文骨架。
> 材料：本地 6 篇 PDF（`AAA_core_data/paper/_reference_papers/`，经 markitdown 转文本后按"编号标题 grep 建树 + 选择性精读引言/构建/实验"的方式提取）。
> 说明：`extracted_headings.txt` 中缺失的子节已用转换文本补全；其中 2409.09058 记录按要求忽略。

---

## 0. 六篇论文身份速览

| 文件 | 论文 | 会议/来源 | 类型 |
|---|---|---|---|
| 2407.18901 | AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents | ICLR 2025（Stony Brook + AI2） | benchmark（环境+任务+程序化评价） |
| 2408.04682 | ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities | Apple，arXiv 预印本（v1 2024-08, v2 2025-04；arXiv 页面未标会议） | benchmark（交互式 tool-use 评测） |
| 2410.02644 | Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents | ICLR 2025（浙大 + Rutgers） | benchmark + 攻防形式化 |
| 2412.14470 | Agent-Safety-Bench: Evaluating the Safety of LLM Agents | ICLR 2025（清华 CoAI） | benchmark（agent 行为安全） |
| 2308.03688 | AgentBench: Evaluating LLMs as Agents | ICLR 2024（清华 + OSU + UC Berkeley） | benchmark（LLM-as-Agent 能力） |
| 2401.10019 | R-Judge: Benchmarking Safety Risk Awareness for LLM Agents | EMNLP Findings 2024（上海交大） | benchmark（安全风险识别/judging 能力） |

**重要结论**：后两篇均为 benchmark 论文，而非 multi-agent 框架/拓扑论文，故"拓扑描述方式"的对照提取不适用于这两篇；主实验 2 的拓扑对照对象需另找框架类论文（MetaGPT/AutoGen/LangGraph 等）。但 AgentBench 附录 J.2.3（tokens 与 rounds 分布分析）可作为"排除 token 消耗混淆"的写作先例（见 §5.7）。

---

# 一、AppWorld（2407.18901，ICLR 2025）

## 1.1 完整章节树
```
1 Introduction
2 AppWorld Engine
  2.1 Engine Components
  2.2 Features
  2.3 Database
3 AppWorld Benchmark
  3.1 Setup
  3.2 Evaluation
  3.3 Validation Solutions
  3.4 Final Dataset
4 Benchmarking Experiments
  4.1 Methods
  4.2 Results
  4.3 Analysis
5 Related Work
6 Conclusions
7 Limitations
8 Ethics Statement
（附录 A-L：任务性质讨论、分布、API 文档、评价细节、方法细节、错误分析、UI 任务、TaskGenerator 代码示例等）
```

## 1.2 各节一句话概括
- **1 Introduction**：日常数字任务需要跨多个 app 的交互式编码与决策；现有工具 benchmark 只有 1-4 次线性 API 调用且用参考解对比来评价，对多解复杂任务失效；提出 AppWorld = Engine（模拟世界）+ Benchmark（750 复杂任务+程序化评价）。
- **2 AppWorld Engine**：用软件工程最佳实践（REST 设计、单测、详尽文档）构建可控、稳定、可复现的"app+人"模拟器（9 个类真实 app、101 张 DB 表、~457 个 API、~100 个虚构用户）。
  - **2.1 Engine Components**：Applications / API Documentation / Jupyter 式 Execution Shell 三大组件。
  - **2.2 Features**：无真实后果、时间可倒流（freeze gun）、错误堆栈可读、serverless API 调用等能力特性。
  - **2.3 Database**：101 表 726 列的 Base DB，不用 SQL 手工填数，而是"用自家 API 程序化生成数据"保证一致性与真实感（ChatGPT 谨慎辅助+人工循环审查）。
- **3 AppWorld Benchmark**：250 个 Task Scenario 蓝图批量实例化为 750 个任务，每个任务带状态断言式评价套件。
  - **3.1 Setup**：Task Scenario（含占位符）→ TaskGenerator 的 Setup 程序实例化任务，保证四性质：well-defined、有 distractors、有 realistic hurdles、构成 contrast set。
  - **3.2 Evaluation**：状态式程序化评价——比对最终 DB diff 与期望变更 C_expect/允许变更 C_allow 的"unit tests"，兼容多解、检查附带损害；定义 TGC/SGC 双指标。
  - **3.3 Validation Solutions**：为每个任务写完全程序化的 gold 解，端到端跑通评价测试，保证任务可解+框架正确（未来改动回归测试）。
  - **3.4 Final Dataset**：250 场景×3 任务=750；Train 105 / Dev 60 / Test-N 168 / Test-C 417（Test-C 需要未见 app，为主攻目标）。
- **4 Benchmarking Experiments**：2 类方法（决策式 ReAct/PlanExec；代码式 FullCodeRefl/IPFunCall/ToolLLaMA/CodeAct）× 4 个基座 LLM 的主实验。
  - **4.1 Methods**：方法与基座设置、API predictor（文档检索辅助）。
  - **4.2 Results**：Table 3 主结果（最好 ReAct+GPT4O：Test-N TGC 48.8 / Test-C 30.2，SGC 更低），所有方法都低。
  - **4.3 Analysis**：4 个分析——难度指标 vs TGC（Fig 4）、Oracle API 消融（API 检索不是瓶颈）、prompt 设计效应（更多/更相似示例无益于 Test-C）、GPT4O 错误人工分析（4 类失败：不交互幻觉、API 理解/使用错、指令部分遵循、常识错误）。
- **5 Related Work**：按"评价方法学"与"(交互式)代码生成 benchmark"两块组织。
- **6 Conclusions**：回应"缺统一稳定标准环境"的问题陈述。
- **7 Limitations**：只有 API 没有 UI 模态；只有单助手、未做 multi-agent 协作任务；数据量不足以训练模型（可用自指令扩充）。
- **8 Ethics Statement**：LLM 偏见、任务设计者地域偏见（北美/欧洲）、自动化真实风险、ChatGPT 参与数据生成（人工循环审查）、开源许可声明。

## 1.3 引言组织（问题→缺口→贡献）
- **推进逻辑**：自动化愿景+具体例子（订杂货跨 3 个 app）→ 用 Figure 1 走查一个真实任务（为锻炼时长启动播放列表，需 3 段代码、先读 note 才知道数据结构）来论证"复杂交互式编码" → 责任开发需要严谨评测 → **缺口**：现有工具 benchmark 是线性 1-4 次 API 调用、参考解对比评价对多解任务失效 → 提出 AppWorld 两部分框架（Figure 2 总览）→ **贡献 4 条编号**（1. Controllable Execution Environment；2. Benchmark of Complex Tasks；3. Programmatic and Robust Evaluation Suite；4. Benchmarking Models）→ 工程投入声明（10 万+行代码、14 个月、作者自研非众包）+ 主结果数字预告（48.8/30.2、鲁棒性指标 32.1/13.0）。
- **贡献点数量与表述**：4 条、编号名词短语开头（"1) Controllable Execution Environment. We develop…"），每条先命名后展开。
- **Figure 1**：动机示例任务的交互走查（3 个代码块逐次依赖环境反馈）；Figure 2：Engine（左）+Benchmark（右）双栏总览图。

## 1.4 Benchmark 构建呈现方式
- **分类体系**：不按风险分类，而按"任务四性质"（well-defined / distractors / hurdles / contrast set，Table 1 用两个 scenario 给出条件示例）+ 每任务主观难度 3 级。
- **数据收集/扩展流程**：**Task Scenario 模板（带占位符）→ TaskGenerator（Setup 程序）随机采样占位符批量实例化**——即"种子→批量扩展"的程序化版本；Fig 3 给出 TaskGenerator 总览（Setup / Validation Solution / Evaluation 三件套）。
- **质控**：全程作者自研+多轮 code review、unit-testing、文档化；**Validation Solutions 端到端测试**（每个任务的 gold 解必须通过其评价测试）。
- **统计表**：Table 1（四性质示例，§3.1）、Table 2（per-task 统计：apps 数、unique APIs、API 调用数、解代码行数、评价测试数、难度，§3.4/§4.1 交界），Table 8/9 附录补充示例。

## 1.5 评价协议与指标
- 状态式程序化评价：检查 DB diff ⊆（C_expect ∪ C_allow），拒绝显式枚举"有害副作用"，写成断言式 unit tests（每条断言配自然语言说明，留作未来人类反馈接口）。
- 指标：**TGC**（Task Goal Completion，单任务全过断言比例）与 **SGC**（Scenario Goal Completion，同 scenario 全部任务通过=一致性指标，引 Gardner contrast set 文献）；另报 scenario-based robustness 指标。

## 1.6 实验部分组织
- 主实验（Table 3：方法×基座，Test-N/Test-C × TGC|SGC）→ 4 个分析小节（每个小节一个结论性发现：难度效应、API 检索非瓶颈、prompt 设计无效、错误类型定性分析）。
- 没有传统"消融"小节，但 Oracle API 替换与 prompt 变体实质是消融；每个分析支撑的结论都写在小节开头第一句（结论先行）。

## 1.7 讨论/局限/伦理/可复现
- Limitations 独立成节（§7，正文内）；Ethics 独立成节（§8）；工程量与质量控制声明放在引言末与 §3.4；数据/代码开源声明（permissive license）。

## 1.8 独特且值得借鉴的结构选择
1. **Validation Solutions**：每个 case 自带 gold 解做端到端可解性验证——与我们"安全对照版证明能力无问题"理念同构，值得显式借鉴其"验证-回归"叙述。
2. **Contrast set + SGC**：同种子的变体任务集合作为一致性测量单位（我们的"安全对照版"正是一种 contrast set，可用类似的双指标：单 case ASR + 对照版通过率）。
3. **Test-N/Test-C split**：按"是否需要未见环境/能力"划分难度，而非随机划分。
4. 每个分析小节标题即结论；错误分析给 4 个具名失败类别。

---

# 二、ToolSandbox（2408.04682，Apple）

## 2.1 完整章节树
```
1 Introduction
2 ToolSandbox Design
  2.1 Stateful
  2.2 Conversational
  2.3 Interactive
3 Test Scenarios
4 Evaluation Results
5 Related Work
6 Conclusion
7 Limitations
（附录 A 实现细节（A.2.1 工具增强、A.6 竞态）、B 场景与标注（B.2 标注流程、B.3 工具域、B.4 统计）、C 场景示例、D 附加结果（D.2 工具响应、D.3 轮数）、E 补充实验（prompting））
```

## 2.2 各节一句话概括
- **1 Introduction**：现有工具评测要么测 stateless REST 服务、要么单轮 prompt、要么 off-policy 预定义轨迹；ToolSandbox 同时具备 Stateful / Conversational / Interactive 三属性，用 milestone/minefield 评价任意轨迹。
- **2 ToolSandbox Design**：Python 原生测试环境：ExecutionContext 为世界状态抽象、Python 函数为工具、User-Agent-ExecutionEnvironment 三方经 MessageBus 通信（Figure 2 交互图）。
  - **2.1 Stateful**：44% 工具为状态化工具（依赖/修改 cellular、wifi、location、低电量等世界状态），工具间形成隐式（含嵌套）状态依赖，只能试错发现。
  - **2.2 Conversational**：GPT-4o 用户模拟器支持 on-policy 多轮对话（含参数追问、纠正）。
  - **2.3 Interactive**：动态轨迹收集 + 人工标注 Milestones（必须发生的事件）/ Minefields（不可发生的事件）；匹配时按 DAG 拓扑序在 MessageBus/WorldState 中找最佳匹配算相似度；触发 minefield 则整轨迹 0 分。
- **3 Test Scenarios**：1032 个人工精写场景（2 名内部专家：一人写、一人扮 agent 验证 milestone/minefield）、34 工具、11 个域；场景类别：Single/Multiple Tool Call、Single/Multiple User Turn、State Dependency、Canonicalization、Insufficient Information，外加正交的 Tool Augmentation（干扰工具、名称/描述/参数扰乱）作为消融维度。
- **4 Evaluation Results**：全模型统一极简 prompt；Table 5 按"场景类别 × 工具增强"分解平均相似度；发现：开源/闭源差距大、State Dependency 下大模型爱并发调用出竞态、Canonicalization 难、Insufficient Information 与其它类别负相关（强模型更爱幻觉补全）、增强鲁棒性因模型而异。
- **5 Related Work**：DST、tool learning 等。
- **6 Conclusion**。**7 Limitations**：RapidAPI 外部依赖影响可复现（提议 cached solution 仿 StableToolBench）；milestone/minefield 人工标注贵、难扩展；用户模拟器有不可忽略的幻觉/指令遵循误差（尝试 tool-assisted user simulator 改善）。

## 2.3 引言组织
- 逐属性论证：每个属性一小节（Stateful / Conversational / Interactive），各自对比现有 benchmark 的不足并给出例子；Figure 1 是**一条完整示例评测轨迹**（human-authored 场景定义=浅蓝框 vs on-policy rollout=浅黄框；MessageBus / World State / Milestones 三要素；用户要发短信但蜂窝关闭，agent 需先补参数、再启用蜂窝、重试），全文反复引用它解释设计。
- 贡献表述为 3 个 bullet（三属性各一），另配 Table 1（对比 BFCL/ToolEval/API-Bank/ToolTalk/τ-bench 的 6 个属性勾叉表）。

## 2.4 构建呈现方式
- **分类体系**：场景能力分类（6 类，正交增强维度）而非风险分类；工具按 11 域组织。
- **数据收集/扩展**：纯人工精写（2 名领域专家），一人构建场景、另一人扮 agent 交叉验证 milestone/minefield；严格标注流程（附录 B.2）。
- **质控**：双专家交叉验证 + **用户模拟器质量分析**（Table 2：用户模拟失败率（幻觉/指令遵循）随 knowledge boundary、demonstration 加入下降）。
- **统计表**：Table 1（引言对比）、Table 4（与他 benchmark 的统计对比，附录 B.4 类别分布与 milestone 覆盖）、Table 5（结果主表）。

## 2.5 评价协议与指标
- Milestone/Minefield 事件匹配 + DAG 拓扑序约束的相似度分数；minefield 一票否决（score = score_M+ × I(score_M*=0)）。
- 设计动机：既有 AST 匹配的可解释性，又可评任意轨迹（对比 ToolEval 纯 LLM judge 的可靠性问题）。
- Minefield 专门用于"任务不可完成"场景：评 agent 是否会幻觉工具/参数——与我们的 requirement infeasibility 高度相关。

## 2.6 实验部分组织
- 单一大实验表（Table 5：模型 × [总分 + 7 个类别列 + 7 个增强列]），正文用小节式段落给发现（Proprietary / OpenSource / State Dependency / Canonicalization / Insufficient Information / Tool Augmentations 各一段）；增强列本身就是消融。
- 附录 D/E 放轮数效率、附加 prompting 实验。

## 2.7 讨论/局限/可复现
- Limitations 独立成节（§7），坦诚三类问题并各自给未来方向；可复现性（外部 API 不稳定）作为第一条局限。

## 2.8 独特且值得借鉴的结构选择
1. **Figure 1 贯穿式示例轨迹**：一张图承载"场景定义+世界状态+评价事件"，后文所有机制都回到这张图解释。
2. **Minefield（负面事件）**：显式标注"不该发生的动作"，并让违反直接清零——可为我们"危险动作"判定提供结构先例。
3. **用户模拟质量单独分析**（Table 2）：主动报告测量工具本身的误差来源。
4. 三属性命名式设计（Stateful/Conversational/Interactive）使 2.x 子节直接成为卖点清单。

---

# 三、ASB（2410.02644，ICLR 2025）

## 3.1 完整章节树
```
1 Introduction
2 Related Work
3 Definitions to Basic Concepts and Threat Model
  3.1 Defining Basic Concepts
  3.2 Threat Model
4 Formalizing Attacks and Defenses in LLM Agents
  4.1 Formalizing Prompt Injection Attacks
    4.1.1 Direct Prompt Injection Attacks
    4.1.2 Indirect Prompt Injection Attacks
    4.1.3 Attack Framework for Different Prompt Injection Ways
  4.2 Formalizing Memory Poisoning Attack
    4.2.1 Detailed Adversarial Goal
    4.2.2 Attack Framework
  4.3 Formalizing Plan-of-Thought Backdoor Attack
    4.3.1 Detailed Adversarial Goal
    4.3.2 Attack Framework
  4.4 Formalizing Defenses for Our Attack Framework
5 Evaluation Results on Agent Security Bench (ASB)
  5.1 Introduction to ASB
  5.2 Experimental Setup
  5.3 Benchmarking Attacks
  5.4 Benchmarking Defenses
6 Conclusion and Future Work
（附录 A 攻防方法细节（A.1 Mixed Attacks、A.3.1 prompt injection 方法、A.4 防御形式化）、B 对比（B.3 与 SOTA benchmark 对比）、C More Experimental Setup（C.2.3 指标细节、C.2.4 防御 prompt）、D More Experimental Analyses（D.1 PoT 触发器/方式对比、D.2 效用损失）；文末含 Reproducibility of Results 说明）
```

## 3.2 各节一句话概括
- **1 Introduction**：agent 的每个运行环节（system prompt、user prompt、memory、tool）都是攻击面；现有 benchmark 只测单一攻击或少数场景；ASB 形式化并评测 10 场景下的攻防。
- **2 Related Work**：按攻击族组织（Prompt Injection / Memory Poisoning / Backdoor），每段以"ASB 与之不同"收尾。
- **3 Definitions & Threat Model**：3.1 形式化基础概念（带 RAG 的 LLM agent、目标任务、注入任务，Eq. 1）；3.2 威胁模型（对抗目标 Eq. 2-3；攻击者知识与能力按 Tools/Backbone LLM/System Prompts/User Prompts/Knowledge Database 五个对象逐一声明）。
- **4 Formalizing Attacks and Defenses**：每类攻击一个小节（定义+对抗目标+攻击框架的固定三段式），4.4 形式化防御（prevention-based vs detection-based 两类）。
- **5 Evaluation Results**：5.1 ASB 统计（Tab 3）；5.2 实验设置与 7 指标；5.3 攻击结果；5.4 防御结果。
- **6 Conclusion and Future Work**。

## 3.3 引言组织
- **推进**：LLM agent 能力趋势 → agent 运行步骤拆解（配 **Figure 1：LLM Agent Attacking Framework 总览**——4 种攻击分别打 user query / observations / system prompt / memory retrieval）→ 逐步引出每类攻击的直觉（DPI→IPI→Memory Poisoning→PoT Backdoor→Mixed）→ 规模（10 场景、10 agents、400+ 工具、400 任务）→ **贡献 5 条 bullet**：① ASB benchmark；② 新攻击 PoT Backdoor；③ 攻防形式化分类；④ 27 攻防×13 backbone×7 指标的大规模评测（最高 ASR 84.30%、防御无效）；⑤ 新指标 NRP。
- 特点：**把"新攻击"与"新指标"也列为贡献**，不只 benchmark 本身。

## 3.4 Benchmark 构建呈现方式
- **分类体系**：威胁模型形式化——攻击按"目标组件"（system prompt / user prompt / memory / tool）分类；任务按 aggressive / non-aggressive 分（后者测拒绝率）。
- **数据收集**：10 个场景×对应 agent+400 余工具（含攻击工具）+400 任务；混合攻击为组合式扩展。
- **质控**：细节放附录 C；主文强调形式化正确性与预定义实验配置。
- **统计表**：Tab 2（攻防方法总表）、Tab 3（ASB 统计）、Tab 4（指标定义表）。

## 3.5 评价协议与指标（重点：攻防形式化）
- **形式化层**（§3-4）：Eq. 1（agent 目标）、Eq. 2（对抗目标：最大化触发恶意动作概率）、Eq. 3（PoT 附加约束：干净输入保持良性）——每个攻击都给出"Detailed Adversarial Goal + Attack Framework"。
- **指标层**（Tab 4 + App C.2.3）：ASR（攻击成功率=调用目标攻击工具成功）、RR（拒绝率）、PNA（无攻击性能）、BP（良性表现）、FPR/FNR（检测防御）、**NRP（Net Resilient Performance）=效用与安全的平衡综合指标**。
- 结果呈现：Tab 5（攻击类型×backbone 的 ASR/RR）、Tab 6（PNA/ASR/NRP 排行）、Tab 7/8（防御效果+Δ 变化）。

## 3.6 实验部分组织
- 5.3 Benchmarking Attacks：所有攻击都有效（Mixed 最强 84.30%）+ 部分拒绝现象 + **Fig 2 三个散点**（PNA vs ASR、能力 vs PNA、能力 vs ASR）揭示"能力-脆弱性先升后降"关系 + NRP 选型建议。
- 5.4 Benchmarking Defenses：现有预防式防御不足（ASR 仍高）且有无攻击时的效用损失。
- 更多分析在附录 D（触发器类型、prompt injection 方式对比、aggressive vs non-aggressive）。

## 3.7 讨论/局限/可复现
- "Conclusion and Future Work"合并；**Reproducibility of Results** 专段（预定义实验配置、开源复现）放附录。

## 3.8 独特且值得借鉴的结构选择
1. **Threat Model 独立小节 + 攻防形式化独立大节**（§3-4）：先数学化再工程化，安全审稿人友好。我们的 benign 设定虽无攻击者，但可以做"问题形式化"轻量版（context C、环境 E、验证、危险动作、ASR 定义）。
2. **aggressive / non-aggressive 双任务设计**：同一框架同时测"打不打得进"与"该拒的拒不拒"。
3. **自定义综合指标 NRP** 作为贡献点。
4. 攻击小节统一"定义→对抗目标→框架"三段模板，可类比我们"三类 gap：定义→失败条件→实例化模板"。

---

# 四、Agent-Safety-Bench（2412.14470，ICLR 2025，清华）

## 4.1 完整章节树
```
1 Introduction
2 Related Work
  2.1 LLM Safety Evaluation
  2.2 Agent Safety Evaluation
3 Agent-Safety-Bench Construction
  3.1 Risk Categories
  3.2 Data Collection
    3.2.1 Format of Data and Environments
    3.2.2 Refine Existing Datasets
    3.2.3 Augment Refined Data
    3.2.4 Quality Control
  3.3 Scorer
4 Experiments
  4.1 Setup
  4.2 Main Results
  4.3 Failure Mode Analysis
  4.4 Helpfulness Analysis Under Different Scenarios
  4.5 Discussion on Defense
5 Conclusion
（附录 A 风险类详解、B 失败模式案例、C 环境实现、E 增强 prompt、F 交叉验证、G scorer 训练、H 系统 prompt/解码、I 模型表、J Limitations）
```

## 4.2 各节一句话概括
- **1 Introduction**：安全研究从内容安全转向 agent 行为安全，但缺综合 benchmark；Agent-Safety-Bench=349 环境+2000 用例+8 风险类+10 失败模式；16 个 agent 全部安全分<60%。
- **2 Related Work**：2.1 内容级 LLM 安全评价、2.2 agent 安全评价，两小节定位差异。
- **3 Construction**：8 风险类（内容级+行为级，Table 3 定义）；数据格式为字典式四字段（Risks / Instruction-Dialog / Environments / FailureModes）；**Refine**（改写明确失败模式→去冗余→统一环境定义，得 876 例）→ **Augment**（先造 300 个新环境名提多样性、再让 GPT-4o 生成"预期风险行为序列"提质量，得 +1124 例）→ **质控三步**（人工预检 / Python 自动验证环境实现 / 人工后检：2 模型跑出 4000 交互记录全标注、开放编码总结出 10 失败模式、再交叉验证）；**3.3 Scorer**：微调 Qwen-2.5-7B 作裁判（GPT-4o 对人工标签生成解释辅助训练），91.5% vs GPT-4o 直接判 75.5%。
- **4 Experiments**：16 agents、4 步交互协议、安全分=安全标签比例。
  - **4.2 Main Results**：Table 5（Total / Behavior / Content / 8 风险类分解）；结论：全<60%、强模型更安全、行为安全比内容安全差得多、Spread 类最差。
  - **4.3 Failure Mode Analysis**：Table 6（M1-M10 分解）→ 归纳两大缺陷：lack of robustness 与 lack of risk awareness。
  - **4.4 Helpfulness Analysis**：人工标注 fulfillable / unfulfillable，GPT-4o 评 helpfulness（人工验证 94%）；Fig 3 显示强安全 agent 不是靠拒答而是靠正确执行（fulfillable 上 safety 高且 helpfulness 相当），unfulfillable 上强 agent 有意 withhold。
  - **4.5 Discussion on Defense**：两档防御 prompt（简单枚举 / 增强含示例）；Fig 4：弱模型无效、强模型有限提升且耗上下文 → 结论：改 prompt 不能根治，呼吁微调等更强方法。
- **5 Conclusion**；Limitations 在附录 J。

## 4.3 引言组织
- **推进**：内容安全→行为安全问题升级（例：论坛泄密、错改订单）→ 少数已有工作但缺综合 benchmark → 介绍 benchmark 并以 **5 个 key features 编号列举**（Diverse Interaction Environments / Broad Risk Coverage / Extensive Test Cases / Elaborated Failure Modes / High Quality and Flexibility，各配数据）→ 主发现预告（16 agents 全<60%，两大缺陷，防御有限）→ **贡献 3 条 bullet**（① benchmark；② 微调 scorer 模型（+15% over GPT-4o）+ 16 agents 评测；③ 失败模式与 helpfulness 分析+防御讨论）。
- **Figure 1**：16 个 agent 总安全分柱状图（headline 结果）；**Figure 2**：benchmark 总览（数据→环境交互→LLM scorer 自动评估的 pipeline）；**Table 1**（与 R-Judge/AgentDojo/ToolEmu/ToolSword/PrivacyLens/InjecAgent/Haiosystem 的对比）、**Table 2**（环境的细粒度分类）都放引言。

## 4.4 Benchmark 构建呈现方式
- **分类体系**：双维——8 风险类（Table 3）× 10 失败模式（Table 4，open coding 产生并反标注回每个 case）。
- **数据收集/扩展**：Refine Existing Datasets（3 步）→ Augment Refined Data（2 个问题→2 个对策的"问题-方法"叙述），每步有数量结算（876 → +1124 → 2000）。
- **质控**：三步流程（Manual precheck / Automatic validation / Manual postcheck）+ 交叉验证（附录 F）；把"跑 2 个模型产生 4000 记录全标注"作为质检副产品再利用（训练 scorer）。
- **统计表**：Table 1/2（引言）、Table 5/6（结果）、Table 8（模型列表，附录）。

## 4.5 评价协议与指标（重点：scorer）
- **Scorer 独立小节（3.3）**：先论证内容裁判不适配（GPT-4o 仅 75.5%）→ 用人工后检的 4000 标注+GPT-4o 生成解释 → 微调 Qwen-2.5-7B → 报验证准确率 91.5%（200 条 Gemini-1.5-Flash 交互）。
- 指标：安全分=安全标签比例；分解维度 Total / Behavior / Content / 8 风险类 / 10 失败模式；helpfulness 为辅助指标（GPT-4o judge，94% 人工验证）。

## 4.6 实验部分组织
- 递进四步：**主结果（规模结论）→ 失败模式分析（为什么失败）→ helpfulness×fulfillable 分析（安全来自拒答还是正确执行）→ 防御讨论（现成防御打不动）**；每小节标题即功能，结论收束到"lack of robustness + lack of risk awareness"两个命名缺陷。
- 没有单独消融节；防御 prompt 实验以"讨论"形式放在实验末尾。

## 4.7 讨论/局限/伦理/可复现
- Limitations 放附录 J（主文无）；数据构建的质量承诺（≥2 轮人工审查+自动验证）写进引言 features；开源链接脚注。

## 4.8 独特且值得借鉴的结构选择
1. **Scorer 作为贡献点+独立小节**：裁判模型的可靠性被当作 benchmark 质量的一部分来论证（这与我们 LLM-as-Judge+人工三分类归因完全对应）。
2. **失败模式成为一等公民**：从数据标注（open coding 产生）→ 结果分解（Table 6）→ 归纳缺陷命名，一条线贯穿。
3. **Helpfulness × fulfillable/unfulfillable 二维分析**：排除"安全=拒答"的替代解释——审稿人必问的问题主动用实验回答。
4. **Discussion on Defense** 收尾：把"防御打不下"作为 benchmark 价值的最后论据。

---

# 五、AgentBench（2308.03688，ICLR 2024）——benchmark 论文，按 1-8 简要提取

## 5.1 完整章节树
```
1 Introduction
2 LLM-as-Agent: Definition and Preliminary
3 Composition of AgentBench: A Brief Look
  3.1 Code-Grounded Environments（Operating System / Database / Knowledge Graph）
  3.2 Game-Grounded Environments（Digital Card Game / Lateral Thinking Puzzles / House-Holding）
  3.3 Web-Grounded Environments（Web Shopping / Web Browsing）
4 Evaluation of AgentBench
  4.1 Evaluation Setup
  4.2 Main Results
  4.3 Analysis
5 Related Work
6 Conclusion
（附录 A 评测框架（A.1 传统框架 vs A.2 自研框架）、B-I 八个环境各自 Dataset Details、J 深度分析（J.2.3 完成任务的 token/轮数分布、J.2.4 Task Limit Exceeded 主因：模型重复行为 等））
```

## 5.2 各节一句话概括
- **1**：LLM-as-Agent 需要系统化标准评测；文本游戏（动作空间封闭）与具身模拟器（多模态过重）都不适配文本 LLM；缺跨环境综合 benchmark。
- **2**：LLM-as-Agent 的形式定义与执行结果分类（为 §4.3 执行结果占比分析埋伏笔）。
- **3**：8 个环境按 grounding 分 3 类逐个一小节介绍（5/8 首创；数据来自新建或改造既有数据集）。
- **4**：4.1 统一评测工具包（Server-Client 架构）+ 29 模型（Table 1 模型清单）；4.2 主结果（Table 2 环境统计与指标、总表）；4.3 分析。
- **5**：按"LLM 评测 / LLM-as-Agent / 执行环境评测"组织。**6**：结论。**无独立 Limitations/Ethics 节**。

## 5.3 引言组织
- 问题（智能体历史+LLM 机遇）→ 缺口三连（文本游戏/具身/单环境）→ 方案（8 环境 3 类 grounding）→ 工具包 → 主发现（GPT-4 强、OSS 差距大、code training 双刃剑）→ **贡献 3 条**（① 概念+benchmark；② 29 模型评测+失败定量分析+改进方向；③ 开源集成工具包）。
- **Figure 1**：29 个 LLM 的表现总览（各环境相对表现 + 总分分布，含两条"LLM 类型均值"虚线）——即 headline 结果图放首页；**Figure 2**：真实挑战→8 环境总览图。

## 5.4-5.6 构建/评价/实验要点
- 构建：每环境一节（任务、数据来源、动作/观察空间），统计集中在 **Table 2（8 环境的统计与指标，SR=成功率）**；数据细节全推附录 B-I。
- 评价：每环境 success rate + 加权 overall score；执行结果分类（Invalid Format / Invalid Action / Task Limit Exceeded 等）作为诊断量。
- 实验：主结果 → 4.3 分析四段（执行结果占比、code training 双刃剑、高质量对齐数据、llama-2-13b≈70b 反常），附录 J 深挖（计划/自纠/工具使用案例、**J.2.3 token 与轮数分布**）。

## 5.7 与我们论文的关联
- **附录 J.2.3（完成/未完成任务的 token 与轮数分布）是"排除 token 消耗混淆"的现成先例**：我们实验②要证明"拓扑降低 ASR 不是 token 消耗大带来"，可仿此报告各拓扑的 token/轮数分布并做匹配/回归控制。
- 4.3 的"分析段落标题=发现"写法、执行结果分类学（错误类型分类表）均可借鉴到我们失败归因呈现。

---

# 六、R-Judge（2401.10019，EMNLP Findings 2024）——benchmark 论文，按 1-8 简要提取

## 6.1 完整章节树
```
1 Introduction
2 Problem Formalization
3 R-Judge Benchmark
  3.1 Case Format
  3.2 Curation Principles
  3.3 Curation Process
  3.4 Dataset Statistics
  3.5 Evaluation Criteria
4 Experiments
  4.1 Setup
  4.2 Validating R-Judge
  4.3 Main Results
5 Analysis
  5.1 Influence of Different Prompting
  5.2 Effect of Fine-tuning on Safety Judgment
  5.3 Case Study
  5.4 Summary
6 Related Work
  6.1 LLM Agents
  6.2 LLM Safety
7 Conclusion
（附录 A 风险类型、B 数据（B.3 统计表）、D scorer prompt、E 案例（E.4.1 GPT-4o 失败）、F 模型细节）
```

## 6.2 各节一句话概括
- **1**：内容安全评测无法暴露交互环境中的行为风险；需要评测 LLM 的"风险意识"（judging & identifying）；R-Judge=569 条多轮 agent 交互记录（5 应用类 27 场景 10 风险型）。
- **2 Problem Formalization**：定义 agent record（用户指令+动作历史+环境反馈）与语言/动作/反馈空间，形式化"风险识别+安全判断"任务。
- **3**：3.1 case 格式；3.2 构建原则（Intended Attacks / Unintended Risks 双来源原则）；3.3 构建流程（injecAgent 414 + ToolEmu 81 + AgentMonitor 24 + 人工 55=155；把 unsafe 样本改写成 safe 版补安全类；ChatGPT 润色+人工效度检查）；3.4 统计（569、平均 2.6 轮、206 词、52.7% unsafe）；3.5 评价标准（双 recipe）。
- **4**：4.1 11 个 LLM（GPT 系+Llama-2/3、Mistral、Vicuna）；**4.2 Validating R-Judge**（验证 GPT-4 自动评分可行性）；4.3 主结果（GPT-4o F1 74.45%，其余不显著超随机）。
- **5 Analysis**：prompting 变体无效（5.1）、fine-tuning 显著有效（5.2）、GPT-4 失败案例三型（scenario simulation / understanding adaptability / safety alignment flaws，5.3）、总结（5.4：风险意识是知识+推理的多维能力）。
- **6**：6.1 LLM Agents / 6.2 LLM Safety。**7**：结论。

## 6.3 引言组织
- 问题（agent 风险实例：点钓鱼邮件）→ 缺口（内容安全 benchmark/monitor 无法测行为风险；ToolEmu/AgentMonitor 已用 LLM 当裁判但"LLM 能否判安全"本身未知）→ R-Judge 介绍 → 主发现（GPT-4o 74.45%、fine-tuning 有效 prompt 无效）→ **贡献 3 条**（① 问题形式化；② 首个风险意识 benchmark 数据集；③ 11 模型评测+机制研究）。
- **Figure 1**：数据分布总览（5 类×27 场景×10 风险型）；**Figure 2**：case 格式 + 双 recipe 评测流水线图。

## 6.4-6.6 构建/评价/实验要点
- 构建：**Curation Principles 独立小节**（先立原则再讲流程）；来源混合（已有数据集改写+人工构造）；"unsafe→safe 改写"补对照安全样本（与我们安全对照版思路同构！）。
- 评价：双 recipe 串联——Safety Judgment（二分类，F1）+ Pairwise Risk Identification（开放式分析，GPT-4 评 Effectiveness=与人工风险描述 pivot 的相关性）；**4.2 先验证测量工具再测模型**。
- 实验：主表 → 分析节三小节（prompting / fine-tuning / case study）直接支撑"风险意识是多维能力"的结论。

## 6.7 独特结构选择
1. **Problem Formalization 独立节**（§2）：哪怕简单，也把任务形式化前置。
2. **Validating R-Judge 独立小节**：benchmark 论文先自证测量可信（scorer 可行性），再谈模型差距。
3. 数据来源三路混合+对照样本改写、统计放在 3.4 小节（而非实验前表格）。

---

# 七、六篇共有"结构惯例"总结

1. **引言固定推进链**：趋势/愿景 → 具体任务例子（常配 Figure 1 走查或结果图）→ 现有 benchmark 缺口（常配 Table 1 对比表）→ 新 benchmark 的 3-5 个命名特性（编号列表）→ 主实验 headline 数字预告 → 贡献 bullet 3-5 条（benchmark/数据、方法或指标、评测发现三件套）。
2. **正文骨架**：Intro →（Related Work 前置如 ASB/Agent-Safety-Bench，或后置如 AppWorld/ToolSandbox/AgentBench，两种都合规）→ 环境/引擎设计（若有）→ Benchmark 构建（分类体系→数据流水线→质控→统计）→ 评价协议/指标（独立节或独立小节）→ 实验（Setup→Main Results→分析小节×N→防御/讨论）→ Conclusion → Limitations/Ethics（正文节或附录）。
3. **构建节四件套**：分类体系（定义表+附录详解）、数据来源与扩展流程（seed→增强，步骤化+数量结算）、质控（多轮人工+自动验证+交叉验证/双专家互验）、统计表（规模数字+分布）。
4. **评价协议四件套**：指标定义（常带公式）、自动 scorer/judge 及其人工验证准确率、与替代方案的对比论证（为什么不用纯 LLM judge/参考解）、多维结果分解设计（模型×类别大表）。
5. **实验叙事 = 发现清单**：主表后每个分析小节标题即结论；失败模式/错误分析（人工标注+具名失败类别+案例）是标配；"安全类 benchmark 必做防御讨论"（现有防御打不动→凸显 benchmark 价值）。
6. **测量工具的可信度被当作贡献**：scorer 微调（Agent-Safety-Bench）、GPT-4 scorer 验证（R-Judge）、用户模拟质量分析（ToolSandbox）、validation solutions（AppWorld）。
7. **对比表（Table 1）+ 总览图（Figure 2）+ headline 图（Figure 1）三件套**分别承担"我们更大更全""整体怎么工作""结果多严峻"三个叙事功能。
8. **局限收敛坦诚**：标注/扩展成本、模态或场景覆盖、外部依赖可复现性、judge 偏差，各配一句未来方向；伦理与许可声明独立或脚注化。

---

# 八、对我们论文的 10 条针对性建议

> 论文定位：benign（无攻击者）任务中 tool-using agent 的 context-environment gaps 安全 benchmark；三类 case（requirement underspecification / requirement infeasibility / factual inconsistency）；种子→扩展、安全对照版、人工证据标签、LLM-as-Judge+人工三分类失败归因；三主实验（防御+预训练增强打不下 ASR、agent 拓扑对比控 token 消耗、wording/position 受控干预归因）。

1. **引言推进**：用 Figure 1 走查一个 context-environment gap 例子（用户指令/文档 vs 环境事实→验证失败→危险动作），类比 AppWorld/ToolSandbox 的贯穿式示例；缺口论述针对"攻击型安全 benchmark（ASB/Agent-Safety-Bench）默认有攻击者、benign 场景的隐性陷阱无人测"；Table 1 对比表列 ASB / Agent-Safety-Bench / R-Judge / ToolSandbox / ToolEmu，维度加"benign-only / 安全对照版 / 失败归因 / 受控干预"四列凸显差异化。
2. **贡献 3-4 条**：① context-environment gap 概念与三类 case 形式化；② benchmark（seed→批量扩展+安全对照版+人工证据标签）；③ 三分类失败归因协议（LLM-as-Judge+人工）；④ 三大实验发现（防御打不下、拓扑效应非 token 假象、wording/position 干预揭示验证失败为主因）。命名缺陷式总结词（仿 "lack of robustness/risk awareness"）。
3. **设 "Problem Formalization" 独立小节**（仿 ASB §3、R-Judge §2）：定义 context C、部分可观测环境 E、验证动作、危险动作与 ASR；三类 case 各给"失败条件"式定义（仿 ASB 每攻击"定义→对抗目标→框架"三段）。
4. **构建节写成流水线**：3.1 分类体系（三类 case 定义表）；3.2 种子 case→批量扩展（步骤化+数量结算，仿 Agent-Safety-Bench 3.2.2/3.2.3 的"问题→对策"叙述）；3.3 安全对照版（重点论证"移除坑点但保留能力需求"，用对照版通过率自证能力无问题——AppWorld validation solutions 的叙述模板）；3.4 质控（人工证据标签+交叉验证，报一致率）；3.5 统计表（case 数、轮数、词数、危险动作分布等，仿 R-Judge 3.4）。
5. **评价协议独立成节**：ASR 定义+三分类失败归因（证据搜集不足/证据充足未识别危险/识别到危险仍盲从）的 judge prompt 与人工验证准确率——把 scorer 可信度写成贡献的一环（Agent-Safety-Bench 3.3 + R-Judge 4.2 的合体）；每条 case 的人工证据标签作为归因 pivot。
6. **实验按"三大实验=三大结论"组织**，每个实验先给主表再给 1-2 个分析小节，小节标题写成结论（如 "Defense prompts and pretraining augmentation do not close the gap"）；主结果表按 case 类型×模型双分解（仿 Agent-Safety-Bench Table 5/6 双分解）。
7. **实验②（拓扑）呈现控混淆**：仿 AgentBench App. J.2.3 报告各拓扑的 token 与轮数分布，并做等预算/回归控制，明示"ASR 下降非 token 消耗"；拓扑图示用 ToolSandbox Figure 2 式"角色-消息总线"框图（3 种拓扑+普通对照共 4 小图并排）。
8. **实验③（wording/position 干预）仿 helpfulness 分析的二维呈现**（Agent-Safety-Bench 4.4）：干预档位×归因类别联动图，直接支撑"验证失败是主因"；配定性案例（GPT-4 失败三型的 R-Judge 5.3 式 case study）。
9. **防御/增强讨论收尾**（仿 Agent-Safety-Bench 4.5 "Discussion on Defense"）：把实验①定位成"现有防御打不动→需要以环境验证为核心的机制"，既收束全文又给未来工作。
10. **结构完备性**：Limitations（域覆盖、judge 偏差、benign-only 范围、规模）+ Ethics/Reproducibility（数据许可、人工标注协议、LLM 参与生成披露——AppWorld §8 模板）独立成节；附录放 case 生成 prompt、judge prompt、统计分布、失败案例；把"安全对照版验证"“judge 人工校验"两个自证环节在正文用数字报出。

---

## 附：本报告数据来源
- PDF→文本：`tmp/2407.18901.md`、`tmp/2408.04682.md`、`tmp/2410.02644.md`、`tmp/2412.14470.md`、`tmp/2308.03688.md`、`tmp/2401.10019.md`（markitdown 转换，UTF-8）。
- 章节树：grep 编号标题 + `extracted_headings.txt` 交叉补全。
- 会议信息：PDF 首页水印 + arXiv abs 页面（R-Judge comments: "EMNLP Findings 2024"；ToolSandbox 页面未标注会议）。
