---
name: story
description: Every story starts here. Drafts a new story card from an idea or backlog entry, or confirms an existing ticket is story-shaped, in product-centric, PM-legible language, then writes the story's story.md, which /plan requires. No sprint tool is touched. Use /plan to decompose the approved story into technical slices.
argument-hint: "[idea, backlog entry, or ticket ID/URL]"
---

Turn the following input into an approved story. Work collaboratively, and do not finalize until the human explicitly approves.

Input:
$ARGUMENTS

---

## Input modes

The input's shape picks the mode:

- **Confirm mode:** the input names or contains an existing ticket in an external tracker: a ticket key (pattern `[A-Z]+-[0-9]+`), a ticket or issue URL, or pasted ticket content carrying its key. Read the ticket (through a connector when one is available, otherwise from what was pasted; if neither gives you its content, ask the human to paste it).
- **Draft mode:** anything else: a backlog entry, free text, a draft card file.

**Confirm mode output** is a review of the ticket. It never restates or redrafts the ticket whole. Present, in order:

1. A verdict line: `<KEY> is story-shaped` or `<KEY> needs changes before planning`.
2. One line per authoring principle below (epic test, product framing, PM-legible prose, outcome-level acceptance criteria): ✅ when it passes; ❌ plus the specific problem when it doesn't.
3. For each ❌, the replacement text for that part of the ticket, paste-ready in a fenced block, for the human to apply in the tracker. An epic gets a proposed split instead: each piece as a full card (Story structure below) in its own fenced block, paste-ready as a new ticket.
4. The tier question (Process step 6).

---

## Authoring principles

**Product-centric framing.** The story captures a user-facing outcome, not a technical task. The summary and acceptance criteria describe what a user can do or experience — not what code was written or which endpoints exist.

**Vertical slices.** A story represents a complete unit of user value, even if delivering it touches multiple codebases, repos, or teams. The fact that it spans repos is an engineering concern, not a story concern — don't split by repo.

**Watch for epics disguised as stories.** A story delivers one user-facing outcome. If the input describes several outcomes that would each independently matter to a user even if the others never shipped, that's not one story with broad reach — it's several stories. Test: "would a user notice or care if only piece A shipped, and B and C never happened?" If yes for more than one piece, split into separate story cards. This is distinct from the "don't split by repo" guidance above — that guards against splitting one outcome that *needs* multiple repos to exist at all (an outcome nobody can observe until both halves ship); this guards against merging several outcomes that each stand alone just because they share a theme or touch related code.

**PM-legible prose.** No HTTP status codes, file paths, code blocks, or step-by-step implementation lists in the description or acceptance criteria. The story should be readable by a PM or stakeholder without a technical background. Technical specifics belong only in the Notes section.

**Outcome-level acceptance criteria.** Each criterion should be verifiable by a non-engineer. Frame as observable user outcomes: "A user who does X experiences Y." Not: "Endpoint returns 200" or "session cookie is set."

---

## Story structure

**Tier** — `core` or `hardened`. The delivery scope downstream planning honors: core defers non-catastrophic hardening into a follow-up hardening story; hardened delivers all hardening within this story. Draft every card as `core`.

**Summary** — One declarative sentence stating the user-facing outcome as a headline. Should complete: "When this story is done, a user can..."

**Background** — One short paragraph: why this matters, what problem it solves. No implementation detail.

**What needs to happen** — A tight bullet list of the high-level work required, in plain language. Systems and repos may be named when they help the reader understand scope, but implementation mechanics stay out.

**Notes** *(include when relevant)* — Implementer-facing context only: related ticket numbers, repo names, known dependencies, open questions. This is the only section where technical specifics belong.

**Acceptance criteria** — Outcome-level bullets, verifiable without engineering knowledge.

---

## Process

1. Read the input from $ARGUMENTS or conversation context, and pick the mode (Input modes above). In confirm mode, steps 2 to 5 take the shape of the Confirm mode output.
2. Check the input against the epic test above. If it describes multiple independently-valuable outcomes, say so and propose splitting into N separate story cards instead of one. Draft each independently (full Story structure per card), present the set together, and let the human approve the split — don't default to bundling just because the input arrived as one request.
3. If the input is ambiguous, ask focused clarifying questions before drafting — not a list.
4. Draft the story using the structure above.
5. Present the draft and ask what to adjust.
6. Iterate until the human approves. Approval covers the tier: confirm `core` or `hardened` with the human explicitly before finalizing, and record the confirmed value on the card.
7. When approved, write `docs/stories/<slug>/story.md` for each approved story (a different docs location named in the repo's `CLAUDE.md` wins). The slug comes from the story title: lowercase, hyphen-separated, at most 40 characters. The file opens with an H1 title and, on the next line, `Tier: <value>` with the confirmed tier. Then:
   - **Draft mode:** the approved card text.
   - **Confirm mode:** a pointer: `Ticket: <KEY> (<link>)`, with the parenthetical omitted when no link is known. It never restates ticket content; the ticket stays the source of truth, including any changes the human pastes into it.

   Present the final card(s) cleanly, or in confirm mode the confirmed ticket key and tier, and the story.md path. Do not create or edit a ticket in any sprint tool; that is the human's step. If a `tracking-config` project memory exists, add each approved story to the live tracker README per the `tracking` skill's workloop checkpoints.
8. After approval, offer: "Ready to decompose this into technical slices? Run /plan with this story." If the input was split into multiple cards, offer this per card, and let the human pick which one to start with rather than assuming an order.
