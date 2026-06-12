# dev-toolkit

A personal dev toolkit for arriving at a new machine or working across projects — one repo to pull down and have environment config, conventions, and the Claude Code workloop ready.

---

## Purpose

This repo collects things that are useful *regardless of which project you're working on*:

- **dotfiles/** — personal shell and tool config fragments to drop in place
- **templates/** — PR/issue/ADR templates and starter docs to copy into projects
- **docs/** — notes, conventions, checklists that apply broadly
- **coding-agent/** — source of truth for global Claude Code agent and command files

These directories are at different stages of development. `coding-agent/` is the most mature; the others exist to grow into.

---

## coding-agent/

This directory mirrors `~/.claude/` and is its **source of truth**. Claude Code loads agent and command files from `~/.claude/` at runtime — `coding-agent/` is where those files are authored, versioned, and reviewed before going live.

### Directory mapping

| This repo | Global (`~/.claude/`) | Purpose |
|---|---|---|
| `coding-agent/CLAUDE.md` | `CLAUDE.md` | Global instructions applied in every Claude Code session |
| `coding-agent/agents/` | `agents/` | Subagent definitions |
| `coding-agent/commands/` | `commands/` | Slash commands |

> **`coding-agent/CLAUDE.md` is a sync payload**, not project-level context for this repo. Its contents are destined for `~/.claude/CLAUDE.md`. The repo-level `CLAUDE.md` at the root of this repo is the project context for working in dev-toolkit itself.

### Keeping in sync

Use `/sync-agents` to detect and reconcile drift between `coding-agent/` and `~/.claude/`. It diffs every file pair, runs a workloop impact analysis, and requires explicit approval before writing anything. Always edit `coding-agent/` first — never edit `~/.claude/` directly when the intent is a lasting change.

### Agents

| Agent | Role |
|---|---|
| `planner` | Decomposes user stories into thin vertical slices with AC and a UAT checklist |
| `architect` | Makes structural decisions and produces ADRs when a slice requires it |
| `coder` | Implements slices using TDD (Red-Green-Refactor) |
| `verifier` | Verifies AC, reviews code quality, surfaces findings for human review |

### Commands

| Command | What it does |
|---|---|
| `/story` | Author a story card collaboratively; no planning begins until human approves |
| `/plan` | Decompose an approved story into slices with AC and UAT checklist |
| `/slice` | Run one slice: architect? → coder → code-review → commit |
| `/code-review` | Walk through changes, run the verifier, handle fixes, and commit |
| `/brainstorm` | Exploratory design session with the architect |
| `/catchup` | Show unpulled commits, new remote branches, and team activity |
| `/sync-agents` | Detect and reconcile drift between `coding-agent/` and `~/.claude/` |

### Workloop

```
/story [idea]
  → draft collaboratively → human approves story card

/plan
  → planner decomposes into slices + UAT checklist → human approves plan

for each slice:
  /slice [slice N]
    → architect (if needed) → human approves design
    → coder implements (TDD)
    → /code-review: verifier + walk-through + fixes → human approves → commit

on final slice:
  → UAT checklist → PR
```

---

## License

Private / personal use.
