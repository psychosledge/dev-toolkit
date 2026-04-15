# coding-agent/

A generalized agentic coding team built around a **plan → code → verify** workloop with thin vertical slices and explicit human approval gates.

## Agents

| Agent | Role |
|---|---|
| `planner` | Decomposes user stories into thin vertical slices and produces a UAT checklist |
| `architect` | Makes structural decisions and produces ADRs when a slice requires it |
| `coder` | Implements slices using TDD (Red-Green-Refactor) |
| `verifier` | Verifies AC, reviews code quality, and gates the pre-commit approval |

## Commands

| Command | What it does |
|---|---|
| `/story` | Invokes planner to decompose a user story; pauses for human approval of the slice plan |
| `/slice` | Runs one slice through the full loop (architect? → coder → verifier) with human gates |
| `/verify` | Standalone verifier invocation against all branch changes since main |

## Workloop

```
/story [user story]
  → planner decomposes into slices + UAT checklist
  → human approves plan

for each slice:
  /slice [slice description]
    → architect (if needed) → human approves design
    → coder implements (TDD)
    → verifier checks AC + code quality → human approves commit

on final slice:
  → human works through UAT checklist → feature complete
```

## Installation

### Global (available in every repo on your machine)
```
cp coding-agent/agents/* ~/.claude/agents/
cp coding-agent/commands/* ~/.claude/commands/
```

### Project-scoped
```
cp -r coding-agent/agents .claude/agents
cp -r coding-agent/commands .claude/commands
```

Project-level agents override global ones by name, so you can customize a single agent for a specific repo without affecting others.

## Project-specific context

All agents read `CLAUDE.md` at the project root for project-specific context (tech stack, architecture patterns, conventions, domain language, testing approach). Run `/init` in a project to generate a `CLAUDE.md` from the existing codebase, then add any context that isn’t derivable from the code (architectural decisions, domain glossary, etc.).
