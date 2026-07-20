#!/usr/bin/env python3
"""Stop hook: the agent may not declare completion while verification fails.

Runs scripts/verify.sh. Non-zero exit -> block the stop (exit 2) so the agent
keeps working. Uses stop_hook_active to avoid infinite loops.
"""
import json
import os
import subprocess
import sys

TIMEOUT_SECONDS = 240


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    # Prevent a blocked stop from re-triggering this hook forever.
    if payload.get("stop_hook_active"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    verify = os.path.join(project_dir, "scripts", "verify.sh")
    if not os.path.exists(verify):
        return 0

    try:
        result = subprocess.run(
            ["bash", verify], cwd=project_dir, capture_output=True,
            text=True, timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print("verify.sh timed out; fix or speed up verification.", file=sys.stderr)
        return 2

    if result.returncode != 0:
        tail = (result.stdout + result.stderr).strip().splitlines()[-20:]
        print("verify.sh failed — work is not done:\n" + "\n".join(tail), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
