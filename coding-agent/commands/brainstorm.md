---
name: brainstorm
description: Collaborative design exploration with the architect. Open-ended by default — formalizes into a spec or ADR only when you say so.
argument-hint: "[design topic or problem]"
---

Invoke the **architect** subagent in brainstorm mode to think through a design problem collaboratively.

Topic:
$ARGUMENTS

---

This is an exploratory session, not a design deliverable. The architect is your thinking partner — expect pushback, alternatives, and questions, not agreement.

The session has two phases:

**Explore** (default)
Think out loud together. No structure required. No output format expected. The architect will challenge ideas, surface alternatives you haven't considered, and ask questions. It will not anchor to your half-formed ideas just because you stated them.

**Formalize** (you trigger this)
When you're ready to turn the thinking into something concrete, say so — "let's formalize this" or similar. The architect will then produce a formal design spec or ADR and follow the standard approval workflow.

There is no automatic transition. You decide if and when the session produces a formal output.
