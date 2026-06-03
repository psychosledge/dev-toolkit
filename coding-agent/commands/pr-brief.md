---
name: pr-brief
description: Produces a ready-to-paste PR title and description from the story's plan, review notes, ADRs, and git history. Replaces /pr-description for stories run through the workloop. Invoked automatically on the final slice, or run standalone before opening a PR.
argument-hint: "[story slug or plan file path (optional)]"
---

Produce a PR title and description for the current story, ready to paste into GitHub.

Story context (optional):
$ARGUMENTS

---

## Step 1 — Locate artifacts

Find `docs/stories/<slug>/plan.md`. If $ARGUMENTS provides a slug or path, use it. Otherwise identify the slug from the most recent git commits (the plan file path appears in orchestrator update commits) or ask the human to confirm.

Once located, read:
- `docs/stories/<slug>/plan.md` — slice list, AC per slice, commit hashes, UAT checklist
- All `docs/stories/<slug>/review-notes-slice-N.md` files — verifier findings and quality signals per slice
- Any ADRs referenced in the plan or linked from the story directory (`docs/adr/`)
- `git log --oneline` for the commits that make up this story (use the commit hashes from the plan)
- `git diff <first-slice-commit>^..HEAD` for the full change set

## Step 2 — Synthesize

From the artifacts, extract:
- The problem being solved (from the story background and AC)
- The approach taken and what was ruled out (from ADRs and review notes)
- Notable quality signals — any blockers resolved, significant refactoring suggestions acted on, test coverage decisions
- The scope: files changed, layers touched, any scaffolding left open

Do not fabricate rationale. If a decision's reasoning isn't in the artifacts, say so rather than inventing it.

## Step 3 — Produce the PR description

Output the following, ready to paste into GitHub:

---

**Title:** [One declarative sentence, under 70 characters, describing the user-facing outcome]

**Body:**

## What changed
[2–4 sentences: what problem this solves, what approach was taken, what was ruled out. Written for a reviewer who knows the codebase but not this story.]

## Key decisions
- **[Decision]:** [1–2 sentence rationale, sourced from ADR or review notes]
- **[Decision]:** [rationale]
[Omit this section if no significant decisions were documented.]

## Test coverage
[1–2 sentences on what's tested and any deliberate gaps or scaffolding left open.]

## UAT
- [ ] [checklist item from plan]
- [ ] [checklist item from plan]
[Copy the UAT checklist from the plan file verbatim. Mark items ✅ if the human confirmed them during Step 5 of /slice.]

---

Keep the description tight. A reviewer should be able to read it in under two minutes and understand what to look for. Omit sections that have nothing meaningful to say.

## Step 4 — Offer drill-down

After presenting the PR description, offer:

> "Want to adjust the framing or expand any section before you open the PR?"

If the human asks for changes, revise inline — do not re-run the full synthesis.
