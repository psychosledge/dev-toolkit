---
name: weekly-recap
description: Builds a weekly recap (Things We Worked On / Things We Plan to Work on Next / an internal-only mood note) from the week's own daily recaps and tracked work. Use when asked to build the weekly recap, or to prep for a weekly status update.
---

# Weekly Recap

Builds a weekly rollup from a week's already-built daily recaps (see the `daily-recap`
skill) plus that week's tracked story/topic-doc activity. Keep it a plain,
self-contained engineering recap — the artifact's own placement inside that week's
`recaps/` directory, alongside the daily recaps it was built from, already establishes
what it covers and why. This skill is still being field-tested, same as `daily-recap`;
treat its shape as a draft and update it directly when a real run surfaces a gap.

## Current Engagement Config

Generic, like `daily-recap` and `week-rollover` — don't hardcode a path here. Read the
same project memory `daily-recap` uses (e.g. named `daily-recap-config`) for the **weeks
root** (the parent of `<monday-of-that-week>/recaps/<date>.md`). If no such memory
exists for the current project, ask the user directly, then offer to save it into the
same config memory the other two skills already read, so all three stay pointed at one
source of truth.

## Step 1 — Identify the target week

If a Monday date is given as an argument, use `<weeks root>/<that-monday>/`. Otherwise,
list `<weeks root>/`, excluding `archive/` — there should be exactly one remaining
entry, the current live week. Use that.

## Step 2 — Gather source material

**Primary: that week's own daily recaps.** Read every file in
`<weeks root>/<monday>/recaps/*.md` except `weekly.md` itself, in full. Don't re-derive
git/calendar/story status from scratch — the daily recaps already did that verification
(merge-status ladder, AC checks, etc.) on their own day. Trust what they say happened,
the same way this skill's own reader would.

**Secondary, for context:** that week's `README.md` (priority order, active items) and
any topic docs it links to — useful for knowing what's officially tracked/prioritized
so a bullet can be phrased against that framing, not just invented fresh.

**Light freshness check only.** Something reported mid-week as "PR open, awaiting
review" may have merged since. Spot-check anything a Worked-On or Next bullet would
otherwise get wrong (a quick merge-status check is enough), don't re-run a full
day-by-day verification pass — that's already been done once per day this skill is
built from.

**Note which days have no daily recap** (a day off, a day nobody ran `/daily-recap`).
Don't guess why; if it matters for framing (e.g. explaining a lighter week), ask the
user rather than assuming.

**Check the tail end of the prior week's last covered day, not just "is this new since
last week's recap."** The prior weekly recap was built at some point in the day it was
sent, not necessarily end-of-day — real work from after that cutoff never made it in
and is legitimate material for this week's recap even though it technically happened
during what reads as "last week." Confirm the actual cutoff with the user if unsure,
rather than assuming a whole day was already covered.

## Step 3 — Build "Things We Worked On" and "Things We Plan to Work on Next"

Single-sentence bullets, not paragraphs. Draw from the daily recaps' own Progress
sections and Standup Summaries, compressed further, not re-derived from raw commits.

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
friction plainly, using the same honest framing the daily recaps it's drawn from
already used. Concrete moments worth reaching for: being included in conversations
beyond the usual lane, a flagged dependency actually getting picked up and resolved on
the client side, responsiveness on both sides of PR review, a stakeholder being decisive
when checked in with, a deliberate move made *because* of something raised the prior
week (see Step 4). Every specific claim must trace to something an actual daily recap
said or the user just told you directly — never invent a plausible-sounding detail to
fill a narrative gap.

**Don't over-explain a structural fact the reader already has context for.** If a
detail's significance depends on a standing situation (e.g. no PM to check a decision
with in real time), state the concrete decision and let the significance sit there
implicitly, rather than spelling out the structural reason in the same sentence — the
target reader already has that context, and a daily recap already carries the more
literal accounting if it's ever needed.

## Step 6 — Persist and present

Write to `<weeks root>/<monday>/recaps/weekly.md`, no title beyond a bare `# Weekly
Recap`, no "covers <date range>" line — the file's own path, alongside that week's daily
recaps, already establishes what it covers. No per-section role header
(`**Engineering:**` or similar) either — this skill produces one person's own weekly
recap, not a merged multi-section document.

If `recaps/weekly.md` already exists for this week, read it first and treat this as a
revision, not a silent overwrite — the user may be iterating on a draft already in
progress.

**Present the full draft in the conversation before treating it as final**, the same
"present, don't just save" principle `daily-recap` follows. Field-testing note: expect
several rounds of correction on tone and framing before a draft is ready to finalize;
that's the normal shape of using this skill, not a sign something's wrong with it.

## Step 7 (optional, if the draft is later shared or published elsewhere)

If the user asks to check this draft against what actually went out: read the final
version and compare it line by line against the saved `weekly.md` draft — what survived
as-is, what got reworded, what got cut, what got added that wasn't in the draft at all.
Record the delta as a dated finding in whatever project memory tracks this project's
weekly-recap process, the same way other field-tested corrections are recorded. Goal:
converge this skill's own voice/scope/level-of-detail toward what actually survives
into whatever the user ends up doing with it.
