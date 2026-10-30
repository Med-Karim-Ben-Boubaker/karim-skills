# Prototype

**Intent:** Make new objects by copying a configured one, without knowing its concrete class.

**Earned when:** objects are costly to configure and a few presets get copied, or code must copy objects it only knows by interface.

**Simplest form first:** `copy.copy` / `copy.deepcopy`, or `dataclasses.replace` on a frozen dataclass. Write `__deepcopy__` only to control what is shared.

**Roles:** prototype (clone), concrete prototypes, optional registry of named presets.

```python
DEFAULT = Config(retries=3, timeout=30)
fast = dataclasses.replace(DEFAULT, timeout=5)
```

**Costs:** cycles and shared references make deep copies tricky.

**Not to be confused with:** Memento (snapshots for undo, not new objects); Factory Method (creates by subclass, not by copy).
