---
name: plan
description: Decompose a user story into sequenced implementation increments with acceptance criteria and a UAT checklist. Human approval gate before any work begins. Use after /story has produced an approved story card.
argument-hint: "[user story or ticket URL]"
---

Invoke the **planner** subagent to decompose the following user story into sequenced implementation increments.

After the planner produces the Slice Plan and UAT Checklist, determine the proposed feature branch before presenting anything to the human:

1. Scan `$ARGUMENTS` for a Jira ticket ID (pattern: `[A-Z]+-[0-9]+`) or a URL containing `/browse/`. If found, extract the ticket ID (e.g., `BDXA-156`) and propose `feature/BDXA-156`.
2. If no ticket is found, derive a short slug from the story title (lowercase, hyphen-separated, ≤ 40 chars) and propose `feature/<slug>`.
3. Check the current repo's `CLAUDE.md` for a branch policy override (e.g., "branch policy: main" or "work directly on main"). If present, skip branch setup and note it in the presentation.
4. Note whether the proposed branch already exists locally (`git branch --list <branch-name>`).

Present the Slice Plan, UAT Checklist, and proposed branch as a single package:

> **Proposed branch:** `feature/BDXA-156` _(will be created / already exists)_

Then ask: "Does this plan and branch look right? Approve to begin."

**Do not proceed until the human explicitly approves.** If they request changes to the plan or branch name, revise and re-present before asking again.

After approval:
- If the branch doesn't exist: `git switch -c <branch-name>`
- If it already exists: `git switch <branch-name>`
- Confirm the active branch, then proceed with slice work.

User story:
$ARGUMENTS
