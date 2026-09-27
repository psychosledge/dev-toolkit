---
name: branching-model
description: How to resolve a repo's branching model, diff base, release pipeline, and branch naming from its own CLAUDE.md, with fallbacks and when to ask. Use before diffing, reviewing, or creating a branch, whenever the base branch matters.
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
```

Any field may be absent — partial declarations are the normal case, not an error state. Treat present fields as authoritative and don't re-derive them. Treat absent fields as genuinely unknown; use the fallback and detection rules below rather than assuming a default silently.

## Resolving the diff base (the branch to merge-base against)

1. `Model: trunk-based` with `Trunk` declared → use it.
2. `Model: release-branching` with `Integration branch` declared → use it as the primary candidate. If `Release pipeline` is also declared, also compute merge-base distance against every branch in the pipeline and use whichever is the **nearest ancestor** to HEAD — not reflexively the integration branch. This is what makes a hotfix cut from a release branch resolve correctly, instead of diffing against everything the whole pipeline is behind by.
3. Nothing declared → `git config workloop.integrationBranch` (local override, unversioned) → the remote default branch (`git symbolic-ref refs/remotes/origin/HEAD`, stripped of the `refs/remotes/origin/` prefix).

## Resolving release/deploy branches (to classify, not diff against)

Read `Release pipeline` if declared, in order. Trunk-based repos have none by definition — don't go looking for one.

## HEAD on a pipeline branch itself

Before running a normal feature review, check whether the current branch **is** one of the declared branches (trunk, integration branch, or any pipeline branch) rather than a feature branch cut from one. If so, this is likely a promotion or release audit, not a feature diff — say so and ask how to proceed instead of walking a large, multi-PR diff as if it were one slice.

## When the declaration is missing or incomplete

Don't silently guess, and don't run a cold questionnaire. Ask only when a concrete signal makes the gap relevant right now — e.g. an unmerged sibling branch alongside the assumed default (`origin/dev` sitting unmerged next to `origin/main`), or a consistent shape across recently-created branches suggesting an undeclared naming convention.

For naming convention specifically: sample branches from the **last 30 days**, and weight branches authored by others more heavily than branches authored by the current git user (`git config user.email`) — self-authored branches may just reflect a skill's own past default rather than real team convention. Surface exactly what was observed plus a recommendation, and let the human make the call — e.g. *"4 of 5 other-authored branches in the last 30 days follow `<TICKET>/<slug>`; recommend canonizing that — record it?"* Never auto-apply a detected pattern.

On confirmation, write directly into **that repo's own `CLAUDE.md`** under `## Branching` — create the section if absent, fill in only the field just resolved if the rest is still unknown, and record an explicit opt-out (e.g. `Feature branch naming: no consistent convention`) when the human says there isn't one, so the question doesn't resurface every session. This is a team-level fact, not a personal one — it belongs in the versioned file that travels with every clone, never in personal memory and never left as a one-off local git-config fix alone.

## Fallback branch naming

When no naming convention is declared or detected, propose a bare `<slug>` — no `feature/` prefix, no ticket embedded — even when a ticket ID is on hand. Only add structure once it's actually known to be this repo's convention.

