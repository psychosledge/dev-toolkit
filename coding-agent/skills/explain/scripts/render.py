#!/usr/bin/env python3
"""Render an explanation spec (JSON) into a single self-contained HTML file.

Derived from the explain-diff gists by Geoffrey Litt and ankitg12 (gist
8e808d387799de4e9839bc393f8e6405).

Spec schema:
  title     (required) page title, plain text
  subtitle  (optional) muted line under the title, plain text
  slug      (optional) filename slug; defaults to a slugified title
  sections  (required) list of {id, heading, html}
            heading is plain text; html is raw markup inserted unescaped
            html may wrap a term in
              <dfn class="term" data-def="one plain-text sentence">term</dfn>
            and the page shows data-def as a hover/tap tooltip
  quiz      (optional) list of {question, options}
            question is plain text
            options is a list of {text, correct, feedback}:
              text     plain text, no markup
              correct  boolean; exactly one true per question
              feedback plain text shown when the option is clicked,
                       explaining why it is right or wrong

Option order is shuffled at render time, so write options in any order and
never try to vary positions by hand.

Usage:
  render.py spec.json --out-dir DIR     -> DIR/YYYY-MM-DD-<slug>.html
  render.py spec.json -o path.html      -> exact path
The final path is printed to stdout.
"""

import argparse
import datetime
import html
import json
import random
import re
import sys
from pathlib import Path


def fail(msg):
    print(f"render.py: {msg}", file=sys.stderr)
    sys.exit(1)


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "explanation"


def validate(spec):
    if not isinstance(spec, dict):
        fail("spec must be a JSON object")
    if not spec.get("title"):
        fail("spec.title is required")
    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        fail("spec.sections must be a non-empty list")
    for i, s in enumerate(sections):
        for key in ("id", "heading", "html"):
            if not s.get(key):
                fail(f"sections[{i}].{key} is required")
        if not re.fullmatch(r"[a-z0-9-]+", s["id"]):
            fail(f"sections[{i}].id must be lowercase letters, digits, hyphens")
    quiz = spec.get("quiz", [])
    if not isinstance(quiz, list):
        fail("spec.quiz must be a list")
    for i, q in enumerate(quiz):
        if not q.get("question"):
            fail(f"quiz[{i}].question is required")
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) < 2:
            fail(f"quiz[{i}].options needs at least 2 options")
        correct = [o for o in opts if o.get("correct")]
        if len(correct) != 1:
            fail(f"quiz[{i}] must have exactly one correct option, found {len(correct)}")
        for j, o in enumerate(opts):
            if not o.get("text"):
                fail(f"quiz[{i}].options[{j}].text is required")
            if not o.get("feedback"):
                fail(f"quiz[{i}].options[{j}].feedback is required")
    check_length_bias(quiz)


def check_length_bias(quiz):
    """Warn when correct answers are recognizable by length alone."""
    if not quiz:
        return
    longest_correct = 0
    for q in quiz:
        lengths = [(len(o["text"]), bool(o.get("correct"))) for o in q["options"]]
        max_len = max(l for l, _ in lengths)
        if any(c and l == max_len for l, c in lengths):
            longest_correct += 1
    if longest_correct > len(quiz) / 2:
        print(
            f"render.py: WARNING: the correct option is the longest in "
            f"{longest_correct}/{len(quiz)} questions. Rewrite options so "
            f"distractors match the correct answer's length and specificity, "
            f"then re-render.",
            file=sys.stderr,
        )


CSS = """
:root {
  --bg: #ffffff; --fg: #1a1a2e; --muted: #6b7280; --accent: #2563eb;
  --border: #e5e7eb; --code-bg: #f6f8fa; --callout-bg: #eff6ff;
  --ok: #16a34a; --ok-bg: #f0fdf4; --bad: #dc2626; --bad-bg: #fef2f2;
  --box-bg: #f9fafb;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111317; --fg: #e5e7eb; --muted: #9ca3af; --accent: #60a5fa;
    --border: #2d3139; --code-bg: #1b1f27; --callout-bg: #172036;
    --ok: #4ade80; --ok-bg: #122117; --bad: #f87171; --bad-bg: #2a1515;
    --box-bg: #181c23;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 17px/1.65 Georgia, 'Times New Roman', serif;
}
main { max-width: 840px; margin: 0 auto; padding: 40px 16px 80px; }
h1 { font-size: 1.9em; line-height: 1.25; margin: 0 0 6px; }
h2 {
  font-size: 1.4em; margin: 2.2em 0 0.6em; padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}
h3 { font-size: 1.12em; margin: 1.6em 0 0.5em; }
.subtitle { color: var(--muted); margin: 0 0 24px; font-size: 1.05em; }
a { color: var(--accent); }
pre, code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.82em;
}
pre {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 8px; padding: 14px 16px; overflow-x: auto;
  white-space: pre-wrap; line-height: 1.5;
}
code { background: var(--code-bg); padding: 1px 5px; border-radius: 4px; }
pre code { background: none; padding: 0; }
.toc {
  background: var(--box-bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 20px; margin: 24px 0;
}
.toc ol { margin: 6px 0; padding-left: 22px; }
.callout {
  background: var(--callout-bg); border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 18px 0;
}
.callout .label {
  display: block; font-size: 0.75em; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--accent); font-weight: 700;
  font-family: system-ui, sans-serif; margin-bottom: 4px;
}
.diagram {
  background: var(--box-bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 18px; margin: 18px 0;
  font-family: system-ui, sans-serif; font-size: 0.85em;
}
.diagram .caption { color: var(--muted); font-size: 0.9em; margin-top: 10px; }
.flow { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.box {
  background: var(--bg); border: 1.5px solid var(--fg); border-radius: 8px;
  padding: 8px 14px; text-align: center;
}
.box .detail { display: block; color: var(--muted); font-size: 0.85em; }
.arrow { color: var(--muted); font-size: 1.1em; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 0.92em; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
th { background: var(--box-bg); font-family: system-ui, sans-serif; font-size: 0.85em; }
.quiz-q {
  background: var(--box-bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 20px; margin: 20px 0;
}
.quiz-q p { margin-top: 0; font-weight: 700; }
.quiz-opt {
  display: block; width: 100%; text-align: left; margin: 8px 0;
  padding: 10px 14px; background: var(--bg); color: var(--fg);
  border: 1px solid var(--border); border-radius: 8px;
  font: inherit; font-size: 0.95em; cursor: pointer;
}
.quiz-opt:hover { border-color: var(--accent); }
.quiz-opt.picked-correct { border-color: var(--ok); background: var(--ok-bg); }
.quiz-opt.picked-wrong { border-color: var(--bad); background: var(--bad-bg); }
.feedback {
  margin: 4px 0 12px; padding: 10px 14px; border-radius: 8px;
  font-size: 0.92em;
}
.feedback.correct { background: var(--ok-bg); border: 1px solid var(--ok); }
.feedback.wrong { background: var(--bad-bg); border: 1px solid var(--bad); }
.term {
  font-style: inherit; cursor: help; position: relative;
  border-bottom: 1px dotted var(--muted); outline: none;
}
.term::after {
  content: attr(data-def);
  position: absolute; left: 0; bottom: calc(100% + 6px); z-index: 10;
  width: max-content; max-width: min(320px, 78vw);
  background: var(--fg); color: var(--bg);
  font: 400 0.78rem/1.45 system-ui, sans-serif;
  padding: 8px 10px; border-radius: 8px;
  opacity: 0; visibility: hidden; transition: opacity 0.12s;
  pointer-events: none;
}
.term:hover::after, .term:focus::after { opacity: 1; visibility: visible; }
.term.term-right::after { left: auto; right: 0; }
@media (max-width: 600px) {
  body { font-size: 16px; }
  main { padding: 24px 16px 60px; }
  .flow { flex-direction: column; align-items: stretch; }
  .arrow { transform: rotate(90deg); text-align: center; }
}
"""

TERM_JS = """
document.querySelectorAll('.term').forEach(function (el) {
  el.setAttribute('tabindex', '0');
  var rect = el.getBoundingClientRect();
  if (rect.left + 320 > document.documentElement.clientWidth) {
    el.classList.add('term-right');
  }
});
"""

QUIZ_JS = """
document.querySelectorAll('.quiz-opt').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var correct = btn.dataset.correct === '1';
    var q = btn.closest('.quiz-q');
    q.querySelectorAll('.quiz-opt').forEach(function (b) {
      b.classList.remove('picked-correct', 'picked-wrong');
    });
    btn.classList.add(correct ? 'picked-correct' : 'picked-wrong');
    var fb = q.querySelector('.feedback');
    if (!fb) {
      fb = document.createElement('div');
      fb.className = 'feedback';
      q.appendChild(fb);
    }
    fb.className = 'feedback ' + (correct ? 'correct' : 'wrong');
    fb.textContent = (correct ? '\\u2705 Correct. ' : '\\u274c Not quite. ')
      + btn.dataset.feedback;
  });
});
"""


def render(spec):
    e = html.escape
    toc_items = [
        f'<li><a href="#{s["id"]}">{e(s["heading"])}</a></li>'
        for s in spec["sections"]
    ]
    quiz = spec.get("quiz", [])
    if quiz:
        toc_items.append('<li><a href="#quiz">Check your understanding</a></li>')

    body = []
    for s in spec["sections"]:
        body.append(f'<h2 id="{s["id"]}">{e(s["heading"])}</h2>')
        body.append(s["html"])

    if quiz:
        body.append('<h2 id="quiz">Check your understanding</h2>')
        for i, q in enumerate(quiz, 1):
            options = list(q["options"])
            random.shuffle(options)
            opts_html = "".join(
                f'<button class="quiz-opt" data-correct='
                f'"{1 if o.get("correct") else 0}" '
                f'data-feedback="{e(o["feedback"])}">{e(o["text"])}</button>'
                for o in options
            )
            body.append(
                f'<div class="quiz-q"><p>{i}. {e(q["question"])}</p>'
                f"{opts_html}</div>"
            )

    subtitle = (
        f'<p class="subtitle">{e(spec["subtitle"])}</p>'
        if spec.get("subtitle")
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(spec["title"])}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>{e(spec["title"])}</h1>
{subtitle}
<nav class="toc"><strong>Contents</strong><ol>{"".join(toc_items)}</ol></nav>
{"".join(body)}
</main>
<script>{TERM_JS}{QUIZ_JS}</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec", help="path to the JSON spec")
    ap.add_argument("-o", "--output", help="exact output path")
    ap.add_argument("--out-dir", help="directory for the date-prefixed file")
    args = ap.parse_args()

    try:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read spec: {exc}")
    validate(spec)

    if args.output:
        out = Path(args.output)
    elif args.out_dir:
        slug = spec.get("slug") or slugify(spec["title"])
        date = datetime.date.today().isoformat()
        out = Path(args.out_dir) / f"{date}-{slug}.html"
    else:
        fail("pass --out-dir or -o")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(spec), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
