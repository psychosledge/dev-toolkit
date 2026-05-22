---
name: slice
description: Execute a planned slice through architect → coder → verifier with human approval gates. Use after /plan has produced an approved plan.
argument-hint: "[slice name and acceptance criteria]"
---

Execute the following slice through the full design → code → verify loop with human approval gates at each checkpoint.

Slice to implement:
$ARGUMENTS

---

Follow this sequence exactly. Do not skip steps or approval gates.

**Step 1 — Architect check**
Does this slice require architectural decisions (new domain concepts, new external integrations, cross-cutting concerns, or anything warranting an ADR)?

- If **yes**: invoke the **architect** subagent. Present the design output to the human and wait for explicit approval before continuing. If changes are requested, revise and re-present.
- If **no**: proceed directly to Step 2.

**Step 2 — Implementation**
Invoke the **coder** subagent to implement the slice using TDD (Red-Green-Refactor). The coder should work within the scope of this slice only.

**Step 3 — Verification**
Invoke the **verifier** subagent to verify the slice against its acceptance criteria and review code quality.

**Step 4 — Comprehension gate**

The verifier has presented the full report including the Explain-Back Prompt. Now run the comprehension gate before accepting commit approval.

Before presenting the explain-back questions, reproduce the full verifier report verbatim to the human. Do not summarize it. The human must see the complete report — AC results, quality rating, all sections — before being asked the explain-back questions.

**Phase 4a — Explain-back exchange**

Present the Explain-Back Prompt questions to the human in a collaborative framing:

> "Before we commit, I want to make sure the decisions in this slice are solid in both our heads. [Question 1]? [Question 2 if present]?"

Wait for the human's response. Then classify the outcome:

**Pass**: The human's answer demonstrates they understand the rationale and tradeoffs. Proceed to Phase 4b.

- Signs of pass: correct identification of why the approach was chosen, awareness of the alternative that was rejected, understanding of the constraint driving the decision.

**Re-explain**: The human says "I'm not sure" or "I don't know", or gives an answer that reveals a gap in understanding (e.g., they describe what the code does but not why it was structured that way). Do not treat this as failure — reframe and try again.

- Reframe by: explaining the decision in different terms, naming the alternative that was considered and why it was rejected, or connecting the decision to a downstream consequence visible in the slice.
- Ask again: "Does that help clarify it? What's your read now?"
- Loop with no time limit until pass or until the human explicitly invokes skip.

**Skip with flag**: The human explicitly says they want to skip the explain-back (e.g., "skip", "I'll trust you", "flag it and move on"). Accept this without friction.

- Update the plan file at `docs/stories/<slug>/plan.md`: in the current slice's section, append a line:
  `> **Comprehension skipped** [YYYY-MM-DD]: [decision topic] — human granted permission to skip`
- Proceed to Phase 4b.

**Phase 4b — Commit approval**

After the explain-back resolves (pass or skip), ask for commit approval normally:

> "All good. Approve to commit, or request any other changes."

If changes are requested, return to Step 2, re-run Step 3, and return to Step 4 (the comprehension gate runs again after any new verification).

**Step 5 — UAT checklist (final slice only)**
If this is the last slice in the plan, after the commit is approved, present the full UAT checklist from the planner and ask the human to confirm all items before the feature is considered complete and ready to ship.
