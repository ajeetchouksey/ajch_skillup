"""AI-901 (Microsoft Azure AI Fundamentals) diagrams."""


def register(api):
    Diagram = api["Diagram"]

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

    return {
        "ai901-d1-workload-chooser": ("ai901", workload_chooser),
        "ai901-d2-foundry-flow": ("ai901", foundry_flow),
    }
