# Dependency

**Answers:** what depends on what, where dependencies pile up, and where they loop. Use it when a module has several dependents or there is a cycle; if every node has one parent and nothing points back, a tree in an architecture figure says it more simply.

## Layout

- **Ranked rows, top→down.** Row 0 is the entry points nothing imports. Each lower row is one step deeper. Rows 120px apart. Edges point down.
- Nodes are packages or modules, never single files unless the files are the modules.
- Every node carries a `badge` with its fan-in (`4 in`). The node with the highest fan-in is the story.
- Third-party packages: `external` nodes in the bottom row, sublabel is the version (`2.31 · pypi`).
- **The cycle**, at most one: a `dashed` edge with `data-color="red"`, routed around the outside of the stack, labelled `cycle`. It is the one edge that points up.

## Budget

≤ 9 nodes, ≤ 14 edges, ≤ 4 rows, 1 cycle.

## Avoid

- A hairball with no rows: rank first, always.
- An upward edge that is not the marked cycle.
- Hiding nodes to fit: collapse leaves into one node (`+6 leaves`) and say so in its `data-note`.
