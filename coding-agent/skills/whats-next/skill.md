---
name: whats-next
description: Answers "what's next" by checking the current week's priority list and active items, and first runs a quick safety-net check for any of today's calendar events that haven't been captured yet. Use when asked "what next," "what should I work on," "what's on my plate," or to review current priorities.
---

# What's Next

The front door for starting a work session on this engagement. Two jobs, in order: catch any
uncaptured meeting from earlier today, then answer what to work on next from the current week's
tracker.

## Current Engagement Config

Resolve the weeks root, `Activity log`, and `Calendar` fields from the `weekly-tracking-config`
project memory (fields defined in the `weekly-tracking` skill). Log format/location come from the `activity-log` skill.

## Step 1 — Fallback calendar check

Skip this step silently unless `Calendar` is set and `Activity log` is `enabled`.

Starting from the most recent calendar event that started before now (`list_events` on the
configured calendar identity), walk backward event by event, checking each one against its own
day's activity log (`docs/weeks/<monday-of-the-week-containing-that-date>/log/<date>.md` —
resolve the week directory from the event's own date, not necessarily the current week) for a
`meeting`-tagged entry referencing it (title match) or a placeholder entry (see the `activity-log`
skill). Stop walking backward as soon as an event is found already logged — anything earlier is
presumably already covered by a prior run — or once the walk reaches 7 calendar days back,
whichever comes first. This is what catches every uncaptured meeting since the last one that was
logged, including the last meeting of a previous work day when today has no events yet (e.g.
running this first thing after a day off or a weekend).

For each unlogged event found along the way:

- **Not logged at all:** a genuine gap — invoke `meeting-notes` for it directly (actually walk
  through capturing it, don't just ask "did anything happen"). If the user says "not now" or
  defers, write the placeholder entry per the `activity-log` skill and move on without pressing
  further.
- **A placeholder already exists and is still unresolved:** don't re-ask about it — the
  placeholder is what suppresses repeat prompts. It counts as "logged" for the walk-back's
  stopping condition, so it also stops the walk from going further back; it stays visible in that
  day's own log history if still unresolved.

**Silent when clean.** If the most recent event already has a log entry, the walk stops
immediately, so say nothing about this step at all — don't report "checked calendar, all clear"
as its own line, just move straight to Step 2. The whole point is this costs nothing observable
when there's no gap.

**Don't run this for a session that isn't actually oriented around "what's next."** A quick
troubleshooting question or a one-off ask shouldn't get this check first — it's tied to the
specific intent of consulting the tracker to decide what to work on, not to session start in
general.

## Step 2 — Answer what's next

Read the current week's `README.md` (`## Priority order` and `## Active items`) and answer
directly from what's there — this skill doesn't re-derive priority itself, the README is already
the source of truth for that. If the priority order looks stale (references something already
closed, or a merge status has changed since it was drafted), say so rather than reciting it as-is,
but a full freshness pass belongs to a dedicated rollover step, not this skill — flag it, don't
re-litigate the whole tracker here.

For each Active item whose status is `PR open`, check whether the PR has merged (`gh pr view
<link> --json state` when the `pr-platform` skill resolves GitHub with `gh` available). If it
has, offer to move the item to Closed items per the `weekly-tracking` skill.
