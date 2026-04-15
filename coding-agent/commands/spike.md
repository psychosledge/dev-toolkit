---
name: spike
description: Time-boxed research spike to answer a focused question before planning. Produces a findings report and recommendation. Use before /story when requirements are unclear.
argument-hint: "[research question]"
---

Conduct a time-boxed spike to answer a focused research question before planning begins.

Research question:
$ARGUMENTS

---

A spike is not open-ended research. It has a defined question and a defined exit condition: enough information for the planner to decompose the work confidently.

**Step 1 — Define the question**
Restate the research question in precise terms. What specifically needs to be known before planning can proceed?

**Step 2 — Investigate**
Explore the codebase, read relevant files, and research the problem space. Stay within the scope of the question — do not investigate beyond what's needed to answer it.

Useful approaches:
- Read existing code for established patterns and constraints
- Identify what already exists vs. what needs to be built
- Identify technical risks or unknowns
- Evaluate options and their tradeoffs

**Step 3 — Produce a findings report**

```
## Spike: [Question]

### What we learned
- [key finding]

### Options considered
| Option | Tradeoffs |
|---|---|
| [option] | [pros/cons] |

### Recommended approach
[What to do and why]

### Assumptions and risks
- [assumption or risk]

### Open questions
- [anything still unresolved]

### Ready to plan?
yes / no — [reason if no]
```

**Step 4 — Present to the human**
Present the findings report and ask whether to proceed to `/story` or continue investigating. Do not proceed to planning unilaterally.