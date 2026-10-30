# Abstract Factory

**Intent:** One object creates a whole family of related objects that must match each other.

**Earned when:** several product types must always come from the same variant (same backend, same theme, same vendor), and the variant is chosen once at startup.

**Simplest form first:** a module or a dict per variant holding its constructors, chosen at startup.

**Roles:** abstract products, concrete products per variant, the factory interface (one method per product), one concrete factory per variant, client.

```python
class StorageFactory(Protocol):
    def reader(self) -> Reader: ...
    def writer(self) -> Writer: ...

def run(factory: StorageFactory) -> None:
    rows = factory.reader().read()
    factory.writer().write(rows)
```

**Costs:** many interfaces and classes; heavy for one or two products.

**Not to be confused with:** Factory Method (one product); Facade (hides use of a subsystem, not its creation).
