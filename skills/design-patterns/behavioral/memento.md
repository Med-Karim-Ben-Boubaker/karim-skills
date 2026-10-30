# Memento

**Intent:** Save an object's state as an opaque snapshot and restore it later, without exposing its internals.

**Earned when:** undo, redo or rollback is needed, and outsiders must not read or depend on the object's fields.

**Simplest form first:** a frozen dataclass or dict snapshot made by the object itself, kept in a list.

**Roles:** originator (makes and restores snapshots), memento (immutable snapshot), caretaker (keeps the history, never reads it).

```python
class Editor:
    def save(self) -> Snapshot: return Snapshot(self._text, self._cursor)
    def restore(self, s: Snapshot) -> None: self._text, self._cursor = s.text, s.cursor

undo_stack: list[Snapshot] = []
```

**Costs:** memory grows with snapshots; Python can't enforce that a snapshot stays private or unchanged.

**Not to be confused with:** Prototype (copies to make a new object, not to roll back); Command (stores the action; often paired with Memento for undo).
