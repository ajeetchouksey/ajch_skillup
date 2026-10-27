# Domain 4: Apply Prompt Engineering and Context Crafting

> **Exam Weight:** 13% | **GH-300 GitHub Copilot Certification**

---

## Overview

Prompt engineering is the practice of crafting inputs to AI models to maximize the quality and relevance of their outputs. For GitHub Copilot, effective prompting means providing the right context, specificity, and structure so Copilot can generate accurate, useful code suggestions.

---

## 1. Prompt Structure and Elements

### Key Concept

**A strong prompt states context, intent, constraints and output format. Copilot fills in only what you leave out.**

GitHub's prompt-engineering guidance starts with the shape of the request. State the broad goal first, then list specific requirements in order of importance, and name the exact functions, files or libraries involved. Each element you leave out becomes a guess, and guesses come from the most common pattern in the training data, not from your codebase.

Specific doesn't mean long. One precise line about input types, return shape and error behaviour beats a paragraph of background. **Think of a prompt as a work ticket for a contractor**: "fix the kitchen" gets you something; "replace the left tap, chrome, keep the existing pipes" gets you what you wanted.

### In Practice

**What breaks without this**: A comment like `# process data` produces a plausible function with invented field names and no error handling. It passes a glance and fails on real records.

**Decision trigger**: Before sending, ask "could a new teammate implement this from my prompt alone?" If they would have to ask about inputs, outputs or edge cases, Copilot is guessing at them too.

**When you'd choose differently**: For exploratory questions ("what are the options for caching here?") start broad on purpose and narrow down in follow-up turns. Over-constraining too early hides alternatives.

### Exam Trap ⚠️

<div class="note-trap">
"Longer prompts always give better results" is a distractor. The guidance rewards <b>specific and unambiguous</b>, not long. Unrelated context dilutes the signal and uses up the context window.
</div>

### The Anatomy of an Effective Copilot Prompt

An effective prompt has four elements:

| Element | Description | Example |
|---------|-------------|---------|
| **Context** | What you're working on | "In a FastAPI application..." |
| **Intent** | What you want Copilot to do | "...generate a function that..." |
| **Constraints** | Requirements and restrictions | "...handles authentication via JWT..." |
| **Format** | Expected input/output shape | "...returns `Dict[str, Any]` with user data" |

### Example: Poor vs. Effective Prompt

```python
# ❌ POOR — too vague
# Process data

# ✅ EFFECTIVE — specific, contextual
# Process a List[Dict[str, Any]] of sales records.
# Each record has: id (str), amount (float), currency (str: 'USD'|'EUR'|'GBP'), date (ISO 8601).
# Convert all amounts to USD using rates: EUR=1.09, GBP=1.27.
# Return Dict[str, float] mapping date (YYYY-MM-DD) to total USD amount.
# Raise ValueError if unsupported currency encountered.
```

---

## 2. How Copilot Determines Context

### Key Concept

**Copilot builds context from what's near the cursor and what you attach, so curating that context is part of prompting.**

For inline suggestions, Copilot reads the code before and after the cursor, the file name and language, and related open tabs. In chat you can steer it further. Attach files, folders or symbols with `#`, select code, ask for a `#codebase` search, and rely on repository custom instructions such as `.github/copilot-instructions.md`.

Implicit signals count as much as explicit ones. Descriptive names, type annotations and a consistent style are themselves context, which is why GitHub lists "follow good coding practices" as a prompting strategy. **Think of your codebase as the briefing pack Copilot reads before answering**: a tidy pack gets a sharper answer.

### In Practice

**What breaks without this**: Copilot suggests a generic `User` shape because the real `UserRecord` interface sat in a closed file. The code compiles in a loosely typed language and corrupts data at runtime.

**Decision trigger**: Ask "where does the truth for this task live?" If it's in one or two known files, attach them. If you don't know, use `#codebase` or let agent mode search.

**When you'd choose differently**: For a self-contained, well-known task (for example validating an email format) extra context adds nothing. Close irrelevant tabs instead of attaching more.

### Exam Trap ⚠️

<div class="note-trap">
"Copilot automatically uses every file in the repository" is wrong. Inline suggestions use the current file and related open tabs. Wider workspace context comes from <b>explicit</b> search such as <code>#codebase</code>, or from an agent choosing to search.
</div>

### Context Sources (in priority order)

```
1. Current file content (before and after cursor; Fill-in-the-Middle)
2. Neighboring open tabs, file name/type, project structure
3. Custom instructions (.github/copilot-instructions.md, *.instructions.md, AGENTS.md)
   added automatically where the surface supports them
4. Explicit chat context: #<file>, #<folder>, #<symbol>, #selection
5. Workspace search: #codebase (older: @workspace participant)
6. Chat history (previous turns in the current conversation)
```

> These are sources, not a strict documented priority order. Copilot assembles and trims them to fit the model's context window.

### Best Practices for Context Optimization

**Open relevant files as tabs:**
- Type definitions / interfaces
- Example implementations following the desired pattern
- Related utilities and helpers

**Use descriptive naming:**
```python
# Good naming provides context implicitly:
def calculate_compound_interest(principal: float, annual_rate: float, years: int) -> float:
    # Copilot understands exactly what this should do from the name alone

# vs.
def calc(p, r, n):  # Copilot has no context
```

**Include type annotations:**
```typescript
// TypeScript interfaces help Copilot understand data shapes:
interface TransactionRecord {
  id: string;
  amount: number;
  currency: 'USD' | 'EUR' | 'GBP';
  timestamp: Date;
}

// Now Copilot can generate type-safe transformations
function aggregateByMonth(transactions: TransactionRecord[]): Map<string, number> {
  // Copilot suggestion will be correctly typed
}
```

---

## 3. Prompting Techniques

### Key Concept

**Zero-shot gives no examples, one-shot gives one, few-shot gives several. The name counts examples, not words.**

Zero-shot works when the task is common and the model already knows the pattern. Few-shot works when your convention is unusual, such as a house date format or an internal error envelope. Showing two or three input/output pairs pins the pattern down better than describing it. GitHub's guidance also suggests unit tests as a form of example.

Other techniques sit beside these. Role prompting frames the perspective ("review as a security engineer"), and breaking a complex task into simpler steps keeps each response focused. **Think of few-shot examples as showing the tailor a suit you already own**: faster and more accurate than describing the cut in words.

### In Practice

**What breaks without this**: Asking zero-shot for "our standard API error format" gets a generic `{ "error": "..." }`, because Copilot has never seen your format. Every endpoint then needs fixing by hand.

**Decision trigger**: Ask "is this pattern specific to us?" If yes, paste examples (few-shot). If no, a clear zero-shot instruction is enough.

**When you'd choose differently**: If the pattern already appears in open files or custom instructions, Copilot can pick it up without inline examples. Put repeated conventions in `.github/copilot-instructions.md` rather than re-pasting examples in every prompt.

### Exam Trap ⚠️

<div class="note-trap">
"Zero-shot means sending no prompt" and "few-shot means one example" are both wrong. Zero-shot still has an instruction, just <b>no examples</b>. One example is <b>one-shot</b>. Few-shot is several examples (commonly two to five).
</div>

### Zero-Shot Prompting

Asking Copilot to perform a task **without providing any examples**. Relies entirely on Copilot's pre-trained knowledge.

**When to use:** Common, well-understood tasks (sort an array, validate an email, fetch from an API).

```python
# Zero-shot: no examples needed — Copilot knows this pattern
# Validate an email address using RFC 5321 format rules. Return bool.
def validate_email(email: str) -> bool:
```

### Few-Shot Prompting

Providing **several concrete examples** (commonly two to five) of the desired input/output pattern before requesting the new completion.

**When to use:** Non-standard, domain-specific, or organization-specific patterns.

```python
# Few-shot: showing examples of the desired transformation pattern

# Example 1:
# Input: "2024-01-15T10:30:00Z" → Output: "Jan 15, 2024 at 10:30 AM UTC"

# Example 2:
# Input: "2024-06-20T14:00:00Z" → Output: "Jun 20, 2024 at 2:00 PM UTC"

# Now apply the same pattern:
def format_timestamp_for_display(iso_timestamp: str) -> str:
    # Copilot infers the exact formatting pattern from examples
```

### Role Prompting

Asking Copilot to adopt an expert persona.

```
"Act as a security engineer reviewing this authentication middleware 
for OWASP Top 10 vulnerabilities. Identify specific risks and 
suggest concrete remediation for each finding."
```

### Single-Responsibility Prompting

Breaking complex tasks into focused, sequential prompts.

```
# Instead of: "Build a complete user authentication system with 
#              registration, login, JWT tokens, refresh tokens, 
#              and rate limiting"

# Do this sequentially:
# Step 1: Generate the User model with password hashing
# Step 2: Generate the JWT token generation utilities  
# Step 3: Generate the login endpoint with credential validation
# Step 4: Generate the refresh token endpoint
# Step 5: Generate the rate limiting middleware
```

---

## 4. Chat Context Variables

### Key Concept

**In chat, `#` references attach precise context. Choose a file when you know where the answer is, and a search when you don't.**

VS Code's current chat model is "attach context with `#`". `#<file>`, `#<folder>` and `#<symbol>` attach items. `#selection` adds the editor selection. `#codebase` runs a workspace code search, and tools such as `#fetch` and `#githubRepo` bring in web and GitHub content. The older `@workspace`, `@vscode` and `@terminal` chat participants are deprecated in VS Code and not supported in its Copilot harness, though you'll still see them in older material and exam questions.

The skill being tested is choosing the narrowest reference that answers the question. A targeted file reference keeps noise out of the context window, and a search finds what you can't name. **Think of `#file` as handing over a specific page and `#codebase` as asking the librarian to search the stacks.**

### In Practice

**What breaks without this**: A developer asks "why does checkout fail?" with no context. Copilot answers from general knowledge about checkout flows instead of the team's actual `checkout.service.ts`.

**Decision trigger**: Ask "can I name the file or symbol?" If yes, attach it with `#`. If no, use `#codebase` (or `@workspace` on surfaces that still support it), or switch to agent mode and let it search.

**When you'd choose differently**: For questions about GitHub objects (issues, pull requests) use **Add Context** or paste the URL. For live web content, use `#fetch` or include the URL rather than a workspace search.

### Exam Trap ⚠️

<div class="note-trap">
"<code>@workspace</code>/<code>#codebase</code> attaches the entire repository to the prompt" is wrong. They search the workspace and add the <b>relevant</b> results. A workspace index helps find code but doesn't attach every file. Neither of them searches the public internet.
</div>

### Available Context References in Copilot Chat

| Reference | Description | When to Use |
|-----------|-------------|-------------|
| `#<file>` / `#<folder>` (e.g. `#file:auth.ts`) | Attach a specific file or folder | Known file, targeted question |
| `#<symbol>` | Attach a code symbol (open its file first) | Question about one function/class |
| `#selection` | Attach the current editor selection | Code-specific questions |
| `#codebase` | Search the workspace for relevant code (doesn't attach every file) | Discovery and architecture questions |
| `#fetch` / a URL | Bring in web page content | Current external docs |
| `#githubRepo` | Search a GitHub repository (`owner/repo`) | Code in another repo |
| `#problems`, `#changes`, `#terminalSelection`, `#terminalLastCommand` | Diagnostics, source-control changes, terminal content | Fixing errors, reviewing diffs, shell help |
| `@workspace`, `@vscode`, `@terminal` | **Chat participants, now deprecated in VS Code** (not supported in its Copilot harness) | Still seen in older docs and exam items: `@workspace` ≈ workspace search |

Source: [VS Code: Manage context for AI](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context) and [VS Code tools and context reference](https://code.visualstudio.com/docs/agents/reference/tools-reference). VS Code's newest UI shows some tools with prefixes (for example `#search/codebase`, `#web/fetch`).

### When to Use `#file` vs. `#codebase` / `@workspace`

| Use `#file` when... | Use `#codebase` (or `@workspace`) when... |
|---------------------|------------------------|
| You know exactly which file contains the context | You need to discover where something is defined |
| You want precise, targeted context | You're asking about patterns across the codebase |
| You need to reference a specific API or type | You want Copilot to find the relevant context itself |

---

## 5. Chat History Usage

### Key Concept

**Chat history is context too: it helps follow-ups and pollutes new tasks. Keep it relevant.**

Within a conversation, earlier turns go back to the model, so you can say "add error handling to the function we just wrote" and Copilot resolves the reference. That's the payoff of iterating in one thread: each refinement builds on the last.

The cost is that stale or unrelated turns still use the context window and can steer answers. GitHub's guidance is to start a new conversation for a new task and remove outdated turns where the surface allows. In VS Code, `/clear` starts fresh and `/compact` summarises a long conversation. **Think of chat history as a whiteboard**: great while you're on one problem, and something to wipe before the next meeting.

### In Practice

**What breaks without this**: After an hour of debugging a Python service, a developer asks for a Go CLI in the same thread. The answer borrows Python-isms and the earlier service's naming.

**Decision trigger**: Ask "does anything earlier in this thread help with my next request?" If not, start a new conversation.

**When you'd choose differently**: For a long multi-step build on one feature, keep the thread and compact it when it gets long, rather than losing accumulated decisions by starting over.

### Exam Trap ⚠️

<div class="note-trap">
"Copilot remembers every previous conversation automatically" is a distractor. Chat history is scoped to the conversation. Starting a new chat (or <code>/clear</code>) gives a clean context. Persistent conventions belong in custom instructions, not in old chats.
</div>

### How Chat History Works

- Each Copilot Chat session maintains conversation history
- Previous messages and responses are included in subsequent prompts
- Copilot uses history to maintain coherence and resolve references ("it", "the function we discussed")
- **Starting a new conversation clears history**, so do that for unrelated tasks (in VS Code: new chat or `/clear`; `/compact` summarises a long thread)

### Effective History Management

```
Session 1: "I'm working on the order processing pipeline"
→ Copilot has order processing context for the rest of this session

Later: "Add error handling to the processor we just built"
→ Copilot knows "the processor" from chat history

New task: Start a NEW conversation to avoid old context polluting new task
```

---

## 6. The Prompt Process Flow

### Key Concept

**A prompt goes in through secure transmission, context gathering, proxy and toxicity filters, then the model. It comes out through post-processing and checks.**

Microsoft Learn describes the inbound flow as: secure HTTPS transmission and context gathering (code around the cursor, file name and type, open tabs, project structure, Fill-in-the-Middle pre-processing), a proxy in a GitHub-owned Azure tenant that blocks prompt hacking, toxicity filtering (hate speech, inappropriate content, personal data), and finally code generation by the LLM.

The outbound flow runs post-processing: a toxicity filter, code-quality checks such as XSS and SQL injection, and optional public-code matching. Responses that fail are truncated or discarded, and only what passes is delivered. **Think of it as a newspaper's editorial desk**: the story is gathered, written, then checked before it goes to print.

### In Practice

**What breaks without this**: Without the flow in mind, developers assume a blocked or truncated answer is a model failure and keep rephrasing. Often a filter, such as the public code filter, removed a near-verbatim match.

**Decision trigger**: When a response is missing or cut short, ask "which stage might have removed it?" If the request asked for well-known public code verbatim, rephrase it towards your own implementation.

**When you'd choose differently**: In agent workflows the flow repeats per step, with tool calls between model turns. Reason about each step's context rather than one single prompt.

### Exam Trap ⚠️

<div class="note-trap">
Watch the order. Filtering happens on <b>both</b> sides of the model: proxy and toxicity filters inbound, toxicity, code-quality and public-code checks outbound. Answers that put the public code filter before generation, or claim prompts go straight to the model, are wrong.
</div>

### End-to-End Process

```
INBOUND
1. Developer types a chat message or a code comment
   ↓
2. Secure transmission (HTTPS) + context gathering
   (code before/after cursor, file name/type, open tabs, project structure,
    attachments, custom instructions, chat history; FIM pre-processing)
   ↓
3. Proxy filter (GitHub-owned Azure tenant): blocks prompt-hacking attempts
   ↓
4. Toxicity filtering: hate speech, inappropriate content, personal data
   ↓
5. LLM generates the response
OUTBOUND
6. Post-processing: toxicity filter, code-quality checks (e.g. XSS, SQL injection),
   optional public-code matching (~150 chars); failures truncated or discarded
   ↓
7. Suggestion/response delivered; your accept/edit/reject feeds the loop
   ↓
8. Developer reviews, iterates if needed
```

Source: [Microsoft Learn: GitHub Copilot user prompt process flow](https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/3-github-copilot-user-prompt-process-flow)

---

## Prompt Engineering Best Practices Summary

| Practice | Impact |
|----------|--------|
| **Be specific about inputs and outputs** | High — dramatically improves suggestion accuracy |
| **Use descriptive variable/function names** | High — implicit prompt engineering at no extra cost |
| **Include type annotations** | High — enables type-safe suggestions |
| **Open relevant neighboring files** | Medium — provides context about patterns and types |
| **Use single-responsibility prompts** | Medium — focused prompts outperform multi-task prompts |
| **Provide examples for non-standard patterns** | High (when needed) — few-shot learning is effective |
| **Iterate and refine** | High — first attempt isn't always optimal |
| **Use `#file` references for precision** | Medium. Avoids adding noise from irrelevant files |
| **Keep history relevant** | Medium. Start a new chat for a new task |
| **Review Copilot's output** | High. Test and verify before relying on it |

These mirror GitHub's documented strategies: start general then get specific, give examples, break complex tasks into simpler tasks, avoid ambiguity, provide relevant context, experiment and iterate, keep history relevant, review Copilot's output, and follow good coding practices ([GitHub Docs: Prompt engineering for GitHub Copilot Chat](https://docs.github.com/en/copilot/concepts/prompting/prompt-engineering)).

---

## Deep Dive: From Vague to Precise — an Iteration Walkthrough

The exam tests prompt engineering less as trivia and more as *judgement*: given a weak prompt and a goal, which change most improves the result? The skill is seeing **why** each refinement helps. Here is one worked scenario, with a single prompt evolving:

> **Attempt 1 (vague):** `# get users`
> Copilot has almost nothing to work with. It might return a bare `SELECT * FROM users` or an arbitrary function. The failure mode here is **under-specification** — no inputs, no outputs, no constraints.

> **Attempt 2 (add intent + shape):** `# Function get_active_users(db) that returns users where status == 'active', as a list of dicts.`
> Now Copilot knows the *name*, the *filter*, and the *return type*. Quality jumps because you supplied **intent and format**.

> **Attempt 3 (add constraints + edge cases):** `# get_active_users(db: Session) -> list[dict]. Return users with status=='active', ordered by created_at desc, limit 100. Exclude soft-deleted (deleted_at is not None). Raise ValueError if db is None.`
> This is production-grade. You've added **constraints** (ordering, limit), a **business rule** (soft-delete), and **error handling**. Copilot now generates something you can almost ship — because you did the thinking a senior engineer would do *before* writing code.

The lesson the exam rewards: **specificity about inputs, outputs, and constraints is the single biggest lever.** Longer isn't better — *more precise* is better. A rambling paragraph of unrelated context actually *hurts* by diluting the signal.

### Zero-shot vs. one-shot vs. few-shot — the distinction people fail

| Term | How many examples? | Use when |
|------|-------------------|----------|
| **Zero-shot** | **0 examples** (but you still write a prompt) | The task is common and well-understood |
| **One-shot** | **1 example** | You need to pin down a specific format |
| **Few-shot** | **Several examples (commonly 2–5)** | The pattern is domain-specific or unusual |

**Memory aid:** the number in the name = the number of *examples*, never the number of words. "Zero-shot" does **not** mean "no prompt" — it means "no worked examples." This exact confusion is a favourite trap.

### Implicit prompt engineering: the free win

The highest-value technique costs nothing extra: **good names and type annotations are themselves prompts.** `def calculate_compound_interest(principal: float, annual_rate: float, years: int) -> float:` tells Copilot everything; `def calc(p, r, n):` tells it nothing. On the exam, if two answers are "write more prose in the comment" vs. "add type annotations and descriptive names," the latter is usually the stronger, lower-cost choice.

### Memory aid: **SCOPE-H**

- **S**pecific: name functions, files, libraries; avoid ambiguity
- **C**ontext: attach the right files or selection; keep tabs relevant
- **O**utput format: state return types and shape
- **P**attern examples: few-shot when the convention is yours
- **E**ither split or iterate: break big tasks down, refine each step
- **H**istory hygiene: new chat for a new task

### Exam Strategy for Domain 4

- Map the term to the **example count**: zero=0, one=1, few=several. Expect at least one question probing this.
- Prefer answers that add **specificity (inputs/outputs/constraints)** over answers that just add length.
- `#codebase` (and the older `@workspace`) searches your **workspace**, never the internet. `#file` is for when you already know the file.
- Chat history is **session-scoped** — starting a new conversation is the correct move to prevent old context polluting a new, unrelated task.

---

## Key Exam Traps ⚠️

| Trap | Correct Answer |
|------|---------------|
| "Few-shot means providing 1 example" | Few-shot is **several examples** (1 is one-shot) |
| "Zero-shot means no prompt" | Zero-shot means **no examples** but you still write a prompt |
| "Longer prompts always produce better results" | Focused, shorter prompts often outperform noisy multi-task prompts |
| "Chat history persists across sessions" | Chat history is **session-scoped** — clears when new conversation starts |
| "`@workspace` / `#codebase` searches the internet" | They search your **workspace** only. Use `#fetch` or a URL for web content |
| "`@workspace` attaches every file" | It searches and adds **relevant** results; an index doesn't attach every file |

---

## Quick Reference

| Technique | Use When |
|-----------|---------|
| Zero-shot | Common, well-established patterns |
| Few-shot | Domain-specific or non-standard patterns |
| Role prompting | Expert review or specialized perspective needed |
| Single-responsibility | Complex multi-step tasks |
| `#file` / `#symbol` | You know exactly which file or symbol has the context |
| `#codebase` (older: `@workspace`) | You need Copilot to discover relevant context |
| Custom instructions | Conventions that should apply to every request |
| New conversation | Switching to an unrelated task (prevents context pollution) |
