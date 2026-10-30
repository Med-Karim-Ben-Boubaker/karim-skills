# Flyweight

**Intent:** Share the identical, immutable part of many objects to save memory.

**Earned when:** only when profiling shows memory exhausted by a huge number of similar objects whose repeated part can be split out.

**Simplest form first:** `functools.lru_cache` on a constructor, `sys.intern` for strings, or `__slots__`.

**Roles:** flyweight (shared immutable state), context (per-object state plus a flyweight reference), factory (returns cached flyweights).

```python
@functools.lru_cache(maxsize=None)
def tree_type(species: str, texture: str) -> TreeType:
    return TreeType(species, texture)

trees = [Tree(x, y, tree_type("oak", "oak.png")) for x, y in positions]
```

**Costs:** more complex code; may trade memory for CPU; a shared cache needs care under threads.

**Not to be confused with:** Singleton (one instance; flyweights are many, immutable); Prototype (copies, doesn't share).
