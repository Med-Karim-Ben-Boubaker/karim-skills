# State

**Answers:** what states a thing can be in, and what moves it between them. Use it when the code has an enum or a status field with transitions.

## Layout

- States are `pill` nodes named exactly as the enum values. Start is a `dot`; terminal states lead to a `dot end`.
- Main path left→right along one row; retries, waits, and failures in a row below it.
- Transitions are edges labelled with the event that triggers them (`fetched`, `timeout`). Add `[guard]` only when two transitions leave on the same event.
- Failure states take `data-color="red"`, success terminal `data-color="green"`. Nothing else is coloured.
- Self-loops: a small U above the state.
- `data-src` on each transition cites the line that sets the new state.

## Budget

≤ 8 states, ≤ 12 transitions.

## Avoid

- A transition from every state to `error`: draw one edge from a small group around the states it applies to, labelled `any → error`.
- Unlabelled transitions: the trigger is the whole point.
