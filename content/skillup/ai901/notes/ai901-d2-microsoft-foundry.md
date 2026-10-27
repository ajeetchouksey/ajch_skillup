# D2: Implement AI solutions by using Microsoft Foundry

> **Exam weight**: 55–60% · **Skills measured as of**: April 15, 2026

## Overview

Domain 2 is the hands-on half of AI-901 and the heavier one. It asks you to build the workloads from Domain 1 in Microsoft Foundry: write system and user prompts, deploy and test a model in the portal, call it from a small Python client with the Foundry SDK, build and call a single agent, and build lightweight apps for text analysis, speech, vision, image generation and information extraction with Azure Content Understanding. The study guide expects you to read short Python snippets and know which SDK, client and method each task uses.

> 💡 **Human Angle**: Almost every app in this domain follows the same four beats: get an endpoint, authenticate, send a request in the right shape, read the right property of the response. Learn the beats once and each new service is just new names.

<div class="note-scribble"><strong>Code note.</strong> The snippets here follow Microsoft Learn's AI-901 training modules and the current Foundry docs (checked October 2026). The SDKs are moving fast: the Foundry SDK is <code>azure-ai-projects</code> 2.x, and Microsoft's samples differ slightly in how they reference an agent. The exam tests the pattern (which client, which call, which property), not exact version numbers.</div>

---

## 2.1 Foundry Resource, Project and Portal Workflow

### Key Concept

**One Foundry resource holds the shared platform; each Foundry project inside it is a workspace for one solution.**

The **Foundry resource** is the Azure resource that provides models, the agent service, quotas, governance, monitoring and security boundaries. A **Foundry project** is a workspace inside it where you build agents, run evaluations and keep files, datasets, indexes and connections. The documented pattern is one resource per team with many projects inside it.

The portal workflow is the same for every solution: create a project, pick a model from the **model catalog** and deploy it, experiment in the **playground**, then call the deployment from a client app. In Foundry terms, the model deployment is the server and your app is the client. **The resource is the office building; each project is a team's floor, with its own desks and filing cabinets.**

![Microsoft Foundry flow: a Foundry resource contains projects; in a project you deploy a model from the catalog, test it in the playground, optionally save it as an agent with tools, then call the deployment or agent from a client app through the project endpoint.](/content/skillup/ai901/images/ai901-d2-foundry-flow.svg)

Two endpoints appear in code. The **project endpoint**, `https://<resource>.services.ai.azure.com/api/projects/<project>`, is what `AIProjectClient` uses. The **OpenAI-compatible endpoint**, `https://<resource>.openai.azure.com/openai/v1`, is what the plain `OpenAI` client uses. Calls authenticate with an API key or a Microsoft Entra ID token.

### In Practice

**What breaks without this**: teams create a new resource for every app and end up with scattered quotas and security settings, or put three apps in one project and mix their agents and files together.

**Decision trigger**: shared governance and quota means the same resource; separate agents, files and evaluations means separate projects.

**When you'd choose differently**: a team with strict billing or regional isolation between apps may need separate resources. Hub-based projects are the older model and only appear in the classic portal.

### Exam Trap ⚠️

<div class="note-trap">
The hierarchy is <strong>resource contains projects</strong>, never the other way round. And the endpoint is a URL while the key is a secret that authenticates calls to it; they are not the same thing.
</div>

---

## 2.2 System and User Prompts

### Key Concept

**The system prompt sets the rules for the whole conversation; the user prompt is the request.**

A **system prompt** (system instructions) defines role, tone, scope, output format and guardrails, for example: "You are a support assistant for Contoso. Only answer about Contoso products. If the answer isn't in the provided text, say you don't know." The application controls it. A **user prompt** is what the end user asks.

Effective prompts are clear and specific, give context, show examples and ask for a structure. **Few-shot** examples guide the format for that request only; they do not retrain the model. **Grounding** puts source text into the prompt and tells the model to answer only from it, with an "out" ("say you don't know") and citations, which reduces fabrication. Models see only what is in each request, so chat apps resend the conversation history or use a service-side conversation. **The system prompt is the job description; the user prompt is today's task.**

### In Practice

**What breaks without this**: an app parses answers that arrive as bullets one day and JSON the next, or an HR bot invents policy because nothing in the prompt told it to stick to the handbook.

**Decision trigger**: if a rule must apply to every reply, it belongs in the system prompt. If the answer must be factual about your data, ground the prompt.

**When you'd choose differently**: reasoning models (such as the GPT-5 series) need fewer prompt tricks; Microsoft notes that techniques like chain-of-thought prompting are not recommended for them.

### Exam Trap ⚠️

<div class="note-trap">
"Add 'always be accurate' and raise the temperature" is never the answer to fabrication. Accuracy comes from grounding the prompt with the facts; a higher temperature makes invention more likely.
</div>

---

## 2.3 Deploy a Model and Use the Playground

### Key Concept

**Deploying a model creates a named endpoint with fixed settings and a rate limit; the playground is where you test it before writing code.**

When you deploy, you choose the **deployment name**, the **deployment type** (for example Global Standard), the **model version** and a **tokens-per-minute (TPM)** rate limit. Deployment allocates capacity, fixes the configuration and creates the endpoint that apps call by deployment name. It does not train the model or give you its weights.

The **model playground** lets you write system instructions, adjust parameters (temperature, max output tokens), add tools, compare up to three models side by side, export code and **save the setup as an agent**. If requests start failing with HTTP 429, the deployment has hit its rate limit: raise TPM within your quota, or reduce max tokens and concurrent requests. **The deployment is the phone line; the playground is the test call before you print the number on the website.**

### In Practice

**What breaks without this**: a team writes code against a model it never tested, then discovers the format, tone or speed is wrong after integration.

**Decision trigger**: before any code, ask whether the prompt and settings already produce the answers you want in the playground.

**When you'd choose differently**: for large offline jobs, testing a few samples interactively and then running a Batch deployment is cheaper than calling a standard deployment millions of times.

### Exam Trap ⚠️

<div class="note-trap">
429 errors are a capacity problem, not a model problem. Temperature changes nothing here, and a Developer deployment is for evaluating fine-tuned models, not a way round rate limits.
</div>

---

## 2.4 A Chat Client with the Foundry SDK

### Key Concept

**`AIProjectClient` connects to the project; `get_openai_client()` gives an OpenAI-compatible client that calls the model.**

The Foundry SDK for Python is `azure-ai-projects`. You create an `AIProjectClient` with the project endpoint and a credential, usually `DefaultAzureCredential` from `azure-identity` (sign in with `az login` first). From it you get an OpenAI-compatible client and call the **Responses API**, passing the **deployment name** as `model`, and read `output_text`.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential())
openai = project.get_openai_client()

response = openai.responses.create(
    model="support-chat",            # the deployment name
    input=[{"role": "system", "content": "You're a helpful assistant."},
           {"role": "user", "content": "What can you help me with?"}])
print(response.output_text)
```

Microsoft's module also shows the plain `OpenAI` client with the OpenAI-compatible endpoint and an API key, and parameters such as `max_output_tokens` and `temperature`. Either way the request shape is the same. **The project client is the receptionist; the OpenAI client is the person you are put through to.**

### In Practice

**What breaks without this**: code passes the base model name ("gpt-4.1-mini") when the deployment is called "support-chat" and fails with deployment-not-found, or `DefaultAzureCredential` fails because nobody signed in.

**Decision trigger**: authentication error means check identity and sign-in; not-found error means check the deployment name.

**When you'd choose differently**: Chat Completions (`chat.completions.create` with `messages`, reading `choices[0].message.content`) also works and appears in many samples; the Responses API is the one Foundry's newer SDK and agents are built on.

### Exam Trap ⚠️

<div class="note-trap">
<code>model=</code> takes the <strong>deployment name</strong>, not the model family. And <code>DefaultAzureCredential</code> is the Entra ID route; it does not take an API key.
</div>

---

## 2.5 Create and Test a Single Agent in the Portal

### Key Concept

**An agent is a model plus instructions plus tools; tools are actions and knowledge is context.**

In the Foundry portal you create an agent (Build > Agents, or "Save as agent" from the playground), choose a model deployment, write the **instructions**, and add **tools**. Built-in tools include **file search** (upload files; they are indexed into a vector store so the agent can ground answers and cite them), **code interpreter** (runs Python in a sandbox for calculations, data analysis and charts), and **web search** (current public information). Custom tools can be functions, OpenAPI specs or MCP servers.

Test the agent in the **agents playground** with realistic and tricky questions and check its responses and tool calls. When it behaves, **publish** it: publishing turns it into a managed Azure resource with a stable endpoint that apps and channels such as Microsoft Teams can use. **Instructions are the job description, tools are the toolbox, and knowledge is the reference library on the shelf.**

| Need | Tool |
|---|---|
| Answer from the company's own documents, with citations | File search |
| Calculate from a CSV, draw a chart | Code interpreter |
| Current public information | Web search |
| Call Azure Language (PII, language detection) | Azure Language MCP server |

### In Practice

**What breaks without this**: an agent asked about product manuals answers from general knowledge because nobody added file search, or a finance agent "calculates" growth rates by predicting digits because it has no code interpreter.

**Decision trigger**: does the agent need to *do* something (tool) or *know* something specific (knowledge)?

**When you'd choose differently**: if no tools or knowledge are needed, a plain model deployment with a good system prompt is simpler than an agent.

### Exam Trap ⚠️

<div class="note-trap">
File search and web search are easy to swap. <strong>Private uploaded documents = file search</strong>; <strong>public, current information = web search</strong>. Neither runs calculations; that is code interpreter.
</div>

---

## 2.6 A Client Application for an Agent

### Key Concept

**Apps call a Foundry agent through the Responses API with an agent reference, authenticated with Microsoft Entra ID.**

The client uses `AIProjectClient` with `DefaultAzureCredential`, gets the OpenAI-compatible client and calls `responses.create`, identifying the agent rather than a model. Microsoft's training shows this form:

```python
agent = project_client.agents.get(agent_name="learning-agent")
openai_client = project_client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}})
print(response.output_text)
```

For multi-turn chat, create a **conversation** and pass its ID with each request so the service keeps the history. The current Agent Service uses **conversations, items, responses and agent versions**; the older Assistants API concepts (threads, messages, runs) are retired. Microsoft's exercise notes that key-based authentication is not supported for this agent code, so sign in with an Entra ID identity. **The agent reference is the name badge on the request: it tells Foundry which agent should answer.**

### In Practice

**What breaks without this**: a developer copies an old Assistants tutorial with threads and runs, or swaps `DefaultAzureCredential` for an API key and every call fails.

**Decision trigger**: if the code talks to an agent, look for `responses.create` plus an agent reference, and an Entra ID credential.

**When you'd choose differently**: Microsoft's samples vary in the exact agent-reference syntax (for example `get_openai_client(agent_name=...)` in newer quickstarts). The pattern is the same: Responses API, agent named, conversation for history.

### Exam Trap ⚠️

<div class="note-trap">
Threads, runs and assistants are the old vocabulary. If an answer option uses <code>threads.runs.create</code>, it is describing the retired Assistants API, not the current Foundry Agent Service.
</div>

---

## 2.7 Text Analysis Apps

### Key Concept

**Use a general model for flexible text tasks and Azure Language when the app needs consistent, structured values.**

Foundry gives you two routes. A general-purpose model, prompted well, can extract key phrases, link entities, assess sentiment and summarise, but its output varies between calls. **Azure Language in Foundry Tools** returns structured, deterministic results, such as a language code with a confidence score or redacted text, which is what automated workflows need.

The Language SDK is `azure-ai-textanalytics`. Create a `TextAnalyticsClient` with the endpoint and an `AzureKeyCredential`, and pass a **list** of documents to each method: `detect_language([text])[0]` returns `primary_language` (name, ISO code, confidence score), and `recognize_pii_entities([text])[0]` returns `redacted_text` and the entities found. Agents can use Language through the **Azure Language MCP server** tool, connected with the Foundry resource name and no separate Language resource. **A chat model is a talented writer; Azure Language is a form that always comes back filled in the same way.**

### In Practice

**What breaks without this**: a workflow expects "es" and receives "It is Spanish", or a ticketing system stores unredacted phone numbers because the developer read `entities` instead of `redacted_text`.

**Decision trigger**: if downstream code parses the result, prefer Azure Language; if a person reads it, a model's flexible prose is often fine.

**When you'd choose differently**: for features Azure Language now marks as legacy (key phrases, sentiment, summarization), Microsoft directs new projects to Foundry models.

### Exam Trap ⚠️

<div class="note-trap">
<code>TextAnalyticsClient</code> methods take a <strong>list</strong> of documents and return a list of results, so a single string goes in as <code>[text]</code> and you read <code>[0]</code>.
</div>

---

## 2.8 Spoken Prompts and Azure Speech Apps

### Key Concept

**Send audio straight to an audio-capable model, or use Azure Speech in Foundry Tools to recognise and synthesise speech.**

To respond to a spoken prompt with one model, deploy a multimodal model that accepts audio (for example the gpt-audio models, the gpt-realtime family or Phi-4-multimodal-instruct). In Chat Completions the audio goes in an `input_audio` content part with base64 data and a format such as `wav`; to get spoken output too, request the text and audio modalities with a voice and format. For live voice agents, the **Voice Live API** is a fully managed, low-latency speech-to-speech service with noise suppression, interruption handling and end-of-turn detection.

For classic speech apps, the SDK is `azure-cognitiveservices-speech`. Create a `SpeechConfig` with the Foundry resource key and endpoint. **Recognition**: `SpeechRecognizer` with `recognize_once_async()` for one utterance (about 30 seconds), or `start_continuous_recognition()` with `recognized` event handlers for longer speech. **Synthesis**: set `speech_synthesis_voice_name`, create a `SpeechSynthesizer` and call `speak_text_async(text).get()`. Use **batch transcription** (files via SAS URIs, asynchronous, best-effort) for archives. **The multimodal model listens and thinks in one step; Azure Speech is the specialist ears and voice you wire to anything.**

```python
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription=key, endpoint=endpoint)
speech_config.speech_synthesis_voice_name = "en-US-Ava:DragonHDLatestNeural"
synth = speechsdk.SpeechSynthesizer(speech_config=speech_config,
    audio_config=speechsdk.audio.AudioOutputConfig(use_default_speaker=True))
result = synth.speak_text_async("Your order has shipped.").get()
```

### In Practice

**What breaks without this**: a dictation app built on `recognize_once_async()` keeps only the first sentence, or a team streams an archive of recordings through real-time recognition.

**Decision trigger**: live conversation means Voice Live or an audio-capable model; transcripts and narration mean Azure Speech; recorded archives mean batch.

**When you'd choose differently**: if the user's question must also drive tools and reasoning, a voice-enabled agent (Voice Live with a Foundry agent) is better than wiring recognition and synthesis by hand.

### Exam Trap ⚠️

<div class="note-trap">
Audio goes in an <code>input_audio</code> part as base64 data, not as an <code>image_url</code> or a file path in the prompt. And <code>speak_text_async</code> is synthesis, while <code>recognize_once_async</code> is recognition.
</div>

---

## 2.9 Visual Input to a Multimodal Model

### Key Concept

**Put an image and a text instruction in the same user message, and a vision-capable model answers about the image.**

Vision-enabled models (for example the GPT-4.1 and GPT-5 series) accept images as URLs or as base64-encoded data. In the **Responses API** the user content holds an `input_text` part and an `input_image` part; in **Chat Completions** it is an `image_url` part, optionally with a `detail` setting.

```python
response = client.responses.create(model=deployment, input=[{"role": "user", "content": [
    {"type": "input_text", "text": "What is in this image? Give 3 bullet points."},
    {"type": "input_image", "image_url": image_url}]}])
print(response.output_text)
```

Image URLs must be reachable by the service, so private images are sent as base64 data URLs. In Chat Completions, `detail: "low"` uses a 512x512 version (cheaper, less detail) and `"high"` lets the model read small text. **Sending an image is like handing someone a photo with a sticky note on it: the note is the question.**

### In Practice

**What breaks without this**: an app sends links to an internal file share the model cannot reach, or misreads a spec sheet because detail was set to low.

**Decision trigger**: is the image public? If not, base64 it. Does the task need fine print? Then use high detail.

**When you'd choose differently**: for repeatable structured fields from many images, a Content Understanding analyzer gives consistent JSON with confidence scores instead of free text.

### Exam Trap ⚠️

<div class="note-trap">
Responses API image parts are <code>input_image</code>; the <code>image_url</code> object with <code>url</code> and <code>detail</code> is the Chat Completions format. Both are correct for their own API.
</div>

---

## 2.10 Creating Visual Outputs and Vision Apps

### Key Concept

**Image models return base64 image data you decode and save; video models run as asynchronous jobs.**

For images, Microsoft recommends the **GPT-image** family. With `images.generate(model=..., prompt=..., size="1024x1024")`, GPT-image models always return base64 data in `data[0].b64_json`, which you decode and write to a file; the Responses API can also generate images through the `image_generation` tool. The older dall-e-3 model was retired on 4 March 2026. For video, **Sora** models create a job that you poll until it completes and then download, which can take minutes.

A lightweight vision app is usually just a vision-capable deployment plus a prompt, with no custom training. Be aware of retirements: Azure Vision Image Analysis 4.0 is deprecated (retiring 25 September 2028), Custom Vision is also retiring, and the Face service's emotion and gender capabilities were retired, with identity features (verification and identification) behind Limited Access. **Image generation is a vending machine that drops the picture straight out; video generation is a print shop where you collect the order later.**

### In Practice

**What breaks without this**: an app looks for an image URL that GPT-image models never return, or waits synchronously for a video that takes minutes.

**Decision trigger**: still image means decode base64 from the response; video means create, poll, download.

**When you'd choose differently**: when you need to edit part of an existing image, use the image edit operation with a mask rather than generating from scratch.

### Exam Trap ⚠️

<div class="note-trap">
Old tutorials mention dall-e-3, Image Analysis custom models and Face emotion detection. All three are retired; the right answers point to GPT-image models, multimodal models or Content Understanding.
</div>

---

## 2.11 Content Understanding: Analyzers for Documents and Forms

### Key Concept

**An analyzer takes content in, applies AI and a schema, and returns structured fields; prebuilt analyzers cover common documents.**

**Azure Content Understanding in Foundry Tools** is part of the Foundry resource. **Prebuilt analyzers** include `prebuilt-read` and `prebuilt-layout` (text, tables, structure), domain analyzers such as `prebuilt-invoice`, `prebuilt-receipt`, `prebuilt-idDocument` and `prebuilt-contract`, and search-oriented analyzers (`prebuilt-documentSearch`, `prebuilt-imageSearch`, `prebuilt-audioSearch`, `prebuilt-videoSearch`). A **custom analyzer** starts from a base (`prebuilt-document`, `prebuilt-image`, `prebuilt-audio` or `prebuilt-video`) and adds a **field schema**.

Each field has a type and a **method**: **extract** returns a value that appears in the content (documents only), **classify** picks from fixed categories, and **generate** writes a value such as a summary. **Confidence scores** (0 to 1) and **grounding** (where the value came from) are opt-in via `estimateFieldSourceAndConfidence`. Content Understanding uses *your* Foundry model deployments: most analyzers need a chat completion model and an embeddings model set as defaults, while `prebuilt-read` and `prebuilt-layout` need none. **An analyzer is a clerk with a form: the schema is the form, and extract, classify and generate are copy, tick-a-box and write-a-sentence.**

| Field | Method |
|---|---|
| Vendor name printed on the invoice | extract |
| Document category from a fixed list | classify |
| One-sentence summary | generate |

### In Practice

**What breaks without this**: the first `prebuilt-invoice` call fails because no model deployments are mapped, or a finance system loads every value with no idea which ones are uncertain.

**Decision trigger**: does the value appear on the page (extract), come from a fixed list (classify), or need writing (generate)?

**When you'd choose differently**: for highly standard forms, or on-premises needs, Azure Document Intelligence prebuilt models and containers remain an option; Microsoft says existing Document Intelligence users do not need to migrate.

### Exam Trap ⚠️

<div class="note-trap">
Confidence and grounding are <strong>not on by default</strong>, and <strong>extract only works for documents</strong>. Both facts make good distractors.
</div>

---

## 2.12 Content Understanding: Images, Audio and Video

### Key Concept

**Images, audio and video use generate and classify fields, and their outputs are descriptions, WebVTT transcripts, key frames and segments.**

**Images**: `prebuilt-imageSearch` returns a paragraph description, and a custom analyzer on `prebuilt-image` can return fields such as a stock level (classify) or an attendee count (generate). Image analyzers are not optimised for text-heavy images, so photographed receipts belong with a document analyzer such as `prebuilt-receipt`.

**Audio**: `prebuilt-audioSearch` gives a transcript and summary, and `prebuilt-callCenter` adds sentiment, topics, people and companies for call recordings. Transcripts are **WebVTT**, with diarization and speaker roles. **Video**: transcripts of spoken words (music and sound effects are ignored), **key frames**, and segment descriptions; turning on segmentation with content categories gives separate output per section. **Treat each modality like a different witness: the document hands you paperwork, the photo shows a scene, the recording tells a story over time.**

### In Practice

**What breaks without this**: an image analyzer fails because a field uses extract, or a team expects one description per chapter from a video analysed as a single segment.

**Decision trigger**: is the content mostly text? Use a document analyzer. Does it unfold over time? Use audio or video analyzers, and enable segmentation if you need per-section output.

**When you'd choose differently**: if you only need a live voice conversation, Voice Live fits better; Content Understanding analyses recordings after the fact.

### Exam Trap ⚠️

<div class="note-trap">
"Music cues become chapter markers" and "the transcript comes back as SSML" are both made-up distractors. Only spoken words are transcribed, and transcripts are WebVTT.
</div>

---

## 2.13 Building an Information Extraction App

### Key Concept

**Analysis is asynchronous: start it, wait or poll, then read the fields and their confidence.**

With the Python SDK (`azure-ai-contentunderstanding`), create a `ContentUnderstandingClient` with the Foundry endpoint and a credential, call `begin_analyze(analyzer_id=..., inputs=[{"url": ...}])`, and call `.result()` on the poller. The fields are on each item in `result.contents`, each with a type, a value (for example `valueString`, `valueDate`) and a confidence when enabled.

```python
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential
client = ContentUnderstandingClient(endpoint=endpoint, credential=AzureKeyCredential(key))
poller = client.begin_analyze(analyzer_id="prebuilt-invoice", inputs=[{"url": invoice_url}])
result = poller.result()
for content in result.contents:
    print(content.fields)
```

Over REST, `POST {endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01` with the `Ocp-Apim-Subscription-Key` header returns **202 Accepted** and an **Operation-Location** header; poll that URL until the status is `Succeeded`. A sensible app routes low-confidence fields to a person before they reach a system of record. **It is a coat check: you hand the content in, get a ticket, and come back for the result.**

### In Practice

**What breaks without this**: a client treats 202 as failure and re-posts, creating duplicate jobs and token costs, or loads blurry-invoice values straight into finance with no review.

**Decision trigger**: if a call returns a poller or a 202, there is a result to collect later.

**When you'd choose differently**: for a quick one-off, the Content Understanding page in the Foundry portal lets you run analyzers on sample files and view the code without writing an app.

### Exam Trap ⚠️

<div class="note-trap">
A 202 with no fields is success, not failure. The answer is always "poll Operation-Location", never "repeat the POST".
</div>

---

## Deep Dive: Making Microsoft Foundry Click

### 1. The connective narrative

Foundry is one platform with one shape. A **Foundry resource** holds models, tools and governance; **projects** hold your work. Inside a project you choose a capability: a **model deployment** for generation and multimodal understanding, an **agent** when the model needs tools and knowledge, or a **Foundry Tool** (Azure Language, Azure Speech, Content Understanding) when a purpose-built service does the job more reliably. The portal is where you try each one, and the SDKs are how your app calls them.

Every client follows the same four beats. **Endpoint**: the project endpoint for `AIProjectClient`, the OpenAI-compatible endpoint for `OpenAI`, or the resource endpoint for Speech, Language and Content Understanding. **Authenticate**: Entra ID through `DefaultAzureCredential`, or a key where the service supports it. **Request shape**: messages with text, `input_image` or `input_audio` parts; a list of documents for Language; a `SpeechConfig` for Speech; an analyzer ID and inputs for Content Understanding. **Read the response**: `output_text`, `redacted_text`, a speech result reason, `b64_json`, or `contents[].fields`.

What changes between services is timing. Chat, Language and Speech calls return at once. Image generation returns base64 straight away. Video generation, batch transcription and Content Understanding are asynchronous: you start a job and collect the result later. Once you know which group a service falls into, most "what should the code do next?" questions answer themselves.

### 2. Worked scenario

> **Scenario.** Fabrikam Outdoor wants a support agent for its website. It must answer questions from 40 PDF product manuals, read photos customers upload of damaged gear, and log each warranty claim's order number, purchase date and fault description into a database. Customers sometimes phone in instead.
>
> **Step 1, project and model.** Create a Foundry project in the team's existing resource and deploy a vision-capable chat model (Global Standard is fine; there is no data-residency rule) with the deployment name `support-chat`. Test the system prompt in the playground: "Answer only from the manuals; if the answer isn't there, say so and offer a human."
>
> **Step 2, agent.** Save it as an agent and add **file search** with the 40 manuals, so answers are grounded and cited. No code interpreter is needed because there are no calculations. Test tricky questions in the agents playground, then publish.
>
> **Step 3, client.** The website calls the agent with `AIProjectClient` and `DefaultAzureCredential` (a managed identity in production), `responses.create` with the agent reference, and a **conversation** so follow-up questions keep context. Photos go in as `input_image` parts, base64-encoded because they are uploaded rather than public.
>
> **Step 4, extraction.** Warranty claims are documents and calls, and the requirement names fields, so it is Content Understanding. A custom document analyzer *extracts* OrderNumber and PurchaseDate and *generates* FaultDescription; phoned-in claims use an audio analyzer with *generate* fields, because extract is document-only. Confidence is switched on, and anything under the team's threshold goes to a person.
>
> **Outcome.** Four services, one project, and every choice traced to a requirement: grounded answers (file search), image understanding (multimodal input), structured claims (Content Understanding), and human review for low confidence (reliability and accountability).

### 3. Memory aid

**"E-A-R-R"** for every client in this domain: **E**ndpoint · **A**uthenticate · **R**equest shape · **R**ead the response. If you can fill in those four for a service, you can answer its code questions.

For Content Understanding field methods, **"Copy, Choose, Compose"**: **extract** copies a value from the document, **classify** chooses from a list, **generate** composes new text.

### 4. Exam strategy for this domain

- Retired vocabulary is the main distractor source: Azure AI Studio, hub projects, the Assistants API's threads and runs, dall-e-3, Face emotion detection, Image Analysis custom models. Prefer answers using current names.
- Look-alike API details: deployment name vs model name, `input_image` vs `image_url`, `recognize_once_async` vs continuous recognition, extract vs generate, file search vs web search.
- The exam rewards testing in the playground before coding, grounding over "be accurate" instructions, structured tools when output feeds automation, and human review for low-confidence results.
- Five minutes before the exam: **for any code question, find the endpoint, the credential, the request shape and the property being read; the wrong options usually get one of those four wrong.**

---

## Cheat Sheet 📋

| Task | Service / SDK | Key call or setting |
|---|---|---|
| Connect to a project | `azure-ai-projects` | `AIProjectClient(endpoint, DefaultAzureCredential())` |
| Chat with a model | OpenAI-compatible client | `responses.create(model=<deployment name>, input=...)` then `output_text` |
| Call an agent | Responses API | agent reference in the request; conversation for multi-turn |
| Agent tools | Foundry Agent Service | file search (own docs), code interpreter (calculations), web search (public, current) |
| Language detection / PII | `azure-ai-textanalytics` | `detect_language([text])`, `recognize_pii_entities([text])` then `redacted_text` |
| Speech to text | `azure-cognitiveservices-speech` | `recognize_once_async()` (short) or `start_continuous_recognition()` (long) |
| Text to speech | Speech SDK | `speech_synthesis_voice_name`, `speak_text_async(text).get()`, SSML for fine control |
| Spoken prompt to a model | Audio-capable model | `input_audio` part with base64 data and format |
| Live voice agent | Voice Live API | Managed speech-to-speech, low latency |
| Image in a prompt | Vision-capable model | `input_image` (Responses) or `image_url` (Chat Completions) |
| Generate an image | GPT-image model | decode `data[0].b64_json` |
| Generate a video | Sora | create job, poll, download |
| Extract fields | `azure-ai-contentunderstanding` | `begin_analyze(...).result()` then `contents[].fields` |
| CU over REST | REST | 202 + Operation-Location, poll until `Succeeded` |
| CU field methods | Analyzer schema | extract (documents only), classify, generate |
