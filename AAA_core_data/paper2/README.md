# paper2 — 论文骨架（预写作）

本文件夹存放《**Context-Environment Gaps: Benchmarking Tool-Using Agent Safety in Benign Tasks**》（工作标题）的论文结构骨架与预写作材料。

| 文件 | 内容 |
| --- | --- |
| `00_骨架设计与写作指南.md` | **主文档**：一句话贡献与叙事主线、结构决策及依据（为什么这么组织）、全文章节树、逐节写作指南（每部分写什么）、图表/附录规划、写作顺序、占位符清单、待确认问题 |
| `main.tex` | LaTeX 章节骨架（可独立编译的 article 版；含 TODO 注释，注释均指向指南对应小节；投稿时整体迁入目标会议模板） |
| `_research/` | 5 份调研报告：26 篇顶会 benchmark/方法论文的全文结构分析（骨架设计的证据基础） |

## `_research/` 报告索引

- `local_structure_A.md` — WebArena / ToolEmu / SWE-bench / τ-bench / AgentDojo（本地 PDF 深析：构建流水线、judge 验身、指标小节、攻防矩阵）
- `local_structure_B.md` — AppWorld / ToolSandbox / Agent Security Bench / Agent-Safety-Bench / AgentBench / R-Judge（本地 PDF 深析：安全 benchmark 双轴分类、scorer、token 混淆控制先例）
- `web_safety_benchmarks.md` — AgentHarm / τ²-bench / R-Judge / SafeAgentBench / Agent-SafetyBench / ASB / InjecAgent / AgentAuditor（安全类横向：威胁模型划界、指标防退化、实验四件套）
- `web_benchmark_craft.md` — GAIA / AgentBench / SWE-bench / OSWorld / τ-bench / MLE-bench / BrowseComp + 2026 新作（benchmark 写作惯例：筛选漏斗、主表形态、分析章六型、污染排除）
- `web_attribution_methods.md` — MAST / AgentBoard / ToolEmu / Lost in the Middle / FormatSpread / MT-Bench（失败归因分类学、受控干预写法、LLM-as-Judge 校准金标准）

> `_keep.txt`、`_write_test.txt` 为工具可用性测试占位文件，可忽略或删除。
