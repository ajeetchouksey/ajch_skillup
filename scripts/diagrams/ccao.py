"""CCAO-F (Claude Certified Associate, Foundations) lesson diagrams: one outcome diagram per lesson.

Lesson ids follow the official exam guide numbering (7 domains, 30 objectives), so file names match the
## headings in the notes. Same five layouts as the GH-BP, AB-731 and CCA-F diagrams (lanes, pairs, table,
funnel/converge, stack), plus four CCAO-only shapes: snippet (a marked-up prompt or draft), decide (a
yes/no diamond chain), sheet (a mini spreadsheet with struck columns) and nest (concentric scopes).
Colours follow the SkillUp colour code by meaning: data sky, good green, warn saffron, risk rose,
focus indigo (the one recommended move per diagram), neutral slate.
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

    def cap_w(D, s, size=12.5):
        """Width of a tracked caption (letter-spacing 0.1em)."""
        return D.f.width("title", s, size) + len(s) * size * 0.1

    def cap_wrap(D, s, maxw, size=12.5):
        lines, cur = [], ""
        for w in s.upper().split(" "):
            t = (cur + " " + w).strip()
            if cur and cap_w(D, t, size) > maxw:
                lines.append(cur); cur = w
            else:
                cur = t
        return lines + [cur]

    def cue(D, x, y, s, direction):
        """A caption followed by a short hot arrow (the fonts have no arrow glyphs)."""
        caption(D, x, y, s)
        ax = x + cap_w(D, s.upper()) + 12
        a, b = (y - 12, y + 3) if direction == "down" else (y + 3, y - 12)
        D.edge([(ax, a), (ax, b)], hot=True)

    def finish(D, y, legend):
        if legend:
            rows, cur, used = [], [], 0
            for k, t in legend:
                iw = (30 if k in ("solid", "dashed") else 20) + D.f.width("title", t.upper(), 11.5) + len(t) * 11.5 * 0.12
                if cur and used + iw > W - 48:
                    rows.append(cur); cur, used = [], 0
                cur.append((k, t)); used += iw + 22
            rows.append(cur)
            y += 26
            for i, r in enumerate(rows):
                if i:
                    y += 20
                D.legend(y, r)
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
            D.last_row = bs
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

    def stack(D, y, layers, gap=10, arrows=None):
        """layers: [cells] drawn top to bottom, full width. arrows="down" links each layer to the next;
        arrows="up" points from each layer to the one above, so a ladder listed top-down is climbed from the bottom."""
        if arrows:
            gap = max(gap, 30)
        bs = []
        for c in layers:
            t, b, k, s = cell(c)
            h = need(D, W - 48, t, b, s)
            bs.append(D.box(W / 2, y + h / 2, W - 48, t, b, kind=k, sub=s, h=h))
            y += h + gap
        for a, b2 in zip(bs, bs[1:]):
            if arrows == "down":
                D.edge([(W / 2, a["b"]), (W / 2, b2["t"])], hot=True)
            elif arrows == "up":
                D.edge([(W / 2, b2["t"]), (W / 2, a["b"])], hot=True)
        D.last_row = bs
        return y

    def fan(D, src, dsts):
        """Plain edges from one box's bottom to the tops of several boxes ((cx, top) pairs)."""
        mid = (src["b"] + min(t for _, t in dsts)) / 2
        for cx, t in dsts:
            D.edge([(src["cx"], src["b"]), (src["cx"], mid), (cx, mid), (cx, t)])

    def gather(D, srcs, dst):
        """Hot edges from several bottoms ((cx, bottom) pairs) into one box's top."""
        mid = (max(b for _, b in srcs) + dst["t"]) / 2
        for cx, b in srcs:
            D.edge([(cx, b), (cx, mid), (dst["cx"], mid), (dst["cx"], dst["t"])], hot=True)

    def chip(D, x, y, s, kind, anchor="start"):
        """A small tag: rounded rect at top y, 18 high, text through D.text."""
        fill, stroke, ink, _ = D.kinds[kind]
        w = D.f.width("label", s, 12.5) + 14
        x0 = x - w if anchor == "end" else x
        D.front.append(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{w:.1f}" height="18" rx="5" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
        tc = ink if kind == "focus" else (SLATE4 if kind in ("neutral", "start") else stroke)
        D.text(x0 + 7, y + 13.5, s, "label", 12.5, tc)
        return w

    def head_ink(D, kind):
        fill, stroke, ink, ink2 = D.kinds[kind]
        return ink2 if kind == "focus" else (SLATE4 if kind in ("neutral", "start") else stroke)

    def snippet(D, x, y, w, heading, lines, kind="neutral", marks=None, mono=False, tags="right", h=None, draw=True):
        """A rounded panel of literal text (a prompt, a draft, CSV rows) with optional marked spans.
        marks: [(line index, substring, kind, tag or None)]. tags="right" puts each tag chip at the right of
        the line where its span starts; tags="below" puts chips on a row under that line, at the span.
        Returns the bottom y (draw=False only measures)."""
        f = D.f
        face = "label" if mono else "body"
        marks = marks or []
        fill, stroke, ink, ink2 = D.kinds[kind]
        cw = lambda s: f.width("label", s, 12.5) + 14
        right = tags == "right"
        reserve = (max((cw(m[3]) for m in marks if m[3]), default=0) + 14) if right and any(m[3] for m in marks) else 0
        tw = w - 24 - reserve
        heads = cap_wrap(D, heading, w - 24) if heading else []
        out = []  # deferred drawing calls, run once the panel height is known
        ty = y + 12 + len(heads) * 16 + (6 if heads else 0)
        for i, hl in enumerate(heads):
            out.append(("text", x + 12, y + 24 + i * 16, hl, "title", 12.5, head_ink(D, kind), 0.1))
        spans = []
        for li, sub, mk, tag in marks:
            s0 = lines[li].find(sub)
            if s0 < 0:
                raise ValueError(f"mark {sub!r} not in line {li}")
            spans.append((li, s0, s0 + len(sub), mk, tag))
        for i, s in enumerate(lines):
            off = 0
            for ln in f.wrap(face, s, 13, tw):
                base = ty + 14
                out.append(("text", x + 12, base, ln, face, 13, ink, None))
                ls, le = off, off + len(ln)
                below = []
                for li, s0, s1, mk, tag in spans:
                    if li != i:
                        continue
                    a, b = max(s0, ls), min(s1, le)
                    if a < b:
                        x0 = x + 12 + f.width(face, ln[:a - ls], 13)
                        x1 = x + 12 + f.width(face, ln[:b - ls], 13)
                        out.append(("rect", x0, base + 3.5, x1 - x0, 2, D.kinds[mk][1]))
                    if tag and ls <= s0 <= le:
                        if right:
                            out.append(("chip", x + w - 12, ty + 0.5, tag, mk, "end"))
                        else:
                            below.append((x + 12 + f.width(face, ln[:s0 - ls], 13), tag, mk))
                ty += 19
                if below:
                    cx = None
                    for bx, tag, mk in sorted(below):
                        bx = max(bx, cx or bx)
                        if bx + cw(tag) > x + w - 12:
                            bx = x + w - 12 - cw(tag)
                            if cx and bx < cx:
                                ty += 22; bx = x + 12
                        out.append(("chip", bx, ty + 1, tag, mk, "start"))
                        cx = bx + cw(tag) + 8
                    ty += 24
                off = le + 1
        hh = max(h or 0, ty - y + 10)
        if draw:
            D.front.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{hh:.1f}" rx="10" '
                           f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            for op in out:
                if op[0] == "text":
                    _, tx, tyy, s, fc, sz, col, tr = op
                    D.text(tx, tyy, s, fc, sz, col, track=tr)
                elif op[0] == "rect":
                    _, rx, ry, rw, rh, col = op
                    D.front.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh}" fill="{col}"/>')
                else:
                    _, cx2, cy2, s, mk, anc = op
                    chip(D, cx2, cy2, s, mk, anc)
        return y + hh

    def snip_row(D, y, specs, widths=None, gap=16):
        """specs: [dict(heading, lines, kind, marks, mono, tags)] side by side at equal height.
        Returns (bottom, [(cx, top, bottom)])."""
        n = len(specs)
        widths = widths or [(W - 48 - (n - 1) * gap) / n] * n
        h = max(snippet(D, 0, 0, w, draw=False, **s) for w, s in zip(widths, specs))
        x, pos = 24, []
        for w, s in zip(widths, specs):
            snippet(D, x, y, w, h=h, **s)
            pos.append((x + w / 2, y, y + h)); x += w + gap
        return y + h, pos

    def decide(D, y, steps, end, x=150, dw=250, yes_right=False, src=None):
        """A vertical chain of yes/no diamonds at x. Standard: "no" goes right (dashed) to a fix box and
        "yes" continues down (solid, hot). yes_right=True swaps them: "yes" goes right (solid, hot) to the
        answer and "no" continues down (dashed). steps: [(question, cell)]; end: the cell after the last
        diamond. src: an optional (x, y) point to link into the first diamond. Returns the bottom y."""
        f = D.f
        n = max(len(f.wrap("title", q, 15, dw * 0.56)) for q, _ in steps)
        dh = max(92, int(n * 17 / 0.5) + 2)
        fl = x + dw / 2 + 56
        fw = W - 24 - fl
        rlab, dlab = ("yes", "no") if yes_right else ("no", "yes")
        prev = None
        for q, fix in steps:
            t, b, k, s = cell(fix)
            fh = need(D, fw, t, b, s)
            rowh = max(dh, fh)
            cy = y + rowh / 2
            d = D.diamond(x, cy, dw, dh, q)
            if prev is None and src:
                D.edge([src, (x, d["t"])], hot=True)
            if prev:
                D.edge([(x, prev["b"]), (x, d["t"])], hot=not yes_right, dashed=yes_right,
                       label=dlab, at=(x + 12, (prev["b"] + d["t"]) / 2 + 5), anchor="start")
            bx = D.box(fl + fw / 2, cy, fw, t, b, kind=k, sub=s, h=fh)
            D.edge([(d["r"], cy), (bx["l"], cy)], hot=yes_right, dashed=not yes_right,
                   label=rlab, at=((d["r"] + bx["l"]) / 2, cy - 8))
            prev = d
            y += rowh + 40
        t, b, k, s = cell(end)
        eh = need(D, dw, t, b, s)
        e = D.box(x, y + eh / 2, dw, t, b, kind=k, sub=s, h=eh)
        D.edge([(x, prev["b"]), (x, e["t"])], hot=not yes_right, dashed=yes_right,
               label=dlab, at=(x + 12, (prev["b"] + e["t"]) / 2 + 5), anchor="start")
        D.last_end = e
        D.fix_left = fl
        return y + eh

    def sheet(D, y, cols, rows, struck=(), keep_kind="good", strike_kind="risk", notes=None):
        """A mini spreadsheet. Struck columns take strike_kind's colour, a line through every data cell
        and "removed" under the header; kept columns take keep_kind and "kept". notes: {column: text}
        drawn under the sheet at that column. Returns the bottom y."""
        f = D.f
        n = len(cols); cw = (W - 48) / n
        hls = [f.wrap("title", c, 13.5, cw - 12) for c in cols]
        nh = max(len(h) for h in hls)
        hh = 12 + nh * 15 + 22
        rh = 28
        for j, c in enumerate(cols):
            gone = c in struck
            fill, stroke, ink, _ = D.kinds[strike_kind if gone else keep_kind]
            cx, x0 = 24 + j * cw + cw / 2, 24 + j * cw
            D.front.append(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{hh:.1f}" '
                           f'fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
            top = y + 12 + (nh - len(hls[j])) * 7.5
            for i, ln in enumerate(hls[j]):
                D.text(cx, top + 11 + i * 15, ln, "title", 13.5, ink, "middle")
            D.text(cx, y + hh - 9, "removed" if gone else "kept", "label", 12, stroke, "middle")
            for r, row in enumerate(rows):
                ry = y + hh + r * rh
                D.front.append(f'<rect x="{x0:.1f}" y="{ry:.1f}" width="{cw:.1f}" height="{rh}" '
                               f'fill="{fill}" stroke="{stroke}" stroke-width="1.25"/>')
                D.text(cx, ry + 18.5, row[j], "body", 12.5, SLATE4 if gone else ink, "middle")
                if gone:
                    D.front.append(f'<line x1="{x0 + 6:.1f}" y1="{ry + 14:.1f}" x2="{x0 + cw - 6:.1f}" y2="{ry + 14:.1f}" '
                                   f'stroke="{stroke}" stroke-width="1.75"/>')
        y += hh + len(rows) * rh
        if notes:
            for c, s in notes.items():
                j = cols.index(c)
                k = strike_kind if c in struck else keep_kind
                D.text(24 + j * cw + cw / 2, y + 18, s, "label", 12.5, D.kinds[k][1], "middle")
            y += 24
        return y

    def nest(D, y, layers, side=None, inset=22):
        """Concentric rounded rects, outermost first: layers = [(title, sub, kind)], each title top-left.
        side: an optional cell drawn as a column on the right with a dashed edge into the innermost rect.
        Returns the bottom y."""
        f = D.f
        n = len(layers)
        right = W - 24 - (214 if side else 0)
        geo, ty = [], y
        for i, (t, sub, k) in enumerate(layers):
            l, r = 24 + inset * i, right - inset * i
            sl = f.wrap("body", sub, 13, r - l - 28) if sub else []
            band = 14 + 16 + len(sl) * 16 + 12
            geo.append((l, r, ty, sl, t, k)); ty += band
        inner_b = ty
        for i, (l, r, top, sl, t, k) in enumerate(geo):
            fill, stroke, ink, ink2 = D.kinds[k or "neutral"]
            bot = inner_b + 14 * (n - 1 - i)
            D.front.append(f'<rect x="{l:.1f}" y="{top:.1f}" width="{r - l:.1f}" height="{bot - top:.1f}" rx="12" '
                           f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            D.text(l + 14, top + 26, t, "title", 16, ink)
            for j, ln in enumerate(sl):
                D.text(l + 14, top + 44 + j * 16, ln, "body", 13, ink2)
        y = inner_b + 14 * (n - 1)
        if side:
            l, r, top, *_ = geo[-1]
            cy = (top + inner_b) / 2
            t, b, k, s = cell(side)
            sw = 180
            sb = D.box(W - 24 - sw / 2, cy, sw, t, b, kind=k, sub=s)
            D.edge([(sb["l"], cy), (r, cy)], dashed=True)
            D.front.append(D.back.pop())  # over the outer layers' fills, not under them
            y = max(y, sb["b"])
        return y

    # ================================================================== D1 (prompting)
    def t1_1(f):
        D, y = new(f, "Vague Prompt, Strong Brief",
                   "Same request; the strong one marks each part Claude can't guess.",
                   "A vague one-line request compared with a strong brief whose lines are marked goal, context, "
                   "audience, format and example; for technical tasks the brief adds the columns, a sample row, the "
                   "rule and the exact error text.")
        y = snippet(D, 24, y, W - 48, "Vague", ["Write something about our loyalty scheme."], "risk",
                    marks=[(0, "Write something about our loyalty scheme.", "risk", "no goal, reader, format or facts")])
        y = snippet(D, 24, y + 14, W - 48, "Strong brief", [
            "Goal: a newsletter section that gets members to use points before 31 March.",
            "Context: points expire 31 March; 2,000-point minimum; three new partner cafés.",
            "Audience: existing members, not new sign-ups.",
            "Format: 120 words, one heading, one call to action.",
            "Example: <example>last spring's section</example>",
        ], "focus", marks=[(0, "Goal:", "data", "G"), (1, "Context:", "data", "C"), (2, "Audience:", "data", "A"),
                           (3, "Format:", "data", "F"), (4, "Example:", "data", "E")])
        y = lanes(D, y + 22, [("Technical tasks too", [("Formula or error", "Columns, one sample row, the rule, the exact #VALUE! text", "data")], "apart")])
        return finish(D, y, [("risk", "vague"), ("focus", "recommended brief"), ("data", "prompt part")])

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
                   "Specific feedback improves the draft; test on several inputs before you reuse it.",
                   "The iteration loop: write a prompt, read the output against your goal, give specific keep-and-change "
                   "feedback, and before reusing the prompt test it on several different inputs and save it as a template; "
                   "'make it better' and 'try again' are not feedback.")
        y = lanes(D, y, [
            (None, [("Prompt", None, "data"), ("Read output", "Against the goal"), ("Specific feedback", "Keep this, change that", "focus"),
                    ("Better draft", None, "good")], True),
            ("Reusing it?", [("Test on 3+ inputs", "Same checklist", "data"), ("Save as a template", None, "good")], True),
            ("Not feedback", [("\"Make it better\"", None, "risk"), ("\"Try again\"", None, "risk")], "apart"),
        ])
        return finish(D, y, [("data", "input"), ("focus", "recommended move"), ("good", "improvement"), ("risk", "vague")])

    def t1_4(f):
        D, y = new(f, "Four Prompts, Four Shapes",
                   "Name the task type, then give it what it needs.",
                   "Four real prompts side by side: an analysis prompt that uses only the attached data and separates "
                   "observations from explanations, a research prompt that asks for linked sources, a drafting prompt that "
                   "sets length, tone and next step, and a brainstorming prompt that asks for twenty varied ideas without "
                   "judging them.")
        a = "Using only the attached applications data, give the top 3 funding gaps with counts. Keep observations apart from explanations."
        r = "What have three national funders published on youth grants since 2025? Link each source."
        d = "Write a 150-word decision letter to an applicant: warm, plain, one clear next step."
        b = "Give 20 fundraising-event ideas across four styles. Don't judge them yet."
        y, _ = snip_row(D, y, [
            dict(heading="Analysis", lines=[a], kind="focus", marks=[(0, "Using only the attached", "good", None)]),
            dict(heading="Research", lines=[r], kind="data", marks=[(0, "Link each source", "good", None)]),
        ], gap=24)
        y, _ = snip_row(D, y + 16, [
            dict(heading="Drafting", lines=[d], kind="data", marks=[(0, "150-word", "good", None), (0, "warm, plain", "good", None)]),
            dict(heading="Brainstorming", lines=[b], kind="data", marks=[(0, "20", "good", None), (0, "Don't judge them yet", "good", None)]),
        ], gap=24)
        return finish(D, y, [("focus", "anchored to your data"), ("data", "task type"), ("good", "what makes it work")])

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
        D, y = new(f, "Spot the Red Flags",
                   "Specific-looking details are where errors hide.",
                   "A mock Claude-drafted article with its red flags marked: an unsupplied statistic and an unsourced quote "
                   "as possible hallucinations, two launch dates that disagree as an inconsistency, and wording that assumes "
                   "engineers are men as bias; asking Claude how confident it is does not count as a check.")
        lines = ["The Safe Hands programme cut site incidents by 37% in its first year.",
                 "\"Safety is our first value,\" said the chief executive at the launch.",
                 "Training starts on 4 March for all engineers and their wives' support network.",
                 "From 11 March, every site will run the new checks."]
        y = snippet(D, 24, y, W - 48, "Claude's draft (intranet article)", lines, "neutral", tags="below", marks=[
            (0, "37%", "warn", "statistic nobody supplied: trace it"),
            (1, "\"Safety is our first value,\"", "warn", "quote not in the notes: check"),
            (2, "4 March", "risk", "dates disagree: reconcile"),
            (2, "engineers and their wives'", "risk", "assumes engineers are men: reword"),
            (3, "11 March", "risk", None),
        ])
        y = lanes(D, y + 22, [("Then", [("Check each flag against the source", None, "focus")], "apart"),
                              ("Not a check", [("Ask Claude how confident it is", None, "risk")], "apart")])
        return finish(D, y, [("warn", "possible hallucination"), ("risk", "inconsistency, bias, false check"),
                             ("focus", "recommended check")])

    def t2_3(f):
        D, y = new(f, "Checking a Claim",
                   "Open the source; asking Claude if it's sure isn't a check.",
                   "The fact-checking path: a claim is matched to a quoted passage or cited source, the source is opened "
                   "and checked for the same date, units, region and currency, and the claim is kept, corrected or removed; "
                   "asking Claude whether it is sure, or asking again, is not a check.")
        y = lanes(D, y, [
            (None, [("Claim", None, "data"), ("Quote or citation", "Ask Claude for it"),
                    ("Open the source", "Same date, units, region, currency?", "focus")], True),
            ("Then", [("Matches: keep", None, "good"), ("Differs: correct", None, "warn"), ("No support: remove", None, "risk")], "apart"),
            ("Not a check", [("\"Are you sure?\"", "Self-rated confidence", "risk"), ("Ask the same question again", None, "risk")], "apart"),
        ])
        return finish(D, y, [("data", "claim"), ("focus", "recommended check"), ("good", "keep"), ("warn", "fix"), ("risk", "drop / false check")])

    def t2_4(f):
        D, y = new(f, "Review Grows With the Stakes",
                   "The more that rides on it, the more qualified the reviewer.",
                   "A review ladder that rises with the stakes: your own read for personal notes, a quick author check for "
                   "internal updates, a sample review for routine high-volume replies, and full review by a qualified person "
                   "for decisions about money, health, legal rights or jobs, who must have authority to change it and must "
                   "tell the person AI was involved; disclaimers, spelling checks and Claude's own uncertainty flags are not review.")
        cue(D, 24, y, "Stakes and audience rise", "down")
        y = stack(D, y + 14, [
            ("Your own read", "Notes and ideas for yourself", "data"),
            ("Author's quick check", "Internal team update"),
            ("Sample review", "Hundreds of routine customer replies"),
            ("Full review by a qualified person", "Claim-decline letter; health, legal or money content", "focus"),
        ], arrows="down")
        y = lanes(D, y + 8, [
            ("High-risk uses also need", [("Authority to change it", None, "good"), ("Tell the person AI was involved", None, "good")], "apart"),
            ("Not review", [("A disclaimer", None, "warn"), ("A spelling check", None, "warn"),
                            ("Only items Claude marks uncertain", None, "warn")], "apart"),
        ], gap=16)
        return finish(D, y, [("data", "input"), ("focus", "recommended for high stakes"), ("good", "required"), ("warn", "false check")])

    def t2_5(f):
        D, y = new(f, "Same Fact, Three Readers",
                   "Change the words and length; never the figure.",
                   "One checked survey figure rewritten for three readers: a trustee summary with the decision needed, a "
                   "volunteer briefing in plain words, and a leaflet line for members, each stating the same figure in "
                   "different language and length.")
        h = need(D, W - 48, "The checked fact", "62% of members over 75 feel lonely at least weekly (survey of 1,240)")
        src = D.box(W / 2, y + h / 2, W - 48, "The checked fact",
                    "62% of members over 75 feel lonely at least weekly (survey of 1,240)", kind="data", h=h)
        y, pos = snip_row(D, y + h + 40, [
            dict(heading="Trustees", kind="focus", lines=["62% of members over 75 report weekly loneliness (n=1,240). "
                                                          "Decision: fund the phone-friend scheme for 12 months?"]),
            dict(heading="Volunteers", lines=["About six in ten members over 75 feel lonely most weeks. Your weekly call matters."]),
            dict(heading="Leaflet", lines=["Feeling lonely? Six in ten members over 75 feel the same. Ask us about a weekly friendly call."]),
        ])
        fan(D, src, [(cx, t) for cx, t, _ in pos])
        bt = "Same figure in every version; you edit and own each one"
        bh = need(D, W - 48, bt)
        y += 40
        z = D.box(W / 2, y + bh / 2, W - 48, bt, kind="good", h=bh)
        gather(D, [(cx, b) for cx, _, b in pos], z)
        return finish(D, y + bh, [("data", "source fact"), ("focus", "audience with a decision to make"), ("good", "your check")])

    def t2_6(f):
        D, y = new(f, "Curate, Then Pick the Format",
                   "Organise the material first; the next step decides the format.",
                   "Messy sign-up emails are first grouped, ordered and de-duplicated, then the same information is shown "
                   "three ways: a one-line inline answer to read once, a rota artifact the team keeps editing, and CSV rows "
                   "for the volunteer system.")
        y = lanes(D, y, [(None, [("140 sign-up emails", "Messy, repeated, unordered", "data"),
                                 ("Grouped and ordered", "By role, then availability; duplicates merged; gaps flagged", "focus")], True)])
        src = D.last_row[1]
        y, pos = snip_row(D, y + 30, [
            dict(heading="Inline (read once)", lines=["Saturday is covered: 46 stewards. Sunday is 6 short."]),
            dict(heading="Artifact (team edits)", kind="good", lines=["Shift rota", "Sat 10–2", "Gate A: Priya, Tom, Ana", "Gate B: …"]),
            dict(heading="CSV (into the volunteer system)", kind="good", mono=True,
                 lines=["name,role,day,start", "Priya Shah,steward,Sat,10:00", "Tom Reid,steward,Sat,10:00"]),
        ], widths=[190, 196, 214])
        fan(D, src, [(cx, t) for cx, t, _ in pos])
        return finish(D, y, [("data", "input"), ("focus", "recommended first step"), ("good", "format for the next step")])

    # ================================================================== D3 (product and model selection)
    def t3_1(f):
        D, y = new(f, "Lightest Feature That Fits",
                   "Answer each question; stop at the first yes.",
                   "A decision path for choosing a feature: recurring files and rules lead to a Project, an answer spread "
                   "across many sources to Research, numbers to calculate from a file to code execution, something to keep "
                   "or share to an artifact, and otherwise a plain chat with web search; a procedure repeated the same way "
                   "is a skill.")
        y = decide(D, y, [
            ("Same files and rules again and again?", ("Project", "Instructions + knowledge for every chat", "good")),
            ("Answer spread across many sources?", ("Research", "Paid plans; web search on; uses limits faster", "good")),
            ("Numbers to calculate or chart from a file?", ("Code execution", "Setting must be on", "good")),
            ("Will you keep, edit or share it?", ("Artifact", "Setting must be on", "good")),
        ], ("Chat", "Add web search for current facts", "focus"), yes_right=True)
        y = lanes(D, y + 24, [(None, [("Same procedure every time, in any chat?", "A skill", "data")], "apart")])
        return finish(D, y, [("good", "heavier feature"), ("focus", "recommended default"),
                             ("data", "procedure"), ("solid", "yes"), ("dashed", "no")])

    def t3_2(f):
        D, y = new(f, "Three Families, by Job",
                   "Judge the task first; versions change, families don't.",
                   "Judge the task first, then pick a family: Haiku for high-volume simple tasks, Sonnet for most everyday "
                   "writing and analysis, and Opus for the hardest multi-step reasoning as the most capable of the three; the "
                   "model menu also lists other models such as Fable, which sits above Opus.")
        y = stack(D, y, [("Judge the task", "Many steps, conflicting information or judgement: heavier. "
                                            "Simple, repeatable, high volume: lighter.", "focus")])
        y += 16
        lt, rt = "FASTER, LOWER COST", "MORE CAPABLE, SLOWER"
        caption(D, 24, y, lt); caption(D, W - 24, y, rt, "end")
        x0, x1 = 24 + cap_w(D, lt) + 14, W - 24 - cap_w(D, rt) - 14
        mid = (x0 + x1) / 2
        D.edge([(mid, y - 4), (x0, y - 4)]); D.edge([(mid, y - 4), (x1, y - 4)])
        y = lanes(D, y + 14, [(None, [
            ("Haiku", "High-volume, simple tasks: tagging, pulling out fields", "data"),
            ("Sonnet", "Most everyday writing and analysis", "data"),
            ("Opus", "Hardest multi-step reasoning; most capable of the three", "data")], "apart")], gap=16)
        y = stack(D, y + 4, [("Also in the menu", "Other models, such as Fable, above Opus for the most demanding work")])
        return finish(D, y - 10, [("focus", "start here"), ("data", "family"), ("neutral", "other models")])

    def t3_3(f):
        D, y = new(f, "Start Light, Step Up on Evidence",
                   "Sample first; pull one lever at a time.",
                   "A step-up path: run a sample on the lightest option at default effort, keep it if quality is good "
                   "enough, raise effort if answers are right but shallow on the hard steps, and step up the model family "
                   "only if that still falls short, remembering that volume multiplies every choice.")
        th = need(D, W - 48, "Run a sample on the lightest option", "20–25 real items, default effort")
        top = D.box(W / 2, y + th / 2, W - 48, "Run a sample on the lightest option", "20–25 real items, default effort",
                    kind="focus", h=th)
        y = decide(D, y + th + 30, [
            ("Good enough?", ("Keep it as the task's default", None, "good")),
            ("Right, but shallow on hard steps?", ("Raise effort", "Low, Medium, High, then Max", "warn")),
        ], ("Step up the model family", "Slower and costlier on every run", "warn"), yes_right=True, src=(150, top["b"]))
        e = D.last_end
        cl = cap_wrap(D, "Climb only if the lower step doesn't fix it", W - 24 - D.fix_left)
        for i, ln in enumerate(cl):
            D.text(D.fix_left, e["cy"] - (len(cl) - 1) * 8 + 4 + i * 16, ln, "title", 12.5, SLATE4, track=0.1)
        y = stack(D, y + 22, [("Volume multiplies every choice", "4,000 blurbs × a heavy setting = hours and a big share of your limit")])
        return finish(D, y - 10, [("focus", "recommended start"), ("good", "keep"), ("warn", "lever: costs time and usage"),
                                  ("solid", "yes"), ("dashed", "no")])

    def t3_4(f):
        D, y = new(f, "Restart, Summarise or Persist",
                   "Chats are temporary; save what you'll need again.",
                   "A chat timeline: decisions made early get mixed up a hundred messages later, so you ask for a summary "
                   "and start a new chat from it, and save anything every chat needs to Project knowledge; for one sensitive "
                   "chat, use incognito outside a Project or turn memory off inside one.")
        y = lanes(D, y, [
            ("Restart", [("Messages 1–40", "Venue and dates agreed", "data"), ("Message 120", "Venues mixed up", "warn"),
                         ("Ask for a summary", "Decisions, facts, open items", "focus"), ("New chat", "Starts from the summary", "good")], True),
            ("Persist", [("Needed in every chat", None, "data"), ("Project knowledge or instructions", None, "good")], True),
            ("One sensitive chat", [("Outside a Project: incognito", "Not in history or memory; kept 30 days"),
                                    ("Inside a Project: memory off", "Set before the first message")], "apart"),
        ], gap=24)
        return finish(D, y, [("data", "input"), ("warn", "symptom"), ("focus", "recommended move"), ("good", "result")])

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
        D, y = new(f, "Map the Process as It Really Runs",
                   "The bottleneck is usually a step nobody wrote down.",
                   "A real appointment-reminder process mapped step by step shows the same client details typed into three "
                   "systems; after mapping, one entry feeds the reminders and texts, while research and planning are checked "
                   "by opening sources and testing the plan with the team.")
        y = lanes(D, y, [
            ("As it runs", [("Client books", None, "data"), ("Typed into booking system",),
                            ("Typed again into reminder tool", None, "warn"), ("Typed again into SMS sheet", None, "warn")], False),
            ("After mapping", [("One entry", None, "focus"), ("Reminders and SMS from it", None, "good")], True),
            ("Also in this lesson", [("Research", "Open the sources key facts rest on", "data"),
                                     ("Plan", "Steps, owners, risks; the team tests it", "data")], "apart"),
        ], gap=24)
        return finish(D, y, [("data", "input"), ("warn", "duplicated step"), ("focus", "recommended redesign"), ("good", "result")])

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
        return finish(D, y, [("good", "value"), ("warn", "limits"), ("data", "safeguards"), ("focus", "recommendation"), ("risk", "hype")])

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
                   "An uploaded file is a snapshot that goes stale when the source changes, so replace it by removing the old "
                   "file first; information that changes often comes through a connector or a synced Google Doc in a private "
                   "Project, and connectors reach only what your account can open, ask before sending or deleting by default "
                   "and store retrieved data with the chat.")
        y = lanes(D, y, [("An upload is a snapshot", [("Mon: deposit rules uploaded", None, "data"),
                                                      ("Wed: rules change at the source", None, "warn"),
                                                      ("Claude still quotes Monday's copy", None, "risk")], False)], gap=24)
        y = pairs(D, y + 6, [
            (("Policy, brand guide, template", "Changes rarely", "data"), ("Upload to knowledge", "Remove the old file before adding the new"), None),
            (("Inbox, calendar, live sheets", "Changes daily", "data"),
             ("Connector, or a synced Google Doc", "Synced Docs: private Projects only", "focus"), None),
        ], heads=("Information", "Use"))
        y = lanes(D, y + 6, [("Connector rules", [("Only what your account can open", None, "good"),
                                                  ("Asks before send or delete, by default", None, "good"),
                                                  ("Stored with the chat", None, "neutral")], "apart")], gap=14)
        return finish(D, y, [("data", "information"), ("warn", "source changed"), ("risk", "stale answer"),
                             ("focus", "recommended for live data"), ("good", "safeguard")])

    def t5_3(f):
        D, y = new(f, "Where Each Rule Lives",
                   "Broader layers apply everywhere; skills join only when the task needs them.",
                   "Nested scopes: account instructions wrap every chat, Project instructions and knowledge wrap the chats in "
                   "one Project, and skills plug in from the side only when a task calls for them; a client rule at account "
                   "level leaks everywhere, and contradictory layers cause inconsistent output.")
        y = nest(D, y, [
            ("Account instructions", "Every chat: British spelling, answer first", "data"),
            ("Project instructions + knowledge", "Chats in this Project: naming rules, warnings format", "focus"),
            ("This chat", "Your request", "neutral"),
        ], side=("Skills", "Load when the task calls for them, in any chat; need code execution", "good"))
        y = lanes(D, y + 26, [("Avoid", [("Client rule at account level", "Leaks into every chat", "risk"),
                                         ("Two layers that contradict", None, "warn")], "apart")])
        return finish(D, y, [("data", "applies everywhere"), ("focus", "most task rules belong here"), ("good", "on demand"),
                             ("risk", "wrong level"), ("warn", "conflict")])

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
                   "Three zones of use: green for drafting, summarising and research with a human owner; amber for anything "
                   "affecting health, money, legal rights, livelihood, housing or education, which needs a qualified person "
                   "with authority to change the outcome and disclosure to the person affected; red for prohibited uses; a "
                   "decision wholly in the person's favour may not need review first where the law allows.")
        y = lanes(D, y, [(None, [
            ("Green: go", "Drafting, summaries, research; a person reviews", "good"),
            ("Amber: human in the loop", "Health, money, rights, livelihood, housing, education: a qualified person with "
                                         "authority, plus disclosure", "warn"),
            ("Red: stop", "Prohibited by the Usage Policy or company policy", "risk")], "apart")], gap=14)
        y = lanes(D, y, [(None, [("Exception", "A decision wholly in the person's favour, such as paying a claim, may not "
                                               "need review first, where the law allows")], "apart")])
        y = stack(D, y + 6, [("Fix for amber", "A qualified person makes the decision, not a better prompt", "focus")])
        return finish(D, y - 10, [("good", "appropriate"), ("warn", "controls needed"), ("risk", "not allowed"), ("focus", "the fix")])

    def t6_2(f):
        D, y = new(f, "Strike Out What the Task Doesn't Need",
                   "Decide before you upload; afterwards is too late.",
                   "A membership spreadsheet with the name, email, date of birth and health columns struck out and a "
                   "non-identifying member key kept alongside club, month and type; before uploading, identify the data, "
                   "check the rules and plan, and keep only what the task needs, because asking Claude to forget it or using "
                   "incognito afterwards is not a control.")
        cols = ["Name", "Email", "Date of birth", "Health answers", "Member key", "Club", "Month", "Type"]
        y = sheet(D, y, cols, [
            ["A. Khan", "a.k@…", "03/04/1990", "Asthma", "M-0417", "Leeds", "Mar", "Off-peak"],
            ["J. Ortiz", "j.o@…", "21/11/1985", "None", "M-0932", "York", "Mar", "Full"],
        ], struck=("Name", "Email", "Date of birth", "Health answers"), notes={"Member key": "non-identifying key"})
        y = lanes(D, y + 22, [
            (None, [("What kind of data?", "Personal, health, financial?", "data"), ("Which rules and plan?", "Policy, approved workspace"),
                    ("Keep only what's needed", None, "focus")], True),
            ("Not controls", [("Upload, then 'forget this'", None, "risk"), ("Use incognito instead", "Still kept 30 days", "risk")], "apart"),
        ])
        return finish(D, y, [("data", "input"), ("focus", "recommended move"), ("good", "kept"), ("risk", "removed / not a control")])

    def t6_3(f):
        D, y = new(f, "When the Policy Doesn't Say",
                   "Silence isn't permission.",
                   "A decision path for policy questions: if the policy covers the tool, data and use, follow it in the "
                   "approved workspace; if a setting or connector blocks legitimate work, request it through the proper route; "
                   "otherwise ask the policy owner before acting, never using a personal or colleague's account or asking "
                   "Claude to interpret the policy.")
        y = decide(D, y, [
            ("Does the policy cover this tool, data and use?", ("Follow it, in the approved workspace", None, "good")),
            ("Is a setting or connector blocking legitimate work?",
             ("Request it through the proper route", "e.g. 'Request' on the connector's page", "good")),
        ], ("Ask the policy owner before acting", None, "focus"), yes_right=True)
        y = lanes(D, y + 24, [("Not routes", [("Personal account", None, "risk"), ("A colleague's account", None, "risk"),
                                              ("Asking Claude what the policy allows", None, "risk")], "apart")], gap=16)
        return finish(D, y, [("good", "covered route"), ("focus", "recommended when unsure"), ("risk", "never a route"),
                             ("solid", "yes"), ("dashed", "no")])

    def t6_4(f):
        D, y = new(f, "Who Answers for It",
                   "Whoever sends it owns it.",
                   "The accountability chain: Claude drafts, you check fairness, disclose AI's role and edit, the work goes "
                   "out under your name, and if it is wrong you and your organisation answer for it; saying the AI wrote it "
                   "does not move responsibility.")
        y = lanes(D, y, [
            (None, [("Claude drafts", None, "neutral"), ("You check fairness, disclose, edit", None, "focus"),
                    ("Sent under your name", None, "data"), ("If it's wrong, you and your organisation answer", None, "good")], True),
            ("Doesn't move responsibility", [("\"The AI wrote that part\"", None, "risk")], "apart"),
            ("What you check", [("Transparency", "Say when AI shaped it"), ("Fairness", "Compare how groups are described"),
                                ("Respect", "Privacy and others' work")], "apart"),
        ], gap=24)
        return finish(D, y, [("focus", "recommended: your check"), ("data", "goes out"), ("good", "accountability"),
                             ("risk", "not an excuse")])

    # ================================================================== D7 (troubleshooting)
    def t7_1(f):
        D, y = new(f, "Diagnose Before You Fix",
                   "Answer in order; fix the first 'no', then retest.",
                   "A yes/no diagnosis path: check that the context is present, that facts come from one current source, that "
                   "the instruction is specific and not contradicted, and that the chat is still short, fixing the first 'no' "
                   "found; only then raise effort or step up the model, changing one thing and retesting with the same input.")
        y = decide(D, y, [
            ("Is the needed context in this chat or Project?", ("Add goal, audience, context", "See 1.1", "good")),
            ("Are the facts from one current source?", ("Replace the stale or duplicate file", "See 5.4", "good")),
            ("Is the instruction specific, at one level?", ("Rewrite it; remove the conflict", "See 5.3", "good")),
            ("Is the chat still short?", ("Summarise and restart", "See 3.4", "good")),
        ], ("Still shallow? Raise effort or step up the model", "See 3.3", "neutral"))
        y = stack(D, y + 22, [("Change one thing, retest with the same input", None, "focus")])
        return finish(D, y - 10, [("good", "fix for that cause"), ("focus", "recommended method"), ("neutral", "last resort"),
                                  ("solid", "yes"), ("dashed", "no")])

    def t7_2(f):
        D, y = new(f, "The Adjustment Ladder",
                   "Start at the bottom; climb only when the step below doesn't stop the problem.",
                   "An adjustment ladder taken one step at a time, moving on only if the earlier step doesn't stop the "
                   "problem: fix a one-off in the chat, update the template, instructions or knowledge for a recurring issue, "
                   "change the model, effort or feature if quality still falls short, and escalate to Architects or Developers "
                   "when configuration can't solve it; or remove Claude from a step the results show it makes worse.")
        y = stack(D, y, [
            ("Escalate to Architects or Developers", "Needs an integration or custom build", "good"),
            ("Change the model, effort or feature", "Quality still falls short"),
            ("Update the template, instructions or knowledge", "The same issue recurs", "focus"),
            ("Fix it in the chat", "Happened once", "data"),
        ], arrows="up")
        y -= 30
        cue(D, 24, y + 22, "Start here, climb only if the lower step doesn't stop it", "up")
        y = lanes(D, y + 66, [("Or, on evidence", [("Remove or narrow Claude's role", "When results show the step is slower or worse", "warn")], "apart")])
        return finish(D, y, [("data", "start here"), ("focus", "recurring"), ("good", "beyond configuration"), ("warn", "remove on evidence")])

    def t7_3(f):
        D, y = new(f, "Same Quality, Less Effort",
                   "Remove repeated work, then check quality held.",
                   "Before and after: fifteen messages a day that re-paste the same policy become a cached Project, batched "
                   "questions, a lighter model for summaries and a weekly quality sample; if quality holds the change stays, "
                   "and faster but worse is not an optimisation.")
        y = lanes(D, y, [
            ("Before", [("15 messages a day", "Policy re-pasted each time", "warn"), ("Slow answers, heavy usage", None, "risk")], False),
            ("After", [("Policy in a Project", "Cached when reused", "data"), ("Questions batched per traveller",),
                       ("Lighter model for summaries",), ("Weekly quality sample", None, "focus")], True),
            ("Then", [("Quality held: keep it", None, "good"), ("Faster but worse: not an optimisation", None, "warn")], "apart"),
        ], gap=24)
        return finish(D, y, [("warn", "symptom or false gain"), ("risk", "cost of repetition"), ("data", "input"),
                             ("focus", "recommended check"), ("good", "keep")])

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
