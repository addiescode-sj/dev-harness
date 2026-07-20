#!/usr/bin/env bash
# Project verification entry point. The Stop hook runs this before the agent
# may declare completion. Add your project's checks below; keep it fast.
set -euo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}"

# --- Add project checks here, e.g.: ---
# npm test --silent
# python3 -m pytest -q
# npm run lint

echo "verify: OK (no project checks configured yet)"
exit 0
