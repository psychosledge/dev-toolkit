# Design moves on when no unwritten requirements apply
Tier: core

## Slice Plan

### Slice 1: "None" and a skipped question complete the design
**Scope:** The architect's unwritten-requirements question gets two defined outcomes beside confirm/add/reject: the human answers "none", or approves without answering. Both end with the ADR's Required tests section showing an empty list and the design proceeding to implementation. The question is asked once per design, including when a revised design is re-presented. The `/slice` and `/auto-slice` design-approval gates carry the same outcome. Out of scope: how the verifier or `/code-review` treats an empty Required tests section (owned by `review-catches-missing-required-tests`).
**Status:** not started
**Commit:** —
**Acceptance Criteria:**
- [ ] A baseline run (skill-testing) on the current text, before any edit, presents a design with candidates, receives "none of these apply, approved", and its output is captured verbatim; the same is done for an approval reply that ignores the question. If neither baseline stalls, re-asks, keeps candidates, or invents requirements, the slice stops with no guidance written and the finding goes to the human.
- [ ] After the edit, a verification run given the "none" reply produces an ADR whose Required tests section shows an empty list, with the "Candidates awaiting confirmation" line removed and no candidate rows left.
- [ ] After the edit, a verification run given an approval reply that does not address the question produces the same empty Required tests section, followed by one line `Offered, not reviewed: <candidates>` naming each dropped candidate.
- [ ] In both verification runs, the question is not asked again: neither in the reply to the answer, nor when the human requests a design change and the architect re-presents the revised design.
- [ ] When a revised design surfaces candidates the first presentation didn't list, the re-presented design asks about only those new candidates. The settled list stays as answered.
- [ ] In both verification runs, the design counts as approved and the flow continues to implementation, with no follow-up question or named stop caused by the empty list. This holds under `/slice` Step 1 and `/auto-slice` Step 1.
- [ ] The architect still never invents a requirement the human did not confirm or name to fill the empty list.
- [ ] The confirm/add/reject revision path from the Unwritten Requirements section behaves as before (existing: coding-agent/agents/architect.md, Unwritten Requirements).
- [ ] The edited text follows the repo's writing rules (no em-dash-joined sentences, no contrast constructions) and is synced to `~/.claude/` with `/sync-global` after commit.
- [ ] The commit that lands this slice deletes `docs/stories/design-moves-on-when-none-apply/` and removes its entry from `docs/stories/README.md`.
**Files:** coding-agent/agents/architect.md (Unwritten Requirements, Human Approval Gate, ADR template Required tests), coding-agent/commands/slice.md (Step 1), coding-agent/commands/auto-slice.md (Step 1), docs/stories/README.md, docs/stories/design-moves-on-when-none-apply/
**Needs Architect:** no — the question, its gate, and the placement across architect.md and the two command files were decided in f5d60d3; this slice fills in two outcomes inside that shape.

**Implementation notes:**
- The line to remove is `Candidates awaiting confirmation. *(remove this line when the human answers)*`, directly under `### Required tests` in architect.md's ADR template.
- The architect revises the ADR in place after the human answers (architect.md, Unwritten Requirements). The two outcomes live in architect.md. Command files only point at them.
- `/auto-slice` Step 1 already keeps design approval as a human gate and says only the human answers the question. `/slice` Step 1 has no mention of the question yet.
- "Stalls" means the architect or orchestrator waits for an answer instead of proceeding on an approval. Per skill-testing, guidance addresses only the failures a baseline actually showed. If one baseline is clean, that outcome gets no new text.
- The architect-found-no-candidates case ("If you found none, say so and ask the same question") ends the same way as a "none" answer. It is covered by the same edit and checked in the walkthrough.
- "The repo's writing rules" are the Sentence-Level Style and Concise Comments sections of the global CLAUDE.md (coding-agent/CLAUDE.md). `/sync-global` runs after the commit and is checked at slice close, not in the commit.
- Planner's call: an empty list renders as the single line `None.` under `### Required tests`, replacing the table. An empty table with headers only reads as a template left unfilled.
- Planner's call: a reply that approves the design and names no candidate to keep counts as "none" ("no", "nothing to add", "looks good, go ahead"). A reply that names some candidates follows the existing confirm/add/reject path.
- Planner's call: the fixture is a fresh subagent given architect.md and a scripted design-gate exchange with two candidates (a timeout-implied response budget and an ordering a consumer assumes). `/slice` and `/auto-slice` Step 1 are driven by a second subagent given the command text, the architect output, and the scripted human reply, reporting what it does next.
- Human's call: a skipped question leaves `Offered, not reviewed: <candidates>` below `None.` A "none" answer leaves only `None.`
- Human's call: a revised design asks about only candidates new since the first presentation.
- Human's call: the hardening draft goes through `/story` into its own directory before the landing commit deletes this one.
- Planner's call: AC 17 is checked inside the verification run with a third scripted reply (confirm one, reject one). It doesn't need a separate baseline, because that text doesn't change.

## Review Focus

- Human requests design changes without answering the question, then the architect re-presents: covered: Slice 1
- `/auto-slice` treats an empty Required tests list as something needing a ruling or a stop: covered: Slice 1
- A skipped question discards candidates the architect found, so a real unwritten requirement the human never looked at drops out of the ADR silently: covered: Slice 1 (`Offered, not reviewed:` line)
- A partial or ambiguous reply ("approved, the first one maybe") leaves unclear which candidates survive: deferred: hardening story ([draft](hardening-story.md))
- Verifier or `/code-review` flagging an empty Required tests section as a missing deliverable: out of scope: owned by `review-catches-missing-required-tests`

## Walkthrough Checklist
(Complete after all slices are implemented and committed)

- [ ] Run `/slice` on a slice that needs the architect. When the design arrives with candidate requirements, reply "none of these apply, approved". Confirm the ADR's Required tests section is empty, the "Candidates awaiting confirmation" line is gone, and the coder starts.
- [ ] Repeat with a reply that approves the design and says nothing about the question. Confirm the same empty section, an `Offered, not reviewed:` line naming the candidates, and that implementation starts.
- [ ] Repeat where the architect found no candidates. Reply "approved". Confirm the empty section and that implementation starts.
- [ ] Ask for a design change without answering the question. Confirm the revised design comes back without the question.
- [ ] Ask for a design change that leads the architect to a new candidate. Confirm the revised design asks about only that candidate.
- [ ] Run `/auto-slice` on an architect slice and answer "none" at the design gate. Confirm no ruling or named stop follows from the empty list and the run continues to the end report.
- [ ] Confirm one candidate and reject the rest. Confirm the ADR keeps exactly the confirmed requirement.
- [ ] Confirm the architect added no requirement you did not confirm or name.
