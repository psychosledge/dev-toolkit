---
name: stakeholder-language
description: Wording rules for anything a stakeholder outside the engineering workloop will read or hear, such as sprint recaps, standup talking points, and demo plans. Referenced by sprint-recap, standup, and demo-prep; not normally invoked directly.
---

# Stakeholder Language

Applies to every artifact or talking point written for an audience beyond the day-to-day
engineering work, technical and non-technical stakeholders alike.

- **No internal tooling jargon** — the internal workloop (`/plan`/`/slice`/`/code-review`,
  "architect"/"verifier," "Reviewer Mode," "workloop" itself, an internal slice number or
  slice count as the way of referring to a piece of work, "red"/"green" test states) means
  nothing to an outside reader. Describe work by what it actually is. `docs/stories/`,
  `plan.md`, "PR," and "ADR" are fine — general engineering terms, not tooling-specific.
- **Describe progress by what the work does for the product, never by the mechanics of
  producing it** (tests written, verifier passed, committed). "Exports now retry failed
  uploads automatically," never "slice 5 went green."
- **Rephrase the walkthrough checklist ("UAT" in older trackers).** In the workloop it means
  local testing where the user plays the role of the end user. Use "testing" or "local
  testing," since an outside reader would take "UAT" as a formal stakeholder acceptance pass
  and "walkthrough" as internal jargon.
- **Don't name who specifically something got handed off to** — say "prepped for hand off,"
  not the person's name.
- **Trim redundant stakeholder-qualifier phrasing** — a shareable artifact is stakeholder-
  facing by construction, so "a stakeholder-raised request" reads redundant; drop the
  qualifier. Keep it when it's identifying an actual stakeholder-owned thing the sentence
  needs to name (e.g. "the stakeholder's new VPN"), not when it's just framing whose idea
  something was.
- **Don't round timeframes generously** — prefer the precise phrasing when it's just as
  short to write.
- **Check organization-name capitalization** stays consistent throughout (e.g. the
  stakeholder organization's name spelled correctly and consistently, not just however a
  source doc happened to write it).
- **No em dashes** — split into two sentences instead.
