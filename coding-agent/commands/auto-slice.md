---
name: auto-slice
description: Execute one planned slice autonomously through architect → coder → verifier with a capped fix loop and an automatic commit. Mid-slice human gates are replaced by a rulings ledger, named stops, and an end report. Opt-in alternative to /slice; use after /plan has produced an approved plan.
argument-hint: "[slice name or number]"
---

Execute the following slice through the same design → code → verify loop as `/slice`, with the mid-slice human gates replaced by rulings, named stops, and an end report. Invoking this command is the session's opt-in to autonomy. A `workloop-config` project memory with an `Autonomy` field records a project's default mode (see Project Config Memory in the global CLAUDE.md); this command never requires one.

Slice to implement:
$ARGUMENTS

---

## Boundaries

**Named stops.** These end the autonomous run immediately. Present the current state and every ruling so far, then wait for the human:

- Any destructive or irreversible operation (deleting user data, rewriting git history, dropping a table)
- Any effect that leaves the repo: `git push` (forbidden in every mode, per the global CLAUDE.md), publishing a package, creating tickets, posting comments, calling an external service with side effects
- A schema or data migration
- A new external dependency or integration
- A plan defect where every path forward is a guess
- The fix-loop cap reached with blockers still open

**Rulings.** Every decision that `/slice` would have asked the human gets recorded, at the moment it's made, under a `## Rulings` heading in `docs/stories/<slug>/plan.md` (create the heading on first use):

> Ruling (Slice N): [decision]. Why: [reason]. Cost if wrong: [impact].

This covers interpreted ambiguities in AC or scope, workarounds for plan defects, parked findings, and judgment calls between reasonable implementations. A deviation with no ruling is a decision made in secret. The end report lists every ruling; none may appear only in the file.

## Steps

**Step 0 — Recap and the one approval**

Run `/slice` Step 0 exactly: locate the plan, present the slice recap, and wait for explicit approval. Add two things:

1. State plainly: "This slice runs autonomously after your approval. The next thing you see is the end report, a design approval request if the architect is needed, or a stop."
2. Confirm the working branch is the plan's feature branch; never run on the repo's base branch. Resolve the checkout the way `/slice` Step 0 does.

**Step 1 — Architect check**

Apply `/slice` Step 1's two tests (pattern, ownership). If either says yes, invoke the **architect**, present the design, and wait for explicit human approval. Design approval is a human gate in every mode.

**Step 2 — Implementation**

Same as `/slice` Step 2: invoke the **coder** (or a **general-purpose** subagent for verification-only slices), scoped to this slice, with the worktree bootstrap note when applicable.

**Step 3 — Verify with a capped fix loop**

Invoke the **verifier** (Owner Mode). Act on its report without pausing:

- **Blockers** (unmet AC, failing suite): send each back through the coder with scoped instructions, then re-invoke the verifier focused on the changed files. This loop runs at most 3 rounds. Blockers still open at the cap are a named stop.
- **High-priority findings** on files this slice's diff touches: fix in the same loop, within the same cap.
- **Medium and low findings, and refactoring suggestions**: record each under `## Deferred findings` in `plan.md` (the section `/code-review` Step 3b uses), with file, one-line issue, and a ruling for why it waits.
- **Comment audit**: apply `Remove` verdicts directly; `Keep` verdicts stand.

**Step 4 — Commit and plan update**

When the verifier reports no blockers, commit with a clear message. A commit is local and reversible; it needs no mid-run approval. Then run `/slice` Step 4 unchanged: update the slice's Status, Commit, and AC checkboxes in `plan.md`, plus the tracker row when a `tracking-config` memory exists.

**Step 5 — End report**

Present, in order:

1. Slice name, commit hash, branch.
2. Verification evidence: verifier quality score, AC met N/M, and the test command with its final output line.
3. **Rulings**, exhaustive, in the order made.
4. **Deferred findings** recorded this run.
5. What's next: the next slice by name, or, when this was the plan's final slice, the walkthrough checklist. Walkthrough confirmation and release/PR prep stay with the human, following `/slice` Step 5.

The per-group walk-through `/code-review` provides in gated mode is deferred here. Offer it: "Want the full walk-through? Run `/code-review` against this branch."
