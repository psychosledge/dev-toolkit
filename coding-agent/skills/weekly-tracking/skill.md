---
name: weekly-tracking
description: Reference for the weekly-tracking-config project memory, the weekly README layout, and the workloop checkpoints that update it. Read and written by week-rollover, weekly-recap, meeting-notes, whats-next, /story, /plan, /slice, and /code-review. Not normally invoked directly.
---

# Weekly Tracking

A tracked project keeps one directory per week, `<weeks root>/<monday-of-that-week>/`, holding
that week's `README.md` (the working backlog), meeting notes, topic docs, `recaps/`, and, when
enabled, the activity log. Finished weeks move to `<weeks root>/archive/`.

## `weekly-tracking-config`

A project memory. Its existence means the project is tracked; with no memory, none of this
applies. Resolve and create it per the Project Config Memory instructions in global
`CLAUDE.md`. Fields:

- **Weeks root:** the directory holding one `<monday>/` directory per week. The stories root is
  the `stories/` directory alongside it.
- **Activity log:** `enabled` or `disabled`. Enabled only when there's a team or stakeholder to
  report to. Format and location are in the `activity-log` skill.
- **Calendar:** the calendar identity to read events from, or `disabled`.
- **Demo tracking:** the recurring meeting that counts as the demo, or `disabled`.

## README layout

Sections, in this order:

1. `# Week of <date>`
2. The Continues-from paragraph, immediately after the H1 and before any heading, worded
   exactly:
   `**Continues from:** `<previous week's archived path>`, which now serves as historical
   reference only, not updated further. This directory carries forward only the still-active
   items, self-contained (no need to open the previous week to follow anything below).`
   Only the path changes from week to week.
3. `## Recap Log`, present only once a recap has been written for the week (shape below).
4. `## Priority order`
5. `## Active items`, a table. When demo tracking is enabled, it has a `Demoed` column.
6. `## Queued for next demo`, only when demo tracking is enabled and something is queued.
7. `## Closed items (not carried forward — see previous directory for full history)`, a list.
   When demo tracking is enabled, each bullet carries an inline `Demoed <YYYY-MM-DD>` note once
   shown.

### Active items

Columns: `Item`, `Status`, `Next step`, plus `Demoed` when demo tracking is enabled. `Item` is a
short name with links to whatever tracks it (the story's `plan.md`, the PR, a topic doc).

### Workloop checkpoints

When a `weekly-tracking-config` memory exists, the workloop commands keep the current week's
README in step with the work, independent of the `Activity log` setting. At each checkpoint,
update the item's row, or add one if no row matches. Match by story slug, PR link, or plain name.

| Checkpoint | Status | Next step |
|---|---|---|
| `/story` approved | `story drafted` | `/plan` |
| `/plan` approved | `planned, 0/N slices` | first slice |
| `/slice` committed | `k/N slices done` | next slice, or UAT |
| PR opened | `PR open` (link in `Item`) | review/merge |
| Released by the repo's release skill | `released <ref>` | none |
| `/code-review` of someone else's PR | review outcome (posted / held / resolved outside this flow) | whose court it's in |

A review-of-someone-else's-PR item never gets shown at Demo Day in its own right, so when demo
tracking is enabled, `/code-review` sets `Demoed` to `N/A` at this same checkpoint, instead of
leaving it blank for week-rollover to chase down later.

A `released <ref>` item is finished, so it moves from Active items to Closed items instead of
staying as a row. A PR item moves to Closed once its merge is confirmed.

### `Demoed`

A date, filled in once the item has been shown to a stakeholder, in a meeting, async, or any
other form. Blank means not yet shown. Being finished and being demoed are independent facts.
`N/A` means the item type doesn't go through Demo Day at all (see the `/code-review` checkpoint
above) — distinct from blank, which means it does and just hasn't happened yet.

### Recap Log

```
## Recap Log

Creation time of each recap file (local machine time, with timezone), for the next
recap run to use as its cutoff — work after a given timestamp is not yet reflected in
that recap.

| File | Created |
|---|---|
| `recaps/weekly.md` | 2026-09-08 17:33 EDT |
```

One row per recap file. A rewrite later the same day appends `(updated HH:MM <tz>)` to the
existing row's `Created` cell rather than adding a second row.
