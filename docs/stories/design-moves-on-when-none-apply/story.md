# Design moves on when no unwritten requirements apply
Tier: core

## Summary

When this story is done, a developer who says a change touches no unwritten requirements, or skips the question, sees the design continue with an empty required-tests list and isn't asked again.

## Background

Design now asks every developer which unwritten requirements a change touches. Many changes touch none. An empty answer or a skipped question should be a normal outcome, and the design shouldn't stall, invent requirements, or keep asking.

## What needs to happen

- Design treats "none" and a skipped question as complete answers.
- The design shows an empty required-tests list in that case.
- The question is asked once per design.

## Notes

- Depends on Testing safeguards on every repo, Slice 3 (architect's unwritten-requirements question and the ADR's Required tests section).
- Covers the /slice and /auto-slice design-approval gates.
- Behavior-shaping, so skill-testing applies.

## Acceptance criteria

- A developer who confirms none of the suggested requirements sees a design with an empty required-tests list.
- A developer who skips the question sees the same result.
- In either case, the question isn't asked again in the same design.
- A design whose developer confirmed nothing still proceeds to implementation.
