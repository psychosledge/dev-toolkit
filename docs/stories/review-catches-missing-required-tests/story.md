# Review catches missing required tests
Tier: core

## Summary

When this story is done, a developer whose design named a required test that was never written sees that gap reported at review.

## Background

Design now turns each confirmed unwritten requirement into a required test. Nothing checks later that those tests got written, so a requirement the developer confirmed can ship with no test enforcing it.

## What needs to happen

- Review compares the required tests named in the design against the tests in the change.
- Each missing one is reported as a finding.

## Notes

- Depends on Testing safeguards on every repo, Slice 3 (the ADR's Required tests section).
- Verifier reads the slice's ADR; slices without an architect have no Required tests section.
- Invariants the design itself introduces get no Required tests entry. On a repo without the Contract, nothing in the ADR names a test for them.
- Open question: whether a missing required test blocks approval or is advisory like the kill-matrix result.
- Behavior-shaping, so skill-testing applies.

## Acceptance criteria

- A required test from the design that's missing at review is reported as a finding naming the requirement it was meant to enforce.
- When every required test is present, review reports no such finding.
- A change whose design listed no required tests gets no such finding.
