---
name: standup
description: Prepares a personal daily standup update from your own commits — covers the previous work day (Friday if Monday) and today so far, split by AM/PM with a prose synthesis for each block. Scans workspace repos by default; pass a directory path to scan all git repos found under it instead.
argument-hint: "[/optional/directory/to/scan]"
---

Prepare my daily standup update from my own commits.

Optional argument: $ARGUMENTS

---

## Step 1 — Identify repos to scan

**If an argument was provided** and it is a directory path:
- Run `find <argument> -maxdepth 2 -name ".git" -type d` to discover all git repos under that directory (up to 2 levels deep).
- Strip the `/.git` suffix from each result to get the repo root paths.
- Use these as the repos to scan.

**If no argument was provided**:
- Read the list of working directories from the session context (primary working directory plus any additional working directories).
- Use these as the repos to scan.

## Step 2 — Determine the time window

Today's date and current time are available from the session context.

Calculate two windows:

**Previous work day** — the most recent calendar day before today that was a weekday:
- If today is Monday, the previous work day is Friday.
- Otherwise, it is yesterday.
- Split that day into AM (midnight → 11:59 AM local) and PM (noon → 11:59 PM local).

**Today so far** — midnight local time to now.
- If the current time is before noon, this is a single "Today" block.
- If the current time is at or after noon, split into AM (midnight → 11:59 AM) and PM (noon → now).

## Step 3 — Detect your identity

For each repo, run:
```
git -C <repo-path> config user.email
git -C <repo-path> config user.name
```

Collect all unique name/email values across repos. You will use these to filter commits in the next step.

## Step 4 — Collect your commits

For each repo, query each time block separately using `--after` and `--before` bounds and `--author` filtering:

```
git -C <repo-path> log \
  --after="<block-start>" \
  --before="<block-end>" \
  --author="<your name or email>" \
  --pretty=format:"%h|%s|%ar" \
  --all-remotes=false
```

Run on `HEAD` (local branch history). Do not fetch — this is a local-only operation.

Tag each result with its repo name (the final path component of the repo root). Collect results per time block across all repos into a single merged list, sorted by commit timestamp.

## Step 5 — Collect uncommitted WIP

For each repo, check for any uncommitted work:

```
git -C <repo-path> status --short
git -C <repo-path> diff --stat HEAD
```

If either returns output, read the full diff to understand what is in flight:

```
git -C <repo-path> diff HEAD
```

Tag each WIP file with its repo name. Collect WIP findings across all repos.

## Step 6 — Present the standup update

Omit any block that has no activity. If all blocks and WIP are empty, say so plainly and stop.

Format each commit block as follows:

```
**[Block label]**
[1-2 sentence prose synthesis]
  • [repo-name] `abc1234` [commit subject]
  • [repo-name] `def5678` [commit subject]
```

Block labels:
- `Yesterday AM` / `Yesterday PM` (or `Friday AM` / `Friday PM` on Mondays, etc.)
- `Today` (single block if before noon) or `Today AM` / `Today PM so far` (if at or after noon)
- `In progress` — always the final block; present only if uncommitted WIP exists

The **In progress** block has no commit list. Instead, write a 1-2 sentence prose description of what the uncommitted changes are doing, followed by a file summary:

```
**In progress**
Working on X — describe the area and intent of the uncommitted changes.
  ~ [repo-name] path/to/changed/file (N lines)
  ~ [repo-name] path/to/changed/file (N lines)
```

Use `~` instead of `•` to visually distinguish WIP from committed work.

**Writing the prose synthesis:**

The synthesis is what you say aloud at standup. Write it to be understood by both engineers and non-engineers on your team.

- Lead with the area or feature, not the implementation mechanic. "Finished the token refresh flow" not "Refactored the TokenService class."
- If commits span multiple features or repos, connect them with "and" or "also" rather than listing.
- One sentence is usually enough. Two only if the work genuinely spans distinct areas.
- Do not start with "I" — standup convention. Start with the verb or the subject area.
  - Good: "Finished the auth refresh flow and patched an expiry edge case."
  - Avoid: "I worked on the auth refresh flow."
- Do not reference commit hashes or branch names in the prose.

## Step 7 — Offer drill-down

After presenting the update, say:

> "Let me know if you want to expand on any of these for more context."

Then wait. Do not read diffs or expand commits proactively.

## Step 8 — Handle drill-down

If asked to expand on a commit or area:

1. Run `git -C <repo-path> show <hash>` to read the full diff.
2. Write a 2–4 sentence explanation of what the change does and why, suitable for explaining to a technical teammate in conversation.

If asked to expand on the WIP:

1. The diff is already loaded from Step 5 — use it directly.
2. Write a 3–5 sentence explanation of the work in progress: what problem it's solving, what approach is being taken, and how far along it appears to be.
