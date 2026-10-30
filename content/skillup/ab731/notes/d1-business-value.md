# D1: Identify the Business Value of Generative AI Solutions

> **Exam weight**: 35–40% · **Questions**: ~37 in the bank

## Overview

This domain tests whether a business leader can tell what kind of AI a problem needs, what it will cost and what could go wrong, before any budget is committed. It covers generative AI against traditional machine learning, the choice between pretrained, fine-tuned and grounded models, token-based cost and ROI, the known failure modes (fabrication, unreliability, bias), prompt engineering, grounding and RAG, data quality, and AI security.

> 💡 **Human Angle**: A CFO doesn't fund the AI that wins the demo. This domain rewards the leader who asks the business question ("what does this save, and what could it get wrong?") before the technology question.

---

## 1.1 Describe the differences between generative AI and other types of AI

### Key Concept

**Pick the AI type by the output you need: new content means generative AI; a label or a number means traditional ML.**

A classifier learns a boundary and outputs one of a fixed set of labels. A regression model outputs a number. A generative model learns a probability distribution over tokens and produces a new sequence one token at a time, so it can write a paragraph nobody has written before. A spam classifier can never output a new category.

**Think of a novelist versus a sorting office**: one writes new letters, the other decides which pigeonhole each existing letter goes in.

![Input data branches to four AI types: generative AI to generate new content, discriminative ML to classify, regression ML to predict a number, and recommendation to surface relevant items](/content/skillup/ab731/images/ab731-d1-ai-type-selection.svg)

### Real use

A retailer wants incoming emails sorted into "complaint", "order query" and "general enquiry", and a reply drafted for each complaint. The sorting is classification, so a model trained on labelled emails does it cheaply and consistently. The reply is new text, so that part is generative AI.

### How it works

- **Generative AI** creates text, images, code or audio: drafting a proposal, summarising a meeting.
- **Discriminative (classification) ML** assigns a label: spam detection, sentiment, fraud flag.
- **Predictive (regression) ML** forecasts a number: sales, demand, delivery delay.
- **Recommendation** surfaces relevant items: "customers like you also bought".

Watch the verb in the scenario: "generate", "draft", "compose" or "create" points to generative AI; "classify", "detect" or "predict" points to traditional ML.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Generative AI | The output is new content | Higher cost per item, output varies |
| Classification ML | The output is one of a fixed set of labels | Needs labelled training data |
| LLM as a zero-shot classifier | No labelled data yet and categories still change | Costs more per item; swap to a trained classifier later |

### How to do it

1. Write down the exact output the business needs: a label, a number or new content.
2. If it's a label or a number and history exists, scope a traditional ML model.
3. If it's new content, scope generative AI and plan grounding and review (1.9, 1.5).

### Exam Trap ⚠️

<div class="note-trap">"Use generative AI to categorise each item" is a common distractor for a pure classification task. It would work, but it is more expensive and less consistent than a classifier trained on labelled examples. A label or a number means ML; new content means generative AI.</div>

### Go deeper

- [Fundamentals of generative AI](https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/)

---

## 1.2 Select a generative AI solution to meet a business need

### Key Concept

**Match the solution to the shape of the work: one prompted task is Copilot; a goal pursued over steps, systems and days is an agent.**

Copilot is assistive: it answers when a person prompts it, one interaction at a time. An AI agent is given an objective, plans the steps, uses tools, keeps state across sessions and adapts when something unexpected turns up. A scheduled script that runs the same fixed steps is neither; it's automation without reasoning.

**Think of Copilot as an assistant and an agent as an employee**: you ask the assistant for help with a task, and you give the employee a goal.

![Four business needs matched to a solution: a one-off draft to Copilot, a research report to the Researcher agent, a goal across systems and days to a custom agent, and a fixed rule-based file move to scripted automation.](/content/skillup/ab731/images/ab731-1-2-solution-choice.svg)

### Real use

A sales manager needs one follow-up email from her own call notes: Copilot drafts it in one prompt. A procurement team runs a negotiation for weeks, checking each new vendor letter against everything agreed so far: an agent that keeps the negotiation history across days fits that work.

### How it works

- **Single, prompted, one session**: Microsoft 365 Copilot in the app the content lives in.
- **Deep research or data analysis**: the built-in Researcher or Analyst agent (2.9).
- **Multi-step, triggered, across systems or days**: a custom agent, usually built in Copilot Studio (2.5).
- **Fixed sequence, no judgement**: plain scripted automation; calling it "agentic" is wrong.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Copilot (assistive) | One task, a human prompts it, done in one session | Someone must prompt every step |
| Built-in agent | Researcher or Analyst's purpose already fits | No company-specific logic |
| Custom agent | Goal spans steps, systems or days, with no prompt each time | Build, govern and monitor it |

### How to do it

1. Ask: is this one prompted request, or a goal with several steps and no human prompt between them?
2. Check whether a built-in agent already covers it before designing a custom one.
3. If the steps never change and need no judgement, use automation, not an agent.

### Exam Trap ⚠️

<div class="note-trap">"Route 500 tickets a day without a human prompting each step" needs an agent, not Copilot. The reverse trap: building an agent for a one-off, single-session request, or calling an unattended fixed-sequence script an AI agent just because nobody triggers it.</div>

### Go deeper

- [Agents for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview)

---

## 1.3 Describe the differences between AI models, including fine-tuned and pretrained models

### Key Concept

**Start with a pretrained model, good prompts and grounding; fine-tune only for a behaviour gap that they can't close.**

A pretrained model is trained on massive general data and works out of the box. A fine-tuned model is a pretrained model given extra training on a smaller, specialised dataset, which changes its weights. That costs labelled data, training spend and time, and the facts it absorbs go stale the moment the source changes. Models also differ in size: larger models reason better, smaller ones are faster and cheaper.

**Think of a pretrained model as a capable generalist hire**: fine-tuning is a three-month specialist bootcamp, and a clear brief (prompting) costs nothing.

![A ladder of customisation: prompt engineering first, then grounding with RAG for knowledge gaps, then fine-tuning only for a persistent style or vocabulary gap.](/content/skillup/ab731/images/ab731-1-3-model-ladder.svg)

### Real use

A legal team wants Q&A over contracts that change monthly: RAG over a pretrained model, because fine-tuned facts would be a month old. A retailer wants marketing copy in a playful, slang-heavy voice the base model keeps missing: that persistent style at high volume is the legitimate fine-tuning case.

### How it works

- **Knowledge gap** (private, current or changing facts): ground the model with RAG (1.10).
- **Behaviour gap** (a distinctive style or specialised vocabulary): fine-tune, if prompting has failed and volume justifies it.
- **Size**: a small model (such as Phi) for simple, high-volume tasks; a large model for complex reasoning (2.13).
- RAG can cite its sources. A fact baked into weights has no document to point to.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Pretrained + prompt | Most general tasks | Can't know private or new facts |
| Pretrained + RAG | Answers need current, private or cited facts | Index to build and maintain |
| Fine-tuned | Stable style or vocabulary the base model can't learn from context | Training cost; facts go stale |

### How to do it

1. Try a well-structured prompt with examples and measure where it falls short.
2. If the gap is facts, ground the model; if the source changes, never fine-tune facts in.
3. Fine-tune only when a measured style gap remains and the volume pays for the training.

### Exam Trap ⚠️

<div class="note-trap">Fine-tuning is not the first thing to reach for, and it is the wrong way to give a model facts that change. A distractor says "a document exists, so it must be RAG": if the document describes how to write (a stable brand voice) rather than facts to retrieve, fine-tuning can be right.</div>

### Go deeper

- [When to use fine-tuning](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/fine-tuning-considerations)

---

## 1.4 Explain the cost drivers in generative AI usage, including tokens and return-on-investment (ROI) considerations

### Key Concept

**Generative AI cost scales with tokens in and out; ROI is the value created set against that cost.**

A token is the unit of text a model processes, roughly ¾ of a word. You pay for input tokens (the prompt, including any retrieved documents) and output tokens (the response). The context window is the most prompt-plus-response tokens a model can handle in one request. So a 10-page contract costs more to summarise than a one-paragraph email, even with the same instruction.

**Think of tokens as a taxi meter**: it runs on every word you send and every word you get back.

![Cost per request is input tokens plus output tokens times the model's price; multiplied by monthly volume it gives operating cost, which is set against time saved, quality and scale to give ROI.](/content/skillup/ab731/images/ab731-1-4-token-meter.svg)

### Real use

A team's AI bill rises 40% in a month with no new users. The cause is a change that stuffs whole documents into every prompt: the number of requests didn't grow, the tokens per request did. Retrieving only the relevant chunks brings the cost back down.

### How it works

- **Cost levers**: shorter prompts, shorter responses, a smaller model for simple tasks, reused system context.
- **Operating cost** = average tokens per request × monthly requests × the model's price.
- **Three ROI lenses**: time saved (hours × rate), quality lift (fewer errors), and scalability (more output from the same headcount).
- Licence-based products (Copilot per user, Foundry Tools commitment tiers) have their own cost models (3.9, 3.10).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Optimise tokens | High volume, low stakes per answer | Risk of trimming context the answer needs |
| Pay for accuracy | A wrong answer costs far more than the tokens | Higher cost per request |
| Measure first | Usage pattern is still unknown | Delays the business case |

### How to do it

1. Estimate input and output tokens for a typical request, including retrieved content.
2. Multiply by monthly volume and the model's price to get operating cost.
3. Set it against time saved, quality and scale, then track both after launch.

### Exam Trap ⚠️

<div class="note-trap">"Cost is driven by the number of users who log in" is wrong for metered generative AI: the unit is tokens, input and output. ROI distractors include irrelevant factors such as the dashboard's colour scheme. And the cheapest model per token can be the most expensive choice once wrong answers are costed.</div>

### Go deeper

- [What is Azure OpenAI in Foundry Models?](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/overview)

---

## 1.5 Identify the challenges of using generative AI solutions, including fabrications, reliability, and bias

### Key Concept

**Generative AI can be fluent and wrong at once: fabrication, unreliability and bias come from how it works, so plan for them.**

A language model predicts the next likely token. It has no built-in fact-checker, it's tuned for text that reads well rather than text that is true, and it inherits whatever patterns sit in its training data. These aren't rare bugs; they are standing risks every use case must plan for.

**Think of a brilliant new hire who never says "I don't know"**: valuable, but you check their work in proportion to what's at stake.

![Three challenges and their mitigations: fabrication is countered by grounding and human review, unreliability by low temperature and evaluation, and bias by representative data and evaluation across groups.](/content/skillup/ab731/images/ab731-1-5-challenges.svg)

### Real use

A hospital's discharge-summary assistant states a wrong dosage with full confidence (fabrication). An executive report differs slightly each run on the same data (reliability). A hiring model trained on ten years of history ranks women lower for senior roles (historical bias).

### How it works

- **Fabrication** (hallucination): plausible but false content. Microsoft's docs say "fabrication"; same thing. Mitigate with grounding and human review.
- **Reliability**: the same input can give different output. **Temperature** controls randomness; 0 is deterministic, and most production use is low but non-zero.
- **Bias**: **historical** (past discrimination in the data), **representation** (groups or languages missing), **measurement** (data collected inconsistently).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Human review of every output | Output affects health, money, jobs or rights | Slower, needs reviewers |
| Grounding + spot checks | Factual answers at volume, moderate stakes | Some errors still reach users |
| Light editorial pass | Low-stakes creative drafts | Variation accepted as a feature |

### How to do it

1. Ask: what happens if this output is wrong, and who would catch it?
2. Ground factual use cases and add human review in proportion to the stakes.
3. Evaluate output across user groups and languages before launch.

### Exam Trap ⚠️

<div class="note-trap">"Use a larger model" doesn't fix fabrication; larger models still fabricate. Different output for the same input is non-determinism (reliability), not fabrication or bias. Match bias to cause: past discrimination is historical, missing groups or languages is representation, inconsistent collection is measurement.</div>

### Go deeper

- [Transparency note for Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/transparency-note)

---

## 1.6 Identify when generative AI solutions can provide business value, including scalability and automation

### Key Concept

**Generative AI pays off on high-volume, language-heavy, checkable work, and the first projects are those high in value and feasibility.**

Its two value engines are **scalability** (handling volume people can't: hundreds of drafts, a thousand summaries) and **automation** (taking over repetitive thinking work). Neither replaces expert judgement in high-stakes decisions. To choose where to start, plot candidates by business value against feasibility (data, complexity, change effort) and time to value.

**Think of a tireless first-draft team**: it gets you most of the way at scale, and your experts spend their time on the part that needs them.

![Value by feasibility matrix: Quick Wins do first, Strategic Bets plan for later, Incremental Gains do if capacity, Avoid don't do](/content/skillup/ab731/images/ab731-d1-value-feasibility-matrix.svg)

### Real use

A manufacturer has three ideas: AI marketing slogans (easy, low impact), equipment-failure prediction (high impact, achievable data) and a full digital twin (high impact, years of data work). It funds failure prediction first, plans the digital twin as a strategic bet, and parks the slogans.

### How it works

- **Sweet spot**: frequent, language-heavy, cheap for a human to check: summarising, drafting, extraction, common Q&A.
- **Poor fit**: tasks needing 100% accuracy (payroll), real-time safety control, unreviewed medical or legal decisions.
- **Quadrants**: Quick Wins (do first), Strategic Bets (plan), Incremental Gains (if capacity), Avoid.
- **KPIs**: adoption rate, time saved, error reduction, cost per task, user satisfaction.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Quick Win | High value and high feasibility | Rarely the most exciting idea |
| Strategic Bet | High value, hard to deliver | Long time to value; plan enabling work |
| Rules-based software | Output must be exactly right every time | No language flexibility |

### How to do it

1. List candidates with their value, feasibility blockers and time to a measurable result.
2. Fund Quick Wins first; put Strategic Bets on a roadmap with their enabling work.
3. Define outcome KPIs before the pilot starts.

### Exam Trap ⚠️

<div class="note-trap">Two absolute distractors: "the highest long-term value always goes first" (that's a Strategic Bet) and "the fastest to implement always goes first" (that's an Incremental Gain). The answer is high value and high feasibility. Measure success with outcome KPIs, not the number of features deployed.</div>

### Go deeper

- [Create business value from AI](https://learn.microsoft.com/en-us/training/modules/create-business-value/)

---

## 1.7 Describe the impact of prompt engineering

### Key Concept

**A better prompt improves output without changing the model, so it's the cheapest, fastest fix and always comes first.**

The model fills in whatever the prompt leaves unspecified. A vague prompt gets a generic answer; a prompt with a goal, context, audience, format and an example narrows the model toward what you want. Because nothing about the model changes, it costs nothing extra and works immediately.

**Think of briefing a contractor**: a clear brief with examples gets the right job first time; a one-line brief gets their guess.

![A vague prompt produces a generic draft, while a prompt with goal, context, audience, format and an example produces an on-brand draft; only facts the model never saw need grounding instead.](/content/skillup/ab731/images/ab731-1-7-prompt-impact.svg)

### Real use

A marketing team says Copilot "doesn't get our brand" and asks for a fine-tuning project. Nobody had put the brand guidelines or a sample paragraph into the prompt. Adding both gets on-brand drafts the same afternoon, at no extra cost.

### How it works

- Prompt quality decides output quality more than most leaders expect, which makes prompting a skill to train, not just typing.
- It fixes vague, generic or wrongly formatted output.
- It can't supply facts the model never saw: that's a grounding problem (1.9).
- It can't make a persistent, specialised style stick at volume: that may be fine-tuning (1.3).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Improve the prompt | Output is generic, inconsistent or badly formatted | Each user must learn to prompt well |
| Ground the model | Answers need private or current facts | Needs a retrieval source |
| Fine-tune | Style gap persists after good prompting | Cost, time and maintenance |

### How to do it

1. Check the prompt states the goal, context, audience, format and constraints.
2. Add one or two examples of good output.
3. Only escalate to grounding or fine-tuning once the prompt has been fixed and measured.

### Exam Trap ⚠️

<div class="note-trap">"Output is generic or inconsistent. What first?" Improve the prompt, not fine-tune, not switch tools. But for wrong facts caused by a knowledge gap, "write better prompts" alone isn't enough: that needs grounding.</div>

### Go deeper

- [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering)

---

## 1.8 Understand techniques of prompt engineering

### Key Concept

**Each prompting technique fixes a different gap: examples for format, steps for reasoning, a role for voice, a system prompt for rules.**

Prompt engineering is a small toolkit, and knowing which tool fits the problem is what the exam tests. Zero-shot asks directly. Few-shot shows two to five examples first. Chain-of-thought asks the model to reason step by step. Role prompting gives it a persona. A system prompt sets persistent rules that apply to every turn.

**Think of a toolbox, not a magic phrase**: you pick the tool for the job in front of you.

![Five prompting techniques and the gap each fixes: zero-shot for simple clear tasks, few-shot for a format or style, chain-of-thought for multi-step reasoning, role prompting for voice and expertise, and a system prompt for rules on every turn.](/content/skillup/ab731/images/ab731-1-8-prompt-techniques.svg)

### Real use

An HR team wants job adverts in a house format. Zero-shot gives a different layout each time; showing two past adverts (few-shot) fixes the format. Their policy assistant gets a system prompt: "Answer only from the attached policies, cite the section, and say so when the policy doesn't cover it."

### How it works

- **Zero-shot**: "Summarise this contract in 3 bullets." Fine for clear, common tasks.
- **Few-shot**: two sample summaries, then "now this one". Fixes format and style.
- **Chain-of-thought**: "Work through it step by step." Helps multi-step reasoning.
- **Role**: "You are a senior legal counsel…" Sets voice and expertise.
- **System prompt**: persistent rules and context, set once by whoever builds the solution.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Few-shot | Output must match a format or style | Longer prompts cost more tokens |
| Chain-of-thought | The task needs reasoning across steps | Longer, slower responses |
| System prompt | Rules must hold for every user and turn | Set by the builder, not each user |

### How to do it

1. Name the gap: format, reasoning, voice or rules.
2. Apply the matching technique, starting with the cheapest.
3. Keep good prompts in a shared library so teams reuse them.

### Exam Trap ⚠️

<div class="note-trap">Don't swap the techniques. Examples before the task are few-shot, not chain-of-thought. A rule that must apply to every turn belongs in the system prompt, not repeated by each user. No technique adds facts the model never saw.</div>

### Go deeper

- [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering)

---

## 1.9 Identify business requirements for grounding solutions

### Key Concept

**Ground a solution when its answers must be current, specific to your organisation and checkable against a source.**

A pretrained model has a knowledge cutoff and has never seen your private data. Grounding connects its answers to authoritative, verified sources at query time, so it answers from them instead of from memory. The business requirement behind grounding is trust: the answer must be right for this organisation today, and a user must be able to verify it.

**Think of grounding as handing an advisor today's file**: without it, they answer from what they remember about companies in general.

![Four business requirements, answers must be current, organisation-specific, verifiable with a citation, and limited to what the user may see, all point to grounding on an authoritative source.](/content/skillup/ab731/images/ab731-1-9-grounding-requirements.svg)

### Real use

An HR assistant without grounding confidently describes a "typical" leave policy that isn't the company's. Grounded on the current policy library, it quotes the company's real rule and links to the section, and when HR updates the policy the answers change the same day.

### How it works

- **Current**: facts change weekly or monthly, faster than any model is retrained.
- **Organisation-specific**: the answer lives in your documents, not on the public web.
- **Verifiable**: compliance or users need a citation to the source.
- **Permission-aware**: users should only see answers from content they're allowed to see.
- First identify the authoritative source, then build retrieval on it (1.10).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Ground the solution | Any of current, private, verifiable is required | Source must be kept clean and owned |
| No grounding | General tasks: rewriting, brainstorming | Retrieval would only add cost |
| Fine-tune instead | Never for changing facts | Stale facts, no citations |

### How to do it

1. Ask: must the answer reflect our own current documents, and must a user be able to verify it?
2. Name the single authoritative source and its owner.
3. Check the source's permissions and quality before connecting it (1.11).

### Exam Trap ⚠️

<div class="note-trap">"Put all the documentation in the system prompt" hits context-window and cost limits, and "use a bigger model that has probably seen similar documents" still lacks your private, current data. When answers depend on your own changing content, the requirement is grounding.</div>

### Go deeper

- [Retrieval-augmented generation in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

---

## 1.10 Understand how retrieval-augmented generation (RAG) is used for AI solutions

### Key Concept

**RAG retrieves the relevant chunks of your data, adds them to the prompt, and has the model answer from them.**

RAG is the standard way to ground a model. Your content is split into chunks and indexed. At query time the system finds the most relevant chunks, adds them to the prompt as context, and the model generates an answer from that context, with references back to the source. Nothing in the model is retrained, so updating the documents updates the answers.

**Think of RAG as an open-book exam**: the book is always current and you can cite the page; fine-tuning is months of study that goes stale.

![RAG sequence: the user asks for Q3 sales, the AI model retrieves relevant chunks from your data, gets $4.2M back from the report, and answers with a grounded reply](/content/skillup/ab731/images/ab731-d1-rag-sequence.svg)

### Real use

Support documentation changes weekly. A RAG solution indexes it in Azure AI Search; when a customer asks about a return, the assistant retrieves the current returns section and answers with a link to it. When the policy changes, re-indexing is all it takes.

### How it works

- **Index**: documents are chunked and indexed, often as vectors for semantic search.
- **Retrieve**: the query finds the most relevant chunks, filtered by the user's permissions where needed.
- **Augment**: those chunks go into the prompt as context.
- **Generate**: the model answers from the context and cites it.
- Benefits: fewer fabrications, current answers, citations, no retraining. Microsoft 365 Copilot grounds on Microsoft Graph the same way (2.6).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| RAG | Facts are private, current or need citations | Retrieval quality limits answer quality |
| Fine-tuning | A behaviour gap, not a knowledge gap | No citations; retrain to update |
| Long prompt with all docs | A handful of short, fixed documents | Cost and context-window limits |

### How to do it

1. Index the authoritative content with a retrieval service such as Azure AI Search.
2. Retrieve the top relevant chunks per question and pass them to the model.
3. Instruct the model to answer only from them and cite the source.

### Exam Trap ⚠️

<div class="note-trap">RAG is the first answer to "how do we use our own, changing data with AI?". Fine-tuning is for style and vocabulary, not for injecting facts. Distractors also suggest retraining whenever documents change; with RAG you just update the index.</div>

### Go deeper

- [Retrieval-augmented generation in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

---

## 1.11 Understand the impact of data on AI solutions, including data type, data quality, and representative datasets

### Key Concept

**AI amplifies whatever is in its data, errors included, so data problems are fixed upstream, not with prompts or bigger models.**

A model can't tell that a duplicate record is wrong or a figure was mistyped; it treats every input as equally trustworthy. Data type decides which model can use it, quality decides whether answers are right, representativeness decides who the solution works for, and recency decides whether insights are current.

**Think of AI as a megaphone, not a filter**: it makes whatever you feed it louder.

![Four data factors flow into an AI solution: data type must match the model, quality errors propagate into answers, unrepresentative data fails missing groups, and stale data gives outdated insights.](/content/skillup/ab731/images/ab731-1-11-data-factors.svg)

### Real use

A sales assistant grounded on three conflicting copies of the price list quotes a different price depending on which copy it retrieves, and users blame "the AI". Consolidating one owned, current price list in a unified data layer (such as Microsoft Fabric) fixes it; a better model wouldn't.

### How it works

- **Data type**: text, images, tables and audio each need a model that handles that type.
- **Data quality**: errors, duplicates and inconsistencies flow straight into output.
- **Representative datasets**: if training data under-represents a group or language, the model performs worse for it.
- **Recency**: stale data gives outdated answers.
- Unify siloed data (CRM, ERP, HR) into one governed source before AI builds on it.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Fix the data first | Answers are wrong, inconsistent or fail one group | Slower start; often a data project |
| Unify sources | Answers depend on several systems that disagree | Bigger programme |
| Accept imperfect data | Exploratory brainstorming, no facts claimed | Not for anything trusted |

### How to do it

1. Identify the data each use case depends on and its owner.
2. Check it for duplicates, conflicts, gaps across user groups and age.
3. Fix it at the source before connecting AI to it.

### Exam Trap ⚠️

<div class="note-trap">"Switch to a more capable model" is the distractor when answers are wrong because data is duplicated, stale or unrepresentative. The exam blames the data before the model. Poor results for one group of users points to a representativeness problem.</div>

### Go deeper

- [What is Microsoft Fabric?](https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview)

---

## 1.12 Describe the importance of secure AI

### Key Concept

**AI connected to data and actions turns one weakness into exposure at scale, and one leak can stop an AI programme.**

A model can't reliably tell instructions apart from the data it reads, because both arrive as tokens. Connect it to company data and the ability to act, and a single manipulated input or over-permissioned connection is reused across every query: it can leak customer data, reveal internal instructions or trigger actions nobody approved. Adoption depends on trust, and a security failure destroys it fastest.

**Think of a letter that says "the bearer may open the vault"**: a careless clerk follows whatever the paper says.

![What the AI can reach multiplies the impact of one weakness: a model alone has limited exposure, a model reading untrusted content can be manipulated, and a model with data and actions can leak data or act at scale.](/content/skillup/ab731/images/ab731-1-12-secure-ai.svg)

### Real use

A support bot that follows instructions found inside ticket text reveals its system prompt and internal discount codes to the first attacker who writes "ignore all previous instructions". The fix is design, not luck: treat ticket text as data, limit what the bot can reach, and filter inputs.

### How it works

- **Attack surface grows with reach**: untrusted content read, data reachable, actions allowed.
- **Scale**: one weakness applies to every query, not one file.
- **Trust**: a visible leak halts adoption and invites regulatory attention.
- **Built in, not bolted on**: Microsoft 365 Copilot respects existing permissions, and Microsoft Foundry adds content filters and Prompt Shields for custom builds.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full threat model | AI reads untrusted content, reaches sensitive data or takes actions | Time before launch |
| Standard app controls | Tool only rewrites text a user pastes in | Revisit if it gains data or actions |
| Pause the launch | Nobody can say what the AI can reach | Delay, but avoids a public incident |

### How to do it

1. Ask: what untrusted content does it read, what data can it reach, what can it do?
2. Give it the least access the use case needs.
3. Add input filtering, authentication and monitoring before go-live (1.15).

### Exam Trap ⚠️

<div class="note-trap">"Secure AI is IT's job after launch" is wrong: security is a business condition of trust and adoption, designed in from the start. And "Copilot respects permissions" doesn't make a custom AI app secure; each solution needs its own controls.</div>

### Go deeper

- [Security for AI](https://learn.microsoft.com/en-us/security/security-for-ai/)

---

## 1.13 Identify scenarios when machine learning adds value

### Key Concept

**Traditional ML earns its place when you need a stable, repeatable prediction from structured history.**

When the task is to classify, score or forecast from structured, historical data, a trained ML model is usually cheaper, faster and more consistent than a language model, because it's built for exactly one fixed output. Fraud scoring, demand forecasting, churn prediction, lead scoring and anomaly detection in sensor data are the classic cases.

**Think of a doctor reading an X-ray**: pattern recognition on known kinds of data, done the same way every time.

![Four structured-data needs that suit traditional ML: score fraud risk per transaction, forecast demand, predict churn or delay, and detect anomalies in sensor readings.](/content/skillup/ab731/images/ab731-1-13-ml-fit.svg)

### Real use

A logistics company wants to know which shipments will be late, based on weather, carrier performance and history. A predictive model trained on past shipments outputs a delay probability for each one; dispatchers act on the highest risks first.

### How it works

- **Needs a fixed output**: a label, a score or a number.
- **Needs history**: enough labelled or measured examples to learn from.
- **Repeats at volume**: thousands of identical decisions where consistency matters.
- **Needs upkeep**: the model must be monitored and retrained as the world changes (1.14).
- Combine both when needed: ML scores the claim, generative AI drafts the letter.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Traditional ML | Structured history, fixed output, high volume | Needs data science and upkeep |
| Generative AI | Output is language or new content | Higher cost per item, varies |
| Rules | Logic is fixed and known in advance | Breaks on new patterns |

### How to do it

1. Confirm the output is a label, score or number.
2. Check there is enough representative history to train on.
3. Plan monitoring and retraining before approving the build.

### Exam Trap ⚠️

<div class="note-trap">A scenario says "predict which shipments will be delayed" and an option offers generative AI to "write a forecast". Predicting a number or probability from history is ML. Also, ML is not "legacy": it is often the cheaper, more reliable choice.</div>

### Go deeper

- [What is Azure Machine Learning?](https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning)

---

## 1.14 Describe the lifecycle of a machine learning solution

### Key Concept

**An ML model is never done: deployment starts a monitor-and-retrain loop that lasts as long as the model is live.**

The lifecycle is a loop: define the problem and success metric, collect and prepare data, train, validate on unseen data, deploy, monitor, and retrain. Once live, the world keeps moving: customer behaviour shifts and fraud tactics evolve, so accuracy falls even though nothing in the model changed. That's **concept drift**.

**Think of a weather model**: trained on past patterns, useless if it never gets new readings.

![The machine learning lifecycle as a loop: define the problem, prepare data, train, validate, deploy, monitor, then retrain and return to training when performance drifts.](/content/skillup/ab731/images/ab731-1-14-ml-lifecycle.svg)

### Real use

A bank's fraud model caught over 90% of fraud at launch. Fourteen months later it catches far less, because criminals changed tactics and nobody retrained it. Monitoring with an accuracy threshold would have triggered a retrain months earlier.

### How it works

1. **Problem definition**: the business question and the success metric.
2. **Data collection and preparation**: representative, clean, split into train, validation and test sets.
3. **Training**: the algorithm learns patterns.
4. **Validation**: precision, recall and accuracy on unseen data, to prove it generalises.
5. **Deployment**: it scores live inputs.
6. **Monitoring**: accuracy, drift and latency in production.
7. **Retraining**: refresh with new data, then back to validation.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Continuous monitoring | Patterns shift (fraud, demand, behaviour) | Ongoing cost and ownership |
| Scheduled retraining | Slow, predictable change | Can miss sudden drift |
| Light periodic checks | Truly stable patterns (fixed-format forms) | Still needs an owner |

### How to do it

1. Agree the success metric before touching data.
2. Name who watches live accuracy, against what threshold.
3. Budget retraining as a permanent cost, not a project phase.

### Exam Trap ⚠️

<div class="note-trap">Deployment is not the finish line. If a model was "deployed and left alone" while performance declines, the answer is the missing monitoring and retraining loop (concept drift), not a data-collection or deployment problem.</div>

### Go deeper

- [Monitor model performance in production](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-model-performance)

---

## 1.15 Identify security considerations for AI systems, including application security, data security, and authentication requirements

### Key Concept

**Secure an AI system in three layers: treat input as untrusted, scope the data per user, and authenticate before anything is retrieved.**

Each AI threat has a signature and a matching control. **Prompt injection** hides instructions in content the model reads. **Data poisoning** corrupts training or fine-tuning data. **Model extraction** probes a public model with huge volumes of varied queries to copy it. **Sensitive data leakage** reveals one user's or customer's data to another.

**Think of a bank branch**: check the paperwork, keep each customer's box separate, and check ID at the door.

![Four AI threats matched to controls: prompt injection to input filtering and treating content as data, data poisoning to validated training sources, model extraction to rate limits and anomaly detection, and data leakage to authentication and per-user data scoping.](/content/skillup/ab731/images/ab731-1-15-security-controls.svg)

### Real use

A fintech exposes a credit-scoring model through a public API. One key sends tens of thousands of systematically varied queries: model extraction. Rate limiting, anomaly alerts and coarser outputs (a band instead of an exact score) cut it off.

### How it works

- **Application security**: validate and filter input; never pass raw input to a model with full privileges; Prompt Shields detect injection attempts.
- **Data security**: expose only the data a use case needs; isolate each customer's data.
- **Authentication**: users sign in (Microsoft Entra ID) before AI reaches org data, and retrieval runs as that user.
- **Lifecycle**: poisoning attacks training data before learning; extraction attacks the deployed model afterwards.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Input filtering + least privilege | AI reads untrusted content | Some legitimate input flagged |
| Per-user authentication and scoping | AI reaches personal or customer data | Integration work |
| Rate limits + monitoring | A model is exposed publicly | Can slow heavy legitimate users |

### How to do it

1. Map each threat to the solution: what it reads, reaches, exposes and learns from.
2. Apply the matching control from the list above.
3. Monitor endpoints and audit data sources after go-live.

### Exam Trap ⚠️

<div class="note-trap">Match the threat to its signature. Instructions hidden in input: prompt injection. Tainted data flowing into training over weeks: data poisoning. Huge volumes of varied queries from one key: model extraction. One customer seeing another's data: missing authentication and data isolation.</div>

### Go deeper

- [Prompt Shields in Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)

---

## Deep Dive: Making Business Value of Generative AI Click

### 1. The connective narrative

Every lesson in this domain answers one of three questions a leader asks before funding AI: *what kind of AI is this, what will it cost, and what could go wrong?* Lessons 1.1, 1.2, 1.13 and 1.14 answer the first: generative AI creates, traditional ML classifies and predicts, agents act on goals, and ML needs lifelong upkeep. Lessons 1.3, 1.4 and 1.6 to 1.10 answer the second: prompting, grounding and fine-tuning are the same question from different angles (how do we get useful output without paying for customisation we don't need?), and tokens set the bill.

Lessons 1.5, 1.11, 1.12 and 1.15 answer the third. Fabrication, bias, bad data and security gaps are the reasons a technically successful pilot fails to scale: nobody trusts the output, or an exposure surfaces too late. The thread through all of it is that the raw model confidently produces something plausible and wrong. The leader's job is to know which guardrail each use case needs.

### 2. Worked scenario

> **Scenario.** A regional insurer considers AI for two needs: flagging likely fraudulent claims, and drafting the plain-language letter sent after each claim decision.
>
> Fraud flagging outputs a score, so it's traditional ML (1.1, 1.13). The team trains on historical claims, validates on held-out data and, crucially, sets up monitoring, because fraud tactics drift (1.14).
>
> The letter is new text, so it's generative AI. It must quote each customer's policy terms, which are private and change, so the team grounds it with RAG rather than fine-tuning (1.9, 1.10). They estimate about 400 input and 250 output tokens per letter at 2,000 letters a month: a small cost next to staff time (1.4).
>
> Both pilots get a security review: authentication and per-customer data scoping, because both touch personal data (1.15). Only the letter gets human review before sending: a wrong fraud score goes to an investigator anyway, but a wrong letter goes straight to a customer (1.5).

### 3. Memory aid

**CRAWL**: the order to work through a use case.
- **C**lassify: generative AI, ML or an agent? (1.1, 1.2, 1.13)
- **R**isk: fabrication, bias, data, security (1.5, 1.11, 1.15)
- **A**nchor: is prompting enough, or does it need grounding? (1.7–1.10)
- **W**eigh: tokens and ROI (1.4)
- **L**aunch: where it sits on the value-feasibility matrix (1.6)

### 4. Exam strategy for this domain

D1's distractors are almost always a category swap: an answer that's true of the *other* AI type, the *other* customisation method or the *other* threat. The exam rewards the cheapest, lowest-risk lever that solves the stated problem: prompting before grounding before fine-tuning, and grounding rather than fine-tuning for facts. When two options sound plausible, pick the one that meets the business need at the lowest cost and risk, not the most sophisticated-sounding one.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| "Generate", "draft", "create" | Generative AI |
| "Classify", "detect", "predict a number" | Traditional ML |
| One prompted task in one session | Copilot |
| Goal across steps, systems or days, no prompt each step | AI agent |
| Fixed steps, runs unattended | Scripted automation, not an agent |
| Output generic or off-brand: cheapest fix? | Improve the prompt first |
| Private, current or cited facts | Grounding with RAG |
| Stable, distinctive style at volume | Fine-tuning |
| Bill rose, same users | More tokens per request |
| Wrong facts stated confidently | Fabrication: ground + human review |
| Same input, different output | Non-determinism (temperature) |
| Past discrimination / missing groups / inconsistent collection | Historical / representation / measurement bias |
| Fund first | High value AND high feasibility (Quick Win) |
| Model deployed and left alone, accuracy falling | Concept drift: monitor and retrain |
| Instructions hidden in input | Prompt injection |
| Tainted data in training over time | Data poisoning |
| Huge varied query volume from one key | Model extraction |
