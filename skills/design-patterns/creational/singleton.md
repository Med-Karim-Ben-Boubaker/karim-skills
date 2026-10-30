# Singleton

**Intent:** Exactly one instance of a class, reachable from anywhere.

**Earned when:** almost never. Prefer passing the one instance in. Consider it only for a process-wide resource no caller should create twice.

**Simplest form first:** a module-level object: modules are imported once, so the module is the singleton. Better still, create the object at startup and pass it to whoever needs it.

**Roles:** one class with a hidden constructor, a stored instance and an accessor.

In `db.py`, imported wherever it's needed:

```python
engine = create_engine(settings.database_url)
```

**Costs:** hidden dependencies, global state, hard to test or replace, needs locking under threads. Widely treated as an antipattern.

**Not to be confused with:** Flyweight (many shared immutable instances, not one); Facade (often one instance, but its point is the simple interface).
