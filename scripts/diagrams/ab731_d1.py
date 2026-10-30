"""AB-731 Domain 1 (Business Value of Generative AI) diagrams."""


def register(api):
    Diagram = api["Diagram"]
    LINE, SLATE4, SLATE7 = api["LINE"], api["SLATE4"], api["SLATE7"]

    def ai_types(f):
        D = Diagram(f, 476, "AI Type Selection Framework",
                    "Choose the AI approach by what the business problem needs the output to be.",
                    "Input data, such as raw data, documents, images, transactions and logs, branches into four "
                    "AI approaches. To generate new content, use generative AI (LLM or diffusion models). To classify "
                    "or label, use discriminative ML (random forest or SVM). To predict a number, use regression ML "
                    "(linear or neural). To surface relevant items, use recommendation (collaborative filtering).")
        ys = [122, 210, 298, 386]
        inp = D.box(126, 254, 204, "Input data",
                    "Your raw data, documents, images, transactions, logs, etc.", kind="data", h=104)
        spec = [("Generate new content", "Generative AI", "LLM / Diffusion", "focus"),
                ("Classify or label", "Discriminative ML", "Random Forest / SVM", "neutral"),
                ("Predict a number", "Regression ML", "Linear / Neural", "neutral"),
                ("Surface relevant items", "Recommendation", "Collaborative Filtering", "neutral")]
        tx = 288
        for y, (t, s, b, k) in zip(ys, spec):
            bx = D.box(492, y, 328, t, b, kind=k, sub=s, h=74)
            D.edge([(inp["r"], 254), (tx, 254), (tx, y), (bx["l"], y)], hot=(k == "focus"))
        D.legend(456, [("data", "input"), ("focus", "generative AI"), ("neutral", "other AI types")])
        return D

    def rag_sequence(f):
        D = Diagram(f, 470, "Grounding with RAG",
                    "The model retrieves from your data before it answers, so the reply is grounded and current.",
                    "Sequence between the user, the AI model and your data (SharePoint or a database). 1: the user "
                    "asks the AI model \"What is our Q3 sales number?\". 2: the AI model retrieves relevant chunks "
                    "from your data. 3: your data returns \"Q3 sales: $4.2M (from report)\". 4: the AI model answers "
                    "the user \"Your Q3 sales were $4.2M, up 12% YoY\".")
        xu, xm, xd = 110, 340, 570
        top, end = 126, 424
        for x in (xu, xm, xd):
            D.back.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{end}" stroke="{SLATE7}" '
                          f'stroke-width="1.5" stroke-dasharray="3 4"/>')
        D.box(xu, top, 180, "User", kind="start", h=52)
        D.box(xm, top, 180, "AI model", kind="neutral", h=52)
        D.box(xd, top, 180, "Your data", kind="data", sub="SharePoint / DB", h=60)
        msgs = [(206, xu, xm, "1  “What is our Q3 sales number?”", False, False),
                (268, xm, xd, "2  Retrieve relevant chunks", False, True),
                (330, xd, xm, "3  “Q3 sales: $4.2M (from report)”", True, False),
                (392, xm, xu, "4  “Your Q3 sales were $4.2M, up 12% YoY”", True, False)]
        for y, a, b, lab, dashed, hot in msgs:
            s = 1 if b > a else -1
            D.edge([(a + 6 * s, y), (b - 8 * s, y)], dashed=dashed, hot=hot,
                   label=lab, at=((a + b) / 2, y - 10))
        D.legend(452, [("solid", "request"), ("dashed", "response"), ("data", "your data")])
        return D

    def value_matrix(f):
        D = Diagram(f, 420, "AI Use Case Prioritisation Matrix",
                    "Score each use case on business value and implementation feasibility.",
                    "Two-by-two matrix of business value against implementation feasibility. High value and high "
                    "feasibility: Quick Wins, do first. High value and low feasibility: Strategic Bets, plan for "
                    "later. Low value and high feasibility: Incremental Gains, do if capacity allows. Low value and "
                    "low feasibility: Avoid, don't do.")
        cl, cr, w = 264, 528, 248
        ry = [176, 302]; h = 110
        for x, t in ((cl, "LOW FEASIBILITY"), (cr, "HIGH FEASIBILITY")):
            D.text(x, 110, t, "title", 12.5, SLATE4, "middle", track=0.12)
        for y, t in ((ry[0], "HIGH"), (ry[1], "LOW")):
            D.text(24, y - 2, t, "title", 12.5, SLATE4, track=0.12)
            D.text(24, y + 14, "BUSINESS VALUE", "title", 12.5, SLATE4, track=0.12)
        D.box(cl, ry[0], w, "Strategic Bets", "High reward but needs investment", kind="warn", sub="Plan for later", h=h)
        D.box(cr, ry[0], w, "Quick Wins", "Fast ROI, builds confidence", kind="focus", sub="Do first", h=h)
        D.box(cl, ry[1], w, "Avoid", "Don't invest time or resources", kind="risk", sub="Don't do", h=h)
        D.box(cr, ry[1], w, "Incremental Gains", "Low value, but easy to deliver", sub="Do if capacity", h=h)
        D.legend(400, [("focus", "do first"), ("warn", "invest carefully"), ("risk", "avoid"), ("neutral", "optional")])
        return D

    return {
        "ab731-d1-ai-type-selection": ("ab731", ai_types),
        "ab731-d1-rag-sequence": ("ab731", rag_sequence),
        "ab731-d1-value-feasibility-matrix": ("ab731", value_matrix),
    }
