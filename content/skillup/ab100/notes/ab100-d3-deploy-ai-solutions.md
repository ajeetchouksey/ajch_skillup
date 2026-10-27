# D3: Deploy AI-Powered Business Solutions

> **Exam weight**: 20–25% (skills measured as of November 16, 2026; 40–45% before that date) · this note covers the whole official Deploy domain, which the platform splits into D3 (monitor, test, ALM) and D4 (responsible AI)

## Overview

Domain 3 covers the full deployment lifecycle: monitoring and tuning agents in production, managing testing and quality gates, ALM (Application Lifecycle Management) across all Microsoft AI platforms, and responsible AI with security, governance, and compliance. This domain merges what were previously Domains 3 and 4.

---

## Section 1: Analyze, Monitor, and Tune AI-Powered Business Solutions

### Key Concept

**Production monitoring needs two alert tiers, infrastructure health and answer quality, and neither covers the other.**

This section defines the metrics, thresholds and telemetry patterns that tell you whether a deployed agent is healthy. Infrastructure signals (P95 latency, tool call failures, HTTP 5xx) show whether the agent responds; quality signals from scheduled evaluations (groundedness, relevance) show whether its responses are any good.

Tuning then follows the telemetry: rising input tokens point at retrieval, falling groundedness at the knowledge base, and latency spikes on pay-as-you-go at rate limits. Cost levers such as prompt caching, leaner retrieval, PTU and model routing come after the quality baseline is protected. **Think of it like a car dashboard: the engine light tells you the car runs, but only the sat-nav tells you you're heading the right way.**

#### Evaluation Metrics Reference

| Metric | What It Measures | Requires | Interpretation |
|--------|-----------------|---------|----------------|
| **Groundedness** | Response supported by retrieved context | Retrieved context | Low = hallucination risk |
| **Relevance** | Response addresses user query | Query + response | Low = off-topic answers |
| **Coherence** | Response is logically structured | Response only | Low = confusing output |
| **Fluency** | Response is grammatically correct | Response only | Low = language quality issue |
| **Similarity** | Response matches reference answer | Ground truth | Low = factual deviation |
| **F1 Score** | Token overlap with correct answer | Ground truth | Low = missing key facts |

> **High Relevance + Low Groundedness** = hallucination pattern — agent answers the question but invents content not in the retrieved context.

#### SLA Alert Design

Define alerts on two tiers:

| Tier | Metric | Typical Threshold |
|------|--------|------------------|
| Infrastructure | P95 latency | < 10 seconds |
| Infrastructure | Tool call failure rate | < 5% |
| Infrastructure | HTTP 5xx error rate | < 1% |
| Quality | Groundedness mean (nightly eval) | ≥ 3.5 / 5 |
| Quality | Relevance mean (nightly eval) | ≥ 3.5 / 5 |

> **Exam tip**: HTTP 5xx alerts catch infrastructure failures — they do NOT detect quality degradation. An agent can return HTTP 200 with a hallucinated response. Quality metric alerts are required for proactive quality monitoring.

#### Telemetry Pattern Interpretation

| Pattern | Likely Cause | Action |
|---------|-------------|--------|
| Input tokens increasing + latency increasing | More chunks retrieved per query (knowledge base growth without quality filtering) | Apply relevance score thresholds, review chunking |
| Groundedness dropping over time | Knowledge base staleness or low-quality new content | Re-evaluate chunking, filter low-relevance chunks |
| Tool failure rate high + latency spike | Tool failures causing retries — fix tools first | Investigate tool errors (API timeouts, auth failures) |
| PAYG latency spikes at high concurrency | Rate limiting (TPM/RPM) | Switch to PTU or implement request queuing |

#### Cost Optimization Techniques

| Technique | Mechanism | Savings |
|-----------|-----------|---------|
| **Prompt caching** | Identical prompt prefix of ≥1,024 tokens; cache reads billed at a discount on Standard deployments (up to 100% on Provisioned) | Depends on the model's cached-token rate and the cache hit rate |
| **RAG optimization** | Fewer, higher-quality retrieved chunks — reduce context tokens | Fewer input tokens per request |
| **PTU for stable high volume** | Reserve throughput — predictable capacity and low latency variance | Can cost less than pay-per-token at sustained high utilisation |
| **Model routing** | Foundry model router sends simple prompts to cheaper models (Balanced, Cost or Quality mode) | Evaluate against your current baseline |

### In Practice

**What breaks without this**: An agent returns HTTP 200 with hallucinated answers for weeks, because the only alerts watch latency and 5xx errors.

**Decision trigger**: Ask: if this metric moved, would I know whether users got worse answers? If not, add a quality alert fed by scheduled evaluation alongside the infrastructure alerts.

**When you'd choose differently**: A low-stakes internal FAQ agent may only need a weekly evaluation run and an analytics review, not nightly evaluation with paging alerts.

### Exam Trap ⚠️

<div class="note-trap">
Prompt caching needs an identical prompt prefix of at least 1,024 tokens, so putting variable content (user name, timestamp) at the start of the prompt defeats it. And cached reads on Standard deployments are discounted, not free; only Provisioned deployments can reach a 100% discount.
</div>

---

## Section 2: Manage the Testing of AI-Powered Business Solutions

### Key Concept

**No variant ships on averages alone: evaluate a golden dataset, meet every threshold, then inspect the outliers.**

This section covers the quality gate between a change and production. A golden dataset with verified answers is evaluated on both versions, each metric is checked against a minimum threshold, and only then does the change move through staging and a small canary.

Red teaming and generated test cases widen coverage: the AI Red Teaming Agent reports attack success rate, and Copilot Studio agent evaluation can generate test sets from knowledge sources or topics. Generated cases still need human curation. **Think of the golden dataset as a fixed driving-test route: because the course never changes, a different score means the driver changed, not the road.**

#### Pre-Deployment Validation Pipeline

```
Golden Dataset → Evaluate (both versions) → Compare Metrics → Meet Thresholds? → Staging → Canary (1-5%) → Production
```

**Golden dataset requirements:**
- ≥ 50 representative examples (ideally 100-200)
- Covers edge cases, domain boundaries, adversarial inputs
- Has verified correct outputs (ground truth) for F1 and Similarity metrics
- Refreshed when new features or significant prompt changes are made

#### A/B Test Decision Framework

When evaluating prompt variants with divergent metrics:
1. Define **metric priorities** based on business risk (e.g., for financial advice: Groundedness > Relevance)
2. Set **minimum thresholds** for each metric (not just averages — check outlier distributions)
3. Choose the variant that satisfies ALL minimum thresholds, prioritizing the highest-risk metric

> **Exam trap**: Never promote a variant based on one metric alone. A variant with higher Relevance but lower Groundedness may fail in production due to hallucinated content.

#### Outlier Analysis

Mean scores can conceal systematic failures. Always analyze outlier distributions:
- 4.6% failure rate (23/500 with Groundedness = 1/5) is significant in high-stakes domains
- Investigate whether outliers cluster around specific query types, domains, or input patterns
- Block deployment if outlier patterns represent unmitigated failure modes

#### Red-Team Testing

Systematic adversarial testing with the **AI Red Teaming Agent (preview)** in Microsoft Foundry, which builds on Microsoft's open-source PyRIT framework, scans model or application endpoints with attack strategies (for example Jailbreak for user prompt attacks and IndirectAttack for cross-prompt attacks), and reports **attack success rate (ASR)** by risk category and attack complexity:

| Attack Type | Description | Mitigation |
|-------------|-------------|-----------|
| **Direct jailbreak** | User overrides system instructions | Prompt Shields for user prompt attacks (on by default in Foundry guardrails) |
| **Indirect injection** | Retrieved content contains instructions | Prompt Shields document attack detection (off by default; can scan agent tool responses, preview) + spotlighting or structural delimiters |
| **Data extraction** | User extracts system prompt or other users' data | Output filtering + prompt confidentiality instruction |
| **Persona override** | User creates alternative persona (DAN, etc.) | Content Safety jailbreak detection |

#### Copilot-Based Test Case Strategy

Use Copilot to accelerate test case creation:
- **Copilot Studio agent evaluation** generates test sets from an agent's knowledge sources or topics (up to 100 test cases per set), from test chat, or from analytics themes based on real user questions
- Use GitHub Copilot to generate test templates from acceptance criteria
- Create scenario variations across all use case permutations
- Produce boundary condition test data
- Generate LLM-as-judge evaluation prompts for automated scoring

> Always validate and curate Copilot-generated test cases — Copilot generates candidates, humans validate correctness.

#### D365 Multi-App End-to-End Test Scenarios

For solutions spanning multiple D365 apps, design tests that:
- Cross application boundaries (e.g., Copilot for Sales in Outlook triggers D365 Sales opportunity update)
- Validate data consistency across apps (D365 Finance → D365 SCM → Power BI)
- Include escalation paths from AI agent to human agent in D365 Contact Center

### In Practice

**What breaks without this**: A prompt variant with a better mean ships, and the 23 of 500 answers that scored 1/5 on groundedness turn out to cluster on one query type that matters most.

**Decision trigger**: Ask: does this change touch prompts, models, tools or knowledge? If yes, rerun the golden dataset on both versions and compare per-metric minimums and outlier counts before any canary.

**When you'd choose differently**: A cosmetic change such as a new greeting message doesn't justify a full A/B test and canary; a quick test chat or a small regression set is enough.

### Exam Trap ⚠️

<div class="note-trap">
Copilot-generated test cases are candidates, not ground truth, and they cover what the agent already knows, so they won't reveal knowledge gaps. For red teaming, a lower attack success rate (ASR) is the better result.
</div>

---

## Section 3: Design the ALM Process for AI-Powered Business Solutions

### Key Concept

**Each platform has its own ALM vehicle: solutions for Copilot Studio and Dynamics 365, IaC plus agent versions for Foundry.**

This section maps how changes move from development to production on each platform. Copilot Studio and Dynamics 365 customizations travel inside Power Platform solutions, with connection references and environment variables swapping per-environment settings. Foundry resources and deployments are declared in Bicep, and agent definitions in source control become agent versions through a pipeline.

Mixed solutions need coordinated channels: F&O code and metadata still move as deployable packages, while the Copilot knowledge and topics for F&O move as Copilot Studio solution components. **Think of it like moving house: the boxes go in the van, the piano needs specialist movers, and the change of address goes to the post office; one move, three channels.**

#### ALM Across Microsoft AI Platforms

| Platform | ALM Approach | Key Artifacts |
|----------|-------------|--------------|
| **Copilot Studio** | Solution-based export/import (Power Platform Solutions); promote dev → staging → prod environments | `.zip` solution package, environment variables for endpoint config |
| **Foundry Agent Service** | IaC (Bicep/ARM) for the Foundry resource, projects, connections and deployments; agent definitions in source control, created as agent versions by the SDK/REST in a pipeline | `bicep` files, agent definitions, environment parameter files |
| **Custom AI models** | Versioned training data and fine-tuning jobs; evaluate on a Developer deployment; evaluation gate before promotion | Model version, evaluation report, deployment config |
| **Dynamics 365 AI** | D365 solution packages; standard ALM via Power Platform | Solution package, environment configuration |

#### Copilot Studio ALM

Key ALM considerations:
- Agents, topics, connectors, and actions are packaged in **Power Platform Solutions**. New agents land in the **default solution**; create a **custom solution** to export, import and manage agents across environments
- Use **connection references** and **environment variables** so each environment uses its own connections and endpoints
- Automate promotion with **Power Platform pipelines**, available from the Copilot Studio solution explorer
- Copilot Studio supports **managed solutions** — changes in production are tracked and can be rolled back
- Actions that call Power Automate flows are included in the solution package

#### Foundry Agents ALM

Pipeline stages for Foundry Agents:
```
Source Control (agent YAML + Bicep)
    → CI: lint + validate schema + run golden dataset evaluation
    → Deploy to DEV Foundry Project (environment-specific model deployment names)
    → Deploy to STAGING + run integration tests
    → Canary to PRODUCTION (1-5% traffic)
    → Full PRODUCTION promotion
```

Foundry snapshots agent versions automatically, so rollback is a version change, and publishing promotes an agent to a stable endpoint.

#### ALM for AI in D365 Finance and Supply Chain

- Use **Lifecycle Services (LCS)** for D365 F&O environment management
- Copilot customizations (knowledge and topics) live in the 'Copilot for finance and operations apps' agent in the Dataverse environment linked to each F&O environment, so they move as Copilot Studio solution components; F&O code and metadata still move as deployable packages
- Data used in AI models (demand forecasting data, financial analytics) has its own ALM: dataset versioning, data pipeline promotion between environments

### In Practice

**What breaks without this**: An agent left in the default solution can't be promoted cleanly, or a solution imported into production still calls the dev endpoint because a URL was hard-coded instead of held in an environment variable.

**Decision trigger**: Ask: which platform owns each artifact (agent, flow, model deployment, F&O code, data)? Each artifact follows its own platform's promotion path, ideally orchestrated from one release pipeline.

**When you'd choose differently**: A throwaway proof of concept in a sandbox can live without pipelines and manual export may be enough, but build it in a custom solution anyway so it can be promoted later.

### Exam Trap ⚠️

<div class="note-trap">
Production should receive managed solutions. Importing unmanaged solutions there lets people edit production directly, and deleting an unmanaged solution removes only the container, not its components. Foundry has no deployment slots either: rollback means switching to a previous agent version or model deployment.
</div>

---

## Section 4: Responsible AI, Security, Governance, Risk, and Compliance

### Key Concept

**Responsible AI becomes real through controls: risk classification, identity, injection defenses, residency, access trimming, immutable audit and erasure.**

This section translates principles and regulation into concrete Azure controls. The EU AI Act risk tier decides how heavy the obligations are; managed identity, Azure RBAC and Azure Policy constrain who and what can call models; Prompt Shields and structural delimiters address prompt manipulation.

Data controls complete the picture: the deployment type and region decide where prompts are processed, security trimming decides what each user can retrieve, WORM storage keeps the audit trail tamper-proof, and erasure must reach indexes and fine-tuned models, not just source files. **Think of it as a bank vault: the policy says who may enter, but the locks, cameras and sealed ledger are what make it true.**

#### Microsoft Responsible AI Principles

| Principle | Definition | Exam-Relevant Scenarios |
|-----------|-----------|------------------------|
| **Fairness** | AI doesn't discriminate based on protected characteristics | Loan denial bias via zip code proxies |
| **Reliability & Safety** | AI performs consistently and safely | Clinical AI failing on edge cases |
| **Privacy & Security** | Data is protected; access is controlled | GDPR compliance for conversation logs |
| **Inclusiveness** | AI works for all people | Accessible interfaces, multilingual support |
| **Transparency** | Users know they're interacting with AI | AI disclosure requirement (EU AI Act Art. 50) |
| **Accountability** | Clear responsibility for AI decisions | Business unit owns decisions; CoE owns standards |

#### EU AI Act Classification

| Risk Level | Examples | Requirements |
|-----------|---------|-------------|
| **Prohibited** | Social scoring, real-time biometric surveillance in public | Banned — cannot deploy |
| **High Risk** | Credit scoring, clinical decision support, CV screening, access control | Conformity assessment, risk management, technical documentation, human oversight |
| **Limited Risk** | Chatbots (must disclose AI), deepfake generation | Transparency obligations |
| **Minimal Risk** | Spam filters, game AI, recommendation systems | No specific obligations |

#### Agent Security Design

| Security Control | Implementation |
|-----------------|---------------|
| **Agent authentication** | Managed Identity for agent-to-service calls (no secrets in code) |
| **Model access control** | Azure RBAC on the Foundry resource and projects — scope access per team; Azure Policy to restrict models and deployment types |
| **Prompt injection defense** | Prompt Shields (user prompt and document attacks) + structural prompt delimiters |
| **Data access on grounding data** | Azure AI Search uses managed identity; index-level access controls |
| **Audit trail** | Log queries, retrieved context, and responses to immutable storage |

#### Prompt Manipulation Vulnerabilities and Mitigations

| Vulnerability | Description | Mitigation |
|--------------|-------------|-----------|
| **Direct injection** | User instructs agent to ignore its system prompt | Azure AI Content Safety jailbreak detection at input layer |
| **Indirect injection** | Retrieved content contains embedded instructions | Content Safety on retrieved content + XML structural delimiters |
| **System prompt extraction** | User asks agent to repeat its instructions verbatim | Output filtering + explicit confidentiality instruction |
| **Persona override** | User creates alternative persona (DAN pattern) | Content Safety jailbreak detection blocks known patterns |

> **Defense-in-depth**: Apply multiple controls — no single mitigation fully eliminates prompt injection risk.

#### Data Residency and Movement Compliance

For EU data residency under GDPR:
- Create the Foundry resource in an EU region — this fixes where **data at rest** lives
- Choose a **Data Zone (EU)** or **Standard** deployment type — **Global** types may process prompts in any Azure region
- Enforce allowed regions and deployment types with **Azure Policy** (for example, deny GlobalStandard)
- Use **Private Endpoints** — data does not traverse public internet
- Don't use Developer deployments for regulated data: they carry no data-residency guarantee
- For fine-tuning: training data must not leave the designated region

#### Grounding Data Access Controls

| Control | Implementation |
|---------|---------------|
| **Field-level security** | Dataverse field permissions restrict which data the agent can retrieve |
| **Row-level security** | Azure AI Search security trimming using the user's identity token |
| **Model tuning access** | Private storage account + managed identity for fine-tuning datasets |
| **Data minimization** | Index only fields needed for the agent's tasks — not full record copies |

#### Audit Trails for AI Systems

Requirements for regulated industries:

| Requirement | Implementation |
|-------------|---------------|
| **Immutability** | Azure Blob Storage with WORM policy (Write Once Read Many) |
| **Long-term retention** | Archive to cool/cold tier after 90 days; 7-year retention for financial services |
| **What to log** | Query, retrieved context chunks, model version, response, timestamp, user ID |
| **Who can access** | Separation of duties — ops team can read logs but cannot delete them |

> **Exam trap**: Azure Monitor logs (retention is an admin-changeable setting and data can be purged) and Cosmos DB with soft-delete are NOT immutable audit stores. Use Azure Blob WORM.

#### GDPR Compliance for AI Agents

| GDPR Requirement | AI Implementation |
|-----------------|------------------|
| **Storage limitation** (Art. 5) | TTL policy on conversation logs (e.g., 90 days) |
| **Right to erasure** (Art. 17) | Partition vector indexes by user ID; delete user partition on request |
| **Data minimization** (Art. 5) | Log only fields necessary for the stated purpose |
| **Right not to be subject to automated decisions** (Art. 22) | Require human review for high-impact AI decisions |

#### Model Decommissioning

Fine-tuned model weights encode training data — deleting the source files does NOT remove learned information:

1. Delete the fine-tuned model and any copies of its weights
2. Delete all deployment endpoints
3. Apply model unlearning techniques if specific data memorization is a concern
4. Document the decommissioning for audit purposes

### In Practice

**What breaks without this**: A Foundry resource in an EU region serves a Global Standard deployment, so prompts are processed outside the EU and the residency commitment breaks without anyone changing the region.

**Decision trigger**: Ask, for every data flow: where is it processed, who can retrieve it, how is it logged, and how is it deleted? Each answer maps to a row in the tables in this section.

**When you'd choose differently**: Minimal-risk internal tools don't need conformity assessments or 7-year WORM retention; size the controls to the risk tier and to your sector's retention rules.

### Exam Trap ⚠️

<div class="note-trap">
Resource region is not processing location: Global deployment types may process prompts in any Azure region even while data at rest stays in the EU. And deleting the training files doesn't remove what a fine-tuned model learned; the model itself must be deleted.
</div>

---

## ALM for Data Used in AI Models and Agents

### Key Concept

**Data is a versioned artifact too: datasets, indexes, golden sets and model weights each need a promotion path.**

This section covers ALM for the data behind models and agents rather than their code. Training datasets are versioned with lineage, knowledge base content is re-indexed and checked with test queries after each update, golden sets live in source control, and model weights are registered with version tags.

Without this, a rollback restores old code that queries new data, and nobody can reproduce last month's behaviour. **Think of it like a recipe book: you can only recreate last year's dish if you kept last year's ingredients list as well as the method.**

| Data Type | ALM Approach |
|-----------|-------------|
| **Training datasets** | Version datasets in Azure ML Data Assets; track lineage |
| **Knowledge base documents** | Re-index after every content update; validate coverage with test queries |
| **Evaluation datasets (golden sets)** | Version-controlled in source repo; updated when agent capabilities change |
| **Model weights** | Registered with version tags (fine-tuned models in Foundry; registry in Azure Machine Learning) |

### In Practice

**What breaks without this**: A knowledge base update ships without re-indexing or test queries, and groundedness drops because the agent retrieves stale or missing chunks.

**Decision trigger**: Ask: to reproduce an answer this agent gave three months ago, which dataset, index, golden set and model version would I need? Each of those must be versioned.

**When you'd choose differently**: When the agent grounds on a live system of record at runtime (for example Dataverse tables), you don't version the data itself; you version the schema, the queries and the evaluation set.

### Exam Trap ⚠️

<div class="note-trap">
Updating source documents doesn't change what the agent retrieves until the index has been refreshed, and a refreshed index without test queries is an unvalidated release. Golden sets go stale too: update them when the agent's capabilities change, or the gate keeps measuring the old agent.
</div>

---

## Copilot Studio Agent Evaluation

### Key Concept

**Agent evaluation turns Copilot Studio testing from one-question-at-a-time chat into repeatable, scored test sets.**

A **test set** holds up to 100 test cases. Each case is a single question or, for conversation test sets, a whole conversation, optionally with an expected answer. You can generate cases with AI (a quick set of 10 from the agent's design, or a full set from a knowledge source or topics), import a CSV, reuse the latest test chat, write them by hand, or build them from **themes** in analytics, which group real user questions. Evaluations run as the signed-in user, can be triggered through Power Platform REST APIs or connectors for CI/CD, and results stay in Copilot Studio for 89 days unless exported.

Each test set can use several **test methods**: **General quality** (an LLM judges relevance, groundedness, completeness and abstention; no expected answer needed), **Compare meaning** (meaning matches the expected answer), **Text similarity** (wording matches), **Exact match**, **Keyword match**, **Tool use** (the expected tools or topics ran), **Content safety** (hate and unfairness, sexual, violence, self-harm, with a permitted level from 0 to 7), and **Custom** (your own instructions and pass/fail labels). **Think of the test methods as different examiners: one marks the essay, one checks the facts, one checks you showed your working.**

### In Practice

**What breaks without this**: Makers test in chat, ship, and discover after a knowledge or instruction change that answers regressed — with no baseline to prove it.

**Decision trigger**: Ask: is there one right wording (exact match or text similarity), one right meaning (compare meaning), no fixed answer (general quality), or a required action (tool use)? Pick methods per goal, and add content safety for anything customer-facing.

**When you'd choose differently**: For agents built and run in Foundry rather than Copilot Studio, use Foundry evaluations and the Azure AI Evaluation SDK. Note that agent evaluation supports agents set to *No authentication* or *Authenticate with Microsoft*, not *Authenticate manually*.

### Exam Trap ⚠️

<div class="note-trap">
General quality needs no expected answers, so it's the only method that works on a freshly generated test set. Every other method needs expected answers, keywords or tools. Generated test cases cover what the agent already knows; they don't find information gaps.
</div>

---

## Foundry Observability in Production

### Key Concept

**Foundry observability is three things working together: evaluation scores quality, monitoring watches it over time, and tracing explains each request.**

**Evaluation** uses built-in evaluators — general quality (coherence, fluency), RAG (groundedness, relevance), safety and security, and agent-specific ones such as tool call accuracy and task completion — plus custom evaluators. **Monitoring** in the Application Insights-backed dashboard tracks token use, latency, error rates and quality scores in production, through continuous evaluation of sampled traffic, scheduled evaluation on test datasets to detect drift, scheduled red teaming, and Azure Monitor alerts. **Tracing**, built on OpenTelemetry, records model calls, tool calls and agent decisions, and supports frameworks such as Microsoft Agent Framework, LangGraph and the OpenAI Agents SDK.

When something goes wrong, **cluster analysis** groups evaluation failures into patterns, and the **agent optimizer (preview)** can generate improved instructions, skills, tool descriptions and model selections, which you then re-evaluate. **It works like a hospital: tests diagnose, monitors catch changes overnight, and the patient chart explains what happened at each step.**

### In Practice

**What breaks without this**: HTTP 200 responses hide hallucinations, latency spikes can't be pinned to a tool or model call, and quality drifts for weeks before users complain.

**Decision trigger**: Ask: do I need to know *whether* quality changed (evaluation and monitoring) or *why* a specific request misbehaved (tracing)? Production agents need both.

**When you'd choose differently**: Copilot Studio agents rely on Copilot Studio analytics and agent evaluation for most of this; Foundry observability matters when the agent runs in Foundry or in your own code.

### Exam Trap ⚠️

<div class="note-trap">
Availability tests and HTTP error alerts prove the endpoint is up, not that the answers are good. And evaluations in the Foundry agents playground are on by default and billed by consumption.
</div>

---

## Deep Dive: Making D3 Click

### 1. The connective narrative

Deploy is where an agent stops being a design and becomes something you have to keep good. The official domain has four parts, and they form a loop. **Testing** sets the bar before release: test sets, evaluators and red teaming define what "good enough" means. **ALM** moves a known-good version between environments without manual drift: solutions and pipelines for Copilot Studio, versioned agent definitions and infrastructure as code for Foundry, a parallel build and evaluation gate for indexes and data. **Monitoring** checks that production still meets the bar, and **tuning** uses what monitoring finds to produce the next version, which goes back through testing.

Responsible AI, security and governance wrap around the loop rather than sitting at the end. Prompt Shields, residency-safe deployment types, least-privilege identities and audit trails are design choices that every release must preserve. That's why the exam likes questions where a technically valid deployment step quietly breaks a governance rule — switching to a Global deployment to fix quota, sharing a maker's credentials, or rebuilding an index in place.

### 2. Worked scenario

> **Scenario.** A bank's Foundry prompt agent answers mortgage questions. After an instruction update, complaints rise and the dashboard shows groundedness falling from 4.3 to 3.6 on its 1–5 scale.
>
> **Step 1 — stop the harm.** Roll back to the previous agent version; Foundry snapshots versions automatically.
>
> **Step 2 — find the pattern.** Run the scheduled evaluation set against both versions and use cluster analysis on the failures. Most failures are questions about fixed-rate penalties, where the new instructions encouraged answering from general knowledge.
>
> **Step 3 — fix and gate.** Rewrite the instructions (optionally with the agent optimizer, preview) and add the failing questions to the test set. Re-run evaluation; promote only if groundedness meets the agreed threshold and no other evaluator regresses.
>
> **Step 4 — check safety.** Run a red-teaming scan with Jailbreak and IndirectAttack strategies and compare ASR with the last release.
>
> **Step 5 — release and watch.** Publish the new version and keep continuous evaluation and Azure Monitor alerts on groundedness.
>
> **Outcome:** rollback in minutes, a root cause backed by data, and a test set that now guards against this regression.

### 3. Memory aid

**TAME** — the Deploy loop:
- **T**est: test sets, evaluators, red teaming, pass thresholds agreed in advance
- **A**LM: custom solutions and pipelines, agent versions, versioned data and indexes
- **M**onitor: continuous and scheduled evaluation, tracing, alerts, analytics themes
- **E**nhance: cluster analysis, optimizer, prompt and retrieval fixes, then back to Test

### 4. Exam strategy for this domain

- Weight dropped to 20–25% from November 16, 2026, but the questions are often hard trade-offs. Read for the step that's missing: an evaluation gate, a rollback path, or a governance rule.
- "Deploy and monitor production" is almost never the answer to a testing question; neither is "rebuild in place" for an ALM question.
- Means hide outliers. Expect at least one question where a good average score conceals a failing cluster.
- Five minutes before the exam: **every change goes test → promote → watch, and you can always roll back.**

---

## Exam Quick Reference — Domain 3 (Deploy)

| Topic | Key Rule |
|-------|---------|
| Groundedness + Relevance | High Relevance + Low Groundedness = hallucination |
| Quality alerts | HTTP 5xx alerts ≠ quality alerts; need separate metric-based alerts |
| Prompt caching | ≥1,024 identical prefix tokens → cache reads at a discount; check cached_tokens in usage |
| Golden dataset | ≥50 examples; validates quality before any deployment; refreshed per change |
| A/B promotion | Define metric priorities; check outliers, not just means |
| Red-team testing | AI Red Teaming Agent (PyRIT) → attack success rate by risk and complexity |
| Copilot test generation | Generates templates + variations + eval prompts; humans validate |
| Copilot Studio ALM | Power Platform Solutions + environment variables per environment |
| Foundry Agents ALM | IaC (Bicep) + agent YAML in source control + CI/CD pipeline |
| EU AI Act: High Risk | Credit scoring, clinical decisions, CV screening → conformity assessment |
| EU AI Act: Limited Risk | Chatbots → must disclose AI identity |
| Prompt injection | Defense-in-depth: Content Safety (input) + structural delimiters + output filtering |
| Audit trail | Azure Blob WORM (immutable); NOT Cosmos DB soft-delete or Azure Monitor |
| GDPR storage limitation | TTL on conversation logs; right to erasure via user-partitioned index |
| Model decommissioning | Delete weights from registry; source file deletion does NOT remove learned info |
| Data residency | EU region + Data Zone (EU) or Standard deployment + Azure Policy + Private Endpoints |
| Copilot Studio testing | Agent evaluation test sets: general quality, compare meaning, tool use, content safety, and more |
| Foundry monitoring | Continuous + scheduled evaluation, scheduled red teaming, Azure Monitor alerts |
