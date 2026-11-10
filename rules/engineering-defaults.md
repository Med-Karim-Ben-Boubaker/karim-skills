# Engineering defaults

For every plan, design and change:

- **Least that works.** Propose the minimal version first and list what you cut, one reason each. Every changed line traces to the request; anything else goes under "Noticed, not done".
- **Fix where it first went wrong.** A failure surfaces as an error. A fallback, default, retry, caught exception or special case needs a state that can really happen.
- **The class, not the instance.** A town, layout, fixture or example is evidence, never a rule, in code, prompts and tickets.
- **Prove before you claim.** Run it the way a person would, writing only to a sandbox (a scratch folder or bucket prefix), and show what you ran and what you saw: the output or the screenshot itself. Every number cites its source.
- **Test what changed, with FIRST tests.** Each test runs in milliseconds, alone or in any order, gives the same result every run and checks its own result (`tdd`). While working, run the narrowest test that can catch the change. Run the full suite once, before you hand back. Code tests never call a model. Run evals only when a person changed a prompt, model, model setting or tool and wants it measured.

The detail lives in the principle skills: `principle-keep-it-simple`, `principle-fix-root-causes`, `principle-take-small-verified-steps`, `principle-design-the-core`, `principle-design-for-operations`, `principle-let-models-judge`.
