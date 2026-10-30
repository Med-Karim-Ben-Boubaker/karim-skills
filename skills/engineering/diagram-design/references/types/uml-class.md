# UML class

**Answers:** what the classes are, what they do, and how they inherit or own each other. Use it only when inheritance, interfaces, or operations are the point; plain data shapes are ER.

## Layout

- One `entity` per class: `head` holds the name, plus `<span class="stereo">«interface»</span>` or `«abstract»` when it applies. Attribute rows, then a `sep`, then operation rows (`+ parse(pdf) → Plan`). Omit an empty compartment.
- Base classes and interfaces on top, implementations below.
- Relationship markers, at the target end:

| Relation | Line | Marker |
|---|---|---|
| inherits | solid | `tri-hollow` |
| implements | `dashed` | `tri-hollow` |
| owns (part dies with whole) | solid | `dia-fill` at the owner |
| has (part lives on) | solid | `dia-hollow` at the owner |
| uses | `dashed` | `arr-open` |

- Add a legend strip showing only the relations used.

## Budget

≤ 7 classes, ≤ 8 relations, ≤ 5 members per compartment.

## Avoid

- Getters, setters, dunder methods: show behaviour that matters.
- Composition and aggregation used loosely: the filled diamond claims lifetime ownership.
