# D3: Identify an Implementation and Adoption Strategy for Microsoft's AI Apps and Services

> **Exam weight**: 20–25% · **Questions**: ~24 in the bank

## Overview

This domain is the leadership playbook for rolling out Microsoft AI responsibly. The study guide splits it in two: aligning an AI strategy with Microsoft's responsible AI policies (principles, governance, an AI council, meeting the standards), and planning adoption across the organisation (an adoption team, barriers, champions, impacts, and the Copilot and Foundry Tools pricing models).

<div class="note-important"><strong>Naming note:</strong> Microsoft's newest documentation has started shortening <strong>Microsoft 365 Copilot</strong> to <strong>Microsoft Copilot</strong>. The AB-731 study guide (skills measured as of July 22, 2026) still uses "Microsoft 365 Copilot", so these notes do too.</div>

> 💡 **Human Angle**: "Culture eats strategy for breakfast." The best-written AI policy still fails the moment employees don't trust it enough to follow it.

---

## 3.1 Explain the importance of responsible AI

### Key Concept

**Responsible AI matters because AI decisions reach people at scale, and harm, lost trust and legal exposure scale with them.**

An AI system makes the same kind of decision thousands of times. If it's unfair, unreliable or opaque, every one of those decisions carries the flaw, and the people affected often can't see why. Microsoft's six principles (Fairness, Reliability and safety, Privacy and security, Inclusiveness, Transparency, Accountability) give leaders a shared standard to check every use case against before it ships.

**Think of the six principles as the six sides of a die**: whichever way a use case lands, one face shows, and the others are still there.

![Responsible AI at the centre of six principles: fairness, reliability and safety, privacy and security, inclusiveness, transparency and accountability, each with a one-line meaning](/content/skillup/ab731/images/ab731-d3-responsible-ai-principles.svg)

### Real use

A marketing lead wants AI to send personalised emails to 50,000 customers with no human review, saving 20 hours a week. Before approving, the leader asks who answers for an off-brand or wrong message sent 50,000 times. The plan gains a review step for new templates and a sampling check.

### How it works

- **People are affected**: hiring, lending, health and service decisions change lives.
- **Scale multiplies flaws**: one bias repeated across every decision.
- **Trust drives adoption**: employees and customers stop using AI they don't trust.
- **Regulation and reputation**: failures become legal and public issues.
- Most real failures break several principles at once: a biased model (Fairness) nobody disclosed (Transparency) that nobody reviewed (Accountability).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full impact assessment | Use case affects rights, money, jobs or safety | Time before launch |
| Lightweight acceptable-use check | Low-risk internal productivity | Revisit if scope grows |
| Don't deploy | Harm can't be mitigated | Lost opportunity |

### How to do it

1. Adopt the six principles as the organisation's AI standard.
2. Ask of each use case: who is affected, and how could they be harmed or excluded?
3. Scale the review to the answer.

### Exam Trap ⚠️

<div class="note-trap">"Responsible AI slows innovation, so apply it after launch" is the distractor. The exam treats responsible AI as a precondition for trust and scale. And removing human review to save time raises Accountability and Reliability concerns, however large the saving.</div>

### Go deeper

- [Embrace responsible AI principles and practices](https://learn.microsoft.com/en-us/training/modules/embrace-responsible-ai-principles-practices/)

---

## 3.2 Establish governance principles for AI use

### Key Concept

**Principles become governance only when they're written as policies with owners, controls and an audit trail, before rollout.**

"We are committed to fairness" changes nothing until it's a rule someone owns: "every AI system used in hiring passes a bias review before deployment". Policy introduced with a tool becomes the habit; policy added later fights the habit. The core set is an acceptable use policy, a data handling policy, an output review policy, an incident response plan and an audit trail.

**Think of principles as a constitution and policies as the laws**: nobody can be held to a constitution until laws turn it into rules.

![Governance turns a principle into practice in four steps: a principle such as fairness becomes a written policy, the policy gets a named owner and control, and the control leaves an audit trail.](/content/skillup/ab731/images/ab731-3-2-principles-to-policy.svg)

### Real use

A CTO reads the company's AI document: "We are committed to fairness, transparency and accountability." Nothing has changed in practice. The next step translates each principle into permitted and prohibited uses, named owners, review steps and logging.

### How it works

- **Acceptable use policy**: what AI may and may not be used for.
- **Data handling policy**: what data may go into AI systems.
- **Output review policy**: which outputs need human review before use; for example, all AI content in external communications is reviewed by a person (upholding Accountability and Reliability).
- **Incident response plan**: what to do when AI produces harmful output.
- **Audit trail**: logging AI use for compliance.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full policy set before rollout | Broad rollout, sensitive data | Takes weeks to agree |
| Interim pilot charter | Small, time-boxed pilot with named users | Findings must feed the final policy |
| Principles only | Never enough on its own | No enforcement |

### How to do it

1. Write the acceptable use and data handling policies first.
2. Give each policy an owner and a control.
3. Turn on logging so the controls can be audited.

### Exam Trap ⚠️

<div class="note-trap">"Wait for issues and respond", "let IT decide case by case" and "email the principles document to all staff" are all wrong. Sharing principles isn't governance; turning them into policies, owners and audit is.</div>

### Go deeper

- [Govern AI (Cloud Adoption Framework)](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/govern)

---

## 3.3 Establish an AI council to guide strategy, oversight, and cross-functional alignment

### Key Concept

**An AI council is a cross-functional decision body: it decides what AI the organisation does and whether it should.**

The council sets AI strategy, approves higher-risk use cases, monitors AI in use and keeps it aligned with business goals and responsible AI. Its strength is who sits on it: business leadership (strategy and funding), IT (architecture and security), Legal (regulation and risk), HR (people and culture) and business functions (real use cases and value). Not everything goes to it: risk decides what escalates.

**Think of a cockpit crew rather than a solo pilot**: each seat watches a different instrument.

![The AI Council draws on five functions: business leadership, IT and technology, legal and compliance, HR and people, and business functions, each with its own remit](/content/skillup/ab731/images/ab731-d3-ai-council.svg)

### Real use

A talent team wants a Copilot Studio agent that scores résumés and auto-rejects candidates below a threshold. That affects people's employment, so it goes to the council. A facilities team's agent that recaps its own stand-up notes into its own Teams channel is approved at business-unit level under the acceptable use policy.

### How it works

- **Strategy**: which two or three AI bets matter most.
- **Oversight**: approve higher-risk use cases; review AI in use, for example quarterly.
- **Alignment**: one forum where IT, Legal, HR and the business agree.
- **Escalate** when a use case decides about people, uses sensitive or regulated data, crosses functions, or faces customers.
- **Data classification** must be complete before the council approves.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full council review | High-risk, people-affecting or cross-functional use | Slower approval |
| Business-unit approval under policy | Narrow, low-risk, single-team use | Needs clear escalation criteria |
| Leadership team as council | Small organisation | Must still include Legal and HR |

### How to do it

1. Seat business, IT, Legal, HR and business-function leaders.
2. Publish the criteria for what must come to the council.
3. Review approved AI on a regular cadence.

### Exam Trap ⚠️

<div class="note-trap">A council of only technical people is wrong, and so is IT approving a high-risk use case alone because "the connectors are configured correctly". The opposite trap is a council that must approve every use case, which creates a bottleneck.</div>

### Go deeper

- [Scale AI in your organization](https://learn.microsoft.com/en-us/training/modules/scale-ai/)

---

## 3.4 Ensure that AI solutions meet responsible AI standards, including fairness, reliability, safety, privacy, security, inclusiveness, transparency, and accountability

### Key Concept

**Every AI solution passes the same responsible AI gates, and high-risk ones add human review and compliance sign-off first.**

The study guide's eight words are Microsoft's six principles: Reliability and safety, and Privacy and security, are each one principle. Meeting them is a process, not a promise. Identify the use case, decide if it's high risk, then apply the governance policy, document AI use for employees, set up a feedback and incident channel, and review it at the AI council.

**Think of airport security with a secondary lane**: everyone goes through the scanner; some bags get opened by hand.

![Checklist flow: identify the use case, add human review and compliance sign-off if it is high risk, then define governance policy, document usage, set up a feedback channel and review quarterly at the AI council](/content/skillup/ab731/images/ab731-d3-implementation-checklist.svg)

### Real use

An HR tool drafts performance improvement plans. It's high risk: the output affects careers. Before launch, the HR director puts in a usage policy, manager training, mandatory manager review of every draft, and quarterly council review.

### How it works

- **Fairness**: no unequal outcomes across groups (age, gender, ethnicity, disability).
- **Reliability and safety**: consistent, predictable, safe failures.
- **Privacy and security**: protected personal data, protected systems.
- **Inclusiveness**: works for everyone, including people with disabilities.
- **Transparency**: people know they're dealing with AI and can understand decisions.
- **Accountability**: humans stay answerable; "the AI decided" is never the answer.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| High-risk lane | Output affects money, jobs, services or safety | Review effort on every output |
| Standard lane | Low-risk internal productivity | Still needs policy and feedback |
| Block | A principle can't be met | Lost use case |

### How to do it

1. Classify the use case's risk.
2. Apply the controls for its lane: policy, training, human review, council oversight.
3. Test against each principle, including accessibility and group-level fairness.

### Exam Trap ⚠️

<div class="note-trap">Microsoft has <strong>six</strong> principles, not eight. Match the scenario: unequal outcomes by group is Fairness; "AI decision: denied" with no reason is Transparency; "who is responsible?" is Accountability; inconsistent output is Reliability. "Deploy, monitor and act if problems appear" fails a high-stakes use case.</div>

### Go deeper

- [Microsoft Responsible AI](https://www.microsoft.com/en-us/ai/responsible-ai)
- [What is responsible AI?](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai)

---

## 3.5 Establish an adoption team

### Key Concept

**Adoption needs named owners, from executive sponsor to champions, and at scale a council, a CoE and business-unit leads, each with its own job.**

An adoption team owns the rollout: not IT alone and not management alone. The executive sponsor funds it and signals that it matters; an adoption lead runs it day to day; IT and security deploy and protect; change management trains and communicates; champions make it real in each team. As AI scales, Microsoft's Scale AI framework adds a Centre of Excellence for standards and reuse, and business-unit AI leads to bridge the two.

**Think of building a kitchen, hiring the head chef, opening the restaurant, then letting specialist chefs write their own menus.**

![Scale AI framework in four phases: unlock AI value with focused pilots, organise for success with council, CoE and BU leads, empower business users with a broad Copilot rollout, then empower subject matter experts to build their own agents](/content/skillup/ab731/images/ab731-d3-scale-framework.svg)

### Real use

A Finance pilot agent succeeds, and Marketing, Sales and HR each start building their own with different connectors and security settings. The fix is the CoE's reusable asset library and standards, with business-unit leads routing builds through it. When IT later can't keep up with department requests, the CoE mentors Legal's experts to build their own contract-review agent.

### How it works

- **Adoption team roles**: executive sponsor, adoption lead, IT/security, change management, champions.
- **AI council**: what we do and whether we should (3.3).
- **Centre of Excellence**: how we build it well: standards, reusable assets, mentoring, a pre-production gate.
- **Business-unit AI leads**: bridge the CoE and each department.
- **Four phases**: unlock AI value, organise for AI success, empower business users, empower subject matter experts.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full adoption team | Broad, behaviour-changing rollout like Copilot | Staff time across functions |
| CoE + BU leads | Several teams building similar AI | A central team to fund |
| Technical owner + docs | Tiny expert audience | Not enough for broad rollout |

### How to do it

1. Name the sponsor, adoption lead and change owner before licences go out.
2. Stand up the CoE when duplication appears.
3. Move to empowering subject matter experts when IT becomes the bottleneck.

### Exam Trap ⚠️

<div class="note-trap">"IT can't keep up with department agent requests" is solved by empowering the experts with low-code tools and CoE mentoring, not by hiring more developers or having the council build. Council = strategy and ethics; CoE = technical standards and reuse.</div>

### Go deeper

- [Scale AI in your organization](https://learn.microsoft.com/en-us/training/modules/scale-ai/)
- [Establish an AI Center of Excellence](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/center-of-excellence)

---

## 3.6 Identify common barriers to adoption

### Key Concept

**Adoption fails on people and process far more than on technology; each common barrier has a known people-side fix.**

Barriers are predictable, so they can be planned for: fear of job loss, lack of trust, skills gaps ("I don't know where to start"), cultural worries ("I'll look lazy"), unclear policy, poor data and change fatigue. People also move through stages (awareness, interest, trial, adoption), and each stage needs a different lever.

**Think of weather on a flight plan**: you can't stop it, but you can route around it if you look before take-off.

![AI adoption curve in four stages: awareness through leadership comms, interest through demos and pilots, trial through champions, adoption through training and support](/content/skillup/ab731/images/ab731-d3-adoption-curve.svg)

### Real use

Six months in, Copilot adoption is 28% against a 70% target. Managers feel it threatens their expert status, employees don't know what's allowed, and training only toured features. The fix is people-side: leaders framing Copilot as amplifying expertise, a clear acceptable use policy, and training built around real workflows.

### How it works

- **Fear of job loss**: honest communication and reskilling.
- **Lack of trust**: transparency and visible results.
- **Skills gap**: workflow-based training and champions.
- **Unclear policy**: a published acceptable use policy.
- **Poor data**: fix data first (1.11).
- **Change fatigue**: prioritise; don't launch everything at once.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Leadership communication | People aren't aware or don't see why | Needs visible executive use |
| Demos and pilots | Aware but not trying | Time to run them |
| Champions + workflow training | Trying but not sticking | Champions' time |

### How to do it

1. Interview users to hear the barrier in their words.
2. Match each barrier to its lever.
3. Rule out technical blockers (licences not assigned) quickly, then work the people side.

### Exam Trap ⚠️

<div class="note-trap">Low adoption is almost never fixed by a technical action. "Re-provision licences", "upgrade the model" or "mandate usage with a leaderboard" are distractors. The answer names the barrier and the people-side lever.</div>

### Go deeper

- [Microsoft 365 Copilot adoption](https://adoption.microsoft.com/en-us/copilot/)

---

## 3.7 Establish an AI champions program

### Key Concept

**Champions are trusted peers in each team who coach colleagues and turn a central rollout into local habit.**

A champions programme finds enthusiastic early adopters in each business unit, trains them deeply, and makes them peer coaches. They show real use cases in their own work, answer "how do I use this in my job?", and bring feedback back to the adoption team. People take advice from a colleague who does the same job more readily than from IT or a mandate.

**Think of local guides in a new city**: the official map helps, but the person who lives there shows you the route people actually take.

![AI champions sit between two loops: the adoption team trains champions and receives best practices back, while champions coach peers and collect their questions and feedback](/content/skillup/ab731/images/ab731-d3-champions-network.svg)

### Real use

Four weeks into a pilot only 20% of users are active: they "don't know where to start" and worry AI "makes them look lazy". A champion in each team shows how they use Copilot for month-end close and openly shares prompts, and usage climbs because a respected peer went first.

### How it works

- **Recruit** volunteers with credibility in each department, before go-live.
- **Train** them deeper than everyone else.
- **Coach** peers in their real workflows.
- **Feed back** questions, wins and blockers to the adoption team.
- Champions aren't managers, the CoE or the council: policy questions go to governance, build questions to the CoE.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Champions programme | Broad rollout; team-level adoption lags | Volunteers' time |
| Central training only | Small, expert audience | Doesn't reach daily habits |
| Mandates | Never as the main lever | Compliance without value |

### How to do it

1. Recruit one or more champions per team before launch.
2. Give them early access, deeper training and a community.
3. Collect their feedback on a regular cadence and act on it.

### Exam Trap ⚠️

<div class="note-trap">"Identify enthusiastic users in each department to coach colleagues" is a champions programme. A "centralised team of AI specialists" is the CoE, and "the governance body for AI strategy" is the AI council.</div>

### Go deeper

- [Become a Microsoft 365 Champion](https://adoption.microsoft.com/en-us/become-a-champion/)

---

## 3.8 Understand potential impacts to data, security, privacy, and cost

### Key Concept

**Assess data, security, privacy and cost together before rollout; each one changes the scope, and scope changes the rest.**

Data classification decides which sites and users are in scope; privacy rules decide which regions; scope decides cost. Microsoft's commitments cover part of it: Microsoft 365 Copilot only surfaces data a user can already access, and prompts, responses and Graph data aren't used to train foundation models. Whether your permissions, labels and regional obligations are in order is still your job.

**Think of Microsoft's commitments as a well-built safe**: it protects what's inside, but you decide what goes in and who gets a key.

![Four impacts assessed together before rollout: data classification and permissions, security and audit, privacy and residency by region, and cost from licences and consumption, all feeding one final scope.](/content/skillup/ab731/images/ab731-3-8-four-impacts.svg)

### Real use

A US retailer plans a Copilot-based customer service solution for the EU, UK and APAC. Before rollout it classifies the data (including EU personal data), identifies GDPR and other regimes, documents where processing happens (Microsoft 365 Copilot is an EU Data Boundary service for EU customers), and only then fixes the scope and the licence count.

### How it works

- **Data**: what will AI reach, is it classified, are permissions right?
- **Security**: who can use AI features, what's logged, how is injection prevented?
- **Privacy**: which laws apply, where is data processed, how long is it retained (Purview retention covers Copilot interactions)?
- **Cost**: licences, consumption, training and support.
- The no-training commitment is real, but it doesn't satisfy every privacy obligation.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full four-way assessment | Graph-grounded Copilot or agents with org data | Weeks before rollout |
| Per-region review | Multinational footprint | Repeated work by region |
| Lighter review | Web-grounded Copilot Chat, no org data | Redo if scope grows |

### How to do it

1. Classify the data in scope and fix permissions.
2. Document applicable laws and processing locations per region.
3. Cost the final scope only after data and privacy sign-off.

### Exam Trap ⚠️

<div class="note-trap">"Does Microsoft train its models on our Copilot data?" No. But "the no-training commitment covers all compliance requirements" and "Microsoft's global certifications mean no regional review is needed" are both wrong. Licensing before the compliance review is the classic skipped step.</div>

### Go deeper

- [Data, privacy and security for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)
- [What is the EU Data Boundary?](https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn)

---

## 3.9 Understand Copilot license types, including pay-as-you go, monthly, and included with Microsoft 365 subscription

### Key Concept

**Three Copilot licence models do three jobs: included chat for everyone, a monthly licence for daily users, pay-as-you-go for occasional agent use.**

**Included**: Copilot Chat for eligible Microsoft 365 users at no extra cost, web-grounded with enterprise data protection, file upload and agents. **Monthly**: the per-user Microsoft 365 Copilot licence for Graph-grounded chat, Copilot in the apps, Researcher and Analyst. **Pay-as-you-go**: metered billing through an Azure subscription for agents used in Copilot Chat, SharePoint agents and the Copilot Retrieval API.

**Think of office transport**: everyone gets the shuttle bus, a taxi account covers occasional trips, and daily drivers get a company car.

![Three Copilot licence models: Copilot Chat included with Microsoft 365 for everyone, the monthly per-user Microsoft 365 Copilot licence for daily in-app users, and pay-as-you-go for occasional agent use billed through Azure.](/content/skillup/ab731/images/ab731-3-9-copilot-licences.svg)

### Real use

A 3,000-person company on Microsoft 365 E3 gives everyone Copilot Chat at no extra cost, buys the monthly licence for 400 people whose daily work needs Copilot in Word, Excel and PowerPoint over their own data, and covers a proposal-drafting agent's occasional users with pay-as-you-go for six months to learn their real usage.

### How it works

- **Included**: no incremental cost; no broad Graph grounding.
- **Monthly**: list price about US$30 per user per month on annual terms (check current pricing); eligible base plans include E3/E5, Business Basic/Standard/Premium, Office 365 E1/E3/E5 and F1/F3.
- **Pay-as-you-go**: linked by a billing policy in the Microsoft 365 admin center; it meters agents, not the full in-app experience.
- Copilot Studio has its own meter in Copilot Credits.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Included Copilot Chat | Everyone needs a secure general assistant | No org-data grounding |
| Monthly licence | Known users need Copilot in their apps and data daily | Fixed per-user cost |
| Pay-as-you-go | Occasional agent use, or learning usage before committing | Variable bill to monitor |

### How to do it

1. Segment users by need: general chat, daily in-app work, occasional agents.
2. License each segment with the matching model.
3. Review usage data to move heavy pay-as-you-go users onto monthly licences.

### Exam Trap ⚠️

<div class="note-trap">"Copilot is never included with Microsoft 365" is wrong: Copilot Chat is. Pay-as-you-go doesn't give unlicensed users the full Word, Excel and PowerPoint experience. A 50-user pilot of the full experience needs 50 monthly licences, not 2,000. And Business plans are eligible; it isn't E3/E5 only.</div>

### Go deeper

- [Microsoft 365 Copilot licensing](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-licensing)
- [Pay-as-you-go for Microsoft 365 Copilot Chat agents](https://learn.microsoft.com/en-us/copilot/microsoft-365/pay-as-you-go/overview)

---

## 3.10 Understand Foundry Tools subscription models, including pay-as-you-go and commitment tiers

### Key Concept

**Foundry Tools start on pay-as-you-go; a commitment tier trades a fixed monthly fee for a lower unit price once volume is predictable.**

**Pay-as-you-go** (Standard pricing) charges per transaction or call with no commitment. A **commitment tier** is a fixed monthly fee for a committed quantity of one feature (such as Speech to text, Translator, Language, Vision OCR or Document Intelligence) at a discounted rate, with usage above the quota charged at an overage rate. Tiers need a single-service resource, run by calendar month and are non-refundable once bought.

**Think of a phone plan**: per-minute billing, or a monthly bundle that's cheaper per minute only if you use the minutes.

![Foundry Tools pricing progression: start on pay-as-you-go during pilots and variable use, then move a feature with steady volume to a commitment tier; token-based model workloads use provisioned throughput instead.](/content/skillup/ab731/images/ab731-3-10-foundry-pricing.svg)

### Real use

A contact centre has run speech-to-text on Standard pricing for six months with stable volume. Moving that Speech resource to a commitment tier cuts the unit cost. A new translation pilot, with usage still unknown, stays on pay-as-you-go.

### How it works

- **Pay-as-you-go**: pilots, prototypes, variable workloads.
- **Commitment tier**: steady, high-volume production of one feature; monthly, non-refundable, changeable for next month.
- **Disconnected containers**: annual commitment plans for offline use.
- **Not the same as PTU**: provisioned throughput reserves capacity for token-based Foundry Models (such as Azure OpenAI deployments). Same logic: commit once usage is predictable.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Pay-as-you-go | Usage is new or volatile | Highest unit price |
| Commitment tier | Months of steady volume above break-even | Pay the fee even if unused |
| Provisioned throughput | Stable, high token volume on a model | Capacity commitment |

### How to do it

1. Start every new feature on pay-as-you-go.
2. Track monthly volume per feature for a few months.
3. Commit the features whose volume is steady and above the tier's break-even.

### Exam Trap ⚠️

<div class="note-trap">"Pay-as-you-go is always cheapest" is wrong for stable high volume; "commit on day one to lock the discount" is wrong for pilots. And don't pick a commitment tier for a token-based model workload: that's provisioned throughput.</div>

### Go deeper

- [Commitment tier pricing for Foundry Tools](https://learn.microsoft.com/en-us/azure/ai-services/commitment-tier)
- [Provisioned throughput](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/provisioned-throughput)

---

## Deep Dive: Making Implementation & Adoption Strategy Click

### 1. The connective narrative

This domain reads like a playbook because it is one, in the order a real rollout happens. Responsible AI comes first (3.1) because you can't govern against a standard you haven't defined. Governance comes next: written policy (3.2) and an AI council with the authority to say yes or no (3.3), plus a repeatable way to check each solution against the standards (3.4). Only then do people questions arrive: an adoption team (3.5), the barriers it will meet (3.6) and champions to build trust locally (3.7).

Impacts (3.8) sit before licensing (3.9, 3.10) on purpose. You classify data and check regional rules before deciding how many seats to buy, because the compliance review changes the scope, and scope changes the licence maths. The domain's biggest idea repeats in nearly every lesson: AI rollouts fail on culture and governance far more often than on technology, so the right answer is nearly always upstream of the technology.

### 2. Worked scenario

> **Scenario.** A 2,000-person professional services firm in Germany, the US and Singapore plans a Microsoft 365 Copilot rollout. Leadership wants to buy licences for everyone now. Following the domain's order, they adopt the six principles (3.1), write acceptable use and data handling policies (3.2) and form a cross-functional council with Legal and HR (3.3).
>
> The council requires an impacts review first (3.8): German employee data falls under GDPR, so the team documents that Microsoft 365 Copilot is an EU Data Boundary service, classifies client-privileged SharePoint content and fixes oversharing. Then licensing (3.9): Copilot Chat for everyone, monthly licences for 300 power users, pay-as-you-go for an occasional proposal agent. Champions are recruited in each office before go-live (3.7), and a year later the CoE mentors tax specialists to build their own agents (3.5).

### 3. Memory aid

**GRIP**: what keeps a rollout under control.
- **G**overnance: policy and the council (3.2, 3.3)
- **R**esponsible AI: six principles, checked per solution (3.1, 3.4)
- **I**mpacts: data, security, privacy, cost before scope (3.8)
- **P**eople: adoption team, barriers, champions (3.5–3.7)

For scaling: **Value, Organise, Users, Experts**.

### 4. Exam strategy for this domain

The traps are "skip a step" traps: licensing before compliance, technology before governance, an IT-only council, scaling before piloting. If an option treats a people or governance problem as a technology problem, it's wrong. Watch the licensing facts: Copilot Chat is included, Business plans are eligible for Microsoft 365 Copilot, and Copilot Studio bills in Copilot Credits.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Remove human review to save time | Accountability and Reliability concern |
| Principles document, nothing changed | Turn principles into policies, owners, controls, audit |
| What before rollout? | Acceptable use and data handling policies |
| Council membership | Cross-functional: business, IT, Legal, HR, functions |
| Auto-reject candidates | Council review (affects people) |
| Team-only, low-risk agent | Business-unit approval under policy |
| How many principles? | Six (Reliability & safety and Privacy & security are pairs) |
| Unequal outcomes by group / no explanation / "who is responsible?" | Fairness / Transparency / Accountability |
| Duplicated agents across teams | CoE standards and reusable assets, via BU leads |
| IT backlog of expert agents | Empower subject matter experts with low-code + CoE mentoring |
| Low adoption | Name the barrier, apply the people-side lever |
| Peer coaches per department | AI champions programme |
| Does Microsoft train on our Copilot data? | No, but that alone isn't full compliance |
| Multinational rollout | Classify data, check regional law and residency first |
| Everyone needs a secure assistant | Copilot Chat (included) |
| Daily in-app use over own data | Monthly Microsoft 365 Copilot licence |
| Occasional agent use | Pay-as-you-go |
| Steady Speech or Translator volume | Commitment tier |
| Steady token volume on a model | Provisioned throughput (PTU) |
