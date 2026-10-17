---
name: branching-model
description: How to resolve a repo's branching model, diff base, release pipeline, branch naming, PR title convention, and how finished work ships (PR or a repo-local release skill) from its own CLAUDE.md, with fallbacks and when to ask. Use before diffing, reviewing, or creating a branch, whenever the base branch matters.
---

# Branching Model

Every repo has a branching model: how work integrates and how releases flow. Resolve it as described here instead of assuming `main`.

## Declaration

Check the *repo's own* `CLAUDE.md` (not the global one) for a `## Branching` section:

```
## Branching
- Model: trunk-based | release-branching
- Trunk: <branch>                              (trunk-based only)
- Integration branch: <branch>                 (release-branching only)
- Release pipeline: <branch> → <branch> → ...  (release-branching only, optional)
- Feature branches: yes | short-lived | no
- Feature branch naming: <pattern>, e.g. `<TICKET>/<slug>` — or "no consistent convention"
- PR title convention: <pattern>, e.g. `<type>: <summary>` (feat, fix, chore, ...) — or "no consistent convention"
- Release: pull request | skill <name>
- Pre-PR CI: in place | clean checkout
```

Any field may be absent — partial declarations are the normal case, not an error state. Treat present fields as authoritative and don't re-derive them. Treat absent fields as genuinely unknown; use the fallback and detection rules below rather than assuming a default silently.

## Resolving the diff base (the branch to merge-base against)

1. `Model: trunk-based` with `Trunk` declared → use it.
2. `Model: release-branching` with `Integration branch` declared → use it as the primary candidate. If `Release pipeline` is also declared, also compute merge-base distance against every branch in the pipeline and use whichever is the **nearest ancestor** to HEAD — not reflexively the integration branch. This is what makes a hotfix cut from a release branch resolve correctly, instead of diffing against everything the whole pipeline is behind by.
3. Nothing declared → `git config workloop.integrationBranch` (local override, unversioned) → the remote default branch (`git symbolic-ref refs/remotes/origin/HEAD`, stripped of the `refs/remotes/origin/` prefix).

## Resolving release/deploy branches (to classify, not diff against)

Read `Release pipeline` if declared, in order. Trunk-based repos have none by definition — don't go looking for one.

## Resolving how finished work ships

`Release` names the step that ships a finished story:

- `pull request`: the story ships as a PR, resolved through the `pr-platform` skill. This is the default when the field is absent and the repo has a PR-capable remote.
- `skill <name>`: a repo-local skill (for example `ship`) owns the release mechanics, such as tagging, publishing, and pushing. The workloop hands off to it and records the ref it released.

When undeclared, look for a repo-local skill named `ship` or `release` (`.claude/skills/` or `.claude/commands/` in the repo). If one exists, or the repo has no PR-capable remote, ask which applies and record the answer under `## Branching` as described below.

## Resolving where pre-PR CI runs

`Pre-PR CI` sets where `/slice` runs the repo's CI checks before proposing a PR:

- `in place`: the current checkout. This is the default when the field is absent.
- `clean checkout`: a throwaway git worktree of the branch, so tests that depend on uncommitted local files such as `.env` fail locally the same way they would in CI. Use it where a red CI check on a PR is costly, such as a client repo.

## HEAD on a pipeline branch itself

Before running a normal feature review, check whether the current branch **is** one of the declared branches (trunk, integration branch, or any pipeline branch) rather than a feature branch cut from one. If so, this is likely a promotion or release audit, not a feature diff — say so and ask how to proceed instead of walking a large, multi-PR diff as if it were one slice.

## When the declaration is missing or incomplete

Don't silently guess, and don't run a cold questionnaire. Ask only when a concrete signal makes the gap relevant right now — e.g. an unmerged sibling branch alongside the assumed default (`origin/dev` sitting unmerged next to `origin/main`), or a consistent shape across recently-created branches suggesting an undeclared naming convention.

For naming convention specifically: sample branches from the **last 30 days**, and weight branches authored by others more heavily than branches authored by the current git user (`git config user.email`) — self-authored branches may just reflect a skill's own past default rather than real team convention. Surface exactly what was observed plus a recommendation, and let the human make the call — e.g. *"4 of 5 other-authored branches in the last 30 days follow `<TICKET>/<slug>`; recommend canonizing that — record it?"* Never auto-apply a detected pattern.

The same applies to PR title convention, sampled from merged PR titles over the same window instead of branch names (resolve the repo's PR platform via the `pr-platform` skill first, then list recent merged PRs through it) and weighted the same way by author. A human explicitly asking for a prefix scheme going forward (e.g. "prefix PR titles with feat/fix") is itself the concrete signal — record it directly rather than waiting to detect a pattern first.

On confirmation, write directly into **that repo's own `CLAUDE.md`** under `## Branching` — create the section if absent, fill in only the field just resolved if the rest is still unknown, and record an explicit opt-out (e.g. `Feature branch naming: no consistent convention`) when the human says there isn't one, so the question doesn't resurface every session. This is a team-level fact, not a personal one — it belongs in the versioned file that travels with every clone, never in personal memory and never left as a one-off local git-config fix alone.

## Fallback branch naming

When no naming convention is declared or detected, propose a bare `<slug>` — no `feature/` prefix, no ticket embedded — even when a ticket ID is on hand. Only add structure once it's actually known to be this repo's convention.

## Fallback PR title convention

When no PR title convention is declared or detected, propose a plain sentence title with no prefix. Only apply a prefix scheme (e.g. `feat:`/`fix:`) once it's confirmed as this repo's convention.

