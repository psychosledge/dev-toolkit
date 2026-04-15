---
name: bug
description: Characterize and fix a bug with TDD — architect check, coder fix with regression test, verifier sign-off, human approval gate before commit.
argument-hint: "[bug description]"
---

Investigate and fix a bug using the coder's TDD bug-fix workflow, then verify the fix.

Bug report:
$ARGUMENTS

---

Follow this sequence exactly.

**Step 1 — Characterize**
Before touching any code, establish:
- What is currently happening?
- What should be happening instead?
- What is the minimal reproduction scenario?
- Which area of the codebase is likely responsible?

Read the relevant code. Do not guess.

**Step 2 — Architect check**
Does this bug reveal a structural problem — incorrect boundaries, a missing abstraction, a design that made this bug inevitable?

- If **yes**: invoke the **architect** subagent to assess the right fix approach. Present the output to the human and wait for explicit approval before proceeding.
- If **no**: proceed to Step 3.

**Step 3 — Fix**
Invoke the **coder** subagent with the characterization from Step 1. The coder must:
1. Write a regression test that reproduces the bug — it must fail first
2. Fix the bug with minimal scope; do not refactor beyond what's needed to fix it
3. Verify the regression test now passes and the full test suite is green

**Step 4 — Verify**
Invoke the **verifier** subagent with:
- The bug characterization from Step 1 as the acceptance criteria
- Expected outcome: the bug no longer occurs and no regressions were introduced

**Step 5 — Human pre-commit gate**
Present the verification report and wait for explicit human approval before committing.