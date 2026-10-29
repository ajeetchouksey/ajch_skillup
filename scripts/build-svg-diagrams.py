#!/usr/bin/env python3
"""
Builds AaryaAI-branded SVG diagrams for SkillUp notes.

  python scripts/build-svg-diagrams.py --fonts <dir> [--only <diagram-id>]

<dir> must contain Barlow-Regular.ttf, Barlow-Medium.ttf and
BarlowCondensed-SemiBold.ttf (SIL OFL, from google/fonts). Each diagram is
written to content/skillup/{exam}/images/{name}.svg with the glyphs it uses
subset and embedded as WOFF2: notes load images through <img>, which cannot
see the page's web fonts. Requires: pip install fonttools brotli

Brand source: ajch_food_for_thoughts/brand/BRAND.md sections 5-6 (the canonical
AaryaAI brand; ajch_platform's src/index.css @theme implements it): Barlow
Condensed 600 for headings and labels, Barlow for body, indigo #5B4BD6 as the
one accent fill, lilac #A99BFF for accent on dark, no blue accent. Surfaces and
status colours follow ajch_platform's glass-card + Mermaid colour-by-meaning
palette (.claude/skills/mermaid-diagram-craft/SKILL.md). ajch_brand's
Inter / violet / sky tokens are stale; don't use them.

Layout: notes render images at most 680px wide (Notes.tsx `max-w-[680px]`),
so every diagram is drawn at width 680 and shows at 1:1. Keep text >= 12px.

Visual grammar (keep it when adding diagrams):
  shape   rounded rect = step/outcome   diamond = decision
  line    solid = yes / happy path      dashed = no / alternative
  colour  indigo fill  = the recommended path or focal concept (one per diagram)
          blue         = input / data
          emerald      = good outcome / mitigation
          amber        = warning / lever to watch
          rose         = risk / anti-pattern
          slate        = everything else
"""
import argparse, base64, io, os
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "skillup")
W = 680

# BRAND.md section 5 accent + platform status colours
INDIGO, LILAC = "#5B4BD6", "#A99BFF"
BLUE4 = "#60a5fa"
EMERALD4, AMBER4, ROSE4 = "#34d399", "#fbbf24", "#fb7185"
SLATE7, SLATE4 = "#334155", "#94a3b8"
TEXT = "#e2e8f0"              # Mermaid primaryTextColor
LINE = "#64748b"              # Mermaid lineColor
LABEL_BG = "#162236"          # Mermaid edgeLabelBackground
# (fill, stroke, text, secondary text) — fills from the Mermaid colour-by-meaning palette
KINDS = {
    "neutral": ("#1a2a42", SLATE7, TEXT, SLATE4),
    "start":   ("#111f35", SLATE7, TEXT, SLATE4),
    "data":    ("#162236", BLUE4, TEXT, SLATE4),
    "good":    ("#1a2a12", EMERALD4, TEXT, SLATE4),
    "warn":    ("#2a1a22", AMBER4, TEXT, SLATE4),
    "risk":    ("#2a1a1a", ROSE4, TEXT, SLATE4),
    "focus":   (INDIGO, LILAC, "#ffffff", "#F0EDFF"),
}
# Focal accent per diagram: (fill, on-dark stroke/accent, secondary text on fill).
# Default indigo (AaryaAI brand). "teal" is SkillUp's "Focus Teal" co-brand (AI-901);
# pick it with Diagram(..., accent="teal") or a partial in the exam's module.
ACCENTS = {"indigo": (INDIGO, LILAC, "#F0EDFF"), "teal": ("#0E7C86", "#4CC1CA", "#E0F7F8")}
# key: (file, family, weight)
FACES = {"title": ("BarlowCondensed-SemiBold.ttf", "Barlow Condensed", 600),
         "label": ("Barlow-Medium.ttf", "Barlow", 500),
         "body":  ("Barlow-Regular.ttf", "Barlow", 400)}
FAMILY = {"Barlow Condensed": "'Barlow Condensed', ui-sans-serif, system-ui, sans-serif",
          "Barlow": "Barlow, ui-sans-serif, system-ui, sans-serif"}


class Fonts:
    def __init__(self, d):
        self.dir = d
        self.tt = {k: TTFont(os.path.join(d, f)) for k, (f, *_) in FACES.items()}

    def width(self, face, text, size):
        tt = self.tt[face]; cmap = tt.getBestCmap(); hmtx = tt["hmtx"]
        return sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in text) * size / tt["head"].unitsPerEm

    def wrap(self, face, text, size, maxw):
        lines = []
        for para in text.split("\n"):
            cur = ""
            for w in para.split(" "):
                t = (cur + " " + w).strip()
                if cur and self.width(face, t, size) > maxw: lines.append(cur); cur = w
                else: cur = t
            lines.append(cur)
        return lines

    def embed(self, used):
        css = []
        for k, chars in used.items():
            if not chars: continue
            f, fam, wt = FACES[k]
            opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "calt"]
            font = TTFont(os.path.join(self.dir, f))
            s = subset.Subsetter(opts); s.populate(text="".join(sorted(chars))); s.subset(font)
            buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
            css.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};"
                       f"src:url(data:font/woff2;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff2')}}")
        return "".join(css)


class Diagram:
    def __init__(self, fonts, h, title, subtitle, desc, accent="indigo"):
        self.f, self.h, self.title, self.desc = fonts, h, title, desc
        self.acc = ACCENTS[accent]
        self.kinds = dict(KINDS, focus=(self.acc[0], self.acc[1], "#ffffff", self.acc[2]))
        self.used = {k: set() for k in FACES}
        self.back, self.front = [], []
        self.text(24, 40, title, "title", 21)
        if subtitle:
            for i, ln in enumerate(fonts.wrap("body", subtitle, 14, W - 48)):
                self.text(24, 62 + i * 18, ln, "body", 14, SLATE4)

    def text(self, x, y, s, face, size, fill=TEXT, anchor="start", layer=None, track=None):
        self.used[face].update(s)
        _, fam, wt = FACES[face]
        ls = f' letter-spacing="{track}em"' if track else ""
        (self.front if layer is None else layer).append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[fam]}" font-size="{size}" font-weight="{wt}"{ls} '
            f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def box(self, cx, cy, w, title, body=None, kind="neutral", sub=None, h=None):
        fill, stroke, ink, ink2 = self.kinds[kind]
        tl = self.f.wrap("title", title, 16, w - 24)
        sl = self.f.wrap("label", sub, 13, w - 24) if sub else []
        bl = self.f.wrap("body", body, 13, w - 24) if body else []
        ch = len(tl) * 18 + len(sl) * 16 + (4 + len(bl) * 16 if bl else 0)
        h = h or max(48, ch + 26)
        x, y = cx - w / 2, cy - h / 2
        self.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="10" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
        ty = cy - ch / 2 + 13
        for ln in tl: self.text(cx, ty, ln, "title", 16, ink, "middle"); ty += 18
        for ln in sl: self.text(cx, ty - 1, ln, "label", 13, stroke if kind not in ("neutral", "start", "focus") else ink2, "middle"); ty += 16
        ty += 4
        for ln in bl: self.text(cx, ty, ln, "body", 13, ink2, "middle"); ty += 16
        return dict(cx=cx, cy=cy, l=x, r=x + w, t=y, b=y + h)

    def diamond(self, cx, cy, w, h, label):
        self.front.append(f'<path d="M{cx},{cy - h/2} L{cx + w/2},{cy} L{cx},{cy + h/2} L{cx - w/2},{cy} Z" '
                          f'fill="#1a2a42" stroke="{self.acc[1]}" stroke-width="1.5" stroke-linejoin="round"/>')
        lines = self.f.wrap("title", label, 15, w * 0.56)
        ty = cy - (len(lines) - 1) * 8.5 + 5
        for ln in lines: self.text(cx, ty, ln, "title", 15, TEXT, "middle"); ty += 17
        return dict(cx=cx, cy=cy, l=cx - w/2, r=cx + w/2, t=cy - h/2, b=cy + h/2)

    def edge(self, pts, dashed=False, label=None, at=None, anchor="middle", hot=False):
        r = 8; d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(1, len(pts) - 1):
            (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
            def toward(ax, ay, bx, by):
                L = max(((bx - ax) ** 2 + (by - ay) ** 2) ** .5, 1e-6); k = min(r, L / 2) / L
                return ax + (bx - ax) * k, ay + (by - ay) * k
            a = toward(x1, y1, x0, y0); b = toward(x1, y1, x2, y2)
            d += f" L{a[0]:.1f},{a[1]:.1f} Q{x1:.1f},{y1:.1f} {b[0]:.1f},{b[1]:.1f}"
        d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
        col = self.acc[1] if hot else LINE
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.back.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2 if hot else 1.5}" '
                         f'stroke-linecap="round"{dash} marker-end="url(#{"arrow-hot" if hot else "arrow"})"/>')
        if label:
            x, y = at; tw = self.f.width("label", label, 13)
            bx = x - (tw / 2 if anchor == "middle" else tw if anchor == "end" else 0)
            self.back.append(f'<rect x="{bx - 5:.1f}" y="{y - 12:.1f}" width="{tw + 10:.1f}" height="17" rx="4" fill="{LABEL_BG}"/>')
            self.text(x, y, label, "label", 13, SLATE4, anchor, layer=self.back)

    def badge(self, cx, cy, n):
        self.front.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{self.acc[0]}" stroke="{self.acc[1]}" stroke-width="1"/>')
        self.text(cx, cy + 4, str(n), "title", 11, "#ffffff", "middle")

    def legend(self, y, items):
        x = 24
        for kind, txt in items:
            if kind in ("solid", "dashed"):
                dash = ' stroke-dasharray="5 4"' if kind == "dashed" else ""
                self.front.append(f'<line x1="{x}" y1="{y - 4}" x2="{x + 22}" y2="{y - 4}" stroke="{LINE}" stroke-width="1.5"{dash}/>')
                x += 30
            else:
                fill, stroke, *_ = self.kinds[kind]
                self.front.append(f'<rect x="{x}" y="{y - 11}" width="12" height="12" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
                x += 20
            t = txt.upper(); self.text(x, y, t, "title", 11.5, SLATE4, track=0.12)
            x += self.f.width("title", t, 11.5) + len(t) * 11.5 * 0.12 + 22

    def svg(self):
        H = self.h
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                f'role="img" aria-labelledby="t d">\n'
                f'<title id="t">{escape(self.title)}</title>\n<desc id="d">{escape(self.desc)}</desc>\n'
                f'<defs><style>{self.f.embed(self.used)}</style>\n'
                # glass-card surface, composited over --aarya-bg
                f'<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#263347"/>'
                f'<stop offset="1" stop-color="#1b2638"/></linearGradient>\n'
                # .card-accent-top default strip (indigo to lilac)
                f'<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{self.acc[0]}"/>'
                f'<stop offset="1" stop-color="{self.acc[1]}"/></linearGradient>\n'
                f'<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<rect width="7" height="7" fill="#1a2a42"/><line x1="0" y1="0" x2="0" y2="7" stroke="{SLATE7}" stroke-width="2.5"/></pattern>\n'
                f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,1 L9,5 L0,9 z" fill="{LINE}"/></marker>\n'
                f'<marker id="arrow-hot" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M0,1 L9,5 L0,9 z" fill="{self.acc[1]}"/></marker></defs>\n'
                f'<rect width="{W}" height="{H}" fill="url(#glass)"/>\n'
                f'<rect width="{W}" height="2" fill="url(#brand)"/>\n'
                + "\n".join(self.back) + "\n" + "\n".join(self.front) + "\n</svg>\n")


# ------------------------------------------------------------------ diagrams

def ab100_decision(f):
    D = Diagram(f, 690, "AI Solution Decision Framework",
                "Ask the questions in order; stop at the first answer that fits.",
                "Decision tree. Start from the business problem. If it is structured and rules-based, use RPA or "
                "Logic Apps. Otherwise, if it does not require language understanding, use traditional ML or Azure ML. "
                "If it does not need multi-step reasoning, use Copilot Studio single-turn. If it does not need "
                "autonomous tool use, use Azure OpenAI with prompt flow. If it does, use agentic AI with the AI "
                "Foundry Agent Service.")
    cx = 340
    root = D.box(cx, 112, 190, "Business problem", kind="start")
    qs = ["Structured and rules-based?", "Requires language understanding?",
          "Multi-step reasoning needed?", "Autonomous tool use required?"]
    ys = [216, 336, 456, 576]
    dm = [D.diamond(cx, y, 214, 94, q) for q, y in zip(qs, ys)]
    D.edge([(cx, root["b"]), (cx, dm[0]["t"])])
    for i, (a, b) in enumerate(zip(dm, dm[1:])):
        D.edge([(cx, a["b"]), (cx, b["t"])], dashed=(i == 0), label="no" if i == 0 else "yes",
               at=(cx + 12, (a["b"] + b["t"]) / 2 + 4), anchor="start")
    rpa = D.box(574, ys[0], 160, "RPA / Logic Apps", h=56)
    D.edge([(dm[0]["r"], ys[0]), (rpa["l"], ys[0])], label="yes", at=(470, ys[0] - 9))
    for t, s, y, d in zip(["Traditional ML / Azure ML", "Copilot Studio", "Azure OpenAI + prompt flow"],
                          [None, "single-turn", None], ys[1:], dm[1:]):
        b = D.box(106, y, 164, t, sub=s, h=56)
        D.edge([(d["l"], y), (b["r"], y)], dashed=True, label="no", at=(210, y - 9))
    ag = D.box(574, ys[3], 160, "Agentic AI", sub="AI Foundry Agent Service", kind="focus", h=62)
    D.edge([(dm[3]["r"], ys[3]), (ag["l"], ys[3])], label="yes", at=(470, ys[3] - 9), hot=True)
    D.legend(666, [("solid", "yes"), ("dashed", "no"), ("focus", "agentic path"), ("start", "start")])
    return D


def ccap_context(f):
    D = Diagram(f, 700, "Context Window Budget",
                "Everything competes for one fixed window (e.g. 200K tokens). Two levers move the most.",
                "A single bar represents the context window, split into system prompt and guardrails, tool definitions, "
                "few-shot examples, retrieved context, conversation history, and space reserved for model output. "
                "Lever 1, retrieved context: sending the full corpus is wasteful because it dilutes relevance and "
                "costs tokens; sending only relevant chunks is precise and cheaper. Lever 2, conversation history: if "
                "it grows too large, summarize or compact older turns; otherwise keep it as is.")
    x0, y0, bh = 24, 118, 80
    segs = [("System prompt + guardrails", 96, "neutral"), ("Tool definitions", 92, "neutral"),
            ("Few-shot examples", 84, "neutral"), ("Retrieved context", 146, 1),
            ("Conversation history", 136, 2), ("Reserved output", 78, "hatch")]
    D.text(x0, y0 - 10, "0", "body", 12, SLATE4); D.text(x0 + 632, y0 - 10, "window limit", "body", 12, SLATE4, "end")
    D.front.append(f'<clipPath id="bar"><rect x="{x0}" y="{y0}" width="632" height="{bh}" rx="10"/></clipPath><g clip-path="url(#bar)">')
    x = x0; badges = []
    for name, w, k in segs:
        fill = {"neutral": "#1a2a42", "hatch": "url(#hatch)"}.get(k, KINDS["warn"][0])
        D.front.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{bh}" fill="{fill}"/>')
        if x > x0: D.front.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0 + bh}" stroke="{SLATE7}" stroke-width="1"/>')
        if isinstance(k, int):
            badges.append((x + w / 2, k))
            D.front.append(f'<rect x="{x + 1.5}" y="{y0 + 1.5}" width="{w - 3}" height="{bh - 3}" fill="none" stroke="{AMBER4}" stroke-width="1.25"/>')
        lines = f.wrap("label", name, 12, w - 14)
        ty = y0 + bh / 2 - (len(lines) - 1) * 7.5 + 4 + (8 if isinstance(k, int) else 0)
        for ln in lines:
            if k == "hatch":
                tw = f.width("label", ln, 12)
                D.front.append(f'<rect x="{x + w/2 - tw/2 - 4:.1f}" y="{ty - 12}" width="{tw + 8:.1f}" height="16" rx="3" fill="#1a2a42"/>')
            D.text(x + w / 2, ty, ln, "label", 12, TEXT, "middle"); ty += 15
        x += w
    D.front.append("</g>")
    D.front.append(f'<rect x="{x0}" y="{y0}" width="632" height="{bh}" rx="10" fill="none" stroke="{SLATE4}" stroke-opacity=".5" stroke-width="1.25"/>')
    for bx, n in badges: D.badge(bx, y0 + 18, n)

    def lever(top, n, name, q, ok, ok_t, ok_b, bad, bad_t, bad_b, bad_kind):
        D.badge(33, top, n); D.text(50, top + 5, name, "title", 14)
        cy = top + 98
        d = D.diamond(140, cy, 220, 92, q)
        up = D.box(540, cy - 44, 232, ok_t, ok_b, kind="good", h=64)
        dn = D.box(540, cy + 44, 232, bad_t, bad_b, kind=bad_kind, h=64)
        D.edge([(d["r"], cy), (280, cy), (280, up["cy"]), (up["l"], up["cy"])], label=ok, at=(352, up["cy"] - 10))
        D.edge([(d["r"], cy), (280, cy), (280, dn["cy"]), (dn["l"], dn["cy"])], dashed=True, label=bad, at=(352, dn["cy"] - 10))
    lever(250, 1, "Retrieved context", "Full corpus or relevant chunks?",
          "relevant chunks", "Efficient", "Precise and cheaper", "full corpus", "Wasteful", "Dilutes relevance, costs tokens", "risk")
    lever(452, 2, "Conversation history", "History growing too large?",
          "yes", "Summarize / compact", "Older turns first", "no", "Keep as is", "History still fits", "neutral")
    D.legend(682, [("warn", "levers you control"), ("good", "good outcome"), ("risk", "anti-pattern")])
    return D


def ab731_bias(f):
    D = Diagram(f, 572, "How Bias Enters a Model",
                "Bias flows down the chain; mitigation intervenes at the data and the model.",
                "Training data contains bias. The model learns and internalizes that bias, produces skewed or "
                "discriminatory outputs, and creates business, legal and ethical risk. Mitigation with diverse data, "
                "human feedback (RLHF) and continuous evaluation acts on the training data and the model, and is "
                "triggered by the risk it reduces.")
    cx, w = 158, 256
    spec = [(130, "Training data", "Data used to train the model", "data", "contains bias"),
            (240, "Model learns bias", "Picks up and internalizes patterns and biases from the data", "neutral", None),
            (350, "Biased outputs", "Skewed or discriminatory results", "neutral", None),
            (460, "Business, legal & ethical risk", "Unfair outcomes, compliance issues, reputational damage", "risk", None)]
    bs = [D.box(cx, y, w, t, b, kind=k, sub=s, h=84) for y, t, b, k, s in spec]
    for a, b in zip(bs, bs[1:]): D.edge([(cx, a["b"]), (cx, b["t"])])
    m = D.box(536, 185, 240, "Mitigation", "Diverse data, human feedback (RLHF) and continuous evaluation", kind="good", h=150)
    D.edge([(m["l"], 130), (bs[0]["r"], 130)], label="diverse data", at=(354, 121))
    D.edge([(m["l"], 240), (bs[1]["r"], 240)], label="RLHF, evaluation", at=(354, 231))
    D.edge([(bs[3]["r"], 460), (536, 460), (536, m["b"])], dashed=True, label="risk drives mitigation", at=(536, 400))
    D.legend(548, [("data", "input"), ("risk", "risk"), ("good", "mitigation"), ("dashed", "feedback")])
    return D


def ab731_champions(f):
    D = Diagram(f, 676, "The AI Champions Network",
                "Champions connect top-down enablement with bottom-up adoption.",
                "Two loops meet at AI Champions, one to two per business unit. In the top-down loop the adoption team "
                "and IT train and support champions, and champions surface best practices back to the adoption team. "
                "In the bottom-up loop champions provide peer coaching to colleagues, and colleagues' questions and "
                "feedback flow back to champions.")
    L, R, C, w = 150, 530, 340, 200
    team = D.box(C, 124, w, "Adoption team / IT", "Lead adoption strategy", h=68)
    train = D.box(L, 262, w, "Train & support", "Training and ongoing support build confidence", h=84)
    surf = D.box(R, 262, w, "Surface best practices", "Share and document what works across teams", h=84)
    ch = D.box(C, 406, 220, "AI Champions", "Advocate, influence and accelerate adoption",
               sub="1–2 per business unit", kind="focus", h=96)
    peer = D.box(L, 552, w, "Peer coaching", "Peer-to-peer learning, more trusted than IT", h=84)
    fb = D.box(R, 552, w, "Questions / feedback", "Collected and escalated to improve tools", h=84)
    D.edge([(team["l"], 124), (L, 124), (L, train["t"])])
    D.edge([(L, train["b"]), (L, 332), (290, 332), (290, ch["t"])])
    D.edge([(390, ch["t"]), (390, 332), (R, 332), (R, surf["b"])])
    D.edge([(R, surf["t"]), (R, 124), (team["r"], 124)])
    D.edge([(290, ch["b"]), (290, 482), (L, 482), (L, peer["t"])])
    D.edge([(R, fb["t"]), (R, 482), (390, 482), (390, ch["b"])])
    D.text(C, 266, "top-down", "body", 13, SLATE4, "middle")
    D.text(C, 556, "bottom-up", "body", 13, SLATE4, "middle")
    D.legend(654, [("focus", "the role this section is about"), ("solid", "flow")])
    return D


DIAGRAMS = {
    "ab100-decision-framework": ("ab100", ab100_decision),
    "ab731-d1-bias-chain": ("ab731", ab731_bias),
    "ab731-d3-champions-network": ("ab731", ab731_champions),
    "ccap-d2-context-window-budget": ("ccap", ccap_context),
}

def load_modules():
    """Diagram groups live in scripts/diagrams/*.py, one file per exam/domain,
    so they can be authored independently. Each module exposes
    register(api) -> {name: (exam, fn)}; `api` is this module's namespace
    (Diagram, KINDS, colour constants, W, ...)."""
    import importlib.util, glob
    found = {}
    here = os.path.dirname(os.path.abspath(__file__))
    for path in sorted(glob.glob(os.path.join(here, "diagrams", "*.py"))):
        spec = importlib.util.spec_from_file_location(f"diagrams_{os.path.basename(path)[:-3]}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name, entry in mod.register(globals()).items():
            if name in DIAGRAMS or name in found:
                raise SystemExit(f"duplicate diagram id {name!r} in {path}")
            found[name] = entry
    return found


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--only", help="diagram id, or a prefix such as ab731-d2-")
    a = ap.parse_args()
    fonts = Fonts(a.fonts)
    DIAGRAMS.update(load_modules())
    for name, (exam, fn) in DIAGRAMS.items():
        if a.only and not name.startswith(a.only): continue
        out = os.path.join(ROOT, exam, "images", name + ".svg")
        svg = fn(fonts).svg()
        open(out, "w", encoding="utf8", newline="\n").write(svg)
        print(f"wrote {os.path.relpath(out)}  ({len(svg.encode()) // 1024} KB)")
