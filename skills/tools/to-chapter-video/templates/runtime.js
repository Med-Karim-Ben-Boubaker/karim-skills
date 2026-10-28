// Scene runtime: turns the chapter's data attributes into one paused GSAP timeline that HyperFrames seeks per frame.
// window.__VIDEO = {beats: [{start, dur}], total} is injected by compose.py; beat k (1-based) is beats[k-1].
(() => {
  const V = window.__VIDEO;
  const tl = gsap.timeline({ paused: true });
  tl.set({}, {}, V.total);
  window.tl = tl;

  const beat = k => V.beats[Math.min(Math.max(k, 1), V.beats.length) - 1];
  // Seconds into the chapter at `share` (0..1) of beat k's narration.
  const at = (k, share = 0) => beat(k).start + share * beat(k).dur;
  window.at = at;

  // Calls fn(p), p from 0 to 1, as the timeline passes through [start, start+len]. Use it for D3, canvas or any
  // code that draws from a number: it stays frame-exact because GSAP, not the wall clock, drives it.
  window.driven = (k, share, len, fn) => {
    const o = { p: 0 };
    fn(0);
    tl.fromTo(o, { p: 0 }, { p: 1, duration: len, ease: "none", immediateRender: false, onUpdate: () => fn(o.p) }, at(k, share));
  };

  const EASE = "power3.out";
  const PRESETS = {
    rise: { from: { autoAlpha: 0, y: 46 } },
    fade: { from: { autoAlpha: 0 } },
    pop: { from: { autoAlpha: 0, scale: 0.82 }, ease: "back.out(1.8)" },
    slideL: { from: { autoAlpha: 0, x: -90 } },
    slideR: { from: { autoAlpha: 0, x: 90 } },
    zoomin: { from: { autoAlpha: 0, scale: 1.35 } },
    growx: { from: { scaleX: 0, transformOrigin: "left center" }, ease: "power2.inOut", len: 1.2 },
    growy: { from: { scaleY: 0, transformOrigin: "center bottom" }, ease: "power2.inOut", len: 1.2 },
    stamp: { from: { autoAlpha: 0, scale: 2.2 }, ease: "back.out(1.4)", len: 0.6 },
  };

  function enter(el, name, t, len) {
    if (name === "draw") {
      const L = el.getTotalLength();
      gsap.set(el, { strokeDasharray: L, strokeDashoffset: L });
      tl.to(el, { strokeDashoffset: 0, duration: len || 1.6, ease: "power2.inOut" }, t);
      return t + (len || 1.6);
    }
    if (name === "type") {
      const full = el.textContent;
      const o = { n: 0 };
      el.textContent = "";
      gsap.set(el, { autoAlpha: 0 });
      tl.set(el, { autoAlpha: 1 }, t);
      const d = len || Math.min(4, full.length * 0.03);
      tl.to(o, { n: full.length, duration: d, ease: "none", onUpdate: () => { el.textContent = full.slice(0, Math.round(o.n)); } }, t);
      return t + d;
    }
    if (name === "count") {
      const to = +el.dataset.to, dec = +(el.dataset.dec || 0), o = { v: 0 };
      el.textContent = (0).toFixed(dec);
      gsap.set(el, { autoAlpha: 0 });
      tl.set(el, { autoAlpha: 1 }, t);
      const d = len || 1.4;
      tl.to(o, { v: to, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = o.v.toFixed(dec); } }, t);
      return t + d;
    }
    const p = PRESETS[name] || PRESETS.rise;
    const d = len || p.len || 0.8;
    tl.from(el, { ...p.from, duration: d, ease: p.ease || EASE, immediateRender: true }, t);
    return t + d;
  }

  function pulse(el, t) {
    tl.fromTo(el, { boxShadow: "0 0 0 0 rgba(42,95,168,.55)" }, { boxShadow: "0 0 0 26px rgba(42,95,168,0)", duration: 1.3, ease: "power1.out", immediateRender: false }, t);
  }

  // data-show="a-b": the element exists only during beats a..b (display:none outside, so it frees its space).
  document.querySelectorAll("[data-show]").forEach(el => {
    const [a, b] = el.dataset.show.split("-").map(Number);
    const last = b || a;
    gsap.set(el, { display: "none" });
    tl.set(el, { display: "" }, at(a));
    if (last < V.beats.length) tl.set(el, { display: "none" }, at(last + 1));
  });

  // data-s="k": enters during beat k with preset data-a at data-at (share of the beat), else staggered 0.15 s.
  const order = {};
  document.querySelectorAll("[data-s]").forEach(el => {
    const k = +el.dataset.s;
    const t = el.dataset.at !== undefined ? at(k, +el.dataset.at) : at(k) + 0.15 * (order[k] = (order[k] ?? -1) + 1);
    const end = enter(el, el.dataset.a || "rise", t, el.dataset.len ? +el.dataset.len : 0);
    if (el.dataset.now !== undefined) pulse(el, end);
  });

  // .kb: slow push-in over the beats the element is visible in (its data-show range, else the whole chapter).
  document.querySelectorAll(".kb").forEach(el => {
    const host = el.closest("[data-show]");
    const [a, b] = host ? host.dataset.show.split("-").map(Number) : [1, V.beats.length];
    const t0 = at(a), t1 = at(b || a, 1);
    tl.fromTo(el, { scale: 1 }, { scale: 1.09, duration: t1 - t0, ease: "none", immediateRender: false }, t0);
  });

  // Mermaid diagrams: <pre class="diagram" data-reveal='{"nodeName": "k" | "k@share"}'>graph source</pre>.
  // Nodes appear at their beat; an edge appears once both its ends are visible. Unlisted nodes show from the start.
  // data-seq="k" on a sequenceDiagram reveals its messages one by one across beat k instead.
  const diagrams = [...document.querySelectorAll("pre.diagram")];
  if (diagrams.length) {
    mermaid.initialize({ startOnLoad: false, theme: document.querySelector("#root.dark") ? "dark" : "neutral",
      fontFamily: "IBM Plex Sans", flowchart: { useMaxWidth: false }, sequence: { useMaxWidth: false } });
    // Fonts first: Mermaid sizes node boxes from measured text, and a fallback font clips the labels.
    window.__diagramsReady = document.fonts.ready.then(() => Promise.all(diagrams.map(async (pre, i) => {
      const { svg } = await mermaid.render(`dg${i}`, pre.textContent);
      const box = document.createElement("div");
      box.className = "diagram";
      for (const a of pre.attributes) if (a.name.startsWith("data-")) box.setAttribute(a.name, a.value);
      box.innerHTML = svg;
      pre.replaceWith(box);
      reveal(box);
    })));
  }

  function when(spec) {
    const [k, s] = String(spec).split("@");
    return at(+k, s ? +s : 0);
  }

  function reveal(box) {
    const map = box.dataset.reveal ? JSON.parse(box.dataset.reveal) : {};
    const names = Object.keys(map).sort((a, b) => b.length - a.length);
    const nameOf = id => names.find(n => new RegExp(`(^|[-_])${n}([-_]|$)`).test(id));
    const shown = {};
    box.querySelectorAll("g.node, g.cluster").forEach(g => {
      const n = nameOf(g.id);
      if (!n) return;
      shown[n] = when(map[n]);
      gsap.set(g, { autoAlpha: 0 });
      tl.fromTo(g, { autoAlpha: 0, scale: 0.85, transformOrigin: "center", transformBox: "fill-box" },
        { autoAlpha: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }, shown[n]);
    });
    const edges = box.querySelectorAll("path[id^='L'], path[id*='-L_'], .edgeLabel, path.relation, path.transition");
    edges.forEach(e => {
      const id = e.id || e.closest("[id]")?.id || "";
      const ends = names.filter(n => new RegExp(`(^|[-_])${n}([-_]|$)`).test(id));
      const t = ends.length ? Math.max(...ends.map(n => shown[n] ?? 0)) + 0.4 : null;
      if (t === null || t <= 0.4) return;
      gsap.set(e, { autoAlpha: 0 });
      tl.to(e, { autoAlpha: 1, duration: 0.5, ease: "none" }, t);
    });
    if (box.dataset.seq) {
      const k = +box.dataset.seq;
      const msgs = [...box.querySelectorAll(".messageLine0, .messageLine1")];
      const texts = [...box.querySelectorAll(".messageText")];
      msgs.forEach((m, i) => {
        const t = at(k, 0.05 + 0.85 * i / Math.max(msgs.length, 1));
        const parts = [m, texts[i]].filter(Boolean);
        gsap.set(parts, { autoAlpha: 0 });
        tl.to(parts, { autoAlpha: 1, duration: 0.4 }, t);
      });
    }
  }

  // Register only once the async parts (fonts, diagrams) have added their tweens: HyperFrames treats a registered
  // timeline as ready to capture.
  (window.__diagramsReady || document.fonts.ready).then(() => {
    window.__timelines = window.__timelines || {};
    window.__timelines.root = tl;
  });
})();
