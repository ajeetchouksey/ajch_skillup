# Domain 2: Claude Code Configuration & Workflows
**Exam Weight: 20%** (official blueprint: Domain 3, "Claude Code Configuration & Workflows")

---

## The Big Idea

Imagine you join a new team. You open Claude Code. It formats your Python with tabs (you hate tabs). It ignores the team's API naming conventions. A colleague on the same repo gets perfect results. What's different? **Configuration.** Claude Code reads instructions from several places (your user files, the project, path-scoped rules, skills) and enforces behaviour from others (permissions, hooks). Knowing which mechanism does what is 20% of the CCA-F exam.

<div class="note-important"><strong>Core Principle:</strong> CLAUDE.md files and rules are <em>context</em>, not enforcement. They are concatenated into Claude's context, and nothing "overrides" anything. If something MUST happen or MUST NOT happen, use permissions or hooks.</div>

---

## 2.1 The CLAUDE.md Hierarchy

### 📖 The Story

Alex is a senior developer who likes 2-space indentation and Conventional Commits everywhere. Their team at Acme Corp has a monorepo with strict architecture rules, and their React components follow naming patterns that differ from their Go services.

Alex needs **three kinds** of instructions:
- Personal preferences (follow Alex across every project)
- Team/project standards (shared with the whole Acme team)
- File-specific requirements (React files get different rules than Go files)

Claude Code covers all three, and the exam tests where each one belongs.

### 🧠 Mental Model: Layers in One Briefing Pack

Think of every instruction file as a page in the same briefing pack handed to Claude at the start of a session:
- **User** (`~/.claude/CLAUDE.md`) = your personal cover note — only in *your* pack
- **Project** (`./CLAUDE.md` or `./.claude/CLAUDE.md`) = the team's shared pages — in everyone's pack via git
- **Directory** (`packages/billing/CLAUDE.md`) = pages added when Claude starts working in that folder
- **Rules** (`.claude/rules/*.md`) = topic pages; with a `paths` glob they're added only when Claude touches matching files

<mark>All pages are read together. Later pages don't cancel earlier ones; if two pages contradict each other, Claude may follow either.</mark>

![Flow diagram for "Mental Model: Layers in One Briefing Pack": Managed policyCLAUDE.mdorg-wide, IT-deployed, ~/.claude/CLAUDE.mdUSER only you, ./CLAUDE.md or./.claude/CLAUDE.mdPROJECT shared via git, subdir/CLAUDE.mdDIRECTORY loads ondemand, .claude/rules/*.mdRULES paths = conditional](/content/skillup/ccaf/images/d2-claude-code-config-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d2-claude-code-config-m1.mmd -->

### The Levels in Detail

| Level | Location | Loaded | Shared? | Use For |
|-------|----------|--------|---------|---------|
| Managed policy | OS-specific path, deployed by IT | Every session | Whole org | Company standards, compliance |
| User | `~/.claude/CLAUDE.md` | At launch | Only you | Personal style, shortcuts |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | At launch | Team, via git | Architecture, team rules |
| Local | `./CLAUDE.local.md` (gitignored) | At launch | Only you | Your sandbox URLs, test data |
| Directory | `subdir/CLAUDE.md` | When Claude reads/edits a file in that subdir | Team, via git | Package-specific conventions |
| Rules | `.claude/rules/*.md` | Unscoped: at launch. With `paths`: when a matching file is read or edited | Team, via git | Topic files, file-type conventions |

<div class="note-scribble">Files in the directories <em>above</em> where you launched load at launch. Files in subdirectories <em>below</em> load on demand. Run <code>/context</code> to see which memory files actually loaded; <code>/memory</code> lists and opens them.</div>

### Level 1: User — Your Personal Preferences

```markdown
# ~/.claude/CLAUDE.md

- Always use TypeScript strict mode
- Prefer functional components over class components
- Use 2-space indentation
- Commit messages: Conventional Commits format
```

This lives on Alex's machine. The team never sees it, and it never goes into version control. That is also why a new teammate doesn't get these instructions: a classic exam diagnosis.

### Level 2: Project — Team-Shared Standards

```markdown
# ./CLAUDE.md (at repo root)

## Architecture
- Monorepo: apps/frontend, apps/backend, packages/shared
- All API responses: {data, error, meta} shape

## Standards
- Testing conventions: @docs/testing.md
- API conventions: @docs/api-conventions.md
```

<div class="note-important"><strong>@import keeps CLAUDE.md modular.</strong> <code>@path/to/file</code> pulls another file into context alongside the CLAUDE.md that references it (relative paths resolve from the importing file; imports can nest up to four hops). Imports organise content but don't save context, because imported files load with their parent.</div>

### Level 3: Rules — Topic Files and Path Scoping

```markdown
---
paths:
  - "apps/frontend/**/*.tsx"
---
# React Component Standards

- Props interface: {ComponentName}Props
- Event handlers: handleClick, handleSubmit
```

The `paths` frontmatter tells Claude Code: "Load this rule only when Claude reads, writes, or edits a file matching one of these globs." A rule without `paths` loads at launch with the same priority as `.claude/CLAUDE.md`.

### The Frontmatter Trap

`paths` (plural) is the **only** field Claude Code reads from a rule's frontmatter. It accepts a YAML list or a comma-separated string, and supports globs such as `**/*.test.tsx` and brace expansion like `src/**/*.{ts,tsx}`.

```yaml
---
paths:
  - "src/**/*.ts"      # ✅ the only field Claude Code reads
---
```

<div class="note-trap"><strong>TRAP:</strong> Options like <code>path:</code> (singular), <code>glob:</code>, <code>applies_to:</code>, <code>scope:</code> or <code>applyTo:</code> (that one is GitHub Copilot's) are all ignored without an error, so the rule silently loads for every file.</div>

### Conflict Walkthrough

| Source | Rule |
|--------|------|
| User | "Use 2-space indentation" |
| Project | "Use 4-space indentation for Python files" |
| Rule (`paths: ["**/*.py"]`) | "Use tabs for indentation" |

When Alex edits a `.py` file, all three instructions are in context and they contradict each other, so **Claude may follow any of them**. The fix isn't to rely on a precedence order; it's to remove the contradiction (for example, delete the indentation line from the project file and keep the Python rule).

<div class="note-scribble">If the exam asks "which rule wins?", the honest answer is "none is guaranteed": instructions are concatenated, ordered from broad to specific. Make the files consistent, or use a hook or linter if the behaviour is mandatory.</div>

---

## 2.2 Skills, Rules, and Tools

### 📖 The Story

Your team lead asks: "I want Claude to know our database schema when writing repository code, AND I want it to be able to run migrations." Two different needs:

1. **Knowing** the schema = context, like having docs open in a tab
2. **Running** a migration = execution, something that changes the world

Context comes from CLAUDE.md, rules, and skills. Execution comes from tools (built-ins like Bash and Edit, or MCP tools).

### 🧠 Mental Model: Library Book vs Power Tool

- A **rule or skill** is a **library book**: you read it and gain knowledge; the book doesn't change the world
- A **tool** is a **power drill**: you use it, holes appear in walls

<mark>Decision rule: "Does it EXECUTE something?" → tool (built-in or MCP). "Does it INFORM Claude?" → CLAUDE.md, a rule, or a skill.</mark>

### Where Each Kind of Context Lives

| You want... | Use | Why |
|---|---|---|
| Facts Claude needs in every session | `CLAUDE.md` | Always loaded |
| Conventions for one file type or area | `.claude/rules/*.md` with `paths` | Loads only when matching files are touched |
| A multi-step procedure or reference used for specific tasks | Skill in `.claude/skills/<name>/SKILL.md` | Description is always visible; the body loads only when invoked or judged relevant |
| To run queries, call APIs, deploy | A tool (built-in or MCP server) | Something has to execute |

### Use Case: Schema-Aware Repository Code

```markdown
<!-- .claude/rules/database-schema.md -->
---
paths:
  - "apps/backend/src/repos/**/*.ts"
---
# Database Schema (Read-Only Context)

| Column | Type | Constraints |
|--------|------|-------------|
| id | uuid | PK, gen_random_uuid() |
| email | text | UNIQUE, NOT NULL |
```

Claude now "knows" the schema whenever it touches repository files. To *query* the live database, you'd add an MCP server.

<div class="note-trap"><strong>TRAP:</strong> Skills don't live in <code>.claude/rules/</code>. Skills are folders under <code>.claude/skills/</code> (or <code>~/.claude/skills/</code>) with a <code>SKILL.md</code>; rules are single Markdown files under <code>.claude/rules/</code>.</div>

---

## 2.3 MCP Server Configuration

### 📖 The Story

Your startup uses a PostgreSQL database, the GitHub API, and an internal search engine. You want Claude Code to query all three through live connections. You need MCP servers.

### 🧠 Mental Model: USB Devices

- Claude Code is the computer
- Each MCP server is a peripheral that brings its own tools
- The transport is the cable: **stdio** for a local process, **HTTP** for a remote server
- The scope decides whose computer the device is plugged into

### Scopes: Who Gets the Server

| Scope | Stored in | Loads in | Shared? |
|---|---|---|---|
| Local (default for `claude mcp add`) | `~/.claude.json` | Current project only | No |
| Project | `.mcp.json` in the repo root | Current project | Yes, via version control |
| User | `~/.claude.json` | All your projects | No |

```bash
# Team-shared server, written to .mcp.json
claude mcp add --scope project --transport http tracker https://mcp.example.com/tracker

# Personal/experimental server, available in all of your projects
claude mcp add --scope user --transport stdio scratch -- npx -y my-experimental-server
```

<div class="note-important"><strong>Project-scoped servers need approval.</strong> In interactive sessions Claude Code asks before using servers from a project's <code>.mcp.json</code>. In <code>claude -p</code> and Agent SDK runs there's no prompt, so those servers load without asking; use <code>--strict-mcp-config</code> or <code>--bare</code> in CI if you don't want repository-defined servers to start.</div>

### A Project `.mcp.json`

```json
{
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["./mcp-servers/db-server.js"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    },
    "search": {
      "type": "http",
      "url": "${SEARCH_URL:-https://search.internal.example.com}/mcp",
      "headers": { "Authorization": "Bearer ${SEARCH_TOKEN}" }
    }
  }
}
```

| Field | Purpose |
|-------|---------|
| `command` + `args` | Launch a local stdio server |
| `type: "http"` + `url` | Connect to a remote server (HTTP is recommended; SSE is deprecated) |
| `env`, `headers` | Credentials and settings, ideally via `${VAR}` expansion |

<div class="note-important"><strong>Environment variable expansion</strong> works in <code>command</code>, <code>args</code>, <code>env</code>, <code>url</code>, and <code>headers</code>: <code>${VAR}</code> or <code>${VAR:-default}</code>. Secrets stay in each developer's shell or CI secret store, never in the committed file. An unset variable with no default stays as the literal text and Claude Code shows a warning.</div>

<div class="note-trap"><strong>TRAP:</strong> MCP servers are configured in <code>.mcp.json</code> (project) or <code>~/.claude.json</code> (local/user), not in CLAUDE.md, not in <code>.claude/rules/</code>, and not via a <code>mcpServers</code> block you hand-write into <code>.claude/settings.json</code>.</div>

---

## 2.4 Non-Interactive Mode (-p Flag)

### 📖 The Story

It's 2 AM. A pull request lands. Your CI pipeline needs to review the diff with no human at the keyboard. Claude Code must run **non-interactively**, read the diff, produce a review, and exit.

### 🧠 Mental Model: The Silent Consultant

- You send a letter (the `-p` prompt)
- They write back (stdout, optionally JSON)
- They leave (exit code)
- They never ask clarifying questions (anything that would need a permission prompt is denied unless you pre-approved it)

### Usage Patterns

```bash
# Basic: prompt in, text out
claude -p "List all TODO comments in src/"

# Pipe input to Claude + prompt
git diff origin/main | claude -p "Find bugs in this diff"

# Machine-parseable, schema-validated output
claude -p "Review this diff" --output-format json \
  --json-schema '{"type":"object","properties":{"findings":{"type":"array"}},"required":["findings"]}' \
  | jq '.structured_output'

# Pre-approve exactly the tools the job needs
claude -p "Run the tests and fix failures" --allowedTools "Bash(npm test *),Read,Edit"
```

| Flag | What it does |
|---|---|
| `-p` / `--print` | Non-interactive: run, print, exit |
| `--output-format text\|json\|stream-json` | JSON includes `result`, `session_id`, cost; with `--json-schema` the validated object is in `structured_output` |
| `--allowedTools` | Tools that run **without a permission prompt** (it doesn't restrict the tool set; `--tools` does) |
| `--bare` | Skip auto-discovery of hooks, skills, plugins, MCP servers, and CLAUDE.md for reproducible CI runs |
| `--max-turns`, `--max-budget-usd` | Cap turns or estimated spend in print mode |

<div class="note-trap"><strong>TRAP:</strong> There is no <code>--headless</code>, <code>--batch</code> or <code>CLAUDE_HEADLESS</code>. The documented non-interactive mode is <code>-p</code>.</div>

### The Exit Code Trap

| Code | Means | What students wrongly think |
|------|-------|----------------|
| **0** | The run succeeded | ❌ "No bugs found" |
| **non-zero** | The run failed (invalid flag, missing authentication, an error that ended the run) | ❌ "Bugs were found" |

<div class="note-important"><strong>Exit 0 = "Claude Code completed the run."</strong> If Claude finds 47 critical security bugs, the run still succeeded. Gate the pipeline on the <em>content</em> (for example a <code>severity</code> field in <code>structured_output</code>), not on the exit code.</div>

<div class="note-scribble">Exit codes describe the MESSENGER, not the MESSAGE.</div>

---

## 2.5 Slash Commands

### 📖 The Story

Your team does code reviews every day, and every time someone retypes the same 8-line prompt. Slash commands save reusable prompts as Markdown files: type `/review` instead.

<mark>A file at `.claude/commands/{name}.md` is invoked as `/{name}`. Custom commands have been merged into skills: `.claude/skills/{name}/SKILL.md` creates the same command and adds supporting files and frontmatter. Existing command files keep working.</mark>

```
.claude/
  commands/
    review.md      → /review
    commit.md      → /commit
  skills/
    scaffold/
      SKILL.md     → /scaffold
```

| Location | Scope |
|---|---|
| `.claude/commands/` or `.claude/skills/` | Project: shared through version control |
| `~/.claude/commands/` or `~/.claude/skills/` | Personal: only you, all projects |

### Use Case: "The Consistent Commit Message"

```markdown
<!-- .claude/commands/commit.md -->
Generate a git commit message for staged changes.

Rules:
1. Conventional Commits: type(scope): description
2. Imperative mood, lowercase, no period
3. Multi-concern changes → suggest splitting into multiple commits

Output ONLY the commit message.
```

<div class="note-trap"><strong>TRAP:</strong> Commands live in <code>.claude/commands/</code> (or as skills in <code>.claude/skills/</code>), not in <code>.claude/rules/</code>, not in CLAUDE.md, and not in a <code>commands</code> array in a config file. <code>~/.claude/commands/</code> is personal and isn't shared with teammates.</div>

---

## 2.6 Permissions

### 📖 The Story

Claude Code runs in four places at your company: developer laptops, a CI review job, a deploy pipeline, and a compliance audit. Each needs different limits. You don't want the CI review bot editing source, and you don't want the audit job making network calls.

### 🧠 Mental Model: Hotel Key Cards, Checked at the Door

- **deny** rules = doors that never open for this guest
- **ask** rules = doors that need the front desk's approval each time
- **allow** rules = doors the card opens without asking

The hotel checks **deny first, then ask, then allow**; the first match decides. An allow rule can't carve an exception out of a deny rule.

### Permission Rules

```json
// .claude/settings.json (project, shared) — .claude/settings.local.json for personal, ~/.claude/settings.json for user-wide
{
  "permissions": {
    "allow": ["Bash(npm run test *)", "Read"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Edit", "Write", "WebFetch", "Read(./.env)"]
  }
}
```

| Rule | Effect |
|---|---|
| `Edit`, `Write` in deny | Claude can't change files |
| `Bash` in deny | Removes the shell entirely |
| `Bash(rm *)` in deny | Blocks matching commands (it matches command text, so pair with other controls for real security) |
| `WebFetch(domain:github.com)` in allow | Allows fetches to that domain only |
| `Read(./.env)` in deny | Blocks reading secrets files |

Reads inside the working directory and a built-in set of read-only commands (such as `ls`, `cat`, and `head`) need no approval. Permission modes (`default`/Manual, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) set the baseline for everything not covered by a rule.

<div class="note-important"><strong>CLAUDE.md can't grant or revoke access.</strong> The permissions docs say it outright: instructions shape what Claude tries, but they don't change what Claude Code allows. Use rules, a permission mode, or a PreToolUse hook.</div>

### Environment Presets

| Environment | Sensible setup | Rationale |
|-------------|------------|-----------|
| 🏠 Local dev | Default mode, allow common test/build commands | Developer is there to approve the rest |
| 🔍 CI review | Deny `Edit`/`Write`; pre-approve only read-only tools | The bot reports; humans decide what to change |
| 🚀 Deploy | Allow only the specific deploy scripts, deny edits | Run known scripts, don't edit source |
| 🛡️ Audit | Read-only, deny `WebFetch` and network commands | Analysis only, no side effects |

<div class="note-trap"><strong>TRAP:</strong> There's no <code>--read-only</code> flag and no "read/write/execute/network" category switch. Read-only is built from deny rules (or plan mode for interactive exploration).</div>

---

## 📋 Domain 2 Cheat Sheet

| Concept | Key Fact |
|---------|----------|
| How instructions combine | All loaded CLAUDE.md files and rules are concatenated; none overrides another |
| User vs project | `~/.claude/CLAUDE.md` is personal and not shared; `./CLAUDE.md` is shared via git |
| Subdirectory CLAUDE.md | Loads on demand when Claude reads/edits a file in that directory |
| Rule frontmatter | Only `paths` (plural) is read; other keys are ignored silently |
| Modular CLAUDE.md | `@path/to/file` imports; `.claude/rules/` topic files |
| Skills | `.claude/skills/<name>/SKILL.md`; on demand; frontmatter controls invocation |
| MCP scopes | local (default, `~/.claude.json`), project (`.mcp.json`), user (`~/.claude.json`) |
| MCP secrets | `${VAR}` / `${VAR:-default}` expansion in `.mcp.json` |
| MCP transports | stdio (local), HTTP (remote, recommended); SSE deprecated |
| Non-interactive mode | `claude -p "prompt"`; `--output-format json` + `--json-schema` → `structured_output` |
| Exit codes | 0 = run succeeded (not "no issues"); non-zero = run failed |
| Commands | `.claude/commands/{name}.md` → `/{name}`; merged into skills |
| Permissions | `.claude/settings.json` allow/ask/deny; deny → ask → allow |
| Inspect memory | `/memory` lists/opens memory files; `/context` shows what loaded |

---

## 🧩 Domain 2 Decision Flowchart

![Flow diagram for "Domain 2 Decision Flowchart": Instructions, Enforcement, New capabilitytools, Team, Just me, Just me,all projects, Whole team,every session, Only for matching files, Only when a task needs it, What are you configuring?](/content/skillup/ccaf/images/d2-claude-code-config-m2.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d2-claude-code-config-m2.mmd -->

<div class="note-scribble">On exam day: "Must it be guaranteed?" → permissions/hooks. "Is it a capability?" → MCP (.mcp.json for the team). "Is it knowledge?" → CLAUDE.md, rules, or skills, chosen by when it's needed.</div>

---

## 3.6 Agent Skills: context: fork, allowed-tools, argument-hint

<div class="note-important"><strong>Explicitly tested in the exam guide.</strong> Skills in <code>.claude/skills/</code> support frontmatter that controls isolation, tool permissions, and argument prompting.</div>

### Skills vs Commands vs CLAUDE.md

| | Commands (.claude/commands/) | Skills (.claude/skills/) | CLAUDE.md |
|---|---|---|---|
| Invocation | User types /name | User types /name, or Claude loads it when relevant | Always loaded |
| Isolation | Same frontmatter as skills (`context: fork` works) | `context: fork` runs it in a subagent | N/A |
| Supporting files | No | Yes (scripts, templates in the skill folder) | Via @imports |
| Best for | Simple saved prompts | Task-specific workflows | Universal standards |

### Frontmatter Options

```markdown
---
description: Scaffold a new module with tests and docs. Use when creating a module.
context: fork
allowed-tools: Write, Edit
disallowed-tools: Bash
argument-hint: "[module-name]"
---
# Scaffold Module Skill

Generate a new module named $ARGUMENTS with tests and documentation.
```

#### `context: fork`

Runs the skill in a **subagent** (the type set by `agent`, `general-purpose` by default) whose prompt is the skill content. The subagent doesn't see your conversation history, and its verbose output stays out of the main session; only its result comes back. Despite the name, it isn't a fork of your current conversation, so the skill's instructions must stand on their own.

Good for:
- **Verbose output** (codebase analysis that dumps hundreds of lines)
- **Exploratory work** (brainstorming alternatives you don't want in the main context)

<div class="note-trap"><strong>TRAP:</strong> A skill produces verbose output and the main conversation fills up. The fix is <code>context: fork</code>.</div>

#### `allowed-tools` (and `disallowed-tools`)

`allowed-tools` lists tools Claude can use **without asking permission** during the turn that invokes the skill. It does **not** restrict which tools are available: every tool stays callable, and your permission settings govern the rest. To remove a tool while the skill is active, use `disallowed-tools` (or a permissions deny rule).

<div class="note-trap"><strong>TRAP (exam vs docs):</strong> The exam guide describes allowed-tools as "restricting tool access during skill execution". On the exam, pick allowed-tools when the question is about scoping a skill's tools. In practice, remember the documented behaviour: it pre-approves; <code>disallowed-tools</code> or deny rules actually block.</div>

#### `argument-hint`

An autocomplete hint showing what to pass, for example `[issue-number]` or `[module-name]`. The arguments arrive in the skill body as `$ARGUMENTS` (or `$0`, `$1`...).

### Personal vs Project Skills

| Location | Scope | Use For |
|---|---|---|
| `.claude/skills/` (project) | Whole team, version-controlled | Shared workflows (scaffold, review) |
| `~/.claude/skills/` (personal) | Just you | Personal variants, experiments |

When names collide, personal skills take precedence over project skills, so create your personal variant under a **different name** to avoid shadowing the team's version.

---

## 3.7 Explore Subagent & /compact

### Explore Subagent

`Explore` is a built-in, read-only subagent for searching and analysing a codebase. It isolates verbose discovery output and returns a summary to the main conversation.

```
Use the Explore subagent to find all callers of authenticate()
and return a summary — not the raw output.
```

![Flow diagram for "Explore Subagent": Spawn, Summary only, Main Agenthigh-level coordination, Explore Subagentverbose discovery, Implementationcontext still clean](/content/skillup/ccaf/images/d2-claude-code-config-m3.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d2-claude-code-config-m3.mmd -->

<div class="note-important"><strong>Combine with plan mode:</strong> plan mode to design, Explore to investigate, then direct execution to implement. Context stays clean at every phase.</div>

### /compact

`/compact` summarises the conversation so far to free context while you keep working in the same session. `/clear`, by contrast, starts over with an empty context.

<div class="note-trap"><strong>TRAP:</strong> An agent gives inconsistent answers mid-session and references "typical patterns" rather than specific classes it found earlier. That's context degradation. The fix is /compact (to summarise) plus scratchpad files (to persist key findings).</div>

### /memory and /context

- `/memory` lists your CLAUDE.md, CLAUDE.local.md and other memory file locations across user and project scopes, opens them for editing, and toggles auto memory.
- `/context` shows what's in the current context window, including which memory files actually loaded at launch.

Both help diagnose "it works on my machine" behaviour, such as a teammate whose instructions live in their own `~/.claude/CLAUDE.md`.

---

## 3.8 Plan Mode vs Direct Execution

### Key Concept

**Plan mode is for decisions; direct execution is for changes you already understand.**

Plan mode lets Claude explore the codebase and design an approach before touching anything: it's built for large-scale or multi-file changes, architectural decisions, and tasks with several valid approaches. Direct execution suits a well-scoped change such as one validation check in one function.

The two combine naturally: plan the migration, approve the plan, then execute it directly. **Plan mode is the architect's drawing; direct execution is the builder working from it.**

### In Practice

**What breaks without this**: Restructuring a monolith in direct mode means discovering service boundaries halfway through dozens of edits, then rewriting them.

**Decision trigger**: Ask whether the stem already states complexity (45+ files, competing integration approaches, "decide service boundaries"). If it does, plan first.

**When you'd choose differently**: A single-file fix with a clear stack trace goes straight to direct execution; planning it is overhead.

### Exam Trap ⚠️

<div class="note-trap">"Start directly and switch to plan mode if it gets complicated" is a distractor when the complexity is already stated in the requirements. The exam wants plan mode up front for architectural work, and direct execution for clearly scoped edits.</div>

---

## Deep Dive

### 1. The connective narrative

Domain 2 is one question asked many ways: **where does this piece of configuration belong?** Start by splitting context from enforcement. CLAUDE.md files, rules, and skills are context: they're concatenated into Claude's window and Claude tries to follow them, but nothing guarantees it. Permissions and hooks are enforcement: Claude Code applies them whatever the model decides.

Within context, the choice is about *who* and *when*. Personal preferences go in `~/.claude/CLAUDE.md`, which is never shared. Team standards go in the project CLAUDE.md, split into `@imports` or `.claude/rules/` topic files when it grows. Conventions for one file type go in a rule with `paths`, so they load only when matching files are touched; that beats subdirectory CLAUDE.md files when the files are scattered (tests next to the code they test). Procedures needed only for certain tasks become skills, which load on demand and can fork into a subagent.

Capabilities come from MCP: `.mcp.json` for the team (with `${VAR}` for secrets), `~/.claude.json` for you. Automation uses `-p` with JSON output and a schema, and session isolation means the reviewer should be a fresh instance, not the session that wrote the code.

### 2. Worked scenario

> **Scenario.** A platform team rolls Claude Code out to 40 developers. Complaints: new hires don't get the API conventions; Terraform rules clutter every session; a "safe" skill still runs shell commands; CI review jobs hang.
>
> **Step 1 — new hires.** The conventions were in one lead's `~/.claude/CLAUDE.md`. Move them to the project CLAUDE.md (or `.claude/rules/api-conventions.md`) and commit.
>
> **Step 2 — Terraform clutter.** Move the Terraform section to `.claude/rules/terraform.md` with `paths: ["terraform/**/*"]`, so it loads only when Terraform files are touched.
>
> **Step 3 — the "safe" skill.** Its `allowed-tools: Write` only pre-approved writes. Add `disallowed-tools: Bash`, and a `Bash(rm *)` deny rule in `.claude/settings.json` for good measure.
>
> **Step 4 — CI hangs.** The job ran `claude "review..."` interactively. Switch to `claude -p ... --output-format json --json-schema ...`, read `structured_output`, and gate on finding severity, not the exit code.
>
> **Outcome:** each problem was a placement error. The fix in every case was moving configuration to the mechanism that matches its scope, timing, and need for enforcement.

### 3. Memory aid

**SCOPE** — questions to place any Claude Code configuration:
- **S**hared or personal? (project files vs `~/.claude/...`)
- **C**ontext or control? (CLAUDE.md/rules/skills vs permissions/hooks)
- **O**n demand or always? (skills and `paths` rules vs CLAUDE.md)
- **P**ipeline? (`-p`, `--output-format json`, `--json-schema`)
- **E**xternal capability? (MCP: `.mcp.json` or `~/.claude.json`)

### 4. Exam strategy for this domain

- Most questions name a symptom ("new teammate doesn't get the rules", "the job hangs", "rules load everywhere") and test whether you can trace it to a location or flag.
- Distractors invent mechanisms: `--headless`, `--batch`, `--read-only`, `CLAUDE_HEADLESS`, `.claude/config.json`, `applyTo`. If you've never seen it in the docs, it's probably a distractor.
- When an option says a CLAUDE.md instruction will *guarantee* behaviour, it's wrong; guarantees come from permissions and hooks.
- Five minutes before the exam: **who sees it, when does it load, and does it have to be enforced?**
