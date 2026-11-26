# Citation verification log

## Single-agent framework terminology — 2026-11-23

- Replaced "shared single-agent ReAct framework" with "shared single-agent framework" and removed the accompanying `Yao2023react` citation and unused bibliography entry. The Agent Topologies outline now uses "Single agent" consistently.
- Implementation checked in `../../src/harness/agent.py` and `../../prompt/system.md`: native tool calls alternate with model decisions; the implementation does not specify the original ReAct prompting scheme. Internal topology names remain unchanged.
- This terminology correction supersedes the earlier ReAct citation addition recorded below.

## Risk self-assessment and citation placement — 2026-11-23

- Added `Tang2025lm` at the end of the existing risk self-assessment sentence. Removed the introductory "Following Agent-SafetyBench" wording from Helpfulness and retained `Zhang2024agent` on the task-grouping sentence. No methodological or scoring changes.
- Tang et al.: title and all six authors in order extracted automatically from citation meta tags at https://arxiv.org/abs/2508.13465 . Raw metadata and rendered entry: `../../tmp/citation_risk_self_metadata.json` and `../../tmp/citation_risk_self_new.bib`.
- Publication verified against the official COLM 2025 proceedings: https://proceedings.colm.cc/paper_files/paper/2025/hash/d1e63f4027efc7c44bfc253eafc15a58-Abstract-Conference.html . The published conference version is cited, with https://openreview.net/forum?id=OeYdS51k8F as the short paper locator. No proceedings pagination, volume, or publisher DOI verified; those fields are omitted.
- The reference supports asking the model to identify risk in a concrete trajectory; it is attached to risk self-assessment rather than the full diagnosis framework or independent review.

## Experimental Setup, Helpfulness — 2026-11-23

- Added `Zhang2024agent` to the sentence attributing the division into safely fulfillable and unfulfillable tasks to Agent-SafetyBench. The subsequent scoring explanation and formula remain unchanged and are this manuscript's definition.
- Supporting passage: https://arxiv.org/html/2412.14470 , Section 4.4. The source uses the same safe-feasibility distinction; its own helpfulness scoring disregards safety, so the citation is attached specifically to the task grouping.
- Title, all seven authors in order, and initial publication year 2024 extracted automatically from citation meta tags at https://arxiv.org/abs/2412.14470 and rendered with the citation-management metadata formatter. Agent-SafetyBench and LLM capitalization protected.
- Enrichment: the official arXiv record and authors' repository https://github.com/thu-coai/Agent-SafetyBench were checked; the repository recommends the 2024 arXiv citation. No published venue or publisher DOI verified; cited as a preprint using the stable arXiv URL. Volume, issue, and proceedings pagination are not applicable to this entry.
- Raw extraction: `../../tmp/citation_helpfulness_*`. Bibliography keys and required metadata checked with citation-management; PDF rebuilt and affected pages inspected.

## Experimental Setup, Models and Agent — 2026-11-23

- Added `Yao2023react` immediately after the introduction of the shared ReAct framework; prose unchanged.
- Title and seven authors, including author order, automatically extracted from the citation metadata at https://arxiv.org/abs/2210.03629 . ReAct capitalization protected in BibTeX.
- Publication enrichment: the arXiv record identifies v3 as the ICLR camera-ready version; https://collaborate.princeton.edu/en/publications/react-synergizing-reasoning-and-acting-in-language-models/ independently confirms the author list and ICLR 2023 publication. The published conference year 2023 is used rather than the initial preprint year 2022.
- Stable published-paper locator: https://openreview.net/forum?id=WE_vluYUL-X . No conference pagination, volume, or publisher DOI verified; those fields are omitted. The arXiv DOI identifies the preprint and is not substituted for a conference DOI.
- Metadata rendered and bibliography validated using citation-management scripts. Raw extraction: `../../tmp/citation_react_*`.

## Introduction, paragraph 1 — 2026-11-23

Claim: serious harm can arise during legitimate user tasks without an external adversary. The citations support the existence of this failure mode; the paragraph makes no deployment-frequency claim.

### Kumar2026agent

- Title: The Agent Incident Registry: Toward Preventing Repeated AI Agent Failures.
- Authors, in order: Divyanshu Kumar; Rohith HN; Nitin Aravind Birur; Sahil Agarwal; Prashanth Harshangi.
- Year: 2026. First submitted September 10; current version v2, September 11.
- Metadata: extracted automatically from the citation meta tags on https://arxiv.org/abs/2609.11030 after the arXiv API timed out; rendered with the citation-management metadata formatter. Title, authors, year, identifier, and publication status checked against that official record.
- Evidence: https://arxiv.org/html/2609.11030, Section 4.4. The frozen 487-record collection includes 92 safety-failure records with no adversary-supplied trigger, of which 87 have realized outcomes. The agent-acted subset includes 82 such records and 77 realized outcomes. Do not conflate these populations or use the updated live-registry count for this paper.
- Publication enrichment: exact-title searches and the official arXiv record yielded no journal or conference publication. Cited as an arXiv preprint. Venue volume, issue, and proceedings pages are not applicable; no publisher DOI verified. Stable arXiv URL retained.

### Wang2026replication

- Title: Replication of Agentic Security Events: Audit and Investigation (ROGUE-AI).
- Authors, in order: Mengxiao Wang; Mahbub Alam; Kalyan Nakka; Nitesh Saxena.
- Year: 2026. First submitted November 19; v1.
- Metadata: extracted from the arXiv API using the citation-management extraction script, then checked against https://arxiv.org/abs/2611.26553. OpenAlex independently returned the same title, authors, year, and identifier. Acronym capitalization protected in BibTeX.
- Evidence: https://arxiv.org/html/2611.26553, Section 5 and abstract. Of 72 eligible incidents with harm in the wild, 62 had no attacker. The abstract explicitly describes agents performing the requested task while overlooking an ordinary hazard. This directly supports the sentence's conjunction of legitimate tasks, absent attackers, and harm. These are curated incident counts, not deployment rates.
- Publication enrichment: exact-title searches and the official arXiv record yielded no journal or conference publication. Cited as an arXiv preprint. Venue volume, issue, and proceedings pages are not applicable. The displayed arXiv DOI was marked pending registration, so the stable arXiv URL is used instead.

### Discovery and validation

- Searched general web/academic results and OpenAlex, then checked the official arXiv abstracts and full texts. Broad AI incident collections and individual news reports were not added to this paragraph.
- Raw discovery and extraction files: `../../tmp/citation_intro1_*`.
- Bibliography: `references.bib`; citation keys checked against `paper_skeleton.tex` with the citation-management validation script. PDF built with the official ICML 2026 bibliography style.

## Introduction, paragraph 2 — 2026-11-23

Claim: existing non-adversarial evaluations have documented unsafe behavior across diverse tasks. Only the citation placeholder was replaced; surrounding claims were preserved at the author's request.

### Ruan2024identifying — ToolEmu

- Official record: https://proceedings.iclr.cc/paper_files/paper/2024/hash/7274ed909a312d4d869cc328ad1c5f04-Abstract-Conference.html
- BibTeX automatically retrieved from the official proceedings export: https://proceedings.iclr.cc/paper_files/paper/4437-/bibtex . Title, author order, year (2024), venue (ICLR), volume (2024), and pages (27031–27098) retained from this record. The official proceedings spell the eighth author's name Chris Maddison; the PDF spells it Chris J. Maddison. The proceedings export is followed.
- Evidence: Section 3, threat model and evaluation. The underlying user intent is explicitly assumed benign; underspecified requests can lead to harmful tool actions. The benchmark covers 144 cases and 36 toolkits.
- Enrichment: official conference record and PDF confirm ICLR 2024 publication. No publisher DOI was supplied or verified; the stable OpenReview URL (https://openreview.net/forum?id=GEcwtMk1uA) is used to avoid an overlong proceedings PDF URL in the two-column reference list. Optional editor fields omitted; LM capitalization protected.

### Shayegani2026just — BLIND-ACT

- Official conference record: https://iclr.cc/virtual/2026/poster/10011107 ; paper: https://openreview.net/forum?id=9W4bPRsEIT .
- Title and all nine authors automatically extracted from https://arxiv.org/abs/2510.01670 citation meta tags, then checked against the official ICLR event page. The paper is cited as ICLR 2026, rather than the 2025 arXiv preprint. OpenAlex independently confirms the conference, author list, and year; author ordering follows the primary records.
- Evidence: Sections 2.1 and 3. The benchmark evaluates unsafe goal pursuit under contextual hazards, ambiguity, and contradictory or infeasible requests. It includes benign-intent cases; its scope also covers other contextual and feasibility failures.
- Enrichment: the official conference program and conference-paper PDF confirm ICLR 2026. No proceedings pagination, volume, or publisher DOI verified; these fields are omitted. OpenReview APIs returned HTTP 403; the official ICLR event page was accessible and used for publication verification.

### Jones2026when — AutoElicit

- Official record and BibTeX: https://proceedings.mlr.press/v306/jones26b.html . BibTeX parsed automatically from the publisher's embedded citation export.
- All nine authors, title, year (2026), venue (43rd ICML), PMLR volume (306), and pages (54549–54632) checked against the official record. Cites the published version, rather than the earlier arXiv preprint.
- Evidence: Sections 3 and 5. Unsafe unintended behaviors are defined to arise under benign instruction and environment contexts without adversarial manipulation; the evaluation surfaces such behavior in computer-use tasks.
- Enrichment: official proceedings and exact-title search confirm the publication fields. No DOI supplied or verified; publisher URL retained. Optional editor, abstract, PDF, and month fields omitted.

### Validation

- Metadata sources were fetched, then checked against official publication records and exact-title searches before bibliography formatting. Raw files are saved as `../../tmp/citation_intro2_*`.
- Bibliography formatted and deduplicated with citation-management; all five manuscript citations checked for missing keys and required fields. The PDF was rebuilt and the introduction and reference pages inspected.
