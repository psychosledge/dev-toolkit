---
name: catchup
description: Fetches all remotes and shows everything not yet local by default (unpulled commits, new remote branches, stale local branches). Pass a time window to show team activity instead.
argument-hint: "[(none) = remote gap] | [time window: yesterday, friday, 1d, 3d, 7d]"
---

Catch up on what the team has been doing across all repos in the current workspace.

Argument: $ARGUMENTS

---

## Step 1 — Identify workspace repos

Read the list of working directories from the session context (primary working directory plus any additional working directories). These are the repos to scan.

## Step 2 — Determine mode

**If no argument is given:** run **Mode B — Remote Gap** (Steps 3B and 4B below).

**If an argument is given:** interpret it as a time window and run **Mode A — Time Window** (Steps 3A and 4A).

Time window interpretation:

| Argument                  | Meaning                                                  |
| ------------------------- | -------------------------------------------------------- |
| `1d`, `3d`, `7d`, `Nd`    | Last N calendar days                                     |
| `Nh`                      | Last N hours                                             |
| `yesterday`               | Since start of yesterday (local midnight)                |
| `friday` / `since-friday` | Since the most recent past Friday at midnight local time |

Convert to an ISO 8601 cutoff timestamp to use with `git log --after`.

---

> **Multi-repo safety:** Always target repos by absolute path using `git -C <absolute-path> <command>` (or run each repo's commands in a separate Bash call). Never use `cd` + `git` in the same shell invocation across multiple repos — the working directory persists between chained commands and will silently run later git commands against the wrong repo.

---

## Step 3A — Fetch and collect activity per repo (Mode A: Time Window)

Work through the following for all workspace repos. **Run each step as a single parallel batch across all repos** — one Bash call per repo, all fired simultaneously. If a repo has no configured remote, note it and skip it in all subsequent steps.

**3A-a. Fetch**

```
git -C <repo-path> fetch --all --prune
```

**3A-a2. Resolve diff base**

Invoke the `branching-model` skill and resolve this repo's diff base by its rules (repo's own `CLAUDE.md` `## Branching` declaration → `git -C <repo-path> config workloop.integrationBranch` → remote default branch). State the result on one line before using it: `Diff base: <branch> (<source>)`, where the source is the repo's `CLAUDE.md`, the `workloop.integrationBranch` override, or the remote default. Use the resolved branch everywhere below instead of assuming `main`/`master`.

**3A-b. Find active branches**

Get all remote-tracking branches, then filter to those with at least one commit newer than the cutoff:

```
git log --oneline --after="<cutoff>" origin/<branch>
```

**3A-c. Separate into two groups**

- **In progress**: branches that have NOT been merged into the resolved diff base. Check with:

  ```
  git branch -r --merged origin/<diff-base>
  ```

  Any remote branch not in that list with recent commits is in-progress. Exclude any branch that is itself a declared release-pipeline branch — those are long-lived deploy branches, not work in progress.

- **Recently merged to `<diff-base>`**: commits on the resolved diff base branch itself that are newer than the cutoff.

**3A-d. Collect commit data per in-progress branch**

```
git log origin/<branch> --after="<cutoff>" --pretty=format:"%h|%s|%an|%ar"
```

The `%h` short hash must be included in every commit line in the output.

Cap at 15 commits per branch. If there are more, note "and N more commits" at the end.

**3A-e. Check for PR status (optional)**

Invoke the `pr-platform` skill and resolve this repo's PR platform by its rules. State the result on one line: `PR platform: <platform> (<declared | detected>), gh <available | unavailable>`. Only if it resolves to GitHub with `gh` available:

```
gh pr list --head <branch> --json number,title,state,isDraft,reviewDecision
```

If the platform isn't GitHub, or `gh` is unavailable, skip silently — do not mention the absence.

## Step 4A — Present the time-window summary

Use this format:

```
## Team Activity — [human-readable window, e.g. "Last 7 Days" or "Since Friday"]
*N repos scanned — N active*

---

### [repo-name]
*Last activity: [relative time]*

**In Progress**

**[branch-name]** — [author of most recent commit] · [N commits]  [PR #N: "title" — open / draft / changes requested]
  • `abc1234` [commit subject] — [author], [relative time]
  • `abc1234` [commit subject] — [author], [relative time]

**Recently Merged to `<diff-base>`**
  • `abc1234` [commit subject] — [author], [relative time]
  • ...

---

[repeat per active repo, sorted by most-recent activity]

*No activity in this window: [repo], [repo]*
```

Omit the **Recently Merged to `<diff-base>`** section entirely if the diff base has no new commits in the window. Omit the PR line if no PR was found. Sort repos by most-recent activity first; within a repo, sort branches by most-recent commit.

Then skip to **Step 5**.

---

## Step 3B — Fetch and collect remote gap per repo (Mode B: Unsynced)

Work through the following for all workspace repos. **Run each step as a single parallel batch across all repos** — one Bash call per repo, all fired simultaneously. If a repo has no configured remote, note it and skip it in all subsequent steps.

**3B-a. Fetch with prune**

```
git -C <repo-path> fetch --all --prune
```

The prune removes stale remote-tracking refs and is what surfaces the "gone" state below.

**3B-a2. Resolve this repo's branching model**

Invoke the `branching-model` skill and resolve by its rules. State the result on one line before using it: `Diff base: <branch> (<source>)`, plus the release pipeline if one is declared.
- **Diff base** — used for merge/staleness checks below.
- **Release pipeline** — ordered list of long-lived deploy branches, if declared. Trunk-based repos have none.

If the repo's own `CLAUDE.md` has no `## Branching` section, fall back to:
```
git -C <repo-path> config workloop.integrationBranch
```
then to:
```
git -C <repo-path> symbolic-ref refs/remotes/origin/HEAD
```
(strip the `refs/remotes/origin/` prefix to get the branch name).

**Missed-pipeline-branch check** (only if nothing is declared): check whether a `dev` branch exists on the remote and is not merged into the resolved diff base:

```
git -C <repo-path> branch -r | grep origin/dev
git -C <repo-path> branch -r --merged origin/<diff-base> | grep origin/dev
```

If `origin/dev` exists but is NOT merged in, that's a concrete signal per the `branching-model` skill's detection rules — ask directly rather than emitting a static tip:

> "`origin/dev` has unmerged commits relative to `origin/<diff-base>` — is `dev` actually this repo's integration branch? I can record that in this repo's `CLAUDE.md` if so."

On confirmation, write the `## Branching` section into that repo's `CLAUDE.md` as described in the `branching-model` skill.

> **Batch these queries:** Steps 3B-b, 3B-c, and 3B-d all read local branch state. After the fetch wave completes, fire `branch -r`, `branch -vv`, and `branch -r --merged origin/<diff-base>` for all repos simultaneously in a single parallel batch before processing any results.

**3B-a3. Compute release-pipeline drift** (only if a pipeline is declared)

For each adjacent pair in the declared pipeline (upstream → downstream):

```
git -C <repo-path> rev-list --count origin/<upstream>..origin/<downstream>
```

This is how many commits the downstream branch is missing from its upstream hop. Report per hop in Step 4B.

**3B-b. New remote branches** (branches on remote with no local counterpart, not yet merged)

```
git -C <repo-path> branch -r | grep -v '\->'
```

Cross-reference with local branches to find remote branches that have no local tracking branch. Then filter out:
- any already merged into the diff base resolved in step 3B-a2:
  ```
  git -C <repo-path> branch -r --merged origin/<diff-base>
  ```
- any branch that is itself a declared release-pipeline branch — those are long-lived deploy branches, reported separately in 3B-a3/4B, not "new work."

Silently skip any remote branch that appears in that merged list. Only branches with commits **not yet in the diff base** should be shown.

For each remaining branch, collect the 5 most recent commits, including author email so it can be compared against `git -C <repo-path> config user.email` (needed for 3B-b2 below):

```
git -C <repo-path> log origin/<branch> -5 --pretty=format:"%h|%s|%an|%ae|%ar"
```

**3B-b2. Detect feature-branch naming convention** (only if `Feature branch naming` is undeclared)

Using the branches and commit authors collected in 3B-b: restrict to branches with activity in the **last 30 days**, split by whether the branch's most recent commit author email matches `git -C <repo-path> config user.email`. Prefer whatever pattern the **other-authored** set shows — self-authored branches may just reflect this skill's own past default, not real team convention. If the other-authored set is too sparse to conclude anything, note that rather than falling back silently.

If a consistent shape emerges, surface it as a finding plus a recommendation and ask before recording anything, e.g. *"4 of 5 other-authored branches in the last 30 days follow `<TICKET>/<slug>`; recommend canonizing that — record it?"* If the sample is mixed, stay silent — don't force a canon on weak signal.

**3B-c. Tracked branches with unpulled commits** (local branch is behind its upstream)

```
git -C <repo-path> branch -vv
```

For every local branch showing `[origin/<name>: behind N]`, collect those unpulled commits:

```
git -C <repo-path> log HEAD..origin/<branch> --pretty=format:"%h|%s|%an|%ar"
```

If the local branch is checked out, it will appear as the current branch (`*`) — note it.

**3B-d. Stale local branches** (local branch whose remote tracking ref has been deleted)

From the `git branch -vv` output, any branch showing `[gone]` is a local branch whose remote was deleted. List these by name only.

**3B-e. Local branch ownership**

For every local branch except the resolved diff base itself (the diff base is shared trunk, not owned by anyone), determine whose work it is:

```
git -C <repo-path> log -1 --pretty=format:"%an|%ae" <branch>
```

Compare the email against:

```
git -C <repo-path> config user.email
```

A match is `mine`; anything else is `not mine`, owned by that commit's author name. This is a tip-commit check, not a "did I ever commit here" check — a branch you checked out to review someone else's PR carries their name, even if your name is attached to the repo elsewhere.

Note the branch's sync state alongside ownership, from the `branch -vv` output already collected in 3B-c/3B-d: `in sync`, `behind N`, `gone`, or `local-only` (no upstream configured at all, e.g. a scratch branch made for a review).

## Step 4B — Present the remote-gap summary

Use this format:

```
## Remote Changes — Not Yet Local
*N repos scanned*

---

### [repo-name]

**Release Pipeline** (only if a pipeline is declared)
  dev → stage → demo → main (prod)
  - stage: 3 behind dev
  - demo: 3 behind stage (in sync with dev)
  - main (prod): 10 behind demo

**New Remote Branches**
  **[branch-name]** — [N commits], last by [author] [relative time]
    • `abc1234` [commit subject] — [author], [relative time]
    • ...

**Behind on Tracked Branches**
  **[branch-name]** ← [N commits] — [currently checked out, if applicable]
    • `abc1234` [commit subject] — [author], [relative time]
    • ...

**Stale Local Branches** (remote deleted)
  • [branch-name]
  • ...

**Local Branches** (ownership, all local branches except the diff base)
  **[branch-name]** — [owner] · [in sync / behind N / gone / local-only]  [mine | not mine]
  ...

---

[repeat per repo]

*All up to date: [repo], [repo]*
```

Omit any section that has nothing to report, including **Release Pipeline** when no pipeline is declared for that repo, and **Local Branches** when the only local branch in a repo is the diff base itself. If every section is empty for a repo, include it in the "All up to date" line instead of showing an empty block. Sort repos with changes first; within a repo, sort tracked-branch entries by how far behind they are (most behind first); within **Local Branches**, sort `not mine` before `mine`.

In **Local Branches**, flag any `not mine` entry that is also `gone` or already covered by the merge check in Step 4B-post2 as a likely delete candidate — but do not delete it there; deletion of any branch, `mine` or `not mine`, only happens after explicit confirmation, per Step 4B-post2.

If any unmerged remote branches appear old (4+ weeks with no recent commits), group them on one line rather than listing commits: `[branch], [branch] — old, likely squash-merged; will clear when remote is deleted.`

Then continue to **Step 4B-post**.

---

## Step 4B-post — Auto-sync fast-forwardable branches (Mode B only)

After presenting the summary, silently fast-forward every local tracked branch that is **strictly behind** its upstream (no diverged commits — `git branch -vv` showed `behind N` with no `ahead` component). Do this for all workspace repos.

For the **currently checked-out branch** in a repo:

```
git -C <repo-path> pull --ff-only
```

For **non-checked-out branches** that are strictly behind:

```
git -C <repo-path> fetch origin <branch>:<branch>
```

If a branch is **diverged** (shows both ahead and behind in `git branch -vv`), skip it — do not attempt a merge or rebase.

After syncing, output a single summary line:

```
*Synced: repo/branch (+N commits), repo/branch (+N commits) — repo/branch skipped (diverged)*
```

Omit the line entirely if nothing was synced and nothing needed skipping.

Then continue to **Step 4B-post2**.

## Step 4B-post2 — Suggest merged stale local branches for deletion (Mode B only)

For every branch collected in Step 3B-d (local branch flagged `[gone]`), check whether its content is already incorporated into the resolved diff base, using patch-id equivalence rather than commit ancestry:

```
git -C <repo-path> cherry origin/<diff-base> <branch>
```

Do NOT use `git merge-base --is-ancestor` for this — a squash- or rebase-merge (the GitHub default) rewrites the commit hash, so the original commit is never literally an ancestor of the diff base even though its content landed. `git cherry` compares patch content instead, so it correctly detects squash- and rebase-merges.

Empty output, or output where every line starts with `-` (patch-equivalent commit found upstream), means fully merged — it's a delete candidate.

Any line starting with `+` (no patch-equivalent commit found upstream) means not fully merged — skip it, keep the branch, and report it as skipped (not merged) rather than silently dropping it from the summary.

Never delete a branch in this step. Report the delete candidates and wait for explicit confirmation:

```
*Merged and safe to delete: repo/branch, repo/branch — confirm to delete.*
```

Omit the line entirely if there were no `[gone]` branches to process, or none were fully merged.

Only on explicit confirmation from the human, delete the confirmed branches:

```
git -C <repo-path> branch -D <branch>
```

(`-D` here is safe specifically because the check above already verified the content against `origin/<diff-base>`, not because force-delete is being used carelessly.) Delete only the branches the human confirmed, not the full candidate list, if they narrow it down.

Then continue to **Step 5**.

---

## Step 5 — Invite drill-down

After the summary, say:

> "Ask me to go deeper on any branch or commit — e.g. 'summarize the auth-refresh branch' or 'walk me through commit abc1234'."

Then wait. Do not read diffs proactively.

## Step 6 — Handle drill-down on a branch

When asked to summarize a branch:

1. If the branch exists in multiple repos, ask which one before proceeding.
2. Find the merge base against the resolved diff base (nearest known ancestor among the diff base and any declared release-pipeline branches — reuse the resolution from Step 3A-a2/3B-a2 if this is the same session, otherwise invoke the `branching-model` skill and re-resolve by its rules):
   ```
   git merge-base origin/<diff-base> origin/<branch>
   ```
3. Show changed files and size:
   ```
   git diff <merge-base>..origin/<branch> --stat
   ```
4. List all commits on the branch since the merge base:
   ```
   git log <merge-base>..origin/<branch> --pretty=format:"%h %s (%an, %ar)"
   ```
5. Read the diff for changed files, grouped by directory, to understand the nature of the changes.
6. Write a 3–5 sentence prose summary: what the branch is doing, what approach it takes, what's been completed so far, and what (if anything) looks incomplete or in flux.

## Step 7 — Handle drill-down on a specific commit

When asked to explain a commit:

1. Show the commit's changed files:
   ```
   git show <hash> --stat
   ```
2. Read the full diff:
   ```
   git show <hash>
   ```
3. Write a 2–4 sentence explanation: what this commit does, why (drawn from the commit message and diff), and which areas of the codebase it touches.
