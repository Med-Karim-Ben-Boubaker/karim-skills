# Primitives

Markup for every component in `assets/template.html`. The template's CSS styles these classes; the page never adds its own colours, fonts, shadows, or radii. Colour comes only from `data-color`.

## Coordinate model

A diagram is a **canvas**: a fixed-size box where HTML components sit at absolute pixel positions, with one SVG layer underneath for the lines. Both share one coordinate system (the SVG has no `viewBox`, so its units are CSS pixels and it can never stretch), so a box at `left:120px; top:80px; width:160px; height:56px` has its right-edge midpoint at `(280, 108)`, and that is where its edge starts.

- Every `left`, `top`, `width`, `height` is a multiple of 4. Canvas size too.
- Every component sets all four explicitly. A box whose height depends on wrapping text breaks the edge maths.
- Paint order is document order: groups, then the SVG, then nodes and labels. Edges therefore run *under* boxes.

## Figure

```html
<section class="figure">
  <header><h2>Data flow</h2><span>one short phrase, or nothing</span></header>
  <div class="scroll">
    <div class="canvas" style="width:960px;height:440px">
      <!-- groups -->
      <svg class="edges"><!-- MARKERS, then edges --></svg>
      <!-- nodes, entities, edge labels -->
    </div>
  </div>
  <div class="legend"><!-- only if colour or line style carries meaning --></div>
</section>
```

## Markers

Paste once as the first child of each `svg.edges`. IDs must be unique per page, so suffix them per figure (`arr-2`) when a page has several figures.

```html
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path class="fill" d="M0 0 L10 5 L0 10 z"/></marker>
  <marker id="arr-open" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path class="open" d="M1 1 L9 5 L1 9"/></marker>
  <marker id="arr-blue" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse"><path class="blue" d="M0 0 L10 5 L0 10 z"/></marker>
  <!-- UML / ER only -->
  <marker id="tri-hollow" viewBox="0 0 12 12" refX="11" refY="6" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto-start-reverse"><path class="hollow" d="M1 1 L11 6 L1 11 z"/></marker>
  <marker id="dia-fill" viewBox="0 0 16 10" refX="15" refY="5" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="10" orient="auto-start-reverse"><path class="fill" d="M1 5 L8 1 L15 5 L8 9 z"/></marker>
  <marker id="dia-hollow" viewBox="0 0 16 10" refX="15" refY="5" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="10" orient="auto-start-reverse"><path class="hollow" d="M1 5 L8 1 L15 5 L8 9 z"/></marker>
  <marker id="crow-many" viewBox="0 0 14 14" refX="13" refY="7" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto-start-reverse"><path class="open" d="M13 1 L1 7 L13 13 M1 7 H13 M5 2 V12"/></marker>
  <marker id="crow-one" viewBox="0 0 14 14" refX="13" refY="7" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto-start-reverse"><path class="open" d="M1 7 H13 M5 2 V12 M9 2 V12"/></marker>
</defs>
```

`marker-end` points at the target; `marker-start` with the same id draws a head at the source (`auto-start-reverse` flips it).

## Node

```html
<div class="node" id="fetch" style="left:120px;top:80px;width:176px;height:56px"
     data-src="src/etl/extract/fetch.py:14" data-note="Downloads council PDFs, retries 3×" data-kind="module">
  <svg class="ico" ...tabler icon...></svg>
  <div class="txt"><span class="label">Fetcher</span><span class="sub">fetch.py</span></div>
</div>
```

Variants (classes add up):

| Class | Use |
|---|---|
| `data-color="blue"` | Category colour. Pastel fill, coloured border. |
| `center` | Icon above text, centred. Use for square boxes. |
| `external` | Dashed, no shadow: outside the system (third-party API, user). |
| `pill` | Fully round: an event, a message, a state. |
| `db` | Softer corners for a store. Pair with the `database` icon. |

Extras inside a node: `<span class="badge">×3</span>` (count, fan-in, replicas) and `<a class="drill" href="extract/ARCHITECTURE.html">open ↘</a>` (drill-down, see SKILL.md).

Sizes: 160–200 × 56 for icon + label + sub; 120 × 48 for label only; 96 × 96 for `center`. Width grows with the label, never the font shrinks: allow 9px per label character plus 72px for icon and padding (`store_document`, 14 chars → 200), and check the sublabel the same way at 7.5px per character.

## Icon node

Eraser's signature look: a glyph in a tinted tile, caption under it, no box. For actors, external systems, and stores at the edge of a diagram.

```html
<div class="inode" id="user" data-color="purple" style="left:40px;top:96px;width:88px;height:72px" data-note="Council clerk">
  <svg class="ico" ...></svg>
  <span class="label">Clerk</span>
</div>
```

## Group

A container for what belongs together: a package, a layer, a trust boundary. Draw it before the SVG layer so everything paints over it.

```html
<div class="group" id="g-extract" data-color="blue" style="left:96px;top:40px;width:448px;height:200px"
     data-src="src/etl/extract/" data-href="extract/ARCHITECTURE.html">
  <div class="title"><svg class="ico" ...></svg>extract<span class="sub">src/etl/extract</span></div>
</div>
```

`dashed` class: a boundary that is logical, not physical (a trust zone, "runs in CI"). Leave 48px between the group's top edge and the first child's top (the title chip sits there), and 24px on the other sides.

## Edge

An edge is an SVG `path` with class `edge`, `data-from` and `data-to` naming the ids it joins. Those two attributes are what make hover-focus light up the right lines.

```html
<path class="edge" id="e1" data-from="fetch" data-to="parse" data-src="src/etl/extract/fetch.py:52"
      d="M296 108 H400" marker-end="url(#arr)"/>
```

| Class | Meaning |
|---|---|
| (none) | Call, import, data passed |
| `dashed` | Async, event, return, optional |
| `dotted` | Weak link: config, reads-at-startup |
| `data-color="…"` | The edge belongs to that colour's category |
| `thick` | The main path, at most one per diagram |

### Routing

- **Straight** when both ends share an x or a y: `M x1 y H x2` or `M x y1 V y2`.
- **Elbow** otherwise, with rounded corners of radius 8. Right then down to a point lower-right, turning at `mx`:
  `M x1 y1 H mx-8 Q mx y1 mx y1+8 V y2-8 Q mx y2 mx+8 y2 H x2`. Flip signs for the other directions.
- **One bend** when the target sits above or below: leave the source's side, enter the target's top or bottom.
  `M x1 y1 H x2-8 Q x2 y1 x2 y1+8 V y2`.

Rules:
1. Leave and enter a box perpendicular to its edge, at least 12px from a corner. Never draw a diagonal.
2. Several edges on one side of a box get separate ports, spread at `L·k/(N+1)` and at least 12px apart.
3. Parallel edges stay at least 12px apart along their whole length. Never stack two strokes.
4. An edge never passes behind a box it doesn't connect. Move the box or reroute.
5. When two edges must cross, the less important one hops: `H cx-6 a6 6 0 0 1 12 0 H x2`.
6. Stop the path where the marker tip should touch the box border, not inside the box.

## Edge label

HTML, centred on a point of the path. Its background masks the line under it, Eraser-style.

```html
<span class="edge-label" data-edge="e1" style="left:348px;top:108px">PDF bytes</span>
```

- Place it on a straight segment, at least 16px from any box and any bend.
- `data-edge` ties it to its path so hover lights both.
- `mono` class for code-ish text (`GET /plans`, `:5432`). `card` class for ER cardinality, placed 16px from the entity border.

## Entity (ER) and class (UML)

```html
<div class="entity" id="plan" style="left:80px;top:60px;width:224px;height:124px" data-src="src/etl/models.py:31">
  <div class="head"><span class="stereo">table</span>Plan</div>
  <div class="row key"><span># id</span><span class="t">uuid</span></div>
  <div class="row"><span>→ municipality_id</span><span class="t">uuid</span></div>
  <div class="row"><span>published_at</span><span class="t">date</span></div>
</div>
```

Height = 40 (head) + 28 × rows + compartment separators. Row *i* (0-based) has its centre at `top + 40 + 28·i + 14`: anchor column-to-column edges there. For UML, put `<div class="sep"></div>` between attributes and operations (adds 1px; round the height up to the grid).

## Sequence parts

```html
<!-- lifeline, inside svg.edges -->
<line class="lifeline" x1="160" y1="96" x2="160" y2="520"/>
<!-- activation bar: centred on the lifeline x -->
<div class="activation" style="left:160px;top:140px;height:96px"></div>
<!-- fragment -->
<div class="frame" style="left:96px;top:260px;width:520px;height:160px">
  <span class="op">alt</span><span class="guard">[cache hit]</span>
  <div class="divider" style="top:84px"></div>
</div>
```

Messages are `edge` paths between lifeline x positions, with `data-from`/`data-to` set to the actors' ids.

## State parts

```html
<div class="dot" style="left:40px;top:92px"></div>            <!-- start -->
<div class="dot end" style="left:840px;top:92px"></div>       <!-- end -->
<div class="node pill" id="queued" style="left:120px;top:80px;width:128px;height:40px"><span class="label">queued</span></div>
```

## Legend

Only when colour or line style carries meaning the labels don't already say.

```html
<div class="legend">
  <span><i class="swatch" data-color="blue"></i>extract</span>
  <span><i class="swatch line"></i>call</span>
  <span><i class="swatch line dashed"></i>async</span>
</div>
```
