---
name: pr-platform
description: How to resolve which PR platform a repo uses (GitHub, Azure DevOps, GitLab) and whether gh is available. Use before any PR operation such as listing, checking out, commenting on, or creating a PR.
---

# PR Platform

Which PR platform a repo uses is a stable, repo-level fact. Resolve it once as described here instead of re-deriving it from the remote URL on every run.

## Declaration

Check the repo's own `CLAUDE.md` for a `## PR Platform` section:

```
## PR Platform
- Platform: GitHub | Azure DevOps | GitLab | other/manual | none
```

`none` means the repo has no PRs. How it ships is the `Release` field in `## Branching` (see the `branching-model` skill).

Treat a present declaration as authoritative and skip the detection below.

## When undeclared

Detect once: `git remote get-url origin` (or `git remote -v`) and match the host. On a `github.com` match, also check `which gh` for CLI availability — a separate, machine-local fact that doesn't get recorded, since it can change independently of the repo (a new machine, a reinstall). Ask whether to record `## PR Platform\n- Platform: GitHub` in the repo's own `CLAUDE.md`, the same way branching declarations get recorded. For any other host, or no PR-capable remote at all, note the platform found and ask before recording it the same way. `gh`-specific commands throughout this workflow apply only when Platform is GitHub.

