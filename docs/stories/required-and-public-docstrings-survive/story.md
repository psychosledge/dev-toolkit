# Required and public docstrings survive comment review
Tier: core

## Summary

When this story is done, a developer whose change adds a docstring that the work requires, or one that documents a public function, has it judged on whether it is accurate and likely to stay accurate.

## Background

The toolkit's comment rules remove any comment that only repeats what the code says. A docstring on a public function often does exactly that, and it still serves readers who see it through help pages and editor hovers without ever opening the code. When a story requires such a docstring, the rule and the requirement point in opposite directions. Today the reviewer settles that on its own judgment, so one run may keep the docstring and the next may mark it for removal.

## What needs to happen

- The comment rules say how to judge a docstring that the work requires or that documents a public function.
- Review keeps such a docstring when it is accurate, and flags it when it is wrong or likely to drift from the code.
- Every other comment is judged by the existing rules.

## Notes

- Gap is in coding-agent/skills/comment-quality/SKILL.md, "The bar" section and its always-flag list. The skill has no rule mentioning docstrings or public API.
- Incident: a verifier run on a fixture where an AC required a docstring on order_total. The verifier noted the restates-the-code rule would mark it Remove — weak and kept it by overriding the rule.
- Behavior-shaping, so skill-testing applies. That incident is the baseline scenario.
- Work right after testing-safeguards-on-every-repo, before executable-contract-per-component.

## Acceptance criteria

- A docstring the work requires, which is accurate, is kept in review with no removal suggested.
- A docstring on a public function, which is accurate, is kept in review even when it repeats what the code says.
- A required or public docstring that is wrong, or that repeats values likely to change, is flagged with the reason.
- A comment inside a function that only repeats the code is still flagged for removal.
