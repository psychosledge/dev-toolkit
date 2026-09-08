# dev-toolkit — Project Context

This repo is a personal dev toolkit, not an application project. There is no build system, test suite, or deployable artifact at the repo root. Work here is primarily authoring and maintaining text files.

## The two CLAUDE.md files

`coding-agent/CLAUDE.md` is a **sync payload** — its contents are destined for `~/.claude/CLAUDE.md` to become global Claude instructions applied in every session on this machine. It is not project context for this repo.

This file (`CLAUDE.md` at the repo root) is the project context for working in dev-toolkit itself.

Never treat these as the same file or apply one in place of the other.

## Working in this repo

- Edit agent and command files in `coding-agent/` first. Run `/sync-global` after to push changes live to `~/.claude/`.
- Never edit `~/.claude/` files directly when making a lasting change — the repo copy will overwrite them on the next sync.
- After any set of changes to `coding-agent/`, commit to the repo and then sync. The repo is the record; `~/.claude/` is the runtime.
