# Writing the script

The script is `video.json`'s chapters and beats. It is a **lesson**, built on the teach skill's philosophy (`skills/tools/teach/SKILL.md`, "Philosophy" and "Lessons"): grounded in a mission, one tangible win per chapter, and built for storage strength, not fluency.

## Shape

| Chapter | Job | Typical beats |
|---|---|---|
| Hook | One concrete question the viewer cares about, from the running example. | 2–3 |
| Roadmap | The 3–5 core ideas, named, in one breath. | 1–2 |
| Core idea × 3–5 | One idea per chapter, each with a real example from the source material. | 3–5 |
| The problem today | Where the current system or practice breaks, shown on the running example. | 3–5 |
| The fix | What changes, in phases if there are any. | 3–6 |
| Walkthrough | The hook question solved step by step, before vs after. | 4–6 |
| Decisions or open questions | Only when the audience must act on them. | 2–4 |
| Recap | The 20 % to remember, one line per core idea. | 2–3 |
| Quiz | 3 retrieval questions; answer each in the next beat after a pause. | 6 |

80/20: cut any idea the viewer can't use. A chapter runs 40–120 s; a whole video 6–20 min.

## Beats

- A beat is 1–4 sentences, 8–30 s of speech, and drives one visible step on screen. Write the beat and its picture together: if nothing new appears, merge the beat into its neighbour.
- Spoken English: short sentences, active voice, concrete nouns. Numbers and names from the source, never invented.
- **One running example** through the whole video (one real plan, one real request, one real bug), so every idea lands on the same object.
- **Real material over abstraction:** a quote from the meeting, the actual function, the real document page, the measured number.
- **Foreign or domain terms:** on screen, the term with its English translation right after it in parentheses, e.g. "Festsetzung (binding provision)". In narration, say the term and its translation once, then use one of them consistently.
- **Spoken form:** code tokens, file names, abbreviations and symbols go in the beat's `say` (`check.py` → "check dot p y", `§ 3` → "section three").
- **Quiz:** ask, leave the viewer a beat to think ("Pause and answer."), then answer in the next beat with the reason.

## Before voicing

Verify every factual claim against a primary source or the real data, and every code reference against the code (`file:line`). Claims from general knowledge are the ones that turn out wrong: in the zoning-plan video, real plans had 7 parts and §§, not the 4 parts and numbered points general knowledge said.
