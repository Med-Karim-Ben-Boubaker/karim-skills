# Agent instructions

## Skill naming

Skills are functions written in English: the user and other skills call them by name. Name each one like a function, verb first, in the imperative: `<verb>-<object>`, so the call reads as an instruction (`implement-spec`, `grill-with-docs`, `improve-codebase-architecture`).

- Principles keep the `principle-` prefix, then an imperative: `principle-keep-it-simple`, `principle-fix-root-causes`.
- A noun name is kept only for a term of art clearer than any verb phrase (`tdd`), a reference skill that other skills load but nothing calls (`codebase-design`), or a name the user chose to keep (`wait-what`).
- The folder name, the `name:` field, and the path in `.claude-plugin/plugin.json` are the same string. Every skill sits directly under `skills/<name>/`, never in a group folder: Codex finds skills only one level deep. Its group goes in `skills/README.md`.

When you rename a skill, update every place that calls it: `/name` commands, lines that call the Skill tool with `"name"`, README links, `plugin.json`, and `display_name` in its `agents/openai.yaml`. For a skill forked from `mattpocock/skills`, record the upstream name in `UPSTREAM.md` so upstream changes still merge.
