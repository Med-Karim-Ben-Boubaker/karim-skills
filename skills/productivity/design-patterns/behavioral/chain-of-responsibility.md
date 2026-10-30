# Chain of Responsibility

**Intent:** Pass a request along a sequence of handlers; each one handles it, passes it on, or stops it.

**Earned when:** a request goes through ordered checks or steps (auth, validation, throttling) that must be added, removed or reordered without touching the caller.

**Simplest form first:** a list of functions run in order, stopping on the first that rejects. Middleware in web frameworks is this pattern.

**Roles:** handler interface, optional base handler (holds the next link), concrete handlers, client (builds the chain).

```python
Check = Callable[[Request], Rejection | None]
CHECKS: list[Check] = [require_auth, validate_body, throttle]

def admit(req: Request) -> Rejection | None:
    return next((r for check in CHECKS if (r := check(req))), None)
```

**Costs:** a request can fall off the end unhandled; the flow is hard to trace when the chain is built in many places.

**Not to be confused with:** Decorator (always forwards; a chain may stop); Command (handlers can be commands).
