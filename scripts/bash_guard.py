#!/usr/bin/env python3
"""PreToolUse hook for Bash: block clearly destructive commands.

Exit 0 = allow, exit 2 = block (stderr goes back to the agent).
This is a guardrail, not a security boundary.
"""
import json
import re
import sys

BLOCKED = [
    (r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\s+/(\s|$)", "recursive delete of /"),
    (r"git\s+push\s+.*--force(\s|$|-)", "force push"),
    (r"git\s+reset\s+--hard\s+origin", "hard reset to remote"),
    (r"(curl|wget)\s+[^|;]*\|\s*(ba)?sh", "pipe remote script to shell"),
    (r"git\s+clean\s+-[a-zA-Z]*f", "git clean -f"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    command = payload.get("tool_input", {}).get("command", "")
    for pattern, reason in BLOCKED:
        if re.search(pattern, command):
            print(f"Blocked by harness policy: {reason}. "
                  f"If truly needed, ask the user to run it manually.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
