# Architecture

**Answers:** what are the parts, and what talks to what. Use it for a package's modules, a service's components, or a system's services.

## Layout

- One **group** per package, layer, or trust boundary; its modules are **nodes** inside. Groups nest at most 2 levels; deeper nesting is a drill-down page.
- Main flow left→right: inputs (icon nodes: user, external API, file drop) on the left, stores on the right or bottom.
- Things outside the codebase are `external` nodes or icon nodes, outside every group.
- Colour per group, not per node. A node takes a colour only when it is the one thing the figure is about.
- Edges carry the verb or the data (`PDF`, `writes`, `GET /plans`). Unlabelled edges mean "calls".

## Budget

≤ 9 nodes, ≤ 3 sibling groups, ≤ 12 edges.

## Drill-down

A group or node that stands for a package with more than about 3 parts of its own gets a `drill` link to that package's page.

## Avoid

- One box per file when the file is a detail: the reader wants the parts, not the filesystem.
- Arrows both ways when one direction is the call and the other is just its return.
- A group around a single node.
