# ER

**Answers:** what is stored, and how it relates. Use it for database tables, ORM models, or persisted schemas.

## Layout

- One `entity` per table: `head` is the table name, rows are columns. Show the key (`# id`), the foreign keys (`→ plan_id`), and at most 3 columns that matter to the story; collapse the rest into one row `… 6 more`.
- The central table (most relationships) in the middle; its children around it.
- Relationship edges go column to column: from the foreign key row's centre to the referenced key row's centre, entering each entity from the side.
- Cardinality with `crow-one` / `crow-many` markers at the ends (`marker-start` and `marker-end`). Add a verb label only when the relation isn't obvious from the names.
- `data-src` on each entity cites the model or migration; on each edge, the foreign key declaration.

## Budget

≤ 7 entities, ≤ 8 relationships, ≤ 6 rows per entity.

## Avoid

- Every column: the diagram is the shape of the data, not the DDL.
- Edges ending on the entity head when a column is the real anchor.
