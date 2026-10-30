# JS patterns

The template's script already gives every page hover focus, source cards, the evidence panel, keyboard access, and the theme toggle. Add a second `<script>` after it only when a figure needs behaviour those don't cover. Each pattern below is a starting point; adapt names, keep the shape.

Rules for any script you add:

- Vanilla JS in an IIFE, no libraries, no network.
- Drive appearance by toggling classes or `data-*` attributes the CSS already styles (`.lit`, `.focusing`, `hidden`). Add CSS only inside a `<style>` block next to the script, using the template's tokens.
- The page reads fully with the script off: the default state shows everything.

## Step through a sequence

Buttons reveal one message at a time. Number the messages with `data-step` on each edge and its label.

```html
<div class="stepper"><button data-prev>←</button><span data-count></span><button data-next>→</button></div>
<script>
(() => {
  const fig = document.currentScript.closest(".figure") || document.querySelector(".figure");
  const items = [...fig.querySelectorAll("[data-step]")];
  const max = Math.max(...items.map(i => +i.dataset.step));
  let n = max;
  const show = () => {
    items.forEach(i => i.style.opacity = +i.dataset.step <= n ? 1 : 0.08);
    fig.querySelector("[data-count]").textContent = `${n} / ${max}`;
  };
  fig.querySelector("[data-prev]").onclick = () => { n = Math.max(1, n - 1); show(); };
  fig.querySelector("[data-next]").onclick = () => { n = Math.min(max, n + 1); show(); };
  show();
})();
</script>
```

Put the stepper inside the figure's `<header>`. Starting at `max` keeps the full picture as the default.

## Filter by category

Legend items become toggles that dim everything not in their colour.

```html
<script>
(() => {
  document.querySelectorAll(".legend [data-filter]").forEach(btn => btn.addEventListener("click", () => {
    const canvas = btn.closest(".figure").querySelector(".canvas");
    const on = btn.classList.toggle("active");
    canvas.classList.toggle("focusing", on);
    canvas.querySelectorAll(".lit").forEach(el => el.classList.remove("lit"));
    if (on) canvas.querySelectorAll(`[data-color="${btn.dataset.filter}"], [data-color="${btn.dataset.filter}"] *`).forEach(el => el.classList.add("lit"));
  }));
})();
</script>
```

Mark each legend item `<span data-filter="blue" style="cursor:pointer">`.

## Toggle a layer

Show or hide one class of element (error paths, async edges) with a checkbox in the figure header.

```html
<label class="mono"><input type="checkbox" checked data-layer=".edge.dashed, .edge-label.async"> async</label>
<script>
(() => {
  document.querySelectorAll("[data-layer]").forEach(cb => cb.addEventListener("change", () => {
    cb.closest(".figure").querySelectorAll(cb.dataset.layer).forEach(el => el.style.display = cb.checked ? "" : "none");
  }));
})();
</script>
```
