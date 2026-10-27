# Domain 2: Use GitHub Copilot Features

> **Exam Weight:** 27% | **GH-300 GitHub Copilot Certification**

---

## Overview

This is the highest-weight domain (25–30% in the GH-300 skills measured as of August 7, 2026). It covers the full breadth of Copilot's feature set: triggering Copilot in the IDE, GitHub Copilot CLI, agentic features (agent mode, MCP, subagents, cloud agent), code review and customisation, Chat usage, and organisation-wide administration.

---

## 1. Using Copilot in the IDE

### Key Concept

**Copilot has one subscription but many entry points: inline suggestions, chat, agent mode and the CLI.**

This section covers enabling Copilot and choosing how to trigger it. Inline suggestions appear as ghost text while you type; Chat answers questions and proposes code; agent mode plans and carries out multi-step tasks; Copilot CLI brings the same agent to the terminal. All of them use the same GitHub account and the same organisation policies.

Picking the entry point is about how much you want Copilot to drive. Inline keeps you typing, Chat keeps you deciding, agent mode lets Copilot act and asks for approval at checkpoints. **Think of it as a car's gearbox: same engine, different gears for different speeds.**

### In Practice

**What breaks without this**: Developers who only know inline completion fight the tool on multi-file work, while developers who jump straight to agent mode for a one-line fix burn AI credits and review time on a change they could have typed.

**Decision trigger**: Ask "am I completing code I am already writing, asking a question, or handing over a task?" Those map to inline, Chat, and agent mode or CLI respectively.

**When you'd choose differently**: If an organisation has disabled a surface by policy (for example Copilot CLI or MCP), the "best" entry point is whichever one is allowed; policy beats preference.

### Exam Trap ⚠️

<div class="note-trap">
Content exclusion support differs by surface. GitHub's docs state that content exclusion is currently not supported in the Edit and Agent modes of Copilot Chat in Visual Studio Code, while inline suggestions and Ask-style chat in VS Code do honour it. An answer claiming exclusions apply identically "everywhere in every IDE" is wrong. Think of exclusions as a guest list checked at some doors, not every door.
</div>

### Supported IDEs and surfaces

GitHub documents Copilot in Visual Studio Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse, Vim/Neovim and Azure Data Studio, plus the GitHub website, GitHub Mobile, the GitHub Copilot app and GitHub Copilot CLI. Feature depth varies: inline suggestions are the most widely supported, while chat and agent support vary by IDE (see the content exclusion support table in Domain 6).

### Enabling Copilot

1. Make sure your account has a Copilot plan (Free, Student, Pro, Pro+, Max, or a Business/Enterprise seat from an organisation).
2. Install or enable GitHub Copilot in your IDE (for example the GitHub Copilot extension from the VS Code Marketplace or JetBrains Marketplace).
3. Sign in with the GitHub account that holds the plan or seat.
4. If your seat comes from an organisation, the features you see depend on the policies the organisation or enterprise has enabled.

### Inline Suggestions (Ghost Text)

- Copilot shows grey "ghost text" as you type.
- **Accept:** `Tab`
- **Dismiss:** `Escape` (or keep typing)
- **Accept next word:** `Ctrl+Right` (VS Code on Windows/Linux; `Cmd+Right` on macOS)
- **Alternatives:** hover over the suggestion to see other options
- **Next edit suggestions (NES):** Copilot predicts the next edit you are likely to make; a gutter arrow marks it, `Tab` jumps to it and `Tab` again accepts it.
- Inline suggestions can be enabled or disabled for all languages or for specific languages (Status Bar Copilot menu, or the `github.copilot.enable` setting).

### Triggering Copilot Chat

- **Chat view**: the side panel for conversations and agent sessions.
- **Inline chat**: ask for an in-place edit at the cursor, or for a terminal command in the terminal.
- **Quick Chat**: a temporary conversation that does not occupy the Chat view.
- **Built-in agents in VS Code**: **Agent** (plans and edits, runs tools), **Plan** (builds a plan before code is written) and **Ask** (answers questions). Edit mode is deprecated as of VS Code 1.110 and its setting is supported only through 1.126; multi-file editing is now done with Agent.

### Content Exclusions from the IDE Perspective

- Exclusions are configured on GitHub (repository, organisation or enterprise settings), not in the IDE. The IDE fetches them.
- In an excluded file you get **no inline suggestions**, and its content is not used to inform suggestions or chat answers elsewhere.
- A diagonal line through the Copilot status bar icon shows that the current file is excluded; hovering shows which setting applies.
- After a change, IDEs that already loaded settings can take **up to 30 minutes** to pick it up. In VS Code run **Developer: Reload Window**; in JetBrains and Visual Studio close and reopen the application; Vim/Neovim fetch exclusions each time a file is opened.
- Exclusions apply only to users whose seat comes from a Copilot Business or Enterprise plan; individual plans do not include content exclusion.

---

## 2. GitHub Copilot CLI

### Key Concept

**Copilot CLI is the Copilot agent in your terminal: the `copilot` command, not the retired `gh copilot` extension.**

This section defines the tool and how to install it. GitHub Copilot CLI lets you ask questions, write and debug code, run commands and work with GitHub.com (for example, make changes and open a pull request) from the terminal on Linux, macOS and Windows. The older `gh-copilot` extension with `gh copilot suggest` and `gh copilot explain` was deprecated in September 2025 and stopped working on October 25, 2025.

The CLI runs in two modes. Interactive mode (`copilot`) is a conversation you steer; programmatic mode (`copilot -p "..."`) runs one prompt and exits, which makes it scriptable. **Think of interactive mode as pair programming at the terminal and `-p` as leaving a note for a colleague who finishes the job and logs off.**

### In Practice

**What breaks without this**: Onboarding docs that still say `gh extension install github/gh-copilot` send new developers to a retired tool, and scripts that call `gh copilot suggest` simply fail.

**Decision trigger**: Ask "do I want to steer this, or run it unattended?" Steering means interactive `copilot`; unattended (CI jobs, scripts) means `copilot -p` with explicit `--allow-tool` and `--deny-tool` rules.

**When you'd choose differently**: For a quick, single shell-command question inside the editor, the IDE's terminal inline chat may be faster than starting a CLI session.

### Exam Trap ⚠️

<div class="note-trap">
Older practice material asks for `gh extension install github/gh-copilot` as "the" install command. That extension is retired. Current install options are `npm install -g @github/copilot` (Node.js 22 or later), `winget install GitHub.Copilot`, `brew install --cask copilot-cli`, or the install script (`curl -fsSL https://gh.io/copilot-install | bash`); since January 2026, running `gh copilot` from GitHub CLI can install and launch it. Do not let an old answer key overrule the current docs.
</div>

### Installation

```bash
# npm (all platforms, Node.js 22+)
npm install -g @github/copilot

# Windows
winget install GitHub.Copilot

# macOS / Linux
brew install --cask copilot-cli
curl -fsSL https://gh.io/copilot-install | bash
```

Prerequisites: an active Copilot plan; PowerShell 6+ on Windows. If your seat comes from an organisation or enterprise, the admin must not have disabled Copilot CLI by policy.

### Key Features and Commands

| What | How |
|------|-----|
| Start an interactive session | `copilot` |
| Run one prompt and exit (scripts, CI) | `copilot -p "Summarise the failing tests" --allow-tool='shell(npm)'` |
| Switch between standard, plan and autopilot mode | `Shift+Tab` (or `/plan PROMPT` to plan before coding) |
| Change model | `/model` or `--model` |
| Manage MCP servers | `/mcp` |
| See or shrink context usage | `/context`, `/compact` |
| Select a custom agent | `/agent` |
| Allow access to another directory | `/add-dir PATH` |
| Include a file / an issue or PR | `@FILENAME` / `#NUMBER` |
| Run a local shell command | `!COMMAND` |
| Resume an earlier session | `/resume` or `--resume` (choose from a list); `--continue` (most recent session in this directory) |
| Hand a task to Copilot cloud agent | `/delegate PROMPT`, or prefix a prompt with `&` |
| Run parts of a task as parallel subagents | `/fleet PROMPT` |

### Tool Approval and Trust

- On first launch in a directory you confirm that you trust it (and its subdirectories). Do not launch from your home directory.
- When Copilot wants to run a tool you can allow it once, allow it for the rest of the session, or refuse with feedback.
- `--allow-tool` allows specific tools (for example `shell(git)` or `write`), `--allow-all-tools` allows everything, and `--deny-tool` blocks specific tools and **takes precedence** over both allow options.
- Auto-approval increases the risk of data loss; local sandboxing is available with `/sandbox enable`.
- Copilot CLI respects content exclusion for Copilot Business and Enterprise users.

### Sessions, Scripts and Files

- A session keeps the conversation, so you can refine a script over several turns. Session-wide tool approvals do not carry over to new or resumed sessions.
- Background compaction starts as the conversation approaches 80% of the token limit (closer to 90% if static context already uses about 75%); if usage reaches about 95% first, the CLI waits for compaction to finish. Use `/compact` to do it yourself.
- `/delegate` hands the task to Copilot cloud agent: Copilot offers to commit unstaged changes to a new branch as a checkpoint, then the cloud agent opens a draft pull request and requests your review. Unlike autopilot mode, which runs locally, delegated work keeps going if you shut down your machine. Organization users need both the Copilot CLI policy and the Copilot cloud agent policy enabled.
- For scripts, `-s` (silent) suppresses session metadata so captured output is clean text, and `--no-ask-user` stops the agent asking clarifying questions.
- Typical uses: generate a Bash or PowerShell script, rename or reorganise files, explain a complex `git` or `awk` command, fix a failing build, open a pull request on GitHub.com.

---

## 3. Advanced Copilot Features

### Key Concept

**Agent mode, MCP, subagents and the cloud agent extend Copilot from suggesting code to completing tasks.**

This section covers the agentic features. Agent mode plans a task, edits the files it decides on, runs tools and terminal commands (with approval) and iterates until done. MCP (Model Context Protocol) connects agents to external tools and data. Subagents do focused pieces of work in their own context and return a result, which keeps the main conversation lean. Copilot cloud agent (formerly called the coding agent) works in an ephemeral cloud environment and returns a pull request.

These features differ in where the work runs and who watches it. Agent mode runs locally while you watch; the cloud agent runs remotely while you do something else. **Think of agent mode as a colleague at your desk and the cloud agent as a contractor who sends back a pull request.**

### In Practice

**What breaks without this**: A long agent session that explores five possible approaches fills its own context window with dead ends, and answer quality drops; a subagent would have done the exploration in a separate context and returned only the conclusion.

**Decision trigger**: Ask "does this task need me watching each step?" Yes means local agent mode; no, with a clear issue and acceptance criteria, means delegate to the cloud agent; "I need side research" means a subagent.

**When you'd choose differently**: Delegation adds model usage and coordination cost, so VS Code's own guidance is that a direct request is often enough for quick lookups or small edits.

### Exam Trap ⚠️

<div class="note-trap">
GitHub App-based Copilot Extensions were sunset on November 10, 2025 in favour of MCP servers, and Copilot knowledge bases were retired on November 1, 2025 in favour of Copilot Spaces. Answers recommending "install a Copilot Extension" or "create a knowledge base" for new work describe retired features. Think of MCP and Spaces as the new plugs that replaced the old sockets.
</div>

### Agent Mode

- Plans, edits multiple files, runs terminal commands and tools, and self-corrects based on results (for example, test failures).
- Select **Agent** from the agent picker in the Chat view. Use **Plan** first if you want a reviewed plan before code changes.
- A permissions picker controls how much autonomy the agent has; review the diff before committing, because stopping a request does not undo completed actions.

### Copilot Edits

- Copilot Edits was the multi-file editing experience where you chose the files and reviewed proposed diffs per file.
- In VS Code, Edit mode is deprecated (1.110) and supported only through 1.126; Agent now handles multi-file edits. The GH-300 outline still names Copilot Edits, so know the concept: **you choose the working set, Copilot proposes diffs, you accept or reject each.**

### Model Context Protocol (MCP)

```
Copilot agent  <->  MCP server  <->  External systems
                                 (issue trackers, databases, docs, APIs)
```

- MCP is an open standard; an MCP server exposes tools and data to the agent.
- Organisations control MCP through the **MCP servers in Copilot** policy.
- Spaces can be used from the IDE through the GitHub MCP server.
- In VS Code, share a server with the team in the workspace `.vscode/mcp.json` (top-level `servers` key), or keep it personal in the user-profile `mcp.json`. Add one with **MCP: Add Server** or by searching `@mcp` in the Extensions view.
- A chat request can have at most 128 tools enabled; deselect tools or whole MCP servers in the tools picker if you hit the limit.

### Agent Sessions and Subagents

- **Agent sessions**: VS Code's Chat view and Agents window manage local, cloud and Copilot CLI sessions; a CLI session can be resumed in VS Code, and a VS Code Copilot session can be continued in the terminal with **Resume in Terminal**.
- **Subagents**: "A subagent works in its own context and returns a focused result to the main agent." A local subagent does not inherit the main conversation history and is stateless (no follow-up messages). Custom agents in `.github/agents/` can be invoked as subagents; set `user-invocable: false` to hide a helper from the agents dropdown, or `disable-model-invocation: true` to stop other agents calling it. The benefit is **optimised context usage**: intermediate work stays out of the main conversation, so write each delegated task to be self-contained.

### Copilot Cloud Agent

- Start from the agents panel, a conversation, or an issue or pull request on GitHub.com.
- Works on one branch at a time and opens one pull request per task; only works with repositories hosted on GitHub; maximum session time 59 minutes.
- Can change only the repository specified when the task starts, so a cross-repository change needs one task per repository.
- Customise with custom instructions, custom agents and skills, MCP servers, hooks, and `.github/workflows/copilot-setup-steps.yml` (a single job named `copilot-setup-steps`, read from the default branch) to install tools or dependencies before Copilot starts; its `timeout-minutes` can only lower the 59-minute limit.

### GitHub Copilot Spaces

- Collections of context (repositories, code, pull requests, issues, free text, images, uploads) that ground Copilot's answers.
- GitHub-based sources update automatically as they change.
- Organisation-owned spaces can be shared with admin, editor or viewer roles; personal spaces can be private, shared with specific users or public.
- Anyone with a Copilot licence, including Copilot Free, can create and use Spaces. Use them in Copilot Chat on GitHub or from the IDE through the GitHub MCP server.

### GitHub Spark

- Spark built full-stack web apps from natural-language descriptions on github.com.
- The github.com Spark experience stopped accepting new users and new apps on **August 4, 2026**, and existing users could export apps until **August 31, 2026**. Deployed apps keep working. GitHub now points builders to Copilot in VS Code, Copilot CLI and the GitHub Copilot app.
- The GH-300 outline still lists Spark, so expect concept-level questions ("natural language to a working web app").

### Pull Request Summaries

- On a pull request, Copilot can generate a summary of what changed and why, which you review and edit.
- Copilot pull request summaries are not included in Copilot Free.

### Copilot Code Review

- Reviews pull requests in any language, identifies issues and suggests fixes; it can hand suggestions to the cloud agent to open a fix PR.
- Available on GitHub.com, GitHub CLI, GitHub Mobile, VS Code, Visual Studio, Xcode and JetBrains IDEs.
- Automatic reviews can be configured by users, repository owners and organisation owners, and through rulesets.
- By default, **Copilot's reviews do not count toward required approvals**; it complements human review.
- Copilot does not review dependency management files (such as `package.json` or `Gemfile.lock`), log files or SVG files.
- Unless it is set to review every push, Copilot reviews a pull request once; use the re-request button in the Reviewers menu for another pass. Review effort is Lite or Balanced (the default).
- Each review consumes AI credits; agentic review features also use GitHub Actions minutes.

### Custom Instructions and Review Standards

| Type | Location / scope |
|------|------------------|
| Repository-wide | `.github/copilot-instructions.md` |
| Path-specific | `.github/instructions/NAME.instructions.md` |
| Agent instructions | `AGENTS.md`, `CLAUDE.md` or `GEMINI.md` |
| Personal | Your settings on GitHub.com (applies to you only) |
| Organisation | Copilot Business and Enterprise only |

- Copilot code review reads repository custom instructions, agent instructions and skills **from the pull request's head branch**, so review standards live in the repository and are versioned with the code.
- On GitHub.com, precedence is personal, then repository, then organisation. Most other clients (VS Code, Visual Studio, Copilot CLI) combine applicable files without a defined order.
- Path-specific files use an `applyTo` glob in their frontmatter (for example `applyTo: '**/*.py'`).
- Custom instructions apply to chat and agent requests; VS Code does not use them for inline suggestions as you type.

```markdown
<!-- .github/copilot-instructions.md -->
## Code Style
- Use snake_case for Python variables
- Prefer async/await over callback patterns

## Review standards
- Flag any SQL built with string concatenation
- Require tests for new public functions
```

---

## 4. Copilot Chat: Limits, Options, Feedback and Commands

### Key Concept

**Chat is steered with context, commands and reusable prompt files; its limits come from the model, plan and context window.**

This section covers how to drive Chat well. You add context with `#` references (files, symbols, the codebase, tools), shortcut common tasks with `/` commands, pick a model per session, and give feedback on responses. Prompt files (`.prompt.md`) package a prompt you reuse, so the whole team asks for the same thing the same way.

Chat has real limits: plans meter usage (Copilot Free has monthly limits; paid plans draw from AI credit allowances), different models cost different amounts, and long conversations eventually hit the context window. **Think of a prompt file as a saved recipe: the kitchen is the same, but every cook gets the same dish.**

### In Practice

**What breaks without this**: Five developers ask for "a code review" five different ways and get five inconsistent standards; a shared prompt file in `.github/prompts/` makes the request repeatable.

**Decision trigger**: Ask "will someone ask this again next week?" If yes, turn it into a prompt file (on-demand) or a custom instruction (always-on).

**When you'd choose differently**: Rules that must apply to every request (naming conventions, banned libraries) belong in custom instructions, not a prompt file, because prompt files run only when someone invokes them.

### Exam Trap ⚠️

<div class="note-trap">
Prompt files and custom instructions are easy to confuse. Custom instructions are applied automatically; prompt files are invoked on demand by typing `/` plus the prompt name or running **Chat: Run Prompt**. Note too that VS Code prompt files run only in Local harness sessions in the Chat view. One is the house rules on the wall; the other is a form you pick up when you need it.
</div>

### Context references and commands (VS Code)

| Kind | Examples |
|------|----------|
| `#` references | `#file`, `#selection`, `#codebase`, `#terminalSelection`, tools such as `#fetch` |
| Chat participants | `@github`, `@terminal`, `@vscode` |
| Slash commands | `/explain`, `/fix`, `/fixTestFailure`, `/tests`, `/new`, `/help`, `/clear` |

Type `/` in the chat input to see every available command; the list varies by IDE and installed skills.

### Prompt files

- Location: `.github/prompts/` in the workspace, or your VS Code user profile for personal prompts.
- Extension: `.prompt.md`. Optional frontmatter: `description`, `name`, `argument-hint`, `agent` (`ask`, `agent`, `plan` or a custom agent), `model`, `tools`.
- Run with `/name`, **Chat: Run Prompt**, or the play button in the editor title. Use `${input:variableName}` to ask the user for a value.
- Tool priority: tools in the prompt file, then the referenced custom agent's tools, then the selected agent's defaults.

### Options, limits and feedback

- **Models**: choose per session; some models are premium and consume more AI credits. Organisations control model access in the **Models** policy page.
- **Plan limits**: Copilot Free is limited to 2,000 completions per month and has a smaller AI credit allowance for chat (the plans page does not publish a figure); paid plans include a monthly allowance of GitHub AI Credits (Pro 1,500, Pro+ 7,000, Max 20,000, Business 1,900 per user, Enterprise 3,900 per user, per the [plans page](https://docs.github.com/en/copilot/get-started/plans)).
- **Copilot Chat on GitHub.com** (github.com/copilot) stores up to 100 of your most recent conversations, and messages are kept for 28 days before permanent deletion.
- **Context window**: long sessions get compacted or lose detail; start a new chat (`/clear`) when the topic changes.
- **Feedback**: rate responses to help improve Copilot. For individual plans, interaction data including thumbs up/down feedback may be used for model training unless you opt out (see Domain 6).

---

## 5. Organization-Wide Administration

### Key Concept

**Admins govern Copilot centrally: policies set feature availability, audit logs record changes, and the REST API manages seats.**

This section covers the administrator's controls. Organisation owners go to **Settings → Copilot** (under "Code, planning, and automation") and use **Policies** and **Models** to decide which features and models members can use, across IDEs, GitHub.com, Copilot CLI and agents. If an enterprise owner sets a policy, the organisation cannot override it.

The audit log records Copilot plan, policy and licence changes plus agent activity on GitHub, and the REST API automates seat assignment. **Think of policies as the building's access cards, the audit log as the door log, and the REST API as the front desk that issues cards in bulk.**

### In Practice

**What breaks without this**: Without an explicit code review policy, members with a Copilot licence cannot use Copilot code review on GitHub.com, and a team assumes the feature is broken when it was simply never enabled.

**Decision trigger**: Ask "is this a per-user preference or an organisational rule?" Organisational rules (public code matching, MCP, code review, CLI) go in policies; seat changes for many users go through the REST API or team-based assignment.

**When you'd choose differently**: In a single small organisation, assigning seats in the UI is simpler than scripting the API; automation pays off when seat changes track an HR or identity system.

### Exam Trap ⚠️

<div class="note-trap">
Removing a seat with the REST API does not cut access instantly. The seat moves to "pending cancellation" and the user loses access at the end of the current billing cycle; users assigned through a team keep access while they remain in that team. Also remember the audit log does not contain prompts: it records configuration and licence events, not what users typed. Think of it as a door log, not a CCTV recording.
</div>

### Copilot Policy Management

- Path: profile picture → **Organizations** → organisation → **Settings** → **Copilot** → **Policies** or **Models**.
- Policies cover privacy (for example **Suggestions matching public code**), feature availability (Copilot in GitHub.com, Copilot CLI, MCP servers in Copilot, cloud agent and partner agents such as Anthropic Claude and OpenAI Codex) and **Previews and feedback** ("Opt in to preview features", "Opt in to user feedback collection").
- Enterprise owners can set a policy for every organisation, or leave the decision to organisations.

### Copilot Code Review Policies

- Enable the **Copilot code review** policy so licensed members can use it on GitHub.com and GitHub Mobile.
- Optional: allow members **without** a Copilot licence to use code review on GitHub.com (off by default; Business and Enterprise only; requires AI credits paid usage to be enabled; billed to the organisation).
- Other controls: default review effort (Lite or Balanced), "Only allow Copilot code review to be triggered by authorized users", Copilot approvals (public preview), MCP tools during review, and runners for agentic capabilities.

### Audit Log Events

- Filter with `action:copilot` for Copilot plan events (for example `copilot.cfb_seat_assignment_created` when a licence is assigned).
- Filter with `actor:Copilot` for agent activity on GitHub.
- Retention: the last 180 days; stream to a SIEM for longer history.
- Not logged: client session data such as the prompts a user sends to Copilot locally.

### Seat Management via REST API

```bash
GET    /orgs/{org}/copilot/billing                 # subscription info and policies
GET    /orgs/{org}/copilot/billing/seats           # list seats with recent activity
POST   /orgs/{org}/copilot/billing/selected_teams  # add seats for team members
DELETE /orgs/{org}/copilot/billing/selected_teams  # pending cancellation for teams
POST   /orgs/{org}/copilot/billing/selected_users  # add seats for users
DELETE /orgs/{org}/copilot/billing/selected_users  # pending cancellation for users
GET    /orgs/{org}/members/{username}/copilot      # one member's seat details
```

Tokens need `manage_billing:copilot`, or `read:org` (read) / `admin:org` (write).

### Usage Metrics API

- The legacy Copilot metrics API closed on April 2, 2026. The current API is report-based: for example `GET /orgs/{org}/copilot/metrics/reports/organization-1-day?day=YYYY-MM-DD` and `.../organization-28-day/latest`, with enterprise, user-level and per-repository variants.
- Enterprise reports are available from October 10, 2025 and up to 1 year back.

---

## Key Exam Traps ⚠️

| Trap | Correct Answer |
|------|---------------|
| "Install Copilot CLI with `gh extension install github/gh-copilot`" | That extension is retired; install `@github/copilot` (npm), WinGet, Homebrew or the install script, and run `copilot` |
| "Agent Mode requires a specific keyboard shortcut" | Agent is selected from the agent picker in the Chat view |
| "copilot-instructions.md goes in the repo root" | It goes in `.github/copilot-instructions.md` |
| "Copilot Code Review replaces human review" | It **complements** human review; by default its reviews don't count toward required approvals |
| "Content exclusions apply in every Copilot mode" | Not in VS Code's Edit and Agent modes; inline and chat are covered |
| "Use a Copilot Extension / knowledge base to add context" | Both retired; use MCP servers and Copilot Spaces |
| "Removing a seat via API ends access immediately" | Seat goes to pending cancellation until the end of the billing cycle |

---

## Quick Reference

| Feature | Where to Find It |
|---------|-----------------|
| Inline suggestions | Any file in the IDE as you type; NES with `Tab` |
| Copilot Chat | IDE Chat view, inline chat, Quick Chat; GitHub.com; Mobile |
| Agent / Plan / Ask | Agent picker in the VS Code Chat view |
| Copilot CLI | Terminal: `copilot` (interactive) or `copilot -p` (programmatic) |
| Cloud agent | Agents panel, conversation, or issue/PR on GitHub.com |
| Subagents | Delegated from the main agent; custom agents in `.github/agents/` |
| Prompt files | `.github/prompts/*.prompt.md`, invoke with `/name` |
| PR Summary | Pull request description on GitHub.com |
| Code Review | PR page → request Copilot as reviewer, or automatic via rulesets |
| Spaces | github.com Copilot Spaces; IDE via GitHub MCP server |
| Organization settings | Organization → Settings → Copilot → Policies / Models |

---

## Deep Dive: Choosing the Right Feature for the Job

### Connective narrative

Domain 2 carries the **highest exam weight (25–30%)**, and the most common question style is: *"A developer wants to do X — which Copilot feature should they use?"* The features overlap, so understanding the **decision boundaries** is worth more than memorising each feature in isolation.

### Inline vs. Chat vs. Edits vs. Agent Mode — the mental model

Think of these four as a ladder of increasing **autonomy and scope**:

| Feature | Scope | Autonomy | Best for |
|---------|-------|----------|----------|
| **Inline suggestions** | Current cursor position | None — you drive every keystroke | Completing the line/block you're actively typing |
| **Copilot Chat** | Conversational, single file/selection | Low — you apply changes manually | Asking questions, explaining, generating a snippet to copy |
| **Copilot Edits** (Edit mode, deprecated in VS Code 1.110) | Multiple files you choose | Medium — proposes diffs across files, you approve each | A *known* change spanning several files ("add types to these components") |
| **Agent Mode** | Whole task, files it decides | High — plans, edits, runs commands, self-corrects | An *open-ended* multi-step goal ("build the login flow with tests") |
| **Cloud agent / Copilot CLI** | A whole task, run outside your editor | Highest — works on its own branch or in your terminal and reports back | Well-scoped issues you want delegated, or terminal-centric work |

**The exam distinction that trips people up:** *Edits* vs *Agent Mode*. Use **Edits** when *you* already know which files change and roughly what the change is. Use **Agent Mode** when the task requires the AI to **figure out the plan itself**, potentially touching files you didn't anticipate and running commands. Edits = you hold the map; Agent = Copilot draws the map. In current VS Code, Edit mode is deprecated and Agent handles multi-file edits, but the exam outline still names Copilot Edits, so know the distinction.

### Worked scenario

> **Task:** "Migrate our REST client from `axios` to the native `fetch` API across the project."
>
> - If you open the 3 files you *know* use axios and want controlled, file-by-file diffs → **Copilot Edits**.
> - If you're not sure how many files are affected and want Copilot to search, plan the migration, update each call site, and run the test suite to confirm → **Agent Mode** (start in **Plan** if you want to approve the plan first).
> - If the migration is a well-described issue you don't need to watch, and you want a pull request back → assign it to **Copilot cloud agent**; it works on its own branch and opens one PR for review.
> - If you want Copilot to audit every call site before deciding, without flooding your main chat → ask the agent to use a **subagent** for the search; only the summary returns to your conversation.
> - If you just want to understand *how* one tricky axios interceptor maps to fetch before deciding → **Chat** with `/explain`.

### Where MCP fits

MCP (Model Context Protocol) is not a "mode" — it's a **connector**. It extends *any* of the above by giving Copilot live access to external systems (a database schema, an issue tracker, live docs). The exam framing: MCP answers the question *"how does Copilot get context it can't see in your open files?"* When a question mentions **schema-aware SQL** or **pulling live requirements from Jira**, MCP is the mechanism. It is also what replaced GitHub App-based Copilot Extensions, which were sunset on November 10, 2025.

### `copilot-instructions.md` — why it matters more than it looks

This single file is the highest-leverage customisation in the exam. It is:
- Located at **`.github/copilot-instructions.md`** (a very common trap answer places it in repo root).
- **Automatically applied** to Copilot requests in that repository for *every* developer — so it standardises AI behaviour team-wide without each person configuring anything. Copilot code review reads it from the pull request's head branch, which is how teams encode custom review standards.
- The right answer whenever a question asks *"how do you make Copilot consistently follow our team's conventions?"*

### Memory aid: "I-CAN-SPOT"

When a question asks "which feature?", run **I-CAN-SPOT**:

- **I** — **Inline**: completing what you are typing (ghost text, NES)
- **C** — **Chat**: asking, explaining, small snippets; `/` commands and `#` context
- **A** — **Agent**: multi-step local task (Plan first if you want approval)
- **N** — **Network of tools**: MCP servers for external data and tools
- **S** — **Subagents and Sessions**: isolate side work; manage local, CLI and cloud sessions
- **P** — **Prompt files and instructions**: reusable prompts on demand; instructions always on
- **O** — **Off-editor**: Copilot CLI in the terminal, cloud agent on GitHub.com
- **T** — **Team governance**: policies, audit log, REST API for seats

### Exam Strategy for Domain 2

- Because this is the biggest domain, budget the most study time here. Expect several "which feature" scenario questions.
- Memorise the **invocation locations** (Agent = agent picker in the Chat view, not a shortcut; CLI = `copilot`, not the retired `gh copilot suggest/explain`; cloud agent = agents panel or an issue on GitHub.com).
- Watch for retired features presented as current: GitHub App-based Copilot Extensions, knowledge bases, the `gh-copilot` extension, the legacy metrics API, and the github.com Spark experience.
- Remember Copilot Code Review **complements** human review — any answer saying it *replaces* reviewers is wrong.
- Content exclusions affect **both** inline *and* Chat in supported IDEs (see Domain 6), but VS Code's Edit and Agent modes do not currently support them.
