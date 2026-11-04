---
name: auto-story
description: Execute all remaining slices of an approved plan back to back using the auto-slice loop, then hand the whole branch to /code-review with the human. Opt-in alternative to running /slice per slice; use after /plan has produced an approved plan.
argument-hint: "[story slug or plan path (optional when one active story exists)]"
---

Execute every remaining slice of the approved plan autonomously, one after another, then return to the human for a whole-branch review and UAT.

Story:
$ARGUMENTS

---

**Shared mechanics.** Each slice runs with `/auto-slice`'s loop, boundaries, rulings format, and fix-loop cap. Read that command's Boundaries section and apply it here in full. A named stop ends the whole run; the end-of-run report then covers everything completed so far plus the stopped slice's state.

**Step 0 — Run recap and the one approval**

1. Locate the plan as `/slice` Step 0 does. Identify every slice whose Status is not done, in plan order.
2. Present the run recap: each remaining slice with its name and one-line scope, which ones the plan flags `Needs Architect` (each of those pauses for design approval when reached), and the working branch.
3. Confirm the branch and checkout the way `/auto-slice` Step 0 does, worktree question included.
4. State plainly: "These N slices run back to back. You'll be interrupted only for architect design approvals and named stops. Per-slice commits happen automatically; nothing is pushed."
5. Wait for explicit approval.

**Per slice**

Run `/auto-slice` Steps 1 through 4: architect check with its human gate, implementation, capped verify loop, commit, plan update. Skip the per-slice end report; rulings and deferred findings accumulate for the run report. After each commit, continue to the next slice without pausing.

**Resuming an interrupted run**

Re-derive position from the record, never from conversation memory: a slice whose plan section shows Status done with a commit hash is complete and never reruns. Cross-check `git log` and the `## Rulings` section, then continue from the first slice without a done Status.

**End of run**

1. Present the run report: slices completed with commit hashes; per-slice verification evidence (quality score, AC met, test command with its final output line); **Rulings**, exhaustive, in order; **Deferred findings**; any slice left incomplete by a stop, with its state.
2. Invoke `/code-review` over the whole branch (Owner Mode, diff base per the `branching-model` skill). The human walk-through returns here: every group, finding, and fix decision follows that command unchanged. The slices are already committed, so fixes from this review land as new commits.
3. After the review, present the UAT checklist and follow `/slice` Step 5 for UAT confirmation and release/PR prep with the human.
