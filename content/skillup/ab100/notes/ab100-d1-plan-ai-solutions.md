# D1: Plan AI-Powered Business Solutions

> **Exam weight**: 35–40% (skills measured as of November 16, 2026; 25–30% before that date) · the largest domain on the exam

## Overview

**Domain 1** covers the upfront strategic and architectural decisions for agentic AI initiatives — from identifying the right use cases and mapping them to Azure services, to estimating costs, aligning stakeholders, and satisfying regulatory requirements before a single line of code is written.

---

## Use Case Identification & ROI

### Key Concept

**Reach for an agent only when the task needs language understanding, multi-step reasoning and autonomous tool use.**

This section gives the triage order for automation ideas. Structured, rules-based work belongs to RPA or Logic Apps; prediction without language belongs to traditional ML; conversational tasks without multi-step reasoning fit Copilot Studio; only autonomous tool use justifies a full agent. (The diagram's "prompt flow" branch predates prompt flow's retirement, announced for April 20, 2027; see D2 for the replacement.)

ROI then decides whether the option that fits is worth building: compare the current process cost with token and service costs, and discount the projected savings by the expected error rate. **Think of it like hiring: you don't bring in a senior consultant to file paperwork that a script could handle.**

#### The Agentic AI Decision Framework

Not every automation problem benefits from an AI agent. The decision tree:

![Decision tree: structured and rules-based problems go to RPA or Logic Apps; no language understanding goes to traditional ML; no multi-step reasoning goes to Copilot Studio; no autonomous tool use goes to Azure OpenAI with prompt flow; otherwise agentic AI on the AI Foundry Agent Service](/content/skillup/ab100/images/ab100-decision-framework.svg)

#### ROI Calculation Factors
- **Cost of current process**: FTE hours × hourly rate × volume
- **Agent cost**: (input tokens × rate) + (output tokens × rate) + Azure AI services
- **Break-even**: typically at >500 repetitive tasks/month
- **Risk discount**: multiply projected savings by (1 - error_rate) for safety margin

### In Practice

**What breaks without this**: A rules-based routing job is rebuilt as an LLM agent, costs more per transaction than the RPA bot it replaced, and now routes the same input differently on different days.

**Decision trigger**: Ask: could a flowchart with fixed rules do this reliably? If yes, an agent is the wrong tool. If no, ask whether the task needs to call tools on its own or just answer.

**When you'd choose differently**: When inputs are unstructured (free-text emails, scanned documents), even a simple routing task can justify language AI, because writing rules for every phrasing is the real cost.

### Exam Trap ⚠️

<div class="note-trap">
The exam often presents scenarios where Copilot Studio looks like the right answer because it's "no-code." Remember: Copilot Studio is correct for **knowledge worker** tasks with existing Microsoft 365 data. Foundry Agent Service (formerly Azure AI Agent Service) is correct when you need **custom code execution**, complex multi-agent orchestration, or non-Microsoft data sources.
</div>

---

## Microsoft Foundry Architecture

### Key Concept

**A Foundry resource is the shared, governed parent; projects are the isolated workspaces where each team builds.**

This section sets out the current resource model. The Foundry resource carries what should be governed once (networking, customer-managed keys, model deployments, quota and shared connections), while each project holds one team's agents, evaluations, datasets, indexes and files. Hub-based projects remain only in the Foundry (classic) portal.

The design choice is where to draw boundaries: projects under one resource for exploration, separate resources for production workloads that need strict isolation. **Think of the resource as an office building with shared security and utilities, and each project as a locked suite inside it.**

#### Foundry Resource vs Project (and Classic Hubs)

Azure AI Foundry is now **Microsoft Foundry**, and Azure AI Services are now **Foundry Tools**. The current resource model is a single **Foundry resource** that contains **projects**. Hub-based projects still exist but live in the **Foundry (classic)** portal, where Microsoft is no longer focusing new investment. The diagram below shows the classic hub model; the same "shared parent, isolated child" idea carries over to Foundry resources and projects.

**Foundry resource** = shared platform: networking, keys, model deployments, quota, resource-level connections

**Project** = a use-case workspace: agents, evaluations, datasets, indexes, files

![Azure AI Foundry Hub providing shared Key Vault, Storage Account, Container Registry and App Insights under one governance layer to the HR Agent, Finance Agent and Customer Support projects](/content/skillup/ab100/images/ab100-d1-hub-vs-project.svg)


| Concept | Foundry resource | Project |
|---------|-----|---------|
| Scope | Workload boundary (one or many use cases) | One use case or team |
| Holds | Networking, customer-managed keys, model deployments, quota, shared connections | Agents, evaluations, datasets, indexes, files, project-level connections |
| Access | Platform / governance team | Dev team (project-scope RBAC for most agent APIs) |
| Isolation | Separate resources for strict production isolation | Separate workspaces inside a shared resource |

> **Rule of Thumb**
For production, Microsoft treats isolation as the default: one Foundry resource per production workload boundary. Co-locate (one resource, a project per use case) for exploration and early prototypes.
Some Foundry Tools APIs, such as speech-to-text, still need permissions at the parent resource scope, so check your capability mix before choosing project-only RBAC.

#### Key Resource-Level Capabilities
- **Foundry Tools** (formerly Azure AI Services): speech, language, vision, translation and more, accessed through the Foundry resource
- **Foundry Models catalog**: models from Microsoft, OpenAI, Anthropic, Meta and others
- **Deployment types**: Global, Data Zone and Standard (regional), each in pay-per-token or provisioned (PTU) form, plus Batch and Developer

### In Practice

**What breaks without this**: Production and experiments share one resource, so a prototype team consumes quota that production depends on, and a networking change made for one use case hits all of them.

**Decision trigger**: Ask: does this workload need its own network rules, keys or quota? If yes, give it its own Foundry resource. If not, add a project to an existing resource.

**When you'd choose differently**: If a capability you need, such as speech-to-text, requires permissions at the parent resource scope, project-only RBAC isn't enough; plan resource-scope roles or a separate resource.

### Exam Trap ⚠️

<div class="note-trap">
"Create a hub" is the classic-portal answer, not the current one: new work uses a Foundry resource with projects. And a new project doesn't isolate networking or keys, because those are set on the resource. Strict production isolation means a separate Foundry resource.
</div>

---

## Model Selection in Microsoft Foundry

### Key Concept

**Pick the smallest model that meets the task's reasoning, latency and location needs, then choose the platform around it.**

This section pairs two choices. The model tree runs from edge or on-device needs (small Phi models) through deep reasoning (reasoning-series models) to high-volume standard work (mini models). Treat the named versions as examples of tiers: Foundry models have published retirement dates and several GPT-4o versions are already deprecated, so check the model retirement schedule before committing to one.

The make-vs-buy table then picks the agent platform: Copilot Studio when data lives in Microsoft 365 or Dataverse and the builders are low-code makers, Foundry Agent Service when you need custom code, any data source, or code-first multi-agent orchestration. **Think of models as vehicles: you don't send a lorry to deliver a letter, or a scooter to move house.**

#### Model Selection Decision Tree

![Model selection decision tree: edge or embedded goes to Phi-3 / Phi-3.5; deep reasoning to GPT-4o / o1-series; standard reasoning with low latency to GPT-4o-mini / Phi-3-mini, otherwise GPT-4o](/content/skillup/ab100/images/ab100-d1-model-selection.svg) 


| Model | Best For | Context | Cost Tier |
|-------|----------|---------|-----------|
| GPT-4o | Complex reasoning, multimodal | 128K | High |
| GPT-4o-mini | High-volume, cost-sensitive | 128K | Low |
| o1-series | Multi-step math/code reasoning | 128K | Very High |
| Phi-3-mini | Edge, low-latency, on-device | 4K | Very Low |
| Phi-3-medium | Balanced local/cloud | 128K | Low |
| Llama 3 | Open-source, fine-tunable | 8K/128K | Variable |

#### Make vs Buy: Copilot Studio vs Custom Agent

| Factor | Use Copilot Studio | Use Foundry Agent Service |
|--------|-------------------|---------------------------|
| Data sources | Microsoft 365, SharePoint, Dataverse | Any (REST, SQL, proprietary) |
| Integration | Power Platform connectors | Azure Functions, custom code |
| Orchestration | Topics-based flow | Code-first, multi-agent |
| Governance | Power Platform DLP | Azure RBAC, custom |
| Code skills | Low-code / no-code | Pro-code required |
| Time to value | Days | Weeks |

### In Practice

**What breaks without this**: A reasoning-series model sits on a latency-sensitive chat path doing simple extraction, so every reply is slow and costs several times what a mini model would.

**Decision trigger**: Ask three things: what is the hardest reasoning step, what is the latency budget, and where must the model run? Those pick the tier. Who will build and maintain the agent picks the platform.

**When you'd choose differently**: When traffic mixes easy and hard prompts, a model router deployment can choose per request instead of you fixing one model (see Foundry Model Router below).

### Exam Trap ⚠️

<div class="note-trap">
"Copilot Studio uses **topics** (not agents) as its orchestration primitive. If the scenario says 'the solution must call a custom Python function or query a proprietary database,' Copilot Studio's connectors may not be sufficient — Foundry Agent Service is the right answer."
</div>

---

## Capacity Planning

### Key Concept

**Provision throughput for steady, latency-sensitive load, pay per token for bursty load, and combine them with spillover.**

This section covers two planning inputs. Provisioned throughput (PTU) reserves model capacity that you pay for whether or not you use it, and in return gives low latency variance; pay-per-token Standard types charge only for what you consume and suit variable traffic, prototypes and dev/test.

Regional planning comes next: confirm the model and deployment type are available where you need them, and match the deployment type to any residency rule. **Think of PTU as a leased line and pay-per-token as a metered phone: the lease is cheaper and steadier only if you keep it busy.**

#### Provisioned Throughput Units (PTU)

![Capacity decision from the traffic estimate: sustained peaks above 100K TPM use PTU, spiky traffic uses pay-as-you-go, and both use a PTU baseline with PAYG overflow](/content/skillup/ab100/images/ab100-d1-ptu-capacity.svg) 


- **PTU (provisioned)**: reserved throughput billed whether or not it's used — best for consistent high volume and when you need low latency variance
- **Pay-per-token (Standard types)**: best for variable or bursty traffic, prototyping and dev/test; Microsoft recommends Global Standard as the default starting point
- **Spillover pattern**: PTU for the steady base load, with pay-per-token capacity absorbing peaks

#### Regional Availability Checklist
- Check model availability per region and deployment type in the Foundry Models catalog
- EU data residency: choose an EU region **and** a Data Zone (EU) or Standard deployment type — Global types may process prompts in any Azure region
- Asia Pacific: East Asia or Australia East
- Cross-region replication for HA: use Azure Front Door + two regional deployments

### In Practice

**What breaks without this**: PTU sized for average load with no overflow returns 429 errors at the daily peak; PTU sized for the peak sits mostly idle and costs more than pay-per-token would have.

**Decision trigger**: Ask: is traffic steady enough to keep reserved capacity busy, and is latency variance a business problem? If both are yes, use a PTU base with spillover to pay-per-token.

**When you'd choose differently**: For a new workload with no traffic history, start on Global Standard pay-per-token, measure real usage, then move the steady base to provisioned.

### Exam Trap ⚠️

<div class="note-trap">
"PTU guarantees no throttling" is wrong: a provisioned deployment returns 429 when requests exceed its capacity, which is why spillover or a pay-per-token fallback exists. And a Global provisioned deployment doesn't meet an EU processing rule; Data Zone (EU) or a regional type does.
</div>

---

## Stakeholder Alignment & Compliance

### Key Concept

**Before building, identify harms, classify regulatory risk and plan personal-data handling, and get stakeholders to sign off on all three.**

This section bundles the pre-build governance work. The Responsible AI checklist runs identify, mitigate, document, monitor and govern; the EU AI Act table sets obligations by risk tier; and the GDPR list turns data protection rules into agent design choices.

Stakeholders sign off on these because they change scope: a high-risk classification adds conformity assessment work, and erasure obligations decide how indexes are partitioned. **Think of it as a building permit: getting it after the walls are up costs far more than getting it first.**

#### Responsible AI Checklist (pre-deployment)
1. **Identify** potential harms (use Microsoft RAI Impact Assessment template)
2. **Mitigate** with content filters, human review, rate limits
3. **Document** in a Transparency Note
4. **Monitor** with Azure AI Content Safety + Azure Monitor alerts
5. **Govern** with Foundry guardrails, RBAC and Azure Policy (for example, policies that restrict deployment types)

#### EU AI Act Risk Categories

| Category | Examples | AB-100 Relevance |
|----------|----------|-----------------|
| Unacceptable | Social scoring, real-time biometric surveillance | Out of scope (prohibited) |
| High-risk | HR screening, credit scoring, safety systems | Requires conformity assessment |
| Limited risk | Chatbots, recommendation systems | Transparency obligations |
| Minimal risk | Spam filters, AI in games | No obligations |

#### GDPR Considerations for Agents
- Conversation history stored in Cosmos DB must have **TTL policy** (data minimization)
- User data in vector indexes → right to erasure requires **index partitioning by user ID**
- Agent outputs used for profiling → **legitimate interest** or consent required

### In Practice

**What breaks without this**: An HR screening agent ships as "just a chatbot", is later classified as high-risk, and the team has to retrofit human oversight, logging and documentation into a live system.

**Decision trigger**: Ask: does the agent make or influence decisions about people, such as hiring, credit or access to services? If yes, plan for high-risk obligations until legal review says otherwise.

**When you'd choose differently**: An internal agent that only summarises public product documentation, with no personal data and no decisions about people, needs a much lighter review, usually transparency alone.

### Exam Trap ⚠️

<div class="note-trap">
The interface doesn't set the risk tier; the use case does. A chat interface that screens job applicants is high-risk, because employment and recruitment are listed in Annex III. And right-to-erasure must reach vector indexes and conversation stores, not just the source system.
</div>

---

## Integration Patterns

### Key Concept

**Choose the trigger by event source, volume and latency; the agent logic behind it stays the same.**

This section maps event sources to triggers: Service Bus queues for durable, high-volume messages, Event Grid for file and blob events, Logic Apps for Office 365 and SaaS connectors, direct HTTP for real-time user calls, and Power Automate for business-owned no-code flows.

The trigger decides durability, latency and who maintains the integration, not what the agent does. **Think of triggers as different doors into the same room: pick the door that suits who is arriving and how many of them.**

#### Event-Driven Agent Trigger Patterns

![Event sources (Exchange email, Power Apps form, Service Bus message, Blob upload) trigger an AI Foundry agent via Logic Apps, Power Automate, Azure Function or Event Grid, and the agent updates CRM, sends a response or creates a ticket](/content/skillup/ab100/images/ab100-d1-event-trigger-patterns.svg) 

| Trigger Pattern | Best For | Latency |
|----------------|----------|---------|
| Service Bus queue | High-volume, durable | Seconds |
| Event Grid | File/blob events | Sub-second |
| Logic Apps | Office 365, SaaS | Seconds |
| HTTP direct | Real-time user interactions | <1s |
| Power Automate | Business users, no-code | Seconds |

### In Practice

**What breaks without this**: Thousands of emails a day are pushed to an agent over direct HTTP; when the agent slows down, calls time out and messages are lost because nothing queued them.

**Decision trigger**: Ask: can the caller wait for the answer, and can we afford to lose a message? If the caller is a user waiting, use HTTP; if messages must not be lost, put a Service Bus queue in front.

**When you'd choose differently**: If business users own the process and volume is modest, Power Automate is easier for them to maintain than a Service Bus pipeline, even though a queue-based design scales further.

### Exam Trap ⚠️

<div class="note-trap">
Event Grid distributes event notifications ("a blob was created"); it isn't a work queue. When a scenario needs durable, ordered processing of business messages with dead-lettering and sessions, the answer is Service Bus.
</div>

---

## Cheat Sheet 📋

| Concept | Key Rule |
|---------|----------|
| Foundry resource vs project | Resource = shared networking, keys, deployments, quota; Project = use-case workspace |
| PTU vs pay-per-token | PTU for consistent high volume or low latency variance; pay-per-token for bursty/dev |
| Copilot Studio | Use for M365 data + low-code + business users |
| Foundry Agent Service | Use when custom code, non-Microsoft data, or complex multi-agent |
| EU AI Act HR tool | High-risk → requires conformity assessment |
| Model: GPT-4o-mini | High volume, cost-sensitive, standard reasoning |
| Model: o1-series | Deep reasoning, math/code — NOT for latency-sensitive paths |
| Spillover pattern | PTU primary + PAYG overflow via load balancer |
| Data residency | EU region + Data Zone (EU) or Standard deployment; never Global |
| Right to erasure | Partition vector indexes by user ID |


---

## Cloud Adoption Framework — AI Adoption Process

### Key Concept

**CAF describes the organisation's AI adoption journey: strategy, plan, ready, then govern, secure and manage.**

This section summarises CAF's AI guidance. Each step builds on the one before: strategy sets outcomes and decision rights, the plan turns use cases into a route to production, AI ready fits workloads into the landing zone, and the last step sets standards for governing, securing and managing them.

The CAF decision tree also steers product choice towards the option with the least operational responsibility that still meets the need. **Think of CAF as the route map for the whole trip, and the Well-Architected Framework as the inspection for each vehicle.**

CAF's AI guidance starts with an **AI strategy** and then walks through the adoption steps, each building on the one before:

| Step | Key Activities |
|-------|---------------|
| **AI strategy** | Lead adoption (business outcomes, decision rights, how value is measured), centralize AI governance (for example in an AI Center of Excellence), give the workforce access to approved AI, and choose which AI to use with the least operational responsibility |
| **AI plan** | Turn AI use cases into a plan for moving them into production |
| **AI ready** | Fit AI workloads into your Azure landing zone and decide whether architecture or governance must change |
| **Govern, secure, manage AI** | Establish standards for governing, securing and managing AI workloads |

The CAF AI decision tree maps needs to products: individual productivity → Microsoft 365 Copilot and in-product or role-based Copilots; low-code business automation → Copilot Studio; custom apps and agents on a managed platform → Microsoft Foundry; your own models → Azure Machine Learning or Microsoft Fabric; full runtime control → Azure infrastructure (never the default).

### In Practice

**What breaks without this**: Teams build agents before any AI strategy exists, so each picks its own models, governance and success measures, and nobody can compare value or enforce a standard.

**Decision trigger**: Ask: is the question about how the organisation adopts AI (strategy, governance, readiness) or about the quality of one workload? The first is CAF; the second is the Well-Architected Framework.

**When you'd choose differently**: A single team piloting one Copilot Studio agent doesn't need the full CAF journey first; it needs the platform's governance (environments, DLP) and can feed what it learns into the strategy.

### Exam Trap ⚠️

<div class="note-trap">
CAF is the adoption *journey* framework. Well-Architected Framework governs *workload quality* (reliability, security, etc.) — applied after architectural decisions are made. And because the decision tree favours the least operational responsibility, "build on raw Azure infrastructure" is never the default answer.
</div>

---

## Grounding Data Quality — ARTCA Dimensions

### Key Concept

**Grounding data is only as good as its weakest dimension: accuracy, relevance, timeliness, cleanliness or availability.**

This section gives five checks to run before data goes into a RAG index. Each catches a different failure: wrong facts, off-topic content, stale values, noisy duplicates and encoding junk, or sources the indexer can't reach.

Which dimension matters most depends on the data: fast-changing values such as prices and stock put timeliness first, while policy documents put accuracy and relevance first. **Think of it like stocking a pharmacy: a correctly labelled drug that has expired is still a bad dispense.**

When evaluating data for RAG knowledge bases, assess five dimensions:

| Dimension | Description | Key Question |
|-----------|-------------|--------------|
| **Accuracy** | Data correctly represents the real world | Do product descriptions match physical attributes? |
| **Relevance** | Data is pertinent to user queries | Is this content useful for the agent's domain? |
| **Timeliness** | Data is current within acceptable staleness thresholds | How often does this data change? Is today's data required? |
| **Cleanliness** | Data is free of duplicates, errors, encoding issues | Are there HTML artifacts, encoding problems, duplicates? |
| **Availability** | Data is accessible to the retrieval pipeline | Can the indexer reach this source? What are the access controls? |

> **Exam tip**: For real-time data (prices, inventory, stock levels), **Timeliness** is typically the most critical dimension to evaluate first.

### In Practice

**What breaks without this**: The agent answers from a price list indexed overnight, quotes yesterday's prices, and customers hold the company to them.

**Decision trigger**: Ask: how fast does this data change compared with how often we index it, and can the indexer reach it with the right access controls?

**When you'd choose differently**: For real-time values, don't index them at all: call the source system through a tool or connector at query time, so timeliness is solved by design.

### Exam Trap ⚠️

<div class="note-trap">
Poor answers are often blamed on the model or the chunking when the root cause is the data. And availability includes access control: if the indexer can't reach a source, or the users shouldn't see it, it isn't usable grounding data.
</div>

---

## AI Center of Excellence (CoE)

### Key Concept

**The AI CoE enables and governs AI across the enterprise; business units own and run their own use cases.**

This section splits responsibilities. The CoE sets approved models and data constraints, maintains the prompt library and shared infrastructure, defines evaluation gates, runs responsible AI reviews and drives AI literacy.

Business units define requirements and success metrics, operate their production agents, and supply domain data and output review. **Think of the CoE as a city's building-standards office: it writes the code and inspects the work, but each owner designs their own building.**

The AI CoE owns enterprise-wide AI enablement — distinct from business units that own specific use cases:

**CoE Responsibilities:**
- Define approved AI models and their data classification constraints
- Maintain the enterprise prompt library (versioned, curated templates)
- Own shared infrastructure (Foundry resources, observability, security baselines)
- Establish evaluation frameworks and quality gates
- Run responsible AI reviews and publish Transparency Notes
- Drive AI literacy and training programs

**Business Unit Responsibilities:**
- Define use case requirements and success metrics
- Operate production agents for their domain
- Provide domain-specific training data and review outputs

### In Practice

**What breaks without this**: Without a CoE, every team runs its own model approvals and evaluations and standards drift apart; with a CoE that tries to own everything, it becomes a bottleneck and use cases stall in its queue.

**Decision trigger**: Ask: is this a shared standard or platform (CoE), or a requirement for one business process (business unit)?

**When you'd choose differently**: A small organisation with one or two AI use cases may give CoE duties to an existing IT or data governance team rather than set up a separate body.

### Exam Trap ⚠️

<div class="note-trap">
The CoE does NOT write business requirements for individual use cases — that belongs to the business unit.
</div>

---

## Foundry Model Router

### Key Concept

**Model router is a deployable model that picks the right model for each prompt, so you don't have to build the routing logic yourself.**

Model router in Microsoft Foundry is a trained language model that you deploy like any other model. It analyses each prompt in real time (complexity, reasoning, task type) and sends it to a suitable underlying model from OpenAI, Anthropic, xAI, DeepSeek, Meta and others. You call one deployment; it chooses per request, and it fails over automatically to the next most suitable model if one has a transient problem. Claude models must be deployed separately before the router can use them.

You tune it with two settings. **Routing mode**: Balanced (default) picks the cheapest model within a small quality band (about 1–2%) of the best model for that prompt; Cost widens the band (about 5–6%) to save more; Quality ignores cost and picks the highest-rated model. **Model subset** limits which models it may route to, and that subset is also the failover set, so pick at least two. **Think of it as a dispatcher who reads every ticket and assigns it to the cheapest technician who can fix it properly.**

### In Practice

**What breaks without this**: Every request goes to the largest model, so simple classifications cost as much as multi-step reasoning, or a hand-built classifier drifts out of date as new models ship.

**Decision trigger**: Ask: is my traffic a mix of easy and hard prompts, and would I accept a router choosing the model per request? If yes, evaluate model router against your current baseline before switching.

**When you'd choose differently**: If you need very long contexts, remember the router's effective context window is that of its **smallest** underlying model, so either restrict the subset to large-context models or keep a dedicated deployment. If every request must hit one validated model (for regulatory reasons), use that model directly.

### Exam Trap ⚠️

<div class="note-trap">
"Model router" on AB-100 means the Foundry feature, not a classifier you write. Watch for: context-length errors (smallest model limits the window → use a model subset), "only approved models" (model subset, which Azure Policy can also govern), and "high-volume, budget-sensitive" (Cost mode). Round-robin load balancing behind API Management is not model routing.
</div>

---

## ROI and TCO Analysis

### Key Concept

**ROI compares net benefit with total investment over the same period, and TCO must count every cost, not just tokens.**

This section gives the formula and the cost categories. Net benefit is savings plus revenue uplift minus ongoing costs; total investment covers implementation, platform, training and operations over the same period, often three years.

The TCO table lists six categories, from Azure infrastructure to ongoing operations, and the usual mistake is to count only AI service costs. **Think of buying a car: the sticker price is only the start, and fuel, insurance and servicing decide what it really costs.**

#### ROI Calculation Framework

`
ROI (%) = (Net Benefit over Period / Total Investment over Period) × 100

Net Benefit = Cost Savings + Revenue Uplift - Ongoing Costs
Total Investment = Implementation + Platform + Training + Operations (3-year)
`

#### TCO Components for AI Solutions

| Category | Examples |
|----------|---------|
| **Azure infrastructure** | Compute, storage, networking, Key Vault |
| **AI service costs** | OpenAI tokens/PTU, AI Search query units, Content Safety |
| **Licensing** | Copilot Studio per-session, M365 Copilot per-user, D365 |
| **Implementation** | Development, integration, testing (often the largest initial cost) |
| **Training & change management** | User training, documentation, adoption programs |
| **Ongoing operations** | Monitoring, knowledge base refreshes, model updates, evaluation |

> **Exam tip**: Candidates often underestimate implementation and ongoing operations costs. A complete TCO captures all six categories above.

### In Practice

**What breaks without this**: The business case counts token costs only; the project goes ahead, and knowledge-base refreshes, evaluation runs and change management turn the projected saving into a loss in year two.

**Decision trigger**: Ask: have we costed all six TCO categories over the same period as the benefits?

**When you'd choose differently**: For a short feasibility pilot, a rough cost estimate is enough; the full multi-year TCO matters when you ask for production funding.

### Exam Trap ⚠️

<div class="note-trap">
Mixing periods, such as year-one cost against three-year savings, inflates ROI. And tokens are rarely the biggest number: implementation is often the largest initial cost.
</div>

---

## Build-Buy-Extend Decision Framework

### Key Concept

**Build only where the process differentiates you; buy or extend for commodity processes.**

This section compares three routes on differentiation, time-to-value, TCO and integration. Building gives full control but carries the highest maintenance burden; buying SaaS is fastest for standard processes; extending Microsoft 365 or Dynamics 365 suits processes that already live there.

The decision rule is about where your value comes from, not about what is technically possible. **Think of a restaurant: cook your signature dishes yourself, but buy the bread.**

| Factor | Build Custom | Buy SaaS | Extend Platform (M365/D365) |
|--------|-------------|---------|---------------------------|
| **Differentiation** | Process is a core competency | Commodity process | Standard process in Microsoft ecosystem |
| **Time-to-value** | 3-12 months | Days-weeks | 1-4 weeks |
| **TCO** | Highest (maintenance burden) | Subscription cost | Medium (licensing + config) |
| **Integration** | Full control | API-limited | Native M365/D365 integration |
| **When to choose** | True differentiator, no solution exists | Standard process, data in SaaS | Process lives in M365/D365 surfaces |

> **Decision rule**: For commodity processes (invoice processing, meeting summarization), prefer Buy or Extend. Build only when differentiation justifies the investment.

### In Practice

**What breaks without this**: A team builds a custom meeting-summary agent that Microsoft 365 Copilot already provides, then spends its budget maintaining it instead of on the process that differentiates the business.

**Decision trigger**: Ask: would a competitor gain an edge from this capability, and does an existing product already cover most of it?

**When you'd choose differently**: If a commodity process has compliance or integration requirements no product meets, building or heavily extending can still be the right call.

### Exam Trap ⚠️

<div class="note-trap">
"Build" isn't automatically the most capable answer; it's usually the most expensive. When a scenario describes a commodity process whose data already lives in Microsoft 365 or Dynamics 365, Extend is usually the answer.
</div>

---

## Small Language Models (SLMs)

### Key Concept

**Small language models win on narrow tasks, tight latency, local deployment and cost; they lose on broad knowledge.**

This section lists when a small model such as Phi beats a large general model: a narrow domain with training data, strict latency, data that must stay on-premises, edge devices, and cost at scale.

The trade-off is capability: a small model has less world knowledge and weaker multi-step reasoning, so it must be matched to a narrow, well-defined task. **Think of an SLM as a torque wrench: better than a whole toolbox for one job, and no use for the rest.**

SLMs (e.g., Phi-3-mini, Phi-3-medium, Phi-3.5) are preferable to large general models when:

| Condition | Rationale |
|-----------|-----------|
| **Narrow domain with training data** | Fine-tuned SLM can outperform GPT-4o on specific tasks |
| **Strict latency requirements** | SLMs inference 2-5× faster than large models |
| **Data sovereignty / on-premises** | SLMs run on local hardware — data never leaves the network |
| **Edge deployment** | SLMs fit on constrained devices (laptops, IoT) |
| **Cost sensitivity at scale** | SLMs cost 10-50× less per token than GPT-4o |

### In Practice

**What breaks without this**: An SLM is deployed as an open-ended assistant, and questions outside its narrow domain get confident, wrong answers.

**Decision trigger**: Ask: is the task narrow and repeatable, and do latency, cost or data location rule out a large cloud model?

**When you'd choose differently**: When the task needs broad knowledge or long multi-step reasoning, use a large model and control cost with routing, caching or batch processing instead.

### Exam Trap ⚠️

<div class="note-trap">
SLMs are NOT universally superior. They fail on tasks requiring broad world knowledge or complex multi-step reasoning that was not in their training data.
</div>

---

## Prompt Library

### Key Concept

**A prompt library is a curated, versioned set of proven prompt templates owned by the AI CoE.**

This section describes what goes into it: task templates, domain templates, notes on why each template works, guidance for adapting it, and version history with performance metrics.

Its value is consistency: the same task gets the same quality across teams without every user becoming a prompt engineer. **Think of it as the organisation's recipe book: tested recipes, with notes on what you can substitute.**

An enterprise prompt library is a **centralized, curated, versioned collection** of proven prompt templates maintained by the AI CoE:

**Contents:**
- Task templates (meeting summary, email draft, code review, data analysis)
- Domain-specific templates (legal contract review, HR policy lookup, financial analysis)
- Annotation on what makes each template effective
- Guidelines for adaptation per task variant
- Version history and performance metrics

**Benefits:**
- Democratizes best practices without requiring all users to become prompt engineers
- Reduces inconsistency — same task, same quality across the organization
- Reduces token waste from poorly structured prompts

> **Exam tip**: A prompt library is an organizational asset owned by the AI CoE — not a feature of the Azure platform.

### In Practice

**What breaks without this**: Each team writes its own prompt for the same task, quality varies widely, and an improvement found by one team never reaches the others.

**Decision trigger**: Ask: is more than one team writing prompts for the same kind of task? If yes, the template belongs in the library.

**When you'd choose differently**: Agent instructions that ship with an agent belong in source control and the deployment pipeline alongside the agent (see D3 ALM); the library is for shared, reusable templates.

### Exam Trap ⚠️

<div class="note-trap">
A prompt library isn't a one-off wiki page: without versions and performance metrics, nobody can tell which template works best or roll back a bad change.
</div>

---

## Foundry Deployment Types and Data Residency

### Key Concept

**Where a model runs your prompt is set by the deployment type, not by the region of the resource.**

Every Foundry model deployment (serverless API) has a deployment type with three dimensions: where data is processed, how you pay, and how predictable latency is. Data at rest always stays in the resource's Azure geography, but inference differs: **Global** types may process prompts in any Azure region; **Data Zone** types process only inside a Microsoft-defined zone (US, EU or Asia Pacific — the EU zone follows the EU Data Boundary); **Standard** and **Regional Provisioned** process within the customer-chosen Azure geography. Each comes in pay-per-token or provisioned (PTU) form, plus **Batch** (asynchronous, 50% cheaper than Global Standard, 24-hour target) and **Developer** (fine-tuned model evaluation only: 24-hour lifetime, no SLA, no residency guarantee).

Microsoft's default advice is to start with **Global Standard** — newest models first, lowest price, broadest regions, highest quota — and move only for a reason: residency (Data Zone or Standard), reserved throughput and low latency variance (provisioned), or large offline jobs (Batch). Azure Policy can block deployment types you don't allow, such as GlobalStandard in an EU-only subscription. **Think of the resource region as where your filing cabinet sits, and the deployment type as which offices are allowed to read the files.**

### In Practice

**What breaks without this**: A team creates its resource in West Europe, picks Global Standard because it's the default, and EU prompts are processed outside the EU — a residency breach nobody notices until audit.

**Decision trigger**: Ask: does any rule restrict where prompts may be processed? If yes, choose Data Zone or Standard and enforce it with Azure Policy. If not, ask whether traffic is steady (provisioned), bursty (Standard types) or offline (Batch).

**When you'd choose differently**: If the newest model you need is only available as Global at launch (new models arrive Global first, then Data Zone, then geography-based), you may have to wait or choose another model rather than relax a residency rule.

### Exam Trap ⚠️

<div class="note-trap">
"The resource is in West Europe, so data stays in the EU" is the classic wrong answer. Region controls data at rest; the deployment type controls processing. Also: Developer deployments carry no data-residency guarantee, and Batch is the answer when nobody is waiting on individual responses.
</div>

---

## Foundry Agent Types: Prompt Agents vs Hosted Agents

### Key Concept

**Choose a prompt agent when configuration is enough, and a hosted agent when you need your own code.**

Foundry Agent Service offers three agent types. A **prompt agent** is defined entirely by configuration — instructions, a model and tools — and Foundry runs it with no application code, containers or packages to maintain; you can author it in the portal or define it in code for CI/CD. A **voice-based prompt agent** adds managed real-time voice through Voice Live. A **hosted agent** is your own code — Microsoft Agent Framework, LangGraph, the OpenAI Agents SDK, the Anthropic Agent SDK or custom code — shipped as a container image or source .zip, which Foundry runs with a managed endpoint, autoscaling, a dedicated Microsoft Entra identity and observability.

You can also skip the agent resource entirely and call the **Responses API** from your own app (an "ephemeral agent"), keeping the agent definition in your codebase. All paths share Foundry models, tools, guardrails and tracing. **A prompt agent is a fully furnished rental; a hosted agent is your own furniture moved into a managed building.**

### In Practice

**What breaks without this**: Teams containerise simple FAQ agents and inherit scaling, patching and security work they didn't need — or try to force custom orchestration into configuration and hit a wall.

**Decision trigger**: Ask: does the agent need to run code I wrote (custom orchestration, a framework, custom protocols)? Yes → hosted agent. No → prompt agent.

**When you'd choose differently**: If the business team owns the agent and wants low-code authoring inside Microsoft 365, Copilot Studio is usually a better fit than either Foundry agent type.

### Exam Trap ⚠️

<div class="note-trap">
"Prompt agents can run any framework's code" is false — that's what hosted agents are for. And "Foundry can't host LangGraph" is also false.
</div>

---

## Deep Dive: Making D1 Click

### 1. The connective narrative

Domain 1 is about decisions you make before anyone builds anything, and they chain together. You start from the business problem and ask whether an agent is even the right tool: rules-based work suits automation, prediction suits a trained model, and agents earn their place when a task needs language understanding, multi-step reasoning and tool use. Then you check the data, because an agent grounded on stale or dirty data fails confidently. Accuracy, relevance, timeliness, cleanliness and availability decide whether grounding can work at all.

Next comes the platform choice, and CAF gives the rule that settles most arguments: pick the option that meets the requirement with the **least operational responsibility**. Extending Microsoft 365 Copilot or using a prebuilt agent beats building; Copilot Studio beats Foundry when low-code is enough; Foundry beats raw infrastructure. Inside Foundry the same logic repeats: prompt agent before hosted agent, Global Standard before anything more specialised, model router before a hand-built classifier.

Finally, the money and the rules. ROI needs a full TCO — licensing and consumption (Copilot Credits, tokens, PTUs), implementation, change management and operations — and constraints such as data residency, RBAC scope and responsible AI requirements can overturn a choice that looked cheapest. A good D1 answer is the cheapest option that still satisfies every stated constraint.

### 2. Worked scenario

> **Scenario.** An EU insurer wants an agent that summarises 2 million archived claim notes once, then answers adjusters' questions interactively. All processing must stay in the EU, and the CFO wants a cost-conscious design.
>
> **Step 1 — split the workload.** The archive job is offline (nobody waits on a single summary); the adjuster agent is interactive and bursty. One deployment type can't be optimal for both.
>
> **Step 2 — apply residency first.** Global types may process anywhere, so they're out for both parts. That leaves Data Zone (EU) or Standard types.
>
> **Step 3 — pick per workload.** The archive job goes to **Data Zone Batch**: same 50% batch discount and 24-hour target as Global Batch, but processing stays in the EU zone. The adjuster agent uses **Data Zone Standard**: pay-per-token suits bursty traffic, with higher quota than geography-based Standard.
>
> **Step 4 — control model cost.** For the interactive agent, evaluate Foundry model router (Data Zone Standard is supported) in Balanced mode with a model subset of approved models, against a single-model baseline.
>
> **Step 5 — lock it in.** Use Azure Policy to deny Global deployment types in the subscription, so nobody "fixes" a quota problem by switching to Global later.
>
> **Outcome:** two deployment types, one residency rule enforced by policy, and a cost model the CFO can check: batch at half price, interactive on pay-per-token with routing.

### 3. Memory aid

**LORD** — the order to settle a D1 design question:
- **L**east operational responsibility (CAF: extend or buy before build; Copilot Studio before Foundry before infrastructure)
- **O**bligations (residency, EU AI Act tier, GDPR, RBAC scope)
- **R**OI with full TCO (licensing, consumption, implementation, change management, operations)
- **D**eployment shape (agent type, deployment type, model router, PTU vs pay-per-token)

### 4. Exam strategy for this domain

- D1 is the largest domain from November 16, 2026 (35–40%), so expect many scenario questions that hinge on one constraint buried in the stem: team skills, residency, "no custom code", or "only approved models".
- Distractors often use absolute language ("always build", "PTU from day 1", "choosing the region guarantees residency"). Absolutes are usually wrong.
- The exam rewards the managed, least-effort option that still meets every constraint, and punishes over-engineering.
- Five minutes before the exam: **read the constraint first, then pick the lightest Microsoft option that satisfies it.**

---

## Updated Exam Quick Reference (Domain 1 — November 2026 Syllabus)

| Topic | Key Decision / Rule |
|-------|-------------------|
| CAF AI adoption | AI strategy → plan → ready → govern, secure, manage |
| Grounding data | Evaluate ARTCA: Accuracy, Relevance, Timeliness, Cleanliness, Availability |
| AI CoE | Owns standards, shared infra, prompt library — NOT use case BRDs |
| Model router | Foundry model router: Balanced (default), Cost, Quality modes; model subset; context = smallest model |
| ROI | 3-year TCO includes: infra + AI services + licensing + impl + training + ops |
| Build-Buy-Extend | Commodity process → Buy or Extend; Differentiator → Build |
| SLMs | Prefer when: narrow domain + training data + latency/cost/sovereignty constraints |
| Prompt library | Centralized, versioned, CoE-owned collection of proven templates |
| Multi-agent platforms | M365 Copilot (extend) → Copilot Studio (low-code) → Microsoft Foundry (pro-code) |
| Deployment types | Global = any region; Data Zone = within EU/US/APAC zone; Standard = within geography; Batch = 50% off, 24-hour target |
| Foundry agent types | Prompt agent = configuration only; hosted agent = your code/framework in a Foundry-run container |
