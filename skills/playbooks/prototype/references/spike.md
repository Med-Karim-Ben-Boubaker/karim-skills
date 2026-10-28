# Spike

The smallest runnable script that answers **"will this library or approach work for us?"** by running it, not by reading its README. Use this when choosing between dependencies, APIs, or technical approaches, or when checking that one candidate survives a specific constraint.

If the question is about business logic or a domain process, this is the wrong branch. Use [logic.md](logic.md). If it's about what something looks like, use [ui.md](ui.md).

## When this is the right shape

- "Can pdfkit or typst produce a signed, PDF/A-compliant letter?"
- "Does this FHIR client handle our server's auth flow?"
- "Is library X fast enough for 50k rows in the browser?"
- "Which of these two queue approaches survives a worker crash mid-job?"

## Process

### 1. Name the constraint

Write down the one or two constraints that decide the choice, and what result counts as pass or fail. A spike that tests "is it nice?" answers nothing. Put this at the top of the spike's README or main file.

### 2. Pick candidates

Two or three real alternatives, including "write it ourselves" or "don't use a library" when that's plausible. Check each candidate's docs and maintenance health first if the user hasn't; call the Skill tool with "research" for anything beyond a quick look.

### 3. Write one script per candidate

Same input, same scenario, same output format, so results compare directly. Exercise the constraint and nothing else: no app around it, no abstractions shared between candidates. Print what you observe: the output, the error, the timing, the file produced.

### 4. Run and record

Run every candidate. Record the raw observation, not your impression of it. When the result is a number, call the Skill tool with "principle-explain-the-number" before trusting it: run it more than once, and name what limits it.

### 5. Hand back the verdict

A short table: candidate, constraint, observed result, pass or fail. Then a recommendation, and what the spike did **not** test. Capture it per the [playbook](../SKILL.md): the `prototype/<question-slug>` branch holds the scripts, and an ADR records the choice if it's hard to reverse.

## Anti-patterns

- **Don't trust the README.** A claim in the docs is a hypothesis until the script shows it.
- **Don't build the integration.** The spike answers the question; wiring the winner into the app is build work.
- **Don't test only the happy path.** Include the input most likely to break the candidate: the big file, the bad credential, the crash mid-run.
