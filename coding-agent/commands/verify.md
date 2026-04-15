---
name: verify
description: Verify the current slice against acceptance criteria and review code quality. Human approval gate before commit.
argument-hint: "[acceptance criteria (optional)]"
---

Invoke the **verifier** subagent to verify the current slice against its acceptance criteria and review code quality.

Provide the slice's acceptance criteria if known, or ask the user to paste them before proceeding.

Check all files changed on this branch since it diverged from main.

Provide:
- AC verification (each criterion: met or not met)
- Quality rating (X/10)
- Strengths and issues (with priority)
- Refactoring suggestions
- Test coverage analysis
- Pre-commit approval gate — pause for explicit human approval before any commit

Branch changes:
!`git diff --stat $(git merge-base main HEAD)`

Files changed:
!`git diff --name-only $(git merge-base main HEAD)`