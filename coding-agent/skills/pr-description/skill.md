---
name: pr-description
description: Writes pull request descriptions. Use when creating a PR, writing a PR, or when the user asks to summarize changes for a pull request.
---

When writing a PR description:

1. Invoke the `branching-model` skill and resolve the diff base by its rules — the nearest known ancestor among the repo's declared diff base and any release-pipeline branches, not a hardcoded `main`. State the result on one line before using it: `Diff base: <branch> (<source>)`, where the source is the repo's `CLAUDE.md`, the `workloop.integrationBranch` override, or the remote default. Run `git diff <diff-base>...HEAD` to see all changes on this branch.
2. Write a description following this format:

## What
One sentence explaining what this PR does.

## Why
Brief context on why this change is needed

## Changes
- Bullet points of specific changes made
- Group related changes together
- Mention any files deleted or renamed
