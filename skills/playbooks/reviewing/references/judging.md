# Judging findings

**Dismiss:**

- **Inflated nits.** If a lane found only nits, the code is probably fine. Say so.
- **Hypotheticals.** "What if this is null?" stays only if you trace a caller that passes null.
- **Premature abstraction.** An extraction the code doesn't need yet.
- **"I'd have done it differently"** with no concrete problem.
- **Missing context.** Findings on code the diff didn't touch, or on patterns the rest of the codebase uses on purpose.

**Keep:**

- Two or more lanes raised it independently.
- It names a concrete execution path.
- It's a security or correctness finding. Scrutinize these harder before dismissing.

**Evidence outranks reading.** A finding proven by running something beats one inferred from the diff. A reading-only claim about behaviour that the behaviour lane ran and saw working is probably wrong; check it against that lane's output.

**Encode, don't repeat.** A finding a lint, type, or test could have caught goes in **Act on** with a note to encode it (**principle-encode-lessons-in-structure**).
