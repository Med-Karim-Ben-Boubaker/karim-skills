# Lane: tests

A test is a claim. Find out whether it can fail. You run in a throwaway worktree; every edit is a sabotage you revert before the next.

Call the Skill tool with "principle-test-behavior-not-implementation" first.

For each test the diff adds or changes:

1. **Break the behaviour.** Make the smallest edit that violates what the test claims (wrong value, skipped effect, done twice). Run the test. It must fail. If it passes, it is `HOLLOW`.
2. **Change the internals.** Where cheap, restructure without changing anything observable (inline a helper, rename a private symbol). Run the test. It must pass. If it fails, it is `PINNED`.
3. `git checkout -- .` before the next test.

Also report: untested acceptance criteria or code paths, tautologies (expected value computed the way the code computes it), and tests that reach past the module's interface. Call the Skill tool with "principle-first-tests" for speed and flakiness; mark timing you couldn't measure as unknown.

```
Tests audited: N
- <test> (<file>): SOLID | HOLLOW: <sabotage> still passed | PINNED: <refactor> broke it
Untested: ...
Tautologies: ...
Wrong seam: ...
```
