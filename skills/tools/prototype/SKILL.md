---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model, domain process, or logic feels right, explore what a UI should look like, or spike a library or approach against a real constraint before committing to it.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model / process feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive. Call the Skill tool with "principle-model-the-domain" before choosing the state shape.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.
- **"Will this library / approach work for us?"** → [SPIKE.md](SPIKE.md). Write the smallest script that exercises the one constraint that matters, run it against each candidate, and record what you observed.

The branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI; a dependency choice → spike) and state the assumption at the top of the prototype.

Whatever the branch, when there is more than one plausible answer, call the Skill tool with "principle-exhaust-the-design-space": build 2 to 3 structurally different variants, not two flavours of one.

## Rules that apply to every branch

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure. With no codebase yet, work in a scratch directory.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. A spike is one command per candidate. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic), on every variant switch (UI), or on every run (spike), print or render the full relevant state so the user can see what changed.
6. **The verdict comes from observation.** Call the Skill tool with "principle-prove-it-works": the answer is what you saw the prototype do (the output, the screenshot, the timing, the user's reaction while clicking through), not what you expected it to do.
7. **Capture it when done.** Commit the prototype to a throwaway `prototype/<question-slug>` branch, out of main, never merged. The commit message states the question and the verdict. Fold any validated decision into the real code if there is any. If the verdict settles a hard-to-reverse trade-off, call the Skill tool with "domain-modeling" to record an ADR that points at the branch. The main branch keeps only the validated decision.
