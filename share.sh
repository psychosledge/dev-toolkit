#!/usr/bin/env bash
# Export tracked files only (no local/untracked state) to a zip for sharing
# outside this machine, e.g. handing the toolkit to a coworker via Drive.
set -euo pipefail

OUT="${1:-$HOME/Desktop/dev-toolkit-share.zip}"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

cd "$(dirname "$0")"
git ls-files -z | tar --null -T - -cf - | tar -xf - -C "$STAGE"

rm -f "$OUT"
(cd "$STAGE" && zip -rq "$OUT" .)

echo "Wrote $OUT"
