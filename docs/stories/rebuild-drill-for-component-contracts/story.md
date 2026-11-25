# Rebuild drill for component contracts
Tier: core

## Summary

When this story is done, a team can check whether a component's contract is complete by having an agent rebuild the component from its contract and seeing what the rebuilt version gets wrong.

## Background

A contract is complete when the component can be rebuilt from it. Running that rebuild on demand turns gaps into new requirements before a production bug exposes them.

## What needs to happen

- A command rebuilds one component in an isolated copy of the repo, using only its contract and design records. It then runs the contract tests and reports the gaps.
- Each gap comes with a proposed new requirement for the developer to accept or reject.
- The drill never changes the developer's real code.

## Notes

- Runs in a scratch worktree.
- New command under `coding-agent/commands/`.
- Depends on Executable Contract per component.

## Acceptance criteria

- A developer runs the drill on a component and gets a list of behaviors the rebuilt version got wrong or missed.
- Each gap comes with a proposed requirement the developer can accept or reject.
- After the drill, the developer's working copy and branch are unchanged.
