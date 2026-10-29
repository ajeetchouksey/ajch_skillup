"""AI-901 (Microsoft Azure AI Fundamentals) diagrams."""


import functools

# Focal accent for every AI-901 diagram (see ACCENTS in build-svg-diagrams.py).
# SkillUp's "Indigo Scholar" co-brand keeps the AaryaAI indigo default.
ACCENT = "indigo"


def register(api):
    Diagram = functools.partial(api["Diagram"], accent=ACCENT)

    def workload_chooser(f):
        D = Diagram(f, 612, "AI Workload Chooser",
                    "Name the workload from what the output must be, not from the file type.",
                    "Your content, such as text, documents, images, audio, video or a user request, branches into six "
                    "AI workloads by the output required. Create new content: generative AI, using a chat or "
                    "image-generation model. Take actions with tools: agentic AI, using Foundry Agent Service. "
                    "Insights about text: text analysis, using Azure Language or a chat model. Convert between speech "
                    "and text: speech, using Azure Speech. Interpret images or video: computer vision, using a "
                    "multimodal model. Named fields as structured output: information extraction, using Azure "
                    "Content Understanding.")
        ys = [126, 206, 286, 366, 446, 526]
        mid = (ys[0] + ys[-1]) / 2
        inp = D.box(112, mid, 176, "Your content",
                    "Text, documents, images, audio, video or a user request", kind="data", h=120)
        spec = [("Create new content", "Generative AI", "Chat or image-generation model"),
                ("Take actions with tools", "Agentic AI", "Foundry Agent Service"),
                ("Insights about text", "Text analysis", "Azure Language or a chat model"),
                ("Convert speech and text", "Speech", "Azure Speech in Foundry Tools"),
                ("Interpret images or video", "Computer vision", "Vision-capable multimodal model"),
                ("Named fields as structured output", "Information extraction",
                 "Azure Content Understanding")]
        tx = 256
        for y, (t, s, b) in zip(ys, spec):
            bx = D.box(478, y, 360, t, b, sub=s, h=70)
            D.edge([(inp["r"], mid), (tx, mid), (tx, y), (bx["l"], y)])
        D.legend(594, [("data", "input"), ("neutral", "output required, workload and Foundry option")])
        return D

    def foundry_flow(f):
        D = Diagram(f, 706, "From Foundry Resource to Client App",
                    "One resource holds many projects; inside a project you deploy, test, optionally build an agent, then call it.",
                    "A Foundry resource provides models, quotas, security and governance shared by the team. It contains "
                    "Foundry projects, each a workspace for one solution with its agents, evaluations, files and "
                    "connections. In a project: step 1, deploy a model from the model catalog, choosing a deployment "
                    "name, deployment type and tokens-per-minute limit. Step 2, test it in the playground with a system "
                    "prompt and parameters, and compare models. Step 3, optionally save it as an agent: model plus "
                    "instructions plus tools such as file search, code interpreter and web search. Step 4, a client app "
                    "calls it through the project endpoint with AIProjectClient, get_openai_client and responses.create, "
                    "passing either the deployment name or an agent reference. The client can also call the tested "
                    "model deployment directly without an agent.")
        res = D.box(340, 124, 632, "Foundry resource",
                    "Models, quotas, security and governance shared by the team", h=60)
        prj = D.box(340, 214, 632, "Foundry project",
                    "Workspace for one solution: agents, evaluations, files, connections", kind="focus", h=60)
        D.edge([(340, res["b"]), (340, prj["t"])], label="contains one or more", at=(352, 174), anchor="start")
        cx, rx = 178, 500
        s1 = D.box(cx, 312, 290, "Deploy a model", "Deployment name, type, TPM limit", sub="from the model catalog", h=74)
        s2 = D.box(cx, 418, 290, "Test in the playground", "System prompt, parameters, compare models", h=66)
        s3 = D.box(cx, 520, 290, "Save as an agent", "Model + instructions + tools", sub="optional", h=74)
        s4 = D.box(cx, 628, 290, "Client app", "Calls the agent, or the model deployment directly", h=66)
        for n, b in enumerate([s1, s2, s3, s4], 1):
            D.badge(b["l"] + 4, b["t"] + 4, n)
        D.edge([(cx, prj["b"]), (cx, s1["t"])])
        D.edge([(cx, s1["b"]), (cx, s2["t"])])
        D.edge([(cx, s2["b"]), (cx, s3["t"])])
        D.edge([(cx, s3["b"]), (cx, s4["t"])])
        t3 = D.box(rx, 520, 300, "Agent tools", "File search (your documents), code interpreter (calculations), web search (public, current)", h=86)
        D.edge([(s3["r"], 520), (t3["l"], 520)])
        t4 = D.box(rx, 628, 300, "Foundry SDK", "AIProjectClient → get_openai_client() → responses.create(deployment name or agent reference)", kind="data", h=86)
        D.edge([(t4["l"], 628), (s4["r"], 628)])
        D.legend(690, [("focus", "workspace"), ("data", "SDK call"), ("neutral", "step or component")])
        return D

    # ------------------------------------------------ one outcome diagram per task
    SLATE4, SLATE7, TEXT, LINE = api["SLATE4"], api["SLATE7"], api["TEXT"], api["LINE"]

    def row(D, y, items, w, gap=16, h=None):
        x0 = (680 - (len(items) * w + (len(items) - 1) * gap)) / 2
        out = []
        for i, it in enumerate(items):
            t, b, k, s = (list(it) + [None, None, None])[:4]
            out.append(D.box(x0 + w / 2 + i * (w + gap), y, w, t, b, kind=k or "neutral", sub=s, h=h))
        return out

    def link_row(D, bs, hot=False):
        for a, b in zip(bs, bs[1:]):
            D.edge([(a["r"], a["cy"]), (b["l"], b["cy"])], hot=hot)

    def down(D, a, b, x=None, **kw):
        x = a["cx"] if x is None else x
        D.edge([(x, a["b"]), (x, b["t"])], **kw)

    def caption(D, x, y, s):
        D.text(x, y, s.upper(), "title", 12.5, SLATE4, track=0.1)

    def para(D, x, y, s, maxw, size=13):
        for ln in D.f.wrap("body", s, size, maxw):
            D.text(x, y, ln, "body", size, SLATE4); y += size + 4

    def rect(D, x, y, w, h, kind):
        fill, stroke, *_ = D.kinds[kind]
        D.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')

    # 1.1 ------------------------------------------------------------------
    def fairness(f):
        D = Diagram(f, 476, "Fairness: Test Outcomes, Not Columns",
                    "Deleting a sensitive column leaves proxies behind; measuring outcomes per group finds the bias.",
                    "Left: a model trained on past decisions learns their bias. Deleting the sensitive column, such as "
                    "gender, does not help, because proxies such as postcode, career gaps and clubs still carry the bias. "
                    "Right: so fairness is measured instead. Compare approval and error rates per group on a held-out "
                    "test set. If there is a gap between groups, rebalance or augment the training data and re-measure. "
                    "If there is no gap, launch and keep monitoring in production.")
        lx, w = 160, 250
        a = D.box(lx, 134, w, "Past decisions", "The training data the model learns from", kind="data", h=64)
        b = D.box(lx, 236, w, "Delete the sensitive column", "For example, gender", kind="warn", h=64)
        c = D.box(lx, 338, w, "Proxies still carry the bias", "Postcode, career gaps, clubs", kind="risk", h=64)
        down(D, a, b); down(D, b, c)
        m = D.box(500, 134, 280, "Compare outcomes per group",
                  "Approval and error rates on a held-out test set", kind="focus", h=72)
        D.edge([(c["r"], 338), (330, 338), (330, 134), (m["l"], 134)], hot=True)
        D.text(338, 302, "measure instead", "label", 13, SLATE4)
        d = D.diamond(500, 252, 200, 88, "Gap between groups?")
        down(D, m, d)
        y = D.box(420, 382, 170, "Rebalance or augment data", "Then re-measure", kind="good", h=68)
        n = D.box(598, 382, 140, "Launch", "Keep monitoring", kind="good", h=68)
        D.edge([(500, d["b"]), (500, 320), (420, 320), (420, y["t"])], label="yes", at=(452, 324))
        D.edge([(500, d["b"]), (500, 320), (598, 320), (598, n["t"])], dashed=True, label="no", at=(560, 324))
        D.legend(458, [("data", "input"), ("warn", "false fix"), ("risk", "risk"), ("focus", "the test"), ("good", "outcome")])
        return D

    # 1.2 ------------------------------------------------------------------
    def reliability(f):
        D = Diagram(f, 620, "Reliability and Safety: Plan for Being Wrong",
                    "Test before launch, filter at runtime, and send low-confidence answers to a person.",
                    "Before launch, evaluate the app with expected, edge-case and adversarial prompts against a "
                    "definition of what wrong or unsafe means. In production, a user prompt passes through guardrails, "
                    "content filters that check prompts and outputs for harmful content. The model reply is "
                    "probabilistic and can be confidently wrong. If confidence is above the threshold, answer the user; "
                    "if not, or the case is risky, route it to a person. Keep monitoring in production and re-evaluate "
                    "after changes.")
        ev = D.box(340, 128, 632, "Before launch: evaluate",
                   "Expected, edge-case and adversarial prompts, against a clear definition of \"wrong\"", kind="focus", h=60)
        lx, w = 150, 230
        p = D.box(lx, 226, w, "User prompt", kind="data", h=52)
        g = D.box(lx, 322, w, "Guardrails", "Content filters check prompts and outputs for harmful content", h=80)
        r = D.box(lx, 430, w, "Model reply", "Probabilistic: can be confidently wrong", kind="warn", h=64)
        down(D, ev, p, x=lx, label="go live", at=(lx + 12, 184), anchor="start"); down(D, p, g); down(D, g, r)
        d = D.diamond(420, 430, 180, 100, "Confidence above threshold?")
        D.edge([(r["r"], 430), (d["l"], 430)])
        per = D.box(598, 430, 130, "Route to a person", "Risky or low confidence", kind="warn", h=72)
        D.edge([(d["r"], 430), (per["l"], 430)], dashed=True, label="no", at=(521, 420))
        ans = D.box(420, 556, 180, "Answer the user", kind="good", h=52)
        D.edge([(420, d["b"]), (420, ans["t"])], label="yes", at=(432, 504), anchor="start")
        mon = D.box(lx, 556, w, "Monitor in production", "Re-evaluate after changes", h=64)
        D.edge([(ans["l"], 556), (mon["r"], 556)], label="then", at=(298, 547))
        D.legend(608, [("focus", "evaluation"), ("data", "input"), ("warn", "watch"), ("good", "outcome"), ("dashed", "fallback")])
        return D

    # 1.3 ------------------------------------------------------------------
    def privacy(f):
        D = Diagram(f, 432, "Privacy and Security: Protect Data at Every Step",
                    "Redact before the model, a log or a person sees it; restrict, minimise and delete around it.",
                    "Personal data in inputs, files and transcripts is redacted with PII detection, which masks card "
                    "numbers and addresses before data reaches the model, logs or people, so they see only what they "
                    "need. Outputs are filtered for personal data, because a model can leak data in its output. Around "
                    "every step: restrict access with Microsoft Entra ID and least-privilege roles; collect only what "
                    "you need and set retention rules up front; and prompts and completions sent to Foundry Models sold "
                    "by Azure are not used to train the base models.")
        bs = row(D, 170, [("Personal data", "Inputs, files, call transcripts", "data"),
                          ("Redact PII", "PII detection masks card numbers and addresses", "focus"),
                          ("Model, logs, people", "See only what they need", "neutral"),
                          ("Output", "Filtered for personal data before it is shown", "good")], 146, h=96)
        link_row(D, bs)
        for b, t in zip(bs, ["what goes in", "", "what it stores", "what it can reveal"]):
            if t: D.text(b["cx"], 112, t.upper(), "title", 12.5, SLATE4, "middle", track=0.1)
        caption(D, 24, 262, "Around every step")
        row(D, 326, [("Restrict access", "Microsoft Entra ID and least-privilege roles"),
                     ("Minimise and delete", "Collect only what you need; set retention rules up front"),
                     ("Not used for training", "Prompts and completions sent to Foundry Models sold by Azure don't train the base models", "good")],
                200, h=104)
        D.legend(416, [("data", "personal data"), ("focus", "redaction"), ("good", "protected")])
        return D

    # 1.4 ------------------------------------------------------------------
    def inclusiveness(f):
        D = Diagram(f, 494, "Inclusiveness: Everyone Can Use It",
                    "Exclusion starts in the design; several ways in and out, tested with real users, fixes it.",
                    "A comparison table. Rows are people who might struggle; columns compare a voice-only kiosk with an "
                    "inclusive design. Someone who can't hear or speak clearly is shut out of a voice-only kiosk, but can "
                    "type or tap and read on-screen answers in an inclusive design. A speaker with an accent or a "
                    "non-native speaker is misheard by a model tested only on native speakers, but an inclusive design "
                    "supports several languages and is tested with diverse speakers. In a noisy place speech "
                    "recognition fails, but touch or text input beside voice still works.")
        xs, w = [118, 340, 562], 204
        D.box(xs[0], 124, w, "Who might struggle", kind="start", h=48)
        D.box(xs[1], 124, w, "Voice-only kiosk", kind="risk", h=48)
        D.box(xs[2], 124, w, "Inclusive design", kind="focus", h=48)
        rows = [("Can't hear or speak clearly", "Shut out: no other way in or out", "Types or taps; reads on-screen answers"),
                ("Accent or non-native speaker", "Misheard: model tested only on native speakers", "Several languages; tested with diverse speakers"),
                ("Noisy place", "Speech recognition fails", "Touch or text input beside voice")]
        for i, (a, b, c) in enumerate(rows):
            y = 214 + i * 96
            D.box(xs[0], y, w, a, h=80)
            D.box(xs[1], y, w, "Excluded", b, kind="risk", h=80)
            D.box(xs[2], y, w, "Included", c, kind="good", h=80)
        D.legend(480, [("risk", "excluded"), ("good", "included"), ("focus", "the fix")])
        return D

    # 1.5 ------------------------------------------------------------------
    def transparency(f):
        D = Diagram(f, 500, "Transparency: The Label on the Medicine",
                    "Things people can see or read let them judge when to trust an answer and when to check it.",
                    "An AI system, such as a chatbot or a screening tool, shows four things people can see or read: an "
                    "AI disclosure such as \"You're chatting with AI\"; stated limitations, what it can get wrong; "
                    "sources for answers, such as citations and links to the policy behind each answer; and documented "
                    "intended uses and limits, such as Microsoft's transparency notes. Together they produce an informed "
                    "user who knows it's AI, its limits and where answers came from. Without them, users trust answers "
                    "they should have checked.")
        sys_ = D.box(105, 275, 160, "AI system", "Chatbot or screening tool", h=72)
        labels = [("AI disclosure", "\"You're chatting with AI\""), ("Stated limitations", "What it can get wrong"),
                  ("Sources for answers", "Citations, links to the policy behind each answer"),
                  ("Documented uses", "Intended uses, limits, transparency notes")]
        user = D.box(578, 275, 170, "Informed user", "Knows it's AI, its limits and where answers came from",
                     kind="focus", h=110)
        for i, (t, b) in enumerate(labels):
            y = 140 + i * 90
            bx = D.box(345, y, 220, t, b, h=72)
            D.edge([(sys_["r"], 275), (210, 275), (210, y), (bx["l"], y)])
            D.edge([(bx["r"], y), (474, y), (474, 275), (user["l"], 275)])
        risk = D.box(105, 430, 170, "Over-trust", "Users trust answers they should have checked", kind="risk", h=72)
        D.edge([(105, sys_["b"]), (105, risk["t"])], dashed=True, label="no labels", at=(115, 366), anchor="start")
        D.legend(488, [("neutral", "what people see or read"), ("focus", "outcome"), ("risk", "without it")])
        return D

    # 1.6 ------------------------------------------------------------------
    def accountability(f):
        D = Diagram(f, 540, "Accountability: People Answer for AI",
                    "Responsibility never moves to the model or its provider; the deploying organisation owns it.",
                    "When an incident happens, the question is who answers for it. Saying the model did it means nobody "
                    "owns the fix, and blaming the model provider fails too: its filters help safety, but accountability "
                    "can't be outsourced. The deploying organisation answers for it and governs and monitors its own use "
                    "case through four measures: a named owner with an escalation path, a review board that approves "
                    "changes, human sign-off for consequential decisions with audit logs, and an agreed way to pause, "
                    "roll back or retire the system.")
        inc = D.box(340, 124, 220, "An incident happens", kind="start", h=48)
        d = D.diamond(340, 226, 200, 96, "Who answers for it?")
        down(D, inc, d)
        bad = D.box(105, 226, 170, "\"The model did it\"", "Nobody owns the fix", kind="risk", h=72)
        D.edge([(d["l"], 226), (bad["r"], 226)], dashed=True, label="wrong", at=(215, 216))
        org = D.box(575, 226, 180, "Deploying organisation", "Governs and monitors its own use case", kind="focus", h=86)
        D.edge([(d["r"], 226), (org["l"], 226)], hot=True, label="right", at=(462, 216))
        prov = D.box(105, 340, 170, "Model provider", "Filters help safety; accountability can't be outsourced", h=80)
        D.edge([(105, prov["t"]), (105, bad["b"])], dashed=True)
        ms = row(D, 464, [("Named owner", "Plus an escalation path"), ("Review board", "Approves changes"),
                          ("Human sign-off", "For consequential decisions, with audit logs"),
                          ("Off switch", "Pause, roll back or retire")], 148, gap=12, h=84)
        for m in ms:
            D.edge([(575, org["b"]), (575, 402), (m["cx"], 402), (m["cx"], m["t"])])
        D.legend(528, [("focus", "who is accountable"), ("risk", "dead end"), ("neutral", "measure")])
        return D

    # 1.7 ------------------------------------------------------------------
    def next_token(f):
        D = Diagram(f, 400, "How a Language Model Writes",
                    "Predict the next token, append it, repeat until it predicts the end.",
                    "Prompt text is split into tokens, small units of text that usage and cost are counted in. Tokens "
                    "become embeddings, vectors where similar meanings point in similar directions. A transformer with "
                    "attention weighs how strongly each token relates to the others in its context, while positional "
                    "encoding gives word order. It predicts the next most likely token, which is appended to the input "
                    "and the loop repeats until the model predicts the end, giving the completion.")
        bs = row(D, 196, [("Prompt text", None, "data"), ("Tokens", "Units of text; cost is counted in them"),
                          ("Embeddings", "Similar meaning, similar direction"),
                          ("Transformer with attention", "Attention = context; positional encoding = order", "focus"),
                          ("Next-token prediction", "Most likely next token")], 118, gap=10, h=110)
        link_row(D, bs)
        p, t = bs[4], bs[3]
        D.edge([(p["cx"], p["t"]), (p["cx"], 118), (t["cx"], 118), (t["cx"], t["t"])], hot=True,
               label="append and repeat", at=((p["cx"] + t["cx"]) / 2, 114))
        c = D.box(p["cx"] - 40, 326, 200, "Completion", "When it predicts the end", kind="good", h=60)
        D.edge([(p["cx"], p["b"]), (p["cx"], c["t"])], label="end", at=(p["cx"] + 10, 280), anchor="start")
        D.legend(386, [("data", "input"), ("focus", "the model"), ("good", "output")])
        return D

    # 1.8 ------------------------------------------------------------------
    def model_choice(f):
        D = Diagram(f, 572, "Choosing a Model by Capability",
                    "Match input and output first; then compare candidates and test them with your own prompts.",
                    "Step 1, match the input and output you need: write, summarise or chat uses a chat model, an LLM or "
                    "SLM; image or audio input with text uses a multimodal model; semantic search and similarity use an "
                    "embeddings model; creating a new image uses a GPT-image model; fixed-format results such as "
                    "language or PII detection use Azure Language in Foundry Tools; a phone or edge device suits an SLM "
                    "such as the Phi family. Step 2: filter the Foundry catalog of models sold by Azure and partner and "
                    "community models, compare candidates on the leaderboards for quality, safety, cost and throughput, "
                    "then try the shortlist with your own prompts using the playground compare feature. Picking the "
                    "model with the most parameters or the cheapest per token is not a selection rule.")
        D.badge(33, 104, 1); D.text(50, 109, "MATCH INPUT AND OUTPUT", "title", 13, SLATE4, track=0.1)
        tiles = [("Write, summarise or chat", "Chat model: LLM or SLM"),
                 ("Image or audio input with text", "Multimodal model"),
                 ("Semantic search, similarity", "Embeddings model"),
                 ("Create a new image", "GPT-image model"),
                 ("Fixed-format results (language, PII)", "Azure Language in Foundry Tools"),
                 ("Phone or edge device", "SLM, such as the Phi family")]
        for i, (t, s) in enumerate(tiles):
            D.box(177 + (i % 2) * 326, 148 + (i // 2) * 66, 310, t, sub=s, h=58)
        D.edge([(340, 300), (340, 362)])
        D.badge(33, 336, 2); D.text(50, 341, "COMPARE, THEN TEST", "title", 13, SLATE4, track=0.1)
        bs = row(D, 402, [("Filter the catalog", "Sold by Azure, or partner and community"),
                          ("Leaderboards", "Quality, safety, cost, throughput"),
                          ("Your own prompts", "Playground compare feature", "focus")], 196, gap=22, h=80)
        link_row(D, bs)
        D.box(340, 500, 632, "Not a rule: most parameters, or cheapest per token",
              "Match capability first, then test with your own data", kind="risk", h=60)
        D.legend(560, [("neutral", "need and model"), ("focus", "decide here"), ("risk", "trap")])
        return D

    # 1.9 ------------------------------------------------------------------
    def deployment_choice(f):
        D = Diagram(f, 600, "Choosing a Deployment Type",
                    "Two questions: where may data be processed, and how will you pay? The answers name the type.",
                    "Question one, where is data processed: Global, any region; Data Zone, stays in the EU or the US; "
                    "Standard or Regional, one geography. Question two, how do you pay: Standard, pay per token; "
                    "Provisioned, reserved throughput with lower latency variance; Batch, asynchronous, 50% off with a "
                    "24-hour target. The two answers combine into the deployment type: for example an EU retailer's live "
                    "chat is Data Zone plus Standard, so Data Zone Standard, and its nightly job is Data Zone Batch. "
                    "Watch the names: Global Standard is the default, Standard alone is not Global Standard, and "
                    "Developer is only for testing fine-tuned models.")
        for hx, q, opts in [(180, "1. Where is data processed?",
                             [("Global", "Any region"), ("Data Zone", "Stays in the EU or the US"),
                              ("Standard / Regional", "One geography")]),
                            (500, "2. How do you pay?",
                             [("Standard", "Pay per token"), ("Provisioned", "Reserved throughput, lower latency variance"),
                              ("Batch", "Asynchronous, 50% off, 24-hour target")])]:
            hd = D.box(hx, 124, 300, q, kind="start", h=48)
            tx = hx - 130
            for i, (t, b) in enumerate(opts):
                y = 204 + i * 72
                bx = D.box(hx + 20, y, 260, t, b, h=60)
                D.edge([(tx, hd["b"]), (tx, y), (bx["l"], y)])
        D.edge([(200, 348), (200, 400)]); D.edge([(520, 348), (520, 400)])
        D.box(340, 438, 632, "Deployment type = where + how you pay",
              "Data Zone + Standard = Data Zone Standard (EU live chat). Data Zone + Batch = Data Zone Batch (nightly job).",
              kind="focus", h=76)
        D.box(340, 526, 632, "Watch the names",
              "Global Standard is the default. \"Standard\" alone is not Global Standard. Developer is only for testing fine-tuned models.",
              kind="warn", h=64)
        D.legend(588, [("start", "question"), ("neutral", "answer"), ("focus", "result"), ("warn", "trap")])
        return D

    def parameters(f):
        D = Diagram(f, 630, "Parameters: How the Model Generates",
                    "Each parameter turns one dial on the reply; reasoning models don't accept most of them.",
                    "Four parameters shape how the model generates its reply. Temperature or top_p: lower temperature is "
                    "more focused and deterministic; change one, not both. Max tokens: too low cuts replies off. "
                    "frequency_penalty cuts repetition. presence_penalty pushes new topics. Reasoning models in the "
                    "GPT-5 series don't accept temperature, top_p or the penalties. HTTP 429 is a rate limit, not a "
                    "parameter problem: raise TPM within quota, or cut max tokens and concurrency.")
        m = D.box(340, 280, 170, "Model generates the reply", kind="focus", h=70)
        spec = [(130, 160, "Temperature or top_p", "Lower temperature = focused, deterministic. Change one, not both.", "neutral"),
                (550, 160, "Max tokens", "Too low cuts replies off", "warn"),
                (130, 400, "frequency_penalty", "Cuts repetition", "neutral"),
                (550, 400, "presence_penalty", "Pushes new topics", "neutral")]
        for x, y, t, b, k in spec:
            bx = D.box(x, y, 230, t, b, kind=k, h=88)
            side = m["l"] if x < 340 else m["r"]
            yy = bx["b"] if y < 280 else bx["t"]
            D.edge([(x, yy), (x, 280), (side, 280)])
        D.box(340, 494, 632, "Reasoning models (GPT-5 series)", "Don't accept temperature, top_p or the penalties", kind="risk", h=60)
        D.box(340, 566, 632, "HTTP 429 = rate limit, not a parameter", "Raise TPM within quota, or cut max tokens and concurrency", kind="warn", h=60)
        D.legend(618, [("focus", "the model"), ("warn", "watch"), ("risk", "doesn't apply")])
        return D

    # 1.11 -----------------------------------------------------------------
    def text_analysis(f):
        D = Diagram(f, 476, "Four Ways to Read the Same Review",
                    "Entities are typed, key phrases aren't, sentiment has a polarity, summaries are extracted or written.",
                    "One hotel review, \"Staff in Seattle were lovely, but parking was awful and check-in was slow\", "
                    "goes through four text analysis techniques. Entity recognition (NER) returns typed items: Seattle is "
                    "a Location. Key phrase extraction returns untyped topics: slow check-in, parking, staff. Sentiment "
                    "analysis gives positive, neutral or negative with scores, and opinion mining ties it to aspects: "
                    "staff positive, parking negative. Summarization is extractive, picking original sentences, or "
                    "abstractive, writing new ones. Language detection and PII detection sit alongside.")
        inp = D.box(340, 128, 632, "Review",
                    "\"Staff in Seattle were lovely, but parking was awful and check-in was slow.\"", kind="data", h=60)
        bs = row(D, 296, [("Entity recognition (NER)", "Seattle = Location", "focus", "Typed"),
                          ("Key phrase extraction", "\"slow check-in\", \"parking\", \"staff\"", "neutral", "Untyped"),
                          ("Sentiment + opinion mining", "staff: positive; parking: negative", "neutral", "Polarity with scores"),
                          ("Summarization", "Picks original sentences, or writes new ones", "neutral", "Extractive or abstractive")],
                 150, gap=10, h=150)
        for b in bs:
            D.edge([(340, inp["b"]), (340, 192), (b["cx"], 192), (b["cx"], b["t"])])
        para(D, 24, 402, "Language detection and PII detection sit alongside. In Azure Language, key phrases, sentiment "
                         "and summarization are legacy (retiring 2029); NER, PII and language detection stay core.", 632)
        D.legend(462, [("data", "input"), ("focus", "typed output"), ("neutral", "technique")])
        return D

    # 1.12 -----------------------------------------------------------------
    def speech(f):
        D = Diagram(f, 492, "Speech: Ears and a Voice",
                    "Recognition turns audio into text; synthesis turns text into audio, shaped by SSML.",
                    "Top lane, speech recognition or speech to text: audio, live, a single file or an archive, goes to an "
                    "acoustic model that turns audio into phonemes, then a language model that turns phonemes into "
                    "words, giving text; diarization separates speakers and speech translation changes language. "
                    "Bottom lane, speech synthesis or text to speech: text is marked up with SSML, XML that controls "
                    "pauses, rate, pitch and pronunciation, and a neural voice speaks it as audio. If you need specific "
                    "fields such as caller name, number and action from recordings, use a Content Understanding audio "
                    "analyzer instead of just a transcript.")
        caption(D, 24, 108, "Speech recognition (speech to text)")
        a = row(D, 164, [("Audio", "Live, a file, or an archive", "data"), ("Acoustic model", "Audio to phonemes"),
                         ("Language model", "Phonemes to words"), ("Text", "Diarization = who spoke; translation = which language", "good")],
                146, h=86)
        link_row(D, a)
        caption(D, 24, 240, "Speech synthesis (text to speech)")
        b = row(D, 292, [("Text", "What to say", "data"), ("SSML", "XML: pauses, rate, pitch, pronunciation", "focus"),
                         ("Neural voice", "Speaks the marked-up text"), ("Audio", "Spoken output", "good")], 146, h=78)
        link_row(D, b)
        D.box(340, 404, 632, "Need fields, not a transcript?",
              "Caller name, number, requested action: use a Content Understanding audio analyzer (1.14)", kind="warn", h=60)
        D.legend(476, [("data", "input"), ("good", "output"), ("focus", "controls how it sounds"), ("warn", "different job")])
        return D

    # 1.13 -----------------------------------------------------------------
    def vision(f):
        D = Diagram(f, 572, "Vision Reads Images; Generation Makes Them",
                    "Interpret an existing image with vision; create a new one with an image-generation model.",
                    "Left, computer vision interprets an existing image: classification labels the whole image, object "
                    "detection adds bounding boxes to say where, captioning describes the scene, and OCR reads text. "
                    "Right, image generation starts from a text prompt: a GPT-image model creates a new image, and Sora "
                    "creates video. Retired or limited: dall-e-3 was retired in March 2026, Image Analysis 4.0 is "
                    "deprecated, Face emotion and gender recognition are retired, and identity features need approved "
                    "Limited Access.")
        lh = D.box(175, 124, 300, "Existing image", "Vision interprets it: the critic", kind="data", h=60)
        caps = [("Classification", "Labels the whole image", "neutral"), ("Object detection", "Where: bounding boxes", "focus"),
                ("Captioning", "Describes the scene", "neutral"), ("OCR", "Reads text in the image", "neutral")]
        for i, (t, s, k) in enumerate(caps):
            y = 210 + i * 66
            b = D.box(195, y, 260, t, sub=s, kind=k, h=56)
            D.edge([(45, lh["b"]), (45, y), (b["l"], y)])
        rh = D.box(505, 124, 300, "Text prompt", "Describe what you want", kind="data", h=60)
        g = D.box(505, 254, 300, "GPT-image model", "Creates a new image: the painter", h=64)
        o = D.box(505, 372, 300, "New image or video", "Sora creates video", kind="good", h=64)
        down(D, rh, g); down(D, g, o)
        D.box(340, 494, 632, "Retired or limited",
              "dall-e-3 retired (March 2026). Image Analysis 4.0 deprecated. Face emotion and gender recognition retired; identity features need Limited Access.",
              kind="risk", h=72)
        D.legend(558, [("data", "input"), ("focus", "\"where\" = detection"), ("good", "created"), ("risk", "retired")])
        return D

    # 1.14 -----------------------------------------------------------------
    def extraction(f):
        D = Diagram(f, 548, "Information Extraction: Content In, Named Fields Out",
                    "One analyzer handles every content type and applies your schema by meaning, not by label.",
                    "Documents, images, audio and video go into an Azure Content Understanding analyzer, which uses OCR, "
                    "speech recognition and generative models plus your schema, and returns named fields as markdown and "
                    "JSON your systems can use. The schema is applied by meaning: \"Invoice No.\", \"Invoice #\" and an "
                    "unlabelled number on the page all map to the same field, InvoiceNumber.")
        ins = [D.box(95, 140 + i * 64, 140, t, kind="data", h=50) for i, t in enumerate(["Documents", "Images", "Audio", "Video"])]
        an = D.box(345, 236, 200, "Content Understanding analyzer", "OCR, speech recognition and generative models, plus your schema",
                   kind="focus", h=150)
        for b in ins:
            D.edge([(b["r"], b["cy"]), (205, b["cy"]), (205, 236), (an["l"], 236)])
        out = D.box(570, 236, 180, "Named fields", "Markdown and JSON your systems can use", kind="good", h=110)
        D.edge([(an["r"], 236), (out["l"], 236)], hot=True)
        caption(D, 24, 400, "Schema by meaning")
        srcs = [D.box(95 + i * 154, 450, 140, t, h=50) for i, t in enumerate(["\"Invoice No.\"", "\"Invoice #\"", "Unlabelled number"])]
        tgt = D.box(585, 450, 150, "InvoiceNumber", kind="good", h=50)
        for s in srcs:
            D.edge([(s["cx"], s["b"]), (s["cx"], 492), (585, 492), (585, tgt["b"])])
        D.legend(534, [("data", "input"), ("focus", "analyzer + schema"), ("good", "named field")])
        return D

    # 2.1 ------------------------------------------------------------------
    def prompts(f):
        D = Diagram(f, 500, "What Goes Into One Request",
                    "The system prompt sets the rules; grounding stops fabrication; the user prompt is today's task.",
                    "One request is a stack. The system prompt, set by the app, holds role, scope, tone and output "
                    "format. Grounding adds source text with the instruction to answer only from it, otherwise say you "
                    "don't know. A few-shot example guides format for this request only and doesn't retrain the model. "
                    "Earlier turns are resent because each request stands alone. The user prompt is today's task. The "
                    "model then returns a grounded reply that matches your data and admits gaps. Adding \"always be "
                    "accurate\" and raising the temperature never fixes fabrication.")
        stack = [("System prompt", "Role, scope, tone, output format: set by the app", "focus"),
                 ("Grounding", "Source text + \"answer only from it, otherwise say you don't know\"", "data"),
                 ("Few-shot example", "Guides format for this request only; no retraining", "neutral"),
                 ("Earlier turns", "Resent: each request stands alone", "neutral"),
                 ("User prompt", "Today's task", "data")]
        y = 104; bs = []
        for t, b, k in stack:
            h = 66 if len(b) > 50 else 60
            bs.append(D.box(200, y + h / 2, 340, t, b, kind=k, h=h)); y += h + 8
        top, bot = bs[0]["t"], bs[-1]["b"]; mid = (top + bot) / 2
        D.back.append(f'<path d="M378,{top} L392,{top} L392,{bot} L378,{bot}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
        mdl = D.box(530, mid, 160, "Model", h=56)
        D.edge([(392, mid), (mdl["l"], mid)])
        rep = D.box(530, mid + 110, 200, "Grounded reply", "Matches your data; admits gaps", kind="good", h=64)
        down(D, mdl, rep)
        D.box(530, 150, 230, "\"Always be accurate\" + higher temperature", "Never fixes fabrication", kind="risk", h=80)
        D.legend(488, [("focus", "the rules"), ("data", "your content"), ("good", "outcome"), ("risk", "false fix")])
        return D

    # 2.2 ------------------------------------------------------------------
    def deploy(f):
        D = Diagram(f, 592, "Deploy, Test, Then Call",
                    "A deployment is the phone line apps dial by name; the playground is the test call.",
                    "In your project, pick a model in the model catalog and deploy it, setting the deployment name, type, "
                    "version and tokens-per-minute (TPM) limit; deploying doesn't train the model. Test it in the "
                    "playground with instructions and parameters, compare models side by side and use View code. The app "
                    "then calls the deployment by name. From the playground you can optionally save it as an agent. "
                    "When the app gets HTTP 429, a capacity problem: if quota is left, raise TPM within quota; if not, "
                    "cut max tokens or concurrency. Changing temperature, or switching to a Developer deployment, which "
                    "is only for evaluating fine-tuned models, does not fix 429.")
        bs = row(D, 156, [("Model catalog", "Pick a model in your project", "data"),
                          ("Deploy", "Name, type, version, TPM limit; no training", "focus"),
                          ("Playground", "Instructions, parameters, compare, View code"),
                          ("App", "Calls the deployment by name", "good")], 146, h=96)
        link_row(D, bs)
        ag = D.box(bs[2]["cx"], 270, 146, "Save as agent", "Optional (2.4)", h=56)
        D.edge([(bs[2]["cx"], bs[2]["b"]), (bs[2]["cx"], ag["t"])], dashed=True)
        caption(D, 24, 330, "When the app gets HTTP 429")
        e = D.box(100, 410, 150, "HTTP 429", "Rate limit: a capacity problem", kind="warn", h=72)
        d = D.diamond(290, 410, 170, 90, "Quota left?")
        D.edge([(e["r"], 410), (d["l"], 410)])
        up = D.box(555, 368, 230, "Raise TPM within quota", kind="good", h=52)
        dn = D.box(555, 452, 230, "Cut max tokens or concurrency", h=52)
        D.edge([(d["r"], 410), (400, 410), (400, 368), (up["l"], 368)], label="yes", at=(420, 372))
        D.edge([(d["r"], 410), (400, 410), (400, 452), (dn["l"], 452)], dashed=True, label="no", at=(420, 456))
        D.box(340, 528, 632, "Not fixes for 429",
              "Changing temperature, or switching to a Developer deployment (only for evaluating fine-tuned models)", kind="risk", h=56)
        D.legend(580, [("focus", "creates the endpoint"), ("warn", "capacity"), ("good", "fix"), ("risk", "trap")])
        return D

    # 2.3 ------------------------------------------------------------------
    def chat_client(f):
        D = Diagram(f, 586, "A Chat Client in a Few Lines",
                    "Authenticate, connect to the project, call the deployment by name, read output_text.",
                    "Your code gets a DefaultAzureCredential from azure-identity, which uses Microsoft Entra ID through az "
                    "login or the VM's managed identity, with no API key. AIProjectClient from azure-ai-projects connects "
                    "to the Foundry project through the project endpoint. get_openai_client returns a client that calls "
                    "the model. responses.create sends the input with model set to the deployment name, for example "
                    "support-chat, not the model family. The deployment's reply is read from output_text. Each request "
                    "stands alone, so resend history or use a conversation.")
        x, w = 240, 420
        a = D.box(x, 134, w, "DefaultAzureCredential", "Entra ID: az login, or the VM's managed identity; no API key",
                  kind="data", sub="azure-identity", h=76)
        b = D.box(x, 240, w, "AIProjectClient(endpoint, credential)",
                  "https://<resource>.services.ai.azure.com /api/projects/<project>", kind="focus", sub="azure-ai-projects", h=76)
        c = D.box(x, 332, w, "get_openai_client()", "A client that calls the model by deployment name", h=56)
        d = D.box(x, 420, w, "responses.create(model=..., input=...)", "model = the deployment name, not the model family", h=64)
        e = D.box(x, 514, w, "r.output_text", "The reply. Each request stands alone: resend history or use a conversation",
                  kind="good", h=64)
        for p, q in [(a, b), (b, c), (c, d), (d, e)]: down(D, p, q)
        pr = D.box(565, 240, 200, "Foundry project", "Reached through the project endpoint", h=76)
        D.edge([(b["r"], 240), (pr["l"], 240)])
        dep = D.box(565, 420, 200, "Model deployment", "Named \"support-chat\"", h=64)
        D.edge([(d["r"], 420), (dep["l"], 420)])
        D.edge([(565, dep["b"]), (565, 514), (e["r"], 514)], label="reply", at=(565, 490))
        D.legend(574, [("data", "credential"), ("focus", "project client"), ("good", "result")])
        return D

    # 2.4 ------------------------------------------------------------------
    def agent(f):
        D = Diagram(f, 722, "Anatomy of a Single Agent",
                    "An agent is a model plus instructions plus tools; pick the tool from what the question needs.",
                    "A model deployment, instructions (the job description) and tools and knowledge (the toolbox and the "
                    "library) combine into an agent. Which tool: answers from your own documents use file search, which "
                    "indexes uploaded files for grounded, cited answers; calculations, data or charts use code "
                    "interpreter, which runs Python in a sandbox; current public information uses web search, with less "
                    "control of sources. If no tools are needed, skip the agent: a plain deployment is simpler. Test in "
                    "the agents playground with expected and tricky questions, then publish, which makes the agent a "
                    "managed Azure resource with a stable endpoint.")
        ing = row(D, 132, [("Model deployment", "Chosen in the agent"), ("Instructions", "The job description"),
                           ("Tools and knowledge", "The toolbox and the library")], 196, gap=22, h=64)
        ag = D.box(340, 252, 280, "Agent", "Model + instructions + tools", kind="focus", h=60)
        for b in ing:
            D.edge([(b["cx"], b["b"]), (b["cx"], 196), (340, 196), (340, ag["t"])])
        caption(D, 24, 312, "Which tool?")
        rows = [("Answer from our own documents?", "File search", "Indexes uploaded files; cited answers"),
                ("Calculations, data or charts?", "Code interpreter", "Runs Python in a sandbox"),
                ("Current public information?", "Web search", "Less control of sources")]
        for i, (q, t, b) in enumerate(rows):
            y = 360 + i * 76
            qb = D.box(170, y, 290, q, kind="start", h=60)
            tb = D.box(520, y, 260, t, b, h=64)
            D.edge([(qb["r"], y), (tb["l"], y)])
        y = 360 + 3 * 76
        qb = D.box(170, y, 290, "No tools needed?", kind="start", h=60)
        tb = D.box(520, y, 260, "Plain deployment", "Skip the agent: simpler", h=64)
        D.edge([(qb["r"], y), (tb["l"], y)], dashed=True)
        D.box(340, 664, 632, "Test in the agents playground, then publish",
              "Publishing makes the agent a managed Azure resource with a stable endpoint", kind="good", h=56)
        D.legend(712, [("focus", "the agent"), ("start", "question"), ("neutral", "tool"), ("good", "ship it")])
        return D

    # 2.5 ------------------------------------------------------------------
    def agent_client(f):
        D = Diagram(f, 566, "Calling an Agent from an App",
                    "Authenticate with Entra ID, name the agent with an agent reference, keep one conversation per user.",
                    "Sequence between three participants: the app back end, the Foundry project reached with "
                    "AIProjectClient, and the agent. The app authenticates with DefaultAzureCredential, Microsoft Entra "
                    "ID, not an API key. It gets the agent with agents.get by name. It calls responses.create on the "
                    "OpenAI client with an agent_reference in extra_body, and the agent returns output_text. A follow-up "
                    "passes the same conversation ID, so the reply keeps context. An option using threads.runs.create "
                    "describes the retired Assistants API, not Foundry Agent Service.")
        xs = [110, 340, 570]
        for x, (t, s, k) in zip(xs, [("App back end", "Your code", "data"), ("Foundry project", "AIProjectClient", "neutral"),
                                     ("Agent", "Model + instructions + tools", "focus")]):
            D.box(x, 124, 190, t, sub=s, kind=k, h=56)
            D.back.append(f'<line x1="{x}" y1="152" x2="{x}" y2="460" stroke="{SLATE7}" stroke-width="1.5" stroke-dasharray="3 4"/>')
        msgs = [(0, 1, 196, "DefaultAzureCredential (Entra ID)", False),
                (0, 1, 244, "agents.get(agent_name=...)", False),
                (0, 2, 292, "responses.create(input, agent_reference)", False),
                (2, 0, 340, "output_text", True),
                (0, 2, 388, "follow-up: same conversation ID", False),
                (2, 0, 436, "reply that keeps context", True)]
        for a, b, y, lab, ret in msgs:
            x1, x2 = xs[a], xs[b]
            x2 += -6 if x2 > x1 else 6
            D.edge([(x1, y), (x2, y)], dashed=ret, label=lab, at=((xs[a] + xs[b]) / 2, y - 8), hot=(y == 292))
        D.box(340, 500, 632, "threads.runs.create", "Retired Assistants API: not Foundry Agent Service", kind="risk", h=56)
        D.legend(554, [("solid", "request"), ("dashed", "response"), ("focus", "agent"), ("risk", "retired")])
        return D

    # 2.6 ------------------------------------------------------------------
    def text_app(f):
        D = Diagram(f, 500, "A Text Analysis App with Azure Language",
                    "Pass a list, read item [0]: the language routes the ticket, the redacted text is stored.",
                    "A TextAnalyticsClient from azure-ai-textanalytics is created with an endpoint and an "
                    "AzureKeyCredential. Ticket text is passed as a one-item list. detect_language with [text], item 0, "
                    "returns primary_language with name, ISO code and score, used to route the ticket. "
                    "recognize_pii_entities with [text], item 0, returns redacted_text plus the entities, so only masked "
                    "text is stored. Choose the Azure Language SDK when code parses the result and needs consistent, "
                    "structured values; choose a Foundry model with a prompt when people read the result and output can "
                    "vary.")
        cl = D.box(370, 128, 400, "TextAnalyticsClient", "azure-ai-textanalytics; endpoint + AzureKeyCredential", kind="focus", h=60)
        inp = D.box(105, 272, 160, "Ticket text", "Passed as a list: [text]", kind="data", h=72)
        m1 = D.box(370, 226, 270, "detect_language([text])[0]", ".primary_language: name, ISO code, score", h=64)
        m2 = D.box(370, 318, 270, "recognize_pii_entities([text])[0]", ".redacted_text, plus the entities", h=64)
        D.edge([(370, cl["b"]), (370, m1["t"])])
        for m in (m1, m2):
            D.edge([(inp["r"], 272), (210, 272), (210, m["cy"]), (m["l"], m["cy"])])
        o1 = D.box(590, 226, 140, "Route the ticket", kind="good", h=56)
        o2 = D.box(590, 318, 140, "Store masked text", kind="good", h=56)
        D.edge([(m1["r"], 226), (o1["l"], 226)]); D.edge([(m2["r"], 318), (o2["l"], 318)])
        caption(D, 24, 386, "Choose")
        row(D, 432, [("Code parses the result", "Azure Language SDK: consistent, structured values"),
                     ("People read the result", "Foundry model + prompt: output varies")], 306, gap=20, h=60)
        D.legend(490, [("focus", "client"), ("data", "input"), ("good", "action")])
        return D

    # 2.7 ------------------------------------------------------------------
    def spoken(f):
        D = Diagram(f, 500, "Three Ways to Answer a Spoken Prompt",
                    "An audio-capable model listens and thinks in one step; the other paths add a session or more parts.",
                    "Lane one, audio-capable model: the spoken question is sent as an input_audio part with base64 data "
                    "and a format such as wav, to a model such as gpt-audio, the gpt-realtime family or "
                    "Phi-4-multimodal-instruct, which answers directly with text and a spoken reply when modalities "
                    "include text and audio with a voice and format. Lane two, the Voice Live API: a managed, low-latency "
                    "speech-to-speech service for live, session-based conversation. Lane three, Azure Speech plus a text "
                    "model: speech to text, a text model, then text to speech; more parts to wire, but custom "
                    "recognition and SSML.")
        caption(D, 24, 106, "Audio-capable model: one step")
        a = row(D, 160, [("Spoken question", "input_audio part: base64, format wav", "data"),
                         ("Audio-capable model", "gpt-audio, gpt-realtime, Phi-4-multimodal-instruct", "focus"),
                         ("Text + spoken reply", "modalities text and audio; voice and format", "good")], 196, gap=22, h=86)
        link_row(D, a, hot=True)
        caption(D, 24, 234, "Voice Live API: live conversation")
        b = row(D, 284, [("Live speech", None, "data"), ("Voice Live API", "Managed, low-latency speech to speech"),
                         ("Natural conversation", "Session-based", "good")], 196, gap=22, h=70)
        link_row(D, b)
        caption(D, 24, 350, "Azure Speech + text model (2.8)")
        c = row(D, 402, [("Audio", None, "data"), ("Speech to text", "Custom recognition"), ("Text model", "Reasons on text"),
                         ("Text to speech", "SSML control", "good")], 146, h=70)
        link_row(D, c)
        D.legend(486, [("data", "spoken input"), ("focus", "one-step model"), ("good", "reply")])
        return D

    # 2.8 ------------------------------------------------------------------
    def speech_app(f):
        D = Diagram(f, 560, "Azure Speech SDK: Pick the Call",
                    "One SpeechConfig; a recognizer to listen, a synthesizer to speak. Match the call to the job.",
                    "A SpeechConfig from azure-cognitiveservices-speech is created with the Foundry resource key and "
                    "endpoint. For recognition, a SpeechRecognizer: a short command uses recognize_once_async, one "
                    "utterance of about 30 seconds; dictation or long speech uses start_continuous_recognition with "
                    "recognized handlers; an archive of recordings uses batch transcription with SAS URIs, asynchronous. "
                    "For synthesis, set speech_synthesis_voice_name, create a SpeechSynthesizer and call "
                    "speak_text_async(text).get(), which speaks in a neural voice.")
        root = D.box(340, 128, 320, "SpeechConfig", "Foundry resource key and endpoint", kind="focus", h=60)
        lis = D.box(175, 228, 290, "SpeechRecognizer", sub="Recognition: audio to text", h=56)
        spk = D.box(505, 228, 290, "SpeechSynthesizer", sub="Synthesis: text to audio", h=56)
        D.edge([(300, root["b"]), (300, 178), (175, 178), (175, lis["t"])])
        D.edge([(380, root["b"]), (380, 178), (505, 178), (505, spk["t"])])
        jobs = [("Short command", "recognize_once_async(): one utterance, about 30 seconds"),
                ("Dictation, long speech", "start_continuous_recognition() with recognized handlers"),
                ("Archive of recordings", "Batch transcription: SAS URIs, asynchronous")]
        for i, (t, b) in enumerate(jobs):
            y = 326 + i * 84
            bx = D.box(195, y, 260, t, b, kind="good" if i < 2 else "warn", h=72)
            D.edge([(45, lis["b"]), (45, y), (bx["l"], y)])
        v = D.box(505, 326, 260, "Set the voice", "speech_synthesis_voice_name", h=60)
        s = D.box(505, 422, 260, "speak_text_async(text).get()", "Speaks in a neural voice", kind="good", h=64)
        down(D, spk, v); down(D, v, s)
        D.legend(546, [("focus", "config"), ("good", "SDK call"), ("warn", "separate batch service")])
        return D

    # 2.9 ------------------------------------------------------------------
    def visual_input(f):
        D = Diagram(f, 500, "An Image and a Question in One Message",
                    "The image is the photo, the text part is the sticky note; a vision-capable model answers.",
                    "One user message holds two content parts: input_text with the question, for example what is in this "
                    "image in three bullet points, and input_image with an image_url that is either a public URL or a "
                    "base64 data URL. A vision-capable model reads both and the answer is read from output_text. Image "
                    "options: use a public URL when the image is internet-reachable; a base64 data URL for private or "
                    "uploaded images; and in Chat Completions, an image_url part with detail high reads fine print but "
                    "uses more tokens.")
        D.back.append(f'<rect x="24" y="104" width="368" height="226" rx="12" fill="none" stroke="{SLATE4}" '
                      f'stroke-width="1.25" stroke-dasharray="6 4"/>')
        caption(D, 40, 126, "One user message")
        D.box(208, 180, 330, "input_text", "The question: \"What is in this image? 3 bullet points.\"", kind="data", h=66)
        D.box(208, 270, 330, "input_image", "image_url: a public URL or a base64 data URL", kind="data", h=66)
        m = D.box(540, 217, 210, "Vision-capable model", kind="focus", h=60)
        D.edge([(392, 217), (m["l"], 217)], hot=True)
        a = D.box(540, 310, 210, "Answer about the image", "r.output_text", kind="good", h=60)
        down(D, m, a)
        caption(D, 24, 372, "Image options")
        row(D, 426, [("Public URL", "Image is internet-reachable"), ("Base64 data URL", "Private or uploaded images"),
                     ("detail: \"high\"", "Chat Completions image_url: fine print, more tokens", "warn")], 200, h=72)
        D.legend(488, [("data", "message parts"), ("focus", "model"), ("good", "answer"), ("warn", "costs more")])
        return D

    # 2.10 -----------------------------------------------------------------
    def visual_output(f):
        D = Diagram(f, 476, "Images Come Back at Once; Video Is a Job",
                    "Decode the image's base64 and save it; for video, create a job, poll it, then download.",
                    "Image lane: a prompt goes to images.generate on a GPT-image deployment, which returns base64 in "
                    "data[0].b64_json, not a URL; decode it and write the bytes to a file. Image edit with a mask "
                    "changes only part of an image. dall-e-3 was retired on 4 March 2026. Video lane with Sora: create a "
                    "job, poll its status until the job finishes, then download the video.")
        caption(D, 24, 106, "Image: returned at once")
        a = row(D, 162, [("Prompt", "\"Flat illustration of a tent at dawn\"", "data"),
                         ("images.generate()", "GPT-image deployment; dall-e-3 retired", "focus"),
                         ("data[0].b64_json", "Base64, not a URL"), ("Decode and save", "Write bytes to tent.png", "good")], 146, h=84)
        link_row(D, a)
        ed = D.box(a[1]["cx"], 266, 146, "Image edit with mask", "Changes only part of an image", h=64)
        D.edge([(a[1]["cx"], a[1]["b"]), (a[1]["cx"], ed["t"])], dashed=True, label="or", at=(a[1]["cx"] + 10, 224), anchor="start")
        caption(D, 24, 326, "Video (Sora): a job you poll")
        b = row(D, 404, [("Prompt", None, "data"), ("Create a job", "Sora video"), ("Poll status", "Until the job finishes", "warn"),
                         ("Download the video", None, "good")], 146, h=64)
        link_row(D, b)
        p = b[2]
        D.edge([(p["cx"] + 30, p["t"]), (p["cx"] + 30, p["t"] - 22), (p["cx"] - 30, p["t"] - 22), (p["cx"] - 30, p["t"])],
               label="not done", at=(p["cx"], p["t"] - 18))
        D.legend(462, [("data", "prompt"), ("warn", "wait"), ("good", "file you keep")])
        return D

    # 2.11 -----------------------------------------------------------------
    def vision_app(f):
        D = Diagram(f, 630, "A Lightweight Vision App",
                    "Photo plus instruction in one request, a fixed reply format, validation in code, a person for surprises.",
                    "A shelf photo taken at closing time is read and base64-encoded as a data URL. One request carries an "
                    "input_text instruction, count empty slots and reply as JSON, and an input_image part. A "
                    "vision-capable deployment, with no custom training, returns JSON such as empty_slots 3. Code "
                    "validates the JSON: valid and expected results generate the restock list; unexpected results go to "
                    "a person. Image Analysis 4.0 is deprecated, retiring 25 September 2028, Custom Vision is retiring "
                    "and Face emotion and gender recognition are retired, so use multimodal models or Content "
                    "Understanding.")
        x, w = 180, 300
        a = D.box(x, 128, w, "shelf.jpg", "Photo taken at closing time", kind="data", h=56)
        b = D.box(x, 208, w, "Read and base64-encode", "data:image/jpeg;base64,...", h=56)
        c = D.box(x, 296, w, "One request", "input_text: \"Count empty slots. Reply as JSON\" + input_image", h=72)
        d = D.box(x, 388, w, "Vision-capable deployment", "No custom training", kind="focus", h=60)
        for p, q in [(a, b), (b, c), (c, d)]: down(D, p, q)
        j = D.box(510, 388, 200, "JSON reply", "{\"empty_slots\": 3}", h=60)
        D.edge([(d["r"], 388), (j["l"], 388)])
        dm = D.diamond(510, 484, 200, 84, "Valid and expected?")
        down(D, j, dm)
        no = D.box(225, 484, 190, "Send to a person", kind="warn", h=52)
        D.edge([(dm["l"], 484), (no["r"], 484)], dashed=True, label="no", at=(365, 474))
        ok = D.box(510, 570, 200, "Restock list", kind="good", h=48)
        D.edge([(510, dm["b"]), (510, ok["t"])], label="yes", at=(522, 536), anchor="start")
        D.box(505, 190, 300, "Retired or retiring",
              "Image Analysis 4.0 (deprecated, retiring 25 Sept 2028), Custom Vision, Face emotion and gender. Use multimodal models or Content Understanding.",
              kind="risk", h=116)
        D.legend(618, [("focus", "model"), ("good", "automated"), ("warn", "human check"), ("risk", "don't build on")])
        return D

    # 2.12 -----------------------------------------------------------------
    def doc_analyzer(f):
        D = Diagram(f, 576, "Document Analyzer: Copy, Choose, Compose",
                    "An analyzer applies a schema to a document; each field is extracted, classified or generated.",
                    "A supplier PDF, a document or form, goes into an analyzer: a prebuilt analyzer such as invoice, "
                    "receipt or layout, or a custom analyzer based on prebuilt-document with your field schema. Each field "
                    "uses one method: extract copies a value on the page and works only for documents; classify picks "
                    "one value from a fixed list; generate writes a value, such as a summary. The result is named fields, "
                    "for example VendorName, DocumentCategory and Summary. Confidence and grounding appear only if "
                    "estimateFieldSourceAndConfidence is enabled, which is off by default; low-confidence fields go to "
                    "human review. Most analyzers need a chat completion model and an embeddings model deployed as "
                    "defaults; read and layout need none.")
        doc = D.box(90, 210, 130, "Supplier PDF", "Document or form", kind="data", h=72)
        an = D.box(290, 210, 220, "Analyzer", "Prebuilt (invoice, receipt, layout), or custom from prebuilt-document with your schema",
                   kind="focus", h=120)
        D.edge([(doc["r"], 210), (an["l"], 210)])
        for t, b, y in [("Extract", "Copy a value on the page (documents only)", 130), ("Classify", "Pick one from a fixed list", 210),
                        ("Generate", "Write a value, such as a summary", 290)]:
            bx = D.box(565, y, 200, t, b, h=64)
            D.edge([(an["r"], 210), (432, 210), (432, y), (bx["l"], y)])
        fl = D.box(200, 412, 300, "Named fields", "VendorName, DocumentCategory, Summary", kind="good", h=64)
        D.edge([(565, 322), (565, 352), (200, 352), (200, fl["t"])])
        rv = D.box(530, 412, 260, "Low confidence: human review",
                   "Needs estimateFieldSourceAndConfidence (off by default)", kind="warn", h=80)
        D.edge([(fl["r"], 412), (rv["l"], 412)])
        D.box(340, 510, 632, "Before you analyze",
              "Most analyzers need a chat completion model and an embeddings model deployed as defaults; read and layout need none.", h=60)
        D.legend(564, [("data", "input"), ("focus", "analyzer + schema"), ("good", "fields"), ("warn", "watch")])
        return D

    # 2.13 -----------------------------------------------------------------
    def image_analyzer(f):
        D = Diagram(f, 566, "Which Analyzer for a Photo?",
                    "Text-heavy photos go to a document analyzer; scenes use image analyzers with classify or generate.",
                    "Decision tree for a photo. If it is text-heavy, like a receipt, use prebuilt-receipt, a document "
                    "analyzer. If not, and you don't need your own fields, use prebuilt-imageSearch for a paragraph "
                    "description. If you need your own fields, build a custom analyzer on prebuilt-image whose fields use "
                    "classify or generate, for example ShelfStatus classified as Full, Low or Empty. Extract is "
                    "documents only and never works for images. For a one-off question, ask a multimodal model (2.9), "
                    "which gives no schema or confidence.")
        ph = D.box(340, 124, 180, "Photo", kind="data", h=48)
        one = D.box(570, 124, 190, "One-off question?", "Multimodal model (2.9): no schema or confidence", h=72)
        D.edge([(ph["r"], 124), (one["l"], 124)], dashed=True)
        d1 = D.diamond(340, 232, 220, 96, "Text-heavy, like a receipt?")
        down(D, ph, d1)
        r1 = D.box(105, 232, 170, "prebuilt-receipt", "Document analyzer", h=64)
        D.edge([(d1["l"], 232), (r1["r"], 232)], label="yes", at=(210, 222))
        d2 = D.diamond(340, 366, 220, 96, "Need your own fields?")
        D.edge([(340, d1["b"]), (340, d2["t"])], dashed=True, label="no", at=(352, 302), anchor="start")
        r2 = D.box(105, 366, 170, "prebuilt-imageSearch", "A paragraph description", h=64)
        D.edge([(d2["l"], 366), (r2["r"], 366)], dashed=True, label="no", at=(210, 356))
        cu = D.box(340, 490, 240, "Custom on prebuilt-image", "classify or generate, e.g. ShelfStatus: Full, Low, Empty",
                   kind="focus", h=72)
        D.edge([(340, d2["b"]), (340, cu["t"])], hot=True, label="yes", at=(352, 436), anchor="start")
        D.box(575, 490, 170, "Not extract", "Extract is documents only", kind="risk", h=72)
        D.legend(552, [("solid", "yes"), ("dashed", "no"), ("focus", "custom image analyzer"), ("risk", "not for images")])
        return D

    # 2.14 -----------------------------------------------------------------
    def audio_video(f):
        D = Diagram(f, 560, "What an Audio or Video Analyzer Returns",
                    "A recording becomes a WebVTT transcript, key frames and segments, each segment with its own output.",
                    "A timeline of one recording with three tracks. Transcript: WebVTT with speakers separated by "
                    "diarization, spoken words only. Key frames: video only. Segments: with segmentation and content "
                    "categories, each section gets its own summary and fields. Set locales for languages. Analyzers: "
                    "prebuilt-audioSearch returns a transcript and summary; prebuilt-callCenter adds sentiment, topics, "
                    "people and companies; your own fields use generate or classify. Music and sound effects are not "
                    "transcribed and don't become chapter markers.")
        x0, x1 = 172, 656
        tw = x1 - x0
        for y, t, s in [(134, "Recording", "set locales"), (184, "Transcript", "WebVTT"), (234, "Key frames", "video only"),
                        (292, "Segments", "own output each")]:
            D.text(24, y - 2, t, "title", 15); D.text(24, y + 14, s, "body", 12, SLATE4)
        rect(D, x0, 116, tw, 34, "data")
        D.text(x0 + 12, 138, "0:00", "label", 12, SLATE4); D.text(x1 - 12, 138, "end", "label", 12, SLATE4, "end")
        rect(D, x0, 166, tw, 34, "neutral")
        D.text(x0 + tw / 2, 188, "Speaker 1 / Speaker 2 (diarization), spoken words only", "label", 13, TEXT, "middle")
        for i in range(10):
            rect(D, x0 + 8 + i * 48, 220, 36, 26, "neutral")
        segw = tw / 3
        for i in range(3):
            rect(D, x0 + i * segw + (3 if i else 0), 266, segw - 3, 52, "focus" if i == 1 else "good")
            D.text(x0 + i * segw + segw / 2, 288, f"Segment {i + 1}", "title", 14, "#ffffff" if i == 1 else TEXT, "middle")
            D.text(x0 + i * segw + segw / 2, 306, "summary + fields", "body", 12, D.kinds["focus"][3] if i == 1 else SLATE4, "middle")
        caption(D, 24, 356, "Analyzers")
        row(D, 410, [("prebuilt-audioSearch", "Transcript and summary"),
                     ("prebuilt-callCenter", "Adds sentiment, topics, people and companies"),
                     ("Your own fields", "generate or classify")], 200, h=72)
        D.box(340, 496, 632, "Ignored", "Music and sound effects aren't transcribed and don't become chapter markers", kind="warn", h=52)
        D.legend(548, [("data", "input"), ("focus", "one segment"), ("good", "segment output"), ("warn", "trap")])
        return D

    # 2.15 -----------------------------------------------------------------
    def cu_app(f):
        D = Diagram(f, 616, "Content Understanding Is Asynchronous",
                    "Hand it in, get a ticket, come back later: start, poll, then route fields by confidence.",
                    "The app sends content with begin_analyze in the SDK or a POST to analyze over REST. The service "
                    "replies 202 Accepted with an Operation-Location header and no fields yet; that is success, so don't "
                    "re-POST. The app polls Operation-Location while it is running until it reports Succeeded; in the "
                    "SDK, poller.result() waits. Then it reads the fields on result.contents, each with a confidence if "
                    "estimateFieldSourceAndConfidence is enabled. Fields with confidence above the threshold go to the "
                    "booking system; the rest go to human review.")
        x, w = 200, 300
        a = D.box(x, 128, w, "Send content", "begin_analyze(), or POST analyze over REST", kind="data", h=60)
        b = D.box(x, 226, w, "202 Accepted", "Operation-Location header; no fields yet", h=60)
        c = D.box(x, 330, w, "Poll Operation-Location", "Until Succeeded. SDK: poller.result() waits", kind="focus", h=68)
        d = D.box(x, 438, w, "Read the fields", "result.contents, with confidence (enable it)", h=60)
        for p, q in [(a, b), (b, c), (c, d)]: down(D, p, q)
        D.edge([(c["r"], 318), (378, 318), (378, 342), (c["r"], 342)])
        D.text(386, 334, "running", "label", 13, SLATE4)
        rp = D.box(540, 226, 240, "Don't re-POST", "A 202 with no fields is success: poll instead", kind="risk", h=64)
        D.edge([(b["r"], 226), (rp["l"], 226)], dashed=True)
        dm = D.diamond(480, 438, 190, 90, "Confidence above threshold?")
        D.edge([(d["r"], 438), (dm["l"], 438)])
        hr = D.box(590, 330, 150, "Human review", kind="warn", h=52)
        D.edge([(dm["r"], 438), (612, 438), (612, hr["b"])], dashed=True, label="no", at=(622, 404), anchor="start")
        ok = D.box(480, 548, 200, "Booking system", kind="good", h=52)
        D.edge([(480, dm["b"]), (480, ok["t"])], label="yes", at=(492, 508), anchor="start")
        D.legend(602, [("focus", "the wait"), ("risk", "trap"), ("good", "automated"), ("warn", "human")])
        return D

    return {
        "ai901-d1-workload-chooser": ("ai901", workload_chooser),
        "ai901-d2-foundry-flow": ("ai901", foundry_flow),
        "ai901-1-1-fairness": ("ai901", fairness),
        "ai901-1-2-reliability-safety": ("ai901", reliability),
        "ai901-1-3-privacy-security": ("ai901", privacy),
        "ai901-1-4-inclusiveness": ("ai901", inclusiveness),
        "ai901-1-5-transparency": ("ai901", transparency),
        "ai901-1-6-accountability": ("ai901", accountability),
        "ai901-1-8-model-choice": ("ai901", model_choice),
        "ai901-1-9-deployment-choice": ("ai901", deployment_choice),
        "ai901-1-9-parameters": ("ai901", parameters),
        "ai901-1-11-text-analysis": ("ai901", text_analysis),
        "ai901-1-12-speech": ("ai901", speech),
        "ai901-1-13-vision-generation": ("ai901", vision),
        "ai901-1-14-information-extraction": ("ai901", extraction),
        "ai901-2-1-prompt-stack": ("ai901", prompts),
        "ai901-2-2-deploy-and-test": ("ai901", deploy),
        "ai901-2-3-chat-client": ("ai901", chat_client),
        "ai901-2-4-single-agent": ("ai901", agent),
        "ai901-2-5-agent-client": ("ai901", agent_client),
        "ai901-2-6-text-analysis-app": ("ai901", text_app),
        "ai901-2-7-spoken-prompts": ("ai901", spoken),
        "ai901-2-8-speech-sdk": ("ai901", speech_app),
        "ai901-2-9-visual-input": ("ai901", visual_input),
        "ai901-2-10-visual-output": ("ai901", visual_output),
        "ai901-2-11-vision-app": ("ai901", vision_app),
        "ai901-2-12-document-analyzer": ("ai901", doc_analyzer),
        "ai901-2-13-image-analyzer": ("ai901", image_analyzer),
        "ai901-2-14-audio-video-analyzer": ("ai901", audio_video),
        "ai901-2-15-async-extraction": ("ai901", cu_app),
    }
