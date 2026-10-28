---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

In the first round, call the Skill tool with "principle-attack-the-premise" and include at least one question that tests whether the plan solves the right problem. When the tree reaches the domain's states, rules, or what must never happen, call the Skill tool with "principle-model-the-domain" to shape those questions.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch an `explorer` agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

Not every open question is a decision or a lookup. Call the Skill tool with "principle-never-block-on-the-human", then route what neither of you can answer:

- **Running something would answer it** (does this process hold up, does this library cope, which layout reads better): call the Skill tool with "prototype".
- **An external fact** (a regulation, a standard, an API's behaviour, what the client wrote last month): call the Skill tool with "research".
- **Only the client or a domain expert knows**: call the Skill tool with "to-questionnaire".

Each of these is an unsettled prerequisite: keep asking the rest of the frontier while it runs.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
