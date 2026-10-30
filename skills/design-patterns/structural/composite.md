# Composite

**Intent:** Treat single items and groups of items through one interface, so trees are handled recursively.

**Earned when:** the domain is a tree (folders, menus, org units, nested line items) and callers keep checking `isinstance` to tell a leaf from a group.

**Simplest form first:** a recursive function over nested data. Use classes when leaves and groups carry real behaviour.

**Roles:** component (shared interface), leaf, composite (holds children, combines their results), client.

```python
class Item(Protocol):
    def price(self) -> Money: ...

@dataclass
class Bundle:
    items: list[Item]
    def price(self) -> Money: return sum((i.price() for i in self.items), Money(0))
```

**Costs:** one interface for very different node types can get vague.

**Not to be confused with:** Decorator (wraps one object, not many); Iterator and Visitor (walk or operate on a composite).
