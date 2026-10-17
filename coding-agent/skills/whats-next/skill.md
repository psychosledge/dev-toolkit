---
name: whats-next
description: Answers "what's next" by checking the live tracker's priority list and active items, and first runs a quick safety-net check for any of today's calendar events that haven't been captured yet. Use when asked "what next," "what should I work on," "what's on my plate," or to review current priorities.
---

# What's Next

The front door for starting a work session on this engagement. Two jobs, in order: catch any
uncaptured meeting from earlier today, then answer what to work on next from the live unit's
tracker.

## Current Engagement Config

Resolve the tracking root, `Cadence`, `Backlog`, `Activity log`, and `Calendar` fields from the
`tracking-config` project memory (fields defined in the `tracking` skill). Log format/location come from the `activity-log` skill.

## Step 1 — Fallback calendar check

Skip this step silently unless `Calendar` is set and `Activity log` is `enabled`.

Call `list_events` with `eventType: ["DEFAULT"]` — this excludes `OUT_OF_OFFICE`/`FOCUS_TIME`/
`WORKING_LOCATION` blocks (lunch, focus time, etc.) up front, since those aren't meetings and
would otherwise force a `meeting-notes` invocation on your own calendar block. If the `Calendar`
field's stored value is a display name rather than a resolved calendar ID (email), resolve it once
via `list_calendars` and update the memory to store the ID directly, so future runs skip that
lookup.

Starting from the most recent (now-filtered) calendar event that started before now, walk backward
event by event, checking each one against its own day's activity log (found per the
`activity-log` skill from the event's own date, which may sit in an archived unit) for a `meeting`-tagged entry
referencing it (title match) or a placeholder entry (see the `activity-log` skill). Stop walking
backward as soon as an event is found already logged — anything earlier is presumably already
covered by a prior run — or once the walk reaches 7 calendar days back, whichever comes first.
This is what catches every uncaptured meeting since the last one that was logged, including the
last meeting of a previous work day when today has no events yet (e.g. running this first thing
after a day off or a weekend).

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

**Release cadence with no live unit:** nothing is in flight. When `Backlog` is set, read it and
suggest what to group into the next release, a single item or several meant to ship together.

Otherwise, read the live unit's `README.md` (`## Priority order` and `## Active items`) and answer
directly from what's there — this skill doesn't re-derive priority itself, the README is already
the source of truth for that. If the priority order looks stale (references something already
closed, or a merge status has changed since it was drafted), say so rather than reciting it as-is,
but a full freshness pass belongs to a dedicated rollover step, not this skill — flag it, don't
re-litigate the whole tracker here.

For each Active item whose status is `PR open`, check whether the PR has merged (`gh pr view
<link> --json state` when the `pr-platform` skill resolves GitHub with `gh` available). If it
has, offer to move the item to Closed items per the `tracking` skill.

In release cadence, when Active items is empty, or becomes empty after those moves, offer to
close out the release per the `tracking` skill.
