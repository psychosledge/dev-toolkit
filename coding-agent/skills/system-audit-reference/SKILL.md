---
name: system-audit-reference
description: Reference for the /system-audit command (tiers, effort and evidence rubrics, writing rules, register template). Not normally invoked directly.
---

# System Audit Reference

Read by `/system-audit`. Supporting files in this directory: `lenses.md` (evidence lens prompts), `measurements.md` (measurement and tooling snippets).

## Tiers

- **Tier 1** blocks production. Items that are missing capabilities carry the note "go-live requirement". The rest are defects in code that exists.
- **Tier 2** bites soon after launch, or makes the system hard to operate and change.
- **Tier 3** is real and low impact.
- **Small findings** are one line each, listed at the end, never pursued. Structure findings (large files, long functions, duplication, dead code) start here and graduate to a numbered finding only when they correlate with churn or defects, or are the root cause of another theme.

## Evidence levels

- **read**: traced in code or configuration.
- **measured**: run against a real system, with the environment named.
- **inferred**: reasoned from verified parts, not run. Say what would confirm it.

## Effort

Effort describes scope and coordination, with no time estimate. Low is a small change with an obvious fix. Med spans several modules or repos, or needs a design choice, new tests or new infrastructure. High needs a cross-repo design decision or a refactor of a core flow. Mark a rating "(assumed)" when it depends on work in flight whose design is not known yet.

## Rules

- Treat ADRs, comments, READMEs, status documents and existing patterns as claims to test. Check a status document against code or a run before quoting it.
- Every finding cites file and line or a measurement, and states its evidence level.
- Agent reports are candidates. Agreement between agents is a signal, never proof. Verify before presenting.
- No numbers or targets without a source. Capture the source at intake or leave the number out.
- Label how representative each environment is (local, dev, UAT, prod). Do not size production from non-production data without saying so.
- Describe infrastructure the team does not own by its current definition only.
- Do not use credentials found in config files. The user supplies them on purpose.
- Do not run test suites or scripts with side effects in the user's own environment without checking what they touch.
- Ask before any measurement that adds load or could disturb a shared environment.
- Never push. Never include secret values in any output.
- Present one theme and one decision at a time.
- Writing style follows the user's global instructions: no em dashes, no contrast constructions, no verdicts appended to facts.

## Register template

```
# <System> audit

Scope: <repos or services>, reviewed <date> against <branch or environment>.

## How to read this
- Tier definitions, Effort, (assumed), Evidence, and the line: Measurements ran against <environments> and are not production figures.

## Summary
- Counts per tier and 3 to 5 lines on the main themes.

## Tier 1
| # | Finding | Fix direction | Effort | Evidence |

## Tier 2
Grouped by theme, same columns, numbering continues.

## Tier 3
Bullets.

## Tracked gaps
## Small findings
## What is in good shape
## Not examined
## Depends on work in flight
```

Rows are numbered sequentially across tiers. Cross-references use final numbers. The register contains no paths into private working documents.

## Working documents

Kept in the output root chosen at intake: `charter.md` (scope, rules, status and resume section), `pass1/` (raw lens reports and a consolidated candidates file), `verification-log.md` (evidence and method per finding, corrections to agent claims), `register-working.md` (all findings with agreed tiers and open questions), `register.md` (the deliverable).
