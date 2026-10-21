---
name: system-audit
description: Collaborative audit of one or more repos as a single system, for handing off to a remaining team or getting oriented on a new project. Finds what blocks production or bites soon after, verifies every claim, and produces a ranked register with tier, fix direction, effort and evidence. Run only when explicitly called.
argument-hint: "[scope: repo paths or service names | resume]"
disable-model-invocation: true
---

Run a system audit with the human. This command is invoked only by the human. It is collaborative: expect many rounds, one theme and one decision at a time.

Before starting, read `~/.claude/skills/system-audit-reference/SKILL.md` (rubrics, rules, register template). Read `lenses.md` and `measurements.md` in that directory when the steps below point to them.

## Resume

If `$ARGUMENTS` is `resume`, or a charter already exists in the output root, read `charter.md`, report the status and the next step in two sentences, and continue from there. Skip the steps already done.

Compare the lenses listed in the charter with the lenses in `lenses.md`. If the library has lenses the charter does not list, offer a supplementary pass for only those: re-run the preflight for the current state of the repos, run pass 1 for the added lenses, then continue through consolidation and the walkthrough. Number new findings after the existing ones, assign them to tiers with the human, and merge them into the register with renumbering and cross-references updated. Record the supplementary pass in the charter.

## Step 1: Intake

Look for the `system-audit-config` project memory first. If found, use its fields without asking again. If missing, ask for the fields below one at a time, then offer to save them as that memory. Fields:

- **Scope**: repos or services reviewed as one system (default from `$ARGUMENTS`).
- **Audience and use**: who reads the result and what decision it informs.
- **Meaning of ready**: what "ready" means to the audience, in their words. Record any target the human states with its source. If there is no source, say so and keep the target out of every output.
- **Environments**: each environment that can be used (local, dev, UAT, prod), how to reach it, whether read-only, and how representative it is of production.
- **Output root**: where working documents go. Default to the human's private documentation location. Nothing goes into a repo, PR or ticket unless the human shares it.
- **Excluded files and sources**: documents or trackers not to read during analysis, and branches or PRs to ignore.
- **Ownership boundaries**: anything outside the team's control (shared infrastructure, other teams' services) and anything still being built.
- **In-flight work**: known open work, owners and expected timing.

Do not ask for anything that can be read from the repos or memory. If an answer is vague, ask one specific follow-up.

## Step 2: Preflight

Without changing anything:

1. Detect the stack for each repo: languages, frameworks, package managers, CI and deploy files, infrastructure repos, test commands, how to run locally.
2. Select lenses from `lenses.md` using their triggers. Tell the human which lenses will run and which were skipped and why.
3. Check that the environments work: credentials present and valid, network reachable, local stack running. If something is broken, stop and ask the human to fix it. Do not work around it.
4. Check the test suites for side effects before running any of them (see `measurements.md`).
5. Check each repo against its remote and report any that are behind. Do not pull without the human's approval.
6. List open PRs, recent branches and recent merges for each repo.

## Step 3: Charter

Write `charter.md` in the output root: scope, audience, meaning of ready, environments with representativeness, ownership boundaries, excluded sources, the rules from the reference, the selected lenses, and a status and resume section. Save it before continuing.

## Step 4: Pass 1, evidence

State the number of agents and a rough token estimate (about 150k to 250k per lens agent for a three-repo system) and ask for confirmation before launching.

Launch one read-only `general-purpose` agent per lens group in a single message, in parallel. Each prompt is the shared brief from `lenses.md` plus that lens, with the paths and the output file name. Do not include your own hypotheses, targets or suspicions in any prompt.

When agents report, treat the reports as unverified candidates. Narrate each arrival in two or three sentences and say that nothing is confirmed yet.

## Step 5: Consolidate

Group the candidates into themes. Merge duplicates, note agreement across agents and note disagreements in tier or claim. Write `pass1/00-consolidated-candidates.md` with a "verify first" table of concrete, cheap-to-check claims. Order themes for the walkthrough: verification items first, then tier 1 themes, then the rest.

## Step 6: Pass 2, verify and walk through

Work one theme at a time. For each:

1. Verify the central claims yourself in the code, and measure where a short measurement is decisive (`measurements.md`). Check the agents' specific citations. Expect corrections and say so plainly.
2. Present: what holds, what was wrong in the agent reports, what you could not verify, and a proposed tier with its reason.
3. Ask for one decision, usually agreement on the tiers. Record the human's answer verbatim in substance.
4. Append evidence, method and corrections to `verification-log.md` and update `register-working.md` before moving on.

Rules for the walkthrough:

- Never present an agent claim as a finding before verifying it.
- If the human's question exposes a mistake, correct the record in every document and say what was withdrawn.
- If an environment fails (expired key, network, data), say so and ask the human to fix it. Pause the dependent checks.
- Ask before measurements that add load or touch shared systems. Put scratch data in a fresh directory and delete it afterward.
- Group findings by root cause when several share one boundary, and say which one is the root.
- Mark a rating "(assumed)" when it depends on unknown work in flight.

## Step 7: Pass 3, in-flight overlap

Map each finding to open PRs, branches and recent merges. Ask the human about work not visible in the repos, one question at a time. Record findings that need re-verification after a pending change lands. Record the dependency in the working register. Do not put overlap tags in the deliverable. Use the "Depends on work in flight" section instead.

## Step 8: Register

Before drafting, list commits that reached the main branch since the analysis began and re-check line citations.

Draft `register.md` from the template in the reference. Check it before showing it: sequential numbering, tier counts that match the summary, consistent columns, no unsourced targets, no time estimates, no paths into private documents, no em dashes.

Show it to the human and take changes one item at a time. Keep working documents consistent with each change.

## Step 9: Close out

Update the charter status, the working register and project memory with where things stand and what needs re-verifying later. If a `tracking-config` project memory exists, update the tracker and activity log per the `tracking` and `activity-log` skills. If it does not exist, skip that silently.

Then follow the session hygiene rule: confirm the tracker and log are current, and suggest starting a new session.

## Never

- Never push, and never include secret values in any output.
- Never use credentials found in config or environment files without the human's say-so.
- Never run anything against production.
- Never read excluded files, and never change the repositories under review.
- Never ask several questions at once.
- If a lens or this command behaves badly, tell the human which file needs improving and what the change would be. Do not compensate silently.
