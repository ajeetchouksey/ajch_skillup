#!/usr/bin/env python3
"""
Embeds subset Barlow (WOFF2, base64) into rendered SVG diagrams.

  python scripts/embed-svg-fonts.py --fonts <dir> <svg>...
  python scripts/embed-svg-fonts.py --fonts <dir> --list .mermaid-svg-written.txt

Notes load diagrams through <img>, which can't see the page's web fonts, so
each SVG carries just the glyphs it uses (same approach as
build-svg-diagrams.py). <dir> needs Barlow-Regular.ttf and Barlow-Medium.ttf.
Requires: pip install fonttools brotli
"""
import argparse, base64, html, io, os, re
from fontTools import subset
from fontTools.ttLib import TTFont

MARK = "<!-- aarya-fonts -->"


def woff2(path, chars):
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def embed(svg_path, fonts):
    svg = open(svg_path, encoding="utf-8").read()
    if MARK in svg:
        svg = re.sub(re.escape(MARK) + r"<style>.*?</style>", "", svg, flags=re.S)
    chars = "".join(html.unescape(t) for t in re.findall(r">([^<>]+)<", svg)) + " .,:-0123456789"
    style = (
        "<style>"
        f"@font-face{{font-family:Barlow;font-weight:100 450;src:url(data:font/woff2;base64,{woff2(os.path.join(fonts, 'Barlow-Regular.ttf'), chars)}) format('woff2')}}"
        f"@font-face{{font-family:Barlow;font-weight:451 900;src:url(data:font/woff2;base64,{woff2(os.path.join(fonts, 'Barlow-Medium.ttf'), chars)}) format('woff2')}}"
        "</style>"
    )
    svg = re.sub(r"(<svg[^>]*>)", lambda m: m.group(1) + MARK + style, svg, count=1)
    open(svg_path, "w", encoding="utf-8", newline="\n").write(svg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--list")
    ap.add_argument("svgs", nargs="*")
    a = ap.parse_args()
    paths = list(a.svgs)
    if a.list:
        paths += [p for p in open(a.list, encoding="utf-8").read().splitlines() if p.strip()]
    for p in paths:
        embed(p, a.fonts)
    print(f"embedded fonts in {len(paths)} svg(s)")


if __name__ == "__main__":
    main()
