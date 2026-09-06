# Deployment Options, SDKs & Prompt Flow

> **Skill track**: Azure AI Foundry Practitioner — Module 1, Lesson 2
> **Try it**: pairs with the hands-on mission "Deploy Your First Prompt Flow in Azure AI Foundry"

## Deployment Options

| Option | Compute model | Billing | Best for |
|---|---|---|---|
| Serverless API (MaaS) | Microsoft-managed, no customer infra | Pay-per-token | Fast start, variable/low volume, many catalog models (Meta, Mistral, Cohere, etc.) |
| Managed compute | Dedicated VM-backed online endpoint | Pay for VM regardless of usage | Need more control over hardware; broader open-model support |
| Azure OpenAI — Standard / Global Standard | Shared, pay-as-you-go capacity | Per-token, variable latency under load | General-purpose Azure OpenAI usage |
| Azure OpenAI — Provisioned (PTU) | Reserved, dedicated capacity | Reserved-unit commitment | Latency-sensitive production workloads needing predictable throughput |
| Azure OpenAI — Global Batch | Asynchronous, 24-hour window | Discounted per-token | Large, non-latency-sensitive batch jobs |

### Common Pitfall ⚠️

<div class="note-trap">
Serverless API availability is *region- and model-specific* — a newly released catalog model may only support managed compute at first, or only be available in a subset of regions. "It's in the catalog" doesn't mean "it's deployable everywhere, every way, immediately."
</div>

## Connections & SDKs

- **Connections** link a project/hub to external resources it needs — most commonly Azure AI Search (for RAG), Azure Storage, Key Vault, and Application Insights.
- **SDKs**: `azure-ai-projects` is the *management-plane* SDK (list connections, deployments, agents, datasets). `azure-ai-inference` (or the OpenAI SDK pointed at a Foundry endpoint) is the *data-plane* SDK for actual inference calls (chat completions, embeddings). Don't confuse the two.

## Fine-Tuning

Training data must be a **JSONL** file, one JSON object per line, each with a `messages` array of role/content pairs (matching the chat-completion format). A fine-tuned model becomes its own custom deployment with separate hosting and usage billing.

## Quota

Azure OpenAI quota is enforced per deployment along two dimensions: **tokens-per-minute (TPM)** and **requests-per-minute (RPM)**. Quota can be split across multiple deployments within a subscription's overall limits.

## Playground & Prompt Flow

| Tool | Purpose |
|---|---|
| Chat playground | Fast, code-free iteration on system message, parameters, and few-shot examples |
| Prompt flow | Visual DAG-based tool for chaining retrieval/prompt/code/LLM nodes, bulk-testing against a dataset, and deploying the chain as a managed endpoint |

### Common Pitfall ⚠️

<div class="note-trap">
Content filters on Azure OpenAI deployments are **on by default** and are *not* a self-service toggle to disable — modifying or disabling them (e.g., for an approved red-teaming exercise) requires applying through Microsoft's **Limited Access** review process.
</div>

## Worked Example: Picking a Deployment Option

Contoso Retail wants to add an AI support chatbot backed by Llama-3.1-70B from the catalog. Traffic is spiky — quiet most of the day, then a burst up to ~50 requests/minute during evening promos — and the team has no appetite for managing VMs.

Walking the decision:

1. **Check the model card first.** Not every catalog model supports every deployment type, and support is region-specific — Llama-3.1-70B's card confirms Serverless API availability in Contoso's region. Skipping this step is the #1 way to pick an unavailable option in practice.
2. **Match the traffic pattern to a billing model.** Spiky, unpredictable volume with no infrastructure team is the textbook case for **Serverless API (MaaS)** — pay-per-token, Microsoft-managed compute, scales with demand automatically. Managed compute would mean paying for a dedicated VM around the clock even during quiet hours; PTU's reserved-capacity commitment doesn't fit unpredictable spiky load either.
3. **Wire up the right SDK for the job.** Actual chat completion calls at runtime go through the **data-plane** SDK (`azure-ai-inference`, or the OpenAI SDK pointed at the Foundry endpoint). If Contoso later needs to programmatically list or manage deployments/connections (e.g., an internal admin dashboard), that's the **management-plane** SDK (`azure-ai-projects`) — a different job entirely.

```python
# Data-plane call: azure-ai-inference (chat completion against the deployed endpoint)
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://contoso-foundry.services.ai.azure.com/models",
    credential=AzureKeyCredential("<key>"),
)
response = client.complete(
    model="Llama-3.1-70B-Instruct",
    messages=[{"role": "user", "content": "Where is my order #4821?"}],
)
```

**Contrast case**: if Contoso instead ran a trading-desk assistant needing guaranteed, consistent sub-second latency regardless of load, the right call flips to **Provisioned throughput (PTU)** — the deciding factor is a *predictability* requirement, not raw volume.

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Serverless API | Pay-per-token, no customer-managed compute |
| Managed compute | Dedicated VM, pay regardless of usage |
| PTU | Reserved capacity, predictable latency |
| Global Batch | Async, 24-hour window, discounted |
| azure-ai-projects | Management plane (connections, deployments, agents) |
| azure-ai-inference | Data plane (chat/embeddings calls) |
| Fine-tune data format | JSONL, `messages` array |
| Quota dimensions | TPM + RPM |
| Content filters | On by default; disabling needs Limited Access approval |
