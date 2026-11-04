---
name: systematic-debugging
description: Root-cause-first debugging process for any bug, failing test, build failure, or unexpected behavior. Use before proposing or writing any fix, especially under time pressure, when a fix seems obvious, or after a previous fix didn't hold.
---

# Systematic Debugging

Find the root cause before attempting any fix. A fix written before the cause is understood treats a symptom, and symptom fixes come back.

## When This Applies

Any technical misbehavior: failing tests, bugs, build failures, integration errors, performance problems. It applies most when skipping it is tempting: an emergency, a fix that seems obvious, or a second attempt after the first fix didn't work. Guess-and-check thrashing is slower than this process, including for simple bugs.

## Phase 1: Investigate

Complete this phase before forming any fix idea.

1. **Read the full error.** Whole message, whole stack trace, line numbers, error codes. The answer is often in text that got skimmed past.
2. **Reproduce reliably.** Exact steps, consistent trigger. If it can't be reproduced, gather more data before theorizing.
3. **Check what changed.** `git diff`, recent commits, new dependencies, config or environment differences.
4. **Instrument boundaries in multi-component failures.** When the path crosses layers (CI to build to signing, API to service to database), log what enters and exits each layer, run once, and read the evidence to find which layer breaks. Then investigate that layer.
5. **Trace bad values to their origin.** Where does the wrong value first appear? Keep walking up the call chain. The fix belongs at the source.

## Phase 2: Compare

- Find similar code in this repo that works. List every difference from the broken code, including differences that look like they can't matter.
- When implementing against a reference or an established pattern, read the reference completely before adapting it.

## Phase 3: Hypothesize and Test

- State one specific hypothesis: "X is the root cause because Y."
- Test it with the smallest possible change. One variable at a time. Never stack multiple candidate fixes in one run.
- Hypothesis confirmed: go to Phase 4. Refuted: form a new one. Don't layer a second fix on top of a failed one.
- If you don't understand something, say so and investigate it. Pretending to understand blocks the next person too.

## Phase 4: Fix

Follow the coder's bug-fix order: a failing test reproducing the bug comes first (Contract-first when the `contract` skill resolves the repo as enabled), then the fix, then the passing run and a check of related behavior.

## The Three-Strikes Breaker

Count your fix attempts. After the third failed fix, stop. Three failures on one bug means the problem is structural: shared state, coupling, or a pattern that fights the change. Signs: each fix surfaces a new problem somewhere else, or each fix needs a "small refactor" that keeps growing.

Do not attempt fix #4. Present the human with what was tried, what each attempt revealed, and the architectural question the failures point at. This is a design conversation, and the architect may need to be involved.

## Red Flags

Each of these thoughts means: stop and return to Phase 1.

| Thought | What's actually true |
|---------|----------------------|
| "Quick fix now, investigate later" | The first fix sets the pattern. Later rarely comes. |
| "Just try changing X and see" | A run without a hypothesis teaches nothing when it fails. |
| "It's probably X" | "Probably" means Phase 1 is unfinished. |
| "No time for process, this is urgent" | Thrashing is the slow path. |
| "Change several things, then run the tests" | A passing run can't say which change mattered; a failing run can't say which change broke it. |
| "One more attempt" (after two failures) | The third failure trips the breaker. Count honestly. |

## When Investigation Finds No Root Cause

If the process genuinely lands on an environmental, timing, or external cause: document what was ruled out, handle it appropriately (retry, timeout, clearer error), and add logging so the next occurrence carries evidence. Most "no root cause" conclusions are an unfinished Phase 1, so check that first.
