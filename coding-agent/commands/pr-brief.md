---
name: pr-brief
description: Synthesizes comprehension history from all approved slices in the current story into a pairing-session-ready brief. Run before a PR review to reconstruct the decisions you approved.
argument-hint: "[story slug or plan file path (optional)]"
---

Produce a PR Brief for the current story by synthesizing the explain-back history and key decisions from all completed slices.

Story context (optional):
$ARGUMENTS

---

Follow this sequence:

**Step 1 — Locate the plan file**

Find `docs/stories/<slug>/plan.md`. If $ARGUMENTS provides a slug or path, use it. Otherwise, identify the slug from recent git commits (the plan file path is in the orchestrator update commits) or ask the human to confirm the slug.

**Step 2 — Extract scaffolding and skip flags**

Read the plan file. Collect:
- All `Scaffolding for` and `Interface contract` fields from each slice
- All `Comprehension skipped` markers and their decision topics

**Step 3 — Synthesize from conversation context**

From the current conversation history, collect:
- The explain-back exchanges: the questions asked and the human's answers (or the re-explain loops that occurred)
- Any decisions where the human demonstrated understanding in their own words

If conversation history for a slice is not available (e.g., context was compacted), note the gap rather than fabricating a summary.

**Step 4 — Produce the PR Brief**

Output the following document:

---

# PR Brief: [Story Title]

## What changed and why
[2-4 sentence narrative covering the full story arc — what problem was solved, what approach was taken, what was ruled out]

## Slice-by-slice decisions

For each slice in the plan:

### [Slice N: name] — [commit hash if known]

**Key decisions:**
- [Decision 1]: [rationale in 1-2 sentences, synthesized from the explain-back exchange or plan context]
- [Decision 2 if present]

**Scaffolding note** (if applicable):
- Created [interface/stub] for [Slice M] — contract: [interface contract text]

**Comprehension skip** (if applicable):
> FLAGGED: [decision topic] was not explained back on [date]. Review this decision before pairing.

## Likely reviewer questions
[3-5 questions a code reviewer might ask, derived from the decisions documented above — phrased as the reviewer would ask them, not as the human would answer them]

## Skipped decisions (full list)
[If any comprehension skips occurred, list them here as a single consolidated block for easy scanning. If none, omit this section.]

---

**Step 5 — Offer drill-down**

After presenting the brief, offer:

> "Want to drill into any of these decisions before the review? I can walk through the rationale for any slice."

Wait for the human's direction. If they ask about a specific decision, explain it using the plan and git diff as sources. Do not invent rationale that wasn't in the original implementation.
