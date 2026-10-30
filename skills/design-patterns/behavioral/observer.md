# Observer

**Intent:** A publisher keeps a list of subscribers and notifies them when something happens.

**Earned when:** a change in one object must trigger reactions in others, and the set of reactors is unknown in advance or changes at runtime.

**Simplest form first:** a list of callables. Keep the list on the instance, never as a shared class attribute.

**Roles:** publisher (subscribe, unsubscribe, notify), subscriber interface (one callback), concrete subscribers, client (wires them).

```python
class Stock:
    def __init__(self): self._listeners: list[Callable[[Item], None]] = []
    def subscribe(self, fn): self._listeners.append(fn)
    def restock(self, item: Item):
        for fn in self._listeners: fn(item)
```

**Costs:** no guaranteed order; reactions are hard to trace; forgotten subscribers leak memory.

**Not to be confused with:** Mediator (two-way coordination through one hub; Observer is one-way); Chain of Responsibility (one handler takes the request; observers all react).
