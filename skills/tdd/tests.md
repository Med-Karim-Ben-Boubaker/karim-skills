# Good and Bad Tests

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

## FIRST

**Slow**: the test waits through the real backoff.

```python
# BAD: sleeps 1 s, 2 s and 4 s on every run
def test_fetch_gives_up_after_three_retries():
    with pytest.raises(FetchError):
        fetch_rates(day, http=FailingHttp())

# GOOD: the wait is passed in, so the test runs in milliseconds and checks the backoff too
def test_fetch_gives_up_after_three_retries():
    waits = []
    with pytest.raises(FetchError):
        fetch_rates(day, http=FailingHttp(), sleep=waits.append)
    assert waits == [1, 2, 4]
```

**Not repeatable**: the test reads the real clock, and recomputes its expected value the way the code does.

```python
# BAD: depends on the day it runs
def test_report_covers_yesterday():
    assert build_daily_report().day == date.today() - timedelta(days=1)

# GOOD: the clock is passed in, and the expected value is a literal
def test_report_covers_yesterday():
    assert build_daily_report(today=date(2026, 3, 2)).day == date(2026, 3, 1)
```
