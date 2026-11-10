---
name: run-<app>
description: "Starts, uses and stops <app> on this machine, writing only to its sandbox. Use to run the app, show a change working, or capture a screenshot or output as evidence."
---

# Run <app>

Every run writes to the sandbox below and nowhere else.

## Needs

<!-- Tools and versions, services to start, logins. Name the env file by path, never its values. From a worktree, load it from the main checkout, which `git worktree list` prints first. -->

## Sandbox

| Output | Env var | Sandbox value |
|---|---|---|
| <!-- local files --> | `<APP>__OUTPUT_PATH` | `.sandbox/<run>/` |
| <!-- object storage --> | `<APP>__STORE_URL` | `s3://<dev-bucket>/sandbox/<run>/` |
| <!-- database --> | `<APP>__DATABASE_URL` | <!-- a dev or throwaway database --> |

`<run>` is the branch and short commit, so two worktrees never share a folder.

**Off limits:** <!-- each place no env var can redirect: the production bucket, the live tracker, outgoing email. Agent runs never trigger these. -->

## Start

```sh
# From a fresh shell in any worktree. The port comes from an env var, so two copies run side by side.
```

Ready when: <!-- the log line, or the URL that answers -->

## Use

<!-- How a person uses it, as commands: the URLs to open; the CLI on a small real input from the repo; the pipeline on one small slice (one town, one day). -->

## Capture

```sh
<command> 2>&1 | tee "$OUT/<step>.txt"
npx playwright screenshot --viewport-size=1280,800 "<url>" "$OUT/<page>.png"
```

## Stop

<!-- How to stop it, and how to empty the sandbox. -->
