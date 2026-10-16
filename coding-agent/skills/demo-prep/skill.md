---
name: demo-prep
description: Plans what to show and what to talk about at an upcoming demo, from recently finished work that hasn't been demoed yet, with a verified "why" and "before" for each item. Use when prepping for a demo or client meeting, or when asked what to demo, for demo talking points, or for a summary of what a story or branch added and fixed.
---

# Demo Prep

Turns finished-but-not-yet-demoed work into a demo plan: what to show live, what to describe,
and what to leave out. Ground every claim in code, not in a plan or ADR's description of it.

## Current Engagement Config

Read the `tracking-config` project memory (fields defined in the `tracking` skill) for the
**tracking root** and `Demo tracking`, if it exists. Without it, this skill works from a named
story or branch only.

## Step 1 — Find the candidates

- **A story or branch named in the request:** that's the only candidate.
- **Otherwise, with `Demo tracking` set:** every item with a blank `Demoed` in the live unit's
  README, plus its `## Queued for next demo` section, plus blank-`Demoed` items in archived units.
  Walk back through archived units by each README's Continues-from path, and stop at the first
  unit with no blank `Demoed` items.
- **Otherwise, with `Demo tracking` disabled:** ask when the last demo was, then take the Closed
  items from the live unit and from archived units back to that date.

Present the candidate list and confirm it before gathering evidence. The user may add work the
tracker never captured or drop something already covered elsewhere.

## Step 2 — Gather evidence

Resolve each repo's diff base with the `branching-model` skill. Per candidate:

1. Read the story's `plan.md` and any ADRs for scope and intent.
2. For each repo, read the commits and diffs against the diff base: `git log --no-merges
   <base>..<branch>` and `git diff --stat <base>...<branch>`, or the merged commits for work
   already on the base. Read commit bodies in full.
3. Read PR descriptions with `gh` when PRs exist, and check merge state.
4. For every "before" claim, read the base's code from before the change (`git show
   <base-or-parent>:<path>`). Never carry a "before" over from a plan, ADR, or PR description
   unverified. If a claim cannot be verified from code, mark it `(unconfirmed)` or leave it out.
5. For repos with unfamiliar areas, delegate the sweep to a subagent and keep only the findings.

## Step 3 — Classify each change

Kind:

- **New feature:** behavior that did not exist before.
- **Bug fixed:** behavior that was wrong before. Confirm in the earlier code that the bug existed.
- **Behavior change:** intentional difference that is neither of the above.
- **Internal:** refactors, removals, test migration, performance. Not visible to users.

Exclude any fix for a problem the same body of work introduced. The audience sees those as
no-ops.

Demo treatment:

- **Show:** visible to the audience and running somewhere you can present it. Ask which
  environment it's deployed to when that isn't evident. Don't assume a merge means deployed.
- **Tell:** real and worth mentioning, but not visible (internal work, a backend-only fix) or
  not yet runnable where you'll present.
- **Hold:** not ready to mention yet, such as unmerged work the user doesn't want to preview.

## Step 4 — Write the plan

Write `demo-prep-<date>.md` in the live unit's directory (the most recently archived unit when
there's no live one), next to the story's `plan.md` for a single named story, or where the user
specifies. Structure:

1. **Show** table, in running order: # | Item | Kind | What to show | Why it matters. Order so
   the demo tells a story: the headline first, then related items grouped together.
2. **Tell** table: Item | Kind | Talking point | Before.
3. **Behavior changes** bullets, when any exist that the audience will notice.

Rules:

- "Why it matters" states the user impact, not the root cause.
- "Before" is the earlier behavior read from code.
- Order repos consistently, UI then API then Agent, or the order the user gives.
- Keep each cell to one or two sentences.
- Leave Hold items out of the file.
- Follow the global sentence-style rules: no em dashes, no "X, not Y" constructions, no appended
  verdicts.
- Test counts come from the latest PR or a fresh run, not from a plan.

## Reply

Give the file path, then list only the judgment calls the user should check: Show/Tell/Hold
calls that depended on deployment state, borderline classifications, and any claim that rests
on partial evidence.
