# Principles

Rules of judgment the agent applies while it works. Each answers one question, so no two overlap. You can run one by name (`/principle-keep-it-simple`), and the agent loads one when its description matches the task.

| Principle | The question it answers |
|---|---|
| [`keep-it-simple`](principle-keep-it-simple/SKILL.md) | Should this exist at all? |
| [`obvious-code`](principle-obvious-code/SKILL.md) | Can a reader understand this and change it alone? |
| [`small-verified-steps`](principle-small-verified-steps/SKILL.md) | How big is this step, and how do I know it worked? |
| [`name-the-trade-off`](principle-name-the-trade-off/SKILL.md) | What are we optimising for, and what do we give up? |
| [`dependency-rule`](principle-dependency-rule/SKILL.md) | Where does this code live, and which way do dependencies point? |
| [`make-illegal-states-unrepresentable`](principle-make-illegal-states-unrepresentable/SKILL.md) | Can this data hold a wrong state? |
| [`strategic-programming`](principle-strategic-programming/SKILL.md) | After this change, does the code look designed for it? |
| [`crash-only`](principle-crash-only/SKILL.md) | What if it fails, stops halfway, runs twice, or runs concurrently? |
| [`measure-before-optimizing`](principle-measure-before-optimizing/SKILL.md) | Is it actually slow, and what limits it? |
| [`fix-root-causes`](principle-fix-root-causes/SKILL.md) | Where did it first go wrong? |

Covered by other skills, so no principle: deep modules and seams (`codebase-design`), testing behaviour through interfaces (`tdd`), the project's vocabulary (`domain-modeling`), the debugging loop (`diagnosing-bugs`), turning recurring corrections into checks (`retro`).
