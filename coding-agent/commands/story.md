---
name: story
description: Author a new story card in product-centric, PM-legible language. Drafts collaboratively — no sprint tool is touched until you say so. Use /plan to decompose an approved story into technical slices.
argument-hint: "[story idea or feature description]"
---

Compose a new story card based on the following input. Work collaboratively — draft first, iterate with the human, and do not finalize until explicitly approved.

Story idea:
$ARGUMENTS

---

## Authoring principles

**Product-centric framing.** The story captures a user-facing outcome, not a technical task. The summary and acceptance criteria describe what a user can do or experience — not what code was written or which endpoints exist.

**Vertical slices.** A story represents a complete unit of user value, even if delivering it touches multiple codebases, repos, or teams. The fact that it spans repos is an engineering concern, not a story concern — don't split by repo.

**PM-legible prose.** No HTTP status codes, file paths, code blocks, or step-by-step implementation lists in the description or acceptance criteria. The story should be readable by a PM or stakeholder without a technical background. Technical specifics belong only in the Notes section.

**Outcome-level acceptance criteria.** Each criterion should be verifiable by a non-engineer. Frame as observable user outcomes: "A user who does X experiences Y." Not: "Endpoint returns 200" or "session cookie is set."

---

## Story structure

**Summary** — One declarative sentence stating the user-facing outcome as a headline. Should complete: "When this story is done, a user can..."

**Background** — One short paragraph: why this matters, what problem it solves. No implementation detail.

**What needs to happen** — A tight bullet list of the high-level work required, in plain language. Systems and repos may be named when they help the reader understand scope, but implementation mechanics stay out.

**Notes** *(include when relevant)* — Implementer-facing context only: related ticket numbers, repo names, known dependencies, open questions. This is the only section where technical specifics belong.

**Acceptance criteria** — Outcome-level bullets, verifiable without engineering knowledge.

---

## Process

1. Read the story idea from $ARGUMENTS or conversation context.
2. If the input is ambiguous, ask focused clarifying questions before drafting — not a list.
3. Draft the story using the structure above.
4. Present the draft and ask what to adjust.
5. Iterate until the human approves.
6. When approved, present the final card cleanly. Do not create a ticket in any sprint tool — that is the human's next step.
7. After approval, offer: "Ready to decompose this into technical slices? Run /plan with this story."
