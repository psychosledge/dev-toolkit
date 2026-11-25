# Executable Contract per component
Tier: core

## Summary

When this story is done, a team can turn on an executable Contract that states what each component must do, is written before the code, and comes first in every review.

## Background

The Contract was meant to be the team's complete, executable description of what the software must do. Coding agents would treat it as guardrails, and it would hold enough to rebuild a component from scratch. What shipped is a partial list in one shared file, written after the code, pointing at tests stored elsewhere. It has drifted from that purpose. With several developers working in parallel, nearly every pull request also conflicts on that file.

## What needs to happen

- Add a new Contract setting for teams that adopt it together. The current setting keeps today's behavior for repos already using it.
- Each component gets its own contract, stored next to its code and written as tests whose names state what the component must do. Requirements that can't be tested yet are recorded as pending.
- Planning names which components' contracts a slice changes. Design states those changes as plain sentences. Implementation writes the contract tests first.
- Agents may rewrite ordinary tests during a refactor. Weakening a contract test needs the developer's agreement.
- Code review covers contract changes first. It flags any change in behavior that has no matching contract change.
- Today's list format moves to a separate reference. Repos already using it keep working from that reference until the format is retired.

## Notes

- Source: https://impatientprogramming.org/xp-revisited/#the-metaphor-finally-has-a-home
- The new mode is declared with `Enabled: executable`. `Enabled: yes` sends agents to `coding-agent/skills/contract/ledger.md`, which holds today's skill text and each agent's current Contract instructions word for word, grouped by role. Each agent gets one line pointing ledger repos there.
- The new mode drops IDs, the Status and `Enforced by` columns, the guard test and the coverage formula.
- Pending forms: `it.todo`, or pytest skip with a reason.
- Scope covers everything needed to rebuild a component, functional and non-functional. The planner's "contract candidate" filter goes away.
- Enabling the Contract is a team agreement recorded in the repo's `CLAUDE.md`. The skill's solo opt-in wording goes away.
- Files: `skills/contract/SKILL.md`, `agents/planner.md`, `agents/architect.md` (Contract section and template row), `agents/coder.md` (step 4 and bug-fix order), `agents/verifier.md` (section 8, report section, and the shared-IDs line from de0a7b2), `commands/code-review.md`, `skills/systematic-debugging/SKILL.md`.
- An active client project is on `Enabled: yes`, so the ledger mode gets its own verification run.
- Depends on Testing safeguards on every repo.

## Acceptance criteria

- A team planning a change with the new Contract turned on sees, before any code, which components' contracts change and the new requirements as plain sentences.
- After implementation, each new requirement is a test stored next to its component's code, named after the requirement. A requirement that can't be tested yet shows as pending.
- Two developers adding requirements to different components on parallel branches can merge without conflicts in the contract.
- When an agent's refactor would weaken or remove a contract test, the agent stops and asks the developer first.
- A code review on such a repo starts with the contract changes. It flags any behavior change that has no matching contract change.
- A repo using the current Contract setting behaves exactly as it does today, with no edits to that repo.
- A repo that hasn't turned the Contract on sees no Contract questions or steps.
