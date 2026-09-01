# D1: Solution Design & Architecture

> **Exam weight**: 17% · **Questions**: ~20 of 120

## Overview

This domain tests whether you can turn an ambiguous business problem into a defensible Claude-based system architecture — and defend the trade-offs you made. It spans the full arc: framing the problem correctly, choosing between workflow/agentic/augmented-LLM patterns, designing input-to-feedback pipelines, decomposing complexity, and orchestrating multiple agents when a single LLM call can't carry the load. At the professional tier, the exam is less interested in "what is an agent" and much more interested in "why did you choose an orchestrator-worker topology instead of a simple prompt chain, and what does that cost you in latency and token spend."

> 💡 **Human Angle**: A good solution architect is like a structural engineer, not a decorator — the question isn't "can this look impressive," it's "will this still be standing, on budget, under load, a year from now." The most elegant multi-agent swarm is the wrong answer if a two-step prompt chain solves the same business problem for a tenth of the cost.

## Translating Business Problems into Claude-Based AI Solutions

### Key Concept

**Translate the business outcome into a problem shape before reaching for an architecture.**

Business stakeholders describe outcomes — "reduce support ticket backlog," "speed up contract review" — not architectures. The architect's first job is translating that outcome into a *problem shape*: classification, extraction, generation, multi-step reasoning, or open-ended research. That shape determines whether Claude is even the right tool, and if so, which pattern applies.

A disciplined translation asks four questions in order: how variable is the input, can "correct output" be evaluated programmatically, does the task need external state or tools mid-reasoning, and what's the acceptable latency and error-cost budget. **Skipping straight to "let's build an agent" is like prescribing surgery before taking a patient history** — the professional-tier trap is reaching for the most capable-sounding tool before confirming a simpler one wouldn't outperform it on cost and reliability.

### In Practice

**What breaks without this**: Every extra agentic hop is one more place for the model to wander off-task. Teams that jump straight to "build an agent" for a stable, well-defined transformation (e.g., extracting five fields from an invoice) end up with a system that's slower, pricier, and *less* reliable than a single structured-output prompt.

**Decision trigger**: Ask "if I wrote this as a flowchart today, would a human follow the same fixed sequence of steps every time, or would the sequence itself depend on what they discover along the way?" Fixed sequence → workflow. Discovery-dependent sequence → agentic.

**When you'd choose differently**: Forcing genuine open-ended investigation into a rigid workflow under-delivers — a task like "find out why this account is at risk of churn," with no predefined data sources, has a problem shape that demands agentic flexibility even though it costs more per run.

### Exam Trap ⚠️

<div class="note-trap">
The exam will describe a task that *sounds* complex ("multi-department approval routing") but is actually deterministic and rule-based. The distractor answer is the most sophisticated-sounding architecture (multi-agent orchestration). The correct answer is usually the simplest pattern that satisfies the requirements — think of over-architecting as bringing a crane to hang a picture frame: impressive, but it doesn't fit through the door and costs ten times more.
</div>

## Designing End-to-End Architectures (Input → Processing → Output → Feedback Loops)

### Key Concept

**A feedback loop is what separates a demo from a production system.**

Every production Claude system decomposes into four stages: **Input** (ingestion, normalization, context assembly), **Processing** (the model call, including any tool-use loop or delegation), **Output** (parsing, validation, guardrail checks), and **Feedback loops** (logging, review, corrections flowing back into prompts or retrieval indexes). Architects who design only the happy-path processing stage and treat feedback as an afterthought build systems that degrade silently, because nothing is watching for drift or recurring failure modes.

The loop closes the gap between "the model got it right in testing" and "we know when it's wrong in production, and can fix it" — whether that's a human review queue, an automated eval harness re-scoring live traffic, or a corrected retrieval index. **A system with no feedback loop is a car with no rearview mirror**: it drives fine on a straight road, with no way to know something's wrong until after it's already crashed.


![Feedback Loop](../images/feedbackloop.png)

### In Practice

**What breaks without this**: A system can pass every pre-launch eval and still fail in production within weeks — real-world input drifts (new document formats, new phrasing) with nobody watching, so the team finds out via a customer complaint, not a dashboard.

**Decision trigger**: Ask "when this system is wrong, how would we know — and how would that knowledge get back into the system?" If the honest answer is "someone would eventually notice and file a ticket," the feedback loop is missing, not just informal.

**When you'd choose differently**: A full feedback/eval loop is over-engineering for low-stakes, low-volume internal tools — a one-off migration script reformatting 200 files just needs a manual spot-check, proportionate to the actual risk.

### Exam Trap ⚠️

<div class="note-trap">
Scenario questions often present an architecture diagram missing the feedback loop and ask "is this architecture complete?" Students focused on whether the model call is correct miss that the diagram has no return path. Treat the feedback loop like a smoke detector: irrelevant on a good day, the only thing that matters on a bad one — and exam scenarios are testing whether you installed it before the fire, not after.
</div>

## Selecting Architectural Patterns (Workflow, Agentic, Augmented LLM)

### Key Concept

**Match the pattern to how much control a task needs, not to how advanced the pattern sounds.**

Anthropic's own guidance (*Building Effective Agents*) draws a clear line between three tiers of system:

- **Augmented LLM**: a single Claude call enhanced with retrieval, tools, and memory — no autonomous multi-step control flow. This is the baseline building block for everything else.
- **Workflows**: predefined code paths that orchestrate LLM calls in a fixed structure — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. The *sequence of steps is fixed by the developer*, even though the content of each step is generated by the model.
- **Agentic systems**: Claude dynamically directs its own process and tool use, maintaining control over how it accomplishes a task. The *sequence itself* is decided by the model at runtime, typically in a loop of plan → act → observe → repeat until a stopping condition is met.

Workflows are predictable, auditable, and cheaper because you can reason about exactly what will execute; agentic systems trade that predictability for handling tasks whose steps can't be fully specified in advance. **Anthropic's own guidance is blunt**: find the simplest solution possible, and add complexity only when it demonstrably improves outcomes — agentic complexity is a cost to justify, not a default.

![Selecting Architectural Patterns](../images/selectingarchpatterns.png)
### In Practice

**What breaks without this**: Deploying an agentic loop for a task that fits a workflow means every run has non-deterministic step count and cost — production runbooks can't set reliable SLAs, and debugging a failure means reconstructing an arbitrary trajectory instead of checking a known sequence of five steps.

**Decision trigger**: Ask "can I write down, today, the exact sequence of LLM calls this task requires, regardless of the input?" Yes → workflow (pick the sub-pattern: chaining for sequential dependent steps, routing for input-type branching, parallelization for independent sub-tasks, orchestrator-workers for dynamic task breakdown with a fixed control layer, evaluator-optimizer for iterative refinement against a quality bar). No → agentic.

**When you'd choose differently**: Agentic control is justified exactly when the number and order of steps can't be pre-scripted — a coding agent that reads a codebase, decides what to change, runs tests, and reacts to failures can't be forced into a fixed workflow, despite the higher variance and cost that comes with it.

### Exam Trap ⚠️

<div class="note-trap">
The exam frequently uses "agentic" and "agent" loosely in a scenario stem, then asks you to pick the correct pattern from an answer set that includes both "orchestrator-workers workflow" and "multi-agent system." These look similar but differ in *who controls the sequence*: in an orchestrator-workers workflow, a central LLM call (not autonomous looping) breaks work into subtasks and dispatches them — it's still a fixed workflow shape. A true multi-agent system has each agent making its own autonomous control-flow decisions. Confusing "multiple LLM calls" with "multiple agents" is the single most common distractor in this domain.
</div>

## Designing Multi-Agent Systems and Orchestration Strategies

### Key Concept

**Multi-agent systems earn their cost only when breadth exceeds what one context window can hold coherently.**

Multi-agent systems become the right answer when a task's breadth exceeds what a single context window or a single agent's tool set can handle — parallel research over independent sub-questions, or systems needing different tool permissions per agent for security isolation. Anthropic's published multi-agent research system uses an **orchestrator (lead agent) + subagents** topology: the lead agent decomposes the query into parallelizable sub-tasks, spins up subagents with narrow objectives and their own context windows, and synthesizes the results — this works because subagents reason with clean, focused context instead of one agent's context filling up with every intermediate step.

Three orchestration topologies recur in practice:

- **Pipeline (sequential handoff)**: Agent A's output becomes Agent B's input, in a fixed order — good for staged transformations (draft → critique → revise) where each stage genuinely depends on the last.
- **Supervisor/orchestrator-worker**: a lead agent dynamically assigns and collects work from subagents it spins up, in parallel or sequence, and owns the synthesis step. Good for breadth-first tasks (research, multi-source data gathering) where subtasks are independent enough to parallelize.
- **Swarm/peer-to-peer**: agents communicate with each other directly with no single controller — rare in production because it's the hardest to debug, audit, and bound; usually a workflow or supervisor pattern achieves the same outcome with far less operational risk.

The orchestration choice has a direct cost: Anthropic's own data shows multi-agent architectures can consume roughly 15x the tokens of a single-agent chat interaction. **Think of it like hiring a project team instead of one generalist** — you get parallelism and specialization, but you're paying for coordination overhead on every task, whether or not that task actually needed it.

![Three orchestration topologies](../images/three_orch_topologies.png)

### In Practice

**What breaks without this**: Giving every subagent the full tool set "for flexibility" collapses both the security and cost benefits of decomposition — a compromised or misfiring subagent now has blast radius equal to the whole system, and you've paid the 15x multi-agent token tax without the isolation it was supposed to buy.

**Decision trigger**: Ask "do these subtasks have independent, non-overlapping objectives that don't need to see each other's intermediate reasoning?" If yes, parallel subagents under an orchestrator are worth the token cost. If subtasks are tightly sequential and each needs the full context of the last, a pipeline (or a single agent with a longer context) is cheaper and easier to debug than fanning out.

**When you'd choose differently**: Multi-agent orchestration is a throughput/quality optimization, not a latency one — a task with a hard, tight SLA (a customer-facing chat response needing sub-2-second turnaround) can't absorb the coordination latency of spinning up an orchestrator and multiple subagents; a single augmented LLM call wins there.

### Exam Trap ⚠️

<div class="note-trap">
Distractor answers love to conflate "using multiple tools" with "multi-agent system." A single agent calling three different tools in sequence within one control loop is still a single-agent (possibly agentic-workflow) system — there is one locus of reasoning and control. Multi-agent requires multiple independent loci of reasoning, each with its own context and decision-making, coordinated by an orchestration layer. Think of it as one chef using three knives versus three chefs in a kitchen — tool count and agent count are not the same axis.
</div>

## Apply Decomposition Techniques for Complex Problem Solving

### Key Concept

**Good decomposition produces sub-tasks that are each independently verifiable — not just smaller.**

Decomposition breaks a problem too large or ambiguous for one prompt/agent into smaller units that are independently solvable, verifiable, and ideally parallelizable. Three strategies map onto the workflow patterns above: **sequential** (each step depends on the last — prompt chaining), **parallel** (independent subtasks running concurrently — parallelization or orchestrator-workers), and **hierarchical** (a top-level goal splits into sub-goals that split further — nested orchestrator layers or a planning agent).

The quality bar is that each resulting sub-unit has a clear, independently verifiable success criterion. **A decomposition nobody can grade in isolation hasn't actually decomposed anything** — it's just relabeled complexity, still one tangled problem underneath.

### In Practice

**What breaks without this**: Accuracy on each sub-task drops when a model juggles multiple different "good answer" criteria in one pass — a single sprawling prompt asking Claude to analyze a 200-page contract, flag risks, summarize obligations, and draft a response produces inconsistent quality across all four, compared to four focused calls.

**Decision trigger**: Ask "can I write a single, unambiguous grading rubric for what a good response to this whole prompt looks like?" If the rubric has to say "and also" more than once, decompose along those "and also" boundaries.

**When you'd choose differently**: Decomposition should track genuine independent sub-problems, not get applied reflexively — splitting "translate this paragraph" into "identify tone" + "translate" + "verify tone preserved" as three separate calls just adds latency and cost to a task that was simple and tightly coupled to begin with.

### Exam Trap ⚠️

<div class="note-trap">
The exam sometimes presents a decomposition that looks reasonable but creates sub-tasks with circular or overlapping dependencies (e.g., Task B needs Task C's output, and Task C needs Task A which needs Task B). The correct answer identifies that the "decomposition" isn't actually decomposed — it's a single tightly coupled task wearing a workflow diagram as a costume. Always trace the dependency graph before accepting a proposed decomposition as valid.
</div>

## Align Solutions to Business Value Pillars

### Key Concept

**Name which business value pillar a design serves — and which one it knowingly sacrifices.**

Every architectural decision in this domain should be traceable to one or more of five business value pillars, because a professional architect is accountable for value delivered, not elegance achieved:

- **Efficiency** — doing the same work with fewer resources (time, headcount, steps).
- **Transformation** — enabling work that was previously impossible or impractical (not just faster, but *new* capability).
- **Productivity** — increasing the output or throughput of existing human workers (augmentation, not replacement, framing).
- **Cost** — direct reduction in operating expense, including model spend, infra, and human review overhead.
- **Performance SLAs** — meeting explicit, contracted thresholds for latency, accuracy, or availability that the business has committed to (internally or to customers).

These pillars often trade off against each other, and the architecture is the mechanism that encodes which trade-off the business actually wants. An agentic multi-agent research system might score high on transformation and productivity but poorly on cost and latency SLA; a narrow single-prompt classifier might score high on cost and SLA but deliver no transformation. **Naming the pillar is what separates a professional justification from a tech-stack preference** — an architect accountable for value delivered always has an answer to "which pillar, and what did we give up."

### In Practice

**What breaks without this**: Technical excellence without a named business pillar is invisible to the people who fund the next phase — teams that build the "best" architecture on merit alone frequently get their project cancelled at the business review, not because the system doesn't work, but because nobody can answer what it actually saved or unlocked.

**Decision trigger**: Before finalizing an architecture, ask "if I had to put one number in front of a VP, which pillar would it be, and does my design choice actually move that number?" If the answer is vague ("it'll be smarter"), the design isn't yet aligned to a pillar.

**When you'd choose differently**: Early-stage exploratory pilots intentionally deprioritize cost and SLA alignment in favor of proving transformation is even possible — it's appropriate to build an expensive, slow proof-of-concept multi-agent system purely to validate that a new capability exists, before any cost-optimization pass.

### Exam Trap ⚠️

<div class="note-trap">
Scenario questions will describe a technically sound architecture and ask "what is the primary business justification" with five answer choices that each name a different pillar. The trap is picking the pillar that sounds most impressive (transformation) when the scenario's actual numbers (e.g., "reduces manual review time from 4 hours to 20 minutes") point to efficiency or productivity. Read the scenario for the *metric actually mentioned*, not the *vibe* of the technology described.
</div>

## Deep Dive: Making Solution Design Click

### 1. The connective narrative

All six concepts in this domain are really one decision process viewed from different angles. It starts with translation: turning a vague business ask into a concrete problem shape. That shape determines the architectural pattern — augmented LLM for single-step tasks, workflow for fixed multi-step sequences, agentic for genuinely open-ended ones. Whichever pattern you pick, it has to be built out as a full input→processing→output→feedback pipeline, because a pattern without a feedback loop is a demo, not a system. When a single agent's context or tool scope can't carry the whole task, you reach for multi-agent orchestration — but that's a cost you pay for parallelism and isolation, not a default upgrade. Underneath both workflow design and multi-agent design sits decomposition: the discipline of breaking work into independently verifiable units, which is what makes a workflow's fixed steps or an orchestrator's subagent tasks actually gradable. And running through every one of those decisions is the business value pillar test — every added layer of complexity (an extra agent, an extra orchestration hop, an extra decomposition step) has to earn its cost against efficiency, transformation, productivity, cost, or SLA, because complexity that doesn't map to a pillar is just risk with no offsetting return.

The unifying principle Anthropic states directly in its own agent-building guidance is to favor the simplest architecture that satisfies the requirement, and add complexity only when it demonstrably improves outcomes. Every concept in this domain is a tool for either measuring "does this satisfy the requirement" (translation, pillars) or for adding calibrated complexity when needed (workflow patterns, multi-agent orchestration, decomposition) — never complexity for its own sake.

### 3. Memory aid

**TAPED** — the five-step check before committing to an architecture:
- **T**ranslate the business ask into a problem shape first.
- **A**sk whether steps are fully specifiable in advance (Augmented LLM / Workflow) or genuinely discovery-dependent (Agentic).
- **P**arallelize or decompose only where sub-tasks are independently verifiable.
- **E**ngineer the feedback loop — no architecture is complete without a return path.
- **D**efend the design against a named business value pillar, not vibes.

### 4. Exam strategy for this domain

- The dominant trap category is **complexity inflation**: scenario stems describe a task that sounds sophisticated, and the wrong-but-tempting answer is the most advanced-sounding pattern (multi-agent, autonomous agentic loop) rather than the simplest pattern that satisfies the stated requirement. Default to the simplest pattern unless the scenario explicitly contains discovery-dependent branching or a stated need for tool/context isolation.
- A second trap category is **terminology look-alikes**: "workflow" vs. "agentic," "orchestrator-workers workflow" vs. "multi-agent system," "multiple tools" vs. "multiple agents." These hinge on one axis — who controls the sequence of steps, fixed-by-developer or decided-at-runtime-by-the-model — so anchor every classification question to that axis.
- The domain rewards reading scenarios for concrete numbers (time saved, cost delta, SLA figures) and punishes answers chosen for technical impressiveness alone. If a scenario states a metric, the correct business-pillar answer almost always maps directly to it.
- The one sentence to remember five minutes before the exam: **pick the simplest architecture that satisfies the requirement, and be ready to name the exact business pillar and feedback mechanism that justify every added layer of complexity.**

## Cheat Sheet 📋

| Concept | Key Rule |
|---------|----------|
| Problem translation | Determine input variability, output evaluability, need for mid-task tool/state, and latency budget *before* picking a pattern |
| Augmented LLM | Single call + retrieval/tools/memory, no autonomous control flow — the default building block |
| Workflow | Developer-fixed sequence of LLM calls (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) — predictable, auditable, cheaper |
| Agentic system | Model decides its own step sequence at runtime in a plan→act→observe loop — flexible, but variable cost/latency, harder to audit |
| Input→processing→output→feedback | All four stages required; feedback loop is what prevents silent production drift |
| Multi-agent orchestration | Justified when subtasks are independent, parallelizable, and/or need tool-scope isolation — costs ~15x tokens of single-agent chat |
| Pipeline vs supervisor vs swarm | Pipeline = fixed sequential handoff; supervisor = orchestrator dispatches/synthesizes parallel subagents; swarm = peer-to-peer, rare, hard to audit |
| Decomposition | Valid only if each sub-task has an independent, verifiable success criterion; check for circular dependencies |
| Business value pillars | Efficiency, Transformation, Productivity, Cost, Performance SLAs — every design choice should map to a named pillar and its explicit trade-off |
| Complexity default | Anthropic's own guidance: start simple, add complexity only when it demonstrably improves outcomes |

## What to Remember

Solution design in this domain is a chain of justified decisions, not a showcase of capability. Translate the business problem honestly before reaching for a pattern. Choose augmented LLM, workflow, or agentic based on whether the step sequence can be fixed in advance — not on how advanced each option sounds. Build the full input→processing→output→feedback loop every time, because the feedback loop is what makes a system observable and correctable in production. Reserve multi-agent orchestration for genuine independence or isolation needs, knowing it costs roughly an order of magnitude more in tokens than a single-agent call. Decompose only along real, independently verifiable sub-problem boundaries. And close every architectural decision by naming which business value pillar it serves and what it costs elsewhere — an architecture without a named pillar is a hobby project, not a professional deliverable.
