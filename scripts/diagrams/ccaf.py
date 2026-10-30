"""CCA-F (Claude Certified Architect, Foundations) lesson diagrams: one outcome diagram per lesson.

Lesson ids follow the official exam guide numbering (1.x agentic, 2.x tools and MCP, 3.x Claude Code,
4.x prompting, 5.x context), so file names match the ## headings in the notes.
Same five layouts as the GH-BP and AB-731 diagrams (lanes, pairs, table, funnel/converge, stack);
colours follow the SkillUp colour code by meaning: data sky, good green, warn saffron, risk rose,
focus indigo, neutral slate.
"""

W = 680


def register(api):
    Diagram = api["Diagram"]
    SLATE4 = api["SLATE4"]

    # ------------------------------------------------------------------ helpers
    def new(f, title, subtitle, desc):
        D = Diagram(f, 0, title, subtitle, desc)
        lines = len(f.wrap("body", subtitle, 14, W - 48)) if subtitle else 0
        return D, 62 + lines * 18 + 26

    def need(D, w, title, body=None, sub=None):
        f = D.f
        tl = f.wrap("title", title, 16, w - 24)
        sl = f.wrap("label", sub, 13, w - 24) if sub else []
        bl = f.wrap("body", body, 13, w - 24) if body else []
        return max(48, len(tl) * 18 + len(sl) * 16 + (4 + len(bl) * 16 if bl else 0) + 26)

    def cell(it):
        it = [it] if isinstance(it, str) else list(it)  # a bare title is allowed
        it += [None] * 4
        return it[0], it[1], it[2] or "neutral", it[3]

    def caption(D, x, y, s, anchor="start"):
        # `code` captions keep their case: uppercasing a path or glob changes its meaning
        if s.startswith("`"):
            D.text(x, y, s.strip("`"), "label", 13, SLATE4, anchor)
        else:
            D.text(x, y, s.upper(), "title", 12.5, SLATE4, anchor, track=0.1)

    def finish(D, y, legend):
        if legend:
            D.legend(y + 26, legend)
            y += 26
        D.h = int(y + 22)
        return D

    def lanes(D, y, spec, gap=30):
        """spec: [(caption, [cells], hot)]; cells are (title, body, kind, sub).
        hot: True hot path, False plain arrows, None dashed, "apart" alternatives with no arrows."""
        for cap, steps, hot in spec:
            if cap:
                caption(D, 24, y, cap); y += 14
            n = len(steps); w = (W - 48 - (n - 1) * gap) / n
            h = max(need(D, w, *cell(s)[:2], cell(s)[3]) for s in steps)
            cy = y + h / 2
            bs = []
            for i, s in enumerate(steps):
                t, b, k, sub = cell(s)
                bs.append(D.box(24 + w / 2 + i * (w + gap), cy, w, t, b, kind=k, sub=sub, h=h))
            for a, b2 in zip(bs, bs[1:]):
                if hot != "apart":
                    D.edge([(a["r"], cy), (b2["l"], cy)], hot=hot, dashed=(hot is None))
            y += h + 26
        return y - 10

    def pairs(D, y, rows, lw=230, gap=80, heads=None, hot_kind="focus"):
        """rows: [(left cell, right cell, label)]."""
        rw = W - 48 - lw - gap
        lx, rx = 24 + lw / 2, W - 24 - rw / 2
        if heads:
            caption(D, 24, y, heads[0]); caption(D, rx - rw / 2, y, heads[1]); y += 14
        for left, right, label in rows:
            lt, lb, lk, ls = cell(left); rt, rb, rk, rs = cell(right)
            h = max(need(D, lw, lt, lb, ls), need(D, rw, rt, rb, rs))
            cy = y + h / 2
            a = D.box(lx, cy, lw, lt, lb, kind=lk, sub=ls, h=h)
            b = D.box(rx, cy, rw, rt, rb, kind=rk, sub=rs, h=h)
            D.edge([(a["r"], cy), (b["l"], cy)], hot=(rk == hot_kind),
                   label=label, at=((a["r"] + b["l"]) / 2, cy - 8) if label else None)
            y += h + 12
        return y

    def table(D, y, heads, rows, first_w=170, gap=12):
        """heads: [cells] for each column; rows: [[cells]] (first cell is the row label)."""
        n = len(heads); rest = (W - 48 - first_w - (n - 1) * gap) / (n - 1)
        ws = [first_w] + [rest] * (n - 1)
        xs, x = [], 24
        for w in ws:
            xs.append(x + w / 2); x += w + gap
        h = max(need(D, w, *cell(c)[:2], cell(c)[3]) for w, c in zip(ws, heads))
        for x, w, c in zip(xs, ws, heads):
            t, b, k, s = cell(c); D.box(x, y + h / 2, w, t, b, kind=k, sub=s, h=h)
        y += h + 10
        for r in rows:
            h = max(need(D, w, *cell(c)[:2], cell(c)[3]) for w, c in zip(ws, r))
            for x, w, c in zip(xs, ws, r):
                t, b, k, s = cell(c); D.box(x, y + h / 2, w, t, b, kind=k, sub=s, h=h)
            y += h + 10
        return y

    def funnel(D, y, top, gates, bottom):
        """top/bottom: cells spanning the width; gates: a row of cells that all lead to the outcome."""
        tt, tb, tk, ts = cell(top)
        th = need(D, W - 48, tt, tb, ts)
        a = D.box(W / 2, y + th / 2, W - 48, tt, tb, kind=tk, sub=ts, h=th)
        y += th + 46
        n, gap = len(gates), 14
        gw = (W - 48 - (n - 1) * gap) / n
        gh = max(need(D, gw, *cell(g)[:2], cell(g)[3]) for g in gates)
        gs = []
        for i, g in enumerate(gates):
            t, b, k, s = cell(g)
            gs.append(D.box(24 + gw / 2 + i * (gw + gap), y + gh / 2, gw, t, b, kind=k, sub=s, h=gh))
        mid = y - 24
        for g in gs:
            D.edge([(a["cx"], a["b"]), (a["cx"], mid), (g["cx"], mid), (g["cx"], g["t"])])
        y += gh + 46
        bt, bb, bk, bs = cell(bottom)
        bh = need(D, W - 48, bt, bb, bs)
        z = D.box(W / 2, y + bh / 2, W - 48, bt, bb, kind=bk, sub=bs, h=bh)
        mid2 = y - 22
        for g in gs:
            D.edge([(g["cx"], g["b"]), (g["cx"], mid2), (W / 2, mid2), (W / 2, z["t"])], hot=True)
        return y + bh

    def converge(D, y, inputs, outcome):
        """A row of inputs that all feed one outcome below (no source box above)."""
        n, gap = len(inputs), 14
        gw = (W - 48 - (n - 1) * gap) / n
        gh = max(need(D, gw, *cell(g)[:2], cell(g)[3]) for g in inputs)
        gs = []
        for i, g in enumerate(inputs):
            t, b, k, s = cell(g)
            gs.append(D.box(24 + gw / 2 + i * (gw + gap), y + gh / 2, gw, t, b, kind=k, sub=s, h=gh))
        y += gh + 46
        bt, bb, bk, bs = cell(outcome)
        bh = need(D, W - 48, bt, bb, bs)
        z = D.box(W / 2, y + bh / 2, W - 48, bt, bb, kind=bk, sub=bs, h=bh)
        mid = y - 22
        for g in gs:
            D.edge([(g["cx"], g["b"]), (g["cx"], mid), (W / 2, mid), (W / 2, z["t"])], hot=True)
        return y + bh

    def stack(D, y, layers, gap=10):
        """layers: [cells] drawn top to bottom, full width."""
        for c in layers:
            t, b, k, s = cell(c)
            h = need(D, W - 48, t, b, s)
            D.box(W / 2, y + h / 2, W - 48, t, b, kind=k, sub=s, h=h)
            y += h + gap
        return y

    # ================================================================== D1 (agentic architecture)
    def t1_1(f):
        D, y = new(f, "The Agentic Loop",
                   "stop_reason decides: run tools while it's tool_use, finish when it's end_turn.",
                   "The agentic loop: send messages to Claude, check stop_reason, run the requested tools and append "
                   "their results while it is tool_use, and return the final answer when it is end_turn.")
        y = lanes(D, y, [
            ("While stop_reason is tool_use", [("Send messages + tools", None, "data"), ("Claude picks a tool", "From context, not a script"),
                                               ("Run the tool", None), ("Append tool_result", "Back to Claude", "focus")], True),
            ("When stop_reason is end_turn", [("Final answer", "Return it", "good")], True),
            ("Not a stop signal", [("Text sounds finished", None, "risk"), ("Turn cap reached", "Safety net only", "warn")], "apart"),
        ], gap=24)
        return finish(D, y, [("data", "request"), ("focus", "loop back"), ("good", "done"), ("risk", "anti-pattern")])

    def t1_2(f):
        D, y = new(f, "Coordinator and Subagents",
                   "Every message goes through the coordinator, which also checks the result for gaps.",
                   "A coordinator analyses the query, sends partitioned subtasks to search, analysis and synthesis "
                   "subagents, receives all results back, and re-delegates targeted queries when the synthesis shows gaps.")
        y = stack(D, y, [("Coordinator", "Decomposes, picks subagents, routes all messages, handles errors", "focus")])
        y = lanes(D, y + 8, [
            ("Subagents (isolated context, partitioned scope)", [("Search: subtopic A", None, "data"), ("Search: subtopic B", None, "data"),
                                                               ("Analysis", None, "data"), ("Synthesis", None, "data")], "apart"),
        ], gap=14)
        y = lanes(D, y + 4, [("Refinement", [("Synthesis reviewed", "Coverage gaps?"), ("Targeted re-delegation", None, "warn"),
                                             ("Final report", None, "good")], True)])
        return finish(D, y, [("focus", "hub"), ("data", "spoke"), ("warn", "gap fix"), ("good", "result")])

    def t1_3(f):
        D, y = new(f, "Briefing a Subagent",
                   "It sees only its prompt, so the prompt carries the findings, the sources and the goal.",
                   "A coordinator passes a subagent a structured brief containing prior findings, source metadata and "
                   "quality criteria; several subagents are spawned in one response to run in parallel.")
        y = converge(D, y, [("Prior findings", "Complete, not summarised", "data"), ("Source metadata", "URL, document, page; kept separate", "data"),
                            ("Goal + quality criteria", "Not step-by-step orders", "data")],
                     ("Task (Agent) tool call", "Allowed in the coordinator's tools; one AgentDefinition per type", "focus"))
        y = lanes(D, y + 20, [("Parallel: several Task calls in one response", [("Subagent 1",), ("Subagent 2",), ("Subagent 3",)], "apart")])
        return finish(D, y, [("data", "in the prompt"), ("focus", "spawn")])

    def t1_4(f):
        D, y = new(f, "Enforce Order in Code",
                   "A gate guarantees the sequence; a handoff carries the case to a human.",
                   "A prerequisite gate blocks process_refund until get_customer has returned a verified ID; when the "
                   "case escalates, a structured handoff with customer ID, root cause, amount and recommended action goes "
                   "to the human agent.")
        y = lanes(D, y, [
            ("Verified first", [("get_customer", "Returns verified ID", "data"), ("Gate: ID present?", None, "focus"),
                                ("process_refund runs", None, "good")], True),
            ("Not verified", [("process_refund called", None, "data"), ("Gate blocks", "Error: verify first", "risk")], None),
            ("Escalation", [("Structured handoff", "Customer ID, root cause, amount, next step", "warn"), ("Human agent", "No need to re-ask", "good")], True),
        ])
        return finish(D, y, [("data", "call"), ("focus", "programmatic gate"), ("risk", "blocked"), ("good", "outcome")])

    def t1_5(f):
        D, y = new(f, "Hooks Around Every Tool Call",
                   "PreToolUse decides whether a call runs; PostToolUse reshapes what comes back.",
                   "A tool call passes a PreToolUse hook that blocks refunds over $500 and redirects them to escalation, "
                   "the tool runs, and a PostToolUse hook normalises timestamps and status codes before Claude sees the result.")
        y = lanes(D, y, [
            (None, [("Claude requests a tool", None, "data"), ("PreToolUse", "Deny refund > $500", "focus"),
                    ("Tool runs",), ("PostToolUse", "Normalise dates, codes", "focus"), ("Claude reads result", None, "good")], True),
            ("Denied", [("Reason returned", "\"Escalate to a human\"", "warn"), ("Escalation path", None, "good")], True),
        ], gap=18)
        return finish(D, y, [("data", "request"), ("focus", "hook"), ("warn", "redirect"), ("good", "outcome")])

    def t1_6(f):
        D, y = new(f, "Fixed Chain or Adaptive Plan",
                   "Predictable work gets a chain; open-ended work gets a plan that changes.",
                   "Two decomposition patterns: a fixed chain of per-file passes followed by an integration pass for "
                   "predictable reviews, and an adaptive loop of mapping, prioritising and re-planning for open-ended "
                   "investigations.")
        y = lanes(D, y, [
            ("Prompt chaining: predictable review", [("File 1 pass", None, "data"), ("File 2 pass", None, "data"),
                                                    ("File n pass", None, "data"), ("Integration pass", "Cross-file data flow", "focus")], True),
            ("Dynamic decomposition: open-ended", [("Map structure", None, "data"), ("Find high-impact areas"),
                                                  ("Prioritised plan",), ("Re-plan on findings", None, "warn")], True),
        ], gap=24)
        return finish(D, y, [("data", "step"), ("focus", "integration"), ("warn", "adapts")])

    def t1_7(f):
        D, y = new(f, "Resume, Fork or Start Fresh",
                   "It depends on whether the session's context is still true.",
                   "From a shared analysis session: resume it when prior context is still valid, fork it into two branches "
                   "to compare approaches, or start a fresh session with a structured summary when files have changed.")
        y = pairs(D, y, [
            (("Context still valid", None, "data"), ("Resume", "CLI -r <name or id> · SDK resume", "good"), None),
            (("Compare two approaches", None, "data"), ("Fork", "CLI fork-session flag · SDK fork_session", "focus"), None),
            (("A few files changed", None, "data"), ("Resume + list the changes", "Targeted re-analysis"), None),
            (("Much has changed", None, "data"), ("Fresh session + summary", "Stale tool results left behind", "warn"), None),
        ], heads=("Situation", "Do this"))
        return finish(D, y, [("data", "situation"), ("good", "continue"), ("focus", "branch"), ("warn", "restart")])

    # ================================================================== D2 (Claude Code: guide domain 3)
    def t3_1(f):
        D, y = new(f, "Where CLAUDE.md Instructions Live",
                   "All loaded files are combined; each file has a different audience.",
                   "Claude Code instruction sources: user-level CLAUDE.md for you only, project CLAUDE.md shared via git, "
                   "subdirectory CLAUDE.md loaded when working there, plus @imports and .claude/rules files, all combined "
                   "into context.")
        y = table(D, y, [("File", None, "start"), ("Who gets it", None, "start"), ("Use it for", None, "start")], [
            [("~/.claude/CLAUDE.md",), ("Only you, all projects", None, "warn"), ("Personal preferences",)],
            [("./CLAUDE.md", None, "focus"), ("Whole team, via git", None, "good"), ("Team standards",)],
            [("CLAUDE.local.md",), ("Only you, this project",), ("Local sandbox details",)],
            [("subdir/CLAUDE.md",), ("Loaded when working there",), ("Folder-specific notes",)],
            [("@import / .claude/rules/",), ("Whoever loads the parent",), ("Modular topic files",)],
        ], first_w=180)
        return finish(D, y, [("focus", "team default"), ("good", "shared"), ("warn", "not shared")])

    def t3_2(f):
        D, y = new(f, "Skills, Commands and CLAUDE.md",
                   "On-demand workflows in skills; always-on standards in CLAUDE.md.",
                   "Where reusable instructions live: project skills and commands shared via git, personal ones in your "
                   "home folder, frontmatter for allowed-tools, argument-hint and context fork, and CLAUDE.md for always-on "
                   "standards.")
        y = pairs(D, y, [
            ((".claude/skills/ · .claude/commands/", "Committed", "data"), ("Team /commands", "Everyone who clones gets them", "good"), None),
            (("~/.claude/skills/", "Personal", "data"), ("Your variants", "Use a different name", "warn"), None),
            (("context: fork", None, "data"), ("Runs in an isolated subagent", "Verbose output stays out", "focus"), None),
            (("allowed-tools · argument-hint", None, "data"), ("Limit tools · prompt for args",), None),
            (("CLAUDE.md", None, "data"), ("Always-on standards", "Not a workflow"), None),
        ], lw=250, heads=("Where / what", "Effect"))
        return finish(D, y, [("data", "location or field"), ("good", "shared"), ("warn", "personal"), ("focus", "isolation")])

    def t3_3(f):
        D, y = new(f, "Rules That Load Only for Matching Files",
                   "A paths glob follows a file type across the whole repository.",
                   "A rule file with paths set to **/*.test.tsx loads when Claude edits any test file in any folder, while a "
                   "subdirectory CLAUDE.md only covers files under its own folder.")
        y = lanes(D, y, [
            ("`.claude/rules/testing.md  ·  paths: **/*.test.tsx`", [("web/Button.test.tsx", "Rule loads", "good"),
                                                                  ("api/user.test.tsx", "Rule loads", "good"),
                                                                  ("api/user.ts", "Rule not loaded", None)], "apart"),
            ("`web/CLAUDE.md`", [("web/Button.test.tsx", "Loads", "good"), ("api/user.test.tsx", "Not covered", "warn"),
                               ("api/user.ts", "Not covered")], "apart"),
        ])
        return finish(D, y, [("good", "convention applied"), ("warn", "missed"), ("neutral", "not relevant")])

    def t3_4(f):
        D, y = new(f, "Plan Mode or Direct Execution",
                   "Plan when the change is big or has several valid designs; act when it's small and clear.",
                   "Task size decides the mode: a single-file fix with a clear cause goes straight to direct execution, "
                   "while a migration or restructuring goes to plan mode with Explore for discovery, then direct "
                   "execution to implement the agreed plan.")
        y = lanes(D, y, [
            ("Large or architectural: migration, 40 dependent files", [("Plan mode", "Read-only", "focus"), ("Explore subagent", "Discovery, returns summary", "data"),
                                                                     ("Agree the plan",), ("Execute", None, "good")], True),
            ("Small and clear: one-file fix, known cause", [("Direct execution", None, "good")], True),
        ], gap=24)
        return finish(D, y, [("focus", "plan"), ("data", "isolated discovery"), ("good", "change made")])

    def t3_5(f):
        D, y = new(f, "Ways to Iterate Towards Right",
                   "Give Claude objective feedback, not longer descriptions.",
                   "Four refinement techniques: concrete input-output examples when descriptions are misread, tests first "
                   "with failures fed back, an interview before building in unfamiliar areas, and batching interacting "
                   "issues into one message.")
        y = pairs(D, y, [
            (("Description misread", None, "warn"), ("2–3 input/output examples", None, "focus"), None),
            (("Behaviour can be specified", None, "data"), ("Tests first, feed failures back", None, "good"), None),
            (("Unfamiliar domain", None, "data"), ("Interview: Claude asks first", None, "good"), None),
            (("Issues affect each other", None, "data"), ("One detailed message", "Independent issues: one at a time", "good"), None),
        ], heads=("Situation", "Technique"), hot_kind="good")
        return finish(D, y, [("warn", "symptom"), ("data", "situation"), ("focus", "most direct fix"), ("good", "technique")])

    def t3_6(f):
        D, y = new(f, "Claude Code in CI",
                   "Non-interactive, schema-shaped, with project context and an independent reviewer.",
                   "A CI job runs claude -p with output-format json and a JSON schema, reads project standards from "
                   "CLAUDE.md and prior findings, and posts structured findings as inline PR comments from an independent "
                   "review session.")
        y = converge(D, y, [("claude -p", "No terminal, no hang", "data"), ("JSON output + schema", "output-format, json-schema", "data"),
                            ("CLAUDE.md", "Standards, fixtures", "data"), ("Prior findings", "Report only new", "data")],
                     ("structured_output → inline PR comments", "From a session that didn't write the code", "focus"))
        return finish(D, y, [("data", "input"), ("focus", "result")])

    # ================================================================== D3 (prompting: guide domain 4)
    def t4_1(f):
        D, y = new(f, "Criteria, Not Caution",
                   "Defining what to report beats asking the model to be careful.",
                   "A vague instruction such as be conservative produces noisy findings that developers learn to ignore, "
                   "while explicit report and skip categories with severity examples produce precise findings that "
                   "developers trust.")
        y = lanes(D, y, [
            ("Vague", [("\"Be conservative\"", None, "data"), ("Model guesses the bar"), ("Noisy findings", None, "risk"),
                       ("Developers ignore all", None, "risk")], None),
            ("Explicit", [("Report: bugs, security", "Skip: style, local patterns", "data"), ("Severity examples"),
                          ("Precise findings", None, "good"), ("Developers trust them", None, "focus")], True),
        ], gap=22)
        return finish(D, y, [("data", "instruction"), ("risk", "lost trust"), ("good", "precise"), ("focus", "outcome")])

    def t4_2(f):
        D, y = new(f, "What Few-Shot Examples Teach",
                   "A few examples set the format and show where the line is.",
                   "Two to four examples, each showing an input, the reasoning and the output, lead to consistent format, "
                   "correct handling of ambiguous cases and generalisation to new patterns.")
        y = converge(D, y, [("Example: clear issue", "Input · reasoning · output", "data"),
                            ("Example: looks wrong, is fine", "Why it's acceptable", "data"),
                            ("Example: ambiguous case", "Why this, not that", "data")],
                     ("Consistent format, sound judgement on new cases", "Fewer false positives and empty fields", "focus"))
        return finish(D, y, [("data", "example"), ("focus", "outcome")])

    def t4_3(f):
        D, y = new(f, "Structure Guaranteed, Truth Checked",
                   "The schema fixes the shape; honest fields and validation handle the content.",
                   "An extraction tool with a JSON schema, tool_choice any or a forced tool, and strict mode yields "
                   "schema-valid output; nullable fields and other or unclear enum values stop the model inventing values, "
                   "while semantic checks still run afterwards.")
        y = lanes(D, y, [
            (None, [("Tool + JSON schema", "strict: true", "data"), ("tool_choice", "any, or force the tool"),
                    ("Schema-valid output", "Always parses", "good"), ("Semantic checks", "Values right? (4.4)", "focus")], True),
            ("Schema design for honesty", [("Nullable fields", "If data may be absent"), ("enum + \"unclear\"",), ("\"other\" + detail",)], "apart"),
        ], gap=22)
        return finish(D, y, [("data", "definition"), ("good", "guaranteed"), ("focus", "still needed")])

    def t4_4(f):
        D, y = new(f, "Validate, Then Retry With the Error",
                   "Specific feedback fixes mistakes; nothing fixes missing data.",
                   "After extraction, semantic validation passes good records; failures with fixable errors are retried "
                   "with the document, the failed output and specific errors, while missing information is flagged instead "
                   "of retried.")
        y = lanes(D, y, [
            ("Passes", [("Extraction", None, "data"), ("Semantic validation", "calculated vs stated total", "focus"), ("Accept", None, "good")], True),
            ("Fixable error", [("Mismatch found",), ("Retry: doc + output + errors", None, "warn"), ("Corrected", None, "good")], True),
            ("Data not in document", [("Field absent",), ("Don't retry", None, "risk"), ("Flag / null", None, "good")], True),
        ])
        return finish(D, y, [("focus", "check"), ("warn", "retry"), ("risk", "won't help"), ("good", "outcome")])

    def t4_5(f):
        D, y = new(f, "Synchronous or Batch",
                   "If someone is waiting, don't batch it.",
                   "Blocking pre-merge checks go to the synchronous Messages API, while overnight and weekly jobs go to the "
                   "Batches API at half the cost; results are matched by custom_id and only failed items are resubmitted.")
        y = lanes(D, y, [
            ("Blocking: pre-merge check", [("Messages API", "Synchronous, full price", "data"), ("Result now", None, "good")], True),
            ("Can wait: nightly, weekly", [("Sample-test the prompt",), ("Batches API", "50% off, up to 24 h", "focus"),
                                          ("Match by custom_id",), ("Resubmit failures only", None, "warn")], True),
        ], gap=22)
        return finish(D, y, [("data", "sync"), ("focus", "batch"), ("warn", "retry subset"), ("good", "result")])

    def t4_6(f):
        D, y = new(f, "Independent Reviewer, Split Passes",
                   "Fresh eyes and focused passes catch what self-review misses.",
                   "A generator instance writes code and an independent reviewer instance without its reasoning reviews it "
                   "in per-file passes and an integration pass, with a confidence on each finding for routing.")
        y = lanes(D, y, [
            (None, [("Generator instance", "Writes the code", "data"), ("Independent reviewer", "No generator reasoning", "focus")], True),
            ("Review passes", [("Per-file: file 1",), ("Per-file: file n",), ("Integration pass", "Cross-file flow", "focus"),
                               ("Findings + confidence", "Route low confidence", "good")], True),
            ("Avoid", [("Same session reviews itself", "Approves its own choices", "risk")], None),
        ], gap=22)
        return finish(D, y, [("data", "generator"), ("focus", "independent"), ("good", "routed findings"), ("risk", "self-review")])

    # ================================================================== D4 (tools and MCP: guide domain 2)
    def t2_1(f):
        D, y = new(f, "Descriptions Decide Tool Choice",
                   "If two descriptions overlap, Claude can't tell the tools apart.",
                   "Two tools with one-line overlapping descriptions cause misrouting; rewritten descriptions that state "
                   "purpose, inputs, outputs, examples and when to use the other tool make selection reliable.")
        y = pairs(D, y, [
            (("get_customer", "\"Looks up customer info\"", "risk"), ("get_customer", "Account details: email, address, phone. Use for account changes.", "good"), "rewrite"),
            (("lookup_order", "\"Gets customer orders\"", "risk"), ("lookup_order", "Order status by order ID. Not for account data.", "good"), "rewrite"),
        ], lw=220, heads=("Before: overlapping", "After: purpose, inputs, boundary"), hot_kind="good")
        y = stack(D, y + 2, [("Also check the system prompt", "Keyword-heavy instructions can pull Claude to the wrong tool", "warn")])
        return finish(D, y - 10, [("risk", "misroutes"), ("good", "clear"), ("warn", "check")])

    def t2_2(f):
        D, y = new(f, "Errors the Agent Can Act On",
                   "isError plus a category tells the agent whether to retry, fix, explain or escalate.",
                   "A tool failure returns isError with a category: transient errors are retried, validation errors are "
                   "fixed and resent, business-rule violations are explained to the customer, and permission errors are "
                   "escalated; an empty result is a success.")
        y = pairs(D, y, [
            (("Transient", "Gateway timeout · isRetryable: true", "warn"), ("Retry (locally)", None, "good"), None),
            (("Validation", "Malformed order ID", "warn"), ("Fix input, resend", None, "good"), None),
            (("Business", "Over policy limit · isRetryable: false", "risk"), ("Explain to the customer", None, "good"), None),
            (("Permission", "Caller not allowed", "risk"), ("Escalate", None, "good"), None),
            (("No matches", "Query worked", "data"), ("Not an error: valid empty result", None, "focus"), None),
        ], heads=("Error category", "Agent's action"), hot_kind="good")
        return finish(D, y, [("warn", "recoverable"), ("risk", "not retryable"), ("good", "action"), ("focus", "success")])

    def t2_3(f):
        D, y = new(f, "Scope Tools by Role",
                   "Fewer, relevant tools per agent; tool_choice decides whether one must be called.",
                   "Instead of every agent holding all eighteen tools, each subagent gets a small role-specific set plus "
                   "one scoped cross-role tool, and tool_choice auto, any or forced controls whether and which tool is called.")
        y = lanes(D, y, [
            ("Avoid", [("Every agent, all 18 tools", "Worse selection, misuse", "risk")], None),
            ("Role-scoped", [("Search agent", "web_search, fetch_page", "data"), ("Analysis agent", "run_query, chart", "data"),
                             ("Synthesis agent", "+ verify_fact only", "focus")], "apart"),
            ("tool_choice", [("auto", "Model decides"), ("any", "Must call a tool", "good"), ("forced", "That tool first", "good")], "apart"),
        ])
        return finish(D, y, [("risk", "overloaded"), ("data", "scoped set"), ("focus", "cross-role tool"), ("good", "guarantees a call")])

    def t2_4(f):
        D, y = new(f, "Wiring MCP Servers into Claude Code",
                   "Shared servers in the repo, secrets in the environment, personal servers at home.",
                   "Team MCP servers go in the project .mcp.json, committed, with tokens read from environment variables, "
                   "while personal servers live in ~/.claude.json; all servers' tools are discovered together, and "
                   "resources expose content catalogs.")
        y = pairs(D, y, [
            ((".mcp.json (project)", "Committed", "data"), ("Whole team", "Bearer ${DB_TOKEN} from each person's env", "focus"), None),
            (("~/.claude.json (user/local)", None, "data"), ("Only you", "Experimental servers", "warn"), None),
            (("All configured servers", None, "data"), ("Tools discovered together", "Detailed descriptions win over built-ins"), None),
            (("MCP resources", None, "data"), ("Content catalog", "Fewer exploratory calls", "good"), None),
        ], lw=240, heads=("Where", "Effect"))
        return finish(D, y, [("data", "config"), ("focus", "team default"), ("warn", "personal"), ("good", "efficiency")])

    def t2_5(f):
        D, y = new(f, "Pick the Right Built-in Tool",
                   "Search before reading; edit snippets, rewrite only when you must.",
                   "Choosing a built-in tool: Grep to search file contents, Glob to find files by name pattern, Read to load "
                   "a file, Edit for a unique snippet, and Read plus Write when the Edit anchor isn't unique.")
        y = pairs(D, y, [
            (("Where is formatCurrency called?", None, "data"), ("Grep", "Searches file contents", "focus"), None),
            (("Find all **/*.test.tsx", None, "data"), ("Glob", "Matches file paths", "focus"), None),
            (("Understand a file", None, "data"), ("Read", "Then follow imports"), None),
            (("Change one unique line", None, "data"), ("Edit", "Anchor must be unique", "good"), None),
            (("Anchor appears twice", None, "warn"), ("Read + Write", "Whole-file rewrite", "good"), None),
        ], heads=("Need", "Tool"))
        return finish(D, y, [("data", "need"), ("focus", "search"), ("good", "modify"), ("warn", "edit fails")])

    # ================================================================== D5 (context and reliability)
    def t5_1(f):
        D, y = new(f, "Keep Exact Facts Out of the Summary",
                   "Summaries round numbers; a case-facts block doesn't.",
                   "A persistent case-facts block with exact amounts, dates and IDs sits outside the summarised history, "
                   "tool outputs are trimmed to relevant fields, and key findings go at the start of long inputs.")
        y = stack(D, y, [
            ("Case facts (every prompt, verbatim)", "Order #A-2291 · refund $1,247.50 · promised by 14 Nov", "focus"),
            ("Summarised history", "Older turns condensed", "data"),
            ("Recent turns", "Full detail"),
            ("Tool results, trimmed", "Only the fields that matter", "good"),
        ])
        y = stack(D, y + 4, [("Long inputs: key findings first, detail under headers", "Avoids lost-in-the-middle", "warn")])
        return finish(D, y - 10, [("focus", "never summarised"), ("data", "condensed"), ("good", "trimmed"), ("warn", "ordering")])

    def t5_2(f):
        D, y = new(f, "When to Escalate",
                   "Explicit triggers, not mood or self-reported confidence.",
                   "Escalation triggers are an explicit request for a human, a policy gap or no progress, while frustration "
                   "alone is resolved by the agent; multiple customer matches lead to asking for another identifier.")
        y = pairs(D, y, [
            (("\"I want a person\"", None, "data"), ("Escalate now", "Don't investigate first", "focus"), None),
            (("Policy silent or ambiguous", None, "data"), ("Escalate", None, "focus"), None),
            (("No progress possible", None, "data"), ("Escalate", None, "focus"), None),
            (("Frustrated, simple issue", None, "data"), ("Resolve it", "Sentiment isn't a trigger", "good"), None),
            (("Three customers match", None, "data"), ("Ask for another identifier", "Don't guess", "warn"), None),
        ], heads=("Signal", "Response"))
        return finish(D, y, [("data", "signal"), ("focus", "escalate"), ("good", "resolve"), ("warn", "clarify")])

    def t5_3(f):
        D, y = new(f, "Propagating Errors Usefully",
                   "Enough context to recover; never silent, never fatal to the whole run.",
                   "A failed subagent returns structured error context with failure type, attempted query, partial results "
                   "and alternatives; the coordinator retries, reroutes or continues, and the final report annotates gaps "
                   "instead of hiding them.")
        y = lanes(D, y, [
            (None, [("Subagent fails", None, "risk"), ("Local retry if transient"), ("Structured error", "Type · query · partial results · alternatives", "focus"),
                    ("Coordinator decides", "Retry, reroute, continue", "good")], True),
            ("Anti-patterns", [("\"No findings\" on failure", "Suppressed", "risk"), ("Abort everything", "On one failure", "risk")], "apart"),
            ("Report", [("Coverage annotations", "Well supported vs gaps", "good")], True),
        ], gap=22)
        return finish(D, y, [("risk", "failure"), ("focus", "error context"), ("good", "recovery")])

    def t5_4(f):
        D, y = new(f, "Exploring a Big Codebase Without Drowning",
                   "Delegate the noise, write findings down, checkpoint state.",
                   "The main agent sends subagents to investigate specific questions and receives summaries, records key "
                   "findings in a scratchpad file, compacts when context fills, and each agent exports state to a manifest "
                   "the coordinator reloads after a crash.")
        y = stack(D, y, [("Main agent: high-level coordination", "Asks specific questions; keeps the big picture", "focus")])
        y = lanes(D, y + 8, [
            (None, [("Subagent: how is billing called?", "Returns a summary", "data"), ("Subagent: where are invoices stored?", "Returns a summary", "data"),
                    ("Scratchpad file", "Key findings persist", "good")], "apart"),
            ("Recovery", [("Each agent exports state",), ("Manifest", None, "warn"), ("Coordinator reloads on resume", None, "good")], True),
        ])
        return finish(D, y, [("focus", "coordinator"), ("data", "isolated exploration"), ("warn", "checkpoint"), ("good", "persists")])

    def t5_5(f):
        D, y = new(f, "Calibrating Human Review",
                   "Look under the average, calibrate confidence, and keep sampling.",
                   "Overall accuracy is broken down by document type and field, confidence thresholds are calibrated on "
                   "labelled data, low-confidence items go to human review, and stratified random samples of "
                   "high-confidence items keep measuring the error rate.")
        y = lanes(D, y, [
            ("Before automating", [("97% overall", None, "warn"), ("By type and field", "Receipts: total 71%", "risk"),
                                   ("Calibrate thresholds", "Labelled validation set", "focus")], True),
            ("In production", [("Low confidence", "Contradictory sources"), ("Human review", None, "good")], True),
            (None, [("High confidence",), ("Stratified random sample", "Error rate, new patterns", "good")], True),
        ])
        return finish(D, y, [("warn", "misleading"), ("risk", "hidden weakness"), ("focus", "calibration"), ("good", "review")])

    def t5_6(f):
        D, y = new(f, "Every Claim Keeps Its Source",
                   "Provenance travels with the claim; conflicts are shown, not settled silently.",
                   "Subagents output claims with source, excerpt and date; the synthesis keeps claim-source mappings, "
                   "annotates conflicting values with both sources, and separates established from contested findings.")
        y = converge(D, y, [("Claim + source", "URL or document", "data"), ("Excerpt", None, "data"), ("Date", "Published or collected", "data")],
                     ("Synthesis keeps and merges the mappings", None, "focus"))
        y = lanes(D, y + 20, [("Report", [("Established findings", None, "good"),
                                          ("Contested", "$4.2B (2023) vs $5.1B (2025), both cited", "warn")], "apart")])
        return finish(D, y, [("data", "required field"), ("focus", "preserved"), ("good", "agreed"), ("warn", "conflict shown")])

    fns = {
        "ccaf-1-1-agentic-loop": t1_1, "ccaf-1-2-coordinator": t1_2, "ccaf-1-3-subagent-context": t1_3,
        "ccaf-1-4-prerequisite-gate": t1_4, "ccaf-1-5-hooks": t1_5, "ccaf-1-6-decomposition": t1_6, "ccaf-1-7-sessions": t1_7,
        "ccaf-3-1-claude-md-hierarchy": t3_1, "ccaf-3-2-commands-skills": t3_2, "ccaf-3-3-path-rules": t3_3,
        "ccaf-3-4-plan-mode": t3_4, "ccaf-3-5-iterative-refinement": t3_5, "ccaf-3-6-ci-cd": t3_6,
        "ccaf-4-1-explicit-criteria": t4_1, "ccaf-4-2-few-shot": t4_2, "ccaf-4-3-structured-output": t4_3,
        "ccaf-4-4-retry-feedback": t4_4, "ccaf-4-5-batch": t4_5, "ccaf-4-6-multi-pass-review": t4_6,
        "ccaf-2-1-tool-descriptions": t2_1, "ccaf-2-2-mcp-errors": t2_2, "ccaf-2-3-tool-distribution": t2_3,
        "ccaf-2-4-mcp-config": t2_4, "ccaf-2-5-builtin-tools": t2_5,
        "ccaf-5-1-context-preservation": t5_1, "ccaf-5-2-escalation": t5_2, "ccaf-5-3-error-propagation": t5_3,
        "ccaf-5-4-codebase-exploration": t5_4, "ccaf-5-5-human-review": t5_5, "ccaf-5-6-provenance": t5_6,
    }
    return {name: ("ccaf", fn) for name, fn in fns.items()}
