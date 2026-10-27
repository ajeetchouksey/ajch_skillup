# Domain 6: Configure Privacy, Content Exclusions, and Safeguards

> **Exam Weight:** 15% | **GH-300 GitHub Copilot Certification**

---

## Overview

This domain covers how to protect sensitive code and data through content exclusions, how to manage the "suggestions matching public code" policy, and the privacy and IP considerations organizations must understand when deploying Copilot. The skills measured (as of August 7, 2026) are: configure content exclusions and editor settings; describe ownership and limitations of outputs; enable suggestions-matching-public-code filtering; and resolve issues with suggestions and content exclusions.

> 💡 **Human Angle**: *"Lock the filing cabinet, check what leaves the building, and know whose name is on the letterhead."* Exclusions, the public code filter and ownership terms are three different locks.

---

## 1. Content Exclusions

### Key Concept

**Content exclusions stop Copilot from reading chosen files, so their content never informs suggestions or chat answers.**

Content exclusion is a Copilot Business and Copilot Enterprise feature. Repository administrators set rules for their own repositories, organization owners set rules for users who get a Copilot seat from that organization, and enterprise owners set rules that apply to every Copilot user in the enterprise. In an excluded file, inline suggestions are unavailable, its content doesn't inform suggestions in other files or Chat responses, and Copilot code review on GitHub.com skips it.

Coverage varies by surface. Exclusions apply to inline suggestions in all major IDEs and to Chat in VS Code, Visual Studio and JetBrains, the GitHub website and Copilot CLI, but are **not supported in Edit and Agent modes of Copilot Chat in VS Code**. Rules from the levels add together; there is no individual or IDE-level setting that can loosen them. **Think of exclusions as a "do not read" stamp on a folder**: it only works where the reader honours the stamp, so you must know which readers do.

### In Practice

**What breaks without this**: Secrets in `.env` files, proprietary pricing logic or PII-laden seed files get pulled into prompts as context and can resurface in suggestions to other developers.

**Decision trigger**: Ask: would it be a problem if this file's content appeared in a prompt or a suggestion? If yes, exclude it at the highest level that covers every repository where it appears (enterprise or organization rather than repo-by-repo).

**When you'd choose differently**: Exclusions are not a secrets-management strategy. Secrets shouldn't be committed at all; use secret scanning, push protection and a vault, and treat exclusions as a backstop. Also, if the work happens in VS Code agent or edit mode, exclusions won't protect the file, so restrict access some other way.

### Exam Trap ⚠️

<div class="note-trap">
Two favourite distractors: "an individual developer can override the organization's exclusions in their IDE" (there is no such setting; the levels add together) and "content exclusion works on every Copilot plan" (Business and Enterprise only). Remember too that VS Code's Edit and Agent modes ignore exclusions.
</div>

### What Are Content Exclusions?

Content exclusions prevent GitHub Copilot from **reading and using specific files, directories, or repositories** as context. Typical candidates:

- Credentials, API keys, and secrets
- Proprietary algorithms and business logic
- Personally Identifiable Information (PII) in data files
- Configuration files with sensitive environment data

### Configuration Levels

| Level | Who configures | Applies to | Where |
|-------|---------------|-----------|-------|
| **Repository** | Repository administrators | Copilot users working in that repository | Repo → Settings → Code, planning, and automation → Copilot → Content exclusion |
| **Organization** | Organization owners | Users assigned a Copilot seat by that organization | Org → Settings → Copilot → Content exclusion |
| **Enterprise** | Enterprise owners | All Copilot users in the enterprise | Enterprise → AI controls → Copilot → Content exclusion |

A repository's Content exclusion page also shows, in grey read-only boxes, rules it inherits from its organization or from other organizations in the same enterprise. Rules **combine**; no level can switch off a rule set at another level.

### Configuring Repository-Level Exclusions

**Format:** a YAML list of quoted paths, one per line. Paths starting with `/` are relative to the repository root; paths without a leading `/` match anywhere in the repository.

```yaml
# Ignore one specific file
- "/src/some-dir/kernel.rs"
# Ignore secrets.json anywhere in this repository
- "secrets.json"
# Ignore any file whose name starts with "secret", anywhere
- "secret*"
# Ignore any file whose name ends in ".cfg", anywhere
- "*.cfg"
# Ignore everything in or below the top-level /scripts directory
- "/scripts/**"
```

### Configuring Organization-Level Exclusions

At organization (and enterprise) level, each rule is keyed by a **repository reference** and lists paths under it. Use `"*"` to match all repositories and non-Git files.

```yaml
# .env files in all file system roots, Git and non-Git
"*":
  - "**/.env"

# A repository in this organization, by name
octo-repo:
  - "/src/some-dir/kernel.rs"

# Any Git host, by URL (http[s]://, git://, ssh:// or user@host:path forms)
https://github.com/primer/react.git:
  - "secrets.json"
  - "/src/**/temp.rb"

git@gitlab.com:gitlab-org/gitlab-runner.git:
  - "**/security/**"
```

The `user@` and `:port` parts of a repository reference are ignored when matching, and for Azure DevOps either the `dev.azure.com` or `visualstudio.com` host form works.

---

## 2. Glob Pattern Reference

### Key Concept

**Exclusion paths use fnmatch patterns, matched case-insensitively; a leading slash anchors the path to the repository root.**

The pattern rules are short. `*` matches any characters within a name, `**` matches across directory levels, `?` matches one character, `[dk]` matches a character set and `{server,session}` matches alternatives. A path that starts with `/` is anchored to the repository root; a bare name such as `"secrets.json"` or `"*.cfg"` matches that file name anywhere in the repository.

Most mistakes come from anchoring, not wildcards. `"/scripts/*"` covers only the direct contents of `/scripts`, while `"/scripts/**"` covers everything below it. **Read a pattern like a postal address**: a leading slash is a full street address, a bare name is "anyone called Smith in town".

### In Practice

**What breaks without this**: An admin writes `"/config/*"` expecting to exclude nested `config/prod/db.yml`, and the most sensitive file stays readable.

**Decision trigger**: Ask: should this rule match one exact location, or a file name wherever it appears? Anchor with `/` for the first; use a bare name or `**/` for the second. Then test it with a real file.

**When you'd choose differently**: If a whole repository is sensitive, don't enumerate file patterns one by one. Add an organization-level rule keyed to that repository's reference that covers all of its paths, or keep Copilot out of that work entirely.

### Exam Trap ⚠️

<div class="note-trap">
Look out for options that treat patterns as case-sensitive (they are case-insensitive) or that confuse `/dir/*` (direct children only) with `/dir/**` (everything below). And remember the leading slash: `"/secrets.json"` is root-only, `"secrets.json"` is anywhere.
</div>

### Glob Syntax for Content Exclusions

| Pattern | What It Matches | Example Match |
|---------|----------------|--------------|
| `"secrets.json"` | A file with that name anywhere in the repo | `secrets.json`, `app/secrets.json` |
| `"*.cfg"` | Any file name ending in `.cfg`, anywhere | `app.cfg`, `conf/db.cfg` |
| `"secret*"` | Any file name starting with `secret`, anywhere | `secret.txt`, `lib/secrets.yml` |
| `"/scripts/**"` | Everything in or below top-level `/scripts` | `/scripts/a.sh`, `/scripts/ci/b.sh` |
| `"/scripts/*"` | Direct contents of `/scripts` only | `/scripts/a.sh` (not `/scripts/ci/b.sh`) |
| `"**/.env"` | `.env` files at any depth | `/.env`, `services/api/.env` |
| `"*.m[dk]"` | Names ending in `.md` or `.mk` | `README.md`, `build.mk` |
| `"{server,session}*"` | Names starting with `server` or `session` | `server.go`, `session_test.go` |

### Common Pattern Mistakes

```yaml
# ❌ Anchored to the root, so nested copies are NOT excluded
- "/config/production.yml"

# ✅ Matches the file name anywhere in the repository
- "production.yml"

# ❌ Only the direct children of /secrets
- "/secrets/*"

# ✅ Everything in or below /secrets
- "/secrets/**"

# ❌ Unquoted or prefixed entries are not the documented syntax
exclude: secrets/

# ✅ One quoted path per list item
- "/secrets/**"
```

The documentation describes no negation (`!pattern`) syntax: list what to exclude rather than what to include.

---

## 3. Public Code Filter (Duplication Detection)

### Key Concept

**The "suggestions matching public code" policy decides whether Copilot blocks matching suggestions or shows them with a code reference.**

For inline suggestions, Copilot compares a potential suggestion plus about 150 characters of surrounding code against an index of public repositories on GitHub.com. Code in private repositories and code hosted outside GitHub isn't searched. When the policy is **Block**, matching suggestions aren't shown; when it's **Allow**, matches are shown with code-referencing details such as the matching repository files and any detected licences, and Copilot Chat responses link to information about the match.

GitHub reports matches in under one percent of suggestions, so this is a narrow control for a narrow risk. It acts on Copilot's output, not on what Copilot reads. **The filter is a customs check at the exit door**: it inspects what leaves, while content exclusions guard what comes in.

### In Practice

**What breaks without this**: A suggestion reproduces a copyleft-licensed function verbatim, ships in a proprietary product, and nobody knows its origin until a licence audit.

**Decision trigger**: Ask: do we need to avoid public-code matches entirely, or do we want to see them with attribution and decide? Block for strict avoidance; Allow with code referencing when your team is set up to review licences.

**When you'd choose differently**: Teams that work heavily with open source and track licences carefully often prefer Allow, because code references surface the origin and licence instead of silently dropping a useful suggestion.

### Exam Trap ⚠️

<div class="note-trap">
Two traps. First, the filter does not stop Copilot reading your files; that is content exclusion. Second, older material says Block is a prerequisite for IP indemnification. Microsoft's Customer Copyright Commitment page states that as of April 3, 2026 the duplicate detection filter is no longer required for CCC coverage of GitHub offerings; the filter remains available as an optional control.
</div>

### Enabling the Public Code Filter

| Scope | Where | Notes |
|-------|-------|------|
| **Enterprise** | Enterprise → AI controls → Copilot → Privacy → "Suggestions matching public code" | Set it for all organizations or delegate to organization owners; Allowed by default for Copilot Business |
| **Organization** | Org → Settings → Copilot → Policies → "Suggestions matching public code" | Applies to members who get Copilot through the organization |
| **Individual** (Free, Pro, Pro+, Max) | Personal Settings → Copilot → "Suggestions matching public code" | **Allow** or **Block**; not configurable if your seat comes from an Enterprise Cloud organization |

| Setting | Behaviour |
|---------|---------|
| **Allow** | Matching suggestions can be shown, with code-referencing information |
| **Block** | Matching suggestions are suppressed; Copilot may offer a different suggestion or none |

### Limitations

- Matching is based on an index of public GitHub.com code; it doesn't search private repositories or code hosted elsewhere
- It is a risk-reduction tool, not a legal guarantee that output is free of third-party IP
- It controls output only; it doesn't stop Copilot reading your files

---

## 4. Output Ownership and Intellectual Property

### Key Concept

**GitHub claims no ownership of Copilot inputs or outputs; responsibility for using the output stays with you.**

GitHub's Generative AI Services Terms (March 2026, which replaced the earlier Copilot Product Specific Terms for Business and Enterprise customers buying directly from GitHub) state that "GitHub does not own Inputs or Outputs." GitHub's responsible-use documentation for code completion adds that users assume the risks of generated code, including security vulnerabilities, bugs and IP infringement.

Defence against third-party IP claims is contractual, not automatic. The terms say that if your agreement provides for defence of third-party claims, that provision applies to Copilot outputs, subject to Microsoft's Customer Copyright Commitment required mitigations. **Ownership is the deed to the house; indemnity is the insurance policy**: you hold the first by default, and the second depends on what your contract says.

### In Practice

**What breaks without this**: Legal teams either block Copilot because they assume GitHub owns the output, or approve it on the false belief that any IP claim is automatically GitHub's problem.

**Decision trigger**: Ask: which agreement covers our Copilot purchase (GitHub customer agreement, Microsoft agreement, or personal Terms of Service) and what does its defence-of-claims clause say? Answer that before promising developers protection.

**When you'd choose differently**: In regulated industries or jurisdictions where copyright in AI-assisted work is unsettled, add internal controls (licence scanning, provenance review, the public code filter set to Block) regardless of what the contract offers.

### Exam Trap ⚠️

<div class="note-trap">
"GitHub owns code generated by Copilot" is false: GitHub does not own inputs or outputs. Equally false is "indemnification is automatic for every Copilot user". Personal plans are governed by the GitHub Terms of Service, and business defence of claims depends on the customer's agreement.
</div>

### Limitations and Caveats

| Topic | Reality |
|-------|---------|
| AI IP law | Still evolving globally; the legal landscape isn't settled |
| Copyright of AI output | Varies by jurisdiction; consult legal counsel for regulated industries |
| Defence of IP claims | Comes from your agreement (and the Customer Copyright Commitment), not from a Copilot setting |
| Public code filter | Optional risk reduction; as of April 3, 2026 not a required mitigation for CCC coverage of GitHub offerings |

---

## 5. Privacy Settings

### Key Concept

**Business and Enterprise data isn't used for model training; personal plans train on interaction data unless the user opts out.**

GitHub's Generative AI Services Terms state that GitHub "will not use Inputs or Outputs to train generative AI models" for covered business customers unless instructed. For Copilot Free, Pro, Pro+ and Max, GitHub announced that from April 24, 2026 interaction data (inputs, outputs, code snippets and associated context) is used to train and improve its models unless the user turns off **"Allow GitHub to use my data for AI model training"** in the Privacy section of their Copilot settings.

Other editor-facing settings sit next to it. Users on personal plans choose Allow or Block for suggestions matching public code, and web search through Bing is disabled by default. For seats assigned by an organization or enterprise, administrators set these policies centrally. **Think of the plan as the lease**: on a business lease the landlord's rules are fixed in the contract; on a personal lease you have to tick the boxes yourself.

### In Practice

**What breaks without this**: A contractor uses a personal Pro plan on client code with the training setting left at its default, breaching the client's data-handling terms.

**Decision trigger**: Ask: whose plan is this seat on? If personal, check the Privacy settings before touching sensitive code. If business, check the organization's policies and content exclusions instead.

**When you'd choose differently**: Where any data leaving the network is unacceptable, setting toggles isn't enough. Use Business or Enterprise with content exclusions, network allowlists, and policies that disable features (for example web search) you don't need.

### Exam Trap ⚠️

<div class="note-trap">
Don't carry over the old "Copilot Individual" framing. The personal plans are now Free, Pro, Pro+ and Max (plus Student), and their training setting is opt-out, meaning on unless the user turns it off. Business and Enterprise are not affected by that change.
</div>

### Individual Settings (personal plans)

| Setting | What It Controls | Notes |
|---------|----------------|-------|
| **Allow GitHub to use my data for AI model training** | Whether interaction data trains GitHub's models | Free, Pro, Pro+, Max; opt-out (from April 24, 2026). Earlier opt-outs were retained |
| **Suggestions matching public code** | Allow or Block matches | Not configurable for seats from an Enterprise Cloud organization |
| **Copilot access to Bing** | Web search in Copilot Chat | Disabled by default |

### Organization Control

- For seats assigned through an organization or enterprise, Copilot features and policies are set by owners in the organization or enterprise settings
- An enterprise can set a policy for all organizations or let each organization choose
- Changes to organization Copilot settings are recorded in the audit log (`copilot.cfb_org_settings_changed`)

### Business / Enterprise vs. Personal Plans

| Plan | Inputs/outputs used for model training | Content exclusion | Central policy management |
|------|--------------------------------------|-------------------|---------------------------|
| **Free / Pro / Pro+ / Max** | Yes, unless the user opts out | Not included | Not included |
| **Business** | No | Included | Included |
| **Enterprise** | No | Included | Included |

---

## 6. Troubleshooting Content Exclusions

### Key Concept

**Most "exclusion isn't working" reports are timing, surface or pattern problems, and each has a specific check.**

After you add or change an exclusion, it can take up to 30 minutes to reach IDEs that already loaded the settings. To apply it sooner, reload: in VS Code run **Developer: Reload Window**; in JetBrains IDEs and Visual Studio close and reopen the application; Vim/Neovim fetch exclusions each time a file is opened. In the IDE, the Copilot status bar icon shows a diagonal line on an excluded file, and hovering over it tells you which setting applies.

If timing isn't the cause, check the surface and the pattern. VS Code's Edit and Agent modes don't honour exclusions, symlinks and repositories on remote filesystems aren't covered, and the IDE can still pass semantic information from an excluded file (type information, hover definitions). **Debug exclusions like a leaking pipe**: check the valve was turned (reload), the right pipe was capped (surface), and the cap fits (pattern).

### In Practice

**What breaks without this**: An admin sees a secret file still feeding answers, assumes the feature is broken and escalates, when the developer was simply in agent mode or hadn't reloaded.

**Decision trigger**: Ask, in order: has it been 30 minutes or has the IDE reloaded? Is the developer in a supported mode and client? Does the status bar icon show the exclusion? Does the pattern actually match the path?

**When you'd choose differently**: If suggestions are missing everywhere (not just in excluded files), it isn't an exclusion problem. Check the extension is up to date, sign out and back in, look at the Copilot logs, and check githubstatus.com for incidents.

### Exam Trap ⚠️

<div class="note-trap">
The trap answer is "content exclusions take effect instantly". Changes can take up to 30 minutes in IDEs that already loaded settings, and reloading is the fix. A second trap: assuming exclusions apply in VS Code agent mode. They don't.
</div>

### Common Issues and Solutions

| Issue | Likely Cause | Solution |
|-------|-------------|---------|
| Excluded file still informs suggestions | Settings not refreshed yet (up to 30 minutes) | Reload: VS Code **Developer: Reload Window**; JetBrains/Visual Studio restart |
| Excluded file used in a VS Code chat | Developer is in Edit or Agent mode | Exclusions aren't supported there; use Ask mode or other controls |
| Pattern not matching | Anchoring or wildcard mistake | Check leading `/`, `*` vs `**`; test with a real path |
| Repo-level rule can't be saved | User isn't a repository administrator | Ask a repo admin, or set it at org level |
| No suggestions in any file of a repo | The whole repository is excluded at org/enterprise level | Review the inherited rules shown on the repo's Content exclusion page |
| Information still leaks via types/hover | IDE passes semantic info indirectly | Known limitation; exclude or isolate the source more broadly |
| Copilot stops working entirely | Outdated extension, auth problem or service incident | Update the extension, sign out and in, check logs and githubstatus.com |

### Validation Workflow

```
1. Configure the exclusion rule (repo, org or enterprise)
   ↓
2. Wait up to 30 minutes OR reload the IDE
   ↓
3. Open a normal file and confirm a suggestion appears
   ↓
4. Make the same edit in an excluded file — no suggestion should be offered
   ↓
5. Hover the Copilot status bar icon — it should show the exclusion and its source
   ↓
6. In Copilot Chat (Ask mode), attach the excluded file and ask "explain this file"
   ↓
7. Confirm the file is not used and is not listed as a reference in the response
```

---

## 7. Audit Log Events

### Key Concept

**The audit log records who changed Copilot settings, seats and policies, never what developers typed into Copilot.**

Filter the organization or enterprise audit log with `action:copilot` to see Copilot plan events such as seat assignments, policy changes and content exclusion edits, and with `actor:Copilot` to see agent activity on GitHub.com. Events are kept for 180 days, so stream them to a SIEM for longer retention.

The audit log doesn't include client session data such as the prompts a user sends to Copilot locally. Usage questions ("who is actually using Copilot?") belong to the Copilot usage metrics dashboards and API, not the audit log. **The audit log is the building's sign-in book, not a recording of the meetings.**

### In Practice

**What breaks without this**: After an exclusion rule disappears, nobody can say who removed it or when, and a compliance review fails for lack of evidence.

**Decision trigger**: Ask: is my question "who changed what configuration, when?" Use the audit log. Is it "how much is Copilot used, and by whom?" Use usage metrics.

**When you'd choose differently**: To capture prompts or agent actions for your own monitoring, you need a custom solution (for example hooks that send Copilot CLI events to your own logging service); the audit log won't provide them.

### Exam Trap ⚠️

<div class="note-trap">
Distractors claim the audit log stores prompts or suggestions for review. It doesn't. It records configuration and licensing events for 180 days. Also beware invented event names; the real ones look like `copilot.content_exclusion_changed` and `copilot.cfb_seat_added`.
</div>

### Copilot-Related Audit Log Events (selection)

Organization admins can monitor governance changes via **Organization → Settings → Audit log**, filtered with `action:copilot`.

| Event | Description |
|-------|-------------|
| `copilot.cfb_org_settings_changed` | An organization-level Copilot feature setting changed |
| `copilot.cfb_seat_added` | A Business/Enterprise seat was added for a user |
| `copilot.cfb_seat_assignment_created` | A seat assignment was created for a user or team |
| `copilot.cfb_seat_assignment_unassigned` | A seat was unassigned; access ends at the end of the billing cycle |
| `copilot.cfb_seat_cancelled` | A seat was cancelled, ending access |
| `copilot.content_exclusion_changed` | The paths excluded from Copilot were updated |
| `copilot.code_review_organization_settings_updated` | Copilot code review settings were updated for an organization |
| `copilot.custom_instructions_updated` | Organization custom instructions were updated |

---

## Deep Dive: Exclusions, Filters, and Ownership Untangled

Domain 6 blends three easily-confused ideas: **content exclusions** (what Copilot can *read*), the **public code filter** (what Copilot can *suggest*), and **output ownership and defence of claims** (who is *responsible*). Keeping them in separate mental boxes is most of the battle.

### Exclusions vs. the public code filter — opposite ends of the pipe

| | Content Exclusions | Public Code Filter |
|---|---|---|
| **Controls** | What goes *into* the prompt | What comes *out* of the model |
| **Stage** | Input / context collection | Output / post-processing |
| **Protects against** | Leaking *your* secrets and IP into prompts | Emitting *others'* public or licensed code |
| **Configured as** | fnmatch paths at repo, org or enterprise level | A policy: Allow or Block |
| **Who sets it** | Repo admins, org owners, enterprise owners (Business/Enterprise only) | The user on personal plans; org or enterprise owners for assigned seats |

A one-liner that resolves most questions: **exclusions guard your inputs; the public code filter guards your outputs.** If a scenario is about hiding `.env` secrets, think exclusions. If it's about not reproducing open-source code, think the filter.

### Levels add up; they don't override

Exclusion rules from the repository, organization and enterprise levels **combine**. A repository shows inherited organization and enterprise rules as read-only grey boxes, so a repo admin can add rules but can't delete inherited ones. There is no individual or IDE-level exclusion setting, which means a developer has no way to un-exclude a file their organization excluded. That is why enterprise- or organization-level rules are the scalable control: one policy covers every repository, and no single person can weaken it.

### Worked scenario: the file that wouldn't stay excluded

> **Scenario.** Contoso's org owner adds `"*": - "**/.env"` at 10:00. At 10:10 a developer in VS Code asks Chat in **Agent** mode to "fix the database connection" and the response quotes values from `services/api/.env`. The owner thinks the rule failed.
>
> **Reasoning.** Three independent causes are possible. (1) *Timing*: rules can take up to 30 minutes to reach an IDE that already loaded settings, and 10 minutes isn't enough. (2) *Surface*: content exclusion isn't supported in Edit and Agent modes of Copilot Chat in VS Code, so even a fully propagated rule wouldn't stop this. (3) *Pattern*: `**/.env` does match `services/api/.env`, so the pattern isn't the problem.
>
> **Outcome.** The developer runs **Developer: Reload Window**, sees the status bar icon with a diagonal line on `.env`, and switches to Ask mode, where attaching the file and asking "explain this file" shows it isn't used. The owner adds a policy note that agent-mode work must not happen in repos with live secrets, and opens a ticket to move those values to a secrets manager, since exclusion was only ever a backstop.

### Ownership and defence of claims — the contractual safety net

You (or your organization) keep your code, and GitHub does not own inputs or outputs. But defence against a third-party IP claim is **not automatic**. Under the GitHub Generative AI Services Terms, it applies if your agreement provides for defence of third-party claims, subject to Microsoft's Customer Copyright Commitment required mitigations. As of April 3, 2026, those mitigations list nothing extra for GitHub offerings, and the duplicate detection filter is optional. On the exam, treat answers that make the filter a *hard prerequisite* for protection with suspicion unless the question is explicitly about the earlier policy, and reject any answer that calls indemnity automatic or universal.

### Memory aid: R.E.A.C.H. when exclusions misbehave

- **R — Reload or wait**: up to 30 minutes, or **Developer: Reload Window** / restart the IDE.
- **E — Edit/Agent mode?** VS Code's Edit and Agent modes don't honour exclusions.
- **A — Anchor and syntax**: leading `/` anchors to the root; `*` vs `**`; case-insensitive fnmatch.
- **C — Coverage gaps**: symlinks, remote filesystems and IDE semantic info aren't covered.
- **H — Hover the status icon**: a diagonal line confirms the exclusion and shows which setting applies.

### Exam Strategy for Domain 6

- Sort every question into one box first: **inputs (exclusions)**, **outputs (filter)**, or **responsibility (ownership and defence of claims)**.
- Exclusion facts that decide answers: Business/Enterprise only; repo, org and enterprise levels that combine; up to 30 minutes or reload; not in VS Code Edit/Agent modes.
- Business and Enterprise inputs and outputs are not used for training; personal plans are opt-out since April 24, 2026.
- The sentence to remember: **exclusions control what Copilot reads, the filter controls what it shows, and your contract controls who is responsible.**

---

## Key Exam Traps ⚠️

| Trap | Correct Answer |
|------|---------------|
| "Content exclusions apply instantly" | **FALSE** — up to 30 minutes in IDEs that already loaded settings; reload to apply sooner |
| "Exclusions only affect inline suggestions, not Chat" | **FALSE** — they cover inline suggestions and Chat on supported clients, and Copilot code review on GitHub.com |
| "Exclusions also apply in VS Code Agent and Edit modes" | **FALSE** — not supported in those modes |
| "The public code filter guarantees no IP issues" | **FALSE** — it reduces one risk; it isn't a legal guarantee |
| "Blocking public code matches is required for indemnity" | **Outdated** — no longer a required CCC mitigation for GitHub offerings as of April 3, 2026 |
| "GitHub owns code Copilot generates" | **FALSE** — GitHub does not own inputs or outputs |
| "Developers can override org exclusions in their IDE" | **FALSE** — no individual/IDE level exists; levels combine |
| "Content exclusion is available on Copilot Pro" | **FALSE** — Business and Enterprise only |
| "Business/Enterprise data is used to train models" | **FALSE** — inputs and outputs aren't used for training |
| "The audit log stores developers' prompts" | **FALSE** — no client session data; 180-day retention of configuration events |

---

## Quick Reference

| Topic | Key Fact |
|-------|---------|
| Exclusion plans | Copilot Business and Enterprise only |
| Exclusion levels | Repository (repo admins), organization (org owners), enterprise (enterprise owners); rules combine |
| Pattern syntax | fnmatch, case-insensitive; `/` anchors to repo root; `"*"` key = all repos at org/enterprise level |
| Propagation | Up to 30 minutes; VS Code **Developer: Reload Window**, JetBrains/VS restart |
| Unsupported surfaces | Edit and Agent modes of Copilot Chat in VS Code; symlinks; remote filesystems |
| Public code filter | ~150 characters of context checked against public GitHub code; Block or Allow (with code references) |
| Who owns output | GitHub does not own inputs or outputs |
| Defence of IP claims | Per your agreement and Microsoft's Customer Copyright Commitment; filter optional since April 3, 2026 |
| Training on data | Business/Enterprise: no. Free/Pro/Pro+/Max: yes unless opted out (from April 24, 2026) |
| Audit log | `action:copilot`, `actor:Copilot`; 180 days; no prompts |
| Validation | Status bar icon with diagonal line; "explain this file" in Chat shows no reference |
