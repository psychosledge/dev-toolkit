---
name: standup
description: Builds standup talking points from the activity log since the last standup, grouped by work item in stakeholder-friendly language, then marks the covered entries with a log marker. Use when asked for a standup recap, standup prep, what to say at standup, or a recap of recent activity for standup.
---

# Standup

Turns raw activity-log entries into talking points to speak from at standup: net progress per
work item since the last standup, what's in motion now, and what's blocked, presented in chat.
The audience includes technical and non-technical stakeholders, so every line follows the
`stakeholder-language` skill.

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
README's Priority order and Active items for each item's current Status and Next step. For
each item the user is actively building, read its story's plan for the remaining slices in
order; Doing is built from them.

Log entries are live capture, not verified. Before a talking point says merged, shipped, or
done: resolve the diff base with the `branching-model` skill and check
`git merge-base --is-ancestor`, or the PR's actual state with `gh pr view`. Unverified means
saying where it actually stands, such as "PR open, awaiting review."

## Step 3 — Build the talking points

Present in chat only; no file is written. Shape:

```
Done:
- <Item label>: <net progress across the window>.

Doing:
- <Item label>: <the step in progress now, then the steps after it, in order>.

Blockers:
- None
```

The three headings are fixed: `Done:`, `Doing:`, `Blockers:`, in this order, every run. Done
covers everything since the last standup marker, however many days that spans; work already
logged today belongs in Done, never in Doing.

- **One bullet per work item under Done**, covering the net progress across all of its window
  entries.
- **Label every bullet** with the item's product name plus its Jira key, such as "Automatic
  retry for failed exports (ABC-123):", and use that same label for the item across Done and
  Doing.
- **First person singular** for the user's own work ("I confirmed ..."). "The team" is only
  for group decisions.
- Each bullet is one or two short sentences a person can say aloud, never a timeline. Describe
  what the work does for the product per the `stakeholder-language` skill, never the mechanics
  of producing it.
- A meeting entry earns a bullet only when it produced a decision or direction change; state
  the decision, never the attendance.
- **Reviews of someone else's PR:** one line per PR, naming the author and the PR number, with
  the fixed outcome phrase "reviewed". Example: "Portfolio charts (Jo's PR #42): reviewed."
  Multiple rounds in the window compress to the same single line, naming the count: "reviewed
  twice." Leave out review findings, comment counts, approval state and
  merge state; the author surfaces their own merge in their update. A log entry that only
  records someone else's PR merging, with no review work of the user's own in the window,
  earns no bullet.
- **Doing holds only the items the user is building**: in-flight code with the user's own next
  implementation step. Each bullet gives that step, then the steps after it from the story's
  plan (remaining slices in order), described in product language. A finished exploration held
  as reference, a coordination step (settling an approach with someone, sending asks, taking a
  proposal to another team), or a demo later in the week never earns a Doing bullet on tracker
  priority alone.
- **Blockers** is always present; when nothing is blocked it holds "- None". Waiting on a PR
  author's replies or a teammate's merge is normal flow. A blocker is something that stops the
  user's own work.

## Step 4 — Write the marker

After presenting, append to today's log file (creating it per the `activity-log` skill if
nothing has been logged yet today):

```
- HH:MM [standup] Standup recap generated; entries above covered.
```

HH:MM is the current time. Work logged after this line lands in the next standup's window. On
a same-day re-run (Step 1), update the existing marker's time in place.
