# Sequence

**Answers:** who calls whom, in what order, for one scenario. Time runs down.

## Layout

- Actors as nodes in one row at the top (`center` nodes, 120 × 56, or icon nodes for humans and external systems), 160–200px apart. Their `id`s are what messages point at.
- One `lifeline` per actor, from the bottom of its box to the bottom of the canvas.
- Messages are horizontal `edge` paths between lifeline x values, 40px apart vertically, with `data-from` and `data-to` set to the actors' ids. Label above the line (`top` = line y − 12), naming the call (`fetch(url)`) in `mono`.
- Message kinds:

| Kind | Line | Head |
|---|---|---|
| Call | solid | `arr` |
| Return | `dashed` | `arr` |
| Async / event | `dashed` | `arr-open` |
| Self-call | solid U loop out to the right, 32px wide, 24px tall | `arr` |

- **Activation** bars where an actor is busy, from the call it receives to its return.
- Branches and loops: one `frame` with `op` `alt`, `opt`, or `loop` and a short `guard`. `alt` has at most 2 regions, split by a `divider`. One frame per figure, never nested.
- The happy path's final return may be `thick`.

## Budget

≤ 5 actors, ≤ 12 messages, 1 frame.

## Avoid

- A message pointing upward: time runs down.
- Returns for every call: draw the return only when the value matters to the story.
- Two scenarios in one figure: split into happy path and failure path.
