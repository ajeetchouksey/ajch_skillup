# Security, Privacy & Operations

> **Skill track**: Azure AI Foundry Practitioner — Module 3, Lesson 2

## Security

| Control | Purpose |
|---|---|
| Managed identity | Authenticate to Foundry/Azure OpenAI via Microsoft Entra ID — no stored secret to leak or rotate |
| RBAC / least privilege | Assign scoped roles (e.g., Azure AI Developer) rather than broad ones (Owner) — least privilege still applies inside Foundry |
| Private endpoints | Disable public network access; keep hub/project traffic off the public internet |
| Customer-managed keys (CMK) | Customer controls the Key Vault-backed encryption key for data at rest, including rotation |

### Common Pitfall ⚠️

<div class="note-trap">
"IP allow-listing" is *not* the same as disabling public network access — it still exposes a public endpoint, just a restricted one. When compliance requires the resource to be unreachable from the public internet at all, the answer is private endpoints + disabling public network access, not allow-listing.
</div>

## Data Use & Privacy

Microsoft's stated policy: customer prompts/completions sent to Azure OpenAI/Azure AI Foundry are **not** used to retrain or improve the shared base models and remain isolated to the customer's own resource. A separate, limited **abuse-monitoring** process may briefly retain data for safety purposes; eligible customers can apply for **modified abuse monitoring** through a formal Limited Access review — this is not a self-service toggle either.

## Operations

| Capability | Purpose |
|---|---|
| Tracing (OpenTelemetry → Application Insights) | End-to-end trace of tool calls, retrieval steps, and model calls within a specific run |
| Azure Monitor | Production metrics: token usage, latency, error rate, alerting |

## The Responsible AI Lifecycle: Identify → Measure → Mitigate → Operate

Microsoft frames responsible AI as four ongoing stages, applied iteratively (not a one-time pre-launch checklist):
1. **Identify** potential harms for the specific use case
2. **Measure** their frequency/severity (evaluations, red-teaming)
3. **Mitigate** them (content filters, system prompt design, grounding/RAG)
4. **Operate** safely in production (monitoring, incident response)

## Worked Example: Scoping Access for a Contractor

A data-science contractor is brought on to tune prompts and evaluate quality in the Foundry playground for one specific project — nothing more. They should **not** be able to deploy new models, change other projects' settings, or see connections belonging to unrelated teams.

- **Wrong**: granting `Owner` at the resource-group level "to save time" — violates least privilege and exposes every project under that group.
- **Wrong**: IP allow-listing their office network as the only control — that's a network-reachability restriction, not an authorization one; it doesn't limit *what* they can do once connected, and it doesn't survive them working from a coffee shop.
- **Right**: assign the contractor the **Azure AI Developer** role, scoped to *that one project* via Microsoft Entra ID / RBAC. This satisfies least privilege (a scoped role, not Owner) while still letting them do their actual job (playground access, running evaluations) without touching deployment or cross-project settings.

## Cheat Sheet 📋

| Concept | Key Rule |
|---|---|
| Managed identity | No stored secret; preferred over API keys |
| Least privilege | Scoped roles (Azure AI Developer) over Owner |
| Private endpoint | True public-network isolation (IP allow-list ≠ this) |
| Customer-managed keys | Customer controls at-rest encryption key |
| Data use | Prompts/completions not used for base-model retraining |
| RAI lifecycle | Identify → Measure → Mitigate → Operate |
