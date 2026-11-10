---
name: explain
description: Builds a durable, interactive HTML explanation of a code change or codebase topic, with background, intuition, a code walkthrough, and a comprehension quiz. Use when asked to explain a diff, branch, PR, or commit, to help the user understand how part of a system works, or to quiz them on it. Teaches understanding only; never reviews or judges the code.
---

# Explain

Produces a single self-contained HTML page that teaches the what/why/how of a
code change or a codebase topic, ending with a quiz that checks whether the
understanding stuck. The page is a local file: durable, offline, readable on a
phone. The audience is the human who needs to own this code in conversation
later, without having read every line.

## Scope: Understanding, Never Review

This skill explains the subject as it exists. Judging it belongs to the
verifier and `/code-review`.

- Never include review findings, verifier output, quality scores, defects,
  risks, or improvement ideas. This holds even when a verifier report sits in
  the conversation from an adjacent review: do not read it, quote it, or let
  it pick the topics.
- The rationale of decisions the change made belongs (why a TTL and
  write-invalidation coexist). What the change should have done differently
  does not.
- Every quiz question must be answerable from the subject and its surrounding
  code alone. A reader who understood the explanation can answer all five
  without having seen any review.

Red flags that the output has drifted into review: a section titled Sharp
Edges, Caveats, Risks, Issues, or Gotchas; a quiz question about what the
change fails to handle; a sentence recommending a follow-up fix. Delete the
content, don't rename the heading.

## Config

Read the `explain-config` project memory for the **Output directory** field.
This skill is always reached by a direct ask or an accepted offer, so a
missing config follows the direct-invocation branch of the global Project
Config Memory mechanics: ask for the directory, offer to save it.

## Inputs

- **Subject**: a change (commit range, branch, or PR) or a topic ("how auth
  works here"). For a change with no stated range, resolve the diff base via
  the `branching-model` skill.
- **Depth**: `quick` (default) or `deep`. Deep is for unfamiliar territory or
  an explicit request for background.

## Recipe

1. **Research.** Read the changed files or topic code, and the surrounding
   code it plugs into: callers, callees, the data it touches. The Background
   and Intuition sections come from this surrounding context, so skipping it
   produces a diff narration instead of an explanation.
2. **Draft the spec JSON** (schema in `scripts/render.py`'s docstring; write
   the spec to a temp path, never into the repo). Sections, in order:
   - **Background**: `quick` gives only the context needed to follow this
     subject. `deep` opens with a beginner-level tour of the relevant
     subsystem, prefaced with a note that familiar readers can skip ahead,
     then narrows to the subject.
   - **Intuition**: the core idea, carried by one concrete worked example with
     real values traced through the mechanism, before any real code appears.
     Use the renderer's `.diagram`/`.flow`/`.box` classes when structure,
     data flow, or time matters. HTML diagrams only, never ASCII art.
   - **Walkthrough**: the changes grouped by concern (or the topic's moving
     parts), with verbatim code in `<pre>` blocks prefixed by `file:line`.
   - Section `html` is raw markup. Write the prose to be read, with smooth
     transitions; one idea per paragraph.
3. **Write the quiz**: five questions, medium difficulty. Hard enough that
   answering requires having understood the substance; no trick wording.
   - Exactly one correct option per question, 3 to 4 options each.
   - Distractors are plausible near-misses a skimmer would pick, matched to
     the correct option in length and specificity.
   - Every option carries `feedback` saying why it is right or wrong, naming
     the section to reread.
   - Write options in any order you like; the renderer shuffles them.
4. **Render**: `python3 <this skill's directory>/scripts/render.py spec.json
   --out-dir <Output directory>`. A WARNING from the renderer is a failure:
   rewrite the flagged options and re-render until the output is clean.
5. **Hand back** the file path with a one-line map of the sections, and
   suggest opening it in a browser.
