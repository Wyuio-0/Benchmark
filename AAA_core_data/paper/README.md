# 论文预写作工作区

本目录存放 benchmark 论文正文、结构提纲、参考文献结构调研和实验—图表矩阵。当前已完成任务定义、关键证据及失败诊断的初稿，其余部分保留写作提纲；待全量实验填充的数字继续使用占位符。

## 文件

- `00_参考文献结构调研.md`：调研高层级 agent/benchmark/safety 论文后，总结它们的通用组织方式，以及本文应借鉴和避免的点。
- `01_论文主骨架.md`：旧版展开提纲，保留叙事、图表和论证材料备查；当前章节结构以本文及 `paper_skeleton.tex` 为准。
- `02_实验图表矩阵.md`：把 RQ、实验、对照、指标、图表和预期归因一一对应，防止实验变成流水账。
- `paper_skeleton.tex`：使用 ICML 2026 官方模板的全篇结构预览稿，正文双栏，附录规划单栏。
- `paper_skeleton.pdf`：编译后的完整 PDF，含五个正文大章节、非编号声明、参考文献和 A–L 附录；支持章节书签导航。
- `references.bib`：经来源核验的 BibTeX 文献库；`citation_audit.md` 记录论断依据与元数据核验结果。
- `build.ps1`：一键重新编译并同步 PDF。
- `templates/icml2026/`：完整官方模板及来源记录；目录根部的配套 `.sty` / `.bst` 文件与官方原件一致。
- `_reference_papers/`：已下载的参考论文 PDF；`extracted_headings.txt` 是自动抽取的章节标题备查。

## 当前章节结构（2026-11-22）

1. Introduction
2. Related Work
3. GAP-CE Bench
   - 3.1 Task Formulation：按 Context and Environment、Gap Types、Threat Model 顺序设置三个不编号的段落标题；gap 定义及 RU/RI/FI 加粗列表放在 Gap Types 下。
   - 3.2 Benchmark Construction：Task Construction、Evidence Annotation、Quality Control、Statistics 四个段落标题。
   - 3.3 Failure Diagnosis：确定性危险判分、证据充分性评估、危险意识评估及三个失败阶段。
4. Experiments
   - Experimental Setup、Main Results and Failure Analysis、Safety Enhancements、Agent Topologies、Evidence Interventions。
5. Conclusion

Limitations、Ethics Statement、Reproducibility Statement 为非编号部分。Discussion 并入实验讨论；指标移入 Experimental Setup；评审校验及完整形式化定义保留在附录。第三节不设三级编号。

## 当前建议的论文一句话定位

本文研究**无攻击者、用户意图良性但上下文与环境状态存在缺口时，工具型 agent 为什么仍会做出危险动作**。可执行环境和关键证据标注支持证据遗漏、风险未识别、风险忽视三个阶段的诊断；其中后两类通过独立的风险自评及评审区分，不据此推断原执行的内部认知。安全对照与 position/wording 干预的构建和结果仍待补充确认。

## 排版与编译

2026-11-18 改用 [ICML 2026 官方模板](https://icml.cc/Conferences/2026/AuthorInstructions)，使用 `preprint` 模式。移除原先的自定义彩色标题和摘要装饰，保留官方字体、栏宽、标题与章节层级。摘要和引言保留原文；引言后的注释提纲转为 PDF 可见的写作要点，附录补充各节内容规划。后续内容仍为结构稿，实验数字和引用需要继续填写与核验。

在本目录运行：

```powershell
./build.ps1
```

需要 TeX Live（`latexmk`、`pdflatex`）。生成的 PDF 同步到本目录、`_build/` 和仓库的 `output/pdf/`。模板下载地址、校验值见 `templates/icml2026/SOURCE.md`。编译缓存保存在 `_build/`。
