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

**Step 0 — Slice recap**
Before any work begins, orient the human to exactly what this slice covers.

1. Locate the plan file: list `docs/stories/` and identify the active story directory. If exactly one exists, use it. If multiple exist, match against the slice name or story context.
2. Read `docs/stories/<slug>/plan.md` and find the section for this slice (match by name or number from `$ARGUMENTS`).
3. Present the recap to the human:

> **Slice [N]: [name]**
> **Scope:** [scope from plan]
> **Acceptance Criteria:**
> - [ ] [criterion]
> - [ ] [criterion]

Then proceed immediately to Step 1 — no approval needed here. If the human flags a scope concern, pause and surface it before continuing.

**Step 1 — Architect check**
Does this slice require architectural decisions (new domain concepts, new external integrations, cross-cutting concerns, or anything warranting an ADR)?

- If **yes**: invoke the **architect** subagent. Present the design output to the human and wait for explicit approval before continuing. If changes are requested, revise and re-present.
- If **no**: proceed directly to Step 2.

**Step 2 — Implementation**
Invoke the **coder** subagent to implement the slice using TDD (Red-Green-Refactor). The coder should work within the scope of this slice only.

**Step 3 — Verification**
Invoke the **verifier** subagent to verify the slice against its acceptance criteria and review code quality.

**Step 4 — Code review walk-through**

Read `coding-agent/commands/code-review.md` and follow Steps 1 through 3 (orient → walk-through → fix loop). The verifier will have written review notes to `docs/stories/<slug>/review-notes-slice-N.md` — the code-review walk-through reads these automatically for the pre-flight summary and inline findings.

Do not run Step 4 of `code-review.md` (the standalone commit step) — Phase 4b below owns the commit.

Once the walk-through is complete and the human is satisfied, proceed to Phase 4b.

**Phase 4b — Commit and plan update**

Ask for explicit commit approval:

> "Approve to commit?"

After approval, commit the changes and update `docs/stories/<slug>/plan.md` for this slice:

1. Run `git log -1 --format="%h"` to get the commit hash.
2. In this slice's section:
   - Change `**Status:** not started` → `**Status:** ✅ done`
   - Change `**Commit:** —` → `**Commit:** <hash>`
   - Check off each AC that was verified: `- [ ]` → `- [x]`
3. Write the updated file.

Do not modify other slices' sections or the UAT checklist.

**Step 5 — UAT checklist and PR prep (final slice only)**
If this is the last slice in the plan, after the commit is approved:

1. Present the full UAT checklist from `docs/stories/<slug>/plan.md` and ask the human to confirm all items.
2. Once UAT is confirmed, invoke the `pr-brief` command to produce the PR title and description from the story's artifacts. The human can paste the output directly into GitHub.
