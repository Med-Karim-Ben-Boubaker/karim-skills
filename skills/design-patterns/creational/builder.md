# Builder

**Intent:** Assemble a complex object step by step, so callers set only the parts they need.

**Earned when:** a constructor with many optional parameters, a stack of overloads, or objects that must never be seen half-built.

**Simplest form first:** keyword arguments with defaults, or a `dataclass`. Use a builder only for multi-step or validated assembly.

**Roles:** builder (one method per step, then a result method), concrete builders, optional director (preset sequences), product.

```python
@dataclass(frozen=True)
class Query:
    table: str
    where: tuple[str, ...] = ()
    limit: int | None = None

q = Query("orders", where=("paid",), limit=10)
```

**Costs:** extra classes; a builder that only sets fields is a dataclass in disguise.

**Not to be confused with:** Abstract Factory (returns finished products at once); Factory Method (picks a type, doesn't assemble).
