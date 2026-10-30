# Data flow

**Answers:** how data changes on its way through. The edges are the story: what shape the data has at each step.

## Layout

- One straight line of steps left→right, the pipeline's order. Wrap into a second row (right→left is confusing; start the second row at the left again, with one elbow down) only when the canvas would pass about 1100px.
- Steps are nodes named by the function or module that does the work; sublabel is the file.
- **Every edge carries the data type** that crosses it, as a `mono` label: `bytes`, `Plan`, `list[Row]`. A reader should be able to follow the types alone and know what happens.
- Sources on the far left as icon nodes, sinks on the far right as `db` nodes or icon nodes.
- Branches (a side output, an error path) leave downward; error paths are `dashed` with `data-color="red"`.
- Group steps by stage (`extract`, `transform`, `load`) when the code has those stages as packages.

## Budget

≤ 8 steps, ≤ 3 branches, ≤ 2 sources, ≤ 2 sinks.

## Avoid

- An edge with no data label: then it is an architecture figure.
- Boxes for data. Data lives on the edges; boxes are what transforms it.
