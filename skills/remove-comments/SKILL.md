---
name: remove-comments
description: "Deletes the comments in a diff with a fresh reviewer subagent, keeping only a short list of exceptions (license headers, constraints we can't change, docstrings on public functions and APIs), flags the code each deleted comment was propping up, then fixes that code and offers to encode claimed constraints as a type, test or lint. Use before review, when implement or implement-spec finish their build, or when review-code flags comments."
---

# Remove Comments

The code says what it does; a comment that has to explain our own code marks a name, a type or a shape to fix. This pass deletes comments and turns what they were covering for into fixes.

## Scope

The files or diff the caller passes. Otherwise the current diff against the default branch, working tree included.

## Steps

1. **Spawn the reviewer.** Start one subagent with a fresh context. Its prompt is [references/comment-reviewer.md](references/comment-reviewer.md) verbatim, then the scope. It deletes comments and reports; it never changes application code.
2. **Judge its report and diff.** Reject:
   - edits to application code, or to files outside the scope;
   - deletions of a comment the keep-list protects;
   - a `MUST FIX` whose reason is wrong, or that flags intended code as a mistake.

   A comment that explained a surprise in our own code stays deleted, with its `MUST FIX`. A kept comment stays only with proof it is about something we can't change. If a deletion or a keep is unclear, read the code it names until it isn't; when it is still unclear, the comment goes. Revert and rerun a rejected report once, naming what was wrong; if the second is wrong too, stop and report it open.
3. **Fix the flags.** Fix the small ones directly: rename, delete a dead path, drop a parameter, use the real API. When a fix needs a new shape (a type, an extracted function, a moved responsibility), sketch it first, then build the smallest root-cause fix within the scope, as `principle-fix-root-causes` describes. Report fixes that need work outside the scope as open; don't widen the scope.
4. **Encode claimed constraints.** A comment that said `do not remove`, `keep this order` or `talk to X before changing` claims a rule. Offer the user the cheapest check that enforces it: a type, a runtime assertion, a test or a lint. When they accept, add it and delete the comment; otherwise delete the comment and report the rule as unenforced. When running unattended, report the offer instead of waiting.
5. **Report** in chat: comments deleted, comments kept and why, `MUST FIX` flags and what fixed each, constraints encoded or left open, reruns, and anything left open.
