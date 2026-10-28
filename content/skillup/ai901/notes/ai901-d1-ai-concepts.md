# D1: Identify AI concepts and capabilities

> **Exam weight**: 40–45% · **Skills measured as of**: April 15, 2026

## Overview

Domain 1 is the vocabulary of the exam. It covers three things: Microsoft's six responsible AI principles, how generative AI models work and how you choose, deploy and configure them, and the common AI workloads (generative and agentic AI, text analysis, speech, computer vision and information extraction). Domain 2 then asks you to build each of these in Microsoft Foundry, so almost every Domain 2 question quietly assumes the concepts here.

> 💡 **Human Angle**: Most questions in this domain are naming problems in disguise. If you can say what kind of input goes in and what kind of output comes out, you can usually name the workload, the model and the principle at stake.

<div class="note-scribble"><strong>Naming note.</strong> Azure AI Foundry is now <strong>Microsoft Foundry</strong>, and Azure AI services are now <strong>Foundry Tools</strong> (for example "Azure Speech in Foundry Tools", "Azure Content Understanding in Foundry Tools"). AI-901 uses the new names and replaces AI-900. Older study material that says "Azure AI Studio" or "Cognitive Services" describes the same ideas under retired names.</div>

---

## 1.1 The Six Responsible AI Principles

### Key Concept

**Microsoft's six principles are fairness, reliability and safety, privacy and security, inclusiveness, transparency and accountability.**

The principles are a checklist for any AI solution, not a feature of one product. Each one asks a different question: does the system treat people equally, does it behave safely, does it protect data, can everyone use it, do people understand it, and who answers for it?

Exam questions describe a measure (captions, a confidence threshold, a disclosure, a review board) and ask which principle it supports. Map the measure to the question it answers, not to the most impressive-sounding principle. **Think of the six principles as six inspectors walking round the same building**: each one checks something different, and a building can pass one inspection and fail another.

| Principle | The question it asks | Microsoft's own example |
|---|---|---|
| **Fairness** | Does it treat people equally? | A college admissions or loan model tested for bias |
| **Reliability and safety** | Does it behave safely, even when unsure? | A robot that only acts above a confidence threshold |
| **Privacy and security** | Is personal data protected? | Airport face images deleted after verification |
| **Inclusiveness** | Is anyone excluded from using it? | Text captions for a speech-based agent |
| **Transparency** | Do people know how it works and its limits? | A bank telling applicants AI is used in loan approval |
| **Accountability** | Who is responsible for it? | A governance framework the organisation applies |

### In Practice

**What breaks without this**: teams fix the principle they thought of first, such as adding a disclaimer, and ship a system that is still biased, still leaks data or still excludes users.

**Decision trigger**: for every design decision, ask which of the six questions it answers. If a principle has no measure against it, that is the gap.

**When you'd choose differently**: some measures serve two principles at once. Testing a speech app with diverse speakers supports both inclusiveness and fairness, and a human-review step supports both reliability and accountability. On the exam, pick the principle the measure most directly serves.

### Exam Trap ⚠️

<div class="note-trap">
Transparency and accountability are the most often swapped pair. <strong>Transparency = telling people</strong> (documentation, disclosure, limitations). <strong>Accountability = people answering for it</strong> (owners, governance, a board that can pause the system). If the measure is something users read, it is transparency; if it is someone with authority to act, it is accountability.
</div>

---

## 1.2 Fairness and Inclusiveness

### Key Concept

**Fairness is about equal outcomes for people who use the system; inclusiveness is about nobody being shut out of using it.**

Fairness problems usually start in the data. A model trained on historical decisions learns whatever bias those decisions held, and removing a sensitive column does not help if other features act as proxies for it. Microsoft's guidance is to minimise bias in the training data and to test the system's outcomes across groups of people.

Inclusiveness problems usually start in the design. A voice-only kiosk excludes people who cannot hear or speak clearly, and a speech model tested only on native speakers in a quiet room fails people with accents or in noisy places. **Fairness asks whether the referee is biased; inclusiveness asks whether everyone was allowed onto the pitch.**

### In Practice

**What breaks without this**: a loan model approves equally qualified applicants at different rates by postcode, or a speech app has far higher error rates for older users, and nobody notices until complaints arrive.

**Decision trigger**: ask who was in the training data and the test group, and who was not. Then ask whether any group gets worse outcomes, or cannot use the interface at all.

**When you'd choose differently**: if the issue is that users do not understand a decision, that is transparency, not fairness. If the issue is that a person's data leaks, that is privacy.

### Exam Trap ⚠️

<div class="note-trap">
"We removed the gender column, so the model is fair" is a classic wrong answer. Proxy features can carry the same bias, so fairness needs <em>outcome testing across groups</em>, not just deleting attributes. Fairness also does not mean everyone gets the same score.
</div>

---

## 1.3 Reliability and Safety, Privacy and Security

### Key Concept

**AI models are probabilistic, so reliable systems test widely, add guardrails and fall back safely; private systems protect data end to end.**

Reliability and safety means the system behaves as intended under expected and unexpected conditions. Because a model can be confidently wrong, safe designs act only above a confidence threshold, route risky or low-confidence cases to a person, apply content filters (guardrails) and keep monitoring in production.

Privacy and security means personal and organisational data is protected throughout the lifecycle: redact personal data before it is used, restrict access, delete what is no longer needed, and make sure the model cannot be prompted into revealing private details. **Reliability is the seatbelt for when the model is wrong; privacy is the lock on what the model can reveal.**

### In Practice

**What breaks without this**: a medicines assistant gives a wrong dosage with full confidence, or a model customised on HR records reveals an employee's salary to a cleverly worded prompt.

**Decision trigger**: ask "what happens when the model is wrong?" (reliability) and "what personal data can reach the model or its output?" (privacy).

**When you'd choose differently**: a low temperature makes answers more repeatable, but it does not make them correct, so it is never a substitute for testing. Encryption protects stored data but does nothing about bias or bad answers.

### Exam Trap ⚠️

<div class="note-trap">
Watch for "set temperature to 0 so testing can be skipped" or "evaluate once before launch, then monitoring is optional". Both are wrong: a deterministic model can repeat the same wrong answer every time, and real users send inputs that pre-release tests never covered.
</div>

---

## 1.4 Transparency and Accountability

### Key Concept

**Transparency means people know they are dealing with AI and understand its limits; accountability means humans stay answerable for it.**

Transparency measures are things users and stakeholders can see: a notice that AI is in use, an explanation of the factors a model considers, documentation of intended uses and known limitations, and citations showing where an answer came from.

Accountability measures are things the organisation does: name owners, set up governance and review, keep a human in the loop for consequential decisions, and be able to pause or fix the system. Responsibility never moves to the model or the model provider. **Transparency is the label on the medicine; accountability is the pharmacist who signs for it.**

### In Practice

**What breaks without this**: users trust an AI answer they should have checked, or, after an incident, the team says "the model generated it" and nobody owns the fix.

**Decision trigger**: ask "would a user know this is AI and what it can get wrong?" and "who can stop this system tomorrow if it causes harm?"

**When you'd choose differently**: a model provider's content filters help with reliability and safety, but they cannot be your accountability process. The deploying organisation still governs its own use case.

### Exam Trap ⚠️

<div class="note-trap">
"The model provider is accountable for everything its model outputs" is wrong. Accountability cannot be outsourced: the organisation that deploys the solution answers for how it is used.
</div>

---

## 1.5 How Generative AI Models Work

### Key Concept

**A language model turns text into tokens and embeddings, then predicts the next most likely token, over and over.**

Text is split into **tokens** (words, sub-words or punctuation), and each token gets a numeric ID. Tokens become **embeddings**: vectors with thousands of dimensions in which words with similar meanings point in similar directions, so "dog" sits near "puppy" and far from "skateboard" (measured with cosine similarity).

A **transformer** processes these vectors. **Attention** lets each token take its context into account, which is why "bank" means something different next to "river" than next to "account", and **positional encoding** tells the model the order of the tokens. The decoder then predicts the most probable next token, appends it and repeats until it predicts the end. **Think of it as extremely well-read predictive text**: it writes fluently because it has seen a lot, not because it looks answers up.

![Flow diagram for "Key Concept": append and repeat, Prompt text, Tokens, Embeddings, Transformer with attention, Next-token prediction, Completion](/content/skillup/ai901/images/ai901-d1-ai-concepts-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ai901/ai901-d1-ai-concepts-m1.mmd -->

Two related terms: **large language models (LLMs)** are big and general, and **small language models (SLMs)**, such as the Phi family, are compact enough for constrained devices. Usage, limits and cost are all measured in tokens.

### In Practice

**What breaks without this**: teams treat the model like a database, expect it to "look up" facts, and are surprised when it produces fluent, confident text that is wrong.

**Decision trigger**: if an answer must be factual and current, ask where the facts come from. If they are not in the prompt (grounding) or a tool, the model is predicting, not retrieving.

**When you'd choose differently**: for tasks with one correct structured answer (a language code, a redacted string), a purpose-built tool such as Azure Language is more consistent than next-token prediction.

### Exam Trap ⚠️

<div class="note-trap">
Positional encoding and attention are easy to swap. <strong>Positional encoding = order</strong>; <strong>attention = context</strong> (how much each token relates to the others). Also, a token is not an API key, and it is not always a whole word.
</div>

---

## 1.6 Choosing a Model by Capability

### Key Concept

**Match the model to the input and output you need first, then compare quality, cost and speed.**

The Foundry model catalog has two broad groups: **models sold directly by Azure** (including Azure OpenAI models, hosted and supported by Microsoft) and **models from partners and the community**. Within them, choose by capability: chat models for text generation, **multimodal** models for mixed input such as an image plus text (vision-enabled GPT models, Phi-4-multimodal-instruct), **embeddings** models (for example text-embedding-3-small) for semantic search, image-generation models for pictures, and SLMs for small devices.

For a well-defined task, such as detecting language or redacting PII, a **Foundry Tool** like Azure Language is often a better fit than a general model, because it returns structured, deterministic output. To compare candidate models, use the catalog's **leaderboards and benchmarks** (quality, safety, throughput), then try the shortlist with your own prompts. **Choosing a model is like hiring for a role**: read the CV first, then give the shortlist a real task.

| Need | Model type |
|---|---|
| Write, summarise, chat | Chat (LLM or SLM) |
| Understand an image or audio with text | Multimodal |
| Vectors for semantic search | Embeddings |
| Create images | Image generation (GPT-image family) |
| Run on a phone or edge device | Small language model |
| Consistent structured text results | A Foundry Tool such as Azure Language |

### In Practice

**What breaks without this**: teams default to the largest model for everything and pay more for slower answers, or use a chat model to produce vectors or language codes it was never meant to produce.

**Decision trigger**: write down the input type, the output type and whether the output must be identical every time. That usually picks the model category on its own.

**When you'd choose differently**: if the task is open-ended or the wording must adapt to context, a general chat model beats a purpose-built tool.

### Exam Trap ⚠️

<div class="note-trap">
"Pick the model with the most parameters" and "pick the cheapest per token" are both wrong answers. The exam rewards matching capability to the task and testing with your own data.
</div>

---

## 1.7 Deployment Options and Configuration Parameters

### Key Concept

**The deployment type decides where data is processed and how you pay; parameters decide how the model generates.**

Deployment types differ along two lines. Where data is processed: **Global** (any Azure region), **Data Zone** (within a zone such as the EU or US) or **Standard/Regional** (one Azure geography). How you pay: **Standard** types bill per token on a best-effort basis, **Provisioned** types reserve throughput units for predictable latency, and **Batch** types run large asynchronous jobs at a 50% discount with a 24-hour target. **Developer** deployments are only for evaluating fine-tuned models. Microsoft recommends starting with **Global Standard** for most workloads.

Parameters shape each response. **Temperature** controls randomness (lower is more focused), **top_p** limits sampling to the most likely tokens (change temperature or top_p, not both), **max tokens** caps response length, **frequency penalty** reduces verbatim repetition, **presence penalty** nudges the model towards new topics, and **stop sequences** end generation early. **Deployment type is the shipping contract; parameters are the cooking instructions.**

| Requirement | Deployment type |
|---|---|
| Default, newest models, lowest price, pay per token | Global Standard |
| Data processed only in the EU or US, pay per token | Data Zone Standard |
| Predictable latency at steady high volume | Provisioned (Global, Data Zone or Regional) |
| Huge offline job, cost over speed | Global Batch or Data Zone Batch |
| Test a fine-tuned model briefly | Developer |

### In Practice

**What breaks without this**: an EU company ships on Global Standard and breaks its data-processing commitment, or a summariser stops mid-sentence because max tokens is too low (finish reason "length").

**Decision trigger**: ask about data location first, then traffic shape (spiky, steady or offline), then latency needs. For parameters, ask whether you want variety or consistency.

**When you'd choose differently**: reasoning models (for example the GPT-5 series) do not accept temperature, top_p or the penalties, and use max completion tokens instead, so the usual tuning knobs do not apply.

### Exam Trap ⚠️

<div class="note-trap">
"Standard" is not "Global Standard". Standard processes data in one geography; Global Standard can use any region. Also, frequency penalty and presence penalty sound alike: <strong>frequency = stop repeating the same words</strong>, <strong>presence = move on to new topics</strong>.
</div>

---

## 1.8 Common AI Workloads

### Key Concept

**Name the workload from its input and output: create content, take actions, analyse text, handle speech, see images, or extract fields.**

**Generative AI** creates new content from a prompt. **Agentic AI** goes further: an agent combines a model, instructions and tools so it can reason about a request and act, such as looking up an order and starting a return. **Text analysis** finds insights in text (entities, key phrases, sentiment, summaries). **Speech** converts between audio and text. **Computer vision** interprets images and video. **Information extraction** turns unstructured content (forms, images, audio, video) into structured fields.

The same input can belong to different workloads depending on the output. A scanned claim form is information extraction if you need the policy number in a database, but computer vision if you only need to know whether a signature box is filled in. **Workloads are verbs, not file types**: ask what the solution has to do with the input.

| Scenario | Workload |
|---|---|
| Draft an email from bullet points | Generative AI |
| Check an order and start a return | Agentic AI |
| Find the main topics in reviews | Text analysis |
| Transcribe calls / read text aloud | Speech |
| Count cars in camera frames | Computer vision |
| Put invoice fields into a database | Information extraction |

![AI workload chooser: each input and required output maps to generative AI, agentic AI, text analysis, speech, computer vision or information extraction.](/content/skillup/ai901/images/ai901-d1-workload-chooser.svg)

### In Practice

**What breaks without this**: a team builds a chatbot when users needed fields in a database, or runs sentiment analysis on scanned forms when it needed extraction.

**Decision trigger**: finish the sentence "the output must be…". New content means generative; an action means agentic; named fields means extraction.

**When you'd choose differently**: real solutions combine workloads. A voice agent uses speech, generative AI and tools together; the exam asks which workload is central to the requirement.

### Exam Trap ⚠️

<div class="note-trap">
"The forms contain text, so it's text analysis" is the classic trap. Text analysis gives insights <em>about</em> text; information extraction maps values to <em>named fields</em>.
</div>

---

## 1.9 Text Analysis Techniques

### Key Concept

**Entities have types, key phrases do not, sentiment has a polarity, and summaries are either extracted or written.**

**Named entity recognition (NER)** finds entities and labels each with a category, such as Person, Location, Organization or DateTime. **Key phrase extraction** returns the main concepts ("wonderful staff", "slow check-in") with no category attached. **Sentiment analysis** labels text positive, neutral or negative with confidence scores, and **opinion mining** (aspect-based sentiment) ties sentiment to specific aspects ("breakfast" positive, "parking" negative). **Summarization** is **extractive** (selects original sentences) or **abstractive** (writes new ones).

Related capabilities are **language detection** (language plus a confidence score) and **PII detection** (finds personal and health information and can return redacted text). In Foundry you can do these with a general-purpose model and a prompt, or with **Azure Language in Foundry Tools**, which gives structured, consistent results. **Key phrases are the highlighter; entities are the labelled sticky notes.**

| Need | Technique |
|---|---|
| Typed people, places, organisations, dates | NER |
| Main talking points, untyped | Key phrase extraction |
| Overall positive or negative | Sentiment analysis |
| Which aspect was liked or disliked | Opinion mining |
| Summary of verbatim sentences | Extractive summarization |
| Summary in new words | Abstractive summarization |
| Mask personal data | PII detection |

### In Practice

**What breaks without this**: a team uses NER to find "what guests talk about" and gets only names and places, or uses document-level sentiment and loses which aspect was the problem.

**Decision trigger**: ask whether you need categories (NER), concepts (key phrases), feelings (sentiment), feelings per aspect (opinion mining) or a shorter text (summarization).

**When you'd choose differently**: Azure Language now marks key phrase extraction, sentiment analysis and summarization as legacy features (retiring in 2029) and directs new work to Foundry models, while NER, PII detection and language detection remain core. The techniques are the same; the tool you use for each is shifting.

### Exam Trap ⚠️

<div class="note-trap">
Key phrase extraction versus NER is the favourite trap. If the expected output has <strong>no type label</strong> ("slow check-in"), it is key phrases. If each item is <strong>labelled</strong> (Seattle = Location), it is NER.
</div>

---

## 1.10 Speech Recognition and Synthesis

### Key Concept

**Speech recognition turns audio into text; speech synthesis turns text into audio, and SSML controls how it sounds.**

**Speech to text** uses an acoustic model (audio to phonemes) and a language model (phonemes to words). Azure Speech in Foundry Tools offers **real-time** transcription with intermediate results, **fast transcription** for single files with predictable latency, and **batch transcription** for large volumes of recorded audio. **Diarization** separates speakers so a transcript can say who said what.

**Text to speech** uses neural voices that sound natural, and **custom voice** creates a branded voice (limited access). **SSML** (Speech Synthesis Markup Language) is XML that controls pauses, rate, pitch, volume and pronunciation. **Speech translation** converts speech in one language to speech or text in another. **Recognition is the stenographer; synthesis is the narrator, and SSML is the narrator's script directions.**

### In Practice

**What breaks without this**: a team tries to tune narration with a model temperature, or uses real-time recognition to work through an archive of ten thousand recordings.

**Decision trigger**: ask which direction the audio flows, whether it is live or recorded, and whether you need to know who spoke.

**When you'd choose differently**: for a full conversational voice agent, the Voice Live API combines recognition, a generative model and synthesis in one managed, low-latency service (see Domain 2).

### Exam Trap ⚠️

<div class="note-trap">
Speech translation (audio in, Azure Speech) is not text translation, and diarization (who spoke) is not speech translation (which language). SSML is XML markup, not a model parameter.
</div>

---

## 1.11 Computer Vision and Image Generation

### Key Concept

**Vision models interpret existing images; image-generation models create new ones.**

Core vision tasks: **image classification** labels the whole image, **object detection** labels objects and returns their bounding boxes, **captioning** describes the scene in a sentence, and **OCR** reads printed or handwritten text. Today, many of these tasks are done by **multimodal models** (vision-enabled GPT models) that take an image and a text instruction together.

**Image-generation models**, such as the GPT-image family, create or edit images from text prompts, and **Sora** models generate video. Older services are being retired: dall-e-3 was retired in March 2026, Azure Vision Image Analysis 4.0 is deprecated (retiring September 2028), and Face emotion and gender recognition were retired for responsible AI reasons. **Vision is the critic describing the painting; generation is the painter.**

| Need | Capability |
|---|---|
| Is there a defect in this photo? | Image classification |
| Where is each defect? | Object detection (bounding boxes) |
| One-sentence scene description | Captioning |
| Text printed on a label | OCR |
| A new image from a description | Image generation |

### In Practice

**What breaks without this**: a factory gets "this board has a defect" when it needed the defect's location, or a team tries to create marketing images with an analysis model.

**Decision trigger**: ask whether the output is a label, a location, a sentence, text read from the image, or a brand-new image.

**When you'd choose differently**: if the image is mostly text (a photographed receipt), document extraction is usually a better fit than image analysis.

### Exam Trap ⚠️

<div class="note-trap">
Classification versus object detection: <strong>"where" means detection</strong>. And captioning describes a scene while OCR reads text, so a question that needs both a description and the label text needs both capabilities.
</div>

---

## 1.12 Information Extraction Across Text, Images, Audio and Video

### Key Concept

**Information extraction turns unstructured content into named, structured fields by applying a schema by meaning.**

**Azure Content Understanding in Foundry Tools** ingests documents, images, audio and video, analyses them with OCR, speech recognition and generative models, and returns structured output (markdown and JSON). A **field schema** defines what you want, and it is applied semantically: "Invoice No.", "Invoice #" or an unlabelled number can all become `InvoiceNumber`. That is the difference from basic OCR, which reads text without understanding it.

Each modality yields different raw material. Documents give text, tables and layout; images give descriptions and fields; audio gives a WebVTT transcript, speakers and a summary; video gives a transcript of spoken words, key frames and segment descriptions. **OCR is a photocopier; Content Understanding is a clerk who reads the form and fills in your spreadsheet.**

### In Practice

**What breaks without this**: a clinic stores raw voicemail transcripts and staff still hunt for the callback number, or a parser built on fixed labels breaks on the first supplier who writes "Inv #".

**Decision trigger**: if the requirement names the fields it needs ("caller name, callback number, requested action"), it is extraction, whatever the input type.

**When you'd choose differently**: if you only need the raw text (OCR) or a transcript, plain speech to text or a read/layout analyzer is enough, and no field schema is needed.

### Exam Trap ⚠️

<div class="note-trap">
"Speech to text and store the transcript" looks like a complete answer for audio extraction, but a transcript is still unstructured. When the question lists specific fields, the answer is an analyzer with a schema.
</div>

---

## Deep Dive: Making AI Concepts Click

### 1. The connective narrative

Everything in this domain hangs off one idea: an AI model is a probabilistic predictor. Generative models predict the next token from embeddings shaped by attention; vision and speech models predict labels, words or boxes from pixels and sound waves. Because every one of them predicts rather than knows, the responsible AI principles are not optional extras. Reliability exists because predictions can be wrong, fairness because predictions inherit bias from data, and transparency because users need to know they are reading a prediction.

The model and deployment choices are how you manage those predictions in practice. You choose a model whose input and output types fit the job, a deployment type that fits your data-location and traffic rules, and parameters that trade variety for consistency. When the task has a single correct structured answer, you pick a purpose-built Foundry Tool, because deterministic output beats a creative guess.

The workloads are the shapes those predictions take. Learn them as input-to-output pairs: text to new text (generative), request to action (agentic), text to insights (text analysis), audio to text and back (speech), image to labels or descriptions (vision), and messy content to named fields (information extraction). Once you can name the pair, Domain 2 is simply "which Foundry tool or model does that pair?"

### 2. Worked scenario

> **Scenario.** A regional insurer wants three things: (1) a voice line where customers report claims, (2) the claim number, incident date and amount captured from each call into its claims system, and (3) a weekly summary of what customers complain about most. The insurer operates in the EU and must keep processing in the EU.
>
> **Reasoning.** Start with workloads. Item 1 is speech (recognition and synthesis) plus generative AI, and if the line can look up policies it becomes agentic. Item 2 names fields, so it is information extraction, here from audio with a Content Understanding analyzer whose schema has ClaimNumber, IncidentDate and Amount. Item 3 is text analysis on the transcripts: key phrase extraction to list topics, plus opinion mining to see which aspects are negative.
>
> **Model and deployment.** The extraction and summaries need a chat model, and Content Understanding also needs an embeddings model. Because of the EU rule, Global Standard is out; Data Zone Standard keeps processing in the EU zone with pay-per-token billing. The weekly report has no latency need, so a Data Zone Batch deployment could cut its cost.
>
> **Responsible AI.** Callers must be told they are speaking to AI (transparency). Low-confidence extracted fields go to a claims handler before payment (reliability and safety, accountability). Card numbers and health details are redacted from stored transcripts (privacy and security). The voice line also offers a text or web alternative for people who cannot use voice (inclusiveness), and the team checks extraction accuracy across accents (fairness).

### 3. Memory aid

**"FRIPTA"** for the six principles (the study guide lists privacy before inclusiveness; the order does not matter on the exam): **F**airness · **R**eliability and safety · **I**nclusiveness · **P**rivacy and security · **T**ransparency · **A**ccountability. Pair it with the question each asks: *equal? safe? usable by all? protected? understood? owned?*

For workloads, **"Create, Act, Analyse, Hear, See, Extract"**: generative, agentic, text analysis, speech, vision, information extraction.

### 4. Exam strategy for this domain

- Most traps are look-alike pairs: transparency/accountability, key phrases/NER, classification/detection, frequency/presence penalty, Standard/Global Standard, positional encoding/attention. Before choosing, say out loud what separates the pair.
- The exam rewards answers that test, monitor and keep humans responsible. It punishes answers that claim a single setting (temperature 0, a bigger model, a vendor filter) solves a responsible AI problem.
- For "which workload?" questions, ignore the file type and read the required output.
- Five minutes before the exam: **name the input, name the output, then name the principle at risk.**

---

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Responsible AI | Six principles: fairness, reliability and safety, privacy and security, inclusiveness, transparency, accountability |
| Transparency vs accountability | Telling people vs people answering for it |
| Token | Word, sub-word or punctuation; usage is measured in tokens |
| Embedding | Meaning as a vector; similar meaning, similar direction |
| Attention | Uses context; positional encoding gives order |
| SLM | Small model for constrained devices (for example Phi) |
| Global Standard | Recommended default; any region; pay per token |
| Data Zone | Processing within the EU or US zone |
| Provisioned | Reserved throughput; predictable latency |
| Batch | Asynchronous; 50% discount; 24-hour target |
| Temperature / top_p | Randomness; change one, not both |
| Frequency vs presence penalty | Less repetition vs more new topics |
| NER vs key phrases | Typed entities vs untyped concepts |
| Opinion mining | Sentiment per aspect |
| SSML | XML that controls synthesized speech |
| Diarization | Who spoke when |
| Object detection | Labels plus bounding boxes |
| Content Understanding | Schema-driven extraction from documents, images, audio and video |
