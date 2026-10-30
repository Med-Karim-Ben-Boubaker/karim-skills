# Command

**Intent:** Turn a request into an object that can be stored, queued, logged, sent elsewhere, or undone.

**Earned when:** operations must be queued, scheduled, retried, recorded, serialised, or undone and redone.

**Simplest form first:** a callable: a function, `functools.partial`, or a lambda. Use a class when the command needs `undo`, serialisation or metadata.

**Roles:** command interface (`execute`, maybe `undo`), concrete commands (hold receiver and arguments), receiver (does the work), invoker (triggers commands, keeps history), client.

```python
@dataclass
class Rename:
    doc: Document; new: str; old: str = ""
    def execute(self): self.old, self.doc.title = self.doc.title, self.new
    def undo(self): self.doc.title = self.old

history: list[Rename] = []
```

**Costs:** another layer between caller and work.

**Not to be confused with:** Strategy (swaps how one task is done; Command packages an action to run later); Memento (stores the state undo restores).
