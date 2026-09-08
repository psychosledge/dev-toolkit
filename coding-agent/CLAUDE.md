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
- Prefer a bare, unadorned list of examples over a backtick-wrapped enumeration when the list is illustrative, not exact values to copy — `(feat, fix, chore)`, not `` (`feat`, `fix`, occasionally `chore`/`feature`) ``.
- Prefer commas and periods over em dashes and double dashes. Heavy em-dash use is a giveaway that text was generated rather than typed, which matters most for anything Bo will send as his own words (Slack messages, emails) but applies everywhere.

## Sentence-Level Style

These apply everywhere: written artifacts, terminal responses, everything.

- Split a sentence joined by an em-dash into two separate sentences. This is the actual fix for the em-dash habit, not a punctuation swap.
- Skip positive-negative contrast constructions ("it's not X, it's Y"). State the fact directly.
- Skip metacommentary verdicts appended to a fact ("which is significant," "worth noting," "a good sign"). State the fact and stop.

## Improve the Agents, Don't Work Around Them

When working in a project that uses the coding-agent workloop (`/story`, `/plan`, `/slice`, `/code-review`, `/sync-agents`), you will sometimes notice that an agent behaves unexpectedly, skips a step, produces incomplete output, or creates friction in the flow.

**When this happens — surface it, don't patch it:**

- Tell the human immediately: which agent or command file has the gap, what the observed behavior was, and what a concrete fix would look like.
- Do **not** write a project memory that describes the workaround (e.g., "the verifier doesn't surface blockers to the human, so remember to check manually").
- Do **not** add one-off inline instructions to future prompts to compensate.
- Do **not** silently adjust your own behavior to cover for an agent's deficiency.

The agent files in `coding-agent/` (synced to `~/.claude/`) are the source of truth for workloop behavior. A memory that describes agent behavior or workflow process is almost always a signal that an agent file needs improving — not that you should remember to compensate.

**The test:** Before writing any memory or inline instruction about the workloop, ask yourself: *Is this describing a gap in an agent file?* If yes, flag it to the human instead.

## Branching Model

Every repo has a branching model — how work integrates and how releases flow. Skills that touch git (`/catchup`, `/plan`, `/code-review`, the verifier) resolve it the same way instead of assuming `main` or each inventing their own lookup.

### Declaration

Check the *repo's own* `CLAUDE.md` (not this file) for a `## Branching` section:

```
## Branching
- Model: trunk-based | release-branching
- Trunk: <branch>                              (trunk-based only)
- Integration branch: <branch>                 (release-branching only)
- Release pipeline: <branch> → <branch> → ...  (release-branching only, optional)
- Feature branches: yes | short-lived | no
- Feature branch naming: <pattern>, e.g. `<TICKET>/<slug>` — or "no consistent convention"
```

Any field may be absent — partial declarations are the normal case, not an error state. Treat present fields as authoritative and don't re-derive them. Treat absent fields as genuinely unknown; use the fallback and detection rules below rather than assuming a default silently.

### Resolving the diff base (the branch to merge-base against)

1. `Model: trunk-based` with `Trunk` declared → use it.
2. `Model: release-branching` with `Integration branch` declared → use it as the primary candidate. If `Release pipeline` is also declared, also compute merge-base distance against every branch in the pipeline and use whichever is the **nearest ancestor** to HEAD — not reflexively the integration branch. This is what makes a hotfix cut from a release branch resolve correctly, instead of diffing against everything the whole pipeline is behind by.
3. Nothing declared → `git config workloop.integrationBranch` (local override, unversioned) → the remote default branch (`git symbolic-ref refs/remotes/origin/HEAD`, stripped of the `refs/remotes/origin/` prefix).

### Resolving release/deploy branches (to classify, not diff against)

Read `Release pipeline` if declared, in order. Trunk-based repos have none by definition — don't go looking for one.

### HEAD on a pipeline branch itself

Before running a normal feature review, check whether the current branch **is** one of the declared branches (trunk, integration branch, or any pipeline branch) rather than a feature branch cut from one. If so, this is likely a promotion or release audit, not a feature diff — say so and ask how to proceed instead of walking a large, multi-PR diff as if it were one slice.

### When the declaration is missing or incomplete

Don't silently guess, and don't run a cold questionnaire. Ask only when a concrete signal makes the gap relevant right now — e.g. an unmerged sibling branch alongside the assumed default (`origin/dev` sitting unmerged next to `origin/main`), or a consistent shape across recently-created branches suggesting an undeclared naming convention.

For naming convention specifically: sample branches from the **last 30 days**, and weight branches authored by others more heavily than branches authored by the current git user (`git config user.email`) — self-authored branches may just reflect a skill's own past default rather than real team convention. Surface exactly what was observed plus a recommendation, and let the human make the call — e.g. *"4 of 5 other-authored branches in the last 30 days follow `<TICKET>/<slug>`; recommend canonizing that — record it?"* Never auto-apply a detected pattern.

On confirmation, write directly into **that repo's own `CLAUDE.md`** under `## Branching` — create the section if absent, fill in only the field just resolved if the rest is still unknown, and record an explicit opt-out (e.g. `Feature branch naming: no consistent convention`) when the human says there isn't one, so the question doesn't resurface every session. This is a team-level fact, not a personal one — it belongs in the versioned file that travels with every clone, never in personal memory and never left as a one-off local git-config fix alone.

### Fallback branch naming

When no naming convention is declared or detected, propose a bare `<slug>` — no `feature/` prefix, no ticket embedded — even when a ticket ID is on hand. Only add structure once it's actually known to be this repo's convention.

## PR Platform

Which PR platform a repo uses is a stable, repo-level fact, like Branching Model above — skills that touch PRs (`/catchup`, `/code-review`, `/slice`) resolve it once instead of re-deriving it from the remote URL on every run.

### Declaration

Check the repo's own `CLAUDE.md` for a `## PR Platform` section:

```
## PR Platform
- Platform: GitHub | Azure DevOps | GitLab | other/manual
```

Treat a present declaration as authoritative and skip the detection below.

### When undeclared

Detect once: `git remote get-url origin` (or `git remote -v`) and match the host. On a `github.com` match, also check `which gh` for CLI availability — a separate, machine-local fact that doesn't get recorded, since it can change independently of the repo (a new machine, a reinstall). Ask whether to record `## PR Platform\n- Platform: GitHub` in the repo's own `CLAUDE.md`, the same way Branching Model detections get recorded. For any other host, or no PR-capable remote at all, note the platform found and ask before recording it the same way. `gh`-specific commands throughout this workflow apply only when Platform is GitHub.

## Project Config Memory

Some facts a skill needs are specific to the current workspace or engagement — a scan root, a calendar identity, an output directory, a review-doc destination — not a team-shared convention that belongs in a repo's own `CLAUDE.md` (see Branching Model and PR Platform above for that category). These are personal to how Bo works, so they belong in project memory instead.

### Pattern

At the start of a run needing such a fact: look for a project memory holding it (see Naming below). If found, use it without re-asking. If not found, ask the user directly for the needed fields, then offer to save them as a project memory so future runs don't re-ask.

### Naming

Name the memory `<domain>-config`, not `<skill>-config`, when the same facts serve more than one skill — e.g. `daily-recap-config` holds the scan root, calendar identity, and output location that `daily-recap`, `weekly-recap`, and `week-rollover` all read, rather than each skill keeping its own copy. A skill's own instructions should name which config memory it reads and which fields it needs from it, and defer to this section for the ask/save mechanics rather than restating them.

### Distinguishing from Branching Model / PR Platform

If the fact would be the same answer for any teammate cloning the repo (a branch name, a PR platform, a docs directory layout), it's team-shared — record it in the repo's own `CLAUDE.md`, not memory. If the fact is about Bo's own environment or workflow (which calendar, which local directory, where a personal record gets written), it's personal — project memory is correct.

## Session Hygiene

If a conversation opens with a "continued from a previous conversation that ran out of context" summary, tell Bo immediately and suggest `/clear` before continuing, rather than building further on the compacted history. Hitting that limit once already means the session ran longer than it should have.

This matters even for a session used to derive daily recaps: the recap skill reads git log, plan.md files, calendar, and that day's own session transcript file on disk, not live scrollback. `/clear` after `/daily-recap` loses nothing.

## Never Push Without Explicit Permission

Do not run `git push` (or any variant: `--force`, `-u`, etc.) unless the human has explicitly asked for it in the current message.

The workloop commits incrementally as slices complete. The human's own code review happens after all slices are committed — pushing before that review ships unverified work. A commit is local and safe; a push is public and irreversible.

This applies even if a previous message approved a push, or if a PR workflow seems to imply it. Each push requires fresh, explicit approval.
