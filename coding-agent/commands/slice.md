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

1. Locate the plan file: list `docs/stories/` and identify the active story directory. If exactly one exists, use it. If multiple exist, match against the slice name or story context. If none exist or none match, tell the human and ask which story this slice belongs to before continuing.
2. Read `docs/stories/<slug>/plan.md` and find the section for this slice (match by name or number from `$ARGUMENTS`).
3. Present the recap to the human:

> **Slice [N]: [name]**
> **Scope:** [scope from plan]
> **Acceptance Criteria:**
> - [ ] [criterion]
> - [ ] [criterion]

4. **Wait for explicit human approval before continuing.** Ask: "Does the scope look right, or do you want to adjust anything before we start?"

Do not proceed to Step 1 until the human confirms. If they flag a scope concern, surface it, revise the plan if needed, and re-present the updated recap before asking again.

**Step 1 — Architect check**
Two independent tests — a slice can pass one and fail the other, so check both:
- **Pattern test:** does this introduce something genuinely new (new domain concepts,
  new external integrations, cross-cutting concerns) rather than reusing an
  already-decided shape or precedent?
- **Ownership test:** does this decide *where* a piece of logic lives — which layer,
  service, or repo owns it — and does that placement have a genuine alternative with a
  different owner, lifecycle, or blast radius (e.g. API vs. UI ownership of a derived
  value, sync vs. async, which service owns a cross-cutting concern)? Reusing an
  existing code pattern to implement the decision does not answer this question.

- If **either** test says yes: invoke the **architect** subagent. Present the design
  output to the human and wait for explicit approval before continuing. If changes are
  requested, revise and re-present.
- If **no** to both: proceed directly to Step 2.

**Step 2 — Implementation**
Invoke the **coder** subagent to implement the slice using TDD (Red-Green-Refactor). The coder should work within the scope of this slice only.

**Step 3 — Verify and review**

Invoke the `/code-review` skill and follow all of its steps. It will run the verifier, walk through changes, handle fixes, and commit.

**Step 4 — Plan update**

After the commit, update `docs/stories/<slug>/plan.md` for this slice:

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
2. Once UAT is confirmed, propose a PR title and description from the story's artifacts. Resolve this repo's PR Platform per the PR Platform instructions in global `CLAUDE.md`. If it resolves to GitHub with `gh` available, offer to create the PR directly with `gh pr create`; otherwise, present the title and description for the human to paste into their platform.
3. If a PR was actually opened and a `weekly-tracking-config` project memory exists with `Activity log: enabled`, append one activity-log entry (see the `activity-log` skill) noting the PR was opened, domain-tagged, referencing the PR link and the story.
