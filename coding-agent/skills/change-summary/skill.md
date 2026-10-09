---
name: change-summary
description: Builds a stakeholder-facing summary of what a story or branch added and fixed, with a "why" per item and a verified "before" for each. Use when asked for a changes summary, a list of new features and bugs fixed, demo talking points, or release/review notes for a story that spans one or more repos.
---

Produce a verified list of what changed and why it matters. Ground every claim in code, not in a plan or ADR's description of it.

## Inputs

Resolve the story or branch from the user's request. Ask only if it is ambiguous. Resolve each repo's diff base with the `branching-model` skill.

## Gather evidence

1. Read the story's `plan.md` and any ADRs for scope and intent.
2. For each repo, read the commits and diffs against the diff base: `git log --no-merges <base>..<branch>` and `git diff --stat <base>...<branch>`. Read commit bodies in full.
3. Read open PR descriptions with `gh` when PRs exist.
4. For every "before" claim, read the base branch's code (`git show <base>:<path>`). Never carry a "before" over from a plan, ADR, or PR description unverified. If a claim cannot be verified from code, mark it `(unconfirmed)` or leave it out.
5. For repos with unfamiliar areas, delegate the sweep to a subagent and keep only the findings.

## Classify each change

- **New feature:** behavior that did not exist on the base.
- **Bug fixed:** behavior that was wrong on the base. Confirm in base code that the bug existed there.
- **Behavior change:** intentional difference that is neither of the above.
- **Internal:** refactors, removals, test migration, performance. Not visible to users.

Exclude any fix for a problem this story itself introduced. The audience sees those as no-ops. When classification is borderline, decide from the base branch's code and list the borderline calls in the reply, not in the file.

## Output

Write `changes-summary.md` next to the story's `plan.md`, or where the user specifies. Structure:

1. **New features** table: Change | Repos | Why. "Why" states the motivation.
2. **Bugs fixed** table: Bug | Repos | Why it matters. "Why it matters" states the user impact, not the root cause.
3. **Behavior changes** bullets.
4. **Internal (tell only)** bullets, each with a "Before" where it adds information.

Rules:
- Order repos consistently, UI then API then Agent, or the order the user gives.
- State "before" as `origin/<base>` behavior read from code.
- Keep each cell to one or two sentences.
- No section listing what was left out, and no sentence justifying an absence.
- Follow the global sentence-style rules: no em dashes, no "X, not Y" constructions, no appended verdicts.
- Test counts come from the latest PR or a fresh run, not from a plan.

## Reply

Give the file path, then list only the judgment calls the user should check: borderline classifications and any claim that rests on partial evidence.
