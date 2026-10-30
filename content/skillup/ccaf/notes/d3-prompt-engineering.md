# D3: Prompt Engineering & Structured Output

> **Exam weight**: 20% · **Questions**: ~58 in the bank · Official exam guide numbering: Domain 4, objectives 4.1–4.6

## Overview

This domain covers how to get precise, consistent and machine-usable output from Claude: explicit criteria instead of vague instructions, few-shot examples, structured output through tool use and JSON schemas, validation and retry loops, the Message Batches API for latency-tolerant work, and review architectures that use independent instances and multiple passes.

> 💡 **Human Angle**: A reviewer that flags everything gets ignored, and then its real findings get ignored too. Precision is what earns trust.

---

## 4.1 Design prompts with explicit criteria to improve precision and reduce false positives

### Key Concept

**Say exactly what to report and what to skip; "be conservative" doesn't improve precision, categorical criteria do.**

Vague instructions such as "check that comments are accurate", "be conservative" or "only report high-confidence findings" leave the model to guess the threshold. Explicit criteria define the categories: "flag a comment only when its claimed behaviour contradicts what the code does", "report bugs and security issues; skip minor style and local patterns". Define each severity level with a concrete code example so classification is consistent.

**Think of a smoke alarm that goes off for toast**: after a week, nobody reacts, even to real smoke.

![A vague instruction such as be conservative produces noisy findings that developers learn to ignore, while explicit report and skip categories with severity examples produce precise findings that developers trust.](/content/skillup/ccaf/images/ccaf-4-1-explicit-criteria.svg)

### Real use

A code-review bot's "comment accuracy" findings are wrong half the time, and developers start dismissing all its findings, including real security issues. The team disables that category while rewriting its criteria with examples, and trust in the other categories recovers.

### How it works

- **Report vs skip**: list categories to report (bugs, security) and to ignore (style, local conventions).
- **Concrete conditions**: "contradicts actual behaviour", not "inaccurate".
- **Severity with examples**: one code example per level.
- **False positives spread distrust**: one noisy category undermines accurate ones.
- **Temporarily disable** a high false-positive category while you fix its prompt.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Explicit categorical criteria | Any review or classification task | Takes effort to define |
| Disable a noisy category | Its false positives are eroding trust | Real issues in it go unflagged meanwhile |
| Confidence filtering ("only if sure") | Not as the main precision lever | Doesn't define what to report |

### How to do it

1. List what to report and what to skip, with the condition for each.
2. Add one concrete example per severity level.
3. Measure false positives per category and switch off the worst until fixed.

### Exam Trap ⚠️

<div class="note-trap">"Tell the model to be more conservative" or "only report high-confidence issues" is the classic distractor. The exam's answer is specific criteria that define which issues count.</div>

### Go deeper

- [Be clear, direct and detailed](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct)

---

## 4.2 Apply few-shot prompting to improve output consistency and quality

### Key Concept

**When instructions alone give inconsistent output, two to four well-chosen examples fix format and teach judgement for ambiguous cases.**

Few-shot examples show the exact output wanted (location, issue, severity, suggested fix) and how to handle the hard cases. The best examples cover ambiguous scenarios and explain why one action was chosen over a plausible alternative, so the model generalises the judgement to new patterns rather than matching only the listed ones. In extraction, examples from varied document layouts reduce empty or invented fields.

**Think of training a new reviewer with marked-up past reviews**: they learn the format and, more importantly, where the line is.

![Two to four examples, each showing an input, the reasoning and the output, lead to consistent format, correct handling of ambiguous cases and generalisation to new patterns.](/content/skillup/ccaf/images/ccaf-4-2-few-shot.svg)

### Real use

An extraction pipeline often returns `null` for the invoice date on supplier invoices that put it in a footer. Adding two examples, one with the date in a header and one in a footer, each showing the correct extraction, fixes the empty fields without a longer instruction.

### How it works

- **2–4 targeted examples**, focused on the ambiguous cases.
- **Show reasoning**: why this action and not the plausible alternative.
- **Show the format**: the exact fields and order you want.
- **Acceptable vs issue**: examples of code that looks suspicious but is fine reduce false positives.
- **Varied documents**: examples from different layouts improve extraction.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Few-shot examples | Format or judgement is inconsistent | Longer prompt |
| More instructions | A rule is simply missing | Often still inconsistent |
| Many near-identical examples | Never | Model copies surface patterns |

### How to do it

1. Collect real cases where output went wrong or was ambiguous.
2. Write 2–4 examples covering them, with input, reasoning and the exact output.
3. Vary the examples so the model learns the principle, not one pattern.

### Exam Trap ⚠️

<div class="note-trap">When detailed instructions already exist and output is still inconsistent, "add more instructions" is the distractor; examples are the answer. And examples that all look alike teach the surface, not the judgement.</div>

### Go deeper

- [Use examples (multishot prompting)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting)

---

## 4.3 Enforce structured output using tool use and JSON schemas

### Key Concept

**A tool with a JSON schema gives you schema-shaped output; the schema fixes the structure, not whether the values are true.**

Define an extraction tool whose `input_schema` is the structure you want, and read the data from the `tool_use` block. `tool_choice` controls whether a tool must be called: `auto` lets the model decide, `any` forces some tool call, and `{"type": "tool", "name": "extract_metadata"}` forces that tool. Structured outputs (`strict: true` on a tool, or `output_config.format`) constrain decoding so responses always match the schema. Design schemas so the model can be honest: nullable fields for information that may be absent, and enums with `unclear` or `other` plus a detail field.

**Think of a form with fixed boxes**: it guarantees every answer is in the right box, not that every answer is right.

![An extraction tool with a JSON schema, tool_choice any or a forced tool, and strict mode yields schema-valid output; nullable fields and other or unclear enum values stop the model inventing values, while semantic checks still run afterwards.](/content/skillup/ccaf/images/ccaf-4-3-structured-output.svg)

### Real use

A feedback pipeline must output product mentions and a priority. With a strict tool schema every response parses. Making `product` nullable stops invented product names when a document mentions none, and a `category` enum with `other` plus `category_detail` handles new themes without schema changes.

### How it works

- **Tool use**: the schema is the tool's `input_schema`; data arrives in `tool_use.input`.
- **`tool_choice`**: `auto` (may answer in text), `any` (must call a tool; good when the document type is unknown and several schemas exist), forced (a specific tool first).
- **Strict mode**: constrained decoding; valid JSON unless the model refuses or hits `max_tokens`.
- **Unsupported constraints** such as `minimum`/`maximum` go in descriptions and your own validation.
- **Semantic errors** (wrong values, totals that don't add up) still need validation (4.4).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `tool_choice: any` | Several schemas, document type unknown | Model picks which tool |
| Forced tool | One extraction must run first | No flexibility |
| Nullable / `unclear` / `other` | Source may lack or blur the data | Downstream must handle nulls |

### How to do it

1. Define the extraction tool with the schema as `input_schema`; enable strict mode.
2. Set `tool_choice` to `any` or force the tool.
3. Make optional data nullable and add `unclear` and `other` + detail where categories vary.

### Exam Trap ⚠️

<div class="note-trap">"Ask for JSON in the prompt and parse it" is the unreliable option. And a schema-valid response can still be wrong: required, non-nullable fields push the model to invent values when the document has none.</div>

### Go deeper

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

---

## 4.4 Implement validation, retry, and feedback loops for extraction quality

### Key Concept

**Retry with the specific error and it usually self-corrects; if the information isn't in the document, no retry will find it.**

After extraction, validate the meaning: do line items add up to the total, is each field in the right place? On failure, send a follow-up with the original document, the failed extraction and the specific validation errors. That works for format and structural mistakes, but not when the source simply lacks the data. Extract a `calculated_total` alongside the `stated_total` so discrepancies flag themselves, and add a `detected_pattern` field to findings so you can analyse which patterns developers dismiss.

**Think of a teacher returning homework with the mistakes circled**: the student can fix what's circled, but not a question about a chapter they were never given.

![After extraction, semantic validation passes good records; failures with fixable errors are retried with the document, the failed output and specific errors, while missing information is flagged instead of retried.](/content/skillup/ccaf/images/ccaf-4-4-retry-feedback.svg)

### Real use

Invoice extractions sometimes have line items that don't sum to the total. The pipeline extracts both `stated_total` and `calculated_total`, retries mismatches with the exact difference in the prompt, and sends documents with no total at all to human review instead of retrying them.

### How it works

- **Semantic validation**: sums, ranges, cross-field consistency (structure is already guaranteed by tool use).
- **Retry with feedback**: original document + failed output + specific errors.
- **Know when to stop**: absent information won't appear on retry.
- **Self-checking fields**: `calculated_total` vs `stated_total`.
- **`detected_pattern`**: lets you find which code constructs cause dismissed findings.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Retry with specific errors | Format, placement or arithmetic mistakes | Extra call |
| Flag, don't retry | Data is missing from the source | Needs a human or a null |
| Blind retry ("try again") | Never | Same mistake again |

### How to do it

1. Add semantic checks after extraction.
2. On failure, resend document, failed extraction and the exact errors.
3. If the data isn't in the document, mark it missing and stop retrying.

### Exam Trap ⚠️

<div class="note-trap">Retrying more times won't extract a value the document doesn't contain. And a retry that just says "try again" without the validation errors gives the model nothing to correct.</div>

### Go deeper

- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

---

## 4.5 Design efficient batch processing strategies

### Key Concept

**Use the Message Batches API for work that can wait: half the price, results within 24 hours, no latency guarantee.**

The Message Batches API processes large sets of requests asynchronously at 50% of standard cost, with results available within 24 hours and no guaranteed latency. That suits overnight reports, weekly audits and nightly test generation, not pre-merge checks that block a developer. Each request carries a `custom_id`; results don't come back in submission order, so match them by `custom_id`. A batch request is a single turn, so multi-turn tool-calling loops don't fit inside one.

**Think of an overnight laundry service**: cheaper than doing it while you wait, but you don't send the shirt you need in an hour.

![Blocking pre-merge checks go to the synchronous Messages API, while overnight and weekly jobs go to the Batches API at half the cost; results are matched by custom_id and only failed items are resubmitted.](/content/skillup/ccaf/images/ccaf-4-5-batch.svg)

### Real use

A team processes 100,000 feedback documents each night. It refines the prompt on a sample first, submits the batch, matches results by `custom_id`, and resubmits only the 300 `errored` and 40 `expired` items. The pre-merge code review stays on the synchronous API.

### How it works

- **Cost and timing**: 50% discount; up to 24 hours; no SLA.
- **Fit**: latency-tolerant, non-blocking workloads.
- **`custom_id`**: correlates each result with its request.
- **Failures**: resubmit only failed items by `custom_id`, with fixes if needed.
- **Single turn**: no multi-turn tool use inside one batch request.
- **Plan submissions** so results land before the deadline the SLA allows.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Batches API | Overnight, weekly or bulk jobs | Up to 24 h to complete |
| Synchronous API | A person or pipeline is waiting | Full price |
| Sample run first | Before any large batch | One extra small run |

### How to do it

1. Refine the prompt on a representative sample.
2. Submit with a unique `custom_id` per document, early enough for your deadline.
3. Match results by `custom_id`; resubmit only failed or expired ones.

### Exam Trap ⚠️

<div class="note-trap">Moving blocking pre-merge checks to batches "for the 50% discount" is wrong: there's no latency guarantee. Assuming results come back in order is wrong too; use <code>custom_id</code>. And don't resubmit the whole batch when a few items fail.</div>

### Go deeper

- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

---

## 4.6 Design multi-instance and multi-pass review architectures

### Key Concept

**A fresh instance reviews better than the one that wrote the code, and per-file passes plus an integration pass review better than one giant pass.**

A model reviewing its own work in the same session still carries the reasoning that produced it, so it tends to agree with its own choices. An independent instance, without that context, catches subtler issues than self-review instructions or extended thinking. For large changes, run focused per-file passes for local issues and a separate integration pass for cross-file data flow, which avoids attention dilution and contradictory findings. Have the model report a confidence with each finding to route review attention.

**Think of proofreading your own essay versus handing it to a colleague**: you read what you meant to write, not what you wrote.

![A generator instance writes code and an independent reviewer instance without its reasoning reviews it in per-file passes and an integration pass, with a confidence on each finding for routing.](/content/skillup/ccaf/images/ccaf-4-6-multi-pass-review.svg)

### Real use

When one session generates code and then reviews it, the review almost always approves. Switching to a separate review instance, given only the diff and the standards, surfaces real issues. A 60-file PR is reviewed file by file, then in one integration pass, so later files get the same attention as the first.

### How it works

- **Self-review bias**: the generator's reasoning stays in context.
- **Independent reviewer**: no prior reasoning; given only code and criteria.
- **Per-file passes**: local bugs, style and security.
- **Integration pass**: interfaces and data flow across files.
- **Confidence per finding**: route low-confidence items to humans.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Independent review instance | Reviewing generated work | Extra call |
| Per-file + integration passes | Large, multi-file changes | More calls to orchestrate |
| Self-review in one session | Quick sanity check only | Misses its own blind spots |

### How to do it

1. Generate in one instance; review in a new one with only the output and criteria.
2. Split big reviews into per-file passes, then one cross-file integration pass.
3. Ask for a confidence per finding and route accordingly.

### Exam Trap ⚠️

<div class="note-trap">"Tell the same session to review its work critically" or "turn on extended thinking" doesn't remove self-review bias; a separate instance does. A bigger context window doesn't fix attention dilution; splitting the review does.</div>

### Go deeper

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

---

## Deep Dive: Making Prompt Engineering & Structured Output Click

### 1. The connective narrative

The domain moves from what you ask for to how you check it. Explicit criteria (4.1) and few-shot examples (4.2) shape the request so the model knows exactly what counts and what the output looks like. Tool use and schemas (4.3) make the output parseable every time. Validation and retries (4.4) catch what schemas can't: values that are well-formed but wrong.

Batch processing (4.5) and multi-pass review (4.6) are about running this at scale. Batches trade latency for cost when nobody is waiting. Independent instances and split passes keep quality high when the work is large, because one tired reviewer, human or model, misses what fresh eyes catch.

### 2. Worked scenario

> **Scenario.** A team extracts data from 100,000 customer feedback documents each night. The prompt lists exactly which themes to tag and which to ignore (4.1), with three examples of tricky documents (4.2). Extraction uses a strict tool schema with a nullable `product` and a `category` enum that includes `other` (4.3).
>
> Records whose stated and calculated totals differ are retried with the specific error; records missing data are flagged, not retried (4.4). The whole job runs through the Batches API, matched by `custom_id`, with only failures resubmitted (4.5). A second instance spot-checks a sample of extractions, recording a confidence for each (4.6).

### 3. Memory aid

**DEFINE, SHOW, SHAPE, CHECK, SCALE**
- **Define** criteria (4.1) · **Show** examples (4.2) · **Shape** with schemas (4.3) · **Check** and retry (4.4) · **Scale** with batches and independent passes (4.5, 4.6).

### 4. Exam strategy for this domain

Distractors swap a structural fix for a softer one: "be conservative" instead of criteria, "more instructions" instead of examples, "ask for JSON" instead of a schema, "same session reviews" instead of an independent instance. Pick the option that changes the mechanism, not the tone.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Too many false positives | Explicit report/skip criteria with examples |
| One category is noisy and eroding trust | Disable it while fixing its prompt |
| Format inconsistent despite instructions | 2–4 few-shot examples |
| Need guaranteed parseable output | Tool with JSON schema / strict structured outputs |
| Several schemas, unknown document type | `tool_choice: any` |
| One extraction must run first | Force the tool by name |
| Model invents missing values | Make the field nullable; add `unclear`/`other` |
| Totals don't add up | Semantic validation + retry with the error |
| Info isn't in the document | Don't retry; flag it |
| Overnight bulk job | Batches API (50% off, ≤24 h) |
| Pre-merge blocking check | Synchronous API |
| Match batch results | `custom_id` |
| Same session approves its own code | Independent review instance |
| Large PR reviewed unevenly | Per-file passes + integration pass |
