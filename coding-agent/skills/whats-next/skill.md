---
name: whats-next
description: Answers "what's next" by checking the current week's priority list and active items, and first runs a quick safety-net check for any of today's calendar events that haven't been captured yet. Use when asked "what next," "what should I work on," "what's on my plate," or to review current priorities.
---

# What's Next

The front door for starting a work session on this engagement. Two jobs, in order: catch any
uncaptured meeting from earlier today, then answer what to work on next from the current week's
tracker.

## Current Engagement Config

Resolve the calendar identity and weeks root from the `daily-recap-config` project memory. Log
format/location come from the `activity-log` skill.

## Step 1 — Fallback calendar check

List today's calendar events up through now (`list_events` on the configured calendar identity,
today's date, events that have already started). For each one, check whether today's activity log
(`docs/weeks/<monday>/log/<date>.md`) already has a `meeting`-tagged entry referencing it (title
match) or a placeholder entry for it (see the `activity-log` skill).

- **Already logged (real entry or resolved placeholder):** nothing to do, move on silently.
- **Not logged at all:** a genuine gap — invoke `meeting-notes` for it directly (actually walk
  through capturing it, don't just ask "did anything happen"). If the user says "not now" or
  defers, write the placeholder entry per the `activity-log` skill and move on without pressing
  further.
- **A placeholder already exists and is still unresolved:** don't re-ask about it again today —
  the placeholder is what suppresses repeat prompts within the same day. It's fair game to
  resurface on a later day's check if it's still sitting there, but that happens naturally
  through that day's own log file, no special handling needed.

**Silent when clean.** If every one of today's events-so-far already has a log entry, say nothing
about this step at all — don't report "checked calendar, all clear" as its own line, just move
straight to Step 2. The whole point is this costs nothing observable when there's no gap.

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
