# D1: Prompting and Task Execution

> **Exam weight**: 14% · **Questions**: ~12 in the bank

## Overview

This domain covers getting useful work out of Claude in everyday business tasks: writing prompts that give Claude what it needs, breaking big requests into steps you can check, improving a prompt over a few rounds, and changing your approach for analysis, research, drafting and brainstorming.

> 💡 **Human Angle**: Claude can't read your mind or your inbox. Most disappointing answers trace back to something the person knew and didn't say.

---

## 1.1 Create effective prompts for business and technical tasks

### Key Concept

**A strong prompt gives Claude the goal, the context, the audience, the format and an example; everything you leave out, Claude has to guess.**

Claude responds to what's on the page. "Write a project update" gets a generic update. "Write a 150-word update for the steering committee on the CRM migration: on track, one risk (data cleanup is two weeks behind), one decision needed (approve extra contractor budget). Plain English, three short paragraphs" gets something you can send. Clear structure helps too: putting pasted material inside labelled tags such as `<notes>` separates it from your instructions.

**Think of briefing a capable new colleague**: they're smart, but they weren't in last week's meeting.

![A strong prompt stacks five parts: the goal, the context and background, the audience, constraints and format, and an example of good output, which together produce a usable first draft.](/content/skillup/ccao/images/ccao-1-1-prompt-anatomy.svg)

### Real use

A project manager asks for "a summary of the vendor proposals" and gets a bland list. She tries again with the decision the summary supports, the three criteria that matter (cost, timeline, support), the reader (the finance director) and a table format. The second answer goes straight into the approval email.

### How it works

- **Goal:** what the output is for and what decision it supports.
- **Context:** background, constraints, what's already been tried.
- **Audience:** who reads it and what they already know.
- **Format and length:** table, bullets, word count, sections.
- **Example:** a sample of good output when the style matters.
- **Structure:** label pasted material, for example `<notes>…</notes>`, and keep instructions separate.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Short, direct prompt | Simple, low-stakes task | Generic output if context matters |
| Full brief (goal, context, audience, format) | Anything you'll send or rely on | Takes a minute longer to write |
| Brief plus an example | Style or format must match exactly | Claude may copy the example too closely |

### How to do it

1. Start with the goal and who will read the result.
2. Add the context Claude can't know: facts, constraints, decisions already made.
3. State the format and length, and add an example if style matters.

### Exam Trap ⚠️

<div class="note-trap">"Ask again more politely" or "use a longer prompt" isn't the fix for a generic answer. The fix is the missing information: the goal, the audience, the context or the format. Length without that content doesn't help.</div>

### Go deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Use XML tags to structure prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)

---

## 1.2 Apply task decomposition techniques to structure complex requests

### Key Concept

**Split a big request into steps you can check: plan, then build each part, then assemble, with each step's output feeding the next.**

One giant request ("write our whole quarterly business review") gets a shallow answer that's hard to fix, because everything happens at once. Breaking it down lets you check each step before building on it: agree the outline, draft each section with the right data, then pull it together. If one part is wrong, you redo that part, not the whole thing.

**Think of building a house**: you check the foundations before anyone puts up walls.

![One large request produces a shallow result that is hard to fix, while a decomposed chain of outline, sections and assembly lets you check and correct each step before moving on.](/content/skillup/ccao/images/ccao-1-2-decomposition.svg)

### Real use

An operations lead needs a new onboarding guide. Instead of one request, she asks Claude for an outline first and adjusts it. Then she drafts each section with the right policy pasted in, and finally asks for a consistency pass across the whole guide. Errors get caught at the outline, where they're cheap to fix.

### How it works

- **Plan first:** ask for an outline, a list of steps or questions to answer.
- **One part per step:** give each step only the material it needs.
- **Check between steps:** correct the plan before building on it.
- **Assemble and review:** a final pass for consistency, tone and gaps.
- **Keep it in one place:** a Project keeps shared context across the steps.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Single request | Short, well-defined task | Hard to fix if it goes wrong |
| Step-by-step chain | Long or multi-part deliverable | More turns to manage |
| Ask Claude to propose the steps | You're unsure how to break it down | Review its plan before following it |

### How to do it

1. Ask Claude for an outline or plan, and edit it.
2. Work through one section or step at a time, checking each.
3. Finish with an assembly and consistency pass.

### Exam Trap ⚠️

<div class="note-trap">"Put everything in one detailed prompt so Claude sees the whole picture" sounds efficient but makes errors hard to spot and fix. For complex work, decompose and check as you go.</div>

### Go deeper

- [Chain complex prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts)

---

## 1.3 Iterate prompts to improve output quality

### Key Concept

**Treat the first answer as a draft: say exactly what to keep, what to change and why, and fix the prompt itself when the same miss keeps coming back.**

Good results usually take a few rounds. Vague feedback ("make it better") gets a random change; specific feedback ("keep the structure, cut it to 200 words, and replace the jargon in paragraph two") gets the change you wanted. If you find yourself making the same correction every time, the prompt is missing something: edit it, or save the fix in Project instructions.

**Think of a tailor's fitting**: you point at the exact seam that's wrong, not "it doesn't look right".

![The iteration loop: write a prompt, read the output against your goal, give specific feedback on what to keep and change, and when the same issue repeats, edit the prompt or instructions instead.](/content/skillup/ccao/images/ccao-1-3-iterate.svg)

### Real use

A communications lead gets a first press release that's accurate but too formal. She replies: "Keep the facts and quotes. Make the opening sentence about the customer benefit, not our company. Aim for a friendlier tone like the example below." The second version is close; one more round fixes the headline.

### How it works

- **Compare to the goal:** what's right, what's missing, what's wrong.
- **Be specific:** name the part, the change and the reason.
- **Keep what works:** say so, or Claude may change it.
- **Show, don't describe:** paste an example of the tone you want.
- **Fix the source:** recurring corrections belong in the prompt or instructions.
- **Edit and resend** your earlier message when the original prompt was the problem.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Specific feedback in the chat | One output needs adjusting | Fix lives only in this chat |
| Edit the original prompt | The prompt itself caused the miss | Lose the earlier answer |
| Update Project instructions | The same correction keeps recurring | Affects every chat in the Project |

### How to do it

1. Read the output against your goal and list what to keep and change.
2. Give specific feedback, with an example if tone or style is the issue.
3. If you correct the same thing twice, move the fix into the prompt or instructions.

### Exam Trap ⚠️

<div class="note-trap">"Regenerate until you get a good one" or "tell Claude to try harder" wastes rounds. Specific feedback, and fixing the prompt when the same issue repeats, is what the exam rewards.</div>

### Go deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

---

## 1.4 Adapt prompting strategies based on task type (analysis, research, drafting, brainstorming)

### Key Concept

**Different tasks need different prompts: analysis needs the data and the question, research needs sources, drafting needs audience and tone, brainstorming needs quantity and range.**

The same prompting habits don't fit every task. For **analysis**, give the data and ask Claude to show its method and state its assumptions. For **research**, ask for sources you can check, and use Research for multi-source questions. For **drafting**, specify audience, purpose, tone and length, ideally with an example. For **brainstorming**, ask for many varied ideas without judging them yet, then narrow down in a second step.

**Think of different tools in one kit**: a ruler, a magnifying glass, a pen and a whiteboard each suit a different job.

![Four task types and what each prompt needs: analysis gives the data and asks for the method, research asks for checkable sources, drafting sets audience, tone and length, and brainstorming asks for many varied ideas before narrowing.](/content/skillup/ccao/images/ccao-1-4-task-types.svg)

### Real use

An HR lead needs three things in one afternoon: an analysis of exit-survey themes (she uploads the survey export and asks for themes with counts and example quotes), a draft announcement about a new benefit (audience, tone and length specified), and ideas for the team offsite (she asks for 20 varied ideas, then picks five to develop).

### How it works

- **Analysis:** supply the data; ask for method, assumptions and findings; check the numbers.
- **Research:** ask for sources and quotes; use Research for multi-source questions; verify citations.
- **Drafting:** audience, purpose, tone, length and an example.
- **Brainstorming:** quantity and variety first; evaluate in a separate step.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Analysis prompt | You have data and a question | Numbers still need checking |
| Research prompt / Research | The answer is spread across sources | Takes longer; verify citations |
| Drafting prompt | You need text someone will read | Needs audience and tone set |
| Brainstorm prompt | You need options, not an answer | Most ideas will be discarded |

### How to do it

1. Name the task type before you write the prompt.
2. Include what that type needs: data, sources, audience or quantity.
3. For brainstorming, generate first and judge in a second step.

### Exam Trap ⚠️

<div class="note-trap">Using a drafting-style prompt for analysis ("write me a report on the survey") skips the data and the method, so the "findings" can't be checked. Match the prompt to the task type.</div>

### Go deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Use examples (multishot prompting)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting)

---

## Deep Dive: Making Prompting Click

### 1. The connective narrative

Every lesson here is about giving Claude what it needs to do the job you have in mind. A good prompt (1.1) supplies the goal, context, audience and format. Decomposition (1.2) keeps big jobs checkable. Iteration (1.3) turns a first draft into the right one with specific feedback, and moves recurring fixes into the prompt. Adapting by task type (1.4) recognises that analysis, research, drafting and brainstorming each need different ingredients.

### 2. Worked scenario

> **Scenario.** A marketing manager must produce a launch plan. She asks Claude for an outline first (1.2), giving the product, audience, budget and deadline (1.1). For the competitor section she uses Research and checks the sources (1.4). The first draft of the announcement is too formal, so she gives specific feedback with an example, and adds "write in our brand voice" to the Project instructions so she doesn't repeat it (1.3).

### 3. Memory aid

**GCAFE** for a strong prompt: **G**oal, **C**ontext, **A**udience, **F**ormat, **E**xample.

### 4. Exam strategy for this domain

Wrong answers usually add effort without adding information: regenerate, be more polite, write longer. The right answer adds what Claude was missing, splits the work into checkable steps, or matches the prompt to the task.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Output is generic | Add goal, context, audience, format |
| Style must match exactly | Include an example |
| Big multi-part deliverable | Outline first, then one part at a time |
| Same correction every time | Fix the prompt or Project instructions |
| "Make it better" didn't work | Give specific keep/change feedback |
| Analysing data | Supply data; ask for method and assumptions |
| Multi-source question | Research, then verify citations |
| Need many options | Brainstorm widely, judge in a second step |
