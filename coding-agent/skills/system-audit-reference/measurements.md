# Measurements and tooling

Prefer a short measurement to a long argument. Read-only unless stated. Run in a scratch directory under the job tmp directory. Treat downloaded files as untrusted: put them in a new empty directory, pass paths as arguments, run Python with `-I`. Never print tokens, cookies or passwords. Delete scratch files after use. State the environment on every result.

## Safety checks before running anything

- Before running a test suite, search it for destructive calls (`deleteMany`, `DROP`, `TRUNCATE`, `rm`) and find which database or service it points at. If it can touch the user's own data, ask first.
- Before any measurement that adds load or concurrency, ask. Check whether the user is on a call or the environment is shared.
- Confirm credentials and network access work before starting. If a key is expired or a VPN is off, stop and tell the user.

## Structure and change cost (L8)

- Largest files: `git ls-files | xargs wc -l | sort -rn | head -25`, excluding generated and data files.
- Churn: `git log --since=6.months --name-only --format= | sort | uniq -c | sort -rn | head -25`. Hotspots are files high in both churn and size.
- Function length and complexity: use what is installed. TypeScript and JavaScript: `eslint` with `complexity` and `max-lines-per-function`. Python: `ruff check --select C901,PLR0915` or `radon cc -s`. Report the top results only.
- Duplication: `jscpd` if available.
- Cycles: `madge --circular` or `dependency-cruiser`.
- Dead code and unused exports: `knip`, `ts-prune`, `vulture`.
- Do not report every large function. Report the top ten and judge them.
- Dead code and cycles with an approved scratch install (registry download, ask first): install `knip`, `madge` and, for Python, `vulture` (with `uv venv` and `uv pip install`) in a scratch directory, never in the repo. Run from the repo directory with a scratch config file and `--reporter json` for knip. List the real entry points in the config (main file, test files, framework config files, graph factories named in config such as `langgraph.json`), and ignore generated files.
- Validate the setup against findings you already have by hand (for example unused injection tokens). If the tool does not rediscover them, the entry-point configuration is wrong.
- Expect false positives: ambient `.d.ts` files, decorator and dependency-injection wiring, framework-registered functions, Pydantic and state fields, callback methods, config packages and CLIs listed as dependencies. Verify each item by searching for callers before listing it. Most unused exports and types are noise.
- `madge --circular --extensions ts` also follows `.vue` imports and dynamic `import()` calls. Group cycles by their common edge, since one coupling can produce dozens of cycles. For Python, a small AST import graph with a strongly-connected-components pass is enough.

## Route inventory (L3 and L8)

- Parse controller or router decorators into a table of method, path, guards and file. Decorator order varies between files (a guard can sit before or after the controller decorator), so check the parser against two controllers by reading them. A parser that reports a guard as missing is a false alarm until read.
- Search every plausible caller for each route's static path with word-boundary patterns: front end source, tests, end-to-end specs, other services, sibling repositories and every remote branch. Common-word routes over-match, so recheck them with exact strings.
- A route with no caller anywhere is a candidate for removal. Note when it is guarded and recent, since it may precede work in flight. An unguarded route with no caller is attack surface with no benefit.

## Dependencies and supply chain (L9)

- `npm audit --omit=dev`, `pnpm audit`, `pip-audit` or `uv pip audit`, `osv-scanner`, whichever exists. Report counts by severity and the few that are reachable.
- Floating or unpinned dependencies: manifests with `*`, `latest` or branch references. Build scripts that clone or install from a branch head.
- Secrets: `gitleaks detect --redact` or `trufflehog` if installed. Report location and type only.
- Containers: base image, `USER` instruction, packages installed at build time.

## Performance (L4)

- Stage timing: use the service's own timing logs or debug header. Run each scenario a few times and report ranges.
- Call counting: count outbound calls per request from the service log.
- Payload: response size and the `Content-Encoding` header.
- Event loop blocking: poll a cheap endpoint of the same process every 200 ms while one slow request runs. A stall as long as the request proves blocking.
- Concurrency: send two or three identical requests at once and compare each stage to the serial run. Ask first.

## Robustness probes (L3)

- Malformed input: send an empty body, wrong types and an oversized field to each core route. Expect 400, record 500s and whether the request reached a downstream service.
- Failure injection by configuration only when the user allows it.

## Nondeterminism (L7)

- Send the same input to a model-backed route five times. Compare the extracted structure and the result counts. Try a plain input and an ambiguous one.

## Currency check

- Before the final register, list commits that reached the main branch since the analysis started and re-check line citations.
