---
name: weekly-tracking
description: Reference for the weekly-tracking-config project memory and the weekly README layout that week-rollover, weekly-recap, meeting-notes, and whats-next read and write. Not normally invoked directly.
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

### `Demoed`

A date, filled in once the item has been shown to a stakeholder, in a meeting, async, or any
other form. Blank means not yet shown. Being finished and being demoed are independent facts.

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
