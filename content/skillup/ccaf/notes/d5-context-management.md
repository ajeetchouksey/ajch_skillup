# D5: Context Management & Reliability

> **Exam weight**: 15% · **Questions**: ~48 in the bank

## Overview

This domain covers keeping agents accurate over long, messy work: preserving critical facts as context grows, knowing when to escalate to a human, propagating errors usefully between agents, managing context while exploring large codebases, calibrating human review, and keeping track of where every claim came from.

> 💡 **Human Angle**: Long-running agents rarely fail all at once. They drift: a number gets rounded, a source gets dropped, an error gets swallowed. Reliability is about catching drift before it reaches a customer.

---

## 5.1 Manage conversation context to preserve critical information across long interactions

### Key Concept

**Keep exact facts out of the summary: store amounts, dates and IDs in a persistent case-facts block, and trim tool output before it piles up.**

Progressive summarisation turns "$1,247.50 refund promised by 14 November" into "customer wants a refund". Models also handle the start and end of long inputs better than the middle ("lost in the middle"), and verbose tool results consume tokens far beyond their value. Keep a structured case-facts block (amounts, dates, order numbers, statuses, what the customer was told) in every prompt, outside the summarised history; trim tool outputs to the fields that matter; put key findings first, with clear headers.

**Think of a hospital chart**: the nurse's notes get summarised at handover, but the allergy list is always at the top, word for word.

![A persistent case-facts block with exact amounts, dates and IDs sits outside the summarised history, tool outputs are trimmed to relevant fields, and key findings go at the start of long inputs.](/content/skillup/ccaf/images/ccaf-5-1-context-preservation.svg)

### Real use

In long billing disputes a support agent starts misquoting order IDs and amounts it confirmed 30 turns earlier, after older turns were compacted. Extracting those facts into a case-facts block that's included in every request, and trimming order-lookup results to five fields, stops the errors.

### How it works

- **Case facts**: exact values, outside summarised history, in every prompt.
- **Trim tool output**: keep only relevant fields before it enters context.
- **Position**: key findings at the start; detail under explicit section headers.
- **Full history in API calls**: the API is stateless, so each request must carry the conversation.
- **Upstream agents return structured data** (facts, citations, relevance scores), not long reasoning, when downstream context is tight.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Case-facts block | Exact values must survive long sessions | Must be kept up to date |
| Trim tool output | Tools return large payloads | Might drop something needed later |
| Summarise history | Old turns are no longer needed verbatim | Loses precision |

### How to do it

1. Identify facts that must stay exact and keep them in a structured block.
2. Filter tool results to the needed fields as they arrive.
3. Put summaries first and organise long inputs with headers.

### Exam Trap ⚠️

<div class="note-trap">"Use a model with a larger context window" doesn't stop summaries from rounding "37.4%" into "about a third". Exact facts need to be kept outside the summary.</div>

### Go deeper

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Long context prompting tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips)

---

## 5.2 Design effective escalation and ambiguity resolution patterns

### Key Concept

**Escalate when the customer asks for a human, when policy doesn't cover the case, or when the agent can't make progress, not because the customer sounds upset.**

Good triggers are explicit: a request for a human (honour it immediately, without first investigating), a policy exception or gap, or no meaningful progress. Sentiment and the model's self-reported confidence are poor proxies for how hard a case is. When a lookup returns several matching customers, ask for another identifier rather than picking one by heuristic. Put the criteria in the system prompt, with examples of escalating versus resolving.

**Think of a good receptionist**: they put you through when you ask for the manager, and they don't when you're merely annoyed about something they can fix.

![Escalation triggers are an explicit request for a human, a policy gap or no progress, while frustration alone is resolved by the agent; multiple customer matches lead to asking for another identifier.](/content/skillup/ccaf/images/ccaf-5-2-escalation.svg)

### Real use

A support agent escalates routine returns whenever the customer sounds frustrated, yet keeps going after a customer says "let me talk to a person". New system-prompt criteria with examples fix both: frustration over a simple return is resolved; an explicit request goes straight to a human.

### How it works

- **Explicit request for a human**: escalate immediately.
- **Policy silent or ambiguous**: escalate.
- **No progress**: escalate.
- **Straightforward issue, upset customer**: offer to resolve.
- **Multiple matches**: ask for an additional identifier.
- **Not triggers**: sentiment scores, self-reported confidence.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Escalate at once | Customer asks for a human | No chance to resolve |
| Resolve autonomously | Clear issue within policy | Customer may still be upset |
| Ask for an identifier | Several records match | One extra exchange |

### How to do it

1. Write explicit escalation criteria in the system prompt.
2. Add few-shot examples of escalate versus resolve, including frustrated-but-simple cases.
3. Instruct the agent to ask for another identifier when results are ambiguous.

### Exam Trap ⚠️

<div class="note-trap">"Escalate when sentiment is negative" and "escalate when confidence is below 70%" sound reasonable, but the exam treats both as unreliable proxies. And "investigate first" is wrong when the customer has explicitly asked for a human.</div>

### Go deeper

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

---

## 5.3 Implement error propagation strategies across multi-agent systems

### Key Concept

**Pass failures up with enough context to decide what to do next; never hide them, and never let one failure stop everything.**

When a subagent fails, the coordinator needs the failure type, what was attempted, any partial results and possible alternatives. "Search unavailable" hides all of that. An access failure (timeout) is different from a valid empty result (the search worked, nothing matched), and the coordinator must be able to tell them apart. Subagents handle transient failures locally and propagate only what they can't fix. The final synthesis notes which findings are well supported and where coverage has gaps.

**Think of a field report**: "couldn't reach site B because the road was flooded; site A done; try the north route" lets headquarters re-plan.

![A failed subagent returns structured error context with failure type, attempted query, partial results and alternatives; the coordinator retries, reroutes or continues, and the final report annotates gaps instead of hiding them.](/content/skillup/ccaf/images/ccaf-5-3-error-propagation.svg)

### Real use

A `data_analyzer` occasionally fails on a malformed dataset and returns "No significant findings", which the report presents as a real result. Changing it to return a structured failure (type, dataset, partial results, suggested alternative) lets the coordinator retry with a cleaned dataset or mark the gap in the report.

### How it works

- **Structured error context**: failure type, query attempted, partial results, alternatives.
- **Access failure vs empty result**: different meaning, different action.
- **Local recovery** for transient errors inside the subagent.
- **Anti-patterns**: silently suppressing errors; terminating the whole workflow on one failure.
- **Coverage annotations** in the synthesis.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Retry locally | Transient error in a subagent | Adds latency |
| Propagate with context | Subagent can't resolve it | Coordinator logic needed |
| Continue with annotated gap | Other parts succeeded | Report is incomplete, honestly |

### How to do it

1. Define an error object: type, attempted action, partial results, alternatives.
2. Retry transient failures in the subagent; propagate the rest.
3. Have the synthesis mark weak or missing coverage explicitly.

### Exam Trap ⚠️

<div class="note-trap">Two opposite anti-patterns: returning "no findings" on failure (suppression), and aborting the whole pipeline because one subagent failed. The answer is structured propagation plus partial results.</div>

### Go deeper

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

---

## 5.4 Manage context effectively in large codebase exploration

### Key Concept

**Delegate noisy exploration to subagents, write key findings to a scratchpad file, and checkpoint state so a crash doesn't mean starting over.**

In long exploration sessions, models start giving inconsistent answers and refer to "typical patterns" instead of the specific classes they found earlier: context has degraded. Subagents can investigate specific questions in their own context and return summaries, while the main agent keeps the big picture. Scratchpad files persist key findings across context boundaries. Summarise each phase before the next, use `/compact` when context fills with discovery output, and have each agent export state to a known location so the coordinator can reload a manifest after a crash.

**Think of an expedition with a field notebook**: scouts go ahead and report back, the notebook keeps what's been found, and a camp map lets a new team pick up where the last stopped.

![The main agent sends subagents to investigate specific questions and receives summaries, records key findings in a scratchpad file, compacts when context fills, and each agent exports state to a manifest the coordinator reloads after a crash.](/content/skillup/ccaf/images/ccaf-5-4-codebase-exploration.svg)

### Real use

Asked how a legacy billing module works, the main agent reads dozens of files and its context fills with file contents. Delegating each question to an Explore subagent, and recording findings in `NOTES.md`, keeps answers specific. A 45-minute research run that crashes during synthesis resumes from its manifest without re-running search and analysis.

### How it works

- **Context degradation**: vague, inconsistent answers late in long sessions.
- **Subagent delegation**: verbose output stays in the subagent's context.
- **Scratchpad files**: record findings; re-read them for later questions.
- **Phase summaries**: inject them into the next phase's subagents.
- **`/compact`**: reduce context during extended sessions.
- **Crash recovery**: each agent exports state; the coordinator loads a manifest and injects it on resume.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Subagent exploration | Discovery output is large | Detail stays in the subagent |
| Scratchpad file | Findings must outlive the context | Must be kept current |
| State manifests | Long runs that may crash | Export logic in every agent |

### How to do it

1. Send specific questions to subagents; keep the main agent on coordination.
2. Write key findings to a scratchpad file and consult it for later questions.
3. Export each agent's state to a known location and reload it on resume.

### Exam Trap ⚠️

<div class="note-trap">"Read all files into the main context up front" causes the degradation the exam describes. "Just resume the session" after a crash doesn't restore lost subagent work; structured state exports do.</div>

### Go deeper

- [Create custom subagents in Claude Code](https://code.claude.com/docs/en/sub-agents)

---

## 5.5 Design human review workflows and confidence calibration

### Key Concept

**Don't trust the overall accuracy figure: check each document type and field, calibrate confidence against labelled data, and keep sampling.**

97% overall accuracy can hide a document type that's wrong a third of the time. Before reducing human review, measure accuracy by document type and by field. Have the model output field-level confidence, then set review thresholds using a labelled validation set, since raw confidence isn't calibrated. Route low-confidence or contradictory extractions to people, and keep sampling high-confidence ones at random, stratified by type, to measure the real error rate and catch new error patterns.

**Think of a quality inspector**: they test every product line separately and keep spot-checking the ones that usually pass.

![Overall accuracy is broken down by document type and field, confidence thresholds are calibrated on labelled data, low-confidence items go to human review, and stratified random samples of high-confidence items keep measuring the error rate.](/content/skillup/ccaf/images/ccaf-5-5-human-review.svg)

### Real use

An invoice pipeline reports 97% accuracy, and the team plans to stop human review. Segmenting shows handwritten receipts at 71% for the total field. They keep review for that segment, set thresholds from a labelled set, and sample 2% of high-confidence extractions from every type each week.

### How it works

- **Aggregate metrics mask segments**: break down by document type and field.
- **Field-level confidence**: per field, not per document.
- **Calibrate** thresholds on a labelled validation set.
- **Route**: low confidence or contradictory sources go to people first.
- **Stratified random sampling** of high-confidence output: ongoing error measurement and new-pattern detection.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Segment analysis | Before reducing human review | Needs labelled data per segment |
| Calibrated thresholds | Routing review by confidence | Recalibrate when data shifts |
| Stratified sampling | Ongoing, after automation | Reviewer time on "good" items |

### How to do it

1. Measure accuracy per document type and field on labelled data.
2. Calibrate field-level confidence thresholds against that data.
3. Route low-confidence items to review; sample high-confidence ones by stratum.

### Exam Trap ⚠️

<div class="note-trap">"97% overall accuracy, so automate everything" is the trap. So is trusting the model's raw confidence without calibration. And sampling only low-confidence items never measures how often high-confidence ones are wrong.</div>

### Go deeper

- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

---

## 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis

### Key Concept

**Carry a source with every claim through every step, and when sources disagree, show the disagreement instead of picking a number.**

Summarisation strips attribution unless claim-to-source mappings are kept as structured data that each agent preserves and merges. Subagents should output claims with source URL or document name, an excerpt, and the publication or collection date; dates stop a 2019 figure and a 2025 figure being read as a contradiction. When credible sources conflict, record both values with their sources and let the coordinator decide how to reconcile. Final reports separate established findings from contested ones and format each content type suitably.

**Think of a court record**: every statement is tied to a witness and a date, and conflicting testimony is recorded, not quietly resolved.

![Subagents output claims with source, excerpt and date; the synthesis keeps claim-source mappings, annotates conflicting values with both sources, and separates established from contested findings.](/content/skillup/ccaf/images/ccaf-5-6-provenance.svg)

### Real use

Two reports give the market size as $4.2B and $5.1B. The first draft of a synthesis picked one and dropped the citation. The fixed pipeline shows both with their sources and dates (2023 vs 2025), explains the difference in methodology, and puts the figure under "contested".

### How it works

- **Claim-source mappings**: URL or document, excerpt, date for every claim.
- **Preserve through synthesis**: merge mappings; don't compress them away.
- **Conflicts**: keep both values with attribution; let the coordinator reconcile.
- **Dates**: required, so time differences aren't mistaken for contradictions.
- **Structure**: established vs contested sections; tables for financial data, prose for news, lists for technical findings.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Structured claim-source output | Any multi-source synthesis | More fields per claim |
| Annotate conflicts | Credible sources disagree | Report is less tidy |
| Require dates | Data can change over time | Sources may lack dates |

### How to do it

1. Make subagents return claims with source, excerpt and date.
2. Require the synthesis agent to keep and merge those mappings.
3. Flag conflicts with both sources; separate established from contested findings.

### Exam Trap ⚠️

<div class="note-trap">Picking "the most recent" or "the most authoritative" value and dropping the other is the distractor; the exam wants the conflict annotated with sources. And a summary that keeps the claim but drops its source has lost provenance.</div>

### Go deeper

- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)

---

## Deep Dive: Making Context Management & Reliability Click

### 1. The connective narrative

Every lesson here protects information as it moves: through time in one conversation (5.1), from agent to human (5.2), between agents when something fails (5.3), across context boundaries in long exploration (5.4), from model to reviewer (5.5), and from source to final report (5.6). Each time, the risk is the same: information gets compressed, dropped or misread, and the agent carries on confidently.

The remedies share a pattern: make important things explicit and structured. Case facts instead of summaries, escalation criteria instead of sentiment, error objects instead of "failed", scratchpads and manifests instead of memory, calibrated thresholds instead of raw confidence, claim-source mappings instead of prose.

### 2. Worked scenario

> **Scenario.** A research pipeline runs for an hour across search, analysis and synthesis agents. Each subagent returns claims with source, excerpt and date (5.6), trimmed to relevant fields (5.1). When the analyser hits a rate limit it retries locally; a malformed dataset comes back as a structured failure, and the report marks the gap (5.3).
>
> Each agent exports state to a manifest, so a crash during synthesis resumes without repeating search (5.4). Conflicting statistics appear with both sources under "contested". Before automating publication, the team checks accuracy by report type and keeps sampling high-confidence outputs (5.5).

### 3. Memory aid

**KEEP IT EXPLICIT**: facts in a block, criteria in the prompt, errors as objects, findings in files, confidence calibrated, sources attached.

### 4. Exam strategy for this domain

The wrong answers usually rely on something implicit: the summary will keep the number, the model will sense when to escalate, "no results" means no results, overall accuracy means every segment is fine. Pick the option that makes the critical information explicit and structured.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Amounts and IDs drift in long sessions | Persistent case-facts block |
| Tool results fill context | Trim to relevant fields |
| Middle findings get missed | Key findings first, with headers |
| Customer asks for a human | Escalate immediately |
| Customer frustrated, simple issue | Resolve; don't escalate on sentiment |
| Several customers match | Ask for another identifier |
| Subagent returns "no findings" on failure | Return structured error context |
| One subagent fails | Don't abort; propagate and annotate the gap |
| Vague answers late in exploration | Subagents + scratchpad file |
| Crash mid-run | Reload state manifest |
| 97% overall accuracy | Check by document type and field first |
| Route human review | Calibrated field-level confidence |
| Measure ongoing error rate | Stratified random sampling |
| Sources disagree | Show both, with attribution and dates |
