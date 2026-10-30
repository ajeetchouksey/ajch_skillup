# D7: Troubleshooting and Optimization

> **Exam weight**: 10% · **Questions**: ~9 in the bank

## Overview

This domain covers what to do when Claude isn't delivering: diagnosing why a prompt or output is falling short, changing the setup based on what results show, and making workflows faster and lighter without losing quality.

> 💡 **Human Angle**: The same correction made by hand every week isn't a habit; it's a bug in the setup.

---

## 7.1 Identify, diagnose, and resolve issues with underperforming prompts or poor outputs

### Key Concept

**Diagnose before you fix: name the symptom, trace it to the prompt, the context, the model or the feature, then change one thing and test again.**

Poor output has causes. Generic answers usually mean missing context or audience. Wrong facts usually mean no source was given, or the knowledge is out of date. Ignored formatting often means the instruction was vague or buried. Shallow reasoning may need a more capable model or higher effort. A chat that starts confusing details may be too long. Change one thing at a time so you know what fixed it.

**Think of a mechanic**: they find which part is failing before replacing anything.

![Symptoms traced to causes and fixes: generic output to missing context, wrong facts to a missing or stale source, ignored format to vague instructions, shallow reasoning to the model or effort setting, and mixed-up details to an overlong chat.](/content/skillup/ccao/images/ccao-7-1-diagnose.svg)

### Real use

A sales Project keeps quoting the wrong discount. The rep's first instinct is to reword her question. Diagnosing instead, she finds two pricing files in the Project's knowledge, one from last year. Removing it fixes every chat, not just hers.

### How it works

- **Generic or off-target:** add goal, audience, context (1.1).
- **Wrong facts:** provide or update the source; ask for quotes (2.3).
- **Format ignored:** make the instruction specific; show an example.
- **Shallow reasoning:** decompose the task, or step up model or effort (3.3).
- **Drifting chat:** summarise and restart (3.4).
- **Change one thing**, then test with the same input.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Fix the prompt | Output misses goal, audience or format | Fix may live in one chat only |
| Fix the source or knowledge | Facts are wrong or outdated | Affects everyone using it |
| Change model or effort | Reasoning is too shallow | More time and usage |

### How to do it

1. Describe the symptom precisely, with an example.
2. Check the likely cause: prompt, source, model or chat length.
3. Change one thing and retest with the same input.

### Exam Trap ⚠️

<div class="note-trap">"Switch to the most capable model" isn't the answer when the cause is stale knowledge or a vague instruction; a bigger model will answer confidently from the same wrong input. Diagnose first.</div>

### Go deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

---

## 7.2 Adjust approach based on feedback and results

### Key Concept

**Let evidence steer: when the same problem keeps coming back, change the setup (instructions, knowledge, model or workflow) instead of correcting each output by hand.**

Feedback comes from reviewers, users and your own results. One-off issues can be fixed in the chat. Recurring ones point to the setup: a missing rule in the Project instructions, an outdated file, a model that's too small, or a step that shouldn't use Claude at all. If the problem goes beyond what you can configure, such as a needed integration or a custom tool, escalate to Claude Architects or Developers.

**Think of a recipe that keeps coming out salty**: you change the recipe, not each plate.

![An adjustment ladder: fix a one-off issue in the chat, update the prompt template for repeat tasks, update Project instructions or knowledge for recurring issues, change the model or feature if quality still falls short, and escalate to Architects or Developers when configuration can't solve it.](/content/skillup/ccao/images/ccao-7-2-adjust.svg)

### Real use

Editors keep fixing the same thing in Claude's newsletter drafts: product names in the wrong case. The writer adds a product-name list and the rule to the Project instructions. The edits stop. Later, the team wants drafts to publish straight to the website, which needs an integration, so she raises it with the platform developers.

### How it works

- **Collect feedback:** what reviewers change, and how often.
- **One-off:** fix it in the chat.
- **Recurring:** update prompt templates, instructions or knowledge.
- **Quality ceiling:** try a different model, effort setting or feature.
- **Out of scope:** integrations and custom tools go to Architects or Developers.
- **Stop:** if Claude doesn't improve a step, take it out of the workflow.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Fix in chat | Happened once | Doesn't prevent repeats |
| Update instructions or knowledge | Same issue recurring | Affects all users of the setup |
| Escalate | Needs integration or custom build | Depends on another team |

### How to do it

1. Track what reviewers change and how often.
2. Move recurring fixes into instructions, knowledge or templates.
3. Escalate what configuration can't solve, or remove Claude from that step.

### Exam Trap ⚠️

<div class="note-trap">Correcting the same issue by hand every week, or building a technical integration yourself, are both wrong. Fix recurring issues in the setup, and escalate technical builds.</div>

### Go deeper

- [AI Fluency: Framework & Foundations](https://www.anthropic.com/ai-fluency/overview)

---

## 7.3 Optimize workflows for efficiency and effectiveness

### Key Concept

**Cut repeated effort: reuse Projects and prompt templates, batch related requests, pick the right model, and stop using Claude where it doesn't help.**

Efficiency means getting the same quality with less time and usage. Practical levers: keep reusable context in Projects instead of re-uploading it (project documents are cached, so reusing them counts less against usage than new content); batch related questions into one message; plan the request so it needs fewer follow-ups; match model and effort to the task; start fresh chats instead of dragging long ones; and save good prompts as templates. Effectiveness means checking that the workflow still produces what's needed.

**Think of a well-organised kitchen**: ingredients prepped, tools within reach, nothing done twice.

![Efficiency levers: reuse Projects instead of re-uploading, batch related requests, pick the right model and effort, restart long chats with a summary, and keep prompt templates, while checking quality still meets the need.](/content/skillup/ccao/images/ccao-7-3-optimize.svg)

### Real use

A recruiter sends Claude ten separate messages a day about the same job: one per CV question. She moves the job description into a Project, batches the questions per candidate into one message, uses a faster model for first-pass screening summaries, and saves her best prompt as a template. She gets the same results with a fraction of the messages.

### How it works

- **Projects:** cached knowledge, no repeated uploads.
- **Batching:** related requests in one message.
- **Planning:** clear, complete requests reduce follow-ups.
- **Model and effort:** fast for simple, capable for hard.
- **Fresh chats:** long chats use more of your usage limit.
- **Templates:** reuse prompts that work.
- **Effectiveness:** measure quality, not just speed.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Batch requests | Several related questions | One longer message to review |
| Reuse a Project | Same context, many chats | Needs maintaining |
| Lighter model | Simple, frequent tasks | Check quality holds |

### How to do it

1. Look for repeated uploads, repeated prompts and many small messages.
2. Move context into a Project, batch requests and save templates.
3. Right-size the model, then confirm quality didn't drop.

### Exam Trap ⚠️

<div class="note-trap">"Send each small question separately so answers are focused" usually costs more messages and context. Batch related requests. And optimising speed while quality drops isn't an improvement.</div>

### Go deeper

- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)

---

## Deep Dive: Making Troubleshooting and Optimization Click

### 1. The connective narrative

This domain closes the loop on the other six. Diagnosis (7.1) traces a bad output to its cause, so the fix lands in the right place. Adjusting (7.2) turns repeated feedback into setup changes, and recognises when the answer is escalation or not using Claude for that step. Optimisation (7.3) removes waste once things work: reuse context, batch requests, right-size the model, and keep checking that quality holds.

### 2. Worked scenario

> **Scenario.** A support team's Claude-drafted replies are slow to produce and often need the same edit. The lead diagnoses that the refund policy in the Project is outdated (7.1), replaces it, and adds the recurring edit as a rule in the Project instructions (7.2). She then has agents batch questions per ticket, switches simple replies to a faster model, and saves three reply templates. Response time drops and review edits fall (7.3).

### 3. Memory aid

**DAO**: **D**iagnose the cause · **A**djust the setup · **O**ptimise without losing quality.

### 4. Exam strategy for this domain

Wrong answers treat symptoms: reword the question, upgrade the model, fix each output by hand, send more small messages. Right answers find the cause, change the setup, escalate technical work and remove repeated effort.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Wrong facts in a Project | Check knowledge for stale or duplicate files |
| Same edit every time | Add a rule to the instructions or template |
| Shallow analysis | Decompose, or step up model or effort |
| Long chat getting confused | Summarise and restart |
| Needs integration with another system | Escalate to Architects or Developers |
| Many small messages | Batch related requests |
| Re-uploading the same files | Use a Project |
| Faster but worse | Not an optimisation |
