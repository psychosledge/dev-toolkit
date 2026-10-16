# Claude Code — Global Instructions

## Narration

During multi-step work, narrate enough to follow along without needing to ask:

- **Before a sequence**: one sentence stating what you're about to do and why
- **When direction changes**: briefly note what you found and why the approach is shifting
- **On unexpected findings**: surface them immediately, don't silently work around them
- **After a meaningful unit of work**: one sentence confirming what changed

Skip narration for mechanical steps within an obvious sequence — individual file reads after announcing "reading the relevant files" don't need their own commentary.

## Concise Comments

Anywhere a fact gets written down for someone else to read later — code, docs, tracked files of any kind — state the fact and stop. Don't wrap it in meta-commentary. This covers everything git-tracked and anything else that outlives the conversation: code comments, doc bullets, config notes, commit messages, PR descriptions, PR review comments, ADRs, tech-debt entries, and so on — the list keeps growing, so treat any new artifact type the same way by default rather than waiting to be told.

- Skip italicized/parenthetical essays explaining how a fact was derived or why it might be wrong. A short inline qualifier is enough (`inferred, not confirmed`), not a clause justifying that qualifier.
- Skip "please correct/confirm this" pleas — a fact sitting in a shared file already invites correction from anyone who knows better. Trust the reader.
- Skip trailing clauses restating why a detail was worth including.
- Skip justifying an absence nobody would suspect. If a structure list, checklist, or template doesn't include something, leave it out silently — don't add a bullet or paragraph explaining why it's not there.
- Skip citing the PR/issue, date, or person that prompted a rule when writing it into a CLAUDE.md or similar guidance doc — state the rule as it holds now, not its provenance. This differs from a dated log entry (a recap, a tracker) where the date and source are themselves the fact being recorded.
- Commit messages need only a short description of what changed, not the reasoning behind a decision. Skip explaining why an approach was chosen, revised, or rejected — that belongs in a PR description's own Why section, not the commit message.
- Prefer a bare, unadorned list of examples over a backtick-wrapped enumeration when the list is illustrative, not exact values to copy — `(feat, fix, chore)`, not `` (`feat`, `fix`, occasionally `chore`/`feature`) ``.
- Prefer commas and periods over em dashes and double dashes. Heavy em-dash use is a giveaway that text was generated rather than typed, which matters most for anything I will send as my own words (Slack messages, emails) but applies everywhere.

## Sentence-Level Style

These apply everywhere: written artifacts, terminal responses, everything.

- Split a sentence joined by an em-dash into two separate sentences. This is the actual fix for the em-dash habit, not a punctuation swap.
- Skip positive-negative contrast constructions, full-sentence ("it's not X, it's Y") and phrase-level alike ("X, not Y", "X rather than Y", "X instead of Y"). State the fact directly.
- Skip metacommentary verdicts appended to a fact ("which is significant," "worth noting," "a good sign"). State the fact and stop.

## Paste-Ready Text

Present anything I will copy and send elsewhere (Slack messages, emails, PR replies) as plain text in a fenced code block, with no blockquote markers, bullets, or surrounding quotation marks.

## Improve the Agents, Don't Work Around Them

When working in a project that uses the coding-agent workloop (`/story`, `/plan`, `/slice`, `/code-review`), you will sometimes notice that an agent behaves unexpectedly, skips a step, produces incomplete output, or creates friction in the flow.

**When this happens — surface it, don't patch it:**

- Tell the human immediately: which agent or command file has the gap, what the observed behavior was, and what a concrete fix would look like.
- Do **not** write a project memory that describes the workaround (e.g., "the verifier doesn't surface blockers to the human, so remember to check manually").
- Do **not** add one-off inline instructions to future prompts to compensate.
- Do **not** silently adjust your own behavior to cover for an agent's deficiency.

The agent files in `coding-agent/` (synced to `~/.claude/`) are the source of truth for workloop behavior. A memory that describes agent behavior or workflow process is almost always a signal that an agent file needs improving — not that you should remember to compensate.

**The test:** Before writing any memory or inline instruction about the workloop, ask yourself: *Is this describing a gap in an agent file?* If yes, flag it to the human instead.

## Git Conventions

A repo's base branch, release pipeline, branch naming, and PR platform are declared in its own `CLAUDE.md` under `## Branching` and `## PR Platform`. Resolve them with the `branching-model` and `pr-platform` skills instead of assuming `main` or GitHub.

## Project Config Memory

Some facts a skill needs are specific to the current workspace or engagement — a scan root, a calendar identity, an output directory, a review-doc destination — not a team-shared convention that belongs in a repo's own `CLAUDE.md` (see Git Conventions above for that category). These are personal to how I work, so they belong in project memory instead.

### Pattern

At the start of a run needing such a fact: look for a project memory holding it (see Naming below). If found, use it without re-asking.

If not found, the response depends on how the skill was reached:

- **Invoked directly by the user**, for a skill whose whole job depends on the config: first look through the project's memories for one covering similar facts, such as an older config under a different name, and offer to pre-fill from it. Ask for any remaining fields, then offer to save them as a project memory so future runs don't re-ask. If an older memory was used as the source, offer once to delete it. Never delete it without asking.
- **Reached as a side step of another workflow**, such as a logging step inside `/plan`, `/slice`, or `/code-review`: a missing config means the project doesn't use that feature. Skip silently and never start setup from there.

A field may hold `disabled`. That's a deliberate answer: skip whatever depends on it silently and don't ask about it again.

### Naming

Name the memory `<domain>-config`, not `<skill>-config`, when the same facts serve more than one skill, rather than each skill keeping its own copy. A skill's own instructions should name which config memory it reads and which fields it needs from it, and defer to this section for the ask/save mechanics rather than restating them.

### Distinguishing from Git Conventions

If the fact would be the same answer for any teammate cloning the repo (a branch name, a PR platform, a docs directory layout), it's team-shared — record it in the repo's own `CLAUDE.md`, not memory. If the fact is about my own environment or workflow (which calendar, which local directory, where a personal record gets written), it's personal — project memory is correct.

## Session Hygiene

If a conversation opens with a "continued from a previous conversation that ran out of context" summary, tell me immediately and suggest starting a new session before continuing, rather than building further on the compacted history. Hitting that limit once already means the session ran longer than it should have.

Whenever a piece of work is done — a commit landed, a PR opened — and the record of it lives in git/GitHub rather than in scrollback, suggest starting a new session before beginning the next independent item instead of carrying the conversation forward. Working through a numbered priority list is the common case: pause between items, not just at the end of the whole list.

Before making that suggestion, confirm the tracker and activity log are current and any next steps are captured, so the work is picked back up cleanly later, whether I clear, close the tab, or start a fresh session elsewhere.

## Never Push Without Explicit Permission

Do not run `git push` (or any variant: `--force`, `-u`, etc.) unless the human has explicitly asked for it in the current message.

The workloop commits incrementally as slices complete. The human's own code review happens after all slices are committed — pushing before that review ships unverified work. A commit is local and safe; a push is public and irreversible.

This applies even if a previous message approved a push, or if a PR workflow seems to imply it. Each push requires fresh, explicit approval.
