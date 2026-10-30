# D3: Product and Model Selection

> **Exam weight**: 12% · **Questions**: ~12 in the bank

## Overview

This domain covers choosing the right part of Claude for the job: a plain chat, a Project, Research or an artifact; Haiku, Sonnet or Opus; the effort and thinking settings; and how to work within the limits of context and memory by knowing when to restart, summarise or save something for later.

> 💡 **Human Angle**: The most capable option isn't the best one for every task. A quick reply doesn't need deep research, and a hundred short drafts don't need the biggest model.

---

## 3.1 Select appropriate Claude product features (Projects, research mode, chat, artifacts)

### Key Concept

**Use chat for one-off tasks, Projects for repeated work with the same context, Research for questions that need many sources, and artifacts for things you'll keep, edit or share.**

A **chat** is the quickest route for a single task. A **Project** keeps instructions and knowledge files together, so every chat in it starts with the same context, which makes it ideal for ongoing work like a client account or a team handbook. **Research** runs multiple searches, follows up on what it finds and returns a cited report; it needs web search turned on and is available on paid plans. An **artifact** is a self-contained output beside the chat, such as a document, dashboard or small tool, that you can refine, export and share.

**Think of a phone call, a shared folder, a research assistant and a finished handout**: each suits a different kind of work.

![Matching the need to the feature: a quick one-off question goes to chat, recurring work with the same files and rules to a Project, a question spread across many sources to Research, and something to keep, edit or share to an artifact.](/content/skillup/ccao/images/ccao-3-1-features.svg)

### Real use

An account manager uses a chat to reword one email, a Project for the client account (with the contract, brand guidelines and account history loaded), Research to prepare for a meeting with a prospect in a new industry, and an artifact for the quarterly review deck she keeps updating.

### How it works

- **Chat:** fastest; context lasts only for that conversation.
- **Projects:** instructions plus knowledge files shared across all chats in the Project.
- **Research:** multi-step searching with citations; needs web search on; paid plans. On mobile it searches the web only, not your connectors.
- **Artifacts:** documents, dashboards and tools beside the chat; need the code execution setting enabled.
- **Web search:** current information for a normal chat.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Chat | One-off task | Context isn't reused |
| Project | Same files and rules, many chats | Needs setting up and maintaining |
| Research | Answer spread across many sources | Slower; verify citations |
| Artifact | You'll reuse, edit or share the output | Depends on settings |

### How to do it

1. Ask: is this one-off, recurring, multi-source or something to keep?
2. Pick chat, Project, Research or artifact accordingly.
3. Turn on web search before using Research.

### Exam Trap ⚠️

<div class="note-trap">Re-uploading the same reference files into a new chat every week is the classic sign you need a Project. And Research isn't needed for a quick fact; a normal chat with web search is faster.</div>

### Go deeper

- [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- [Use Research on Claude](https://support.claude.com/en/articles/11088861-use-research-on-claude)

---

## 3.2 Differentiate between Claude model types (Haiku, Sonnet, Opus)

### Key Concept

**Haiku is the fastest and cheapest, Sonnet balances speed and capability, and Opus is the most capable for complex reasoning.**

Claude comes in three model families. **Haiku** is built for speed and high volume: short replies, classification, extraction and simple drafting. **Sonnet** is the balanced everyday choice for most business writing and analysis. **Opus** is the most capable, for complex reasoning, long multi-step work and the hardest problems, and it uses more of your usage allowance. Version numbers change over time; the family names tell you where a model sits.

**Think of a scooter, a car and a lorry**: each is the right vehicle for a different load.

![Three model families compared: Haiku is fastest and lowest cost for high-volume simple tasks, Sonnet balances speed and capability for everyday work, and Opus is most capable for complex reasoning at the highest cost.](/content/skillup/ccao/images/ccao-3-2-models.svg)

### Real use

A support team drafts hundreds of short replies a day with Haiku. Their analysts use Sonnet for weekly reports. Once a quarter, a strategy lead uses Opus to work through a complex pricing analysis with many interacting assumptions.

### How it works

- **Haiku:** speed and volume; straightforward tasks.
- **Sonnet:** everyday work; strong balance of quality and speed.
- **Opus:** hardest reasoning and long, multi-step work.
- **Model menu:** next to the send button; changes apply from the next response.
- **Usage:** more capable models, higher effort and longer thinking use more of your limit.
- **Admins** on Enterprise plans may restrict which models are available.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Haiku | High volume, simple, speed matters | Weaker on complex reasoning |
| Sonnet | Most everyday business tasks | Not the fastest or the deepest |
| Opus | Complex, high-value reasoning | Slower; uses more of your limit |

### How to do it

1. Judge how hard the reasoning is and how many times you'll run the task.
2. Choose the family that fits, using the model menu.
3. Move up a family only if quality falls short.

### Exam Trap ⚠️

<div class="note-trap">"Always use the most capable model to maximise quality" wastes speed and usage on simple, high-volume work. Match the model to the task.</div>

### Go deeper

- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)

---

## 3.3 Align model selection with task requirements (cost, speed, quality)

### Key Concept

**Start with the smallest model that does the job well, and move up only when quality falls short; use effort and thinking for hard problems, not routine ones.**

Every task trades cost, speed and quality. High-volume, simple work favours speed and low cost; one-off, high-value reasoning favours quality. Besides the model, the menu has **effort** and **thinking** settings: higher effort and thinking help with complex problems but take longer and use more of your usage limit. A practical approach is to test the task on a faster model first, and step up when the results aren't good enough.

**Think of choosing a courier**: standard post for routine letters, express only when it really matters.

![Balancing cost, speed and quality: high-volume simple tasks go to a fast model with default effort, everyday work to the balanced model, and complex high-value reasoning to the most capable model with higher effort or thinking.](/content/skillup/ccao/images/ccao-3-3-tradeoffs.svg)

### Real use

A marketing team tests product-description drafts on Haiku and finds them good enough for 500 items. For the annual brand strategy memo, the lead uses Opus with higher effort, because the reasoning matters more than the time it takes.

### How it works

- **Cost:** more capable models and higher effort use more of your limit.
- **Speed:** smaller models and lower effort respond faster.
- **Quality:** larger models and thinking help most on complex reasoning.
- **Volume** multiplies every choice: small savings per task add up.
- **Test before scaling:** try the cheaper option on a sample first.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Fast model, default effort | High volume, simple, time-sensitive | May miss nuance |
| Balanced model | Everyday quality matters | Moderate usage |
| Most capable + higher effort or thinking | Complex, high-stakes reasoning | Slow, highest usage |

### How to do it

1. Run a few real examples on the fastest suitable model.
2. Step up the model or effort only where quality isn't good enough.
3. Keep the choice for repeated tasks so you don't decide each time.

### Exam Trap ⚠️

<div class="note-trap">For "high volume, short, simple", the answer is the faster, lower-cost model. "Turn on thinking for everything" adds time and usage without helping routine tasks.</div>

### Go deeper

- [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)

---

## 3.4 Understand and manage context limitations and memory considerations (when to restart, summarize, or persist)

### Key Concept

**When a chat gets long or drifts, summarise what matters and start fresh; anything you'll need again belongs in a Project or memory, not buried in an old chat.**

Each conversation has a limited context window (its size depends on the model and plan), and long conversations use more of your usage limit. Very long chats can also drift as earlier details compete with newer ones. Chats in a Project don't share context with each other unless the information is in the Project's knowledge. On paid plans, Claude can search past chats, and memory carries useful details forward; you can view and edit memory, turn it off for a chat, or use an incognito chat that isn't saved to history or memory.

**Think of a whiteboard**: when it's full, photograph the key points, wipe it, and start again with just those points.

![Context decisions: a chat that has grown long or drifted is summarised and restarted, information needed in every chat is saved to Project knowledge or instructions, earlier conversations are found with chat search or memory, and a sensitive one-off chat uses incognito.](/content/skillup/ccao/images/ccao-3-4-context.svg)

### Real use

After a two-hour session planning a product launch, Claude starts mixing up early decisions. The planner asks for a summary of all decisions so far, opens a new chat in the launch Project, and pastes the summary in. She also adds the final launch timeline to the Project's knowledge so every future chat has it.

### How it works

- **Restart:** when a chat is long, slow or drifting; carry over a summary.
- **Summarise:** ask Claude for the decisions, facts and open questions so far.
- **Persist:** Project knowledge or instructions for anything needed repeatedly.
- **Chat search and memory:** paid plans can search past chats; memory can be viewed, edited or turned off.
- **Incognito:** not saved to history or memory; not available in Projects.
- **Usage:** long chats use more of your limit than fresh ones.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Continue the chat | Still short and focused | Grows heavier over time |
| Summarise and restart | Long, drifting or slow chat | Detail not in the summary is lost |
| Persist in a Project | Needed in many future chats | Must be kept up to date |
| Incognito chat | Sensitive one-off you don't want saved | No history, no memory |

### How to do it

1. When a chat drifts or slows, ask for a summary of decisions and open items.
2. Start a new chat with that summary.
3. Move anything you'll reuse into Project knowledge or instructions.

### Exam Trap ⚠️

<div class="note-trap">"Keep everything in one endless chat so Claude remembers it all" is the trap: long chats drift and use more usage. And separate chats in a Project don't see each other's content unless it's added to Project knowledge.</div>

### Go deeper

- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [Chat search and memory](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)

---

## Deep Dive: Making Product and Model Selection Click

### 1. The connective narrative

This domain is about fit. Features (3.1) fit the shape of the work: one-off, recurring, multi-source or reusable. Models (3.2) and settings (3.3) fit the difficulty and volume: fast and cheap for simple work at scale, capable and thorough for hard problems. Context management (3.4) keeps any of it working over time by restarting with summaries and saving what matters where it will be found again.

### 2. Worked scenario

> **Scenario.** A customer-success team sets up a Project per key account, with contracts and meeting notes as knowledge (3.1). Daily reply drafts run on Haiku; renewal analyses run on Sonnet; the annual risk review uses Opus with higher effort (3.2, 3.3). When a long renewal chat starts confusing two customers' figures, the lead summarises, restarts, and adds the agreed figures to the Project knowledge (3.4).

### 3. Memory aid

**C-P-R-A** for features: **C**hat (once), **P**roject (repeat), **R**esearch (many sources), **A**rtifact (keep). And for models: **H**aiku-fast, **S**onnet-steady, **O**pus-deep.

### 4. Exam strategy for this domain

Wrong answers usually reach for the biggest option: the top model, Research for a quick fact, one endless chat. The right answer is the lightest option that meets the need, plus saving reusable context in a Project.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Re-uploading the same files every time | Use a Project |
| Question needs many sources and citations | Research (paid plans; web search on) |
| Something to keep editing or share | Artifact |
| Hundreds of short simple drafts | Haiku |
| Everyday reports and writing | Sonnet |
| Complex multi-step reasoning | Opus, maybe higher effort |
| Long chat starts confusing details | Summarise and start a new chat |
| Need info in every chat | Project knowledge or instructions |
| Sensitive one-off, don't keep it | Incognito chat |
