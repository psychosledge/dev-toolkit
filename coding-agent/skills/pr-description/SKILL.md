---
name: pr-description
description: Writes pull request titles and descriptions. Use when creating a PR, writing a PR, or when the user asks to summarize changes for a pull request.
---

When writing a PR title and description:

1. Invoke the `branching-model` skill and resolve the diff base by its rules — the nearest known ancestor among the repo's declared diff base and any release-pipeline branches, not a hardcoded `main`. State the result on one line before using it: `Diff base: <branch> (<source>)`, where the source is the repo's `CLAUDE.md`, the `workloop.integrationBranch` override, or the remote default. Run `git diff <diff-base>...HEAD` to see all changes on this branch.
2. Also resolve `PR title convention` from the same `## Branching` declaration. State it on one line: `PR title convention: <pattern> (<declared | detected | default>)`. Apply it to the title; fall back to a plain sentence with no prefix when nothing is declared or detected, per the `branching-model` skill's fallback.
3. Write the title and description for a reader who has the codebase, the ticket, and the running app, and nothing else. Every term names one of those: code (files, functions, tools), the ticket and its ID, or behavior a user observes. Workloop artifacts never appear by name, label, or ID: stories, story tiers, slices, acceptance-criterion labels, hardening stories, plans, rulings, and ADRs that exist only in plan.md. A decision recorded in one of them appears as the decision itself ("renders the table as server-side markdown"). Follow-up work appears as what it will do, plus its ticket ID when the ticket tracker has issued one.
4. Write a description following this format:

## What
One sentence explaining what this PR does.

## Why
Brief context on why this change is needed

## Changes
- Bullet points of specific changes made
- Group related changes together
- Mention any files deleted or renamed
