# Domain 3: Understand GitHub Copilot Data and Architecture

> **Exam Weight:** 13% | **GH-300 GitHub Copilot Certification**

---

## Overview

This domain covers how GitHub Copilot processes data — from the moment a developer types in the IDE to the suggestion appearing on screen — and the fundamental architectural and LLM limitations developers must understand.

---

## 1. Data Flow Architecture

### Key Concept

**Your code never reaches a model directly: it passes a GitHub proxy and filters on the way in and out.**

The inbound trip starts in the IDE. Copilot gathers context around the cursor (code before and after it, the file name and type, open tabs, project structure), builds a prompt, and sends it over HTTPS to a proxy hosted in a GitHub-owned Microsoft Azure tenant. The proxy blocks prompt-hacking attempts, and content filters screen for harmful or offensive input before the LLM sees anything.

The outbound trip mirrors it. Generated text is filtered again for harmful content, checked for code-quality issues such as SQL injection or XSS, and optionally compared against public code, and anything that fails is truncated or discarded. **Think of the proxy as airport security that screens you on departure and again on arrival**: nothing boards the model unchecked, and nothing lands in your editor unchecked.

### In Practice

**What breaks without this**: Teams that picture Copilot as "IDE talks to the model" put controls in the wrong place. They expect the public code filter to stop secrets leaving the machine (it can't, because it runs on the response) or expect content exclusions to clean up responses (they work at context collection, before the prompt exists).

**Decision trigger**: Ask "am I trying to stop data going *out*, or stop a suggestion coming *back*?" Outbound means content exclusions and what's open in the editor. Inbound means the public code filter and your own review.

**When you'd choose differently**: Agentic surfaces such as agent mode, the CLI and the cloud agent also run tools and read files on their own, so the editor-context model undersells what they can see. There you reason about tool permissions and trusted directories as well as the prompt pipeline.

### Exam Trap ⚠️

<div class="note-trap">
Distractors often put the public code filter on the inbound side ("it stops code that matches public repos from being sent"). It runs during <b>post-processing</b>, on the model's suggestion. Remember: <i>exclusions guard the door out, the public code filter guards the door in.</i>
</div>

### The Copilot Data Pipeline

```
[Developer IDE]
      |
      | (1) Editor context collected
      v
[Copilot Extension/Plugin]
      |
      | (2) Context assembled into prompt
      v
[GitHub Copilot Proxy (GitHub servers)]
      |
      | (3) Safety filtering applied
      | (4) Prompt sent to LLM
      v
[Large Language Model]
      |
      | (5) Suggestions generated
      v
[GitHub Copilot Proxy]
      |
      | (6) Post-processing (public code filter, safety checks)
      v
[Developer IDE]
      |
      | (7) Suggestions displayed to developer
```

### Step-by-Step Breakdown

**Step 1: Context Collection**
The Copilot extension collects context from the IDE:
- Current file content (before and after cursor)
- Open neighboring tab files
- File language and type information
- Project structure, file paths, languages and frameworks
- Explicit chat context (attached `#` files, selection, `#codebase` search results) and chat history (for Copilot Chat)

**Step 2: Prompt Construction**
Context is assembled into a structured prompt sent to the model. The prompt includes:
- System instructions (Copilot behavior guidelines)
- Code context (current file, neighbors)
- User's explicit request (comment or chat message)
- Repository custom instructions (for example `.github/copilot-instructions.md`) where the surface supports them

**Step 3: Proxy and input filtering (pre-processing)**
The prompt travels over HTTPS to a proxy hosted in a GitHub-owned Microsoft Azure tenant, which:
- Blocks attempts to hack the prompt or make the system reveal how it generates suggestions
- Applies content filtering for hate speech, offensive or inappropriate content, and personal data

**Step 4: LLM Inference**
The filtered prompt is sent to a large language model. Copilot offers models from several providers, chosen by the user in the model picker or automatically (Auto). Don't memorise a single "Copilot model".

**Step 5 & 6: Post-processing**
Returned suggestions are filtered:
- **Toxicity filter**: Removes harmful or offensive generated content
- **Code quality checks**: Look for common bugs and vulnerabilities such as XSS or SQL injection
- **Public code matching (optional)**: When the policy blocks matches, suggestions that closely match public GitHub code (about 150 characters of surrounding context are compared) are suppressed. When it allows them, the suggestion is shown with a code reference.
- If a response fails these checks, it is truncated or discarded

**Step 7: Suggestion Display**
The processed suggestion is returned to the IDE as ghost text (inline) or a chat response.

---

## 2. Data Usage and Sharing Policies

### Key Concept

**Retention and training are separate questions, and the answers depend on your plan and the surface you use.**

Retention is about how long GitHub keeps prompts and responses, and it varies by surface. Microsoft Learn says Copilot in the code editor discards completion prompts once a suggestion is returned. Chat used outside the editor (github.com, GitHub Mobile, the CLI) keeps conversation history, because those features rely on thread history. GitHub's Copilot FAQ gives the Business and Enterprise defaults as: IDE prompts and suggestions not retained, prompts and suggestions from other access retained for 28 days, and user engagement data kept for two years.

Training is about whether interaction data improves GitHub's models. Since April 24, 2026, interaction data from Copilot Free, Pro and Pro+ is used for AI model training unless the user opts out. Copilot Business and Enterprise data is not used. **Think of retention as how long the receipt is kept and training as whether the shop studies your shopping basket**: two different policies, often confused.

### In Practice

**What breaks without this**: A contractor on a personal Copilot Pro plan works on client code and assumes the "Business never trains" rule covers them. It doesn't. Their interaction data is used for training by default unless they turn off **Allow GitHub to use my data for AI model training**.

**Decision trigger**: Ask two questions, in order. "Which plan is this seat on?" decides training. "Which surface is the developer using?" decides retention.

**When you'd choose differently**: If an organization needs a contractual guarantee rather than a personal setting, the answer is to give the contractor an org-assigned Business or Enterprise seat, not to rely on each individual opting out.

### Exam Trap ⚠️

<div class="note-trap">
"Copilot Business keeps chat history, so it trains on it" mixes up retention and training. Business and Enterprise data is <b>not used for model training</b>, whatever the retention window. Individual plans (Free/Pro/Pro+) <b>are</b> used for training by default since April 24, 2026, with an opt-out.
</div>

### What Data Is Transmitted?

| Data | Transmitted? | Notes |
|------|-------------|-------|
| Code context (current file) | Yes | Used for prompt construction |
| Open neighboring files | Yes | Included as context when relevant |
| Your prompt text | Yes | Sent to model for processing |
| Copilot suggestions | Yes (back to you) | Returned by model |
| User engagement data | Yes | Pseudonymous identifiers for interactions with Copilot (per GitHub's Copilot FAQ) |

### Data Retention

- **Code completions in the editor**: Prompts are discarded once a suggestion is returned ([Microsoft Learn: GitHub Copilot data](https://learn.microsoft.com/en-us/training/modules/introduction-prompt-engineering-with-github-copilot/4-github-copilot-data))
- **Chat outside the editor** (github.com, GitHub Mobile, CLI): prompts and suggestions are retained for 28 days, because these features rely on thread history. Copilot Chat on GitHub.com keeps messages for 28 days and stores up to 100 recent conversations ([Chat in GitHub](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-github)).
- **User engagement data**: kept for two years. **Feedback data**: stored for as long as needed for its intended purpose.
- These are the Business and Enterprise defaults in the FAQ on GitHub's [Copilot feature page](https://github.com/features/copilot); the FAQ does not list periods for Free, Pro or Pro+.

### Training on interaction data, by plan

| Plan | Interaction data used for AI model training? |
|------|----------------------------------------------|
| Copilot Free / Pro / Pro+ (individual plans) | **Yes by default since April 24, 2026**. Opt out with *Allow GitHub to use my data for AI model training* under Privacy settings |
| Copilot Business | **No**. Not affected by the April 2026 change |
| Copilot Enterprise | **No**. Not affected by the April 2026 change |

Source: [GitHub blog: Updates to GitHub Copilot interaction data usage policy](https://github.blog/news-insights/company-news/updates-to-github-copilot-interaction-data-usage-policy/) (March 25, 2026).

> **Key Exam Fact:** GitHub Copilot **Business** and **Enterprise** interaction data is not used to train AI models. Individual-plan data is, unless the user opts out.

---

## 3. How Context Is Determined

### Key Concept

**Copilot sees only the context it is given: the current file, related open tabs, attachments and instructions, never your whole disk.**

For inline suggestions, the strongest signal is the code before and after the cursor. Copilot uses Fill-in-the-Middle, so both sides count. Open tabs, the file name and language, and project structure add supporting context. In chat, you add more yourself: explicit `#` references, selected code, a `#codebase` search, and repository custom instructions.

All of it competes for one token budget. When there's too much, lower-priority context is dropped, so relevant open files and precise references matter more than sheer volume. **Think of the context window as a desk, not a library**: Copilot can only work with what fits on the desk right now.

### In Practice

**What breaks without this**: Copilot writes a helper that duplicates one that already exists, or invents a type shape, because the real definition was never in context. The file wasn't open, or the relevant section was truncated away.

**Decision trigger**: When a suggestion contradicts code you know exists, ask "was that code actually in context?" Open the file, attach it with `#`, or select the relevant block before asking again.

**When you'd choose differently**: For open-ended discovery ("where do we validate tokens?") you don't know which file to attach. Use a `#codebase` search or agent mode, which can search the workspace itself, rather than hand-picking tabs.

### Exam Trap ⚠️

<div class="note-trap">
"Copilot indexes and reads every file on your machine" is false. Inline suggestions draw on the editor context (current file and related open tabs). Workspace search happens only when you or an agent invoke it. Content exclusions remove files from that context, though IDE-supplied semantic information (such as type info) can still leak in indirectly.
</div>

### Neighboring Files (Neighboring Tab Context)

Copilot uses **open editor tabs** as context beyond the current file:

- **Why**: Other open files provide codebase patterns, type definitions, and conventions
- **How**: Content from open tabs is included in the prompt (limited by token window)
- **Best practice**: Open relevant files (interfaces, utilities, examples) before requesting suggestions

### Context Hierarchy

![Flow diagram for "Context Hierarchy": 1 · Current file: highestprioritybefore-cursor andafter-cursor content, 2 · Open neighbouringtabsmost recently used files, 3 · Workspace search#codebase in VS Codechat; finds relevant code, 4 · Custom instructionscopilot-instructions.md,*.instructions.md,AGENTS.md, 5 · Chat historyearlier messages in thisconversation](/content/skillup/ghc/images/ghc-d3-data-architecture-m1.svg)
<!-- diagram source: scripts/diagrams/mermaid/ghc/ghc-d3-data-architecture-m1.mmd -->

### The Context Window Limit

Every LLM has a maximum **context window** (measured in tokens — roughly 3–4 characters per token). When context exceeds this limit:
- Older or lower-priority content is truncated
- Content exclusions (Business/Enterprise) keep specified files out of context. They aren't currently supported in Edit and Agent modes of Copilot Chat in VS Code.
- Focused, specific prompts are more effective than broad ones

---

## 4. Code Suggestion Lifecycle

### Key Concept

**Every suggestion follows the same loop: trigger, gather context, build prompt, proxy, model, post-process, display, accept or reject.**

The lifecycle starts when you pause typing or write a comment. Copilot snapshots context, builds a scoped prompt, and sends it securely to the proxy. The model returns candidates, which pass toxicity, code-quality and (optionally) public-code-matching checks before showing up as ghost text.

Nothing changes in your file until you explicitly accept, in full or in part. Your accept, edit or reject actions feed back into how future suggestions are shaped. **Think of it as a waiter's round trip**: take the order, check the kitchen's work at the pass, serve it, and wait for you to say whether to keep it.

![Flow diagram for "Key Concept": Tab accept, Esc or keep typing, Trigger in IDE, Gather context, Build prompt, Proxy and input filters, LLM generates, Post-processing filters, Ghost text shown, Developer](/content/skillup/ghc/images/ghc-d3-data-architecture-m2.svg)
<!-- diagram source: scripts/diagrams/mermaid/ghc/ghc-d3-data-architecture-m2.mmd -->

### In Practice

**What breaks without this**: Developers blame "the model" for problems that come from other stages. A suggestion that vanishes may have been blocked by the public code filter, and a suggestion that ignores a file may reflect a content exclusion or truncated context.

**Decision trigger**: When troubleshooting, walk the loop and ask which stage failed. No trigger? (Check the status icon or a disabled language.) Missing context? Filtered response? Each stage has its own fix.

**When you'd choose differently**: Agent mode and the cloud agent run a longer loop (plan, edit, run tools, check, iterate) instead of a single completion. You review a diff or pull request at the end rather than accepting ghost text with Tab.

### Exam Trap ⚠️

<div class="note-trap">
"Copilot writes code into your file as soon as it's generated" is false. Inline suggestions are <b>proposed</b> as ghost text and only applied when you accept them. Also, the public code filter acts <b>after</b> generation (post-processing), not as a training-time exclusion.
</div>

### Complete Lifecycle of an Inline Suggestion

![Flow diagram for "Complete Lifecycle of an Inline Suggestion": GitHub Copilot service, 5 · Sent to the Copilot proxyover HTTPS, 6 · Pre-processing filters, 7 · LLM inference, 8 · Candidate completionsgenerated, 9 · Post-processing filtersincl. public-code filter, In your IDE, 1 · Developer types code, 2 · Extension detects apause or trigger, 3 · Context snapshot:current file, open tabs](/content/skillup/ghc/images/ghc-d3-data-architecture-m3.svg)
<!-- diagram source: scripts/diagrams/mermaid/ghc/ghc-d3-data-architecture-m3.mmd -->

### Latency Factors

- Network latency to GitHub servers
- Model inference time (varies by model complexity)
- Post-processing time
- Extensions and IDE responsiveness

---

## 5. LLM Limitations

### Key Concept

**LLMs predict plausible text. They don't check facts, run your code, or know what happened after their training cutoff.**

Every limitation follows from that. Copilot can hallucinate APIs, suggest deprecated patterns, miss code outside its context window, reflect biases in its training data, and give different answers to the same prompt. Quality also varies by language, depending on how much training data existed for it.

None of these is a bug to be patched away. They are properties of probabilistic generation, which is why GitHub's responsible-use guidance puts the risk of generated code on the user and expects human review. **Think of Copilot as a very well-read intern with no debugger**: fast and fluent, and it must be checked.

### In Practice

**What breaks without this**: A suggested library method that doesn't exist fails at runtime in production. Or a deprecated crypto call passes code review because it "looked standard".

**Decision trigger**: Ask "does this suggestion depend on a fact I haven't verified: an API name, a version, a security default?" If yes, check the official docs or run tests before accepting.

**When you'd choose differently**: For well-known, low-risk patterns covered by tests (for example a standard sort or formatting helper), a quick review plus the test suite is enough. Save deep manual verification for security-sensitive, unfamiliar or version-sensitive code.

### Exam Trap ⚠️

<div class="note-trap">
Answers claiming Copilot "always knows the latest API versions", "is always correct for popular languages" or "returns the same output every time" are wrong. Watch for absolute language. The correct answer usually mentions <b>verification</b> and <b>testing</b>. (Chat can use web search such as Bing when that setting is enabled, but inline suggestions still rely on training data plus your context.)
</div>

### The Fundamental Limitations Every Developer Must Know

**1. Training Data Cutoff**
- LLMs have a knowledge cutoff date — they don't know about events, libraries, or APIs released after training
- **Impact**: Copilot may suggest deprecated APIs, removed functions, or outdated security practices
- **Mitigation**: Verify against current documentation; don't blindly trust library versions suggested

**2. Hallucinations**
- LLMs confidently generate plausible-sounding but incorrect information
- **Examples**:
  - Non-existent API methods (`df.rolling_sum()` that doesn't exist in pandas)
  - Wrong function signatures with incorrect parameter counts or types
  - Made-up library names that don't exist on npm/PyPI
- **Mitigation**: Always verify method existence in official docs before committing

**3. Context Window Constraints**
- Limited context means Copilot may not "see" all relevant code in large files
- May produce suggestions inconsistent with code that exists outside its context window
- **Mitigation**: Keep files focused; open only relevant files; attach specific files with `#` references

**4. Probabilistic Output**
- LLMs are fundamentally probabilistic — the same prompt can produce different outputs
- Copilot's suggestions are the statistically most likely continuation, not necessarily the "correct" answer
- **Mitigation**: Validate suggestions with tests; never assume the first suggestion is correct

**5. No Runtime Knowledge**
- Copilot cannot run code or access actual runtime state
- Cannot know your current variable values, database state, or API responses
- **Mitigation**: Provide explicit values and expected behavior in prompts

**6. Potential for Bias**
- Trained on human-written code that may contain biased patterns or non-inclusive conventions
- **Mitigation**: Review generated code for inclusive naming, non-discriminatory logic

---

## Deep Dive: Making the Architecture Concrete

Domain 3 is where candidates lose easy marks because the concepts feel abstract. The fix is to anchor every fact to a concrete mechanism. Two areas deserve special attention: **the context window** and **the data-privacy tiers**.

### Tokens and the context window — with real numbers

A **token** is roughly ¾ of a word (about 3–4 characters of English or code). Window sizes vary by model; some models available in Copilot offer up to a 1 million token window. When people say a model has a "context window of 128k tokens," they mean the model can consider about that many tokens of prompt + response *combined* at once. Everything Copilot knows about your task in a single request must fit in that budget.

> **Why this matters practically.** Imagine a 4,000-line file. That's well over 30,000 tokens on its own. Add the system instructions, your `copilot-instructions.md`, three open neighbour tabs, and chat history, and you can blow past the window. When that happens, Copilot **silently truncates the lowest-priority context first** — usually the far edges of neighbour files and older chat turns. The result: a suggestion that looks reasonable but is *inconsistent with code it never actually saw*.

This is the mechanism behind a classic exam scenario: *"Copilot generated a function that duplicates one that already exists elsewhere in the same large file — why?"* Answer: the existing function fell outside the context window. The mitigation is not "a bigger model" — it's **keeping files focused, closing irrelevant tabs, and attaching the right files explicitly with `#` references** so the important context survives truncation.

### The data pipeline, retold as a story

Don't memorise the seven steps as a list — remember the *shape*: your code never goes straight to a model. It flows **IDE → GitHub's proxy (pre-filter) → LLM → proxy (post-filter: public code filter, safety) → IDE**. The proxy is the security checkpoint on both the inbound and outbound trip. Two exam-relevant consequences:

1. **The public code filter runs on the way *back*** (post-processing), not before generation. It suppresses a suggestion *after* the model produced it.
2. **Content exclusions act at the IDE/collection stage**. Excluded files never enter the prompt, which is why they protect secrets so well. The caveats: they're Business/Enterprise only, they're not supported in VS Code's Edit and Agent chat modes, and they don't apply to symlinks.

### The privacy tiers — the single most tested fact in this domain

| Tier | Interaction data used for training? | The one-line rule |
|------|-------------------------------------|-------------------|
| Free / Pro / Pro+ | Yes, unless the user opts out (since April 24, 2026) | Opt-out lives in personal Copilot settings → Privacy |
| **Business** | **No** | Org-assigned seats aren't used for training |
| **Enterprise** | **No** | Org-assigned seats aren't used for training |

If you remember nothing else from Domain 3, remember: **Business and Enterprise data is not used to train models.** Retention is a separate policy that varies by surface. Editor completion prompts are discarded after the suggestion is returned, while chat history outside the editor is kept. Keeping data is not the same as training on it, and the exam likes to blur that line.

### Worked scenario

> **Scenario.** A consultancy has 40 developers on Copilot Business and 5 freelancers who bring their own Copilot Pro plans. The CISO asks two questions: "Is client code used to train models?" and "Can we keep `/secrets/**` out of Copilot?"
>
> **Reasoning.** For the 40 Business seats, interaction data isn't used for training, and the org can set a content exclusion for `/secrets/**`. For the 5 Pro freelancers, training is on by default unless each person opts out, and org content exclusions don't apply to seats the org doesn't assign. The fix is to give the freelancers org-assigned Business seats. That puts them under the org's no-training terms and its exclusions. The CISO should also know that exclusions don't currently apply in VS Code's Agent and Edit modes, so a written policy and secret scanning are still needed.
>
> **Outcome.** One seat model, one policy surface, and no reliance on five individuals each changing a personal setting.

### Memory aid: **PIPE-R**

- **P**rompt built from editor context (cursor, tabs, file type, instructions)
- **I**nbound proxy: block prompt hacking, filter toxic content and personal data
- **P**redict: the LLM generates candidates
- **E**gress checks: toxicity, code quality, optional public-code matching
- **R**eview: ghost text waits for you to accept or reject

### Exam Strategy for Domain 3

- Keep **retention** (how long data is kept, which varies by surface) separate from **training** (not used for Business/Enterprise; used by default for individual plans unless opted out).
- Any answer claiming Copilot has **real-time internet access** or reads your **disk at rest** is wrong — it uses open-editor context and the assembled prompt only.
- When a scenario describes an *inconsistent or duplicate* suggestion in a big file, the cause is the **context window**, not a model defect.

---

## Key Exam Traps ⚠️

| Trap | Correct Answer |
|------|---------------|
| "Copilot reads from your filesystem at rest" | No — it reads open editor content and context |
| "Business tier code is used to train models" | **FALSE**. Business/Enterprise interaction data isn't used for training |
| "Individual plans are never used for training" | **FALSE**. Since April 24, 2026, Free/Pro/Pro+ data is used unless the user opts out |
| "Copilot always knows the latest APIs" | **FALSE**. A training data cutoff applies (chat web search is an optional, separate setting) |
| "Context window is unlimited" | **FALSE** — limited; older content gets truncated |
| "All suggestions are 100% accurate" | **FALSE** — probabilistic; must validate |

---

## Quick Reference

| Concept | Key Fact |
|---------|---------|
| Data retention (Business/Enterprise defaults) | IDE prompts and suggestions not retained; github.com, Mobile and CLI prompts and suggestions 28 days; engagement data 2 years |
| Business/Enterprise training | Not used for AI model training |
| Individual plan training | Used by default since Apr 24, 2026; opt-out in Privacy settings |
| Proxy | Hosted in GitHub-owned Azure tenant; blocks prompt hacking; filters toxic content |
| Context sources | Code around cursor, open tabs, file type, project structure, `#` attachments, instructions, chat history |
| Public code filter | Post-processing step; ~150 chars compared to public GitHub code; block or show with reference |
| LLM hallucinations | Confidently wrong — always verify API usage |
| Training cutoff | May suggest deprecated/removed APIs |
| Context window | Token-limited; large files may have truncated context |
