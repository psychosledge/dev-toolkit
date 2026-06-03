---
name: verify
description: Verify the current slice against acceptance criteria and review code quality. Human approval gate before commit.
argument-hint: "[acceptance criteria (optional)]"
---

Invoke the **verifier** subagent to verify the current slice against its acceptance criteria and review code quality.

Provide the slice's acceptance criteria if known, or ask the user to paste them before proceeding.

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
