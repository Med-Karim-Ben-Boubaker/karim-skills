---
name: principle-let-models-judge
description: "Splits LLM work from code: the model reads and judges fuzzy input, code checks its answer's structure and builds the output; prompts teach the class, never the case; evals are not tests and run rarely. Use when writing prompts, agents or LLM pipeline steps, fixing a wrong model answer, or planning or running evals."
---

# Let Models Judge

Fuzzy work (reading a page, classifying a document, finding a source) goes to a model. Crisp work (checking structure, enforcing invariants, building output) stays in code. Rule-based code that grows to handle fuzzy input is the duct tape of LLM systems: every new input breaks it and needs another rule.

## Split the work

- **The model reads and points.** It answers with pointers (line IDs, labels, URLs, spans) and a short reason, not rewritten text.
- **Code checks the pointers and the structure:** the IDs exist, the URL loads and sits on an allowed site, the answer matches its schema. Never require a quote to appear verbatim: that check is too brittle.
- **Code builds the output** from checked pointers.
- **A wrong reading is fixed in the prompt first**, then with a better model, never with a rule in code.
- **An answer that still fails after its repair** becomes a flagged item for a person, never silent output.

## Prompts teach the class, never the case

- Define each part by its meaning and its job, with criteria. Use varied examples labelled "for example", never taken from the eval set.
- **No patch prompting:** no rule written for one case, no fixture, town or vendor names, no layouts or wording from one document, no piles of "don't", no escalating IMPORTANT and NEVER, no step lists fitted to one input.
- Explain the why, define terms, and let the model flag ambiguity or decline.
- Fold each fix into the existing text and prune lines that don't measurably help.
- Knowledge that varies by context (a region's law, a vendor's format) lives in a knowledge file the prompt loads, not in the prompt and not in code.

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
