---
name: code-review
description: Verify correctness, walk through changes with the human, handle fixes, and commit. Runs the verifier automatically — AC check if criteria are available, quality assessment always.
argument-hint: "[PR URL or #number for reviewer mode | acceptance criteria or base ref for owner mode (optional)]"
---

Walk through the current code changes with the human before committing.

## Mode Detection

Inspect `$ARGUMENTS` before doing anything else:

- **Reviewer Mode**: `$ARGUMENTS` contains a PR/MR reference — a URL from any platform (GitHub, Azure DevOps, GitLab) or a bare PR number (e.g. `#123`). You are reviewing someone else's code — you will propose comments, not make changes or commit.
- **Owner Mode**: no PR reference in `$ARGUMENTS`. You are reviewing your own changes before committing.

Record the mode. It governs the rest of the steps.

## Before Starting

**Reviewer Mode — check out the PR branch first:**

Invoke the `pr-platform` skill and resolve this repo's PR platform by its rules. State the result on one line: `PR platform: <platform> (<declared | detected>), gh <available | unavailable>`. This mode's `gh` commands (checkout, posting comments) assume it resolves to GitHub with `gh` available — if it doesn't, tell the human and ask how to proceed instead of running them.

Ask the human, in plain chat, on every Reviewer Mode run and before touching any branch: "Review in a worktree, or check the PR branch out in this checkout?" Wait for the answer. The current checkout may be running a local stack, so never default either way.

**Worktree:** skip the dirty-tree check, since the current checkout is left alone. If `.claude/worktrees/pr-<number>` already exists from an earlier round of this review, reuse it with `git -C .claude/worktrees/pr-<number> pull`. Otherwise create it:

```
gh pr view <PR URL or number from $ARGUMENTS> --json headRefName --jq .headRefName
git fetch origin <headRefName>
git worktree add .claude/worktrees/pr-<number> <headRefName>
```

If the PR is already merged or closed and the worktree exists, offer to remove it with `git worktree remove` instead of reviewing.

Run every later step (diff, verifier, file reads) from the worktree, using absolute paths, and give the verifier the worktree path. Install dependencies in the worktree from the lockfile before the verifier runs tests. Confirm the branch name and that the worktree exists before proceeding.

**This checkout:** check for a dirty working tree:

```
git status --porcelain
```

If dirty, stop and tell the human. Ask them to stash or commit before proceeding. Do not continue until clean.

Once clean, check out the PR branch:

```
gh pr checkout <PR URL or number from $ARGUMENTS>
```

Confirm the branch name and that the checkout succeeded before proceeding.

**Both modes:**

Check for a `CLAUDE.md` at the project root. Read it and apply project-specific context — architecture patterns, code style, domain language — so your explanations are grounded in what this project expects.

Check for a story plan at `docs/stories/*/plan.md`. If found, note the story name and its one-line summary — you'll surface it at the top of the review so the human has product context before the technical walk-through begins.

Invoke the `branching-model` skill and resolve the diff base by its rules — the nearest known ancestor among the repo's declared diff base and any release-pipeline branches, not a hardcoded `main`. State the result on one line before using it: `Diff base: <branch> (<source>)`, where the source is the repo's `CLAUDE.md`, the `workloop.integrationBranch` override, or the remote default. **Before using it, check whether HEAD itself is one of those declared branches** (trunk, integration branch, or any pipeline branch) rather than a feature branch cut from one — if so, this is likely a promotion or release audit, not a feature review. Say so and ask how to proceed instead of walking what could be a large, multi-PR diff as if it were one slice.

Run `git fetch origin <diff-base>` before computing the merge-base — a stale local ref silently pulls already-merged upstream commits into what looks like this PR's/slice's own diff.

Otherwise, run `git diff --stat $(git merge-base origin/<diff-base> HEAD)` and `git diff --name-only $(git merge-base origin/<diff-base> HEAD)` to understand the scope of changes.

## Step 1 — Verify

Record the **verifier baseline** as a fingerprint of HEAD plus the working tree. This is used later to avoid redundant re-invocations:

```
{ git rev-parse HEAD; git diff HEAD; git ls-files -o --exclude-standard; git ls-files -o --exclude-standard | xargs -r cat; } | shasum
```

Invoke the **verifier** subagent to review code quality and verify correctness. Tell it which mode this is (Owner or Reviewer) — it phrases its Approval Status section differently depending on which.

- If acceptance criteria are available (passed as `$ARGUMENTS`, or findable in `docs/stories/<slug>/plan.md`), verify each criterion.
- If no AC exists, skip the AC check and proceed to quality assessment only.

After the verifier completes, open the review with story context (if found) and the pre-flight summary:

> **Story:** [story name] — [one-line summary] *(omit if no plan.md found)*
> **Verifier Pre-flight**
> Quality: X/10 | AC: N/M met | Blockers: [none / list]

If there are blockers, name them here so they're on the human's radar before the walk-through begins.

The verifier's full report — strengths, refactoring suggestions, and test coverage analysis — is available in context and informs the walk-through. Per-file findings surface during each group; refactoring suggestions and test coverage gaps appear in the final consolidation.

## Step 2 — Walk Through the Changes

**a) Group the changed files by concern** — not alphabetically, but by what problem they solve together. Small changes may have only one group.

**b) For each group — present ONE group per response, then stop and wait:**
0. Open the response with a one-line mode header: `**Reviewing PR #<number>**` (Reviewer Mode) or `**Reviewing local changes**` (Owner Mode). Keep the mode anchored every turn rather than relying on the mode recorded once at the start.
1. Name the group and its purpose in one sentence
2. Read the relevant files and paste the meaningful changed code **verbatim in a code block** (typically 10–40 lines — actual file contents, not raw diff syntax), prefixed with the exact file path and line range shown (e.g. `src/foo.ts:42-58`) so the human can jump straight to it. The human cannot see file contents unless you paste them; never describe or reference code without showing it.
3. Explain **what changed** — specifically and concisely
4. Explain **why** — what problem this solves, what alternative was rejected, what constraint drove the structure. This is the most important part.
5. Surface any verifier findings for this group's files — present as "Verifier flagged:" with their priority. For each finding, paste the relevant code verbatim in a code block so the human can see exactly what is being discussed. If none, skip.
6. Note any additional quality issues you observe that the verifier didn't catch. Same rule: show the relevant code verbatim in a code block, never just describe it. These get the same fix-now/defer/skip treatment as verifier findings — self-observed issues aren't exempt from step 8's default.
7. **Comment audit.** Show the verifier's Comment Audit verdicts for this group's files, each comment in full with its verdict (`Keep`, `Remove — wrong`, or `Remove — weak`) and reason. Don't override a verdict. If a comment describing code this group touches is missing from the audit, audit it against `comment-quality` and show it with the others, marked as added during the walk-through. If the verifier listed none for this group, skip.
8. For each finding surfaced in steps 5–7:

   Before writing any of these, confirm the mode recorded in Mode Detection. `Fix now` / `defer` / `skip` belongs only to Owner Mode; `Proposed comment` belongs only to Reviewer Mode. If you're in Reviewer Mode and about to write "Fix now," you're in the wrong branch — write a proposed comment instead.

   **Owner Mode** — give your recommendation on its own line:
   > **Recommendation:** Fix now — [one-sentence reason]
   The label must be `fix now`, `defer`, or `skip`. Be direct: "Fix now — untested behavior in a TDD project is a blocker"; "Skip — cosmetic preference in a recovery-only path". Both `Remove — wrong` and `Remove — weak` comment-audit verdicts get `Fix now` — removing a comment is free, so there's no reason to defer or skip it. A `Keep` verdict needs no recommendation line; it's not a finding.

   Default to `fix now` for any finding on a line, function, or file this slice's diff already touches — the marginal cost is near zero, and work that gets deferred rarely gets picked up later on its own priority. `Defer` requires a concrete reason the fix is unsafe or disproportionate right now: a blast radius wider than this slice, a design decision that needs its own discussion, or a file this diff doesn't otherwise touch. "Not part of this ticket" alone doesn't qualify as a defer reason.

   **Reviewer Mode** — draft a proposed PR comment on its own line:
   > **Proposed comment ([Blocker | Suggestion | Question | Nit]):** [comment text] *(file:line if inline)*
   Frame the issue as a question, observation, or concern — do not prescribe a solution. Keep it to 1–2 sentences: state the concern and stop, no preamble or hedging (see Concise Comments in global `CLAUDE.md`, which covers PR review comments). Include the target file and line number when the finding is tied to a specific location. These are drafts: no comment is approved for posting per group — the single decision of what to post happens once, together, at the end (Step 2c).

   Before drafting a `Question`, try to answer it: read the code it asks about, then any companion PRs or docs named in the request. Draft the question only for what that leaves open, such as the author's intent or code in a repo you can't read. If the answer turns up, drop the comment, or restate it as a `Suggestion` or `Nit` that carries the evidence. A question the author could see the reviewer could have looked up costs them a round-trip.

   For comment-audit findings specifically, Reviewer Mode disposition depends on the verdict. `Remove — wrong` always becomes a proposed comment (Suggestion or Blocker depending on how misleading the claim is) — a false comment is a correctness risk for whoever maintains that code next, regardless of who wrote it. `Remove — weak` does not become a proposed comment by default: note it happened and move on, since raising a stranger's stylistic nit costs them a round-trip for something with no functional effect. Track weak-comment counts across the whole review; if the same weakness recurs three or more times, raise one bundled `Suggestion` in Step 2c's consolidation instead of one `Nit` per instance. `Keep` needs no comment at all.

9. **Owner Mode:** If any findings were surfaced (steps 5–7): ask "Want to fix any of these now, or continue?" Wait for an explicit answer — do not move on or start fixes without one. If the human calls out a fix, handle it immediately via Step 3 before proceeding to the next group. If the human pushes back on a `Keep` verdict specifically, that's not a fix request, it's a request to investigate: invoke the `comment-quality` skill and dig until the disposition resolves to one of removed, corrected, or identified tech debt (folds into Step 3b). This exploration is opt-in, triggered only by an explicit pushback — never run it automatically just because a comment was defended. If no findings: "Ready to move on?"

   **Reviewer Mode:** If any comments were proposed: ask "Do you agree with these, or any questions/concerns?" Use the answer to refine, merge, or drop drafts — this is not a posting decision, so don't frame it as one ("post", "approve", etc.). Findings may need rephrasing or grouping once later groups are in, so keep everything as drafts until Step 2c. Pushback on a `Keep` verdict triggers the same investigation described above, resolving to removed, corrected, or noted as tech debt — Reviewer Mode records no deferred findings of its own, so a tech-debt outcome here becomes a proposed comment instead. If no findings: "Ready to move on?"

**Do not present the next group until the human replies.** One group per response is the rule — not a suggestion.

**c) After all groups, consolidate:**
- 2–3 sentence summary of the full change
- Any remaining issues not already addressed during the walk-through:
  - **Blockers** (failing tests, unmet AC)
  - **Owner Mode:** Recommended fixes (quality issues, verifier refactoring suggestions, test coverage gaps) and optional improvements
  - Comment audit tally: comments removed (wrong), removed (weak), kept. **Reviewer Mode:** plus any bundled `Suggestion` raised here for a weak-comment pattern that recurred three or more times across the review.
  - If nothing remains: "No outstanding issues — the implementation looks clean."

**Owner Mode:** Ask: "Anything else to address before committing? Call out by number, or say 'commit' to proceed."

**Reviewer Mode:** Ask: "Any comments to add or edit? Call out by number, or say 'continue' to move to per-comment wording review." This is a scope check, not a posting decision — Step 3 still walks each comment individually for exact wording before anything posts. Never use the word "post" in this question; it is reserved for Step 3's own gate.

## Step 3 — Fix Loop (Owner Mode) / Post Comments (Reviewer Mode)

### Owner Mode — Fix Loop

Keep a running list of files changed during this fix session.

For each approved fix:
1. Invoke the **coder** subagent with specific, scoped instructions — reference the exact file and issue
2. After the coder finishes, do a targeted re-walk: show the updated code, explain what changed. Keep it brief — context is already established.
3. Add the changed files to the fix session list.
4. Ask: "Good? Anything else to adjust?"
5. Repeat for remaining fixes.

Once all requested fixes are done, ask:

> "Want a clean pass before committing?"

If **yes**: recompute the fingerprint and compare it to the verifier baseline from Step 1. If it is unchanged (no commits and no working-tree edits since the last verifier run), the full verifier report is still valid — skip re-invoking the verifier and proceed directly to the targeted re-walk below. If it changed, re-invoke the **verifier** subagent, passing it the list of files changed during this fix session and instructing it to focus its scan on those files for regressions and new issues; for all other files, only surface findings not previously addressed. The Comment Audit still covers every comment in scope across the whole diff, not only the fix-session files. Update the verifier baseline.

Either way, walk through the files changed during this fix session using the same per-group format from Step 2 (show code, explain, surface verifier findings, give recommendations). If new issues come up, go through the per-group decision point and fix as needed, then offer another clean pass. Repeat until the human is satisfied or declines.

If **no**: proceed to Step 3b.

### Step 3b — Deferred Findings (Owner Mode only)

Before committing, settle where every deferred finding from this review goes.

1. **Collect deferred findings.** Gather every finding from Step 2 (and any surfaced during the Fix Loop) whose final disposition is `defer` — recommended defer and left unfixed, or explicitly deferred by the human. Also include any comment-audit `Keep` verdict that, after pushback investigation (Step 2b), resolved to identified tech debt rather than removal or correction. Skip anything disposed as `fix now` (already handled above) or `skip` (not real debt, no record needed).
2. **Record each one in the story.** Append it to this story's `docs/stories/<slug>/plan.md` under a `## Deferred findings` heading (create the heading if this is the first entry), with file and lines, a one-line issue, and why it's deferred: the concrete reason it's unsafe or disproportionate to fix now (blast radius wider than this slice, a design decision needing its own discussion, or a file outside this diff), never "not part of this ticket".
3. **Ask where each one goes next.** Present the deferred findings together, one line each, and ask the human where each should go. Typical destinations: the backlog when the `tracking-config` memory sets `Backlog`, a debt file in the repo, a new ticket in the team's tracker, or nowhere beyond the plan. When a `debt-tracking-config` project memory names a usual destination, propose it as the default. Never write to a destination the human didn't choose. For a ticket, create it through an available tracker connector only on the human's go-ahead; otherwise present a title and description as paste-ready text.
4. **Resolved items.** If a fix made during this review resolves something already recorded in the backlog or a debt file, point it out and ask whether to remove or close it.

If there's nothing deferred and nothing resolved, skip this step silently and proceed to commit.

### Reviewer Mode — Post Comments

Before posting anything, walk the human through every comment queued for posting one at a time, each in its own message: category, file:line (if inline), and the complete literal comment text exactly as it would post, as a blockquote. Never compress into a summary table or a one-line-per-entry list — the human needs to proofread the exact text landing on someone else's PR, not a paraphrase, and wants to do it per-comment, not skim a batch. Get an explicit go/edit/drop on each before moving to the next.

Once every comment has been confirmed individually, ask: "Ready to post these?"

On approval, post each comment:
- **Inline comment** (file and line known): `gh api repos/{owner}/{repo}/pulls/{number}/comments` with `body`, `commit_id` (from `git rev-parse HEAD`), `path`, and `line`
- **General comment** (no specific line): `gh pr review {number} --comment -b "{text}"`

Confirm which comments posted successfully. Do not make any code changes to the branch. If the human asks you to fix something directly, confirm explicitly before touching any files — modifying another person's PR is the exception, not the norm.

## Step 4 — Commit (Owner Mode) / Save Review Doc (Reviewer Mode)

### Owner Mode — Commit

Once the human is satisfied, ask for explicit commit approval:

> "Approve to commit?"

Commit on approval with a clear commit message describing the change.

**Log it, if this project keeps an activity log.** If a `tracking-config` project memory exists with `Activity log: enabled`, append one activity-log entry (see the `activity-log` skill for format/location) per repo touched (domain inferred from the changed files, asking only if genuinely ambiguous), describing what was committed in one line, referencing the story's `plan.md` if one was found earlier.

### Reviewer Mode — Done

The review is complete once comments are posted. If a `tracking-config` project memory exists, record the outcome on this PR's row in the live tracker README, adding the row if none matches, per the `tracking` skill's workloop checkpoints.

**Log it, if this project keeps an activity log.** If a `tracking-config` project memory exists with `Activity log: enabled`, append one `PR review - <domain>`-tagged activity-log entry (see the `activity-log` skill for format/location) (domain inferred from what was reviewed, asking only if genuinely ambiguous), describing the review's outcome in one line, referencing the PR link.
