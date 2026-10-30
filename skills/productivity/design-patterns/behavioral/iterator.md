# Iterator

**Intent:** Walk a collection's items without exposing how it stores them.

**Earned when:** callers know a collection's internals in order to loop over it, or several traversal orders are needed.

**Simplest form first:** a generator function with `yield`, or `__iter__` returning one. Python's `for` loop is the pattern.

**Roles:** iterator interface, concrete iterators, collection (creates iterators), client.

```python
class Tree:
    def walk(self) -> Iterator[Node]:
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(node.children)
```

**Costs:** overkill for a plain list; can be slower than direct access.

**Not to be confused with:** Visitor (runs an operation on each element; an iterator only yields them); Composite (what iterators often walk).
