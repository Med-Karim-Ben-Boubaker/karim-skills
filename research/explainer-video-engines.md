# Explainer video engines for `to-chapter-video`

Researched 2026-10-25. Confidence tiers follow `~/.claude/skills/research/EPISTEMICS.md`: **Verified** (primary source states it), **Inferred** (follows from verified facts; chain shown), **Guess**, **Unknown**. Engine facts come from three explorer passes; facts about our pipeline come from reading `/tmp/handoff-explainer-skills/tools/` and `HANDOFF.md`.

## Answer

Keep our pipeline and extend it. Do not adopt Remotion, Revideo or Manim. Change the scene runtime from CSS keyframes to a **paused GSAP timeline registered on `window.__timelines`**. That is the timing contract HyperFrames uses ([repo](https://github.com/heygen-com/hyperframes), Verified). With it, `record.py` seeks GSAP and WAAPI to the same time on every frame, and any JS animation built on GSAP (SVG diagram steps, counters, morphs) becomes deterministic. The step/at-share model, per-beat TTS, ffmpeg muxing, `split.py` and the player all stay. Because scenes would then follow HyperFrames' contract, run a 30-minute spike rendering one beat with `npx hyperframes render`. If it is deterministic and handles our per-beat audio, swap our recorder for it without rewriting the scenes (Inferred: the scene format is the same contract). Remotion's license is a risk while company size is unknown. It also needs a React rewrite. Revideo is pre-1.0 and has a small community. Manim would mean leaving HTML/JS completely, which is the opposite of what the user asked for. Arbitrary rAF-driven code (D3 transitions, canvas, Three.js) needs a virtual clock on top. Add that only when a scene needs it.

## Comparison

| Criterion | Ours today | Ours + GSAP seek (+ optional virtual clock) | HyperFrames | Remotion | Revideo | Manim CE + manim-voiceover |
|---|---|---|---|---|---|---|
| Headless CLI to MP4 | Yes (`record.py`) | Yes | Yes, `npx hyperframes render` (Verified) | Yes, `npx remotion render` (Verified) | Yes, `renderVideo()` API (Verified) | Yes (Inferred: Manim's CLI; not in findings) |
| Deterministic frames | Yes for WAAPI/CSS (seeks `currentTime`) | Yes for WAAPI + GSAP (Inferred); rAF code only with a virtual clock | Claimed, with golden baselines (Verified claim, not run) | Unknown | Inferred (time-driven generators) | Inferred (frame-stepped renderer) |
| Per-beat voiceover timing | Yes: beat audio length sets `dur`; `data-at` is a share of it | Same | `<audio data-start data-duration>` (Verified); per-beat fit Unknown | `calculateMetadata` sets `durationInFrames`; `<Audio>` + `<Sequence>` (Verified) | `Audio` node; sync via `waitFor` (Inferred) | `self.voiceover(...)` with `tracker.duration` (Verified), the best fit of all |
| JS animation | No: rAF code is not stepped | GSAP yes; D3/canvas/Three via virtual clock | GSAP (Verified); CSS/WAAPI Unknown | React per frame | TypeScript generators | Python only |
| SWE diagram animation | Hand-written SVG + `draw` keyframes | GSAP on SVG from Mermaid/our layout (Inferred) | Same as ours (HTML/SVG) | React SVG | Canvas nodes | Manim primitives, no Mermaid |
| License | Ours | Ours; GSAP free (Verified) | Apache-2.0 (Verified) | Paid above 3 employees (Verified) | MIT (Verified) | MIT (Verified) |
| Maturity | One real 16.6-min video shipped | Same | v0.8.198, created 2026-03-10, very active (Verified) | v4.0.538, 67k stars (Verified) | 0.11.0, pre-1.0, 4.1k stars (Verified) | Manim v0.22.0; voiceover v0.4.0, 321 stars (Verified) |
| Linux install | Playwright + system Chrome + ffmpeg (works today) | + GSAP script | Node 22+, FFmpeg (Verified) | Chrome Headless Shell auto-downloaded + apt libs (Verified) | Node ≥22.12; ships ffmpeg (Verified) | LaTeX/cairo/pango: Unknown |
| Agent driving | Our scripts | Our scripts | Built for agents; CLI, Claude Code plugin, skills (Verified/secondary) | 12 official Agent Skills, Claude Code plugin; MCP deprecated (Verified) | README says Claude can write scenes; no skills (Verified) | Community MCPs, stale or tiny (Verified) |
| Porting our scenes | None | Rewrite one ~30-line runtime (`enter()`) (Inferred) | Small if CSS seeks, else same as GSAP port (Inferred) | Full rewrite to React (Inferred) | Full rewrite to generators (Inferred) | Full rewrite to Python (Inferred) |

## Option: keep our pipeline as is

- **How it works (read from source):** `scenes2.py` writes one HTML page per scene. Elements carry `data-s` (step), `data-a` (entrance) and `data-at` (share of the beat's narration). A ~30-line inline script turns these into CSS `animation` declarations and exposes `window.__W` (motion windows). `record.py` opens `?step=N&dur=<speech>`, pauses `document.getAnimations()`, sets `currentTime` per frame at 30 fps, screenshots only inside motion windows, and pipes JPEGs and the beat MP3 into ffmpeg. Four beats record in parallel.
- **Strengths:** sync is exact by construction, it is proven on a 16.6-min, 15-chapter video, and it costs nothing to keep.
- **Gap:** rAF-driven JS (GSAP, D3, canvas, Three.js) is not stepped (main-session finding). That blocks the user's "JavaScript animation code in scenes" requirement. Scenes are hand-written Python string templates (`scenes2.py`, 526 lines), so authoring cost is high. HANDOFF §"Suggested skill design" already names layout templates as the main design work.

## Option: extend ours (GSAP seek, then a virtual clock)

- **Step 1, GSAP seek:** build each step's entrances as tweens on one paused `gsap.timeline()` and register it on `window.__timelines`. `record.py` then calls `tl.seek(t)` (or sets total time) next to the WAAPI `currentTime` loop. Inferred: a paused timeline seeked to an absolute time is deterministic, and HyperFrames relies on exactly this to render ([repo](https://github.com/heygen-com/hyperframes), Verified). GSAP is free for everyone ([gsap.com/licensing](https://gsap.com/licensing/), Verified). A forum post reports a restriction on no-code tools that compete with Webflow. That source is secondary and the terms of use were not read. It is unlikely to apply to an internal explainer pipeline (Guess).
- **Step 2, virtual clock (only if needed):** override `Date`, `performance.now`, `requestAnimationFrame`, `setTimeout` and `setInterval` through `page.add_init_script`, the timesnap technique (Verified, timesnap README). timesnap/timecut themselves are stale (last pushes 2024-01 and 2023-07) and warn that CSS transitions/animations "will likely not render as intended" (Verified). So keep WAAPI seeking for CSS and use the virtual clock only for rAF code. Inferred: the two coexist, because WAAPI `currentTime` is set explicitly rather than read from the clock.
- **Motion windows:** GSAP tweens report start and duration, so `__W` can be derived from the timeline (Inferred). That keeps the "screenshot only while moving" speed-up.
- **Cost:** rewrite the `enter()` runtime and add a seek call in `record.py`. The HTML element attributes do not change (Inferred from reading `scenes2.py`).

## Option: HyperFrames (heygen-com/hyperframes)

- **Verified ([repo](https://github.com/heygen-com/hyperframes)):** Apache-2.0. "Write HTML. Render video. Built for agents." "The renderer seeks each frame in headless Chrome and encodes the result with FFmpeg." Timing comes from a paused GSAP timeline on `window.__timelines`. Audio is set with `<audio data-start data-duration data-track-index data-volume>`. It needs Node 22+ and FFmpeg. It claims "same input, same frames, same output" with golden baselines. Created 2026-03-10, v0.8.198 released 2026-10-25, 71,972 stars (GitHub API).
- **Agent tooling (secondary):** `npx hyperframes init|render|preview`, `claude plugin install hyperframes@hyperframes`, `npx skills add heygen-com/hyperframes`.
- **Fit:** architecturally it is our pipeline productized: HTML scenes, headless Chrome seeking, ffmpeg. It adds GSAP, which the user wants.
- **Risks:** pre-1.0 and seven months old (Verified dates). Whether it seeks CSS/WAAPI animations is Unknown. Whether it renders one MP4 per beat or a whole timeline with audio placed by `data-start` is Unknown, and that decides how per-beat TTS plugs in. Its determinism claim has not been run.

## Option: Remotion

- **Verified:** CLI `npx remotion render <entry> <Comp> out.mp4 --props=props.json` ([docs](https://www.remotion.dev/docs/cli/render)). `calculateMetadata` sets `durationInFrames` from props ([docs](https://www.remotion.dev/docs/calculate-metadata)), so beat-audio-driven length is first-class. `getMediaMetadata()` replaces the deprecated `getAudioDurationInSeconds`. `@remotion/captions` is MIT. There are 12 official Agent Skills and a Claude Code plugin ([docs](https://www.remotion.dev/docs/ai/skills)). The hosted MCP is deprecated and shuts down no earlier than 2026-08-31 ([docs](https://www.remotion.dev/docs/ai/mcp)). It is the most mature option: 67,373 stars, v4.0.538 on 2026-10-22.
- **License (Verified, [LICENSE.md](https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md)):** free for individuals, for-profit companies with up to 3 employees, non-profits and evaluation; a Company License otherwise. "In Remotion 5.0, the license will slightly change." Vendor pricing ([remotion.pro/license](https://www.remotion.pro/license)): Creators $25/mo per seat, Automators $0.01 per render with a $100/mo minimum, Enterprise from $500/mo. Inferred: an agent pipeline falls under Automators, so it would cost at least $100/mo if the company has more than 3 employees.
- **Cost to us:** scenes become React components, so every scene and the runtime are rewritten (Inferred). Determinism is Unknown (frame-based by design, but not verified in the docs).

## Option: Revideo (midrender/revideo)

- **Verified:** headless `renderVideo()` (`@revideo/renderer`, Puppeteer + Vite, ships its own ffmpeg). Time-driven `Audio` node. MIT. 0.11.0 on npm 2026-07-10, last commit 2026-07-15, 4,143 stars, no GitHub releases, Node ≥22.12. README: "A scene is plain TypeScript, so Claude or Codex can produce one from a prompt." No skills or MCP.
- **Inferred:** voiceover sync is manual (`yield* waitFor(duration)`). Scenes are canvas nodes, not DOM, so our HTML scenes and Mermaid SVG do not carry over.
- **Motion Canvas**, its parent, has no headless CLI (render is triggered from the editor over Vite HMR, Verified from source). Its `@motion-canvas/ffmpeg` is GPLv3 and its last release was 2024-12-14. Ruled out.

## Option: Manim CE + manim-voiceover

- **Verified:** `with self.voiceover(text=...) as tracker: self.play(..., run_time=tracker.duration)` (quickstart), the cleanest voice-driven timing of any option. Whisper-based per-word bookmarks exist (syntax Unknown). manim-voiceover is MIT, v0.4.0 2026-06-14. Manim v0.22.0 2026-10-08.
- **TTS:** sources disagree. The README lists Gemini, Azure, gTTS and pyttsx3. The docs list Recorder, Azure, Coqui, gTTS, OpenAI, pyttsx3 and ElevenLabs. An OpenRouter service would be a custom subclass (Unknown: base class not read).
- **Against:** Python, not JavaScript, which contradicts the user's explicit requirement. There is no Mermaid/HTML path, so C4 and sequence diagrams would be hand-built from primitives (Inferred). Its MCP servers are stale or tiny (Verified). Linux deps (LaTeX, cairo, pango) are Unknown.

## SWE diagram animation

- **Verified/secondary:** no mature Mermaid step-animation project was found. A "mermaid-to-gif" skill (secondary, [claudeskills.info](https://claudeskills.info/skills/zc277584121/marketing-skills/mermaid-to-gif/)) uses Playwright + `stroke-dashoffset` + FFmpeg, which is our `draw` entrance. excalidraw-animate and excanim exist (secondary). D2 is MPL-2.0; its animation support is Unknown.
- **Inferred approach:** render Mermaid to SVG in the scene page, tag nodes and edges with steps (by Mermaid's generated ids or a label map), then animate per beat with GSAP: nodes pop, edges draw, sequence messages slide, state transitions highlight. This needs the GSAP seek from the recommended option. It works the same under HyperFrames. A layout check is still needed (HANDOFF: overflow hit twice).

## Patterns to copy (Code2Video, TheoremExplainAgent)

- **Planner / Coder / Critic split** (Code2Video, MIT, ICML 2026, Verified from repo). The planner writes beats and a scene spec. The coder writes the scene. The critic does "layout refinement with anchors". For us, the critic checks the last frame of each scene for overflow. That matches the contact-sheet gotcha in HANDOFF.
- **Render, then fix with vision** (TheoremExplainAgent `--use_visual_fix_code`: "Use VLM to fix code with rendered visuals", Verified flag). Render one still per step, have Claude look at it, and patch the scene before the full recording.
- **Stage flags** (`--only_plan`, `--only_render`, `--max_scene_concurrency`, Verified). Our stages are already rerunnable (`record.py <beats>`, `--assemble`). Keep one entry point with a flag per stage.
- **Per-scene render and retry**: a failed scene does not fail the video. `record.py` already records per beat.
- **Local TTS fallback** (TheoremExplainAgent uses Kokoro, Verified). OpenRouter lists `hexgrad/kokoro-82m` (HANDOFF), a cheap fallback voice.
- Not found: how either project syncs audio to animation (Unknown).

## Recommended architecture for `to-chapter-video`

Stages are one script each, idempotent and cached, as today:

1. **Grill + plan.** A short grilling on audience, the one question, real examples and diagrams wanted. Then write `beats.json` (chapters → beats of 1–4 sentences, pedagogical structure from HANDOFF §5) and `scenes.json`: per scene a layout template (title, two-column, doc+crop, flow, cards, timeline, quote, quiz, **diagram**) and elements with `step`, `enter`, `at`.
2. **Voice.** `voice.py`: OpenRouter `POST /api/v1/audio/speech`, default `fish-audio/drama-3`, model as a parameter, one MP3 per beat, skip if cached. Key from `OPENROUTER_API_KEY`, never printed.
3. **Scenes.** `scenes.py` renders `scenes.json` through layout templates to HTML. The runtime builds one paused GSAP timeline per page from the step/at attributes, registers it on `window.__timelines`, and exposes `__W` derived from it. A scene may add custom JS that appends to that timeline. Diagram layouts take Mermaid source plus a step map.
4. **Check.** Render the last frame of each step as a still, build a contact sheet, and have Claude review it (vision-fix loop). Fix scenes before recording.
5. **Record.** `record.py` as today, plus a GSAP seek per frame. The virtual-clock init script is opt-in per scene (`"clock": "virtual"`) for D3, canvas or Three code.
6. **Chapters + player.** `split.py` and `player.template.html` unchanged. Publish in batches of at most 64 MB, each file under 15 MB.

Decision gate: if the HyperFrames spike (below) passes, step 5 becomes `npx hyperframes render` per beat and steps 1–4 and 6 stay.

## Spike result (2026-10-25): HyperFrames v0.8.198

One 40.6 s composition rendered with `npx hyperframes@0.8.198 render . -o out.mp4 --fps 30` on this Linux machine (Node 24, ffmpeg 8). It used two real narration beats (`s02-01.mp3`, `s02-02.mp3`), a CSS keyframe box, a GSAP box, a `requestAnimationFrame` box with a `performance.now()` clock, and a Mermaid flowchart rendered asynchronously whose nodes and edges were added to the GSAP timeline afterwards. All results below are **Verified** by frame extraction and ffmpeg measurements.

| Question | Result |
|---|---|
| CSS keyframes seeked without porting? | Yes. At t = 2.0 s the CSS box sits exactly where the GSAP box does (mid-tween). |
| GSAP timeline | Yes, exact. |
| rAF / `performance.now()` code | Yes. The clock read 0.50 / 2.00 / 3.50 at those frames, so HyperFrames virtualizes time. `hyperframes lint` still flags it as an error (`requestanimationframe_in_composition`, `non_deterministic_code`). |
| Mermaid async render, tweens added after | Yes. First node at 27 s, all nodes and edges by 37 s, as scheduled. |
| Per-beat audio via `<audio id data-start data-duration>` | Yes. Speech at -18 dB and -23 dB, the 26.49–26.6 s gap at -68 dB. Audio without an `id` is silent (lint error `media_missing_id`). |
| Deterministic | Yes. Two renders gave bit-identical frames (same `framemd5` hash, PSNR inf). |
| Speed | 38 s for 40.6 s of video (3 workers, screenshot capture). First run took 4 m 17 s wall time, including one-time setup. |
| Telemetry | On by default; disabled with `hyperframes telemetry disable`. |

**Consequence:** HyperFrames can replace `record.py` without porting the scenes. It also adds a linter (`hyperframes lint`) and a layout inspector (`hyperframes inspect`) usable as skill gates.

## What we don't know

| Open question | Searched | Who/what can answer |
|---|---|---|
| Does HyperFrames seek CSS/WAAPI animations, or only GSAP? | HyperFrames repo page | 30-min spike: one existing scene with CSS entrances plus one GSAP tween, then `npx hyperframes render`, then compare frames |
| Can HyperFrames render one MP4 per beat with our MP3, or must it render a whole timeline with `data-start` audio? | Repo page, audio attributes | Same spike; read `npx hyperframes render --help` |
| Is HyperFrames' determinism real on this machine? | Claim with golden baselines, not run | Render the same beat twice, then `cmp` or a frame hash |
| Is Remotion frame-deterministic? | Remotion docs | Only matters if Remotion is reconsidered |
| User's company size (Remotion license) | n/a | The user |
| Do GSAP's terms of use restrict this use? | gsap.com/licensing (free); one secondary forum post | Read GSAP's standard no-charge license / terms page |
| Does a virtual clock coexist with WAAPI seeking in Chrome? | timesnap README (CSS caveat) | Spike: one D3 transition plus one CSS entrance on a page, rendered through `record.py` with the init script |
| Reliable mapping from Mermaid source to SVG element ids per diagram type (C4, sequence, class/ER, state) | No mature Mermaid step-animation project found; mermaid-to-gif skill (secondary) | Spike: render one diagram of each type and inspect the ids |
| D2 animation support | D2 found (MPL-2.0); animation not checked | D2 docs |
| manim-voiceover OpenRouter integration and bookmark syntax | README and docs (they disagree on TTS list) | Only if Manim is reconsidered; read the `SpeechService` base class |
| How Code2Video / TheoremExplainAgent sync audio to animation | Both repos' READMEs | Read their render code |
| Remotion 5.0 license change | LICENSE.md header only | Watch the Remotion release notes |
