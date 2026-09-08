---
name: week-rollover
description: Closes out the current week's tracker/recaps directory (archives it) and scaffolds the next week's directory in one action. Use when asked to close out the week, start a new week, or "roll over" to the next week.
---

# Week Rollover

Archives a finished week's directory and creates the next one, as a single combined
action — this is the week-boundary equivalent of the `daily-recap` skill's daily
cadence. A week's tracker docs, meeting notes, and recaps all live and move together
under a single `docs/weeks/<monday>/` directory. This skill is still being field-tested;
treat its shape as a draft, same as `daily-recap`, and update it directly when a real
run surfaces a gap.

## Confirming Items With the User

Several steps below ask the user to confirm a status or action on each of several
items — stories to archive (Step 3), active items in the freshness walk (Step 7). In
every such case: present one item, stop, and wait for the user's response before moving
to the next. Never lay out several items as a table or list in one message for blanket
approval — that shape invites breezing past something that actually changed, even when
an item's status looks obviously unchanged. "Obviously fine" is a guess about an item's
status, not a documented one.

## Current Engagement Config

Generic, like `daily-recap` — don't hardcode a path here. Resolve per the Project
Config Memory instructions in global `CLAUDE.md`, reading the same `daily-recap-config`
project memory `daily-recap` uses; the **weeks root** this skill operates on is that
path's `docs/weeks/` directory (the parent of the `<monday-of-that-week>/recaps/<date>.md`
output path documented there), and the **stories root** is that same engagement's
`docs/stories/` directory (a sibling of the weeks root).

## Step 1 — Identify the current (outgoing) week

List `<weeks root>/`, excluding the `archive/` subdirectory. There should be exactly one
remaining entry — the live week, named by its Monday date. If there's more than one
(an unusual state — a prior rollover may not have completed cleanly), stop and ask which
one is actually meant to close, rather than guessing.

## Step 2 — Pre-close checks

Don't archive a week that isn't actually ready to close — the source material for its
retrospective (the daily recaps) becomes harder to work with once it's sitting in
`archive/` rather than the live directory, so catch gaps now, not after the move.

- **Check for `recaps/weekly.md` inside the outgoing week.** If it's missing, stop and
  ask whether to build it now (via the `weekly-recap` skill) before continuing — don't
  silently archive a week with no retrospective, and don't silently build one without
  asking either, in case one is already in progress elsewhere.
- **Sanity-check that the week actually looks finished** — e.g. a daily recap exists for
  the most recent work day before today. If the outgoing week looks only partially
  through (rolling over mid-week, a short week, a holiday), ask for confirmation rather
  than assuming "close the week" always means every work day already happened.

## Step 3 — Archive completed stories

A story only moves to `docs/stories/archive/` at the next weekly kickoff, not
immediately on completion — even a same-day merge stays in the live `docs/stories/`
list until this step runs.

For every story under `<stories root>/` (excluding `archive/`):

1. **Verify merge status directly against git — don't trust the plan.md's own "done" or
   "merged" claim.** Resolve the repo's diff base per the Branching Model instructions
   in global `CLAUDE.md` (its declared integration branch, or trunk — not an assumed
   default branch), then run `git merge-base --is-ancestor <commit> origin/<diff-base>`
   for whatever commit the plan.md cites as the final one. A plan.md marking a slice
   "✅ done" means the implementation was finished in the coding workflow's own sense,
   not that it's merged — same distinction `daily-recap` already enforces for its own
   "shipped" language.
2. **Present each genuinely-merged story found one at a time, per the confirmation rule
   above, and confirm before moving.** Don't auto-archive silently — a story can be
   merged but still have an active, logged follow-up (e.g. a "pick this up once X
   unblocks" note) that means it's not actually done-done yet. Let the user make that
   call per story.
3. On confirmation: `mv <stories root>/<slug> <stories root>/archive/<slug>`.
4. **Grep-fix every reference to the old path across `docs/weeks/**/*.md`** (both the
   live week and any archived weeks — these are simple path substitutions, not content
   rewrites, so there's no reason to carve out an exception for historical weeks). Also
   check `docs/stories/**/*.md` for any sibling story referencing this one by path.
5. If nothing is left to move, say so — don't force this step to find something.

## Step 4 — Archive the week (the move)

```
mv <weeks root>/<outgoing-monday> <weeks root>/archive/<outgoing-monday>
```

One move. Everything inside — the tracker README, meeting notes, topic docs, and the
`recaps/` subdirectory — travels together, which is the entire point of having merged
the two trees into one.

**Still-active topic docs that move forward (Step 6) can leave dangling cross-tree
references behind in `docs/stories/**/*.md`.** A story's `plan.md` can cite a topic doc
by a path that embeds the week it was written in — once that doc travels forward to the
new week's directory in Step 6, the story's reference points at a location the file no
longer occupies. Grep every topic doc being moved forward (its bare filename is enough,
no need to match the full path) against `docs/stories/**/*.md`, not just
`docs/weeks/**/*.md`, and fix any hit to the new week's path. Same class of problem as
Step 3 above — just the reverse direction (a story citing a topic doc, instead of a week
citing a story).

## Step 5 — Determine the new week

Default to the Monday immediately following the outgoing week's Monday (i.e., 7 days
later) — this assumes back-to-back weeks with no gap. If today's date doesn't fall
within that new week (e.g. this rollover is happening late, or after a gap), say so and
ask which Monday to actually use rather than silently assuming continuity.

## Step 6 — Scaffold the new week (the create)

```
mkdir -p <weeks root>/<new-monday>/recaps
```

Seed `<weeks root>/<new-monday>/README.md` using the same section structure as the
outgoing week's README (`# Week of <date>`, `## Priority order`, `## Active items`,
`## Closed items (not carried forward — see previous directory for full history)`).

- **Active items** — carry forward every item from the outgoing README's own "Active
  items" that wasn't moved to "Closed items" there. This is the actual point of the
  "not carried forward" note on Closed items — everything else *is* expected to carry
  forward until it's explicitly closed out.
- **Priority order** — don't invent one, but don't just leave it blank and silently wait
  either: **ask directly whether the user wants a draft priority order now**, once the
  Active items list is settled. This is two-stage by design, not a one-shot fill-in — the
  point is to hand the user something to walk into the week's own planning meeting with
  (this rollover is meant to run before that meeting, as prep), then finalize/adjust it
  together afterward once real input from that meeting exists. If they say not yet, leave
  it blank and don't ask again unprompted this session. If they say yes, draft one from
  the carried-forward Active items, present it, and treat it as a draft until they
  explicitly finalize it (possibly in a later message, after their meeting happens).
- **Closed items** — always starts empty in a new week's README.
- **Physically move (not copy) every topic doc still referenced by a carried-forward
  Active item or heads-up** from the outgoing week's directory into the new one — a bare
  relative link (`[foo.md](foo.md)`) only resolves if the file is actually there. A doc
  tied to a now-Closed item, or a dated record of one specific past meeting (which never
  continues to be updated), stays behind in the archive and gets cited by explicit
  "see the previous directory's `X.md`" phrasing instead of a bare link — don't move
  those. After moving, verify every remaining link in the new README's rendered
  markdown actually resolves to a file that exists, and check the cross-tree
  consequence described in Step 4 above.

**Present the drafted new README before writing it** — same "present, don't just save"
principle `daily-recap` follows. This presentation is a structural check only (does the
carried-forward list and section shape look right), not a status check — don't read
approval of the whole draft as confirmation that any individual item's status is
correct. That confirmation only happens in the per-item walk in Step 7, which runs
regardless of how this draft presentation goes. Carrying forward the wrong items
(something that was actually resolved in conversation but never marked closed in the
doc, for instance) is exactly the kind of status-marker staleness `daily-recap` itself
already watches for in this same file — don't propagate a stale status into a fresh
week's file without a chance to catch it first.

## Step 7 — Walk each active item for a freshness check

Walk the new README's Active items one at a time, presenting the currently-recorded
status and asking whether it's still accurate. Not a formality — stale status claims
propagate silently otherwise.

- **Table order by default.** Walk items in the order they're already written, rather
  than reordering by assumed importance or recency. Deviate only when a specific item's
  correction has obvious, immediate bearing on another (e.g. two items share the same
  underlying bug or handoff claim) — in that case, resolve the connected items together,
  say explicitly that you're doing so out of table order, then return to where you left
  off.
- **A correction is rarely contained to the README row alone.** A stale status claim can
  propagate into multiple topic docs and a story's own plan.md, not just the README row
  where it was first caught. Once a correction surfaces, grep for the same claim
  elsewhere before considering the item resolved — a single-file fix that leaves other
  files still asserting the old, wrong status isn't a fix.
- **Verify against a primary source before accepting either party's recollection.**
  Don't overwrite a documented "not yet confirmed" status with a verbal claim without
  checking it — cross-check the story's own plan.md or the session's own saved
  artifacts first. Where a live check is actually possible to run directly (e.g. an
  unauthenticated endpoint, no session needed), just run it instead of relying on
  memory.
- **A story reaching genuinely-closed status mid-walkthrough triggers Step 3.** Don't
  wait for a second pass — if confirming an item's state reveals it's actually done and
  merged, archive it right then (with the user's confirmation), fix references, and
  continue the walkthrough from where it left off.
- **This step can surface real external escalations** (e.g. "this handoff has no
  official ticket, might not be getting real priority") — when it does, note the
  concrete next action (a specific meeting to raise it at, a person to ping) directly in
  the item's own "Next step" cell rather than leaving it as a vague to-do.
- **Consolidating several rows into one dedicated section is a legitimate outcome of
  this walkthrough, not just status corrections.** Several separate table rows can turn
  out to all be hard dependencies of one story, found during the item-by-item walk, not
  before it. When that happens, break the story out of the table into its own `###`
  heading with sub-bullets per dependency, keeping the remaining simple, single-line
  items in the table. Don't force this reorganization preemptively; do it when the
  walkthrough itself surfaces that several rows are really one story's dependencies
  wearing separate hats.
- **Verify a superficial pattern match actually supports the conclusion being drawn
  from it**, rather than treating string/keyword similarity as evidence on its own (e.g.
  a name containing a suggestive term isn't proof of the category it's being used to
  infer). More generally: a "gotcha" that requires stacking several inferences to
  contradict something the user stated plainly is much more likely a misunderstanding on
  this end than an actual catch — verify the inference chain itself before presenting it
  as a contradiction.
- **When corrected on an item's actual scope, don't try to reconcile with the prior
  version — start clean.** If prior speculation split one plainly-described issue into
  several inferred sub-issues that turn out wrong, delete the speculative version
  outright and write one plain restatement of the observed fact, with no inferred
  cause — don't try to merge or salvage the earlier, overcomplicated version.

## Step 8 — Sweep embedded open questions in active stories

Distinct from `daily-recap`'s own open-questions walk (scoped to that day's recap, run
daily since who's-blocking-whom changes daily) and from Step 7 above (walks whatever's
already summarized into the README): **this step checks a source neither of those ever
looks at** — a "Still open" or "Needs Architect: yes" callout sitting inside an active
story's own `plan.md` that never got summarized into any README row at all, and so would
otherwise never surface again once the blocker it referred to has cleared.

For every story under `<stories root>/` (excluding `archive/`): grep its `plan.md` for
"Still open," "Needs Architect: yes," and any "## Open Questions" heading. For each hit,
check whether subsequent events in the same file (or elsewhere) already overtook it —
same discipline as Step 7: verify against what the file itself says happened since,
don't just ask "is this still true" and accept a guess. Mark resolved-by-events ones
explicitly (don't just delete the question — note what changed and when, so the plan.md
retains a record of what was asked and how it was resolved). A story with nothing
stale here is a fine, common outcome — don't force a finding.

## Step 9 — Confirm

Report what moved and what got created — old week's path → its new archive path, the
new week's path, and any stories archived along the way — so it's easy to verify against
the actual directory listing.
