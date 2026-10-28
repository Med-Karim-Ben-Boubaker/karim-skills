# video.json

The single source for the video's words and structure. `cv.py` reads it in every stage; the scenes read only their beat numbers from it.

```json
{
  "title": "How Raft reaches agreement",
  "eyebrow": "Backend guild · explainer",
  "footer": "Raft · backend guild",
  "meta": "6 chapters. One write followed through a leader crash.",
  "foot": "Narration voiced with Fish Audio Drama 3. Source: raft.github.io paper, sections 5.1–5.4.",
  "voice": { "model": "fish-audio/drama-3" },
  "pause": 0.45,
  "chapter_pause": 1.0,
  "theme": { "accent": "#2A5FA8" },
  "parts": [["Start", [1, 2]], ["The algorithm", [3, 4, 5]], ["Wrap-up", [6]]],
  "chapters": [
    {
      "id": "hook",
      "kicker": "Intro",
      "title": "Five servers, one crashes",
      "class": "dark",
      "beats": [
        "Five servers hold the same data. One of them crashes in the middle of a write.",
        { "text": "Who decides what the data is now? Raft's answer fits in check dot p y.",
          "say": "Who decides what the data is now? Raft's answer fits in check dot p y." }
      ]
    }
  ]
}
```

| Key | Required | Meaning |
|---|---|---|
| `title` | yes | Player page title and default footer text. |
| `eyebrow`, `meta`, `foot` | no | Player header line, summary under the title, credits line under the player. |
| `footer` | no | Left text in every scene's footer. |
| `voice.model` | no | OpenRouter speech model; default `fish-audio/drama-3`. `voice.voice` sets a voice id where the model has them. |
| `pause`, `chapter_pause` | no | Silence after each beat and after a chapter's last beat, in seconds. |
| `theme` | no | Overrides of the CSS tokens in `templates/scene.css` (`accent`, `ink`, `paper`, `blue`, `orange`, …), without the `--`. |
| `parts` | no | Chapter groups in the player's rail: `[name, [chapter numbers, 1-based]]`. |
| `chapters[].id` | yes | Scene file name (`scenes/<id>.html`) and the argument to rerun one chapter. Stable, kebab-case. |
| `chapters[].kicker`, `.title` | yes | Short label (footer, rail) and the chapter's headline in the player. |
| `chapters[].class` | no | `dark` or `accent` background for the whole scene. |
| `chapters[].beats` | yes | The narration, one entry per animation step. A string is shown and spoken; `{text, say}` shows `text` in captions and speaks `say`. |

**Beats are the clock.** Beat k's audio length sets when step k's elements enter (`data-s="k"`). Editing a beat's spoken text re-voices only that beat (clips are cached by model, voice and text), then `compose` re-times the chapter.

Use `say` whenever the spoken form differs from the written one: code tokens (`check.py` → "check dot p y"), abbreviations ("GStT" → "G S t T"), numbers read a particular way.
