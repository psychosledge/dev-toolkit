---
name: verify
description: Verify code quality and correctness. Works with or without a plan — AC check runs if criteria are available, quality assessment always runs. Human approval gate before commit.
argument-hint: "[acceptance criteria (optional)]"
---

Invoke the **verifier** subagent to review code quality and verify correctness.

**If acceptance criteria are available** (passed as arguments, or findable in `docs/stories/<slug>/plan.md`), verify each criterion and report met/not met.

**If no AC exists**, skip the AC check entirely — do not prompt the user for criteria they don't have. Proceed directly to the quality assessment.

Check all files changed on this branch since it diverged from main.

The verifier will produce:
- AC verification (each criterion: met or not met)
- Quality rating (X/10)
- Strengths and issues (with priority)
- Refactoring suggestions
- Test coverage analysis

After the verifier presents its report, read `coding-agent/commands/code-review.md` and follow Steps 1 through 3 (orient → walk-through → fix loop). The verifier will have written review notes to disk — the walk-through reads these for the pre-flight summary and inline findings.

Do not run Step 4 of `code-review.md` (the standalone commit step) — this command owns the commit.

Once the walk-through is complete and the human is satisfied, ask for explicit commit approval:

> "Approve to commit?"

Commit on approval.

Branch changes:
!`git diff --stat $(git merge-base main HEAD)`

Files changed:
!`git diff --name-only $(git merge-base main HEAD)`
