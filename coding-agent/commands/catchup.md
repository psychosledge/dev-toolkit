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

**3A-b. Find active branches**

Get all remote-tracking branches, then filter to those with at least one commit newer than the cutoff:

```
git log --oneline --after="<cutoff>" origin/<branch>
```

**3A-c. Separate into two groups**

- **In progress**: branches that have NOT been merged into the default branch. Check with:

  ```
  git branch -r --merged origin/main   # or origin/master
  ```

  Any remote branch not in that list with recent commits is in-progress.

- **Recently merged to main**: commits on `origin/main` (or `origin/master`) itself that are newer than the cutoff.

**3A-d. Collect commit data per in-progress branch**

```
git log origin/<branch> --after="<cutoff>" --pretty=format:"%h|%s|%an|%ar"
```

The `%h` short hash must be included in every commit line in the output.

Cap at 15 commits per branch. If there are more, note "and N more commits" at the end.

**3A-e. Check for PR status (optional)**

Only if both conditions hold: `gh` CLI is available (`which gh`) AND the repo has a GitHub remote (`git remote -v | grep github.com`).

If both hold:

```
gh pr list --head <branch> --json number,title,state,isDraft,reviewDecision
```

If `gh` is unavailable or the repo has no GitHub remote, skip silently — do not mention the absence.

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

**Recently Merged to Main**
  • `abc1234` [commit subject] — [author], [relative time]
  • ...

---

[repeat per active repo, sorted by most-recent activity]

*No activity in this window: [repo], [repo]*
```

Omit the **Recently Merged to Main** section entirely if main has no new commits in the window. Omit the PR line if no PR was found. Sort repos by most-recent activity first; within a repo, sort branches by most-recent commit.

Then skip to **Step 5**.

---

## Step 3B — Fetch and collect remote gap per repo (Mode B: Unsynced)

Work through the following for all workspace repos. **Run each step as a single parallel batch across all repos** — one Bash call per repo, all fired simultaneously. If a repo has no configured remote, note it and skip it in all subsequent steps.

**3B-a. Fetch with prune**

```
git -C <repo-path> fetch --all --prune
```

The prune removes stale remote-tracking refs and is what surfaces the "gone" state below.

**3B-a2. Resolve integration branch per repo**

For each repo, determine the integration branch using this two-step lookup — run both in the same parallel batch as the fetch where possible:

1. **Check for an explicit override first:**

   ```
   git -C <repo-path> config catchup.integrationBranch
   ```

   If this returns a value, use it. Stop here.

2. **Fall back to the remote default branch:**
   ```
   git -C <repo-path> symbolic-ref refs/remotes/origin/HEAD
   ```
   Strip the `refs/remotes/origin/` prefix to get the branch name (e.g. `main`, `master`).

**After resolving**, check whether a `dev` branch exists on the remote AND is not already merged into the resolved integration branch:

```
git -C <repo-path> branch -r | grep origin/dev
git -C <repo-path> branch -r --merged origin/<integration> | grep origin/dev
```

If `origin/dev` exists but is NOT merged in, emit a hint at the end of this repo's section:

```
Tip: origin/dev has unmerged commits — if it's your integration branch, run: git -C <repo-path> config catchup.integrationBranch dev
```

> **Batch these queries:** Steps 3B-b, 3B-c, and 3B-d all read local branch state. After the fetch wave completes, fire `branch -r`, `branch -vv`, and `branch -r --merged origin/<integration>` for all repos simultaneously in a single parallel batch before processing any results.

**3B-b. New remote branches** (branches on remote with no local counterpart, not yet merged)

```
git -C <repo-path> branch -r | grep -v '\->'
```

Cross-reference with local branches to find remote branches that have no local tracking branch. Then filter out any already merged into the integration branch resolved in step 3B-a2:

```
git -C <repo-path> branch -r --merged origin/<integration>
```

Silently skip any remote branch that appears in that merged list. Only branches with commits **not yet in the integration branch** should be shown.

For each remaining branch, collect the 5 most recent commits:

```
git -C <repo-path> log origin/<branch> -5 --pretty=format:"%h|%s|%an|%ar"
```

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

## Step 4B — Present the remote-gap summary

Use this format:

```
## Remote Changes — Not Yet Local
*N repos scanned*

---

### [repo-name]

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

---

[repeat per repo]

*All up to date: [repo], [repo]*
```

Omit any section that has nothing to report. If every section is empty for a repo, include it in the "All up to date" line instead of showing an empty block. Sort repos with changes first; within a repo, sort tracked-branch entries by how far behind they are (most behind first).

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

Then continue to **Step 5**.

---

## Step 5 — Invite drill-down

After the summary, say:

> "Ask me to go deeper on any branch or commit — e.g. 'summarize the auth-refresh branch' or 'walk me through commit abc1234'."

Then wait. Do not read diffs proactively.

## Step 6 — Handle drill-down on a branch

When asked to summarize a branch:

1. If the branch exists in multiple repos, ask which one before proceeding.
2. Find the merge base against the default branch:
   ```
   git merge-base origin/main origin/<branch>
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
