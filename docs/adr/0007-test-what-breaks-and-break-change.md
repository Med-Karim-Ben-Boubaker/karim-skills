---
status: accepted
---

# One testing principle across the lifecycle, and a QA pass that tries to break the work

`tdd` wrote good functional tests of the user flow, yet the lexi-municipal-etl pipeline kept failing on its first full-size runs because of limits nobody had named: page pixel sizes over a provider's caps (#631, #690, #691), OCR running out of memory after 953 of about 23,500 documents (#707), open-file limits past about 500 workers (#640, #642), leases lost to steps longer than the five-minute stale window (#556, #632, #681), storage calls growing with every item (#556, #633), a memory leak per Publisher (#664), PDFium parallelism (#708) and the Build budget (#586). Each of those 13 audited incidents is a fast unit test once the limit has a name. A wider sweep of the lexi-municipal-etl and lexi trackers (first page of each list, titles only, 47 of the hits unverified user reports) found about 95 bugs from real runs: about 53 bad input, 25 limits, 10 logic, 3 dependency faults, 2 config. Most of what escaped was never in reach of a functional test.

**Decision.**

- **One principle, `principle-test-what-breaks`**, holds the testing mindset from Gayathri Mohan's *Full Stack Testing* (O'Reilly, 2022), clustered by the stage that applies it: **Spec** (name the operating envelope, the worst real inputs, the outcome for bad input, each dependency's failure modes), **Build** (limit, cost and fault tests beside the functional ones), **Break** (attack the finished work, then rehearse at full size before the first real run), **Loops** (every check has a trigger; red means stop), **Learn** (every escaped defect becomes a test and names the stage that missed it). Its `fault-checklist.md` lists the faults per data system. It replaces the untracked draft `tdd/data-testing.md`.
- **A new skill, `break-change`**, is the QA pass: like `diagnose-bug` without a bug to start from, it walks the checklist at each agreed seam and writes attacks as tests that try to go red. Run for someone else's work, it writes tests and stops at its report; the author fixes each break. `implement` runs it in a fresh subagent at the start of Reviewing, before `remove-comments` and `review-code`, so no ticket state changes.
- **The other skills point to it**: `tdd` picks cases as functional, then robustness; `grill` asks for limits and failure modes, `write-spec` gains **Limits and Failure Modes**, and each child ticket carries its share as **Must survive**; `review-code` gains three baseline checks; `set-up-repo` gains scale and smoke test rows; `diagnose-bug` and `run-retro` record which stage missed an escaped defect.

**Considered options:** one principle file per book theme (data, security, performance, pipelines) would repeat the same "what breaks?" question in six places and cost description budget each time. Keeping the QA pass inside `tdd` would make the author attack their own assumptions, the blind spot ADR 0006 already names.

**Revisit when:** a defect from a limit or a bad input reaches a real run after a `break-change` pass marked its seam Held, or `break-change` takes longer than Building on most tickets.
