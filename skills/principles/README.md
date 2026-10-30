# Principles

Rules of judgment the agent applies while it works. Each answers one question, so no two overlap. You can run one by name (`/principle-keep-it-simple`), and the agent loads one when its description matches the task.

| Principle | The question it answers |
|---|---|
| [`keep-it-simple`](principle-keep-it-simple/SKILL.md) | Should this exist at all? |
| [`write-obvious-code`](principle-write-obvious-code/SKILL.md) | Can a reader understand this and change it alone? |
| [`take-small-verified-steps`](principle-take-small-verified-steps/SKILL.md) | How big is this step, and how do I know it worked? |
| [`name-the-trade-off`](principle-name-the-trade-off/SKILL.md) | What are we optimising for, and what do we give up? |
| [`point-dependencies-inward`](principle-point-dependencies-inward/SKILL.md) | Where does this code live, and which way do dependencies point? |
| [`make-illegal-states-unrepresentable`](principle-make-illegal-states-unrepresentable/SKILL.md) | Can this data hold a wrong state? |
| [`program-strategically`](principle-program-strategically/SKILL.md) | After this change, does the code look designed for it? |
| [`design-for-crashes`](principle-design-for-crashes/SKILL.md) | What if it fails, stops halfway, runs twice, or runs concurrently? |
| [`measure-before-optimizing`](principle-measure-before-optimizing/SKILL.md) | Is it actually slow, and what limits it? |
| [`fix-root-causes`](principle-fix-root-causes/SKILL.md) | Where did it first go wrong? |

Covered by other skills, so no principle: deep modules and seams (`codebase-design`), testing behaviour through interfaces (`tdd`), the project's vocabulary (`model-domain`), the debugging loop (`diagnose-bug`), turning recurring corrections into checks (`run-retro`).
