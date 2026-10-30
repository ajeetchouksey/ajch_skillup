# D4: Workflow Integration and Solution Design

> **Exam weight**: 16% · **Questions**: ~15 in the bank

## Overview

This domain covers using Claude beyond single tasks: turning messy input into clear requirements, researching and planning, prototyping solutions, fitting Claude into the way a team already works, and explaining honestly to stakeholders what Claude adds and where its limits are. It also covers knowing when work should go to Claude Architects or Developers instead.

> 💡 **Human Angle**: The best Claude workflows rarely start as a big redesign. They start with one annoying step that someone stopped doing by hand.

---

## 4.1 Apply Claude to analyze requirements and use cases

### Key Concept

**Use Claude to turn scattered notes, emails and interviews into clear requirements, then judge which tasks really suit AI.**

Requirements arrive messy: meeting notes, stakeholder emails, survey comments. Claude can extract the needs, group them, spot contradictions and list open questions, which you then confirm with the people involved. When weighing a use case, Anthropic's AI Fluency framework calls this **Delegation**: understand the goal and the work first, then decide what Claude should automate, what it should help a person with (augmentation), and what stays with people.

**Think of a sharp analyst after a day of workshops**: they hand you a tidy list of needs and the questions nobody answered.

![From messy input to a decision: notes, emails and interviews are turned by Claude into grouped requirements, contradictions and open questions, which people confirm before choosing what to automate, what to augment and what to keep human.](/content/skillup/ccao/images/ccao-4-1-requirements.svg)

### Real use

An operations manager pastes notes from five interviews about the purchase-approval process. Claude groups the pain points, flags that two teams describe different approval limits, and lists six open questions. After a follow-up call, the confirmed requirements show that drafting approval summaries is a good fit for Claude, while approving spend must stay with managers.

### How it works

- **Extract:** needs, constraints, stakeholders, success measures.
- **Organise:** group and prioritise; highlight contradictions.
- **Question:** list what's missing or ambiguous.
- **Delegate wisely:** automate repetitive steps, augment judgement-heavy ones, keep accountable decisions with people.
- **Confirm** with the real stakeholders; Claude only knows what you gave it.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Claude organises raw input | Lots of unstructured notes | Must confirm with people |
| Automate the step | Repetitive, low-risk, well-defined | Needs checks on output |
| Augment a person | Judgement matters | Person stays involved |
| Keep it human | Accountable or sensitive decisions | No time saved |

### How to do it

1. Give Claude the raw input and ask for requirements, conflicts and open questions.
2. Confirm them with stakeholders.
3. For each task, decide: automate, augment or keep human.

### Exam Trap ⚠️

<div class="note-trap">Treating Claude's requirements list as final skips the stakeholders. And "automate the whole process with Claude" ignores which steps need human judgement or accountability.</div>

### Go deeper

- [AI Fluency: Framework & Foundations](https://www.anthropic.com/ai-fluency/overview)

---

## 4.2 Leverage Claude for research, planning, and process optimization

### Key Concept

**Research gathers and cites, planning turns a goal into ordered steps, and optimisation finds the slow or repetitive steps worth changing.**

For **research**, Research mode runs several searches, follows leads and returns a report with citations; it can also draw on your connected tools on web and desktop. For **planning**, give Claude the goal, deadline, resources and constraints, and ask for steps, owners, dependencies and risks. For **process optimisation**, describe the current process step by step and ask Claude to find bottlenecks, duplicated work and steps it could take over.

**Think of a researcher, a project planner and a process consultant** sitting at one desk.

![Three uses side by side: research gathers sources and returns a cited report, planning turns a goal into steps with owners and risks, and process optimisation maps the current steps to find bottlenecks and candidates for Claude.](/content/skillup/ccao/images/ccao-4-2-research-plan-optimize.svg)

### Real use

A school's operations lead uses Research to compare enrolment systems used by similar schools, asks Claude for a term-by-term rollout plan with risks, and then maps the current enrolment process with Claude, which spots that the same data is typed into three systems.

### How it works

- **Research:** paid plans, web search on; cites sources to verify.
- **Planning:** goal, constraints, resources in; steps, dependencies, owners, risks out.
- **Optimisation:** describe each step, its time and its pain; ask for bottlenecks and duplication.
- **Validate:** check sources, and test plans with the people who will do the work.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Research | Many sources, need citations | Slower; verify claims |
| Planning prompt | Turning a goal into steps | Plan is only as good as the inputs |
| Process mapping | A process feels slow or repetitive | Needs an honest description of reality |

### How to do it

1. Name which of the three you need: facts, a plan or a better process.
2. Give the right inputs: question, goal and constraints, or current steps.
3. Verify sources and test plans with the people involved.

### Exam Trap ⚠️

<div class="note-trap">A cited report is not verified until you open the sources. And optimising a process described from memory, rather than as it really runs, fixes the wrong steps.</div>

### Go deeper

- [Use Research on Claude](https://support.claude.com/en/articles/11088861-use-research-on-claude)

---

## 4.3 Use Claude to support solution design, development, and iteration

### Key Concept

**Prototype early: let Claude draft options, build a working version as an artifact, and improve it with real feedback; hand off to developers when it needs real integration.**

Claude can help design solutions without code: compare approaches with pros and cons, draft a process or template, and build a working prototype as an artifact, such as a calculator, checklist tool or dashboard that people can try. Feedback from real users then drives the next version. When a solution needs production systems, integrations or code that others depend on, that's work for Claude Architects and Developers.

**Think of a cardboard model before the building**: cheap to change, and it tells you what people actually need.

![Solution iteration: Claude drafts options, builds a prototype artifact, real users try it, feedback drives the next version, and anything needing production integration is handed to developers.](/content/skillup/ccao/images/ccao-4-3-prototype.svg)

### Real use

A training coordinator needs a way for managers to pick courses for their team. Claude compares three approaches, then builds an artifact that recommends courses from a few questions. Five managers try it; their feedback adds a budget filter. Connecting it to the HR system is passed to the internal developers.

### How it works

- **Options first:** ask for two or three approaches with trade-offs.
- **Prototype:** an artifact people can use; export or share it.
- **Test with users:** real tasks, real feedback.
- **Iterate:** one change at a time, keep what works.
- **Escalate:** production systems, integrations and APIs go to Architects and Developers.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Option comparison | Unsure which approach fits | Still need to choose |
| Artifact prototype | People need to try it | Not a production system |
| Hand off to developers | Needs integration, scale or APIs | Longer lead time |

### How to do it

1. Ask Claude for a few approaches and pick one.
2. Build a prototype artifact and let real users try it.
3. Iterate on feedback; escalate when integration or code is needed.

### Exam Trap ⚠️

<div class="note-trap">Treating a prototype artifact as a production system, or building complex integrations yourself, oversteps the Associate role. The exam expects you to recognise when to escalate to Architects and Developers.</div>

### Go deeper

- [What are artifacts and how do I use them?](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them)

---

## 4.4 Integrate Claude into existing workflows to augment or redesign them

### Key Concept

**Start by having Claude help with one step of the way the team already works; redesign the whole process only once you've seen where Claude really helps.**

Augmenting means Claude speeds up or improves a step people already do: drafting the weekly report from notes, summarising a long email thread, preparing meeting briefs. Redesigning means changing the process itself because Claude makes a new way possible. Connectors (such as Gmail, Google Calendar and Google Drive) and shared Projects let Claude work with the team's real material. For actions like sending email, Claude asks for your approval by default.

**Think of adding a dishwasher before redesigning the kitchen.**

![Two paths: augmenting adds Claude to one step of the existing workflow, such as drafting the weekly report from notes, while redesigning changes the process itself once the gains are proven.](/content/skillup/ccao/images/ccao-4-4-augment-redesign.svg)

### Real use

A sales operations team first uses Claude only to draft the weekly pipeline summary from exported notes, cutting two hours a week. After a month of reliable results, they redesign: a shared Project holds the account context, and the Monday meeting starts from Claude's draft instead of building the summary live.

### How it works

- **Pick one step:** frequent, time-consuming, easy to check.
- **Augment:** Claude drafts, people review and finish.
- **Connect sources:** connectors and Projects bring in real material.
- **Measure:** time saved, quality, rework.
- **Redesign** once the gains are proven and the team trusts the output.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Augment a step | Starting out, or process works well | Smaller gains |
| Redesign the process | Augmenting proved value; process is the bottleneck | Change for the whole team |
| Leave as is | Step needs human judgement or is rare | No time saved |

### How to do it

1. Map the current workflow and pick one step to augment.
2. Run it with Claude for a few weeks and measure the result.
3. Redesign the process only when the evidence supports it.

### Exam Trap ⚠️

<div class="note-trap">"Redesign the whole department's process around Claude on day one" skips proving value. Start by augmenting one step and measure it.</div>

### Go deeper

- [Use Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)

---

## 4.5 Communicate Claude's value and limitations to stakeholders

### Key Concept

**Show measured results on real tasks, and say plainly what Claude can't do, what it gets wrong and who checks its work.**

Stakeholders trust evidence, not enthusiasm. Value is best shown with before-and-after measures on real work: time saved, turnaround, consistency, satisfaction. Limitations belong in the same conversation: Claude can be wrong with confidence, only knows what it's given or can search, and needs human review for high-stakes output. Being honest about AI's role is part of what the AI Fluency framework calls **Diligence**.

**Think of a good pilot programme report**: what worked, what didn't, what it costs and what's next.

![A balanced stakeholder message: measured value such as time saved and consistency on real tasks, stated limits such as errors and knowledge gaps, the safeguards in place such as human review, and the recommended next step.](/content/skillup/ccao/images/ccao-4-5-communicate.svg)

### Real use

After a six-week pilot, a communications lead presents: drafting time for newsletters fell from 4 hours to 90 minutes, two factual errors were caught in review, every draft is still checked by an editor, and she recommends extending to the internal blog.

### How it works

- **Measure:** baseline before, results after, on the same tasks.
- **Show examples:** real outputs, including corrected ones.
- **Name the limits:** errors, missing knowledge, need for review.
- **Explain safeguards:** who reviews what, and data rules followed.
- **Recommend** a clear next step.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Metrics + examples | Asking for adoption or budget | Needs a baseline |
| Live demo on real work | Stakeholders are sceptical | Can go wrong live |
| Limits stated up front | Always | Less exciting, more trusted |

### How to do it

1. Capture a baseline before introducing Claude.
2. Report measured results with real examples, including fixes.
3. State the limits and safeguards, then recommend a next step.

### Exam Trap ⚠️

<div class="note-trap">Promising that Claude "removes the need for review" or "is always accurate" damages trust the first time it's wrong. Present measured value and honest limits together.</div>

### Go deeper

- [AI Fluency: Framework & Foundations](https://www.anthropic.com/ai-fluency/overview)

---

## Deep Dive: Making Workflow Integration Click

### 1. The connective narrative

This domain moves from tasks to ways of working. Requirements analysis (4.1) decides what's worth doing and what should stay human. Research, planning and optimisation (4.2) shape the approach. Prototyping (4.3) tests it cheaply. Integration (4.4) brings it into the team's real workflow, one step at a time. Communication (4.5) earns the trust that lets it spread, with honest limits and a clear point where Architects and Developers take over.

### 2. Worked scenario

> **Scenario.** A finance team's month-end report takes three days. The analyst gives Claude the process notes and finds that consolidating comments from ten managers is the bottleneck (4.1, 4.2). Claude builds a prototype artifact that structures the comments (4.3). The team uses Claude only for that step for two months (4.4), then presents the time saved, the review step and the remaining limits to the CFO (4.5). Connecting directly to the accounting system goes to the developers.

### 3. Memory aid

**ARPIC**: **A**nalyse, **R**esearch and plan, **P**rototype, **I**ntegrate one step, **C**ommunicate honestly.

### 4. Exam strategy for this domain

Wrong answers jump too far: automate everything, redesign on day one, promise no errors, build integrations yourself. Right answers start small, measure, keep people accountable, and escalate technical work.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Messy interview notes | Claude extracts requirements and open questions; confirm with people |
| Decide what to hand to Claude | Automate repetitive, augment judgement, keep accountable decisions human |
| Compare options across sources | Research, then verify citations |
| Process feels slow | Map the real steps; find bottlenecks |
| People need to try an idea | Prototype as an artifact |
| Needs system integration or APIs | Escalate to Architects or Developers |
| First rollout | Augment one step; measure |
| Pitching to leadership | Measured results plus honest limits |
