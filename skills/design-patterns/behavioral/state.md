# State

**Intent:** An object delegates its behaviour to a state object and swaps that object as its state changes.

**Earned when:** the same `if self.status == ...` cascade appears in several methods, and states have different behaviour, not just different labels.

**Simplest form first:** an `Enum` plus a transition table (dict of allowed moves) when states differ only in which moves are allowed. Classes when each state has its own behaviour. See `principle-make-illegal-states-unrepresentable`.

**Roles:** context (holds the current state, delegates), state interface, concrete states (may trigger transitions).

```python
class Status(Enum): DRAFT = 1; REVIEW = 2; PUBLISHED = 3

ALLOWED = {Status.DRAFT: {Status.REVIEW}, Status.REVIEW: {Status.DRAFT, Status.PUBLISHED}}

def move(doc: Doc, to: Status) -> None:
    if to not in ALLOWED.get(doc.status, set()): raise InvalidTransition(doc.status, to)
    doc.status = to
```

**Costs:** too heavy for a few states that rarely change.

**Not to be confused with:** Strategy (the client picks it and it never switches itself; states switch each other).
