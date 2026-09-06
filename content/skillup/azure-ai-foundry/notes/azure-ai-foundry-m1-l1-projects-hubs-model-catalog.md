# Projects, Hubs & the Model Catalog

> **Skill track**: Azure AI Foundry Practitioner — Module 1, Lesson 1

## Overview

Azure AI Foundry is Microsoft's unified platform for discovering, deploying, customizing, and orchestrating generative AI models and agents. This lesson covers the platform's structural building blocks — hubs, projects, and the model catalog — the foundation everything else in this track builds on.

> 💡 **Human Angle**: *Think of the model catalog as a car showroom and the deployment type as how you pay for the car — lease it by the mile (serverless/pay-per-token), buy it outright and park it in your garage (managed compute), or reserve a dedicated lane on the highway (provisioned throughput).*

## Foundry Projects vs. Hubs

| Concept | What it is | When to use |
|---|---|---|
| Foundry project (Azure AI Foundry resource) | A single, unified project with simplified default networking/identity | Recommended default for new, single-team projects |
| Hub-based project | A project that inherits shared connections, compute, and security boundaries from a parent hub | Multiple teams/projects need consistent shared governance |

### Common Pitfall ⚠️

<div class="note-trap">
Don't assume hub-based projects are "legacy" or being removed — they're still the right choice when several product teams must share the same connections, compute, and network/security posture. Pick the right structure for the *scenario*, not a blanket "always use the newer one" rule.
</div>

## Model Catalog

The model catalog is the central hub for browsing models across providers: Azure OpenAI, Microsoft (Phi family), Meta (Llama), Mistral, Cohere, DeepSeek, xAI, and more — each with benchmarks, licensing terms, and supported deployment options listed on its model card.

| Feature | Purpose |
|---|---|
| Benchmarks | Compare quality, cost, and latency/throughput across models before choosing one |
| License info | Understand usage rights per model family (varies — some commercial, some open-weight) |
| Deployment options per model | Not every model supports every deployment type — check the model card |

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Recommended new-project default | Foundry project (Azure AI Foundry resource) |
| Hub's job | Shared connections/compute/security across multiple projects |
| Model catalog benchmarks | Compare quality/cost/latency before choosing a model |
