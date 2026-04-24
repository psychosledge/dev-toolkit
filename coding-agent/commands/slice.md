---
name: slice
description: Execute a planned slice through architect → coder → verifier with human approval gates. Use after /plan has produced an approved plan.
argument-hint: "[slice name and acceptance criteria]"
---

Execute the following slice through the full design → code → verify loop with human approval gates at each checkpoint.

Slice to implement:
$ARGUMENTS

---

Follow this sequence exactly. Do not skip steps or approval gates.

**Step 1 — Architect check**
Does this slice require architectural decisions (new domain concepts, new external integrations, cross-cutting concerns, or anything warranting an ADR)?

- If **yes**: invoke the **architect** subagent. Present the design output to the human and wait for explicit approval before continuing. If changes are requested, revise and re-present.
- If **no**: proceed directly to Step 2.

**Step 2 — Implementation**
Invoke the **coder** subagent to implement the slice using TDD (Red-Green-Refactor). The coder should work within the scope of this slice only.

**Step 3 — Verification**
Invoke the **verifier** subagent to verify the slice against its acceptance criteria and review code quality.

**Step 4 — Human pre-commit gate**
The verifier presents the full report (blockers and non-blockers together) and waits for human direction. If changes are requested, return to Step 2, then re-run Step 3 and Step 4 so the human sees fresh verification results before approving the commit.

**Step 5 — UAT checklist (final slice only)**
If this is the last slice in the plan, after the commit is approved, present the full UAT checklist from the planner and ask the human to confirm all items before the feature is considered complete and ready to ship.