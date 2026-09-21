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

Resolve this repo's PR Platform per the PR Platform instructions in global `CLAUDE.md`. This mode's `gh` commands (checkout, posting comments) assume it resolves to GitHub with `gh` available — if it doesn't, tell the human and ask how to proceed instead of running them.

Check for a dirty working tree:

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

Resolve the diff base per the Branching Model instructions in global `CLAUDE.md` — the nearest known ancestor among the repo's declared diff base and any release-pipeline branches, not a hardcoded `main`. **Before using it, check whether HEAD itself is one of those declared branches** (trunk, integration branch, or any pipeline branch) rather than a feature branch cut from one — if so, this is likely a promotion or release audit, not a feature review. Say so and ask how to proceed instead of walking what could be a large, multi-PR diff as if it were one slice.

Otherwise, run `git diff --stat $(git merge-base <diff-base> HEAD)` and `git diff --name-only $(git merge-base <diff-base> HEAD)` to understand the scope of changes.

## Step 1 — Verify

Run `git rev-parse HEAD` and record the hash as the **verifier baseline HEAD**. This is used later to avoid redundant re-invocations.

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
2. Read the relevant files and paste the meaningful changed code **verbatim in a code block** (typically 10–40 lines — actual file contents, not raw diff syntax). The human cannot see file contents unless you paste them; never describe or reference code without showing it.
3. Explain **what changed** — specifically and concisely
4. Explain **why** — what problem this solves, what alternative was rejected, what constraint drove the structure. This is the most important part.
5. Surface any verifier findings for this group's files — present as "Verifier flagged:" with their priority. For each finding, paste the relevant code verbatim in a code block so the human can see exactly what is being discussed. If none, skip.
6. Note any additional quality issues you observe that the verifier didn't catch. Same rule: show the relevant code verbatim in a code block, never just describe it. These get the same fix-now/defer/skip treatment as verifier findings — self-observed issues aren't exempt from step 8's default.
7. **Audit comments in this group's files.** Scope is every comment describing a line, function, or block this group touches, not just comment lines the diff itself added or edited — a diff can change what's true about the code around a comment without touching the comment's own text. This includes comments inside wholly new files, which won't show as `+` lines against the diff base the way changes to existing files do. Apply the bar `coder.md` and `verifier.md` already hold code to: a comment survives only if it states something the code can't say for itself (an ordering requirement, an external-system quirk, a rationale truly invisible in the code). For a comment with more than one clause or sentence, decompose it into its individual claims and judge each independently rather than rendering one holistic verdict — keep only the clauses that survive, trim to a single strong clause if the rest are weak, and remove the whole comment if none survive. Flag a rationale restated at a second location instead of stated once at its source, a comment describing behavior actually owned and implemented elsewhere (a different file, module, or component) even when accurate, and any comment citing an ADR/story/other internal doc by name or number instead of inlining the fact.

   Before a `Keep` verdict, verify the comment's claim against the actual code — don't grant one just because the claim sounds like the kind of thing that's allowed to survive. If the comment describes something outside what's shown in this group (another file, an external system, a doc), check it: grep the sibling code, read the referenced file. A claim that doesn't hold is `Remove — wrong`, not `Keep`, no matter how load-bearing it sounds.

   Show every comment found in this group, in full, with one of three verdicts:
   - `Keep: <reason>` — the bar is met and the claim checks out.
   - `Remove — wrong: <reason>` — the comment misdescribes the code (a correctness issue, not a style one).
   - `Remove — weak: <reason>` — the comment doesn't meet the bar but isn't inaccurate (redundant, restates the code, weak rationale).

   If no comments were added or touched in this group, skip.
8. For each finding surfaced in steps 5–7:

   Before writing any of these, confirm the mode recorded in Mode Detection. `Fix now` / `defer` / `skip` belongs only to Owner Mode; `Proposed comment` belongs only to Reviewer Mode. If you're in Reviewer Mode and about to write "Fix now," you're in the wrong branch — write a proposed comment instead.

   **Owner Mode** — give your recommendation on its own line:
   > **Recommendation:** Fix now — [one-sentence reason]
   The label must be `fix now`, `defer`, or `skip`. Be direct: "Fix now — untested behavior in a TDD project is a blocker"; "Skip — cosmetic preference in a recovery-only path". Both `Remove — wrong` and `Remove — weak` comment-audit verdicts get `Fix now` — removing a comment is free, so there's no reason to defer or skip it. A `Keep` verdict needs no recommendation line; it's not a finding.

   Default to `fix now` for any finding on a line, function, or file this slice's diff already touches — the marginal cost is near zero, and work that gets deferred rarely gets picked up later on its own priority. `Defer` requires a concrete reason the fix is unsafe or disproportionate right now: a blast radius wider than this slice, a design decision that needs its own discussion, or a file this diff doesn't otherwise touch. "Not part of this ticket" alone doesn't qualify as a defer reason.

   **Reviewer Mode** — draft a proposed PR comment on its own line:
   > **Proposed comment ([Blocker | Suggestion | Question | Nit]):** [comment text] *(file:line if inline)*
   Frame the issue as a question, observation, or concern — do not prescribe a solution. Keep it to 1–2 sentences: state the concern and stop, no preamble or hedging (see Concise Comments in global `CLAUDE.md`, which covers PR review comments). Include the target file and line number when the finding is tied to a specific location. These are drafts: no comment is approved for posting per group — the single decision of what to post happens once, together, at the end (Step 2c).

   For comment-audit findings specifically, Reviewer Mode disposition depends on the verdict. `Remove — wrong` always becomes a proposed comment (Suggestion or Blocker depending on how misleading the claim is) — a false comment is a correctness risk for whoever maintains that code next, regardless of who wrote it. `Remove — weak` does not become a proposed comment by default: note it happened and move on, since raising a stranger's stylistic nit costs them a round-trip for something with no functional effect. Track weak-comment counts across the whole review; if the same weakness recurs three or more times, raise one bundled `Suggestion` in Step 2c's consolidation instead of one `Nit` per instance. `Keep` needs no comment at all.

9. **Owner Mode:** If any findings were surfaced (steps 5–7): ask "Want to fix any of these now, or continue?" Wait for an explicit answer — do not move on or start fixes without one. If the human calls out a fix, handle it immediately via Step 3 before proceeding to the next group. If the human pushes back on a `Keep` verdict specifically, that's not a fix request, it's a request to investigate: dig until the disposition resolves to one of removed, corrected, or identified tech debt (folds into Step 3b). This exploration is opt-in, triggered only by an explicit pushback — never run it automatically just because a comment was defended. If no findings: "Ready to move on?"

   **Reviewer Mode:** If any comments were proposed: ask "Do you agree with these, or any questions/concerns?" Use the answer to refine, merge, or drop drafts — this is not a posting decision, so don't frame it as one ("post", "approve", etc.). Findings may need rephrasing or grouping once later groups are in, so keep everything as drafts until Step 2c. Pushback on a `Keep` verdict triggers the same investigation described above, resolving to removed, corrected, or noted as tech debt — Reviewer Mode has no `TECH_DEBT.md` to write to, so a tech-debt outcome here becomes a proposed comment or a note in the optional review doc from Step 4 instead. If no findings: "Ready to move on?"

**Do not present the next group until the human replies.** One group per response is the rule — not a suggestion.

**c) After all groups, consolidate:**
- 2–3 sentence summary of the full change
- Any remaining issues not already addressed during the walk-through:
  - **Blockers** (failing tests, unmet AC)
  - **Owner Mode:** Recommended fixes (quality issues, verifier refactoring suggestions, test coverage gaps) and optional improvements
  - **Reviewer Mode:** Any proposed comments not yet approved or skipped
  - Comment audit tally: comments removed (wrong), removed (weak), kept. **Reviewer Mode:** plus any bundled `Suggestion` raised here for a weak-comment pattern that recurred three or more times across the review.
  - If nothing remains: "No outstanding issues — the implementation looks clean."

**Owner Mode:** Ask: "Anything else to address before committing? Call out by number, or say 'commit' to proceed."

**Reviewer Mode:** Ask: "Any comments to add or edit before posting? Call out by number, or say 'post' to proceed."

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

If **yes**: run `git rev-parse HEAD` and compare to the verifier baseline HEAD from Step 1. If HEAD is unchanged (no new commits since the last verifier run), the full verifier report is still valid — skip re-invoking the verifier and proceed directly to the targeted re-walk below. If HEAD changed, re-invoke the **verifier** subagent, passing it the list of files changed during this fix session and instructing it to focus its scan on those files for regressions and new issues; for all other files, only surface findings not previously addressed. Update the verifier baseline HEAD.

Either way, walk through the files changed during this fix session using the same per-group format from Step 2 (show code, explain, surface verifier findings, give recommendations). If new issues come up, go through the per-group decision point and fix as needed, then offer another clean pass. Repeat until the human is satisfied or declines.

If **no**: proceed to Step 3b.

### Step 3b — Reconcile Tech Debt (Owner Mode only)

Before committing, reconcile every finding from this review against the durable tech-debt record.

Check project memory for this repo's debt-tracking file(s) beyond `TECH_DEBT.md`. Some repos split per-slice debt (`TECH_DEBT.md`, this command writes to it directly) from a separate systemic/curated list owned by another team — memory names that file and its write policy when one exists. Treat any such file as read-only cross-reference: never upsert into it automatically, even for a finding that reads as squarely systemic (true across the codebase, not particular to this slice) — surface it as a candidate for that file in the summary (step 4) and let the human decide whether and how to add it.

1. **Collect deferred findings.** Gather every finding from Step 2 (and any surfaced during the Fix Loop) whose final disposition is `defer` — recommended defer and left unfixed, or explicitly deferred by the human. Also include any comment-audit `Keep` verdict that, after pushback investigation (Step 2b), resolved to identified tech debt rather than removal or correction. Skip anything disposed as `fix now` (already handled above) or `skip` (not real debt, no record needed).
2. **Record each one, twice:**
   - Append to this story's `docs/stories/<slug>/plan.md` under a `## Deferred tech debt` heading (create the heading if this is the first entry in this story).
   - Upsert into `TECH_DEBT.md` at the root of the repo the finding belongs to (create the file if it doesn't exist yet). Use this entry format:
     ```
     ## <file path>
     - **Line(s):** <line numbers or range>
     - **Issue:** <one-line description>
     - **Why deferred:** <the concrete reason it's unsafe or disproportionate to fix now — blast radius wider than this slice, a design decision needing its own discussion, or a file outside this diff; not "not part of this ticket">
     - **Surfaced in:** <story slug>, Slice <N>
     ```
3. **Resolve entries this slice fixed.** Separately — if any fix made *during this slice* resolves a finding that already has an entry in `TECH_DEBT.md` (matched by file and description), remove that entry entirely. `TECH_DEBT.md` is a record of currently-known debt, not a historical log — entries don't accumulate once addressed. If removing an entry leaves the file with no remaining entries, delete the file.
4. **Show the human a short summary** of what's being added to and removed from `TECH_DEBT.md` (file names and one-line descriptions only), plus any candidates surfaced for another repo's curated debt file, before proceeding to commit. No separate approval gate needed for the `TECH_DEBT.md` changes — those ride along with the commit approval in Step 4. A candidate for another file is a separate ask, not folded into that approval.

If there's nothing to defer and nothing to resolve, skip this step silently and proceed to commit.

### Reviewer Mode — Post Comments

Show the human the complete list of approved comments before posting anything — one entry per line, formatted as: category, file:line (if inline), and comment text.

Ask: "Ready to post these?"

On approval, post each comment:
- **Inline comment** (file and line known): `gh api repos/{owner}/{repo}/pulls/{number}/comments` with `body`, `commit_id` (from `git rev-parse HEAD`), `path`, and `line`
- **General comment** (no specific line): `gh pr review {number} --comment -b "{text}"`

Confirm which comments posted successfully. Do not make any code changes to the branch. If the human asks you to fix something directly, confirm explicitly before touching any files — modifying another person's PR is the exception, not the norm.

## Step 4 — Commit (Owner Mode) / Save Review Doc (Reviewer Mode)

### Owner Mode — Commit

Once the human is satisfied, ask for explicit commit approval:

> "Approve to commit?"

Commit on approval with a clear commit message describing the change.

### Reviewer Mode — Done

The review is complete once comments are posted. Note the outcome (posted / held / resolved outside this flow) in the weekly tracker per the project's own conventions, if one is in use.
