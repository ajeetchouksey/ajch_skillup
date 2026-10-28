# Domain 5: Context Management & Reliability
**Exam Weight: 15%**

---

## 🧠 The Core Mental Model

> **Context window = a desk.** Too many papers and you can't find anything. The papers at the top and bottom of the stack get noticed; the ones in the middle get buried. Summarize = file the old papers but keep the receipts. Cache = pre-printed name badges at a conference — the first one costs time, the rest are free.

<div class="note-important"><strong>The Three Commandments of Context:</strong> (1) Position matters — start and end get attention; (2) Never lose specific numbers; (3) Pay once, reuse many times via caching.</div>

---

## 5.1 The Lost-in-the-Middle Problem

### 📖 Story: "The Buried Account Number"

A fintech support agent was processing a complex dispute. The system prompt set the tone (message 1). Then came 45 messages of back-and-forth. The customer's account number — `ACC-8827-XR` — was mentioned in message 4. By message 46, when Claude needed to file the dispute, it referenced "the customer's account" but couldn't surface the actual number. It was *buried in the middle*.

The team moved the account number into the system prompt's critical-context block. Problem solved overnight.

<div class="note-scribble">Think of attention like a U-shaped bathtub — water pools at both ends, the middle is dry. That's where info goes to die.</div>

### The U-Shaped Attention Curve

![Flow diagram for "The U-Shaped Attention Curve": Attention Distribution U-Shaped, Start HIGH attention, ... MIDDLE ... LOW attention, END HIGH attention](/content/skillup/ccaf/images/d5-context-management-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m1.mmd -->

```
Attention Level
 ####                                ####
 ####................................####
 ####................................####
 —————————————-> Position
 START          MIDDLE               END
 (HIGH)         (LOW)                (HIGH)
```

<div class="note-important"><strong>Critical info goes at START and END.</strong> The middle of the context window receives the least attention from the model. This is an empirically observed behavior, not a bug.</div>

### Positioning Strategy Table

| Content | Position | Why |
|---|:-:|-|
| System prompt / role | Start | Highest attention, sets behavior |
| Critical constraints | Start | Must never be forgotten |
| Reference documents | Middle | Searched when needed (acceptable) |
| Current task / query | End | Recency boost for focus |
| Output format | End | Fresh in working memory |

<div class="note-trap"><strong>TRAP:</strong> An exam question may show "critical customer SLA" placed in the middle of a 50K-token document block, with Claude failing to honor it. The fix is NEVER "add more emphasis" — it's repositioning to start or end.</div>

### Use Case: "The Sandwich Technique"

```python
messages = [
    {"role": "user", "content": [
        # Position 1 (Start): Critical context - HIGH attention
        {"type": "text", "text": "<context>Enterprise customer. LTV: $45K. Account: 3 years.</context>"},

        # Position 2 (Middle): Reference bulk - acceptable lower attention
        {"type": "text", "text": "<docs>[... 50K tokens of product documentation ...]</docs>"},

        # Position 3 (End): Current task - HIGH attention (recency)
        {"type": "text", "text": "<task>Explain Enterprise Plus tier benefits. Be concise.</task>"}
    ]}
]
```

**Mental model:** You're writing a memo. Put the TL;DR at the top, the appendix in the middle, and the action item at the bottom. Nobody reads the appendix cover-to-cover — they search it when needed.

---

## 5.2 Progressive Summarization

### 📖 Story: "The Vanishing Order Number"

A support agent processed 30 messages. On message 31, it forgot the customer's order number from message 3. Why? The context window hit capacity. The system summarized old messages — but the junior dev who wrote the summarizer used a generic prompt: *"Summarize the conversation so far."*

The summary said: "Customer had a billing issue with a recent order." The order number `ORD-4829AF01`, the charge of `$147.32`, the date `2025-03-15` — all gone. The customer had to repeat everything. CSAT dropped. The fix was one line in the summarization prompt: **"PRESERVE all IDs, amounts, dates, and commitments VERBATIM."**

<div class="note-important"><strong>NEVER round, approximate, or paraphrase specific data values when summarizing.</strong> Order IDs, dollar amounts, dates, email addresses, error codes — these must survive compression intact.</div>

### Mental Model: Filing Cabinets

> Summarization is filing, not shredding. You keep the receipts (IDs, amounts, dates) and throw away the small talk. If you can't reconstruct the exact transaction from your summary, you've filed wrong.

### The Architecture

![Flow diagram for "The Architecture": Context Window Management, System Prompt nevercompressed, Summary of turns 1-20compressed 80%, Full turns 21-30 verbatimrecent, Current message alwaysfull](/content/skillup/ccaf/images/d5-context-management-m2.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m2.mmd -->

### What to Preserve vs Compress

| Always Preserve (Verbatim) | Safe to Compress |
|-|-|
| Order IDs, customer IDs | Pleasantries ("Thanks!", "Sure!") |
| Dollar amounts, dates | Repeated explanations |
| Email addresses, phone numbers | Claude's verbose reasoning |
| Error messages, codes | Already-answered questions |
| Promises/commitments made | Exploratory back-and-forth |
| Technical specs (versions) | "You're welcome" exchanges |

<div class="note-trap"><strong>TRAP:</strong> If an exam question shows a summary that says "customer was charged approximately $150 in March" when the original was "$147.32 on 2025-03-15," that summary is WRONG. The correct answer always preserves exact values.</div>

<div class="note-scribble">The rule is simple: if it has digits or looks like an identifier, copy-paste it into the summary. No exceptions.</div>

### Implementation

```python
def manage_context(messages: list, max_tokens: int = 100000) -> list:
    if count_tokens(messages) <= max_tokens:
        return messages  # No compression needed

    system_prompt = messages[0]
    recent_count = 10
    old_messages = messages[1:-recent_count]
    recent_messages = messages[-recent_count:]

    # Summarize old messages (preserve specifics!)
    summary = client.messages.create(
        model="claude-sonnet-5-5",
        system="""Summarize conversation. PRESERVE VERBATIM:
- IDs, order numbers, account numbers
- Dollar amounts, dates, times
- Names, addresses, emails
- Error codes, versions
- Promises made
REMOVE: pleasantries, reasoning, repetition.""",
        messages=[{"role": "user", "content": format_messages(old_messages)}]
    ).content[0].text

    return [
        system_prompt,
        {"role": "user", "content": f"<summary>{summary}</summary>"},
        {"role": "assistant", "content": "Context loaded. Continuing..."},
        *recent_messages
    ]
```

---

## 5.3 Tool Result Trimming

### 📖 Story: "The 10,000-Row Explosion"

A developer built an MCP tool that returned full database query results. One user asked "show me all customers in California." The tool returned 10,247 rows, each with 15 fields: hundreds of thousands of tokens dumped into the context window. Even when it fits, critical details get lost in the middle of those rows, and every later turn pays for them again.

The fix: return the top 5 results with a `total_count` and a pagination hint. Claude learned to ask for more only when needed.

### Mental Model: The Librarian

> A good tool is like a librarian. You don't dump all 10,000 books on someone's desk. You bring the 5 most relevant ones and say, "I have 10,000 more if these aren't right." Let the user ask for specifics.

![Flow diagram for "Mental Model: The Librarian": < 5KB, 5KB, Tool returns data, Size check, Send as-is, Trimming Strategy, Server-side trim in toolimplementation, Client-side trim beforesending to Claude, Pagination page-by-page](/content/skillup/ccaf/images/d5-context-management-m3.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m3.mmd -->

### Strategy 1: Server-Side Trim (Best Practice)

```python
@mcp.tool()
def search_products(query: str, limit: int = 5) -> dict:
    results = db.search(query, limit=50)  # Fetch more for ranking

    # Return only what Claude needs
    return {
        "results": [{"id": r.id, "name": r.name, "price": r.price}
                   for r in results[:limit]],
        "total": len(results),
        "message": f"Top {limit} of {len(results)}. Ask for more if needed."
    }
```

### Strategy 2: Pagination

```python
@mcp.tool()
def list_customers(page: int = 1, per_page: int = 10) -> dict:
    """Returns one page at a time. Use page param to navigate."""
    offset = (page - 1) * per_page
    customers = db.customers.find().skip(offset).limit(per_page)
    return {
        "customers": [brief(c) for c in customers],
        "pagination": {"page": page, "total_pages": total // per_page + 1}
    }
```

<div class="note-scribble">Every tool should answer: "What's the MINIMUM Claude needs to decide the next step?" — not "here's everything I know."</div>

---

## 5.4 Escalation and Ambiguity Resolution

### Key Concept

**Escalate for the right reasons: the customer asks for a human, policy is silent or needs an exception, or the agent can't make progress.**

The exam guide's escalation triggers are explicit customer requests for a human (honoured immediately, without investigating first), policy exceptions or gaps (for example competitor price matching when the policy only covers your own site), and inability to make meaningful progress. Complexity alone isn't a trigger, and neither are frustration or the agent's own confidence score: **sentiment-based escalation and self-reported confidence are unreliable proxies for actual case complexity.**

When a customer is frustrated but the issue is within the agent's capability, acknowledge it and offer the resolution, escalating only if they reiterate that they want a person. When a lookup returns several matching customers, ask for another identifier instead of picking one. **A good agent is a good receptionist: it hands you to the manager the moment you ask, but it doesn't send every raised voice upstairs.**

### In Practice

**What breaks without this**: First-contact resolution sinks to 55% because the agent escalates easy cases with photo evidence while improvising refunds that needed a policy exception.

**Decision trigger**: Before tuning thresholds or adding classifiers, ask whether the system prompt states explicit escalation criteria with few-shot examples of escalate versus resolve. That's the proportionate first fix.

**When you'd choose differently**: Hard business limits (refunds over $500) aren't an escalation *judgment* at all; enforce them in code with a hook that blocks the call and redirects to a human.

### Exam Trap ⚠️

<div class="note-trap">"Escalate when self-rated confidence drops below 7/10", "escalate on negative sentiment", and "train a classifier on historical tickets" are the three standard distractors. The exam answer is explicit criteria plus few-shot examples, and a structured handoff (customer ID, root cause, amounts, recommended action) when escalation happens.</div>

### Handoff Payload

```python
handoff = {
    "customer_id": "CUS-20931",
    "issue": "Duplicate charge on order ORD-4829AF01",
    "root_cause": "Payment retried after gateway timeout; both captures settled",
    "amounts": {"charged": 147.32, "duplicate": 147.32},
    "actions_taken": ["verified identity", "confirmed two captures in billing"],
    "recommended_action": "Refund duplicate capture of $147.32",
    "escalation_reason": "Refund requires approval above agent limit",
}
```

The human may never read the transcript, so the handoff has to stand on its own.

---

## 5.5 Prompt Caching

### 📖 Story: "The $15 Cache That Saved $15K"

A legal-tech startup sent the same 50K-token system prompt (case law, compliance rules, firm policies) with every API call, paying full input price for *unchanging text* thousands of times a day.

One engineer added `cache_control: {"type": "ephemeral"}` to the system prompt block. The first call cost 25% more (the cache write). Every hit after that was billed at a small fraction of the input price (0.1x on most models, 0.05x on Claude Opus 5.5 and Sonnet 5.5) and returned faster. That single annotation paid for itself within minutes.

<div class="note-important"><strong>Exam scope:</strong> the exam guide lists "prompt caching implementation details (beyond knowing it exists)" and "API pricing calculations" as out of scope. Know what caching is for; treat the numbers below as reference.</div>

<div class="note-scribble">Caching is the easiest win in the entire Anthropic API. If you send the same big block repeatedly, you're burning money for no reason.</div>

### Mental Model: Pre-Printed Name Badges

> Cache = pre-printed name badges at a conference. Making the first badge costs time (design, print). But once the template exists, stamping out 999 more is nearly free. The badge expires after 5 minutes of no one picking it up (TTL). If someone grabs one every 4 minutes, it stays available forever.

![Flow diagram for "Mental Model: Pre-Printed Name Badges": Subsequent Requests Cache Read, First Request Cache Write, 1.25x cost, 0.1x cost lower on somecurrent models, 50K token system prompt, Cache, System prompt from cache](/content/skillup/ccaf/images/d5-context-management-m4.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m4.mmd -->

### How to Use

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    system=[{
        "type": "text",
        "text": large_system_prompt,       # 50K tokens
        "cache_control": {"type": "ephemeral"}  # Cache this!
    }],
    messages=[{
        "role": "user",
        "content": [{
            "type": "text",
            "text": reference_docs,         # Another 20K tokens
            "cache_control": {"type": "ephemeral"}  # Cache this too!
        }, {
            "type": "text",
            "text": "What's the return policy?"  # No cache (changes every time)
        }]
    }]
)
```

### Cache Properties — <mark>MEMORIZE for Exam</mark>

| Property | Value |
|----|---|
| TTL | <mark>**5 minutes**</mark> (refreshed on each hit); 1 hour optional |
| Minimum cacheable prompt | 512 tokens on current models (Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1); 1,024–4,096 on some older models |
| Max breakpoints per request | <mark>**4**</mark> |
| Cache write cost | **1.25x** base input (5-minute) or **2x** (1-hour) |
| Cache read cost | **0.1x** base input on most models; 0.05x on Opus 5.5 and Sonnet 5.5; 0.025x on Fable 5.1 |
| Prefix order | tools → system → messages, up to the breakpoint |

<div class="note-important"><strong>TTL refreshes on every cache hit.</strong> If requests come in every 4 minutes, the cache lives forever. If there's a 5+ minute gap with no hits, the cache expires and the next request pays the 1.25x write cost again.</div>

<div class="note-trap"><strong>TRAP:</strong> Exam might say "cache TTL is 5 minutes total regardless of usage." WRONG — it's 5 minutes since LAST hit. Continuous usage keeps it alive indefinitely.</div>

### Use Case: "The Relative-Cost Math"

```
100 requests/hour, each with the same 50K-token prefix (in units of "base input price x 50K tokens"):

Without caching:  100 x 1.0              = 100 units
With caching:     1 x 1.25 + 99 x 0.1    = ~11 units   (0.1x read models)
                  1 x 1.25 + 99 x 0.05   = ~6 units    (Opus 5.5 / Sonnet 5.5)
```

### Optimal Breakpoint Placement

```
Breakpoint 1: System prompt (rarely changes)     <-- HIGH value
Breakpoint 2: Reference documents (static)       <-- HIGHEST value
Breakpoint 3: Conversation history (grows)       <-- MEDIUM value
Breakpoint 4: Tool definitions (if large)        <-- HIGH value
NO cache: Current user message (changes always)
```

<div class="note-scribble">Rule of thumb: cache what's STATIC, don't cache what's DYNAMIC. If it changes every request, caching wastes the 1.25x write cost.</div>

---

## 5.6 Message Batches API

### 📖 Story: "The Batch That Ran Overnight"

A content team needed to classify 50,000 product descriptions into 12 categories. They switched from real-time calls to the Message Batches API — same model, same prompts — at half the price. The trade-off: results arrive asynchronously (most batches finish within an hour, and anything not processed within 24 hours expires) instead of in real time. Nobody was waiting on the result, so it was an easy call.

### Mental Model: Overnight Shipping vs. Same-Day

> Batches API = choosing ground shipping. Same package arrives, costs half as much, but you wait up to 24 hours. Don't use it when the customer is standing at the counter waiting.

![Flow diagram for "Mental Model: Overnight Shipping vs. Same-Day": Batches API, Processing up to 24h, JSONL Input up to 100Krequests, Anthropic Batch API, Results 50% cost](/content/skillup/ccaf/images/d5-context-management-m5.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m5.mmd -->

### Key Properties

| Property | Value |
|----|---|
| Max requests per batch | <mark>**100,000**</mark> |
| Cost | <mark>**50% of standard**</mark> API pricing |
| Processing time | Most finish within 1 hour; requests not processed within <mark>**24 hours**</mark> expire |
| Size limit | 100,000 requests or 256 MB, whichever comes first |
| Results available | **29 days** after the batch is created |
| Result types | succeeded, errored, canceled, expired (expired requests aren't billed) |
| `custom_id` | <mark>YOUR tracking key</mark> (echoed in results) |

<div class="note-important"><strong>custom_id is YOUR identifier.</strong> You set it per-request in the batch. Anthropic echoes it back in results so you can map outputs to your original inputs. It's not auto-generated — YOU control it.</div>

### When to Use

| Good Fit | Bad Fit |
|-|-|
| Classify 50K documents | Real-time chatbot |
| Generate 10K descriptions | Interactive support |
| Evaluate 5K test prompts | Latency-sensitive API |
| Any task where hours of wait = OK | Need response in seconds |

<div class="note-trap"><strong>TRAP:</strong> Exam question: "A startup needs real-time responses for a chatbot. Which API approach reduces cost by 50%?" If "Batches API" is an option, it's the WRONG answer. Batches are NOT for real-time — they trade latency for cost.</div>

### Implementation

```python
# Step 1: Build the request list
requests = []
for i, doc in enumerate(documents):
    requests.append({
        "custom_id": f"doc-{i}",  # YOUR tracking ID - echoed in results
        "params": {
            "model": "claude-sonnet-5-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": f"Classify: {doc}"}]
        }
    })

# Step 2: Submit the batch (a list of requests, each with its own custom_id)
batch = client.messages.batches.create(requests=requests)

# Step 3: Poll until processing has ended, then read results (custom_id maps back to your data)
for r in client.messages.batches.results(batch.id):
    print(f"{r.custom_id}: {r.result.type}")  # succeeded / errored / canceled / expired
```

---

## 5.7 Retry & Rate Limiting

### 📖 Story: "The Retry Loop From Hell"

An engineer's code retried every failed API call. Worked great for 429s (rate limits) — backoff, retry, succeed. Then one day, a malformed request started returning 400 (Bad Request). The code retried it. And retried. And retried. 5 retries x exponential backoff = 63 seconds of waiting for a request that would *never* succeed. Multiply by 10,000 concurrent users. The retry queue grew until the service OOM-crashed. The fix: <mark>don't retry client errors such as 400, 401, or 403</mark>; they mean YOUR request is broken. 429 is the exception: it's a 4xx code that means "slow down", so you back off and retry.

<div class="note-important"><strong>The Golden Rule of Retries:</strong> 429 and 5xx = retry with backoff. Other 4xx (400, 401, 403, 404) = do NOT retry; fix the request. Rate limits are out of scope for the exam, but the retry logic shows up in reliability questions.</div>

### Mental Model: Traffic Lights

> 429 = red light at a busy intersection. Wait, try again, you'll get through. 5xx = road construction. Come back in a few minutes. 4xx = you're driving the wrong way on a one-way street. No amount of waiting fixes that — turn around (fix your request).

![Flow diagram for "Mental Model: Traffic Lights": 200 OK, 429 Rate Limit, 5xx Server Error, Other 4xx Client Error, Yes, No, API Call, Response?, Success, Retries left?](/content/skillup/ccaf/images/d5-context-management-m6.svg)
<!-- diagram source: scripts/diagrams/mermaid/ccaf/d5-context-management-m6.mmd -->

### Exponential Backoff + Jitter Pattern

```python
import time, random
from anthropic import RateLimitError, APIError

def call_with_retry(client, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except RateLimitError:
            if attempt == max_retries - 1: raise
            delay = 2**attempt + random.uniform(0, 2**attempt * 0.5)
            time.sleep(delay)  # 1s, 2s, 4s, 8s, 16s (with jitter)
        except APIError as e:
            if e.status_code >= 500:  # Server error = retry
                time.sleep(2**attempt)
            else:
                raise  # Client error (400, 401, 403) = don't retry!
```

<div class="note-scribble">Jitter prevents the "thundering herd" — if 1000 clients all back off to exactly 4 seconds, they all slam the server simultaneously at t+4s. Random jitter spreads them out.</div>

### Rate Limit Headers

```
x-ratelimit-remaining-requests: 847   <-- How many requests left
x-ratelimit-remaining-tokens: 62000   <-- Token budget remaining
x-ratelimit-reset-requests: 2025-...  <-- When request limit resets
```

### Key Rules

| Status | Action | Mental Model |
|----|----|------|
| 429 (Rate Limited) | Retry with exponential backoff + jitter | Red light — wait your turn |
| 500-599 (Server Error) | Retry with backoff | Road construction — try later |
| Other 4xx (400, 401, 403...) | **Do NOT retry** — fix the request | Wrong way — turn around |

<div class="note-trap"><strong>TRAP:</strong> "Your API returns 401 Unauthorized intermittently. What should you do?" The answer is NOT "add retry logic." 401 is a 4xx — it means your API key is wrong or expired. Fix the credential, don't retry.</div>

---

## 5.8 Token Budget Management

### 📖 Story: "The Surprise $800 Bill"

A dev team tested their agent in development with short prompts. Worked great. In production, real users sent long messages with pasted documents. One user pasted a 50-page contract into a single message. The agent processed it (120K input tokens), generated a long analysis (4K output tokens), then the conversation continued for 15 turns — each turn re-sending the growing history. The monthly bill hit $800 before anyone noticed.

The fix: monitor `response.usage` after every call, set budget alerts, and implement progressive summarization when token count exceeds a threshold.

### Usage from API Response

```python
response = client.messages.create(...)
print(response.usage.input_tokens)              # Tokens you sent
print(response.usage.output_tokens)             # Tokens Claude generated
print(response.usage.cache_read_input_tokens)   # Tokens served from cache
print(response.usage.cache_creation_input_tokens)  # Tokens written to cache
```

### Estimation Rule of Thumb

```
Current tokenizer (Claude Opus 4.7 and later): 1M tokens ≈ 555k words ≈ 2.5M characters
Older models: 1M tokens ≈ 750k words
```

<div class="note-scribble">Quick math: current Claude models have a 1M-token context window, roughly 555,000 words on the current tokenizer. Token counting specifics are out of scope for the exam; what matters is that every resent turn and every verbose tool result consumes budget.</div>

<div class="note-important"><strong>Always check response.usage after API calls.</strong> The usage object tells you exactly what you spent. Use it for budget monitoring, alerting, and deciding when to trigger summarization.</div>

---

## 5.9 Updated Caching & Batches (2026)

### 📖 Story: "The Cache That Pre-Warmed Itself"

A SaaS platform served 500 users who all hit the same legal-AI feature. Each request sent a 30K-token system prompt. The first user every morning paid the cache-write cost and experienced ~2 seconds of extra latency. The team added a cache pre-warming call at application startup — `max_tokens: 0` — so the cache was hot before any user arrived. First-user latency dropped by 40%.

### Automatic Caching (Simplest Approach)

Instead of manually placing `cache_control` on individual blocks, add it at the top level:

```python
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # Top-level: auto-caches last block
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "My name is Alex."},
        {"role": "assistant", "content": "Hello Alex!"},
        {"role": "user", "content": "What's my name?"},
    ],
)
```

The system automatically places the cache breakpoint on the last cacheable block and moves it forward as conversations grow.

<div class="note-scribble">Auto-caching is the "set it and forget it" option. Manual breakpoints give more control but auto works great for conversational agents.</div>

### Cache Pre-Warming (Latency Optimization)

**Use Case: "Zero-Latency Startup"**

Warm the cache BEFORE users arrive using `max_tokens: 0`:

```python
# Fire at application startup - no output generated, no output tokens billed
prewarm = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=0,  # Zero output = cache write only
    system=[{
        "type": "text",
        "text": "Your large system prompt...(5K+ tokens)...",
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "warmup"}],
)
# prewarm.stop_reason == "max_tokens", prewarm.content == []
```

<div class="note-trap"><strong>TRAP:</strong> max_tokens: 0 is rejected inside the Message Batches API (an ephemeral cache entry written during batch processing would likely expire before the follow-up request runs). Check the prompt caching docs for its other restrictions.</div>

<div class="note-important"><strong>max_tokens: 0 produces no output.</strong> stop_reason will be "max_tokens" and content will be an empty array. You're paying only for the cache write — no output tokens billed.</div>

### 1-Hour Cache Duration

**Use Case: "The Slow-Turn Agent"**

For agents where users take >5 minutes between interactions (think: agentic side-agents doing research, or a human reviewing a document between turns), the default 5-minute TTL causes constant cache misses:

```python
"cache_control": {"type": "ephemeral", "ttl": "1h"}  # 2x base input cost
```

| TTL | Write Cost | Read Cost | When to Use |
|---|-----|-----|-----|
| 5 min (default) | 1.25x | 0.1x (0.05x on Opus 5.5 / Sonnet 5.5) | Rapid multi-turn, frequent reuse |
| 1 hour | 2x | same as 5 min | Agentic side-agents, slow user turns, batches with shared context |

<div class="note-trap"><strong>TRAP:</strong> The 1-hour TTL costs 2x on write (not 1.25x). Read pricing is the same as for the 5-minute cache.The exam may ask "what's the cost difference between 5-min and 1-hour caching?" — the answer is only the write cost changes.</div>

### Updated Cache Properties (2026) — <mark>Full Reference</mark>

| Property | Value |
|----|---|
| Default TTL | <mark>**5 minutes**</mark> (refreshed on each hit) |
| Extended TTL | <mark>**1 hour**</mark> (at 2x write cost) |
| Min tokens (current models: Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1) | <mark>**512 tokens**</mark> |
| Min tokens (older models) | 1,024 (e.g. Sonnet 4.5/4.6, Opus 4.8), 2,048 (Opus 4.7), 4,096 (Opus 4.5/4.6, Haiku 4.5) |
| Max breakpoints | <mark>**4 per request**</mark> |
| Cache write cost | **1.25x** (5-min) or **2x** (1-hour) |
| Cache read cost | **0.1x** on most models; 0.05x Opus 5.5 / Sonnet 5.5; 0.025x Fable 5.1 |

<div class="note-important"><strong>Minimum cacheable length differs by model.</strong> If the prompt up to your breakpoint is shorter than the minimum, it isn't cached and no error is returned.</div>

---

## Cheat Sheet

<div class="note-scribble">Print this page. Stick it on your monitor the night before the exam. These are the numbers they test.</div>

| Concept | Key Fact | Mental Model |
|---|----|------|
| Lost-in-the-middle | Put critical info at START + END; middle gets less attention | U-shaped bathtub |
| Summarization rule | NEVER round/approximate specific values — preserve verbatim | Filing, not shredding |
| Tool result trim | Return summary + pagination, not raw 10K rows | Librarian, not dump truck |
| Escalation triggers | Customer asks for a human, policy gap/exception, no meaningful progress (not sentiment or self-rated confidence) | Receptionist, not a panic button |
| Cache TTL | 5 minutes (refreshed on hit) | Name badge — unused ones expire |
| Cache minimum | 512 tokens on current models; up to 4,096 on some older ones | — |
| Cache breakpoints | Max 4 per request | — |
| Cache savings | Reads at 0.1x on most models (0.05x Opus 5.5 / Sonnet 5.5) | First badge costs time, rest free |
| Extended cache | 1-hour TTL at 2x write cost | — |
| Pre-warming | max_tokens: 0 (not supported inside batches) | Heating the oven before cooking |
| Batches API | 100K requests, 50% cost, up to 24h processing | Ground shipping |
| Batches custom_id | Your tracking key — echoed back in results | Your label on the package |
| Retry: 429 | Exponential backoff + jitter | Red light — wait |
| Retry: other 4xx | Do NOT retry (fix the request) | Wrong way — turn around |
| Retry: 5xx | Retry with backoff | Road construction — try later |
| Context window | 1M tokens on current models (~555k words) | — |

---

### Exam Day Quick-Fire

1. **Where does critical info go?** Start and end (never middle)
2. **Summarization loses an order ID — what went wrong?** Missing "preserve verbatim" instruction
3. **Cache TTL expired — why?** No hits for 5+ minutes (or 1hr for extended)
4. **50% cost reduction but async?** Batches API
5. **API returns 400 — retry?** NO. Fix the request.
6. **max_tokens: 0 — what does it do?** Cache pre-warming (no output generated)
7. **Can max_tokens: 0 run inside a batch?** NO.
8. **Minimum cacheable prompt on current models?** 512 tokens (higher on some older models)
9. **How many cache breakpoints max?** 4 per request
10. **custom_id in batches — who sets it?** YOU (the developer), not Anthropic

---

## 5.10 Error Propagation Across Multi-Agent Systems

### Key Concept

**Recover locally when you can; when you can't, tell the coordinator exactly what failed, what you tried, and what you still have.**

A subagent should handle transient failures itself (retry, alternate source) and propagate only what it can't resolve, as structured context: failure type, the query it attempted, partial results, and possible alternatives. That lets the coordinator retry with a modified query, try another source, or proceed with partial results.

Two anti-patterns sit on either side. Suppressing an error by returning empty results marked as success makes the coordinator reason from false data; terminating the whole workflow on a single failure throws away everything that worked. **Report errors like a field medic's tag: what happened, what was done, what's still needed.**

### In Practice

**What breaks without this**: A timeout comes back as `{"results": []}`, and the final report confidently says no evidence exists. Or a generic "search unavailable" status hides that the failure was a single malformed query.

**Decision trigger**: Ask whether the coordinator could make a good next decision from the error alone. If not, add the missing fields, and keep "access failed" distinct from "query succeeded with no matches".

**When you'd choose differently**: When a source is down for the whole run, finish anyway and annotate the synthesis with coverage gaps (which findings are well supported, which areas lack sources) rather than blocking.

### Exam Trap ⚠️

<div class="note-trap">Generic retry-then-"unavailable" (hides context), empty-success (suppresses the error), and terminate-everything (over-reacts) are all wrong. The answer is structured error context plus partial results, and coverage annotations in the final output.</div>

---

## 5.11 Context in Large Codebase Exploration

### Key Concept

**Long explorations degrade; persist what you learn outside the conversation and delegate the noisy parts.**

In extended sessions, models start giving inconsistent answers and refer to "typical patterns" instead of the specific classes they found earlier. That's context degradation. Counter it with scratchpad files that record key findings, subagents that investigate specific questions ("find all test files", "trace refund flow dependencies") and return summaries, and `/compact` when the window fills with verbose discovery output.

Between phases, summarize what you've learned and inject that summary into the next phase's subagents. For crash recovery, have each agent export its state to a known location and let the coordinator load a manifest on resume and inject the relevant state into each agent's prompt. **Treat the context window as working memory and the scratchpad as the lab notebook: the notebook survives when memory doesn't.**

### In Practice

**What breaks without this**: Two hours in, the agent contradicts what it established in the first twenty minutes, and a crash means starting the whole analysis again.

**Decision trigger**: When answers start drifting toward generic patterns, or before spawning the next phase of subagents, write the findings down and pass the summary forward.

**When you'd choose differently**: If prior tool results are mostly still valid, resume the session and tell it which files changed; if they're stale, start a fresh session seeded with a structured summary.

### Exam Trap ⚠️

<div class="note-trap">"Use a model with a larger context window" and "lower the temperature" don't fix context degradation. Scratchpad files, subagent delegation, phase summaries, and <code>/compact</code> do. For crash recovery, the answer is exported state plus a manifest the coordinator loads on resume.</div>

---

## 5.12 Human Review Workflows and Confidence Calibration

### Key Concept

**An aggregate accuracy number can hide a broken segment; measure by document type and field before you automate.**

A pipeline that is 97% accurate overall may be failing badly on one document type or one field. Validate accuracy by segment before reducing human review, and keep measuring with **stratified random sampling** of high-confidence extractions, which estimates error rates per segment and surfaces novel error patterns.

Field-level confidence scores are useful only once they're calibrated against a labelled validation set (items marked ~80% confident should be right ~80% of the time). Then route low-confidence fields, and documents with ambiguous or contradictory sources, to human reviewers, so their limited time goes where errors are likely. **Calibrated confidence is a triage nurse; uncalibrated confidence is a patient diagnosing themselves.**

### In Practice

**What breaks without this**: Human review is cut back because "accuracy is 97%", and handwritten invoices, 5% of volume, quietly go wrong for months.

**Decision trigger**: Before auto-accepting any class of extraction, ask for accuracy broken down by document type and field, and for the calibration curve of the confidence scores.

**When you'd choose differently**: Reviewing only low-confidence items misses confident-but-wrong errors, so keep a stratified sample of high-confidence items under review too.

### Exam Trap ⚠️

<div class="note-trap">"Overall accuracy is high, so remove human review", "trust the model's self-reported accuracy", and "review only items that failed schema validation" are distractors. The answers are segment-level accuracy, stratified sampling, and confidence calibrated on labelled data.</div>

---

## 5.13 Provenance and Uncertainty in Multi-Source Synthesis

### Key Concept

**Every claim should arrive at the final report still attached to its source, its date, and any disagreement.**

Source attribution is lost when findings are summarized without claim-source mappings. Require subagents to output structured mappings (claim, excerpt, source URL or document name, page, publication or collection date) and require the synthesis agent to preserve and merge them.

When credible sources conflict, annotate the conflict with both values and their sources rather than picking one; dates often explain apparent contradictions (different collection years). Structure reports to separate well-established findings from contested ones, and render each content type in its natural form: financial data as tables, news as prose, technical findings as lists. **A good report is a court transcript, not a rumour: who said what, when, and where they disagree.**

### In Practice

**What breaks without this**: The final report states one market-size figure with no citation, when two sources disagreed and one of them was five years older.

**Decision trigger**: Ask whether a reader could trace every number back to its source and date. If not, fix the subagent output schema first.

**When you'd choose differently**: If the coordinator must reconcile conflicts (for example, a policy that the most recent official figure wins), let the analysis step flag conflicts and leave the decision to the coordinator before synthesis.

### Exam Trap ⚠️

<div class="note-trap">"Average the two figures", "pick the more recent value silently", and "summarize sources into one blended paragraph" all destroy provenance. The answer keeps both values with attribution and dates, and labels the finding as contested.</div>

---

## Deep Dive

### 1. The connective narrative

Domain 5 is about keeping an agent **honest over time**. Context is finite and attention is uneven: models handle the start and end of long inputs better than the middle, summaries quietly round away the numbers customers care about, and verbose tool results crowd out reasoning. So you keep transactional facts in a persistent "case facts" block, trim tool output to the fields that matter, put key findings first, and use headers to organize the rest.

Reliability then extends outward. Escalation follows explicit criteria rather than mood or self-rated confidence, and ambiguity is resolved by asking, not guessing. Errors travel as structured context, so a coordinator can recover rather than collapse. Long explorations survive through scratchpads, phase summaries, and manifests.

Finally, trust is earned with measurement: accuracy by segment, stratified sampling, calibrated confidence for routing human review, and provenance that keeps every claim tied to its source and date. Caching and batching are the cost levers around all of this, but the exam treats them lightly; the reliability patterns carry the weight.

### 2. Worked scenario

> **Scenario.** A multi-issue support agent forgets a customer's order number after summarization, escalates every frustrated customer, and its monthly accuracy report says 96% while one document type is failing.
>
> **Step 1 — persist facts.** Extract order IDs, amounts, dates, and statuses into a case-facts block sent with every prompt, outside the summarized history.
>
> **Step 2 — trim tools.** Keep only the five return-relevant fields from the 40-field order lookup before it enters context.
>
> **Step 3 — fix escalation.** Replace the sentiment trigger with explicit criteria and few-shot examples; honour explicit requests for a human immediately; ask for another identifier when lookups return multiple customers.
>
> **Step 4 — measure honestly.** Break accuracy down by document type and field, sample high-confidence items per segment, and calibrate field-level confidence before deciding what to auto-accept.
>
> **Outcome:** no more lost order numbers, fewer unnecessary escalations, and a review process that finds the failing segment instead of averaging it away.

### 3. Memory aid

**FACTS** — Domain 5 in five moves:
- **F**acts block: amounts, dates, IDs kept outside summaries
- **A**ttention-aware ordering: key findings first, headers for the rest
- **C**riteria for escalation, not sentiment or self-rated confidence
- **T**raceable claims: sources, dates, conflicts preserved
- **S**egmented measurement: stratified sampling, calibrated confidence

### 4. Exam strategy for this domain

- When a question mentions summaries losing detail, the answer preserves specifics verbatim or moves them out of the summarized history.
- "Overall accuracy is high" in a stem is a warning sign; look for the option that segments the metric.
- Escalation questions punish both over-escalation (sentiment) and under-escalation (ignoring explicit requests or policy gaps).
- Five minutes before the exam: **keep the facts, show the sources, measure by segment, escalate on criteria.**
