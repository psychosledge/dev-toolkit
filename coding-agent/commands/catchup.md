---
name: catchup
description: Summarizes recent team activity across all workspace repos — fetches all remotes, lists active branches and commits in a configurable time window, then stays interactive for drill-down on any branch or commit.
argument-hint: "[time window: yesterday, friday, 1d, 3d, 7d (default)]"
---

Catch up on what the team has been doing across all repos in the current workspace.

Time window argument: $ARGUMENTS

---

## Step 1 — Identify workspace repos

Read the list of working directories from the session context (primary working directory plus any additional working directories). These are the repos to scan.

## Step 2 — Parse the time window

Interpret the argument as:

| Argument | Meaning |
|---|---|
| *(none)* | Last 7 days |
| `1d`, `3d`, `7d`, `Nd` | Last N calendar days |
| `Nh` | Last N hours |
| `yesterday` | Since start of yesterday (local midnight) |
| `friday` / `since-friday` | Since the most recent past Friday at midnight local time |

Convert to an ISO 8601 cutoff timestamp to use with `git log --after`.

## Step 3 — Fetch and collect activity per repo

For each workspace repo, work through the following. If the repo has no configured remote, note it and skip to the next repo.

**3a. Fetch**
```
git fetch --all --prune
```

**3b. Find active branches**

Get all remote-tracking branches, then filter to those with at least one commit newer than the cutoff:
```
git log --oneline --after="<cutoff>" origin/<branch>
```

**3c. Separate into two groups**

- **In progress**: branches that have NOT been merged into the default branch. Check with:
  ```
  git branch -r --merged origin/main   # or origin/master
  ```
  Any remote branch not in that list with recent commits is in-progress.

- **Recently merged to main**: commits on `origin/main` (or `origin/master`) itself that are newer than the cutoff.

**3d. Collect commit data per in-progress branch**

```
git log origin/<branch> --after="<cutoff>" --pretty=format:"%h|%s|%an|%ar"
```

Cap at 15 commits per branch. If there are more, note "and N more commits" at the end.

**3e. Check for PR status (optional)**

Only if both conditions hold: `gh` CLI is available (`which gh`) AND the repo has a GitHub remote (`git remote -v | grep github.com`).

If both hold:
```
gh pr list --head <branch> --json number,title,state,isDraft,reviewDecision
```

If `gh` is unavailable or the repo has no GitHub remote, skip silently — do not mention the absence.

## Step 4 — Present the summary

Use this format:

```
## Team Activity — [human-readable window, e.g. "Last 7 Days" or "Since Friday"]
*N repos scanned — N active*

---

### [repo-name]
*Last activity: [relative time]*

**In Progress**

**[branch-name]** — [author of most recent commit] · [N commits]  [PR #N: "title" — open / draft / changes requested]
  • [commit subject] — [author], [relative time]
  • [commit subject] — [author], [relative time]

**Recently Merged to Main**
  • [commit subject] — [author], [relative time]
  • ...

---

[repeat per active repo, sorted by most-recent activity]

*No activity in this window: [repo], [repo]*
```

Omit the **Recently Merged to Main** section entirely if main has no new commits in the window. Omit the PR line if no PR was found. Sort repos by most-recent activity first; within a repo, sort branches by most-recent commit.

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
