# Writing scenes

A scene is `scenes/<chapter id>.html`: an HTML fragment that `cv.py compose` drops into a 1920×1080 frame (`.frame`, a flex column with 100 px side margins, above a footer and progress bar). The composed page loads `templates/scene.css`, GSAP, Mermaid and `templates/runtime.js`; HyperFrames seeks that timeline frame by frame, so everything on screen is a function of time and syncs exactly to the narration.

Worked example: `examples/runtime-demo/` (a diagram revealed node by node, typed code, a counter, a JS-driven bar).

## Timing attributes

| Attribute | Meaning |
|---|---|
| `data-s="k"` | Enters during beat k (1-based, `video.json` order). Before that it is invisible but keeps its space. |
| `data-a="rise"` | Entrance: `rise` (default), `fade`, `pop`, `slideL`, `slideR`, `zoomin`, `growx`, `growy`, `stamp`, `draw` (SVG path stroke), `type` (types its text), `count` (counts to `data-to`, `data-dec` decimals). |
| `data-at="0.4"` | When it enters, as a share of beat k's narration. Without it, elements of a beat enter 0.15 s apart in document order. Place each element where the narration names it. |
| `data-len="1.2"` | Entrance length in seconds. |
| `data-now` | A pulse after the entrance, for "this one". |
| `data-show="2-4"` | Exists only during beats 2–4 (`display:none` outside, freeing its space). Use it to swap whole layouts within one chapter. |
| `class="kb"` | Slow push-in (scale 1 → 1.09) over the beats it is visible, for document images. |

## Building blocks (scene.css)

Layout: `.row`, `.col`, `.grow`, `.stage` (fills the remaining height). Text: `.eyebrow`, `h1` (124 px), `h2` (68 px), `h3`, `p` (32 px), `.gloss` (28 px, secondary), `.mono`, `.tag`, `.muted`. Boxes: `.card` with `g` (kept), `b` (new), `o` (problem, dashed), `x` (dropped); `.pill g|b|o|x`; `.num` (numbered circle); `.doc` (paper document with shadow, put an `<img class="kb">` inside); `.ring` and `.stamp` (absolute callouts over a `.doc`); `.chev` (chevron roadmap); `.code` (dark code block, `<span class="hl">` highlights); `.quote`. Colours come from tokens (`var(--accent)`, `--blue`, `--orange`, `--keep`, `--grey`, `--tint-g|b|o`).

Minimum on-screen text: 24 px. A chapter header is usually:

```html
<div class="eyebrow" data-s="1" data-a="fade">Idea 2</div>
<h2 data-s="1" data-at="0.02">Only part of the bundle is law text</h2>
```

## Layouts

Vary them across chapters; repeat a layout at most twice in a row.

| Layout | Use for | Skeleton |
|---|---|---|
| Title | Hook, chapter openers | `class: dark` chapter; `.eyebrow`, `h1`, one `.gloss` line |
| Two columns | Claim + evidence | `.row` of `.col.grow` + `.doc` |
| Document + crops | Real pages | `.doc` with `img.kb`, then `.ring`/`.stamp` callouts entering on the beat that names them |
| Cards grid | 3–6 parallel items | `.row` of `.card` (`data-s` per card, same beat, staggered) |
| Flow / diagram | Systems, pipelines | `pre.diagram` (below) inside `.stage` or a `.card.grow` |
| Timeline | History, phases | `.chev` or a horizontal `.row` of `.num` + text, entering left to right |
| Before / after | Walkthrough | `.row` of two `.card.grow` (`o` then `g`), the right one entering a beat later |
| Code | Real functions | `.code` with `data-a="type"`, then `.hl` spans or a `.ring` on the line that matters |
| Quote | Stakeholder words | `.quote` + `.gloss` with who and when |
| Quiz | Retrieval | Question `h2` on beat k, answer `.card g` with `data-show` on beat k+1 |
| Number | One striking figure | `<span data-a="count" data-to="300">` at 160 px+ |

## SWE diagrams

Pick the diagram by the question the chapter answers, with the blueprint skill's table (`skills/tools/blueprint/SKILL.md`, "Choosing diagrams"): C4 context for where it sits, data flow for transforms, sequence for one request, class for core types, state for lifecycles, ER for storage. Its rules hold here too: name nodes exactly as in the code, keep under about 15 nodes, one level per diagram (split a deep system across chapters).

```html
<pre class="diagram" data-reveal='{"fetch":"1@0.15","segment":"1@0.3","check":"2","store":"2@0.6"}'>
flowchart LR
  fetch[fetch.py] --> segment[segment.py] --> check[check.py] --> store[(database)]
</pre>
```

- `data-reveal` maps a Mermaid node id to `"k"` or `"k@share"`. Unlisted nodes show from the start. An edge appears 0.4 s after the later of its two ends. Works for flowchart, class, state and ER nodes.
- `data-seq="k"` on a `sequenceDiagram` reveals its messages one by one across beat k.
- A diagram the runtime can't express (highlight a path, move a token along an edge) is hand-drawn SVG: `<path data-s="3" data-a="draw">`, `<g data-s="3" data-a="pop">`. SVG elements need no extra CSS; `scene.css` already sets `transform-box: fill-box`.

## Custom animation code

Scene `<script>` blocks run after the runtime, with these globals:

- `tl`: the chapter's paused GSAP timeline. Add tweens at absolute times: `tl.to("#token", {x: 600, duration: 2}, at(3, 0.2))`.
- `at(k, share)`: seconds into the chapter at that share of beat k.
- `driven(k, share, len, p => …)`: calls the function with p from 0 to 1 over `len` seconds. Use it for D3, canvas, Three.js or any drawing computed from a number.

Drive every animation from `tl`, `at` or `driven`. HyperFrames' lint flags `requestAnimationFrame`, `Date.now()` and `performance.now()` as non-deterministic, and `cv.py check` fails on lint errors.

## Assets

Put images in the project's `assets/` folder and reference them as `assets/<file>`. Crop real document pages to the part the beat talks about (PIL or ffmpeg) rather than showing a whole page at unreadable size.

## Fixing what check and the contact sheet show

- **Layout issue** from `inspect`: text overflowing its box or the frame. Shorten the text, drop to a smaller class, or split the step with `data-show`.
- **Crowded last frame:** more than about 7 items on screen at once. Move earlier items out with `data-show` ranges.
- **Element visible too early or late:** its `data-at` doesn't match where the narration names it. Read the beat text and move it.
