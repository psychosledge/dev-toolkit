---
name: skill-testing
description: Test protocol for behavior-shaping edits to skill, agent, and command files. Use when creating or changing any file under coding-agent/ or ~/.claude/ (agents, commands, skills) whose text shapes agent behavior, before the change is committed or synced.
---

# Skill Testing

Guidance text is code that runs on an agent. An edit shipped without a test reflects what the author thinks needs preventing, and agents routinely fail in ways the author didn't predict.

## Does This Edit Need a Test?

**Test it** when the edit shapes behavior: a rule an agent could skip, a workflow step, an output format, a decision criterion, a trigger description.

**Ship it untested** when the edit is mechanical or reference-only: corrected paths, renamed fields, typo fixes, factual reference updates, reordering with no wording change.

## Match the Form to the Failure

Before writing guidance, classify the failure it addresses. The form that fixes one failure type backfires on another.

| Observed failure | Form to write | Form that backfires |
|---|---|---|
| Agent knows the rule and skips it under pressure | Hard rule, plus a rationalization table and red-flags list | Soft guidance ("prefer...", "consider...") |
| Agent complies but the output has the wrong shape | A positive recipe stating what the output is: its parts, in order | A prohibition list ("don't restate", "never narrate") |
| Agent omits a required element from output it already produces | A required field or slot in the template it fills in | Prose reminders near the template |
| Behavior should depend on a condition | A conditional keyed to an observable predicate | An unconditional rule with exemption clauses |

Under a competing incentive, agents negotiate with prohibitions; a recipe leaves nothing to negotiate. Avoid nuance clauses ("don't X unless it matters"): they reopen the negotiation. A real exception becomes its own conditional on an observable predicate.

## The Cycle

**Baseline first.** Before writing the guidance, run the tempting scenario on a fresh subagent without it. Capture what the agent does and says, verbatim. If the baseline doesn't exhibit the failure, there is nothing to fix: stop without writing the guidance.

**Write minimal guidance** addressing the failures the baseline actually produced, in the form the table above picks.

**Re-run the same scenario** with the guidance in place. The agent should now behave correctly and, for discipline rules, cite the guidance when tempted.

**Close loopholes.** A new rationalization in the re-run gets an explicit counter (a rationalization-table row, a red-flag entry), then another re-run. Repeat until no new loopholes appear.

## Running a Test

Dispatch a fresh `general-purpose` subagent per run. Its prompt holds, in order: the draft file's full text framed as its operating instructions, then a realistic task that tempts the failure (real file paths, concrete constraints, a forced choice). Fresh context per run; never reuse a subagent across runs, since it remembers the previous attempt.

Pressure scenarios for discipline rules combine three or more pressures: time, sunk cost, authority, exhaustion. An academic question ("what does the rule say?") tests recall and proves nothing about compliance.

## Micro-Testing Wording

When comparing candidate wordings, or when a change is small enough that a full pressure scenario feels heavy:

- 5+ repetitions per variant, each in a fresh context.
- Always include a no-guidance control.
- Read every flagged output manually. Automated counts mistake template echoes and quoted counter-examples for hits.
- Variance is a signal. Five runs converging on one shape means the wording binds. Five different interpretations mean it doesn't, and the form needs tightening before more words get added.

## The Floor

The minimum for any behavior-shaping change, however small: one baseline run before the edit and one verification run after it, both read in full. "The edit is obviously clear" is the author grading their own prose; the subagent run is the grade that counts.
