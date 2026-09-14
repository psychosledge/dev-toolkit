---
name: daily-recap
description: Generates a daily work recap (progress, friction, untracked work, open questions, calendar) for this client engagement, which has no sprint board and no dedicated PM. Use when asked to generate a daily recap, work summary, or "what did I do today/yesterday."
---

# Daily Recap

Builds a single day's work recap — the substitute artifact for a sprint board /
PM-tracked status on this engagement, giving Bo's own leadership visibility into effort
and hurdles. This skill is still being field-tested; don't treat any one run's shape as
final, and prefer asking the user over guessing whenever a signal is ambiguous.

## Current Engagement Config

This skill is generic — the facts it needs (scan root, calendar identity, output
location, demo cadence, org roles) are specific to whichever engagement it's being run
for, and none of them belong hardcoded here. Resolve them per the Project Config Memory
instructions in global `CLAUDE.md`: a `daily-recap-config` project memory holding scan
root / calendar identity / output location / demo cadence (which recurring meeting
counts as "the demo," and how often it runs), plus a separate org-roles memory (who's a
PM, who's a client stakeholder, who owns what — these change as people roll on/off an
engagement, so they belong in memory, not here).

Everything below refers back to those four config values plus the org-roles memory;
nothing else in this skill should hardcode a path, calendar name, or org fact directly.

## Setup

- **Target date:** parse from the skill arguments if given (`YYYY-MM-DD`), otherwise use
  today.

## 1. Git activity (secondary/cross-check signal)

Enumerate git repos under the scan root (see Current Engagement Config above):

```
find <scan root> -maxdepth 3 -type d -name .git
```

For each one, run:

```
git log --all --author="$(git config user.name)" --since="<date> 00:00:00" --until="<next-date> 00:00:00" --pretty=format:"%H|%ad|%s" --date=iso
```

Collect everything found. Treat this as a cross-check and an untracked-work detector —
not the primary source of what the day was about (see below for why).

**Check whether every commit found is actually merged before saying so anywhere in the
recap.** A commit existing is not evidence it shipped. Resolve the diff base per the
Branching Model instructions in global `CLAUDE.md`, then check with:

```
git merge-base --is-ancestor <hash> origin/<diff-base> && echo MERGED || echo NOT-MERGED
gh pr list --state all --search "<hash>"   # or --head <branch> — is there a PR, and what state
```

Use this status ladder, and never round up to a higher rung than what's actually true:
- **Merged** — the commit is an ancestor of the resolved diff base. This is the *only*
  status that gets to use the words "shipped" or "done."
- **PR open** — a pull request exists but isn't merged yet. Say "PR open, awaiting
  review/merge," not "done."
- **Implemented, not yet merged** — commits exist on a feature/local branch, no PR
  open yet. Say exactly that — not "shipped," not "done," not "completed."
A story's own `plan.md` marking a slice "✅ done" refers to that slice's *implementation*
being complete in the coding workflow's own sense (code written, tests pass, committed)
— it is not evidence of merge status and must not be translated directly into
"shipped"/"done" without independently checking the ladder above.

**Read the full commit body, not just the subject line, for every commit you're about
to cite as evidence of a specific piece of work.** A single commit can bundle two
genuinely separate, separately-creditable pieces of work under a subject line that only
describes one of them. For every commit surfaced in step 1, run:

```
git show -s --format="%B" <hash>     # full multi-paragraph message, not just %s
git show --stat <hash>                # file-level scope
```

The full body is often enough by itself. If the file-stat scope spans clearly distinct
areas and the message doesn't clearly account for all of them, that's a signal to look
at the actual diff before deciding this is one piece of work rather than several — but
don't do a full line-by-line diff read of every commit by default; the message body
plus file-stat scope is the "quick" version of this check, and is usually enough.

## 2. Story plan mining (primary signal)

Find every `docs/stories/<slug>/plan.md`, in both locations:
- top-level, untracked: at the root of the engagement's untracked docs directory (the
  same one the weekly directories in Current Engagement Config's output location live
  under) — i.e. `<that docs dir>/stories/*/plan.md`
- per-repo, git-tracked: `<repo>/docs/stories/*/plan.md`, for each repo under the scan
  root

For git-tracked ones, check `git log -p` / `git diff` for changes landing on the target
date. For untracked ones there's no diff history at all — **check file mtime for
"modified since the last recap run," not just a text grep for the target date.** A file
edited today can contain content self-dated to an earlier day, because that's when the
underlying conversation happened, not when the file was edited — a grep for today's
date string would miss it. Use mtime to find what changed, then read the dateline
inside to understand when the underlying event actually happened.

**This is the primary source, not git log.** A quiet git log day is not proof of a
quiet work day — real substance can live entirely in a plan.md's dated annotations and
land there before it's ever committed.

Also collect any still-unresolved "**Needs Architect:**" or "Open Assumptions Flagged
for Approval" callouts, regardless of whether they were touched on the target date —
these feed the "In my way" bucket below, when they genuinely name an external party (see
that section for the distinction between a real external dependency and the user's own
undecided call). **Check two places, not just `docs/stories/`:** every
currently active story's `plan.md`, and every topic doc's own "Open Questions" section
(see below) — a pre-story investigation doc (e.g. a not-yet-storified bug writeup) can
carry open questions of its own before anything graduates to `docs/stories/` at all.

**There is no standalone `open-questions.md` file.** Open questions live inside
whatever document they're actually about — a story's own `plan.md`, or a topic doc's
own "Open Questions" section — updated in place and removed (not just marked resolved)
once answered, the same convention `TECH_DEBT.md` uses. Don't go looking for a separate
open-questions artifact; if a topic doc has no "Open Questions" section, it has none
outstanding.

**Always list the whole untracked docs directory, not just `docs/stories/`.** The
untracked docs directory nests by week: `docs/weeks/<monday-of-that-week>/` holds that
week's own tracker doc (a blanket to-do list, not a sprint board — see Current
Engagement Config) plus every topic doc and self-documenting artifact from that week —
including a `/code-review` findings doc (`<date> - Review - <repo> PR #<n>
(<title>)/findings.md`) or meeting notes (`<date> - Meeting Notes - <title>/notes.md`)
nested inside the week they actually happened in, not flat at the docs root. To find the
right week for the target date: list `docs/weeks/`, compute each entry's date range
(that Monday through the following Sunday), and use whichever range contains the target
date — archiving a closed week and scaffolding the next one is a dedicated skill's job
(see the week-rollover skill), not something this skill does. Once you've found the
right week directory, list its full contents and read anything relevant in full —
except its own `recaps/` subdirectory, which is this skill's own daily and weekly
output (`docs/weeks/<monday>/recaps/`), nested inside the same directory as the topic
docs it mines — treat that one subdirectory as output, not source, so a prior day's
recap doesn't get re-mined as if it were new topic-tracking content. Don't
pattern-match on the specific examples above otherwise — naming conventions for what
shows up here aren't fully predictable in advance. These docs can go stale exactly like
plan.md does (an item marked "still open" may have been resolved days later in
conversation, not by editing the doc) — cross-check against what the user tells you in
step 4, don't take the doc's own status markers as final.

**A rich pre-planning artifact existing doesn't mean there's no friction to report.**
Some assigned work traces to genuinely deep investigation docs that are explicitly
pre-`/story` triage, not nothing — but the real friction can still be that items stall
there and never graduate to a scoped story with acceptance criteria, because no one is
doing that graduation work. Report it that way — "rich investigation exists, but
nothing has turned it into a scoped story" — rather than either "no artifact exists"
(wrong) or "this is fully tracked" (also wrong).

**Some artifacts may exist in systems this skill can't read at all** (e.g. a Slack
Canvas) — if the user mentions one, note that it exists and that this recap can't see
it, rather than silently omitting the fact that a real tracking document exists
somewhere outside this skill's reach.

## 3. Calendar

Use the Google Calendar MCP tools (`list_events` on the calendar identity from Current
Engagement Config above) for the full target date. Apply these rules exactly; they
exist specifically to avoid noise and to avoid leaking personal detail that isn't
reliably scrubbed at the source:

**Cross-reference meeting notes docs against calendar events by title match.** A
meeting-notes doc found while listing the week's directory (step 2 above) is named
`<date> - Meeting Notes - <exact calendar event summary>.md`. When both a calendar event
and a matching notes doc exist for the same date, treat them as the same meeting and
merge: the calendar event gives exact time/attendees/organizer, the notes doc gives what
actually happened. Don't just list them as two separate line items. Don't assume a
meeting notes doc exists for every calendar event or vice versa; match by title when
both are present, don't require it.

- `eventType == OUT_OF_OFFICE` **and** has a `recurringEventId` → exclude entirely.
  Routine recurring time off is noise, not a line item.
- `eventType == OUT_OF_OFFICE` **and no** `recurringEventId` (one-off) → include, but
  generically as **"OOO"** with only the time span. Never surface the event's real
  title — a personal, one-off block's title is not reliably generic at the source, so
  the scrub happens here, not by asking the user to rename calendar events.
- No `attendees` array at all → a generic time-block: title + duration only, nothing
  else. This is a known, deliberate pattern — a same-titled placeholder can block time
  on a client-visible calendar while the real meeting's details live on a separate
  calendar this skill can't see. Don't treat it as an anomaly worth a question.
- The user's own `responseStatus` is `declined` → exclude entirely. They didn't attend,
  so it shouldn't read as time spent. **Check the attendee entry with `"self": true`
  specifically**, not one that merely looks like the user — a calendar can list a
  similar-looking address as declined while the actual `self`-flagged entry (the
  account the calendar belongs to) shows accepted. Excluding based on any
  look-alike entry instead of the real `self` one would wrongly drop a meeting they
  attended.
- A meeting with a large attendee list (rough threshold: more than ~10) → summarize as
  a count plus one-line description (e.g. "company-wide demo session, ~28 attendees")
  rather than listing every name — the point is a 10-second-glance recap, and a wall of
  names defeats that for an all-hands-style event. Small/medium meetings still get a
  full attendee list.
- Otherwise → a real meeting: title, start time + duration, attendee list (names/emails
  only). Never include accept/decline/no-response status for *other* attendees — that's
  not part of the goal. Never include Zoom/meeting join links or dial-in passwords in
  the written recap, even though they're present in the raw event description.

**If the target date's calendar includes the configured demo event** (see Current Engagement
Config's demo cadence fact), record its end time — this feeds the Progress step's "not yet
demoed" tagging below. A day with no demo event needs no such cutoff.

**RSVP status is not proof of attendance — do a quick pass with the user before
finalizing Calendar.** An event classified as attended (accepted, no decline) can
still be one the user didn't actually attend — e.g. it overlapped their own OOO block
and they sent a written update instead. The calendar API only reports whether they
*responded* accepted, not whether they actually *showed up*; nothing in the raw data
distinguishes the two. Once the day's events are classified, list them back to the
user in one consolidated question (not the full one-at-a-time treatment Friction and
"In my way" get below — this is a single lightweight check, not a per-item
interview) and ask if anything needs correcting: a meeting they didn't actually attend
despite accepting, one where they gave an update async instead of showing up, or any
other note worth folding in. Apply corrections before writing the section, not after.

## 4. Build the recap

Sections, in this order:

### Standup Summary
**Goes first, above everything else.** The rest of this doc is reference detail the
user reads once when writing it and rarely again — this section is what they actually
glance at before a standup to answer "what did you get done, what are you doing
now/next, what's in your way" without re-reading the whole thing. Keep it to a handful
of single-line bullets per bucket, written after the rest of the recap is drafted (it's
a compression of what's below, not a new source of information):

- **Done:** things that actually completed/shipped/resolved *today specifically* — a
  merged/committed slice, a review that finished with no blockers, an open question
  that got resolved. Not carried-forward context, not work still in progress.
- **Doing now / next:** the user's own explicit forward-looking plans (e.g. "pivoting to
  X tomorrow," "reviewing the PR before sending it on," "resuming the branch now that X
  is unblocked"). Can be more than one bullet if there are genuinely several concrete
  next steps; don't force it down to one at the cost of dropping a real one. If nothing
  explicit exists, say so rather than inventing a plan.
- **In my way:** genuine external dependencies only — something the user is actually
  waiting on, from a person or system outside their own control, tagged
  **[Needs: <name>]** (a named person outside this session). If nothing is genuinely
  blocked on an outside party on a given day, this bucket is empty — that's a good,
  valid outcome, not a sign something was missed.

  **Don't restate a standing structural friction fact here.** Once a standing gap
  (e.g. self-scoping due to no PM) is documented, treat it as established baseline
  rather than daily content — this bucket is for active, named external dependencies
  only. Distinct from the "don't dedupe recurring friction" principle below, which
  covers evolving themes (a new instance, an escalation), not a single fully-settled
  fact.

  **Keep this distinct from an open question (a decision nobody's made yet).** A design
  decision the user will make themselves — even one they'll think through with help
  before deciding — is not "blocked on" anything; it's their own next step, and belongs
  in "Doing now / next" above or in Progress, not here. Don't invent a third party (e.g.
  "the architect") who needs to weigh in before they can proceed — if no such external
  party exists, that phrasing is a leak of internal tooling vocabulary into a document
  meant for people who've never heard of it.

  Each unresolved item from step 2's "Needs Architect"/"Open Assumptions" callouts that
  genuinely names an external party, plus anything fresh that came up today, becomes a
  bullet here. Only tag `[Needs: <name>]` when there's actual corroborating evidence the
  dependency is real (e.g. that person is independently named elsewhere as owning
  related work). Do **not** infer this from how a source document happens to phrase it —
  phrasing like "needs someone with X access" is not proof of who "someone" is; it can
  just as easily be the user's own follow-up in a different repo. When in doubt, ask
  instead of tagging.

**Compression must not inflate scope.** A detailed section can state real qualifiers
(count of slices, "one path not all consumers," "started but not merged") that a
compressed one-line summary then drops, turning "2 of 6 planned slices done, wired into
one path" into something that reads as "fully done." When summarizing, keep whatever
scope qualifier the detailed section already states — compression should make a claim
*shorter*, never *bigger*. If a true detail doesn't fit in one line without a
qualifier, keep the qualifier and cut something else instead.

### Progress
Story-linked work for the date, drawn from step 2's findings (status changes,
decisions, corrections), cross-referenced against step 1's commits where they land
same-day or adjacent. Include self-corrections and mistakes transparently — don't
curate them out, they're evidence of diligence, not something to hide. No
time/effort quantification.

**Surface positive feedback verbatim, don't paraphrase it away.** If the week's tracker
doc, a PR review, or something the user tells you directly captures a specific compliment
or positive quote about the work (a reviewer's own words, a stakeholder's approval), quote
it directly next to the item it's about, attributed and dated. "Reviewed positively" loses
exactly the texture this is for.

**Tag same-day work completed after the demo.** If step 3 recorded a demo end time for
this date, check every item's actual completion (merge timestamp, not commit or PR-open
time) against it. Anything completed after gets *"(not yet demoed)"* appended to its
bullet — this is a same-day comparison only, not something to carry across days here;
`week-rollover` is what sweeps these forward at the week boundary.

### Friction / Coordination Overhead
Don't infer this purely from artifacts — ask the user directly, as an actual question,
*before* drafting this section, not after. Useful prompts:
- "What were you blocked on today, waiting on someone else for?"
- "Did anything take longer than it reasonably should have, and why?"
- "Any decisions you had to make without an architect or PM to check with?"
Only fall back to what plan.md's own corrections/discoveries suggest if the user has
nothing to add. If a guess would otherwise need a "not confirmed" flag, ask the
question instead of drafting the guess and flagging it — see "5. Present, don't just
save" below, which applies to every section, not just this one.

**Walk each drafted friction item one at a time before finalizing.** This section is
the user's own subjective account of what actually slowed them down or put them in an
awkward spot, not something artifacts can verify — so after asking the upfront prompts
and drafting bullets from the answers, present each resulting bullet individually (not
the whole section at once) and get a reaction before moving to the next. Scoped to this
section and the "In my way" bucket specifically because both involve judgment/attribution that
can't be cross-checked against a commit or a calendar entry — Progress, Untracked Work,
and Calendar are grounded in verifiable artifacts and don't get this same one-at-a-time
treatment by default.

**A recurring friction theme showing up again is signal, not noise — never compress,
dedupe, or omit it just because it appeared in a prior day's recap.** An ongoing
structural friction (e.g. no real story-level tracking, an unclear PM situation) is
expected to keep coming up daily, and that repetition is exactly the point — it's the
evidence leadership needs to gauge how the engagement is going. When a friction item
involves specific people or org roles, check project memory (the org-roles memory from
Current Engagement Config) for current facts rather than guessing or asserting from
what a prior recap said — those facts change as people roll on/off the engagement.

**When a standing item hasn't changed since the prior day, don't re-write it in full
prose — write "Nothing new today" instead**, in both Friction and the "In my way"
bucket. Only restate in full when something about it has actually changed (resolved,
escalated, newly corroborated). A day-count of how long something's been a live
friction is derivable from the recap files' own dates directly, if it's ever needed.

### Untracked Work
Any git commit or calendar meeting (from steps 1/3) that doesn't map to a known story
slug. Don't guess at what it was — ask a one-line question per item, e.g. "this
commit/meeting doesn't map to a tracked story — one-line description for the recap?"
Exception: if the commit message itself is already fully self-explanatory, don't
manufacture a question just to have one — use the message as the description. Note the
count of untracked items found for the day; the trend itself is a data point worth
preserving (evidence of untriaged intake with no PM to route it).

**Propose a calendar prep-reminder for any item tied to a specific future meeting.**
When an "In my way" item, Progress item, or a "found during UAT"-style discovery names
something the user should raise with a specific person at a specific recurring
meeting, don't just log it as a follow-up and hope they remember when that meeting
comes around. If there's no reliable automated way to ping them right before a meeting
starts, the fallback is: draft ready-to-paste text for a **private, personal** calendar
event — title, a time ~15 minutes before the real meeting's next occurrence, and a
description with the specific point to raise (plus a pointer to the fuller write-up doc
if one exists) — and hand it to the user to add themselves. Look up the meeting's
actual next occurrence via the calendar tools (don't guess the date), and never attach
this to the real shared meeting's own event (editing an event organized by someone
else, or one other attendees see, is not appropriate) — always a separate,
user-only block.

### Calendar
The classified events from step 3, in chronological order.

## Never leak internal tooling jargon

This recap is meant to be legible to anyone the user shares it with — leadership,
possibly people who've never touched Claude Code. This project's internal workloop (the
`/story`/`/plan`/`/slice`/`/code-review` commands, the "architect"/"verifier" agent
roles, "Reviewer Mode," the term "workloop" itself) means nothing to an outside reader
and would just be confusing noise to include by name. Before finalizing, scan the draft
for these and rewrite in plain, outcome-oriented language:
- "Reviewed via `/code-review` (Reviewer Mode)" → "Reviewed the PR for quality and
  correctness" (drop the tool/mode name; keep "no story/plan applied" only if rephrased
  plainly, e.g. "no formal spec existed for this branch to check against").
- "the verifier agent had been running a lint autofix" → "our review tooling had been
  auto-fixing lint issues" (no agent-role names).
- "architect output landed as ADR-013" → "a design decision was documented (ADR-013)"
  — "ADR" itself is a standard, explainable engineering term and fine to keep; the
  internal agent-role framing is not.
- A pending decision "for the architect to make" → it's the user's own decision; see
  the "In my way" note above. Never imply a third party called "the architect"
  exists.
- Meta-notes about this skill's own gaps, or about *other* skills' bugs discovered
  incidentally, do not belong in the leadership-facing recap at all — that's a note for
  the user's own tooling backlog, not something to surface to whoever reads this doc.
  Leave it out of the recap entirely and mention it back to the user directly instead.
`docs/stories/`, `plan.md`, and general engineering terms (PR, ADR) are fine — those
aren't Claude-Code-tooling-specific and read fine to an outside technical audience.

**Don't lead with an internal slice number as the primary way of referring to a piece
of work** (e.g. "Slice 1," "Slice 3") — it's meaningless to a reader who never saw the
plan doc's own numbering, even with a descriptive parenthetical attached. Describe work
by what it actually is (e.g. "the identity/profile layer," "the agency lookup feature")
and drop the slice number from the lead description entirely. It's fine to keep a slice
number as a trailing, parenthetical cross-reference for the user's own later lookup
(e.g. "...now uses live data (Slice 3 of this story)") if it doesn't get in the way of
the sentence otherwise reading naturally without it.

## The recap stands alone — don't reference other artifacts by name

The recap itself must never say things like "now logged in the README" or "see the
week's tracker" — it should read as a complete, self-contained account of the day, not
something that sends the reader elsewhere to get the full picture. This applies even
when the recap and some other doc (the week's README, a story's plan.md, a topic doc)
were updated in the same conversation as a direct result of something surfaced while
drafting the recap — the recap describes *what happened* ("this hadn't been tracked
anywhere until today"), not *which file now contains it*. Sourcing from those documents
(git activity, plan.md mining, the week's directory) is exactly what step 1/2 already
do — the restriction is only on the recap's own prose citing them back by name as a
pointer.

## Never fabricate supporting detail

Every specific claim about what the user did, decided, or experienced must trace to an
actual source — a plan.md annotation, a commit message, a calendar event, or something
the user said directly. If a narrative has a gap that would read better with a specific
detail (e.g. "had to track down X," "spent hours on Y"), do not invent one to fill it,
even if it sounds plausible given the surrounding facts. Leave the gap explicit, or ask.

## 5. Present, don't just save

This skill is still being field-tested — show the drafted recap in the conversation so
the user can react to it before treating it as final, in addition to writing it to the
output path.

**Record the cutoff.** Immediately after writing the recap file, get its actual creation
timestamp from the filesystem — don't estimate it — and add a row for it to a
`## Recap Log` table in that week's README (create the section, right after the header,
if this is the first entry). This is what lets the *next* recap run know precisely how
far a given day's recap already covers, without re-deriving it from scratch. Never write
the current wall-clock time as a stand-in for the file's real creation time.

**Ask before drafting, don't flag after.** For anything you'd otherwise guess at, infer
without a source, or want to hedge/flag as "not confirmed" — stop and ask a direct,
specific question about it *before* writing that part of the draft, rather than writing
a best guess into the file with a flagged caveat attached. Asking while generating means
the user can actually answer accurately; a flagged guess sitting in a file they might
not read until later just means the inaccuracy sits there unless they happen to catch
it. This applies everywhere a guess would otherwise appear — not just Friction (which
already has an "ask directly" rule, see above), but any section: an ambiguous commit's
purpose, an unconfirmed org affiliation, a hypothesis about root cause, anything. The
one exception is a source-level gap with nothing to ask about (e.g. "calendar not
connected," "no plan.md found for an active repo") — there's no question to ask there,
so name the gap plainly in the draft instead of silently omitting it.

**Walk the "In my way" bucket's `[Needs: <name>]` items one at a time before
finalizing.** These are uniquely error-prone — forward-looking claims about who owns
what and who's actually blocking whom, which the underlying artifacts (commits, plan.md,
calendar) can't fully verify on their own; misattributing the user's own assigned work as
an external dependency, or overstating a nice-to-have as a blocker, are both easy
mistakes to make here. After drafting the full recap, present every such item
individually — one item, wait for a reaction, then the next — rather than presenting the
whole bucket at once or folding this into the general "present, don't just save"
review. Apply corrections immediately (including to any other doc the correction
touches, e.g. the week's README) before moving to the next item.

Friction / Coordination Overhead gets the identical one-at-a-time treatment — see its
own section above. **Scoped deliberately to these two, not every section.**
Extending this to Progress, Untracked Work, and Calendar by default isn't the right
call — those are grounded in verifiable artifacts (a commit exists or it doesn't, a
calendar event has these attendees or it doesn't), so the error risk is lower and of a
different kind (missing context, wrong emphasis) than the attribution/classification
errors "In my way" and Friction are prone to. A daily per-item interactive
walkthrough across every section of every recap risks turning a lightweight daily
ritual into a long interview, which could hurt adoption more than the accuracy gain
helps. If Progress/Untracked Work/Calendar start producing wrong or misleading content
in practice, revisit this — but don't apply the pattern uniformly on a hypothesis.
