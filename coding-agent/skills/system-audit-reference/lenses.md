# Evidence lenses

Each lens runs as one read-only subagent. Group small lenses into one agent when the system is small. Select lenses from the preflight. Skip a lens whose trigger is absent.

## Shared brief (put at the top of every agent prompt)

- Goal: find things that block production go-live or bite soon after. State the audience and what "ready" means here, as given at intake.
- Read the charter at `<output root>/charter.md`. Its rules bind you.
- Treat ADRs, comments, docs and patterns as claims to test.
- Do not read or cite the files listed as excluded at intake.
- Read-only on the repositories: no edits, no git writes. Read-only commands are fine. Do not call production. Do not print or copy secret values.
- Every finding cites file and line and states how verified: `read`, `run` or `inferred`. For inferred, say what would confirm it.
- Do not pad. Skip nits. Small real things go in a short separate list.
- Do not include the lead's hypotheses, targets or suspicions in your reasoning. You were not given any.
- Plain, terse sentences. No em dashes.
- Output: write to `<output root>/pass1/NN-<lens>.md` and return a short summary. File format: ranked candidates (at most 15), each with ID, title, tier guess, repos, evidence list, claim in 2 to 3 sentences, concrete failure scenario, how verified, confidence, what would disprove it. Then small findings, then a "Did not examine" list.

## L1 Contracts, duplication, abstraction boundaries
Trigger: more than one service or module boundary.
Look for: drift between hand-copied shapes across services, unvalidated boundaries, casts instead of validation, vendor or provider details leaking past wrappers, abstractions that exist but are not used (unused interfaces, unused injection tokens, consumers bound to concrete classes), the same rule implemented in several places and whether the copies agree, normalization repeated at call sites.

## L2 Variant divergence
Trigger: the system handles two or more variants of one concept (providers, platforms, tenants, regions, user types).
Inventory every place the variants are handled differently, mark each justified or accidental, and look for behavior that silently differs for one variant, one variant failing and degrading the other, and variants with tests for only one.

## L3 Failure modes, auth, configuration
Trigger: always.
Look for: outbound calls without timeouts, retries, cancellation or concurrency bounds, partial failure handling, errors swallowed into empty results, what the user sees on failure, authentication and authorization gaps (unguarded routes, tier or tenant gates that are missing), session lifetime and revocation, credentials copied into tokens, logs, traces or browser code, input validation at the boundary, CORS and rate limiting, configuration validation at startup, unsafe defaults, drift between local and deployed configuration.

## L4 Performance and cost under load
Trigger: any user-facing latency or any metered dependency.
Break one request into stages and measure each. Look for serial awaits that could overlap, unbounded fan-out, N+1 calls, missing caches, payload size, pagination, compression, event-loop or thread blocking, connection pooling, per-request metered calls (LLM, third-party APIs). State what a load test would need to show. Name the environment and its representativeness on every number.

## L5 Untested behavior
Trigger: always.
Rank the riskiest behavior by the consequence of silent failure. For each, find the test and judge what it asserts and whether it would fail if the behavior broke. Look for tests that mock the unit under test, assert only fixtures, cover only the happy path, or exist for one variant. Check which tests boot the real module graph. Run the suites and report results and skips. Check what CI gates on and whether deploys depend on CI.

## L6 Observability, deploy, operability
Trigger: always.
Look for: structured logs, correlation IDs across services, error reporting, metrics, alarms and notification targets, what the health checks actually prove, whether liveness and dependency checks are mixed, deploy gates and approvals, rollback path, migrations, single points of failure, backups, graceful shutdown, runbooks, anything the remaining team could not work out without the people leaving. Mark anything owned outside the team and describe it by its current definition only.

## L7 LLM and agent behavior
Trigger: any call to a language model.
Look for: model and temperature in effect (read the deployed values, not defaults), nondeterminism that changes user-visible results (repeat the same input), structured output versus free text, malformed output handling, prompt injection exposure and the blast radius (tools, credentials), cost and quota per request, prompt caching, timeouts and retries on the model call, blocking calls inside async code, fallbacks when the model is unavailable, evals (what they cover, frozen data, thresholds, repetitions, whether anything gates a change), traces that capture sensitive data.

## L8 Structure and change cost
Trigger: always. Measure with tools first, then read only the top results. See `measurements.md` for commands.
Report the largest files and functions, highest complexity, duplication, dependency cycles, dead code and unused exports, and git churn multiplied by size to find hotspots. Judge each hotspot by what it costs to change (responsibilities mixed in one unit, twin code paths, shotgun edits). List the top ten at most. These are small findings by default. Promote one to a numbered finding when it is a hotspot by churn or defect history, or when it is the root cause of another finding, and say which.

## L9 Dependencies and supply chain
Trigger: any package manifest, lockfile or container image.
Run the available audit tools (see `measurements.md`). Look for known vulnerabilities, long-unmaintained or heavily outdated packages, unpinned or floating dependencies, git or private dependencies fetched at build time without a pinned revision, missing or ignored lockfiles, base images and the user the container runs as, and secrets present in the repository or its history.

## L10 Data and privacy
Trigger: any database, object store, log pipeline or trace store.
Look for: schema and index fit for the query patterns, migration safety, backup and restore (and whether restore has been exercised), retention, personal or sensitive data in logs, traces, caches, URLs and analytics events, data shared across tenants, deletion paths.

## L11 Frontend quality
Trigger: a user interface.
Look for: loading, empty and error states for every remote call, behavior on stream or request failure (spinners that never clear), accessibility basics (labels, focus, contrast, keyboard use), bundle size and first-load cost, rendering cost for large result sets, browser support, state that survives navigation incorrectly.

## L12 Concurrency, idempotency, time
Trigger: always, light touch.
Look for: operations that are unsafe to retry, race conditions between requests for the same user or record, time zone and date boundary handling, values computed once at startup that should be per request, shared mutable state.

## L14 Event sourcing and replication
Trigger: an append-only event log, event store or multi-replica sync (offline-first clients, several devices, several writers).
Look for: event ordering and causality across replicas (clocks, sequence numbers, tie-breaks), idempotent append and dedupe by event ID, sync cursors or watermarks that can skip or repeat events, partial upload or download that leaves a replica believing it is current, whether a "synced" or "up to date" indicator reflects actual convergence, snapshot and event-log consistency (snapshot taken at one cursor and restored against another, snapshot versioning and invalidation), projection determinism (same events in any arrival order give the same state, dependence on wall clock or local state during replay), handlers that read projections to validate and so behave differently per replica, event schema versioning and upcasting, events that are mutated, deleted or rewritten, conflicting concurrent commands and how they resolve, and how a diverged replica is detected and repaired.

## L13 Documentation and handoff
Trigger: the team or ownership will change, or the audience asks about operability.
Look for: a runbook, onboarding steps that work from a clean checkout, who operates the system after the review, undocumented manual steps, knowledge that exists only in people's heads or private channels.
