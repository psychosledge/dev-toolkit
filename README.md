# dev-toolkit

A personal dev toolkit for arriving at a new machine or working across projects — one repo to pull down and have environment config, conventions, and the Claude Code workloop ready.

---

## Purpose

This repo collects things that are useful *regardless of which project you're working on*:

- **dotfiles/** — personal shell and tool config fragments to drop in place
- **coding-agent/** — source of truth for global Claude Code agent, command, and skill files

`templates/` (PR/issue/ADR templates) and `docs/` (broadly-applicable notes and checklists) are planned additions, not yet started. `coding-agent/` is the most mature piece here.

---

## install.sh

Entry point for Coder's dotfiles bootstrapping: point a workspace's Dotfiles URL at this repo (SSH, via a read-only deploy key) and Coder clones it and runs `install.sh` automatically. It copies `coding-agent/{CLAUDE.md,agents,commands,skills}` into `~/.claude/` and `dotfiles/{zshrc,zprofile,gitconfig}` into `$HOME`, so a fresh Linux workspace gets the same Claude Code workloop and shell config as this machine.

---

## coding-agent/

This directory mirrors `~/.claude/` and is its **source of truth**. Claude Code loads agent and command files from `~/.claude/` at runtime — `coding-agent/` is where those files are authored, versioned, and reviewed before going live.

### Directory mapping

| This repo | Global (`~/.claude/`) | Purpose |
|---|---|---|
| `coding-agent/CLAUDE.md` | `CLAUDE.md` | Global instructions applied in every Claude Code session |
| `coding-agent/agents/` | `agents/` | Subagent definitions |
| `coding-agent/commands/` | `commands/` | Slash commands |
| `coding-agent/skills/` | `skills/` | Skills invoked by name or auto-triggered by their description |

> **`coding-agent/CLAUDE.md` is a sync payload**, not project-level context for this repo. Its contents are destined for `~/.claude/CLAUDE.md`. The repo-level `CLAUDE.md` at the root of this repo is the project context for working in dev-toolkit itself.

### Keeping in sync

Use `/sync-global` to detect and reconcile drift between `coding-agent/` and `~/.claude/`. It diffs every file pair, runs a workloop impact analysis, and requires explicit approval before writing anything. Drift runs both ways: edit `coding-agent/` first for changes conceived here, or edit `~/.claude/` directly while working reactively in another project and reconcile back with `/sync-global` later.

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
| `/system-audit` | Audit a repo (or set of repos) for what blocks production, manual invoke only |
| `/sync-global` | Detect and reconcile drift between `coding-agent/` and `~/.claude/` |

### Skills

| Skill | What it's for |
|---|---|
| `branching-model` | Resolve a repo's base branch, PR platform, and branch naming before diffing or creating a branch |
| `pr-platform` | Resolve which PR platform a repo uses and whether `gh` is available |
| `pr-description` | Write pull request titles and descriptions |
| `comment-quality` | The bar a code comment must clear, for writing and reviewing |
| `tracking` | Tracker README layout and workloop checkpoints for sprint/release cadences; read and written by most of the above commands |
| `activity-log` | Shared activity-log format and categorization, used by other skills |
| `sprint-rollover` | Archive the current sprint/week and scaffold the next one |
| `sprint-recap` | Build a sprint or weekly status recap for client and leadership |
| `demo-prep` | Plan what to show and talk about at an upcoming demo |
| `meeting-notes` | Capture a meeting's purpose, decisions, and feedback live |
| `whats-next` | Check the tracker's priority list and active items for "what's next" |
| `system-audit-reference` | Reference used by `/system-audit` (tiers, rubrics, register template) |

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

## Session & tracking docs

A handful of skills (`tracking`, `activity-log`, `sprint-recap`, `sprint-rollover`, `demo-prep`,
`meeting-notes`, `whats-next`) maintain a lightweight tracker alongside the code. This only
activates once a `tracking-config` project memory exists for a project; an untracked project is
unaffected.

### Starting a session

Say "what's next," or invoke the `whats-next` skill directly, at the start of a work session. It
first checks for any meeting earlier today that wasn't logged yet, then reads the live unit's
tracker to say what to work on.

### Shape, by cadence

A tracked project has one **live unit** at a time under `<tracking root>/`, plus an `archive/` of
finished ones:

- **Sprint cadence** — a time-boxed unit. Ends on a date; `sprint-rollover` archives it and
  scaffolds the next one.
- **Release cadence** — a unit ships everything in it together, ending at release close-out
  rather than a date. Zero live units between releases is normal.

A live unit directory holds:

```
<tracking root>/<unit>/
  README.md        # the working tracker: priority order, active/closed items
  recaps/          # recap docs, once any have been written
  log/<date>.md    # activity log, one file per day, only when enabled
  ...              # meeting notes and topic docs
```

### Keeping tracker docs out of a shared repo

`tracking-config` is a project memory, not a file in the repo, so the tracking root doesn't have
to live inside the project's own git repo. On a client or otherwise shared repo, point it at a
sibling directory in the same workspace instead — outside the repo, inside the same Coder/VS
Code workspace — so the tracker, recaps, and activity log stay private and never enter shared
history.

---

## License

Private / personal use.
