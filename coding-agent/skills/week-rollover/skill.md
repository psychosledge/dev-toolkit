---
name: week-rollover
description: Closes out the current week's tracker/recaps directory (archives it) and scaffolds the next week's directory in one action. Use when asked to close out the week, start a new week, or "roll over" to the next week.
---

# Week Rollover

Archives a finished week's directory and creates the next one, as a single combined
action. A week's tracker docs, meeting notes, and recaps all live and move together
under a single `docs/weeks/<monday>/` directory.

## Confirming Items With the User

Several steps below ask the user to confirm a status or action on each of several
items — not-yet-demoed hits (Step 3), stories to archive (Step 4), active items in the
freshness walk (Step 8). In every such case: present one item, stop, and wait for the
user's response before moving to the next. Never lay out several items as a table or
list in one message for blanket approval — that shape invites breezing past something
that actually changed, even when an item's status looks obviously unchanged. "Obviously
fine" is a guess about an item's status, not a documented one.

## Current Engagement Config

Generic — don't hardcode a path here. Resolve per the Project Config Memory instructions
in global `CLAUDE.md`, reading the `weekly-tracking-config` project memory (fields defined in the `weekly-tracking` skill) for the **weeks root** (the directory
holding one `<monday-of-that-week>/` directory per week) and the `Activity log` and
`Demo tracking` fields. The **stories root** is the `stories/` directory alongside it.

## Step 1 — Identify the current (outgoing) week

List `<weeks root>/`, excluding the `archive/` subdirectory. There should be exactly one
remaining entry — the live week, named by its Monday date. If there's more than one
(an unusual state — a prior rollover may not have completed cleanly), stop and ask which
one is actually meant to close, rather than guessing.

## Step 2 — Pre-close checks

Don't archive a week that isn't actually ready to close — the source material for its
retrospective becomes harder to work with once it's sitting in `archive/` rather than
the live directory, so catch gaps now, not after the move.

- **Check for `recaps/weekly.md` inside the outgoing week.** If it's missing, stop and
  ask whether to build it now (via the `weekly-recap` skill) before continuing — don't
  silently archive a week with no retrospective, and don't silently build one without
  asking either, in case one is already in progress elsewhere.
- **Sanity-check that the week actually looks finished** — e.g. the activity log (if
  enabled) has entries through the most recent work day before today. If the outgoing week looks only
  partially through (rolling over mid-week, a short week, a holiday), ask for
  confirmation rather than assuming "close the week" always means every work day already
  happened.

## Step 3 — Check for not-yet-demoed work

Skip this step if `Demo tracking` is `disabled`. The new week's README then has no
`Demoed` field and no `## Queued for next demo` section.

`Demoed` is a field directly on each Active/Closed item's own row or bullet in the
*outgoing* week's own README, not a separate file. An archived week's directory already
survives intact, so this status doesn't need a home outside the week to avoid being
lost — it just needs to be carried forward correctly when the item itself isn't done
being tracked yet.

**Ask first, don't assume blank means unshown.** Before walking the outgoing README's
items, ask directly: "Anything get demoed or otherwise shown to a stakeholder this week
that isn't marked yet?" Apply anything the user reports before the per-item walk below.

Then walk every Active item row and every Closed item bullet in the outgoing README for a
`Demoed` field that's blank. For each hit:

1. **Confirm with the user it's still accurate.** The upfront question above may not have
   surfaced every case — don't assume `Demoed` is genuinely still blank just because the
   row says so.
2. **If still unshown, note it** for Step 7 to carry into the new week's
   `## Queued for next demo` section — regardless of whether the underlying item is fully
   done and otherwise headed for Closed items or Step 4's archiving. Being finished and
   being demoed are independent facts; an item that would otherwise just disappear from
   the new README (a normal closed item) still needs this explicit carry-forward if it
   hasn't been shown yet.
3. **If confirmed shown, fill in the `Demoed` date on that row now**, in the outgoing
   README, before it archives.

No hits is a fine, common outcome — don't force a finding, and don't invent one from an
item that merely finished late in the week without an actual demo — in a meeting,
async, or any other form — separating it from whenever it gets shown.

## Step 4 — Archive completed stories

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
   not that it's merged. A rebase or squash before merge can rewrite the cited commit's
   SHA entirely — if the cited hash isn't an ancestor, don't conclude "not merged" on
   that alone; check the PR's actual state (`gh pr view`) and/or search
   `git log origin/<diff-base>` by branch name or PR number before ruling it unmerged.
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

## Step 5 — Archive the week (the move)

```
mv <weeks root>/<outgoing-monday> <weeks root>/archive/<outgoing-monday>
```

One move. Everything inside — the tracker README, meeting notes, topic docs, and the
`recaps/` subdirectory — travels together.

**Still-active topic docs that move forward (Step 7) can leave dangling cross-tree
references behind in `docs/stories/**/*.md`.** A story's `plan.md` can cite a topic doc
by a path that embeds the week it was written in — once that doc travels forward to the
new week's directory in Step 7, the story's reference points at a location the file no
longer occupies. Grep every topic doc being moved forward (its bare filename is enough,
no need to match the full path) against `docs/stories/**/*.md`, not just
`docs/weeks/**/*.md`, and fix any hit to the new week's path. Same class of problem as
Step 4 above — just the reverse direction (a story citing a topic doc, instead of a week
citing a story).

## Step 6 — Determine the new week

Default to the Monday immediately following the outgoing week's Monday (i.e., 7 days
later) — this assumes back-to-back weeks with no gap. If today's date doesn't fall
within that new week (e.g. this rollover is happening late, or after a gap), say so and
ask which Monday to actually use rather than silently assuming continuity.

## Step 7 — Scaffold the new week (the create)

```
mkdir -p <weeks root>/<new-monday>/recaps
```

Seed `<weeks root>/<new-monday>/README.md` with the README layout from the `weekly-tracking`
skill, with the outgoing week's archived path in the Continues-from paragraph.

Don't carry the outgoing README's `## Recap Log` section forward, and don't seed an empty one.

- **Active items** — before drafting anything, split the outgoing README's own "Active
  items" (everything not already moved to "Closed items" there — that's the actual
  point of the "not carried forward" note) into two buckets:
  1. **Genuinely open** — its own "Next step" cell describes real remaining work (not
     "None"/"Done"). Draft these directly into the new Active items table; they need
     real attention in Step 8 regardless.
  2. **Looks fully resolved** — Status already reads Done/merged and there's no real
     next step left. Do **not** draft these into the table at all. Hold them as a
     separate list to run through Step 8's confirmation first — most of these will turn
     out to just move to Closed or disappear, and writing them into the file only to
     edit them back out again is wasted motion (see Step 8's batching note).
  Bucket 2 still gets the same one-at-a-time confirmation discipline as bucket 1 — this
  split is about when something touches the file, not about skipping scrutiny.
- **Queued for next demo** — populate directly from Step 3's confirmed-still-unshown
  items. Include an item here even if it's also fully closed out below or archived in
  Step 4 — this section tracks "has it been shown," a separate question from "is it
  done." Omit the section entirely if Step 3 found nothing.
- **Priority order** — always draft one from the carried-forward Active items once that
  list is settled, don't ask whether to. This is two-stage by design, not a one-shot
  fill-in — the point is to hand the user something to walk into the week's own planning
  meeting with (this rollover is meant to run before that meeting, as prep), then adjust
  it together afterward once real input from that meeting exists. It's the real priority
  list from the moment it's written, not a placeholder — updates from the planning
  meeting or over the course of the week are normal drift, the same as any other Active
  item, not a special unfinalized state that needs calling out in the doc itself.
  Don't fold PR-review items awaiting the user's own response into this numbered list —
  they surface too often and clear too quickly to hold a fixed rank; carry them forward
  in Active items (or a dedicated callout, if the user has directed one to exist) with a
  plain note that they take priority over the numbered list whenever one is actually
  open, distinct from a PR review sitting in someone else's court (that's background,
  not urgent).
- **Closed items** — always starts empty in a new week's README, and stays empty at
  scaffold time — Step 8 is what may add to it, not this step. When Step 8 confirms an
  item is genuinely finished, it belongs here only if something else *in this same new
  README* still needs a live pointer to it — in practice, almost always because it's
  also referenced from `## Queued for next demo` (which necessarily outlives the item's
  own row once that row is gone). Having an archived story behind it (Step 4) is not by
  itself a reason to add an entry — most archived stories need no further mention here
  at all once their work is done, because nothing else in the new README depends on
  pointing back to them. A finished item that nothing else here still points to just
  disappears from the new README entirely; the previous archived directory already has
  the full record.
- **Physically move (not copy) every topic doc still referenced by a carried-forward
  Active item or heads-up** from the outgoing week's directory into the new one — a bare
  relative link (`[foo.md](foo.md)`) only resolves if the file is actually there. A doc
  tied to a now-Closed item, or a dated record of one specific past meeting (which never
  continues to be updated), stays behind in the archive and gets cited by explicit
  "see the previous directory's `X.md`" phrasing instead of a bare link — don't move
  those. The same applies to a doc that's purely reference material with no active work
  item attached to it, even if the topic it covers is still technically unscoped —
  confirm with the user whether a given topic doc is meant to move or stay when it's
  ambiguous, rather than defaulting to "still mentioned in Active items, so it moves."
  After moving, verify every remaining link in the new README's rendered markdown
  actually resolves to a file that exists, and check the cross-tree consequence
  described in Step 5 above.

**Present the drafted new README before writing it.** At this point the file only
contains bucket 1 (genuinely open items) plus whatever else Step 3/6 already settled;
bucket 2 hasn't been written anywhere yet. This presentation is a structural check only
(does the carried-forward list and section shape look right), not a status check —
don't read approval of the whole draft as confirmation that any individual item's status
is correct. That confirmation happens in the per-item walk in Step 8 (covering both
buckets), which runs regardless of how this draft presentation goes. Carrying forward
the wrong items (something that was actually resolved in conversation but never marked
closed in the doc, for instance) is exactly the kind of status-marker staleness worth
catching before it propagates — don't propagate a stale status into a fresh week's file
without a chance to catch it first.

## Step 8 — Walk each active item for a freshness check

Walk bucket 1 (already in the drafted README) and bucket 2 (held back from Step 7, not
yet written anywhere) one item at a time, presenting the currently-recorded status and
asking whether it's still accurate. Not a formality — stale status claims propagate
silently otherwise.

- **Batch the file edits, not the confirmations.** Confirming an item in chat doesn't
  require touching the live README for that single row right away. Accumulate each
  item's resolved disposition (stays active as drafted / needs corrected text / moves to
  Closed / drops entirely) as the walk proceeds, then apply them in one consolidated
  edit per file (README, plan.md, topic doc) at the end of the walk rather than one edit
  per row per confirmation. The one-at-a-time discipline governs the conversation; it
  says nothing about write cadence, and writing-then-immediately-rewriting the same row
  is pure overhead.
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
- **A story reaching genuinely-closed status mid-walkthrough triggers Step 4.** Don't
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
- **Section-level shape check.** The per-item walk above only ever looks at
  Active-items rows — it won't catch a whole *section* that's degraded into freeform
  prose. Separately from the per-item walk, look at each top-level section of the
  drafted new README and ask whether it's shaped as terse, scannable rows/bullets (fine,
  however many there are) or as a paragraph that has to be read start to finish to get
  the point (a sign it belongs in its own topic doc, or a link to an existing
  authoritative source like a story's `plan.md` or an ADR). This is a shape check, not a
  length check — a long Priority order list is fine; a short narrative paragraph is not.
  Flag a violation for a judgment call rather than automatically rewriting it — some
  short, one-off status notes are legitimately narrative and don't need their own topic
  doc.

## Step 9 — Sweep embedded open questions in active stories

Distinct from Step 8 above (which only walks whatever's already summarized into the
README): this step checks a source Step 8 never looks at — a "Still open" or "Needs
Architect: yes" callout sitting inside an active story's own `plan.md` that never got
summarized into any README row at all, and so would otherwise never surface again once
the blocker it referred to has cleared.

For every story under `<stories root>/` (excluding `archive/`): grep its `plan.md` for
"Still open," "Needs Architect: yes," and any "## Open Questions" heading. For each hit,
check whether subsequent events in the same file (or elsewhere) already overtook it —
same discipline as Step 8: verify against what the file itself says happened since,
don't just ask "is this still true" and accept a guess. Mark resolved-by-events ones
explicitly (don't just delete the question — note what changed and when, so the plan.md
retains a record of what was asked and how it was resolved). A story with nothing
stale here is a fine, common outcome — don't force a finding.

## Step 10 — Confirm

Report what moved and what got created — old week's path → its new archive path, the
new week's path, any stories archived along the way, and anything carried into
`## Queued for next demo` — so it's easy to verify against the actual directory listing.
