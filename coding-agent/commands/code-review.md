---
name: code-review
description: Walk through code changes with the human — explains what changed and why, surfaces issues in context, handles fixes, and gates commit approval. Works standalone or after /verify.
argument-hint: "[optional: base ref to diff against, e.g. main or a commit hash]"
---

Walk through the current code changes with the human before committing.

## Before Starting

Check for a `CLAUDE.md` at the project root. Read it and apply project-specific context — architecture patterns, code style, domain language — so your explanations are grounded in what this project expects.

## Step 1: Orient

Determine the diff base: use `$ARGUMENTS` if provided (e.g., `main`, a commit hash), otherwise default to `main` (or `HEAD` if no `main` branch exists). Run `git diff` against that base and `git log --oneline -5` for recent context. If the diff is large, scan it first to understand the shape of the change before diving in.

## Step 2: Walk Through the Changes

**a) Group the changed files by concern** — not alphabetically, but by what problem they solve together. Examples: "the new middleware and its types", "the store and the views that use it", "tests for the above". Small changes may have only one group.

**b) For each group — present ONE group per response, then stop and wait:**
1. Name the group and its purpose in one sentence
2. Read the relevant files and show the meaningful changed code in a code block — actual file contents, not raw diff syntax (typically 10–40 lines)
3. Explain **what changed** — specifically and concisely
4. Explain **why** — what problem this solves, what alternative was rejected, what constraint drove the structure. This is the most important part.
5. Note any quality issues you observe naturally for this code
6. End with: "Questions on this group before I move on?"

**Do not present the next group until the human replies.** One group per response is the rule — not a suggestion.

**c) After all groups, consolidate:**
- 2–3 sentence summary of the full change
- Sorted issue list:
  - **Blockers** (failing tests, unmet requirements)
  - **Recommended fixes** (quality issues worth addressing)
  - **Optional improvements** (low-priority suggestions)
  - If nothing flagged: "No issues — the implementation looks clean."
- Ask: "Which of these would you like to address? Call out any by number, or say 'commit as-is' to proceed."

## Step 3: Fix Loop (if fixes requested)

For each approved fix:
1. Invoke the **coder** subagent with specific, scoped instructions — reference the exact file and issue
2. After the coder finishes, do a targeted re-walk: show the updated code, explain what changed. Keep it brief — context is already established.
3. Ask: "Good? Anything else to adjust?"
4. Repeat for remaining fixes.

## Step 4: Commit

Once the human is satisfied, ask for explicit commit approval:

> "Approve to commit?"

Commit on approval with a clear commit message describing the change.

This command is standalone — it does not update plan files or UAT checklists. Use `/slice` for the full workloop.
