# D4: Tool Design & MCP Integration

> **Exam weight**: 18% · **Questions**: ~45 in the bank · Official exam guide numbering: Domain 2, objectives 2.1–2.5

## Overview

This domain covers the tools agents call and how they're wired in: descriptions that make tool selection reliable, structured error responses from MCP tools, how many tools each agent should have and how `tool_choice` works, configuring MCP servers in Claude Code, and picking the right built-in tool (Read, Write, Edit, Bash, Grep, Glob) for each job.

> 💡 **Human Angle**: The model can only choose well between tools it can tell apart. Most misrouting is a documentation problem, not a model problem.

---

## 2.1 Design effective tool interfaces with clear descriptions and boundaries

### Key Concept

**The description is how Claude chooses a tool, so it must say what the tool does, what it takes, what it returns, and when to use it instead of its neighbours.**

Claude picks tools mainly from their descriptions. A one-line description such as "Looks up customer info" leaves it guessing between similar tools. Good descriptions state the purpose, input formats, example queries, edge cases and the boundary with similar tools. Overlapping descriptions cause misrouting; renaming tools, sharpening descriptions, or splitting a generic tool into purpose-specific ones fixes it. System prompt wording matters too: a keyword-heavy instruction can pull Claude towards the wrong tool.

**Think of signposts at a junction**: if two signs both say "Town", drivers take whichever they see first.

![Two tools with one-line overlapping descriptions cause misrouting; rewritten descriptions that state purpose, inputs, outputs, examples and when to use the other tool make selection reliable.](/content/skillup/ccaf/images/ccaf-2-1-tool-descriptions.svg)

### Real use

When customers ask to change their account email, a support agent keeps calling `lookup_order`. Both tools had one-line descriptions mentioning "customer". Rewriting them, with `get_customer` covering "account details: email, address, phone; use for account changes" and `lookup_order` covering "order status by order ID; not for account data", stops the misrouting.

### How it works

- **Purpose and boundary**: what it does, and when to use the alternative.
- **Inputs and outputs**: formats, examples, edge cases.
- **Differentiate**: rename and rewrite overlapping tools; split generic ones.
- **Check the system prompt**: keyword-sensitive instructions can override good descriptions.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Rewrite descriptions | Similar tools get confused | Effort per tool |
| Split a generic tool | One tool does unrelated jobs | More tools to manage |
| Rename tools | Names suggest overlapping purposes | Callers must update |

### How to do it

1. List tools that get confused and compare their descriptions side by side.
2. Rewrite each: purpose, inputs, outputs, an example, and "use X instead when…".
3. Review the system prompt for words that pull towards the wrong tool.

### Exam Trap ⚠️

<div class="note-trap">"Add few-shot examples of tool calls" or "use a more capable model" are weaker fixes when the root cause is vague, overlapping descriptions. The first fix is the descriptions themselves.</div>

### Go deeper

- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

---

## 2.2 Implement structured error responses for MCP tools

### Key Concept

**Return errors the agent can act on: set isError, say what kind of failure it was, and whether retrying makes sense.**

An MCP tool signals failure by returning a result with `isError: true`, so the agent sees the error and can react. "Operation failed" gives it nothing to work with. Structured metadata does: an `errorCategory` (transient, validation, business, permission), an `isRetryable` flag, and a clear description, with a customer-friendly explanation for business-rule violations. A query that succeeded with no matches is not an error and shouldn't look like one.

**Think of a doctor's note versus "I'm ill"**: one tells the employer when to expect you back and what to arrange.

![A tool failure returns isError with a category: transient errors are retried, validation errors are fixed and resent, business-rule violations are explained to the customer, and permission errors are escalated; an empty result is a success.](/content/skillup/ccaf/images/ccaf-2-2-mcp-errors.svg)

### Real use

`process_refund` can fail because the payment gateway timed out, the order ID is malformed, the caller lacks permission, or the refund exceeds policy. Returning one generic error made the agent retry everything. Categorised errors let it retry the timeout, fix the ID, escalate the permission problem and explain the policy limit.

### How it works

- **`isError: true`** in the tool result tells the agent the call failed.
- **Transient** (timeout): retryable.
- **Validation** (bad input): fix and resend.
- **Business** (policy violation): not retryable; explain to the customer.
- **Permission**: not retryable by the agent; escalate.
- **Empty result ≠ error**: "no matches" is a valid answer.
- Subagents retry transient errors locally and pass up only what they can't resolve.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Categorised error + `isRetryable` | Any tool that can fail several ways | More error-handling code |
| Generic "failed" | Never | Agent can't choose a recovery |
| Empty success | Query ran but found nothing | Must be distinguishable from failure |

### How to do it

1. Map each failure mode to a category and a retryable flag.
2. Return `isError: true` with that metadata and a readable description.
3. Return an empty result, not an error, when nothing matched.

### Exam Trap ⚠️

<div class="note-trap">Treating "no results found" as an error makes the agent retry a query that worked. Returning uniform "Operation failed" messages makes it retry business-rule violations that will never succeed.</div>

### Go deeper

- [MCP specification: tools (error handling)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

---

## 2.3 Distribute tools appropriately across agents and configure tool choice

### Key Concept

**Give each agent only the tools its role needs; a long tool list makes selection less reliable and invites misuse.**

An agent with many tools (around 18 or more) chooses less reliably, and agents holding tools outside their specialisation tend to misuse them. Scope tools by role, add a narrow cross-role tool only for a frequent need (for example `verify_fact` for a synthesis agent), and route complex cases back through the coordinator. Replace generic tools with constrained ones. `tool_choice` sets how tools are used: `auto` (model decides), `any` (must call some tool), or a forced tool name.

**Think of a surgical tray**: each surgeon gets the instruments for their procedure, not the whole hospital's supply.

![Instead of every agent holding all eighteen tools, each subagent gets a small role-specific set plus one scoped cross-role tool, and tool_choice auto, any or forced controls whether and which tool is called.](/content/skillup/ccaf/images/ccaf-2-3-tool-distribution.svg)

### Real use

A synthesis agent with web search started running its own searches and drifting off-brief. Removing search from it, and giving it one `verify_fact` tool for quick checks, keeps it on synthesis; anything needing real research goes back to the coordinator.

### How it works

- **Fewer tools, better selection**: large sets increase decision complexity.
- **Role-scoped**: only what the role needs.
- **Scoped cross-role tools**: for frequent, simple needs.
- **Constrained tools**: `run_tests` instead of a generic `run_command`.
- **`tool_choice`**: `auto`, `any` (no conversational reply), or `{"type": "tool", "name": "…"}` to force one first.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Role-scoped tool sets | Multi-agent systems | Some requests need routing |
| `tool_choice: any` | You need a tool call, not prose | Model still picks which tool |
| Forced tool | A specific step must run first | No model discretion |

### How to do it

1. List each agent's role and the tools it actually needs.
2. Remove the rest; add narrow cross-role tools only for frequent needs.
3. Set `tool_choice` to force or require tool calls where the workflow depends on it.

### Exam Trap ⚠️

<div class="note-trap">"Give every agent every tool for flexibility" is the trap: selection gets worse and agents stray outside their role. And <code>auto</code> doesn't guarantee a tool call; use <code>any</code> or force the tool.</div>

### Go deeper

- [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

---

## 2.4 Integrate MCP servers into Claude Code and agent workflows

### Key Concept

**Share team MCP servers in the project's .mcp.json with credentials from environment variables; keep personal servers in your user config.**

Project-scoped servers live in `.mcp.json` at the repository root and are committed, so the whole team gets them. Personal or experimental servers are added at user (or local) scope and stored in `~/.claude.json`. `.mcp.json` expands `${VAR}` and `${VAR:-default}`, so tokens come from each developer's environment and never get committed. Tools from all configured servers are discovered at connection time and available together. MCP resources expose catalogs of content so agents don't need exploratory calls to find what exists.

**Think of a shared office phone list with no passwords on it**: everyone dials the same numbers, and each person uses their own login.

![Team MCP servers go in the project .mcp.json, committed, with tokens read from environment variables, while personal servers live in ~/.claude.json; all servers' tools are discovered together, and resources expose content catalogs.](/content/skillup/ccaf/images/ccaf-2-4-mcp-config.svg)

### Real use

A team wants every developer to get the same development-database MCP server, each with their own credentials. They add it to `.mcp.json` with `"Authorization": "Bearer ${DB_TOKEN}"` and commit it. One developer trying an experimental server adds it at user scope, so nobody else is affected.

### How it works

- **Project scope**: `.mcp.json`, committed; Claude Code asks for approval before using these servers.
- **User / local scope**: `~/.claude.json`; personal.
- **Env expansion**: `${VAR}` and `${VAR:-default}` in command, args, env, url and headers.
- **Discovery**: tools from all servers are available at once.
- **Descriptions matter**: detailed MCP tool descriptions stop Claude preferring weaker built-in tools.
- **Prefer community servers** for standard integrations; build custom ones for team-specific workflows.
- **Resources**: expose catalogs so agents see what's available.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Project `.mcp.json` | The whole team needs the server | Each person sets their env vars |
| User scope | Personal or experimental server | Not shared |
| Community server | Standard integration (GitHub, databases) | Less tailored |

### How to do it

1. Add shared servers to `.mcp.json`, with secrets as `${VAR}` references, and commit it.
2. Add personal servers with `claude mcp add --scope user`.
3. Write detailed tool descriptions and expose catalogs as resources.

### Exam Trap ⚠️

<div class="note-trap">Committing a token in <code>.mcp.json</code> is the security trap; use environment variable expansion. Putting a team server in a personal config means teammates don't get it.</div>

### Go deeper

- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
- [MCP specification: resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)

---

## 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

### Key Concept

**Grep searches file contents, Glob finds files by name pattern, Edit changes a unique snippet, and Read plus Write replaces a whole file.**

Each built-in tool has one job. **Grep** searches inside files for patterns: function names, error messages, imports. **Glob** matches file paths, such as `**/*.test.tsx`. **Read** loads a file; **Write** writes a whole file; **Edit** replaces a specific snippet that must be unique in the file. When Edit fails because the anchor text appears more than once, Read the file and Write the corrected version. Build understanding incrementally: Grep for entry points, then Read to follow imports.

**Think of a library**: the catalogue finds books by title (Glob), the index finds pages by word (Grep), and you only photocopy the pages you need.

![Choosing a built-in tool: Grep to search file contents, Glob to find files by name pattern, Read to load a file, Edit for a unique snippet, and Read plus Write when the Edit anchor isn't unique.](/content/skillup/ccaf/images/ccaf-2-5-builtin-tools.svg)

### Real use

To find every caller of `formatCurrency`, Claude Greps for the name, finds it re-exported through a wrapper module, lists the wrapper's exported names, and Greps for each of them. An Edit to a repeated config line fails as non-unique, so Claude Reads the file and Writes the corrected version.

### How it works

- **Grep**: content search across the codebase.
- **Glob**: path patterns, by name or extension.
- **Read / Write**: whole-file operations.
- **Edit**: targeted change; the matched text must be unique.
- **Fallback**: Read + Write when Edit can't find a unique anchor.
- **Trace through wrappers**: collect exported names, then search each one.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Grep | Looking for code or text inside files | Can return many matches |
| Glob | Looking for files by name or extension | Doesn't search contents |
| Edit vs Read + Write | Edit for unique snippets; Read + Write otherwise | Write replaces the whole file |

### How to do it

1. Start with Grep (contents) or Glob (paths) to find entry points.
2. Read the relevant files and follow imports from there.
3. Edit unique snippets; fall back to Read + Write if the anchor repeats.

### Exam Trap ⚠️

<div class="note-trap">Swapping Grep and Glob is the classic trap: "find all test files" is Glob; "find where this function is called" is Grep. Reading every file in the repo up front wastes context; search first, then read.</div>

### Go deeper

- [Claude Code tools reference](https://code.claude.com/docs/en/tools-reference)

---

## Deep Dive: Making Tool Design & MCP Click

### 1. The connective narrative

An agent's choices are only as good as the tools in front of it and what those tools say about themselves. Descriptions (2.1) decide whether Claude picks the right tool. Error responses (2.2) decide whether it recovers sensibly when a tool fails. Distribution (2.3) decides how many choices it faces, and `tool_choice` decides whether it must act.

MCP configuration (2.4) is how those tools reach Claude Code safely and consistently across a team. The built-in tools (2.5) are the everyday toolkit, and using the right one keeps context small and edits reliable.

### 2. Worked scenario

> **Scenario.** A support platform has an orchestrator and three subagents. Each subagent gets only its role's tools, and the synthesis agent gets one `verify_fact` tool (2.3). Customer tools are rewritten so `get_customer` and `lookup_order` describe clear, non-overlapping purposes (2.1).
>
> `process_refund` returns categorised errors: timeouts are retried locally, policy violations come back non-retryable with a customer-friendly message, and "no orders found" is a normal empty result (2.2). The team's ticketing MCP server sits in `.mcp.json` with `${TICKET_TOKEN}` (2.4). Engineers debugging it use Grep to find callers and Glob to list handlers (2.5).

### 3. Memory aid

**DESCRIBE, CATEGORISE, SCOPE, SHARE, PICK**
- **Describe** tools clearly (2.1) · **Categorise** errors (2.2) · **Scope** tools per agent (2.3) · **Share** MCP via `.mcp.json` with env vars (2.4) · **Pick** the right built-in (2.5).

### 4. Exam strategy for this domain

Distractors usually treat a tool-interface problem as a model problem ("use a better model") or remove information the agent needs ("return a simple error"). Pick the option that gives the model clearer choices and richer signals.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Agent calls the wrong of two similar tools | Rewrite descriptions with boundaries |
| One tool does unrelated jobs | Split into purpose-specific tools |
| Tool fails with "Operation failed" | `isError` + category + `isRetryable` |
| Timeout | Transient; retry (locally in the subagent) |
| Policy violation | Not retryable; explain to the customer |
| "No matches" | Valid empty result, not an error |
| Agent with ~18+ tools misroutes | Scope tools by role |
| Must call a tool, not chat | `tool_choice: any` |
| Specific tool first | Forced `tool_choice` |
| Team-wide MCP server | `.mcp.json`, committed |
| Credentials in MCP config | `${VAR}` expansion |
| Personal MCP server | User scope (`~/.claude.json`) |
| Find files by pattern | Glob |
| Find code by content | Grep |
| Edit anchor not unique | Read + Write |
