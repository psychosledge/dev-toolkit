---
name: daily-recap
description: Generates a daily work recap (progress, friction, untracked work, open questions, calendar) for this client engagement, which has no sprint board and no dedicated PM. Use when asked to generate a daily recap, work summary, or "what did I do today/yesterday."
---

# Daily Recap

Builds a single day's work recap — the substitute artifact for a sprint board /
PM-tracked status on this engagement, ultimately meant to give Bo's own leadership
visibility into effort and hurdles. This skill is still being field-tested; don't treat
any one run's shape as final, and prefer asking the user over guessing whenever a
signal is ambiguous.

## Current Engagement Config

This skill is generic — the facts it needs (scan root, calendar identity, output
location, org roles) are specific to whichever engagement it's being run for, and none
of them belong hardcoded here. At the start of a run, look for a project memory
describing the current engagement's daily-recap config (e.g. named
`daily-recap-config`, holding scan root / calendar identity / output location) plus one
covering org roles (who's a PM, who's a client stakeholder, who owns what — these
change as people roll on/off an engagement, so they belong in memory, not here).

If no such memory exists for the project this session is running in, ask the user
directly for: scan root, calendar identity, and output location — then offer to save
the answers as a project memory so future runs don't re-ask. Everything below refers
back to those three values plus the org-roles memory; nothing else in this skill should
hardcode a path, calendar name, or org fact directly.

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
git log --all --author="Bo Ramsey" --since="<date> 00:00:00" --until="<next-date> 00:00:00" --pretty=format:"%H|%ad|%s" --date=iso
```

Collect everything found. Treat this as a cross-check and an untracked-work detector —
not the primary source of what the day was about (see below for why).

**For every commit found, check whether it's actually merged before saying so anywhere
in the recap.** Confirmed 2026-07-31, and it was bad: every single "done ✅" / "shipped"
claim across 5 days of recaps (2026-07-27 through 2026-07-31) turned out to describe
work still sitting on an unmerged feature branch — `feature/live-agency-data-sourcing`
was 5 commits ahead of `origin/main` with zero merged, and even the item-search-reframe
commits from days earlier were never ancestors of `origin/main` either, with no open PR
for either branch. **"Shipped" means the commit is an ancestor of the repo's default
branch — nothing less.** Check with:

```
git merge-base --is-ancestor <hash> origin/main && echo MERGED || echo NOT-MERGED
gh pr list --state all --search "<hash>"   # or --head <branch> — is there a PR, and what state
```

Use this status ladder, and never round up to a higher rung than what's actually true:
- **Merged** — the commit is an ancestor of `origin/main` (or the repo's actual default
  branch). This is the *only* status that gets to use the words "shipped" or "done" in
  the sense Bo means them.
- **PR open** — a pull request exists but isn't merged yet. Say "PR open, awaiting
  review/merge," not "done."
- **Implemented, not yet merged** — commits exist on a feature/local branch, no PR
  open yet. This is where most of this week's "done ✅" claims actually were. Say
  exactly that — "implemented on the feature branch, not yet merged, no PR open" — not
  "shipped," not "done," not "completed."
A story's own `plan.md` marking a slice "✅ done" refers to that slice's *implementation*
being complete in the coding workflow's own sense (code written, tests pass, committed)
— it is not evidence of merge status and must not be translated directly into
"shipped"/"done" without independently checking the ladder above.

**Read the full commit body, not just the subject line, for every commit you're about
to cite as evidence of a specific piece of work.** Confirmed 2026-07-31 (surfaced by a
completely separate Claude session working from Sarah's side, not by this skill): a
single commit, `70d8c1f1` ("fix: geoid/CountyObject rollout follow-up fixes," 2026-07-24),
contained two genuinely separate, separately-creditable pieces of work — a live
data-loss bug fix, and unrelated hardening of both recommender adapters against a
missing API field, with new test coverage. Every recap this week had filed the whole
commit under "the geoid bug fix" because that's what the original triage doc called it
and what Bo confirmed verbally — nobody had actually read this commit's own body, which
spells out both pieces explicitly in separate paragraphs. For every commit surfaced in
step 1, run:

```
git show -s --format="%B" <hash>     # full multi-paragraph message, not just %s
git show --stat <hash>                # file-level scope
```

The full body is often enough by itself (as it would have been here). If the file-stat
scope spans clearly distinct areas (e.g. recommender adapters *and* search filters *and*
unrelated docs) and the message doesn't clearly account for all of them, that's a signal
to look at the actual diff before deciding this is one piece of work rather than several
— but don't do a full line-by-line diff read of every commit by default; the message
body plus file-stat scope is the "quick" version of this check, and is usually enough.

## 2. Story plan mining (primary signal)

Find every `docs/stories/<slug>/plan.md`, in both locations:
- top-level, untracked: under the same untracked docs directory the output location
  (Current Engagement Config) lives in — i.e. `<that docs dir>/stories/*/plan.md`
- per-repo, git-tracked: `<repo>/docs/stories/*/plan.md`, for each repo under the scan
  root

For git-tracked ones, check `git log -p` / `git diff` for changes landing on the target
date. For untracked ones there's no diff history at all — **check file mtime for
"modified since the last recap run," not just a text grep for the target date.**
Confirmed 2026-07-29: new content was added to two workstream files *today* but
self-dated `(2026-07-28)` inside the text, because that's when the underlying
conversation happened, not when the file was edited. A grep for today's date string
would have missed it entirely. Use mtime to find what changed, then read the dateline
inside to understand when the underlying event actually happened — the two aren't the
same thing, and mtime is the more reliable trigger for "is there something new here."

**This is the primary source, not git log.** Validated 2026-07-27: git log surfaced
exactly one unrelated commit that day, while the real substance (a deprecated-endpoint
discovery, live API re-validation, an ADR correction) lived entirely in the plan.md's
dated annotations and wasn't committed until the following day. Expect this lag to
recur — a quiet git log day is not proof of a quiet work day.

Also collect any still-unresolved "**Needs Architect:**" or "Open Assumptions Flagged
for Approval" callouts, regardless of whether they were touched on the target date —
these feed Open Questions below. **Check two places, not just `docs/stories/`:** every
currently active story's `plan.md`, and every topic doc's own "Open Questions" section
(see below) — a pre-story investigation doc (e.g. a not-yet-storified bug writeup) can
carry open questions of its own before anything graduates to `docs/stories/` at all.

**Reorganized 2026-08-10: there is no longer a standalone `open-questions.md` file.**
Open questions now live inside whatever document they're actually about — a story's own
`plan.md`, or a topic doc's own "Open Questions" section — updated in place and removed
(not just marked resolved) once answered, the same convention `TECH_DEBT.md` already
uses. Don't go looking for a separate open-questions artifact; if a topic doc has no
"Open Questions" section, it has none outstanding.

**Always list the whole untracked docs directory, not just `docs/stories/`.** The
untracked docs directory now nests by week: `docs/weeks/<monday-of-that-week>/` holds
that week's own tracker doc (a blanket to-do list, not a sprint board — see Current
Engagement Config) plus every topic doc and self-documenting artifact from that week —
including a `/code-review` findings doc (`<date> - Review - <repo> PR #<n>
(<title>)/findings.md`) or meeting notes (`<date> - Meeting Notes - <title>/notes.md`)
nested inside the week they actually happened in, not flat at the docs root. To find the
right week for the target date: list `docs/weeks/`, compute each entry's date range
(that Monday through the following Sunday), and use whichever range contains the target
date — creating a new week directory is the user's own weekly-kickoff ritual, not
something this skill does. Once you've found the right week directory, list its full
contents and read anything relevant in full — don't pattern-match on the specific
examples above, naming conventions for what shows up here aren't fully predictable in
advance. These docs can go stale exactly like plan.md does (an item marked "still open"
may have been resolved days later in conversation, not by editing the doc) — cross-check
against what the user tells you in step 4, don't take the doc's own status markers as
final.

**A rich pre-planning artifact existing doesn't mean there's no friction to report.**
Confirmed 2026-07-29: some of Bo's assigned work traces to genuinely deep investigation
docs, not nothing — but those docs are explicitly pre-`/story` triage (see their own
README for why), and the real friction is that items stall there and never graduate to
a scoped story with acceptance criteria, because no one is doing that graduation work.
Report it that way — "rich investigation exists, but nothing has turned it into a
scoped story" — rather than either "no artifact exists" (wrong) or "this is fully
tracked" (also wrong).

**Some artifacts may exist in systems this skill can't read at all** (e.g. a Slack
Canvas) — if the user mentions one, note that it exists and that this recap can't see
it, rather than silently omitting the fact that a real tracking document exists
somewhere outside this skill's reach.

## 3. Calendar

Use the Google Calendar MCP tools (`list_events` on the calendar identity from Current
Engagement Config above) for the full target date. Apply these rules exactly; they
exist specifically to avoid noise and to avoid leaking personal detail that isn't
reliably scrubbed at the source:

**Cross-reference meeting notes docs against calendar events by title match.**
Reorganized 2026-08-10: a meeting-notes doc found while listing the week's directory
(step 2 above) is now named `<date> - Meeting Notes - <exact calendar event summary>.md`
— e.g. a calendar event titled "Working Session for Item Search" produces
`2026-08-10 - Meeting Notes - Working Session for Item Search.md`. When both exist for
the same date, treat them as the same meeting and merge: the calendar event gives exact
time/attendees/organizer, the notes doc gives what actually happened. Don't just list
them as two separate line items. This convention only applies going forward — don't
expect it on notes docs from before 2026-08-10, and don't assume a meeting notes doc
exists for every calendar event or vice versa; match by title when both are present,
don't require it.

- `eventType == OUT_OF_OFFICE` **and** has a `recurringEventId` → exclude entirely.
  Routine recurring time off is noise, not a line item.
- `eventType == OUT_OF_OFFICE` **and no** `recurringEventId` (one-off) → include, but
  generically as **"OOO"** with only the time span. Never surface the event's real
  title — personal blocks on this calendar are not reliably generic at the source (a
  real one is literally titled "Lunch and School Pickup"), so the scrub happens here,
  not by asking Bo to rename calendar events.
- No `attendees` array at all → a generic time-block: title + duration only, nothing
  else. This is a known, deliberate pattern — a same-titled placeholder blocks time on
  the client-visible calendar while the real meeting's details live on a separate
  calendar this skill can't see. Don't treat it as an anomaly worth a question.
- Bo's own `responseStatus` is `declined` → exclude entirely. He didn't attend, so it
  shouldn't read as time spent. **Check the attendee entry with `"self": true`
  specifically** — confirmed 2026-07-30: an event can list a `boramsey@artium.ai` entry
  as declined while the `"self": true` entry (`bo.ramsey@infotechinc.com`, the account
  this calendar belongs to) shows accepted. Excluding based on any attendee entry that
  merely looks like Bo, instead of the actual `self` one, would wrongly drop a meeting
  he attended.
- A meeting with a large attendee list (rough threshold: more than ~10) → summarize as
  a count plus one-line description (e.g. "company-wide demo session, ~28 attendees
  across InfoTech and Artium") rather than listing every name — the point is a
  10-second-glance recap, and a wall of names defeats that for an all-hands-style event.
  Small/medium meetings still get a full attendee list.
- Otherwise → a real meeting: title, start time + duration, attendee list (names/emails
  only). Never include accept/decline/no-response status for *other* attendees — that's
  not part of the goal. Never include Zoom/meeting join links or dial-in passwords in
  the written recap, even though they're present in the raw event description.

## 4. Build the recap

Sections, in this order:

### Standup Summary
**Goes first, above everything else.** The rest of this doc is reference detail Bo
reads once when writing it and rarely again — this section is what he actually glances
at before a standup to answer "what did you get done, what are you doing now/next,
what's in your way" without re-reading the whole thing. Confirmed with Bo 2026-07-29:
this was the missing piece after the first 3 field-test recaps. Keep it to a handful of
single-line bullets per bucket, written after the rest of the recap is drafted (it's a
compression of what's below, not a new source of information):

- **Done:** things that actually completed/shipped/resolved *today specifically* — a
  merged/committed slice, a review that finished with no blockers, an open question
  that got resolved. Not carried-forward context, not work still in progress.
- **Doing now / next:** the clearest explicit forward-looking statement already present
  in Progress or Open Questions (e.g. "pivoting to X tomorrow," "awaiting Y's follow-up
  push," "UAT not yet run"). If nothing explicit exists, say so rather than inventing a
  plan.
- **In my way:** the `[Needs: <name>]` and `[Needs: architect decision]` tagged items
  from Open Questions Carried Forward, plus — when it's still true that day — a
  one-line restatement of the standing structural friction (e.g. "no acceptance
  criteria provided, self-scoping"). This is the one bucket most directly useful for
  the "we need a PM" case, so don't soften or drop it just because it repeats daily.

**Compression must not inflate scope.** Confirmed miss (2026-07-30): the Standup
Summary said a new story's "hardcoded agency/state lists" were replaced "everywhere,"
when only 2 of 6 planned slices were actually done and the detailed Progress section
below it said outright that most consumers still read the old static lists. Nothing
was fabricated — a true "2 of 6 slices done, wired into one path" got compressed into
something that reads as "fully done." When summarizing, keep whatever scope qualifier
(count of slices, "one path not all consumers," "started but not merged") the detailed
section already states — compression should make a claim *shorter*, never *bigger*.
If a true detail doesn't fit in one line without a qualifier, keep the qualifier and
cut something else instead.

### Progress
Story-linked work for the date, drawn from step 2's findings (status changes,
decisions, corrections), cross-referenced against step 1's commits where they land
same-day or adjacent. Include self-corrections and mistakes transparently — don't
curate them out, they're evidence of diligence, not something to hide. No
time/effort quantification.

### Friction / Coordination Overhead
Don't infer this purely from artifacts — ask the user directly, as an actual question,
before drafting this section. Useful prompts:
- "What were you blocked on today, waiting on someone else for?"
- "Did anything take longer than it reasonably should have, and why?"
- "Any decisions you had to make without an architect or PM to check with?"
Only fall back to what plan.md's own corrections/discoveries suggest if the user has
nothing to add. **Confirmed miss (2026-08-12):** drafted this section from inferred
artifact patterns, flagged it in the doc as "not confirmed with Bo," and asked
afterward only because Bo pushed back — backwards from the rule above. If a guess
would otherwise be flagged here, ask the question instead of drafting the guess; see
the note under "5. Present, don't just save" below, which applies to every section,
not just this one.

**Walk each drafted friction item one at a time before finalizing.** Added 2026-08-12,
same reasoning as the identical rule for Open Questions Carried Forward under step 5:
this section is Bo's own subjective account of what actually slowed him down or put
him in an awkward spot, not something artifacts can verify — so after asking the
upfront prompts and drafting bullets from his answers, present each resulting bullet
individually (not the whole section at once) and get his reaction before moving to the
next. Scoped to this section and Open Questions specifically because both involve
judgment/attribution that can't be cross-checked against a commit or a calendar entry
— Progress, Untracked Work, and Calendar are grounded in verifiable artifacts and
don't get this same one-at-a-time treatment by default (see step 5's note on scoping
this deliberately rather than applying it to every section).

**A recurring friction theme showing up again is signal, not noise — never compress,
dedupe, or omit it just because it appeared in a prior day's recap.** Confirmed with Bo
2026-07-29: an ongoing structural friction (currently: no real Story-level tracking,
client-side PM transition) is expected to keep coming up daily, and that repetition is
exactly the point — it's the evidence leadership needs to gauge how the engagement is
going. When a friction item involves specific people or org roles (who's an internal PM
vs. a client stakeholder, who owns what), check project memory (the org-roles memory
from Current Engagement Config) for current facts rather than guessing or asserting from
what a prior recap said — those facts change as people roll on/off the engagement.

### Untracked Work
Any git commit or calendar meeting (from steps 1/3) that doesn't map to a known story
slug. Don't guess at what it was — ask a one-line question per item, e.g. "this
commit/meeting doesn't map to a tracked story — one-line description for the recap?"
Exception: if the commit message itself is already fully self-explanatory (e.g. "fix:
rename Promise resolver to satisfy promise/param-names lint rule"), don't manufacture a
question just to have one — use the message as the description. Note the count of
untracked items found for the day; the trend itself is a data point worth preserving
(evidence of untriaged intake with no PM to route it).

### Open Questions Carried Forward
This section is for genuine external dependencies only — something Bo is actually
waiting on, from a person or system outside his own control. It is NOT a place for
Bo's own normal next steps, even ones that involve deciding between technical options.
Each unresolved item from step 2's "Needs Architect"/"Open Assumptions" callouts, plus
anything fresh that came up today, gets exactly one of:
- **[Your follow-up]** — the user's own next action, even if it lands in a different
  repo or a different Claude Code session.
- **[Needs: <name>]** — a named person outside this session. Only use this tag when
  there's actual corroborating evidence the dependency is real (e.g. that person is
  independently named elsewhere as owning related work). Do **not** infer this from how
  a source document happens to phrase it — phrasing like "needs someone with X access"
  is not proof of who "someone" is. Concrete miss to not repeat (2026-07-28): a plan.md
  said a Terraform/credentials task "needs a human with Terraform/infra access," and
  that was relayed as blocked-on-someone-else without asking — it was actually the
  user's own follow-up, just in a different repo. When in doubt, ask instead of tagging.

**Do not tag a pending technical decision as an open question or blocker just because
it will be worked through collaboratively before Bo decides.** Confirmed with Bo
2026-07-30: a design decision that Bo will make himself — even one he'll think through
with help before deciding — is not "blocked on" anything. It's his own next step.
Concrete miss to not repeat: tagging "does X apply to Y" as `[Needs: architect
decision]`, as if some third party named "the architect" needed to weigh in before Bo
could proceed. There is no such external party — that phrase was a leak of this
project's own internal tooling vocabulary into a document meant for people who've never
heard of it. Put items like this in Progress or the Standup Summary's "Doing now/next"
instead, phrased as Bo's own pending call (e.g. "Next: decide whether X applies to Y —
my own design decision, not yet made").

**Propose a calendar prep-reminder for any item tied to a specific future meeting.**
Added 2026-08-12: when an Open Question, Progress item, or a "found during UAT"-style
discovery names something Bo should raise with a specific person at a specific
recurring meeting (e.g. "bring this up with Karoliina at Job Search Sync"), don't just
log it as a follow-up and hope Bo remembers when that meeting comes around. There's no
reliable automated way to ping Bo right before a meeting starts (checked 2026-08-12:
calendar write access isn't authorized, and cron-based reminders are session-scoped and
unreliable across days), so the fallback is: draft ready-to-paste text for a **private,
personal** calendar event — title, a time ~15 minutes before the real meeting's next
occurrence, and a description with the specific point to raise (plus a pointer to the
fuller write-up doc if one exists) — and hand it to Bo to add himself. Look up the
meeting's actual next occurrence via the calendar tools (don't guess the date), and
never attach this to the real shared meeting's own event (editing an event organized by
someone else, or one other attendees see, is not appropriate) — always a separate,
Bo-only block. Example done 2026-08-12: a "🔔 Prep: Job Search Sync — raise viewport
county/state highlighting idea" event for the next Job Search Sync occurrence.

### Calendar
The classified events from step 3, in chronological order.

## Never leak internal tooling jargon

This recap is meant to be legible to anyone Bo shares it with — leadership, possibly
people who've never touched Claude Code. Confirmed with Bo 2026-07-30: this repo's
internal workloop (the `/story`/`/plan`/`/slice`/`/code-review` commands, the
"architect"/"verifier" agent roles, "Reviewer Mode," the term "workloop" itself) means
nothing to anyone but Bo and would just be confusing noise to include by name. Before
finalizing, scan the draft for these and rewrite in plain, outcome-oriented language:
- "Reviewed via `/code-review` (Reviewer Mode)" → "Reviewed the PR for quality and
  correctness" (drop the tool/mode name; keep "no story/plan applied" only if rephrased
  plainly, e.g. "no formal spec existed for this branch to check against").
- "the verifier agent had been running a lint autofix" → "our review tooling had been
  auto-fixing lint issues" (no agent-role names).
- "architect output landed as ADR-013" → "a design decision was documented (ADR-013)"
  — "ADR" itself is a standard, explainable engineering term and fine to keep; the
  internal agent-role framing is not.
- A pending decision "for the architect to make" → it's Bo's own decision; see the
  Open Questions note above. Never imply a third party called "the architect" exists.
- Meta-notes about this skill's own gaps, or about *other* skills' bugs (e.g. a
  `/code-review` process inconsistency) discovered incidentally, do not belong in the
  leadership-facing recap at all — that's a note for Bo's own tooling backlog, not
  something to surface to whoever reads this doc. Leave it out of the recap entirely
  and mention it back to Bo directly instead.
`docs/stories/`, `plan.md`, and general engineering terms (PR, ADR) are fine — those
aren't Claude-Code-tooling-specific and read fine to an outside technical audience.

**Correction (2026-07-31): "Slice N" labeling is NOT fine, reversing an earlier call.**
Confirmed with Bo: leading with "Slice 1 (BidX)" / "Slice 3" as the primary way of
referring to a piece of work is meaningless to a reader who never saw the plan doc's
own numbering — even with a descriptive parenthetical attached. Describe work by what
it actually is ("the identity/profile layer," "the BidExpress agency lookup") and drop
the slice number from the lead description entirely. It's fine to keep a slice number
as a trailing, parenthetical cross-reference for Bo's own later lookup (e.g. "...now
uses live BidX data (Slice 3 of this story)") if it doesn't get in the way of the
sentence otherwise reading naturally without it.

## The recap stands alone — don't reference other artifacts by name

Confirmed with Bo 2026-08-12: the recap itself must never say things like "now logged
in the README" or "see the week's tracker" — it should read as a complete, self-contained
account of the day, not something that sends the reader elsewhere to get the full
picture. This applies even when the recap and some other doc (the week's README, a
story's plan.md, a topic doc) were updated in the same conversation as a direct result
of something surfaced while drafting the recap — the recap describes *what happened*
("this hadn't been tracked anywhere until today"), not *which file now contains it*.
Sourcing from those documents (git activity, plan.md mining, the week's directory) is
exactly what step 1/2 already do — the restriction is only on the recap's own prose
citing them back by name as a pointer.

## Never fabricate supporting detail

Every specific claim about what Bo did, decided, or experienced must trace to an
actual source — a plan.md annotation, a commit message, a calendar event, or something
Bo said directly. If a narrative has a gap that would read better with a specific
detail (e.g. "had to track down X," "spent hours on Y"), do not invent one to fill it,
even if it sounds plausible given the surrounding facts. Leave the gap explicit, or ask.
Confirmed miss (2026-07-27 draft): wrote "had to personally track down who owns the
item-search API" — nothing said this; the plan.md only said the owner had confirmed an
endpoint. Cut it, don't embellish it.

## 5. Present, don't just save

This skill is still being field-tested — show the drafted recap in the conversation so
the user can react to it before treating it as final, in addition to writing it to the
output path.

**Ask before drafting, don't flag after.** Confirmed with Bo 2026-08-12: for anything
you'd otherwise guess at, infer without a source, or want to hedge/flag as
"not confirmed" — stop and ask Bo a direct, specific question about it *before* writing
that part of the draft, rather than writing your best guess into the file with a
flagged caveat attached. His own words: asking while generating means he can actually
answer accurately; a flagged guess sitting in a file he might not read until later just
means the inaccuracy sits there unless he happens to catch it. This applies everywhere
a guess would otherwise appear — not just Friction (which already had an "ask
directly" rule, see above), but any section: an ambiguous commit's purpose, an
unconfirmed org affiliation, a hypothesis about root cause, anything. The one exception
is a source-level gap with nothing to ask about (e.g. "calendar not connected," "no
plan.md found for an active repo") — there's no question to ask there, so name the gap
plainly in the draft instead of silently omitting it.

**Walk Open Questions Carried Forward one at a time before finalizing.** Added
2026-08-12, after this step caught two real misclassifications in one run (an item
tagged `[Needs: Karoliina]` that was actually Bo's own assigned work with no external
dependency at all; another tagged the same way that turned out to be a nice-to-have,
not a blocker). This section is uniquely error-prone — it's forward-looking claims
about who owns what and who's actually blocking whom, which the underlying artifacts
(commits, plan.md, calendar) can't fully verify on their own. After drafting the full
recap, present every item in this section individually — one item, wait for Bo's
reaction, then the next — rather than presenting the whole section at once or folding
this into the general "present, don't just save" review. Apply his corrections
immediately (including to any other doc the correction touches, e.g. the week's
README) before moving to the next item. This is now a standard step for every recap
that has open questions, not a one-off.

Friction / Coordination Overhead gets the identical one-at-a-time treatment — see its
own section above. **Scoped deliberately to these two sections, not every section.**
Discussed with Bo 2026-08-12: extending this to Progress, Untracked Work, and Calendar
by default isn't the right call — those are grounded in verifiable artifacts (a commit
exists or it doesn't, a calendar event has these attendees or it doesn't), so the error
risk is lower and of a different kind (missing context, wrong emphasis) than the
attribution/classification errors Open Questions and Friction are prone to. A daily
per-item interactive walkthrough across every section of every recap risks turning a
lightweight daily ritual into a long interview, which could hurt adoption more than
the accuracy gain helps. If Progress/Untracked Work/Calendar start producing wrong or
misleading content in practice, revisit this — but don't apply the pattern uniformly
on a hypothesis.
