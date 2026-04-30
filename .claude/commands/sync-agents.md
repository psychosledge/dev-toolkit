---
name: sync-agents
description: Detect and reconcile drift between global (~/.claude/) and repo (coding-agent/) agent and command files. Analyzes each diff for workloop impact before recommending changes.
argument-hint: "[optional: path to repo root, defaults to current directory]"
---

You are performing a drift audit between global Claude config files and this repo's source-of-truth agent/command files. Your goal is not just to list differences — you must critically evaluate each difference against the intended workloop before recommending any action.

## Locations

**Global (what Claude actually runs):**
- `~/.claude/agents/` — subagent definitions
- `~/.claude/commands/` — slash command skills

**Repo (source of truth):**
- `coding-agent/agents/` — subagent definitions
- `coding-agent/commands/` — slash command skills

If a repo root was passed as an argument, use that path instead of the current directory.

---

## Step 1: Discovery

List all `.md` files in each of the four directories. Build a complete matrix of every unique filename across all four locations.

---

## Step 2: Classify Each File

For each filename, run `diff` between the global and repo versions and classify as:

- **Identical** — no differences (skip in report, note count only)
- **Repo ahead** — repo has changes the global copy doesn't
- **Global ahead** — global has changes the repo copy doesn't
- **Diverged** — both sides have changes relative to each other (non-trivial merge needed)
- **Repo only** — exists in repo but not in global
- **Global only** — exists in global but not in repo

---

## Step 3: Workloop Impact Analysis

This is the critical step. For every non-identical file, evaluate the diff against the intended workloop. Be skeptical — question whether each change is genuinely better, genuinely worse, or just different.

**The intended workloop:**
1. `/story` — author a story card in product-centric, PM-legible language; draft and iterate with the human; no planning begins until the human explicitly approves the card
2. `/plan` — planner decomposes the approved story into thin vertical slices with AC and a UAT checklist; writes plan to `docs/stories/<slug>/plan.md`; human approves before any work begins
3. `/slice` — for each slice: architect check (if needed) → coder implements with TDD → verifier runs full review → **human sees full report unconditionally** → human approves → commit
4. `/bug` — characterize → architect check → coder fix with regression test → verifier → human approves → commit
5. `/verify` — standalone verification pass
6. Human gates are **unconditional** — the human always sees complete results before any action is taken, whether passing or failing
7. Agents surface issues to the human; they never compensate silently or loop autonomously

**For each non-identical file, work through these questions:**

- Does this change strengthen or weaken a human gate? (Any weakening is a serious concern.)
- Could it cause the orchestrator to loop silently — fixing things before the human sees them?
- Does it improve or degrade TDD discipline (red-green-refactor)?
- Does it add clarity or introduce ambiguity about the agent's responsibilities?
- Is it consistent with what other agents in the team depend on or expect?
- Does it improve the quality bar, or does it lower the bar for shipping?
- Does it add unnecessary process overhead or complexity?
- If this is a removal, is something important now missing?

Rate the impact: **Positive** / **Neutral** / **Negative** / **Mixed** — and justify the rating in one or two sentences. Don't default to Positive just because a change adds content.

---

## Step 4: Reconciliation Report

Present findings using this structure for each non-identical or orphaned file:

---
### `[filename]` — [Repo ahead / Global ahead / Diverged / Repo only / Global only]

**What changed:** [Plain-English summary of the diff — what was added, removed, or modified]

**Workloop impact:** [Positive / Neutral / Negative / Mixed]
[One or two sentences of critical analysis. Name the specific workloop principle affected.]

**Recommendation:** [Copy repo → global / Copy global → repo / Manual merge needed / No action — with brief rationale]

---

After all files, present a summary table:

| File | Direction | Impact | Recommendation |
|------|-----------|--------|----------------|
| ... | ... | ... | ... |

Also report the count of identical files skipped.

---

## Step 5: Human Approval Gate

**Do not copy, write, or modify any files.** Present the full report and ask:

> "Review the reconciliation above. Tell me which files to sync — you can say 'approve all', name specific files, or override any recommendation. I will not touch any files until you give explicit approval."

---

## Step 6: Execute Approved Changes

For each approved action:

1. **Copy repo → global**: copy the repo file to the global location, overwriting the global version
2. **Copy global → repo**: copy the global file to the repo location, overwriting the repo version
3. **Manual merge**: show both versions side-by-side, work through the merge interactively with the human before writing anything
4. Confirm each write with the exact source → destination path

After all copies are complete, re-run `diff` on every changed pair to confirm no remaining drift on the synced files.
