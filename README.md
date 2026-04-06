# dev-toolkit

A private, personal toolkit of reusable development utilities I can copy into any project and tweak as needed.

This repo is intentionally **generic**: it includes everyday dev conveniences (dotfiles, templates, docs) plus a dedicated subtree for **Claude Code / coding-agent** assets.

---

## Repository layout

### `coding-agent/` (Claude Code / coding-agent assets)
This folder is designed to be **copyable** into other repos (all or in part) to power Claude Code workflows.

- `coding-agent/skills/`
  Re-usable skills. Each skill lives in its own folder and contains a `SKILL.md`.

- `coding-agent/agents/`
  Agent definitions / prompt packs / reusable role instructions.

- `coding-agent/commands/`
  Scripts and utilities that support coding-agent workflows.

### Non-agentic utilities
- `dotfiles/` — personal config fragments (`gitconfig`, `zshrc`, etc.)
- `templates/` — PR/issue/ADR templates, starter docs
- `docs/` — notes, conventions, checklists

---

## How I use this repo

### Default workflow: copy + customize per project
1. Find what I need in this repo.
2. Copy it into the target project.
3. Rename / tweak it to match the project conventions.
4. Commit it with the project so the project stays self-contained.

This repo is the source of starters—not a dependency that projects must link to.

---

## License
Private / personal use.
