---
name: comment-quality
description: The bar every code comment must clear, for writing and reviewing code. Use when writing, adding, or reviewing code comments, and when judging whether an existing comment should stay.
---

# Comment Quality

Comments are a smell, not a tool. Apply this bar to every comment regardless of whether the
project has its own documented comment policy. Code that needs a comment to be understood is a
design problem; a comment only survives if it's defended strongly (an ordering requirement, an
external-system quirk, a rationale truly invisible in the code) — flag anything weaker for
removal, not just rewording.

When writing code, the default for every comment you're about to write is that it shouldn't
exist. Run it through the same bar below before writing it.

## The bar

**Accuracy isn't the bar.** Never grant `Keep` just because a comment's claim checks out
against the code — that only clears the floor. An accurate comment still fails if it restates
an effect already visible from the surrounding code (a `v-if`/template gate, a name that
already says it), weighs the chosen approach against a rejected alternative, or matches a
pattern every sibling instance in the file leaves uncommented. Verifying accuracy answers "is
this true," not "does this earn its place" — always ask the second question separately, even
for a clause that survives the first, and even for a clause you already trimmed down to
because the rest of the comment was weak.

**Two concrete tests, per surviving clause.** (1) Would a competent reader actually try to "fix"
this without the comment? If the code's intent is already legible on its face — explicit
arithmetic, a named computed property, a type union, a well-chosen name — a comment answering a
question nobody would ask fails this test no matter how true or well-written it is. Reserve
`Keep` for a comment protecting against a *plausible* misreading (a value that looks simplifiable
but silently breaks something if it is), not a hypothetical one. (2) Is this fact already
dictated somewhere else — a project convention, a type declaration, an accessibility/design-system
rule the repo already enforces, a policy documented anywhere reachable? If a reader who wondered
"why is it done this way" could find the answer by consulting that authority, restating it here
is redundant; if the repo's own rules already make the decision, a comment defending that decision
adds nothing. Both must fail — genuinely non-obvious need, not recorded elsewhere — for a clause
to survive.

**Prefer rewriting the code over keeping the comment.** Before `Keep` on a clause that passes
both tests above, ask whether a rename, an extracted constant, or a restructured conditional
(e.g. replacing a fragile multi-class combination with one explicit computed variant) would make
the fact self-evident and remove the need entirely. Propose that instead of defending the
comment — it's the preferred outcome, not a fallback. Only keep a comment when no reasonable
rewrite removes the need, and even then it must compress to a short fragment (a few words), never
a full sentence or clauses joined by em-dashes/"and."

**On the fence, drop it.** If the checks above leave genuine doubt whether a comment earns its
place, the default is removal, not `Keep`. The asymmetry favors dropping: a wrongly-removed
comment is one line, sitting in git history, trivial to reinstate if it turns out to matter. A
wrongly-kept one persists, invites the next person to pattern-match on it, and compounds. `Keep`
is for a comment that clearly clears the bar, not one that merely fails to clearly fail it.

**Decompose before judging.** Split a comment with more than one clause or sentence into its
individual factual claims, and test each claim independently against the bar rather than
rendering one holistic verdict on the comment as a whole. A comment can read as earned because
one clause sounds substantive while the others are dead weight. Keep only the clauses that
independently survive: trim to just the strong clause if one is buried among weak ones, and
remove the whole comment if none survive.

**Ownership.** Flag a comment that describes behavior whose actual mechanism lives in a
different file, module, or component, even when the description is accurate and appears
nowhere else. This is distinct from the restated-rationale check below, which catches the same
explanation written twice — this one catches an explanation written only at a location that
doesn't own the behavior it describes. Point the reader to the source instead of narrating it
secondhand at the call site.

**Always flag:**
- A comment justifying something every other instance of the same pattern in the file (other
  `emit()` calls, other similar functions) does silently.
- A rationale restated at a second location instead of stated once at its source.
- Em-dash-joined comment sentences.
- A comment that explains what the code already says for itself.
- A comment citing an ADR/story/other internal doc by name or number instead of inlining the
  fact (the reader may have no access to that doc).
- A comment framed around avoiding a past bug ("Regression: ...", "This used to ..."). A test's
  existence already documents what it guards against. If there's a real fact worth keeping (why
  the bug happened, a non-obvious mechanism), state that fact directly rather than narrating it
  as regression history.
- `// Arrange` / `// Act` / `// Assert` comments in a test, even when an existing precedent in
  the file already uses them. The blank lines between phases already show the structure.

If the project's own CLAUDE.md/AGENTS.md documents additional comment conventions, check those
too, but they add to this bar, they don't substitute for it.

## Auditing

**Scope.** The audit isn't limited to comment lines the diff itself added or edited. Any
comment describing a line, function, or block the diff touches is in scope, even when the
comment's own text is untouched — a diff can change what's true about the code around a
comment without touching the comment's own lines. This includes comments inside wholly new
files.

Before a `Keep` verdict, verify the comment's claim against the actual code. If the comment
describes something outside the code in view (another file, an external system, a doc), check
it: grep the sibling code, read the referenced file.

Show every comment in scope, in full, with one of three verdicts:

- `Keep: <reason>` — the bar is met and the claim checks out.
- `Remove — wrong: <reason>` — the comment misdescribes the code (a correctness issue, not a
  style one).
- `Remove — weak: <reason>` — the comment doesn't meet the bar but isn't inaccurate (redundant,
  restates the code, weak rationale).
