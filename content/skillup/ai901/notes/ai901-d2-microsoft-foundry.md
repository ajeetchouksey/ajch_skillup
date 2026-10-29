# D2: Implement AI solutions by using Microsoft Foundry

> **Exam weight**: 55–60% · **Skills measured as of**: April 15, 2026 · One section per official task, 2.1 to 2.15

## Overview

Domain 2 builds the Domain 1 workloads in Microsoft Foundry and expects you to read short Python snippets. **One Foundry resource holds the shared platform (models, quotas, security); each Foundry project inside it is a workspace for one app.** `AIProjectClient` uses the project endpoint `https://<resource>.services.ai.azure.com/api/projects/<project>`.

> 💡 **Human Angle**: Every app follows four beats: get an endpoint, authenticate, send a request in the right shape, read the right property. Learn them once and each service is just new names.

![Microsoft Foundry flow: a Foundry resource contains projects; in a project you deploy a model from the catalog, test it in the playground, optionally save it as an agent with tools, then call the deployment or agent from a client app through the project endpoint.](/content/skillup/ai901/images/ai901-d2-foundry-flow.svg)

<div class="note-scribble"><strong>Code note.</strong> Snippets follow the AI-901 modules and current Foundry docs (October 2026; <code>azure-ai-projects</code> 2.x). The exam tests the pattern, not exact versions.</div>

---

## 2.1 Create effective system and user prompts for generative AI models

### Key Concept

**The system prompt sets the rules for the whole conversation; the user prompt is the request.**

**The system prompt is the job description; the user prompt is today's task.**

### Real use

An HR assistant's system prompt says "Answer only from the policy text provided; if it isn't there, say you don't know." Invented policy answers stop.

### How it works

- Rules for every reply (role, scope, tone, output format) go in the **system prompt**, which the app controls.
- **Grounding** puts source text in the prompt, says "answer only from it" and allows "I don't know"; this reduces fabrication.
- **Few-shot** examples guide format and style for that request only; they don't retrain the model.
- Each request stands alone, so chat apps resend earlier turns or use a conversation.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| State output structure + an example | Code parses the reply | Tokens on every call |
| Grounding with source text | Answers must match your data | Longer prompts |
| Fewer prompt tricks | Reasoning models (GPT-5 series) | Chain-of-thought not recommended |

### How to do it

1. Write role, scope and output format in the system prompt.
2. Paste the source text and say "answer only from it; otherwise say you don't know".
3. Add one example of the exact output format, then test in the playground.

### Exam Trap ⚠️

<div class="note-trap">"Add 'always be accurate' and raise the temperature" never fixes fabrication; grounding does.</div>

### Go deeper

- [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)

---

## 2.2 Deploy a model and interact with it in the Foundry portal

### Key Concept

**Deploying allocates capacity and creates an endpoint that apps call by deployment name; the playground is where you test it first.**

**The deployment is the phone line; the playground is the test call.**

### Real use

A support team compares two models side by side in the playground on 20 real tickets, picks the cheaper one that scored as well, and exports the code for developers.

### How it works

- Workflow: create a project, deploy a model from the catalog, test in the playground, then call it from the app.
- At deployment you set the name, type (e.g. Global Standard), version and tokens-per-minute (TPM) limit. It doesn't train the model.
- The playground sets instructions and parameters, compares models side by side, exports code and can **save as agent**.
- Use one Foundry resource with a separate project per app.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Raise TPM within quota | HTTP 429 errors | Uses more quota |
| Cut max tokens / concurrency | 429 and no quota left | Shorter or slower replies |
| Playground compare | Choosing between models | Small sample only |

### How to do it

1. In your project, open the **model catalog**, pick a model and select **Deploy**.
2. Set deployment name, type and TPM.
3. Open it in the **playground**, add instructions, test real and tricky prompts.
4. Use **View code** to copy the endpoint and sample.

### Exam Trap ⚠️

<div class="note-trap">429 is a capacity problem: temperature changes nothing, and a Developer deployment is only for evaluating fine-tuned models.</div>

### Go deeper

- [Deploy Foundry Models in the portal](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/deploy-foundry-models)
- [Microsoft Foundry playgrounds](https://learn.microsoft.com/en-us/azure/foundry/concepts/concept-playgrounds)

---

## 2.3 Create a lightweight chat client application by using the Foundry SDK

### Key Concept

**`AIProjectClient` connects to the project; `get_openai_client()` gives a client that calls the model by deployment name.**

**The project client is the receptionist; the OpenAI client is who you're put through to.**

### Real use

An internal IT helper is a 15-line script on a VM that authenticates with the VM's managed identity, so no API key is stored anywhere.

### How it works

- Package `azure-ai-projects`; credential `DefaultAzureCredential` from `azure-identity` (run `az login` as an identity with project access).
- Call the Responses API with `model=` set to the **deployment name** and read `output_text`.
- Each request stands alone: resend history or use a conversation.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `AIProjectClient` + Entra ID | Production; same client for agents | Needs sign-in or managed identity |
| Plain `OpenAI` client + API key | Quick local test | Key must be protected |
| Chat Completions | Existing samples (`choices[0].message.content`) | Not the base for agents |

### How to do it

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
                          credential=DefaultAzureCredential())
openai = project.get_openai_client()
r = openai.responses.create(model="support-chat",   # deployment name
                            input="What can you help me with?")
print(r.output_text)
```

### Exam Trap ⚠️

<div class="note-trap"><code>model=</code> takes the <strong>deployment name</strong>, not the model family. <code>DefaultAzureCredential</code> doesn't take an API key.</div>

### Go deeper

- [Quickstart: Get started with the Microsoft Foundry SDK](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code)

---

## 2.4 Create and test a single-agent solution in the Foundry portal

### Key Concept

**An agent is a model plus instructions plus tools; tools take actions and knowledge grounds answers in data.**

**Instructions are the job description, tools the toolbox, knowledge the library.**

### Real use

An outdoor retailer's agent uses file search over 40 PDF manuals and answers "how do I re-proof this jacket?" with a citation to the right page.

### How it works

- **File search** indexes uploaded files for grounded, cited answers; **code interpreter** runs Python for calculations and charts; **web search** gets current public information.
- The **Azure Language MCP server** tool connects with your Foundry resource name; no separate Language resource is needed.
- **Publishing** turns the agent into a managed Azure resource with a stable endpoint.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| File search | Answers from your own documents | Keep files current |
| Code interpreter | Calculations, data, charts | Sandbox only |
| Web search | Current public information | Less control of sources |
| No agent | No tools needed | Plain deployment is simpler |

### How to do it

1. Go to **Build > Agents > Create agent** (or **Save as agent** from the playground).
2. Choose the model deployment and write instructions.
3. Add tools (upload files for file search).
4. Test in the **agents playground** with expected and tricky questions, then publish.

### Exam Trap ⚠️

<div class="note-trap"><strong>Private documents = file search</strong>; <strong>public, current = web search</strong>. Calculations need code interpreter.</div>

### Go deeper

- [Quickstart: Create a prompt agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent)
- [File search tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search)

---

## 2.5 Create a lightweight client application for an agent

### Key Concept

**Apps call an agent through the Responses API with an agent reference, authenticated with Microsoft Entra ID.**

**The agent reference is the name badge on the request.**

### Real use

A website chat widget calls the published product-help agent from a small back end, with one conversation per shopper so follow-ups keep context.

### How it works

- Use `AIProjectClient` + `DefaultAzureCredential`; this code path needs Entra ID, not an API key.
- Name the agent with `extra_body={"agent": {..., "type": "agent_reference"}}`.
- For multi-turn chat, create a **conversation** and pass its ID in each call. Threads and runs are retired Assistants vocabulary.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Call the agent | You need its tools and knowledge | More setup |
| Call the model (2.3) | No tools needed | You manage prompts yourself |

### How to do it

```python
agent = project_client.agents.get(agent_name="learning-agent")
openai_client = project_client.get_openai_client()
r = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}})
print(r.output_text)
```

### Exam Trap ⚠️

<div class="note-trap">An option using <code>threads.runs.create</code> describes the retired Assistants API, not Foundry Agent Service.</div>

### Go deeper

- [What is Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/foundry/agents/overview)

---

## 2.6 Build a lightweight application that includes text analysis

### Key Concept

**Use Azure Language when the app needs consistent, structured values, and a general model when wording can vary.**

**Azure Language is a form that always comes back filled in the same way.**

### Real use

A ticketing system detects each ticket's language to route it, and stores only PII-redacted text so agents never see card numbers.

### How it works

- SDK `azure-ai-textanalytics`; `TextAnalyticsClient` with endpoint and `AzureKeyCredential`.
- Methods take a **list** of documents: `detect_language([text])[0]` returns `primary_language` (name, ISO code, score).
- `recognize_pii_entities([text])[0]` returns `redacted_text` and the entities.
- Agents can use Language through the Azure Language MCP server tool.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Azure Language SDK | Code parses the result | Fixed features |
| Foundry model + prompt | People read the result | Output varies |

### How to do it

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
print(client.detect_language([text])[0].primary_language.iso6391_name)
print(client.recognize_pii_entities([text])[0].redacted_text)
```

### Exam Trap ⚠️

<div class="note-trap">Pass <code>[text]</code> and read <code>[0]</code>. Masked output is <code>redacted_text</code>, not <code>entities</code>.</div>

### Go deeper

- [PII detection in Azure Language](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview)

---

## 2.7 Respond to spoken prompts by using a deployed multimodal model

### Key Concept

**An audio-capable model takes speech in and answers directly, without a separate transcription step.**

**It listens and thinks in one step.**

### Real use

Technicians ask a field-service app questions by voice with their hands busy; an audio-capable model answers in speech.

### How it works

- Deploy a multimodal model that accepts audio (gpt-audio, gpt-realtime family, Phi-4-multimodal-instruct).
- Audio goes in an `input_audio` content part as base64 data with a format such as `wav`.
- For spoken replies, set `modalities` to text and audio plus an `audio` setting with voice and format.
- The **Voice Live API** is a managed, low-latency speech-to-speech service for live conversations.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Audio-capable model | One spoken question | Fewer speech-tuning options |
| Voice Live API | Live, natural conversation | Session-based |
| Azure Speech + text model (2.8) | Custom recognition or SSML | More parts to wire |

### How to do it

```python
completion = client.chat.completions.create(
    model="gpt-audio-deployment",
    modalities=["text", "audio"], audio={"voice": "alloy", "format": "wav"},
    messages=[{"role": "user", "content": [
        {"type": "input_audio", "input_audio": {"data": audio_b64, "format": "wav"}}]}])
```

### Exam Trap ⚠️

<div class="note-trap">Audio goes in an <code>input_audio</code> part as base64, not an <code>image_url</code> or a file path in the prompt.</div>

### Go deeper

- [Voice Live API overview](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live)
- [Quickstart: Azure OpenAI audio generation](https://learn.microsoft.com/en-us/azure/foundry/openai/audio-completions-quickstart)

---

## 2.8 Build a lightweight application by using Azure Speech in Foundry Tools

### Key Concept

**Azure Speech gives any app specialist ears (recognition) and a voice (synthesis).**

**Recognition is the stenographer; synthesis is the narrator.**

### Real use

A delivery IVR reads "Your order has shipped" in a neural voice and transcribes callers' replies continuously so nothing is cut off after one sentence.

### How it works

- SDK `azure-cognitiveservices-speech`; `SpeechConfig` with the Foundry resource key and endpoint.
- `recognize_once_async()` handles one utterance (about 30 seconds); `start_continuous_recognition()` with `recognized` handlers handles long speech.
- Synthesis: set `speech_synthesis_voice_name`, create a `SpeechSynthesizer`, call `speak_text_async(text).get()`.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `recognize_once_async()` | Short commands | Stops after one utterance |
| Continuous recognition | Dictation, long speech | Event handling code |
| Batch transcription | Archives (SAS URIs, async) | Best-effort timing |
| Voice Live (2.7) | Speech must drive reasoning and tools | Session-based |

### How to do it

```python
import azure.cognitiveservices.speech as speechsdk
cfg = speechsdk.SpeechConfig(subscription=key, endpoint=endpoint)
print(speechsdk.SpeechRecognizer(speech_config=cfg).recognize_once_async().get().text)

cfg.speech_synthesis_voice_name = "en-US-Ava:DragonHDLatestNeural"
speechsdk.SpeechSynthesizer(speech_config=cfg).speak_text_async("Your order has shipped.").get()
```

### Exam Trap ⚠️

<div class="note-trap"><code>speak_text_async</code> is synthesis; <code>recognize_once_async</code> is recognition. Archives need batch transcription.</div>

### Go deeper

- [Speech to text quickstart](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text)
- [Batch transcription](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription)

---

## 2.9 Interpret visual input in prompts by using a deployed multimodal model

### Key Concept

**Put an image and a text instruction in the same user message, and a vision-capable model answers about the image.**

**It's a photo handed over with a sticky note: the note is the question.**

### Real use

An insurer's app lets customers photograph car damage; the model describes the damaged parts and pre-fills a claim for an assessor to confirm.

### How it works

- Responses API: an `input_text` part plus an `input_image` part. Chat Completions: an `image_url` part with optional `detail`.
- Image URLs must be reachable by the service, so private images go as base64 data URLs.
- `detail: "high"` processes at higher resolution to read small text; `"low"` is cheaper.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Public URL | Image is internet-reachable | None for private files |
| Base64 data URL | Private or uploaded images | Bigger request |
| `detail: "high"` | Fine print matters | More tokens |

### How to do it

```python
r = client.responses.create(model=deployment, input=[{"role": "user", "content": [
    {"type": "input_text", "text": "What is in this image? Give 3 bullet points."},
    {"type": "input_image", "image_url": image_url}]}])
print(r.output_text)
```

### Exam Trap ⚠️

<div class="note-trap">Responses API uses <code>input_image</code>; <code>image_url</code> with <code>detail</code> is the Chat Completions format.</div>

### Go deeper

- [How to use vision-enabled chat models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/gpt-with-vision)

---

## 2.10 Create new visual outputs by using generative models

### Key Concept

**Image models return base64 data you decode and save; video models run as jobs you poll.**

**Image generation is a vending machine; video is a print shop where you collect the order later.**

### Real use

A marketing team generates five banner concepts from one brief, then uses image edit with a mask to change only the background of the winner.

### How it works

- Use the **GPT-image** family; dall-e-3 was retired on 4 March 2026.
- `images.generate(...)` returns base64 in `data[0].b64_json`; decode it and write the bytes to a file.
- **Sora** video: create a job, poll its status, then download the video.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `images.generate` | New still image | Review for safety and brand |
| Image edit with mask | Change part of an image | Need a mask |
| Sora | Short video | Minutes per job |

### How to do it

```python
import base64
result = client.images.generate(model="gpt-image-deployment",
                                prompt="Flat illustration of a tent at dawn", size="1024x1024")
open("tent.png", "wb").write(base64.b64decode(result.data[0].b64_json))
```

### Exam Trap ⚠️

<div class="note-trap">GPT-image models don't return an image URL, and dall-e-3 is retired.</div>

### Go deeper

- [Image generation models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/dall-e)
- [Sora video generation overview](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/video-generation)

---

## 2.11 Build a lightweight application that includes vision capabilities

### Key Concept

**A lightweight vision app is a vision-capable deployment plus a photo and a text instruction in one request; no custom training.**

**Treat the model as a sharp-eyed assistant that needs a clear question and answer format.**

### Real use

A warehouse app photographs each shelf at closing time; the model returns `{"empty_slots": 3}` and a restock list is generated automatically.

### How it works

- Read the image, base64-encode it, send it with an instruction, and ask for a fixed format such as JSON.
- Image Analysis 4.0 is deprecated (retiring 25 September 2028) and Custom Vision is retiring; use multimodal models or Content Understanding.
- Face emotion and gender recognition are retired; identity features need approved access.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Multimodal model + prompt | Flexible questions about images | Validate free-form output |
| Content Understanding image analyzer | Same fields from many images | Schema design |
| Document analyzer (2.12) | Text-heavy images like receipts | Not for scenes |

### How to do it

```python
import base64
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(endpoint=project_endpoint, credential=DefaultAzureCredential())
client = project.get_openai_client()
b64 = base64.b64encode(open("shelf.jpg", "rb").read()).decode()
r = client.responses.create(model="vision-chat", input=[{"role": "user", "content": [
    {"type": "input_text", "text": 'Count empty slots. Reply as JSON: {"empty_slots": int}'},
    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64}"}]}])
print(r.output_text)
```

1. Test the prompt in the playground with a sample image.
2. Validate the JSON in code.
3. Send unexpected results to a person.

### Exam Trap ⚠️

<div class="note-trap">New vision apps built on Image Analysis custom models, Custom Vision or Face emotion detection point at retired or retiring services.</div>

### Go deeper

- [How to use vision-enabled chat models](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/gpt-with-vision)
- [What is Azure Vision in Foundry Tools? (retirement notes)](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview)

---

## 2.12 Extract information from documents and forms by using Azure Content Understanding in Foundry Tools

### Key Concept

**An analyzer takes a document in, applies AI and a schema, and returns structured fields; prebuilt analyzers cover common forms.**

**Extract, classify and generate are copy, tick a box and write a sentence.**

### Real use

An accounts-payable team runs `prebuilt-invoice` on supplier PDFs and only reviews fields with low confidence.

### How it works

- Prebuilt: `prebuilt-read`/`prebuilt-layout` (text, tables), `prebuilt-invoice`, `prebuilt-receipt`, `prebuilt-idDocument`, `prebuilt-contract`. Custom analyzers start from `prebuilt-document`.
- Field methods: **extract** (value on the page, documents only), **classify** (fixed list), **generate** (written value).
- Confidence and grounding are off by default: enable `estimateFieldSourceAndConfidence`.
- Most analyzers need a chat completion model and an embeddings model deployed and set as defaults; read and layout need none.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `prebuilt-read` / `prebuilt-layout` | You need text and tables only | No named fields |
| Domain prebuilt (invoice, receipt) | Standard forms | Fixed fields |
| Custom analyzer | Your own fields | Design and test the schema |

### How to do it

```json
{ "baseAnalyzerId": "prebuilt-document",
  "config": { "estimateFieldSourceAndConfidence": true },
  "fieldSchema": { "fields": {
    "VendorName":       { "type": "string", "method": "extract" },
    "DocumentCategory": { "type": "string", "method": "classify", "enum": ["Goods", "Services"] },
    "Summary":          { "type": "string", "method": "generate" } } } }
```

### Exam Trap ⚠️

<div class="note-trap">Confidence isn't on by default, and extract works only for documents.</div>

### Go deeper

- [Analyzer configuration reference](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/analyzer-reference)
- [Prebuilt analyzers](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/prebuilt-analyzers)

---

## 2.13 Extract information from images by using Content Understanding

### Key Concept

**Image analyzers turn photos into descriptions and fields using generate and classify, never extract.**

**A photo is a witness to a scene: ask what it saw, not what it says in writing.**

### Real use

A retailer analyses shelf photos from 300 stores; `ShelfStatus` is classified Full, Low or Empty and a dashboard shows which stores need restocking.

### How it works

- `prebuilt-imageSearch` returns a paragraph description.
- A custom analyzer on `prebuilt-image` adds your fields with classify or generate.
- Image analyzers aren't tuned for text-heavy images: a receipt photo belongs with `prebuilt-receipt`.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `prebuilt-imageSearch` | You need a description | No custom fields |
| Custom on `prebuilt-image` | Your own fields from scenes | Schema design |
| Document analyzer | Receipts, invoices, IDs | Not for scenes |
| Multimodal model (2.9) | One-off question | No schema or confidence |

### How to do it

```json
{ "baseAnalyzerId": "prebuilt-image",
  "fieldSchema": { "fields": {
    "ShelfStatus": { "type": "string", "method": "classify", "enum": ["Full", "Low", "Empty"] },
    "Notes":       { "type": "string", "method": "generate" } } } }
```

### Exam Trap ⚠️

<div class="note-trap"><strong>Extract is document-only</strong>; image fields use generate or classify.</div>

### Go deeper

- [Content Understanding image overview](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/image/overview)

---

## 2.14 Extract information from audio and video by using Content Understanding

### Key Concept

**Audio and video analyzers return WebVTT transcripts, summaries, key frames and segments, plus your generate or classify fields.**

**A recording is a witness that tells its story over time.**

### Real use

A bank runs `prebuilt-callCenter` on support calls for sentiment and topics, and segments training videos so each chapter gets its own summary.

### How it works

- `prebuilt-audioSearch`: transcript and summary. `prebuilt-callCenter`: adds sentiment, topics, people and companies.
- Transcripts are **WebVTT** with diarization; video transcribes spoken words only (music and effects ignored) plus key frames.
- Enable segmentation with content categories so each section gets its own output; set `locales` for languages.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `prebuilt-audioSearch` | Transcript + summary | No call analytics |
| `prebuilt-callCenter` | Call recordings | Call-centre focus |
| Video with segmentation | Per-section output | Longer processing |
| Voice Live (2.7) | Live conversation | Not analysis of recordings |

### Exam Trap ⚠️

<div class="note-trap">Transcripts are WebVTT, not SSML, and music cues don't become chapter markers.</div>

### Go deeper

- [Content Understanding audio overview](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/audio/overview)
- [Content Understanding video overview](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/video/overview)

---

## 2.15 Build a lightweight application with information extraction capabilities by using Content Understanding

### Key Concept

**Analysis is asynchronous: start it, wait or poll, then read the fields and their confidence.**

**It's a coat check: hand it in, get a ticket, come back later.**

### Real use

A clinic sends voicemails to a custom audio analyzer overnight; high-confidence callback requests go to the booking system and the rest to a receptionist.

### How it works

- SDK `azure-ai-contentunderstanding`: `begin_analyze(...)` returns a poller; `.result()` waits; fields are on `result.contents`.
- REST analyze returns **202 Accepted** with an **Operation-Location** header; poll it until `Succeeded`.
- Enable `estimateFieldSourceAndConfidence`, and send fields below a confidence threshold to human review.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Foundry portal CU page | Trying analyzers, no code | Not an app |
| Python SDK | Python app | Package install |
| REST | Any language | You write the polling |

### How to do it

```python
client = ContentUnderstandingClient(endpoint=endpoint, credential=AzureKeyCredential(key))
poller = client.begin_analyze(analyzer_id="prebuilt-invoice", inputs=[{"url": invoice_url}])
result = poller.result()
for content in result.contents:
    print(content.fields)
```

1. Enable confidence in the analyzer.
2. Route low-confidence fields to a person.
3. Over REST, poll Operation-Location; never re-POST.

### Exam Trap ⚠️

<div class="note-trap">A 202 with no fields is success: poll Operation-Location, don't repeat the POST.</div>

### Go deeper

- [Quickstart: Content Understanding REST API](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/quickstart/use-rest-api)

---

## Deep Dive: Making Microsoft Foundry Click

Pick a capability per requirement: a model deployment, an agent when tools are needed, or a Foundry Tool (Language, Speech, Content Understanding) when a purpose-built service is more reliable. Timing is the other split: chat, Language and Speech return at once; video, batch transcription and Content Understanding are asynchronous.

> **Worked scenario.** Fabrikam wants a support agent over 40 PDF manuals that reads photos of damaged gear and logs order number, purchase date and fault description for warranty claims. Some customers phone in.
>
> **Model and agent (2.2, 2.4).** Deploy a vision-capable model as `support-chat`, test the grounded system prompt in the playground, save as an agent with **file search**, and publish.
>
> **Client (2.5, 2.9).** The site calls the agent with `DefaultAzureCredential` and a conversation per visitor, sending photos as base64 `input_image` parts.
>
> **Extraction (2.12, 2.14, 2.15).** A document analyzer *extracts* OrderNumber and PurchaseDate and *generates* FaultDescription. Phoned-in claims use an audio analyzer with generate fields, and low-confidence values go to a person.

**Memory aids.** **E-A-R-R**: Endpoint · Authenticate · Request shape · Read the response. For Content Understanding: **Copy, Choose, Compose** = extract, classify, generate.

---

## Cheat Sheet 📋

| Task | Service / SDK | Key call or setting |
|---|---|---|
| 2.1 | Prompts | Rules in system prompt; grounding with "I don't know" |
| 2.2 | Foundry portal | Deployment name, type, TPM; 429 = raise TPM |
| 2.3 | `azure-ai-projects` | `responses.create(model=<deployment name>)` → `output_text` |
| 2.4 | Agent Service | File search, code interpreter, web search; publish = stable endpoint |
| 2.5 | Responses API | Agent reference + conversation + Entra ID |
| 2.6 | `azure-ai-textanalytics` | `detect_language([text])[0]`; `redacted_text` |
| 2.7 | Audio model / Voice Live | `input_audio` base64; modalities text + audio |
| 2.8 | `azure-cognitiveservices-speech` | once vs continuous; `speak_text_async`; batch for archives |
| 2.9 | Vision model | `input_image` / `image_url`; base64 for private; `detail: high` |
| 2.10 | GPT-image / Sora | decode `b64_json`; video = job, poll, download |
| 2.11 | Vision app | Photo + instruction in one request; Image Analysis deprecated |
| 2.12 | CU documents | Prebuilt or custom; extract/classify/generate; enable confidence |
| 2.13 | CU images | `prebuilt-image`; generate/classify only |
| 2.14 | CU audio/video | audioSearch, callCenter; WebVTT; segmentation |
| 2.15 | CU app | `begin_analyze().result()`; 202 + poll Operation-Location |
