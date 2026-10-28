# Publishing the player

`cv.py package` writes `out/player.html` (chapters, transcript cues and parts embedded), `out/media/chNN.mp4` + `chNN.jpg`, and `out/publish.json`: the media files split into batches that fit one publish.

Limits that shaped it: each binary file ≤ 15 MB (package re-encodes a chapter at a higher CRF until it fits), ≤ 64 MB per publish call, `.vtt` is not a served type (the player builds captions in the page from the embedded cues with `addTextTrack` + `VTTCue`).

Steps:

1. Load the `artifact-design` skill if this conversation hasn't (the player already follows its contract; the skill is needed for the publish rules).
2. Publish `out/player.html` with `files` set to the first batch from `publish.json`, each entry mapping `media/<file>` to `out/media/<file>`, plus `icon: "video"` and a one-sentence description.
3. Publish the same `file_path` again with each further batch in `files`, until every batch is up. Files left out of a later publish are kept.
4. Open the artifact link once and play the first chapter: video loads, subtitles show, transcript line highlights.

To fix one chapter after publishing: rerun its stages with its id, then republish with only that chapter's two files in `files`.

The Motion artifact type is not a host for this: it is for animations written as code inside the artifact, has no audio asset type, and won't load films over 300 s.
