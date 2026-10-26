"""AB-100 Domain 1 (Plan AI-powered business solutions) diagrams."""


def register(api):
    Diagram, SLATE4, SLATE7 = api["Diagram"], api["SLATE4"], api["SLATE7"]

    def frame(D, x, y, w, h, label):
        D.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#1b2638" '
                      f'fill-opacity=".55" stroke="{SLATE4}" stroke-opacity=".45" stroke-width="1.25"/>')
        D.text(x + 14, y + 22, label.upper(), "title", 12.5, SLATE4, track=0.12)

    def hub_project(f):
        D = Diagram(f, 548, "Azure AI Foundry: Hub vs Project",
                    "Hub = shared platform and governance. Project = individual AI application or team workspace.",
                    "The Azure AI Foundry Hub contains the Hub itself, the shared governance layer, which provides four "
                    "shared resources: Key Vault for shared secrets, Storage Account for shared artifacts, Container "
                    "Registry for shared images, and App Insights for shared monitoring. The Hub serves several projects, "
                    "for example Project: HR Agent, Project: Finance Agent and Project: Customer Support.")
        frame(D, 24, 88, 632, 230, "Azure AI Foundry Hub")
        hub = D.box(340, 140, 260, "Hub", sub="Shared governance layer", kind="focus", h=58)
        xs = [106, 262, 418, 574]
        res = [("Key Vault", "Shared secrets"), ("Storage Account", "Shared artifacts"),
               ("Container Registry", "Shared images"), ("App Insights", "Shared monitoring")]
        for x, (t, s) in zip(xs, res):
            b = D.box(x, 260, 140, t, s, h=72)
            D.edge([(340, hub["b"]), (340, 196), (x, 196), (x, b["t"])])
        frame(D, 24, 372, 632, 130, "Projects")
        for x, name in zip([130, 340, 550], ["HR Agent", "Finance Agent", "Customer Support"]):
            b = D.box(x, 452, 188, "Project: " + name, h=52)
            D.edge([(340, 318), (340, 346), (x, 346), (x, b["t"])])
        D.legend(530, [("focus", "shared governance"), ("solid", "shared with")])
        return D

    def model_selection(f):
        D = Diagram(f, 650, "Model Selection Decision Framework",
                    "Ask the questions in order; stop at the first answer that fits.",
                    "Decision tree starting from the task type. If the task runs on the edge or embedded, use Phi-3 or "
                    "Phi-3.5. If not, ask the reasoning depth: deep reasoning uses GPT-4o or the o1-series. For "
                    "standard reasoning, ask the latency priority: low latency uses GPT-4o-mini or Phi-3-mini, and "
                    "balanced uses GPT-4o.")
        cx = 300
        root = D.box(cx, 112, 170, "Task type", kind="start")
        qs, ys = ["Edge / embedded?", "Reasoning depth?", "Latency priority?"], [216, 336, 456]
        dm = [D.diamond(cx, y, 200, 94, q) for q, y in zip(qs, ys)]
        D.edge([(cx, root["b"]), (cx, dm[0]["t"])])
        D.edge([(cx, dm[0]["b"]), (cx, dm[1]["t"])], dashed=True, label="no", at=(cx + 12, 280), anchor="start")
        D.edge([(cx, dm[1]["b"]), (cx, dm[2]["t"])], label="standard", at=(cx + 12, 400), anchor="start")
        phi = D.box(96, ys[0], 144, "Phi-3 / Phi-3.5", h=56)
        D.edge([(dm[0]["l"], ys[0]), (phi["r"], ys[0])], label="yes", at=(184, ys[0] - 9))
        deep = D.box(584, ys[1], 144, "GPT-4o / o1-series", h=56)
        D.edge([(dm[1]["r"], ys[1]), (deep["l"], ys[1])], label="deep reasoning", at=(456, ys[1] - 10))
        mini = D.box(584, ys[2], 144, "GPT-4o-mini / Phi-3-mini", h=64)
        D.edge([(dm[2]["r"], ys[2]), (mini["l"], ys[2])], label="low latency", at=(456, ys[2] - 10))
        bal = D.box(cx, 572, 170, "GPT-4o", h=52)
        D.edge([(cx, dm[2]["b"]), (cx, bal["t"])], label="balanced", at=(cx + 12, 524), anchor="start")
        D.legend(632, [("start", "start"), ("solid", "answer"), ("dashed", "no")])
        return D

    def ptu(f):
        D = Diagram(f, 478, "Azure OpenAI Capacity Decision Framework",
                    "Size capacity from the traffic estimate: is the peak sustained?",
                    "Start from the traffic estimate in tokens per minute and ask whether the peak is sustained. If yes, "
                    "above 100K tokens per minute, use PTU: reserved capacity with predictable latency. If traffic is "
                    "spiky or variable, use pay-as-you-go: the S0 tier with shared capacity. If both, use a PTU "
                    "baseline with pay-as-you-go overflow.")
        cy = 270
        src = D.box(100, cy, 152, "Traffic estimate", sub="tokens/min", kind="data", h=62)
        dm = D.diamond(290, cy, 168, 128, "Peak sustained?")
        D.edge([(src["r"], cy), (dm["l"], cy)])
        outs = [(150, "PTU", "Reserved capacity\nPredictable latency", "yes, > 100K TPM"),
                (cy, "Pay-as-you-go", "S0 tier\nShared capacity", "spiky / variable"),
                (390, "PTU baseline + PAYG overflow", None, "both")]
        bs = [D.box(568, y, 176, t, b, h=76) for y, t, b, _ in outs]
        D.edge([(290, dm["t"]), (290, 150), (bs[0]["l"], 150)], label=outs[0][3], at=(385, 141))
        D.edge([(dm["r"], cy), (bs[1]["l"], cy)], label=outs[1][3], at=(424, cy - 10))
        D.edge([(290, dm["b"]), (290, 390), (bs[2]["l"], 390)], label=outs[2][3], at=(385, 381))
        D.legend(460, [("data", "input"), ("solid", "answer")])
        return D

    def triggers(f):
        D = Diagram(f, 470, "Event-Driven Agent Trigger Patterns",
                    "Event sources reach the agent through an integration service; the agent then acts.",
                    "Four event sources trigger an AI agent in AI Foundry, each through an integration service: an email "
                    "arriving in Exchange via Logic Apps, a form submitted in Power Apps via Power Automate, a queue "
                    "message in Service Bus via an Azure Function, and a document uploaded to Blob Storage via Event "
                    "Grid. The agent then takes actions: update CRM, send response, or create ticket.")
        ys = [132, 214, 296, 378]
        srcs = [("Email arrives", "Exchange", "Logic Apps"), ("Form submitted", "Power Apps", "Power Automate"),
                ("Queue message", "Service Bus", "Azure Function"), ("Document uploaded", "Blob Storage", "Event Grid")]
        ag = D.box(368, 255, 136, "AI Agent", "AI Foundry", kind="focus", h=150)
        for y, (t, b, via) in zip(ys, srcs):
            s = D.box(102, y, 156, t, b, kind="data", h=64)
            if ag["t"] < y < ag["b"]:
                D.edge([(s["r"], y), (ag["l"], y)], label=via, at=(240, y - 10))
            else:
                end = ag["t"] if y < ag["t"] else ag["b"]
                D.edge([(s["r"], y), (322, y), (322, end)], label=via, at=(240, y - 10))
        for y, a in zip([175, 255, 335], ["Update CRM", "Send response", "Create ticket"]):
            b = D.box(580, y, 152, a, sub="action", h=60)
            D.edge([(ag["r"], 255), (468, 255), (468, y), (b["l"], y)])
        D.legend(452, [("data", "event source"), ("focus", "agent"), ("solid", "trigger / action")])
        return D

    return {
        "ab100-d1-hub-vs-project": ("ab100", hub_project),
        "ab100-d1-model-selection": ("ab100", model_selection),
        "ab100-d1-ptu-capacity": ("ab100", ptu),
        "ab100-d1-event-trigger-patterns": ("ab100", triggers),
    }
