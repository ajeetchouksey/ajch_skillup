# Domain 1: Business Value of Generative AI
**Exam Weight: 38% — Heaviest Domain (tied)**

---

## Overview

Domain 1 tests whether a business leader can tell what kind of AI a problem needs, what it will cost, and what could go wrong before any budget is committed. It covers generative AI versus traditional machine learning, model choices (pretrained, fine-tuned, grounded with RAG), token-based cost and ROI, the known failure modes (fabrication, unreliability, bias), prompt engineering, data quality, AI security, agents, and use-case prioritisation.

> **🧠 The Golden Rule - "Generative AI CREATES new content. Other AI CLASSIFIES or PREDICTS existing patterns."**

**The mental model:** Think of traditional ML as a **doctor reading an X-ray** — pattern recognition in known data. Generative AI is like a **ghost-writer** — it produces net-new content by learning patterns from training data.

<div class="note-scribble">The trick the exam uses: "Generate a summary" is generative AI. "Identify which emails are spam" is classification (traditional ML). Look for the word "generate," "create," "draft," or "compose" as the tell.</div>

> 💡 **Human Angle**: A CFO doesn't fund the AI that wins the demo — the same way nobody buys a sports car for a grocery run; Domain 1 consistently rewards the leader who asks the business question ("what does this save, and what could it get wrong?") before the technology question.

---

## 1.1 Generative AI vs Other AI Types

### Key Concept

**Pick the AI type by the output you need: new content means generative AI; a label or number means traditional ML.**

These categories differ in what the model is mathematically optimised to output, not just in the words used to describe them. A classifier learns a decision boundary and outputs a category, or a probability over a fixed set of labels. A generative model learns a probability distribution over sequences of tokens and produces a new sequence by sampling from it one token at a time.

That's why a generative model can write a paragraph nobody has written before, while a spam classifier can never output a new category — it was never trained to produce anything but "spam" or "not spam." **Think of it as a novelist versus a sorting office**: one writes new letters, the other only decides which pigeonhole each existing letter goes in.

| Type | What it does | Example |
|---|---|---|
| **Generative AI** | Creates new content (text, images, code, audio) | Drafting a proposal, generating code, creating images |
| **Discriminative / Classification** | Puts inputs into categories | Spam detection, sentiment analysis, fraud flag |
| **Predictive / Regression** | Forecasts a numeric outcome | Sales forecasting, demand prediction |
| **Recommendation** | Surfaces relevant items | "Users like you also bought..." |

![Input data branches to four AI types: generative AI to generate new content, discriminative ML to classify, regression ML to predict a number, and recommendation to surface relevant items](/content/skillup/ab731/images/ab731-d1-ai-type-selection.svg)

**When traditional machine learning adds value:** when the task is to classify, score or forecast from structured, historical data — flagging fraudulent transactions, predicting demand or delivery delays, scoring leads, detecting anomalies in sensor readings. A trained ML model is usually cheaper, faster and more consistent than an LLM for these, because it is built for exactly one fixed output.

<mark>Exam shortcut: The word "generate", "draft", "compose", or "create" always points to generative AI.</mark>

### In Practice

**What breaks without this**: an LLM gets used to route 10,000 emails a day into three fixed categories, at many times the per-item cost of a trained classifier and with run-to-run variation a classifier wouldn't have. The opposite mistake is just as real: a classifier can't draft the reply, however good its accuracy.

**Decision trigger**: ask, "is the output a fixed label or a number, or is it new text, images or code?" A fixed label or number points to traditional ML; anything net-new points to generative AI.

**When you'd choose differently**: when there are no labelled training examples and the categories keep changing, an LLM with a clear prompt (zero- or few-shot classification) can be the pragmatic first step. You buy speed to launch at a higher cost per item, and you can switch to a trained classifier once labelled data builds up.

### Exam Trap ⚠️

<div class="note-trap">
Common distractor: "use generative AI to categorise each item" for a pure classification task. It would work, but it is overkill: more expensive and less consistent than a classifier trained on labelled examples. The exam rewards matching the AI type to the output. A label or a number means ML; new content means generative AI.
</div>

---

## 1.1b The Lifecycle of a Machine Learning Solution

### Key Concept

**An ML model is never "done": deployment starts a monitor-and-retrain loop that lasts as long as the model is live.**

Choosing traditional ML (§1.1) is only the first decision. The model then has to be built, shipped and kept accurate, and that's a repeating cycle, not a one-off project. Every stage exists to stop a specific failure: a vague success metric, unrepresentative data, a model that memorises instead of generalising, or one that quietly stops matching the real world.

Once a model is live, the world keeps moving. Customer behaviour shifts, fraud tactics evolve and markets change, so a model's accuracy degrades even though nothing in it changed — this is **concept drift**. **Think of an ML model like a weather forecaster's model of the atmosphere**: trained on historical patterns, but useless if it's never updated with new readings.

| Stage | What happens |
|---|---|
| **1. Problem definition** | Define the business question the model must answer (e.g., "is this transaction fraudulent?") and agree the success metric before touching any data |
| **2. Data collection & preparation** | Gather relevant, representative data; clean, label, and split it into training / validation / test sets |
| **3. Training** | The algorithm learns patterns from the training data, adjusting its internal parameters to minimise error |
| **4. Validation & evaluation** | Test the model against data it hasn't seen, using metrics (accuracy, precision, recall) to confirm it generalises rather than memorises |
| **5. Deployment** | Release the model into production so it can score real, live inputs |
| **6. Monitoring** | Track live performance — accuracy, drift, latency — because production data shifts over time |
| **7. Retraining** | Refresh the model with new data when performance degrades, then loop back into training/validation |

<div class="note-scribble">The lifecycle is a loop, not a line: problem → data → train → validate → deploy → monitor → retrain → back to train. ML earns its place where a stable, repeatable prediction over structured data (fraud scoring, demand forecasting, churn prediction) is worth this ongoing upkeep.</div>

### In Practice

**What breaks without this**: a fraud model that caught most fraud at launch quietly lets more through every month as criminals change tactics. Nobody notices until losses show up in the finance report, because nobody owned monitoring.

**Decision trigger**: ask, "who watches this model's live accuracy, against what threshold, and what triggers a retrain?" If nobody can answer, the project plan stops at deployment, and it shouldn't.

**When you'd choose differently**: a model scoring a truly stable pattern (for example, classifying fixed-format internal forms) can be retrained on a slow schedule instead of under continuous watch. You still monitor it, just less often.

### Exam Trap ⚠️

<div class="note-trap">
Candidates assume "deployment" is the finish line. It isn't. Monitoring and retraining are permanent, ongoing stages of the lifecycle, not optional cleanup. If a scenario describes a model that was "deployed and left alone" while performance declines, the correct answer is the missing monitoring/retraining loop (concept drift) — not a data-collection or deployment problem.
</div>

---

## 1.2 Pretrained vs Fine-tuned Models

### Key Concept

**Start with a pretrained model and good prompts; fine-tune only when prompting and grounding can't close the gap.**

A **pretrained model** is trained on massive general datasets (the internet, books, code) and is ready to use out of the box. A **fine-tuned model** is a pretrained model given extra training on a smaller, domain-specific dataset to specialise it. Fine-tuning changes the model's weights, so it costs labelled data, training spend and time.

Fine-tuning changes how the model behaves (style, tone, specialised vocabulary). It is a poor way to give the model facts that change. **Think of a pretrained model as hiring a Harvard MBA generalist**: fine-tuning is sending them to a 3-month specialised bootcamp. Both are useful, but the bootcamp costs money and time, so first try simply telling the generalist what they need to know (prompting).

| | Pretrained | Fine-tuned |
|---|---|---|
| **Cost** | Lower | Higher (training cost) |
| **Setup time** | Immediate | Weeks to months |
| **Best for** | General tasks | Specialised domain (legal, medical, brand voice) |
| **Requires** | Prompt engineering | Labelled training data |

### In Practice

**What breaks without this**: a team spends weeks and a training budget fine-tuning on internal documents, then finds that the answers go stale the moment the documents change, and the model still can't cite where an answer came from.

**Decision trigger**: ask, "have we tried a well-structured prompt with examples, and grounding on our data, and measured where they fall short?" If not, it's too early to fine-tune.

**When you'd choose differently**: a stable, distinctive writing style or a specialised vocabulary that the base model keeps getting wrong, used at enough volume to justify the training cost, is a legitimate case for fine-tuning.

### Exam Trap ⚠️

<div class="note-trap">
Fine-tuning is NOT the first thing you reach for. The exam tests whether you know to try prompt engineering + RAG FIRST before spending money on fine-tuning. Fine-tune only when the domain vocabulary or style is so specialised that a base model cannot learn it from context.
</div>

---

## 1.2b RAG vs Fine-tune Decision Framework

### Key Concept

**RAG gives the model facts at runtime; fine-tuning changes how it writes. Choose by what the problem needs.**

When a scenario asks *"how should the business customise AI?"*, the deciding question is whether the gap is knowledge or behaviour. Knowledge gaps (current, private or frequently changing facts) are closed by retrieving the right content at query time. Behaviour gaps (a different writing style, or domain vocabulary the model can't pick up from context) are closed by changing the weights.

RAG also returns source references, which fine-tuning can't do: once a fact is baked into weights, there's no document to point to. **Think of RAG as an open-book exam and fine-tuning as months of study**: the open book is always current and lets you cite the page; the study changes how you think but goes stale.

| Question | If YES → | If NO → |
|---|---|---|
| Is the business problem about accessing current/private data? | **RAG** — ground the model in your documents | Continue to next question |
| Does the model need a completely different writing style or domain vocabulary? | **Fine-tuning** — adjust model weights | Use prompt engineering first |
| Is the cost of fine-tuning justified by the expected volume? | **Fine-tuning** | **RAG** — cheaper and more flexible |
| Does the output require verifiable citations? | **RAG** — returns source references | Fine-tuning has no source traceability |

<div class="note-important"><strong>Exam rule:</strong> RAG is ALWAYS the right first answer for "how do we use our company's own data with AI?" — fine-tuning is for vocabulary and style, not for injecting facts.</div>

### In Practice

**What breaks without this**: product documentation that changes weekly gets fine-tuned into a model monthly. Users get last month's answers, and every update means another training run.

**Decision trigger**: ask, "if the source document changed tomorrow, would the answer need to change tomorrow?" If yes, use RAG.

**When you'd choose differently**: a brand voice described by a style guide that changes every two years, used for high-volume copy with no citation requirement, is a style problem. Fine-tuning is defensible there even though a document exists.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "a document exists, so it must be RAG." Walk the framework instead. If the document describes how to write (style, voice) rather than facts to retrieve, and it rarely changes, fine-tuning can win. If the facts change or citations are needed, RAG wins.
</div>

---

## 1.3 Cost Drivers: Tokens & ROI

### Key Concept

**Generative AI cost scales with tokens in and out; ROI is the value created divided by that cost.**

A token is the basic unit of text an LLM processes, roughly ¾ of a word or about 4 characters. You pay for tokens IN (the prompt, including any retrieved documents) and tokens OUT (the response). Longer prompts and longer responses both cost more. The **context window** is the most prompt-plus-response tokens a model can handle in one request; content beyond it gets truncated or dropped.

Tokens exist because a model can't process raw text directly. It converts words and word-fragments into numeric IDs it can run matrix maths on, and that compute scales with the number of tokens. So a 10-page contract costs more to summarise than a one-paragraph email, even with the same instruction. **Think of tokens as a taxi meter**: it runs on every word you send and every word you get back.

| Cost lever | How to optimise |
|---|---|
| Prompt length | Be concise; avoid repeating context unnecessarily |
| Response length | Ask for summaries, not exhaustive responses |
| Model size | Use smaller models for simple tasks, large models for complex reasoning |
| Cache/reuse | Reuse common system prompt context where possible |

**ROI considerations:** For a business leader, ROI = (Value saved / generated) ÷ Cost of AI usage

<div class="note-important"><strong>Three ROI lenses:</strong><br/>1. <strong>Time savings</strong> — hours saved on repetitive tasks × hourly rate<br/>2. <strong>Quality lift</strong> — fewer errors, higher output quality<br/>3. <strong>Scalability</strong> — same headcount, more output (AI doesn't get tired)</div>

📎 See D3 §3.7 (Copilot Licence Types) and §3.8 (Foundry Tools Subscription Models) for the cost/licensing models behind these ROI numbers.

### In Practice

**What breaks without this**: a solution that stuffs whole documents into every prompt costs several times its forecast. Monthly spend rises with no change in user numbers, because the cost per request grew, not the number of requests.

**Decision trigger**: ask, "what is the average input and output token count per request, times the monthly request volume?" That figure, priced against the model you chose, is the operating cost to set against the time-savings value.

**When you'd choose differently**: if a wrong answer costs far more than the tokens (regulatory review, legal analysis), optimise for accuracy, not token spend. The cheapest model per token can be the most expensive choice overall.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "cost is driven by the number of users who log in." For metered generative AI, the primary cost unit is tokens (input AND output). ROI distractors also include irrelevant factors (dashboard colours, how impressive the demo looked). Real ROI levers are time saved, quality, scalability and the AI's own running cost.
</div>

---

## 1.4 Challenges of Generative AI

### Key Concept

**Generative AI can be fluent and wrong at the same time: fabrication, unreliability and bias are built into how it works.**

LLMs predict the next likely token. They have no built-in fact-checker, are tuned for text that reads well rather than text that is true, and inherit whatever patterns sit in their training data. So the three challenges below aren't rare bugs. They are standing risks every use case has to plan for.

The mitigations are structural rather than cosmetic: ground the model in verified sources, keep a human in the loop where the stakes are high, and evaluate outputs across user groups. **Think of a brilliant new hire who never says "I don't know"**: valuable, but you check their work in proportion to what's at stake.

#### Fabrications (Hallucinations)
The model confidently generates plausible-sounding but **factually incorrect** content.

**Why it happens:** LLMs predict the next likely token — they don't have a fact-checker. They optimise for coherent text, not factual accuracy.

**Mitigation:** Grounding (RAG), retrieval from verified sources, human-in-the-loop review for high-stakes outputs.

<div class="note-scribble">The exam loves the word "hallucination" vs "fabrication." Microsoft documentation uses "fabrication." Same thing.</div>

#### Reliability
AI outputs can vary for the same input (temperature/randomness) and may degrade on edge cases. Not guaranteed deterministic.

This variance comes from **temperature**, the setting that controls how much randomness the model adds when it picks the next token. Temperature 0 makes output deterministic (same input, same output); higher values sample less-likely tokens for more varied phrasing. Most production deployments use a low, non-zero temperature: enough variety to avoid sounding robotic, not so much that the same question gets materially different answers.

#### Bias
Training data reflects real-world human biases. If the training data over-represents certain demographics, viewpoints, or languages, the model will too.

**Types to know:**
- **Historical bias** — past data encodes past discrimination (e.g., hiring data that favoured one group)
- **Representation bias** — some groups under-represented in training data
- **Measurement bias** — data collected inconsistently across groups

![Bias flows from training data through the model into biased outputs and business, legal and ethical risk; mitigation through diverse data, RLHF and evaluation acts on the data and the model](/content/skillup/ab731/images/ab731-d1-bias-chain.svg)

### In Practice

**What breaks without this**: a discharge-summary assistant states a wrong dosage with full confidence, or a hiring model trained on ten years of history ranks one group lower. Either way the harm reaches people before anyone notices, because the output looked right.

**Decision trigger**: ask, "what happens if this output is wrong, and who would catch it?" The higher the consequence, the more grounding, human review and group-by-group evaluation the use case needs.

**When you'd choose differently**: for low-stakes creative work (brainstorming slogans, first-draft social posts), variation is a feature and heavy review is wasted effort. A light editorial pass is enough.

### Exam Trap ⚠️

<div class="note-trap">
Two look-alike traps. (1) "Use a larger model" does not fix fabrication — larger models still hallucinate; grounding plus human review does. (2) Different outputs for the same input is non-determinism (reliability/temperature), not hallucination or bias. Also match bias type to cause: past discrimination = historical, missing groups or languages = representation, inconsistent collection = measurement.
</div>

---

## 1.5 When Generative AI Adds Business Value

### Key Concept

**Generative AI pays off on high-volume, language-heavy, repeatable work, not on high-stakes decisions that need 100% accuracy.**

Its two value engines are **scalability** and **automation**. Scalability means handling volume people can't: a person might write 5 personalised emails an hour, while Copilot can draft hundreds, and the same goes for summarising 1,000 support tickets or translating documents into 10 languages. Automation means taking over repetitive thinking work that used to need human time.

The value comes from multiplying human capacity, not replacing expert judgement. **Think of it as a tireless first-draft team**: it gets you most of the way at scale, and your experts spend their time on the part that needs them.

AI can take over **repetitive cognitive tasks** that previously required human time:
- First-draft generation (proposals, reports, emails)
- Summarisation (meeting notes, research papers)
- Code assistance (boilerplate, unit tests)
- Data extraction (pulling structured data from unstructured text)

<div class="note-important"><strong>High-value scenarios for the exam:</strong><br/>✅ Summarising large documents<br/>✅ Drafting communications at scale<br/>✅ Accelerating code review<br/>✅ Answering common employee/customer questions<br/>✅ Extracting insights from data<br/><br/>❌ Low-value / risky scenarios:<br/>❌ High-stakes medical / legal decisions without human review<br/>❌ Real-time safety-critical systems<br/>❌ Tasks requiring 100% accuracy (payroll calculations)</div>

### In Practice

**What breaks without this**: a pilot aimed at a low-volume, judgement-heavy task saves a few hours a month, can't show ROI, and sours leadership on AI, while a high-volume drafting task elsewhere goes untouched.

**Decision trigger**: ask, "how often does this task happen, how much of it is reading or writing language, and can a human cheaply check the result?" Frequent, language-heavy and easy to check is the sweet spot.

**When you'd choose differently**: a deterministic calculation (payroll, tax) needs rules-based software, not a probabilistic model, however often it runs.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: placing generative AI where 100% accuracy or real-time safety is required (payroll calculations, safety-critical control, unreviewed medical or legal decisions). The exam rewards high-volume drafting, summarising, extraction and Q&A, with human review where the stakes are high.
</div>

---

## 1.6 Prompt Engineering

### Key Concept

**Prompt engineering improves output without changing the model, so it's the cheapest and fastest fix to try first.**

Prompt engineering means **crafting the input to get the output you need**. The model fills in whatever the prompt leaves unspecified. A vague prompt gets a generic answer, while a prompt with context, constraints, a role and examples narrows the model toward what you actually want.

Because it changes nothing about the model, it costs nothing extra and takes effect immediately. That's why it always comes before RAG or fine-tuning. **Think of it like briefing a contractor**: a clear brief with examples gets you the right job first time, and a one-line brief gets you their guess.

| Technique | What it does | Example |
|---|---|---|
| **Zero-shot** | Ask directly, no examples | "Summarise this contract in 3 bullets" |
| **Few-shot** | Give 2-5 examples before the task | Show 2 sample summaries, then ask for a third |
| **Chain-of-thought** | Ask the model to reason step-by-step | "Think step by step before answering..." |
| **Role prompting** | Give the model a persona | "You are a senior legal counsel..." |
| **System prompt** | Set persistent context / rules | Instructions that apply to all turns |

<div class="note-important"><strong>Business impact:</strong> A well-engineered prompt can greatly improve output quality without any model changes or additional cost. This is why prompt engineering is a skill, not just typing.</div>

### In Practice

**What breaks without this**: a marketing team concludes Copilot "doesn't get our brand" and asks for a fine-tuning project, when nobody had put the brand guidelines or a sample paragraph into the prompt.

**Decision trigger**: ask, "does the prompt state the goal, the audience, the format, the constraints and an example?" If any is missing, fix the prompt before escalating to RAG or fine-tuning.

**When you'd choose differently**: if the gap is missing facts (private or current data), no prompt can supply what the model never saw. That's a grounding problem (§1.7). If it's a persistent, specialised style at high volume, it may be a fine-tuning problem (§1.2b).

### Exam Trap ⚠️

<div class="note-trap">
"A user is getting inconsistent or generic quality from Copilot. What should they do first?" → Improve the prompt (be more specific, add context and examples). NOT fine-tune the model, NOT switch tools. But for fabrication caused by knowledge gaps, "write better prompts" alone is insufficient — that needs grounding.
</div>

---

## 1.7 Grounding and RAG (Retrieval-Augmented Generation)

### Key Concept

**Grounding ties answers to your authoritative data at query time, so the model answers from sources instead of memory.**

A pretrained model's knowledge has a **cutoff date** and doesn't know about your organisation's private data. **Grounding** connects the model's responses to authoritative, verified data sources so it doesn't fabricate. RAG is the standard pattern: retrieve the relevant chunks from your data, add them to the prompt, then generate an answer from them.

The business requirement behind grounding is trust. Answers must be current, specific to the organisation, and checkable against a source. **Think of RAG as giving the model the answer book at runtime**: fine-tuning teaches skills during training, while RAG hands over the right page at the moment of the question.

![RAG sequence: the user asks for Q3 sales, the AI model retrieves relevant chunks from your data, gets $4.2M back from the report, and answers with a grounded reply](/content/skillup/ab731/images/ab731-d1-rag-sequence.svg)

**Benefits of grounding:**
- Reduces hallucinations dramatically
- Keeps answers current (no knowledge cutoff)
- Cites sources (verifiable)
- Doesn't require model retraining

<mark>RAG vs Fine-tuning: RAG = give the model the answer book at runtime. Fine-tuning = teach the model new skills during training. RAG is cheaper, faster, and updatable.</mark>

### In Practice

**What breaks without this**: an HR assistant answers from what it absorbed in general training, confidently describing a "typical" leave policy that isn't the company's, with no source to check against.

**Decision trigger**: ask, "must the answer reflect our own, current documents, and must a user be able to verify it?" If yes, ground it, and identify the authoritative source before you build.

**When you'd choose differently**: general-knowledge tasks (rewriting a paragraph, brainstorming) don't need retrieval. Adding RAG there only adds tokens, latency and an index to maintain.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "put all the documentation into the system prompt" or "use a bigger model that has probably seen similar documents." Stuffing everything into the prompt runs into context-window and cost limits; a bigger model still lacks your private, current data. Retrieval of the relevant chunks at runtime (RAG) is the answer.
</div>

---

## 1.8 Data Quality and AI Solutions

### Key Concept

**Garbage in, garbage out: AI amplifies whatever is in the data, so fix data upstream, not with prompts.**

A model has no independent way to know a duplicate record is wrong or a mistyped figure is inaccurate. It treats every input as equally trustworthy unless the data pipeline filters it first. Data type, quality, representativeness and recency all flow straight into output quality.

That's why data cleaning has to happen upstream of the AI system, not downstream. No prompt tweak or model upgrade fixes a fact that was already wrong before the model saw it. **Think of AI as a megaphone, not a filter**: it makes whatever you feed it louder, errors included.

| Data factor | Impact |
|---|---|
| **Data type** | Text, images, structured (tables), audio — model must match data type |
| **Data quality** | Errors, duplicates, inconsistencies propagate into AI outputs |
| **Representative datasets** | If training data excludes a group, the model will perform poorly for that group |
| **Data recency** | Stale data produces outdated insights |

### In Practice

**What breaks without this**: an assistant grounded on three conflicting copies of the price list gives a different price depending on which copy it retrieves, and users blame "the AI".

**Decision trigger**: ask, "is there one authoritative, current, deduplicated source for the data this use case depends on, and does it represent every group the solution serves?" If not, the data work is the first workstream.

**When you'd choose differently**: for exploratory brainstorming where no factual accuracy is claimed, imperfect source data matters far less. Data quality investment should scale with how much the output is trusted.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "switch to a more capable model" when outputs are wrong because the underlying data is duplicated, stale or unrepresentative. The exam blames the data before the model. Poor performance for one group of users points to a representativeness problem in the dataset.
</div>

---

## 1.9 Security Considerations for AI

### Key Concept

**AI adds new attack surfaces, because an LLM can't reliably tell instructions apart from the data it reads.**

Secure AI matters because an AI system connected to organisational data and actions turns a single weakness into exposure at scale. If one manipulated input or one over-permissioned connection is used across every query, it can leak customer data, reveal internal instructions or trigger actions nobody approved. Security failures also destroy the trust that adoption depends on: one leak can halt a programme.

These threats work because system instructions and the data a model reads arrive as the same stream of tokens. Prompt injection hides new instructions inside content the model retrieves (a document, an email, a web page), hoping the model treats them as commands. **Think of it like a letter that says "the bearer is authorised to open the vault"**: a careless clerk follows whatever the paper says.

| Threat | Description |
|---|---|
| **Prompt injection** | Malicious input that overrides the system's intended instructions |
| **Data poisoning** | Corrupted training data manipulates model behaviour |
| **Model extraction** | Attacker probes the model to replicate it |
| **Sensitive data leakage** | Model outputs training data or user data from previous sessions |

Data poisoning and model extraction target opposite ends of the lifecycle in §1.1b. Poisoning corrupts training data before the model learns from it; extraction probes a live, deployed model afterwards to reverse-engineer what it learned.

**Application security:** Validate and sanitise inputs. Use access controls. Don't pass raw user input directly to the model with full privileges.

**Data security:** Only expose the data a use case needs; isolate one customer's or user's data from another's.

**Authentication requirements:** Users should be authenticated before accessing AI features connected to sensitive org data (e.g., Copilot + Microsoft Graph).

<div class="note-important"><strong>Microsoft's approach:</strong> Microsoft 365 Copilot respects existing M365 permissions. A user can only access data through Copilot that they could already access directly. The AI doesn't bypass security boundaries.</div>

### In Practice

**What breaks without this**: a support bot that follows instructions found inside ticket text reveals its system prompt and internal discount codes to the first attacker who writes "ignore all previous instructions". A financial-summary tool without per-user authorisation shows one customer another customer's portfolio.

**Decision trigger**: ask, "what untrusted content does this model read, what data can it reach, and what can it do?" Treat retrieved content as data, never as instructions. Authenticate users and scope data to them. Rate-limit and watch the endpoints of any model you expose.

**When you'd choose differently**: an internal tool that only rewrites text a user pastes in, with no connected data and no actions, has a much smaller attack surface. Standard application controls are enough there, and it doesn't need the full threat-modelling effort.

### Exam Trap ⚠️

<div class="note-trap">
Match the threat to its signature. Instructions hidden in an input = prompt injection (treat input as untrusted data, validate/sanitise). Tainted data flowing into training or fine-tuning over time = data poisoning (validate and audit data sources). Huge volumes of systematically varied queries from one key = model extraction (rate limiting, anomaly detection, limit output granularity). Model revealing memorised or other users' data = sensitive data leakage.
</div>

---

## 1.10 AI Agents — Agentic AI vs Copilot

### Key Concept

**Copilot assists. Agents act: given a goal, an agent plans and carries out multi-step work without a prompt at each step.**

Copilot is assistive: it responds when a human prompts it, one interaction at a time, within a session. An AI agent is given an objective and works out the steps itself. It uses tools, triggers business processes and keeps state across sessions and tasks, adapting when something unexpected turns up.

That reasoning and adaptation is what separates an agent from scripted automation (RPA). A nightly script that runs the same fixed steps unattended isn't agentic just because nobody triggers it. **Think of Copilot as your AI assistant and an agent as an AI employee**: you ask the assistant for help, and you give the employee a goal and let them work out the steps.

| | Microsoft Copilot | AI Agent |
|---|---|---|
| **Mode** | Assistive — responds when prompted | Autonomous — takes initiative, acts without being asked each step |
| **Actions** | Text generation, summarisation, analysis | Multi-step workflows, tool use, triggering business processes |
| **Memory** | Single-session context | Can maintain state and context across sessions and tasks |
| **Examples** | Draft this email | Monitor my inbox, extract action items, update the CRM, send a summary |

![An agent takes the goal of processing new contracts, plans it into four steps from retrieving the contract to updating the tracker, and outputs a summary report to legal](/content/skillup/ab731/images/ab731-d1-agent-workflow.svg)

**M365 agent examples:**
- **Researcher agent** — autonomously researches a topic across web + your org data, synthesises a report
- **Analyst agent** — writes and runs Python code to analyse data, generates charts and insights
- **Custom agents** built in Copilot Studio — automate specific business workflows

<div class="note-scribble">The "agentic" trend is the biggest shift in enterprise AI right now — but use the built-in Researcher/Analyst agents when their documented purpose fits, and build a custom Copilot Studio agent only for company-specific logic, systems or rules.</div>

### In Practice

**What breaks without this**: 500 support tickets a day are "handled" by staff prompting Copilot ticket by ticket. The process is as manual as before, and nothing tracks state across steps.

**Decision trigger**: ask, "does this need multiple steps across systems, a trigger without a human prompt, or memory across days?" If yes, it's an agent use case. If it's a single prompted request that ends with one draft, Copilot is enough.

**When you'd choose differently**: a one-off, single-session task (one follow-up email from your own notes) doesn't justify building an agent. An unchanging, rule-based file move is better served by plain scripted automation, without an AI agent.

### Exam Trap ⚠️

<div class="note-trap">
"Which should be used to automatically categorise and route 500 support tickets per day without human prompting at each step?" → An <strong>AI agent</strong>, not Copilot. Copilot requires a human to prompt each interaction. Agents operate autonomously over a defined goal. The reverse trap: building an agent for a one-off single-session request, or calling a fixed-sequence scheduled script "agentic".
</div>

---

## 1.11 AI Use Case Prioritisation — Value × Feasibility

### Key Concept

**Fund the use cases with high value AND high feasibility first; "could we build it?" isn't "should it go first?"**

Prioritise on three dimensions: **business value** (revenue impact, cost savings, customer experience, employee productivity), **implementation feasibility** (data availability, technical complexity, change-management effort) and **time to value** (how quickly results can be measured). Plotting value against feasibility produces four quadrants, each with a different action.

Quick wins come first because they build organisational confidence and executive trust, which funds the bigger bets. **Think of it as picking the low-hanging fruit that is also the ripest**: easy to reach isn't enough, and the juiciest fruit at the top of the tree can wait for a ladder.

1. **Business value** — revenue impact, cost savings, customer experience improvement, employee productivity
2. **Implementation feasibility** — data availability, technical complexity, change management effort required
3. **Time to value** — how quickly you can see measurable results

![Value by feasibility matrix: Quick Wins do first, Strategic Bets plan for later, Incremental Gains do if capacity, Avoid don't do](/content/skillup/ab731/images/ab731-d1-value-feasibility-matrix.svg)

| Quadrant | Value | Feasibility | Action |
|---|---|---|---|
| **Quick Wins** | High | High (easy) | Do first — fast ROI, builds confidence |
| **Strategic Bets** | High | Low (hard) | Plan carefully — high reward but needs investment |
| **Incremental Gains** | Low | High (easy) | Do if time permits |
| **Avoid** | Low | Low (hard) | Don't invest time or resources |

**KPIs to measure AI success**

| KPI | What it measures |
|---|---|
| **Adoption rate** | % of target users actively using the tool weekly |
| **Time saved** | Hours per week reclaimed from manual tasks |
| **Error reduction** | % decrease in errors compared to pre-AI baseline |
| **Cost per task** | Before vs after AI — total cost to complete a task |
| **User satisfaction** | NPS or survey score from employees / customers |

<div class="note-important"><strong>Exam pattern:</strong> "What should be measured to determine if an AI pilot was successful?" → KPIs like time saved, adoption rate, error reduction, cost per task. NOT "number of AI features deployed" or "how much the technology impressed users."</div>

<div class="note-scribble">Even a small pilot that saves 2 hours/week across 50 people creates visible ROI (100 hours/week reclaimed) that funds the next, bigger investment.</div>

### In Practice

**What breaks without this**: the steering committee funds the most exciting idea, which depends on a 9-month data project. A year later there is still no measurable result and the AI budget is under review.

**Decision trigger**: ask, "for each candidate, what is the value, what blocks feasibility (data, complexity, change effort), and when could we measure a result?" Fund the high-value, high-feasibility ones first, and put strategic bets on a planned roadmap.

**When you'd choose differently**: if a strategic bet is existential (a competitor threat, a regulatory deadline), start its enabling work, such as the data infrastructure, in parallel with the quick wins rather than after them.

### Exam Trap ⚠️

<div class="note-trap">
Two absolute-language distractors: "the highest long-term value always takes priority" (ignores feasibility — that's a Strategic Bet, plan it later) and "the fastest to implement should always go first" (ignores value — that's an Incremental Gain). The answer is the Quick Win: high value AND high feasibility. And measure success with outcome KPIs, not feature counts.
</div>

---

## Deep Dive: Making Business Value of Generative AI Click

### 1. The connective narrative

Every topic in this domain answers one of three questions a business leader has to ask before committing budget to an AI initiative: *what kind of AI is this, what will it cost, and what could go wrong?* Section 1.1 answers the first question — generative AI creates, traditional ML classifies or predicts, and picking the wrong category means solving the wrong problem. Sections 1.2 through 1.8 answer the second — pretrained vs fine-tuned, tokens, RAG vs fine-tuning, and data quality are all really the same question asked from different angles: how do we get useful output without overspending on customisation we don't need?

Sections 1.9 through 1.11 answer the third. Security threats, hallucinations, and bias aren't abstract compliance checkboxes — they're the reasons a technically successful pilot still fails to scale, because nobody trusted the output or nobody caught the exposure until it was expensive. The value-prioritisation matrix in §1.11 exists precisely because "could we build this?" and "should we build this first?" are different questions, and Domain 1 is testing whether you keep them separate.

The thread that ties all of it together: generative AI's value is real, but it is not automatic. Every mitigation in this domain — grounding, human-in-the-loop review, prompt engineering before fine-tuning, KPI-based pilots before scaling — exists because the raw model, on its own, will confidently produce something plausible-sounding and wrong. The business leader's job is not to be impressed by the output; it's to know which of these guardrails the specific use case actually needs.

### 2. Worked scenario

> **Scenario.** A regional insurer is deciding whether to pilot AI for two separate needs: (1) flagging potentially fraudulent claims, and (2) drafting the plain-language explanation letters sent to customers after a claim decision.
>
> For (1), the task is "identify which claims look fraudulent" — that's classification, not generation, so this is traditional ML (§1.1), not a generative AI project. The team trains a fraud-scoring model, validates it against a held-out set of historical claims, deploys it, and — critically — sets up ongoing monitoring, because fraud tactics evolve and the model's accuracy will drift within months without retraining (§1.1b).
>
> For (2), "draft an explanation letter" is generative AI. The letters need to reference the specific policy terms and claim details for each customer — private, current company data — so the team grounds the model with RAG against the policy database rather than fine-tuning (§1.2b): RAG is cheaper, needs no retraining when policy wording changes, and can cite the specific clause it used. Cost is estimated in tokens: each letter runs roughly 400 input tokens (claim details + retrieved policy clauses) and 250 output tokens; at 2,000 letters/month, that's a small, predictable line item compared to the fully-loaded cost of a human writing each one (§1.3).
>
> Before either pilot ships, both go through the same two checks: a security review (does the fraud model or the letter-drafting tool expose customer PII beyond what the requesting employee could already see? — §1.9), and a KPI plan (time saved per letter, fraud-catch-rate lift, not "how advanced the AI looks" — §1.11). Only the letter-drafting pilot needs human-in-the-loop review before send, because a wrong fraud *score* gets a human investigator's attention anyway, while a wrong *letter* goes straight to a customer.

### 3. Memory aid

**CRAWL** — the order a business leader should actually work through Domain 1's concepts on a real use case:
- **C**lassify — generative or traditional ML? (§1.1)
- **R**isk — hallucination, bias, security exposure (§1.4, §1.9)
- **A**nchor — does it need grounding/RAG, or is prompting enough? (§1.6, §1.7)
- **W**eigh — token cost and ROI (§1.3)
- **L**aunch — agent or Copilot, and where it ranks in the value/feasibility matrix (§1.10, §1.11)

### 4. Exam strategy for this domain

D1's distractors are almost always a category swap — an answer that's technically true of the *other* AI type, the *other* customisation method, or the *other* mitigation. The exam rewards recognising which lever is cheapest and fastest for the stated problem (prompt engineering before RAG before fine-tuning; RAG before fine-tuning for facts) and punishes reaching for the most sophisticated-sounding fix when a cheaper one solves it. Five minutes before the exam: when two options both sound plausible, pick the one that solves the stated business need at the lowest cost and risk — not the one that sounds most technically advanced.

---

## 🎯 Domain 1 Exam Traps

| Trap | Correct answer |
|---|---|
| "Generate" or "create" in scenario | → Generative AI (it creates; ML classifies — don't confuse) |
| "Classify", "categorise", "detect" | → Traditional ML / discriminative AI |
| "Predict a number" | → Predictive ML / regression |
| "Improve output quality — cheapest fix?" | → Prompt engineering first, before RAG or fine-tuning |
| "Knowledge cutoff / private data" | → RAG, not fine-tuning |
| "Frequently-changing facts" | → RAG (updateable without retraining) |
| "Specialised domain vocabulary" | → Fine-tuning, only when prompt + RAG can't bridge the gap |
| "Copilot vs Agent" | → Copilot = assistive (prompted). Agent = autonomous (acts on goals) |
| "Pilot success metric" | → KPIs: time saved, adoption rate, error reduction |
| "Model deployed — is the work done?" | → No. Monitoring + retraining are ongoing lifecycle stages (catch concept drift) |
| Hallucination mitigation | → RAG + human review, NOT just better prompts or a bigger model |
| ROI calculation | → Time savings + quality + scalability, against token/licence cost |
| Bias types | → Know historical, representation, and measurement bias by name |

---

## 📌 D1 Hard Question Patterns

These patterns appear in harder exam questions. Knowing them prevents traps.

**Pattern 1 — RAG before Fine-tune**
> *"A company wants Copilot to answer questions using its internal HR policy documents. What should they do first?"*
>
> ✅ Use RAG / grounding to connect the LLM to the document store. Fine-tuning is NOT the answer — HR policies are data, not vocabulary.

**Pattern 2 — Hallucinations need structural fix, not prompt fix**
> *"Users report that the AI assistant sometimes gives wrong answers. What is the most effective mitigation?"*
>
> ✅ RAG (grounding) + human review workflow. "Write better prompts" alone is NOT sufficient — prompts cannot prevent hallucinations caused by knowledge gaps.

**Pattern 3 — Token cost and context window**
> *"A business wants to reduce AI costs. Which action has the most direct impact?"*
>
> ✅ Reduce context window / input token count. Both input AND output tokens cost money. Long system prompts + long documents = high cost.

**Pattern 4 — AI value is multiplicative, not additive**
> *"Where does generative AI provide the most business value?"*
>
> ✅ Tasks that are high-volume, time-consuming, and require human language (drafting, summarising, translating, coding). AI multiplies human capacity — it doesn't replace expert judgment in high-stakes decisions.
