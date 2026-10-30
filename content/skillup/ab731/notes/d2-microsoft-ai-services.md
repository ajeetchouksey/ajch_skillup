# D2: Identify Benefits, Capabilities, and Opportunities for Microsoft's AI Apps and Services

> **Exam weight**: 35–40% · **Questions**: ~32 in the bank

## Overview

This domain asks one question over and over: which Microsoft product meets this business need with the least custom work? It covers the Copilot family (Microsoft Copilot, Copilot Chat, Microsoft 365 Copilot, Researcher and Analyst), Microsoft Graph and permissions, Copilot Studio and the extensibility framework, and Microsoft Foundry with Foundry Tools, plus model choice and the build, buy or extend decision.

<div class="note-scribble"><strong>Naming note.</strong> Azure AI Foundry was renamed <strong>Microsoft Foundry</strong> at Microsoft Ignite in November 2025, and Azure AI services became <strong>Foundry Tools</strong>. The study guide uses the new names; older material and some answer options still say "Azure AI Foundry". Both mean the same platform.</div>

> 💡 **Human Angle**: Reaching for Microsoft Foundry when Copilot Studio already does the job is like hiring a construction crew to hang a picture frame: real capability, wrong tool for the job.

---

## 2.1 Map business processes and use cases to Copilot

### Key Concept

**Start Copilot on frequent, draftable tasks; leave judgement-heavy and relationship work with people.**

Mapping a process means listing its tasks, classifying each by how much AI can take on, and starting where the return is fastest. Automatable and augmentable tasks happen often and take time, so every minute saved repeats every week. Judgement-heavy and relationship work gains far less, because the expertise or the human connection is the value.

**Think of sorting laundry before washing**: separate what the machine handles from what needs hand care.

![Four steps to map a business process to Copilot: list tasks, classify them, prioritise automatable and augmentable work, then map to a Copilot feature.](/content/skillup/ab731/images/ab731-d2-process-to-copilot-mapping.svg)

### Real use

A retail operations director with 200 staff asks where Copilot pays back first. The team lists its week: meeting recaps, email replies, weekly reports and sales analysis come first; negotiating with suppliers and coaching store managers stay human.

### How it works

- **Automatable** (highest benefit): meeting summaries, email triage, extracting data from invoices.
- **Augmentable** (high): proposals, Excel analysis, research; AI drafts, people refine.
- **Judgement-heavy** (lower): complex legal interpretation, senior strategy.
- **Relationship-based** (minimal): client relationships, counselling, coaching.
- Then map each chosen task to the Copilot feature in the app where its content lives (2.4).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Automatable first | You need visible ROI fast | Less impressive than strategic use |
| Augmentable next | Knowledge work with a human finishing step | Needs training to review well |
| AI as preparation aid | Judgement-heavy work | The decision stays fully human |

### How to do it

1. List a team's recurring tasks with how often they happen and how long they take.
2. Classify each into the four types.
3. Start with frequent automatable and augmentable tasks and measure time saved.

### Exam Trap ⚠️

<div class="note-trap">Distractors put judgement-heavy or relationship tasks first because they sound high-value. For the fastest Copilot ROI, the exam picks automatable and augmentable tasks: high frequency, measurable time saved.</div>

### Go deeper

- [Microsoft 365 Copilot adoption](https://adoption.microsoft.com/en-us/copilot/)

---

## 2.2 Understand differences in capabilities between versions of Copilot

### Key Concept

**The Copilot versions differ above all in how much of your organisation's data they can reason over.**

**Microsoft Copilot** is the consumer assistant for personal accounts. **Copilot Chat** is included for eligible Microsoft 365 work and school users, with enterprise data protection, and is mainly web-grounded. **Microsoft 365 Copilot** is the paid per-user add-on that grounds answers in Microsoft Graph (your email, meetings, chats and files) and works inside Word, Excel, PowerPoint, Outlook and Teams.

**Think of three keys to one building**: the lobby, the lobby with security watching, and the offices you're cleared for.

![Three Copilot versions compared: Microsoft Copilot for personal accounts grounded on the web, Copilot Chat included for work accounts with enterprise data protection, and licensed Microsoft 365 Copilot grounded in Microsoft Graph inside the apps.](/content/skillup/ab731/images/ab731-2-2-copilot-versions.svg)

### Real use

A company tells all staff "you have Copilot". Most only have Copilot Chat, and tickets pile up from people who expected it to find their SharePoint files. Clear communication of who has which version, and why, would have prevented it.

### How it works

- **Microsoft Copilot**: web-grounded, no enterprise data protection, free; for personal tasks.
- **Copilot Chat**: web-grounded plus uploaded files and agents; enterprise data protection; included at no extra cost.
- **Microsoft 365 Copilot**: web plus Graph and the semantic index; Copilot in the apps; Researcher and Analyst. Paid add-on, list price about US$30 per user per month on annual terms (check current pricing).
- Eligible base plans are broad: Microsoft 365 E3/E5, Business Basic/Standard/Premium, Office 365 E1/E3/E5, F1/F3 and others.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Copilot Chat | Staff need secure AI chat over web content and their uploads | No broad org-data grounding |
| Microsoft 365 Copilot | Daily work needs AI over own email, meetings and files, in the apps | Per-user cost |
| Agent in Copilot Chat (pay-as-you-go) | One narrow task needs org data | Metered billing to manage |

### How to do it

1. Segment users by whether their work needs answers from their own Microsoft 365 data.
2. Give everyone Copilot Chat; license Microsoft 365 Copilot for the segment that needs Graph.
3. Tell each group exactly what their version can and can't reach.

### Exam Trap ⚠️

<div class="note-trap">"Microsoft Copilot" and "Microsoft 365 Copilot" are different products, and Copilot Chat is a third. Any answer saying the consumer Copilot or unlicensed Copilot Chat summarises your organisation's SharePoint content is wrong. Newer Microsoft docs sometimes shorten the licensed product's name, but the exam keeps "Microsoft 365 Copilot".</div>

### Go deeper

- [Microsoft 365 Copilot licensing](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-licensing)

---

## 2.3 Understand capabilities of Microsoft 365 Copilot Chat web and mobile experiences

### Key Concept

**Copilot Chat is the included, enterprise-protected chat for work accounts, on web and mobile; it's web-grounded unless the user is licensed.**

Work users reach Copilot Chat at m365copilot.com, in the Microsoft 365 Copilot app on web and mobile, in Teams and Outlook, and in the Edge side pane. (copilot.microsoft.com is the consumer Microsoft Copilot.) Everyone gets web-grounded answers with enterprise data protection, file upload, image creation and agents. Licensed users can also switch the scope to Work, grounding the same chat in Microsoft Graph.

**Think of one front desk with two levels of clearance**: everyone gets help; only cleared staff can ask about the back-office files.

![Copilot Chat's Work toggle searches Microsoft Graph org data while the Web toggle searches Bing.](/content/skillup/ab731/images/ab731-d2-copilot-chat-work-web-toggle.svg)

### Real use

A field team uses Copilot Chat on their phones to rewrite customer emails and summarise PDFs they upload, all under enterprise data protection. Their manager, who holds the licence, switches to Work to ask "what did my team decide about the Leeds store last week?".

### How it works

- **Included** for eligible Microsoft 365 work and school users, with enterprise data protection.
- **Web grounding** for everyone; **Work (Graph) grounding** for Microsoft 365 Copilot licence holders.
- **File upload**, **image creation**, and **agents**.
- Agents used by unlicensed users are billed **pay-as-you-go** through an Azure subscription.
- Admins can turn web grounding off or restrict access for regulated groups.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Copilot Chat (web scope) | Secure general assistant, drafting, uploaded files | Doesn't search org data |
| Work scope | Licensed user needs answers from own work data | Needs the licence |
| Web grounding off | Regulated group can't use web results | Less general knowledge |

### How to do it

1. Pin Copilot Chat for all eligible users and explain what it reaches.
2. Teach licensed users the Work/Web scope switch.
3. Set a pay-as-you-go billing policy if unlicensed users will use agents.

### Exam Trap ⚠️

<div class="note-trap">"Copilot Chat requires a Microsoft 365 Copilot licence" is wrong: it's included. "Copilot Chat searches all your work files for free" is also wrong: broad Graph grounding comes with the licence. And copilot.microsoft.com is the consumer product, not the work experience.</div>

### Go deeper

- [Microsoft 365 Copilot Chat overview](https://learn.microsoft.com/en-us/copilot/overview)

---

## 2.4 Understand capabilities of the Copilot experience in various Microsoft 365 apps

### Key Concept

**Each app's Copilot does what that app's content allows; start Copilot where the content already lives.**

It's one assistant working over different material. Excel holds structured tables, so Copilot analyses data, writes formulas and builds charts. Teams holds meeting transcripts, so it recaps decisions and action items. Outlook holds threads, so it summarises and drafts replies. Copilot Pages turns a chat answer into a shared, editable page a team keeps building on.

**Think of one interpreter visiting different rooms**: the same skills each time, but what it can tell you depends on what's in the room.

![Microsoft 365 apps matched to their Copilot strengths: Word drafts and rewrites, Excel analyses and charts, PowerPoint builds decks from documents, Outlook summarises threads and drafts replies, Teams recaps meetings, and Pages keeps a shared AI canvas.](/content/skillup/ab731/images/ab731-2-4-copilot-apps.svg)

### Real use

An executive missed a 90-minute board meeting in Teams. Instead of reading the transcript or exporting it to Word, she opens the Copilot recap in Teams and gets the decisions and her own action items in a minute.

### How it works

- **Word**: draft, rewrite, summarise, generate from an outline or other files.
- **Excel**: analyse data, formulas, charts, trends.
- **PowerPoint**: build a deck from a prompt or a Word document; add slides.
- **Outlook**: summarise threads, draft replies, coach on tone.
- **Teams**: meeting recap, action items, chat summaries.
- **Copilot Pages**: a persistent, multi-user canvas populated from Copilot chat.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Copilot in the source app | The task's content lives in one app | Limited to that app's content |
| Copilot Chat (Work) | The task spans emails, files and meetings | Less in-app formatting help |
| Copilot Pages | Several people build on AI output over days | Not a formal document workflow |

### How to do it

1. Ask where the task's content lives.
2. Open Copilot in that app; use Chat when it spans several sources.
3. Move to Pages when a team will keep adding to the result.

### Exam Trap ⚠️

<div class="note-trap">Distractors offer a workaround in the wrong app, like exporting a Teams transcript to Word to summarise it. Use the app that natively holds the content. For a shared, AI-populated working document, the answer is Copilot Pages, not separate Word drafts or individual chats.</div>

### Go deeper

- [Microsoft 365 Copilot overview](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-overview)

---

## 2.5 Understand capabilities of Microsoft Copilot Studio

### Key Concept

**Copilot Studio is the low-code builder for custom agents: knowledge, actions and channels, and it can trigger and run a whole workflow.**

It fills the gap between out-of-the-box Copilot and a fully coded build. An agent gets knowledge sources (SharePoint, websites, documents), actions through connectors and Power Automate, and channels to live in (Teams, Microsoft 365 Copilot, websites). It can start on an event and orchestrate several steps, pausing only where a human must decide. IT pros, power users and business analysts build agents without code.

**Think of a kit-car workshop**: you assemble something tailored from proven parts, without machining the engine.

![Copilot Studio connects to a knowledge base, Power Automate actions and connectors to other systems.](/content/skillup/ab731/images/ab731-d2-copilot-studio-building-blocks.svg)

### Real use

Onboarding used to mean each hiring manager prompting Copilot for a welcome email, an IT ticket and an access request. A Copilot Studio agent now triggers when a new hire appears in the HR system, creates the ticket and request, notifies facilities, and asks the manager only to approve high-risk access.

### How it works

- **Knowledge**: answer from your documents and sites.
- **Actions**: call systems through connectors and Power Automate flows.
- **Triggers and orchestration**: start on an event and sequence steps, with human approval where needed.
- **Channels**: Teams, Microsoft 365 Copilot, websites, mobile; external users and human handoff.
- **Billing**: Copilot Credits (formerly "messages"), prepaid or pay-as-you-go; usage by Microsoft 365 Copilot-licensed users in Copilot Chat, Teams or SharePoint is zero-rated for many scenarios.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Copilot Studio agent | Knowledge + a few actions + a channel, or a triggered workflow | Credits to budget, agent to govern |
| Copilot or a built-in agent | Existing Graph data already answers it | No custom logic |
| Microsoft Foundry | Custom model or bespoke orchestration code | Developer build and operations |

### How to do it

1. Describe the need as knowledge, actions, triggers and channel.
2. Build the agent in Copilot Studio and connect its knowledge and actions.
3. Add approval steps for high-risk actions and publish to the channel.

### Exam Trap ⚠️

<div class="note-trap">"Copilot Studio is for developers training models" is wrong; it's low-code and doesn't train models. A customer-facing helpdesk with knowledge, an order API and human handoff doesn't need Foundry. And "give managers a better prompt template" never automates a multi-step process: an agent that triggers and orchestrates does.</div>

### Go deeper

- [What is Copilot Studio?](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio)

---

## 2.6 Understand capabilities of Microsoft Graph

### Key Concept

**Microsoft Graph is how Microsoft 365 Copilot knows your organisation, and why it can't see past each user's permissions.**

Graph is the API layer over Microsoft 365 data: mail, calendar, Teams chats and meetings, SharePoint and OneDrive files. When a user asks Copilot something, it retrieves relevant content through Graph under that user's identity and grounds its answer in it. Because retrieval runs as the user, Copilot can only surface content the user could already open. Copilot connectors bring outside content into Graph too.

**Think of a librarian who fetches books on your library card**: fast and thorough, but only from shelves your card unlocks.

![Microsoft 365 Copilot reaches Outlook, Teams, SharePoint, OneDrive and the Microsoft 365 apps through the Microsoft Graph API.](/content/skillup/ab731/images/ab731-d2-graph-data-connector.svg)

### Real use

Before rolling Copilot out to 5,000 staff, an enterprise runs a SharePoint Advanced Management oversharing report. It finds "everyone in the org" links on old compensation files. IT restricts their discoverability and labels them, so Copilot can't surface what years of loose sharing exposed.

### How it works

- **Permission trimming**: Copilot only surfaces data the user has at least view access to.
- **No cross-tenant sharing** of your data.
- **Copilot connectors** bring third-party content (Confluence, ServiceNow) into Graph.
- **Oversharing still matters**: Copilot makes existing over-permissioned content easy to find.
- **SharePoint Advanced Management**: oversharing reports, restricted content discoverability, site access reviews; plus sensitivity labels.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Rely on permission inheritance | Small pilot on tightly scoped sites | Hidden oversharing remains |
| Remediate oversharing first | Broad or tenant-wide rollout | Work before go-live |
| Copilot connector | Needed data lives outside Microsoft 365 | Build and maintain the connector |

### How to do it

1. Run an oversharing report before a broad rollout.
2. Fix permissions, restrict discoverability and label sensitive content.
3. Add Copilot connectors for knowledge outside Microsoft 365.

### Exam Trap ⚠️

<div class="note-trap">"Copilot can see all company data" and "you must build custom role filters for Copilot" are both wrong: it sees exactly what each user's permissions allow. But "permission inheritance is enough" is wrong before a broad rollout, and "disable Graph" overcorrects. The right move is targeted oversharing remediation.</div>

### Go deeper

- [Data, privacy and security for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)
- [SharePoint Advanced Management](https://learn.microsoft.com/en-us/sharepoint/advanced-management)

---

## 2.7 Identify benefits and capabilities of an integrated Microsoft AI solution, including risk mitigation and safety benefits

### Key Concept

**Staying in one Microsoft stack means AI inherits the identity, permissions, compliance and safety controls you already run.**

Stitching together unrelated AI tools means re-solving sign-in, permissions, data protection, audit and safety for each one. Inside Microsoft's stack, Copilot, agents and Foundry builds reuse Microsoft Entra ID sign-in and existing Microsoft 365 permissions, enterprise data protection covers prompts and responses, Microsoft Purview applies labels, retention, DLP and audit to AI interactions, and Foundry adds content safety and evaluations to custom builds.

**Think of adding a room to a house that's already wired and alarmed**: the new room is covered on day one.

![An integrated Microsoft AI solution stacks four shared protections: one identity and permission model, enterprise data protection, Microsoft Purview compliance on AI interactions, and built-in safety and evaluations in Microsoft Foundry.](/content/skillup/ab731/images/ab731-2-7-integrated-benefits.svg)

### Real use

A bank compares a third-party chatbot with Microsoft 365 Copilot. The third-party tool would need its own access model, data processing agreement, logging and DLP. With Copilot, existing sensitivity labels, retention policies and audit already apply to Copilot interactions, so the risk review takes weeks, not months.

### How it works

- **One identity and permission model**: Entra ID and existing permissions apply to Copilot, agents and Graph grounding.
- **Enterprise data protection**: work prompts and responses are protected, and customer content isn't used to train foundation models.
- **Compliance tooling in place**: Purview sensitivity labels, retention, DLP and audit cover AI interactions.
- **Built-in safety**: Foundry content filters, Prompt Shields, evaluations and monitoring.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Integrated Microsoft stack | Data is in Microsoft 365 and controls exist | Less freedom to mix vendors |
| Third-party tool | It meets a need Microsoft's stack can't | Re-create identity, compliance and audit |
| Foundry custom build | Custom app, still needs Azure controls | Developer effort |

### How to do it

1. List the controls you already run: sign-in, labels, retention, DLP, audit.
2. Check which apply automatically to the AI option you're considering.
3. Count every control you'd have to rebuild for a non-integrated tool.

### Exam Trap ⚠️

<div class="note-trap">The benefit is reused controls, not "Microsoft AI never makes mistakes". An option claiming integration removes the need for human review or governance is wrong; integration reduces risk, it doesn't remove it.</div>

### Go deeper

- [Enterprise data protection in Microsoft 365 Copilot](https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection)
- [Microsoft Purview data security and compliance for generative AI](https://learn.microsoft.com/en-us/purview/ai-microsoft-purview)

---

## 2.8 Map business processes and use cases to Microsoft's AI apps and services

### Key Concept

**Map each need to the highest layer of Microsoft's stack that meets it; every layer down adds build time.**

Microsoft's AI comes in four layers. **Applications**: Microsoft 365 Copilot, Copilot Chat. **Extensibility**: Copilot Studio, agents and connectors. **Platform**: Microsoft Foundry and Foundry Tools such as Azure AI Search and Azure Vision. **Foundation**: models in the Foundry Models catalog. Business users mostly work at the top; developers build at the bottom.

**Think of buying a house versus building one**: the further down you start, the more you control and the more you build yourself.

![Business users reach Microsoft 365 Copilot, Microsoft Copilot and Copilot Studio, with Microsoft Graph as the org data connector, while developers and IT build on Microsoft Foundry (formerly Azure AI Foundry) with Azure AI Search and Azure Vision.](/content/skillup/ab731/images/ab731-d2-ai-products-by-audience.svg)

### Real use

A logistics firm wants 500 warehouse staff to ask questions of a shipment database that lives entirely outside Microsoft 365, and most staff have no Copilot licence. A standalone agent built on Microsoft Foundry and billed on consumption costs far less than licensing everyone.

### How it works

- **Who are the users?** Employees in Microsoft 365, or external customers?
- **Where is the data?** In Microsoft 365 (Graph), or in another system?
- **What must it do?** Draft and summarise, run a workflow, or power a custom product?
- Employees + Microsoft 365 data → Copilot; a workflow or knowledge agent → Copilot Studio; external users, custom models or data outside Microsoft 365 at scale → Foundry.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Microsoft 365 Copilot | Employees, Microsoft 365 data, everyday work | Per-user licence |
| Copilot Studio | Knowledge, actions, workflows, internal or external | Credits and agent governance |
| Microsoft Foundry | Custom app, model or data outside Microsoft 365 | Build, host and operate it |

### How to do it

1. Write down users, data location and the job to be done.
2. Start at the Applications layer; drop a layer only when the scenario rules it out.
3. Compare licence and consumption cost for the actual user count.

### Exam Trap ⚠️

<div class="note-trap">The most powerful-sounding product is the usual distractor. If the scenario says "business users in Word and Teams", a Foundry build is wrong even though it would work. The reverse also appears: per-user Copilot licences for hundreds of occasional users of a non-Microsoft 365 system.</div>

### Go deeper

- [Leverage AI tools and resources for your business](https://learn.microsoft.com/en-us/training/modules/leverage-ai-tools/)

---

## 2.9 Identify when to use Researcher or Analyst in Copilot

### Key Concept

**Researcher synthesises sources into a cited report; Analyst works through data with code. Choose by input: documents or a dataset.**

Both are built-in reasoning agents in Microsoft 365 Copilot that take longer and plan several steps. **Researcher** gathers from the web and your work content (files, email, meetings, chats you can access) and writes a structured, source-cited report. **Analyst** cleans, analyses and charts raw data by writing and running Python. Neither runs a company-specific workflow; that needs a custom agent.

**Think of a journalist and a statistician**: one tells you what the sources say, the other what the numbers say.

![Choosing a reasoning agent: documents and web sources go to Researcher for a cited report, a dataset goes to Analyst for code-driven analysis and charts, and a company-specific process goes to a custom Copilot Studio agent.](/content/skillup/ab731/images/ab731-2-9-researcher-analyst.svg)

### Real use

A product team needs a competitive landscape combining news, analyst papers and its own strategy decks: Researcher. A business analyst has 50,000 rows of sales and wants the top five categories by growth with a trend chart: Analyst.

### How it works

- **Researcher**: multi-source research, competitive analysis, briefings; cites sources; may ask clarifying questions.
- **Analyst**: spreadsheets and CSVs; runs Python; surfaces trends and builds charts.
- Both are included with the Microsoft 365 Copilot licence and found in Copilot Chat.
- For a quick formula or small chart, Copilot in Excel is faster.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Researcher | Input is documents and web sources; output is a report | Slower than standard chat |
| Analyst | Input is a dataset; output is calculated insight | Needs reasonably clean data |
| Custom agent | Company-specific rules or systems | Build and govern it |

### How to do it

1. Ask: is the main input documents or rows and columns?
2. Pick Researcher or Analyst accordingly; set Researcher's scope to work, web or both.
3. Use a custom Copilot Studio agent only for company-specific logic.

### Exam Trap ⚠️

<div class="note-trap">Distractors swap the two, or claim a built-in agent can run a proprietary business process. Researcher is for research and reports; Analyst is for data analysis with code. Neither replaces a custom agent for company-specific logic.</div>

### Go deeper

- [Get started with Researcher](https://learn.microsoft.com/en-us/microsoft-365/copilot/researcher-agent)
- [Explore prebuilt Microsoft 365 Copilot agents](https://learn.microsoft.com/en-us/training/modules/explore-prebuilt-microsoft-365-copilot-agents/)

---

## 2.10 Identify when to build, buy, or extend, including the Microsoft 365 Copilot extensibility framework

### Key Concept

**Buy what exists, extend what almost fits, and build only when nothing in Microsoft 365 can serve the need.**

**Buy** is Microsoft 365 Copilot as it is. **Extend** adds your knowledge, actions or a focused role to Copilot through the extensibility framework: Copilot connectors (new knowledge), actions via APIs or MCP servers (new skills) and declarative agents (a scoped role on Copilot's own model). **Build** is a custom engine agent or a Microsoft Foundry app with its own model and orchestration. Each step down adds cost, time and maintenance.

**Think of furnishing an office**: buy the standard desk, add a shelf, commission joinery only when nothing fits.

![Buy, extend or build: buy uses Microsoft 365 Copilot as is, extend adds connectors, actions and declarative agents, and build creates a custom engine agent or Foundry app.](/content/skillup/ab731/images/ab731-2-10-buy-extend-build.svg)

### Real use

A financial services firm wants Copilot to answer from a compliance knowledge base in a legacy system. It extends: a declarative agent in Copilot Studio with a connector to that system. Weekly project status reports from Teams chats and SharePoint need nothing new at all: Microsoft 365 Copilot already reasons over that content.

### How it works

- **Copilot connectors** (formerly Graph connectors): bring external content into Graph.
- **Actions** (API plugins or MCP servers): let an agent read or update another system.
- **Declarative agents**: instructions, knowledge and actions around Copilot's model.
- **Custom engine agents**: your own model and orchestration.
- "Plugin" now means an installable package bundling agents, connectors and MCP integrations.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Buy | Copilot already covers the need | No customisation |
| Extend | Copilot lacks your data, an action or a focused role | Build and govern extensions |
| Build | External users, a custom model, or a product feature | Highest cost and maintenance |

### How to do it

1. Check whether Microsoft 365 Copilot already answers from existing data.
2. If not, name the gap: knowledge, action or focus, and extend.
3. Build only when users, model or experience fall outside what extending can do.

### Exam Trap ⚠️

<div class="note-trap">Distractors jump straight to Build because it sounds most capable, or propose fine-tuning to make Copilot aware of an internal system. Making external data available to Copilot is an extensibility problem: a connector or a declarative agent.</div>

### Go deeper

- [Microsoft 365 Copilot extensibility](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/)

---

## 2.11 Map business processes and use cases to Foundry Tools

### Key Concept

**Break a custom AI process into steps, then match each step to a prebuilt Foundry Tool before building anything yourself.**

Foundry Tools (formerly Azure AI services) are prebuilt capabilities: Azure Vision for images, Document Intelligence and Content Understanding for documents and forms, Speech, Translator and Language for text and audio, and Azure AI Search for retrieval. Most custom AI processes are a chain of these steps, composed in Microsoft Foundry with a model where language generation is needed.

**Think of a professional kitchen's appliances**: you don't build an oven to bake one cake.

![A process broken into steps, each mapped to a Foundry Tool: read a photo with Azure Vision, extract form fields with Document Intelligence, find relevant records with Azure AI Search, transcribe calls with Speech, and generate the answer with a Foundry model.](/content/skillup/ab731/images/ab731-2-11-foundry-tools-map.svg)

### Real use

An e-commerce company wants customers to upload a photo of a product and get compatible accessories. Azure Vision identifies the product in the image; Azure AI Search retrieves matching accessories from the catalogue. No custom vision model is trained.

### How it works

- **Image understanding, OCR**: Azure Vision.
- **Forms, invoices, contracts**: Document Intelligence, Content Understanding.
- **Speech to text, text to speech**: Speech.
- **Translation, sentiment, key phrases, entities**: Translator, Language.
- **Find the relevant content**: Azure AI Search (the retrieval layer for RAG).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Prebuilt Foundry Tool | A standard capability covers the step | Less control over the model |
| Compose tools in Foundry | The process chains several capabilities | Developer integration work |
| Custom model | Nothing prebuilt meets accuracy needs | Data, training and upkeep |

### How to do it

1. Write the process as a chain of steps with inputs and outputs.
2. Match each step to a Foundry Tool.
3. Build custom only for steps no tool covers well enough.

### Exam Trap ⚠️

<div class="note-trap">Distractors propose training a custom model for a step a Foundry Tool already does (reading text from images, finding similar documents). And if the users are employees with data in Microsoft 365, Copilot or Copilot Studio may get there faster than any Foundry build.</div>

### Go deeper

- [What are Foundry Tools?](https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services)

---

## 2.12 Identify capabilities of Foundry Tools, including Azure Vision in Foundry Tools, Azure AI Search, and Microsoft Foundry

### Key Concept

**Microsoft Foundry is the platform for building custom AI apps and agents; Azure Vision and Azure AI Search are two of the tools it plugs in.**

**Microsoft Foundry** covers the build lifecycle: choose a model from the catalog, develop prompts and agents, evaluate, deploy and monitor. **Azure Vision in Foundry Tools** analyses images: captions, tags, objects, and OCR to read text. **Azure AI Search** indexes content for keyword, vector and semantic search, and is the usual retrieval layer for RAG. Face analysis is a separate, limited-access tool.

**Think of the kitchen and two of its appliances**: the kitchen gives space, safety and workflow; the appliances do specialised jobs.

![Three capabilities: Microsoft Foundry as the platform for models, agents, evaluation, deployment and monitoring; Azure Vision for image analysis and OCR; and Azure AI Search for keyword, vector and semantic retrieval.](/content/skillup/ab731/images/ab731-2-12-foundry-tools.svg)

### Real use

A support team must search 10 million past tickets for those most relevant to a new customer question, even when the words differ. Azure AI Search with vector and semantic ranking finds them; a Foundry model drafts the answer from the top results.

### How it works

- **Microsoft Foundry**: model catalog, agent service, prompt development, evaluations, content safety, deployment, monitoring.
- **Azure Vision**: image analysis, object detection, OCR on photos and scans.
- **Azure AI Search**: indexes documents; keyword, vector and hybrid search; semantic ranking.
- **Other Foundry Tools**: Speech, Language, Translator, Document Intelligence, Content Understanding.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Azure AI Search | Find relevant content in large collections | Index design and upkeep |
| Azure Vision | Understand or read images | Prebuilt categories |
| Microsoft Foundry | Build, evaluate and run a custom AI app or agent | Developer skills needed |

### How to do it

1. Identify whether the need is retrieval, image understanding or a whole custom app.
2. Use Azure AI Search for retrieval, Azure Vision for images.
3. Assemble and evaluate them in a Foundry project.

### Exam Trap ⚠️

<div class="note-trap">Look-alike names: "Foundry" (the platform) and "Foundry Tools" (the prebuilt services); "Azure AI Foundry" and "Microsoft Foundry" (same platform). Don't eliminate an answer for using the old name. And Azure AI Search is a retrieval layer for RAG, not just a website search box.</div>

### Go deeper

- [What is Azure AI Search?](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [What is Azure Vision?](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview)

---

## 2.13 Match an AI model to a business need

### Key Concept

**Model choice trades latency, cost and accuracy, and where the model must run; the biggest model is rarely the best fit.**

Larger models reason better over long or ambiguous input but cost more and respond slower. Small models such as Phi are fast and cheap for simple, high-volume tasks and can run on-premises or at the edge. Open models such as Llama and Mistral can be self-hosted, which removes per-token fees but makes hosting yours. Total cost includes the cost of wrong answers.

**Think of choosing a vehicle**: you don't take a lorry to post a letter, or move house on a scooter.

![Decision tree for choosing a Foundry model: proprietary for complex reasoning, Phi-3 for budget or edge, open source for cost control.](/content/skillup/ab731/images/ab731-d2-foundry-model-choice.svg)

### Real use

An e-commerce FAQ bot must answer in under a second on a tight budget: a small model. A compliance team reviewing multi-document loan agreements, where one missed conflict costs far more than the tokens: a large frontier model. A contractor in an air-gapped facility: an open model on its own hardware.

### How it works

- **Real-time, simple, high volume**: small model (Phi).
- **Complex reasoning, long documents, high stakes**: large model with a large context window.
- **No cloud allowed**: small or open model self-hosted.
- **Images plus text**: a multimodal model.
- Open models deployed as serverless deployments in Foundry are billed per token; only self-hosting removes token fees.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Small model | Speed and cost matter, task is simple | Weaker on complex reasoning |
| Large model | A wrong answer is expensive | Higher cost and latency |
| Self-hosted open model | Data can't leave your facility | You run the infrastructure |

### How to do it

1. Ask where the model must run.
2. Ask what a wrong or slow answer costs.
3. Route by difficulty when volume and stakes are both high: small for routine, large for hard cases.

### Exam Trap ⚠️

<div class="note-trap">"Always use the most capable model" and "always use the cheapest model" are mirror-image distractors. Optimise total cost, including wrong answers. "Open source is free" is only true of per-token fees, and only when you host it yourself.</div>

### Go deeper

- [Foundry Models overview](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/foundry-models-overview)

---

## 2.14 Identify the benefits of Microsoft Foundry and Foundry Tools, including scalability and security

### Key Concept

**Foundry lets a custom AI app grow from prototype to millions of users with enterprise security, model choice and safety built in.**

Building AI from scratch means solving hosting, scale, security and safety yourself. Microsoft Foundry and Foundry Tools run on Azure, so they scale with demand. Access goes through Microsoft Entra ID, private networking can keep traffic off the public internet, and content filters and evaluations come built in. You aren't locked to one model vendor.

**Think of renting a fitted professional kitchen**: you cook; the building, fire safety and power supply come with it.

![Four benefits of Microsoft Foundry and Foundry Tools: scalability on Azure from prototype to production, security with Entra ID and private networking, choice of models from many providers, and governance with content safety and evaluations.](/content/skillup/ab731/images/ab731-2-14-foundry-benefits.svg)

### Real use

A retailer launches an AI shopping assistant for a seasonal sale. Traffic jumps tenfold for two weeks; the Foundry deployment scales with it, content filters block abusive prompts, and the security team reviews one familiar Azure access model instead of a new vendor's.

### How it works

- **Scalability**: Azure infrastructure from pilot to global production; pay-as-you-go or reserved capacity.
- **Security**: Entra ID access control, role-based access, private networking, data encryption.
- **Choice**: OpenAI, Microsoft (Phi), open models (Llama, Mistral) and more in one catalog.
- **Governance and safety**: content filters, Prompt Shields, evaluations, monitoring.
- **Prebuilt tools**: no need to build vision, speech or search yourself.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Microsoft Foundry | Custom app at scale with enterprise controls | Developer build |
| Copilot or Copilot Studio | Employees with Microsoft 365 data | Less custom |
| Self-built stack | Rare, highly specialised requirements | You own scale, security, safety |

### How to do it

1. Confirm the need is custom enough to justify a build (2.10).
2. Build in a Foundry project with Entra ID access and content filters on.
3. Start on pay-as-you-go; reserve capacity once volume is predictable (3.10).

### Exam Trap ⚠️

<div class="note-trap">Distractors claim Foundry locks you to one model provider, or that security must be added by a third party. Foundry offers many model providers, and Entra ID, private networking and content safety are part of the platform.</div>

### Go deeper

- [What is Microsoft Foundry?](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)

---

## Deep Dive: Making Microsoft's AI Apps & Services Click

### 1. The connective narrative

The four-layer stack in 2.8 (Foundation, Platform, Extensibility, Applications) is the skeleton for this domain. Nearly every lesson asks which layer meets a need with the least custom work. The Copilot versions, Copilot Chat, the app experiences, Graph and Researcher and Analyst (2.2–2.4, 2.6, 2.9) sit at the Applications layer, because most employees need AI inside tools they already use. Copilot Studio and the extensibility framework (2.5, 2.10) sit one layer down, for needs Copilot can't reach. Microsoft Foundry and Foundry Tools (2.11–2.14) sit at the bottom, for needs no low-code tool reaches.

Governance rides along, and it matters most at the top. Graph's oversharing problem (2.6) exists because Copilot is the layer most people use daily, at conversational speed, so old permission mistakes become visible on day one. The integrated stack (2.7) is the reason staying inside Microsoft's layers lowers risk. Model choice (2.13) applies the same restraint one level deeper: don't reach for the biggest model by default.

### 2. Worked scenario

> **Scenario.** A global retailer has three needs. Marketing wants help drafting product descriptions: that's Microsoft 365 Copilot in Word and Copilot Chat, no customisation (2.2, 2.4). HR wants onboarding to trigger across IT, access and facilities without a manager prompting each step: a Copilot Studio agent (2.5). Data science wants a recommendation model trained on three years of purchases: Microsoft Foundry, because no low-code tool trains a custom model (2.12–2.14).
>
> Before the marketing rollout goes broad, IT runs an oversharing report and finds two years of "share with everyone" links on old campaign folders. It restricts discoverability and labels them before go-live (2.6). The recommendation model runs on a small model for real-time suggestions and starts on pay-as-you-go while volume is unknown (2.13, 3.10).

### 3. Memory aid

**F-P-E-A**, bottom to top: **F**oundation → **P**latform → **E**xtensibility → **A**pplications. For any scenario, start at A and drop a layer only when the scenario rules out everything above it.

### 4. Exam strategy for this domain

The traps are look-alike terms: Microsoft Copilot vs Copilot Chat vs Microsoft 365 Copilot, Researcher vs Analyst, Build vs Extend, Foundry vs Foundry Tools, Azure AI Foundry vs Microsoft Foundry. The exam rewards the minimum layer or tool that meets the requirement and punishes jumping to a custom build when Copilot or an extension already covers it.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Fastest Copilot ROI | Automatable and augmentable tasks first |
| Free/consumer Copilot summarising company SharePoint | Wrong: only Microsoft 365 Copilot grounds in Graph |
| Is Copilot Chat paid? | No: included; agents for unlicensed users bill pay-as-you-go |
| Missed Teams meeting | Copilot recap in Teams |
| Shared AI-populated working document | Copilot Pages |
| Knowledge + actions + channel, low-code | Copilot Studio |
| Process runs with no human prompting each step | Copilot Studio agent that triggers and orchestrates |
| Copilot sees all data? | No: only what each user can already open |
| Broad rollout over messy SharePoint | Oversharing remediation with SharePoint Advanced Management first |
| Why integrated Microsoft AI? | Reuses identity, permissions, Purview and safety controls |
| Research report from documents and web | Researcher |
| Analyse a dataset, build charts | Analyst |
| Copilot needs data from another system | Copilot connector or declarative agent (extend) |
| External users, custom model | Build on Microsoft Foundry |
| Read text in images | Azure Vision |
| Find relevant documents, RAG retrieval | Azure AI Search |
| Simple, real-time, cheap | Small model (Phi) |
| Air-gapped, no per-token fee | Self-hosted open model |
| Azure AI Foundry vs Microsoft Foundry | Same platform, renamed November 2025 |
