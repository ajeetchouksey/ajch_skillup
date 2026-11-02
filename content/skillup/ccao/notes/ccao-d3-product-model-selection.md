# D3: Product and Model Selection

> **Exam weight**: 12% · **Questions**: 22 in the bank

## Overview

This domain is about choosing the right part of Claude for the job and keeping long work on track. The first lesson covers features: chat, Projects, Research, artifacts, code execution and skills. The next two cover models and effort, and the last covers context and memory. The AI Fluency competency at work is **Delegation**: deciding what to hand to which tool.

> 💡 **Human Angle**: The most capable option isn't the best one for every task. A quick reply doesn't need deep research, and a hundred short drafts don't need the biggest model.

---

## 3.1 Select appropriate Claude product features (Projects, research mode, chat, artifacts)

### Key Concept

**Pick the lightest feature that fits the shape of the work.**

The shape comes from three questions: is the work one-off or recurring, does it draw on one source or many, and will you read the output once or keep it? Heavier features cost setup, time or usage, so they only pay off when the work needs them.

**Think of a phone call, a shared folder, a research assistant and a finished handout**: you wouldn't send a research assistant to check a shop's opening hours.

![A decision path for choosing a feature: recurring files and rules lead to a Project, an answer spread across many sources to Research, numbers to calculate from a file to code execution, something to keep or share to an artifact, and otherwise a plain chat with web search; a procedure repeated the same way is a skill.](/content/skillup/ccao/images/ccao-3-1-features.svg)

### Real use

A partnerships lead at a semi-professional football club writes one sponsor email in chat, runs the sponsorship season from a Project and uses Research to scan a new sector. Code execution charts her uploaded match-day attendance CSV (a plain file of rows and columns that spreadsheets open), and the club's brand-format skill styles the sponsor deck.

### How it works

Someone runs Research for a quick opening-hours check and waits for a long report, while retyping the same contract into a new chat every Monday.

- **Chat and web search:** fastest for one-off tasks; context lasts only for that chat. Web search adds current facts, with citations in every response.
- **Project:** instructions and knowledge files shared by every chat in it (see 5.1).
- **Research:** several searches that build on each other. Paid plans only, with web search on; it uses limits faster, runs on its own model whatever you picked, and on Mobile searches only the web.
- **Make and run:** artifacts open beside the chat for things you'll keep, edit or share. Code execution runs code on an uploaded file, such as analysing and charting a CSV, and creates Excel, Word, PowerPoint or PDF files. Skills are saved procedures Claude loads only when a task needs them: built-in ones handle those file types, and custom ones capture things like your brand format. All three need the **Code execution and file creation** setting.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Chat (with web search) | A one-off task or a quick current fact | Context isn't reused |
| Project | The same files and rules recur across many chats | Needs setting up and keeping current |
| Research | The answer is spread across many sources | Slower; uses limits faster; open the sources |
| Artifact | You'll keep, edit or share the output | Needs the setting on |
| Code execution on an uploaded file | Numbers must be calculated or charted from real data | Check the method and a few results |
| Skill | A task must be done the same way every time | Someone must build and maintain it |

### How to do it

1. Ask: one-off or recurring, one source or many, read or keep?
2. Pick the lightest feature that fits.
3. Check that the setting it needs is on.

### Exam Trap ⚠️

<div class="note-trap">Using Research for a quick fact that web search answers in seconds burns time and usage on a long report nobody needed.</div>

### Go deeper

- [Claude 101 (Anthropic Academy)](https://anthropic.skilljar.com/claude-101)
- [Use research on Claude](https://support.claude.com/en/articles/11088861-use-research-on-claude)

---

## 3.2 Differentiate between Claude model types (Haiku, Sonnet, Opus)

### Key Concept

**Haiku suits speed and volume, Sonnet suits everyday work, and Opus suits the hardest reasoning.**

Judge the task before you pick: how many steps it has, whether its information conflicts and how much judgement it needs, against how simple and repeatable it is. The family name tells you where a model sits, while version numbers change.

**Think of a scooter, a car and a lorry**: each is the right vehicle for a different load.

![Judge the task first, then pick a family: Haiku for high-volume simple tasks, Sonnet for most everyday writing and analysis, and Opus for the hardest multi-step reasoning as the most capable of the three; the model menu also lists other models such as Fable, which sits above Opus.](/content/skillup/ccao/images/ccao-3-2-models.svg)

### Real use

A digital-team member at a regional tourism board uses Haiku to tag 600 archived attraction listings by theme and Sonnet to draft the weekly visitor newsletter. Opus untangles a multi-year visitor-numbers analysis whose sources conflict. While choosing, she notices the menu also lists Fable.

### How it works

One team runs a simple tagging job on the heaviest model and waits; another runs a tangled pricing analysis on the fastest one and gets a shallow answer. Neither judged the task first.

- **Haiku:** the fastest, lowest-cost family, for high-volume, simple, repeatable tasks such as sorting items into groups or pulling fields out of text. Its job is volume and simplicity, not one task type.
- **Sonnet:** balances speed and capability, and is a common everyday choice for most writing and analysis. It isn't a sorting-only model either.
- **Opus:** the most capable of the three families the exam names, for long, multi-step reasoning and the hardest problems. It's slower, uses more of your limit and isn't on the Free plan.
- **The menu:** it sits next to the send button, and "More models" shows extra options. It also lists other models, such as Fable, which sits above Opus for the most demanding work. On Enterprise, an admin may limit which models you see.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Haiku | High volume, simple, speed matters | Weaker on complex reasoning |
| Sonnet | Most everyday writing and analysis | Not the fastest or the deepest |
| Opus | Complex, multi-step, high-value reasoning | Slower; uses more of your limit |

### How to do it

1. Judge the reasoning the task needs.
2. Judge how often you'll run it.
3. Pick the family in the model menu.

### Exam Trap ⚠️

<div class="note-trap">Defaulting to the most capable family for everything makes simple, high-volume work slower and uses up your limit without better results.</div>

### Go deeper

- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)

---

## 3.3 Align model selection with task requirements (cost, speed, quality)

### Key Concept

**Test the lightest option on a sample, then step up effort or model only where quality falls short.**

Every task trades cost, speed and quality, and volume multiplies each choice across hundreds of items. A 25-item sample tells you more than a guess.

**Think of choosing a courier**: standard post does routine letters, and express is for when it really matters.

![A step-up path: run a sample on the lightest option at default effort, keep it if quality is good enough, raise effort if answers are right but shallow on the hard steps, and step up the model family only if that still falls short, remembering that volume multiplies every choice.](/content/skillup/ccao/images/ccao-3-3-tradeoffs.svg)

### Real use

A data steward at a public library service tests 25 of 4,000 catalogue blurbs on the lightest model at its default effort; quality holds, so she runs the batch. For a tricky comparison of two lending policies, she raises effort first and checks the result before considering a bigger model.

### How it works

A weekly batch of 300 short summaries runs at maximum effort on the heaviest model, takes all afternoon and eats a large share of the week's usage. A sample would have shown the lightest setting was enough.

- **Start light, on a sample:** run a handful of real items on the lightest model at its Default effort (the level each model marks as recommended) and check them.
- **Effort:** controls how thorough Claude is with each response. Low and Medium suit routine work and stretch your usage, High is the best balance, and Max is the most thorough; higher effort is slower and uses more of your limit.
- **Thinking:** on current models in Claude, thinking can't be turned off (on Opus 5.5 it is always on), so effort is the setting you change. Where an older model still shows a thinking toggle, it helps on complex problems. Typing "think harder" into the prompt isn't the lever.
- **Pick the lever that matches the gap:** right but shallow on the hard steps? Raise effort. Still short, or the task has become harder? Step up the family for that task, not for every task, and recheck when a repeated task changes.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Lightest model at default effort | High volume, simple, time-sensitive | May miss nuance; sample it |
| Raise effort | Same model, but the hard steps come back shallow | Slower; uses more of your limit |
| Step up the model family | Quality still falls short at higher effort, or the task now needs deeper reasoning | Slower and costlier on every run |
| Keep the setting as that task's default | The task repeats unchanged | Recheck it when the task changes |

### How to do it

1. Run 20–25 real items on the lightest option.
2. Raise effort where the hard steps are shallow.
3. Step up the model only if that isn't enough.
4. Keep the setting for that task.

### Exam Trap ⚠️

<div class="note-trap">Setting maximum effort on every task, including quick replies, makes routine work slower and drains usage with no gain in quality.</div>

### Go deeper

- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)
- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)

---

## 3.4 Understand and manage context limitations and memory considerations (when to restart, summarize, or persist)

### Key Concept

**When a chat drifts, carry a summary into a fresh chat; save what you'll reuse in the Project.**

A chat can only take so much of the conversation into account at once (its context window). Long chats drift as early details compete with later ones, and they use more of your usage limit. Anything you'll need again belongs where it will be found.

**Think of a full whiteboard**: photograph the key points, wipe it and start again.

![A chat timeline: decisions made early get mixed up a hundred messages later, so you ask for a summary and start a new chat from it, and save anything every chat needs to Project knowledge; for one sensitive chat, use incognito outside a Project or turn memory off inside one.](/content/skillup/ccao/images/ccao-3-4-context.svg)

### Real use

A programme coordinator at an international development charity notices a two-hour workshop-planning chat mixing up venues. She asks for a summary of decisions, restarts in the workshop Project and adds the agreed agenda to Project knowledge. For a staff-grievance note she turns memory off for that one chat, as incognito isn't available in Projects.

### How it works

Three hours into one planning chat, Claude mixes up which venue was agreed, because early decisions are buried under a hundred later messages.

- **Restart and persist:** ask for a summary of decisions, facts and open questions, and start a new chat with it. Put what every future chat needs into Project knowledge or instructions (see 5.1).
- **Memory:** on by default on Free, Pro, Max and Ultra. On Team and Enterprise, owners control it, and it's off for each member until they turn it on. You can view and edit memory, but deleting a chat doesn't remove memory entries made from it.
- **Chat search** (asking Claude to find a past chat) is for paid plans only.
- **One sensitive chat, two options:** incognito (outside Projects only) isn't saved to history or memory, but it's still kept for 30 days and, on Team and Enterprise, included in organisation data exports. Memory off for this chat ("+" menu, before the first message) works inside Projects; the chat stays in your history.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Continue the chat | Still short and focused | Grows heavier over time |
| Summarise and restart | Long, drifting or slow chat | Detail left out of the summary is lost |
| Save to Project knowledge or instructions | Needed in many future chats | Must be kept current |
| Memory off for this chat | Keep the chat, but don't use or add to memory | Must be set before the first message |
| Incognito chat | A one-off you don't want in history or memory | Outside Projects only; can't be reopened once closed |

### How to do it

1. When a chat drifts, ask for a summary of decisions and open items.
2. Start a new chat with it.
3. Move what you'll reuse into the Project.

### Exam Trap ⚠️

<div class="note-trap">Keeping one endless chat "so Claude remembers everything" makes it drift and burns usage, and the decisions you need end up buried.</div>

### Go deeper

- [Use Claude's chat search and memory to build on previous context](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)
- [Use incognito chats](https://support.claude.com/en/articles/12260368-use-incognito-chats)

---

## Deep Dive: Making Product and Model Selection Click

### 1. The connective narrative

Every lesson here is Delegation: deciding what work to hand to which tool, and at what size. Features fit the shape of the work, model families fit its difficulty, and effort and samples fit its volume.

Context habits keep long work honest. A chat is a temporary workspace, a Project is where reusable knowledge lives, and memory and incognito decide what carries forward. Each choice starts light and steps up only when the work shows it needs more.

### 2. Worked scenario

> **Scenario.** An architecture practice's office manager is running a studio move.
>
> 1. **Where the move lives.** A single chat or a Project? The floor plans and supplier quotes come up in every chat, so she sets up a Project and adds them as knowledge.
> 2. **Comparing five removal firms.** Research or web search? Web search covers the quick price checks in seconds. She saves Research for one question that spans many sources, the rules on office moves, and opens the sources her conclusions rest on.
> 3. **Model for 200 label descriptions.** She runs a sample of 20 on the lightest model at default effort. Quality holds, so the other 180 run the same way.
> 4. **The long chat drifts on day three.** She asks for a summary, restarts from it and saves the final layout to the Project, so every later chat starts from the agreed plan.

### 3. Memory aid

Five questions, each choosing one thing:

- **Once or again?** Chat or Project.
- **One source or many?** Web search or Research.
- **Read or keep?** Inline answer or artifact.
- **Simple or hard?** Lighter or heavier model.
- **Short or long?** Continue, or summarise and restart.

### 4. Exam strategy for this domain

- Wrong answers reach for the biggest option: the top model, maximum effort, Research for a quick fact, or one endless chat.
- Right answers pick the lightest fit, test it on a sample and save reusable context in a Project.
- Five minutes before: lightest fit first; step up only on evidence.

---

## Cheat Sheet 📋

| Situation | What to do |
|---|---|
| Re-uploading the same files every week | Use a Project |
| Quick current fact | Chat with web search |
| Question spread across many sources | Research (paid plans; web search on) |
| Analyse an uploaded CSV, or make a chart or file | Code execution (setting on) |
| Repeatable format or procedure | A skill |
| Hundreds of short simple drafts | Haiku, tested on a sample |
| Shallow answers on a hard step | Raise effort, then step up the family |
| Long chat confusing details | Summarise and start fresh |
| Sensitive one-off outside a Project | Incognito (still kept 30 days) |
| Sensitive chat inside a Project | Turn memory off for that chat |
