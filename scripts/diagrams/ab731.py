"""AB-731 (AI Transformation Leader) lesson diagrams: one outcome diagram per lesson.

The lessons that already had a fitting diagram keep it (ab731_d1/d2/d3.py); these cover the rest.
Same five layouts as the GH-BP diagrams so every lesson reads the same way:
  lanes   one or more captioned rows of steps, left to right (the good lane is the hot path)
  pairs   need → answer rows (threat → control, need → product)
  table   a comparison grid with a header row
  funnel  one input, a row of gates, one outcome
  stack   layered boxes, most important at the top
Colours follow the SkillUp colour code by meaning: data sky, good green, warn saffron,
risk rose, focus indigo (one focal element per diagram), neutral slate.
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
        it = list(it) + [None] * 4
        return it[0], it[1], it[2] or "neutral", it[3]

    def caption(D, x, y, s, anchor="start"):
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

    # ================================================================== D1
    def d1_2(f):
        D, y = new(f, "Match the Solution to the Shape of the Work",
                   "One prompted task needs Copilot; a goal across steps, systems or days needs an agent.",
                   "Four business needs matched to a solution: a one-off draft to Copilot, a research report to the "
                   "Researcher agent, a goal across systems and days to a custom agent, and a fixed rule-based file move "
                   "to scripted automation.")
        y = pairs(D, y, [
            (("One follow-up email", "One prompt, one session", "data"), ("Microsoft 365 Copilot", "Assistive: a person prompts it"), None),
            (("Report from web + internal docs", None, "data"), ("Researcher agent", "Built-in, already fits"), None),
            (("Weeks-long negotiation", "Remember history, act each morning", "data"), ("Custom agent", "Plans steps, keeps state, uses tools", "focus"), None),
            (("Rename and move files nightly", "Same fixed steps every time", "data"), ("Scripted automation", "Not an agent: no reasoning", "warn"), None),
        ], heads=("Business need", "Solution"))
        return finish(D, y, [("data", "need"), ("neutral", "assistive or built-in"), ("focus", "agentic"), ("warn", "not AI")])

    def d1_3(f):
        D, y = new(f, "Customise in This Order",
                   "Each step costs more than the last, so climb only when the cheaper one can't close the gap.",
                   "A ladder of customisation: prompt engineering first, then grounding with RAG for knowledge gaps, "
                   "then fine-tuning only for a persistent style or vocabulary gap.")
        y = lanes(D, y, [
            (None, [("1. Prompt engineering", "Free, instant; fixes vague or generic output", "focus"),
                    ("2. Ground with RAG", "Knowledge gap: private, current, cited facts", "data"),
                    ("3. Fine-tune", "Behaviour gap: stable style or vocabulary at volume", "warn")], True),
            ("Never", [("Fine-tune changing facts", "Stale the day the source changes; no citations", "risk")], None),
        ])
        return finish(D, y, [("focus", "try first"), ("data", "knowledge"), ("warn", "costly"), ("risk", "wrong tool")])

    def d1_4(f):
        D, y = new(f, "The Token Meter and ROI",
                   "Tokens in and out set the cost per request; volume sets the bill; value sets the return.",
                   "Cost per request is input tokens plus output tokens times the model's price; multiplied by monthly "
                   "volume it gives operating cost, which is set against time saved, quality and scale to give ROI.")
        y = lanes(D, y, [
            ("Cost", [("Input tokens", "Prompt + retrieved text", "data"),
                      ("Output tokens", "The response", "data"),
                      ("× price × volume", "Monthly operating cost", "warn")], True),
            ("Value", [("Time saved", "Hours × rate", "good"),
                       ("Quality lift", "Fewer errors", "good"),
                       ("Scale", "More output, same team", "good")], True),
        ])
        y = stack(D, y + 6, [("ROI: value created set against AI cost","Cheapest per token isn't cheapest overall if wrong answers are costly", "focus")])
        return finish(D, y - 10, [("data", "tokens"), ("warn", "cost"), ("good", "value"), ("focus", "decision")])

    def d1_5(f):
        D, y = new(f, "Three Built-in Challenges and Their Fixes",
                   "Each comes from how the model works, so each needs a structural mitigation.",
                   "Three challenges and their mitigations: fabrication is countered by grounding and human review, "
                   "unreliability by low temperature and evaluation, and bias by representative data and evaluation "
                   "across groups.")
        y = pairs(D, y, [
            (("Fabrication", "Fluent, confident, false", "risk"), ("Ground on verified sources", "Plus human review where stakes are high", "good"), None),
            (("Reliability", "Same input, different output", "warn"), ("Low temperature + evaluation", "Test consistency before launch", "good"), None),
            (("Bias", "Historical, representation, measurement", "risk"), ("Representative data", "Evaluate results group by group", "good"), None),
        ], heads=("Challenge", "Mitigation"), hot_kind="good")
        return finish(D, y, [("risk", "harm"), ("warn", "variance"), ("good", "mitigation")])

    def d1_7(f):
        D, y = new(f, "What a Better Prompt Changes",
                   "Same model, same cost: only the brief is different.",
                   "A vague prompt produces a generic draft, while a prompt with goal, context, audience, format and an "
                   "example produces an on-brand draft; only facts the model never saw need grounding instead.")
        y = lanes(D, y, [
            ("Vague prompt", [("\"Write a campaign proposal\"", None, "data"), ("Model fills the gaps", "With its own guesses"),
                              ("Generic draft", "Off-brand, rewritten by hand", "warn")], None),
            ("Engineered prompt", [("Goal, audience, format", "+ brand guide and a sample", "data"), ("Model follows the brief",),
                                   ("On-brand draft", "Usable first time", "focus")], True),
            ("Still missing", [("Facts it never saw", "Private or current data", "data"), ("No prompt can add them",),
                               ("Ground it (1.9)", None, "good")], True),
        ])
        return finish(D, y, [("data", "input"), ("warn", "weak result"), ("focus", "prompt fix"), ("good", "grounding fix")])

    def d1_8(f):
        D, y = new(f, "Prompting Techniques: Pick by the Gap",
                   "Each technique fixes one kind of problem.",
                   "Five prompting techniques and the gap each fixes: zero-shot for simple clear tasks, few-shot for a "
                   "format or style, chain-of-thought for multi-step reasoning, role prompting for voice and expertise, "
                   "and a system prompt for rules on every turn.")
        y = pairs(D, y, [
            (("Simple, clear task", None, "data"), ("Zero-shot", "Ask directly"), None),
            (("Must match a format or style", None, "data"), ("Few-shot", "2–5 examples first", "focus"), None),
            (("Multi-step reasoning", None, "data"), ("Chain-of-thought", "\"Work through it step by step\""), None),
            (("Needs a voice or expertise", None, "data"), ("Role prompting", "\"You are a senior counsel…\""), None),
            (("Rules for every turn", None, "data"), ("System prompt", "Set once by the builder"), None),
        ], heads=("Gap", "Technique"))
        return finish(D, y, [("data", "gap"), ("neutral", "technique"), ("focus", "most used")])

    def d1_9(f):
        D, y = new(f, "Business Requirements That Call for Grounding",
                   "Any one of them means the model must answer from your sources, not its memory.",
                   "Four business requirements, answers must be current, organisation-specific, verifiable with a "
                   "citation, and limited to what the user may see, all point to grounding on an authoritative source.")
        y = converge(D, y, [("Current", "Facts change weekly", "data"), ("Organisation-specific", "Lives in our docs", "data"),
                            ("Verifiable", "Must cite a source", "data"), ("Permission-aware", "Only what the user may see", "data")],
                     ("Ground on one authoritative, owned source", "Then build retrieval on it (RAG)", "focus"))
        return finish(D, y, [("data", "requirement"), ("focus", "grounding")])

    def d1_11(f):
        D, y = new(f, "Data Decides the Answer",
                   "AI amplifies whatever it's given, so fix the data at the source.",
                   "Four data factors flow into an AI solution: data type must match the model, quality errors propagate "
                   "into answers, unrepresentative data fails missing groups, and stale data gives outdated insights.")
        y = pairs(D, y, [
            (("Data type", "Text, images, tables, audio", "data"), ("Model must handle that type", None), None),
            (("Data quality", "Duplicates, conflicts, errors", "data"), ("Errors repeated in answers", None, "risk"), None),
            (("Representativeness", "Groups or languages missing", "data"), ("Fails the people left out", None, "risk"), None),
            (("Recency", "Out-of-date records", "data"), ("Outdated insights", None, "warn"), None),
        ], heads=("Factor", "Impact"))
        y = stack(D, y + 4, [("Fix upstream: one owned, clean, current source", "Not with prompts or a bigger model", "focus")])
        return finish(D, y - 10, [("data", "data factor"), ("risk", "wrong answers"), ("warn", "stale"), ("focus", "fix")])

    def d1_12(f):
        D, y = new(f, "Reach Multiplies Risk",
                   "The more an AI can read, reach and do, the further one weakness travels.",
                   "What the AI can reach multiplies the impact of one weakness: a model alone has limited exposure, a "
                   "model reading untrusted content can be manipulated, and a model with data and actions can leak data "
                   "or act at scale.")
        y = lanes(D, y, [
            (None, [("Model alone", "Rewrites pasted text", "good"),
                    ("+ reads untrusted content", "Can be manipulated", "warn"),
                    ("+ data and actions", "Leaks or acts at scale", "risk")], True),
        ])
        y = stack(D, y + 6, [("Design security in: least access, filtered input, authentication, monitoring",
                              "One leak can stop the whole AI programme", "focus")])
        return finish(D, y - 10, [("good", "low exposure"), ("warn", "manipulable"), ("risk", "high impact"), ("focus", "response")])

    def d1_13(f):
        D, y = new(f, "Where Traditional ML Earns Its Place",
                   "A fixed output, structured history and thousands of repeat decisions.",
                   "Four structured-data needs that suit traditional ML: score fraud risk per transaction, forecast "
                   "demand, predict churn or delay, and detect anomalies in sensor readings.")
        y = pairs(D, y, [
            (("Is this transaction fraud?", None, "data"), ("Classification", "Risk score per transaction", "focus"), None),
            (("How much will we sell?", None, "data"), ("Regression", "Demand forecast"), None),
            (("Which shipments will be late?", None, "data"), ("Prediction", "Delay probability"), None),
            (("Is this sensor reading odd?", None, "data"), ("Anomaly detection", "Alert on outliers"), None),
        ], heads=("Business question", "ML approach"))
        return finish(D, y, [("data", "structured history"), ("neutral", "ML output"), ("focus", "example")])

    def d1_14(f):
        D, y = new(f, "The ML Lifecycle Is a Loop",
                   "Deployment starts the job; monitoring and retraining never stop.",
                   "The machine learning lifecycle as a loop: define the problem, prepare data, train, validate, deploy, "
                   "monitor, then retrain and return to training when performance drifts.")
        y = lanes(D, y, [
            ("Build", [("Define problem", "Agree the metric", "data"), ("Prepare data", "Representative, split"),
                       ("Train",), ("Validate", "On unseen data")], True),
            ("Run, for as long as it's live", [("Deploy", "Scores live inputs"), ("Monitor", "Accuracy, drift", "focus"),
                                               ("Drift detected", "World changed", "warn"), ("Retrain", "Back to validate", "good")], True),
        ], gap=24)
        return finish(D, y, [("data", "start"), ("focus", "owned by someone"), ("warn", "concept drift"), ("good", "recovery")])

    def d1_15(f):
        D, y = new(f, "AI Threats and Their Controls",
                   "Match the signature to the threat, then apply its control.",
                   "Four AI threats matched to controls: prompt injection to input filtering and treating content as "
                   "data, data poisoning to validated training sources, model extraction to rate limits and anomaly "
                   "detection, and data leakage to authentication and per-user data scoping.")
        y = pairs(D, y, [
            (("Prompt injection", "Instructions hidden in input", "risk"), ("Treat input as data", "Filter input; Prompt Shields; least privilege", "good"), None),
            (("Data poisoning", "Tainted data in training", "risk"), ("Validate data sources", "Audit what feeds training", "good"), None),
            (("Model extraction", "Mass varied queries, one key", "risk"), ("Rate limits + anomaly alerts", "Coarser outputs", "good"), None),
            (("Data leakage", "One user sees another's data", "risk"), ("Authenticate, scope per user", "Retrieval runs as the user", "focus"), None),
        ], heads=("Threat", "Control"), hot_kind="good")
        return finish(D, y, [("risk", "threat"), ("good", "control"), ("focus", "authentication")])

    # ================================================================== D2
    def d2_2(f):
        D, y = new(f, "Three Copilots, Three Reaches",
                   "They differ most in how much of your organisation's data they can use.",
                   "Three Copilot versions compared: Microsoft Copilot for personal accounts grounded on the web, Copilot "
                   "Chat included for work accounts with enterprise data protection, and licensed Microsoft 365 Copilot "
                   "grounded in Microsoft Graph inside the apps.")
        y = table(D, y, [("Compare", None, "start"), ("Microsoft Copilot", "Consumer"), ("Copilot Chat", "Work, included", "data"),
                         ("Microsoft 365 Copilot", "Work, licensed", "focus")], [
            [("Grounding",), ("Web",), ("Web + uploads + agents",), ("Web + Microsoft Graph", None, "good")],
            [("Enterprise data protection",), ("No", None, "risk"), ("Yes", None, "good"), ("Yes", None, "good")],
            [("In Word, Excel, Teams with org data",), ("No",), ("No",), ("Yes", None, "good")],
            [("Cost",), ("Free",), ("No extra cost",), ("Per user per month", None, "warn")],
        ], first_w=150)
        return finish(D, y, [("data", "everyone at work"), ("focus", "full org data"), ("good", "yes"), ("risk", "no")])

    def d2_4(f):
        D, y = new(f, "Copilot Where the Content Lives",
                   "Open Copilot in the app that already holds the task's material.",
                   "Microsoft 365 apps matched to their Copilot strengths: Word drafts and rewrites, Excel analyses and "
                   "charts, PowerPoint builds decks from documents, Outlook summarises threads and drafts replies, Teams "
                   "recaps meetings, and Pages keeps a shared AI canvas.")
        y = pairs(D, y, [
            (("Word", "Documents", "data"), ("Draft, rewrite, summarise", None), None),
            (("Excel", "Tables", "data"), ("Analyse, formulas, charts", None), None),
            (("PowerPoint", "Slides", "data"), ("Deck from a prompt or a Word doc", None), None),
            (("Outlook", "Threads", "data"), ("Summarise, draft replies", None), None),
            (("Teams", "Meetings and chats", "data"), ("Recap: decisions, action items", None, "focus"), None),
            (("Copilot Pages", "Shared canvas", "data"), ("Team keeps building on AI output", None, "good"), None),
        ], lw=200, heads=("Where content lives", "What Copilot does"))
        return finish(D, y, [("data", "app"), ("focus", "missed meeting"), ("good", "collaboration")])

    def d2_7(f):
        D, y = new(f, "What an Integrated Stack Gives You",
                   "New AI inherits controls you already run, instead of rebuilding them per tool.",
                   "An integrated Microsoft AI solution stacks four shared protections: one identity and permission "
                   "model, enterprise data protection, Microsoft Purview compliance on AI interactions, and built-in "
                   "safety and evaluations in Microsoft Foundry.")
        y = stack(D, y, [
            ("Copilot, agents and Foundry apps", "The AI your people use", "focus"),
            ("One identity and permission model", "Microsoft Entra ID; existing Microsoft 365 permissions", "good"),
            ("Enterprise data protection", "Prompts and responses protected; not used to train foundation models", "good"),
            ("Microsoft Purview on AI interactions", "Sensitivity labels, retention, DLP, audit", "good"),
            ("Built-in safety for custom builds", "Foundry content filters, Prompt Shields, evaluations", "good"),
        ])
        return finish(D, y - 10, [("focus", "AI layer"), ("good", "inherited control")])

    def d2_9(f):
        D, y = new(f, "Researcher, Analyst or a Custom Agent",
                   "Choose by the input: documents, a dataset, or a company-specific process.",
                   "Choosing a reasoning agent: documents and web sources go to Researcher for a cited report, a dataset "
                   "goes to Analyst for code-driven analysis and charts, and a company-specific process goes to a custom "
                   "Copilot Studio agent.")
        y = pairs(D, y, [
            (("Documents + web sources", "News, papers, internal decks", "data"), ("Researcher", "Multi-step research; cited report", "focus"), None),
            (("A dataset", "50,000 rows of sales", "data"), ("Analyst", "Runs Python; trends and charts", "focus"), None),
            (("Company-specific process", "Own rules and systems", "data"), ("Custom agent", "Built in Copilot Studio"), None),
            (("Quick formula, small sheet", None, "data"), ("Copilot in Excel", "Faster than a reasoning agent"), None),
        ], heads=("Input", "Use"))
        return finish(D, y, [("data", "input"), ("focus", "built-in reasoning agent"), ("neutral", "other option")])

    def d2_10(f):
        D, y = new(f, "Buy, Extend, Build",
                   "Each step down adds cost, time and maintenance, so each needs a reason.",
                   "Buy, extend or build: buy uses Microsoft 365 Copilot as is, extend adds connectors, actions and "
                   "declarative agents, and build creates a custom engine agent or Foundry app.")
        y = lanes(D, y, [
            ("Buy", [("Microsoft 365 Copilot", "As it is", "good")], True),
            ("Extend: name the gap", [("Knowledge", "Copilot connector", "focus"), ("Action", "API plugin or MCP server", "focus"),
                                      ("Focus", "Declarative agent", "focus")], "apart"),
            ("Build", [("Custom engine agent", "Own model and orchestration", "warn"), ("Microsoft Foundry app", "External users, product features", "warn")], "apart"),
        ])
        return finish(D, y, [("good", "first choice"), ("focus", "extensibility framework"), ("warn", "highest effort")])

    def d2_11(f):
        D, y = new(f, "Map Each Step to a Foundry Tool",
                   "Most custom AI processes are a chain of prebuilt capabilities.",
                   "A process broken into steps, each mapped to a Foundry Tool: read a photo with Azure Vision, extract "
                   "form fields with Document Intelligence, find relevant records with Azure AI Search, transcribe calls "
                   "with Speech, and generate the answer with a Foundry model.")
        y = pairs(D, y, [
            (("Identify a product in a photo", None, "data"), ("Azure Vision", "Image analysis, OCR"), None),
            (("Pull fields from invoices", None, "data"), ("Document Intelligence", "Forms and documents"), None),
            (("Find matching catalogue items", None, "data"), ("Azure AI Search", "Vector + semantic retrieval", "focus"), None),
            (("Transcribe support calls", None, "data"), ("Speech", "Speech to text"), None),
            (("Write the reply", None, "data"), ("Foundry model", "Generates from retrieved context"), None),
        ], heads=("Process step", "Foundry Tool"))
        return finish(D, y, [("data", "step"), ("neutral", "prebuilt tool"), ("focus", "retrieval for RAG")])

    def d2_12(f):
        D, y = new(f, "Microsoft Foundry and Two of Its Tools",
                   "The platform builds and runs the app; the tools do specialised jobs inside it.",
                   "Three capabilities: Microsoft Foundry as the platform for models, agents, evaluation, deployment and "
                   "monitoring; Azure Vision for image analysis and OCR; and Azure AI Search for keyword, vector and "
                   "semantic retrieval.")
        y = stack(D, y, [("Microsoft Foundry", "Model catalog, agents, evaluations, content safety, deployment, monitoring", "focus")])
        y = lanes(D, y + 8, [
            ("Foundry Tools it plugs in", [("Azure Vision", "Captions, tags, objects, OCR", "data"),
                                           ("Azure AI Search", "Keyword, vector, semantic search", "data"),
                                           ("Others", "Speech, Language, Translator, Document Intelligence")], "apart"),
        ])
        return finish(D, y, [("focus", "platform"), ("data", "named in the study guide"), ("neutral", "more tools")])

    def d2_14(f):
        D, y = new(f, "Why Build on Microsoft Foundry",
                   "Scale, security, choice and safety come with the platform.",
                   "Four benefits of Microsoft Foundry and Foundry Tools: scalability on Azure from prototype to "
                   "production, security with Entra ID and private networking, choice of models from many providers, "
                   "and governance with content safety and evaluations.")
        y = converge(D, y, [("Scalability", "Prototype to millions of users", "good"),
                            ("Security", "Entra ID, private networking", "good"),
                            ("Choice", "Many model providers", "good"),
                            ("Governance", "Content safety, evaluations", "good")],
                     ("A custom AI app you can trust in production", "Without building the plumbing yourself", "focus"))
        return finish(D, y, [("good", "benefit"), ("focus", "outcome")])

    # ================================================================== D3
    def d3_2(f):
        D, y = new(f, "From Principle to Governance",
                   "A principle changes nothing until it's a policy with an owner, a control and a record.",
                   "Governance turns a principle into practice in four steps: a principle such as fairness becomes a "
                   "written policy, the policy gets a named owner and control, and the control leaves an audit trail.")
        y = lanes(D, y, [
            (None, [("Principle", "\"We are fair\"", "data"), ("Policy", "Hiring AI passes bias review"),
                    ("Owner + control", "HR lead signs off", "focus"), ("Audit trail", "Review logged", "good")], True),
        ], gap=24)
        y = stack(D, y + 6, [("Core policies before rollout", "Acceptable use · data handling · output review · incident response · audit")])
        return finish(D, y - 10, [("data", "intent"), ("focus", "accountability"), ("good", "evidence")])

    def d3_8(f):
        D, y = new(f, "Four Impacts, One Scope",
                   "Assess them together: each one changes the scope, and scope changes cost.",
                   "Four impacts assessed together before rollout: data classification and permissions, security and "
                   "audit, privacy and residency by region, and cost from licences and consumption, all feeding one "
                   "final scope.")
        y = converge(D, y, [("Data", "Classified? Permissions right?", "data"), ("Security", "Who can use it? Logged?", "data"),
                            ("Privacy", "Which laws, which regions?", "data"), ("Cost", "Licences + consumption", "warn")],
                     ("Final rollout scope", "Users, regions and data in scope; then the licence count", "focus"))
        return finish(D, y, [("data", "assessment"), ("warn", "follows scope"), ("focus", "decision")])

    def d3_9(f):
        D, y = new(f, "Three Copilot Licence Models",
                   "Segment users by need, then match each segment to a model.",
                   "Three Copilot licence models: Copilot Chat included with Microsoft 365 for everyone, the monthly "
                   "per-user Microsoft 365 Copilot licence for daily in-app users, and pay-as-you-go for occasional "
                   "agent use billed through Azure.")
        y = pairs(D, y, [
            (("Everyone", "Secure general assistant", "data"), ("Included: Copilot Chat", "No extra cost; web-grounded", "good"), None),
            (("Daily users of own data in apps", "Word, Excel, Teams", "data"), ("Monthly per-user licence", "Microsoft 365 Copilot", "focus"), None),
            (("Occasional agent users", "Unpredictable demand", "data"), ("Pay-as-you-go", "Metered via Azure; agents only", "warn"), None),
        ], heads=("User segment", "Licence model"))
        return finish(D, y, [("data", "segment"), ("good", "included"), ("focus", "licensed"), ("warn", "metered")])

    def d3_10(f):
        D, y = new(f, "Foundry Pricing: Learn, Then Commit",
                   "Pay as you go while usage is unknown; commit once it's steady.",
                   "Foundry Tools pricing progression: start on pay-as-you-go during pilots and variable use, then move a "
                   "feature with steady volume to a commitment tier; token-based model workloads use provisioned "
                   "throughput instead.")
        y = lanes(D, y, [
            ("Foundry Tools (Speech, Translator, Language, Vision OCR…)",
             [("Pay-as-you-go", "Pilots, variable use", "data"), ("Months of steady volume", None),
              ("Commitment tier", "Fixed monthly fee, lower unit price", "focus")], True),
            ("Token-based Foundry Models",
             [("Pay-as-you-go", "Per token", "data"), ("Stable, high token volume", None),
              ("Provisioned throughput", "Reserved capacity", "good")], True),
        ])
        return finish(D, y, [("data", "start here"), ("focus", "commitment tier"), ("good", "PTU")])

    fns = {
        "ab731-1-2-solution-choice": d1_2, "ab731-1-3-model-ladder": d1_3, "ab731-1-4-token-meter": d1_4,
        "ab731-1-5-challenges": d1_5, "ab731-1-7-prompt-impact": d1_7, "ab731-1-8-prompt-techniques": d1_8,
        "ab731-1-9-grounding-requirements": d1_9, "ab731-1-11-data-factors": d1_11, "ab731-1-12-secure-ai": d1_12,
        "ab731-1-13-ml-fit": d1_13, "ab731-1-14-ml-lifecycle": d1_14, "ab731-1-15-security-controls": d1_15,
        "ab731-2-2-copilot-versions": d2_2, "ab731-2-4-copilot-apps": d2_4, "ab731-2-7-integrated-benefits": d2_7,
        "ab731-2-9-researcher-analyst": d2_9, "ab731-2-10-buy-extend-build": d2_10, "ab731-2-11-foundry-tools-map": d2_11,
        "ab731-2-12-foundry-tools": d2_12, "ab731-2-14-foundry-benefits": d2_14,
        "ab731-3-2-principles-to-policy": d3_2, "ab731-3-8-four-impacts": d3_8, "ab731-3-9-copilot-licences": d3_9,
        "ab731-3-10-foundry-pricing": d3_10,
    }
    return {name: ("ab731", fn) for name, fn in fns.items()}
