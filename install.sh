#!/usr/bin/env bash
# Coder dotfiles entry point: maps this repo onto a fresh workspace's $HOME.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$HOME/.claude"
cp -f "$REPO_DIR/coding-agent/CLAUDE.md" "$HOME/.claude/CLAUDE.md"

for dir in agents commands skills; do
  mkdir -p "$HOME/.claude/$dir"
  cp -rf "$REPO_DIR/coding-agent/$dir/." "$HOME/.claude/$dir/"
done

find "$HOME/.claude" -name '.gitkeep' -delete
find "$HOME/.claude" -name '.DS_Store' -delete

cp -f "$REPO_DIR/dotfiles/zshrc" "$HOME/.zshrc"
cp -f "$REPO_DIR/dotfiles/zprofile" "$HOME/.zprofile"
cp -f "$REPO_DIR/dotfiles/gitconfig" "$HOME/.gitconfig"

echo "dev-toolkit: installed Claude agent files and shell dotfiles into $HOME"
