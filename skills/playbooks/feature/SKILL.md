---
name: feature
description: "Playbook for new or changed behaviour: a ticket, a spec slice, or a described change. Shape first, then test-first slices, then proof on the real surface. Use when the user wants something built that changes what the code does."
---

# Feature

**You own the design.** Shape first, then fill it in one tested slice at a time.

If the input is a spec with a ticket graph, follow [references/ticket-graph.md](references/ticket-graph.md) instead: it runs this playbook once per ticket. If a ticket reference is given, fetch it and state its title. Read `GLOSSARY.md` and the ADRs in the area.

1. **Learn the area.** Call the Skill tool with "how" over any subsystem you haven't traced this session. *Done when:* you can name the files and the seam the change goes through.
2. **Name the shape.** Write the types, signatures, and module layout before any logic (**principle-foundational-thinking**). Stateful logic gets a structure, not scattered conditionals (**principle-model-the-domain**). *Done when:* the shape is written in your todo list or a scratch file.
3. **Pick the seam.** The highest interface where the behaviour is observable (**principle-deep-modules**). *Done when:* the seam is stated before the first test.
4. **Red → green, one slice at a time.** Call the Skill tool with "tdd". Parse external input at the edge (**principle-boundary-discipline**). Anything retried gets a test that runs it twice (**principle-make-operations-idempotent**). *Done when:* every acceptance criterion has a test that went red, then green.
5. **Prove it on the real surface.** Run it the way its user would: endpoint, CLI, page (**principle-prove-it-works**). *Done when:* each criterion is checked against output you saw. Tests passing is evidence, not the verdict.
6. **Update blueprints.** If a folder's modules, interface, or data flow changed, call the Skill tool with "blueprint". *Done when:* the README matches the code, or `skip: no structural change`.
7. **Commit in small green units** (**principle-sequence-verifiable-units**): scaffold or types, then each slice with its test. Then run the **review** playbook. *Done when:* every commit passes on its own and review returned a verdict.

Steps only a human can do (credentials, a third-party dashboard, a cutover) get a script from the "wizard" skill. Decide reversible choices yourself and list them in the reply (**principle-never-block-on-the-human**). Ask only about product calls and one-way doors. If the work mixes behaviour change with restructuring, land the **refactoring** first.

**Reply:** what you built, the shape you chose and why, the choices you made alone, the real-surface evidence, the review verdict.
