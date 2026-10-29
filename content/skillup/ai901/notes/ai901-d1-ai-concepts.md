# D1: Identify AI concepts and capabilities

> **Exam weight**: 40–45% · **Skills measured as of**: April 15, 2026 · One section per official task, 1.1 to 1.14

## Overview

Domain 1 is the vocabulary of the exam: the six responsible AI principles (1.1–1.6), how generative models work and are chosen, deployed and configured (1.7–1.9), and the common AI workloads (1.10–1.14). Domain 2 builds each of these in Microsoft Foundry.

> 💡 **Human Angle**: Most questions here are naming problems in disguise. Say what goes in and what must come out, and you can usually name the workload, the model and the principle at stake.

<div class="note-scribble"><strong>Naming note.</strong> Azure AI Foundry is now <strong>Microsoft Foundry</strong>, and Azure AI services are now <strong>Foundry Tools</strong> (for example "Azure Speech in Foundry Tools"). "Azure AI Studio" and "Cognitive Services" are retired names.</div>

---

## 1.1 Describe considerations for fairness in an AI solution

### Key Concept

**A fair AI system gives comparable outcomes to comparable people, whatever group they belong to.**

**Fairness asks whether the referee is biased**, not whether everyone wins.

![Fairness: deleting a sensitive column leaves proxies such as postcode behind, so compare outcomes per group and rebalance the data if there is a gap.](/content/skillup/ai901/images/ai901-1-1-fairness.svg)

### Real use

A lender compares loan approval and error rates by age band and region before launch. It finds one region rejected more often at equal income and retrains on rebalanced data before customers see it.

### How it works

- Bias usually starts in the data: a model trained on past decisions learns their bias.
- Deleting a sensitive column doesn't help when other features (postcode, career gaps, clubs) act as proxies.
- So fairness is measured: check training data for historical bias, then compare outcomes across groups.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Rebalance or augment training data | Testing shows a gap | More data and effort |
| Test outcomes per group (Fairlearn, RAI dashboard) | Always, before and after launch | Needs group labels for testing |
| Human review of borderline cases | Decisions are high-impact | Slower, staff cost |

If people can't *use* the system at all, that's inclusiveness (1.4), not fairness.

### How to do it

1. List groups that could be harmed (age, gender, region, language).
2. Measure outcomes and error rates per group on a held-out test set.
3. Fix the biggest gap, re-measure, and keep monitoring in production.

### Exam Trap ⚠️

<div class="note-trap">"We removed the gender column, so the model is fair" is wrong: proxies carry the same bias, so outcomes must still be tested across groups.</div>

### Go deeper

- [What is Responsible AI (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai)

---

## 1.2 Describe considerations for reliability and safety in an AI solution

### Key Concept

**Models are probabilistic and can be confidently wrong, so a safe system plans for being wrong.**

**Reliability is the seatbelt**: you fit it because a crash is possible.

![Reliability and safety: evaluate before launch, filter prompts and outputs with guardrails, answer only above a confidence threshold and route the rest to a person.](/content/skillup/ai901/images/ai901-1-2-reliability-safety.svg)

### Real use

A pharmacy chatbot answers medicine questions from approved leaflets. Low-confidence or risky dosage questions are routed to a pharmacist, and guardrails block harmful content.

### How it works

- Test with expected *and* edge-case inputs before release.
- Act only above a confidence threshold; route risky cases to a person.
- **Guardrails** (content filters) check prompts and outputs for harmful content.
- Keep monitoring in production: real users send inputs no test covered.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Confidence threshold + human fallback | Wrong answers are costly | Reviewer workload |
| Guardrails | Any public-facing generative app | Block harm, not factual errors |
| Evaluation + production monitoring | Every app | Finds some issues only after launch |

### How to do it

1. Define what "unsafe" or "wrong" means for this app.
2. Evaluate on realistic and adversarial prompts.
3. Configure guardrails in the Foundry portal (**Build > Guardrails**).
4. Route low-confidence outputs to a person; monitor and re-evaluate after changes.

### Exam Trap ⚠️

<div class="note-trap">"Set temperature to 0 so testing can be skipped" is wrong: a deterministic model can repeat the same wrong answer every time.</div>

### Go deeper

- [Guardrails and controls overview in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview)

---

## 1.3 Describe considerations for privacy and security in an AI solution

### Key Concept

**Protect personal and business data at every step: what goes into the model, what it stores and what it can reveal.**

![Privacy and security: redact PII before the model, logs or people see it, filter outputs, and restrict access, minimise data and delete it around every step.](/content/skillup/ai901/images/ai901-1-3-privacy-security.svg)

### Real use

A support centre runs PII detection on call transcripts, so card numbers and addresses are masked before analysts read them. An airport deletes face images as soon as a traveller is verified.

### How it works

- Collect only what you need; redact personal data before it reaches a model, a log or a person.
- Restrict access with Microsoft Entra ID and least-privilege roles.
- A model can leak data in its output: remove or anonymise sensitive training or grounding records and filter outputs for personal data.
- Prompts and completions sent to Foundry Models sold by Azure are not used to train the base models.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| PII redaction (Azure Language) | Text contains personal data | Run it before storage |
| Entra ID + RBAC, managed identity | Any production app | Setup vs shared keys |
| Data minimisation and deletion | Data is sensitive (faces, health) | Decide retention up front |

### How to do it

1. Map where personal data appears (inputs, files, logs, outputs).
2. Redact it with PII detection and restrict who can access the rest.
3. Set retention rules and test whether prompts can extract private details.

### Exam Trap ⚠️

<div class="note-trap">Masking PII or deleting images is <strong>privacy</strong>, not safety. Encryption protects stored data but does nothing about bias or bad answers.</div>

### Go deeper

- [Data, privacy and security for Foundry Models sold by Azure](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy)

---

## 1.4 Describe considerations for inclusiveness in an AI solution

### Key Concept

**An inclusive AI system can be used by everyone, including people with disabilities, accents or limited connectivity.**

**Inclusiveness asks whether everyone was allowed onto the pitch.**

![Inclusiveness: a voice-only kiosk shuts out people who can't hear or speak clearly, accented speakers and noisy places, while several input and output modes include them.](/content/skillup/ai901/images/ai901-1-4-inclusiveness.svg)

### Real use

A council's voice assistant also shows on-screen answers, accepts typed and touch input and supports several languages. It was tested with older residents and non-native speakers before launch.

### How it works

- Exclusion usually starts in the design: a voice-only kiosk shuts out people who can't hear or speak clearly.
- A speech model tested only on native speakers in a quiet room fails accents and noisy places.
- The fix: several ways to interact, and test groups that look like real users.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Captions, on-screen answers | Output is spoken | Small extra cost |
| Touch/text input beside voice | Input is voice-only | More UI to maintain |
| Diverse test groups | Always | Recruiting effort |

If everyone can use it but one group gets worse *decisions*, that's fairness (1.1).

### How to do it

1. List who might struggle (vision, hearing, motor, language, connectivity).
2. Offer at least two ways to interact and to receive output.
3. Test with those users and track error rates per group.

### Exam Trap ⚠️

<div class="note-trap">Captions or an alternative input mode map to <strong>inclusiveness</strong>, not transparency.</div>

### Go deeper

- [Embrace responsible AI principles and practices (training)](https://learn.microsoft.com/en-us/training/modules/embrace-responsible-ai-principles-practices/)

---

## 1.5 Describe considerations for transparency in an AI solution

### Key Concept

**People should know when they're dealing with AI, what it was built to do and where it can go wrong.**

**Transparency is the label on the medicine.**

![Transparency: an AI disclosure, stated limitations, sources and documented uses produce an informed user; without them users over-trust answers.](/content/skillup/ai901/images/ai901-1-5-transparency.svg)

### Real use

A bank tells loan applicants that AI helps screen applications and lists the main factors it uses. Its support bot cites the policy page behind each answer.

### How it works

- Transparency measures are things people can see or read: an AI disclosure, stated limitations, sources for answers, documented intended uses.
- Microsoft publishes **transparency notes** for its AI services so builders can pass the same information on.
- Without it, users trust answers they should have checked.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| "You're chatting with AI" + limitations | Any user-facing bot | Says nothing about a specific answer |
| Citations / source links | Grounded Q&A | Only as good as the sources |
| Documentation of uses and limits | Builders, auditors | Few end users read it |

### How to do it

1. Tell users up front that AI is involved and what it can get wrong.
2. Show sources for factual answers.
3. Publish intended uses, limitations and how to reach a human.

### Exam Trap ⚠️

<div class="note-trap"><strong>Transparency = telling people</strong> (disclosure, documentation); <strong>accountability = people answering for it</strong> (owners, review board).</div>

### Go deeper

- [Transparency note for Azure OpenAI in Foundry Models](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/transparency-note)

---

## 1.6 Describe considerations for accountability in an AI solution

### Key Concept

**Humans and the deploying organisation stay answerable for an AI system; responsibility never moves to the model.**

**Accountability is the pharmacist who signs for the medicine.**

![Accountability: after an incident the deploying organisation, not the model or its provider, answers for it through a named owner, review board, human sign-off and an off switch.](/content/skillup/ai901/images/ai901-1-6-accountability.svg)

### Real use

An insurer's AI claims triage has a named owner, a review board that approves changes, an audit log of automated decisions and a documented way to switch it off.

### How it works

- Accountability measures are things the organisation does: owners, oversight, an escalation process, human sign-off for consequential decisions.
- A model provider's filters help safety, but the organisation that deploys the solution must govern and monitor its own use case.
- Without it, after an incident everyone says "the model did it" and nobody owns the fix.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Named owner + escalation path | Every AI system | Needs real authority |
| Review board / governance | Several or high-risk systems | Slows releases |
| Human sign-off + audit logs | High-impact decisions | Staff cost, storage |

### How to do it

1. Name an owner and escalation path for each system.
2. Decide which decisions need human sign-off, and log them.
3. Agree how to pause, roll back or retire the system.

### Exam Trap ⚠️

<div class="note-trap">"The model provider is accountable for its outputs" is wrong. Accountability cannot be outsourced.</div>

### Go deeper

- [Responsible AI for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/responsible-use-of-ai-overview)

---

## 1.7 Describe how generative AI models work

### Key Concept

**A language model turns text into tokens and embeddings, then predicts the next most likely token, adds it and repeats until it predicts the end.**

**Think of it as extremely well-read predictive text.**

![Flow diagram for "Key Concept": append and repeat, Prompt text, Tokens, Embeddings, Transformer with attention, Next-token prediction, Completion](/content/skillup/ai901/images/ai901-d1-ai-concepts-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ai901/ai901-d1-ai-concepts-m1.mmd -->

### Real use

A help-desk team learns the model predicts rather than looks things up, so it puts the relevant knowledge-base articles in each prompt, and accuracy rises sharply.

### How it works

- **Token**: a small unit of text (word, part of a word, punctuation). Usage and cost are counted in tokens.
- **Embedding**: a vector where similar meanings point in similar directions; "dog" and "puppy" are close, "skateboard" is elsewhere (cosine similarity).
- **Attention** weighs how strongly each token relates to the others in its context; **positional encoding** gives word order.
- **LLMs** are large and general; **SLMs** (for example the Phi family) are compact enough for phones and edge devices.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| LLM | Open-ended or complex tasks | Cost, latency |
| SLM | Edge, offline or simple high-volume tasks | Narrower knowledge |

### Exam Trap ⚠️

<div class="note-trap"><strong>Attention = context</strong>; <strong>positional encoding = order</strong>. A token is not an API key and not always a whole word.</div>

### Go deeper

- [Introduction to generative AI and agents (training)](https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/)

---

## 1.8 Identify an appropriate AI model, based on capabilities

### Key Concept

**Match the model to the input and output you need first, then compare quality, cost and speed.**

**Choosing a model is like hiring**: read the CV, then give the shortlist a real task.

![Model choice: match the input and output to a chat, multimodal, embeddings, GPT-image, Azure Language or SLM option, then compare on leaderboards and test with your own prompts.](/content/skillup/ai901/images/ai901-1-8-model-choice.svg)

### Real use

A retailer's search uses an embeddings model (text-embedding-3-small) to match "warm waterproof jacket" to products, and a chat model only to write the summary shown to the shopper.

### How it works

- The Foundry catalog has **models sold directly by Azure** (including Azure OpenAI) and **partner and community models**.
- Multimodal models take image or audio plus text; embeddings models make vectors for search; GPT-image models create images; SLMs fit small devices.
- For well-defined tasks like language detection or PII detection, **Azure Language in Foundry Tools** gives consistent, structured output.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Chat model (LLM/SLM) | Write, summarise, chat | Output varies |
| Multimodal model | Image or audio input with text | Higher cost per call |
| Embeddings model | Semantic search, similarity | Produces vectors, not text |
| Azure Language | Fixed-format results (language, PII) | Fixed feature set |

### How to do it

1. Write down input type, output type, and whether output must be identical every time.
2. Filter the catalog, then compare candidates on the **leaderboards** (quality, safety, cost, throughput).
3. Try the shortlist with your own prompts using the playground's **compare** feature.

### Exam Trap ⚠️

<div class="note-trap">"Pick the model with the most parameters" or "the cheapest per token" are both wrong; match capability, then test with your own data.</div>

### Go deeper

- [Microsoft Foundry Models overview](https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview)
- [Model benchmarks and leaderboards](https://learn.microsoft.com/en-us/azure/foundry/concepts/model-benchmarks)

---

## 1.9 Identify appropriate model deployment options and configuration parameters

### Key Concept

**The deployment type decides where data is processed and how you pay; parameters decide how the model generates.**

**Deployment is the shipping contract; parameters are the cooking instructions.**

![Deployment choice: where data is processed (Global, Data Zone, Regional) plus how you pay (Standard, Provisioned, Batch) names the deployment type, such as Data Zone Standard.](/content/skillup/ai901/images/ai901-1-9-deployment-choice.svg)

### Real use

An EU retailer runs live chat on Data Zone Standard to keep processing in the EU, and its nightly product-description rewrite on Data Zone Batch for half the price.

### How it works

- **Where**: Global (any region), Data Zone (EU or US), Standard/Regional (one geography). **How you pay**: Standard per token; Provisioned reserves throughput for lower latency variance; Batch is asynchronous, 50% off, 24-hour target. Developer is only for testing fine-tuned models.
- **Temperature** lower = focused and deterministic; change temperature *or* **top_p**, not both. **Max tokens** too low cuts replies off. **frequency_penalty** cuts repetition; **presence_penalty** pushes new topics. HTTP 429 = rate limit: raise TPM within quota or cut max tokens and concurrency.

![Parameters: temperature or top_p, max tokens, frequency_penalty and presence_penalty each shape the reply; reasoning models don't accept most of them, and HTTP 429 is a rate limit.](/content/skillup/ai901/images/ai901-1-9-parameters.svg)

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Global Standard | Default, pay per token | Data may be processed in any region |
| Data Zone Standard | Processing must stay in EU/US | Fewer models or regions |
| Provisioned | Steady high volume, predictable latency | Pay for reserved capacity |
| Global / Data Zone Batch | Huge offline jobs | Up to 24 hours |

### Exam Trap ⚠️

<div class="note-trap">"Standard" is not "Global Standard". Reasoning models (GPT-5 series) don't accept temperature, top_p or the penalties.</div>

### Go deeper

- [Deployment types in Microsoft Foundry Models](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types)
- [Work with chat completion models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/chatgpt)

---

## 1.10 Identify scenarios for common AI workloads, including generative and agentic AI, text analysis, speech, computer vision, and information extraction

### Key Concept

**Name the workload from its required output: create content, take actions, analyse text, handle speech, see images or extract fields.**

**Workloads are verbs, not file types.**

![AI workload chooser: each input and required output maps to generative AI, agentic AI, text analysis, speech, computer vision or information extraction.](/content/skillup/ai901/images/ai901-d1-workload-chooser.svg)

### Real use

A retailer drafts emails with generative AI, lets an agent check orders and start returns, and pulls invoice fields into its finance system with information extraction.

### How it works

- **Generative AI** creates content; **agentic AI** adds instructions and tools so it can reason and act.
- **Text analysis** finds insights in text; **speech** converts audio and text; **computer vision** interprets images and video.
- **Information extraction** pulls specific fields into structured output. A scanned form is extraction if you need its values, vision if you only need to know it's signed.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Generative app | Output is new content | Can't take actions |
| Agent | Output is a completed task | More to test and govern |
| Information extraction | Output is named fields | Schema design needed |
| Computer vision | Output is a label, location or description | Not for field values |

### Exam Trap ⚠️

<div class="note-trap">"The forms contain text, so it's text analysis" is the classic trap: named fields mean information extraction.</div>

### Go deeper

- [What is Microsoft Foundry?](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)

---

## 1.11 Describe common text analysis techniques, including keyword extraction, entity detection, sentiment analysis, and summarization

### Key Concept

**Entities have types, key phrases don't, sentiment has a polarity, and summaries are either extracted or written.**

**Key phrases are the highlighter; entities are labelled sticky notes.**

![Text analysis on one review: NER gives typed entities, key phrases are untyped, sentiment and opinion mining give polarity per aspect, and summaries are extractive or abstractive.](/content/skillup/ai901/images/ai901-1-11-text-analysis.svg)

### Real use

A hotel group runs opinion mining on reviews and learns guests love the staff but dislike parking at three sites; managers read a weekly summary instead of 2,000 reviews.

### How it works

- **NER** labels entities with categories (Person, Location, DateTime); **key phrase extraction** returns untyped topics ("slow check-in").
- **Sentiment** is positive, neutral or negative with scores; **opinion mining** ties it to aspects ("parking" negative).
- **Extractive** summarization picks original sentences; **abstractive** writes new ones. **Language detection** and **PII detection** sit alongside.
- Azure Language marks key phrases, sentiment and summarization as legacy (retiring 2029); NER, PII and language detection stay core.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Azure Language (e.g. language detection SDK call) | Code needs consistent, structured values | Fixed features |
| Foundry model + prompt | Wording or task is open-ended | Output varies |

### Exam Trap ⚠️

<div class="note-trap">No type label ("slow check-in") = key phrases; labelled items (Seattle = Location) = NER.</div>

### Go deeper

- [What is Azure Language in Foundry Tools?](https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview)
- [Sentiment analysis and opinion mining](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview)

---

## 1.12 Identify features and capabilities of speech recognition and speech synthesis

### Key Concept

**Speech recognition turns audio into text; speech synthesis turns text into audio, and SSML controls how it sounds.**

**Recognition is the stenographer; synthesis is the narrator.**

![Speech: recognition turns audio into text through acoustic and language models; synthesis turns text marked up with SSML into audio with a neural voice.](/content/skillup/ai901/images/ai901-1-12-speech.svg)

### Real use

A contact centre batch-transcribes calls overnight with speaker diarization, and reads order updates to callers in a neural voice tuned with SSML.

### How it works

- Speech to text uses an acoustic model (audio to phonemes) and a language model (phonemes to words): real-time, fast (single file) or **batch** (archives via SAS URIs, asynchronous).
- **Diarization** separates speakers; **speech translation** changes language.
- Text to speech uses neural voices; **SSML** (XML) controls pauses, rate, pitch and pronunciation.
- Need specific fields (name, number, action) from recordings? That's a Content Understanding audio analyzer, not just a transcript.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Real-time speech to text | Live captions, commands | Not for archives |
| Batch transcription | Thousands of recordings | Asynchronous, best-effort |
| SSML | Pronunciation or pacing must be exact | More markup |
| Voice Live API | Live voice conversation with AI (2.7) | Built for sessions |

### Exam Trap ⚠️

<div class="note-trap">Diarization (who spoke) is not translation (which language). SSML is XML markup, not a model parameter.</div>

### Go deeper

- [What is Azure Speech?](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview)
- [SSML overview](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup)

---

## 1.13 Identify features and capabilities of computer vision and image-generation models

### Key Concept

**Vision models interpret existing images; image-generation models create new ones.**

**Vision is the critic; generation is the painter.**

![Vision versus generation: vision classifies, detects (where), captions and reads existing images; a GPT-image model creates new images and Sora creates video.](/content/skillup/ai901/images/ai901-1-13-vision-generation.svg)

### Real use

A factory flags defective circuit boards and draws a box round each defect; its marketing team mocks up packaging with a GPT-image model.

### How it works

- **Classification** labels the whole image; **object detection** adds bounding boxes ("where"); **captioning** describes the scene; **OCR** reads text.
- Many of these are now done by multimodal models; repeatable fields across many images suit a Content Understanding image analyzer.
- GPT-image models create images and Sora creates video. dall-e-3 was retired (March 2026) and Image Analysis 4.0 is deprecated.
- Face emotion and gender recognition are retired; identity features (verification, identification) need approved Limited Access.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Object detection | You need *where* | More labelling than classification |
| Captioning + OCR | Describe a scene *and* read its label | Two capabilities |
| Image generation | You need a new image | Review outputs for safety |

### Exam Trap ⚠️

<div class="note-trap"><strong>"Where" means detection</strong>, not classification. A receipt photo is a document job, not image analysis.</div>

### Go deeper

- [How to use vision-enabled chat models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/gpt-with-vision)
- [Image generation models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/dall-e)

---

## 1.14 Identify techniques to extract information from text, images, audio, and videos

### Key Concept

**Information extraction turns unstructured content into named fields by applying a schema by meaning.**

**OCR is a photocopier; Content Understanding is a clerk who fills in your spreadsheet.**

![Information extraction: documents, images, audio and video go through a Content Understanding analyzer with a schema applied by meaning and come out as named fields.](/content/skillup/ai901/images/ai901-1-14-information-extraction.svg)

### Real use

A clinic turns voicemails into a callback list: caller name, number and requested action land in its booking system, so staff no longer replay recordings.

### How it works

- **Azure Content Understanding in Foundry Tools** analyses documents, images, audio and video with OCR, speech recognition and generative models, returning markdown and JSON.
- The schema is applied by meaning: "Invoice No.", "Invoice #" and an unlabelled number can all map to `InvoiceNumber`.
- Documents give text, tables and layout; images a description; audio a transcript and summary; video a transcript of spoken words, key frames and per-segment descriptions or fields.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| OCR or speech to text only | You need raw text | No fields |
| Prebuilt analyzer | A standard form (invoice, receipt) | Fixed fields |
| Custom analyzer with schema | You name your own fields | Design and test the schema |

### Exam Trap ⚠️

<div class="note-trap">"Transcribe and store the transcript" isn't extraction: when fields are listed, the answer is an analyzer with a schema.</div>

### Go deeper

- [What is Azure Content Understanding?](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview)

---

## Deep Dive: Making AI Concepts Click

Every model in this domain predicts rather than knows. That is why the principles exist: reliability because predictions can be wrong, fairness because they inherit bias, transparency because users need to know they're reading a prediction.

> **Worked scenario.** An EU insurer wants a claims voice line, claim number, date and amount captured from each call, and a weekly complaints summary.
>
> **Workloads.** The voice line is speech plus generative AI (agentic if it looks up policies). Captured fields mean information extraction with a Content Understanding audio analyzer. The summary is text analysis: key phrases plus opinion mining.
>
> **Deployment.** The EU rule rules out Global Standard, so Data Zone Standard is used, and the weekly report runs on Data Zone Batch.
>
> **Principles.** Callers are told it's AI (transparency) and low-confidence fields go to a handler (reliability, accountability). Card details are redacted (privacy), a web form serves people who can't use voice (inclusiveness), and accuracy is checked across accents (fairness).

**Memory aids.** **FRIPTA**: Fairness · Reliability and safety · Inclusiveness · Privacy and security · Transparency · Accountability. Ask: *equal, safe, usable by all, protected, understood, owned?*

For workloads: **Create, Act, Analyse, Hear, See, Extract**.

---

## Cheat Sheet 📋

| Task | Concept | Key rule |
|---|---|---|
| 1.1 | Fairness | Test outcomes across groups; proxies defeat column deletion |
| 1.2 | Reliability and safety | Edge-case testing, guardrails, human fallback, monitoring |
| 1.3 | Privacy and security | Redact, restrict access, delete when done |
| 1.4 | Inclusiveness | Several input/output modes; diverse testers |
| 1.5 | Transparency | Disclose AI, limits and sources |
| 1.6 | Accountability | Owners and oversight; can't be outsourced |
| 1.7 | How models work | Next-token prediction; attention = context; positional encoding = order |
| 1.8 | Model choice | Input + output first; leaderboards, then your own prompts |
| 1.9 | Deployment | Global Standard default; Data Zone for EU/US; Provisioned steady; Batch offline |
| 1.9 | Parameters | Temperature *or* top_p; frequency = repetition; 429 = raise TPM |
| 1.10 | Workloads | Name the output: create, act, analyse, hear, see, extract |
| 1.11 | Text analysis | NER typed, key phrases untyped, opinion mining per aspect |
| 1.12 | Speech | Batch for archives; diarization = who; SSML = how it sounds |
| 1.13 | Vision | "Where" = detection; GPT-image creates; Face emotion retired |
| 1.14 | Extraction | Schema by meaning across documents, images, audio, video |
