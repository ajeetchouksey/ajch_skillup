# D1: Agentic Architecture & Orchestration

> **Exam weight**: 27% · **Questions**: ~65 in the bank

## Overview

This domain covers how Claude-based agents run and coordinate: the agentic loop driven by `stop_reason`, coordinator and subagent designs, how context is passed to subagents, enforcing workflow order with code rather than prompts, Agent SDK hooks, choosing between fixed pipelines and adaptive decomposition, and managing sessions with resume and fork.

> 💡 **Human Angle**: An agent is only as trustworthy as the parts you don't leave to chance. The exam keeps asking one question: which behaviour must be guaranteed by code, and which can be left to the model's judgement?

---

## 1.1 Design and implement agentic loops for autonomous task execution

### Key Concept

**The loop is driven by stop_reason: run the requested tools while it's tool_use, and stop when it's end_turn.**

Each iteration sends the conversation to Claude and inspects the response. If `stop_reason` is `tool_use`, your code executes the requested tools, appends the assistant message and a user message containing the `tool_result` blocks to the history, and calls Claude again. When `stop_reason` is `end_turn`, the task is done. Claude decides which tool to call next from the context; your code doesn't script the sequence.

**Think of a detective who keeps asking for the next file**: you fetch whatever is asked for, until the detective says the case is closed.

![The agentic loop: send messages to Claude, check stop_reason, run the requested tools and append their results while it is tool_use, and return the final answer when it is end_turn.](/content/skillup/ccaf/images/ccaf-1-1-agentic-loop.svg)

### Real use

A support agent receives "Where's my refund?". Claude calls `get_customer`, then `lookup_order`, then `get_refund_status`, each chosen after seeing the previous result, and ends with an answer. The loop never knew the sequence in advance; it just kept running tools until `end_turn`.

### How it works

- **Continue** while `stop_reason == "tool_use"`: execute every `tool_use` block in the response.
- **Append** the assistant turn, then a user turn with one `tool_result` per `tool_use_id`, so the model can reason about the results.
- **Stop** on `end_turn`. Treat `max_tokens` and other stop reasons explicitly.
- **Model-driven**: Claude picks the next tool from context, unlike a pre-configured decision tree.
- A turn cap is a safety net, not the primary stopping mechanism.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Model-driven loop | Steps depend on what earlier tools return | Less predictable path |
| Fixed tool sequence | The steps never vary | Can't adapt to findings |
| Safety cap on turns | Always, as a backstop | Don't rely on it to end normal runs |

### How to do it

1. Call the Messages API with your tools and the conversation so far.
2. If `stop_reason` is `tool_use`, run each requested tool and append the results as `tool_result` blocks.
3. Repeat until `stop_reason` is `end_turn`; return the final text.

### Exam Trap ⚠️

<div class="note-trap">Anti-patterns the exam lists: ending the loop when the assistant's text "sounds finished", parsing phrases like "I'm done", stopping because the response contains text, or using an arbitrary iteration cap as the main exit. The signal is <code>stop_reason</code>.</div>

### Go deeper

- [How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)

---

## 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

### Key Concept

**A coordinator decomposes the task, picks which subagents to run, routes everything through itself, and checks the combined result for gaps.**

In hub-and-spoke designs the coordinator owns task decomposition, delegation, error handling and aggregation, and all communication between subagents passes through it. Subagents have isolated context: they don't see the coordinator's conversation. A good coordinator analyses each query and invokes only the subagents it needs, partitions scope so subagents don't duplicate work, and re-delegates targeted queries when the synthesis has gaps.

**Think of a restaurant host**: every order goes through one person who knows which station does what and checks the plate before it leaves.

![A coordinator analyses the query, sends partitioned subtasks to search, analysis and synthesis subagents, receives all results back, and re-delegates targeted queries when the synthesis shows gaps.](/content/skillup/ccaf/images/ccaf-1-2-coordinator.svg)

### Real use

A research system asked about "AI in creative industries" splits only into visual art, and the report misses music, writing and film. The fix is in the coordinator: broader decomposition, partitioned subtopics, and a review step that spots the missing areas and sends new queries before final synthesis.

### How it works

- **Hub-and-spoke**: subagents never talk directly; the coordinator routes for observability and consistent error handling.
- **Isolated context**: each subagent gets only what the coordinator puts in its prompt (1.3).
- **Dynamic selection**: simple queries don't need the full pipeline.
- **Partition scope** to minimise overlap.
- **Iterative refinement**: evaluate the synthesis for gaps, re-delegate, re-synthesise.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Coordinator + specialist subagents | Broad tasks with separable parts | More orchestration code |
| Single agent | Narrow task, few tools | Context fills faster |
| Full pipeline every time | Never by default | Wastes calls on simple queries |

### How to do it

1. Have the coordinator break the query into partitioned subtasks that cover the whole topic.
2. Invoke only the subagents those subtasks need, passing each its full context.
3. Review the synthesis for gaps and re-delegate before returning.

### Exam Trap ⚠️

<div class="note-trap">When a report misses whole areas of a topic, the root cause is usually the coordinator's narrow decomposition, not the search or synthesis subagents. And letting subagents call each other directly loses the coordinator's observability and error handling.</div>

### Go deeper

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

---

## 1.3 Configure subagent invocation, context passing, and spawning

### Key Concept

**Subagents start with a blank slate: everything they need must be in the prompt you send them.**

A coordinator spawns subagents with the Task tool (renamed **Agent** in Claude Code 2.1.63; `Task` still works as an alias), so the coordinator's `allowedTools` must include it. Each subagent type is described by an `AgentDefinition`: a description that tells the coordinator when to use it, a system prompt, and its allowed tools. Subagents don't inherit the parent's history or share memory between invocations. To run them in parallel, the coordinator emits several Task calls in one response.

**Think of briefing a contractor by email**: they weren't in your meetings, so the email has to contain the findings, the sources and the goal.

![A coordinator passes a subagent a structured brief containing prior findings, source metadata and quality criteria; several subagents are spawned in one response to run in parallel.](/content/skillup/ccaf/images/ccaf-1-3-subagent-context.svg)

### Real use

A `data_analyzer` subagent keeps ignoring search findings because the team assumed it could see what the coordinator saw. Passing the complete search results in its prompt, as structured data with source URLs and page numbers kept separate from content, fixes the analyses immediately.

### How it works

- **Spawn**: the Task (Agent) tool; it must be in the coordinator's allowed tools.
- **Define**: `AgentDefinition` with description, prompt and tools per subagent type.
- **Pass context explicitly**: full prior findings, with metadata (source, document, page) separated from content.
- **Parallelise**: multiple Task calls in a single coordinator response, not one per turn.
- **Brief by goals**: give research goals and quality criteria, not step-by-step procedures.
- **Fork** a session to explore divergent approaches from a shared baseline (1.7).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Parallel Task calls in one response | Subtasks are independent | Results arrive together to merge |
| Sequential spawning | A later subtask needs an earlier result | Slower end to end |
| Fork from a baseline | Comparing two approaches after shared analysis | Two branches to track |

### How to do it

1. Define each subagent type with a clear description, prompt and minimal tools.
2. Include `Task` in the coordinator's allowed tools.
3. Put complete, structured findings and the goal in each subagent's prompt; spawn independent ones together.

### Exam Trap ⚠️

<div class="note-trap">"The subagent can see the coordinator's conversation" is the trap: it can't. Also wrong: spawning parallel work across separate turns (that serialises it), and forgetting <code>Task</code> in <code>allowedTools</code>, which leaves the coordinator unable to delegate.</div>

### Go deeper

- [Subagents in the Agent SDK](https://code.claude.com/docs/en/agent-sdk/subagents)
- [Create custom subagents in Claude Code](https://code.claude.com/docs/en/sub-agents)

---

## 1.4 Implement multi-step workflows with enforcement and handoff patterns

### Key Concept

**When order must be guaranteed, enforce it in code: prompts follow rules most of the time, and "most" isn't enough for money or identity.**

Prompt instructions such as "always verify the customer first" have a non-zero failure rate. For deterministic compliance, use programmatic prerequisites: block `process_refund` until `get_customer` has returned a verified customer ID in this session. When a case must go to a human mid-process, hand off a structured summary so nobody has to re-ask the customer.

**Think of a bank vault with a time lock**: the procedure manual says wait; the lock makes sure.

![A prerequisite gate blocks process_refund until get_customer has returned a verified ID; when the case escalates, a structured handoff with customer ID, root cause, amount and recommended action goes to the human agent.](/content/skillup/ccaf/images/ccaf-1-4-prerequisite-gate.svg)

### Real use

A support agent occasionally issues refunds before verifying identity, despite a clear system prompt. A gate in code now rejects `process_refund` unless a verified customer ID exists, and returns an error telling the agent to verify first. Escalations carry customer ID, root cause, refund amount and recommended action.

### How it works

- **Programmatic prerequisites**: track completed steps in state and block downstream tools until they're done.
- **Prompt guidance**: fine for preferences and soft ordering.
- **Multi-concern requests**: split into distinct items, investigate in parallel with shared context, then give one resolution.
- **Structured handoff**: customer details, root cause, amounts, actions taken, recommended next step.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Programmatic gate | Compliance must be guaranteed (identity, payments) | Code to maintain |
| Prompt instruction | Soft preference; occasional deviation is acceptable | Non-zero failure rate |
| Structured handoff | Any escalation to a human | Agent must gather fields first |

### How to do it

1. List the steps that must happen in order and the tools they unlock.
2. Enforce them in the tool layer or a hook, returning a clear error when a prerequisite is missing.
3. Define a handoff schema and require it on every escalation.

### Exam Trap ⚠️

<div class="note-trap">"Make the system prompt more emphatic" (capitals, "CRITICAL") doesn't make compliance deterministic. Removing the refund tool entirely breaks legitimate refunds. The answer is a programmatic prerequisite.</div>

### Go deeper

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

---

## 1.5 Apply Agent SDK hooks for tool call interception and data normalisation

### Key Concept

**Hooks run your code around every tool call: PreToolUse can block or redirect a call, PostToolUse can reshape a result before Claude sees it.**

Hooks give deterministic guarantees where prompts are probabilistic. A PreToolUse hook inspects the outgoing call and can deny it, for example a refund above $500, and point the agent to an escalation path instead. A PostToolUse hook transforms tool output, for example normalising Unix timestamps, ISO 8601 strings and numeric status codes from different MCP tools into one format before the model reasons over them.

**Think of airport security**: one checkpoint screens what goes out, another inspects what comes back in.

![A tool call passes a PreToolUse hook that blocks refunds over $500 and redirects them to escalation, the tool runs, and a PostToolUse hook normalises timestamps and status codes before Claude sees the result.](/content/skillup/ccaf/images/ccaf-1-5-hooks.svg)

### Real use

Three MCP tools return dates as `1730246400`, `2026-10-30T00:00:00Z` and `30/10/2026`, and the agent miscalculates refund windows. A PostToolUse hook converts all three to ISO 8601. A PreToolUse hook denies refunds over $500 with a message to escalate to a human.

### How it works

- **PreToolUse**: runs before the tool; returns `permissionDecision` (`allow`, `deny`, `ask`), a `permissionDecisionReason` the model sees, or `updatedInput`.
- **PostToolUse**: runs after the tool; `updatedToolOutput` replaces the result, `additionalContext` appends to it.
- **Deterministic**: hooks always run; prompt rules usually run.
- **Redirect, don't just block**: tell the agent what to do instead (escalate).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| PreToolUse hook | A rule must never be broken (limits, permissions) | Code to maintain |
| PostToolUse hook | Tool outputs vary in format or contain noise | Must handle every format |
| Prompt instruction | Guidance where occasional misses are acceptable | Probabilistic |

### How to do it

1. Identify rules that must hold every time and outputs that need cleaning.
2. Register a PreToolUse hook matched to the risky tool that denies violations with a redirect message.
3. Register a PostToolUse hook that normalises the tool's result before returning it.

### Exam Trap ⚠️

<div class="note-trap">Pre vs post is the tested distinction: blocking an action needs <strong>PreToolUse</strong> (PostToolUse runs after the refund already happened). Normalising data the model will read needs <strong>PostToolUse</strong>. And "add the rule to the system prompt" isn't a guarantee.</div>

### Go deeper

- [Intercept and control agent behaviour with hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

---

## 1.6 Design task decomposition strategies for complex workflows

### Key Concept

**Use a fixed chain when the steps are predictable, and adaptive decomposition when what you find decides what to do next.**

**Prompt chaining** breaks a task into a fixed sequence: analyse each file on its own, then run a cross-file integration pass. It suits predictable, multi-aspect reviews and avoids attention dilution. **Dynamic decomposition** first maps the structure, identifies high-impact areas, then builds a prioritised plan that changes as dependencies are discovered. It suits open-ended investigations.

**Think of a checklist inspection versus a detective case**: one follows the same steps every time; the other follows the leads.

![Two decomposition patterns: a fixed chain of per-file passes followed by an integration pass for predictable reviews, and an adaptive loop of mapping, prioritising and re-planning for open-ended investigations.](/content/skillup/ccaf/images/ccaf-1-6-decomposition.svg)

### Real use

A 40-file pull request reviewed in one pass gets detailed comments on the first files and almost none on the rest. Splitting it into per-file passes plus one integration pass for cross-file data flow gives even coverage. A "why is checkout slow?" investigation instead starts by mapping services and follows the evidence.

### How it works

- **Prompt chaining**: fixed steps; each step's output feeds the next.
- **Per-file + integration**: local issues per file, then data flow across files.
- **Adaptive**: map structure → find high-impact areas → plan → re-plan on new findings.
- One giant pass dilutes attention and can produce contradictory findings.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Prompt chaining | Steps are known and repeatable | Can't follow unexpected leads |
| Dynamic decomposition | Open-ended investigation | Less predictable cost and path |
| Single pass | Small, self-contained task | Attention dilution at scale |

### How to do it

1. Ask whether the steps are known before you start.
2. If yes, chain them: per-file passes, then an integration pass.
3. If no, map first, prioritise, and let the plan adapt as findings arrive.

### Exam Trap ⚠️

<div class="note-trap">"Use a model with a bigger context window" doesn't fix attention dilution on large reviews; splitting the work does. And a fixed pipeline is the wrong tool for open-ended debugging, where the next step depends on what you just found.</div>

### Go deeper

- [Chain complex prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts)

---

## 1.7 Manage session state, resumption, and forking

### Key Concept

**Resume a session when its context is still true, fork it to try an alternative, and start fresh with a summary when its tool results are stale.**

In Claude Code, `--resume <session>` continues a specific prior conversation by ID or by the name you gave it (`--name`, or `/rename` mid-session); `--fork-session` with `--resume` creates a new session ID from that history. In the Agent SDK, pass `resume` with a session ID, and add `fork_session` (Python) or `forkSession` (TypeScript) to branch. Forking copies the conversation, not the filesystem.

**Think of a bookmark and a photocopy**: the bookmark returns you to your place; the photocopy lets you scribble a different ending without touching the original.

![From a shared analysis session: resume it when prior context is still valid, fork it into two branches to compare approaches, or start a fresh session with a structured summary when files have changed.](/content/skillup/ccaf/images/ccaf-1-7-sessions.svg)

### Real use

After analysing a codebase, a developer forks the session twice to compare two refactoring strategies from the same baseline. Next week, after teammates changed six files, they start a fresh session seeded with a summary and the list of changed files rather than resuming with stale tool results.

### How it works

- **Resume** (`--resume <name or id>`, SDK `resume`): full prior context; best when it's still accurate.
- **Fork** (`--fork-session`, SDK `fork_session` / `forkSession`): new session from a copy of the history.
- **Stale results**: old file reads still sit in context and mislead the model.
- **Tell a resumed session what changed**, so it re-reads only those files.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Resume | Prior context is mostly valid | Stale results if files changed |
| Fork | Comparing approaches from one baseline | Two sessions to manage |
| Fresh + summary | Many files changed since the last session | Lose detail not in the summary |

### How to do it

1. Name long investigations so you can `--resume` them by name.
2. Before resuming, list the files that changed and ask for targeted re-analysis.
3. If much has changed, start fresh and inject a structured summary instead.

### Exam Trap ⚠️

<div class="note-trap">Resuming after big code changes without telling the agent leaves it reasoning from outdated tool results. And forking doesn't isolate file edits: both branches work on the same files on disk.</div>

### Go deeper

- [Work with sessions (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/sessions)

---

## Deep Dive: Making Agentic Architecture Click

### 1. The connective narrative

Every lesson in this domain answers one design question: what does the model decide, and what does your code guarantee? The loop (1.1) lets the model choose tools while your code owns the stopping signal. The coordinator (1.2) lets the model plan while your architecture owns routing and error handling. Subagents (1.3) reason freely, but only over the context you deliberately give them.

Enforcement (1.4) and hooks (1.5) are where the line is sharpest: anything that must never go wrong, such as identity checks and refund limits, moves out of the prompt and into code. Decomposition (1.6) and sessions (1.7) are about keeping that reasoning focused: split work so attention isn't diluted, and keep context accurate so the model isn't reasoning over stale facts.

### 2. Worked scenario

> **Scenario.** A refund-support agent is moving to production. The loop runs on `stop_reason` (1.1). A PreToolUse hook blocks refunds over $500 and redirects them to escalation, and a PostToolUse hook normalises dates from three MCP tools (1.5). `process_refund` is gated until `get_customer` returns a verified ID (1.4).
>
> Complex cases go to a coordinator that splits "refund plus address change plus complaint" into three items, spawns specialist subagents in parallel with the customer record in each prompt (1.2, 1.3), and escalates with a structured handoff when policy is silent. Engineers debugging the system fork a session to compare two retry strategies from the same analysis (1.7).

### 3. Memory aid

**LOOP-GATE-BRIEF**
- **LOOP**: `stop_reason` drives it.
- **GATE**: guarantees go in code (prerequisites, hooks).
- **BRIEF**: subagents only know what you tell them.

### 4. Exam strategy for this domain

Most distractors replace a guarantee with a stronger-worded prompt, or assume shared context that doesn't exist. Pick the option that moves the must-never-fail rule into code, and that passes context explicitly.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| When does the loop stop? | `stop_reason == "end_turn"` |
| Loop ends when text "looks done" | Anti-pattern: use `stop_reason` |
| Report misses parts of the topic | Coordinator's decomposition too narrow |
| Subagent ignores earlier findings | Pass them in its prompt; context isn't inherited |
| Coordinator can't spawn subagents | Add `Task` (Agent) to `allowedTools` |
| Run subagents in parallel | Several Task calls in one response |
| Refund before identity check | Programmatic prerequisite, not a stronger prompt |
| Block a refund over $500 | PreToolUse hook, redirect to escalation |
| Mixed date formats from tools | PostToolUse hook to normalise |
| Large review misses later files | Per-file passes + integration pass |
| Open-ended investigation | Dynamic, adaptive decomposition |
| Compare two approaches from one analysis | Fork the session |
| Files changed since last session | Tell it what changed, or start fresh with a summary |
