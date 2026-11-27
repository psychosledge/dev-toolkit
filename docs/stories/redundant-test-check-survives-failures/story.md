# Redundant-test check survives tooling failures
Tier: core

## Summary

When this story is done, a developer whose repo's mutation-testing tool fails, times out, or runs too long still gets a redundant-test result, and is told the tool failed and the manual check ran instead.

## Background

The check that each new test catches something unique uses a repo's mutation-testing tool when one is set up. When that tool breaks or can't finish, the check currently has no defined behavior, so the developer may get no result or a misleading one.

## What needs to happen

- When the tool fails, times out, or is too slow, the check falls back to the manual check.
- The report says the tool failed, why, and that the manual check ran in its place.

## Notes

- Kill-matrix rules live in coding-agent/skills/kill-matrix/SKILL.md, read by the verifier now and by the coder after Testing safeguards on every repo, Slice 2.
- Open question: what counts as too slow (a fixed time budget, or the agent's judgment).
- Behavior-shaping, so skill-testing applies.

## Acceptance criteria

- A developer whose mutation-testing tool fails sees the failure reported, with the manual check's result in its place.
- The same holds when the tool times out or is too slow to finish.
- The report always says which check ran: the tool or the manual check.
