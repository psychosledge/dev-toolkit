# Reference Material

Third-party repos vendored for study. Nothing here is synced to `~/.claude/` or executed; `/sync-global` discovery covers `coding-agent/` only.

## superpowers/

Jesse Vincent's cross-harness development methodology plugin.

- Source: https://github.com/obra/superpowers
- Snapshot: commit `22f0b463e7a5e579904dd6211a520321035526f7` (2026-11-03), `.git` removed
- License: MIT (LICENSE file in the snapshot)
- Analyzed 2026-11-04 against the coding-agent workloop. Ideas adopted from it: `systematic-debugging` skill, coder evidence rules, `skill-testing` skill, the `/plan` builder check, planner self-review with Review Focus.
- Richest files for later exploration:
  - `skills/writing-skills/` (skill TDD; `references/bulletproofing.md`, `references/testing-skills-with-subagents.md`, `references/persuasion-principles.md`)
  - `skills/subagent-driven-development/` and `skills/executing-plans/SKILL.md` (autonomous execution: ruling ledger, named stops, fix-loop caps, final whole-branch review)
  - `skills/brainstorming/SKILL.md` (Socratic requirements drawing-out, builder check, design-doc gate)
  - `skills/systematic-debugging/` supporting files (`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`)
  - `tests/systematic-debugging/pressure-scenarios/` (worked examples of pressure-scenario tests)

To refresh: clone the source repo, replace this directory with the new tree minus `.git`, and update the snapshot commit and date here.
