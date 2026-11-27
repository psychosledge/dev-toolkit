---
name: kill-matrix
description: Checks that each new or changed test catches a mutation no other test catches, using the repo's mutation-testing tooling or a manual kill check, and defines how a test that kills nothing unique is reported. Read by the coder before handoff and by the verifier on every review, on every repo.
---

# Kill-Matrix

Every new or changed test should prove it catches something no other test catches.

**When the repo already has mutation-testing tooling configured** (a Stryker config, a `mutmut` config, a PIT/pitest plugin entry, `cargo-mutants`, or the equivalent for the stack): run it scoped to the new or changed tests. A test that kills zero unique mutants is a removal candidate, not an automatic deletion, so flag it for the human.

**When no such tooling exists**, the common case on a repo you don't control the toolchain for: do a manual kill check instead. For each new test, name the specific mutation it's supposed to catch (a flipped comparison, a dropped branch, an off-by-one), and confirm by inspection that the test would actually fail under that exact mutation. This is an approximation, not a replacement for real mutation testing, so say so when reporting it.

When applying mutations by hand, make sure each mutant is what actually runs: clear build or bytecode caches between mutations (for Python, delete `__pycache__` or set `PYTHONPYCACHEPREFIX` to a temporary directory), and confirm the original code passes again after restoring it.

## Reporting the outcome

A test that kills no unique mutant is a removal candidate. Report it in the report's Kill-Matrix section (the verifier's `## Kill-Matrix`, the coder's `### Kill Check`), one line per test, naming the mutation or mutations checked:

```
- <test identifier> — <mutation checked> — no unique kill
```

That line is the whole report of a removal candidate. The finding is advisory: it goes in the Kill-Matrix section only, and stays out of Issues, Refactoring Suggestions, the quality rating, and the approval status. The test stays in the code until the human calls it out for removal.

Every observation that a test duplicates, overlaps, or adds no coverage beyond another test is this same finding, whatever severity it seems to deserve. It is reported once, as the Kill-Matrix line. A mutation table or reasoning may sit above the line in the Kill-Matrix section.

| Rationalization | Reality |
|---|---|
| "It's only a low Issue that points to the Kill-Matrix entry." | A pointer is a second listing of the same finding. |
| "The weak assertion is a test-quality problem, separate from the kill result." | No unique kill is the measure of that problem. One line covers it. |
| "Readers skim Issues, so it should show up there too." | Kill-Matrix is a fixed section of every report. The human reads it there. |

The check runs on its own evidence. A test the coder flagged and the human kept is flagged again in a review's first verifier pass when it still kills nothing unique. On a clean pass, the verifier's Clean Pass rules set the scope.

## No new tests

When the diff adds or changes no tests, or the repo has no test suite, the Kill-Matrix section says the check found no new tests and lists no removal candidates. Name no mutations for tests that don't exist.
