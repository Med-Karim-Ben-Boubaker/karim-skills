---
name: principle-name-the-trade-off
description: "Makes architecture decisions explicit: picks at most three driving architecture characteristics, names what each option buys and costs, scales design effort to how hard the decision is to undo, and records the why in an ADR. Use when choosing between designs, technologies, architecture styles, data models or datastores, defining nonfunctional requirements, or writing the design part of a spec. For whether to build it at all, use principle-keep-it-simple; for where code lives, use principle-point-dependencies-inward."
---

# Name the Trade-off

Everything in software architecture is a trade-off (the **First Law of Software Architecture**). A choice with no named cost has not been analysed yet. Aim for the **least-worst** option for this context, not the best in general.

1. **Pick the driving characteristics.** From the requirements, name at most three **architecture characteristics** (the "-ilities") that decide the design: performance, scalability, availability, reliability, consistency, evolvability, testability, cost, time to market. Make each measurable ("p99 under 200 ms at 50 req/s", not "fast").
2. **Name what each option buys and gives up** against those characteristics. Write the cost down next to the choice.
3. **Spend design effort by reversibility.** **One-way doors** (public APIs, wire and storage formats, schemas, data ownership, the datastore) earn **design it twice**: compare two or more radically different options (`codebase-design` DESIGN-IT-TWICE.md, or the `prototype` skill). **Two-way doors** get the simplest option now. Decide at the **last responsible moment**, and keep details (database, framework, transport) swappable so they can wait.
4. **Record the why** in an **ADR**: context, decision, consequences, rejected options (`model-domain` ADR-FORMAT.md). Why matters more than how (the **Second Law**).
5. **Name the revisit trigger**: the measurable condition that reopens the decision, so the choice can stay simple today without becoming permanent.

**Decide what matters**: spend design attention and complexity on the few things that are important; give everything else the plain default.

## Output

For a one-way door, present the trade-off like this:

```
Driving characteristics: availability 99.9%, evolvability, cost under $50/month

| Option | Buys | Costs | Undo |
|---|---|---|---|
| Postgres table + polling worker | one datastore, transactions | ~1 s latency, load grows with volume | easy |
| Managed queue | push delivery, scales on its own | a second system to run, duplicate deliveries | moderate |

Decision: Postgres + polling. Wins on cost and evolvability; 1 s latency is acceptable.
Revisit when: above 50 jobs/s, or sub-second latency becomes a requirement.
```

For a two-way door, one line is enough: the choice and why.

**Terms:** revisit trigger, architecture characteristics, quality attributes, nonfunctional requirements (NFRs), SLOs, least-worst architecture, First and Second Laws of Software Architecture, one-way and two-way doors, last responsible moment, design it twice, Architecture Decision Record (ADR), fitness functions, CAP theorem, PACELC.
