# Testing safeguards on every repo
Tier: core

## Slice Plan

### Slice 1: Review flags redundant tests on every repo
**Scope:** The verifier runs the kill-matrix check on every repo, Contract or not, and reports it outside the Contract section. The kill-matrix rules (`coding-agent/skills/contract/SKILL.md` `## Kill-matrix check`) move verbatim to a new standalone skill, `coding-agent/skills/kill-matrix/SKILL.md`, preloaded through the verifier's frontmatter `skills:` list. The rules hold no Contract-specific text: tooling is detected from the repo's own mutation-testing config files, the manual path names each mutation and confirms by inspection, and they cover new or changed tests. A flagged test is advisory. It doesn't change the verifier's approval status and never enters the `/auto-slice` fix loop. The coder (which has no kill check today), the architect, and every other Contract behavior (rows, coverage, Contract-first bug fix order) stay as they are.
**Status:** ✅ done
**Commit:** 33e0ebe
**Acceptance Criteria:**
- [x] A skill-testing baseline (5 fresh runs, current verifier text, repo with no `## Contract` section, diff adding a test strictly subsumed by an existing one) is captured before the edit. Observed: 5/5 detected the redundant test; 5/5 filed it under Issues as medium and lowered the quality rating (6–7/10); 5/5 recommended deleting it as a Refactoring Suggestion; no run reported it in a dedicated Kill-Matrix section.
- [x] The same scenario after the edit (5 fresh runs) shows the redundant test listed only in the `## Kill-Matrix` section as a removal candidate, with the mutation it was checked against named. It does not appear in Issues or Refactoring Suggestions, no run recommends deleting it, and the quality rating doesn't count it.
- [x] The verifier's report carries the kill-matrix result in a `## Kill-Matrix` section, placed after Test Coverage Analysis and present on every repo. It opens with `tooling used / manual check` and lists each flagged test as `test identifier — mutation checked — no unique kill`. The Contract section no longer contains a Kill-matrix line, and section 9 is no longer gated on the Contract.
- [x] The `contract` skill no longer holds the kill-matrix rules or a pointer to them, and no file under `coding-agent/` sends a reader to the `contract` skill for them.
- [x] A verification run on a repo with `Enabled: yes`, with the same redundant-test diff, shows that test flagged as a removal candidate. The kill-matrix result appears exactly once in the report, and each flagged test is listed once.
- [x] When the diff adds or changes no tests, or the repo has no test suite, the `## Kill-Matrix` section says the check found no new tests and lists no removal candidates, with no invented mutants.
- [x] The verifier checks independently of the coder: a test the coder flagged and the human kept is flagged again at review if it still kills nothing unique. "Once" applies within each report.
- [x] The verifier never deletes or edits a flagged test, and a flagged test doesn't lower the approval status. In an `/auto-slice` run, a flagged test is recorded under `## Deferred findings`, is never sent to the fix loop, reaches the human in the end report, and stays in the code.
- [x] Changes committed on main and synced with `/sync-global`.
**Files:** coding-agent/agents/verifier.md, coding-agent/skills/contract/SKILL.md, coding-agent/skills/kill-matrix/SKILL.md (new), coding-agent/commands/auto-slice.md (existing: end-report and Deferred findings handling), coding-agent/commands/code-review.md (existing: consolidation)
**Needs Architect:** no. Planner's call: the home is a standalone skill. Inlining the rules in both agents would make two copies, which the interface contract rules out.
**Scaffolding for:** Slice 2: Coder checks new tests before handoff. The `kill-matrix` skill is the single source both agents read.
**Interface contract:** The kill-matrix rules live only in `coding-agent/skills/kill-matrix/SKILL.md` and state the tooling path, the manual-check path, and the "removal candidate, never automatic deletion" outcome. The flagged-test entry format is the one in this slice's report criterion. Slice 2 preloads the same skill, reuses that entry format, and adds no second copy of the rules. Removing a flagged test happens only through `/code-review`'s fix flow, when the human calls it out.

### Slice 2: Coder checks new tests before handoff
**Scope:** The coder runs the kill-matrix check on the tests it added or changed before reporting back, on every repo, and lists any test that catches nothing new as a removal candidate in its report. The coder has no kill check today. This adds one as a new workflow step after REFACTOR and before the Contract exhale, and it isn't gated on the Contract. The coder does not delete the test. The verifier's check from Slice 1 still runs at review.
**Status:** not started
**Commit:** —
**Acceptance Criteria:**
- [ ] A skill-testing baseline run (fresh subagent, current coder text, repo with no `## Contract` section, slice whose natural test set includes one test fully covered by another) is captured in full before the edit and shows no kill check in the coder's report.
- [ ] The same scenario after the edit shows the coder naming, per new test, the mutation it catches, and listing the redundant test as a removal candidate under a `### Kill Check` subsection of its report, in Slice 1's entry format.
- [ ] The coder leaves a flagged test in place and reports it. It never removes one itself. Removal happens in `/code-review`'s fix flow when the human calls it out.
- [ ] The coder preloads the `kill-matrix` skill through its frontmatter `skills:` list; no rule text is duplicated in coder.md.
- [ ] On a repo with `Enabled: yes`, the same scenario shows the redundant test flagged as a removal candidate, with the kill check appearing once in the coder's report.
- [ ] Changes committed on main and synced with `/sync-global`.
**Files:** coding-agent/agents/coder.md, coding-agent/commands/slice.md and coding-agent/commands/auto-slice.md (where the coder's report reaches the human)
**Needs Architect:** no. Reuses the home and outcome decided in Slice 1.

### Slice 3: Design asks which unwritten requirements a change touches
**Scope:** On every repo, the architect asks the human which unwritten requirements the change touches (a response-time budget a caller relies on, an ordering guarantee, an idempotency assumption), offering the candidates it found in the code. Each one the human confirms is listed in the ADR as a required test. On a repo with the Contract enabled, the same single question also feeds the ADR's Contract rows. The Contract section of the architect no longer owns the question. Story wrap-up lands in this slice's commit.
**Status:** not started
**Commit:** —
**Acceptance Criteria:**
- [ ] A skill-testing baseline run (fresh subagent, current architect text, repo with no `## Contract` section, design task where a caller visibly relies on an unstated budget or ordering) is captured in full before the edit and shows no question about unwritten requirements.
- [ ] The same scenario after the edit shows the architect listing the unwritten requirements it found in the code as candidates, alongside the draft design at its Human Approval Gate, and asking which ones the change touches. The question rides with the design, with no separate round trip.
- [ ] After the human answers, the revised ADR lists each confirmed requirement under a `### Required tests` section (requirement, then the test that enforces it), placed beside the Contract rows section. A rejected candidate does not appear.
- [ ] On a repo with `Enabled: yes`, a verification run shows the question asked once. Confirmed requirements that are durable invariants, per the `contract` skill's "What belongs in it", appear both as Required tests and as Contract rows, without a second question.
- [ ] In an `/auto-slice` run, the question is presented with the design at the design-approval gate (existing: coding-agent/commands/auto-slice.md, Step 1), which waits for the human in every mode. It is not answered by a ruling.
- [ ] The architect's Contract section no longer contains the unwritten-requirements behavior; it holds only the Contract-file reading and row proposal.
- [ ] Changes committed on main and synced with `/sync-global`.
- [ ] Before this commit, `hardening-story.md` has been taken through `/story` into its own `docs/stories/<slug>/` directory with an entry in `docs/stories/README.md`.
- [ ] The commit deletes `docs/stories/testing-safeguards-on-every-repo/` and removes its entry from `docs/stories/README.md`.
**Files:** coding-agent/agents/architect.md, coding-agent/commands/auto-slice.md (existing: design-approval gate), docs/stories/README.md
**Needs Architect:** yes. Where the question sits in the architect's flow, how it shares one answer with the Contract-row proposal, and the shape of the ADR's required-tests field are open decisions with alternatives.

## Review Focus

Failure-mode sweep, core tier:

- A flagged test deleted without the human's agreement, in either `/slice` or `/auto-slice` (silent loss of coverage): covered: Slice 1, Slice 2
- Diff adds no tests, or the repo has no test suite (dev-toolkit itself): kill check should report "no new tests" without inventing mutants. covered: Slice 1
- Developer confirms zero unwritten requirements or skips the question: design proceeds with an empty required-tests field and no re-ask. deferred: hardening story
- An ADR's required test never gets written by the coder, and nothing at review checks for it: deferred: hardening story
- Configured mutation tooling fails, times out, or is too slow to run scoped: deferred: hardening story
- Slices marked `Needs Architect: no` never get the unwritten-requirements question: out of scope: the story places the question in design

Hardening story draft: [hardening-story.md](hardening-story.md)

## Walkthrough Checklist
(Complete after all slices are implemented and committed)

- [ ] In a scratch repo with no `## Contract` section, run `/slice` on a slice that needs the architect and whose code has a caller relying on an unstated budget. Verify the architect asks which unwritten requirements the change touches and lists its candidates.
- [ ] Confirm one candidate and reject another. Verify the ADR lists the confirmed one as a required test and omits the rejected one.
- [ ] In the same repo, let the coder add a test that catches nothing an existing test doesn't. Verify the coder's report names it as a removal candidate and the test is still in the code.
- [ ] Continue to review. Verify the verifier's report flags the same test as a removal candidate in a section outside any Contract section.
- [ ] Decline removal. Verify the test stays and is committed.
- [ ] Repeat with a second redundant test and agree to removal. Verify it is removed only after that agreement.
- [ ] Run one slice through `/auto-slice` with a redundant test. Verify the test appears in the end report and is still in the code.
- [ ] In a scratch repo with `Enabled: yes`, run the same design. Verify the unwritten-requirements question is asked once and confirmed durable requirements appear as Contract rows.
- [ ] In that repo, verify the coder's report and the verifier's report each show the kill check once, with each flagged test listed once, and the Contract section carries no kill-matrix line.
- [ ] Open `coding-agent/skills/contract/SKILL.md`. Verify it holds no kill-matrix rules and nothing else in `coding-agent/` points to it for them.
- [ ] Verify `~/.claude/` matches `coding-agent/` for every touched file.
