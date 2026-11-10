#!/usr/bin/env python3
"""Wait until a GitHub pull request or GitLab merge request needs its agent, then print why and exit.

Run inside the repo: watch-merge-request.py <github|gitlab> <number> [seconds between checks, default 60]
Prints one of: conflict, merged, closed.
"""

import json
import subprocess
import sys
import time


def github_reason(pull_request: dict) -> str | None:
    if pull_request["state"] in ("MERGED", "CLOSED"):
        return pull_request["state"].lower()
    if pull_request["mergeable"] == "CONFLICTING":
        return "conflict"
    return None


def gitlab_reason(merge_request: dict) -> str | None:
    if merge_request["state"] in ("merged", "closed"):
        return merge_request["state"]
    if merge_request["has_conflicts"] or merge_request["detailed_merge_status"] == "conflict":
        return "conflict"
    return None


TRACKERS = {
    "github": (lambda number: ["gh", "pr", "view", number, "--json", "state,mergeable"], github_reason),
    "gitlab": (lambda number: ["glab", "api", f"projects/:id/merge_requests/{number}"], gitlab_reason),
}


def main() -> None:
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in TRACKERS:
        sys.exit(__doc__)
    command, reason_of = TRACKERS[sys.argv[1]]
    number = sys.argv[2]
    pause = float(sys.argv[3]) if len(sys.argv) == 4 else 60.0
    while True:
        answer = subprocess.run(command(number), check=True, capture_output=True, text=True)
        if reason := reason_of(json.loads(answer.stdout)):
            print(reason)
            return
        time.sleep(pause)


if __name__ == "__main__":
    main()
