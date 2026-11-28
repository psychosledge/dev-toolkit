# Unclear requirement answers get one clarifying question
Tier: core

## Slice Plan

### Slice 1: An unclear answer gets one clarifying question
**Scope:** The architect's Unwritten Requirements revision gets a fourth case beside the three from design-moves-on-when-none-apply: the reply leaves one or more listed candidates' status unclear. The architect asks one question naming only the unclear candidates, then revises the ADR from the clarification and does not ask again. The design does not move to implementation while the question is open. The `/slice` and `/auto-slice` design-approval gates relay the question to the human and wait for the answer. Under `/auto-slice`, only the human answers it. Out of scope: how the verifier or `/code-review` treats the Required tests section (owned by `review-catches-missing-required-tests`).
**Status:** done
**Commit:** —
**Acceptance Criteria:**
- [x] A baseline run (skill-testing) on the current text, before any edit, presents a design with two candidates and receives "approved, the first one maybe"; a second baseline receives "approved, keep the first". Each output is captured verbatim. If neither baseline guesses (drops or keeps an unclear candidate without asking), the slice stops with no guidance written and the finding goes to the human.
- [x] After the edit, a verification run given "approved, the first one maybe" asks one question naming the first candidate as unclear, and the design does not proceed to implementation before the answer.
- [x] After the edit, a verification run given "approved, keep the first" asks one question naming only the second candidate. The first candidate is not part of the question.
- [x] When the clarification answers each unclear candidate, the ADR is revised by the existing keep/add/reject rule (existing: coding-agent/agents/architect.md, Unwritten Requirements), and the design proceeds with no further question about the requirements.
- [x] When the clarification still leaves a candidate unclear, the architect asks nothing further: the candidate is dropped and listed on the `Offered, not reviewed:` line, and the design proceeds.
- [x] A clear reply gets no clarifying question: "none of these apply, approved", an approval silent on the requirements, "keep the first, drop the second", and "only the first". Each follows its existing outcome (existing: coding-agent/agents/architect.md, Unwritten Requirements).
- [x] Under `/slice` Step 1 and `/auto-slice` Step 1, the orchestrator relays the clarifying question to the human and waits. Under `/auto-slice`, no ruling answers it and no named stop is raised.
- [x] The architect never keeps an unclear candidate, or invents one, without the human's confirmation.
- [x] The edited text follows the repo's writing rules (no em-dash-joined sentences, no contrast constructions) and is synced to `~/.claude/` with `/sync-global` after commit.
**Files:** coding-agent/agents/architect.md (Unwritten Requirements, Human Approval Gate), coding-agent/commands/slice.md (Step 1), coding-agent/commands/auto-slice.md (Step 1)
**Needs Architect:** no — the question, its gate, and the revision cases were placed in architect.md with pointers from the two command files in f5d60d3 and f58af2e; this slice adds one case inside that shape.

**Implementation notes:**
- The three existing revision cases and the re-presentation rule are in architect.md, Unwritten Requirements. The Human Approval Gate section states "An approval completes the gate whatever the Required tests section holds after the revision", which an open clarifying question now precedes.
- `/slice` Step 1 and `/auto-slice` Step 1 each say an approval silent on the requirements passes the gate and the reply goes to the architect. Neither says what happens when the architect comes back with a question.
- Per skill-testing, guidance addresses only the failures a baseline actually showed. If the "keep the first" baseline already asks about the second candidate, that reply shape gets no new text.
- Confirmed by the human: a candidate is unclear when the reply hedges on it (maybe, probably, not sure), refers to it in a way that matches no candidate or more than one, or keeps some candidates and says nothing about it. A reply that says the rest go ("only the first", "just the first") is clear.
- Confirmed by the human: a candidate still unclear after the clarification is handled like a skipped question: dropped, and listed on `Offered, not reviewed:`.
- Planner's call: the fixture reuses design-moves-on-when-none-apply's setup. A fresh subagent gets architect.md and a scripted design-gate exchange with two candidates (a timeout-implied response budget and an ordering a consumer assumes). `/slice` and `/auto-slice` Step 1 are driven by a second subagent given the command text, the architect's clarifying question, and a scripted human reply, reporting what it does next.
- "The repo's writing rules" are the Sentence-Level Style and Concise Comments sections of coding-agent/CLAUDE.md. `/sync-global` runs after the commit and is checked at slice close.

**Builder-check answers:**
- The three existing cases (architect.md, Unwritten Requirements): the reply names candidates to keep or requirements to add (keep confirmed, add named, delete rejected); it refers to the requirements and keeps none (table becomes `None.`); it says nothing about them (table becomes `None.`, plus `Offered, not reviewed: <each candidate>` below it when candidates were listed). The fourth case sits before these: a reply that leaves any candidate unclear gets the question first, and the clarified answer then lands in one of the three.
- `Offered, not reviewed:` sits in the Required tests section, one line below the table (or below `None.`). With one candidate kept and one still unclear, the section holds the kept row and the `Offered, not reviewed:` line naming the unclear one.
- A requirement the human names in the clarification is added under the keep/add/reject rule and counts as confirmed. AC18's "invents" means a requirement nobody listed or named.
- After the clarification the ADR is revised in place. A clarification that requests no design change does not re-present the design. The reply's approval stands and implementation begins.
- Planner's call: the Human Approval Gate sentence is edited so an approval with an open clarifying question completes the gate once the answer is folded in. The human does not approve again.
- Planner's call: the question names every candidate the reply does not settle. For "approved, the first one maybe" with two candidates, that is both, since the reply hedges on the first and keeps none outright. AC12 is read as "names the first candidate among the unclear ones", and Walkthrough step 2 answers "keep the first, drop the second".
- Planner's call: a reference that matches no candidate or more than one leaves every candidate it might mean unclear, plus any the reply does not otherwise settle.
- Planner's call: the unclear rule is written in architect.md as a general rule with two or three short examples. A bare "approved, the first" keeps some and is silent on the rest, so it is unclear about the others.
- Planner's call: a hedged reply with no approval ("the first one maybe") is not an approval. The architect sends the clarifying question and the gate stays open for the approval, which can come in the same answer.
- Planner's call: if exactly one baseline guesses, guidance targets that reply shape. The verification AC for the other shape still runs as a regression check.
- Planner's call: in the architect-only run, AC12 passes when the output ends with the clarifying question and does not treat the design as approved or hand off to implementation.
- Planner's call: the AC17 orchestrator run uses the verification run's clarifying question verbatim. The human's answer goes back to the same architect, matching `/slice` Step 1's "Send the reply to the architect".
- Planner's call: under `/auto-slice` the clarification is not a ruling, so it stays out of the rulings ledger. The ADR's Required tests section records the outcome.
- Planner's call: AC18 is checked across the AC12 to AC16 run outputs, with no dedicated scenario.
- Baseline and verification outputs go in the slice's end report to the human. The story directory is deleted on landing, so nothing is persisted there.
- AC19's sync half is a post-commit step checked at slice close, outside the verifier's diff review.
- Tier `core` sets the failure-mode dispositions in Review Focus. It does not change the test protocol.
- Planner's call: the `/slice` and `/auto-slice` Step 1 additions are one-sentence pointers: relay the architect's clarifying question to the human and wait, then send the answer to the architect per its Unwritten Requirements section.
- The fixture is recreated from scratch. The two candidates come from architect.md's own examples: a response-time budget implied by a caller's timeout, and an ordering a consumer assumes.

### Slice 2: Clarifying holds up across design revisions
**Scope:** The clarifying question from Slice 1 holds on the two re-presentation paths. A clarifying reply that also requests a design change settles the requirements and revises the design in one pass. An unclear reply to candidates first listed on a re-presented design, under "Candidates awaiting confirmation", gets the same one question, naming only those candidates.
**Status:** not started
**Commit:** —
**Acceptance Criteria:**
- [ ] A baseline run (skill-testing) on the text as Slice 1 left it, before any Slice 2 edit, covers both paths: a clarifying reply that also requests a design change, and "approved, the new one maybe" to a re-presented design listing one new candidate. Each output is captured verbatim. A path whose baseline neither asks twice nor guesses gets no new text.
- [ ] After the edit, a clarifying reply that also requests a design change gets the revised design re-presented with the requirements settled by the clarification and no requirements question.
- [ ] After the edit, an unclear reply to a re-presented design asks one question naming only the unclear candidates listed under "Candidates awaiting confirmation". The recorded answer from earlier presentations is not reopened.
- [ ] After that clarification, the design moves on with no further requirements question. A candidate still unclear lands on `Offered, not reviewed:`, as in Slice 1.
- [ ] The edited text follows the repo's writing rules and is synced to `~/.claude/` with `/sync-global` after commit.
- [ ] The commit that lands this slice deletes `docs/stories/clarify-unclear-requirement-answers/` and removes its entry from `docs/stories/README.md`.
**Files:** coding-agent/agents/architect.md (Unwritten Requirements re-presentation paragraph), docs/stories/README.md, docs/stories/clarify-unclear-requirement-answers/
**Needs Architect:** no. It extends the re-presentation paragraph Slice 1 leaves in place.

**Implementation notes:**
- Slice 1's landing commit leaves the story directory in place, since Slice 2 is the story's last slice.
- The fixture reuses Slice 1's two candidates. The re-presented design adds one new candidate: an idempotency assumption behind a retry, from architect.md's own examples.

## Review Focus

- Clarifying reply is itself unclear, risking a second question or a guess: covered: Slice 1
- A clear partial reply ("only the first") over-triggers the question: covered: Slice 1
- `/auto-slice` answers the clarifying question with a ruling or raises a named stop: covered: Slice 1
- Clarifying reply also requests a design change, so the re-presentation and the clarification interleave: covered: Slice 2
- Unclear reply to candidates first listed on a re-presented design ("Candidates awaiting confirmation"): covered: Slice 2

## Walkthrough Checklist
(Complete after all slices are implemented and committed)

- [ ] Run `/slice` on a slice that needs the architect. When the design arrives with two candidates, reply "approved, the first one maybe". Confirm one question comes back naming the first candidate and the coder does not start.
- [ ] Answer "keep it". Confirm the ADR keeps the first candidate, drops the second, and the coder starts with no further question.
- [ ] Repeat with "approved, keep the first". Confirm the question names only the second candidate.
- [ ] Repeat, and answer the clarifying question with another hedge. Confirm no second question, the candidate appears on `Offered, not reviewed:`, and the coder starts.
- [ ] Reply "none of these apply, approved". Confirm no clarifying question and the ADR shows `None.`
- [ ] Reply "only the first". Confirm no clarifying question and the ADR keeps exactly the first candidate.
- [ ] Run `/auto-slice` on an architect slice and give a hedged answer at the design gate. Confirm the clarifying question reaches you, no ruling answers it, and the run continues to the end report after you answer.
- [ ] At a clarifying question, answer it and request a design change in the same reply. Confirm the revised design comes back with the requirements settled and no requirements question.
- [ ] On a re-presented design that lists a new candidate, reply "approved, the new one maybe". Confirm one question names only the new candidate and the earlier answer is not reopened.
- [ ] Confirm the architect kept no candidate you did not confirm.

## Rulings

> Ruling (Slice 1): Baseline B ("approved, keep the first") guessed, deleting the unnamed second candidate as rejected; baseline A ("approved, the first one maybe") asked without guessing but also reopened the option choice. The guidance is one general unclear-candidate rule covering hedges, unmatched references, and keep-some-silent-on-the-rest, with the clear "only the first" form stated. Why: the human-confirmed definition is a single rule, the Human Approval Gate sentence must change for either shape, and A's question was not limited to the candidates. Cost if wrong: a few words of guidance for the hedge shape that the baseline already handled.

> Ruling (Slice 1): /sync-global runs once after Slice 2 commits, covering both slices. Why: its Step 5 approval gate would interrupt the autonomous run, and Slice 2 edits the same architect.md section. Cost if wrong: ~/.claude/ runs the pre-story text until the end of the run.

## Deferred findings

- (Slice 1, medium) coding-agent/agents/architect.md, Unwritten Requirements: "Fold the answer in by the three cases below" does not say that the first reply's clear statuses stand, so a silent or "none" clarifying answer after "keep the first" could read as replacing the kept row with `None.`; placement of `Offered, not reviewed:` below a table with kept rows is unstated. Ruling: waits for the whole-branch /code-review, where the fix and a silent-follow-up regression run can land together. Cost if wrong: a kept requirement loses its test on that reply shape until fixed.
- (Slice 1, low) coding-agent/agents/architect.md, Unwritten Requirements: the third unclear clause covers "keeps some", so the rule alone does not make the second candidate unclear in "the first one maybe"; the example carries it. Ruling: waits for /code-review; V1 already asks about both. Cost if wrong: a three-candidate hedge may leave the rest to inference.
- (Slice 1, low) coding-agent/agents/architect.md, Unwritten Requirements: an unmatched reference "leaves every candidate it might mean unclear" is undefined when it matches none, and the plan's "plus any the reply does not otherwise settle" is missing. Ruling: waits for /code-review; no run exercised it. Cost if wrong: an unmatched reference may be read as a new requirement.
- (Slice 1, low) coding-agent/agents/architect.md, Unwritten Requirements: "Ask once per design" can read as conflicting with the clarifying question. Ruling: waits for /code-review; no run misread it. Cost if wrong: a literal reader skips the clarifying question.
- (Slice 1, low) plan.md Rulings: the guidance reaches past the one guessing baseline shape. Ruling: the human confirms or trims at /code-review. Cost if wrong: unbaselined text for hedges and unmatched references.
