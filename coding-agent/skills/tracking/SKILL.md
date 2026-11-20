---
name: tracking
description: Reference for the tracking-config project memory, the tracker README layout for sprint and release cadences, the workloop checkpoints that update it, story archiving, and release close-out. Read and written by sprint-rollover, sprint-recap, demo-prep, meeting-notes, whats-next, /story, /plan, /slice, and /code-review. Invoke directly to close out a release.
---

# Tracking

A tracked project groups its in-flight work into one **unit** at a time, a directory
`<tracking root>/<unit>/` holding that unit's `README.md` (the working tracker), meeting notes,
topic docs, its `recap.md`, and, when enabled, the activity log. A finished unit moves to
`<tracking root>/archive/`. The cadence decides what a unit is and what ends it:

- **`sprint`:** a time box. It ends on a date, and `sprint-rollover` archives it and scaffolds
  the next one. Exactly one live unit at all times.
- **`release`:** everything intended to ship together, from a single story or bug to a group of
  items. It ends when the last item ships, through release close-out below. Zero live units is
  normal between releases.

The **live unit** is the only entry in `<tracking root>/` other than `archive/`. More than one
is an unusual state, such as an interrupted rollover. Stop and ask which one is live.

## `tracking-config`

A project memory. Its existence means the project is tracked; with no memory, none of this
applies. Resolve and create it per the Project Config Memory instructions in global
`CLAUDE.md`. Fields:

- **Tracking root:** the directory holding the unit directories and `archive/`. The stories root
  is the `stories/` directory alongside it.
- **Cadence:** `sprint` or `release`.
- **Sprint naming:** sprint cadence only. `date` (the sprint's start date, `YYYY-MM-DD`),
  `number` (`sprint-<n>`), or `ask` (a label given at each rollover, slugged for the directory).
- **Sprint length:** sprint cadence only. `<N>w`, or `variable` (ask for the end date at each
  rollover).
- **Backlog:** the file or directory holding not-yet-started work, or `disabled`.
- **Activity log:** `enabled` or `disabled`. Enabled only when there's a team or stakeholder to
  report to. Format and location are in the `activity-log` skill.
- **Calendar:** the calendar identity to read events from, or `disabled`.
- **Demo tracking:** the recurring meeting that counts as the demo, or `disabled`.

An older `weekly-tracking-config` memory maps over as: its weeks root becomes the tracking root,
`Cadence: sprint`, `Sprint naming: date`, `Sprint length: 1w`, `Backlog: disabled`, and the
remaining fields carry over unchanged.

## Unit naming

- **Sprint:** per `Sprint naming`.
- **Release:** `<start date>-<slug>`, the date the release is scaffolded (`YYYY-MM-DD`) and a
  short slug for the work, such as `2026-10-16-journal-export`. Never a version: the version is
  decided at release time. Release close-out prefixes the released ref.

## README layout

Sections, in this order:

1. The H1: `# Sprint <label> (<start> to <end>)` for a sprint, omitting the range when unknown,
   or `# Release <name>` for a release.
2. The Continues-from paragraph, present only when the unit has a predecessor, immediately after
   the H1 and before any heading, worded exactly:
   `**Continues from:** `<previous unit's archived path>`, which now serves as historical
   reference only, not updated further. This directory carries forward only the still-active
   items, self-contained (no need to open the previous directory to follow anything below).`
   Only the path changes from unit to unit. This paragraph is how skills find the previous
   unit, whatever its naming scheme.
3. `## Recap Log`, present only once a recap has been written for the unit (shape below).
4. `## Priority order`
5. `## Active items`, a table. When demo tracking is enabled, it has a `Demoed` column.
6. `## Queued for next demo`, only when demo tracking is enabled and something is queued.
7. `## Closed items (not carried forward — see previous directory for full history)`, a list.
   When demo tracking is enabled, each bullet carries an inline `Demoed <YYYY-MM-DD>` note once
   shown.

In a release, Priority order and Active items cover only what this release ships. Anything not
going out with it stays in the backlog.

### Active items

Columns: `Item`, `Status`, `Next step`, plus `Demoed` when demo tracking is enabled. `Item` is a
short name with links to whatever tracks it (the story's `plan.md`, the PR, a topic doc).

### Workloop checkpoints

When a `tracking-config` memory exists, the workloop commands keep the live unit's README in
step with the work, independent of the `Activity log` setting. At each checkpoint, update the
item's row, or add one if no row matches. Match by story slug, PR link, or plain name.

| Checkpoint | Status | Next step |
|---|---|---|
| `/story` approved | `story drafted` | `/plan` |
| `/plan` approved | `planned, 0/N slices` | first slice |
| `/slice` committed | `k/N slices done` | next slice, or walkthrough |
| PR opened | `PR open` (link in `Item`) | review/merge |
| Released by the repo's release skill | `released <ref>` | none |
| `/code-review` of someone else's PR | review outcome (posted / held / resolved outside this flow) | whose court it's in |

An item that hasn't been through `/story` yet, picked up from the backlog or a board, has next
step `/story`. Every story starts there, and `/plan` requires the `story.md` it writes.

A review-of-someone-else's-PR item never gets shown at Demo Day in its own right, so when demo
tracking is enabled, `/code-review` sets `Demoed` to `N/A` at this same checkpoint.

A `released <ref>` item is finished, so it moves from Active items to Closed items. A PR item
moves to Closed once its merge is confirmed, or once the PR is closed. At that move, for a
merged PR from your own branch, do all of the following without asking: fast-forward the local
base branch; remove the PR's worktree if one exists; delete the local branch with `git branch -d`,
or `git branch -D` when `-d` refuses and `gh pr view` confirms the PR merged; delete the remote
branch with `git push origin --delete <branch>` only if `git ls-remote --heads origin <branch>`
shows it still exists (many platforms auto-delete it at merge). A PR closed without merging
keeps its branches. For a review worktree `.claude/worktrees/pr-<number>` of someone else's PR,
offer to remove it with `git worktree remove`.

**Release cadence with no live unit:** a checkpoint that needs to add a row first starts the
next release. Propose a name per Unit naming from the item at hand, confirm it, then scaffold
`<tracking root>/<name>/` with the README layout above, pointing Continues-from at the most
recently archived release if there is one. Remove the item from the backlog file if it was
listed there.

**Release cadence, Active items now empty:** when a checkpoint moves the last Active item to
Closed, ask whether the release is ready to close out, and run release close-out below on a
yes.

### `Demoed`

A date, filled in once the item has been shown to a stakeholder, in a meeting, async, or any
other form. Blank means not yet shown. Being finished and being demoed are independent facts.
`N/A` means the item type doesn't go through Demo Day at all (see the `/code-review` checkpoint
above), distinct from blank, which means it does and just hasn't happened yet.

### Recap Log

```
## Recap Log

Creation time of each recap file (local machine time, with timezone), for the next
recap run to use as its cutoff — work after a given timestamp is not yet reflected in
that recap.

| File | Created |
|---|---|
| `recap.md` | 2026-09-08 17:33 EDT |
```

One row per recap file. A rewrite later the same day appends `(updated HH:MM <tz>)` to the
existing row's `Created` cell rather than adding a second row.

## Deferred-finding dispositions

Shared by `/plan` (the planner, when the failure-mode sweep defers findings) and `/code-review`
Step 3b. Matches deferred findings against the project's recorded work once per run, so deferral
lands somewhere the team can see, without duplicates.

**Sources.** The `tracking-config` memory's `Backlog` field names a local file or directory. A
`debt-tracking-config` project memory names a remote board instead, with fields `Board:` (the
tracker and project, such as a Jira project key or board URL) and `Query hint:` (optional search
terms folded into the scoped search; absent or `disabled` means none). When both configs exist,
`debt-tracking-config` is the destination for deferred findings. Resolve and create these per
the Project Config Memory instructions in the global `CLAUDE.md`. A source marked `disabled` is
skipped while any other configured source still runs. With no config at all, or every source
`disabled`, the pass is skipped and each caller's own fallback governs: the planner keeps the
drafted hardening story as the sole destination, and `/code-review` Step 3b asks where each
finding goes.

**The pass.** Once per run, per configured source (at most two): batch-match every deferred
finding in one go. A local backlog file is read whole (a directory-valued `Backlog`: every file
in it, read whole); a remote board gets a scoped search (project-plus-keyword or JQL queries
built from the findings, the story slug, and the `Query hint` when set), never a full backlog
read. A failed source read (a board search that errors, or a configured backlog file that is
missing or unreadable) is stated to the human and the run falls back to the hardening story; a
failure is never reported as "no match".

**Dispositions.** Present every match and non-match to the human in one batch; the human picks per finding:

- **covered as-is**: an existing item already covers it. Record the ticket ID or backlog line,
  and offer an optional trail comment on that item.
- **covered with a tweak**: an existing item nearly covers it. Draft the expansion text and show
  it; a shared item changes only after the human approves the draft.
- **no match**: draft a new ticket or backlog entry carrying the trail
  `Deferred from story <slug> (docs/stories/<slug>/plan.md)`; it lands only on the human's
  go-ahead, and sprint placement is the human's call.

**Known issues.** The planner's sweep also sends known issues through this pass: pre-existing
defects that are silent and off-path (planner Step 6.3). They match and dispose like deferred
findings, with two differences. A no-match draft is the planner's one-line entry with no
`Deferred from story` trail. A local backlog file with a `## Known issues` section takes the
entry there, unranked. With no configured source, the planner presents the drafted line at the
approval gate for the human to place, and records the outcome the same way.

**Recording.** Record each outcome in parentheses beside the finding's own record. The planner
appends it after the intact Review Focus token on the finding's line, as
`deferred: hardening story (covered as-is: PROJ-123)`, `(tweak drafted: PROJ-45)`, or
`(new entry: <ref or path>)`. `/code-review` appends
the outcome to the finding's entry under the plan's `## Deferred findings` heading. A finding's
outcome never lands on a line it doesn't own. On a replan or repeat review, read the prior run's
annotations before overwriting and seed the match with those references, alongside the story
slug in the search, so already-ticketed findings match their own tickets instead of accumulating
duplicates.

## Archiving a story

A story moves to `<stories root>/archive/` only at a unit boundary (a sprint rollover or a
release close-out), never immediately on completion. For each story under `<stories root>/`
(excluding `archive/`):

1. **Verify merge status directly against git. Don't trust the plan.md's own "done" or
   "merged" claim.** Invoke the `branching-model` skill and resolve the repo's diff base by its
   rules, then run `git merge-base --is-ancestor <commit> origin/<diff-base>` for whatever
   commit the plan.md cites as the final one. A plan.md marking a slice "✅ done" means the
   implementation was finished in the coding workflow's own sense, not that it's merged. A
   rebase or squash before merge can rewrite the cited commit's SHA entirely. If the cited hash
   isn't an ancestor, check the PR's actual state (`gh pr view`) and/or search
   `git log origin/<diff-base>` by branch name or PR number before ruling it unmerged.
2. **Present each genuinely-merged story one at a time and confirm before moving.** A story can
   be merged but still have an active follow-up (e.g. a "pick this up once X unblocks" note)
   that means it's not done-done yet. Let the user make that call per story.
3. On confirmation: `mv <stories root>/<slug> <stories root>/archive/<slug>`.
4. **Grep-fix every reference to the old path across `<tracking root>/**/*.md`**, live and
   archived units alike. These are path substitutions, not content rewrites. Also check
   `<stories root>/**/*.md` for any sibling story referencing this one by path.
5. If nothing is left to move, say so.

## Release close-out

Release cadence only. Runs when the user asks to close out the release, or when the release's
Active items are empty (see the checkpoint above, and `whats-next`).

1. **Confirm it's actually done.** Every Active item is closed, and each closed item's PR is
   merged or its release ref exists. Check rather than trusting the README. Anything still open
   either goes back to Active items (stop here) or the user decides it moves to the backlog.
2. **Demo status.** Skip if `Demo tracking` is `disabled`. Ask once whether anything was shown to
   a stakeholder that isn't marked yet, and fill in those `Demoed` dates. Leave blanks as they
   are. `demo-prep` finds them in the archive.
3. **Archive the release's stories** per Archiving a story above.
4. **Move the directory.** `mv <tracking root>/<name> <tracking root>/archive/<released ref>-<name>`,
   such as `archive/v1.22.0-2026-10-16-journal-export`, using the released ref (version or tag).
   With no released ref, the name stays unchanged. Grep-fix references to the old path across
   `<tracking root>/**/*.md` and `<stories root>/**/*.md`.
5. **Don't scaffold the next release.** It starts at the next checkpoint that adds a row.
6. **Report** the archived path, any stories archived, and the top of the backlog as candidates
   for the next release when `Backlog` is set.
