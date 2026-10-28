---
name: shipping
description: "Playbook for landing finished work: clean commits, a PR body with evidence, push. Use when the user says ship it, open a PR, commit and push, or at the end of a code playbook once review passed."
---

# Shipping

**You own what lands.** Ship only what a review verdict covers.

1. **Check the verdict.** *Done when:* a **review** verdict of `PASS` or `PASS+NOTES` covers the current head SHA. If the head moved since, rerun review.
2. **Shape the commits** (**principle-sequence-verifiable-units**). Small, ordered, each green on its own. Subject in the imperative; the body says why, not what. *Done when:* `git log` reads as the story of the change.
3. **Write the PR body.** Call the Skill tool with "pr". *Done when:* the body has before/after evidence and states its blast radius.
4. **Push and open the PR.** Use `gh`. Ask before force-pushing a shared branch or merging. *Done when:* you've read the PR back with `gh pr view` and it shows the right base and head.

**Reply:** the PR URL, the verdict it carries, and anything left for the user to decide.
