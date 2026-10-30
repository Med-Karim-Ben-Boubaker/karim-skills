# Template Method

**Intent:** A base class fixes the order of an algorithm's steps; subclasses fill in some of them.

**Earned when:** several classes run near-identical algorithms that differ in a few steps, and the copies drift apart.

**Simplest form first:** one function that takes the varying steps as arguments.

**Roles:** abstract class (the template method and the steps: abstract, default, hooks), concrete classes (fill steps, never override the template).

```python
def import_file(path: Path, parse: Callable[[bytes], list[Row]]) -> Report:
    rows = parse(path.read_bytes())
    clean = [validate(r) for r in rows]
    return summarise(clean)

import_file(p, parse=parse_csv)
```

**Costs:** inheritance couples subclasses to the base; a fixed skeleton resists change; overriding a default step can break callers' expectations.

**Not to be confused with:** Strategy (composition, swapped at runtime); Factory Method (a template method whose step creates an object).
