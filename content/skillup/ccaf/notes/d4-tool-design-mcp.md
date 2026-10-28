# Domain 4: Tool Design & MCP (Model Context Protocol)
**Exam Weight: 18%**

---

## Core Principle

> **"Fewer, well-described, role-scoped tools beat many overlapping ones."**

---

## 4.1 Too Many Tools on One Agent

Your agent has 42 tools. The PM says "just add one more." You watch the logs: Claude calls `update_customer_address` when the user asks to cancel an order, and `search_orders` instead of `search_customers`. Same naming patterns, descriptions that all start with "This tool handles..."---and now the model is basically guessing.

<div class="note-important"><strong>The exam guide's principle:</strong> giving an agent access to too many tools (its example: 18 instead of 4-5) degrades tool selection reliability by increasing decision complexity, and agents given tools outside their specialization tend to misuse them. There is no published accuracy curve or magic cut-off; the risk grows with tool count and with overlap between tools.</div>

### Why It Happens

Each tool adds **name + description + schema** to the context, and every extra option is another candidate to weigh:
- Similar descriptions blur together
- More candidates mean more chances to pick the *almost right* tool
- Tools outside an agent's role invite misuse (a synthesis agent starts running web searches)

<div class="note-scribble">Mental model: tools are job postings on a board. Would YOU pick the right one if 40 postings all said "handles customer stuff"?</div>

### Fix Order: Descriptions First, Then Distribution

1. **Fix the descriptions.** When two tools are confused, the first, low-effort fix is expanding each description with input formats, example queries, edge cases, and when to use it versus the similar tool (the exam guide's sample answer). Anthropic's tool docs call detailed descriptions "by far the most important factor in tool performance."
2. **Rename or split overlapping tools** so each has one clear contract.
3. **Distribute tools by role.** If descriptions are already good and one agent simply has too many, give each subagent only its own tools, with a few scoped cross-role tools for high-frequency needs.
4. **Load on demand.** For large libraries, Anthropic's tool docs suggest tool search (deferred loading) and service-prefixed names such as `github_list_prs`.

### Use Case: "The 40-Tool Disaster"

Your enterprise team built a monolith MCP server: 40 tools, one namespace. Three structural options:

![Flow diagram for "Use Case: 'The 40-Tool Disaster'": Problem: 40+ tools on oneagent, Option 1:Split MCP servers bydomain, Option 2:Coordinator + role-scopedsubagents, Option 3:Load only relevant toolstool search / per-intentsets](/content/skillup/ccaf/images/d4-tool-design-mcp-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m1.mmd -->

**Option 1: Multiple MCP Servers** --- split by domain.

```json
{
  "mcpServers": {
    "database": { "command": "node", "args": ["./mcp/db.js"] },
    "deploy": { "command": "python", "args": ["./mcp/deploy.py"] },
    "monitor": { "command": "node", "args": ["./mcp/monitor.js"] }
  }
}
```

**Option 2: Coordinator + subagents** --- the coordinator delegates; each subagent holds only its domain's tools.

```python
agents = {
    "database-agent": AgentDefinition(description="Data queries and migrations", prompt=DB_PROMPT,
                                      tools=["mcp__database__query", "mcp__database__describe"]),
    "deploy-agent":   AgentDefinition(description="Deployments and rollbacks", prompt=DEPLOY_PROMPT,
                                      tools=["mcp__deploy__release", "mcp__deploy__rollback"]),
}
```

**Option 3: Dynamic loading** --- expose only the tools a request needs.

<div class="note-trap"><strong>TRAP:</strong> Read the stem. If two tools with minimal descriptions are being confused, "expand the descriptions" is the <em>first</em> step, and a routing layer or consolidation is over-engineering. If descriptions are already good and one agent carries dozens of tools across domains, distribute the tools by role.</div>

---

## 4.2 Tool Description Engineering

Your agent picked `search_orders` instead of `search_customers` for the fifth time today. Same tool name pattern, nearly identical descriptions: "Search for things in the system." Both return JSON. Both take a `query` string. Claude had *no signal* to differentiate them.

<mark>Tool descriptions are like job postings --- if two sound the same, candidates apply to the wrong one.</mark>

### The 3-Element Rule

Every tool description MUST have these three components, no exceptions:

```
1. WHAT it does (purpose)
2. WHEN to use it (positive trigger)
3. WHEN NOT to use it (negative --- prevents confusion)
```

![Flow diagram for "The 3-Element Rule": Tool Description, WHAT: Primary purpose, WHEN: Use triggers, WHEN NOT:Disambiguation](/content/skillup/ccaf/images/d4-tool-design-mcp-m2.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m2.mmd -->

<div class="note-important"><strong>The WHEN NOT section is the most impactful element.</strong> Without it, Claude has no negative signal to reject a tool that looks 80% correct.</div>

### Use Case: "The Tool That Cried Wolf"

Two tools: `search_knowledge_base` and `get_customer`. Both vaguely "search for info." Without negative descriptions, Claude calls `search_knowledge_base` for account lookups because the word "search" matches. The fix:

```python
# BAD --- Claude doesn't know what, when, or when not
@mcp.tool()
def search(query: str) -> str:
    """Search for things."""

# GOOD --- All 3 elements present
@mcp.tool()
def search_knowledge_base(query: str) -> dict:
    """Search the internal product knowledge base for support articles.
    
    Use when: Customer asks about product features, pricing, or 
    troubleshooting steps covered in help documentation.
    
    Do NOT use when:
    - Looking up customer account data (use get_customer instead)
    - Checking order status (use get_order instead)  
    - Company policy questions (use get_policy instead)
    
    Returns: Top 5 matching articles with titles and excerpts.
    """
```

<div class="note-scribble">The "Do NOT use when" section is doing 80% of the disambiguation work. It's the most underrated part of tool design.</div>

### Another Strong Example

```python
@mcp.tool()
def create_ticket(title: str, description: str, priority: str) -> dict:
    """Create a new support ticket in the ticketing system.
    
    Use when: Issue requires tracking or follow-up beyond current conversation.
    
    Do NOT use when:
    - Issue resolved in this conversation (no ticket needed)
    - Ticket already exists (use update_ticket instead)
    - It's a feature request (use submit_feature_request instead)
    
    Priority: "critical" (system down), "high" (major broken), 
    "medium" (minor broken), "low" (questions/nice-to-haves)
    """
```

<div class="note-trap"><strong>TRAP:</strong> The exam may show a description with only "what" and "when." That's still a bad description. All THREE elements are required for production-quality tool design.</div>

---

## 4.3 tool_choice Modes

It's Friday afternoon. Your PM says: "Claude keeps chatting instead of calling the classifier. Just make it call the tool." You set `tool_choice: {"type": "tool", "name": "classify_intent"}`. Claude now **cannot refuse**---it must produce valid JSON matching that tool's schema. Problem solved. Ship it.

![Flow diagram for "4.3 toolchoice Modes": tool_choice, autodefaultClaude MAY call tools, anyClaude MUST call a toolpicks which one, toolClaude MUST callTHIS SPECIFIC tool, noneTools disabledreasoning only](/content/skillup/ccaf/images/d4-tool-design-mcp-m3.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m3.mmd -->

### When to Use Each

| Mode | API Code | Use Case |
|------|----------|----------|
| `auto` | `{"type": "auto"}` | General chat that MAY need tools |
| `any` | `{"type": "any"}` | Every response MUST produce structure |
| `tool` (forced) | `{"type": "tool", "name": "X"}` | **Guaranteed** specific JSON output |
| `none` | `{"type": "none"}` | Planning step (no execution) |

### Use Case: "The Guaranteed Schema Machine"

<mark>Forcing a tool guarantees the call; strict: true guarantees the input matches the schema.</mark> With a forced tool, the API prefills the assistant turn so Claude emits the tool_use block with no text before it (and no thinking block). Model support varies: Claude Opus 5.5, Sonnet 5.5, and Fable 5.1 reject `any` and named-tool `tool_choice` with a 400 error, so on those models use `auto` with strict tools or structured outputs.

```python
response = client.messages.create(
    model="claude-opus-5",          # accepts forced tool use
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "classify_intent"},  # MUST call this
    messages=[{"role": "user", "content": customer_message}]
)
# The response starts with the tool_use block; add strict: true for schema guarantees
result = response.content[0].input  # {"intent": "complaint", "confidence": 0.92}
```

<div class="note-important"><strong>tool_choice controls WHETHER a tool is called. strict: true controls WHETHER the output matches schema exactly.</strong> They solve different problems and stack together.</div>

<div class="note-scribble">Mental model: tool_choice = "you MUST fill this form." strict: true = "and every field must match the type declarations perfectly."</div>

<div class="note-trap"><strong>TRAP:</strong> The exam will test the difference between tool_choice (forces the call) and strict: true (guarantees schema). They are NOT the same thing. Forced tool_choice alone doesn't guarantee schema---it just guarantees the call happens.</div>

---

## 4.4 Parallel Tool Calls

Claude is helping a user plan a trip. It needs the weather in NYC, the weather in London, and the AAPL stock price. These are *independent* --- no result depends on another. So Claude fires all three in a single response, as parallel `tool_use` blocks. Your code must handle all of them and send results back in one message.

![Sequence diagram for "4.4 Parallel Tool Calls": Tool 3, Tool 2, Tool 1, Claude, "I need 3, independent, pieces of data", par, Parallel Execution, Synthesize all](/content/skillup/ccaf/images/d4-tool-design-mcp-m4.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m4.mmd -->

### Your Code Must Handle Multiple Results

```python
# Claude's response contains multiple tool_use blocks
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,  # MUST match!
            "content": json.dumps(result)
        })

# Send ALL results back in ONE message
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})
```

<div class="note-important"><strong>tool_use_id MUST match between the tool call and the result.</strong> Mismatched IDs = broken conversation state.</div>

### Parallel vs Sequential Decision

| Parallel | Sequential |
|---|---|
| Independent data fetches | Step B needs Step A's output |
| Multiple analyses of same input | Conditional logic (if A then B else C) |
| Same tool, different params | Stateful operations (write then verify) |

<div class="note-scribble">If you can draw the calls side-by-side with no arrows between them, it's parallel. If there's a "then" relationship, it's sequential.</div>

---

## 4.5 Graceful Tool Failure

Your `get_customer` tool crashes with an unhandled `ConnectionRefusedError`. The tool returns `None`. Claude sees... nothing useful. So it does what any model would do with missing data: it makes something up. The user gets a confident answer about a customer that doesn't exist. Welcome to "The Null That Hallucinated."

<mark>A tool crash or None return is the number one cause of Claude hallucinating factual data in agentic systems.</mark>

![Flow diagram for "4.5 Graceful Tool Failure": Success, Known error, Crash, Tool Executes, Result?, OK: {success: true, data:{...}}, Error: {error: not_found,suggestion: ...}, CRASH: Generic error orNone, Claude uses data, Claude follows suggestion](/content/skillup/ccaf/images/d4-tool-design-mcp-m5.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m5.mmd -->

### Use Case: "The Null That Hallucinated"

The user asks "What's the status of order ORD-999?" Your tool throws an exception and returns nothing. Claude responds: "Your order ORD-999 is currently in transit, expected delivery Thursday." Completely fabricated. The fix: **always return structured errors with guidance.**

```python
@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Look up customer by ID."""
    try:
        customer = db.find(customer_id)
        if not customer:
            return {
                "error": "customer_not_found",
                "message": f"No customer '{customer_id}'. Format: CUS-XXXXX.",
                "suggestion": "Try search_customer_by_email instead."
            }
        return {"success": True, "data": serialize(customer)}
    except DatabaseTimeoutError:
        return {
            "error": "database_timeout",
            "message": "DB timed out (5s). Usually transient.",
            "suggestion": "Retry in a moment."
        }
```

### What Claude Does With Each Return Type

| Return | Claude's Behavior |
|--------|------------------|
| `{"success": true, "data": {...}}` | Uses data normally |
| `{"error": "not_found", "suggestion": "..."}` | Follows suggestion |
| `{"error": "timeout", "suggestion": "retry"}` | May retry |
| Tool crashes / returns `None` | **May hallucinate data!** |

<div class="note-trap"><strong>TRAP:</strong> The exam loves testing what happens on None/crash returns. The answer is ALWAYS "Claude may hallucinate." Structured error returns are the fix. Never let a tool return nothing.</div>

<div class="note-scribble">Think of structured errors as "redirects" for Claude. You're saying "go HERE instead" rather than leaving it lost in a dead end with no signal.</div>

---

## 4.6 MCP Primitives

Your team is designing an MCP server and someone asks: "Should we make the refund policy a tool or a resource?" Another person says: "And what about the escalation template?" These three things *feel* similar --- they all provide info --- but MCP distinguishes them by **who initiates the interaction.**

<mark>MCP Primitives: Tools = employee actions, Resources = reference books on the shelf, Prompts = forms the user fills out.</mark>

![Flow diagram for "4.6 MCP Primitives": 3 MCP Primitive Types, ToolsModel-initiated ACTIONSClaude decides to call, ResourcesApp-loaded READ-ONLYdataApplication decides toload, PromptsUser-selected TEMPLATESUser explicitly chooses](/content/skillup/ccaf/images/d4-tool-design-mcp-m6.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m6.mmd -->

### The Initiation Model (Exam-Critical)

| Primitive | Initiated By | Analogy | Example |
|-----------|:---:|---|---|
| **Tool** | Model | Employee does a task | `send_email()`, `run_query()` |
| **Resource** | Application | Book on the shelf, app grabs it | `customer://123/profile` |
| **Prompt** | User | Form the user picks and fills | `/escalation_template` |

<div class="note-important"><strong>Who initiates each primitive is THE exam question for MCP.</strong> Tools = model. Resources = application. Prompts = user. Memorize this.</div>

### Code Examples

```python
# TOOL --- Claude decides when to call (model-initiated)
@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    """Send email. Use when: customer requests confirmation."""
    return {"sent": True, "message_id": "msg_123"}

# RESOURCE --- Application pre-loads into context (app-initiated)
@mcp.resource("support://policies/refund")
def refund_policy() -> str:
    """Current refund policy. Loaded when support session starts."""
    return "Full refund within 30 days..."

# PROMPT --- User explicitly selects (user-initiated, like a slash command)
@mcp.prompt()
def escalation_template(severity: str) -> list:
    """Template for escalating to engineering."""
    return [{"role": "user", "content": f"Draft {severity} escalation..."}]
```

<div class="note-scribble">If the exam says "application loads data at session start" --- that's a Resource. If "Claude decides to do something" --- Tool. If "user picks a template from a menu" --- Prompt.</div>

<div class="note-trap"><strong>TRAP:</strong> Resources are READ-ONLY. If the exam describes writing/mutating data, that's a Tool, not a Resource --- regardless of what the data looks like.</div>

---

## 4.7 FastMCP Server (Complete Example)

You've been asked to build a customer support MCP server. It needs: a tool to look up orders, a resource for the refund policy (loaded at session start), and it needs to run on stdio transport for local development. Here's the complete implementation:

```python
from mcp.server.fastmcp import FastMCP   # FastMCP ships in the official MCP Python SDK

mcp = FastMCP("customer-support")

@mcp.tool()
def lookup_order(order_id: str) -> dict:
    """Look up order details by ID.
    
    Use when: Customer asks about order status or shipping.
    Do NOT use when: General questions not about a specific order.
    Format: ORD-XXXXXXXX (8 alphanumeric after prefix)
    """
    if not order_id.startswith("ORD-") or len(order_id) != 12:
        return {"error": "invalid_format", "message": "Expected: ORD-XXXXXXXX"}
    
    order = db.orders.find(order_id)
    if not order:
        return {"error": "not_found", "message": f"No order {order_id}"}
    
    return {
        "order_id": order.id,
        "status": order.status,
        "items": [{"name": i.name, "qty": i.qty} for i in order.items],
        "eta": order.estimated_delivery.isoformat()
    }

@mcp.resource("support://policies/refund")
def refund_policy() -> str:
    """Refund policy loaded at session start."""
    return "Full refund <30 days. 50% refund 31-60 days. No refund >60 days."

if __name__ == "__main__":
    mcp.run()  # stdio transport (default)
```

### Wire It Up

```json
{
  "mcpServers": {
    "customer-support": {
      "command": "python",
      "args": ["./mcp-servers/support.py"],
      "type": "stdio"
    }
  }
}
```

<div class="note-scribble">Notice: the tool has all 3 description elements, validates input format, returns structured errors on failure. This is the pattern to internalize for the exam.</div>

---

## 4.8 JSON Schema for Tool Parameters

Claude reads your tool's JSON Schema to know what params to fill. Vague schemas produce vague calls. Your schema IS your documentation for the model.

### Use Case: "The Ambiguous Parameter"

Tool: `search_products(query, limit, status)`. No format hints. Claude sends `limit: "ten"` (string) and `status: "ACTIVE"` (wrong case). Your tool crashes. The fix: constrain everything in the schema.

### Key Practices

| Practice | Example |
|----------|---------|
| Specify format | `"description": "ISO date (YYYY-MM-DD)"` |
| Declare defaults | `"default": 10` |
| Set ranges | `"minimum": 1, "maximum": 100` |
| Use enums | `"enum": ["active", "archived", "all"]` |
| Mark required | `"required": ["query"]` |

```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string", "description": "Search query. Max 200 chars."},
    "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 100},
    "status": {"type": "string", "enum": ["active", "archived", "all"], "default": "active"}
  },
  "required": ["query"]
}
```

<div class="note-important"><strong>Enums + descriptions + required fields steer Claude toward correct inputs.</strong> Vague schemas produce garbage inputs. Note that strict tool use doesn't support numeric or string range keywords (<code>minimum</code>, <code>maximum</code>, <code>minLength</code>...), so with <code>strict: true</code> state ranges in the description and validate them in your code.</div>

<div class="note-scribble">Think of the schema as the "form validation rules" Claude sees before it fills in the form. More constraints = fewer mistakes.</div>

---

## 4.9 Claude 101 — Tool Use Fundamentals (2026)

You integrate tool use for the first time. You define a `web_search` tool in your API call. Claude returns a result... but you never executed anything. Wait — `web_search` is a **server tool**. Anthropic executed it for you on their side. Your custom tools? Those are **client tools** — you must execute them yourself and send back results.

### Two Categories of Tools

![Flow diagram for "Two Categories of Tools": Server Tools ANTHROPIC executes, web_search,code_execution,web_fetch, tool_search, Results appear directlyin response, Client Tools YOU execute, User-defined tools+ Anthropic-schema toolsbash, text_editor, stop_reason: tool_use, Your code executes, Send tool_result back](/content/skillup/ccaf/images/d4-tool-design-mcp-m7.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m7.mmd -->

<div class="note-important"><strong>Server tools need NO tool_result from you.</strong> The results are embedded in Claude's response. Client tools require your code to execute them and send a tool_result message.</div>

### Server Tools (No Execution Needed)

```python
# Server tool — Anthropic handles execution
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    tools=[{"type": WEB_SEARCH_TOOL_TYPE, "name": "web_search"}],  # current versioned type from the tool reference
    messages=[{"role": "user", "content": "What's the latest on Mars rover?"}],
)
# Results are IN the response — no tool_result needed from you
```

### Strict Tool Use (Schema Guarantees)

Add `strict: true` to ensure Claude's tool calls **always** match your schema exactly:

```python
tools = [{
    "name": "extract_data",
    "description": "Extract structured data from text",
    "strict": True,  # GUARANTEES schema conformance
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}       # no minimum: strict mode rejects range keywords
        },
        "required": ["name", "age"],
        "additionalProperties": False
    }
}]
```

<div class="note-trap"><strong>TRAP:</strong> strict: true on tool definitions guarantees schema compliance at the API level. This is DIFFERENT from tool_choice which controls WHETHER a tool is called, not whether the output conforms. The exam WILL test this distinction.</div>

### Tool Use Cost

Tool definitions (names, descriptions, schemas), tool_use blocks, and tool_result blocks all count as tokens, and enabling tools adds a tool-use system prompt. Every tool you attach costs context even if it's never called, which is one more reason to scope tools to each agent's role.

### Complete Agentic Tool Loop

This is the canonical pattern. If the exam shows an agentic loop and asks what's wrong, you need this structure memorized:

```python
messages = [{"role": "user", "content": user_input}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        tools=tools,
        messages=messages,
    )
    
    # stop_reason drives the loop
    if response.stop_reason == "end_turn":
        break  # Done — final text response
    if response.stop_reason != "tool_use":
        handle_other_stop(response)  # max_tokens, refusal, ...
        break
    
    # Process ALL tool calls (may be parallel)
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })
    
    # Append assistant response + tool results
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
```

<div class="note-important"><strong>The agentic loop continues while stop_reason == "tool_use" and ends on "end_turn".</strong>If stop_reason == "tool_use", Claude needs you to execute tools and return results. Breaking on the wrong condition = broken agent.</div>

<div class="note-trap"><strong>TRAP:</strong> The tool_results go in a message with role "user" — NOT "tool" or "system". The assistant's response (including its tool_use blocks) must also be appended BEFORE the results. Skipping either breaks the loop.</div>

---

## 📋 Domain 4 Cheat Sheet

| Concept | Key Fact |
|---------|----------|
| Tool count | <mark>Too many tools on one agent (exam example: 18 vs 4-5) degrades selection; scope tools by role</mark> |
| Tool description | MUST have: what + when to use + when NOT to use |
| Guaranteed call | `tool_choice: {"type": "tool", "name": "X"}` (rejected on Opus 5.5 / Sonnet 5.5 / Fable 5.1) |
| Schema guarantee | `strict: true` on tool definition (different from tool_choice!) |
| Parallel calls | Independent tools called in same response, matched by `tool_use_id` |
| Error returns | Structured `{error, message, suggestion}` — never None/crash |
| MCP Tools | Model-initiated (Claude decides) |
| MCP Resources | App-initiated (loaded at session start, read-only) |
| MCP Prompts | User-initiated (user explicitly selects) |
| MCP transport | stdio for local servers; HTTP for remote (SSE deprecated) |
| Server tools | No `tool_result` needed — Anthropic executes them |
| Client tools | YOU execute and send `tool_result` back |
| Tool confusion fix | Reduce tools OR improve "Do NOT use when" descriptions |
| Agentic loop exit | `stop_reason == "end_turn"` (NOT `"tool_use"`) |
| Tool cost | Every attached tool's definition costs context, called or not |

<div class="note-scribble">If you remember ONE thing from this domain: detailed, differentiated descriptions first; role-scoped tool sets second; structured error returns always.</div>

---

## 4.6 MCP Resources vs Tools

<div class="note-important"><strong>Explicitly in exam guide appendix.</strong> Resources are the mechanism to expose content catalogs — distinct from tools.</div>

### The Three MCP Primitives

| Primitive | Who Initiates | Purpose | Example |
|---|---|---|---|
| **Tools** | Claude (model) | Execute actions | `search_issues`, `create_ticket` |
| **Resources** | Application | Expose read-only content catalogs | Issue list, DB schema, doc hierarchy |
| **Prompts** | User | User-selectable prompt templates | `/review`, `/summarise` |

### Why Resources Matter for Exams

Without resources, an agent exploring a knowledge base must call tools repeatedly (exploratory tool calls) just to discover what content exists. Resources give the agent **visibility upfront**.

![Flow diagram for "Why Resources Matter for Exams": With MCP Resources, reads catalog at session start, knows what exists, targetedcalls only, Agent, Resource: topic index, 1-2 tool calls, Without MCP Resources, search for topics, search again, tool call](/content/skillup/ccaf/images/d4-tool-design-mcp-m8.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d4-tool-design-mcp-m8.mmd -->

<div class="note-trap"><strong>TRAP:</strong> Question asks how to reduce exploratory tool calls. Answer involves exposing a content catalog as an MCP resource — NOT adding more tools.</div>

---

## 4.7 The isError Flag & Structured Error Taxonomy

The `isError` flag is the MCP-native way to signal tool failures back to the agent **without throwing exceptions**.

```typescript
// ✅ Correct MCP error return
return {
  isError: true,
  content: [{
    type: "text",
    text: JSON.stringify({
      errorCategory: "transient",   // transient | validation | permission | business
      isRetryable: true,
      message: "Database connection timeout after 5s",
      attemptedQuery: "SELECT * FROM orders WHERE id = ?",
      suggestion: "Retry in 2-3 seconds"
    })
  }]
}
```

### Error Category Taxonomy

| Category | isRetryable | Agent Action |
|---|---|---|
| `transient` | `true` | Retry with exponential backoff |
| `validation` | `false` | Fix input parameters and retry |
| `permission` | `false` | Escalate to human / surface to user |
| `business` | `false` | Explain policy to user, don't retry |

### Edit Tool Fallback Pattern

When the `Edit` built-in tool fails because anchor text is non-unique:

| When this happens | Fall back to |
|---|---|
| Edit tool error: *"Found multiple matches for anchor text"* | **Read** the full file, then **Write** the full file with your changes |

<div class="note-trap"><strong>TRAP:</strong> Edit requires <code>old_string</code> to appear exactly once. Claude Code's tool reference says to supply a longer string with enough surrounding context, or set <code>replace_all: true</code> to change every occurrence. When no unique anchor can be found, the exam guide's answer is the Read + Write fallback: read the full file, write it back with the change.</div>

---

## 4.10 Built-in Tools: Read, Write, Edit, Bash, Grep, Glob

### Key Concept

**Grep finds content, Glob finds file names, Read and Write move whole files, and Edit changes one unique spot.**

Grep searches file contents for patterns (all callers of a function, an error message, an import). Glob matches file paths by name or extension (`**/*.test.tsx`). Read loads a full file; Write creates or overwrites one; Edit replaces an `old_string` that must appear exactly once (or every occurrence with `replace_all: true`). Bash runs shell commands.

Good exploration is incremental: Grep for entry points, Read to follow imports and trace the flow, and for wrapper modules first list every exported name, then Grep for each one. **Grep is the index at the back of the book, Glob is the table of contents, and Read is turning to the page.**

### In Practice

**What breaks without this**: Reading every file up front floods the context; using Glob to find callers returns file names, not usages; Edit on a repeated anchor fails.

**Decision trigger**: Ask whether you're looking for *text inside files* (Grep), *files by name* (Glob), or *changing a file* (Edit for one unique spot; Read + Write when no unique anchor exists).

**When you'd choose differently**: In current Claude Code on macOS, Linux, and WSL, Glob and Grep are left out of the default tool set and Claude searches with `find` and `grep` through Bash (embedded `bfs` and `ugrep`); naming Glob or Grep in `--tools` or `--allowedTools` (or the SDK equivalents) brings them back. The selection logic the exam tests is the same either way.

### Exam Trap ⚠️

<div class="note-trap">"Find all callers of <code>processRefund</code>" is Grep, not Glob. "Find all <code>*.test.tsx</code> files" is Glob, not Grep. And when Edit can't match a unique anchor, the exam's answer is Read the file, then Write it back with the change.</div>

---

## 4.11 MCP Servers in Claude Code: Scopes, Secrets, and Build vs Buy

### Key Concept

**Team servers go in the project's `.mcp.json`; personal servers stay in `~/.claude.json`; secrets stay in environment variables.**

`claude mcp add` defaults to **local** scope (your `~/.claude.json`, this project only). `--scope project` writes `.mcp.json` in the repo root for the team, and `--scope user` puts a server in `~/.claude.json` for all of your own projects. `.mcp.json` supports `${VAR}` and `${VAR:-default}` expansion in `command`, `args`, `env`, `url`, and `headers`, so tokens never get committed.

Tools from every configured server are discovered at connection time and available together. A tool's description decides whether Claude prefers it over a built-in like Grep, and MCP **resources** expose catalogs (issue summaries, documentation trees, schemas) so the agent doesn't need exploratory calls. **`.mcp.json` is the office's shared printer list; `~/.claude.json` is the printer on your own desk.**

### In Practice

**What breaks without this**: A teammate adds a server without a scope flag and tells everyone it's shared, but it only exists in their local config; or a token is hard-coded into a committed `.mcp.json`.

**Decision trigger**: Ask who needs the server and where the credential lives. Team → project scope with `${TOKEN}`; experiment → user or local scope.

**When you'd choose differently**: For standard integrations (Jira, GitHub), use an existing community or vendor MCP server; build a custom one only for team-specific workflows. In CI, project servers from `.mcp.json` load without an approval prompt, so use `--strict-mcp-config` or `--bare` when the job shouldn't start repository-defined servers.

### Exam Trap ⚠️

<div class="note-trap">"Put the token in <code>.mcp.json</code>" (leaks secrets), "configure the team server in <code>~/.claude.json</code>" (not shared), and "the agent keeps using Grep, so delete Grep" (fix the MCP tool's description instead) are the classic distractors.</div>

---

## Deep Dive

### 1. The connective narrative

This domain (Domain 2, Tool Design & MCP Integration, in the official blueprint) starts from one fact: **the model chooses tools by reading their descriptions.** A description has to say what the tool does, what input it expects, when to use it, and when to use the similar tool instead. Overlapping names and vague descriptions cause misrouting, and keyword-heavy system prompts can override even good descriptions.

From there it's about the *shape* of the tool surface. Split a generic tool into purpose-specific ones with clear contracts, constrain risky ones (a validating `load_document` instead of a raw `fetch_url`), and give each agent only the tools its role needs, adding a scoped cross-role tool such as `verify_fact` where round trips would otherwise dominate. `tool_choice` decides whether a call is forced, and strict schemas decide whether its input is valid.

Failures are part of the interface too. Return `isError` with a category (transient, validation, business, permission), a retryable flag, and a human-readable explanation, and keep "nothing found" distinct from "couldn't look". In Claude Code, MCP servers are wired in by scope, with environment variables for secrets and resources for catalogs, while built-in tools follow a simple rule: Grep for content, Glob for names, Edit for one unique change.

### 2. Worked scenario

> **Scenario.** A developer-productivity agent has 26 tools from three MCP servers plus the built-ins. It often greps the repo instead of calling the richer `code_search` MCP tool, retries a permission error ten times, and the Jira server's token was just found in git history.
>
> **Step 1 — descriptions.** Rewrite `code_search`'s description: what it indexes, the query formats it accepts, what it returns, and when to prefer it over Grep.
>
> **Step 2 — errors.** Make the MCP server return `isError: true` with `errorCategory: "permission"` and `isRetryable: false`, so the agent explains the problem instead of retrying.
>
> **Step 3 — secrets.** Rotate the token, replace it with `${JIRA_TOKEN}` in `.mcp.json`, and switch to a maintained community or vendor Jira server rather than the home-grown one.
>
> **Step 4 — tool load.** Move release tooling into a release subagent so the exploration agent only sees the tools it uses.
>
> **Outcome:** better routing from better descriptions, no wasted retries, no secrets in git, and a smaller decision for every request.

### 3. Memory aid

**DICE** — designing a tool surface:
- **D**escribe precisely (purpose, inputs, examples, boundaries)
- **I**solate by role (scoped tool sets, few cross-role tools)
- **C**ategorize errors (`isError`, category, retryable, explanation)
- **E**xpose catalogs as resources, and wire servers by the right scope

### 4. Exam strategy for this domain

- When two tools are confused and their descriptions are thin, the first fix is the descriptions; routing layers and consolidation are "valid but more effort than a first step".
- Access failure versus valid empty result appears in several guises; the answer always keeps them distinct.
- Watch for over-provisioning: giving the synthesis agent every web tool "to avoid round trips" violates least privilege.
- Five minutes before the exam: **descriptions first, scope second, structured errors always.**
