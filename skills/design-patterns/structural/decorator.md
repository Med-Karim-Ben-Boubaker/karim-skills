# Decorator

**Intent:** Wrap an object in another with the same interface that adds behaviour before or after delegating; wrappers stack.

**Earned when:** optional behaviours (retry, cache, log, auth) combine in different ways, and a subclass per combination would explode.

**Simplest form first:** for functions, Python's `@decorator` syntax with `functools.wraps`. For objects, a wrapper class with the same interface. The pattern and the syntax share a name, not a mechanism.

**Roles:** component interface, concrete component, decorators (hold a component, forward, add behaviour), client (assembles the stack).

```python
class RetryingClient(HttpClient):
    def __init__(self, inner: HttpClient, attempts: int = 3): ...
    def get(self, url: str) -> Response:
        for _ in range(self.attempts - 1):
            try: return self.inner.get(url)
            except TransientError: pass
        return self.inner.get(url)

client = RetryingClient(LoggingClient(RealClient()))
```

**Costs:** order of layers matters; removing one layer from a stack is awkward; deep stacks are hard to debug.

**Not to be confused with:** Proxy (same interface, but controls one service's access or lifecycle, and the client doesn't compose it); Adapter (changes the interface); Chain of Responsibility (a link may stop the request; a decorator always forwards).
