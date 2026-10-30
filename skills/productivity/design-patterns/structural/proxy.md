# Proxy

**Intent:** A stand-in with the same interface as a service that controls access to it: lazy creation, access checks, caching, remote calls, logging.

**Earned when:** callers need the real interface but something must happen around every call, and neither the callers nor the service should change.

**Simplest form first:** a wrapper that forwards with `__getattr__`, or `functools.cache` for a pure caching proxy.

**Roles:** service interface, service, proxy (holds or creates the service, adds its work, forwards), client.

```python
class LazyModel(Model):
    def __init__(self, path: Path): self._path, self._model = path, None
    def predict(self, x):
        if self._model is None:
            self._model = load_model(self._path)
        return self._model.predict(x)
```

**Costs:** one more layer; adds latency where it does work on each call.

**Not to be confused with:** Decorator (stacked by the client to add features; a proxy manages one service itself); Adapter (changes the interface); Facade (different, simpler interface).
