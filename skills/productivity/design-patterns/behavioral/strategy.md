# Strategy

**Intent:** Put interchangeable algorithms behind one interface, so the caller can pick or swap them.

**Earned when:** a conditional selects between variants of one algorithm, and the same conditional or the list of variants keeps growing.

**Simplest form first:** pass a function. `sorted(key=...)` is a strategy. Use a class only when the strategy carries configuration or several related methods.

**Roles:** context (holds a strategy, calls it), strategy interface, concrete strategies, client (chooses).

```python
Pricing = Callable[[Order], Money]

def checkout(order: Order, pricing: Pricing) -> Invoice:
    return Invoice(order, total=pricing(order))

checkout(order, pricing=member_discount)
```

**Costs:** callers must know the variants to choose; a class per stable variant is noise.

**Not to be confused with:** State (states switch themselves); Template Method (inheritance, fixed when written; Strategy is composition, swapped at runtime); Command (packages an action to run later).
