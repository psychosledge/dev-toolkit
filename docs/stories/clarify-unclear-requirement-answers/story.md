# Unclear requirement answers get one clarifying question
Tier: core

## Summary

When this story is done, a developer whose answer to the unwritten-requirements question leaves it unclear which suggested requirements apply is asked once to clarify before the design moves on.

## Background

Design asks the developer which suggested unwritten requirements a change touches. A clear yes, no, or "none" settles the list. A partial or hedged reply, such as "approved, the first one maybe", leaves it open which requirements stay. The design then has to guess, and a guess can drop a requirement the developer meant to keep or keep one they meant to drop.

## What needs to happen

- Design recognizes when an answer leaves a suggested requirement's status unclear.
- It asks one clarifying question naming the unclear requirements, then settles the list.

## Notes

- Follows design-moves-on-when-none-apply, which defines the "none" and skipped-question outcomes.
- Covers the /slice and /auto-slice design-approval gates. Under /auto-slice only the human answers, so the clarifying question is part of the human design gate.
- Behavior-shaping, so skill-testing applies.

## Acceptance criteria

- A developer whose answer leaves a suggested requirement unclear is asked once which of the unclear ones apply.
- After the developer clarifies, the design moves on without asking again.
- A clear answer, including "none", gets no clarifying question.
