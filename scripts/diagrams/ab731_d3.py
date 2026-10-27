"""AB-731 Domain 3 (Implementation & Adoption Strategy) diagrams.

Notes file: content/skillup/ab731/notes/d3-adoption-strategy.md
(ab731-d3-champions-network lives in scripts/build-svg-diagrams.py.)
"""


def register(api):
    Diagram = api["Diagram"]

    def principles(f):
        D = Diagram(f, 432, "Microsoft's Responsible AI Principles",
                    "Six principles, one standard: every AI use case is checked against all of them.",
                    "Hub diagram. Responsible AI sits at the centre with six principles around it. Fairness: no "
                    "discrimination by race, gender, age or disability. Reliability and safety: works consistently, "
                    "fails predictably and safely. Privacy and security: personal data and systems are protected from "
                    "attack and misuse. Inclusiveness: benefits everyone regardless of ability or background. "
                    "Transparency: users understand AI decisions. Accountability: humans remain responsible for AI "
                    "outcomes.")
        hub = D.box(340, 240, 150, "Responsible AI", sub="6 principles", kind="focus", h=72)
        left = [("Fairness", "No discrimination by race, gender, age or disability"),
                ("Reliability & safety", "Works consistently; fails predictably and safely"),
                ("Privacy & security", "Protects personal data and systems from attack and misuse")]
        right = [("Inclusiveness", "Benefits everyone regardless of ability or background"),
                 ("Transparency", "Users understand AI decisions"),
                 ("Accountability", "Humans remain responsible for AI outcomes")]
        ys = [140, 240, 340]
        for (t, b), y in zip(left, ys):
            bx = D.box(118, y, 190, t, b, h=84)
            D.edge([(hub["l"], 240), (240, 240), (240, y), (bx["r"], y)])
        for (t, b), y in zip(right, ys):
            bx = D.box(562, y, 190, t, b, h=84)
            D.edge([(hub["r"], 240), (440, 240), (440, y), (bx["l"], y)])
        D.legend(412, [("focus", "the standard"), ("neutral", "principle")])
        return D

    def council(f):
        D = Diagram(f, 392, "Composition of an AI Council",
                    "Cross-functional, not IT alone: each function brings its own remit.",
                    "The AI Council draws members from five functions. Business leadership: strategy, vision, "
                    "investment and oversight. IT and technology: architecture, infrastructure, security and "
                    "integration. Legal and compliance: policies, regulations, risk management and ethics. HR and "
                    "people: talent, training, change management and culture. Business functions such as finance, "
                    "marketing, sales and operations: use cases, adoption, measurement and value realization.")
        top = D.box(340, 116, 220, "AI Council", sub="Cross-functional", kind="focus", h=60)
        cols = [("Business leadership", None, "Strategy\nVision\nInvestment\nOversight"),
                ("IT / technology", None, "Architecture\nInfrastructure\nSecurity\nIntegration"),
                ("Legal & compliance", None, "Policies\nRegulations\nRisk mgmt\nEthics"),
                ("HR / people", None, "Talent\nTraining\nChange mgmt\nCulture"),
                ("Business functions", "Finance, marketing, sales, ops", "Use cases\nAdoption\nMeasurement\nValue realization")]
        w, gap = 122, 8
        x0 = (680 - (5 * w + 4 * gap)) / 2
        for i, (t, s, b) in enumerate(cols):
            cx = x0 + w / 2 + i * (w + gap)
            bx = D.box(cx, 274, w, t, b, sub=s, h=174)
            D.edge([(340, top["b"]), (340, 166), (cx, 166), (cx, bx["t"])])
        D.legend(380, [("focus", "governing body"), ("neutral", "member function")])
        return D

    def checklist(f):
        D = Diagram(f, 676, "Responsible AI Implementation Checklist",
                    "Verify these before deploying any AI solution. High-risk use cases get an extra gate.",
                    "Flow. Identify the use case, then ask whether it is high risk: health, finance, HR or legal. If yes, "
                    "it requires human review plus compliance sign-off. If no, it follows standard deployment. Both "
                    "paths then define a governance policy, document AI usage for employees, establish a feedback and "
                    "incident channel, and finish with a quarterly AI council review.")
        cx = 340
        start = D.box(cx, 112, 200, "Identify use case", kind="start")
        dm = D.diamond(cx, 232, 236, 120, "High risk? Health / Finance / HR / Legal")
        D.edge([(cx, start["b"]), (cx, dm["t"])])
        yes = D.box(98, 232, 148, "Human review + compliance sign-off", kind="warn", h=72)
        no = D.box(582, 232, 148, "Standard deployment", h=72)
        D.edge([(dm["l"], 232), (yes["r"], 232)], label="yes", at=(198, 223))
        D.edge([(dm["r"], 232), (no["l"], 232)], dashed=True, label="no", at=(482, 223))
        steps = [("Define governance policy", 360), ("Document AI usage for employees", 440),
                 ("Establish feedback / incident channel", 520), ("Quarterly AI council review", 600)]
        bs = [D.box(cx, y, 260, t, h=52) for t, y in steps]
        D.edge([(98, yes["b"]), (98, 360), (bs[0]["l"], 360)])
        D.edge([(582, no["b"]), (582, 360), (bs[0]["r"], 360)])
        for a, b in zip(bs, bs[1:]):
            D.edge([(cx, a["b"]), (cx, b["t"])])
        D.legend(656, [("solid", "yes / flow"), ("dashed", "no"), ("warn", "extra gate"), ("start", "start")])
        return D

    def chain(D, y, steps, h):
        w, gap = 138, 26
        x0 = (680 - (4 * w + 3 * gap)) / 2
        bs = [D.box(x0 + w / 2 + i * (w + gap), y, w, t, b, kind=k, h=h) for i, (t, b, k) in enumerate(steps)]
        for a, b in zip(bs, bs[1:]):
            D.edge([(a["r"], y), (b["l"], y)])
        return bs

    def strategy(f):
        D = Diagram(f, 236, "Aligning AI to Business Strategy",
                    "Start from business need and work toward technology, never the reverse.",
                    "Four steps left to right. Start with business strategy and its top three priorities. Map each to "
                    "an AI opportunity: which task, which tool. Set KPIs with measurable outcomes. Secure an executive "
                    "sponsor for funding and endorsement.")
        chain(D, 142, [("Business strategy", "Top 3 priorities", "focus"),
                       ("Map to AI opportunity", "Which task? Which tool?", "neutral"),
                       ("Set KPIs", "Measurable outcomes", "neutral"),
                       ("Executive sponsor", "Funding + endorsement", "neutral")], 92)
        D.legend(220, [("focus", "start here"), ("solid", "flow")])
        return D

    def data_estate(f):
        D = Diagram(f, 476, "The Unified Data Estate",
                    "Break down silos: connect every source into one layer before AI builds on it.",
                    "CRM data, ERP data, HR data and other data all flow into Microsoft Fabric, the unified data layer. "
                    "Fabric then feeds two outcomes: analytics and reporting (dashboards, reports, insights) and AI and "
                    "advanced analytics (machine learning, forecasting, advanced insights).")
        srcs = ["CRM data", "ERP data", "HR data", "Other data"]
        w, gap = 136, 18
        x0 = (680 - (4 * w + 3 * gap)) / 2
        fab = D.box(340, 266, 280, "Microsoft Fabric", sub="Unified data layer", kind="focus", h=72)
        targets = [240, 300, 380, 440]
        for i, (s, tx) in enumerate(zip(srcs, targets)):
            cx = x0 + w / 2 + i * (w + gap)
            b = D.box(cx, 116, w, s, kind="data", h=48)
            D.edge([(cx, b["b"]), (cx, 186), (tx, 186), (tx, fab["t"])])
        outs = [(190, 250, "Analytics & reporting", "Dashboards, reports, insights"),
                (490, 430, "AI & advanced analytics", "Machine learning, forecasting, advanced insights")]
        for cx, sx, t, b in outs:
            o = D.box(cx, 394, 270, t, b, kind="good", h=72)
            D.edge([(sx, fab["b"]), (sx, 336), (cx, 336), (cx, o["t"])])
        D.legend(458, [("data", "source"), ("focus", "unified layer"), ("good", "outcome")])
        return D

    def adoption_curve(f):
        D = Diagram(f, 236, "Adoption Curve for AI",
                    "Each stage has its own lever, from leadership comms to hands-on support.",
                    "Four stages left to right. Awareness, driven by leadership communications. Interest, driven by demos "
                    "and pilots. Trial, driven by the champions programme. Adoption, sustained by training and support.")
        chain(D, 142, [("Awareness", "Leadership comms", "neutral"),
                       ("Interest", "Demos + pilots", "neutral"),
                       ("Trial", "Champions programme", "neutral"),
                       ("Adoption", "Training + support", "good")], 84)
        D.legend(220, [("good", "goal"), ("solid", "progression")])
        return D

    def scale(f):
        D = Diagram(f, 588, "Scale AI Framework: From Pilot to Enterprise",
                    "Prove value, organise for it, then put AI in the hands of users and experts.",
                    "Four phases in sequence, following Microsoft Learn's Scale AI in your organization module. "
                    "Phase 1, unlock AI value: align leaders on two or three strategic bets, prove ROI with focused "
                    "pilots, secure executive sponsorship and define KPIs. Phase 2, organise for AI success: AI Council "
                    "plus Centre of Excellence plus business unit leads, with clear roles to decide, build and govern. "
                    "Phase 3, empower business users: broad Copilot rollout with AI in everyday apps, backed by a "
                    "champions programme and training. Phase 4, empower subject matter experts: experts build their "
                    "own agents and apps with no-code and low-code tools such as Copilot Studio, Power Platform and "
                    "Microsoft Foundry, with the CoE mentoring and reviewing.")
        cx, w = 340, 480
        p = [D.box(cx, 144, w, "Phase 1: Unlock AI value",
                   "Align leaders on 2–3 strategic bets\nProve ROI with focused pilots\nExec sponsorship + KPIs", h=88),
             D.box(cx, 260, w, "Phase 2: Organise for AI success",
                   "AI Council + CoE + BU leads\nClear roles: decide, build, govern", h=72),
             D.box(cx, 376, w, "Phase 3: Empower business users",
                   "Broad Copilot rollout: AI in everyday apps\nChampions programme + training", h=72),
             D.box(cx, 492, w, "Phase 4: Empower subject matter experts",
                   "Experts build their own agents and apps\nNo/low-code: Copilot Studio, Power Platform, Foundry\nCoE mentors and reviews", h=88)]
        for i, b in enumerate(p):
            D.badge(b["l"] + 22, b["t"] + 22, i + 1)
        for a, b in zip(p, p[1:]):
            D.edge([(cx, a["b"]), (cx, b["t"])])
        D.legend(570, [("solid", "next phase")])
        return D

    return {
        "ab731-d3-responsible-ai-principles": ("ab731", principles),
        "ab731-d3-ai-council": ("ab731", council),
        "ab731-d3-implementation-checklist": ("ab731", checklist),
        "ab731-d3-strategy-alignment": ("ab731", strategy),
        "ab731-d3-unified-data-estate": ("ab731", data_estate),
        "ab731-d3-adoption-curve": ("ab731", adoption_curve),
        "ab731-d3-scale-framework": ("ab731", scale),
    }
