# Domain 2: Microsoft AI Apps & Services
**Exam Weight: 38% — Heaviest Domain (tied)**

---

## 🧠 The Golden Rule

> **"Microsoft 365 Copilot = AI embedded in your daily work apps. Foundry Tools = AI you build custom solutions with."**

<div class="note-important"><strong>Core distinction:</strong> If the scenario is about a business user in Word / Excel / Teams / Outlook getting AI help → M365 Copilot. If the scenario is about building a custom AI application, agent, or service → Foundry Tools / Azure AI Foundry. Copilot Studio sits in between — it lets non-developers build custom agents using M365 data.</div>

> 💡 **Human Angle**: Reaching for Azure AI Foundry when Copilot Studio would already do the job is like hiring a construction crew to hang a picture frame — real capability, wrong tool for the size of the job.

---

## 2.1 The Microsoft AI Stack

Microsoft's AI offering is structured in four layers, from raw infrastructure to end-user applications. Understanding which layer each product lives in is core to the exam.

| Layer | What it provides | Key products |
|---|---|---|
| **1 — Foundation** | AI models + compute infrastructure | Azure OpenAI Service, Model Catalog (GPT-4o, Phi, Llama, Mistral) |
| **2 — Platform** | Developer tools to build, evaluate, and deploy AI solutions | Azure AI Foundry, Azure AI Search, Azure Vision in Foundry Tools |
| **3 — Extensibility** | Low-code/no-code agent and copilot builder | Microsoft Copilot Studio, M365 Copilot plugins, connectors |
| **4 — Applications** | Ready-to-use AI embedded in productivity apps | Microsoft 365 Copilot, Microsoft Copilot (consumer), Copilot Chat |

<div class="note-important"><strong>How the layers connect:</strong> Foundation models power the Platform tools. Platform tools power the Extensibility layer. Extensibility customises the Applications. Responsible AI principles span all four layers.</div>

This layering exists because each layer trades flexibility for speed. A business user at the Applications layer gets zero setup time but no customisation; a developer at the Foundation layer gets full control over model choice and infrastructure but has to build everything above it themselves. Most business scenarios are solved by picking the highest layer that still meets the requirement, precisely because every layer down adds build time, cost, and ongoing maintenance the layer above didn't need.

**Responsible AI spans all layers** — Microsoft's six principles (Fairness, Reliability, Privacy, Inclusiveness, Transparency, Accountability) are applied at every level, from model training to end-user UI.

![Diagram 1](/content/skillup/ab731/images/d2-microsoft-ai-services-01.png)

---

## 2.2 Microsoft Copilot vs Microsoft 365 Copilot

<div class="note-trap"><strong>This is a favourite exam trap.</strong> These are two different products.</div>

| | **Microsoft Copilot** | **Microsoft 365 Copilot** |
|---|---|---|
| **Audience** | Anyone (consumer + business) | M365 subscribers (paid add-on) |
| **Powered by** | Bing + GPT | GPT + **Microsoft Graph** (your org data) |
| **Access to org data** | ❌ No | ✅ Yes — emails, docs, Teams chats, calendar |
| **Licence** | Free (Copilot) or included | Paid add-on (~$30/user/month) |
| **Use case** | General web research, tasks | Work productivity with YOUR org data |

<div class="note-scribble">The key differentiator: Microsoft Graph. M365 Copilot can answer "Summarise last week's emails about Project X" because it reads YOUR Graph data. Free Microsoft Copilot cannot do this.</div>

---

## 2.3 Microsoft Graph — The Data Connector

Microsoft Graph is the **API layer that connects Copilot to your organisation's data** stored in Microsoft 365 services.

![Diagram 2](/content/skillup/ab731/images/d2-microsoft-ai-services-02.png)

**Why it matters for Copilot:**
- When you ask Copilot "What are my action items from today's meetings?" — Graph pulls your Teams transcripts and calendar
- Copilot **respects existing permissions** — you only see data you're already authorised to see
- No data is shared across tenants

<mark>Exam key point: Microsoft Graph is WHY M365 Copilot knows about your specific org. Without Graph, Copilot would only know public internet information.</mark>

---

## 2.4 Copilot in Microsoft 365 Apps

| App | Key Copilot capabilities |
|---|---|
| **Word** | Draft, rewrite, summarise documents; generate from outline |
| **Excel** | Analyse data, generate formulas, create charts, highlight trends |
| **PowerPoint** | Generate presentations from a Word doc or prompt; add slides; design suggestions |
| **Outlook** | Draft emails, summarise threads, schedule meetings, coaching on tone |
| **Teams** | Meeting transcription + summary, action items, live translation, chat summaries |
| **OneNote** | Organise notes, generate summaries, create to-do lists |
| **Loop** | Collaborative workspaces with AI-generated content that stays in sync |

Each app's capabilities follow from what that app already stores and structures, not from a separate AI feature bolted on per app. Excel's formula generation and chart creation work because a spreadsheet is already structured data Copilot can reason over directly; Teams' meeting recap works because Teams already captures a timestamped transcript Copilot can summarise. It's the same underlying model in every case, reasoning over whatever structured content the host app already produces.

<div class="note-important"><strong>Exam pattern:</strong> "A manager needs to quickly catch up on a 2-hour meeting they missed. Which Copilot feature is most appropriate?" → Teams Copilot meeting recap / summary.</div>

---

## 2.5 Copilot Chat (Web & Mobile)

**Copilot Chat** is the chat interface available at copilot.microsoft.com and in the Microsoft 365 mobile apps.

- Available to M365 users as part of their subscription (or free tier for consumer)
- Supports **web search** (grounded in Bing) + **work data** (via Graph, for M365 users)
- Supports **file uploads** for analysis
- Can generate images (via DALL·E integration)

**Work vs Web toggle:** In the M365 Copilot Chat interface, users can toggle between searching the web or searching their work data. This is a common exam concept.

---

## 2.6 Researcher and Analyst in Copilot

Two specialised **Copilot agents** available in Microsoft 365:

| Agent | Purpose | Best for |
|---|---|---|
| **Researcher** | Deep research using the web + your org data | Building comprehensive reports, competitive analysis, literature review |
| **Analyst** | Data analysis, running Python code, generating visualisations | Analysing spreadsheets, surfacing trends, creating charts from data |

<div class="note-scribble">Researcher = web + docs research. Analyst = data crunching. If the exam gives a scenario about analysing a sales CSV → Analyst. If it's about researching market trends → Researcher.</div>

---

## 2.7 Microsoft Copilot Studio

**What it is:** A low-code/no-code platform to **build custom AI agents and copilots** connected to your organisation's data and processes.

**Who uses it:** IT professionals, power users, business analysts — no coding required.

**Key capabilities:**
- Create custom copilots with specific knowledge bases (SharePoint, websites, documents)
- Add to Teams, websites, mobile apps
- Integrate with Power Platform (Power Automate for actions)
- Connect to third-party systems via connectors
- Create custom agents for specific business functions (HR bot, IT helpdesk, sales assistant)

![Diagram 3](/content/skillup/ab731/images/d2-microsoft-ai-services-03.png)

<div class="note-important"><strong>Build vs Buy vs Extend:</strong><br/><strong>Buy</strong> = Use M365 Copilot out-of-the-box (no customisation)<br/><strong>Extend</strong> = Use Copilot Studio to customise/extend M365 Copilot<br/><strong>Build</strong> = Use Azure AI Foundry to build a custom AI application from scratch</div>

---

## 2.8 M365 Copilot Extensibility Framework

When out-of-the-box Copilot isn't enough, you can extend it:

| Extension type | What it does | Who builds it |
|---|---|---|
| **Plugins** | Give Copilot new capabilities (e.g., call your CRM API) | Developers |
| **Connectors** | Bring external data into Microsoft Graph | IT/Developers |
| **Declarative agents** | Copilot agents scoped to specific knowledge/tasks | Copilot Studio / Developers |
| **Custom engine agents** | Full custom AI agents using Azure AI Foundry | Developers |

<mark>Exam pattern: "A company wants Copilot to answer questions from their internal knowledge base in Confluence. What's the best approach?" → Build a declarative agent in Copilot Studio with the Confluence data.</mark>

---

## 2.9 Azure AI Foundry and Foundry Tools

**Azure AI Foundry** is Microsoft's platform for building, deploying, and managing enterprise AI solutions.

<div class="note-important"><strong>Terminology update:</strong> As of the August 2026 Microsoft Learn documentation revision, Microsoft has rebranded <strong>Azure AI Foundry</strong> to <strong>Microsoft Foundry</strong> (the official docs URL now redirects from <code>/azure/ai-foundry/</code> to <code>/azure/foundry/</code>). <strong>Foundry Tools</strong> remains the umbrella term for the AI services collection (Speech, Vision, Language, Document Intelligence, Content Understanding, Face, etc.) that sits alongside Microsoft Foundry. The AB-731 exam's own study guide resource list still links to this page under the label "Azure AI Foundry documentation" — so both names may appear interchangeably in exam questions and answer options. Don't be thrown by either term: they refer to the same underlying platform capability described in this section.</div>

### What's in Foundry Tools

| Tool | What it does |
|---|---|
| **Microsoft Foundry** | End-to-end AI project hub — model selection, prompt flows, evaluation, deployment |
| **Azure AI Search** | Vector + semantic search — the retrieval layer for RAG solutions |
| **Azure Vision in Foundry Tools** | Computer vision — image analysis, OCR, object detection, face analysis |
| **Model Catalog** | Access to hundreds of models: OpenAI (GPT-4o), Microsoft (Phi), open source (Llama, Mistral) |

### Benefits of Foundry Tools
- **Scalability** — scales from prototype to millions of users on Azure infrastructure
- **Security** — enterprise-grade access control, private networking, content filters
- **Choice** — use any model from the catalog, not locked to one vendor
- **Governance** — built-in responsible AI tooling, content safety filters, evaluations

<div class="note-important"><strong>Business scenario → Tool mapping:</strong><br/>📄 Understand documents from photos → Azure Vision (OCR)<br/>🔍 Search across thousands of internal documents → Azure AI Search<br/>🤖 Build a custom customer service bot → Microsoft Foundry + Copilot Studio<br/>📊 Analyse images from a factory floor → Azure Vision in Foundry Tools</div>

---

## 2.10 Matching AI Models to Business Needs

Not all models are equal. The exam tests your ability to match:

| Business need | Model characteristic to look for |
|---|---|
| Real-time chat with customers | Low latency, cost-effective (smaller model e.g. Phi) |
| Complex legal document analysis | High accuracy, large context window (GPT-4o) |
| Code generation at scale | Code-specialised model |
| Multilingual customer support | Strong multilingual capabilities |
| Image understanding | Multimodal model (vision + text) |
| On-premise deployment | Small, deployable model (Phi-3 mini) |

Matching model to need is a latency-cost-accuracy trade-off, not a preference. A larger model like GPT-4o carries more parameters and more compute per token, which buys stronger reasoning over long or ambiguous input at the price of higher latency and cost. A smaller model like Phi-3 answers faster and cheaper because it does less computation per token — the right call for a real-time chat widget where users notice a half-second delay, not for a legal document where taking the extra time to get it right is the whole point.

<div class="note-scribble">The exam won't ask you to memorise specific model benchmarks. It tests the concept: bigger/more expensive model ≠ always better. Match capability to task. Phi-3 for simple tasks, GPT-4o for complex reasoning.</div>

---

## 🎯 Domain 2 Exam Traps

| Trap | Correct answer |
|---|---|
| "Copilot" vs "M365 Copilot" | M365 Copilot has Microsoft Graph access; base Copilot does not |
| "Build vs Extend" | Try Copilot Studio extension before building from scratch in Foundry |
| "Researcher vs Analyst" | Researcher = web/doc research; Analyst = data analysis with code |
| "Which Copilot for collaborative AI content?" | Copilot Pages — persistent, multi-user canvas (not a single-session Word draft) |
| "Automate vs Augment first?" | Start with automatable tasks (meeting summaries, email drafts) for fastest ROI |
| "Budget-sensitive edge deployment?" | Phi model family — lightweight, runs on-device or in constrained environments |
| "Azure AI Search" | It's the retrieval/search layer for RAG — not just a search engine |
| "Copilot sees all data" | Copilot respects existing M365 permissions — can't access what user can't access |
| "Copilot rollout + years of SharePoint sharing" | Run SharePoint Advanced Management oversharing remediation BEFORE rollout — permission inheritance alone isn't proactive governance |
| "Multi-step process, no human prompting each step" | Copilot Studio agent that triggers and orchestrates — NOT a better prompt template |

---

## 2.11 Copilot Experiences — Pages, Chat, and Cross-App Features

Beyond per-app Copilot features, M365 Copilot includes cross-app experiences:

| Experience | What it is | Key differentiator |
|---|---|---|
| **Copilot Chat** (formerly Business Chat / BizChat) | Unified chat interface — query across all your work data (emails, docs, Teams, calendar) or web | Single place to ask anything about your work |
| **Copilot Pages** | Collaborative AI canvas — Copilot populates it, multiple users can continue editing | Persistent, shareable AI-generated artifact (unlike a single-session chat) |
| **Work / Web toggle** | In Copilot Chat, switch between your org data (Microsoft Graph) and Bing web search | Explicitly controls whether the AI searches your internal data or the public web |

![Diagram 4](/content/skillup/ab731/images/d2-microsoft-ai-services-04.png)

<div class="note-trap"><strong>Exam trap — Pages vs Word:</strong> "A team needs a shared AI-populated document where multiple members can continue adding Copilot-generated research" → <strong>Copilot Pages</strong> (multi-user, persistent, AI-populated). NOT Word Copilot (single session, single user).</div>

<div class="note-scribble">Copilot Chat is the power user's home base — if you need to ask "what did my team work on last week?" or "find all emails about Project X and summarise the key decisions", Copilot Chat with the Work toggle does this in one place. No need to open four apps.</div>

---

## 2.12 Mapping Business Processes to Copilot

Not every task benefits equally from AI. Map each task type to the right Copilot approach:

| Task type | AI benefit | Best Copilot application |
|---|---|---|
| **Automatable** | Highest — repetitive, structured, rule-based | Meeting summaries, email triage, invoice data extraction |
| **Augmentable** | High — knowledge work where AI drafts and humans refine | Writing proposals, data analysis in Excel, research in Chat |
| **Judgment-heavy** | Lower — deep expertise + ethics required | Complex legal interpretation, senior strategic decisions |
| **Relationship-based** | Minimal — human connection IS the value | Client relationship management, counselling, coaching |

### The mapping process

![Diagram 5](/content/skillup/ab731/images/d2-microsoft-ai-services-05.png)

<div class="note-important"><strong>Exam pattern:</strong> "Which tasks should be prioritised for Copilot deployment?" → Automatable tasks first (meeting summaries, email drafts, document extraction) — fastest, clearest ROI. Augmentable tasks (analysis, writing) second. Never start with judgment-heavy or relationship tasks.</div>

---

## 2.13 Choosing the Right Foundry Model

The Foundry Model Catalog contains hundreds of models. The exam tests your ability to match business need to model type:

| Scenario | Best model choice | Why |
|---|---|---|
| Complex legal reasoning, long documents | **GPT-4o** | High accuracy, large context window, strong reasoning |
| Real-time customer chat at low cost | **Phi (Phi-3 mini/small)** | Lightweight, fast, cost-effective for simple tasks |
| On-premise or edge deployment (no cloud) | **Phi-3 mini** | Small enough to run locally |
| Budget-conscious, open-source preferred | **Llama / Mistral** | Open source = no per-token cost, customisable |
| Domain-specific brand voice / jargon | **Fine-tuned model** | When base model cannot learn domain via prompting |
| Image + text understanding | **GPT-4o (multimodal)** | Vision + language in one model |

Open-source models like Llama and Mistral earn their place in this table for a different reason than raw capability: because their weights are published, an organisation can run them without per-token licensing fees, fine-tune them without vendor lock-in, or deploy them entirely on-premises for a regulatory reason a closed API can't satisfy. The trade-off is that the organisation now owns the hosting, scaling, and security work a managed API would otherwise handle.

![Diagram 6](/content/skillup/ab731/images/d2-microsoft-ai-services-06.png)

<div class="note-trap"><strong>Exam trap:</strong> "Bigger model = always better" is WRONG. The exam tests that you match model capability to task complexity. Using GPT-4o for a simple FAQ chatbot is expensive overkill. Using Phi-3 for complex multi-document contract analysis will produce poor results.</div>

---

## 2.14 Buy / Build / Extend Decision Framework

The AB-731 exam often presents a scenario and asks: *"What is the MOST APPROPRIATE solution?"* Use this framework:

| Approach | When to choose | Microsoft product |
|---|---|---|
| **Buy** | Need AI capability immediately, no customisation required | Microsoft 365 Copilot (out-of-box) |
| **Extend** | Need to add org-specific data or workflows to existing Copilot | Copilot Studio (extend M365 Copilot via plugins, connectors) |
| **Build** | Need fully custom AI experience, not based on M365 Copilot | Copilot Studio (standalone agent) or Azure AI Foundry |

<div class="note-important"><strong>Exam rule:</strong> "Extend" is the answer when a business already has M365 Copilot and wants to add capabilities. "Build" from scratch (Foundry) is only justified when M365 Copilot cannot serve the use case at all (e.g., external-facing customer chatbot on a public website).</div>

---

## 2.15 Proactive Governance Before a Copilot Rollout

### Key Concept

**Permission inheritance stops accidents at query time — it does nothing about oversharing that already exists.**

Microsoft 365 Copilot only surfaces content a user could already open directly — that's true and it's the answer to "does Copilot bypass security?" (§2.3). But it says nothing about *how much* content a user was already, quietly, over-permissioned to see. Years of "share with everyone in the org" links, stale guest access, and broadly-scoped SharePoint sites don't cause harm while a human has to click through folders manually — nobody has time to browse 4,000 files looking for something sensitive.

A Copilot rollout changes that instantly: a single chat query surfaces anything the user's existing permissions technically allow, indexed and summarised in seconds. **Think of oversharing as a locked door with the key under the mat**: harmless until something starts systematically checking under every mat in the building at once.

### In Practice

**What breaks without this**: a broad Copilot rollout surfaces a forgotten "share with entire org" link on a compensation spreadsheet or an M&A draft the moment the first curious employee asks Copilot the right question — a dormant sharing mistake becomes an active data exposure on day one of rollout, not because Copilot did anything wrong, but because nobody checked what it would now be able to find.

**Decision trigger**: ask, "if I ran an oversharing report today, would I be comfortable with a chat interface instantly surfacing everything it finds, under each user's own permissions?" If the honest answer is no, remediate before rollout — don't lean on "Copilot respects permissions" as if it were a substitute for a clean permission baseline.

**When you'd choose differently**: a small, contained pilot on a handful of already-tightly-scoped team sites doesn't need a full tenant-wide oversharing sweep first — proactive remediation earns its cost at broad or tenant-wide rollout scale, where the blast radius of a missed overshare is largest.

Use **SharePoint Advanced Management** to do this work before rollout, not after:

| SharePoint Advanced Management action | What it does |
|---|---|
| **Oversharing report** | Surfaces sites/files shared far more broadly than their sensitivity warrants |
| **Restrict content discoverability** | Excludes selected sites from org-wide search and Copilot retrieval without changing who can still open the file directly |
| **Site access review** | Flags stale permissions and inactive guest access for removal |
| **Sensitivity labels + auto-labelling** | Applies protection (encryption, access restriction) to sensitive content before an AI feature can retrieve it |

<div class="note-trap"><strong>Exam trap:</strong> "Disable Graph connectivity entirely" and "make every employee individually re-request access" are both overcorrections — they block legitimate work instead of fixing the actual problem. The correct action is targeted: find the overshared content, shrink its discoverability, label it — then roll out. Doing nothing ("permission inheritance is enough") and doing too much (disabling Graph) are both wrong for the same reason: neither actually looks at what's overshared.</div>

---

## 2.16 Automating Multi-Step Business Processes with Copilot Studio

### Key Concept

**A Copilot Studio agent can trigger itself and run a whole workflow; ad hoc Copilot chat needs a human to prompt every single step.**

Using Copilot in Outlook to draft one onboarding email is assistive — someone has to open the app, remember what's needed, and ask, one exchange at a time (this is the same Copilot-vs-agent distinction as D1 §1.10, applied to a concrete business process). A Copilot Studio agent removes the human from the loop between steps: it can trigger automatically on an event — a new hire record appearing in the HR system — and then sequence the IT ticket, the access request, and the facilities notification itself, tracking status across all of them.

**Think of ad hoc Copilot chat as phoning a colleague for one favour at a time; a Copilot Studio process agent is handing that colleague a checklist and the authority to work through it unsupervised**, only interrupting you at the one step that genuinely needs a human decision.

```mermaid
flowchart TD
  A[New hire added to HR system] -->|triggers agent| B[Copilot Studio agent starts]
  B --> C[Create IT ticket]
  B --> D[Initiate access request]
  B --> E[Notify facilities]
  C --> F{Approval required?}
  D --> F
  E --> F
  F -->|yes: high-risk access| G[Route to manager]
  F -->|no: standard request| H[Auto-complete step]
  G --> I[Status tracked across steps]
  H --> I
  I --> J[Onboarding logged end-to-end]

  style A fill:#162236,stroke:#60a5fa,color:#e2e8f0
  style B fill:#1a2a42,stroke:#7c3aed,color:#e2e8f0
  style F fill:#1a2a42,stroke:#7c3aed,color:#e2e8f0
  style G fill:#2a1a22,stroke:#fbbf24,color:#e2e8f0
  style H fill:#1a2a12,stroke:#34d399,color:#e2e8f0
  style J fill:#1a2a12,stroke:#34d399,color:#e2e8f0
```

*A Copilot Studio agent triggers on a new-hire event and orchestrates IT, access, and facilities steps, inserting a human approval gate only for high-risk requests.*

### In Practice

**What breaks without this**: a process split across separate ad hoc Copilot chats has no memory between steps and no owner if a step is skipped — a manager who forgets to trigger the facilities notification leaves a new hire without a desk assignment, and nobody finds out until the new hire's first day, because nothing was tracking status across the handoff.

**Decision trigger**: ask, "does this process span more than one system, or more than one step that should happen without someone re-opening Copilot chat to ask for it?" If yes, that's a Copilot Studio automation candidate, not a better prompt template.

**When you'd choose differently**: a genuinely one-off, single-system task that needs judgment at every step — drafting one custom, sensitive termination letter, say — doesn't benefit from orchestration; ad hoc Copilot chat with a human reviewing each line is still the right tool there.

<div class="note-trap"><strong>Exam trap:</strong> "Give managers a more detailed prompt template" and "have each system owner pilot their own Copilot chat" both sound like progress but leave the process exactly as manual as before — no trigger, no orchestration, no status tracking. If the scenario says a process should run "without a human prompting each step," a better prompt is never the answer; an agent that triggers and orchestrates is.</div>

---

## Deep Dive: Making Microsoft's AI Apps & Services Click

### 1. The connective narrative

The four-layer stack in §2.1 — Foundation, Platform, Extensibility, Applications — is the skeleton the rest of this domain hangs on. Nearly every topic after it is really the same question asked about a different scenario: *which layer solves this business need with the least amount of custom work?* Microsoft 365 Copilot (§2.2–§2.6) sits at the top, Applications layer, because most employees just need AI inside the tools they already use. Copilot Studio (§2.7, §2.15, §2.16) sits one layer down, Extensibility, for when the business need is specific enough that out-of-the-box Copilot can't reach it — a custom knowledge base, a multi-step workflow that has to trigger itself. Azure AI Foundry (§2.9, §2.13) sits at the bottom two layers, for when the need is custom enough that no low-code tool reaches it at all.

Governance rides along with that same stack, and it gets *more* important, not less, the higher up you go — not the reverse, which is the counterintuitive part. §2.15's SharePoint oversharing problem exists precisely because the Applications layer (Copilot) is the layer most employees touch daily, at the highest volume, with the least technical friction — so permission mistakes made years ago at the data layer become visible at conversational speed the moment Copilot goes broad. The Build/Buy/Extend framework (§2.7, §2.14) and the extensibility framework (§2.8) exist to stop teams from jumping straight to "build" (Foundry) when "extend" (Copilot Studio) already solves it — that's the domain's most consistently tested judgment call.

Model selection (§2.10, §2.13) is the same "least resource for the job" logic applied one level deeper: once you're building on Foundry, you still shouldn't reach for the largest, most expensive model by default. Phi for a cheap, low-latency FAQ bot; GPT-4o for genuinely complex reasoning over long documents. The domain rewards restraint at every layer of the decision, not just the top one.

### 2. Worked scenario

> **Scenario.** A global retailer is rolling out AI across three separate needs. First, marketing wants help drafting product descriptions and social copy — that's Word and Copilot Chat, Applications layer, no customisation needed (§2.2, §2.4). Second, HR wants new-hire onboarding to trigger automatically across IT, access provisioning, and facilities without a manager re-prompting at each step — that's a Copilot Studio agent, Extensibility layer, built exactly as described in §2.16. Third, the data science team wants a custom product-recommendation model trained on three years of purchase history — that's Azure AI Foundry, Platform/Foundation layers, because no low-code tool trains a custom model from scratch (§2.9, §2.13).
>
> Before the marketing rollout goes broad, IT runs a SharePoint Advanced Management oversharing report (§2.15) and finds two years' worth of "share with everyone" links on old campaign folders — nobody browsed them manually, so nobody noticed, but a Copilot query would surface them instantly. IT restricts discoverability and applies sensitivity labels before go-live, not after a complaint. For the recommendation model, the team starts on Foundry's pay-as-you-go tier while validating accuracy, then moves to a commitment tier once usage volume is predictable (§3.8) — mirroring the same pattern used for Copilot licensing scale-up.

### 3. Memory aid

**F-P-E-A**, bottom to top: **F**oundation → **P**latform → **E**xtensibility → **A**pplications (§2.1's own stack). For any scenario, ask which layer solves it with the least custom work — and don't drop a layer lower than the scenario actually requires.

### 4. Exam strategy for this domain

The traps in this domain are almost all look-alike-term traps: Microsoft Copilot vs Microsoft 365 Copilot, Researcher vs Analyst, Build vs Extend, Foundry vs Foundry Tools. The exam rewards correctly identifying the *minimum* layer or tool that satisfies the stated requirement, and punishes jumping to a custom build (Foundry) or a from-scratch agent when Copilot or an extension already covers it. One sentence for five minutes before the exam: default to the most out-of-the-box layer that satisfies the scenario, and only drop down a layer when the scenario explicitly rules out everything above it.

---

## 📌 D2 Hard Question Patterns

**Pattern 1 — Copilot vs Copilot Studio**
> *"A company wants employees to have an AI assistant that answers HR policy questions. What is the QUICKEST path to value?"*
>
> ✅ Microsoft 365 Copilot + SharePoint connector (extend). NOT Copilot Studio build-from-scratch — that's overkill for internal staff who already have M365 licences.

**Pattern 2 — Microsoft Graph powers Copilot**
> *"Why can Microsoft 365 Copilot access a user's emails and calendar without extra configuration?"*
>
> ✅ Microsoft Graph — the unified API layer that Copilot uses to read/write across M365 apps. Graph respects existing permissions, so Copilot inherits the user's data access.

**Pattern 3 — Foundry vs Studio scope**
> *"A developer team wants to build an AI model trained on 5 years of internal sales data. Which tool is most appropriate?"*
>
> ✅ Azure AI Foundry — for custom model development, fine-tuning, and MLOps. Copilot Studio is low-code for building agents, not for training models.

**Pattern 4 — Researcher / Analyst Copilot agents**
> *"A business analyst needs to synthesise insights from 50 reports per week. Which Copilot capability addresses this?"*
>
> ✅ Analyst agent in Copilot (deep analysis, Python code execution, charts). Researcher agent handles broad web + org data synthesis. These are the two premium agentic features in M365 Copilot.
