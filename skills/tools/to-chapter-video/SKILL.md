---
name: to-chapter-video
description: "Turn a detailed prompt into a narrated, animated explainer video split into chapters, published as a chapter-player page with subtitles and a synced transcript. Use when the user wants a video, video course, animated explainer or narrated walkthrough of a system, codebase, domain or concept."
---

# To chapter video

Turns an explanation into a **lesson on video**: a script of beats, each voiced by OpenRouter text-to-speech and shown as one animated step of an HTML scene, rendered frame-exact by HyperFrames and published as a chapter player. The pipeline is `scripts/cv.py`; every stage is idempotent and reruns alone, and naming chapter ids limits a stage to those chapters.

Work in a project folder (default: `<scratchpad>/<video-slug>/`, or where the user says). Run long stages per the user's watchable-commands rule: log to a file, hand over the `tail -f` command, read the log with `tail`/`grep`.

## Steps

1. **Preflight.** `python3 <skill>/scripts/cv.py preflight <project>` (create the folder first). It checks `OPENROUTER_API_KEY`, Node ≥ 22, ffmpeg, and turns HyperFrames telemetry off. When the key is missing, ask the user to export it in their shell profile and say they should never paste it in chat; never read `.env` files to find it. Done when preflight exits 0.

2. **Brief.** Run a short grilling (call the Skill tool with "grilling"), capped at two rounds, on what the prompt leaves open:
   - the **mission**: who watches and what they can do afterwards;
   - the **running example**: one real object followed through the whole video;
   - the sources: meetings, code, documents, data;
   - length;
   - language and domain terms that need translations.

   Write the answers to `<project>/brief.md`. Done when every item has an answer or a stated default.

3. **Ground.** Read the sources and collect the material each beat will show: quotes with who and when, code with `file:line`, real document pages and crops into `assets/`, measured numbers. For a codebase, read its blueprint READMEs first, then call the Skill tool with "how" for a subsystem you can't read directly. Done when every claim the script will make traces to a source or to real data, and none rests on general knowledge alone.

4. **Script.** Write `video.json` per [references/video-json.md](references/video-json.md), shaped by [references/script.md](references/script.md). Show the user the chapter list (kicker, title, beat count, seconds estimate) in one short message and carry on; their changes come back as edits. Done when each chapter has its job from the shape table and every beat names what appears on screen.

5. **Voice.** `cv.py voice <project>` voices only new or changed beats and logs the cost. Done when it reports 0 clips left.

6. **Scenes.** Write `scenes/<id>.html` per chapter, per [references/scenes.md](references/scenes.md). For more than about 6 chapters, hand groups of chapters to subagents with the brief, `video.json`, `assets/` and `references/scenes.md`. Then run `cv.py compose <project>` and `cv.py check <project>`; fix every lint error and layout issue. Done when check exits 0 for every chapter.

7. **Render.** `cv.py render <project> [ids]`, then read every contact sheet in `build/check/<id>.jpg`; each one shows the last frame of each beat. Fix overflow, crowding, unreadable text and elements entering on the wrong beat, then re-run compose, check and render for those chapters only. Done when every sheet reads cleanly at a glance.

8. **Package and publish.** `cv.py package <project>`, then publish per [references/publish.md](references/publish.md). Done when the artifact link plays the first chapter with subtitles, and the user has the link, the total length and the voice cost.

## Rules

- Every animation runs on the chapter's GSAP timeline, through the data attributes or `tl`/`at`/`driven`. That is what keeps picture and narration in sync.
- Domain or foreign terms appear on screen with their English translation in parentheses, e.g. "Festsetzung (binding provision)".
- Real material over abstract boxes: the actual page, the actual function, the actual quote.
- Keep `video.json` as the single source of words. Scenes reference beats by number and never repeat narration as on-screen paragraphs.
