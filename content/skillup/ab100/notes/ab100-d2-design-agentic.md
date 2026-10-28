# D2: Design Agentic AI Solutions

> **Exam weight**: 30–35% (skills measured as of November 16, 2026; 25–30% before that date)

## Overview

Domain 2 is the technical design domain — it covers how to architect multi-agent systems using Microsoft Foundry, Foundry Agent Service, Copilot Studio, and Microsoft Agent Framework (the successor to AutoGen and Semantic Kernel). It tests your ability to choose orchestration patterns, design memory and tool layers, and wire agents together correctly.

---

## Orchestration Patterns

### Key Concept

**Use one agent until the task's shape forces you to split it, then match the multi-agent pattern to that shape.**

This section starts with the single-versus-multi decision. A single agent is simplest when the work is sequential and fits in its context; parallel sub-tasks across independent domains justify parallel agents, and dependent steps justify a sequential pipeline.

The pattern table then names the shapes: sequential, parallel, hierarchical, debate and Magentic, each suited to a different kind of dependency between steps. **Think of it like staffing a job: one person if one person can do it, and a team only when the work genuinely splits.**

#### Single-Agent vs Multi-Agent Decision

![Flow diagram for "Key Concept": No, Yes, Task, Parallelizablesub-tasks?, Fits incontext window?, Single Agent, Coordinator + Memory, Independentdomains?, Multi-AgentParallel, SequentialPipeline](/content/skillup/ab100/images/ab100-d2-design-agentic-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab100/ab100-d2-design-agentic-m1.mmd -->

#### Multi-Agent Patterns

| Pattern | Structure | When to Use |
|---------|-----------|-------------|
| **Sequential** | A → B → C | Each step depends on previous output |
| **Parallel** | A → [B, C, D] → Merge | Independent subtasks, reduce latency |
| **Hierarchical** | Coordinator → [Specialist A, B] | Domain specialization + routing |
| **Debate** | Agent A ↔ Agent B → Critic | Improve accuracy via adversarial review |
| **Magentic** | Manager agent + specialists (web, file, coder); grew out of AutoGen's Magentic-One | Open-ended research tasks |

### In Practice

**What breaks without this**: A team splits a simple FAQ flow into five agents; every answer now takes several model calls, latency triples, and failures are hard to trace across hand-offs.

**Decision trigger**: Ask: are there sub-tasks that can run independently, or domains that need different tools and instructions? If neither, keep one agent.

**When you'd choose differently**: When one agent's tool list or instructions grow so large that it starts picking the wrong tool, splitting into a coordinator and specialists can help even if the work is sequential.

### Exam Trap ⚠️

<div class="note-trap">
Magentic orchestration (from AutoGen's Magentic-One) is NOT the same as generic multi-agent. It's a **specific pattern** in which a manager agent plans and coordinates specialists for open-ended web/file/code tasks. Use it when the task is: unstructured, requires browsing + coding + file operations. Do NOT use it for structured business workflows — hierarchical coordinator pattern is correct there.
</div>

---

## Foundry Agent Service

### Key Concept

**Foundry Agent Service runs your agents; you choose how much of the agent is configuration and how much is your own code.**

Foundry Agent Service (formerly Azure AI Agent Service) hosts and scales agents in Microsoft Foundry. The current version (Agents v2) is built on the **Responses API**, so the old Assistants terms have been replaced: threads, messages, runs and assistants are now **conversations, items, responses and agent versions**. Agents come in three types — **prompt agents** (instructions, model and tools, fully managed), **voice-based prompt agents** (real-time voice through Voice Live) and **hosted agents** (your own code or framework in a Foundry-run container) — and every agent change is snapshotted as a version you can compare or roll back to.

Agents act through **tools**: built-in ones such as web search, file search, code interpreter and memory, plus your own functions, OpenAPI specs and MCP servers. A **toolbox** curates a set of tools once and exposes them to many agents through one managed MCP-compatible endpoint, with central authentication, governance and versioning. Each agent can have its own Microsoft Entra identity, run inside your virtual network, use guardrails against prompt injection, publish to Microsoft Teams and Microsoft Copilot, and talk to other agents over the **A2A** protocol (v1.0 is generally available). **Think of the service as an airport: prompt agents are passengers on scheduled flights, hosted agents are private jets using the same runways, towers and security.**

![Flow diagram for "Key Concept": tool call, response, User or app, Conversationitems, Agent versioninstructions + model + tools, Toolbox / tools, File search, Code interpreter, Web search, MCP servers / functions /OpenAPI](/content/skillup/ab100/images/ab100-d2-design-agentic-m2.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab100/ab100-d2-design-agentic-m2.mmd -->

### In Practice

**What breaks without this**: Teams copy tool configuration into every agent, rotate credentials five times, and lose track of which agent version is live when an instruction change causes a regression.

**Decision trigger**: Ask: is this agent configuration-only (prompt agent) or does it need my code (hosted agent)? Do several agents share tools (toolbox)? Does another platform's agent need to call it (A2A endpoint)?

**When you'd choose differently**: If you already run agent code elsewhere and just want Foundry models and tools, call the Responses API directly and keep the agent definition in your app instead of creating an agent resource.

### Exam Trap ⚠️

<div class="note-trap">
Older material talks about threads, runs and the Assistants API. On current Foundry Agent Service, the equivalents are conversations, items and responses, and agents are versioned. If a question asks how to undo a bad instruction change quickly, the answer is rolling back to the previous agent version, not rebuilding the agent.
</div>

---

## Copilot Studio Design

### Key Concept

**A Copilot Studio agent answers through topics, tools and knowledge; orchestration mode decides how it picks between them.**

This section shows the building blocks. Topics are authored conversation flows, actions and plugins call flows and external APIs (current Copilot Studio groups connectors, flows, REST APIs, prompts and MCP servers as tools), knowledge sources ground generative answers, and adaptive cards render rich replies.

Under classic orchestration the agent picks the topic whose trigger phrases best match the query and falls back to knowledge; under generative orchestration, the default for new agents, it picks topics, tools, other agents and knowledge by their descriptions and can combine several in one answer. **Think of classic orchestration as a phone menu and generative orchestration as a receptionist who reads the request and calls the right people.**

#### Copilot Studio Architecture

![Flow diagram for "Key Concept": Matched, No match, UserTeams/Web/Custom, Copilot, Topicmatching, Topic Flow, Fallback / Generative AI, Knowledge SourceSharePoint/URLs/Dataverse, ActionsPower Automate flows, External APIsHTTP connector](/content/skillup/ab100/images/ab100-d2-design-agentic-m3.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab100/ab100-d2-design-agentic-m3.mmd -->

#### Topics vs Actions vs Plugins

| Concept | Purpose | Trigger |
|---------|---------|---------|
| **Topic** | Conversation flow for a specific intent | User phrase matching |
| **Action (flow)** | Call Power Automate or external API | Within a topic |
| **Plugin** | Expose external API as tool | AI-driven selection |
| **Knowledge source** | Add docs/URLs to generative answers | Fallback or explicit |
| **Adaptive card** | Rich response in Teams/Web | Within topic |

### In Practice

**What breaks without this**: An agent switched to generative orchestration keeps vague topic and tool descriptions, so it calls the wrong tool or two overlapping topics compete unpredictably.

**Decision trigger**: Ask: which orchestration mode is the agent using? Under classic, fix trigger phrases; under generative, fix names and descriptions of topics, tools and knowledge.

**When you'd choose differently**: For a tightly scripted, regulated dialogue where every path must be predictable, classic orchestration with explicit topics may be the safer choice.

### Exam Trap ⚠️

<div class="note-trap">
In Copilot Studio, **generative answers** (the fallback AI response) and **topics** (explicit flow) are DIFFERENT. Generative answers search knowledge sources. Topics override generative answers when a phrase is matched (that's classic orchestration; under generative orchestration the agent chooses topics by their descriptions and can search knowledge proactively). The exam tests whether you know which one activates for a given input.
</div>

---

## Microsoft Agent Framework

### Key Concept

**Microsoft Agent Framework is the successor to both AutoGen and Semantic Kernel, and it gives you five ready-made ways to orchestrate several agents.**

Agent Framework (for .NET and Python, with Go in public preview) combines AutoGen's simple agent abstractions with Semantic Kernel's enterprise features — session state, type safety, middleware and telemetry — and adds graph-based **workflows** for explicit control of execution paths. Its rule of thumb: use an **agent** when the task is open-ended or conversational, a **workflow** when the process has well-defined steps, and plain code if a function can do the job.

For multi-agent work it provides built-in orchestration patterns: **Sequential** (agents run one after another in a fixed order), **Concurrent** (agents run in parallel), **Handoff** (agents transfer control to each other based on context), **Group Chat** (agents collaborate in a shared conversation) and **Magentic** (a manager agent dynamically coordinates specialists). Orchestrations support human-in-the-loop through approval-required tools that pause the workflow. **Pick the pattern the way you'd staff a project: an assembly line, a parallel team, a relay, a meeting, or a project manager with specialists.**

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

agent = Agent(
    client=FoundryChatClient(
        project_endpoint="https://your-foundry-service.services.ai.azure.com/api/projects/your-foundry-project",
        model="gpt-5.4-mini",
        credential=AzureCliCredential(),
    ),
    name="HelloAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
)
result = await agent.run("What is the largest city in France?")
```

| Pattern | Order of work | Who owns the conversation | Use when |
|---------|---------------|---------------------------|----------|
| Sequential | Fixed, one after another | The pipeline | Each step needs the previous output |
| Concurrent | Parallel | Aggregator | Independent sub-tasks, lower latency |
| Handoff | Decided by agents | Whoever receives the handoff | Triage to the right specialist |
| Group Chat | Turn by turn | Shared conversation | Collaboration or review between agents |
| Magentic | Planned by a manager | The manager | Open-ended tasks with unknown steps |

### In Practice

**What breaks without this**: A fixed two-step pipeline built as a free-form group chat costs extra model calls and occasionally runs steps in the wrong order; a triage system built as a sequence drags every customer through every specialist.

**Decision trigger**: Ask two questions: is the order of work known in advance (sequential or concurrent), and who should own the conversation afterwards (handoff gives it away; Magentic keeps a manager in charge)?

**When you'd choose differently**: If the business team owns the solution and wants low-code orchestration, Copilot Studio's generative orchestration with connected agents may be simpler than code-first Agent Framework.

### Exam Trap ⚠️

<div class="note-trap">
AutoGen class names such as RoundRobinGroupChat and SelectorGroupChat belong to the older framework. AB-100 questions now describe Agent Framework patterns. "Fixed order" means Sequential; "pass the customer to the right specialist, who takes over" means Handoff; "manager plans an open-ended task" means Magentic.
</div>

---

## Memory Architecture

### Key Concept

**Match each kind of agent memory to a store with the right lifetime: context, session, history or knowledge.**

This section maps memory tiers to Azure services. The context window holds the current turn; Azure Cache for Redis holds short-lived session state and tool results; Cosmos DB holds conversation history and preferences for days or months; Azure AI Search holds long-lived knowledge as vectors.

The design rule is lifetime and access pattern: fast and short for session state, durable and queryable for history, searchable for knowledge. **Think of it as a desk, a filing cabinet and a library: what you are working on, what you have done, and what you can look up.**

#### Memory Tiers for Agents

![Flow diagram for "Key Concept": Long-term Memory, Short-term Memory, Working Memory, in-context, persist/retrieve, RAG retrieval, Context WindowCurrent conversation, Azure Cache for RedisSession state, tool results, Cosmos DBConversation historyUser preferences, Azure AI SearchVector embeddingsKnowledge base](/content/skillup/ab100/images/ab100-d2-design-agentic-m4.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab100/ab100-d2-design-agentic-m4.mmd -->

| Memory Type | Azure Service | TTL | Use For |
|-------------|--------------|-----|---------|
| In-context | Token window | Request lifetime | Current turn reasoning |
| Working | Azure Cache for Redis | Minutes | Multi-turn session state |
| Episodic | Cosmos DB (NoSQL) | Days/months | Conversation history |
| Semantic | Azure AI Search (vector) | Persistent | Knowledge retrieval |

### In Practice

**What breaks without this**: Everything is kept in the context window, so long conversations hit token limits, cost rises with every turn, and the agent forgets the user's preferences the next day.

**Decision trigger**: Ask, for each piece of state: how long must it live, who needs to read it, and must it be searchable by meaning?

**When you'd choose differently**: If you build on Foundry Agent Service, conversations persist history for you and the built-in memory tool can cover long-term memory, so you may not need to run Redis and Cosmos DB yourself.

### Exam Trap ⚠️

<div class="note-trap">
Redis is short-term working memory, not the place for long-term history or knowledge; and a vector index is for retrieval by meaning, not a transactional store for session state. Long-term memory that must be deleted on request also falls under GDPR erasure.
</div>

---

## RAG Pipeline Design in Microsoft Foundry

### Key Concept

**Production RAG needs good chunks, hybrid search and semantic reranking, not vector search alone.**

This section walks the pipeline. Documents are chunked and embedded into an Azure AI Search index holding both vectors and keywords; at query time hybrid search combines vector similarity with BM25 keyword matching, the semantic ranker re-scores the top results, and the best chunks are injected into the prompt.

Chunking decides what can be retrieved at all: fixed-size for uniform documents, sentence or semantic for prose and long technical documents, hierarchical when you need both summary and detail. **Think of chunking as cutting a book into index cards: cut badly and the answer is split across two cards nobody retrieves together.**

#### Full RAG Architecture

![Flow diagram for "Key Concept": Source DocumentsPDF/Word/HTML, Chunkingindexing pipeline, Embedding Modeltext-embedding-3-large, Azure AI SearchVector + Keyword Index, User Query, Query Embedding, Hybrid SearchVector + BM25, Semantic RerankingAzure AI Search, Context injectioninto prompt, LLM Response](/content/skillup/ab100/images/ab100-d2-design-agentic-m5.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab100/ab100-d2-design-agentic-m5.mmd -->

#### Chunking Strategies

| Strategy | Chunk Size | Best For |
|----------|-----------|----------|
| Fixed-size | 512 tokens | Uniform documents |
| Sentence-based | Variable | Prose, documentation |
| Semantic | Variable (topic boundary) | Long technical docs |
| Hierarchical | Parent + child chunks | Summary + detail retrieval |

#### Hybrid Search (Recommended)
- **Vector search**: semantic similarity (finds "similar meaning")
- **Keyword (BM25)**: exact term matching (finds "exact words")
- **Semantic reranker**: re-scores top-N results using a cross-encoder model
- Always use hybrid + reranker for production — pure vector search misses exact terminology

### In Practice

**What breaks without this**: A pure vector index misses exact product codes and error numbers, so the agent answers a question about "error 0x80070005" with a document about a different error.

**Decision trigger**: Ask: do users search with exact terms (codes, names, IDs) as well as natural language? If yes, use hybrid search plus the semantic ranker.

**When you'd choose differently**: For small, stable knowledge sets in Copilot Studio or a Foundry prompt agent, built-in knowledge or file search may be enough without designing your own index.

### Exam Trap ⚠️

<div class="note-trap">
"Vector search is always better than keyword search" is wrong: vectors find similar meaning, BM25 finds exact words, and production designs use both. Reranking re-orders what retrieval returned; it can't recover a chunk that was never retrieved.
</div>

---

## Prompt Flow (Retiring) and Its Replacement

### Key Concept

**Prompt flow is being retired on April 20, 2027; new orchestration work belongs in Microsoft Agent Framework.**

Prompt flow in Microsoft Foundry and Azure Machine Learning is no longer recommended for new development, its container images no longer receive updates, and after April 20, 2027 the authoring experience, VS Code extensions and runtime images won't be supported or available. It isn't available in the new Foundry portal at all — only in Foundry (classic). Microsoft's migration path maps each prompt flow concept onto Agent Framework: a flow becomes a `WorkflowBuilder` graph, nodes become executors, LLM nodes become agents, conditional nodes become conditional edges, parallel nodes become fan-out and fan-in edges, and evaluation flows become Azure AI Evaluation SDK evaluators.

The migration has five gated steps: audit and map every node, rebuild, validate parity by running both versions side by side and scoring with evaluators (the guide suggests a mean similarity of at least 3.5 out of 5), migrate operations (tracing, deployment, a CI quality gate), then cut over and decommission. Agent Framework is code-first, so teams that relied on the visual editor need to plan for that. **It's like moving house before the lease ends: pack room by room, check everything arrived, then hand back the keys.**

### In Practice

**What breaks without this**: Flows keep "working" until the retirement date, then the platform they run on disappears, with no security updates to the runtime images in the meantime.

**Decision trigger**: Ask: does anything in production depend on prompt flow deployments or runtime images? If yes, plan the Agent Framework migration and parity testing now.

**When you'd choose differently**: If the flow was a simple prompt-plus-retrieval chain with no custom code, a Foundry prompt agent with file search may replace it with no code at all.

### Exam Trap ⚠️

<div class="note-trap">
There's no automatic converter from prompt flow YAML to the new portal, and existing deployments don't keep running indefinitely. Answers that say "keep using prompt flow" or "import the flow into the new portal" are wrong.
</div>

---

## Cheat Sheet 📋

| Concept | Key Rule |
|---------|----------|
| Magentic | Manager agent plans open-ended tasks: browse + code + files; NOT for structured workflows |
| Hierarchical pattern | Use when routing decisions require reasoning about task type |
| Conversation vs response | Foundry Agent Service (v2): conversation holds items; each response is one execution (replaces threads/runs) |
| Code Interpreter | Executes Python in a sandbox — use for data analysis, not arbitrary code |
| Copilot Studio trigger | Topics fire on phrase match; generative answers are the fallback |
| RAG: hybrid search | Always use vector + BM25 + semantic reranker for production |
| Chunking: semantic | Best for long technical documents with topic boundaries |
| Memory: Redis | Working memory / session state (minutes TTL) |
| Memory: AI Search | Knowledge base / long-term semantic retrieval |
| Sequential vs Handoff | Sequential = fixed order; Handoff = agents transfer control based on context |


---

## Model Context Protocol (MCP) in Copilot Studio

### Key Concept

**MCP lets a Copilot Studio agent use an external server's tools and resources through one open, self-describing protocol.**

This section explains the mechanism. An MCP server publishes tools the model can call and resources the agent can read; you connect it to an agent with the MCP onboarding wizard, generative orchestration must be on, and changes on the server appear in the agent automatically.

The comparison table sets MCP against a custom Power Platform connector: MCP suits systems that already have a server, tools shared by many agents and standard discovery; a connector suits single integrations and the certified connector ecosystem. **Think of MCP as a universal power socket: build the plug once, and any compatible appliance can use it.**

MCP allows Copilot Studio agents to connect to external systems that expose a standardized MCP server interface:

**How it works:**
1. Use an existing MCP server or create one that wraps an external API or system
2. The MCP server publishes **tools** (functions the model can call) and **resources** (file-like data the agent can read); Copilot Studio currently supports tools and resources, not MCP prompts
3. Connect the server to the agent with the **MCP onboarding wizard** — generative orchestration must be turned on
4. Tools and resources appear automatically, and Copilot Studio reflects changes when the server adds, updates or removes them

**When to use MCP vs. custom connector:**
| MCP | Custom Power Platform Connector |
|-----|-------------------------------|
| System has an MCP server already | No MCP server available |
| Multiple agents need to share tools | Single agent, single connector |
| Standardized discovery required | Microsoft-certified connector ecosystem |

> **Exam tip**: MCP is an **open protocol** — not a Microsoft-proprietary feature. It enables interoperability between AI systems and tools across vendors.

### In Practice

**What breaks without this**: Each agent team writes its own connector to the same internal system, and when the API changes, five connectors break on different days.

**Decision trigger**: Ask: does the system already expose an MCP server, or will several agents across platforms need the same tools? If yes, use MCP.

**When you'd choose differently**: If the agent uses classic orchestration, or a certified Power Platform connector already covers the system with the governance you need, a connector is simpler.

### Exam Trap ⚠️

<div class="note-trap">
Copilot Studio supports MCP tools and resources, not MCP prompts, and MCP needs generative orchestration. MCP is an open protocol, so "MCP only works with Microsoft systems" is wrong.
</div>

---

## Computer Use in Copilot Studio

### Key Concept

**Computer use lets an agent operate websites and desktop apps through their UI when no API exists.**

This section covers how it works. A Computer-Using Agent model combines vision and reasoning to click, choose menus and type on a machine you set up, from a task described in natural language, and it adapts when screens change; it needs generative orchestration.

The design controls matter as much as the capability: who the agent acts as (maker or end-user credentials), which sites and apps it may act on, HTTPS, stored credentials, human supervision and dedicated least-privilege machines. Each step also costs Copilot Credits. **Think of it as giving a temp your keyboard: useful when there is no other way in, but only with a locked-down account and someone checking.**

Computer use is a Copilot Studio tool that lets an agent operate **websites and Windows desktop apps** on a machine you set up, by selecting buttons, choosing menus and typing — useful when there's no API:

**How it works:**
- Powered by Computer-Using Agent (CUA) models that combine vision with reasoning; you can also choose other supported models
- You describe the task in natural language; because it's AI-driven, it adapts when buttons or screens change
- Requires **generative orchestration**; works best for autonomous agents running in the background

**Design and security controls:**
- **Credentials**: maker-provided (default) or end-user. If you share an agent that uses maker credentials, anyone using it acts with the maker's access on that machine
- **Access control**: an allow list of websites and apps the model may act on (it can still *open* other sites but can't interact with them)
- **Enforce HTTPS**, stored credentials (internal storage or Azure Key Vault), and **human supervision** for potentially harmful instructions
- Use dedicated, least-privilege machines

**Cost:** billed per step — 5 Copilot Credits per step with a standard model, 15 with a premium model.

> **Exam tip**: Computer use is for UI-only systems. Prefer an API connector or MCP tool when one exists, and treat maker-provided credentials on a shared agent as a privilege-escalation risk.

### In Practice

**What breaks without this**: A shared agent uses maker credentials, so every user acts with the maker's access on the target system, and an audit finds actions nobody can attribute.

**Decision trigger**: Ask: is there an API, connector or MCP server for this system? If not, and the process is UI-only, computer use is the option.

**When you'd choose differently**: When an API or connector exists, use it: it's faster, cheaper per action, and more reliable than driving a UI.

### Exam Trap ⚠️

<div class="note-trap">
The allow list limits what the model may interact with, not what it may open, and maker-provided credentials on a shared agent let every user act with the maker's access. Computer use also needs generative orchestration, so it isn't available to a classic-orchestration agent.
</div>

---

## Agent Types — Comparison Table

### Key Concept

**The more freedom an agent has to decide and act, the more governance it needs.**

This section contrasts three agent types. Task agents run a bounded workflow with fixed steps, autonomous agents perceive events and choose their own actions without continuous prompting, and prompt-and-response agents answer queries or generate structured output.

The governance list follows from that: task agents need workflow validation, prompt-and-response agents need content safety and hallucination controls, and autonomous agents carry the heaviest burden, with approval gates, rollback and audit trails. **Think of it as a driving licence: a learner on a fixed route needs less supervision than a driver who picks their own destination.**

| Type | Definition | Triggers | Actions | Example |
|------|-----------|---------|---------|---------|
| **Task Agent** | Executes a specific, bounded workflow with fixed steps | User request or event | Predefined tool sequence | Portfolio summary agent |
| **Autonomous Agent** | Perceives environment, makes decisions, acts without continuous prompting | Time, event, or threshold | Dynamic — decides its own actions | Market monitoring + trade execution |
| **Prompt-and-Response Agent** | Responds to user queries, generates structured output | User query | Generate response | Report generation, Q&A |

**Governance implications:**
- Task agents: need workflow validation and error handling
- Autonomous agents: need **human approval gates**, rollback mechanisms, audit trails — highest governance burden
- Prompt-and-response: need content safety, hallucination controls

### In Practice

**What breaks without this**: An autonomous monitoring agent is given trade-execution rights with the same light controls as a Q&A bot, and one bad signal turns into real transactions with no approval or rollback.

**Decision trigger**: Ask: can this agent take actions with real-world effect without a person asking each time? If yes, design approval gates, rollback and audit before go-live.

**When you'd choose differently**: An autonomous agent whose only action is to notify a person (for example, raising an alert) needs less control than one that changes systems, because the person remains the decision point.

### Exam Trap ⚠️

<div class="note-trap">
"Autonomous" doesn't mean "unsupervised": autonomous agents need the most governance, not the least. And a prompt-and-response agent still needs content safety even though it takes no actions.
</div>

---

## Agent Behaviors in Copilot Studio

### Key Concept

**Reasoning and voice change how a Copilot Studio agent thinks and talks, and each brings its own design rules.**

This section covers two behaviours. Reasoning makes the agent work through a problem step by step before answering, which helps complex analysis at the cost of latency and tokens; in current Copilot Studio, deep reasoning is a preview setting on generative orchestration that uses a reasoning model (Azure OpenAI o3) for the steps the agent judges need it, or for steps whose instructions include the keyword "reason".

Voice agents answer by phone: basic voice agents use classic orchestration, real-time voice agents use generative orchestration with a speech-to-speech model, and both need a phone number through Azure Communication Services and Dynamics 365 Contact Center. **Think of voice design as writing for radio: short sentences, no tables, and nothing that only works on a screen.**

#### Reasoning Mode
- Activates **chain-of-thought (CoT)** processing before generating the final response
- Agent generates an internal reasoning trace: breaks problem into steps, evaluates options, then responds
- **Use when**: complex multi-step analysis, legal/financial reasoning, scientific questions
- **Trade-offs**: higher latency, more tokens consumed

#### Voice-Enabled Agents
- Copilot Studio supports interactive voice response through **basic voice agents** (classic orchestration, NLU-based intent recognition) and **real-time voice agents** (generative orchestration with a speech-to-speech real-time model for low latency)
- Voice agents accept **speech and DTMF** input and support call transfer and speech/DTMF customization
- You need a **phone number**, obtained through **Azure Communication Services**, and you integrate the agent with **Dynamics 365 Contact Center**
- **Design rules**: short, conversational responses; no markdown, lists or tables (they don't work in speech)
- Generative-orchestration features such as MCP tools need a real-time voice agent, not a basic one

### In Practice

**What breaks without this**: Reasoning is turned on for every turn of a simple FAQ agent, so answers are slow and cost more; or a chat agent's markdown answers are reused for voice, and callers hear list markers read aloud.

**Decision trigger**: Ask: does this request genuinely need multi-step analysis, and which channel will the answer be heard or read on?

**When you'd choose differently**: For simple lookups, leave reasoning off and use instructions and knowledge; for voice features that need generative orchestration, such as MCP tools, choose a real-time voice agent rather than a basic one.

### Exam Trap ⚠️

<div class="note-trap">
Reasoning doesn't make answers grounded or correct by itself; it adds analysis, latency and cost. And basic voice agents use classic orchestration, so generative-only features aren't available to them.
</div>

---

## Microsoft Power Platform Well-Architected Framework for AI

### Key Concept

**Power Platform Well-Architected checks an AI workload's design against five pillars before you build it.**

This section lists the pillars with their AI-specific concerns: reliability (agent uptime, Dataverse capacity), security (DLP, connector authentication, model access), operational excellence (ALM, environments, monitoring), performance efficiency (session limits, query optimisation) and experience optimisation (conversation quality, topic coverage, fallback).

The value is in applying it early, so design reviews catch gaps while they are cheap to fix. **Think of the pillars as a pre-flight checklist: you run it before take-off, not after landing.**

The Power Platform WAF provides five pillars for intelligent application workloads:

| Pillar | AI-Specific Concerns |
|--------|---------------------|
| **Reliability** | Agent uptime, Copilot Studio failover, Dataverse capacity |
| **Security** | DLP policies, connector authentication, AI model access controls |
| **Operational Excellence** | ALM for agents, environment strategy, monitoring dashboards |
| **Performance Efficiency** | Copilot Studio session limits, Dataverse query optimization |
| **Experience Optimization** | Conversational UX quality, topic coverage, fallback handling |

> **Exam tip**: WAF is applied **during design** to validate architectural decisions — not after deployment.

### In Practice

**What breaks without this**: An agent goes live without DLP policies or an environment strategy, makers connect it to unapproved connectors, and the fix needs a redesign rather than a setting change.

**Decision trigger**: Ask, during design: have we reviewed this workload against all five pillars, including experience optimisation for the conversation itself?

**When you'd choose differently**: For a code-first agent built on Azure rather than Power Platform, the Azure Well-Architected Framework and its AI workload guidance are the better reference.

### Exam Trap ⚠️

<div class="note-trap">
Experience optimisation is a Power Platform pillar; the Azure Well-Architected Framework names its fifth pillar cost optimisation instead. Don't mix the two pillar lists when a question names one framework.
</div>

---

## D365 Copilot for Sales and Copilot for Service

### Key Concept

**Role-based Copilots bring CRM data into the tools people already use, and you configure them rather than code them.**

This section covers the sales and service experiences. The seller experience in Outlook and Teams, now documented as Sales agent (formerly Microsoft 365 Copilot for Sales), summarises email, drafts CRM-grounded replies, prepares meetings and works with Dynamics 365 Sales or Salesforce; Copilot in the Dynamics 365 Customer Service agent desktop summarises cases and conversations and drafts knowledge-grounded email.

For contact centres, Copilot Studio is the AI front end and unified routing hands conversations, with context, to human agents. Most standard scenarios are configured in admin settings, not built. **Think of these Copilots as factory-fitted options: you choose and tune them, you don't weld them on yourself.**

#### Copilot for Sales
- Surfaces in Outlook and Teams
- **Built-in capabilities**: email summarization, reply drafting grounded in CRM data, meeting preparation, opportunity insights
- **Extensibility**: custom connectors add non-Dynamics data sources; configuration controls which insights surface
- **Sales agent**: a conversational agent in Microsoft 365 Copilot that lets sellers query connected CRM data in natural language; CRM results respect each seller's security access

#### Copilot for Service
- Surfaces in D365 Customer Service agent desktop
- **Built-in capabilities**: case summarization, email draft with knowledge base grounding, conversation summary, next-step suggestions
- **Customization**: business terms (tone, prohibited topics), summarization field configuration, additional knowledge sources
- **Key design decision**: configure in D365 admin center — no custom code required for standard scenarios

#### D365 Contact Center Integration
- Copilot Studio is the designated AI front-end for D365 Contact Center
- Supports voice (IVR-style), chat, and social messaging channels
- D365 unified routing engine handles escalation — passes conversation context to human agent
- Design the agent for **channel-specific behavior** (voice topics differ from chat topics in formatting)

### In Practice

**What breaks without this**: A team builds a custom agent to summarise service cases that the built-in Copilot already summarises, and agents now see two summaries that disagree.

**Decision trigger**: Ask: does a built-in sales or service Copilot capability already cover this, so that configuration (fields, knowledge sources, business terms) is enough?

**When you'd choose differently**: When the scenario needs logic or data the built-in capability can't reach, extend it (for example with connectors) or build a Copilot Studio agent for that part.

### Exam Trap ⚠️

<div class="note-trap">
Names change often: the Outlook and Teams seller app has been called Viva Sales, Sales Copilot, Microsoft 365 Copilot for Sales and now Sales agent. Questions test capability and where it is configured, so focus on "configure in the admin settings, no custom code for standard scenarios".
</div>

---

## Extending Copilot in Dynamics 365 Finance and Supply Chain

### Key Concept

**Copilot in finance and operations apps is a Copilot Studio agent, so you extend it in Copilot Studio, not in F&O settings.**

The Copilot chat and generative help and guidance in Dynamics 365 Finance and Supply Chain Management are delivered by an agent named **Copilot for finance and operations apps**, which lives in the Dataverse environment linked to the F&O environment. Help and guidance answers through that agent's out-of-box *conversational boosting* topic, which uses generative answers over its knowledge sources; by default that knowledge is limited to Microsoft's published product documentation.

To add your own knowledge, open Copilot Studio in the linked Dataverse environment, open the agent, and on the **Knowledge** tab upload files (such as PDF, Word or RTF); wait for the status to show *Ready*, test, then publish. Other source types, such as SharePoint, need **your own topic** in that agent. Finance and operations data itself can be added as a knowledge source through virtual entities or Dataverse tables (preview), and the same data can feed custom agents or a declarative agent in Microsoft 365 Copilot. **It's a franchise kitchen: the menu comes from head office, but you add local dishes in the same kitchen, not by painting them on the shop window.**

### In Practice

**What breaks without this**: Teams look for a knowledge setting inside F&O, don't find one, and build a second agent, so users get two help experiences that disagree.

**Decision trigger**: Ask: is the content uploadable files (add on the Knowledge tab) or a live source such as SharePoint (add your own topic)? And is it about using the product? The boosting topic assumes added knowledge relates to product use, so unrelated content can produce misleading answers.

**When you'd choose differently**: If users want ERP answers from inside Microsoft 365 Copilot rather than inside the F&O app, build a declarative agent with F&O data as knowledge and publish it to Copilot.

### Exam Trap ⚠️

<div class="note-trap">
Answers that configure F&O knowledge "in the Dynamics 365 Finance admin settings" or "by opening a Microsoft support ticket" are wrong. The supported path is Copilot Studio → 'Copilot for finance and operations apps' agent → Knowledge (files) or your own topic (other sources) → test → publish. Turning on AI general knowledge is optional, off by default, and increases the risk of incorrect answers.
</div>

---

## Deep Dive: Making D2 Click

### 1. The connective narrative

Domain 2 asks you to turn a strategy into a buildable design, and nearly every question is really asking "which layer should own this?". The bottom layer is grounding: data processing, chunking, hybrid search and knowledge sources decide what the agent can know. The middle layer is the agent itself: a Copilot Studio agent with topics and generative orchestration, a Foundry prompt agent, or a hosted agent running your own code. The top layer is orchestration: how several agents divide the work, using Copilot Studio connected agents, A2A, or one of Agent Framework's five patterns.

Extensibility runs across all three layers. MCP and connectors give agents tools; computer use is the fallback when only a UI exists; toolboxes share tools across Foundry agents; voice agents and Teams or Microsoft 365 Copilot publishing decide where people meet the agent. The prebuilt layer — Copilot in Dynamics 365 apps, Copilot for Sales and Service, Power Platform AI hub — sits beside all of this, and the exam keeps checking that you extend what Microsoft ships before building something parallel.

The constant trade-off is control against effort. Every step from Copilot Studio to Foundry prompt agents to hosted agents, or from generative answers to custom code, buys control with more ownership. A good D2 answer gives each component the least powerful mechanism that meets its requirement, and keeps generative orchestration on wherever you need MCP, computer use or real-time voice.

### 2. Worked scenario

> **Scenario.** A utility company wants a phone-based outage assistant. Callers describe a problem; the agent checks an outage map exposed by an internal MCP server, logs a ticket in a legacy web portal with no API, and transfers complex cases to a human.
>
> **Step 1 — channel.** Phone means a voice-enabled Copilot Studio agent with a number from Azure Communication Services, integrated with Dynamics 365 Contact Center for transfer to people.
>
> **Step 2 — orchestration mode.** The agent must choose between tools on the fly, and MCP requires generative orchestration. That rules out a basic voice agent (classic orchestration), so choose a **real-time voice agent**.
>
> **Step 3 — outage data.** Connect the MCP server through the MCP onboarding wizard. Its tools (for example `get-outages`) appear automatically and update when the server changes.
>
> **Step 4 — the legacy portal.** No API exists, so add **computer use** with end-user or narrowly scoped credentials, an access-control allow list for the portal, Enforce HTTPS, and a dedicated least-privilege machine. Budget 5 Copilot Credits per step with a standard model.
>
> **Step 5 — speech design.** Keep responses short and avoid lists and markdown.
>
> **Outcome:** each requirement maps to one mechanism, and the single constraint that drives the design is that MCP needs generative orchestration.

### 3. Memory aid

**G-TOE** — check these four before choosing a D2 design:
- **G**rounding: which knowledge source or retrieval design gives the right data?
- **T**ools: connector, MCP, computer use or code — the least powerful one that works
- **O**rchestration: Copilot Studio generative orchestration, connected agents/A2A, or an Agent Framework pattern
- **E**xperience: where users meet it — Teams, Microsoft 365 Copilot, voice, Dynamics 365 app

### 4. Exam strategy for this domain

- Watch for terms from retired or renamed products: threads and runs (now conversations and responses), AutoGen class names (now Agent Framework patterns), prompt flow (retiring), Viva Topics (retired).
- Many distractors build something parallel to a Microsoft feature that already exists. Prefer extending the built-in agent, Copilot or connector.
- Generative orchestration is the hidden prerequisite for MCP and computer use and the deciding factor between basic and real-time voice agents.
- Five minutes before the exam: **find the one requirement that forces a mechanism, then choose the lightest design around it.**

---

## Updated Exam Quick Reference (Domain 2 — November 2026 Syllabus)

| Topic | Key Decision / Rule |
|-------|-------------------|
| MCP in Copilot Studio | Open protocol; connect via MCP onboarding wizard; tools + resources; needs generative orchestration |
| Computer Use | Last-resort for UI-only workflows; prefer API connectors |
| Task agent | Fixed workflow, bounded scope |
| Autonomous agent | Self-directed, highest governance burden — needs approval gates |
| Prompt-response agent | Query-driven, generates output |
| Reasoning mode | CoT processing — use for complex multi-step analysis |
| Voice agents | Basic (classic orchestration) or real-time (generative, speech-to-speech); ACS phone number + D365 Contact Center |
| Agent Framework patterns | Sequential, concurrent, handoff, group chat, Magentic |
| Prompt flow | Retires April 20, 2027 — migrate to Agent Framework workflows |
| F&O Copilot knowledge | Copilot Studio → 'Copilot for finance and operations apps' agent; files direct, SharePoint via your own topic |
| Power Platform WAF | 5 pillars: reliability, security, opex, performance, experience |
| Copilot for Sales | M365 Copilot + Outlook/Teams — custom connectors for non-D365 data |
| Copilot for Service | D365 admin config — no code for standard scenarios |
| D365 Contact Center | Copilot Studio = unified AI layer across voice/chat/social |
| MCP vs connector | MCP: standardized discovery; connector: Microsoft-certified ecosystem |
