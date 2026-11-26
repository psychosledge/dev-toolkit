# Harden the testing safeguards
Tier: core

## Summary

When this story is done, the unwritten-requirements question and the redundant-test check behave sensibly at their edges: no tests, no answers, failing tooling, and required tests that never got written.

## Background

Testing safeguards on every repo made both safeguards run on every repo. Its plan deferred the edge cases below to this follow-up.

## What needs to happen

- When the developer confirms no unwritten requirements, or skips the question, design continues with an empty required-tests list and doesn't ask again.
- Review notices when a required test named in the design was never written.
- When configured mutation tooling fails, times out, or is too slow, the check falls back to the manual check and says which one ran.

## Acceptance criteria

- A design where the developer confirms nothing shows an empty required-tests list, and the question isn't repeated in the same design.
- A required test from the design that's missing at review is reported as a finding.
- A mutation-tool failure is reported, and the manual check's result appears in its place.
