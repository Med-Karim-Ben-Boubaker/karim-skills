---
name: blueprint
description: "Write or update a folder's README.md as an engineering blueprint: Mermaid diagrams (C4, data flow, sequence, class, state), minimal text, facts, assumptions, ADR links, and up/down links tying parent and child READMEs into one tree. Use when creating or editing a README.md in a codebase, or after a change alters a folder's modules, interface, or data flow. For AGENTS.md, CLAUDE.md, or skills, use writing-for-agents."
---

# Blueprint

A folder's `README.md` is its **blueprint**: a human reads it instead of the code. Diagrams carry the structure; text carries only what a diagram can't: facts, assumptions, constraints, and links to decisions. Blueprints live in the folders they describe and link into a **tree** that mirrors the folder tree. Nothing is centralised in `docs/`.

The check script is the source of truth for the tree rules: `scripts/check_readmes.py` in this skill's folder.

## Steps

1. **Scope.** List the folders to write or update. A folder earns a README when it has a seam: a public interface other code calls. Small helper folders, `__pycache__`, and fixtures don't. Work **bottom-up**: leaves first, then each parent, because a parent's diagram summarises its children. Done when every folder in scope is listed in bottom-up order.
2. **Read the code.** For each folder, collect what the diagrams will show: modules and who imports whom, the core data types, the main scenario's calls, any lifecycle states, and the ADRs in the area (`docs/adr/`, local `adr/` folders). For a subsystem too big to read directly, call the Skill tool with "how". Done when every box and arrow you plan to draw traces to a file, an import, or a call.
3. **Write the blueprint** with the skeleton below, picking diagrams by the question each answers.
4. **Connect.** Up link on the first line. In the parent: the child's folder name as a node in a diagram, and a row in the links table under that diagram. A type or rule shared by siblings goes in their lowest common parent.
5. **Check.** Run `python3 <this skill>/scripts/check_readmes.py <repo or subtree root>`. Done when it exits 0 with no warnings for the folders in scope.

## Skeleton

```markdown
↑ [<parent folder>](../README.md)

# <folder name>

<1–3 sentences: what this folder does and for whom.>

## Where it sits
<C4 component diagram or data flow diagram: this folder as one box, its neighbours upstream and downstream.>

## Parts
<Module dependency flowchart; child folders as nodes, named exactly as the folders.>

| Part | What it does |
|---|---|
| [<child>](<child>/README.md) | <one line> |
| `<module>.py` | <one line> |

## Core types
<classDiagram of the main data shapes only.>

## Main flow
<sequenceDiagram or data flow diagram for the one central scenario.>

## Facts and assumptions
- <a fact the code relies on, a constraint, a known limit; ≤ 10 bullets>

## Decisions
- [ADR-NNNN <title>](<relative path>)
```

Drop any section that answers no question a newcomer would ask. The root README of a repo is the C4 context level: the system, its users, and the external systems; its children are the top-level packages.

## Choosing diagrams

| Question | Diagram | Mermaid |
|---|---|---|
| Where does this sit in the system? | C4 context / component | `flowchart`, `C4Context` |
| What depends on what? | Module dependency | `flowchart` |
| How does data get transformed? | Data flow diagram | `flowchart LR` |
| How is one request handled? | Sequence | `sequenceDiagram` |
| What are the core types? | Class / schema | `classDiagram` |
| What states can this be in? | State machine | `stateDiagram-v2` |
| What is stored? | Entity-relationship | `erDiagram` |
| What runs where? | Deployment | `architecture-beta`, `flowchart` |

Diagram rules:

- **Name nodes after the code**: folder, module, class, and function names exactly as written. The check matches child folder names against the parent's diagrams.
- **One level per README.** A child is one box in its parent; its internals live in its own README.
- **Keep each diagram under about 15 nodes.** Split a bigger one, or push the detail down to a child README.
- **Links go in tables**, since GitHub renders Mermaid without `click` links.

## Text rules

- Short, direct sentences; at most 3 per paragraph.
- Text adds what the diagrams can't show. A sentence that narrates a diagram gets deleted.
- Rationale lives in ADRs; the README links them. For an unrecorded decision, call the Skill tool with "domain-modeling" to write the ADR.
- **Catalogs** (numbered rules, config keys, error codes) stay local, outside the blueprint text: split them into child READMEs when they follow sub-folders, else into a sibling file in the same folder (for example `RULES.md`), linked from the Parts table.
- A README that is not a blueprint (test fixtures, corpus notes) carries `<!-- blueprint: skip -->` and stays out of the tree.
