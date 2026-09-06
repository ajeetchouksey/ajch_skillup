# Multi-Agent Orchestration & RAG

> **Skill track**: Azure AI Foundry Practitioner — Module 2, Lesson 2

## Multi-Agent Orchestration

| Pattern | Description |
|---|---|
| Connected agents | One Agent Service agent registers another agent as a callable tool — coordinator/specialist pattern, all within the Agent Service |
| Semantic Kernel | Microsoft SDK exposing existing app code as "plugins" the model can call; strong DI/.NET-Python-Java support |
| AutoGen | Microsoft framework for orchestrating multi-round conversations *among* multiple autonomous agents (planner/researcher/critic-style workflows) |

### Common Pitfall ⚠️

<div class="note-trap">
Multi-agent design is justified by **task decomposition into distinct specialist roles** (different instructions/tools/guardrails per role) — not by a desire to minimize API calls, cut cost, or because "more agents sounds more advanced."
</div>

## RAG Beyond File Search

Building a *custom* RAG pipeline (outside the File search tool) requires: **chunking** documents into retrieval-sized passages, then generating **vector embeddings** for each chunk, indexed in Azure AI Search for vector/hybrid similarity search at query time.

## Streaming

Streaming delivers run output incrementally (token-by-token / event-by-event) to the client, enabling a typewriter-style UI instead of waiting for the full completion — a delivery-layer concern, unrelated to tools or safety.

## Worked Example: Choosing Tools and an Orchestration Pattern

A support team wants one assistant that can: (a) answer questions from an uploaded 40-page policy PDF, (b) look up a customer's live order status via an internal REST API that already has a published OpenAPI 3.0 spec, and (c) hand off complex billing disputes to a specialist that reasons more carefully about refund policy.

Walking the tool/pattern choice for each requirement:

1. **(a) Policy Q&A over an uploaded PDF → File search.** This is grounded retrieval with citations over a document the team controls — exactly File search's job. Bing grounding would be wrong here (it searches the live web, not your own uploaded document), and Code interpreter would be wrong too (it executes Python, it doesn't retrieve text).
2. **(b) Order lookup via an existing REST API → OpenAPI tool, not Function calling.** The distinguishing detail is that a spec *already exists* — the OpenAPI tool consumes it directly with no per-endpoint wrapper code. Function calling would require hand-writing a JSON-schema function definition for this one action; reach for it when there's no existing spec, or the "function" is really custom logic (e.g., a calculation) rather than a real HTTP endpoint.
3. **(c) Escalate to a billing specialist → Connected agents, not AutoGen.** This is a coordinator delegating one specific, bounded task to a specialist with different instructions/guardrails — precisely the connected-agents pattern (register the billing agent as a callable tool on the coordinator). AutoGen is for open-ended, multi-round conversations *among* peer autonomous agents (e.g., a planner/researcher/critic loop) — reaching for it here would be over-engineering a simple delegation.

```json
// Simplified agent definition showing tool composition for requirements (a) and (b)
{
  "name": "SupportCoordinator",
  "instructions": "Answer policy questions from the knowledge base. For order status, call the Orders API. Escalate billing disputes to BillingSpecialistAgent.",
  "model": "gpt-4o",
  "tools": [
    { "type": "file_search", "vector_store_ids": ["vs_policy_docs"] },
    { "type": "openapi", "spec_url": "https://internal.contoso.com/orders/openapi.json", "auth": "managed_identity" }
  ]
}
```

**Common gotcha to notice**: nothing above required AutoGen or Semantic Kernel — most real support-bot scenarios resolve with File search + OpenAPI tool + (at most) connected agents. Reach for the heavier orchestration frameworks only when the scenario actually describes autonomous multi-agent reasoning, not just "the agent uses several tools."

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Connected agents | Agent-as-a-tool-for-another-agent |
| Semantic Kernel | Plugin-style code integration, DI-friendly |
| AutoGen | Multi-agent conversational orchestration |
| Custom RAG steps | Chunk → embed → index (Azure AI Search) |
