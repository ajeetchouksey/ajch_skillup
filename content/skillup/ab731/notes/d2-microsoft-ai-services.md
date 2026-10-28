# Domain 2: Microsoft AI Apps & Services
**Exam Weight: 38% — Heaviest Domain (tied)**

---

## 🧠 The Golden Rule

> **"Microsoft 365 Copilot = AI embedded in your daily work apps. Foundry Tools = AI you build custom solutions with."**

<div class="note-important"><strong>Core distinction:</strong> If the scenario is about a business user in Word / Excel / Teams / Outlook getting AI help → M365 Copilot. If the scenario is about building a custom AI application, agent, or service → Foundry Tools / Microsoft Foundry. Copilot Studio sits in between — it lets non-developers build custom agents using M365 data.</div>

> 💡 **Human Angle**: Reaching for Microsoft Foundry when Copilot Studio would already do the job is like hiring a construction crew to hang a picture frame — real capability, wrong tool for the size of the job.

## Overview

Domain 2 asks one question over and over: which Microsoft product solves this business need with the least custom work? It covers the Copilot family (Microsoft Copilot, Copilot Chat, Microsoft 365 Copilot, Researcher and Analyst), Microsoft Graph and permissions, Copilot Studio and the extensibility framework, and Microsoft Foundry with Foundry Tools. It closes with model selection, process mapping, the Buy / Extend / Build decision, and the governance work a Copilot rollout needs before go-live.

<div class="note-scribble"><strong>Naming note.</strong> Azure AI Foundry was renamed <strong>Microsoft Foundry</strong> at Microsoft Ignite in November 2025, and Azure AI services were rebranded <strong>Foundry Tools</strong>. The AB-731 study guide uses the new names; older material and some answer options may still say "Azure AI Foundry". Both refer to the same platform.</div>

---

## 2.1 The Microsoft AI Stack

### Key Concept

**Pick the highest layer of Microsoft's AI stack that still meets the requirement; each layer down costs build time.**

Microsoft's AI offering is structured in four layers, from raw models and compute to ready-made applications. Knowing which layer a product lives in is how you answer most "which product?" questions in this domain.

Each layer trades flexibility for speed. A business user at the Applications layer gets zero setup time but little customisation; a developer at the Foundation layer gets full control over model choice and infrastructure but has to build everything above it. **Think of it like buying a house versus building one**: the further down you start, the more you control and the more you have to construct yourself.

| Layer | What it provides | Key products |
|---|---|---|
| **1 — Foundation** | AI models + compute infrastructure | Azure OpenAI (in Foundry Models), Foundry Models catalog (e.g. GPT-4o, Phi, Llama, Mistral) |
| **2 — Platform** | Developer tools to build, evaluate, and deploy AI solutions | Microsoft Foundry, Azure AI Search, Azure Vision in Foundry Tools |
| **3 — Extensibility** | Low-code/no-code agent builder and Copilot extensions | Microsoft Copilot Studio, declarative agents, Copilot connectors |
| **4 — Applications** | Ready-to-use AI embedded in productivity apps | Microsoft 365 Copilot, Microsoft Copilot (consumer), Copilot Chat |

<div class="note-important"><strong>How the layers connect:</strong> Foundation models power the Platform tools. Platform tools power the Extensibility layer. Extensibility customises the Applications. Responsible AI principles span all four layers.</div>

Model names in this note (GPT-4o, Phi-3, Llama, Mistral) are illustrative. The Foundry Models catalog changes often, so the exam tests the type of model you need, not a specific version.

**Responsible AI spans all layers** — Microsoft's six principles (Fairness, Reliability and safety, Privacy and security, Inclusiveness, Transparency, Accountability) are applied at every level, from model training to end-user UI.

![Business users reach Microsoft 365 Copilot, Microsoft Copilot and Copilot Studio, with Microsoft Graph as the org data connector, while developers and IT build on Microsoft Foundry (formerly Azure AI Foundry) with Azure AI Search and Azure Vision.](/content/skillup/ab731/images/ab731-d2-ai-products-by-audience.svg)

### Benefits of an integrated Microsoft AI solution (risk mitigation and safety)

The study guide asks you to name what you gain by staying inside one Microsoft stack rather than stitching together unrelated tools:

| Benefit | What it means in practice |
|---|---|
| **One identity and permission model** | Microsoft Entra ID sign-in and existing Microsoft 365 permissions apply to Copilot, agents and Graph-grounded answers. Copilot only surfaces what the user can already open. |
| **Enterprise data protection** | Work prompts and responses in Copilot Chat and Microsoft 365 Copilot are covered by enterprise data protection, and customer content isn't used to train the foundation models. |
| **Compliance tooling already in place** | Sensitivity labels, retention, DLP and audit (Microsoft Purview) and SharePoint Advanced Management apply to AI interactions as well as to files. |
| **Built-in safety on custom builds** | Microsoft Foundry adds content safety filters, evaluations and monitoring to custom apps and agents. |

### In Practice

**What breaks without this**: teams build from the bottom of the stack by default, so a need that out-of-the-box Copilot already met turns into a six-month custom project with its own hosting, security review and maintenance backlog.

**Decision trigger**: ask, "what is the highest layer where this requirement is already met?" Start at Applications and only drop a layer when the scenario rules out everything above it (external users, a custom model, data Copilot can't reach).

**When you'd choose differently**: if the core requirement is a capability no higher layer offers, such as training a custom model on proprietary data or serving anonymous public users at high volume, starting at the Platform layer is the right call, not over-engineering.

### Exam Trap ⚠️

<div class="note-trap">
Common distractor: the most powerful-sounding product. When a scenario says "business users in Word and Teams", an answer built on Microsoft Foundry is wrong even though it would technically work. The exam rewards the highest layer that meets the requirement, the way you'd buy a ready-made suit before commissioning a tailor.
</div>

---

## 2.2 Microsoft Copilot vs Copilot Chat vs Microsoft 365 Copilot

### Key Concept

**The versions of Copilot differ in one thing above all: how much of your organisation's data they can reason over.**

Microsoft offers three Copilot experiences that exam questions deliberately blur. Microsoft Copilot is the consumer assistant. Copilot Chat is the free, enterprise-protected chat for work accounts. Microsoft 365 Copilot is the paid add-on that grounds answers in your Microsoft Graph data and works inside the apps.

The deciding feature is Microsoft Graph grounding. Only the licensed Microsoft 365 Copilot reasons broadly across your emails, meetings, chats, files and sites; Copilot Chat is mainly web-grounded, plus whatever content a user uploads or an agent provides. **Think of it like three keys to the same building**: one opens the lobby, one opens the lobby with security watching, and one opens the offices you're cleared for.

| | **Microsoft Copilot** (consumer) | **Copilot Chat** (work, included) | **Microsoft 365 Copilot** (work, licensed) |
|---|---|---|---|
| **Audience** | Anyone with a personal account | Eligible Microsoft 365 work/school users | Users assigned the paid add-on licence |
| **Grounding** | Web | Primarily web + uploaded files + agents (limited org grounding in Outlook) | Web + **Microsoft Graph** (emails, docs, Teams chats, calendar) + semantic index |
| **Enterprise data protection** | ❌ No | ✅ Yes | ✅ Yes |
| **Copilot inside Word/Excel/PowerPoint with org data** | ❌ No | ❌ Not the full experience | ✅ Yes |
| **Licence** | Free (consumer) | Included at no extra cost | Paid add-on — list price ~US$30/user/month on an annual commitment; check current pricing |
| **Use case** | General web research, personal tasks | Secure work chat on web content and files | Work productivity with YOUR org data |

The paid licence sits on top of a broad range of base plans, not just enterprise E-plans: Microsoft 365 E3/E5, Business Basic/Standard/Premium, Office 365 E1/E3/E5, F1/F3 and others are eligible ([licensing options](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-licensing)). Microsoft's newest docs sometimes shorten the licensed product's name to "Microsoft Copilot". The exam keeps "Microsoft 365 Copilot" for the work product and "Microsoft Copilot" for the consumer one.

<div class="note-scribble">The key differentiator: Microsoft Graph. M365 Copilot can answer "Summarise last week's emails about Project X" because it reads YOUR Graph data. Free Microsoft Copilot cannot do this.</div>

### In Practice

**What breaks without this**: an organisation buys the paid licence for every employee when most only needed secure web chat, or it assumes Copilot Chat will summarise everyone's SharePoint content and then finds the free tier can't reach it.

**Decision trigger**: ask, "does this user need answers grounded in their own emails, meetings and files, inside the apps?" If yes, that's the Microsoft 365 Copilot licence. If they only need secure chat over web content and documents they upload, Copilot Chat already covers them.

**When you'd choose differently**: a user who needs Graph grounding only for one narrow task can be served by an agent in Copilot Chat on pay-as-you-go billing, rather than a full per-user licence.

### Exam Trap ⚠️

<div class="note-trap">
<strong>This is a favourite exam trap.</strong> "Microsoft Copilot" and "Microsoft 365 Copilot" are different products, and Copilot Chat is a third. If an answer says the free or consumer Copilot can summarise your organisation's SharePoint content, it's wrong. Only the licensed Microsoft 365 Copilot grounds broadly in Microsoft Graph. A visitor's badge and an employee's badge both get you through the front door, but only one opens the filing room.
</div>

---

## 2.3 Microsoft Graph — The Data Connector

### Key Concept

**Microsoft Graph is why Microsoft 365 Copilot knows your organisation, and why it can't see past your permissions.**

Microsoft Graph is the **API layer that connects Copilot to your organisation's data** stored in Microsoft 365 services. When a user asks a question, Copilot retrieves relevant content through Graph under that user's identity, then grounds its answer in what came back.

Because retrieval runs as the user, Copilot inherits their access exactly. It can't open a file the user couldn't open, and no data is shared across tenants. **Think of Graph as a librarian who fetches books on your library card**: fast and thorough, but only from the shelves your card unlocks.

![Microsoft 365 Copilot reaches Outlook, Teams, SharePoint, OneDrive and the Microsoft 365 apps through the Microsoft Graph API.](/content/skillup/ab731/images/ab731-d2-graph-data-connector.svg)

**Why it matters for Copilot:**
- When you ask Copilot "What are my action items from today's meetings?" — Graph pulls your Teams transcripts and calendar
- Copilot **respects existing permissions** — you only see data you're already authorised to see
- No data is shared across tenants
- Copilot connectors (§2.8) bring content from outside Microsoft 365 into Graph so Copilot can use it too

<mark>Exam key point: Microsoft Graph is WHY M365 Copilot knows about your specific org. Without Graph, Copilot would only know public internet information.</mark>

### In Practice

**What breaks without this**: leaders treat Copilot as a separate data store that needs its own access rules, and spend weeks designing per-role filters that duplicate permissions Microsoft 365 already enforces.

**Decision trigger**: ask, "where does this data live?" If it's in Exchange, SharePoint, OneDrive or Teams, Graph already reaches it. If it's in a third-party system, you need a Copilot connector or an agent with an action before Copilot can use it.

**When you'd choose differently**: for data that must never be surfaced by AI even to users who technically have access, permission inheritance isn't enough. Restrict discoverability or apply sensitivity labels first (§2.15).

### Exam Trap ⚠️

<div class="note-trap">
Two opposite distractors: "Copilot can see all company data" and "you must build custom role filters for Copilot". Both are wrong. Copilot sees exactly what the user's existing Microsoft 365 permissions allow, through Graph, nothing more and nothing less. It works like a mirror of your access, not a master key.
</div>

---

## 2.4 Copilot in Microsoft 365 Apps

### Key Concept

**Each app's Copilot does what that app's content allows; it's one model reasoning over different structured content.**

Copilot's capabilities differ per app because each app stores different material. Excel holds structured tables, Teams holds timestamped transcripts, and Outlook holds threads.

Excel's formula generation and chart creation work because a spreadsheet is already structured data Copilot can reason over directly. Teams' meeting recap works because Teams already captures a transcript Copilot can summarise. **Think of Copilot as one interpreter visiting different rooms**: same skills each time, but what it can tell you depends on what's in the room.

| App | Key Copilot capabilities |
|---|---|
| **Word** | Draft, rewrite, summarise documents; generate from outline |
| **Excel** | Analyse data, generate formulas, create charts, highlight trends |
| **PowerPoint** | Generate presentations from a Word doc or prompt; add slides; design suggestions |
| **Outlook** | Draft emails, summarise threads, schedule meetings, coaching on tone |
| **Teams** | Meeting transcription + summary, action items, live translation, chat summaries |
| **OneNote** | Organise notes, generate summaries, create to-do lists |
| **Loop** | Collaborative workspaces with AI-generated content that stays in sync |

<div class="note-important"><strong>Exam pattern:</strong> "A manager needs to quickly catch up on a 2-hour meeting they missed. Which Copilot feature is most appropriate?" → Teams Copilot meeting recap / summary.</div>

### In Practice

**What breaks without this**: training that tours every feature in every app leaves employees unsure which app to open for their actual task, so adoption stalls at "I tried it once".

**Decision trigger**: ask, "where does the content for this task already live?" Meeting content means Teams, a dataset means Excel, a thread means Outlook. Start Copilot where the content is.

**When you'd choose differently**: when a task spans several sources (emails, a deck and meeting notes together), Copilot Chat grounded in work data is a better starting point than any single app.

### Exam Trap ⚠️

<div class="note-trap">
Distractors offer a workaround in the wrong app, such as exporting a Teams transcript into Word to summarise it. The exam rewards the app that natively holds the content: Teams for missed meetings, Excel for data, Outlook for threads. Don't carry the water to the well.
</div>

---

## 2.5 Copilot Chat (Web & Mobile)

### Key Concept

**Copilot Chat is the included, enterprise-protected chat for work accounts; it's mainly web-grounded unless the user is licensed.**

**Copilot Chat** is the secure chat experience available to eligible Microsoft 365 users at no extra cost. Work users reach it at m365copilot.com, in the Microsoft 365 Copilot app (web and mobile), in Teams and Outlook, and in the Edge side pane. copilot.microsoft.com is the consumer Microsoft Copilot, not the work experience ([Copilot Chat overview](https://learn.microsoft.com/en-us/copilot/overview)).

What it can reach depends on the licence. Without the Microsoft 365 Copilot licence it's primarily web-grounded, plus files the user uploads, agents, and limited organisational grounding in Outlook. With the licence, the same chat reasons broadly across Graph data. **Think of it as the same front desk with two levels of clearance**: everyone gets help, but only cleared staff can ask about the files in the back office.

- Included for eligible Microsoft 365 work and school users, with **enterprise data protection**
- **Web-grounded** answers for everyone; **work data** grounding through Microsoft Graph for Microsoft 365 Copilot-licensed users
- Supports **file uploads** for analysis
- Can **create images**
- Can **use agents**. Agents used by unlicensed Copilot Chat users are billed **pay-as-you-go** through an Azure subscription ([pay-as-you-go overview](https://learn.microsoft.com/en-us/copilot/microsoft-365/pay-as-you-go/overview))

**Work vs Web scope:** licensed users choose whether a chat is grounded in their organisation's data (Microsoft Graph) or the public web. This work/web scope control is a common exam concept (see the diagram in §2.11).

### In Practice

**What breaks without this**: an organisation tells all employees "you have Copilot" when most only have Copilot Chat, and support tickets pile up from users who expected it to find their SharePoint files.

**Decision trigger**: ask, "does this group need secure AI chat, or AI over their own organisational data?" Secure chat means Copilot Chat, already included. Organisational data means the licence or a scoped agent.

**When you'd choose differently**: for a heavily regulated group where even web-grounded chat isn't acceptable, admins can turn web grounding off or restrict access. "Included" doesn't mean it must be switched on for everyone.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "Copilot Chat requires a Microsoft 365 Copilot licence" or "Copilot Chat searches all your work files for free". Both are wrong. Copilot Chat is included at no extra cost and is web-first; broad Graph grounding comes with the paid licence. Think of a free public library card versus a staff pass to the archive.
</div>

---

## 2.6 Researcher and Analyst in Copilot

### Key Concept

**Researcher synthesises sources into a report; Analyst crunches data with code. Pick by input: documents or datasets.**

Microsoft 365 Copilot includes two specialised reasoning **agents** for work that's too deep for a single chat turn. Both take longer and plan multiple steps, but they're built for different inputs.

Researcher gathers and synthesises information across the web and your organisation's data (and connected sources) into a structured, cited report. Analyst works through raw data, writing and running Python to clean, analyse and chart it. **Think of Researcher as the journalist and Analyst as the statistician**: one tells you what the sources say, the other tells you what the numbers say.

| Agent | Purpose | Best for |
|---|---|---|
| **Researcher** | Deep research using the web + your org data | Building comprehensive reports, competitive analysis, literature review |
| **Analyst** | Data analysis, running Python code, generating visualisations | Analysing spreadsheets, surfacing trends, creating charts from data |

<div class="note-scribble">Researcher = web + docs research. Analyst = data crunching. If the exam gives a scenario about analysing a sales CSV → Analyst. If it's about researching market trends → Researcher.</div>

### In Practice

**What breaks without this**: a team asks Researcher to find growth trends in a 50,000-row file and gets a narrative summary instead of the calculated answer, or asks Analyst for a market landscape that needs reading, not computation.

**Decision trigger**: ask, "is the main input a set of documents and web sources, or a dataset?" Documents point to Researcher; rows and columns point to Analyst.

**When you'd choose differently**: for a quick formula or chart on a small sheet, Copilot in Excel is faster than invoking a reasoning agent. For a company-specific workflow with its own rules, you need a custom agent in Copilot Studio (§2.7), not either built-in agent.

### Exam Trap ⚠️

<div class="note-trap">
Distractors swap the two agents, or say a built-in agent can run a proprietary business process. Researcher is for multi-source research and reports; Analyst is for data analysis with code. Neither replaces a custom Copilot Studio agent for company-specific logic. A good journalist still isn't your accountant.
</div>

---

## 2.7 Microsoft Copilot Studio

### Key Concept

**Copilot Studio is the low-code builder for custom agents over your own knowledge, actions and channels.**

**What it is:** a low-code/no-code platform to **build custom AI agents** connected to your organisation's data and processes. **Who uses it:** IT professionals, power users and business analysts — no coding required.

It fills the gap between out-of-the-box Copilot and a fully coded build. You give an agent knowledge sources, actions it can take through connectors and Power Automate, and the channels where it lives. **Think of Copilot Studio as a kit-car workshop**: you assemble something tailored from proven parts, without machining the engine yourself.

**Key capabilities:**
- Create custom agents with specific knowledge bases (SharePoint, websites, documents)
- Publish to Teams, Microsoft 365 Copilot, websites, mobile apps
- Integrate with Power Platform (Power Automate for actions)
- Connect to third-party systems via connectors
- Create custom agents for specific business functions (HR bot, IT helpdesk, sales assistant)

![Copilot Studio connects to a knowledge base, Power Automate actions and connectors to other systems.](/content/skillup/ab731/images/ab731-d2-copilot-studio-building-blocks.svg)

**Billing:** since 1 September 2025 Copilot Studio usage is measured in **Copilot Credits** (formerly "messages"), bought as prepaid packs or on pay-as-you-go through an Azure subscription. When Microsoft 365 Copilot-licensed users use agents in Copilot Chat, Teams or SharePoint for generative answers or Graph grounding, that usage is zero-rated ([Copilot Studio licensing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)).

<div class="note-important"><strong>Build vs Buy vs Extend:</strong><br/><strong>Buy</strong> = Use M365 Copilot out-of-the-box (no customisation)<br/><strong>Extend</strong> = Use Copilot Studio to customise/extend M365 Copilot<br/><strong>Build</strong> = Use Microsoft Foundry to build a custom AI application from scratch</div>

### In Practice

**What breaks without this**: every department request for a specialised assistant joins the developer backlog, so a simple HR policy bot waits months behind custom-code projects.

**Decision trigger**: ask, "can this be described as knowledge + a few actions + a channel?" If yes, it's a Copilot Studio agent. If it needs a custom-trained model or bespoke orchestration code, move to Microsoft Foundry.

**When you'd choose differently**: if Microsoft 365 Copilot or a built-in agent already answers the question from existing Graph data, building any agent is unnecessary. Use what's there first.

### Exam Trap ⚠️

<div class="note-trap">
Distractor: "Copilot Studio is for developers training models" or "a customer-facing helpdesk bot needs Foundry". Copilot Studio is low-code, supports external channels, connectors and human handoff, and doesn't train models. Choose Foundry only when the scenario needs custom model work. You don't need a foundry to assemble furniture from a flat-pack.
</div>

---

## 2.8 M365 Copilot Extensibility Framework

### Key Concept

**Extend Copilot by giving it new knowledge (connectors), new skills (actions), or a focused role (agents).**

When out-of-the-box Copilot isn't enough, the extensibility framework lets you add to it rather than replace it. The building blocks answer different gaps: Copilot can't see some data, can't act in some system, or needs to behave as a specialist for one task.

Copilot connectors (formerly Microsoft Graph connectors) bring external content into Graph so Copilot can search it. Actions let an agent call an API or MCP server. Declarative agents wrap instructions, knowledge and actions around Copilot's own model, while custom engine agents bring their own model and orchestration. **Think of it like staffing a desk**: connectors stock the shelves, actions hand over the tools, and an agent is the job description.

| Extension type | What it does | Who builds it |
|---|---|---|
| **Copilot connectors** (formerly Graph connectors) | Bring external content (e.g. Confluence, ServiceNow) into Microsoft Graph and the semantic index so Copilot can use it | IT/Developers |
| **Actions** (API plugins or MCP servers) | Let a declarative agent call an external API or tool — e.g. look up or update a CRM record. This is what older material calls a "plugin" | Developers / Copilot Studio |
| **Declarative agents** | Copilot's own model and orchestrator, scoped with custom instructions, knowledge and actions | Copilot Studio agent builder / Microsoft 365 Agents Toolkit |
| **Custom engine agents** | Your own model and orchestration, e.g. built on Microsoft Foundry or Copilot Studio's full experience | Developers |

Microsoft now uses **"plugin"** for an installable package that bundles declarative agents, skills, Copilot connectors and MCP integrations for a task ([What is a Microsoft 365 Copilot plugin?](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/plugins-overview)). On the exam, treat "plugin" in older wording as "give Copilot a new capability".

<mark>Exam pattern: "A company wants Copilot to answer questions from their internal knowledge base in Confluence. What's the best approach?" → A Copilot connector to bring Confluence content into Graph, or a declarative agent in Copilot Studio with Confluence as its knowledge.</mark>

### In Practice

**What breaks without this**: teams build a separate chatbot for each external system, so users juggle five assistants that each know one corner of the business, and none sits inside the Copilot they already use.

**Decision trigger**: ask, "is the gap knowledge, action or focus?" Missing knowledge points to a connector, a missing ability to act points to an action, and a need for specialist behaviour points to a declarative agent.

**When you'd choose differently**: when you need a different model, your own orchestration logic, or an experience outside Microsoft 365 entirely, a custom engine agent (or a full Foundry build) is justified over a declarative agent.

### Exam Trap ⚠️

<div class="note-trap">
Distractors propose fine-tuning a model or building a separate Foundry app to make Copilot aware of an internal system. Making external data available to Copilot is an extensibility problem: a connector or a declarative agent, not model training. Add a shelf to the library; don't rebuild the library.
</div>

---

## 2.9 Microsoft Foundry and Foundry Tools

### Key Concept

**Microsoft Foundry is the platform for custom AI apps and agents; Foundry Tools are its prebuilt AI building blocks.**

**Microsoft Foundry** (formerly Azure AI Foundry) is Microsoft's platform for building, deploying and managing enterprise AI solutions: model choice, prompt and agent development, evaluation, deployment and monitoring. **Foundry Tools** (formerly Azure AI services) are the prebuilt capabilities you plug in: Speech, Language, Translator, Azure Vision, Document Intelligence, Content Understanding and others, plus Azure AI Search for retrieval.

You reach for Foundry when the need is too custom for Copilot or Copilot Studio: a public-facing app, a custom model, or AI embedded in your own product. **Think of Foundry as a professional kitchen and Foundry Tools as its appliances**: the kitchen gives you space, safety rules and workflow, and the appliances do specialised jobs you'd never build yourself.

<div class="note-important"><strong>Terminology update:</strong> At Microsoft Ignite in November 2025, Microsoft renamed <strong>Azure AI Foundry</strong> to <strong>Microsoft Foundry</strong> (formalised in the January 2026 product terms), and rebranded Azure AI services as <strong>Foundry Tools</strong>. The AB-731 study guide uses "Microsoft Foundry" and "Foundry Tools", but its resource list still labels the docs link "Azure AI Foundry documentation", so both names can appear in questions and answer options. They refer to the same platform.</div>

### What's in Foundry Tools

| Tool | What it does |
|---|---|
| **Microsoft Foundry** | End-to-end AI project hub — model selection, prompt flows, evaluation, deployment |
| **Azure AI Search** | Vector + semantic search — the retrieval layer for RAG solutions |
| **Azure Vision in Foundry Tools** | Computer vision — image analysis, OCR, object detection (face analysis is a separate tool, Azure AI Face, with limited-access restrictions) |
| **Foundry Models catalog** | Access to a large catalog of models: OpenAI (e.g. GPT-4o), Microsoft (Phi), open models (Llama, Mistral) and others |

### Benefits of Microsoft Foundry and Foundry Tools
- **Scalability** — scales from prototype to millions of users on Azure infrastructure
- **Security** — enterprise-grade access control (Microsoft Entra ID), private networking, content filters
- **Choice** — use any model from the catalog, not locked to one vendor
- **Governance** — built-in responsible AI tooling, content safety filters, evaluations

<div class="note-important"><strong>Business scenario → Tool mapping:</strong><br/>📄 Understand documents from photos → Azure Vision (OCR)<br/>🔍 Search across thousands of internal documents → Azure AI Search<br/>🤖 Build a custom customer service bot → Microsoft Foundry + Copilot Studio<br/>📊 Analyse images from a factory floor → Azure Vision in Foundry Tools</div>

### In Practice

**What breaks without this**: a team builds OCR, search and content moderation from scratch for a customer app, spending months on solved problems and shipping without the safety filters Foundry provides by default.

**Decision trigger**: ask, "is there a prebuilt Foundry Tool for this step?" Reading images or documents points to Vision or Document Intelligence, finding relevant content points to Azure AI Search, and speech points to Speech. Compose those inside Foundry before writing custom models.

**When you'd choose differently**: if the users are employees working in Microsoft 365 and the data is already in Graph, Copilot or a Copilot Studio agent gets there faster with less to operate than a Foundry build.

### Exam Trap ⚠️

<div class="note-trap">
Look-alike names: "Foundry" (the platform) versus "Foundry Tools" (the prebuilt services), and "Azure AI Foundry" versus "Microsoft Foundry" (same platform, old and new names). Don't eliminate an answer just because it uses the older name. Like a company that changed its logo, it's still the same company.
</div>

---

## 2.10 Matching AI Models to Business Needs

### Key Concept

**Model choice is a latency-cost-accuracy trade-off; the biggest model is rarely the best fit.**

Not all models are equal, and the exam tests whether you match model characteristics to the task. Larger models reason better over long or ambiguous input; smaller models answer faster and cheaper.

A larger model like GPT-4o does more computation per token, which buys stronger reasoning at the price of higher latency and cost. A smaller model like Phi-3 does less work per token, which suits a real-time chat widget where users notice a half-second delay. **Think of it like choosing a vehicle**: you don't take a lorry to post a letter, and you don't move house on a scooter.

| Business need | Model characteristic to look for |
|---|---|
| Real-time chat with customers | Low latency, cost-effective (smaller model e.g. Phi) |
| Complex legal document analysis | High accuracy, large context window (e.g. GPT-4o) |
| Code generation at scale | Code-specialised model |
| Multilingual customer support | Strong multilingual capabilities |
| Image understanding | Multimodal model (vision + text) |
| On-premise deployment | Small, deployable model (e.g. Phi-3 mini) |

<div class="note-scribble">The exam won't ask you to memorise specific model benchmarks. It tests the concept: bigger/more expensive model ≠ always better. Match capability to task. Phi-3 for simple tasks, GPT-4o for complex reasoning.</div>

### In Practice

**What breaks without this**: a high-volume FAQ bot runs on a frontier model and the monthly bill grows tenfold with no quality gain users notice, or a compliance review runs on a tiny model and misses the conflicts it was built to catch.

**Decision trigger**: ask, "what does a wrong or slow answer cost here?" If it's cheap and speed matters, go small. If a miss is expensive, pay for accuracy.

**When you'd choose differently**: when both volume and stakes are high, route requests: a small model handles routine cases and a larger model takes the hard ones (see §2.13).

### Exam Trap ⚠️

<div class="note-trap">
Two mirror-image distractors: "always use the most capable model" and "always use the cheapest model". Optimising cost means total cost, including the cost of wrong answers. Fit the model to the job, like hiring a specialist surgeon for surgery and not for taking blood pressure.
</div>

---

## 2.11 Copilot Experiences — Pages, Chat, and Cross-App Features

### Key Concept

**Chat answers in the moment; Pages keeps AI output as a shared, editable artifact the team keeps building.**

Beyond per-app features, Microsoft 365 Copilot includes cross-app experiences. Copilot Chat is the single place to ask about all your work data or the web, and Copilot Pages turns a chat response into a persistent canvas others can edit.

The difference that matters is persistence and collaboration. A chat session belongs to one user and scrolls away; a Page is shared, stays put, and multiple people can keep adding Copilot-generated content to it. **Think of Chat as a conversation and Pages as the whiteboard you leave up after the meeting.**

| Experience | What it is | Key differentiator |
|---|---|---|
| **Copilot Chat** (formerly Business Chat / BizChat) | Unified chat interface — query across all your work data (emails, docs, Teams, calendar) or web | Single place to ask anything about your work |
| **Copilot Pages** | Collaborative AI canvas — Copilot populates it, multiple users can continue editing | Persistent, shareable AI-generated artifact (unlike a single-session chat) |
| **Work / Web scope** | In Copilot Chat, licensed users switch between org data (Microsoft Graph) and Bing web search | Explicitly controls whether the AI searches your internal data or the public web |

![Copilot Chat's Work toggle searches Microsoft Graph org data while the Web toggle searches Bing.](/content/skillup/ab731/images/ab731-d2-copilot-chat-work-web-toggle.svg)

<div class="note-scribble">Copilot Chat is the power user's home base — if you need to ask "what did my team work on last week?" or "find all emails about Project X and summarise the key decisions", Copilot Chat with the Work scope does this in one place. No need to open four apps.</div>

### In Practice

**What breaks without this**: a research team each keeps private chat threads, then someone spends a day copy-pasting outputs into one document, and the best findings get lost in individual histories.

**Decision trigger**: ask, "will more than one person keep building on this AI output over days?" If yes, use Pages. If it's a one-off question, use Chat.

**When you'd choose differently**: when the output is a formal deliverable with tracked changes, a template or approval workflow, draft it with Copilot in Word, where those document controls live.

### Exam Trap ⚠️

<div class="note-trap">
<strong>Pages vs Word:</strong> "A team needs a shared AI-populated document where multiple members can continue adding Copilot-generated research" → <strong>Copilot Pages</strong> (multi-user, persistent, AI-populated). NOT Word Copilot in separate documents, and NOT individual chat sessions. Notes passed around a table get lost; a shared whiteboard doesn't.
</div>

---

## 2.12 Mapping Business Processes to Copilot

### Key Concept

**Start Copilot where tasks are repetitive or draftable; leave judgment-heavy and relationship work to people.**

Not every task benefits equally from AI. Mapping a process means listing its tasks, classifying each by how much AI can take on, and starting where the return is fastest.

Automatable and augmentable tasks are high-frequency and time-consuming, so every saved minute repeats every week. Judgment-heavy and relationship-based work gains far less, because the human expertise or connection *is* the value. **Think of it like sorting laundry before washing**: separate what the machine handles from what needs hand care, and you get faster results with fewer ruined shirts.

| Task type | AI benefit | Best Copilot application |
|---|---|---|
| **Automatable** | Highest — repetitive, structured, rule-based | Meeting summaries, email triage, invoice data extraction |
| **Augmentable** | High — knowledge work where AI drafts and humans refine | Writing proposals, data analysis in Excel, research in Chat |
| **Judgment-heavy** | Lower — deep expertise + ethics required | Complex legal interpretation, senior strategic decisions |
| **Relationship-based** | Minimal — human connection IS the value | Client relationship management, counselling, coaching |

### The mapping process

![Four steps to map a business process to Copilot: list tasks, classify them, prioritise automatable and augmentable work, then map to a Copilot feature.](/content/skillup/ab731/images/ab731-d2-process-to-copilot-mapping.svg)

<div class="note-important"><strong>Exam pattern:</strong> "Which tasks should be prioritised for Copilot deployment?" → Automatable tasks first (meeting summaries, email drafts, document extraction) — fastest, clearest ROI. Augmentable tasks (analysis, writing) second. Never start with judgment-heavy or relationship tasks.</div>

### In Practice

**What breaks without this**: a rollout leads with an impressive but rare use case, such as drafting board strategy, so most employees never see daily value and usage drops after the launch week.

**Decision trigger**: ask, "how often does this task happen, and could a first draft or summary save most of the time?" Frequent and draftable tasks go first.

**When you'd choose differently**: a judgment-heavy task can still gain from AI as a research or preparation aid, such as gathering precedents before a legal review. The human decision stays human.

### Exam Trap ⚠️

<div class="note-trap">
Distractors put judgment-heavy or relationship tasks first because they sound high-value. For fastest Copilot ROI, the exam picks automatable and augmentable tasks: high frequency, measurable time saved. Pick the low-hanging fruit before you climb the tree.
</div>

---

## 2.13 Choosing the Right Foundry Model

### Key Concept

**Choose a Foundry model by task complexity, deployment constraint and total cost, not by leaderboard rank.**

The Foundry Models catalog offers many model families, and the exam tests matching a business need to a model type. Complexity of reasoning, where the model must run, and how you want to pay all narrow the choice.

Open models like Llama and Mistral earn their place for reasons other than raw capability: published weights mean you can fine-tune them without vendor lock-in or run them entirely on your own infrastructure. The trade-off is ownership of hosting, scaling and security. **Think of it as leasing versus owning a building**: owning removes the rent, but the repairs are now yours.

| Scenario | Best model choice | Why |
|---|---|---|
| Complex legal reasoning, long documents | **Large frontier model (e.g. GPT-4o)** | High accuracy, large context window, strong reasoning |
| Real-time customer chat at low cost | **Small model (e.g. Phi-3 mini/small)** | Lightweight, fast, cost-effective for simple tasks |
| On-premise or edge deployment (no cloud) | **Small open-weight model (e.g. Phi-3 mini)** | Small enough to run locally |
| Budget-conscious, open-source preferred | **Open model (e.g. Llama / Mistral)** | Self-hosted = no per-token fee (you pay for and run the infrastructure); customisable |
| Domain-specific brand voice / jargon | **Fine-tuned model** | When base model cannot learn domain via prompting |
| Image + text understanding | **Multimodal model (e.g. GPT-4o)** | Vision + language in one model |

"No per-token cost" applies only when you host the model yourself. Open models deployed as serverless or standard deployments in Microsoft Foundry are billed per token like any other managed model.

![Decision tree for choosing a Foundry model: proprietary for complex reasoning, Phi-3 for budget or edge, open source for cost control.](/content/skillup/ab731/images/ab731-d2-foundry-model-choice.svg)

### In Practice

**What breaks without this**: a regulated team picks a managed API for data that contractually can't leave its facility, or picks "free" open source and then discovers the cost of running GPU infrastructure it never budgeted for.

**Decision trigger**: ask three questions in order. Where must it run (cloud, on-premises, edge)? How hard is the reasoning? How will we pay (per token, reserved capacity, or our own hardware)?

**When you'd choose differently**: if the team has no capacity to operate infrastructure and no residency constraint, a managed deployment in Foundry, billed per token, usually beats self-hosting even for open models.

### Exam Trap ⚠️

<div class="note-trap">
"Bigger model = always better" is WRONG. Using GPT-4o for a simple FAQ chatbot is expensive overkill; using Phi-3 for complex multi-document contract analysis will produce poor results. Also watch for "open source is always free": it's free of per-token fees only when you host it yourself. A free puppy still needs feeding.
</div>

---

## 2.14 Buy / Build / Extend Decision Framework

### Key Concept

**Buy what exists, extend what almost fits, and build only when nothing in Microsoft 365 can serve the use case.**

The AB-731 exam often asks for the *most appropriate* solution, and this framework is how you answer. Each step down the ladder adds cost, time and maintenance, so you need a reason to take it.

Buying is Microsoft 365 Copilot as-is. Extending adds your data or workflows through Copilot Studio, connectors and agents. Building means a standalone agent or a Microsoft Foundry application. **Think of it like furnishing an office**: buy the standard desk, add a custom shelf if you need one, and only commission bespoke joinery when nothing off the shelf fits the room.

| Approach | When to choose | Microsoft product |
|---|---|---|
| **Buy** | Need AI capability immediately, no customisation required | Microsoft 365 Copilot (out-of-box) |
| **Extend** | Need to add org-specific data or workflows to existing Copilot | Copilot Studio (extend M365 Copilot with agents, actions, connectors) |
| **Build** | Need fully custom AI experience, not based on M365 Copilot | Copilot Studio (standalone agent) or Microsoft Foundry |

Cost follows the same ladder: Buy is a per-user licence, Extend and standalone Copilot Studio agents consume Copilot Credits (zero-rated for many licensed-user scenarios, §2.7), and Foundry builds are billed by Azure consumption.

<div class="note-important"><strong>Exam rule:</strong> "Extend" is the answer when a business already has M365 Copilot and wants to add capabilities. "Build" from scratch (Foundry) is only justified when M365 Copilot cannot serve the use case at all (e.g., external-facing customer chatbot on a public website).</div>

### In Practice

**What breaks without this**: a company with Microsoft 365 Copilot already deployed builds a separate Foundry app for an internal knowledge base, then pays to host, secure and maintain something an agent in Copilot would have covered.

**Decision trigger**: ask, "who are the users and where is the data?" Internal users with Microsoft 365 data point to Buy or Extend. External users, a custom model, or a product feature point to Build.

**When you'd choose differently**: even for internal users, a Build is justified when the requirement needs a custom model, specialised orchestration, or integration into a line-of-business app outside Microsoft 365.

### Exam Trap ⚠️

<div class="note-trap">
Distractors jump straight to Build because it sounds most capable. The exam's default order is Buy, then Extend, then Build, and each step needs a requirement the previous one can't meet. Don't build a bridge where a ferry already runs.
</div>

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

Use **SharePoint Advanced Management** to do this work before rollout, not after. It's included with the Microsoft 365 Copilot licence ([Copilot Studio licensing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing) lists what the licence includes):

| SharePoint Advanced Management action | What it does |
|---|---|
| **Oversharing report** | Surfaces sites/files shared far more broadly than their sensitivity warrants |
| **Restrict content discoverability** | Excludes selected sites from org-wide search and Copilot retrieval without changing who can still open the file directly |
| **Site access review** | Flags stale permissions and inactive guest access for removal |
| **Sensitivity labels + auto-labelling** | Applies protection (encryption, access restriction) to sensitive content before an AI feature can retrieve it |

### Exam Trap ⚠️

<div class="note-trap">"Disable Graph connectivity entirely" and "make every employee individually re-request access" are both overcorrections — they block legitimate work instead of fixing the actual problem. The correct action is targeted: find the overshared content, shrink its discoverability, label it — then roll out. Doing nothing ("permission inheritance is enough") and doing too much (disabling Graph) are both wrong for the same reason: neither actually looks at what's overshared.</div>

---

## 2.16 Automating Multi-Step Business Processes with Copilot Studio

### Key Concept

**A Copilot Studio agent can trigger itself and run a whole workflow; ad hoc Copilot chat needs a human to prompt every single step.**

Using Copilot in Outlook to draft one onboarding email is assistive — someone has to open the app, remember what's needed, and ask, one exchange at a time (this is the same Copilot-vs-agent distinction as D1 §1.10, applied to a concrete business process). A Copilot Studio agent removes the human from the loop between steps: it can trigger automatically on an event — a new hire record appearing in the HR system — and then sequence the IT ticket, the access request, and the facilities notification itself, tracking status across all of them.

**Think of ad hoc Copilot chat as phoning a colleague for one favour at a time; a Copilot Studio process agent is handing that colleague a checklist and the authority to work through it unsupervised**, only interrupting you at the one step that genuinely needs a human decision.

![Flow diagram for "Key Concept": triggers agent, yes: high-risk access, no: standard request, New hire added to HRsystem, Copilot Studio agent starts, Create IT ticket, Initiate access request, Notify facilities, Approval required?, Route to manager](/content/skillup/ab731/images/d2-microsoft-ai-services-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ab731/d2-microsoft-ai-services-m1.mmd -->

*A Copilot Studio agent triggers on a new-hire event and orchestrates IT, access, and facilities steps, inserting a human approval gate only for high-risk requests.*

### In Practice

**What breaks without this**: a process split across separate ad hoc Copilot chats has no memory between steps and no owner if a step is skipped — a manager who forgets to trigger the facilities notification leaves a new hire without a desk assignment, and nobody finds out until the new hire's first day, because nothing was tracking status across the handoff.

**Decision trigger**: ask, "does this process span more than one system, or more than one step that should happen without someone re-opening Copilot chat to ask for it?" If yes, that's a Copilot Studio automation candidate, not a better prompt template.

**When you'd choose differently**: a genuinely one-off, single-system task that needs judgment at every step — drafting one custom, sensitive termination letter, say — doesn't benefit from orchestration; ad hoc Copilot chat with a human reviewing each line is still the right tool there.

### Exam Trap ⚠️

<div class="note-trap">"Give managers a more detailed prompt template" and "have each system owner pilot their own Copilot chat" both sound like progress but leave the process exactly as manual as before — no trigger, no orchestration, no status tracking. If the scenario says a process should run "without a human prompting each step," a better prompt is never the answer; an agent that triggers and orchestrates is.</div>

---

## Deep Dive: Making Microsoft's AI Apps & Services Click

### 1. The connective narrative

The four-layer stack in §2.1 — Foundation, Platform, Extensibility, Applications — is the skeleton the rest of this domain hangs on. Nearly every topic after it is really the same question asked about a different scenario: *which layer solves this business need with the least amount of custom work?* Microsoft 365 Copilot (§2.2–§2.6) sits at the top, Applications layer, because most employees just need AI inside the tools they already use. Copilot Studio (§2.7, §2.15, §2.16) sits one layer down, Extensibility, for when the business need is specific enough that out-of-the-box Copilot can't reach it — a custom knowledge base, a multi-step workflow that has to trigger itself. Microsoft Foundry (§2.9, §2.13) sits at the bottom two layers, for when the need is custom enough that no low-code tool reaches it at all.

Governance rides along with that same stack, and it gets *more* important, not less, the higher up you go — not the reverse, which is the counterintuitive part. §2.15's SharePoint oversharing problem exists precisely because the Applications layer (Copilot) is the layer most employees touch daily, at the highest volume, with the least technical friction — so permission mistakes made years ago at the data layer become visible at conversational speed the moment Copilot goes broad. The Build/Buy/Extend framework (§2.7, §2.14) and the extensibility framework (§2.8) exist to stop teams from jumping straight to "build" (Foundry) when "extend" (Copilot Studio) already solves it — that's the domain's most consistently tested judgment call.

Model selection (§2.10, §2.13) is the same "least resource for the job" logic applied one level deeper: once you're building on Foundry, you still shouldn't reach for the largest, most expensive model by default. A small model like Phi for a cheap, low-latency FAQ bot; a large model like GPT-4o for genuinely complex reasoning over long documents. The domain rewards restraint at every layer of the decision, not just the top one.

### 2. Worked scenario

> **Scenario.** A global retailer is rolling out AI across three separate needs. First, marketing wants help drafting product descriptions and social copy — that's Word and Copilot Chat, Applications layer, no customisation needed (§2.2, §2.4). Second, HR wants new-hire onboarding to trigger automatically across IT, access provisioning, and facilities without a manager re-prompting at each step — that's a Copilot Studio agent, Extensibility layer, built exactly as described in §2.16. Third, the data science team wants a custom product-recommendation model trained on three years of purchase history — that's Microsoft Foundry, Platform/Foundation layers, because no low-code tool trains a custom model from scratch (§2.9, §2.13).
>
> Before the marketing rollout goes broad, IT runs a SharePoint Advanced Management oversharing report (§2.15) and finds two years' worth of "share with everyone" links on old campaign folders — nobody browsed them manually, so nobody noticed, but a Copilot query would surface them instantly. IT restricts discoverability and applies sensitivity labels before go-live, not after a complaint. For the recommendation model, the team starts on pay-as-you-go while validating accuracy, then considers reserved capacity once usage volume is predictable (§3.8) — mirroring the same pattern used for Copilot licensing scale-up.

### 3. Memory aid

**F-P-E-A**, bottom to top: **F**oundation → **P**latform → **E**xtensibility → **A**pplications (§2.1's own stack). For any scenario, ask which layer solves it with the least custom work — and don't drop a layer lower than the scenario actually requires.

### 4. Exam strategy for this domain

The traps in this domain are almost all look-alike-term traps: Microsoft Copilot vs Copilot Chat vs Microsoft 365 Copilot, Researcher vs Analyst, Build vs Extend, Foundry vs Foundry Tools, Azure AI Foundry vs Microsoft Foundry. The exam rewards correctly identifying the *minimum* layer or tool that satisfies the stated requirement, and punishes jumping to a custom build (Foundry) or a from-scratch agent when Copilot or an extension already covers it. One sentence for five minutes before the exam: default to the most out-of-the-box layer that satisfies the scenario, and only drop down a layer when the scenario explicitly rules out everything above it.

---

## 🎯 Domain 2 Exam Traps

| Trap | Correct answer |
|---|---|
| "Copilot" vs "M365 Copilot" | M365 Copilot has broad Microsoft Graph grounding; consumer Copilot does not, and Copilot Chat is mainly web-grounded |
| "Is Copilot Chat paid?" | No — included at no extra cost for eligible Microsoft 365 users; agents used by unlicensed users bill pay-as-you-go |
| "Build vs Extend" | Try Copilot Studio extension before building from scratch in Foundry |
| "Researcher vs Analyst" | Researcher = web/doc research; Analyst = data analysis with code |
| "Which Copilot for collaborative AI content?" | Copilot Pages — persistent, multi-user canvas (not a single-session Word draft) |
| "Automate vs Augment first?" | Start with automatable tasks (meeting summaries, email drafts) for fastest ROI |
| "Budget-sensitive edge deployment?" | Phi model family — lightweight, runs on-device or in constrained environments |
| "Open source = free?" | Only when self-hosted; open models on Foundry managed deployments are billed per token |
| "Azure AI Search" | It's the retrieval/search layer for RAG — not just a search engine |
| "Copilot sees all data" | Copilot respects existing M365 permissions — can't access what user can't access |
| "Copilot rollout + years of SharePoint sharing" | Run SharePoint Advanced Management oversharing remediation BEFORE rollout — permission inheritance alone isn't proactive governance |
| "Multi-step process, no human prompting each step" | Copilot Studio agent that triggers and orchestrates — NOT a better prompt template |
| "Azure AI Foundry vs Microsoft Foundry" | Same platform — renamed at Ignite, November 2025 |

---

## 📌 D2 Hard Question Patterns

**Pattern 1 — Copilot vs Copilot Studio**
> *"A company wants employees to have an AI assistant that answers HR policy questions. What is the QUICKEST path to value?"*
>
> ✅ Microsoft 365 Copilot grounded in the HR policy content (in SharePoint, or brought in with a Copilot connector) — extend, not build. NOT a Copilot Studio build-from-scratch — that's overkill for internal staff who already have M365 licences.

**Pattern 2 — Microsoft Graph powers Copilot**
> *"Why can Microsoft 365 Copilot access a user's emails and calendar without extra configuration?"*
>
> ✅ Microsoft Graph — the unified API layer that Copilot uses to read/write across M365 apps. Graph respects existing permissions, so Copilot inherits the user's data access.

**Pattern 3 — Foundry vs Studio scope**
> *"A developer team wants to build an AI model trained on 5 years of internal sales data. Which tool is most appropriate?"*
>
> ✅ Microsoft Foundry — for custom model development, fine-tuning, and MLOps. Copilot Studio is low-code for building agents, not for training models.

**Pattern 4 — Researcher / Analyst Copilot agents**
> *"A business analyst needs to synthesise insights from 50 reports per week. Which Copilot capability addresses this?"*
>
> ✅ Researcher agent — multi-source synthesis of documents and web content into a report. Analyst agent is for deep data analysis (Python code execution, charts) over datasets. These are the two built-in reasoning agents in M365 Copilot.
