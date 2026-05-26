# Claude Code — Global Instructions

## Improve the Agents, Don't Work Around Them

When working in a project that uses the coding-agent workloop (`/story`, `/slice`, `/bug`, `/verify`, `/sync-agents`), you will sometimes notice that an agent behaves unexpectedly, skips a step, produces incomplete output, or creates friction in the flow.

**When this happens — surface it, don't patch it:**

- Tell the human immediately: which agent or command file has the gap, what the observed behavior was, and what a concrete fix would look like.
- Do **not** write a project memory that describes the workaround (e.g., "the verifier doesn't surface blockers to the human, so remember to check manually").
- Do **not** add one-off inline instructions to future prompts to compensate.
- Do **not** silently adjust your own behavior to cover for an agent's deficiency.

The agent files in `coding-agent/` (synced to `~/.claude/`) are the source of truth for workloop behavior. A memory that describes agent behavior or workflow process is almost always a signal that an agent file needs improving — not that you should remember to compensate.

**The test:** Before writing any memory or inline instruction about the workloop, ask yourself: *Is this describing a gap in an agent file?* If yes, flag it to the human instead.

## Never Push Without Explicit Permission

Do not run `git push` (or any variant: `--force`, `-u`, etc.) unless the human has explicitly asked for it in the current message.

The workloop commits incrementally as slices complete. The human's own code review happens after all slices are committed — pushing before that review ships unverified work. A commit is local and safe; a push is public and irreversible.

This applies even if a previous message approved a push, or if a PR workflow seems to imply it. Each push requires fresh, explicit approval.
