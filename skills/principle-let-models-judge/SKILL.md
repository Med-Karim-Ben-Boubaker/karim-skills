---
name: principle-let-models-judge
description: "Splits LLM work from code: the model judges fuzzy input, code checks the answer's structure; prompts teach the class, never the case; a wrong model answer is fixed with prompt, more reasoning or another model, not like a code bug; evals run rarely. Use for any AI engineering work: code that calls an LLM, prompts, agents, tools, model choice, evals."
---

# Let Models Judge

Fuzzy work (reading a page, classifying a document, finding a source) goes to a model. Crisp work (checking structure, enforcing invariants, building output) stays in code. Rule-based code that grows to handle fuzzy input is the duct tape of LLM systems: every new input breaks it and needs another rule. Building with a model differs from building code, down to how a wrong result is fixed.

## Split the work

- **The model reads and points.** It answers with pointers (line IDs, labels, URLs, spans) and a short reason, not rewritten text.
- **Code checks the pointers and the structure:** the IDs exist, the URL loads and sits on an allowed site, the answer matches its schema. Never require a quote to appear verbatim: that check is too brittle.
- **Code builds the output** from checked pointers.
- **A wrong reading is never fixed with a rule in code**: see **A wrong answer is not a code bug**.
- **An answer that still fails after its repair** becomes a flagged item for a person, never silent output.

## Prompts teach the class, never the case

- Define each part by its meaning and its job, with criteria. Use varied examples labelled "for example", never taken from the eval set.
- **No patch prompting:** no rule written for one case, no fixture, town or vendor names, no layouts or wording from one document, no piles of "don't", no escalating IMPORTANT and NEVER, no step lists fitted to one input.
- Explain the why, define terms, and let the model flag ambiguity or decline.
- Fold each fix into the existing text and prune lines that don't measurably help.
- Knowledge that varies by context (a region's law, a vendor's format) lives in a knowledge file the prompt loads, not in the prompt and not in code.

## A wrong answer is not a code bug

A code bug is fixed the classical way: a test that goes red on it, then the change that turns it green (`tdd`, `diagnose-bug`). A model's wrong answer has no such switch. One more rule in the prompt may fix today's case and fail on the next input, so it proves nothing. Work these levers in order, one at a time, and judge each on a handful of cases beyond the one that failed:

1. **Rule out the code.** Read what the model was given: its context, the tool results, the schema, a page cut short. A model that never saw the fact has a code bug around it, and that is fixed with a test.
2. **Teach the class in the prompt**, as the section above says: sharpen the definition or the criteria the failing case fell under.
3. **Give the model more room to reason:** a higher reasoning effort or thinking budget, a reason before the answer, or a step that does two jobs split into two calls.
4. **Try another model.** Ask the user before running a more expensive one, and say what it costs per run.
5. **Still wrong:** write the limit down and let the pipeline flag such items for a person.

## Evals are not tests

| | Code tests | Evals |
|---|---|---|
| Measure | The code's behaviour | A model's behaviour on a task |
| Call a model | Never: fakes, fixtures, recorded answers | Yes |
| Run | Targeted while working; full suite once, on the way into the default branch | Rarely |
| Cost | Seconds | Minutes to hours, and real money |

Run an eval only when a person changed a prompt, model, model setting or tool in a way that changes behaviour, and wants it measured. Everything else is a code test. When one runs:

- **Estimate cost and time first,** and say both.
- **Start with the smallest set that answers the question:** a handful of hard cases, one run. Widen only when it holds.
- **The cheapest model that passes.** One metric and one threshold per component; no statistics, charts or dashboards unless asked.
- **Accept known limits.** Hard sets are harder than reality: flag the failures, write the limit down, and stop iterating when the bar holds.
- **Fix the harness and build the missing tools before hill climbing** on models or prompts.

**Terms:** LLM-as-a-component, structured output, grounding, pointer-based extraction, schema validation, patch prompting, prompt overfitting, few-shot examples, data leakage, eval set, held-out set, LLM-as-a-judge, hill climbing, cost per document, known limits.
