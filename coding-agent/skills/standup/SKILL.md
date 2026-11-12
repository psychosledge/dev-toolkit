---
name: standup
description: Builds standup talking points from the activity log since the last standup, grouped by work item in stakeholder-friendly language, then marks the covered entries with a log marker. Use when asked for a standup recap, standup prep, what to say at standup, or a recap of recent activity for standup.
---

# Standup

Turns raw activity-log entries into talking points to speak from at standup: net progress per
work item, what's next, and what's blocked, presented in chat. The audience includes technical
and non-technical stakeholders, so every line follows the `stakeholder-language` skill.

## Current Engagement Config

Read the `tracking-config` project memory (fields defined in the `tracking` skill) for the
tracking root and `Activity log`. The log is this skill's primary source; with
`Activity log: disabled` or no config, say so and stop.

## Step 1 — Resolve the window

Scan the live unit's `log/*.md` files newest-first for the most recent `[standup]` entry (see
the `activity-log` skill). If the unit rolled over since the last standup, continue into the
previous unit's log via the README's Continues-from path. The window runs from that entry's
timestamp through now. "The day before" is never the window: a standup covers everything since
the last one, which handles weekends, skipped standups, and same-morning work with no date
math.

- **No marker found anywhere:** first run on this project. Ask how far back to cover, once.
- **The most recent marker is from earlier today:** the user is iterating on the same standup.
  Rebuild the window from the marker before it (or the first-run ask), and in Step 4 update
  today's marker line in place rather than appending a second one.

## Step 2 — Gather

Read every log file the window touches, in full — including today's, which usually holds
same-morning entries that belong in the window. `[standup]` entries are markers, never
material. Group the rest by `ref`; entries with no ref stand alone. Read the live unit
README's Priority order and Active items for each item's current Status and Next step.

Log entries are live capture, not verified. Before a talking point says merged, shipped, or
done: resolve the diff base with the `branching-model` skill and check
`git merge-base --is-ancestor`, or the PR's actual state with `gh pr view`. Unverified means
saying where it actually stands, such as "PR open, awaiting review."

## Step 3 — Build the talking points

Present in chat only; no file is written. Shape:

```
Since <last standup day>'s standup:
- <Item>: <net progress since then>. <Where it stands now.>

Today:
- <top of the README's Priority order, with its Next step>

Waiting on:
- <anything blocked on someone else>
```

- One bullet per work item, covering the net progress across all of its window entries.
  Describe what the work does for the product per the `stakeholder-language` skill, never the
  mechanics of producing it.
- Each bullet is one or two short sentences a person can say aloud, never a timeline.
- A meeting entry earns a bullet only when it produced a decision or direction change; state
  the decision, never the attendance.
- `PR review - <domain>` entries compress to one line per PR, such as "reviewed the
  date-picker changes, now approved."
- "Today" comes from the tracker, never invented; keep it to the top one or two priorities.
- Omit "Waiting on" when nothing is blocked.

## Step 4 — Write the marker

After presenting, append to today's log file (creating it per the `activity-log` skill if
nothing has been logged yet today):

```
- HH:MM [standup] Standup recap generated; entries above covered.
```

HH:MM is the current time. Work logged after this line lands in the next standup's window. On
a same-day re-run (Step 1), update the existing marker's time in place.
