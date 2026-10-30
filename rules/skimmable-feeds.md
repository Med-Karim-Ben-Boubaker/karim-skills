# Skimmable feeds

A **feed** is any set of short generated texts a reader scans side by side: session or chat titles, notification summaries, dashboard cards, changelog lines, issue or ticket titles, commit subjects, list items. Readers skim a feed, so every item takes the same shape.

1. **Lead with the verb or subject.** Use verb, then object. Drop a subject every item shares.
2. **Put the deciding words first.** Readers see the first two words of each item. Start with what tells one item apart from the next: status, action, or theme.
3. **Use one template and one word per concept.** Same grammar, same tense, same slots in every item. Choose "issue" or "ticket" and keep it.
4. **Vary only what differs.** Readers read every difference as meaningful. Use the same fields at the same level of detail, and let only the values change.
5. **Pick verbs that carry the tone.** Write "Users love", "Users complain", "Build fails". The verb should give the sentiment before the reader reaches the rest.

## Examples

Session titles:

| Before | After |
|---|---|
| Question about the auth flow | Tracing the auth token refresh |
| Can you fix the failing CI? | Fixing the flaky CI test in `api/` |
| README stuff | Rewriting the install section of the README |

Notification summaries:

| Before | After |
|---|---|
| Your order from Acme has an update: it shipped | Shipped: Acme order #4411 |
| Heads up, we noticed a problem with payment | Failed: payment for invoice 2093 |
| PR #88 got some comments from a reviewer | Changes requested: PR #88 |

Review-theme cards, one template (verb + theme, count, one quote):

| Before | After |
|---|---|
| Chess is a popular new draw | Users complain the chess mode is too hard (12 reviews): "lost every game" |
| Many people mentioned streaks | Users love streaks (74 reviews): "kept me going for 300 days" |
