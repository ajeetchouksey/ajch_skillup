# Deployment Options, SDKs & Prompt Flow

> **Skill track**: Microsoft Foundry Practitioner — Module 1, Lesson 2
> **Try it**: pairs with the hands-on mission "Deploy Your First Prompt Flow in Azure AI Foundry" (Prompt flow is a Foundry (classic) feature that retires on April 20, 2027; see the Playground & Prompt Flow section before building anything new on it)

## Prerequisites

- Comfortable reading a Python HTTP client call (you don't need to write one from scratch, just follow along)
- Lesson 1 (Projects, Hubs & the Model Catalog) — this lesson assumes you already know what a Foundry project and the model catalog are
- Basic idea of what "requests per minute" and "tokens" mean for an API — no math beyond arithmetic

## Overview

Picking a model is only half the job — you also have to decide *how it's hosted*, *how your code talks to it*, and *how you prove the prompt in front of it works* before anything reaches production. This lesson covers all three, because in practice they're one decision, not three: the deployment option you pick constrains which SDK calls make sense, and bulk evaluation only pays off once you've settled on a deployment stable enough to test against.

> 💡 **Human Angle**: *Think of the model catalog as a car showroom and the deployment type as how you pay for the car — lease it by the mile (serverless/pay-per-token), buy it outright and park it in your garage (managed compute), or reserve a dedicated lane on the highway (provisioned throughput).*

## Deployment Options

### Key Concept

**The deployment option you pick is a bet on your traffic shape, not a technology preference.**

Microsoft Foundry gives you two ways to host a catalog model: a **serverless deployment**, where Microsoft hosts the model and you call an API, or **managed compute**, where the model weights run on dedicated VMs. Within serverless there are three billing families: **Standard** (pay-per-token), **Provisioned** (hourly reserved capacity), and **Batch** (discounted, asynchronous).

These options differ on one axis that matters day to day: who pays for idle capacity. With Standard, Microsoft absorbs it, so a quiet Tuesday costs you nothing. With Provisioned or managed compute you reserve capacity up front, so a quiet Tuesday costs the same as a busy Friday, but you get *guaranteed* throughput or hardware control in return.

Each billing family also comes in **Global**, **Data Zone**, or regional flavours, which decide where prompts are processed: global might route to any Azure region, data zone stays within a boundary such as the EU or US, and regional stays in one region. Batch is the odd one out. **It trades an immediate answer for a steep discount**, queuing a large job asynchronously instead of responding in real time.

| Option | Compute model | Billing | Best for |
|---|---|---|---|
| Standard (Global / Data Zone / regional) | Serverless, Microsoft-managed | Pay-per-token, variable latency under load | Fast start, variable or unknown volume |
| Provisioned (Global / Data Zone / Regional) | Serverless, reserved capacity | Hourly reserved capacity | Latency-sensitive production workloads needing predictable throughput |
| Batch (Global / Data Zone) | Serverless, asynchronous queue | Discounted batch token pricing | Large, non-latency-sensitive jobs |
| Managed compute | Dedicated VM-backed endpoint | VM core hours regardless of usage | Open models (for example Hugging Face) that need their own hardware |

Managed compute deployments of open models have historically required a hub-based project in the Foundry (classic) portal; check the current docs before planning around them on a Foundry resource. Availability of every option varies by model and region.

![Flow diagram for "Key Concept": no, can wait, yes, flat and predictable, spiky or unknown, no, Urgent response needed?, Batch, Traffic shape?, Need own hardware?, Standard](/content/skillup/azure-ai-foundry/images/azure-ai-foundry-m1-l2-deployment-sdks-prompt-flow-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/azure-ai-foundry/azure-ai-foundry-m1-l2-deployment-sdks-prompt-flow-m1.mmd -->
*Match your traffic to a deployment family, then pick the processing scope.*

### In Practice

**What breaks without this**: a team that defaults to managed compute "because that's what we did before" ends up paying for a VM that sits at 8% utilization overnight — real money for capacity nobody's using, when a Standard (pay-per-token) deployment would have cost near-zero during those same idle hours.

**Decision trigger**: ask *"if I plotted my requests-per-minute over a week, would the line be flat or spiky?"* Flat and predictable → Provisioned is worth the commitment. Spiky or unknown → start with Standard, because you can move to Provisioned later once you have real traffic data, but you can't easily walk back an over-provisioned reservation. Then ask *"where may prompts be processed?"* to choose Global, Data Zone, or regional.

**When you'd choose differently**: a spiky-traffic team would normally reach for Standard, but if that spike happens to be a hard latency-SLA workload (a trading desk, a live support handoff) where *variable* latency under load is itself unacceptable — not just average latency — Provisioned's predictability can be worth paying for headroom you don't always use.

### Common Pitfall ⚠️

<div class="note-trap">
Deployment options are *region- and model-specific*. A newly released catalog model may only support some deployment types at first, or only be available in a subset of regions. "It's in the catalog" doesn't mean "it's deployable everywhere, every way, immediately." Always check the model card before committing to an architecture around a specific deployment type.
</div>

## Connections & SDKs

### Key Concept

**Two clients exist because configuring a project and calling a model are different jobs done at different times.**

The **project client** in `azure-ai-projects` (version 2.x targets the current Foundry portal; 1.x targets classic) handles Foundry-native operations with no OpenAI equivalent: listing connections, reading project properties, enabling tracing. The **OpenAI-compatible client** from the `openai` package is what your application calls on every user request for chat completions, embeddings, or the Responses API. The project client can hand you one already pointed at your project endpoint. The older `azure-ai-inference` package was retired on August 26, 2026; Microsoft's migration path is the `openai` package.

**Connections** are what tie a project to the outside resources it needs — most commonly an Azure AI Search index for RAG, plus Storage, Key Vault, and Application Insights. Get the connection wrong and neither client will save you. **It's like wiring a new office**: the phone line works perfectly, but if nobody plugged in the filing cabinet, every lookup comes back empty.

### In Practice

**What breaks without this**: copying a 2024-era sample that builds a `ChatCompletionsClient` from `azure-ai-inference` — the package is retired, so new code built on it is migration debt on day one. The same goes for mixing SDK generations: a 2.x `azure-ai-projects` sample run against a classic (1.x) setup, or the other way round, fails with confusing errors.

**Decision trigger**: ask *"is this code configuring the project (connections, tracing, project properties), or is it running per user request to get model output?"* Configuring → project client. Model output → OpenAI-compatible client.

**When you'd choose differently**: a background job that periodically audits a project's connections (a governance script, say) legitimately uses the project client even though it runs on a schedule "like" a hot-path job — the distinguishing factor is *what it's asking for* (project metadata vs. a model's output), not how often it runs.

## Fine-Tuning

### Key Concept

**Fine-tuning data must already look exactly like the conversation you'll have in production.**

The training file is JSONL — one JSON object per line — and each line's `messages` array uses the same role/content shape (`system`/`user`/`assistant`) the chat-completion API expects at inference time. This isn't an arbitrary format choice: the model is learning to continue conversations shaped like your training examples, so if your training data doesn't match your production prompt structure, the fine-tune won't transfer.

### In Practice

**What breaks without this**: a team trains on flat prompt/completion pairs (no `messages` structure, no system role) and then wonders why the fine-tuned model behaves inconsistently once it's called through a normal chat-completion request — the mismatch between training shape and inference shape is the cause.

**Decision trigger**: ask *"could I take one line of my training file and use it, unmodified, as an actual API call?"* If not, the data isn't ready to submit.

**When you'd choose differently**: if you're trying to fix formatting/tone rather than add new knowledge, a well-crafted system prompt often gets you 80% of the way there for a fraction of the cost and turnaround time — reach for fine-tuning once prompt engineering has genuinely plateaued, not as the first lever you pull.

```jsonc
// One line of a valid fine-tuning training file
{"messages": [
  {"role": "system", "content": "You are a support agent for Contoso Retail. Keep replies under 3 sentences."},
  {"role": "user", "content": "Where is my order #4821?"},
  {"role": "assistant", "content": "Order #4821 shipped yesterday and is expected by Thursday. I've sent the tracking link to your email."}
]}
```

## Quota

### Key Concept

**Quota is enforced on two independent dimensions, and hitting either one throttles you.**

Azure OpenAI tracks tokens-per-minute (TPM) and requests-per-minute (RPM) separately per deployment. A workload sending few requests with huge payloads can exhaust TPM while nowhere near its RPM limit; a chatty workload sending many tiny requests can hit RPM while barely touching TPM. Quota can be split across multiple deployments within the subscription's overall ceiling, which is how teams isolate a noisy-neighbor workload from a latency-critical one.

### In Practice

**What breaks without this**: a team load-tests with a handful of large-payload requests, sees TPM headroom to spare, and ships — then gets throttled in production once real traffic sends ten times as many small requests, because they never checked RPM.

**Decision trigger**: ask *"which dimension will my real traffic pattern hit first — big payloads or high request counts?"* — and load-test against *that* dimension specifically, not just whichever one is easier to simulate.

**When you'd choose differently**: if two workloads share a deployment and one starts starving the other of quota, splitting them into separate deployments (each with its own TPM/RPM allocation) is the fix — not requesting a blanket quota increase, which just delays the same conflict at a higher ceiling.

## Playground & Prompt Flow

### Key Concept

**The playground is for exploring a prompt; a batch evaluation is for proving it works before you ship it.**

The playground gives fast, code-free iteration on a system message, parameters, and a couple of few-shot examples. It's ideal for the first hour of figuring out what you even want the model to do. Proving the prompt is a different stage: you run it against a real dataset and score the results with built-in evaluators (groundedness, relevance, coherence, and others), the same way every time.

For years the Foundry tool for that second stage was **Prompt flow**, a visual, DAG-based canvas for chaining retrieval, prompt, and LLM nodes and bulk-testing the chain. Prompt flow is now a classic-only feature: it's no longer recommended for new development, its container images no longer get security or package updates, and it retires on **April 20, 2027**. Microsoft's replacement is **Microsoft Agent Framework**, which is code-first. A flow becomes a `WorkflowBuilder` graph of executors, and its evaluation flow becomes evaluators from the Azure AI Evaluation SDK. **Think of Prompt flow as scaffolding**: useful while the building went up, but you take it down before you move in.

### In Practice

**What breaks without this**: a team ships a prompt that looked great for the five examples they tried by hand in the playground, then discovers in production that it fails on a whole category of inputs nobody happened to try. A scored batch evaluation against a real dataset is exactly what would have caught that before launch. A second failure: a team starts a new project on Prompt flow in 2026 because an old tutorial used it, and inherits a forced migration within a year.

**Decision trigger**: ask *"have I tried this prompt against more than a handful of hand-picked inputs?"* If no, you're still in playground territory. If you need a repeatable, scored answer across dozens or hundreds of inputs, run a batch evaluation. If you also need multi-step orchestration, build it in Agent Framework, not Prompt flow.

**When you'd choose differently**: if you already run production Prompt flows, keep them running while you migrate. Microsoft's guide suggests auditing every node, rebuilding in Agent Framework, then running both side by side and scoring output parity with `SimilarityEvaluator` before cutting over.

### Common Pitfall ⚠️

<div class="note-trap">
Two things trip teams up here. First, Prompt flow isn't "the low-code way to build in the new Foundry": it lives only in the classic portal and retires on April 20, 2027. Second, guardrails (content filters) on Foundry Models sold by Azure are **on by default**. Every customer can pick a Low, Medium, or High blocking level and can turn filtering off for *inputs*, but turning it off for *outputs* requires approval through Microsoft's Limited Access Review for modified guardrails.
</div>

## Deep Dive: Making Deployment, SDKs & Prompt Flow Click

### 1. The connective narrative

These three topics look separate but resolve into one pipeline. You start by choosing a deployment option — a bet on your traffic shape — because that decision determines what "calling the model" even looks like: a pay-per-token Standard deployment, or a Provisioned one your finance team signed off on for guaranteed latency. Once you have a stable endpoint, the client split (the `azure-ai-projects` project client vs. the `openai` client) reflects the two different jobs done against it: setting the project up, and calling the model constantly. And once you're iterating on *what you send* to that endpoint — the actual prompt — a batch evaluation is where you stop trusting your own five hand-picked test inputs and start proving the prompt holds up across a real dataset before it goes anywhere near production traffic. (That used to be Prompt flow's job; it's retiring, so new work belongs in evaluations and Agent Framework.)

Fine-tuning and quota sit slightly to the side of that main pipeline, but they answer the two questions that come up the moment the pipeline is live: "what if prompting alone isn't enough?" (fine-tune, but only after prompting has genuinely plateaued) and "what happens when real traffic arrives?" (quota, on two independent axes that traffic can hit separately).

### 2. Worked scenario

> **Scenario.** Contoso Retail wants to add an AI support chatbot backed by DeepSeek-V3.2 from the catalog. Traffic is spiky — quiet most of the day, then a burst up to ~50 requests/minute during evening promos — and the team has no infrastructure headcount to manage VMs.
>
> Walking the decision end to end:
>
> 1. **Check the model card first.** Not every catalog model supports every deployment type, support is region-specific, and models retire (the catalog's lifecycle filter and the model retirement schedule show dates). The card confirms a pay-per-token Standard deployment type in Contoso's region. Skipping this step is the single most common way teams pick an option that turns out to be unavailable.
> 2. **Match the traffic pattern to a billing model.** Spiky, unpredictable volume with no infrastructure team is the textbook case for a **Standard (pay-per-token) serverless deployment** — Microsoft-managed, billed per token, nothing to run. Contoso's customers are all in the EU and legal wants prompts processed there, so they choose **Data Zone Standard** over Global Standard. Managed compute would mean paying for a dedicated VM around the clock even during the quiet hours; Provisioned's reserved capacity doesn't fit unpredictable spiky load either.
> 3. **Wire up the right client for the job.** The actual chat-completion calls at runtime go through the **OpenAI-compatible client** from the `openai` package, authenticated with Microsoft Entra ID rather than a stored key:
>
> ```python
> from openai import OpenAI
> from azure.identity import DefaultAzureCredential, get_bearer_token_provider
>
> token_provider = get_bearer_token_provider(
>     DefaultAzureCredential(), "https://ai.azure.com/.default"
> )
> client = OpenAI(
>     base_url="https://contoso-foundry.openai.azure.com/openai/v1/",
>     api_key=token_provider,
> )
> response = client.chat.completions.create(
>     model="DeepSeek-V3.2",  # your deployment name
>     messages=[{"role": "user", "content": "Where is my order #4821?"}],
> )
> ```
>
> If Contoso later needs a setup script that lists the project's connections or turns on tracing, that's the **project client** in `azure-ai-projects` instead — a different job entirely, not a fallback for the same job.
> 4. **Before launch, run a batch evaluation of the actual support prompt** against a few hundred real historical support questions, not the handful the team tried by hand — this is what catches a category of question the prompt silently mishandles before a customer finds it in production.
> 5. **Load-test against both quota dimensions**, not just one: a 50 requests/minute promo burst with moderately long support responses could plausibly hit either the RPM or the TPM ceiling first, and only measuring one gives a false sense of headroom.
>
> **Contrast case**: if Contoso instead ran a trading-desk assistant needing guaranteed, consistent sub-second latency regardless of load, the right call flips to a **Provisioned** deployment — the deciding factor is a *predictability* requirement, not raw volume.

### 3. Memory aid

Before picking a deployment option, run through this checklist in order:

1. **Shape** — flat or spiky traffic?
2. **Control** — do I need my own hardware, or is "just give me an endpoint" fine?
3. **Latency guarantee** — does *variability* under load break something, not just average speed?
4. **Urgency** — does this need to answer right now, or can it run as a batch for a discount?
5. **Scope** — may prompts be processed anywhere (Global), within a boundary (Data Zone), or only in one region?

The first four pick the family (Standard, Provisioned, Batch, or managed compute); the fifth picks the processing scope.

### 4. Applying this in real projects

- The most common real-world mistake isn't picking the wrong deployment option — it's picking a *reasonable* one and never revisiting it once real traffic data exists. A Standard deployment chosen for an unknown launch-day traffic shape should be reassessed against Provisioned once you have a month of real RPM/TPM data.
- Put the model's retirement date in your plan on day one. Catalog models deprecate and retire on a published schedule, and a migration is cheaper when it's planned than when it's forced.
- Teams reach for fine-tuning far earlier than they should. If you haven't tried a longer, more structured system prompt with a few strong few-shot examples first, you don't yet know whether you actually need fine-tuning.
- Quota throttling in production is almost always a "we tested the wrong dimension" problem, not a "we needed more quota" problem — check which axis your real traffic actually stresses before requesting an increase.

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Standard (serverless) | Pay-per-token, no customer-managed compute |
| Managed compute | Dedicated VM, pay regardless of usage |
| Provisioned | Hourly reserved capacity, predictable latency |
| Batch | Async, discounted |
| Global / Data Zone / regional | Where prompts may be processed |
| azure-ai-projects (2.x) | Project client: connections, project properties, tracing |
| openai | Model calls: chat completions, embeddings, Responses API |
| azure-ai-inference | Retired August 26, 2026; migrate to `openai` |
| Fine-tune data format | JSONL, `messages` array matching production shape |
| Quota dimensions | TPM + RPM — enforced independently |
| Guardrails (content filters) | On by default; turning off output filtering needs modified-guardrails approval |
| Playground vs. batch evaluation | Explore by hand vs. prove at scale before shipping |
| Prompt flow | Classic-only, retires April 20, 2027; migrate to Microsoft Agent Framework |
