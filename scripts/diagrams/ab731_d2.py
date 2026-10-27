"""AB-731 Domain 2 (Microsoft AI Apps & Services) diagrams.
Source PNGs: content/skillup/ab731/images/d2-microsoft-ai-services-01..06.png"""


def register(api):
    Diagram, SLATE4, SLATE7, W = api["Diagram"], api["SLATE4"], api["SLATE7"], api["W"]

    def products(f):
        D = Diagram(f, 620, "Who Uses Which Microsoft AI Product",
                    "Business users work in Copilot products; developers and IT build on Microsoft Foundry.",
                    "Two audiences. Business users use three products: Microsoft 365 Copilot (AI in Word, Excel, "
                    "Teams and Outlook), Microsoft Copilot (free, Bing-based, consumer; no access to org data) and "
                    "Copilot Studio (build custom copilots and agents). Microsoft 365 Copilot and Copilot Studio "
                    "connect to Microsoft Graph, your organisation's data connector. Developers and IT professionals "
                    "use Microsoft Foundry to build enterprise AI, which in turn uses Azure AI Search and Azure Vision "
                    "in Foundry Tools.")
        D.text(24, 110, "BUSINESS USERS", "title", 12, SLATE4, track=0.12)
        user = D.box(340, 132, 200, "Business user", kind="start")
        cols = [120, 340, 560]
        spec = [("Microsoft 365 Copilot", None, "AI in Word, Excel, Teams, Outlook"),
                ("Microsoft Copilot", "no access to org data", "Free / Bing / consumer"),
                ("Copilot Studio", None, "Build custom copilots / agents")]
        ps = [D.box(x, 250, 200, t, b, sub=s, h=84) for x, (t, s, b) in zip(cols, spec)]
        for x in cols:
            D.edge([(340, user["b"]), (340, 178), (x, 178), (x, ps[0]["t"])] if x != 340
                   else [(340, user["b"]), (340, ps[1]["t"])])
        g = D.box(340, 364, 240, "Microsoft Graph", "Your org's data connector", kind="data", h=60)
        D.edge([(120, ps[0]["b"]), (120, 312), (280, 312), (280, g["t"])])
        D.edge([(560, ps[2]["b"]), (560, 312), (400, 312), (400, g["t"])])
        D.front.append(f'<line x1="24" y1="420" x2="{W - 24}" y2="420" stroke="{SLATE7}" stroke-width="1"/>')
        D.text(24, 448, "DEVELOPERS / IT", "title", 12, SLATE4, track=0.12)
        dev = D.box(110, 516, 170, "Developer / IT professional", kind="start", h=64)
        fd = D.box(330, 516, 180, "Microsoft Foundry", "Build enterprise AI", h=64)
        se = D.box(562, 476, 188, "Azure AI Search", h=52)
        vi = D.box(562, 556, 188, "Azure Vision in Foundry Tools", h=52)
        D.edge([(dev["r"], 516), (fd["l"], 516)])
        D.edge([(fd["r"], 516), (444, 516), (444, 476), (se["l"], 476)])
        D.edge([(fd["r"], 516), (444, 516), (444, 556), (vi["l"], 556)])
        D.legend(604, [("start", "audience"), ("data", "org data layer")])
        return D

    def graph(f):
        D = Diagram(f, 492, "Microsoft Graph: The Data Connector",
                    "Copilot reaches your organisation's Microsoft 365 data through the Graph API.",
                    "Microsoft 365 Copilot calls the Microsoft Graph API, which connects to five Microsoft 365 data "
                    "sources: Outlook (mail and calendar), Microsoft Teams (chat and collaboration), SharePoint "
                    "(files and intranet), OneDrive (files and storage), and the Microsoft 365 apps (Word, Excel, "
                    "PowerPoint and others).")
        src = [("Outlook", "Mail & calendar"), ("Microsoft Teams", "Chat & collaboration"),
               ("SharePoint", "Files & intranet"), ("OneDrive", "Files & storage"),
               ("Microsoft 365 apps", "Word, Excel, PowerPoint, etc.")]
        ys = [130 + i * 70 for i in range(5)]
        mid = ys[2]
        cp = D.box(92, mid, 136, "M365 Copilot", kind="start", h=60)
        g = D.box(282, mid, 160, "Microsoft Graph API", kind="focus", h=72)
        D.edge([(cp["r"], mid), (g["l"], mid)])
        for (t, b), y in zip(src, ys):
            s = D.box(540, y, 232, t, b, kind="data", h=58)
            D.edge([(g["r"], mid), (396, mid), (396, y), (s["l"], y)] if y != mid else [(g["r"], mid), (s["l"], mid)])
        D.legend(476, [("focus", "the connector"), ("data", "M365 data source")])
        return D

    def studio(f):
        D = Diagram(f, 330, "What Copilot Studio Connects To",
                    "A custom agent draws on knowledge, takes actions, and reaches other systems.",
                    "Copilot Studio has three building blocks. Knowledge base: SharePoint, websites, documents and "
                    "similar sources. Power Automate: take actions in business processes and apps. Connectors: "
                    "Salesforce, SAP, Dataverse, APIs and other systems.")
        top = D.box(340, 118, 220, "Copilot Studio", kind="focus", h=52)
        cols = [122, 340, 558]
        spec = [("Knowledge base", "SharePoint, websites, documents, etc.", "data"),
                ("Power Automate", "Take actions in business processes and apps", "neutral"),
                ("Connectors", "Salesforce, SAP, Dataverse, APIs, etc.", "data")]
        for x, (t, b, k) in zip(cols, spec):
            bx = D.box(x, 240, 196, t, b, kind=k, h=84)
            D.edge([(340, top["b"]), (340, 170), (x, 170), (x, bx["t"])] if x != 340
                   else [(340, top["b"]), (340, bx["t"])])
        D.legend(314, [("data", "knowledge / data"), ("neutral", "actions")])
        return D

    def toggle(f):
        D = Diagram(f, 300, "Copilot Chat: Work vs Web Toggle",
                    "The toggle decides whether Copilot searches your org data or the public web.",
                    "A user asks Copilot Chat. With the Work toggle, Copilot Chat searches Microsoft Graph: emails, "
                    "docs, Teams and calendar. With the Web toggle, it searches Bing, the public internet.")
        mid = 186
        u = D.box(72, mid, 96, "User", kind="start", h=52)
        c = D.box(220, mid, 140, "Copilot Chat", kind="focus", h=60)
        D.edge([(u["r"], mid), (c["l"], mid)])
        wk = D.box(546, 130, 220, "Microsoft Graph", "Emails · Docs · Teams · Calendar", kind="data", h=66)
        wb = D.box(546, 242, 220, "Bing", "Public internet", kind="data", h=66)
        D.edge([(c["r"], mid), (310, mid), (310, 130), (wk["l"], 130)], label="Work toggle", at=(330, 121), anchor="start")
        D.edge([(c["r"], mid), (310, mid), (310, 242), (wb["l"], 242)], label="Web toggle", at=(330, 233), anchor="start")
        return D

    def mapping(f):
        D = Diagram(f, 236, "Mapping a Business Process to Copilot",
                    "Four steps from task list to Copilot feature; start where ROI is fastest.",
                    "Step 1: list all tasks in the process. Step 2: classify each task as automatable, augmentable, "
                    "judgment-heavy or relationship-based. Step 3: prioritise automatable and augmentable tasks for "
                    "the fastest ROI. Step 4: map each to a Copilot feature such as Teams, Excel, Chat or an agent.")
        w, gap = 144, 20
        spec = [("List all tasks", "in the process", "neutral"),
                ("Classify each", "Auto / Augment / Judgment / Relationship", "neutral"),
                ("Prioritise Auto + Augment", "for fastest ROI", "focus"),
                ("Map to Copilot feature", "Teams / Excel / Chat / Agent", "neutral")]
        prev = None
        for i, (t, b, k) in enumerate(spec):
            cx = 24 + w / 2 + i * (w + gap)
            bx = D.box(cx, 160, w, t, b, kind=k, h=104)
            D.badge(bx["cx"], bx["t"], i + 1)
            if prev: D.edge([(prev["r"], 160), (bx["l"], 160)])
            prev = bx
        return D

    def models(f):
        D = Diagram(f, 578, "Choosing a Foundry Model",
                    "Match model capability to the task; bigger is not always better.",
                    "Decision tree. Is it complex reasoning or a long document? If yes, choose a proprietary solution "
                    "such as GPT-4o. If no, is it budget-sensitive or an edge deployment? If yes, choose "
                    "Phi-3, a lightweight model. If no, is open source or cost control wanted? If yes, choose an "
                    "open-source solution such as Llama 3 or Mistral; if no, choose the proprietary solution.")
        cx = 200
        q = [D.diamond(cx, y, 236, 96, t) for y, t in
             [(144, "Complex reasoning or a long document?"), (276, "Budget-sensitive or edge deployment?"),
              (408, "Open-source or cost control?")]]
        D.edge([(cx, q[0]["b"]), (cx, q[1]["t"])], dashed=True, label="no", at=(cx + 12, 215), anchor="start")
        D.edge([(cx, q[1]["b"]), (cx, q[2]["t"])], dashed=True, label="no", at=(cx + 12, 347), anchor="start")
        osb = D.box(cx, 508, 220, "Open-source solution", "Llama 3 / Mistral", h=56)
        D.edge([(cx, q[2]["b"]), (cx, osb["t"])], label="yes", at=(cx + 12, 472), anchor="start")
        phi = D.box(510, 276, 200, "Phi-3", "Lightweight", h=56)
        D.edge([(q[1]["r"], 276), (phi["l"], 276)], label="yes", at=(364, 267))
        pr = D.box(510, 408, 200, "Proprietary solution", "Large frontier model (e.g. GPT-4o)", h=56)
        D.edge([(q[2]["r"], 408), (pr["l"], 408)], dashed=True, label="no", at=(364, 399))
        D.edge([(q[0]["r"], 144), (640, 144), (640, 408), (pr["r"], 408)], label="yes", at=(560, 135))
        D.legend(562, [("solid", "yes"), ("dashed", "no")])
        return D

    return {
        "ab731-d2-ai-products-by-audience": ("ab731", products),
        "ab731-d2-graph-data-connector": ("ab731", graph),
        "ab731-d2-copilot-studio-building-blocks": ("ab731", studio),
        "ab731-d2-copilot-chat-work-web-toggle": ("ab731", toggle),
        "ab731-d2-process-to-copilot-mapping": ("ab731", mapping),
        "ab731-d2-foundry-model-choice": ("ab731", models),
    }
