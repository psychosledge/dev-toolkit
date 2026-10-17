---
name: plan
description: Decompose a user story into sequenced implementation increments with acceptance criteria and a UAT checklist. Human approval gate before any work begins. Use after /story has produced an approved story card.
argument-hint: "[user story or ticket URL]"
---

Invoke the **planner** subagent to decompose the following user story into sequenced implementation increments.

After the planner produces the Slice Plan and UAT Checklist, determine the proposed feature branch before presenting anything to the human:

1. Invoke the `branching-model` skill and resolve this repo's branching model by its rules (the repo's own `CLAUDE.md` `## Branching` section, with the usual fallbacks). Note the diff base, whether feature branches are used, and the naming convention if declared. State the diff base on one line in the plan presentation: `Diff base: <branch> (<source>)`, where the source is the repo's `CLAUDE.md`, the `workloop.integrationBranch` override, or the remote default.
2. If `Feature branches: no`, skip branch setup entirely and note it in the presentation.
3. Otherwise, construct the branch name:
   - Scan `$ARGUMENTS` for a ticket ID (pattern: `[A-Z]+-[0-9]+`, common to Jira, Azure Boards, and Linear) or a URL containing a ticket path segment (e.g. `/browse/` for Jira). If found, extract the ticket ID and derive a short human-readable slug from the story title (lowercase, hyphen-separated, ≤ 30 chars).
   - If no ticket is found, derive a short slug from the story title (lowercase, hyphen-separated, ≤ 40 chars).
   - If `Feature branch naming` is declared, substitute the ticket/slug into that pattern (e.g. `<TICKET>/<slug>` → `ABC-123/short-description`).
   - If nothing is declared, propose a bare `<slug>` — no `feature/` prefix, no ticket embedded, even when a ticket ID is on hand. Only add structure once it's actually known to be this repo's convention (`/catchup` is what detects and records it — this command only consumes the declaration).
4. Note whether the proposed branch already exists locally (`git branch --list <branch-name>`).

**Scan for relevant tech debt.** Check the places this project records known issues: the `Backlog` from the `tracking-config` memory when set, and any debt record named in a `debt-tracking-config` project memory. Cross-reference entries that name file paths against each slice's `Files` field. For any overlap, present the matching entries to the human as an explicit, optional addition — do not fold them into the plan automatically:

> **Related tech debt found:**
> - `<file>` — <one-line issue description> (from `<source>`)
>
> Fold any of these into this plan's scope, or leave them deferred?

For anything the human chooses to include, add it as its own slice (or fold into an existing slice touching the same file, human's call) before presenting the final package. If neither source exists, or nothing overlaps, skip this silently — don't mention it.

Present the Slice Plan, UAT Checklist, and proposed branch as a single package:

> **Proposed branch:** `<branch-name>` _(will be created / already exists)_

Then ask: "Does this plan and branch look right? Approve to begin."

**Do not proceed until the human explicitly approves.** If they request changes to the plan or branch name, revise and re-present before asking again.

After approval:
- If the branch doesn't exist: switch to the resolved diff base first (`git switch <diff-base>`, pulling latest if behind), then create the new branch from there with `git switch -c <branch-name>`.
- If it already exists: `git switch <branch-name>`.
- Confirm the active branch, then proceed with slice work.

**Update the tracker README, if this project is tracked.** If a `tracking-config` project memory exists, update this story's row in the live tracker README per the `tracking` skill's workloop checkpoints.

**Log the plan, if this project keeps an activity log.** If a `tracking-config` project memory exists with `Activity log: enabled`, append one activity-log entry (see the `activity-log` skill for format/location) per repo this story's slices touch (domain inferred from the repo/story content, asking only if genuinely ambiguous), describing the plan in one line, referencing the story's `plan.md`.

User story:
$ARGUMENTS
