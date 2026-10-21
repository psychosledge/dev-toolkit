---
name: activity-log
description: Reference for the shared activity-log format, location, and categorization taxonomy other skills use when they write or read log entries. Not normally invoked directly.
---

# Activity Log

Defines the append-only activity log this engagement's other skills write into and read
from, replacing end-of-day reconstruction with entries captured at the moment work
happens.

## Location

One file per day, inside the live unit: `<tracking root>/<live unit>/log/<date>.md`. See the
`tracking-config` project memory (fields defined in the `tracking` skill) for the tracking root
and how to find the live unit. To read a past day's log, glob `<tracking root>/**/log/<date>.md`,
which finds it in the live unit or the archive under any naming scheme. Entries are written only
when that config has `Activity log: enabled`. In release cadence with no live unit, ask whether
to start the next release per the `tracking` skill before writing. Create the
`log/` directory and file the first time an entry is written for a given day; don't pre-create
empty files for days with nothing logged yet.

## Entry format

One line per entry, appended in chronological order. This is a log, not a curated doc — a
correction gets a new entry, never a rewrite of an old one:

```
- HH:MM [tag] Description. (ref: link-or-slug)
```

- **HH:MM** — local time the entry was logged (not necessarily when the work happened, if logged
  slightly after the fact at the same checkpoint).
- **tag** — one of:
  - A bare domain tag: `backend`, `frontend`, `agent`, `infrastructure` — the user's own work.
  - `PR review - <domain>` — reviewing someone else's work, filed under the domain of what's
    being reviewed. A prefix, not a second independent axis — the two consistently travel
    together in practice (own work vs. reviewing someone else's), so no separate
    activity-type/domain split.
  - `meeting` — a calendar event. No domain tag even if the meeting was about a specific
    domain; the meeting itself is the unit.
  - No `full-stack` bucket. A story spanning repos gets one entry per repo (see Cross-repo
    below), each correctly domain-tagged, not one combined entry.
- **Description** — one line, plain language, what actually happened, not what's planned. For a
  meeting entry: a short pointer to the meeting's own topic/purpose, never attendance — the
  detail (decisions, feedback, follow-ups) belongs in the meeting notes doc, not restated here.
- **ref** — optional, a link or slug pointing at the shared story/topic doc/PR this entry belongs
  to. Required whenever an entry is one of several logged under the same underlying story;
  omit for a one-off item with nothing to link to.

## Domain tagging at log time

Infer the domain from context available at the checkpoint (repo, branch, files touched, the
meeting's own subject) rather than asking every time — asking every time reintroduces the ritual
this design exists to remove. Ask only when genuinely ambiguous. A rare question beats a silently
wrong tag, but a question on every entry defeats the point.

## Cross-repo story entries

A story spanning more than one repo (e.g. an API change and its UI consumer) gets one log entry
per repo, each correctly domain-tagged, cross-referenced to the same story/topic doc via the
`ref` field. Never invent a combined entry or a "full-stack" tag to cover it in one line.

## Consumers

Other skills write and read this log directly — see each skill's own file for how it uses these
entries. This file only defines the shared format those consumers depend on; it doesn't track
who they are, since that list changes independently of the format itself.

## Placeholder entries (surfaced, not yet resolved)

When something is surfaced (e.g. an uncaptured calendar event) and the user doesn't capture it
on the spot (defers, says "not now," or doesn't answer), write a placeholder rather than leaving
the gap silent:

```
- HH:MM [meeting] <event title> — flagged, not yet captured.
```

A placeholder's presence is what suppresses re-asking about the same event again later the same
day. It's a real log line, not a TODO comment — if it's still a placeholder days later, that's
visible directly in the log's own history, no separate tracking needed. When the event is
eventually captured for real, replace the placeholder line with the real entry rather than
leaving both.
