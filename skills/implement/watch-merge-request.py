#!/usr/bin/env python3
"""Wait until a GitLab merge request needs its agent, then print why and exit.

Run inside the repo: watch-merge-request.py <iid> [seconds between checks, default 60]
Prints one of: conflict, merged, closed.
"""

import json
import subprocess
import sys
import time


def needs_agent(merge_request: dict) -> str | None:
    if merge_request["state"] in ("merged", "closed"):
        return merge_request["state"]
    if merge_request["has_conflicts"] or merge_request["detailed_merge_status"] == "conflict":
        return "conflict"
    return None


def fetch(iid: str) -> dict:
    answer = subprocess.run(
        ["glab", "api", f"projects/:id/merge_requests/{iid}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(answer.stdout)


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    iid = sys.argv[1]
    pause = float(sys.argv[2]) if len(sys.argv) == 3 else 60.0
    while (reason := needs_agent(fetch(iid))) is None:
        time.sleep(pause)
    print(reason)


if __name__ == "__main__":
    main()
