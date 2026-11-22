# 2024–2026 顶级/主流会议 Agent 安全类 Benchmark 论文全文写作结构调研

> 调研日期：2026-11-17。方法：web 搜索定位论文 → 抓取 arXiv HTML 全文（arxiv.org/html/<id>，个别用 ar5iv/OpenReview）→ 提取完整章节树到子节粒度 + 各章节正文要点。
> 信息来源统一标注 arXiv 链接；venue 以 OpenReview / ACL Anthology 最终为准（个别待核处在文中注明）。
> 共分析 8 篇：AgentHarm（ICLR 2025）、τ²-bench（2025 Sierra）、R-Judge（ICLR 2024）、SafeAgentBench（EMNLP 2024 Findings）、Agent-SafetyBench（ICLR 2025）、Agent Security Bench（ICLR 2025）、InjecAgent（2024）、AgentAuditor（2025，含 2026 v3 更新）。

---

## 1. AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents

**发表处/年份**：ICLR 2025；arXiv:2410.09024（Gray Swan AI + UK AI Security Institute）。链接：https://arxiv.org/abs/2410.09024
**一句话定位**：首个测"显式恶意 agent 多步任务（direct prompting 攻击下）"的 benchmark，且评分内建"能力保持"检验，用于给 jailbreak 打分。

**完整章节树**（arXiv HTML v3）：
```
1 Introduction
2 Related work
3 Benchmark
  3.1 Overview of AgentHarm
    3.1.1 Behaviors
    3.1.2 Synthetic Tools
    3.1.3 Fine-Grained Grading Rubrics
    3.1.4 Cost
  3.2 Design Principles
4 Evaluation
  4.1 Settings
  4.2 Main Results
  4.3 Ablation Studies and Analysis
5 Discussion（含 Limitations + Conclusion）
Acknowledgements / References
Appendix B Additional Details（system prompt、refusal judge prompt 等）
Appendix C Additional Results（per-category 图、public/private 全表、工具调用统计）
Appendix D Additional Examples（D.1 harmful vs benign 示例；D.2 detailed vs open-ended；D.5 执行日志）
```

**每节一句话**：
- 1 Introduction：从"chatbot 单轮鲁棒性 ≠ agent 多轮鲁棒性"切入，给出 benchmark 特性与实证发现两组贡献。
- 2 Related work：对比 jailbreak/agent 能力/现有 misuse 数据集，指出现有数据无法评 agent 多步 misuse。
- 3 Benchmark：交代三大组件（behaviors、synthetic tools、grading rubrics）并用 3.2 Design Principles 显式论证设计取舍。
- 4 Evaluation：定义基础 agent 循环 + 两种攻击，给主结果图和多个消融。
- 5 Discussion：Limitations bullet + 结论。

**贡献点表述**：引言里贡献分**两组 bullet**——第一组 5 条讲 benchmark 性质（①广覆盖：110 唯一 + 330 增强行为、11 harm 类；②评分含能力维度并配 benign 对照集；③易用（集成 Inspect 框架）；④可靠评分（人写 rubric，LLM 只做窄子任务）；⑤防污染（30% 私有集永不暴露给公共 API））；第二组 3 条讲实证发现（无攻击也大量顺从；简单通用越狱模板迁移即奏效；越狱后 agent 保持多步一致性）。写法：每条 bullet 都是"性质 + 支撑数字/机制"一句话。

**Benchmark 构建呈现**：3.1.1 按 11 个 harm 类（Fraud/Cybercrime/Self-harm/Harassment/Sexual/Copyright/Drugs/Disinformation/Hate/Violence/Terrorism）× 每类 10 个手写 base behavior = 110，再做 4 种增强（detailed / open-ended × hint / no-hint）→ 440；每个 harmful 行为配**同主题 benign 改写版**（能力对照）；数据划分 10% val / 60% public test / 30% private test。3.1.2 合成工具：104 个无副作用函数（含自纠错反馈），LLM 只用来生成长文本返回内容。3.1.3 评分：人写细粒度 rubric（可给部分分），LLM judge 仅用于窄的语义子项；另有独立 refusal judge。统计表（Table 1）列：base 数、总数、split 大小、harm 类数、工具数、平均工具数/行为（3.53）、token 成本。3.1.4 Cost 专节报运行成本与耗时。3.2 Design Principles 是"设计决策辩护"专节：广度 vs 深度、能力退化检测、可用性、评分可靠性、防污染。

**评价协议**：指标 = **Harm score**（rubric 部分分）、**Refusal rate**（refusal judge 扫全部消息）、**non-refused harm score**（仅在未拒绝样本上计分，对照 benign 得分以证明越狱后能力未退化）。Judge = GPT-4o 只做窄子任务 + 拒绝判定。被测：OpenAI/Anthropic/Google/Mistral/Meta 16 个模型，基础 while-loop agent（temperature 0，最多 4096 token），攻击 = forced tool call + 通用越狱模板。

**实验组织**：4.2 主结果用**三联图**（harm score / refusal / non-refused harm vs benign）+ 附录精确数字表；4.3 消融：best-of-n（Table 2）、prompting（CoT/ReAct/拒绝提示，Table 3）、error analysis（人工看 GPT-3.5 vs GPT-4o 执行日志找失败模式）；附录另有 chat vs agent 拒绝率对比、per-category 分布。结论链：无攻击高 harm score → 越狱模板大幅抬升 → non-refused 分数≈benign 分数 ⇒ 越狱不损能力。

**局限与伦理**：5 Discussion 里 Limitations bullet 5 条（仅英文；单轮用户无跟进；评分可能漏掉合法替代执行轨迹；绑定自定义工具；只测基础 agent 能力非开放式自主能力）。伦理处理散落在 3.1.1（不放真实人名/地址、只做数字可实现行为、合成工具降低真实危害）+ 私有集防污染。

**独特且值得借鉴**：① benign 孪生数据集 + non-refused 计分（能力保持检验）；② Design Principles 专节把设计取舍当卖点写；③ 3.1.4 Cost 专节给预算敏感的审稿人；④ private holdout + canary 防污染；⑤ "LLM 只做窄子项评分"的可信 judge 策略。

---

## 2. τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment

**发表处/年份**：arXiv:2506.07982（2025-06，Sierra + U Toronto/Vector）。链接：https://arxiv.org/abs/2506.07982 （venue 待核，暂为 arXiv 2025）
**一句话定位**：把 τ-bench 从"单控"（只有 agent 有工具）扩展为"双控"（用户模拟器也带工具作用于共享世界，Dec-POMDP 形式化），分离推理失败与沟通/协调失败。

**完整章节树**：
```
1 Introduction
2 Related Work
  （三个无编号段落小标题：Benchmarks for Conversational AI Agents. / User Simulation for Conversational Agents. / Multi-Agent Benchmarks.）
3 τ2-bench: Evaluating Agents in a Dual-Control Environment
  3.1 The Dec-POMDP Formalism
  3.2 Domain and task creation
  3.3 Task evaluation
4 Experiments
  4.1 Agent settings
  4.2 Results
    Pass^k scores. / Ablation analysis. / Impact of policy document on performance. / Impact of number of actions and sub-tasks.
  4.3 How does dual-control impact benchmark reliability?
    User simulator quality evaluation. / Reliability of the user simulator.
5 Conclusion
Appendix A Telecom Domain（A.1 User Persona / A.2 Example Task / A.3–A.4 Example Trajectories）
Appendix B Verifying Original τ2-bench（B.1 Verifying Implementation / B.2 Verifying Tasks）
Appendix C Prompts（agent/user system prompt 模板、任务指令示例）
Appendix D Domain Policies（retail/airline/telecom 全文策略、troubleshooting workflow 图）
Appendix E User Simulator Quality（各域错误类型与失败模式、示例）
```

**每节一句话**：
- 1：单控 benchmark 测不了"引导用户动手"的真实场景；列 4 大贡献。
- 2：三段式 related work，按"对话 agent 基准 / 用户模拟 / 多智能体"组织。
- 3：Dec-POMDP 七元组形式化 → 三阶段域与任务构建 → 分类断言式任务判定。
- 4：模型与用户模拟器设置 → pass^k + 三组分析消融 → benchmark 可靠性（错误源分解 + 用户模拟器人工审计）。
- 5：结论。

**贡献点表述**：摘要与引言同构地列**编号 4 条**：①Telecom dual-control 域（Dec-POMDP 建模、双方各有工具、附 SOTA 掉点数字）；②组合式任务生成器（原子组件程序化生成、可验证、全覆盖、可控复杂度）；③可靠用户模拟器（工具+状态约束行为，报错误率数字对比 τ-bench）；④细粒度失败诊断（no-user vs dual-control 掉 ~20% pass^1）。每条都是"机制 + 数字证据"。

**Benchmark 构建呈现**：3.2 三阶段：Stage1 agent 数据库+工具（LLM 生成 PRD→实现→单测→人工修到全过）；Stage2 用户侧数据库+工具（mock 手机）；Stage3 程序化任务生成——原子子任务 = (init 函数集, sol 函数集, assert 函数集)，互斥子任务分组、每组至多取一拼成组合任务，**按构造保证正确性**。统计表（Table 1）按域列 agent DB / agent 工具 / 用户工具 / 任务数（telecom 114，全量 2285）。质量控制写在附录 B：迭代审查（跑仿真→修任务指令→查 **underspecification / overspecification / non-unique solutions**）+ 分类断言（environment assertions / communication assertions / natural language assertions / action assertions）。

**评价协议**：任务成功由**确定性/半确定性断言**判（DB check、status assertion、NL assertion、action matching，按任务选子集；telecom 只用断言函数）；指标 **pass^k**（k 次独立运行全过的比例，pass^1 为均值），每任务跑 4 次、temperature 0。被测：gpt-4.1-mini / gpt-4.1 / o4-mini / claude-3.7-sonnet，用户模拟器固定 gpt-4.1；成本公开（$0.086/$0.059 每任务，全域一轮 ~$40）。

**实验组织**：4.2 按分析目标分四块（pass^k 域间对比；Default/No-User/Oracle Plan 三模式消融——分离推理负荷 vs 沟通协调；policy 文档给不给的影响；动作数/子任务数→复杂度影响）；4.3 专节评"benchmark 本身可靠性"：先分解三类错误源（实现错误、任务规范错误、用户模拟器错误）逐一排除，再双人标注用户模拟器错误（critical vs benign 两级），报各域错误率（retail 40%/12% critical vs telecom 16%/6%）。

**局限与伦理**：无独立 Limitations 章；局限隐含在 4.3（模拟器保真度）与附录 B/E。伦理风险低（mock 环境、客服域）。

**独特且值得借鉴**：① **"benchmark 可靠性"作为一级小节（4.3）**，先证工具没问题再证发现；② 三模式对照（Default/No-User/Oracle Plan）做因果分解——与我们"拓扑对照排除 token 消耗混淆"同构；③ 断言分类学（env/communication/NL/action）；④ 任务审查清单（under/over-specification、非唯一解）直接可搬去我们的 requirement underspecification 质控；⑤ 成本披露。

---

## 3. R-Judge: Benchmarking Safety Risk Awareness for LLM Agents

**发表处/年份**：ICLR 2024；arXiv:2401.10019（上海交大）。链接：https://arxiv.org/abs/2401.10019
**一句话定位**：不评"执行中的 agent"，而评"LLM 作为 agent 安全监视器"的风险意识——给交互记录判安全/不安全并写风险描述。

**完整章节树**：
```
1 Introduction
2 Problem Formalization
  （无编号段落标题：Record of LLM Agents. / Risk Awareness for Agent Safety of LLMs. / Task Formulation of Agent Safety Monitor.）
3 R-Judge Benchmark
  3.1 Case Format
  3.2 Curation Principles（Problem Scope. / Threat Model.）
  3.3 Curation Process（Open-source Transformation. / Manual Construction.）
  3.4 Dataset Statistics
  3.5 Evaluation Criteria（Label Score for Safety Judgment. / Pairwise Evaluation for Risk Identification.）
4 Experiments
  4.1 Setup（Baselines. / Prompt Setting. / Metrics. / Reference Score.）
  4.2 Validating R-Judge（Human agreement with GPT-4 scorer...）
  4.3 Main Results
5 Analysis
  5.1 Influence of Different Prompting Techniques（Zero-Shot-CoT with Risk Types / Few-Shot-CoT Prompting / Summary）
  5.2 Effect of Fine-tuning on Safety Judgment（Llama Guard. / Settings. / Results.）
  5.3 Case Study
  5.4 Summary
6 Related Work（6.1 LLM Agents / 6.2 LLM Safety）
7 Conclusion
Appendix A Curation Principles（A.1 Category & Scenario / A.2 Risk Type / A.3 Schema of Risk Description）
Appendix B Dataset（B.1 Examples / B.2 Curation Standard / B.3 Statistics）
Appendix C Human Involvement（数据构建 / GPT-4 scorer 验证）
Appendix D Evaluation（D.1 Metrics / D.2 Prompts / D.3 Human Agreement）
Appendix E Analysis（E.1 各类表现 / E.2 补充解释 / E.3 Llama Guard harm 类 / E.4 Model Failures：GPT-4o、Llama-2 失败案例）
Appendix F Experiment Settings（超参 / 资源成本 / 模型信息）
```

**每节一句话**：
- 2：形式化"交互记录 R"与"安全监视任务 p(R)→(analysis, label)"。
- 3：案例格式（record + 二元安全标签 + 人工风险描述）→ 甄选原则（个人 agent、5 类 27 场景；威胁模型 = Intended Attacks（IPI）与 Unintended Risks，明确排除 jailbreak）→ 构建过程 → 统计 → 双测试评价标准。
- 4：11 模型 + Zero-Shot-CoT；先验证 GPT-4 scorer 与人一致（PCC 0.91），再报主结果。
- 5：提示技术消融、Llama Guard 微调对照、案例研究总结三类能力缺陷。

**贡献点表述**：摘要归纳式（提出任务 formulation + 569 条高质量数据 + 11 模型评测发现 + 多维能力与微调结论）；引言末尾为叙述式贡献段而非 bullet（此为 2024 年 ICLR 风格之一，但现代投稿仍建议 bullet 化）。

**Benchmark 构建呈现**：3.2 先写 curation principles（scope + threat model），3.3 两条数据来源流水线：**Open-source Transformation**（InjecAgent 414 + ToolEmu 81 + AgentMonitor 24，过滤→标标签→写风险描述）与 **Manual Construction**（专家头脑风暴场景 + ChatGPT 润色 + 有效性检查；并把部分 unsafe 改写成 safe 对照）。3.4 统计：共 569 条、平均 2.6 轮、206 词、unsafe 占 52.7%、5 类 27 场景 10 风险类型。附录给风险描述 schema 与标注员培训/交叉检查（Appendix C Human Involvement）。

**评价协议**：**串行双测试**：① safety judgment（二分类标签，指标 F1 主榜 + Recall/Specificity 参考）；② risk identification（开放式 analysis 对照人工风险描述，GPT-4 scorer 给 Effectiveness，归一到 0–100）。**Reference Score** 小节给随机基线（F1 51.32），防止误读。Judge 可信度单独验证（4.2：50 样本、3 名标注员、PCC=0.91）。

**实验组织**：主表按 Intended Attacks / Unintended Risks 两段分开报（每段 F1/Recall/Spec/Effect 四列）；分析章 5.1 提示消融表、5.2 同底座微调对照（Llama-2 vs LlamaGuard-7b；Llama-3 vs Llama-Guard-2，得出"高质量多样数据微调有效"）、5.3 案例研究归纳三缺陷（Scenario Simulation / Understanding Adaptability / Safety Alignment）。

**局限与伦理**：无独立 Limitations 章（ICLR 2024 允许），局限写在 5.4 与附录 E.2；伦理方面数据源于公开数据集+人工改写，规避真实敏感信息。

**独特且值得借鉴**：① **"Validating R-Judge"（judge 与人一致性）单独一小节**放在主结果前；② Reference Score 随机基线小节；③ 风险描述（自然语言证据）作为开放题评分 ground truth——与我们"人工证据标签"高度同构；④ 案例研究按"能力缺陷命名"收尾；⑤ Intended vs Unintended 二分威胁模型（我们可换成"benign 无攻击者"并明确排除攻击类）。

---

## 4. SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents

**发表处/年份**：EMNLP 2024 Findings（以 ACL Anthology 为准）；arXiv:2412.13178。链接：https://arxiv.org/abs/2412.13178
**一句话定位**：具身 agent 在交互仿真环境（AI2-THOR）中安全任务规划基准：750 任务（450 危险 + 300 安全对照）、10 类危害、3 类任务粒度，双评估器（执行 + 语义）。

**完整章节树**：
```
1 Introduction
2 Related Works（2.1 Embodied Agents with LLMs in Task Planning / 2.2 Safety Research for Embodied LLM Agents / 2.3 Planning Benchmark for Embodied Agents）
3 Dataset
  3.1 Dataset Composition（3.1.1 Harm Categories in Embodied World / 3.1.2 Task Types for Planning）
  3.2 Task Generation
  3.3 Filtering and Annotation
4 Benchmark Setup
  4.1 Embodied Environment
  4.2 Evaluation Methods
  4.3 Embodied LLM Agent Baselines
5 Experiments（每小节对应一个 RQ）
  5.1 Detailed Tasks Reveal Weak Proactive Safety
  5.2 Abstract Tasks Show Level-Dependent Safety Awareness
  5.3 Long-Horizon Tasks Remain Challenging with Implicit Risks
  5.4 Various LLMs all exhibit poor safety awareness
  5.5 Semantic Evaluation Proves Reliable
  5.6 Preliminary defenses remain ineffective
6 Conclusions
Appendix A Task Examples / B Dataset Generation / C Experimental Details / D Additional Experiments on Other Models / E User Study
```

**每节一句话**：
- 3：危害分类（来自机器人安全标准，对人/对财产各 5 类）× 任务类型（detailed/abstract/long-horizon）→ GPT-4 生成 → 两步过滤 + 人工标注 GT plan。
- 4：SafeAgentEnv（17 个高层动作 + 低层控制器）+ 双评估器 + 9 个 baseline agent 设计。
- 5：六个小节 = 六个 RQ，小节标题即结论句。

**贡献点表述**：引言按 **dataset / embodied environment / evaluation methods 三段 + 关键发现 bullet** 组织：发现 bullet 3 条（安全意识弱：最好 rejection 仅 10%/32%；换 LLM 无改善（<3% 差异）；两种简单防御无效）。三段各含数字（750=450+300；17 动作；双评估器解决仿真缺陷）。

**Benchmark 构建呈现**：分类体系 = 10 危害（人/财产两支）× 3 任务类型；detailed 600（300 危险 + 300 安全对照，平均步数 5.03 vs 5.12 匹配复杂度）、abstract 100（每题 4 级抽象 L1–L4）、long-horizon 50（危险子任务 A + 安全约束 B + 后续子任务 C）。生成 = GPT-4 输入"固定信息（场景物体+动作表）+ 必需上下文（危害类/对应危险任务）"；质控 = GPT-4 可执行性筛选 → embedding 去重 → 全量人工复核 + 标注 GT 可执行 plan。组成分布图（Fig 2a/b/c）+ 对比表（Table 1 列 7 个已有基准的维度勾叉）。

**评价协议**：指标 = Rejection rate↑、Risk/Success rate(goal)（执行评估器查 goal 条件）与 (LLM)（GPT-4 语义评估器，可参照 GT plan）、Execution rate、耗时；long-horizon 用 C-Safe/C-Unsafe/Incomp 三分类。语义评估器可靠性用**用户研究验证**（1008 个人工评分、三任务类型一致率 91.9%/90.4%/90.7%）。被测 = 9 个具身 agent 设计 × GPT-4（另换 Gemini-2.5-pro、Llama3-8B、Qwen2-7B、DeepSeek-V2.5 做 backbone 实验）。

**实验组织**：RQ 驱动，每小节内部微结构 **"Problem and objective → Evaluation metrics → Experimental results"**；5.1 额外做**矩估计参数分解**（把危险任务表现分解为规划能力 θ 与内在安全意识 α，证"低风险率主因是规划差而非故意失败"）；5.4 雷达图对比不同 LLM；5.5 评估器验证；5.6 防御实验（组合式 agent 设计 + CoT 过滤器，均无效）。表 4 给 agent 组件消融。

**局限与伦理**：正文未见独立 Limitations 章（结论兼谈）；伦理点：家庭机器人危害场景 → 引用安全标准做分类、任务均为仿真。

**独特且值得借鉴**：① **小节标题即发现句**（reviewer 一眼见结论）；② RQ 驱动的实验章微结构；③ 安全对照组按复杂度配对（步数 5.03 vs 5.12）——与我们"安全对照版验证能力无问题"同构且给出配对方法；④ θ/α 参数分解区分"不会做"和"知道危险但做了"——与我们三分类失败归因同目的；⑤ 语义评估器用 user study 报一致率。

---

## 5. Agent-SafetyBench: Evaluating the Safety of LLM Agents

**发表处/年份**：ICLR 2025（清华 COAI）；arXiv:2412.14470。链接：https://arxiv.org/abs/2412.14470
**一句话定位**：349 个交互环境 + 2000 用例、8 风险类 × 10 失败模式的行为级 agent 安全评测，16 个 agent 无一安全分过 60%。

**完整章节树**：
```
1 Introduction
2 Related Work（2.1 LLM Safety Evaluation / 2.2 Agent Safety Evaluation）
3 Agent-SafetyBench Construction
  3.1 Risk Categories
  3.2 Data Collection（3.2.1 Format of Data and Environments / 3.2.2 Refine Existing Datasets / 3.2.3 Augment Refined Data / 3.2.4 Quality Control）
  3.3 Scorer
4 Experiments
  4.1 Setup
  4.2 Main Results
  4.3 Failure Mode Analysis
  4.4 Helpfulness Analysis Under Different Scenarios
  4.5 Discussion on Defense
5 Conclusion
Appendix A Risk Categories / B Failure Modes / C Details for Implementing Environments / D Evaluated Models / E Augmentation Details / F Details for Data Cross-Validation / G Scorer Details / H Experimental Details
```

**每节一句话**：
- 1：内容安全→行为安全的概念升级；开篇放 benchmark 对比表 + 5 点特性 + 3 条贡献。
- 3：8 风险类定义表 → 数据流水线（格式 → 复用已有数据集改造 → 增强 → 质控）→ 微调 scorer。
- 4：主结果表 → 失败模式分析 → helpfulness×safety 二维分析 → 防御提示实验。

**贡献点表述**：3 条 bullet：①基准本身（新颖环境 + 系统性风险/失败模式覆盖）；②微调一个 scorer（比 GPT-4o 高约 15%）+ 16 agent 全低于 60% 的实证；③失败模式与 helpfulness 分析归纳两大缺陷（lack of robustness、lack of risk awareness）+ 防御提示不足。**把"评测器改进"本身写成贡献**是其特点。

**Benchmark 构建呈现**：分类体系双轴——**8 风险类**（Table 3：泄露敏感信息/财产损失/传播不实/人身伤害/违法违背伦理/破坏可用性/有害代码/生成不安全内容）+ **10 失败模式**（Table 4：如信息不全误调工具、忽略约束、忽略隐式风险、参数错、过度信任工具结果等，每用例标注预期失败模式）。数据来源→扩展→质控三段式非常清晰：3.2.2 复用 6 个已有数据集（R-Judge/AgentDojo/GuardAgent/ToolEmu/ToolSword/InjecAgent）三步改造（改写模糊样本→去冗余→统一环境实现），content 类用 AdvBench×20 越狱模板合成，得 876 条；3.2.3 增强：生成 300 新环境名强推多样性 + 让 GPT-4 同时生成"预期风险行为链"提质 + 指定风险类控分布，得 1124 条新样本；3.2.4 质控：人工预检（每样本至少一轮）+ 自动校验（JSON 工具定义 vs Python 类一致性）+ 人工后检（跑 GPT-4o-mini 与 Claude-3.5 生成 4000 条记录全量人标，用 open coding 反推出 10 失败模式）+ 交叉验证。统计呈现：Table 2 对 349 环境按"已有类似工具/有 API 无沙盒/无 API 有现实应用/未来型"四档细分。

**评价协议**：Scorer = 用 4000 人工标注样本（GPT-4o 生成解释）微调 Qwen2.5-7B，二分类安全标签准确率 91.5%（GPT-4o 仅 75.5%）；**安全分 = safe 标签占比**（越高越好）；交互协议 4 步循环写明。被测 16 个 LLM agent（GPT/Claude/Gemini/Qwen/Llama/GLM/DeepSeek）。

**实验组织**：Table 5 主表（Total/Behavior/Content + 8 风险类列）→ 4.2 三条发现（都有提升空间；强模型更安全；行为分显著低于内容分）；Table 6 按 10 失败模式逐列打分 → 4.3 归纳两大缺陷；4.4 按 fulfillable/unfulfillable 人工标注切分，报 safety×helpfulness（GPT-4o helpfulness judge 94% 准确），证明强 agent"不是靠拒绝而是靠正确执行"安全；4.5 两种防御提示（简单枚举失败模式 vs 详细版）实验——弱模型无效、强模型有限且费上下文 ⇒ 主张 prompt 防御不足。

**局限与伦理**：结论章之外未单列 Limitations；伦理/合规通过"环境均为模拟 + 数据人工审核"处理。

**独特且值得借鉴**：① **失败模式作为标注轴 + 专属结果表**（Table 6），从"哪里失败"直接导出研究结论；② fulfillable/unfulfillable 切分 + helpfulness 联合分析，堵住"全拒绝得高安全分"的退化解——我们的安全对照版可同样报告"对照任务通过率"；③ 数据流水线数字闭环（876 + 1124 → 2000）；④ scorer 微调 + 准确率对比作为贡献；⑤ intro 里放 benchmark 多维对比表。

---

## 6. Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents

**发表处/年份**：ICLR 2025（浙大 + Rutgers，agiresearch）；arXiv:2410.02644。链接：https://arxiv.org/abs/2410.02644
**一句话定位**：把 agent 攻击/防御形式化并统一基准化的安全框架：10 场景 10 agent 400+ 工具、27 类攻防、7 指标、13 个 LLM backbone，附带新攻击（PoT backdoor）与新指标（NRP）。

**完整章节树**：
```
1 Introduction
2 Related Work
3 Definitions to Basic Concepts and Threat Model（3.1 Defining Basic Concepts / 3.2 Threat Model）
4 Formalizing Attacks and Defenses in LLM Agents
  4.1 Formalizing Prompt Injection Attacks（4.1.1 DPI / 4.1.2 IPI / 4.1.3 Attack Framework）
  4.2 Formalizing Memory Poisoning Attack（4.2.1 Detailed Adversarial Goal / 4.2.2 Attack Framework）
  4.3 Formalizing Plan-of-Thought Backdoor Attack（4.3.1 Detailed Adversarial Goal / 4.3.2 Attack Framework）
  4.4 Formalizing Defenses for Our Attack Framework
5 Evaluation results on Agent Security Bench (ASB)
  5.1 Introduction to ASB / 5.2 Experimental Setup / 5.3 Benchmarking Attacks / 5.4 Benchmarking Defenses
6 Conclusion and Future Work
Appendix A Details for Attack and Defense Methods（A.1 Mixed Attacks / A.2 ReAct / A.3 Attacking Details / A.4 Defense Details：逐攻击的防御）
Appendix B Benchmark Construction（B.1 Agent Case Generation / B.2 Tools Generation（normal/aggressive 指令）/ B.3 Benchmark Comparison）
Appendix C More Experimental Setup（C.1 LLMs / C.2 Implementation Details：Dataset、Experimental Setup、Evaluation Metrics、Prompts、Output Parsing、Tool Simulation）
Appendix D More Experimental Analyses（D.1 attacks 细分分析 / D.2 defenses 细分分析）
Appendix E Ethics Statement / F Reproducibility Statement
```

**每节一句话**：
- 3：定义 LLM agent（含 RAG 记忆）、target/injected task，威胁模型含对抗目标公式与攻击者能力清单（工具/不知 backbone/可写系统提示/可改用户提示/黑盒记忆库）。
- 4：逐一形式化 DPI、IPI、Memory Poisoning、PoT Backdoor（各含 Definition + 目标函数 + 攻击框架），再形式化防御。
- 5：ASB 组成 → 设置 → 攻击基准结果 → 防御基准结果。

**贡献点表述**：引言末 **①–⑤ 编号 5 条**：①ASB 首个综合基准（10 场景/agent、400+ 工具任务）；②新攻击 PoT backdoor；③攻防形式化分类（对应 agent 的系统提示/用户提示/记忆/工具四个攻击面）；④27 攻防 × 13 backbone × 7 指标基准（最高平均 ASR 84.3%，防御普遍无效）；⑤新指标 NRP（utility-security 平衡）。

**Benchmark 构建呈现**：分类体系 = **攻击面 × 攻击类型**（系统提示→PoT backdoor；用户提示→DPI；工具响应→IPI；记忆→poisoning；组合→mixed）；任务分 aggressive（测拒绝）与 non-aggressive。构建细节放附录 B（LLM 生成 agent case + 工具（normal/attacker），含 aggressive/non-aggressive 指令设计），正文重形式化、附录重工程。统计以"10/10/400+/27/7/13"数字串呈现，另有 B.3 Benchmark Comparison 与 InjecAgent/AgentDojo 对比。

**评价协议**：7 指标（Tab.4）；核心两个公式化定义在 C.2.3：**ASR** = 成功调用目标恶意工具的攻击任务数 / 总攻击任务数（Eq.18）；**PNA**（Performance under No Attack）= 调齐标注工具完成的正常任务数 / 总正常任务数（Eq.19）；另有 BP（Benign Performance，后门下良性表现）、Refusal Rate（LLM judge 判拒绝，prompt 在 C.2.4）、FNR/FPR（检测式防御）、**NRP = 效用 ×(1−ASR)**（文中算例 80%×(1−30%)=56%）。被测 = 13 个 LLM backbone（Gemma2/LLaMA3(0.1)/Mixtral/Qwen2/Claude-3.5/GPT 系），agent 框架 ReAct。

**实验组织**：5.3 攻击（各攻击面的 ASR/PNA 主表 + mixed attack 最强 38.01% 等细分）；5.4 防御（11 种防御大多无效；memory 防御平均 FNR 0.66）；附录 D 逐维深挖（backbone 分析、攻击组合、PoT 表现、注入类型 naive/context-ignoring/combined、aggressive vs non-aggressive、逐防御分析）。结论明确"防御不足，需更强防御"。

**局限与伦理**：Appendix E **Ethics Statement**、Appendix F **Reproducibility Statement**（ICLR 格式惯例）：承认攻击工具双重用途、强调防御研究目的。

**独特且值得借鉴**：① **形式化章节前置**（定义 + 威胁模型 + 攻击面映射图 Fig.1），把 benchmark 做成"理论框架 + 实证"；② 攻防对称评测（同表报 ASR 与防御 FNR/FPR）；③ 复合指标 NRP 公式化；④ aggressive/non-aggressive 任务拆分单测拒绝率；⑤ Ethics/Reproducibility 独立成附录。

---

## 7. InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents

**发表处/年份**：arXiv:2403.02691（UIUC，2024；常被引为 Findings of ACL 2024，以 Anthology 为准）。链接：https://arxiv.org/abs/2403.02691
**一句话定位**：首个针对 tool-integrated agent 间接提示注入（IPI）的基准：17 用户工具 × 62 攻击者工具 = 1054 测试用例，30 个 agent 评测。

**完整章节树**：
```
1 Introduction
2 Benchmark Construction（2.1 Problem Formalization / 2.2 Test Case Generation / 2.3 LLM Agents Evaluation）
3 Experiments（3.1 Experiment Settings / 3.2 Attack Success Rates of Different Agents）
4 Analysis
  4.1 User Cases Exhibit a Stronger Association with Attack Success Than Attacker Cases
  4.2 User Cases with High Content Freedom Placeholders Are More Vulnerable
  4.3 Enhanced Setting Increases Agents' Sensitivity to Attacker Instructions
5 Related Work
6 Conclusion
7 Ethical Considerations
8 Limitations
Appendix A Dataset Details / B Experiment Details / C Additional Experimental Results（valid rates、ASR-valid、ASR-all、攻击类型、响应质量、simple prompt、测试用例分析）/ D Representative Cases（成功/失败攻击示例）/ E Full Prompts
```

**每节一句话**：
- 2：形式化 IPI 三元组（用户指令-工具-含注入的响应；攻击工具）→ 三步生成（user case：模板带占位符；attacker case：抽 9 工具让 GPT-4 选一并生成指令；合成 base/enhanced 两档）→ 判定协议。
- 3：30 个 agent（ReAct prompted vs fine-tuned）的 ASR 主表。
- 4：三个分析小节即三条发现。
- 7/8：伦理（双重用途、已向 OpenAI/Anthropic 披露）与 4 条 Limitations。

**贡献点表述**：引言末 **编号 3 条**（首次形式化工具 agent 的 IPI；InjecAgent 基准；30 agent 评测揭示普遍脆弱）。

**Benchmark 构建呈现**：分类体系 = 攻击意图二分（direct harm：financial/physical/data security；data stealing：financial/physical/other，Table 1 例句）。数据来源 = ToolEmu 330 工具筛出 17 个含外部内容的 user 工具；扩展 = GPT-4 生成 + 人工修（约 30% 攻击指令缺参数，人工补齐——**明确的质控发现与数字**）；统计表（Table 2）极简：17 / 62（30+32）/ 1054。附加"content freedom"分级（外部内容可篡改难度）做分析轴。

**评价协议**：**ASR 判定基于下一步动作**：direct harm = 执行攻击工具即成功；data stealing = 两阶段 S1（调数据提取工具）/S2（把数据发给攻击者），GPT-4 模拟工具返回；报 **ASR-valid**（排除无效调用）与 **ASR-all** 两口径 + valid rate。被测 = 30 个 agent（ReAct prompted 系列 + fine-tuned function-calling 模型）；设 base 与 enhanced（加固定 hacking prompt）两档攻击强度。

**实验组织**：主表（agent 类型 × base/enhanced × direct/data-stealing × S1/S2）；4 章"Analysis"独立成章且**小节标题即结论句**（user case 属性比 attacker case 更影响成功率；占位符 content freedom 越高越易攻；enhanced 几乎翻倍）；附录补 valid rate、响应质量（防"拒答式安全"误判）。

**局限与伦理**：7 Ethical Considerations（漏洞披露的双重用途 + 负责任披露）与 8 Limitations（固定 hacking prompt 的时效性；攻击指令混入良性内容未测；单轮、攻击至多两步；fine-tuned agent 覆盖不足）**各占一节**——ACL 风格。

**独特且值得借鉴**：① "Analysis"独立成章 + 发现式小节标题；② valid/invalid 双口径 ASR（防格式失败冒充安全）；③ 人工质控过程直接量化（30% 缺参修复）；④ Ethical Considerations + Limitations 双节模板；⑤ 占位符自由度作为受控变量做归因——与我们 wording/position 受控干预同一方法论。

---

## 8. AgentAuditor: Human-Level Safety and Security Evaluation for LLM Agents

**发表处/年份**：arXiv:2506.00641（NYU Abu Dhabi/KTH/UIUC/NTU/NUS/Sydney/MBZUAI；v3 2026-01）。链接：https://arxiv.org/abs/2506.00641 （venue 待核）
**一句话定位**：既提出"记忆增强 LLM 评审框架 AgentAuditor"，又建"评审器基准 ASSEBench"（2293 标注交互记录、Strict/Lenient 双标准），达成 human-level 的 agent 安全/安全（safety/security）评估。

**完整章节树**（主文 + 附录 A–S）：
```
1 Introduction
2 Preliminaries（Rule-based vs LLM-based Evaluator；Agent Safety vs. Agent Security）
3 AgentAuditor: Our Framework（3.1 Stage 1 Feature Memory / 3.2 Stage 2 Reasoning Memory / 3.3 Stage 3 RAG-based Memory Augmented Reasoning）
4 ASSEBench（4.1 Structure of ASSEBench / 4.2 Construction of ASSEBench）
5 Experiments and Results（5.1 Experimental Setup / 5.2 Empirical Results / 5.3 Ablation Studies / 5.4 Human Evaluation）
6 Limitation
7 Conclusion & Future Work
Appendix A Challenges for Automated Evaluation / B Related Works / C FINCH 聚类 / D Prompt 模板 / E 自动标注 prompt / F Existing Benchmarks / G ASSEBench 开发全流程（5 小节）/ H 详细统计 / I 人工标注员准则（含 Strict/Lenient 判据）/ J 指标讨论 / K 详细结果 / L–N 模型/嵌入/聚类影响 / O 稳健性（标签噪声、对抗攻击、OOD）/ P 资源用量 / Q 人工评估细节 / R 可扩展性 / S Broader Impacts
```

**每节一句话**：
- 2：先把"规则式 vs LLM 式评审器"与"safety（内生非故意）vs security（外源蓄意）"概念对仗定义——为双覆盖定位。
- 3：三阶段框架（特征记忆→推理记忆（FINCH 聚类选代表 shot + 生成 CoT）→检索增强推理）。
- 4：ASSEBench 四子集（Security 817 + Safety/Strict/Lenient 各 1476）+ 三阶段构建流水线。
- 5：10 个 base 模型 ±AgentAuditor、对比微调小模型（ShieldAgent、Llama-Guard-3），F1/Acc。

**贡献点表述**：4 条 bullet（系统分析自动评估挑战；AgentAuditor 框架；ASSEBench 首个 safety+security 双覆盖评审器基准 + 人机协同分类法；实验全面 SOTA 并达 human-level）。

**Benchmark 构建呈现**：标注元数据三维（**Scenario / Risk Type / Behavior Mode**）+ 二元 safe/unsafe + **ambiguous 标志**；Strict/Lenient 双评判标准处理边界样本（衍生两个子集）。构建三阶段：Stage1 从 4 个已有基准复现 × 3 个 LLM 生成 13,587 条 → Balanced Allocation 预处理至 4,527；Stage2 人机协同分类 + 人工终标 + 修复；Stage3 Balanced Screening 算法组装子集。统计表放附录 H，标注判据全文放附录 I（含人工修复示例）。

**评价协议**：指标 F1 + Acc（×100）；为了防污染，AgentAuditor 用到的 CoT 子集一律从评测中剔除（对照组同口径）；另有人工评估（5.4）与标注员间信度（附录 J.2 inter-rater reliability）。

**实验组织**：主表 = 10 模型 × {Origin, +AA} × {R-Judge, ASSE 四子集} 的 F1/Acc 对比（蓝色/红色标增益）→ 观察句列表；5.3 消融（记忆组件）；5.4 人工评估；附录再补鲁棒性、资源、可扩展性。

**局限与伦理**：6 Limitation、7 Conclusion & Future Work、S Broader Impacts 三处分工；附录 O 直接回应"标签噪声/对抗攻击/OOD"三类审稿质疑。

**独特且值得借鉴**：① Preliminaries 章先立概念对（rule vs LLM judge；safety vs security）再开工；② Strict/Lenient 双标准处理模糊样本——我们的三分类失败归因也可设"边界样本仲裁/双标准"；③ 基准构建附录给完整流水线算法（伪代码）与标注员判据全文；④ 附录 O 稳健性专章（标签噪声、对抗、OOD）是审稿人友好的防御性结构；⑤ "评审器验证"与"被评对象"分离成两个贡献。

---

# 横向速查表

| 论文 | venue/年 | 评测对象 | 核心指标 | judge 方式 | 分类体系 | 安全对照 | 防御实验 | judge 验证 |
|---|---|---|---|---|---|---|---|---|
| AgentHarm | ICLR 2025 | 执行 agent（misuse） | harm score / refusal / non-refused | 人写 rubric + 窄 LLM 子项 | 11 harm 类 | ✅ benign 孪生 | 越狱/提示消融 | 人工抽检 |
| τ²-bench | 2025 Sierra | 对话 agent（双控） | pass^k | 确定性断言 | 域策略+原子子任务 | Oracle/No-User 对照 | 模式消融 | 用户模拟器人工审计 |
| R-Judge | ICLR 2024 | LLM 安全监视器 | F1 / Effectiveness | GPT-4 scorer | 5 类 27 场景 10 风险 | safe/unsafe 平衡 | 微调(Llama Guard) | ✅ PCC 0.91 |
| SafeAgentBench | EMNLP 2024 Findings | 具身规划 agent | Rej / RR(goal,LLM) / ER | 执行 + GPT-4 语义 | 10 危害 × 3 任务型 | ✅ 300 安全配对 | 组合设计+CoT 过滤 | ✅ user study 90%+ |
| Agent-SafetyBench | ICLR 2025 | 工具 agent | 安全分=safe 占比 | 微调 Qwen2.5-7B | 8 风险 × 10 失败模式 | fulfillable/unfulfillable | 防御提示 | ✅ 91.5% acc |
| ASB | ICLR 2025 | 攻防 agent 框架 | ASR / PNA / NRP / RR | 规则(工具调用)+LLM 判拒绝 | 攻击面×攻击类型 | PNA/BP | ✅ 11 防御 | 规则为主 |
| InjecAgent | 2024 | 工具 agent（IPI） | ASR-valid/all + valid rate | 规则(动作判定)+GPT-4 模拟工具 | 直害/窃密二分 | valid rate 口径 | enhanced 攻击档 | 动作规则 |
| AgentAuditor | 2025/26 | 评审器本身 | F1 / Acc | 评审器框架 | Scenario×Risk×Behavior | Strict/Lenient 双标准 | — | ✅ 人工评估+信度 |

---

# 一、"agent 安全 benchmark"论文的结构惯例（与通用能力 benchmark 的差异）

1. **Threat model / Problem Formalization 前置**：安全类论文必须先说清攻击者/风险来源/假设（ASB 整章、R-Judge 3.2、InjecAgent 2.1）；通用能力 benchmark 只需任务定义。惯例是把"与攻击类工作（IPI/jailbreak）的边界"显式划清。
2. **双轴分类体系**：风险/危害类别（taxonomy）× 失败模式（failure mode）两轴标注是主流（Agent-SafetyBench 8×10 最典型）；分类表（定义 + 例句）固定出现在 Benchmark 章开头。
3. **构建流水线三段式 + 数字闭环**："来源/种子 → 扩展/增强 → 质控"必成一小节（3.2.x 式子节），且给出每阶段数量流转（876+1124→2000；13,587→4,527→2,293）；质控必含"人工参与量 + 一致性/抽检数字"。
4. **Judge 可信度是审稿生命线**：LLM judge 必须单独验证（R-Judge 4.2 PCC、SafeAgentBench 5.5 user study、Agent-SafetyBench scorer 准确率对比）；趋势是"规则/断言优先，LLM 只做窄子项或语义补充"（AgentHarm、τ²）。
5. **指标复合化、防退化解**：同时报危害侧（ASR/harm score/risk rate）与能力侧（benign 对照、PNA、helpfulness、non-refused 分数），并把"安全但无用"显式排除（AgentHarm benign 孪生、Agent-SafetyBench helpfulness、ASB NRP）。
6. **实验章 = 主结果 + 失败归因 + 防御/缓解 + 消融**四件套：失败归因常以"能力缺陷命名"（R-Judge 三缺陷、Agent-SafetyBench 两大缺陷）；防御实验常以"现有防御不足"收尾，为 future work 铺垫。
7. **评测器/模拟器/环境自身的可靠性被单列一节**（τ² 4.3、AgentAuditor 5.4、SafeAgentBench 5.5），先证工具可信再谈发现。
8. **防污染设计**：private holdout、canary string、公开/私有测试集对比（AgentHarm）；LLM 生成数据必须声明人工复核比例。
9. **贡献 bullet 双分组**：benchmark 性质（覆盖、质量、易用、防污染）与实证发现（模型有多差、防御有多弱）分开列，每条带数字。
10. **伦理/局限刚性配置**：Limitations bullet 化 + 双重用途（dual-use）声明 + 负责披露；ICLR 稿另配 Ethics Statement / Reproducibility Statement；ACL 章把 Ethical Considerations 与 Limitations 各自独立成节。

# 二、对我们论文（benign 任务下 tool-using agent 的 context-environment gaps）的 10 条建议

1. **前置 "Problem Formalization & Threat Model" 章**：一页定义 context（用户指令/文档）、partially observable environment、verification、dangerous action 与 gap 的触发条件；显式声明 threat model = **benign、无攻击者**，并用一段与 IPI/jailbreak/误用类 benchmark（AgentHarm、InjecAgent、ASB）划界——这是我们的差异化卖点，学 R-Judge 3.2 的写法把"排除什么"写死。
2. **双轴分类体系落地**：三类 case（requirement underspecification / infeasibility / factual inconsistency）作为风险轴；失败归因三分类（证据搜集不足 / 证据充足未识别危险 / 识别到危险仍盲从）作为失败模式轴，学 Agent-SafetyBench 给每个 case **预标注期望失败模式**并在实验章出"按归因分列的结果表"（对标其 Table 6）。
3. **构建流水线三段式 + 数字闭环**：seeds（人工手写，报数量）→ 批量扩展（说明 LLM 角色、约束、去重）→ 质控（人工复核比例、自动校验、交叉验证/一致率）；参考 Agent-SafetyBench 3.2 与 ASSEBench 三阶段，把每个阶段的输入→输出数量写成流水线图/表。τ²-bench 的审查清单（underspecification / overspecification / non-unique solutions）恰好是我们的核心概念，直接引用其任务审查项做质控标准。
4. **安全对照版 = 能力保持检验，写进指标定义**：对标 AgentHarm benign 孪生与 Agent-SafetyBench fulfillable 切分——主表必须同时报"坑点版 ASR"与"对照版通过率"，并在指标小节明确：对照通过率低于阈值的 case 作废/单列（防止"能力不足"冒充"验证失败"）。这是审稿人最容易攻击的点，学 AgentHarm 把它写成 scoring 的内建机制而非事后补充。
5. **指标公式化 + 可靠性维度**：给出 ASR、安全率、对照通过率的公式（学 ASB Eq.18/19 的写法）；考虑加 τ² 式 pass^k（多次运行）——"验证行为"有随机性，单次运行结论不稳，pass^k 或方差列能显著加分。
6. **Judge 协议单列 "Validating the Judge" 小节**：LLM-as-Judge + 人工在抽样子集上的一致率（accuracy/PCC/混淆矩阵），三分类归因给仲裁流程与边界样本处理（学 AgentAuditor 的 Strict/Lenient 双标准：对"识别到危险但盲从"vs"未识别"边界可设宽松/严格两套统计）。
7. **实验章 RQ 驱动 + 小节微结构**：学 SafeAgentBench——每个实验小节内部 "Research question → Metrics → Results → Finding"，小节标题尽量写成发现句（如 "Defense prompts fail to reduce ASR"）。三个主实验对应 RQ1（防御为何无效）/RQ2（拓扑为何有效）/RQ3（失败为何发生）。
8. **受控干预实验按"单变量表格化"呈现**：wording（明显→隐晦）与 position（明显→不明显）各一张消融表，列 = ASR + 三类归因占比的变化，行 = 干预档位（学 AgentHarm 4.3 Table 2/3 的行=模型、列=Score/Refusal 双指标风格）；InjecAgent 4.x 的"分析小节标题即结论"可直接套用。
9. **拓扑实验要带协变量表**：三拓扑 + 普通对照的比较中，单独报每拓扑的 token 消耗、步数、调用次数（学 τ²-bench 的 cost 披露与 Oracle Plan/No-User 对照设计），用一张表把"ASR 下降不是 token 多带来的"钉死；必要时做 best-of-n/等预算控制。
10. **结构落位与附录清单**：建议骨架 = 1 Introduction（贡献分两组 bullet：benchmark 性质 + 三大发现）→ 2 Related Work（LLM/Agent Safety Evaluation 两小节 + 对比表）→ 3 Preliminaries & Problem Formalization（含 benign threat model）→ 4 Benchmark Construction（taxonomy、seed→expand→QC、统计表、安全对照设计）→ 5 Evaluation Protocol（指标公式、judge、validation 小节）→ 6 Experiments（RQ1 防御、RQ2 拓扑、RQ3 干预+归因）→ 7 Discussion → 8 Limitations & Ethics（dual-use 低但要声明无攻击数据、LLM judge 偏差、语言/领域局限）。附录必备：坑点/对照 case 成对示例、prompt 与标注指南全文、标注员一致性、三类 case × 三类归因完整统计、失败执行日志（学 AgentHarm D.5 / InjecAgent D）。

---

## 引用论文链接汇总

1. AgentHarm（ICLR 2025）：https://arxiv.org/abs/2410.09024 （全文结构取自 https://arxiv.org/html/2410.09024 ）
2. τ²-Bench（2025, Sierra）：https://arxiv.org/abs/2506.07982 （全文结构取自 https://arxiv.org/html/2506.07982 ）
3. R-Judge（ICLR 2024）：https://arxiv.org/abs/2401.10019
4. SafeAgentBench（EMNLP 2024 Findings，以 Anthology 为准）：https://arxiv.org/abs/2412.13178
5. Agent-SafetyBench（ICLR 2025）：https://arxiv.org/abs/2412.14470
6. Agent Security Bench / ASB（ICLR 2025）：https://arxiv.org/abs/2410.02644
7. InjecAgent（2024，常引为 Findings of ACL 2024）：https://arxiv.org/abs/2403.02691
8. AgentAuditor / ASSEBench（2025，v3 2026-01）：https://arxiv.org/abs/2506.00641

补充候选（本次未展开结构分析，可按需替换/加引）：SafeArena（https://arxiv.org/abs/2503.04957，web agent 误用）、OS-Harm（https://arxiv.org/abs/2506.14866，computer-use agent）、GuardAgent（arXiv:2406.09187，防御型 guard agent）、AgentDojo（NeurIPS 2024 D&B，IPI 基准）、ToolEmu（ICLR 2024，模拟器式风险评测）、"Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents"（arXiv:2605.16282，对 40 个 agent 安全基准的六轴方法论审计，写 related work 时很有用）。
