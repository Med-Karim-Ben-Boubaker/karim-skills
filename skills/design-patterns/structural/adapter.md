# Adapter

**Intent:** Wrap an object so its interface matches what the caller expects.

**Earned when:** a third-party or legacy class does the job but has the wrong interface or data format.

**Simplest form first:** a conversion function at the boundary. Use a class when the caller needs an object that fulfils an interface.

**Roles:** client, client interface, service (incompatible), adapter (implements the interface, wraps the service, translates).

```python
class StripePayments(Payments):
    def __init__(self, client: stripe.Client): self._client = client
    def charge(self, amount: Money) -> ChargeId:
        return ChargeId(self._client.create_charge(cents=amount.cents).id)
```

**Costs:** one more class per adapted service; sometimes changing the service is simpler.

**Not to be confused with:** Decorator (keeps the interface, adds behaviour); Proxy (keeps the interface, controls access); Facade (new interface over a whole subsystem).
