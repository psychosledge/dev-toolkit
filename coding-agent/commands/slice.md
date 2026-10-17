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
If the slice's **Files** line expects production or test code, invoke the **coder**
subagent to implement it using TDD (Red-Green-Refactor), within this slice's scope only.

If the slice is verification or measurement only (**Files** expects no code beyond scripts
or notes), invoke a **general-purpose** subagent instead. Give it the plan path, the ACs,
and a rule to add a failing test first and fix only if verification surfaces a real gap.

If the working directory is a freshly created git worktree, tell the subagent to bootstrap
it before the first test run: install dependencies, then run any build step the test command
depends on, such as workspace packages that resolve each other from build output.

**Step 3 — Verify and review**

Invoke the `/code-review` skill and follow all of its steps. It will run the verifier, walk through changes, handle fixes, and commit.

If the working tree has no diff, skip `/code-review`. Present the subagent's results to
the human and wait for approval before Step 4.

**Step 4 — Plan update**

After the commit, update `docs/stories/<slug>/plan.md` for this slice:

1. Run `git log -1 --format="%h"` to get the commit hash. With no commit (verification-only
   slice), write `**Commit:** — (no code change)`.
2. In this slice's section:
   - Change `**Status:** not started` → `**Status:** ✅ done`
   - Change `**Commit:** —` → `**Commit:** <hash>`
   - Check off each AC that was verified: `- [ ]` → `- [x]`
3. Write the updated file.

Do not modify other slices' sections or the UAT checklist.

If a `tracking-config` project memory exists, update this story's row in the live tracker README per the `tracking` skill's workloop checkpoints.

**Step 5 — UAT checklist and PR prep (final slice only)**
If this is the last slice in the plan, after the commit is approved:

1. Present the full UAT checklist from `docs/stories/<slug>/plan.md` and ask the human to confirm all items.
2. Once UAT is confirmed, invoke the `branching-model` skill and resolve this repo's `Release` field. State it on one line: `Release: <pull request | skill <name>> (<declared | detected | default>)`.
3. **`Release: skill <name>`:** ask "Run `/<name>` now?" On a yes, invoke that skill and let it handle the release. The yes is the human's explicit approval for whatever that skill does, including any push. Skip the PR steps. Take the released ref (version or tag) from the skill's output, then from `git tag --points-at HEAD`, and otherwise ask the human.
4. **`Release: pull request`:** before proposing the PR, run the repo's CI checks locally. Read whatever CI config the repo actually uses (e.g. `.github/workflows/`, `.gitlab-ci.yml`, a Jenkinsfile) for its lint, format, and test steps, or ask the human if none is detected. Resolve where they run from the `branching-model` skill's `Pre-PR CI` field. `in place` runs them in the current checkout, after `git status --porcelain` confirms nothing untracked or uncommitted that the tests could depend on; anything listed goes to the human before the checks run. `clean checkout` runs them in a throwaway worktree of the branch at `.claude/worktrees/ci-<branch>`, with dependencies installed from the lockfile, and removes it with `git worktree remove` once the checks finish, pass or fail. If a check fails, treat it like any other slice defect: send it back through coder (TDD) → verifier → human approval → a new commit, rather than patching it inline here. Once CI passes, invoke the `pr-description` skill to propose a PR title and description from the story's artifacts. Invoke the `pr-platform` skill and resolve this repo's PR platform by its rules. State the result on one line: `PR platform: <platform> (<declared | detected>), gh <available | unavailable>`. If it resolves to GitHub with `gh` available, offer to create the PR directly with `gh pr create`; otherwise, present the title and description for the human to paste into their platform.
5. If a release actually happened or a PR was actually opened, and a `tracking-config` project memory exists:
   - Update this story's row in the live tracker README per the `tracking` skill's workloop checkpoints.
   - If `Activity log: enabled`, append one activity-log entry (see the `activity-log` skill), domain-tagged, noting the release with its ref or the PR opened with its link, and referencing the story.
