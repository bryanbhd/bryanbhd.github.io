#!/usr/bin/env python3
"""Render portfolio.md to index.html for GitHub Pages.

    ./build_site.py          # portfolio.md -> index.html

Uses the markdown package from the md2pdf venv in Enterprise-Sandbox/documents.
"""
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bryan Debnam — Systems Architect / AI Platform Engineer</title>
<meta name="description" content="Portfolio: AI governance and MLOps lifecycle, agentic AI platforms, AI security triage, and enterprise infrastructure architecture.">
<link rel="canonical" href="https://bryandebnam.com/">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Bryan Debnam">
<meta property="og:title" content="Bryan Debnam — Systems Architect / AI Platform Engineer">
<meta property="og:description" content="AI governance and MLOps lifecycle, agentic AI platforms, AI security triage, and enterprise infrastructure architecture.">
<meta property="og:url" content="https://bryandebnam.com/">
<meta name="twitter:card" content="summary">
<style>
:root {
  --bg: #ffffff; --fg: #1b1f24; --muted: #5b6570; --accent: #1f4e9c;
  --rule: #d8dee6; --card: #f6f8fa; --code-bg: #eef1f5;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1319; --fg: #e6e9ee; --muted: #9aa5b1; --accent: #7aa7ee;
    --rule: #263040; --card: #161c25; --code-bg: #1b222c;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.62 -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}
.wrap { max-width: 860px; margin: 0 auto; padding: 48px 22px 80px; }
h1 { font-size: 2.1rem; line-height: 1.15; margin: 0 0 6px; letter-spacing: -0.4px; }
h1 + p { color: var(--muted); margin: 0 0 6px; font-size: 1.05rem; }
h2 {
  font-size: 1.32rem; margin: 44px 0 14px; padding-bottom: 7px;
  border-bottom: 2px solid var(--accent); color: var(--accent);
}
h3 { font-size: 1.06rem; margin: 28px 0 8px; }
p, li { margin: 8px 0; }
ul { padding-left: 22px; }
a { color: var(--accent); }
hr { border: 0; border-top: 1px solid var(--rule); margin: 34px 0; }
strong { color: var(--fg); }
em { color: var(--muted); }
code {
  background: var(--code-bg); padding: 1px 5px; border-radius: 3px;
  font: 0.88em/1.4 "SF Mono", Consolas, monospace;
}
.tablewrap { overflow-x: auto; margin: 16px 0; }
table { border-collapse: collapse; width: 100%; font-size: 0.9rem; min-width: 620px; }
th, td { border: 1px solid var(--rule); padding: 8px 10px; text-align: left; vertical-align: top; }
th { background: var(--card); }
h3 + p + ul, h3 + ul { margin-top: 6px; }
footer { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--rule);
         color: var(--muted); font-size: 0.85rem; }
@media (max-width: 600px) {
  .wrap { padding: 30px 16px 60px; }
  h1 { font-size: 1.7rem; }
}
</style>
</head>
<body>
<div class="wrap">
"""

FOOT = """
<footer>Built from <code>portfolio.md</code>. Updated {date}.</footer>
</div>
</body>
</html>
"""


def main():
    src = HERE / "portfolio.md"
    body = markdown.markdown(
        src.read_text(),
        extensions=["tables", "fenced_code", "attr_list", "sane_lists", "smarty"],
    )
    # let wide skills table scroll on phones instead of blowing out the layout
    body = re.sub(r"<table>", '<div class="tablewrap"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)

    from datetime import date
    html = HEAD + body + FOOT.format(date=date.today().isoformat())
    (HERE / "index.html").write_text(html)
    print(f"[site] wrote {HERE / 'index.html'} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
