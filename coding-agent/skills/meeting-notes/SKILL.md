---
name: meeting-notes
description: Captures a meeting's purpose, decisions, and feedback live, during or immediately after it happens, into that day's Meeting Notes doc and the activity log. Use when the user wants to brain-dump a meeting, start "meeting notes" or "notes mode," or capture what just happened in a call.
---

# Meeting Notes

The primary mechanism for capturing meeting content — live, during or right after
the meeting, instead of end-of-day reconstruction. Deliberately lightweight: the point is zero
reconstruction cost, not a polished document.

## Current Engagement Config

Resolve the tracking root, `Activity log`, `Calendar`, and `Demo tracking` fields from the
`tracking-config` project memory (fields defined in the `tracking` skill) per the Project Config Memory instructions in global
CLAUDE.md. Entry format and location for the activity log come from the `activity-log` skill.

## Step 1 — Identify the meeting

If the user names the meeting, use that. If `Calendar` is `disabled`, ask which meeting this is.
Otherwise, check the calendar (`list_events` on the configured calendar identity) for whichever event is happening now or ended within roughly the
last hour — don't ask "which meeting" if there's only one plausible candidate. If more than one
plausible candidate exists (back-to-back meetings, or it's been a while since the last one
ended), ask which one this is for.

## Step 2 — Capture, don't classify

This is live, one-meeting-at-a-time capture; attendance doesn't matter, and none of the
OOO/decline/attendee-list classification rules a written recap-style artifact might use apply
here. Ask directly, in plain language:

- What was this meeting actually about?
- What got decided, or what guidance/feedback came out of it?
- Anything that needs to be raised or followed up on because of it?

Take what the user gives as-is — this is their own brain dump, not a document to interrogate or
verify against other sources. If they're mid-meeting and typing fast, keep questions minimal and
let them lead; don't turn this into an interview if they're just dumping notes.

Treat the meeting as still in progress across multiple messages by default. A message is one
more increment of capture, not a signal the meeting ended — don't wrap up, summarize as final,
or stop tracking the meeting until the user explicitly says it's over (or a new meeting starts).

## Step 3 — Write the notes doc

Find the live unit per the `tracking` skill. In release cadence with no live unit, ask whether to
start the next release per the `tracking` skill, and otherwise ask where to write. Write to
`<live unit>/meetings/<date> - <exact calendar event summary>.md`, matching the
event's own title exactly. If no calendar event was found (a meeting outside the tracked
calendar, or the user is capturing something informal), use whatever title they give it. All of a
unit's meeting notes live as flat files under that single `meetings/` directory, not one
subdirectory per meeting.

If a notes doc already exists for this meeting — whether it's a later increment of the same
in-progress meeting or a separate capture session resuming after being interrupted — append to it
rather than overwriting.

## Step 4 — Log it

Skip this step if `Activity log` is `disabled`.

Append one `meeting`-tagged entry to today's activity log (see the `activity-log` skill for
format and location) at the same time the notes doc is written — a one-line summary of what the
meeting was about, with a `ref` pointing at the notes doc. This is the checkpoint that gets the
meeting into the log without a separate logging step.

If this capture resolves a placeholder entry written earlier for this same meeting, replace the
placeholder line with the real entry rather than leaving both — the placeholder's whole job was
to mark "seen, not yet resolved," which is now resolved.

## Step 4b — If this is the demo meeting, update Demoed status

Skip this step if `Demo tracking` is `disabled`. Otherwise, if the meeting just captured matches
the configured demo meeting, update `Demoed` status directly.

Look at the live unit's README `## Active items` table and `## Closed items` list for
rows/bullets with `Demoed` blank, plus any `demo-prep-*.md` plan written in the live unit since
the last demo, and ask directly: "Which of these got shown or discussed in this demo?" For each
one confirmed: fill in today's date on that row/bullet directly, in whichever README holds it,
live or archived (in the `Demoed` format the `tracking` skill defines for Closed items, or the table
column for Active items). Don't ask about rows that already have a `Demoed` date — only
the open ones.

## Step 5 — Nothing to present

There's no draft to review before saving — the notes doc and log entry are the direct product of
what the user just said, not a compressed or reinterpreted artifact.
