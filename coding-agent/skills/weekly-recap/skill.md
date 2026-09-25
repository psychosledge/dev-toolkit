---
name: weekly-recap
description: Builds a weekly recap (Things We Worked On / Things We Plan to Work on Next / an internal-only mood note) from the week's own activity log and tracked work. Use when asked to build the weekly recap, or to prep for a weekly status update.
---

# Weekly Recap

Builds a weekly rollup from that week's own activity log (see the `activity-log` skill)
plus that week's tracked story/topic-doc activity. Keep it a plain, self-contained
engineering recap — the artifact's own placement inside that week's `recaps/` directory
already establishes what it covers and why. This skill is still being field-tested;
treat its shape as a draft and update it directly when a real run surfaces a gap.

## Current Engagement Config

Generic — don't hardcode a path here. Resolve per the Project Config Memory instructions
in global `CLAUDE.md`, reading the `daily-recap-config` project memory, for the **weeks
root** (the parent of `<monday-of-that-week>/log/<date>.md`) — one config memory shared
across every skill that needs it, not a separate copy per skill.

## Step 1 — Identify the target week

If a Monday date is given as an argument, use `<weeks root>/<that-monday>/`. Otherwise,
list `<weeks root>/`, excluding `archive/` — there should be exactly one remaining
entry, the current live week. Use that.

## Step 2 — Gather source material

**Primary: that week's own activity log.** Read every file in `<weeks root>/<monday>/log/*.md`
(see the `activity-log` skill for format/location), in full, in chronological order. Each
entry's tag (a domain, a `PR review - <domain>` prefix, or `meeting`) tells building work from
review work from meeting content.

**Log entries are raw, live capture, not independently verified.** A log entry saying
"implemented X" carries no merge-status check. Before describing anything as
merged/shipped/done in this skill's own output, verify it directly: resolve the diff
base per the Branching Model instructions in global `CLAUDE.md`, then
`git merge-base --is-ancestor <commit> origin/<diff-base>` (or `gh pr list`/`gh pr view`
for a PR's actual state). If it isn't merged, say "PR open, awaiting review" or
"implemented, not yet merged," not "done" — this verification is this skill's own job.

**Secondary, for context:** that week's `README.md` (priority order, Active/Closed items,
and each item's own `Demoed` status, a column on Active items or an inline note on
Closed items) and any topic docs it links to. This is also the best source for a week
the log itself is thin or empty — the log is new, expect real gaps for a while — since
the README's own Active/Closed items already carry dated, status-checked history.

**Note gaps in the activity log** (a day with nothing logged at all). Don't guess why;
if it matters for framing (e.g. explaining a lighter week), ask the user rather than
assuming.

**Check the tail end of the prior week's last covered day, not just "is this new since
last week's recap."** The prior weekly recap was built at some point in the day it was
sent, not necessarily end-of-day — real work from after that cutoff never made it in
and is legitimate material for this week's recap even though it technically happened
during what reads as "last week." Confirm the actual cutoff with the user if unsure,
rather than assuming a whole day was already covered.

## Step 3 — Build "Things We Worked On" and "Things We Plan to Work on Next"

Single-sentence bullets, not paragraphs. Draw from the activity log's own entries and the
README's Active/Closed items, compressed further, not re-derived from raw commits from
scratch.

- **"Worked on" vs. "next":** something counts as worked-on only if real progress
  happened this week, even if unfinished (e.g. a fix planned to land same-day still
  counts as worked-on, not next). Something that only *became possible* this week (a
  blocker clearing) belongs in next, not worked-on, even if crediting the unblocking
  itself is tempting.
- **Don't list an activity that's just part of doing other listed work as its own
  bullet** (e.g. demoing shipped work isn't separate work from having shipped it).
- **Split compound bullets that are actually two distinct pieces of work.** Two
  bullets that happen to trace to the same day or the same PR review are still two
  bullets if they're separately meaningful accomplishments — don't force them into one
  just because they're related, and don't artificially split one single piece of work
  into two either.
- **Don't restate the same fact across both lists.** If a next-bullet is just the
  unfinished tail of something already described in worked-on, cut it — but a genuinely
  new piece of forward work that a worked-on item enabled (e.g. "the design is now
  approved" this week, "build it" next week) is a different fact, not a restatement.
- **Don't name who specifically something got handed off to** — say "prepped for hand
  off," not the person's name.
- **Trim redundant "client"-qualifier phrasing** — this whole artifact is client-facing
  work by construction, so "a client-raised request" reads redundant; drop the
  qualifier. Keep it when it's identifying an actual client-owned thing the sentence
  needs to name (e.g. "the client's new VPN"), not when it's just framing whose idea
  something was.
- **Rephrase "UAT" specifically for this artifact.** What gets called "UAT" internally
  on this engagement is usually the user's own local/pre-flight testing, not a
  stakeholder-involved acceptance pass — use "testing," "local testing," or "pre-flight"
  here instead, since an outside reader would assume the more formal meaning.
- **Verify claims that span the whole week before generalizing them** (e.g. "review
  moved fast in both directions" needs to actually be true across separate instances
  that week, not one instance stretched to sound like a pattern).
- **Don't round timeframes generously** — prefer the precise phrasing when it's just as
  short to write.
- **Check organization-name capitalization** stays consistent throughout (e.g. the
  client's name spelled correctly and consistently, not just however a source doc
  happened to write it).
- **No internal tooling jargon** — this project's internal workloop (`/plan`/`/slice`/
  `/code-review`, "architect"/"verifier," "Reviewer Mode," "workloop" itself, an internal
  slice number as the lead way of referring to a piece of work) means nothing to an
  outside reader. Describe work by what it actually is. `docs/stories/`, `plan.md`, "PR,"
  and "ADR" are fine — general engineering terms, not tooling-specific.
- **No em dashes** — split into two sentences instead.

## Step 4 — The callback question

Before drafting the mood paragraph: find the immediately preceding Monday's directory
under `<weeks root>/archive/` and read its own `recaps/weekly.md` mood section, if one
exists. Ask the user directly: **"Any callbacks to last week's mood note you want to
include — something that followed through, got resolved, or was a deliberate response
to it?"** Don't guess at a callback from the artifacts alone; this is exactly the kind
of connective, judgment-call material only the user actually knows (e.g. deliberately
sequencing a week's work around a concern raised the week before). If no prior week
exists yet, skip this question silently — there's nothing to call back to.

## Step 5 — Build the mood paragraph

Internal-only, one paragraph, about collaboration with the client, not technical
content — keep specific bugs/endpoints out of it, that's what the bullets above are
for. This is the one section that doesn't need to be diplomatic or softened; say real
friction plainly, in the same honest framing the activity log and README entries it's
drawn from already use. Concrete moments worth reaching for: being included in conversations
beyond the usual lane, a flagged dependency actually getting picked up and resolved on
the client side, responsiveness on both sides of PR review, a stakeholder being decisive
when checked in with, a deliberate move made *because* of something raised the prior
week (see Step 4). Every specific claim must trace to something the activity log, the README, or the user
just told you directly — never invent a plausible-sounding detail to fill a narrative
gap.

**Actively pull forward any positive quotes already captured** in the week's tracker doc
or the activity log (a reviewer's own words, a stakeholder's praise) and use them directly —
this is exactly the concrete texture this section wants, and re-describing the interaction
generically defeats the point of having captured the actual words live.

**Don't over-explain a structural fact the reader already has context for.** If a
detail's significance depends on a standing situation (e.g. no PM to check a decision
with in real time), state the concrete decision and let the significance sit there
implicitly, rather than spelling out the structural reason in the same sentence — the
target reader already has that context, and the activity log/README already carry the
more literal accounting if it's ever needed.

## Step 6 — Persist and present

Write to `<weeks root>/<monday>/recaps/weekly.md`, no title beyond a bare `# Weekly
Recap`, no "covers <date range>" line — the file's own path, alongside that week's
activity log, already establishes what it covers. No per-section role header
(`**Engineering:**` or similar) either — this skill produces one person's own weekly
recap, not a merged multi-section document.

If `recaps/weekly.md` already exists for this week, read it first and treat this as a
revision, not a silent overwrite — the user may be iterating on a draft already in
progress.

**Record the cutoff.** Immediately after writing (or re-writing) `weekly.md`, get its
actual creation/modification timestamp from the filesystem — don't estimate it — and
add or update its row in the `## Recap Log` table in that week's README (create the
section if it doesn't exist yet). This is what lets the next weekly-recap run's Step 2
"tail end of the prior week" check resolve the cutoff precisely instead of guessing.

**Present the full draft in the conversation before treating it as final** — don't just
save it and move on. Field-testing note: expect several rounds of correction on tone and
framing before a draft is ready to finalize; that's the normal shape of using this skill,
not a sign something's wrong with it.

## Step 7 (optional, if the draft is later shared or published elsewhere)

If the user asks to check this draft against what actually went out: read the final
version and compare it line by line against the saved `weekly.md` draft — what survived
as-is, what got reworded, what got cut, what got added that wasn't in the draft at all.
Record the delta as a dated finding in whatever project memory tracks this project's
weekly-recap process, the same way other field-tested corrections are recorded. Goal:
converge this skill's own voice/scope/level-of-detail toward what actually survives
into whatever the user ends up doing with it.
