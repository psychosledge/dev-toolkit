# Retire the ledger Contract format
Tier: core

## Summary

When this story is done, a developer on a repo still using the old Contract list is told the format is retired and offered a conversion, and the toolkit supports a single Contract format.

## Background

The old list format stays available while one client project finishes, around 2026-12-02. After that, keeping both formats means every agent carries two sets of Contract instructions. A repo still on the old setting must never be switched to the new rules silently, because its file doesn't match them.

## What needs to happen

- Remove the old format's instructions.
- A repo still on the old setting gets a notice and an offer to convert its list into per-component contract tests.

## Notes

- Start after the client project on `Enabled: yes` ends.
- This removes `ledger.md`, the routing lines and the `yes` value.
- In the conversion, rows marked `met` become contract tests in the component they belong to, and `unenforced` rows become pending tests.
- Depends on Executable Contract per component.

## Acceptance criteria

- A developer working in a repo still on the old setting is told the format is retired and offered a conversion before any Contract step runs.
- That repo is treated as the new format only after the developer accepts the conversion.
- A repo already on the new format sees no change.
