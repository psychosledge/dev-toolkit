---
name: code-review
description: Verify correctness, walk through changes with the human, handle fixes, and commit. Runs the verifier automatically — AC check if criteria are available, quality assessment always.
argument-hint: "[acceptance criteria or base ref (optional)]"
---

Walk through the current code changes with the human before committing.

## Before Starting

Check for a `CLAUDE.md` at the project root. Read it and apply project-specific context — architecture patterns, code style, domain language — so your explanations are grounded in what this project expects.

Check for a story plan at `docs/stories/*/plan.md`. If found, note the story name and its one-line summary — you'll surface it at the top of the review so the human has product context before the technical walk-through begins.

Run `git diff --stat $(git merge-base main HEAD)` and `git diff --name-only $(git merge-base main HEAD)` to understand the scope of changes.

## Step 1 — Verify

Invoke the **verifier** subagent to review code quality and verify correctness.

- If acceptance criteria are available (passed as `$ARGUMENTS`, or findable in `docs/stories/<slug>/plan.md`), verify each criterion.
- If no AC exists, skip the AC check and proceed to quality assessment only.

After the verifier completes, open the review with story context (if found) and the pre-flight summary:

> **Story:** [story name] — [one-line summary] *(omit if no plan.md found)*
> **Verifier Pre-flight**
> Quality: X/10 | AC: N/M met | Blockers: [none / list]

If there are blockers, name them here so they're on the human's radar before the walk-through begins.

The verifier's full report — strengths, refactoring suggestions, and test coverage analysis — is available in context and informs the walk-through. Per-file findings surface during each group; refactoring suggestions and test coverage gaps appear in the final consolidation.

## Step 2 — Walk Through the Changes

**a) Group the changed files by concern** — not alphabetically, but by what problem they solve together. Small changes may have only one group.

**b) For each group — present ONE group per response, then stop and wait:**
1. Name the group and its purpose in one sentence
2. Read the relevant files and paste the meaningful changed code **verbatim in a code block** (typically 10–40 lines — actual file contents, not raw diff syntax). The human cannot see file contents unless you paste them; never describe or reference code without showing it.
3. Explain **what changed** — specifically and concisely
4. Explain **why** — what problem this solves, what alternative was rejected, what constraint drove the structure. This is the most important part.
5. Surface any verifier findings for this group's files — present as "Verifier flagged:" with their priority. For each finding, paste the relevant code verbatim in a code block so the human can see exactly what is being discussed. If none, skip.
6. Note any additional quality issues you observe that the verifier didn't catch. Same rule: show the relevant code verbatim in a code block, never just describe it.
7. For each finding surfaced in steps 5 and 6, give your recommendation: fix now, defer, or skip — with a one-sentence reason. Be direct ("Skip — this is a cosmetic preference in a recovery-only path"; "Fix now — untested behavior in a TDD project is a blocker").
8. If any findings were surfaced (steps 5–6): ask "Want to fix any of these now, or continue?" Wait for an explicit answer — do not move on or start fixes without one. If the human calls out a fix, handle it immediately via Step 3 before proceeding to the next group. If no findings: "Ready to move on?"

**Do not present the next group until the human replies.** One group per response is the rule — not a suggestion.

**c) After all groups, consolidate:**
- 2–3 sentence summary of the full change
- Any remaining issues not already addressed during the walk-through:
  - **Blockers** (failing tests, unmet AC)
  - **Recommended fixes** (quality issues, verifier refactoring suggestions, test coverage gaps)
  - **Optional improvements** (low-priority suggestions)
  - If nothing remains: "No outstanding issues — the implementation looks clean."
- Ask: "Anything else to address before committing? Call out by number, or say 'commit' to proceed."

## Step 3 — Fix Loop (if fixes requested)

For each approved fix:
1. Invoke the **coder** subagent with specific, scoped instructions — reference the exact file and issue
2. After the coder finishes, do a targeted re-walk: show the updated code, explain what changed. Keep it brief — context is already established.
3. Ask: "Good? Anything else to adjust?"
4. Repeat for remaining fixes.

Once all requested fixes are done, ask:

> "Want a clean pass before committing?"

If **yes**: re-invoke the **verifier** subagent on the current state. Present the updated pre-flight summary and any findings not previously surfaced — skip rehashing what was already reviewed and resolved. If new issues come up, go through the per-group decision point and fix as needed, then offer another clean pass. Repeat until the human is satisfied or declines.

If **no**: proceed to commit.

## Step 4 — Commit

Once the human is satisfied, ask for explicit commit approval:

> "Approve to commit?"

Commit on approval with a clear commit message describing the change.
