"""CCAO-F (Claude Certified Associate, Foundations) lesson diagrams: one outcome diagram per lesson.

Lesson ids follow the official exam guide numbering (7 domains, 30 objectives), so file names match the
## headings in the notes. Same five layouts as the GH-BP, AB-731 and CCA-F diagrams (lanes, pairs, table,
funnel/converge, stack); colours follow the SkillUp colour code by meaning: data sky, good green,
warn saffron, risk rose, focus indigo, neutral slate.
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

    # ================================================================== D1 (prompting)
    def t1_1(f):
        D, y = new(f, "Anatomy of a Strong Prompt",
                   "Five parts turn a vague request into a brief Claude can meet.",
                   "A strong prompt stacks five parts: the goal, the context and background, the audience, constraints "
                   "and format, and an example of good output, which together produce a usable first draft.")
        y = converge(D, y, [("Goal", "What it's for", "data"), ("Context", "Background, facts", "data"),
                            ("Audience", "Who reads it", "data"), ("Format", "Length, structure", "data"),
                            ("Example", "What good looks like", "data")],
                     ("Usable first draft", "Specific, on-brief, fewer rounds of fixes", "focus"))
        y = lanes(D, y + 22, [("Missing a part?", [("\"Write something about X\"", "Generic, wrong length", "risk"),
                                                   ("When unsure", "Say \"not provided\" instead of guessing", "good")], "apart")])
        return finish(D, y, [("data", "prompt part"), ("focus", "result"), ("risk", "vague"), ("good", "safe default")])

    def t1_2(f):
        D, y = new(f, "Break the Request Down",
                   "Steps you can check beat one request that does everything.",
                   "One large request produces a shallow result that is hard to fix, while a decomposed chain of outline, "
                   "sections and assembly lets you check and correct each step before moving on.")
        y = lanes(D, y, [
            ("All at once", [("One big request", "Summary, risks, plan, letter", "data"), ("Shallow result", "Hard to see what went wrong", "risk")], False),
            ("Decomposed", [("Outline", None, "data"), ("Check",), ("Sections", "One at a time"), ("Check",),
                            ("Assemble", "Builds on checked steps", "focus")], True),
        ], gap=20)
        return finish(D, y, [("data", "start"), ("focus", "recommended"), ("risk", "skims every part")])

    def t1_3(f):
        D, y = new(f, "The Iteration Loop",
                   "Specific feedback improves the draft; repeated fixes belong in the prompt.",
                   "The iteration loop: write a prompt, read the output against your goal, give specific feedback on what "
                   "to keep and change, and when the same issue repeats, edit the prompt or instructions instead.")
        y = lanes(D, y, [
            (None, [("Prompt", None, "data"), ("Read output", "Against the goal"), ("Specific feedback", "Keep this, change that", "focus"),
                    ("Better draft", None, "good")], True),
            ("Same issue every time?", [("Edit the prompt or template", "So the next run starts better", "good")], True),
            ("Not feedback", [("\"Make it better\"", None, "risk"), ("\"Try again\"", None, "risk")], "apart"),
        ])
        return finish(D, y, [("data", "start"), ("focus", "the lever"), ("good", "improvement"), ("risk", "vague")])

    def t1_4(f):
        D, y = new(f, "Prompt by Task Type",
                   "Each kind of task needs something different from the prompt.",
                   "Four task types and what each prompt needs: analysis gives the data and asks for the method, research "
                   "asks for checkable sources, drafting sets audience, tone and length, and brainstorming asks for many "
                   "varied ideas before narrowing.")
        y = table(D, y, [("Task", None, "start"), ("Give Claude", None, "start"), ("Ask for", None, "start")], [
            [("Analysis", None, "focus"), ("The data", "Work from it only"), ("Method and evidence", "Facts apart from guesses")],
            [("Research", None, "data"), ("The question and scope",), ("Sources and citations", "To check", "good")],
            [("Drafting", None, "data"), ("Audience, tone, length",), ("A draft to edit",)],
            [("Brainstorming", None, "data"), ("The goal and limits",), ("Many varied ideas", "Then narrow down", "good")],
        ], first_w=150)
        return finish(D, y, [("focus", "anchored to data"), ("data", "task type"), ("good", "what makes it useful")])

    # ================================================================== D2 (output evaluation)
    def t2_1(f):
        D, y = new(f, "Before You Use the Output",
                   "Fluent isn't the same as right: pass every gate first.",
                   "Output evaluation as a set of gates: every requirement covered, every fact supported by a source, "
                   "numbers recomputed, and nothing important missing, before the output is ready to use.")
        y = lanes(D, y, [
            (None, [("Claude's output", None, "data"), ("Requirements covered?", "Compare to the brief"), ("Facts supported?", "Compare to the source"),
                    ("Numbers recomputed?", "Spot-check totals"), ("Ready to use", None, "focus")], True),
            ("Not checks", [("Reads well", None, "warn"), ("Sounds confident", None, "warn"), ("Claude says it's complete", None, "warn")], "apart"),
        ], gap=18)
        return finish(D, y, [("data", "input"), ("focus", "passes"), ("warn", "false signal")])

    def t2_2(f):
        D, y = new(f, "Red Flags and Their Checks",
                   "Specific-looking details are where hallucinations hide.",
                   "Red flags matched to checks: an exact citation or section number is checked against the source, a "
                   "precise statistic is traced to its origin, contradictory figures are reconciled, and one-sided or "
                   "stereotyped wording is reviewed for bias.")
        y = pairs(D, y, [
            (("Exact citation or section", "No source given", "warn"), ("Check it in the official text", None, "good"), None),
            (("Precise statistic", None, "warn"), ("Trace it to the original source", None, "good"), None),
            (("Two figures disagree", "8% here, 12% there", "risk"), ("Reconcile against the source", None, "focus"), None),
            (("Unequal wording about groups", None, "risk"), ("Review for bias; describe equals equally", None, "good"), None),
        ], heads=("Red flag", "Check"), lw=250)
        return finish(D, y, [("warn", "possible hallucination"), ("risk", "error or bias"), ("good", "check")])

    def t2_3(f):
        D, y = new(f, "Checking a Claim",
                   "Open the source; asking Claude if it's sure isn't a check.",
                   "The fact-checking path: a claim is matched to a quoted passage or cited source, the source is opened "
                   "and compared, and the claim is kept, corrected or removed; asking Claude whether it is sure is not a check.")
        y = lanes(D, y, [
            (None, [("Claim", None, "data"), ("Quote or citation", "Ask Claude for it"), ("Open the source", "Compare, check the date", "focus")], True),
            ("Then", [("Matches: keep", None, "good"), ("Differs: correct", None, "warn"), ("No support: remove", None, "risk")], "apart"),
            ("Not a check", [("\"Are you sure?\"", "Self-rated confidence", "risk"), ("Ask the same question again", None, "risk")], "apart"),
        ])
        return finish(D, y, [("data", "claim"), ("focus", "the check"), ("good", "keep"), ("warn", "fix"), ("risk", "drop / false check")])

    def t2_4(f):
        D, y = new(f, "How Much Review?",
                   "Review grows with the stakes, not with the length.",
                   "A review matrix: low-stakes personal work needs no review, internal work a quick check, external or "
                   "customer-facing work a reviewer, and decisions affecting people's money, health, legal rights or jobs "
                   "need a qualified expert before use.")
        y = table(D, y, [("Output", None, "start"), ("Example", None, "start"), ("Review", None, "start")], [
            [("Personal, low stakes", None, "data"), ("Notes for yourself",), ("Your own read", None, "good")],
            [("Internal", None, "data"), ("Team update",), ("Quick check",)],
            [("External", None, "data"), ("Customer email, public post",), ("A second reviewer", None, "warn")],
            [("Affects people's rights", None, "data"), ("Health, money, legal, jobs",), ("Qualified expert", "Before use", "focus")],
        ], first_w=190)
        return finish(D, y, [("data", "stakes"), ("good", "light"), ("warn", "reviewer"), ("focus", "expert")])

    def t2_5(f):
        D, y = new(f, "Same Facts, Three Audiences",
                   "Keep the facts; change the emphasis, words and length.",
                   "The same project findings adapted for three audiences: a three-line executive summary with the "
                   "decision needed, a team briefing with actions and owners, and a customer FAQ in plain language.")
        y = stack(D, y, [("Project findings", "One set of checked facts", "data")])
        y = lanes(D, y + 18, [(None, [("Executives", "3 lines, decision needed", "focus"), ("Team", "Actions and owners"),
                                       ("Customers", "Plain-language FAQ")], "apart")])
        y = stack(D, y + 6, [("You edit and own each version", "Compare, combine the best parts, check voice", "good")])
        return finish(D, y, [("data", "source"), ("focus", "adapted"), ("good", "your edit")])

    def t2_6(f):
        D, y = new(f, "Format Follows the Next Step",
                   "Ask where the result goes next, then pick the format.",
                   "Format follows the next step: a quick answer stays inline, a document or tool to keep or share becomes "
                   "an artifact or file, and data for a spreadsheet or another tool becomes structured data such as a table or CSV.")
        y = pairs(D, y, [
            (("Quick answer", "Read once", "data"), ("Inline in the chat", "Short, curated"), None),
            (("Keep, edit or share", "Document, timeline, tool", "data"), ("Artifact or file", None, "focus"), None),
            (("Into a spreadsheet or tool", None, "data"), ("Structured data", "Table or CSV, one row per item", "good"), None),
        ], heads=("Where it goes", "Format"))
        return finish(D, y, [("data", "next step"), ("focus", "artifact"), ("good", "structured")])

    # ================================================================== D3 (product and model selection)
    def t3_1(f):
        D, y = new(f, "Match the Need to the Feature",
                   "The lightest feature that fits the shape of the work.",
                   "Matching the need to the feature: a quick one-off question goes to chat, recurring work with the same "
                   "files and rules to a Project, a question spread across many sources to Research, and something to "
                   "keep, edit or share to an artifact.")
        y = pairs(D, y, [
            (("One-off task", None, "data"), ("Chat", "Fastest; context stays in that chat"), None),
            (("Same files and rules, many chats", None, "data"), ("Project", "Instructions + knowledge", "focus"), None),
            (("Answer spread across many sources", None, "data"), ("Research", "Cited report; web search on; paid plans", "good"), None),
            (("Something to keep, edit or share", None, "data"), ("Artifact", "Beside the chat; code execution on", "good"), None),
        ], heads=("Need", "Feature"), lw=250)
        return finish(D, y, [("data", "need"), ("focus", "repeat work"), ("good", "feature")])

    def t3_2(f):
        D, y = new(f, "Three Model Families",
                   "Family names tell you where a model sits; versions change.",
                   "Three model families compared: Haiku is fastest and lowest cost for high-volume simple tasks, Sonnet "
                   "balances speed and capability for everyday work, and Opus is most capable for complex reasoning at "
                   "the highest cost.")
        y = table(D, y, [("Family", None, "start"), ("Strength", None, "start"), ("Best for", None, "start")], [
            [("Haiku", None, "data"), ("Fastest, lowest cost",), ("High-volume, simple tasks", "Short replies, extraction")],
            [("Sonnet", None, "focus"), ("Balanced",), ("Everyday writing and analysis",)],
            [("Opus", None, "data"), ("Most capable", "Uses the most of your limit", "warn"), ("Complex, multi-step reasoning",)],
        ], first_w=130)
        return finish(D, y, [("data", "family"), ("focus", "everyday default"), ("warn", "cost")])

    def t3_3(f):
        D, y = new(f, "Cost, Speed and Quality",
                   "Start light, test a sample, step up only where quality falls short.",
                   "Balancing cost, speed and quality: high-volume simple tasks go to a fast model with default effort, "
                   "everyday work to the balanced model, and complex high-value reasoning to the most capable model with "
                   "higher effort or thinking.")
        y = pairs(D, y, [
            (("High volume, simple", "500 product blurbs", "data"), ("Fast model, default effort", None, "good"), None),
            (("Everyday quality", "Weekly report", "data"), ("Balanced model",), None),
            (("Complex, high value", "Annual strategy memo", "data"), ("Most capable + higher effort or thinking", None, "focus"), None),
        ], heads=("Task", "Choice"))
        y = lanes(D, y + 6, [("Method", [("Test a sample", None, "data"), ("Good enough?", "Keep it"), ("Not yet", "Step up one level", "warn")], True)])
        return finish(D, y, [("data", "task"), ("good", "light"), ("focus", "heavy"), ("warn", "step up")])

    def t3_4(f):
        D, y = new(f, "Restart, Summarise or Persist",
                   "Chats are temporary; save what you'll need again where it will be found.",
                   "Context decisions: a chat that has grown long or drifted is summarised and restarted, information "
                   "needed in every chat is saved to Project knowledge or instructions, earlier conversations are found "
                   "with chat search or memory, and a sensitive one-off chat uses incognito.")
        y = pairs(D, y, [
            (("Long or drifting chat", "Mixing up details", "warn"), ("Summarise, then start a new chat", None, "focus"), None),
            (("Needed in every chat", None, "data"), ("Project knowledge or instructions", None, "good"), None),
            (("Something from an earlier chat", None, "data"), ("Chat search or memory", "Paid plans; memory is editable"), None),
            (("Sensitive one-off", None, "data"), ("Incognito chat", "Not saved to history or memory"), None),
        ], heads=("Situation", "Do this"))
        return finish(D, y, [("warn", "symptom"), ("focus", "restart"), ("good", "persist"), ("data", "situation")])

    # ================================================================== D4 (workflow integration)
    def t4_1(f):
        D, y = new(f, "From Notes to Requirements",
                   "Claude structures and questions; people confirm and decide.",
                   "From messy input to a decision: notes, emails and interviews are turned by Claude into grouped "
                   "requirements, contradictions and open questions, which people confirm before choosing what to "
                   "automate, what to augment and what to keep human.")
        y = converge(D, y, [("Meeting notes", None, "data"), ("Emails", None, "data"), ("Interviews", None, "data")],
                     ("Claude: grouped requirements, contradictions, open questions", None, "neutral"))
        y = lanes(D, y + 20, [(None, [("Stakeholders confirm", "Answer the open questions", "focus"),
                                      ("Decide", "Automate, augment or keep human", "good")], True)])
        return finish(D, y, [("data", "input"), ("focus", "people confirm"), ("good", "decision")])

    def t4_2(f):
        D, y = new(f, "Research, Plan, Optimise",
                   "Three uses, each with its own output and its own check.",
                   "Three uses side by side: research gathers sources and returns a cited report, planning turns a goal "
                   "into steps with owners and risks, and process optimisation maps the current steps to find bottlenecks "
                   "and candidates for Claude.")
        y = table(D, y, [("Use", None, "start"), ("You give", None, "start"), ("You get", None, "start")], [
            [("Research", None, "data"), ("Question and scope",), ("Cited report", "Verify key facts", "good")],
            [("Planning", None, "data"), ("Goal, dates, team, budget",), ("Steps, owners, risks", "You adjust and commit")],
            [("Process optimisation", None, "focus"), ("The current steps",), ("Bottlenecks, duplication, Claude candidates", None, "good")],
        ], first_w=170)
        return finish(D, y, [("data", "use"), ("focus", "process view"), ("good", "output")])

    def t4_3(f):
        D, y = new(f, "Prototype, Test, Hand Over",
                   "Iterate with real users; production integration goes to developers.",
                   "Solution iteration: Claude drafts options, builds a prototype artifact, real users try it, feedback "
                   "drives the next version, and anything needing production integration is handed to developers.")
        y = lanes(D, y, [
            (None, [("Draft options", None, "data"), ("Prototype artifact", None, "focus"), ("Users try it",),
                    ("Feedback themes", "Next version")], True),
            ("Needs integration, security or scale?", [("Hand over to Architects or Developers", "Prototype + requirements", "good")], True),
        ], gap=22)
        return finish(D, y, [("data", "start"), ("focus", "prototype"), ("good", "escalate")])

    def t4_4(f):
        D, y = new(f, "Augment or Redesign",
                   "Start by speeding up a step; change the process once gains are proven.",
                   "Two paths: augmenting adds Claude to one step of the existing workflow, such as drafting the weekly "
                   "report from notes, while redesigning changes the process itself once the gains are proven.")
        y = lanes(D, y, [
            ("Augment", [("Collect notes",), ("Claude drafts report", "Team edits and approves", "focus"), ("Send",)], True),
            ("Redesign", [("One validated extract", None, "data"), ("Claude: table, commentary, summaries", None, "good"),
                          ("Checks kept", "Review before sharing", "good")], True),
            ("Watch for", [("Removing review to go faster", None, "risk"), ("Changing everything at once", None, "warn")], "apart"),
        ])
        return finish(D, y, [("focus", "first step"), ("good", "redesign"), ("warn", "hard to trace"), ("risk", "lost control")])

    def t4_5(f):
        D, y = new(f, "A Balanced Stakeholder Message",
                   "Measured value, honest limits, the safeguards and a clear ask.",
                   "A balanced stakeholder message: measured value such as time saved and consistency on real tasks, "
                   "stated limits such as errors and knowledge gaps, the safeguards in place such as human review, and "
                   "the recommended next step.")
        y = converge(D, y, [("Value", "Hours saved, measured", "good"), ("Limits", "Errors, knowledge gaps", "warn"),
                            ("Safeguards", "Human review, policy", "data")],
                     ("Recommended next step", "Extend, adjust or stop, with the evidence", "focus"))
        y = lanes(D, y + 20, [("Not evidence", [("\"AI can do anything\"", None, "risk"), ("\"Competitors use it\"", None, "risk")], "apart")])
        return finish(D, y, [("good", "value"), ("warn", "limits"), ("data", "safeguards"), ("risk", "hype")])

    # ================================================================== D5 (configuration)
    def t5_1(f):
        D, y = new(f, "Inside a Project",
                   "Chats share the knowledge and instructions, not each other's conversation.",
                   "A Project stacks three layers: instructions that set behaviour for every chat, knowledge files that "
                   "every chat can use, and the chats themselves, which share the knowledge but not each other's conversation.")
        y = stack(D, y, [("Instructions", "Role, tone, format, rules: every chat", "focus"),
                         ("Knowledge", "Files every chat can use; RAG on paid plans when it grows", "data")])
        y = lanes(D, y + 8, [("Chats", [("Chat A",), ("Chat B",), ("Chat C",)], "apart")], gap=14)
        y = lanes(D, y, [("Not shared", [("What chat A said", "Isn't seen by chat B", "warn"), ("Fix", "Add it to knowledge", "good")], True)])
        return finish(D, y, [("focus", "instructions"), ("data", "knowledge"), ("warn", "common mistake"), ("good", "fix")])

    def t5_2(f):
        D, y = new(f, "Uploads or Connectors",
                   "Stable reference gets uploaded; changing data gets connected.",
                   "Choosing between uploads and connectors: a stable policy document is uploaded to Project knowledge, "
                   "while live email, calendar and Drive files are reached through connectors, which only see the "
                   "connected account and ask before sending or deleting.")
        y = pairs(D, y, [
            (("Policy, brand guide, template", "Changes rarely", "data"), ("Upload to knowledge", "Replace when it changes"), None),
            (("Inbox, calendar, live sheets", "Changes daily", "data"), ("Connector", "Gmail, Calendar, Drive", "focus"), None),
        ], heads=("Information", "Use"))
        y = lanes(D, y + 6, [("Connector rules", [("Connected account only", None, "good"), ("Asks before send or delete", None, "good"),
                                                  ("Stored with the chat", None, "neutral")], "apart")], gap=14)
        return finish(D, y, [("data", "information"), ("focus", "live"), ("good", "safeguard")])

    def t5_3(f):
        D, y = new(f, "Three Instruction Layers",
                   "Put each rule at the level where it applies.",
                   "Three instruction layers by scope: account instructions apply to every chat, project instructions "
                   "apply to chats in one Project, and skills add specific behaviour when needed.")
        y = table(D, y, [("Layer", None, "start"), ("Applies to", None, "start"), ("Example", None, "start")], [
            [("Account instructions", None, "data"), ("All your chats",), ("British spelling; answer first",)],
            [("Project instructions", None, "focus"), ("Chats in one Project",), ("Client terms, report template",)],
            [("Skills", None, "data"), ("When needed",), ("A specialised format or method",)],
        ], first_w=180)
        y = lanes(D, y + 4, [("Avoid", [("Client rules in account settings", None, "risk"), ("Conflicting rules across layers", None, "warn")], "apart")])
        return finish(D, y, [("data", "layer"), ("focus", "most task rules"), ("risk", "wrong level"), ("warn", "conflict")])

    def t5_4(f):
        D, y = new(f, "Keeping a Project Current",
                   "A stale Project still answers confidently, from old information.",
                   "The Project maintenance cycle: an owner reviews it on schedule, replaces outdated files with the "
                   "single current version, updates instructions, tests with real questions, and tells users what changed.")
        y = lanes(D, y, [
            (None, [("Owner reviews", "On schedule or on change", "data"), ("Replace old files", "One current version", "focus"),
                    ("Update instructions",), ("Test real questions",), ("Tell users", None, "good")], True),
            ("Avoid", [("Old and new side by side", None, "risk"), ("No owner", None, "warn")], "apart"),
        ], gap=18)
        return finish(D, y, [("data", "trigger"), ("focus", "key step"), ("good", "done"), ("risk", "conflict")])

    # ================================================================== D6 (governance)
    def t6_1(f):
        D, y = new(f, "Three Zones of Use",
                   "Ask who is affected, and what happens if Claude is wrong.",
                   "Three zones of use: green for drafting, summarising and research with a human owner; amber for "
                   "decisions affecting health, money, legal rights or jobs, which need a qualified human in the loop and "
                   "disclosure; red for uses prohibited by the Usage Policy or company policy.")
        y = lanes(D, y, [(None, [
            ("Green: go", "Drafting, summaries, research; a person reviews", "good"),
            ("Amber: human in the loop", "Health, money, legal rights, jobs; plus disclosure", "warn"),
            ("Red: stop", "Prohibited by the Usage Policy or company policy", "risk")], "apart")], gap=14)
        y = stack(D, y, [("Fix for amber", "A qualified person makes the decision, not a better prompt", "focus")])
        return finish(D, y, [("good", "appropriate"), ("warn", "controls needed"), ("risk", "not allowed"), ("focus", "the fix")])

    def t6_2(f):
        D, y = new(f, "Check the Data Before Uploading",
                   "Once it's uploaded, it's shared.",
                   "A data check before uploading: identify the data type, check the organisation's policy and the plan "
                   "in use, then remove or anonymise identifiers, use an approved workspace, or don't upload at all.")
        y = lanes(D, y, [(None, [("What is the data?", "Personal, confidential, regulated?", "data"),
                                 ("Policy and plan", "What's allowed, where"), ("Minimise", "Only the columns needed", "focus")], True)])
        y = lanes(D, y, [("Then", [("Anonymise identifiers", None, "good"), ("Approved workspace", None, "good"),
                                   ("Don't upload", None, "warn")], "apart")])
        y = lanes(D, y, [("Not controls", [("\"Don't remember this\"", None, "risk"), ("\"It's only internal\"", None, "risk")], "apart")])
        return finish(D, y, [("data", "classify"), ("focus", "minimise"), ("good", "safe path"), ("risk", "not a control")])

    def t6_3(f):
        D, y = new(f, "Policy in Practice",
                   "Silence in the policy isn't permission.",
                   "Policy in practice: use the approved workspace, not a personal account; respect admin settings; follow "
                   "data and disclosure rules; and when the policy is silent, ask its owner before acting.")
        y = pairs(D, y, [
            (("Company data", None, "data"), ("Approved workspace", "Not a personal account", "good"), None),
            (("Feature or connector off", None, "data"), ("Respect admin settings", "Request a change", "good"), None),
            (("Data and disclosure rules", None, "data"), ("Follow them", None, "good"), None),
            (("Policy is silent", None, "warn"), ("Ask the policy owner first", None, "focus"), None),
        ], heads=("Situation", "Do this"))
        return finish(D, y, [("data", "covered"), ("warn", "not covered"), ("good", "follow"), ("focus", "ask")])

    def t6_4(f):
        D, y = new(f, "Four Ethical Responsibilities",
                   "Whoever sends it answers for it.",
                   "Four ethical responsibilities: be transparent about AI's role, own and check the result, check for "
                   "bias and fairness toward the people affected, and respect privacy and intellectual property.")
        y = converge(D, y, [("Transparency", "Say when AI shaped it", "data"), ("Fairness", "Check outputs about people", "data"),
                            ("Respect", "Privacy and IP", "data")],
                     ("Accountability", "You own the result, whoever drafted it", "focus"))
        y = lanes(D, y + 20, [("Never", [("\"The AI is responsible\"", None, "risk")], "apart")])
        return finish(D, y, [("data", "responsibility"), ("focus", "ownership"), ("risk", "wrong")])

    # ================================================================== D7 (troubleshooting)
    def t7_1(f):
        D, y = new(f, "Symptom, Cause, Fix",
                   "Diagnose first, then change one thing and retest.",
                   "Symptoms traced to causes and fixes: generic output to missing context, wrong facts to a missing or "
                   "stale source, ignored format to vague instructions, shallow reasoning to the model or effort setting, "
                   "and mixed-up details to an overlong chat.")
        y = table(D, y, [("Symptom", None, "start"), ("Likely cause", None, "start"), ("Fix", None, "start")], [
            [("Generic output", None, "warn"), ("Missing context",), ("Goal, audience, details",)],
            [("Wrong facts", None, "warn"), ("Missing or stale source", None, "focus"), ("Provide or replace it",)],
            [("Format ignored", None, "warn"), ("Vague instruction",), ("Be specific; show an example",)],
            [("Shallow reasoning", None, "warn"), ("Model or effort",), ("Decompose, or step up",)],
            [("Mixed-up details", None, "warn"), ("Overlong chat",), ("Summarise and restart",)],
        ], first_w=160)
        return finish(D, y, [("warn", "symptom"), ("focus", "most common in Projects")])

    def t7_2(f):
        D, y = new(f, "The Adjustment Ladder",
                   "Fix it at the lowest level that stops it happening again.",
                   "An adjustment ladder: fix a one-off issue in the chat, update the prompt template for repeat tasks, "
                   "update Project instructions or knowledge for recurring issues, change the model or feature if quality "
                   "still falls short, and escalate to Architects or Developers when configuration can't solve it.")
        y = stack(D, y, [
            ("Fix it in the chat", "Happened once", "data"),
            ("Update the prompt template", "Repeat task, same fix"),
            ("Update Project instructions or knowledge", "Recurring across people", "focus"),
            ("Change the model or feature", "Quality still falls short"),
            ("Escalate to Architects or Developers", "Needs integration or a custom build", "good"),
        ])
        return finish(D, y, [("data", "one-off"), ("focus", "recurring"), ("good", "beyond configuration")])

    def t7_3(f):
        D, y = new(f, "Efficiency Levers",
                   "Less repeated effort, same quality.",
                   "Efficiency levers: reuse Projects instead of re-uploading, batch related requests, pick the right model "
                   "and effort, restart long chats with a summary, and keep prompt templates, while checking quality "
                   "still meets the need.")
        y = converge(D, y, [("Reuse Projects", "No re-uploads", "data"), ("Batch requests", None, "data"),
                            ("Right model", None, "data"), ("Fresh chats", None, "data"), ("Templates", None, "data")],
                     ("Faster, lighter workflow", None, "focus"))
        y = lanes(D, y + 20, [("Then", [("Quality still meets the need?", None, "good"), ("If not, it isn't an optimisation", None, "warn")], "apart")])
        return finish(D, y, [("data", "lever"), ("focus", "result"), ("good", "check"), ("warn", "false gain")])

    fns = {
        "ccao-1-1-prompt-anatomy": t1_1, "ccao-1-2-decomposition": t1_2, "ccao-1-3-iterate": t1_3, "ccao-1-4-task-types": t1_4,
        "ccao-2-1-accuracy-completeness": t2_1, "ccao-2-2-red-flags": t2_2, "ccao-2-3-fact-check": t2_3,
        "ccao-2-4-review-matrix": t2_4, "ccao-2-5-audiences": t2_5, "ccao-2-6-formats": t2_6,
        "ccao-3-1-features": t3_1, "ccao-3-2-models": t3_2, "ccao-3-3-tradeoffs": t3_3, "ccao-3-4-context": t3_4,
        "ccao-4-1-requirements": t4_1, "ccao-4-2-research-plan-optimize": t4_2, "ccao-4-3-prototype": t4_3,
        "ccao-4-4-augment-redesign": t4_4, "ccao-4-5-communicate": t4_5,
        "ccao-5-1-project": t5_1, "ccao-5-2-uploads-connectors": t5_2, "ccao-5-3-instruction-layers": t5_3, "ccao-5-4-maintain": t5_4,
        "ccao-6-1-use-zones": t6_1, "ccao-6-2-data-check": t6_2, "ccao-6-3-policy": t6_3, "ccao-6-4-ethics": t6_4,
        "ccao-7-1-diagnose": t7_1, "ccao-7-2-adjust": t7_2, "ccao-7-3-optimize": t7_3,
    }
    return {name: ("ccao", fn) for name, fn in fns.items()}
