# High-level

**Answers:** what is the whole system, end to end, in one picture. The root view a newcomer opens first: who uses it, what it is made of, what it depends on outside.

## Layout

- Three columns left→right: **actors and sources** (icon nodes) · **the system** (one large group, its top-level packages as nodes or small groups) · **external systems and stores** (icon nodes or `external` nodes).
- Cross-cutting concerns (auth, config, logging, scheduler) go in a full-width strip of small nodes along the bottom of the system group, with no edges: position says "used everywhere".
- Each top-level package node gets a `drill` link to its own page. This view is the top of the drill-down tree.
- Edges only cross the system boundary: one per actor or external system, labelled with the protocol or the data (`HTTPS`, `PDF`, `SQL`).

## Budget

≤ 3 actors, ≤ 6 packages, ≤ 4 externals, ≤ 10 edges.

## Avoid

- Internal calls between packages: that is the architecture figure of the next page down.
- Version numbers, ports, hosts: that is deployment.
