# D6: Governance, Risk, and Responsible Use

> **Exam weight**: 15% · **Questions**: ~12 in the bank

## Overview

This domain covers using Claude responsibly at work: recognising which uses are appropriate, handling sensitive and regulated data, following your organisation's AI policies and Anthropic's Usage Policy, and understanding the ethical side of using AI, including being open about it and owning the result.

> 💡 **Human Angle**: Most AI incidents at work aren't dramatic. They're a spreadsheet of customer data pasted into the wrong place, or an AI-drafted decision nobody checked.

---

## 6.1 Identify appropriate and inappropriate use cases

### Key Concept

**Low-risk drafting, analysis and research with a person accountable are good uses; decisions about people need a qualified human in the loop; some uses aren't allowed at all.**

Think in three zones. **Green:** drafting, summarising, analysing, brainstorming and research where a person reviews and owns the result. **Amber:** uses that affect people's health, legal rights, finances, jobs or access to essential services. Anthropic's Usage Policy requires a qualified human who can review and change Claude's recommendation, and disclosure to the person affected. **Red:** uses prohibited by the Usage Policy or your organisation's policy, and tasks that need certainty Claude can't give, such as final legal or medical judgements without an expert.

**Think of traffic lights**: green go, amber proceed with a qualified person in control, red stop.

![Three zones of use: green for drafting, summarising and research with a human owner; amber for decisions affecting health, money, legal rights or jobs, which need a qualified human in the loop and disclosure; red for uses prohibited by the Usage Policy or company policy.](/content/skillup/ccao/images/ccao-6-1-use-zones.svg)

### Real use

An HR team uses Claude to draft job adverts (green) and to summarise interview notes for the hiring panel, where the panel makes the decision (amber, human in the loop). A request to have Claude automatically reject candidates below a score is stopped: it's a decision about people with no human reviewing it.

### How it works

- **Green:** human owns and reviews the output; low impact if wrong.
- **Amber:** affects people's health, money, legal rights, livelihood or access to services; needs qualified human review with authority, plus disclosure.
- **Red:** prohibited by the Usage Policy or company policy.
- **Ask:** who is affected, and what if Claude is wrong?

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Go ahead | Green: low risk, person owns the result | Still review before use |
| Human in the loop | Amber: affects people's rights or money | Slower, but required |
| Don't use Claude | Red, or certainty is required | Do it another way |

### How to do it

1. Ask who is affected and what happens if the output is wrong.
2. Place the use in green, amber or red.
3. For amber, put a qualified person in charge of the decision and tell those affected.

### Exam Trap ⚠️

<div class="note-trap">"Claude scores candidates and the system rejects anyone below 60" is the classic inappropriate use: an automated decision about people with no qualified human in the loop. The fix isn't a better prompt; it's a person who makes the decision.</div>

### Go deeper

- [Anthropic Usage Policy](https://www.anthropic.com/legal/aup)
- [2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update)

---

## 6.2 Apply data sensitivity, regulatory, and privacy considerations

### Key Concept

**Before you paste or upload, ask what the data is, whether you're allowed to share it, and which Claude plan you're using; when in doubt, remove or anonymise it.**

Personal data, customer records, health or financial details, confidential business information and regulated data need care. Your organisation's rules decide what may be used, and on which plan. Plans differ: on consumer plans (Free, Pro, Max), whether chats are used to improve models depends on a privacy setting you control, and incognito chats are not used for training. On Team and Enterprise plans, under commercial terms, Anthropic doesn't use your data to train models. Often the simplest safe step is to remove or anonymise identifiers before uploading.

**Think of photocopying a document for an outside meeting**: black out what the room doesn't need to see.

![A data check before uploading: identify the data type, check the organisation's policy and the plan in use, then remove or anonymise identifiers, use an approved workspace, or don't upload at all.](/content/skillup/ccao/images/ccao-6-2-data-check.svg)

### Real use

A project manager wants Claude to find trends in a spreadsheet with customer names and account numbers. Company policy restricts sharing regulated personal data. She removes the names and account numbers, keeps region and product columns, and uploads the anonymised version in the company's Team workspace. The analysis works just as well.

### How it works

- **Classify:** personal, confidential, regulated or public?
- **Policy:** what your organisation allows, and on which plan.
- **Minimise:** share only the columns or passages the task needs.
- **Anonymise:** remove or replace names, IDs and account numbers.
- **Plan matters:** consumer privacy settings vs commercial (Team/Enterprise) terms.
- **Incognito** isn't saved to history or memory and isn't used for training, but it doesn't override your company's data policy.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Use as is | Public or approved, non-sensitive data | None |
| Anonymise first | Analysis doesn't need identities | Small preparation step |
| Don't upload | Policy forbids it, or identity is essential and not approved | Do the task another way |

### How to do it

1. Identify what kind of data it is.
2. Check your organisation's policy and which plan you're using.
3. Remove or anonymise identifiers, or don't upload.

### Exam Trap ⚠️

<div class="note-trap">"Upload it, then tell Claude not to remember it" doesn't satisfy a data policy: the data has already been shared. Remove or anonymise before uploading. And "it's only internal analysis" isn't an exemption.</div>

### Go deeper

- [Is my data used for model training?](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)
- [Who can view my conversations?](https://support.claude.com/en/articles/8325621-i-would-like-to-input-sensitive-data-into-my-chats-with-claude-who-can-view-my-conversations)

---

## 6.3 Follow organizational AI policies and governance standards

### Key Concept

**Your organisation's AI policy decides which plan, data and uses are allowed; follow it, and when it's silent, ask before you act.**

Organisations set rules for AI: which tools and plans are approved, what data may be used, which uses need sign-off, and how AI use is disclosed. On Team and Enterprise plans, owners and admins also control settings for everyone, such as whether memory, code execution or certain connectors are available, and which models can be used. Following policy means using the approved workspace rather than a personal account, respecting admin settings rather than working around them, and asking the policy owner when a case isn't covered.

**Think of the company expenses policy**: you don't decide alone what's reimbursable, and you ask when something is unusual.

![Policy in practice: use the approved workspace, not a personal account; respect admin settings; follow data and disclosure rules; and when the policy is silent, ask its owner before acting.](/content/skillup/ccao/images/ccao-6-3-policy.svg)

### Real use

A marketer wants to analyse customer feedback quickly and thinks of using her personal Claude account at home, where she has more features. Policy says company data goes only into the company's Enterprise workspace. She uses the workspace, and asks the AI governance lead whether a new connector can be enabled.

### How it works

- **Approved tools and plans:** company data stays in the approved workspace.
- **Admin settings:** memory, code execution, connectors and models may be set centrally.
- **Data rules:** what can be uploaded, and anonymisation requirements.
- **Disclosure:** when and how to say AI was used.
- **Escalate:** ask the policy owner when a case isn't covered.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Follow the policy | The case is covered | None; it's the rule |
| Ask the policy owner | Policy is silent or unclear | Short delay |
| Request a change | A rule blocks legitimate work | Takes time to approve |

### How to do it

1. Check the policy for the tool, data and use case.
2. Use the approved workspace and settings.
3. If unclear, ask the policy owner before going ahead.

### Exam Trap ⚠️

<div class="note-trap">Using a personal account "because it has more features" to work around company settings is the trap. So is assuming that silence in the policy means permission.</div>

### Go deeper

- [Anthropic Usage Policy](https://www.anthropic.com/legal/aup)
- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)

---

## 6.4 Understand the ethical implications of AI usage

### Key Concept

**Be open about AI's role, own the result you put your name to, and watch for bias and harm to the people affected.**

Anthropic's AI Fluency framework calls this **Diligence**: taking responsibility for how AI is used. In practice that means being transparent with colleagues and customers about AI's role where it matters, checking outputs for bias and fairness, respecting intellectual property and other people's data, considering who could be harmed, and remembering that "Claude wrote it" doesn't move accountability away from you.

**Think of a ghostwriter's client**: whoever signs the letter answers for what it says.

![Four ethical responsibilities: be transparent about AI's role, own and check the result, check for bias and fairness toward the people affected, and respect privacy and intellectual property.](/content/skillup/ccao/images/ccao-6-4-ethics.svg)

### Real use

A teacher uses Claude to draft feedback on student essays. She tells students AI helped draft feedback that she then reviewed, checks that the feedback isn't harsher for students writing in a second language, and changes anything she disagrees with. The grades remain her judgement.

### How it works

- **Transparency:** say when AI materially shaped the work, as your context requires.
- **Accountability:** you own what you send, whoever drafted it.
- **Fairness:** check for bias, especially in outputs about people.
- **Respect:** others' privacy, data and intellectual property.
- **Harm:** ask who could be hurt if the output is wrong or misused.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Disclose AI use | AI materially shaped work others rely on | Some readers may trust it less |
| Extra fairness review | Output describes or judges people | Takes more time |
| Don't use AI | Using it would mislead or harm | Do the work yourself |

### How to do it

1. Decide whether and how to disclose AI's role for this audience.
2. Review outputs about people for bias and fairness.
3. Take ownership: edit, check and stand behind what you send.

### Exam Trap ⚠️

<div class="note-trap">"The AI produced it, so the AI is responsible" is always wrong. Accountability stays with the person and organisation using it. Hiding AI's role where it matters to the reader is also a transparency failure.</div>

### Go deeper

- [AI Fluency: Framework & Foundations](https://www.anthropic.com/ai-fluency/overview)

---

## Deep Dive: Making Governance and Responsible Use Click

### 1. The connective narrative

This domain answers "should we, and how safely?" before "how?". Use cases (6.1) sort work into what's fine, what needs a qualified human in the loop and what's off-limits. Data handling (6.2) decides what can go into Claude at all and in what form. Organisational policy (6.3) sets the local rules and settings, with the policy owner as the person to ask. Ethics (6.4) runs through all of it: be open, be fair, and own the result.

### 2. Worked scenario

> **Scenario.** A bank's operations team wants Claude to help with loan-application summaries. Summarising for the loan officer is amber: the officer decides and the customer is told AI assisted (6.1). Applicants' account numbers are removed before upload, and only the bank's Enterprise workspace is used (6.2, 6.3). The team checks summaries for unfair wording about applicants and the officer remains accountable for every decision (6.4).

### 3. Memory aid

**ZONE**: **Z**one the use (green, amber, red) · **O**nly approved data and workspace · **N**otify people affected · **E**thics: own it and check fairness.

### 4. Exam strategy for this domain

Wrong answers prioritise speed or convenience: upload as is, use a personal account, let Claude decide, assume silence means yes. Right answers anonymise first, use the approved workspace, keep a qualified human in the loop and ask the policy owner.

---

## Cheat Sheet 📋

| Scenario says… | Answer |
|---|---|
| Automated decision about people | Qualified human in the loop, plus disclosure |
| Customer names and account numbers | Remove or anonymise before uploading |
| "Tell Claude not to retain it" | Not a data control |
| Personal account has more features | Use the approved workspace |
| Policy doesn't mention the case | Ask the policy owner |
| Consumer plan and training | Controlled by your privacy setting |
| Team or Enterprise and training | Not used for training under commercial terms |
| "The AI is responsible" | No: the person and organisation are |
| Output describes people | Check for bias and fairness |
