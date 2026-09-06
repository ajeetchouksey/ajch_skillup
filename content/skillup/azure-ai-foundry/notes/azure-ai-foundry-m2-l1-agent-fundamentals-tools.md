# Agent Service Fundamentals & Built-in Tools

> **Skill track**: Azure AI Foundry Practitioner — Module 2, Lesson 1

## Overview

This lesson covers the Azure AI Foundry **Agent Service** — its core conversation objects and built-in tools, the pieces you compose before reaching for multi-agent orchestration.

> 💡 **Human Angle**: *A well-tooled single agent is like one very capable generalist employee — give it the right set of tools before assuming it needs a whole team.*

## Core Conversation Objects

| Object | Role |
|---|---|
| Agent | The configured persona: instructions (system prompt), model, and enabled tools |
| Thread | A persistent conversation — stores the ordered message history server-side |
| Message | One turn within a thread |
| Run | One execution of the agent against a thread's messages |

Editing an agent's **instructions** changes its tone/behavior immediately on the next run — no redeployment or retraining needed.

## Built-in Tools

| Tool | What it does | Not to be confused with |
|---|---|---|
| Code interpreter | Executes Python in a sandbox — data analysis, calculations, chart generation | File search (retrieval, not execution) |
| File search | Retrieves grounded passages from an uploaded document vector store, with citations | Code interpreter |
| Function calling | Model decides when to invoke a developer-defined function with structured (JSON-schema) arguments | OpenAPI tool |
| OpenAPI tool | Agent calls an external REST API directly from a published OpenAPI 3.0 spec (anonymous / API-key / managed-identity auth) | Function calling (which needs a hand-written wrapper per function) |
| Bing grounding | Grounds answers in live web search results (via a Grounding with Bing Search resource) — for time-sensitive info | File search (only searches your own uploaded docs) |
| Fabric data agent | Queries structured data already modeled in Microsoft Fabric, without re-exporting it | File search (unstructured documents) |

### Common Pitfall ⚠️

<div class="note-trap">
"Which tool lets the agent call an internal REST API?" has *two* plausible-looking answers: Function calling and the OpenAPI tool. The distinguishing detail: OpenAPI tool works directly from an existing OpenAPI 3.0 spec with no per-endpoint wrapper code; function calling requires you to define each function's schema by hand. Look for "already has a published spec" vs. "one specific action" to pick correctly.
</div>

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Conversation objects | Agent, Thread, Message, Run |
| Code interpreter | Executes Python (analysis, charts) |
| File search | Retrieval + citation over uploaded docs |
| Function calling | Model fills args for a hand-defined function |
| OpenAPI tool | Calls an API directly from its spec, no wrapper needed |
| Bing grounding | Live web search grounding |
| Fabric data agent | Query structured Fabric data directly |
| Change agent tone/rules | Edit instructions, no redeploy needed |
