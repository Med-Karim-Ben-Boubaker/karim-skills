---
name: diagram-design
description: "Turns code into technical diagrams a human reads instead of the code: architecture, dependency, data flow, sequence, state, ER, UML class, deployment, rendered as a self-contained HTML page in Eraser's visual style, where every box and arrow links back to its source line."
disable-model-invocation: true
---

# Diagram design

The user does not read code. They read the diagram. Every diagram you draw replaces a stretch of reading with a picture that a human takes in at a glance, so **the picture carries the meaning and text is the last resort**.

You write the page yourself: HTML for boxes, SVG for lines, using only the components in [`assets/template.html`](assets/template.html). Its CSS is Eraser's design system and its JS adds hover focus, source cards, and an evidence panel. You never restyle it.

## Text minimisation

This rule outranks every other rule in the skill.

- **A label names; it never explains.** 1–3 words. A module, a class, a table, a verb on an edge (`PDF`, `writes`, `GET /plans`).
- **Sublabels carry an identifier, not a phrase**: a file name, a port, a type.
- **Per diagram, one header phrase at most.** No paragraphs anywhere on the page.
- **Everything else goes in `data-note`**, a single short sentence on the component, shown on hover and in the panel. Detail is there when asked for and invisible until then.
- **Encode before you write.** Before adding a word, ask which of these can carry it instead:

| Meaning | Visual channel |
|---|---|
| belongs to | nesting inside a group |
| category / layer / owner | `data-color` (one colour per category, ≤ 4 per page) |
| outside the system | `external` (dashed, no shadow) or an icon node |
| kind of thing (DB, queue, user, file) | icon |
| order / time | left→right or top→down position |
| sync vs async, strong vs weak | solid / `dashed` / `dotted` line |
| the main path | `thick` on one edge |
| how many | a `badge` (`×3`, `4 in`) |
| has more inside | a `drill` link |

A diagram passes when someone who has never seen the code can say what the system does after 10 seconds, and has read fewer than 40 words to do it.

## Steps

1. **Pin the question.** Restate the user's request as the one question the diagram answers ("how does a council PDF become a database row?"). Pick the type from the table below. If the request needs several questions answered, plan one figure per question on the same page. Done when each figure has a question and a type.
2. **Read the code.** Collect only what the figures will show: the components and their files, who calls or imports whom, the data passed, the states and transitions, the tables and keys. For a large area, send a subagent to map it and keep only its map. Done when every box and every arrow you plan to draw has a `path:line` that proves it.
3. **Cut.** Apply the deletion test: remove any box a reader wouldn't miss, merge two boxes that always travel together, drop any arrow the layout already implies. Stay inside the type's budget; over budget, split into an overview plus a detail figure, or plan a drill-down page. Done when every remaining element earns its place.
4. **Lay out on paper first.** Write the coordinates as a short list before writing HTML: canvas size, each group and box with `left, top, width, height`, each edge with its route. Main flow left→right (or top→down for sequence and dependency), everything on a 4px grid, 32px or more between boxes, 64px or more where a labelled edge runs. Done when no two boxes overlap and every edge has a route that obeys the routing rules in [`references/primitives.md`](references/primitives.md).
5. **Write the page.** Copy `assets/template.html` to the target path, then fill the title, the crumbs, and one `<section class="figure">` per figure from the primitives. Put `data-src="path:line"` (space-separated if several) on every node, group, entity, and edge, with paths relative to the repo root, and set `<html data-root="/abs/repo/root">` so sources open in the editor. Done when no placeholder text is left.
6. **Review by looking.** Serve the page's folder over local HTTP (`python3 -m http.server`; `file://` is blocked) and screenshot it with Playwright, in light and in dark (`document.documentElement.dataset.theme = "dark"`). Hover one node and check that its edges light up. Look for overlapping boxes, labels on borders or bends, arrows that start inside a box or end short of it, clipped text, and lines that pass behind boxes. Fix and re-shoot. Done when a screenshot shows none of these.
7. **Report** the file path and one line per figure saying what question it answers.

## Choosing the type

| Question | Type | Guide |
|---|---|---|
| What are the parts, and what talks to what? | Architecture | [types/architecture.md](references/types/architecture.md) |
| What is the whole system, end to end, in one picture? | High-level | [types/high-level.md](references/types/high-level.md) |
| What depends on what? Where are the cycles? | Dependency | [types/dependency.md](references/types/dependency.md) |
| How does data change on its way through? | Data flow | [types/data-flow.md](references/types/data-flow.md) |
| Who calls whom, in what order, for one scenario? | Sequence | [types/sequence.md](references/types/sequence.md) |
| What states can this be in, and what moves it? | State | [types/state.md](references/types/state.md) |
| What is stored, and how does it relate? | ER | [types/er.md](references/types/er.md) |
| What are the classes, their operations, and inheritance? | UML class | [types/uml-class.md](references/types/uml-class.md) |
| What runs where, how many, behind which boundary? | Deployment | [types/deployment.md](references/types/deployment.md) |

Read the chosen type's guide before step 4. If a table or a sentence would answer the question better than any diagram, say so and give that instead.

## Budget

Per figure: **≤ 9 boxes, ≤ 12 edges, ≤ 4 colours, 1 thick edge.** Types tighten this; their guides say how. Over budget means two figures, not a denser one.

## Drill-down

Link pages when the code itself nests: a box that stands for a package with its own internals worth a diagram, or a system view whose parts each have a story. Then:

- The parent box or group gets `<a class="drill" href="<child page>">open ↘</a>` and `data-href` with the same path.
- The child page's crumbs link back up: `<a href="../<parent page>">↑ parent</a>`.
- Draw a child only when it has more than about 3 parts of its own; a leaf stays a box.

Draw the pages the user asked for, plus the children they need to make sense. Name each page after what it shows, next to the code it describes (`src/etl/extract/data-flow.html`), unless the user names a place.

## Trust

Every element must trace to code. Name boxes exactly as the code does: module, class, table, and function names as written. When a box is a summary of several files (a package), `data-src` lists the folder. When an edge stands for a call, cite the call site; for an import, the import line; for data passed, the line that passes it. If you can't cite something, leave it out of the drawing; an uncited box is a guess the user can't check.

## Icons and JS

- Icons: [`references/icons.md`](references/icons.md).
- Behaviour beyond the template (stepping through a sequence, toggling layers, filtering by colour): write it as a second `<script>` after the template's, following the patterns in [`references/js-patterns.md`](references/js-patterns.md). Leave the template's own script unchanged.
