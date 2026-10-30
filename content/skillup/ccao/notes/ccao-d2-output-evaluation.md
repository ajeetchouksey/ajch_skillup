# D2: Output Evaluation and Validation

> **Exam weight**: 21% · **Questions**: ~18 in the bank

## Overview

This is the heaviest domain on the exam. It covers judging what Claude produces before anyone relies on it: checking accuracy and completeness, spotting hallucinations, inconsistencies and bias, verifying facts against real sources, deciding when a person must review, adapting output for its audience, and choosing the right format.

> 💡 **Human Angle**: Claude writes fluently whether or not it's right. Fluency is not evidence; the source is.

---

## 2.1 Evaluate Claude-generated outputs for accuracy and completeness

### Key Concept

**Check the output against two things: the request (is everything covered?) and the source (is every fact supported?).**

Accuracy means each statement is true and matches the source material. Completeness means the output does everything you asked: every requirement, section and question is covered. An answer can be accurate but incomplete (it skipped a requirement) or complete but inaccurate (it covered everything, with a wrong figure). Check both, and recompute any numbers yourself.

**Think of checking a delivery against the order form**: every item present, and every item the right one.

![Output evaluation as a set of gates: every requirement covered, every fact supported by a source, numbers recomputed, and nothing important missing, before the output is ready to use.](/content/skillup/ccao/images/ccao-2-1-accuracy-completeness.svg)

### Real use

Claude summarises a 40-page contract for a sales director. The summary reads well, but checking it against the request shows the renewal terms were never covered, and against the contract that the notice period is 60 days, not 30. Both are fixed before the summary goes to the customer meeting.

### How it works

- **Completeness:** tick off each requirement from your prompt.
- **Accuracy:** check each fact, figure and name against the source.
- **Numbers:** recompute totals, percentages and dates.
- **Omissions:** ask what's missing that the reader will expect.
- **Ask Claude for help:** "List each requirement and where you addressed it", then still check yourself.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Quick read-through | Low-stakes, internal draft | Errors can slip through |
| Requirement-by-requirement check | Output will be sent or used | Takes a few minutes |
| Line-by-line source check | Facts or figures matter (contracts, finance) | Slowest, most reliable |

### How to do it

1. List the requirements from your prompt and tick each one off.
2. Check facts and figures against the source; recompute numbers.
3. Note gaps and ask Claude to fill them, then re-check.

### Exam Trap ⚠️

<div class="note-trap">"The output is well written and confident, so it's accurate" is the trap. Fluency and confidence say nothing about correctness. Check against the request and the source.</div>

### Go deeper

- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

---

## 2.2 Identify hallucinations, inconsistencies, and biases in responses

### Key Concept

**Be most suspicious of specific details that look authoritative: citations, figures, names, dates and quotes.**

A hallucination is confident content that isn't true or isn't in the source: an invented citation, a made-up statistic, a policy section that doesn't exist. Inconsistencies are contradictions within the output (a total that doesn't match its parts, a date that changes). Bias shows up as one-sided framing, stereotypes, or assumptions about groups of people. All three can sit inside text that reads perfectly well.

**Think of a witness who fills gaps in their memory**: the story flows, but some details were never there.

![Red flags matched to checks: an exact citation or section number is checked against the source, a precise statistic is traced to its origin, contradictory figures are reconciled, and one-sided or stereotyped wording is reviewed for bias.](/content/skillup/ccao/images/ccao-2-2-red-flags.svg)

### Real use

A summary of a new regulation cites "Section 4.2(b)" with confidence. The section exists, but says something different. Elsewhere, a candidate-shortlist summary describes one applicant as "energetic and young" and another as "experienced but may struggle with new tools", which is age bias that would never go into a hiring record.

### How it works

- **Hallucination signals:** exact citations, statistics, quotes, URLs, names you didn't provide.
- **Inconsistency signals:** totals that don't add up, changing dates or names, contradictions between sections.
- **Bias signals:** loaded wording, stereotypes, assumptions about groups, one-sided comparisons.
- **Self-reported confidence** is not evidence of accuracy.
- **Reduce the risk up front:** give Claude the source, ask it to answer only from it, and allow "I don't know".

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Spot-check high-risk details | Most business outputs | Misses subtle errors |
| Check every specific claim | Compliance, legal, external content | Time-consuming |
| Bias review by a second person | Output affects people (hiring, reviews) | Needs a reviewer |

### How to do it

1. Highlight every citation, figure, name, date and quote.
2. Check each against the source, and the totals against their parts.
3. Read for wording about people and groups; rewrite anything biased.

### Exam Trap ⚠️

<div class="note-trap">"Ask Claude how confident it is and trust high confidence" is wrong: self-rated confidence isn't a reliable signal. Verify specific claims against the source.</div>

### Go deeper

- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

---

## 2.3 Apply fact-checking and validation techniques

### Key Concept

**Verify against authoritative sources, not against Claude: ask for the source and the exact quote, then check them yourself.**

Fact-checking means confirming a claim with evidence outside the conversation. Useful techniques: give Claude the source document and ask it to quote the passage behind each claim; ask Research for cited sources and open them; cross-check important facts with a second independent source; recompute numbers; and explicitly allow Claude to say "I don't know" rather than guess. Asking Claude "are you sure?" is not verification.

**Think of a journalist's two-source rule**: a story runs only when the facts are confirmed independently.

![The fact-checking path: a claim is matched to a quoted passage or cited source, the source is opened and compared, and the claim is kept, corrected or removed; asking Claude whether it is sure is not a check.](/content/skillup/ccao/images/ccao-2-3-fact-check.svg)

### Real use

A policy analyst asks Claude to brief leadership on a new data-protection rule, uploading the official text. She tells Claude to quote the clause supporting each point and to say "not covered" where the text is silent. She then checks three key quotes against the official text before sending.

### How it works

- **Ground it:** provide the source; ask Claude to answer only from it.
- **Quote first:** ask for the exact passage behind each claim.
- **Cite and open:** Research and web search give citations; open them and check.
- **Second source:** confirm key facts independently.
- **Recompute:** do the arithmetic yourself.
- **Allow uncertainty:** "If the document doesn't say, write 'not stated'."

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Quote-from-source | You have the source document | Only as good as the document |
| Research with citations | Facts are spread across the web | Citations still need opening |
| Independent second source | High-stakes facts | Takes more time |

### How to do it

1. Give Claude the authoritative source and ask it to quote support for each claim.
2. Open and check citations or quotes for the important claims.
3. Remove or correct anything you can't confirm.

### Exam Trap ⚠️

<div class="note-trap">"Ask Claude to double-check its own answer" isn't fact-checking; it's the same source checking itself. Validation needs an authoritative source outside the conversation.</div>

### Go deeper

- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
- [Use Research on Claude](https://support.claude.com/en/articles/11088861-use-research-on-claude)

---

## 2.4 Determine when human review or additional verification is required

### Key Concept

**The higher the stakes and the wider the audience, the more a qualified person must check before the output is used.**

Not every output needs the same scrutiny. A brainstorm for your own use needs none. An internal summary needs a quick check. Anything external, regulated, financial, legal, medical, or affecting people's jobs or rights needs review by a person qualified to judge it. Anthropic's Usage Policy requires a qualified human in the loop for high-risk uses that affect people's health, legal rights, finances or livelihood.

**Think of the "four eyes" rule in finance**: the bigger the payment, the more sign-offs it needs.

![A review matrix: low-stakes personal work needs no review, internal work a quick check, external or customer-facing work a reviewer, and decisions affecting people's money, health, legal rights or jobs need a qualified expert before use.](/content/skillup/ccao/images/ccao-2-4-review-matrix.svg)

### Real use

A team uses Claude for three things: drafting internal meeting notes (author skims them), customer emails (a team lead reviews templates before use), and summarising employee performance feedback for promotion decisions (HR reviews every summary, and the decision stays with the manager).

### How it works

- **Stakes:** what happens if it's wrong? Money, legal exposure, harm to people.
- **Audience:** just you, your team, the whole company, customers, the public.
- **Domain expertise:** legal, medical, financial or regulated content needs a qualified reviewer.
- **Novelty:** first-time use cases get more review until trusted.
- **Human-in-the-loop:** high-risk decisions about people need a person with authority to change them.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| No review | Personal drafts and ideas | Never for anything shared |
| Self-check | Internal, low-stakes output | Your own blind spots remain |
| Expert review | External, regulated or people-affecting | Slower; needs a reviewer |

### How to do it

1. Ask: who will see this, and what happens if it's wrong?
2. Match the review level to the answer.
3. For high-stakes work, a qualified person reviews and owns the decision.

### Exam Trap ⚠️

<div class="note-trap">"Claude is usually accurate, so skip review to save time" fails for external or high-stakes work. And "review everything line by line" wastes effort on low-stakes drafts. Scale review to stakes and audience.</div>

### Go deeper

- [2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update)

---

## 2.5 Edit, adapt, refine, and compare outputs for the intended audience

### Key Concept

**Shape the same content for each reader: what they already know, what they need to decide, and how much time they'll give it.**

One set of findings may need to become an executive summary, a team briefing and a customer FAQ. Each audience needs a different length, vocabulary, level of detail and call to action. Claude adapts well when you name the audience and their need. Asking for two or three versions side by side lets you compare approaches and pick or combine the best.

**Think of explaining the same news to your CEO, your team and a customer**: same facts, three different conversations.

![The same project findings adapted for three audiences: a three-line executive summary with the decision needed, a team briefing with actions and owners, and a customer FAQ in plain language.](/content/skillup/ccao/images/ccao-2-5-audiences.svg)

### Real use

A product manager has a detailed release report. She asks Claude for a three-line summary for the leadership channel, a version for support agents focused on what changes for customers, and a plain-language customer note. She compares two versions of the customer note and keeps the clearer one.

### How it works

- **Name the audience** and what they need to do with the output.
- **Adjust** length, vocabulary, detail and tone.
- **Compare versions:** ask for two or three and pick or merge.
- **Edit yourself:** add context Claude can't know; remove anything inaccurate.
- **Consistency:** every version must state the same facts.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| One version for all | Everyone has similar needs | Too much detail for some, too little for others |
| Version per audience | Readers differ in role or expertise | More to review |
| Side-by-side alternatives | You're unsure which approach works | Extra reading to compare |

### How to do it

1. List each audience and what they need to know or decide.
2. Ask Claude for a version per audience, or two alternatives to compare.
3. Check every version states the same facts, then edit for your voice.

### Exam Trap ⚠️

<div class="note-trap">"Send the detailed version to everyone so nothing is lost" ignores the reader. And adapting must never change the facts: a simpler version can leave detail out, not alter it.</div>

### Go deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

---

## 2.6 Organize and curate information and select appropriate output formats (artifacts, inline, structured data)

### Key Concept

**Choose the format by what happens next: read once means inline, reuse or share means an artifact or file, and feeding another tool means structured data.**

Inline text in the chat suits quick answers you'll read and move on from. An artifact is a self-contained output beside the chat, such as a document, dashboard or small interactive tool, that you can keep editing, export or share. Claude can also create downloadable files (Word, Excel, PowerPoint, PDF) when file creation is turned on. Structured data, such as a table, CSV or JSON, suits anything another system or spreadsheet will use. Curating means organising content into a clear structure with headings, groups and priorities.

**Think of sticky notes, a report and a spreadsheet**: each suits a different next step.

![Format follows the next step: a quick answer stays inline, a document or tool to keep or share becomes an artifact or file, and data for a spreadsheet or another tool becomes structured data such as a table or CSV.](/content/skillup/ccao/images/ccao-2-6-formats.svg)

### Real use

An event coordinator asks for a quick answer about venue capacity rules (inline), then a run-of-show document she'll edit with the team (artifact, exported to Word), and finally the attendee list cleaned into columns for the registration system (structured data, CSV).

### How it works

- **Inline:** quick answers, explanations, short drafts.
- **Artifact:** documents, dashboards, small tools you'll refine, export or share.
- **Files:** Word, Excel, PowerPoint, PDF via file creation (code execution must be on).
- **Structured data:** tables, CSV or JSON for spreadsheets and other tools.
- **Curate:** group, order by priority, add headings and a summary first.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Inline | Read once, move on | Hard to reuse |
| Artifact or file | Reuse, edit, export or share | Needs the capability turned on |
| Structured data | Another tool or spreadsheet will use it | Less readable as prose |

### How to do it

1. Decide what happens to the output next.
2. Ask for that format explicitly, with columns or sections named.
3. Check structure and contents before exporting or sharing.

### Exam Trap ⚠️

<div class="note-trap">Asking for a long prose report when the data is headed into a spreadsheet creates manual rework. Pick the format for the next step. And artifacts and file creation depend on the code execution setting being enabled.</div>

### Go deeper

- [What are artifacts and how do I use them?](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them)
- [Create and edit files with Claude](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)

---

## Deep Dive: Making Output Evaluation Click

### 1. The connective narrative

This domain is the safety net under everything else. Checking accuracy and completeness (2.1) catches what went wrong; knowing the red flags (2.2) tells you where to look; fact-checking (2.3) is how you confirm. Deciding the review level (2.4) scales that effort to the stakes. Adapting for the audience (2.5) and choosing the format (2.6) make sure correct content actually works for the person who receives it.

### 2. Worked scenario

> **Scenario.** A compliance associate asks Claude to summarise a new regulation for the sales team. She uploads the official text and asks for quotes behind each point (2.3). One summary cites a sub-clause that says something else, and she corrects it (2.2). She ticks off every requirement in her prompt (2.1). Because the guidance will change how salespeople talk to customers, the legal team reviews it (2.4). She produces a one-page briefing for sales and a short FAQ (2.5), saved as an artifact the team can update (2.6).

### 3. Memory aid

**SOURCE**: **S**cope covered? · **O**rigin of each fact? · **U**nusual specifics flagged? · **R**eview level set? · **C**hanged for the audience? · **E**xport format right?

### 4. Exam strategy for this domain

The tempting wrong answers trust signals that aren't evidence: confidence, fluency, formality, or Claude checking itself. The right answer checks against an authoritative source, and scales human review to the stakes and audience.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Confident citation or section number | Verify against the official source |
| "Ask Claude if it's sure" | Not verification |
| Totals don't match parts | Inconsistency: reconcile |
| Wording about age or gender in hiring notes | Bias: rewrite and review |
| Output for customers or regulators | Qualified human review |
| Decision affects someone's job or money | Human in the loop with authority |
| Same findings for execs and customers | Version per audience, same facts |
| Data going to a spreadsheet | Structured data (table or CSV) |
| Document the team will keep editing | Artifact or file |
