# D2: Claude Code Configuration & Workflows

> **Exam weight**: 20% · **Questions**: ~51 in the bank · Official exam guide numbering: Domain 3, objectives 3.1–3.6

## Overview

This domain covers how a team shapes Claude Code: where instructions live (CLAUDE.md hierarchy, imports and `.claude/rules/`), reusable workflows (custom commands and skills), rules that load only for matching files, when to plan before acting, how to iterate towards a correct result, and running Claude Code non-interactively in CI.

> 💡 **Human Angle**: Most "Claude ignored our standards" problems are configuration problems: the instruction was in the wrong file, loaded for the wrong person, or never loaded at all.

---

## 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organisation

### Key Concept

**Put each instruction where the right people get it: team standards in the project, personal preferences in your user file, topic detail in rules or imports.**

Claude Code loads CLAUDE.md from several levels and combines them rather than letting one override another. `~/.claude/CLAUDE.md` is personal and applies to all your projects, but isn't shared with teammates. `./CLAUDE.md` (or `.claude/CLAUDE.md`) is the project file, committed for the team. CLAUDE.md files in subdirectories load when Claude works on files there. `@path/to/file` imports another file, up to four hops deep, and `.claude/rules/` holds topic-specific files instead of one huge CLAUDE.md.

**Think of company policy, team handbook and your own sticky notes**: each has its own audience, and putting a team rule on your sticky note means nobody else sees it.

![Claude Code instruction sources: user-level CLAUDE.md for you only, project CLAUDE.md shared via git, subdirectory CLAUDE.md loaded when working there, plus @imports and .claude/rules files, all combined into context.](/content/skillup/ccaf/images/ccaf-3-1-claude-md-hierarchy.svg)

### Real use

A new developer's Claude Code ignores the team's commit format. The rule was in a senior engineer's `~/.claude/CLAUDE.md`, so only that engineer ever had it. Moving it to the project CLAUDE.md, committed to git, fixes it for everyone; `/memory` confirms which files each session loads.

### How it works

- **User** `~/.claude/CLAUDE.md`: only you, all projects.
- **Project** `./CLAUDE.md`: shared through version control.
- **Local** `./CLAUDE.local.md`: personal, project-specific, gitignored.
- **Subdirectory** CLAUDE.md: loaded on demand when Claude touches files there.
- **`@import`**: pull in a standards file; relative to the importing file; max depth four.
- **`.claude/rules/`**: one topic per file, discovered recursively.
- **`/memory`**: shows which memory files are loaded.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Project CLAUDE.md | Every teammate needs it | Grows large without discipline |
| User CLAUDE.md | Only your own preferences | Invisible to the team |
| `@import` or `.claude/rules/` | Standards differ by package or topic | More files to keep tidy |

### How to do it

1. Move team-wide rules into the project CLAUDE.md and commit it.
2. Split long sections into `.claude/rules/*.md` or `@import` per-package standards.
3. Run `/memory` to confirm what loads when behaviour seems inconsistent.

### Exam Trap ⚠️

<div class="note-trap">"A new teammate isn't getting the instructions" almost always means they're in someone's user-level file. And files don't override each other: they're all concatenated, so contradictory instructions anywhere in the hierarchy cause inconsistent behaviour.</div>

### Go deeper

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)

---

## 3.2 Create and configure custom slash commands and skills

### Key Concept

**Use a skill or command for a workflow you invoke on demand; use CLAUDE.md for standards that must always be loaded.**

A file in `.claude/commands/` and a skill in `.claude/skills/<name>/SKILL.md` both create a `/name` command; Claude Code has merged commands into skills, and skills add supporting files and richer frontmatter. Project-level ones are committed for the team; personal ones live under `~/.claude/`. Frontmatter controls behaviour: `allowed-tools` limits tools during the skill, `argument-hint` prompts for parameters, and `context: fork` runs the skill in an isolated subagent so its verbose output stays out of your main conversation.

**Think of a recipe card versus the kitchen rules on the wall**: you pull out the recipe when you cook that dish; the rules apply to everything.

![Where reusable instructions live: project skills and commands shared via git, personal ones in your home folder, frontmatter for allowed-tools, argument-hint and context fork, and CLAUDE.md for always-on standards.](/content/skillup/ccaf/images/ccaf-3-2-commands-skills.svg)

### Real use

A team wants shared `/review`, `/test` and `/commit` workflows. They add them as project skills so every clone gets them. The verbose `/review` runs with `context: fork`, so the main session receives only its summary. A developer who wants a terser review creates a personal variant with a different name, so teammates aren't affected.

### How it works

- **Project**: `.claude/skills/` or `.claude/commands/`, committed and shared.
- **Personal**: `~/.claude/skills/` or `~/.claude/commands/`; use a different name for personal variants.
- **`context: fork`**: runs in a fresh subagent that doesn't see your conversation; instructions must stand alone.
- **`allowed-tools`**: restricts tools while the skill runs.
- **`argument-hint`**: shows which arguments to pass.
- **`disable-model-invocation`**: only you can trigger it, useful for side effects like `/commit`.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Skill or command | Task-specific workflow, invoked when needed | Must be invoked |
| CLAUDE.md | Universal standards for every task | Always uses context |
| `context: fork` | Output is verbose or exploratory | Doesn't see the conversation |

### How to do it

1. Create `.claude/skills/<name>/SKILL.md` with a clear description and steps.
2. Add `allowed-tools`, `argument-hint` and, for noisy skills, `context: fork`.
3. Commit project skills; keep personal variants under `~/.claude/` with distinct names.

### Exam Trap ⚠️

<div class="note-trap">Putting a team command in <code>~/.claude/commands/</code> means only you have it. Editing a shared project skill to suit your personal taste changes it for everyone; create a personal variant with a different name instead. And always-on standards belong in CLAUDE.md, not in a skill nobody invokes.</div>

### Go deeper

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)

---

## 3.3 Apply path-specific rules for conditional convention loading

### Key Concept

**A rule file with a paths glob loads only when Claude works on matching files, wherever they sit in the repository.**

Files in `.claude/rules/` can start with YAML frontmatter containing a `paths` field of glob patterns. Such rules load only when Claude reads or edits a matching file, which keeps irrelevant conventions out of context and saves tokens. Globs match by file type or pattern across the whole repo, which a subdirectory CLAUDE.md can't do.

**Think of a sign that lights up only in the room it applies to**: the test rules glow only when you're near a test file.

![A rule file with paths set to **/*.test.tsx loads when Claude edits any test file in any folder, while a subdirectory CLAUDE.md only covers files under its own folder.](/content/skillup/ccaf/images/ccaf-3-3-path-rules.svg)

### Real use

Test files live next to their components in dozens of folders. A subdirectory CLAUDE.md would need copying into every folder. One `.claude/rules/testing.md` with `paths: ["**/*.test.tsx"]` applies the testing conventions to every test file, and stays out of context the rest of the time.

### How it works

- Frontmatter `paths:` takes one or more glob patterns, for example `**/*.test.tsx` or `src/api/**/*.ts`.
- The rule loads when Claude works with a matching file; otherwise it isn't in context.
- Rules without `paths` load for every session.
- Subdirectory CLAUDE.md applies by location only.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Path-scoped rule | Convention follows a file type spread across folders | Glob must be right |
| Subdirectory CLAUDE.md | Convention belongs to one folder tree | Doesn't reach files elsewhere |
| Unscoped rule | Applies to all work | Always uses tokens |

### How to do it

1. Create `.claude/rules/<topic>.md`.
2. Add frontmatter with `paths:` listing the glob patterns it applies to.
3. Edit a matching file and check with `/memory` that the rule loaded.

### Exam Trap ⚠️

<div class="note-trap">For conventions that span many directories (all test files, all Terraform files), the answer is a path-scoped rule with a glob, not copies of CLAUDE.md in each folder and not one root CLAUDE.md that loads everything for every task.</div>

### Go deeper

- [Organize rules with .claude/rules/](https://code.claude.com/docs/en/memory)

---

## 3.4 Determine when to use plan mode vs direct execution

### Key Concept

**Plan first when the change is large, multi-file or has several valid designs; act directly when it's small and clear.**

Plan mode lets Claude explore the codebase and propose an approach without editing anything, so architectural choices are agreed before work starts and costly rework is avoided. Direct execution suits well-scoped changes such as a single-file fix with a clear stack trace. The built-in Explore subagent does verbose discovery in its own context and returns a summary, keeping the main conversation lean during long tasks.

**Think of an architect's drawing versus fixing a squeaky hinge**: you don't draw plans for a hinge, and you don't knock down walls without them.

![Task size decides the mode: a single-file fix with a clear cause goes straight to direct execution, while a migration or restructuring goes to plan mode with Explore for discovery, then direct execution to implement the agreed plan.](/content/skillup/ccaf/images/ccaf-3-4-plan-mode.svg)

### Real use

This week a team must refactor error-handling middleware that 40 backend files depend on, and fix a typo in a button label. The refactor starts in plan mode, with Explore mapping every call site, and the agreed plan is then executed. The typo is fixed directly.

### How it works

- **Plan mode**: read-only exploration and a proposed plan; nothing changes until you approve.
- **Direct execution**: Claude edits immediately.
- **Explore subagent**: read-only, isolated context; returns a summary of what it found.
- **Combine**: plan to investigate and decide, then execute directly.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Plan mode | Migrations, restructuring, multi-file or architectural changes | Slower start |
| Direct execution | One clear, well-scoped change | Risky if scope is misjudged |
| Explore subagent | Discovery output would flood the main context | Summary may omit detail |

### How to do it

1. Judge the scope: number of files, design choices, risk.
2. For large changes, enter plan mode and let Explore map the code; review the plan.
3. Approve and execute; for small changes, skip straight to execution.

### Exam Trap ⚠️

<div class="note-trap">Plan mode for a one-line fix wastes time, and direct execution for a library migration invites rework. The exam pairs plan mode with "architectural", "multiple valid approaches" and "many files"; direct execution with "single file" and "clear stack trace".</div>

### Go deeper

- [Common workflows](https://code.claude.com/docs/en/common-workflows)

---

## 3.5 Apply iterative refinement techniques for progressive improvement

### Key Concept

**When prose isn't working, show examples or tests; when the domain is new, let Claude interview you first.**

If a transformation is described in words and Claude keeps interpreting it differently, two or three concrete input/output examples settle it. Test-driven iteration writes the tests first (expected behaviour, edge cases, performance) and feeds failures back until they pass. The interview pattern asks Claude to question you before implementing, surfacing things like cache invalidation or failure modes. Interacting problems go in one message; independent ones can be fixed one at a time.

**Think of a tailor**: measurements beat descriptions, a fitting reveals what's off, and a good tailor asks questions before cutting.

![Four refinement techniques: concrete input-output examples when descriptions are misread, tests first with failures fed back, an interview before building in unfamiliar areas, and batching interacting issues into one message.](/content/skillup/ccaf/images/ccaf-3-5-iterative-refinement.svg)

### Real use

A date-parsing function keeps mishandling formats despite a careful description. Three input/output pairs fix the interpretation. The team then writes tests for edge cases (leap years, time zones), shares the failures, and iterates until they're green.

### How it works

- **Examples**: 2–3 input/output pairs beat paragraphs of description.
- **Tests first**: failures are precise, objective feedback.
- **Interview**: "ask me questions before you start" surfaces hidden requirements.
- **Batch interacting issues**: fixes that affect each other need to be seen together.
- **Sequence independent issues**: one at a time keeps each change clear.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Input/output examples | Descriptions are interpreted inconsistently | Examples must cover the edge cases |
| Test-driven iteration | Behaviour can be specified as tests | Writing tests first takes time |
| Interview pattern | Unfamiliar domain, unclear requirements | Extra round-trip before code |

### How to do it

1. Replace a vague description with 2–3 concrete examples.
2. Write tests for behaviour and edge cases; iterate by pasting failures.
3. In unfamiliar areas, ask Claude to interview you before implementing.

### Exam Trap ⚠️

<div class="note-trap">Re-describing the same requirement in longer prose rarely fixes inconsistent output; examples do. And sending interacting issues one at a time causes fixes that break each other.</div>

### Go deeper

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

---

## 3.6 Integrate Claude Code into CI/CD pipelines

### Key Concept

**In CI, run Claude Code non-interactively with -p, ask for schema-shaped JSON, and give it project context through CLAUDE.md.**

`claude -p "<prompt>"` (or `--print`) runs without a terminal, so the job never hangs waiting for input. `--output-format json` returns a machine-readable result, and adding `--json-schema` puts output matching your schema in a `structured_output` field, ready to post as inline PR comments. CLAUDE.md carries testing standards, fixtures and review criteria into the run. A review is more effective from an independent session than from the session that wrote the code.

**Think of a night-shift inspector with a written checklist**: nobody is there to answer questions, so everything they need is in the brief and the form.

![A CI job runs claude -p with output-format json and a JSON schema, reads project standards from CLAUDE.md and prior findings, and posts structured findings as inline PR comments from an independent review session.](/content/skillup/ccaf/images/ccaf-3-6-ci-cd.svg)

### Real use

A team reviews every PR in CI. The job runs `claude -p` with a findings schema (file, line, severity, issue, fix) and posts each finding as an inline comment. After new commits, it passes the previous findings in and asks only for new or still-unaddressed issues, so comments aren't duplicated.

### How it works

- **`-p` / `--print`**: non-interactive; no input hangs.
- **`--output-format json`** + **`--json-schema`**: result in `structured_output`; check the field exists before using it.
- **`--allowedTools`**: allow only what the job needs.
- **CLAUDE.md**: testing standards, fixtures, review criteria.
- **Re-runs**: include prior findings; report only new or unresolved ones.
- **Test generation**: include existing tests so it doesn't duplicate covered scenarios.
- **`--bare`** skips CLAUDE.md, hooks and MCP discovery, so pass needed context explicitly if you use it.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `-p` with JSON schema | Output feeds automation | Must handle a missing `structured_output` |
| Independent review session | Reviewing generated code | Extra run |
| `--bare` | Reproducible runs with no local config | Project CLAUDE.md and rules don't load |

### How to do it

1. Call `claude -p` with `--output-format json --json-schema '<schema>'` and a minimal `--allowedTools`.
2. Document review criteria and test conventions in CLAUDE.md.
3. On re-runs, include previous findings and ask only for new or unaddressed issues.

### Exam Trap ⚠️

<div class="note-trap">A CI job that "hangs" usually ran Claude Code without <code>-p</code>. Asking the generating session to review its own code is weaker than an independent instance. And adding <code>--bare</code> silently drops project CLAUDE.md and rules from the run.</div>

### Go deeper

- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

---

## Deep Dive: Making Claude Code Configuration Click

### 1. The connective narrative

This domain is about putting the right context in front of Claude at the right moment. CLAUDE.md (3.1) is the always-on layer, and where it lives decides who gets it. Skills and commands (3.2) are on-demand layers for specific workflows. Path-scoped rules (3.3) are conditional layers that load only for matching files. Together they balance "Claude knows our standards" against "Claude's context isn't full of irrelevant rules".

The other three lessons are about working style. Plan mode (3.4) decides when to think before acting. Iterative refinement (3.5) gives Claude objective feedback (examples, tests) instead of ever-longer descriptions. CI (3.6) puts all of it to work with no human present: non-interactive flags, structured output, and project context loaded from the same files.

### 2. Worked scenario

> **Scenario.** A monorepo team sets up Claude Code. Shared conventions (package manager, commit format) go in the project CLAUDE.md; one developer's preference for terse answers stays in their `~/.claude/CLAUDE.md` (3.1). Backend error-handling standards load through a rule with `paths: ["services/**/*.ts"]` so they stay out of frontend sessions (3.3).
>
> Shared `/review`, `/test` and `/commit` skills are committed; `/commit` disables model invocation so it only runs when a developer asks (3.2). A middleware refactor starts in plan mode (3.4). In CI, `claude -p` with a JSON schema posts findings as inline comments, and re-runs report only new issues (3.6).

### 3. Memory aid

**ALWAYS, ON-DEMAND, WHEN-MATCHED**
- **Always**: CLAUDE.md (project for the team, user for you).
- **On demand**: skills and commands.
- **When matched**: path-scoped rules.

### 4. Exam strategy for this domain

Most traps put an instruction at the wrong scope: personal when it should be shared, always-on when it should be conditional, or directory-based when the convention follows a file type. Find who needs the instruction and when, then pick the mechanism that matches.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| New teammate doesn't get team rules | Rules are in a user file; move to project CLAUDE.md |
| Personal style preference | `~/.claude/CLAUDE.md` (or CLAUDE.local.md) |
| CLAUDE.md is huge | Split into `.claude/rules/` or `@import` |
| Which memory files are loaded? | `/memory` |
| Team-wide command | `.claude/skills/` or `.claude/commands/`, committed |
| Verbose skill clutters the session | `context: fork` |
| Limit tools inside a skill | `allowed-tools` |
| Conventions for all test files | Rule with `paths: ["**/*.test.tsx"]` |
| Library migration or restructuring | Plan mode (then execute) |
| Single-file fix, clear stack trace | Direct execution |
| Prose misread repeatedly | 2–3 input/output examples |
| CI job hangs | Add `-p` |
| Machine-readable CI findings | `--output-format json --json-schema` |
| Duplicate PR comments on re-run | Pass prior findings; report only new ones |
