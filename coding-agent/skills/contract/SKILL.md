---
name: contract
description: Resolves whether a repo has adopted the Contract, a durable, versioned record of what the software must do, functional and non-functional, each obligation backed by an executable test. Defines its location, schema, coverage metric, and the Contract-first bug fix order. Read by architect, planner, coder, and verifier whenever a slice might introduce or touch a durable system invariant.
---

# Contract

The Contract is a per-repo record of the system's required behavior, functional and non-functional, kept separate from any one story's acceptance criteria because it's meant to outlive the story that introduced it. A caller with a 150ms timeout against a component that happens to average 100ms is exactly the kind of obligation this exists to catch: nothing about the code states it, so a later "improvement" can break it with no test anywhere to catch the regression.

## Declaration

Check the repo's own `CLAUDE.md` for a `## Contract` section:

```
## Contract
- Enabled: yes | no
- Location: <path>   (default: docs/contract.md)
```

Absent entirely, or `Enabled: no`: the Contract doesn't apply to this repo. Skip every step below silently, the same way an unconfigured `tracking-config` means skip tracking steps silently.

This is opt-in by design, including on a repo several people work in. Nothing here assumes the rest of a team is maintaining it. A partially-adopted Contract is still useful, and the coverage metric below exists specifically to report that honestly instead of implying completeness that isn't there.

## What belongs in it

Not every acceptance criterion is Contract material. A criterion describing one-off story behavior ("the button shows a spinner while loading") stays in that story's own plan. A criterion describing a durable invariant the system must keep holding regardless of which story touches it next (a latency budget, an idempotency guarantee, an ordering requirement, a security boundary) belongs in the Contract.

Functional and non-functional obligations both qualify. Non-functional ones are the ones most likely to have no other home, since nothing about a type signature states a latency budget.

## Schema

One row per obligation, in the file at the declared location:

```
| ID | Obligation | Type | Enforced by | Status | Added |
|----|-----------|------|-------------|--------|-------|
| C-001 | Fetching a user profile completes in <150ms at p99 | non-functional | test/profile.perf.test.ts:12 | met | Slice 2, 2026-10-28 |
| C-002 | A duplicate webhook delivery is a no-op, not a second charge | functional | unenforced | not met | Slice 3, 2026-10-28 |
```

- **ID**: sequential, `C-NNN`, never reused once assigned.
- **Obligation**: the required behavior in prose, describing what must be true, not how it's implemented. Same rule as an ADR: no code blocks, no pasted implementation.
- **Type**: `functional` or `non-functional`.
- **Enforced by**: the file:line of the test that actually checks this obligation, or `unenforced` if no such test exists yet.
- **Status**: `met` (enforced and currently passing) or `not met` (enforced but currently failing, or still `unenforced`).
- **Added**: the slice or story that introduced it, and the date.

A superseded obligation gets a `Superseded by C-NNN` note in its own Status cell instead of being deleted. The file is a versioned record, and git history alone isn't a substitute for an in-file trail when an obligation was explicitly replaced rather than just edited.

On first adoption, write this header at the top of the file, before the table:

```
Obligations introduced through this workflow. Not a claim of full system coverage.
```

## Contract coverage

Report it as:

```
Contract coverage: <obligations with Status: met> / <total obligations recorded>
```

This is obligation-level coverage of what's recorded in the file, not a claim about the share of the whole system's behavior. Measuring true system-wide coverage would need static analysis this toolkit has no way to perform. State the number with that scope every time it's reported rather than rounding it up to sound more complete than it is.

## Contract-first bug fix order

When a production bug surfaces in a repo with the Contract enabled, the obligation comes before the test:

1. Add the missing obligation to the Contract, `Enforced by: unenforced`, `Status: not met`.
2. Write the regression test.
3. Confirm the test fails for the right reason before any fix lands.
4. Fix the code.
5. Update the obligation: `Enforced by: <test file:line>`, `Status: met`.

A bug found in code with the Contract enabled means the Contract was missing something, not just that a test was missing.

## Kill-matrix check

Every new or changed test should prove it catches something no other test catches.

**When the repo already has mutation-testing tooling configured** (a Stryker config, a `mutmut` config, a PIT/pitest plugin entry, `cargo-mutants`, or the equivalent for the stack): run it scoped to the new or changed tests. A test that kills zero unique mutants is a removal candidate, not an automatic deletion, so flag it for the human.

**When no such tooling exists**, the common case on a repo you don't control the toolchain for: do a manual kill check instead. For each new test, name the specific mutation it's supposed to catch (a flipped comparison, a dropped branch, an off-by-one), and confirm by inspection that the test would actually fail under that exact mutation. This is an approximation, not a replacement for real mutation testing, so say so when reporting it.

When applying mutations by hand, make sure each mutant is what actually runs: clear build or bytecode caches between mutations (for Python, delete `__pycache__` or set `PYTHONPYCACHEPREFIX` to a temporary directory), and confirm the original code passes again after restoring it.
