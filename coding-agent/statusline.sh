#!/bin/bash
# Claude Code two-line status line. Reads the status JSON on stdin. Requires jq.
#
#   Opus 5  ━━━━━━╌╌╌╌╌╌╌╌╌ 42% (84k) $1.23 ~ 12%
#   dev-toolkit  feat/exports  (worktree: audit)
#
# Line 1: model, context window bar and percent, context tokens, session cost,
# seven-day rate-limit usage. Line 2: directory, branch, active worktree.

input=$(cat)

# One field per line: bash 3.2's `read` collapses empty tab-separated fields,
# which would shift every later value. Newlines are stripped for the same reason.
{
  read -r MODEL
  read -r DIR
  read -r PCT
  read -r TOKENS
  read -r COST
  read -r SEVEN_DAY
  read -r WORKTREE_PATH
} < <(
  printf '%s' "$input" | jq -r '
    def clean: tostring | gsub("[\r\n]"; " ");
    ((.model.display_name  // "?") | clean),
    ((.workspace.current_dir // .cwd // "") | clean),
    ((.context_window.used_percentage // 0) | floor),
    ( (.context_window.current_usage.input_tokens // 0)
    + (.context_window.current_usage.cache_creation_input_tokens // 0)
    + (.context_window.current_usage.cache_read_input_tokens // 0) ),
    (.cost.total_cost_usd // 0),
    ((.rate_limits.seven_day.used_percentage // -1) | floor),
    ((.worktree.path // "") | clean)
  ' 2>/dev/null | tr -d '\r'
)

MODEL=${MODEL:-?}
PCT=${PCT:-0}
TOKENS=${TOKENS:-0}
COST=${COST:-0}
SEVEN_DAY=${SEVEN_DAY:--1}

MODEL="${MODEL% (1M context)}"

DIM='\033[2m'
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
MAGENTA='\033[35m'
RESET='\033[0m'

[ "$PCT" -lt 0 ] && PCT=0
[ "$PCT" -gt 100 ] && PCT=100

if   [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
else                        BAR_COLOR="$GREEN"; fi

BAR_WIDTH=15
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /━}"
[ "$EMPTY"  -gt 0 ] && printf -v PAD  "%${EMPTY}s"  && BAR="${BAR}${PAD// /╌}"

TOKEN_STR="$((TOKENS / 1000))k"
COST_FMT=$(printf '$%.2f' "$COST")
DIR_NAME="${DIR##*/}"

# Omitted when the payload has no rate-limit data, so "unreported" never reads as 0%.
SEVEN_DAY_STR=""
if [ "$SEVEN_DAY" -ge 0 ]; then
    if   [ "$SEVEN_DAY" -ge 80 ]; then USAGE_COLOR="$RED"
    elif [ "$SEVEN_DAY" -ge 60 ]; then USAGE_COLOR="$YELLOW"
    else                               USAGE_COLOR="$GREEN"; fi
    SEVEN_DAY_STR=" ${USAGE_COLOR}~ ${SEVEN_DAY}%${RESET}"
fi

echo -e "${MAGENTA}${MODEL}${RESET} ${BAR_COLOR}${BAR}${RESET} ${PCT}% ${DIM}(${TOKEN_STR})${RESET} ${DIM}${COST_FMT}${RESET}${SEVEN_DAY_STR}"

LINE2="${DIM}${DIR_NAME}${RESET}"

BRANCH=$(git -C "$DIR" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ "$BRANCH" = "HEAD" ]; then
    BRANCH=$(git -C "$DIR" rev-parse --short HEAD 2>/dev/null)
    [ -n "$BRANCH" ] && BRANCH="detached@${BRANCH}"
fi
[ -n "$BRANCH" ] && LINE2="${LINE2} ${CYAN}${BRANCH}${RESET}"

if [ -n "$WORKTREE_PATH" ]; then
    LINE2="${LINE2} ${DIM}(worktree: ${WORKTREE_PATH##*/})${RESET}"
fi

echo -e "$LINE2"
