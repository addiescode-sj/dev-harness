#!/usr/bin/env bash
# SessionStart hook: inject current state so a new session resumes from files,
# not from previous conversation history.
set -euo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}"

if [ -f docs/current-state.md ]; then
  echo "=== docs/current-state.md ==="
  cat docs/current-state.md
fi

# List plans that still have unchecked tasks
for t in docs/plans/*/TASKS.md; do
  [ -f "$t" ] || continue
  if grep -q '^- \[ \]' "$t"; then
    echo "OPEN PLAN: $t ($(grep -c '^- \[ \]' "$t") tasks remaining)"
  fi
done

exit 0
