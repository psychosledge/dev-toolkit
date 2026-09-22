---
name: sync-global
description: Detect and reconcile drift between this repo (source of truth) and the machine's actual global environment — Claude agent/command/skill files, and coding-environment dotfiles. Claude files get a workloop-impact analysis; dotfiles get a portability and secret-safety check.
argument-hint: "[optional: path to repo root, defaults to current directory]"
---

You are performing a drift audit between this repo's source-of-truth files and what's actually live on the machine. The goal is landing on a new environment, cloning this repo, and running this command to be fully set up — for Claude's own workloop and for general coding environment setup alike. Your job is not just to list differences — you must critically evaluate each one before recommending any action, and the evaluation differs by category (see Step 3).

## Locations

### Claude config

**Global (what Claude actually runs):**
- `~/.claude/CLAUDE.md` — global instructions
- `~/.claude/agents/` — subagent definitions
- `~/.claude/commands/` — slash command skills
- `~/.claude/skills/` — skills (each a subdirectory containing `skill.md`, possibly plus supporting files)

**Repo (source of truth):**
- `coding-agent/CLAUDE.md` — global instructions
- `coding-agent/agents/` — subagent definitions
- `coding-agent/commands/` — slash command skills
- `coding-agent/skills/` — skills (same subdirectory shape as global)

### Dotfiles

Coding-environment setup outside of Claude — shell config, tool config, git identity. Unlike Claude config (discovered by scanning directories), dotfiles are an explicit, declared list of pairs. A file living in `dotfiles/` with no pairing below isn't in scope until a pairing is added here.

| Repo (source of truth) | Live (what the shell/tools actually read) |
|---|---|
| `dotfiles/zprofile` | `~/.zprofile` |
| `dotfiles/zshrc` | `~/.zshrc` |
| `dotfiles/gitconfig` | `~/.gitconfig` |

When adding a new dotfile to this sync, add its pair here first.

**Exclusion — `gitconfig`'s `[user] email`:** never diff or copy this line in either direction. It's per-machine identity, not portable config — the repo template omits it on purpose. If the live `~/.gitconfig` is missing `[user] email` entirely (a genuinely new machine), check the `git-identity-config` project memory for this machine's default; if no memory exists, ask the human and offer to save one. A client-specific repo overriding email via its own local (uncommitted) `user.email` is a separate, already-handled case — don't touch it.

If a repo root was passed as an argument, use that path instead of the current directory.

---

## Step 1: Discovery

**Claude config:** List all `.md` files in the four flat directories (`agents/`, `commands/`, both locations), plus `CLAUDE.md` at the repo and global roots. Build a complete matrix of every unique filename across all locations.

**Skills are a separate shape.** `skills/` holds one subdirectory per skill (`skills/<name>/skill.md`, possibly with supporting files alongside), not flat `.md` files. List subdirectory names in `coding-agent/skills/` and `~/.claude/skills/`, and diff each pair's `skill.md` the same way as an agent/command file. Treat a skill that exists in only one location as **Repo only** / **Global only**, same as any other orphaned file — do not decide whether it "belongs" in the repo (e.g. because it looks project-specific or personal rather than part of the core workloop); surface it and let the human make that call in Step 5. If a skill directory has supporting files beyond `skill.md`, note their presence but diff only `skill.md` unless the human asks to look closer.

**Dotfiles:** Use the declared pairs from the Locations table above — no scanning needed. Also list any file directly inside `dotfiles/` that has no declared pairing, and any file in `dotfiles/` not present at all in the table; surface these to the human in Step 5 as "needs a pairing decision" rather than guessing a home path.

---

## Step 2: Classify Each File

For each filename (or dotfile pair), run `diff` between the global/live version and repo version and classify as:

- **Identical** — no differences (skip in report, note count only)
- **Repo ahead** — repo has changes the global copy doesn't
- **Global ahead** — global has changes the repo copy doesn't
- **Diverged** — both sides have changes relative to each other (non-trivial merge needed)
- **Repo only** — exists in repo but not in global
- **Global only** — exists in global but not in repo

**`gitconfig` exception:** ignore the `[user] email` line before diffing — it's excluded from sync (see Locations above). A diff that's non-empty only on that line is Identical for classification purposes.

**Windows path note:** Use forward-slash paths (e.g., `C:/Users/psych/.claude/...`) in diff commands. Backslash paths in bash cause `\$` to escape the dollar sign, silently breaking variable expansion and producing empty output that looks like "no differences."

**Sanity check:** After completing comparisons, run `ls -la` on each file pair and confirm the sizes match your classification. If sizes differ but you reported "IDENTICAL", the comparison failed — re-run that file's diff individually before proceeding.

---

## Step 3a: Claude Config — Workloop Impact Analysis

This is the critical step for Claude config files. For every non-identical file — including files with no numbered step of their own below — evaluate the diff against the workloop it supports. Be skeptical — question whether each change is genuinely better, genuinely worse, or just different. Nothing in scope is exempt from this step because it isn't one of the core numbered files; every file here supports the workloop, some just more indirectly than others.

**Drift direction alone is not evidence of a mistake.** Global-ahead drift is routinely the expected result of the reactive half of the workflow — editing `~/.claude/` directly while working in another project, then syncing back here later. Report what changed and its workloop impact; don't speculate about how or why the drift happened unless the diff itself introduces a problem.

**The core workloop (direct steps):**
1. `/story` — author a story card in product-centric, PM-legible language; draft and iterate with the human; no planning begins until the human explicitly approves the card
2. `/plan` — planner decomposes the approved story into thin vertical slices with AC and a UAT checklist; writes plan to `docs/stories/<slug>/plan.md`; human approves before any work begins
3. `/slice` — for each slice: architect check (if needed) → coder implements with TDD → verifier runs full review → **human sees full report unconditionally** → human approves → commit
4. `/bug` — characterize → architect check → coder fix with regression test → verifier → human approves → commit
5. `/verify` — standalone verification pass
6. Human gates are **unconditional** — the human always sees complete results before any action is taken, whether passing or failing
7. Agents surface issues to the human; they never compensate silently or loop autonomously

**Everything else in scope supports that core workloop indirectly** rather than being a step in it — don't treat "not one of the 7 above" as "not workloop-relevant":
- `brainstorm` — feeds ideation into `/story` before a card is drafted
- `catchup` — keeps the human's view of remote/team state current, which `/plan` and `/slice` both assume is accurate
- `pr-description` — writes the artifact the human reviews at the commit/PR step of `/slice` and `/bug`
- `daily-recap` / `weekly-recap` / `week-rollover` — turn the workloop's own output (commits, plan docs, session transcripts) into status the human acts on

**For each non-identical file, work through these questions.** Not every question applies to every file — a support skill has no "TDD discipline" to degrade — but answer the ones that do rather than skipping the file because none of the core-workloop language fits literally:

- Does this change strengthen or weaken a human gate, or (for a support file) the accuracy/completeness/trustworthiness of what it hands the human? (Any weakening is a serious concern.)
- Could it cause the orchestrator — or, for a support file, the skill itself — to loop silently, infer, or paper over something before the human sees it?
- Does it improve or degrade TDD discipline (red-green-refactor)? (Coder/verifier/architect only.)
- Does it add clarity or introduce ambiguity about the agent's or skill's responsibilities?
- Is it consistent with what other agents or skills in the team depend on or expect (e.g. a plan.md path or commit format another skill reads)?
- Does it improve the quality bar, or does it lower the bar for shipping — or, for a support file, for the artifact it produces?
- Does it add unnecessary process overhead or complexity?
- If this is a removal, is something important now missing?

Rate the impact: **Positive** / **Neutral** / **Negative** / **Mixed** — and justify the rating in one or two sentences. Don't default to Positive just because a change adds content.

**Check every non-identical or orphaned file for genericity and noise, not just skills.** A skill in `skills/` isn't automatically workloop machinery like an agent or command — it can be anything from a shared, reusable capability to a personal one-off that happens to live in the global namespace, which is why this check exists at all. But two of the three tests below are format-agnostic: a colleague's name or a dated journal entry is exactly as out of place in an agent or command file as in a skill. Run all three tests against every file that's new, changed, or orphaned (Global only / Repo only):

1. **No real third-party names or identifiers, ever — bright line, not a judgment call.** Colleague names, client/customer names, org names, email domains, meeting names, or any other identifier belonging to a specific person or engagement must not appear in a skill file, including as an "illustrative example." These are personal skills meant to travel across many projects and customers — a customer's name has no business sitting in a file that goes to the next one. Genericize the example instead of citing the real instance (`a named stakeholder`, not `Karoliina`; `a colleague's own session`, not `Sarah's session`). This applies even when the real example reads as harmless in isolation — the rule is categorical, not a severity judgment per instance.
2. **Distill the rule, don't preserve the journal.** The test: could a reader reconstruct *when this was discovered, who found it, or what the specific incident was* just from reading the skill file? If yes, that's a transcript, not an instruction. A skill file should state the resulting behavior plainly — what to do, or what not to do — without the "Confirmed miss (date): here's the story" wrapper. Drop dates, drop "Added/Confirmed/Reorganized (YYYY-MM-DD)" tags, drop direct quotes from the human, drop specific hashes/PR numbers/incident blow-by-blows. Keep only what's left once the story is stripped out: is there still an actionable rule? If the story *is* the content — a same-day build log, a change history, a single field-test's list of findings — that content belongs in a project memory (a design/field-testing doc), not the skill file. A skill with zero dated annotations and zero "why we changed this" narrative is the healthy target state, not a sign of a skill that hasn't been field-tested.
3. **Assumed environment**: does the file assume one specific directory layout, calendar, tool connector, or workflow convention exists, without checking first or asking when it doesn't? (Most likely to hit in a skill, but an agent or command can bake in the same assumption.)

Rate this **Genericity** independently of workloop impact — Positive / Neutral / Negative / Mixed — since a file can be workloop-safe (no gate weakened) while still being noisy or overly specific. Don't collapse the two into one verdict. Test 1 (real names) is disqualifying on its own regardless of how the other two tests score — treat any hit as Negative and name the exact instance in the report, don't average it away against otherwise-clean content.

---

## Step 3b: Dotfiles — Portability & Secret Safety

Dotfiles have no "workloop" to protect, so don't force the workloop questions onto them. What they need to protect instead: nothing secret ever gets committed to the repo, and nothing machine-specific gets presented as a universal default. Run both checks on every non-identical or orphaned dotfile pair.

**Secret safety — bright line, not a judgment call.** Scan the diff for anything that looks like a live credential: API keys/tokens (`ghp_`, `gho_`, `sk-`, `AKIA`, similar prefixed tokens), or a `password=`/`secret=`/`token=`-shaped assignment holding something that isn't obviously a placeholder. Any hit is **Blocked** — do not recommend copying that file in either direction. Say exactly what was found (which line, what it looks like) and tell the human to rotate/remove it first. Never silently strip the secret and sync the rest — surface it and stop on that file.

**Portability.** The bar is "would this line help on basically any environment I'd code in," not "is this line correct for the machine I'm on right now." Flag:
- A tool, alias, or PATH entry for something not actually used day-to-day (dead weight carried out of habit rather than active use)
- A hardcoded absolute path, hostname, or identity value (e.g. an email tied to one specific employer/account) that won't hold across every environment this repo gets cloned into
- Logic scoped to one specific project (a per-project hook, a project name in a comment or function name) rather than general-purpose environment setup
- Duplicated lines or PATH entries doing the same thing redundantly

Rate **Portability**: Positive / Neutral / Negative / Mixed, and **Secret Safety**: Safe / Blocked. A Blocked file's recommendation is always "remove the secret before this can sync" regardless of how Portability scores.

---

## Step 4: Reconciliation Report

Present findings using this structure for each non-identical or orphaned file. Use the Claude-config fields (Workloop impact / Genericity) for agents, commands, skills, and CLAUDE.md; use the dotfile fields (Portability / Secret Safety) for anything in the dotfiles table.

---
### `[filename]` — [Repo ahead / Global ahead / Diverged / Repo only / Global only]

**What changed:** [Plain-English summary of the diff — what was added, removed, or modified]

**Claude config file — Workloop impact:** [Positive / Neutral / Negative / Mixed]
[One or two sentences of critical analysis. Name the specific workloop principle affected.]

**Claude config file — Genericity:** [Positive / Neutral / Negative / Mixed]
[One or two sentences — hardcoded specifics, process noise, or assumed environment, if any.]

**Dotfile — Portability:** [Positive / Neutral / Negative / Mixed]
[One or two sentences — dead-weight tooling, hardcoded identity/paths, project-specific logic, or redundancy, if any.]

**Dotfile — Secret Safety:** [Safe / Blocked]
[If Blocked: exactly what was found and where.]

**Recommendation:** [Copy repo → global / Copy global → repo / Manual merge needed / No action / Remove secret before sync — with brief rationale. For Negative genericity or portability, the recommendation may be "extract config before syncing" rather than a straight copy.]

---

After all files, present a summary table:

| File | Direction | Impact/Portability | Genericity/Secret Safety | Recommendation |
|------|-----------|---------------------|---------------------------|-----------------|
| ... | ... | ... | ... | ... |

Also report the count of identical files skipped.

---

## Step 5: Human Approval Gate

**Do not copy, write, or modify any files.** Present the full report and ask:

> "Review the reconciliation above. Tell me which files to sync — you can say 'approve all', name specific files, or override any recommendation. I will not touch any files until you give explicit approval."

---

## Step 6: Execute Approved Changes

For each approved action:

1. **Copy repo → global**: copy the repo file to the global location, overwriting the global version
   - For `CLAUDE.md`: `coding-agent/CLAUDE.md` → `~/.claude/CLAUDE.md`
   - For agents/commands: `coding-agent/<dir>/<file>` → `~/.claude/<dir>/<file>`
   - For skills: `coding-agent/skills/<name>/` → `~/.claude/skills/<name>/` (whole directory)
   - For dotfiles: `dotfiles/<file>` → the paired live path from the Locations table
2. **Copy global → repo**: copy the global file to the repo location, overwriting the repo version
   - For `CLAUDE.md`: `~/.claude/CLAUDE.md` → `coding-agent/CLAUDE.md`
   - For agents/commands: `~/.claude/<dir>/<file>` → `coding-agent/<dir>/<file>`
   - For skills: `~/.claude/skills/<name>/` → `coding-agent/skills/<name>/` (whole directory)
   - For dotfiles: the paired live path → `dotfiles/<file>`
3. **Manual merge**: show both versions side-by-side, work through the merge interactively with the human before writing anything
4. Confirm each write with the exact source → destination path
5. Never execute a "Remove secret before sync" item automatically — that always requires the human to rotate/remove the secret and confirm before any copy happens.

After all copies are complete, re-run `diff` on every changed pair to confirm no remaining drift on the synced files.

Dotfile copies to `~/.zshrc` or `~/.zprofile` don't take effect in already-open shells — mention that a new terminal (or `source`) is needed, but don't run it yourself.
