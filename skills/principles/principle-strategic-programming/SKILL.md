---
name: principle-strategic-programming
description: "Lands a change in existing code as if the design had planned for it: redesigns toward the new requirement, migrates every caller and deletes the old path, uses expand-migrate-contract across deploys, and cleans only the code it touches. Use when adding a requirement to existing code, replacing an internal API, or reaching for a flag, special case, wrapper or compatibility shim to make a change fit. For whether to make the change, use principle-keep-it-simple; for pacing it, use principle-small-verified-steps."
---

# Strategic Programming

Working code isn't enough. Each change should leave the code as if it had been designed for the new requirement from the start (**strategic** vs **tactical** programming). Tactical patches, a flag here and a special case there, add up to complexity no single change caused (the **tactical tornado**).

- **Redesign, then deliver.** Ask: "if this requirement had existed on day one, what would the code look like?" Move to that shape in small verified steps. Often the right shape is smaller than the current one.
- **One path.** When you replace an internal API, migrate every caller and delete the old one in the same change. Callers you control need no shims, aliases or deprecation periods.
- **Expand, migrate, contract** across a deploy boundary (**parallel change**). For public APIs, stored data and wire formats: add the new form, move readers and writers, then remove the old form. The removal step is part of the task, planned up front. For large replacements, grow the new system around the old one (**strangler fig**).
- **Boy Scout Rule, scoped.** Leave the code you touch cleaner than you found it. Refactor what the change needs, nothing beyond it.
- **Fix the shape behind the smell.** One change that edits many files (**Shotgun Surgery**) or one module edited for unrelated reasons (**Divergent Change**) means code that changes together lives apart. Move it together.
- **Incremental design.** Invest in the design every day so the **cost of change** stays flat. When your understanding of the right design jumps ahead, move the code toward it steadily, change by change.

## Example

Orders can now ship to several addresses.

- **Tactical:** add `second_address`, plus an `if order.second_address` in each of the four places that ship. The next request adds `third_address`.
- **Strategic:** replace `address` with `shipments: list[Shipment]`, move the four callers to it, delete `address`. A single address is now a list of one, and no caller has a special case.

**Terms:** strategic vs tactical programming, incremental design, cost of change, tactical tornado, technical debt, refactoring, preparatory refactoring, parallel change, expand–migrate–contract, strangler fig, Boy Scout Rule, Shotgun Surgery, Divergent Change, backward and forward compatibility.
