# Testing safeguards on every repo
Tier: core

## Summary

When this story is done, a developer on any repo is asked about unwritten requirements during design and is told when a new test catches nothing the existing tests don't, whether or not the repo uses a Contract.

## Background

Two of the toolkit's safeguards only run on repos that have turned on the Contract. One asks which unwritten requirements a design depends on, such as a response-time budget a caller relies on, and requires a test for each. The other checks that every new test catches a mistake no other test catches. Both catch real problems on any codebase. Tying them to the Contract leaves most repos without them. It also means the Contract redesign would have to carry them along.

## What needs to happen

- On every repo, design asks which unwritten requirements a change touches and lists each confirmed one as a required test.
- On every repo, the check that each new test catches something new runs before a change is handed off and again during review.
- The Contract no longer owns either safeguard.

## Notes

- The architect's Contract section only proposes rows when the Contract is enabled. The verifier's section 9 (Kill-Matrix Check) and its report line are limited to Contract repos.
- The kill-matrix rules currently live in the contract skill and need their own home: their own skill, or the coder and verifier.
- Regression-test-first is already unconditional in systematic-debugging and the coder.
- Behavior-shaping, so `skill-testing` applies.
- Ships before Executable Contract per component, which depends on it.

## Acceptance criteria

- A developer designing a change on a repo without a Contract is asked which unwritten requirements it touches. Each one they confirm appears in the design as a required test.
- A developer whose change adds a test that catches nothing the existing tests catch sees that test flagged as a removal candidate, on a repo without a Contract.
- A flagged test is only removed when the developer agrees.
- On a repo with the Contract turned on, each safeguard runs once, with no repeated questions or duplicate flags.
