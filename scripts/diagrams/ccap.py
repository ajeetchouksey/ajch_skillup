"""CCAP diagrams (domains 1-2): feedback loop, pattern selection,
orchestrator + subagents, prompt-caching sequence."""


def register(api):
    Diagram = api["Diagram"]
    SLATE7, SLATE4 = api["SLATE7"], api["SLATE4"]

    def feedback_loop(f):
        D = Diagram(f, 430, "End-to-End Architecture with a Feedback Loop",
                    "Four stages carry each request; the feedback loop is the return path that makes it production-grade.",
                    "Main flow left to right: Input (ingestion and context assembly) to Processing (model call, tool "
                    "loop or agent delegation) to Output (validation, guardrails and formatting) to Delivery (user or "
                    "downstream system). Output also feeds the Feedback Loop (logging, eval, human review). The "
                    "feedback loop sends retraining and prompt updates back to Processing, and corrections back to "
                    "Input.")
        cy, w, h = 160, 144, 100
        xs = [97, 259, 421, 583]
        spec = [("Input", "ingestion + context assembly", "data"),
                ("Processing", "model call / tool loop / agent delegation", "neutral"),
                ("Output", "validation + guardrails + formatting", "neutral"),
                ("Delivery", "user / downstream system", "neutral")]
        bs = [D.box(x, cy, w, t, b, kind=k, h=h) for x, (t, b, k) in zip(xs, spec)]
        for a, b in zip(bs, bs[1:]):
            D.edge([(a["r"], cy), (b["l"], cy)])
        fb = D.box(540, 330, 200, "Feedback Loop", "logging, eval, human review", kind="focus", h=90)
        D.edge([(470, bs[2]["b"]), (470, fb["t"])])
        D.edge([(fb["l"], 310), (259, 310), (259, bs[1]["b"])], dashed=True,
               label="retraining / prompt updates", at=(267, 262), anchor="start")
        D.edge([(fb["l"], 350), (97, 350), (97, bs[0]["b"])], dashed=True,
               label="corrections", at=(105, 262), anchor="start")
        D.legend(410, [("data", "input"), ("focus", "feedback loop"), ("solid", "main flow"), ("dashed", "return path")])
        return D

    def arch_patterns(f):
        D = Diagram(f, 494, "Selecting an Architectural Pattern",
                    "One question decides the tier: can the steps be fully specified in advance?",
                    "Decision: can the steps be fully specified in advance? Yes, as a single step: use an Augmented "
                    "LLM, a single call enhanced with retrieval, tools and memory. Yes, as a fixed multi-step sequence: "
                    "use a Workflow, where the developer fixes the sequence; sub-patterns are chaining, routing, "
                    "parallel, orchestrator-workers and evaluator-optimizer. No, the steps depend on what is "
                    "discovered: use an Agentic System, where the model decides the sequence at runtime.")
        d = D.diamond(340, 160, 400, 124, "Can the steps be fully\nspecified in advance?")
        cols, by, bh = [124, 340, 556], 368, 128
        boxes = [
            D.box(cols[0], by, 200, "Augmented LLM", "Single call + retrieval, tools, memory", h=bh),
            D.box(cols[1], by, 200, "Workflow",
                  "chaining / routing / parallel / orchestrator-workers / evaluator-optimizer",
                  sub="sequence fixed by developer", h=bh),
            D.box(cols[2], by, 200, "Agentic System", "Model decides the sequence at runtime", h=bh),
        ]
        labels = ["yes, single step", "yes, fixed multi-step", "no, depends on what's discovered"]
        for i, (x, b, lab) in enumerate(zip(cols, boxes, labels)):
            pts = [(340, d["b"]), (340, 250), (x, 250), (x, b["t"])] if x != 340 else [(340, d["b"]), (340, b["t"])]
            D.edge(pts, dashed=(i == 2), label=lab, at=(x, 282))
        D.legend(474, [("solid", "yes"), ("dashed", "no")])
        return D

    def orchestrator(f):
        D = Diagram(f, 610, "Orchestrator + Subagents",
                    "A lead agent fans work out to subagents, each with its own context and scoped tools.",
                    "The user query goes to the orchestrator, or lead agent. The orchestrator dispatches work to "
                    "Subagent 1, Subagent 2 and Subagent 3, each with its own context and scoped tools; the link to "
                    "Subagent 2 is drawn two-way. All three subagents feed Result Synthesis. The orchestrator "
                    "delivers the final output to the user.")
        C, R = 320, 650
        q = D.box(C, 112, 220, "User Query", kind="data", h=48)
        o = D.box(C, 200, 280, "Orchestrator / Lead Agent", kind="focus", h=56)
        D.edge([(C, q["b"]), (C, o["t"])])
        xs, sy = [120, 320, 520], 326
        subs = [D.box(x, sy, 180, f"Subagent {i + 1}", "own context + scoped tools", h=68) for i, x in enumerate(xs)]
        D.edge([(230, o["b"]), (230, 256), (xs[0], 256), (xs[0], subs[0]["t"])])
        D.edge([(C, o["b"]), (C, subs[1]["t"])])
        D.back[-1] = D.back[-1].replace("marker-end=", 'marker-start="url(#arrow)" marker-end=')
        D.edge([(410, o["b"]), (410, 256), (xs[2], 256), (xs[2], subs[2]["t"])])
        syn = D.box(C, 444, 220, "Result Synthesis", h=48)
        D.edge([(xs[0], subs[0]["b"]), (xs[0], 444), (syn["l"], 444)])
        D.edge([(C, subs[1]["b"]), (C, syn["t"])])
        D.edge([(xs[2], subs[2]["b"]), (xs[2], 444), (syn["r"], 444)])
        out = D.box(C, 532, 240, "Final Output to User", h=48)
        D.edge([(o["r"], 200), (R, 200), (R, 532), (out["r"], 532)])
        D.legend(590, [("data", "input"), ("focus", "lead agent"), ("solid", "flow")])
        return D

    def caching(f):
        D = Diagram(f, 672, "Prompt Caching Across Requests",
                    "Put the static prefix before the cache breakpoint; only the user query changes per request.",
                    "Sequence between a client and the Claude API. A static prefix (system prompt, tool definitions, "
                    "examples) ends at a cache_control breakpoint. Request 1 sends the static prefix plus user query A; "
                    "the response is a cache miss on the prefix, with full processing and a cache write. Request 2 "
                    "sends the static prefix plus user query B; the response is a cache hit on the prefix, reused, "
                    "cheap and fast. Request 3 sends the static prefix plus user query C; the response is a cache hit, "
                    "with the prefix reused again within the TTL.")
        CL, API, top, bot = 90, 590, 112, 626
        for x in (CL, API):
            D.back.insert(0, f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bot}" stroke="{SLATE7}" '
                             f'stroke-width="1.5" stroke-dasharray="4 4"/>')
        D.box(CL, top, 140, "Client", kind="data", h=44)
        D.box(API, top, 140, "Claude API", h=44)
        D.box(340, 186, 600, "Static prefix",
              "system prompt, tool defs, examples, ending at a cache_control breakpoint", kind="focus", h=58)
        reqs = [("A", "cache MISS on prefix", "full processing, cache write", "neutral"),
                ("B", "cache HIT on prefix", "reused, cheap + fast", "good"),
                ("C", "cache HIT", "prefix reused again within TTL", "good")]
        y = 250
        for i, (qry, sub, body, kind) in enumerate(reqs):
            D.edge([(CL, y + 14), (API, y + 14)], label=f"Request {i + 1}: [Static Prefix] + [User Query {qry}]",
                   at=(CL + 10, y + 3), anchor="start")
            cy = y + 64
            D.edge([(API, cy), (CL, cy)], dashed=True)
            D.box(340, cy, 400, "Response", body, kind=kind, sub=sub, h=66)
            y += 130
        D.legend(652, [("focus", "cached prefix"), ("good", "cache hit"), ("solid", "request"), ("dashed", "response")])
        return D

    return {
        "ccap-d1-feedback-loop": ("ccap", feedback_loop),
        "ccap-d1-architecture-patterns": ("ccap", arch_patterns),
        "ccap-d1-orchestrator-subagents": ("ccap", orchestrator),
        "ccap-d2-prompt-caching": ("ccap", caching),
    }
