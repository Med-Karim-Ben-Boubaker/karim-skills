# Factory Method

**Intent:** Code asks a creation method for an object and lets a subclass or a parameter decide the concrete type.

**Earned when:** the same `if kind == ...: X() elif ...: Y()` construction appears in more than one place, or a library must let callers plug in their own types.

**Simplest form first:** a dict from key to class or function. Subclass a creator only when the creator also has behaviour that varies.

**Roles:** Product (shared interface), concrete products, creator (calls the factory method), concrete creators.

```python
EXPORTERS = {"csv": CsvExporter, "json": JsonExporter}

def make_exporter(fmt: str) -> Exporter:
    return EXPORTERS[fmt]()
```

**Costs:** a subclass per product when done with inheritance.

**Not to be confused with:** Abstract Factory (a family of products, not one); Builder (one product in steps).
