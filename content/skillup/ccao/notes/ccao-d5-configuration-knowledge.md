# D5: Configuration and Knowledge Management

> **Exam weight**: 12% · **Questions**: ~12 in the bank

## Overview

This domain covers setting Claude up so good results repeat: Projects with instructions and knowledge, uploaded files versus live connectors such as Google Drive and Gmail, writing standing instructions at the right level, and keeping all of it current as things change.

> 💡 **Human Angle**: A well-set-up Project means nobody has to re-explain the brand voice, re-upload the price list or remember the house style ever again, until someone forgets to update it.

---

## 5.1 Configure Claude Projects with instructions and knowledge sources

### Key Concept

**A Project bundles standing instructions and knowledge files, so every chat inside it starts with the same context.**

You create a Project, write its instructions (how Claude should behave in it) and add knowledge (files Claude uses across all its chats). Chats inside a Project don't share context with each other unless the information is in the Project's knowledge. Each Project also keeps its own memory, separate from other Projects. On paid plans, when knowledge approaches the context limit, retrieval (RAG) switches on automatically and expands the Project's capacity, up to about ten times. On Team and Enterprise plans, a Project can be shared with "Can view" or "Can edit" access.

**Think of a team binder**: the rules on the first page and the reference material behind it, handed to everyone who joins.

![A Project stacks three layers: instructions that set behaviour for every chat, knowledge files that every chat can use, and the chats themselves, which share the knowledge but not each other's conversation.](/content/skillup/ccao/images/ccao-5-1-project.svg)

### Real use

A customer-support lead creates a "Returns policy" Project. Its instructions say: answer as a support specialist, quote the policy section, and say "escalate" when the policy doesn't cover a case. Its knowledge holds the returns policy, the warranty terms and twenty example replies. Every agent's chat in the Project now starts from the same rules and documents.

### How it works

- **Instructions:** role, tone, format and rules for every chat in the Project.
- **Knowledge:** files used across all chats; the source of truth for the topic.
- **Separate chats:** don't see each other unless the content is in knowledge.
- **Project memory:** separate from other Projects.
- **RAG on paid plans:** switches on near the context limit and expands capacity.
- **Sharing (Team and Enterprise):** "Can view" or "Can edit".

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Project | Same rules and files, many chats or people | Must be maintained |
| Plain chat with uploads | One-off use of a file | Repeat uploads every time |
| Shared Project | A team needs the same setup | Edit access must be managed |

### How to do it

1. Create the Project and write its instructions.
2. Add the authoritative knowledge files, one current version each.
3. Share it with view or edit access as needed, and test with a few real questions.

### Exam Trap ⚠️

<div class="note-trap">"Information discussed in one chat is automatically available in other chats in the same Project" is false. Shared context comes from the Project's knowledge and instructions.</div>

### Go deeper

- [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- [Retrieval augmented generation (RAG) for projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)

---

## 5.2 Manage uploaded knowledge and connectors (e.g., Google Drive, Gmail)

### Key Concept

**Upload stable reference files to the Project; connect live sources such as Drive, Gmail and Calendar when the information keeps changing.**

Uploaded files are a snapshot: perfect for policies, guidelines and templates that change rarely. Connectors let Claude reach live information in tools like Gmail, Google Calendar and Google Drive, and only the data of the account you connected. By default, Claude asks for your approval before actions like sending email or sharing or deleting Drive files. Data retrieved through a connector is stored with the chat it came from, so deleting the chat removes it.

**Think of a printed handbook versus a live dashboard**: one is fixed and dependable, the other is always current.

![Choosing between uploads and connectors: a stable policy document is uploaded to Project knowledge, while live email, calendar and Drive files are reached through connectors, which only see the connected account and ask before sending or deleting.](/content/skillup/ccao/images/ccao-5-2-uploads-connectors.svg)

### Real use

An executive assistant keeps the travel policy and expense rules as Project knowledge, and connects Google Calendar and Gmail so Claude can draft the week's briefing from the actual schedule and recent threads. Claude drafts replies, but asks before sending any of them.

### How it works

- **Uploads:** fixed snapshots; replace them when the source changes.
- **Connectors:** live access to Gmail, Calendar, Drive and other tools.
- **Scope:** a connector only sees the connected account's data.
- **Approvals:** sending email and sharing or deleting files ask first by default.
- **Retention:** connector data is stored with its chat.
- **Admins** on Team and Enterprise can set connector policies.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Upload to knowledge | Stable reference material | Goes stale if not replaced |
| Connector | Information changes often | Needs access and approvals |
| Both | Fixed rules plus live data | Two things to manage |

### How to do it

1. Put stable reference files in Project knowledge.
2. Connect the live tools the task needs, with the right account.
3. Review actions Claude proposes, like sending email, before approving.

### Exam Trap ⚠️

<div class="note-trap">Uploading this week's inbox export to Project knowledge every Monday is a sign you need a connector. And a connector doesn't give Claude access to colleagues' mailboxes, only to the account you connected.</div>

### Go deeper

- [Use Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)

---

## 5.3 Create effective system-level instructions

### Key Concept

**Standing instructions set the rules once: role, audience, tone, format and what to do when unsure; write them at the level where they apply.**

Claude has layers of standing instructions. **Account instructions** (Settings → "Your Claude" → Instructions) apply to all your chats: your role, preferred format, terms you use. **Project instructions** apply only to chats in that Project. **Skills** add specific behaviours or expertise on demand. Good instructions are specific and positive ("Use British spelling; lead with the answer; use a table for comparisons"), include what to do when information is missing, and stay short enough to follow.

**Think of a job description, a project brief and a checklist**: general, specific and on-demand.

![Three instruction layers by scope: account instructions apply to every chat, project instructions apply to chats in one Project, and skills add specific behaviour when needed.](/content/skillup/ccao/images/ccao-5-3-instruction-layers.svg)

### Real use

A consultant's account instructions say she works in healthcare operations and prefers concise answers with the recommendation first. Her "Hospital A" Project instructions add the client's terminology, the report template and "if data is missing, list it as an open question rather than estimating".

### How it works

- **Account instructions:** all chats; your general preferences.
- **Project instructions:** one Project; task rules, role, template.
- **Skills:** on demand; specialised behaviour or formats.
- **Write well:** specific, positive, with an example; say what to do when unsure.
- **Avoid conflicts:** don't set contradicting rules at different levels.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Account instructions | Preferences for everything you do | Apply even where they don't fit |
| Project instructions | Rules for one body of work | Only in that Project |
| A skill | Specialised behaviour you call on | Must be set up |

### How to do it

1. Decide the scope: all chats, one Project, or on demand.
2. Write specific, positive rules with a short example, plus what to do when unsure.
3. Test with real prompts and tighten anything Claude misreads.

### Exam Trap ⚠️

<div class="note-trap">Putting client-specific rules in account instructions makes them apply to every chat, including unrelated ones. Put rules at the level they belong. And vague instructions ("be good", "be professional") change very little.</div>

### Go deeper

- [Understanding Claude's personalization features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)

---

## 5.4 Inform, maintain, and update Claude configurations, knowledge sources, and instructions

### Key Concept

**Treat a Project like a living document: give it an owner, review it on a schedule, and replace stale files instead of piling up versions.**

Configurations go stale. A price list changes, a policy is revised, a new product launches, and the Project keeps answering from the old version. Keeping two versions of the same document makes it worse, because Claude may use either. Good practice: an owner for each shared Project, a review date, one current version of each file, notes in the instructions about what changed, and telling users when important changes happen.

**Think of a shared spreadsheet with an owner**: someone checks it's right before the month-end close.

![The Project maintenance cycle: an owner reviews it on schedule, replaces outdated files with the single current version, updates instructions, tests with real questions, and tells users what changed.](/content/skillup/ccao/images/ccao-5-4-maintain.svg)

### Real use

Sales reps notice the Project quoting last year's discount rules. The owner finds both the old and new pricing files in the knowledge, removes the old one, adds "Pricing updated 1 October" to the instructions, tests three common questions, and posts a note in the team channel.

### How it works

- **Owner:** one person accountable for each shared Project.
- **Review schedule:** monthly or when source documents change.
- **One version:** remove superseded files; don't keep "v1" and "v2".
- **Test:** a few standard questions after every change.
- **Announce:** tell users what changed and when.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Scheduled review | Shared Projects used by a team | Takes recurring time |
| Update on source change | Policies or prices change | Someone must notice the change |
| Hand over ownership | The owner changes role or leaves | New owner needs a handover |

### How to do it

1. Assign an owner and a review date.
2. Replace outdated files with the current version and update instructions.
3. Test with standard questions and tell users what changed.

### Exam Trap ⚠️

<div class="note-trap">"Add the new policy alongside the old one so nothing is lost" leaves Claude two conflicting sources. Replace the old version, and note the change.</div>

### Go deeper

- [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)

---

## Deep Dive: Making Configuration and Knowledge Click

### 1. The connective narrative

This domain is about making good results repeatable. A Project (5.1) packages the rules and the reference material. Choosing between uploads and connectors (5.2) decides whether that material is a snapshot or live. Instructions at the right level (5.3) set behaviour without clashing. Maintenance (5.4) keeps the whole setup true over time, which matters because a stale Project fails quietly: it still answers confidently, from old information.

### 2. Worked scenario

> **Scenario.** An HR team builds a "People policies" Project (5.1). The handbook and benefits guide are uploaded as knowledge; the HR calendar is connected so Claude can answer "when is open enrolment?" from the live schedule (5.2). Project instructions say to quote the policy section and to escalate anything about individual cases to HR (5.3). When the parental-leave policy changes, the owner swaps the file, updates the instructions and tells managers (5.4).

### 3. Memory aid

**PICK**: **P**roject for shared context · **I**nstructions at the right level · **C**onnectors for live data · **K**eep it current.

### 4. Exam strategy for this domain

Wrong answers treat chats as shared memory, pile up versions, put rules at the wrong level or upload live data repeatedly. Right answers use Project knowledge for shared context, connectors for live sources, scoped instructions and an owner who keeps it current.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Same files and rules for many chats | Project with instructions and knowledge |
| Chat A's info missing in chat B | Add it to Project knowledge |
| Knowledge base is very large (paid plan) | RAG switches on automatically |
| Information changes daily | Connector (Gmail, Calendar, Drive) |
| Claude about to send an email | Approval prompt by default |
| Rule applies to all your chats | Account instructions |
| Rule applies to one client's work | Project instructions |
| Old and new policy both in knowledge | Remove the old one |
| Project answers from old data | Owner reviews and replaces files |
