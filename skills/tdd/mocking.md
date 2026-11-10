# When to Mock

Code tests never call a model or the network. For a client you own (an LLM, an HTTP API), record real responses once and replay them; see [Recorded responses](#recorded-responses).

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

## Recorded responses

- **Record once against the real service** with a cassette library: pytest-recording or VCR.py in Python, Polly.js or nock's recorder in JavaScript. Filter auth headers and keys out of the cassette before it's committed.
- **Replay with recording off.** pytest-recording's default `none` mode makes a test that would reach the network fail instead of calling out.
- **Re-record only when the prompt, model or API changed**, and review the cassette diff like code.

A recorded response proves the code handles that answer. Whether the model still gives it is an eval's question (`principle-let-models-judge`).
