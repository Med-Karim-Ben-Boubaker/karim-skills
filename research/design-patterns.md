# Design patterns: research synthesis

Source: refactoring.guru/design-patterns (catalogue, intro pages, 22 pattern pages, 22 Python example pages).
Method: all facts come from WebFetch summaries written by a small model, not raw page text.
Labels: **[V]** = the summary states it (not checked against the raw page). **[I]** = inferred by the note author, not stated on the site.
In the per-pattern sections, every bullet is [V] unless tagged [I].

---

## 1. Summary

- The catalogue lists **22 classic patterns** in three groups: **5 creational**, **7 structural**, **10 behavioral**. [V]
- Each pattern has its own page with intent, problem, solution, structure, applicability, steps, pros, cons and relations. Each also has a Python example page. [V]
- The history page says the 1994 GoF book had **23** patterns. The site's 22 are a subset. The notes do not say which one is missing (see section 6). [V] / open
- Creational = how objects get made. Structural = how objects and classes fit together. Behavioral = how objects talk and share work. [V]

---

## 2. About patterns

Sources: intro pages `/design-patterns`, `/what-is-pattern`, `/history`, `/why-learn-patterns`, `/criticism`, `/classification`, `/catalog`. [V]

- **What it is.** A reusable answer to a design problem that keeps coming back. It is a blueprint, not finished code. You adapt it to your program. [V]
- **Analogy.** An algorithm is a recipe with exact steps. A pattern fixes the end result and its features, but you choose the build order. [V]
- **Parts.** The what-is-pattern page lists Intent, Motivation, Structure and a Code example. Some catalogues add Applicability, Implementation steps and Relations. [V] (The landing page describes the parts differently. See section 6.)
- **Scale.** Patterns differ in size: language idioms (one language), design patterns (many languages), architectural patterns (a whole app). [V]
- **History.** Architect Christopher Alexander described reusable patterns for buildings and towns in *A Pattern Language*. Four programmers (Gamma, Vlissides, Johnson, Helm) brought the idea to object-oriented software. Their 1994 book had 23 patterns and got the nickname "Gang of Four". [V]
- **Why learn them.** Proven fixes for common problems, a way of thinking about object design that transfers, and a shared vocabulary for a team. [V]
- **Criticism.** (a) Patterns can patch missing language features. Lambdas make Strategy unnecessary in some languages. (b) Applying them mechanically, without fit to context, can make code worse. (c) Overuse: forcing a pattern where plain code would do. [V]
- **Classification.** By intent (the three groups above). Patterns also differ in scale, as noted above. [V]

---

## 3. Pattern index

Intent and use-when are condensed from the Intent and Applicability sections. [V]

| # | Pattern | Group | Intent (one line) | Use when (signal) | Main risk / con |
|---|---|---|---|---|---|
| 1 | Factory Method | Creational | A base method decides which product to make; subclasses choose the type | Concrete types unknown up front; new types must not touch client code | Many subclasses |
| 2 | Abstract Factory | Creational | Make families of matching objects through one interface | Several related product families must stay consistent | Many interfaces and classes; overkill for simple cases |
| 3 | Builder | Creational | Assemble a complex object in steps; same steps, different results | Many optional parameters; several representations of one product | Several new classes |
| 4 | Prototype | Creational | Copy an object without depending on its concrete class | Copy objects of unknown type via an interface; costly presets | Circular references are tricky |
| 5 | Singleton | Creational | Exactly one instance, with a well-known access point | One shared resource (e.g. a DB handle) | Hidden coupling; hard to test; threads need guards |
| 6 | Adapter | Structural | Make incompatible interfaces work together | Third-party or legacy class has the wrong interface | More classes; editing the service may be simpler |
| 7 | Bridge | Structural | Split abstraction from implementation so each varies | Two or more independent dimensions would multiply subclasses | Overkill for an already cohesive class |
| 8 | Composite | Structural | Treat single items and trees of items through one interface | Domain is tree-shaped | Shared interface is hard when element types differ |
| 9 | Decorator | Structural | Add behaviour by wrapping an object in another | Optional features, stacked at runtime; subclassing awkward | Hard to remove one layer; order dependence; messy stacks |
| 10 | Facade | Structural | One simple entry point to a complex subsystem | Subsystem is complex but clients need common tasks | Grows into a bloated catch-all |
| 11 | Flyweight | Structural | Share the identical part of data across many objects | Huge count of similar objects exhausts memory | May trade memory for CPU; added complexity |
| 12 | Proxy | Structural | Stand-in with the same interface that controls access | Lazy creation, access control, caching, remote access, logging | More classes; responses may be delayed |
| 13 | Chain of Responsibility | Behavioral | Pass a request along handlers; each handles or forwards | Handler set or order unknown ahead; handlers change at runtime | Some requests go unhandled |
| 14 | Command | Behavioral | Wrap a request as an object | Queue, delay, log, or undo/redo | Extra layer; more complexity |
| 15 | Iterator | Behavioral | Walk a collection without exposing its storage | Hide internals; several or paused traversals | Overkill for simple collections; can be slower |
| 16 | Mediator | Behavioral | Objects talk only through one intermediary | Tightly coupled peers; components not reusable | Mediator becomes a "God object" |
| 17 | Memento | Behavioral | Save and restore state without exposing internals | Undo/redo; rollback; encapsulation must hold | Memory from snapshots; immutability not guaranteed in Python, JS, PHP |
| 18 | Observer | Behavioral | Subscribers are notified of a publisher's events | One change must update an unknown or changing set of objects | No guaranteed notification order |
| 19 | State | Behavioral | Object changes behaviour with its internal state | Behaviour depends heavily on state; big conditionals on a state field | Excessive for few or rarely changing states |
| 20 | Strategy | Behavioral | Put interchangeable algorithms in separate classes | Algorithm chosen or swapped at runtime; big conditional picks it | Extra classes; functions or lambdas can often replace them |
| 21 | Template Method | Behavioral | Base class fixes the algorithm skeleton; subclasses fill steps | Near-identical algorithms differ in a few steps | Fixed skeleton can restrict; Liskov risk when a default is suppressed |
| 22 | Visitor | Behavioral | Move an operation out of the classes it acts on | New operations over a stable structure of many classes | Every visitor changes when element classes change |

---

## 4. Patterns in detail

### 4.1 Creational

#### 1. Factory Method
Source: https://refactoring.guru/design-patterns/factory-method

- **Intent:** The base class defines how an object is created. Subclasses pick the concrete type.
- **Problem:** A logistics app is built around trucks and must add ships. Each new transport type means edits across the core code and more type-check branches.
- **Solution:** Replace direct construction with a call to a creation method on the creator. Subclasses override it to return different products that share one interface.
- **Roles:** Product (shared interface); Concrete Products; Creator (core logic, declares the factory method, may give it a default); Concrete Creators (override it; may return cached or pooled objects).
- **Use when:** exact types are not known in advance; new types must be addable without changing clients; building a library where users plug in their own parts; reusing costly objects through a pool (connections).
- **Steps (condensed):** define the product interface; add a factory method returning it; move all direct construction into it (optionally chosen by a parameter); add a subclass per product; if subclasses are not worth it, select by parameter; make the base method abstract or give it a default.
- **Pros:** less coupling between creator and products; creation code in one place; new products need no client change.
- **Cons:** many subclasses; fits best when introduced into an existing creator hierarchy.
- **Relations:** a common starting point that can grow into Abstract Factory, Prototype or Builder. Abstract Factory is often built from factory methods. Can be combined with Iterator. A specialised Template Method.
- **Python:** Abstract Creator with an abstract factory method and a concrete method that uses the product. Two creators, abstract Product with `operation`, two products. Features: `abc.ABC`, `@abstractmethod`, `from __future__ import annotations`, type hints. No Protocol, dataclass or generator. Idiomatic alternative [I]: a function or dict of callables often replaces the creator hierarchy.

#### 2. Abstract Factory
Source: https://refactoring.guru/design-patterns/abstract-factory

- **Intent:** Create families of matching objects through one interface, without binding code to their concrete classes.
- **Problem:** A furniture catalogue sells chairs, sofas and tables in several styles. Mixing styles breaks the look. The range changes often, and core code should not change with it.
- **Solution:** One interface per product type; each style implements all of them. A factory interface has one creation method per product type. One concrete factory per style. Clients use only abstract types. The app chooses the factory at startup (config or environment) and passes it on.
- **Roles:** Abstract Products; Concrete Products (per style); Abstract Factory; Concrete Factories (one per family); Client.
- **Use when:** code must work with several families of related objects whose concrete types may change; a class has many factory methods that dilute its job.
- **Steps:** grid the product types and variants; write abstract product interfaces; write an abstract factory with one method per product; write one concrete factory per variant; pick the factory at startup; replace direct constructor calls.
- **Pros:** products from one factory are guaranteed compatible; client decoupled; creation in one place; new variants need no client change.
- **Cons:** many new interfaces and classes; overcomplicates simple cases.
- **Relations:** Factory Method is simpler and often the start point. Builder returns a product after extra steps; Abstract Factory returns products at once. Often built from factory methods; Prototype can help. Can hide subsystem creation as a lighter alternative to Facade. Pairs with Bridge. Factories can be Singletons.
- **Python:** AbstractFactory with one method per product member; two concrete factories; two abstract product types with two variants each; client works only through abstract types. Features: `abc.ABC`, `@abstractmethod`, forward-reference annotations. Idiomatic alternative [I]: a dict mapping a family name to a set of callables, or a module.

#### 3. Builder
Source: https://refactoring.guru/design-patterns/builder

- **Intent:** Build a complex object in stages, so the same process can produce different versions.
- **Problem:** A house with many optional parts (walls, roof, pool, heating). A subclass per combination causes class explosion. One constructor with many parameters is unwieldy, since most go unused.
- **Solution:** Move construction into builder objects with one method per part. Callers invoke only the steps they need. Builders implement steps differently (wood vs stone). The product is fetched from the builder. An optional director holds preset step sequences.
- **Roles:** Builder interface; Concrete Builders (with a result method); Products (need not share a hierarchy); Director (optional); Client.
- **Use when:** a constructor has many optional parameters or a stack of overloads; several representations share steps; nested or tree-shaped objects are built recursively; callers must never see a half-built object.
- **Steps:** find the steps common to all variants; declare them in a builder interface; write a concrete builder per variant with a result method; optionally add a director; the client creates builder and director, runs them, and fetches the product (from the director only if all products share an interface, otherwise from the builder).
- **Pros:** incremental construction, steps can be deferred or repeated; construction code reused across variants; construction separated from product behaviour.
- **Cons:** several new classes; more overall complexity.
- **Relations:** often evolves from Factory Method. Differs from Abstract Factory in allowing extra steps before retrieval. Suits building Composite trees. Can pair with Bridge (director as abstraction, builders as implementations). Builders can be Singletons.
- **Python:** Abstract Builder with a `product` property and three build steps; concrete builder holds an in-progress product and resets after it is read; a simple product; a Director runs fixed sequences. Features: `abc.ABC`, `@property`, `typing.Any`. No Protocol or dataclass. The page's chaining example is prose only. Note: the base class declares `product` returning None while subclasses return a product, a type mismatch [V, from the note]. Idiomatic alternative [I]: keyword arguments, `dataclasses`, or a plain constructor cover most cases. The example does not show these.

#### 4. Prototype
Source: https://refactoring.guru/design-patterns/prototype

- **Intent:** Copy existing objects without tying code to their concrete classes.
- **Problem:** Copying from outside means creating an instance and copying each field. That fails for private state and couples the caller to the class. It is worse when code only knows an interface.
- **Solution:** Each copyable class offers a clone method. The object makes a new instance of its own class and copies its values, so it can reach private state. Callers clone through the common interface. Preconfigured objects act as templates in place of subclasses that differ only in setup.
- **Roles:** Prototype interface (declares clone); Concrete Prototype (handles edge cases such as links and cycles); Client; Prototype Registry (optional, named ready-made templates).
- **Use when:** copying objects of unknown concrete type (e.g. from third-party code via an interface); many subclasses exist only to vary setup; objects are costly to configure and a few standard configurations are needed.
- **Steps:** add clone to a shared interface or to each class; each class copies all its fields, and subclasses delegate to the parent so inherited private state is copied; clone returns the current class, never a parent type; optionally add a registry with lookup.
- **Pros:** copying without tying code to concrete classes; repeated setup replaced by cloning presets; easier production of complex objects; an alternative to inheritance for presets.
- **Cons:** cloning objects with circular references is tricky.
- **Relations:** Abstract Factory can use Prototype to build its methods. Keeps copies of Commands in a history. Clones Composite and Decorator structures instead of rebuilding them. Avoids inheritance, unlike Factory Method, but needs more setup. A simpler alternative to Memento when objects are plain and have no external links.
- **Python:** One class holding an int, a list, and a helper object with a parent pointer (a cycle). Uses `copy.copy` and `copy.deepcopy` through `__copy__`/`__deepcopy__` hooks, the `memo` dict for cycles, and `self.__class__(...)`. Usage note: Python's `copy` module already provides this, so you rarely write it yourself. Idiomatic alternative [I]: `copy.copy` or `copy.deepcopy` alone usually suffice; custom hooks are needed only to control sharing.

#### 5. Singleton
Source: https://refactoring.guru/design-patterns/singleton

- **Intent:** Guarantee a class has exactly one instance, with a shared way to reach it.
- **Problem:** A shared resource (a database connection or file) should have one controller object. A normal constructor always makes a new object. Global variables are easy to reach but any code can overwrite them.
- **Solution:** Block direct construction. A static accessor creates the one object on first request, stores it in a static field, and returns the same object afterwards.
- **Roles:** One class only: private constructor, static field holding the instance, static accessor.
- **Use when:** one object should serve many parts of a program (a single DB handle); tighter control than a global; the creation rule sits in one place so it can later allow more instances.
- **Steps:** add a private static field; add a public static fetch method; create lazily on first call; make the constructor private; switch callers to the static method.
- **Pros:** only one instance; global access point; created only when first needed.
- **Cons:** takes on two responsibilities (against SRP); can hide dependencies between components; multithreaded code needs guards; hard to unit-test (private constructors and static methods resist mocking).
- **Relations:** a Facade can often be a Singleton. Flyweight looks similar, but allows many immutable instances; Singleton has exactly one, possibly mutable. Abstract Factory, Builder and Prototype can each be Singletons.
- **Python:** A metaclass with a class-level instance cache that overrides `__call__`, plus a class that uses it. A second version adds a `threading.Lock` in the metaclass with a double check. Demo uses `threading.Thread`. Usage note: many developers consider it an antipattern, and its use is declining in Python. Features: metaclass, `__call__`, `with` on a lock. Idiomatic alternative [I]: a module is already a singleton, because import caches it. A module-level object is simpler than a metaclass.

### 4.2 Structural

#### 6. Adapter (also called Wrapper)
Source: https://refactoring.guru/design-patterns/adapter

- **Intent:** Make objects with incompatible interfaces work together.
- **Problem:** An app gets XML, but a third-party analytics library accepts only JSON. The library cannot be changed, and changing it would break existing code.
- **Solution:** A translator object sits between them. It converts calls and data for the wrapped object, which does not know it exists.
- **Roles:** Client; Client Interface (the protocol the client expects); Service (the incompatible class); Adapter (implements the client interface, wraps the service, translates). A class-adapter variant uses multiple inheritance, mainly suited to C++.
- **Use when:** an existing class's interface does not match; a middle layer is needed for legacy or third-party classes; shared behaviour is wanted across subclasses without duplication.
- **Steps:** find the incompatible service and its clients; define the client-facing interface; create an adapter implementing it; hold a reference to the service; delegate, doing only conversion; clients depend only on the interface.
- **Pros:** conversion code separated from business logic; new adapters do not touch clients.
- **Cons:** more classes and interfaces; sometimes editing the service directly is simpler.
- **Relations:** Bridge is planned up front; Adapter is retrofitted. Decorator keeps and extends the interface; Adapter changes it. Proxy keeps the same interface; Adapter gives a different one. Facade defines a new interface over a whole subsystem; Adapter usually wraps one object.
- **Python:** Target (concrete, not abstract), Adaptee with an incompatible output format, and Adapter. Two versions: inheritance (Adapter subclasses both) and composition (Adapter holds an Adaptee). Features: basic classes, multiple inheritance, string forward references. No ABC; the Target relies on duck typing. Usage note: "pretty common", especially around legacy code. Variance: the Python Target is concrete, while the general description uses an interface [V, from the note]. Idiomatic alternative [I]: a wrapper class or a plain conversion function is often enough.

#### 7. Bridge
Source: https://refactoring.guru/design-patterns/bridge

- **Intent:** Split a tangled class into an abstraction (control side) and an implementation (worker side), so each can change without disturbing the other.
- **Problem:** Combining two independent traits (shape and colour) by subclassing multiplies classes with each new option.
- **Solution:** Replace inheritance with composition. One dimension gets its own hierarchy. The main class holds a reference to an object from it and delegates the related work.
- **Roles:** Abstraction (control; delegates low-level work); Implementation interface (basic operations each platform must offer); Concrete Implementations; Refined Abstractions; Client (pairs the two, works mostly with the abstraction).
- **Use when:** a large class has several variants of one feature (e.g. several DB backends); a class must vary along two or more independent dimensions; implementations are swapped at runtime; changes in one area should not touch the whole codebase.
- **Steps:** identify the independent dimensions; define the abstraction's operations; define the low-level implementation interface; build concrete implementations; give the abstraction a field pointing to an implementation; create refined abstractions; inject the implementation through the constructor.
- **Pros:** platform-independent code; clients isolated from platform details; both sides extend independently; clearer single responsibilities.
- **Cons:** unnecessary complexity when applied to an already cohesive class.
- **Relations:** Adapter (retrofitted vs planned up front). State and Strategy use similar composition with different intent. Abstract Factory can hide the pairing from the client. Builder: a director can act as the abstraction, with builders as implementations.
- **Python:** Abstraction holding an Implementation reference; ExtendedAbstraction; abstract Implementation (`abc.ABC`); two concrete implementations; the client picks the pairing at setup. Features: `abc.ABC`, `@abstractmethod`, type hints. No Protocol. The notes are general to the pattern, not Python-specific. Idiomatic alternative [I]: passing a callable or strategy object at construction is usually simpler than a parallel class hierarchy.

#### 8. Composite
Source: https://refactoring.guru/design-patterns/composite

- **Intent:** Organise objects into trees, so single items and groups are handled through the same interface.
- **Problem:** Totalling the price of nested products and boxes needs type checks and depth knowledge. A plain loop does not work.
- **Solution:** Products and boxes share one interface (e.g. a price method). A product returns its own price. A box sums its children's prices and adds its own extras. Recursion handles nesting.
- **Roles:** Component (shared interface); Leaf (no children, does the real work); Container/Composite (holds leaves or containers, forwards and combines); Client (uses the component interface only).
- **Use when:** the domain is tree-shaped; clients should treat simple and nested elements the same.
- **Steps:** confirm the domain is a tree of leaves and containers; define a component interface that suits both; build leaves; build a container that stores component-typed children and forwards work; add child add/remove either on the container or on the interface (trade-off: interface purity).
- **Pros:** trees are easier with polymorphism and recursion; new element types do not change tree-handling code.
- **Cons:** a shared interface is hard to design when element types differ a lot; generalising it can hurt readability.
- **Relations:** Builder builds large trees step by step. Chain of Responsibility: requests travel up parents. Iterator and Visitor traverse or operate on the whole tree. Flyweight shares leaves. Decorator has a similar diagram (one child vs many; can be combined). Prototype clones big trees.
- **Python:** Abstract Component with a parent property, no-op `add` and `remove`, `is_composite`, and abstract `operation`; a Leaf; a Composite that holds children and recurses. Features: `abc.ABC`, `@abstractmethod`, `@property` with setter, `typing.List`. Usage note: common in UI trees and graphs. Idiomatic alternative [I]: a plain recursive function over nested lists or dicts often replaces the class tree.

#### 9. Decorator
Source: https://refactoring.guru/design-patterns/decorator

- **Intent:** Add behaviour by wrapping an object in another object that provides the extra behaviour.
- **Problem:** A notifier starts as email-only. SMS, Facebook and Slack get added, and some users want several at once. A subclass per combination explodes.
- **Solution:** Hold a reference to a helper and delegate to it. Each wrapper matches the wrapped object's interface, forwards calls, and adds logic before or after. Wrappers stack. The client assembles the stack, so callers see no difference.
- **Roles:** Component (shared interface); Concrete Component (base object); Base Decorator (holds a wrapped component and forwards everything); Concrete Decorators (add behaviour around forwarded calls); Client (composes layers).
- **Use when:** responsibilities must be added at runtime without editing existing code; business logic is split into optional layers; inheritance is awkward or impossible (e.g. a final class).
- **Steps:** identify the core object and the optional layers; define a shared interface; build the concrete component; build a base decorator that holds and forwards; make every class follow the interface; create concrete decorators; the client assembles them.
- **Pros:** extends without subclasses; adds or removes features at runtime; combines behaviours by stacking; splits monolithic classes.
- **Cons:** removing one specific wrapper from the stack is hard; making behaviour independent of stacking order is hard; layered setups can look messy.
- **Relations:** Adapter changes the interface; Decorator keeps it. Proxy has the same interface, usually manages its service's lifecycle, while the client composes decorators. Chain of Responsibility has a similar shape, but handlers may stop the chain, and decorators must not break request flow. Composite: one child vs many. Prototype clones composed structures. Strategy changes inner logic; Decorator changes the outer shell.
- **Python:** Component interface; ConcreteComponent; Decorator base holding a wrapped component and forwarding; two concrete decorators adding text. Features: plain classes, `@property`, no `abc`. The base method uses `pass` despite a string return annotation. Usage note: "fairly standard", common in stream code. The page does not mention Python's `@decorator` syntax. Idiomatic alternative [I]: Python's `@decorator` syntax with `functools.wraps` is the idiomatic way to wrap functions. This is a name clash: the GoF pattern is a class wrapper, not the language feature.

#### 10. Facade
Source: https://refactoring.guru/design-patterns/facade

- **Intent:** Give a large library, framework or group of classes a streamlined entry point.
- **Problem:** Direct use of a complex toolkit spreads setup, dependencies and call order through the code. That ties business logic to vendor details.
- **Solution:** One class wraps the subsystem and exposes only the operations clients need. Example: a cat-video app needs one conversion call, and the facade hides a heavy video library. Swapping libraries later changes only the facade.
- **Roles:** Facade (routes requests, coordinates components); additional facade (splits off unrelated features so none bloats); Complex subsystem (objects that do not know the facade exists); Client (uses only the facade).
- **Use when:** the subsystem is complicated but clients need common tasks; a layered architecture uses a facade as each layer's entry point.
- **Steps:** decide whether a simpler interface would decouple clients; create a facade that delegates and manages subsystem setup and lifecycle; route all access through it; split into focused facades if it grows.
- **Pros:** shields code from subsystem complexity.
- **Cons:** can become a bloated catch-all coupled to much of the app.
- **Relations:** Adapter wraps one object to fit an interface; Facade defines a new interface over a subsystem. Abstract Factory is the alternative when only object creation must be hidden. Flyweight: many small objects vs one object for a subsystem. Mediator: a facade adds no behaviour and the subsystem does not know it; a mediator centralises communication, and components talk to it. Singleton: a facade can often be one instance. Proxy: both wrap a complex object, but a proxy matches the service interface and is interchangeable; a facade is not.
- **Python:** A Facade holding two subsystem objects, running a fixed sequence in `operation()`, and creating default subsystems when none are passed in. The subsystems do not know the facade. The client uses only the facade. Features: plain classes, `__init__`, `from __future__ import annotations`. No ABC. Usage note: "common", especially with large libraries and APIs. Idiomatic alternative [I]: a module exposing a few functions is usually the idiomatic facade.

#### 11. Flyweight
Source: https://refactoring.guru/design-patterns/flyweight

- **Intent:** Reduce memory by letting many objects share the identical part of their data.
- **Problem:** A game particle system (bullets, missiles, shrapnel) creates so many objects that a low-memory machine runs out of RAM.
- **Solution:** Split each object's data. The shared, unchanging part goes into a lightweight shared object. The per-instance part (position, speed, direction) is stored elsewhere and passed in when needed.
- **Roles:** Flyweight (shared, immutable data); Context (unique data plus a reference to a flyweight); Client (supplies or computes the unique data); Flyweight Factory (pool that returns an existing flyweight or creates one).
- **Use when:** only when a huge number of similar objects is needed, their data exhausts memory, and the duplicated state can be extracted and shared.
- **Steps:** split fields into shared and per-object; make shared fields immutable, set in the constructor; change methods to take per-object data as parameters; optionally add a factory that reuses flyweights; clients store per-object data, possibly in a context class.
- **Pros:** large memory savings when many similar objects exist.
- **Cons:** may trade memory for CPU if context data must be recomputed on each call; added complexity.
- **Relations:** shared leaves in a Composite can be flyweights. Facade: one object for a whole subsystem; Flyweight: many small objects. Resembles Singleton only if all shared state sits in one object; flyweights allow several instances with different intrinsic state, and they are immutable.
- **Analogy:** none. The page uses a particle system and a forest (tree types shared across many positions) as examples.
- **Python:** A Flyweight holds shared (intrinsic) state while the unique (extrinsic) data is passed into its method. A FlyweightFactory caches flyweights under a string key built from the shared state. Features: a class-level dict as cache (shared across factory instances), `Dict` hints, `json.dumps` for the key. No lock, so not thread-safe. Usage note: the page says the only purpose is saving memory, and to skip it if RAM is not a constraint. Idiomatic alternative [I]: `functools.lru_cache` or `sys.intern` covers caching for immutable values. The class-level cache is not thread-safe.

#### 12. Proxy
Source: https://refactoring.guru/design-patterns/proxy

- **Intent:** A stand-in object that controls access to a real one, so extra work can happen before or after a request reaches it.
- **Problem:** Some objects are heavy and needed rarely. Adding deferred setup to every client duplicates code. The original class may be locked in a library you cannot change.
- **Solution:** A stand-in with the same interface as the real service. It creates the real object when needed, forwards work, and can add lazy setup or caching invisibly. Because the interface matches, it can replace the service anywhere.
- **Roles:** Service Interface (shared contract); Service (real logic); Proxy (holds a reference to the service, adds its own processing, often manages its lifecycle); Client (works through the interface).
- **Use when:** defer creating a heavy object until it is used; restrict access to authorised callers; reach a remote service while hiding network details; log request history; cache repeated results; release a heavy object when no client uses it.
- **Steps:** make proxy and service share an interface (subclassing is the fallback); give the proxy a service field, usually creating it; each proxy method does its extra work, then delegates; optionally add a helper that chooses proxy or real service; optionally defer service creation to first use.
- **Pros:** controls the service invisibly; manages its lifecycle; works even when the service is not ready; new proxies can be added without touching the service or clients.
- **Cons:** more classes; responses may be delayed.
- **Relations:** Adapter changes the interface, Proxy keeps it, Decorator enhances it. Facade offers a new, simpler interface; Proxy matches its service's interface. Decorator has a similar structure; a proxy manages its service's lifecycle, while the client composes decorators.
- **Python:** Abstract Subject (`abc.ABC`, `@abstractmethod`); RealSubject; a Proxy holding a RealSubject that checks access and logs before forwarding; a client accepting any Subject. The page's sample always grants access. Features: `abc.ABC`, `@abstractmethod`, `__init__`. Usage note: the page says it is "not a frequent guest" in Python apps, but useful for adding behaviour without changing clients. Idiomatic alternative [I]: `__getattr__` delegation or a functools-style wrapper is often simpler. `unittest.mock` and descriptors are other ways to intercept access; the page does not mention them.

### 4.3 Behavioral

#### 13. Chain of Responsibility
Source: https://refactoring.guru/design-patterns/chain-of-responsibility

- **Intent:** Pass a request through a sequence of handlers. Each handler processes it or forwards it.
- **Problem:** An online order needs an auth check, an admin check, input sanitising, IP-based login throttling and caching. The checks tangle together, and reusing them across components duplicates code.
- **Solution:** Each check is a handler with a shared interface, linked to the next. A handler can stop the chain. Variant: the first capable handler takes the request, as in GUI event propagation. A chain can follow an object tree.
- **Roles:** Handler interface; optional Base Handler (next link and default forwarding); Concrete Handlers; Client (builds chains, can start at any point).
- **Use when:** request types or their order are unknown in advance; handlers must run in order; the set of handlers changes at runtime.
- **Steps:** define the handler interface and a request object; optional base handler; concrete handlers decide to process or forward; assemble chains in the client or through config factories; allow starting at any point; handle unhandled requests and single-link chains.
- **Pros:** controls order; separates the trigger from the execution; handlers can be added without changing the client.
- **Cons:** some requests go unhandled.
- **Relations:** Command, Mediator and Observer connect senders and receivers in different ways. Often combined with Composite (request bubbles up to the root). Handlers can be Commands. Structurally like Decorator, but handlers may stop the flow.
- **Python:** Abstract Handler; AbstractHandler with `set_next` and default forwarding; three concrete handlers; the client builds the chain. Features: `abc.ABC`, `@abstractmethod`, `Any`/`Optional`, `super()`. The base `handle` is marked abstract but has a body. Usage note: "fairly common" in filters and event pipelines. Idiomatic alternative [I]: a list of callables, or a generator-based pipeline, is simpler.

#### 14. Command
Source: https://refactoring.guru/design-patterns/command

- **Intent:** Wrap a request as an object, so it can be queued, delayed, logged or undone.
- **Problem:** Toolbar buttons, menus and shortcuts all need the same actions. A subclass per button ties the GUI to the logic and duplicates it.
- **Solution:** Each action is a command object that holds a receiver, a method and its arguments, behind a shared interface (usually a no-argument `execute`). UI elements hold and trigger commands. Commands can be shared and swapped at runtime.
- **Roles:** Sender (invoker); Command interface; Concrete Command; Receiver (business logic); Client (builds receivers, commands and senders).
- **Use when:** operations should be objects; they must be queued, scheduled, logged, serialised or sent remotely; undo/redo is needed via a history stack.
- **Steps:** a command interface with `execute`; turn each request into a concrete command; senders hold the interface and call the command instead of the receiver; the client wires receiver, then command, then sender.
- **Pros:** decouples the invoker from the operation; supports undo/redo, deferred execution, and composition.
- **Cons:** an extra layer and more complexity.
- **Relations:** Chain of Responsibility handlers can be commands. Memento stores undo state. Strategy changes how one task is done; Command wraps an operation for deferred or history use. Prototype copies commands kept in a history. Visitor is a more powerful Command.
- **Python:** Abstract Command with `execute`; SimpleCommand; ComplexCommand holding a Receiver; Receiver does the work; Invoker runs optional before and after commands. Features: `abc.ABC`, `@abstractmethod`, `isinstance` checks in the Invoker. No `__call__`. Usage note: common as a replacement for callbacks in UI, task queues and undo history. Idiomatic alternative [I]: a plain callable (a function, `functools.partial`, or an object with `__call__`) is the idiomatic command. The class hierarchy is needed only for undo or serialisation.

#### 15. Iterator
Source: https://refactoring.guru/design-patterns/iterator

- **Intent:** Step through a collection without exposing how it stores its items.
- **Problem:** A social network's profile collection needs traversals (friends, DFS/BFS over trees, random access). Those traversals clutter the collection and tie clients to its class.
- **Solution:** Move traversal into iterator objects that share one interface. Each keeps its own position, so several can walk one collection. A new traversal means a new iterator class.
- **Roles:** Iterator interface; Concrete Iterators; Collection interface (returns iterators); Concrete Collections; Client.
- **Use when:** the collection's internals are complex and should be hidden; traversal code is bulky and repeated; the data structure is not known in advance.
- **Steps:** an iterator interface with `next` and helpers; a collection interface that returns iterators; concrete iterators per collection; collections create their iterators; clients use them.
- **Pros:** separation of concerns; new collections and traversals can be added safely; several or paused traversals at once.
- **Cons:** overkill for simple collections; can be slower than direct access.
- **Relations:** traverses Composite. Factory Method creates iterators. Memento saves the position. Visitor runs operations during iteration.
- **Python:** WordsCollection with an `__iter__` that returns a fresh ascending iterator, plus a reverse-iterator method. AlphabeticalOrderIterator holds the traversal state and reads the collection's private list. Features: `collections.abc.Iterable` and `Iterator` (not `abc.ABC` directly), `__iter__`, `__next__`, `__getitem__`, a lazy sort on first `__next__`, `list[Any] | None`. Usage note: "very common" in Python. Idiomatic alternative [I]: a generator function with `yield` (or `sorted(...)` inside `__iter__`) replaces the iterator class. The example's own note hints at this; the page does not show it.

#### 16. Mediator
Source: https://refactoring.guru/design-patterns/mediator

- **Intent:** Objects communicate only through one intermediary, which lowers coupling.
- **Problem:** A profile dialog: a "has dog" checkbox reveals a breed field, and submit validates everything. Logic inside each control couples the controls to each other.
- **Solution:** Controls notify a mediator instead of each other. The dialog can be the mediator. A shared mediator interface lets other dialogs reuse the controls.
- **Roles:** Components (hold the mediator through an interface); Mediator interface (usually one `notify` method); Concrete Mediator (knows its components and may create them).
- **Use when:** classes are tightly interdependent; components cannot be reused because of their neighbours; reuse otherwise needs many subclasses; coordination should be swappable by swapping the mediator.
- **Steps:** find the coupled group; define a mediator interface; a concrete mediator holds the components; optionally create or destroy components; pass the mediator in the constructor; replace direct calls with notifications.
- **Pros:** centralised communication; new mediators added without changing components; lower coupling.
- **Cons:** the mediator can become a "God object".
- **Relations:** Facade vs Mediator: a facade adds no behaviour and subsystem objects still talk directly; components talk to a mediator. Mediator is often built on Observer's mechanism.
- **Python:** Abstract Mediator with `notify`; ConcreteMediator holds both components and dispatches by event label; BaseComponent with a mediator property; two components report to the mediator instead of calling each other. Features: `abc.ABC` on the mediator only (no `@abstractmethod`), `@property`, forward references. Usage note: most common in GUI coordination; the mediator plays the controller in MVC. Complexity and popularity ratings are blank in the captured text. Idiomatic alternative [I]: a plain event bus, or callbacks registered in a dict.

#### 17. Memento
Source: https://refactoring.guru/design-patterns/memento

- **Intent:** Save and restore an object's state without exposing its internals.
- **Problem:** Undo in a text editor covers text, formatting and images. Copying fields out either breaks encapsulation or ties the history to every internal field.
- **Solution:** The owner makes its own snapshot (a memento) and keeps it in an opaque container. Outsiders see only metadata (timestamp, operation name). The owner restores from the snapshot.
- **Roles:** Originator (creates and restores snapshots); Memento (immutable snapshot, visible only to the originator); Caretaker (keeps the history and decides when to save or restore; cannot read contents).
- **Use when:** undo/redo; rollback of failed operations (transactions); exposing fields would break encapsulation.
- **Steps:** identify the originator; the memento mirrors the state, is immutable, and is set via the constructor; nest it in the originator, or expose a metadata-only interface; the originator produces and restores from mementos; the caretaker manages timing and storage; optionally move restore logic into the memento.
- **Pros:** encapsulation kept; simpler originator.
- **Cons:** memory use from frequent snapshots; cleanup needed; immutability is not guaranteed in Python, JS or PHP.
- **Relations:** Command plus Memento for undo; Iterator state rollback; Prototype is simpler when state has no hard-to-recreate external links.
- **Analogy:** none. The page uses editor undo as its running example.
- **Python:** Originator with save, restore and a state-changing method; an abstract Memento that exposes only metadata; a ConcreteMemento keeping state and timestamp; a Caretaker that keeps a stack of snapshots and undoes. Features: `abc.ABC`, `@abstractmethod`, `@staticmethod`, `datetime`, `try/except` in undo. Privacy is by naming convention only. Usage note: the page says serialisation can implement the pattern, common in Python, but it is not the only or most efficient way. Idiomatic alternative [I]: a frozen dataclass or a plain dict snapshot, plus `copy.deepcopy`, is usually enough. The page does not show these.

#### 18. Observer
Source: https://refactoring.guru/design-patterns/observer

- **Intent:** Subscribers are notified when events occur in a publisher.
- **Problem:** A shopper wants a restock alert. Visiting the shop wastes trips; mass emailing spams everyone.
- **Solution:** The publisher keeps a subscriber list. Subscribers join and leave at runtime. The publisher calls a shared notify method, optionally passing event data. A helper object may manage subscriptions.
- **Roles:** Publisher (raises events; add and remove); Subscriber interface (one `notify`/`update` method); Concrete Subscribers; Client (wires them up).
- **Use when:** one object's change must update others, and the set of others is unknown or dynamic; observation is temporary or conditional; GUI event handlers.
- **Steps:** split the core publisher from the reactors; define a subscriber interface; add and remove methods typed to that interface; put subscription logic in a base class or helper; notify on events; decide whether data is pushed or pulled; the client wires everything.
- **Pros:** subscribers added without touching the publisher; wiring at runtime.
- **Cons:** no guaranteed notification order.
- **Relations:** Mediator is often built on Observer's mechanism. Observer creates one-way links; Mediator centralises the communication.
- **Analogy:** a magazine subscription.
- **Python:** Abstract Subject (attach, detach, notify); ConcreteSubject with state and an observer list; abstract Observer with `update`; two concrete observers that react under conditions. Features: `abc.ABC`, `@abstractmethod`, `typing.List`, `random.randrange`. The observer list is a class-level attribute, so all instances share one mutable list; the page flags this as a pitfall. Usage note: "common", especially in GUIs. Idiomatic alternative [I]: plain callables in a list are the idiomatic subscribers. The page notes this in passing.

#### 19. State
Source: https://refactoring.guru/design-patterns/state

- **Intent:** An object changes its behaviour as its internal state changes, so it appears to switch class.
- **Problem:** A document is Draft, Moderation or Published, and "publish" does something different in each. Conditionals in every method become hard to maintain.
- **Solution:** One class per state holds that state's behaviour. The context holds the current state object and delegates to it. Transitions swap the reference. States share an interface and may trigger transitions themselves (unlike Strategy).
- **Roles:** Context; State interface; concrete states (may share an abstract base).
- **Use when:** behaviour depends heavily on state; there are many states; state-specific code changes often; big conditionals test a state field.
- **Steps:** pick the context; a state interface with only the varying operations; a class per state; a state-typed field and setter on the context; replace conditionals with delegation; create state instances from the context, a state, or the client.
- **Pros:** single responsibility; states added without changing others; simpler context.
- **Cons:** excessive for few or rarely changing states.
- **Relations:** Bridge, Strategy and Adapter are structurally similar. State is "an extension of Strategy" in which states can trigger transitions.
- **Analogy:** smartphone buttons behave differently when unlocked, locked, or low on battery.
- **Python:** Context holding the current state, forwarding requests, plus `transition_to`; abstract State with two handlers and a back-reference to the context; two concrete states that switch the context to each other. Features: `abc.ABC`, `@abstractmethod`, `@property` with setter, forward references. Usage note: "commonly used" to replace switch-based state machines. The page gives no data behind "commonly". Idiomatic alternative [I]: a dict of handler functions, or an Enum-keyed transition table, is simpler when states carry little behaviour.

#### 20. Strategy
Source: https://refactoring.guru/design-patterns/strategy

- **Intent:** Put interchangeable algorithms into separate classes.
- **Problem:** A navigation app adds walking, transit, cycling and tourist routes to one growing navigator class. That causes merge conflicts and fragile changes.
- **Solution:** Each route method becomes a strategy with a shared build-route operation. The navigator holds the active strategy and delegates to it. Strategies swap at runtime, and new options do not touch the navigator.
- **Roles:** Context; Strategy interface; concrete strategies; Client (picks and sets the strategy, often through a setter).
- **Use when:** algorithm variants are switched at runtime; many similar classes differ in one behaviour; core logic should be separated from algorithm details; a large conditional chooses the algorithm.
- **Steps:** find the frequently changing algorithm or big conditional; define the interface; move each variant into a class; give the context a strategy field with a setter; the context calls only the interface; the client selects.
- **Pros:** runtime swap; isolation; composition over inheritance; open/closed principle.
- **Cons:** extra classes for few stable algorithms; clients must know the differences; first-class functions or lambdas can often replace the classes.
- **Relations:** Bridge, State and Adapter are structurally similar. Command wraps an operation for deferred or history use; Strategy swaps methods of one task. Decorator changes the outer behaviour; Strategy changes the inner logic. Template Method uses inheritance and is fixed at compile time; Strategy uses composition and works at runtime. State extends Strategy.
- **Analogy:** getting to the airport by bus, taxi or bicycle.
- **Python:** A Context with a `strategy` property that delegates to the current strategy; abstract Strategy with `do_algorithm`; ConcreteStrategyA (ascending) and ConcreteStrategyB (descending). Features: `abc.ABC`, `@abstractmethod`, `@property` setter, `typing.List`. Note: the page's `reversed` returns an iterator, which does not match its `List` annotation [V, from the note]. Usage note: "very common" in frameworks that let users customise without subclassing. Idiomatic alternative [I]: pass a function (e.g. `sorted` with `key` and `reverse`) instead of a strategy class. This is the clearest case of the Strategy vs first-class-function swap.

#### 21. Template Method
Source: https://refactoring.guru/design-patterns/template-method

- **Intent:** A base class fixes the skeleton of an algorithm; subclasses fill in the steps.
- **Problem:** Data mining over DOC, CSV and PDF files. Each format needs its own parsing, but analysis and reporting are nearly identical. The client has type checks, and changes touch many classes.
- **Solution:** Split the algorithm into named steps. The base class has one template method that calls them in order. Steps are abstract (subclasses must implement), default (may be overridden), or hooks (empty extension points). Shared logic moves up; format logic stays down.
- **Roles:** Abstract class (steps and the template method); concrete classes (implement abstract steps, optionally override others, never touch the template method).
- **Use when:** clients customise parts while the structure stays fixed; several classes have near-identical algorithms that differ slightly.
- **Steps:** study the algorithm; a base class with the template method; consider making the template non-overridable; default implementations for shared steps; abstract methods for variable steps; hooks at key points; one subclass per variation.
- **Pros:** clients change only what they need; duplication removed.
- **Cons:** the fixed skeleton may restrict; suppressing a default step can violate Liskov; many steps are hard to maintain.
- **Relations:** Factory Method is a specialised Template Method. Strategy is the compositional, runtime alternative.
- **Analogy:** mass housing built from one standard plan with per-house variations.
- **Python:** AbstractClass with a `template_method` that fixes step order; concrete steps; abstract steps; empty hook methods. ConcreteClass1 implements the required steps; ConcreteClass2 also overrides a hook. Features: `abc.ABC`, `@abstractmethod`, default methods, plain inheritance. No Protocol. Usage note: "common" in Python frameworks as an extension point through inheritance. Idiomatic alternative [I]: passing the varying steps as callables to one function, or using `Protocol`-typed parameters, is often simpler than inheritance.

#### 22. Visitor
Source: https://refactoring.guru/design-patterns/visitor

- **Intent:** Move an operation out of the objects it acts on, so new operations need no change to those objects.
- **Problem:** A geodata graph of cities and industries must export to XML. Adding export methods to the node classes is risky, the architect does not allow it, and more formats are expected later.
- **Solution:** The operation lives in a visitor class. Each node has one `accept` method that calls the visitor's matching visit method, so the node picks the right method and no type checks are needed. New behaviour means a new visitor.
- **Roles:** Visitor interface (one visit method per element type); concrete visitors; Element interface (`accept`); concrete elements; Client.
- **Use when:** operations span a structure with many classes (e.g. a tree); core classes should stay focused; behaviour applies to only some classes in a hierarchy.
- **Steps:** a visit method per element class; `accept` on the element interface; each element calls its own visit method; elements depend only on the visitor interface; one visitor per behaviour (it may need private data); the client passes visitors through `accept`.
- **Pros:** new behaviours without changing elements; one behaviour's versions grouped; visitors can accumulate state.
- **Cons:** every visitor must change when element classes change; visitors may lack access to private members.
- **Relations:** Visitor is a more powerful Command. Runs over Composite trees. Combined with Iterator for mixed types.
- **Analogy:** an insurance agent who offers different policies depending on the building type.
- **Python:** Element interface with `accept`; two element classes, each with an extra method; Visitor interface with one operation per element type; two concrete visitors; the client loops and passes one visitor to every element (double dispatch). Features: `abc.ABC`, `@abstractmethod`, `typing.List`, forward references. No `__call__` and no `functools.singledispatch`. Usage note: the page says it is not very common, because of its complexity and narrow applicability. It gives no Python-specific guidance. Idiomatic alternative [I]: `functools.singledispatch`, or `match` statements over node types (Python 3.10+), often replaces the double-dispatch boilerplate.

---

## 5. Patterns that get confused

Relations from the notes, grouped into comparisons. All [V] unless tagged [I].

| Pair | Key difference |
|---|---|
| **Strategy vs State** | Both delegate to a swappable object. In Strategy the client picks the algorithm and strategies do not switch each other. In State, states trigger their own transitions. State is "an extension of Strategy". |
| **Decorator vs Proxy vs Adapter** | Adapter changes the interface. Decorator keeps and extends it, and decorators stack. Proxy keeps it and controls access or lifecycle of one service. The client composes decorators; a proxy manages its service. |
| **Factory Method vs Abstract Factory vs Builder** | Factory Method makes one product, chosen by a subclass. Abstract Factory makes a family of matching products at once. Builder assembles one product in steps, with extra steps allowed before retrieval. Designs often start at Factory Method and grow into the other two. |
| **Mediator vs Observer** | Observer creates one-way links from publisher to subscribers. Mediator centralises two-way coordination; components talk to the mediator, not to each other. A mediator is often built on Observer's mechanism. |
| **Command vs Strategy** | Command wraps a request as an object for queueing, logging or undo. Strategy swaps how one task is done. |
| **Facade vs Mediator** | A facade adds no behaviour and the subsystem does not know it exists; the subsystem's objects still talk directly. A mediator is the hub that components talk through. |
| **Facade vs Adapter** | Adapter wraps one object to fit an interface. Facade defines a new interface over a whole subsystem. |
| **Facade vs Proxy** | Both wrap a complex object. A proxy matches the service's interface and can replace it. A facade has a different, simpler interface and is not interchangeable. |
| **Singleton vs Flyweight** | Singleton has exactly one instance, possibly mutable. Flyweight allows many instances, each with immutable shared state. |
| **Facade vs Flyweight** | Facade: one object for a whole subsystem. Flyweight: many small objects that share data. |
| **Bridge vs State vs Strategy vs Adapter** | All use composition in similar shapes. Intent differs. Adapter is retrofitted; Bridge is planned up front. |
| **Chain of Responsibility vs Decorator** | Both have a similar shape. A handler may stop the chain; a decorator must not break request flow. |
| **Template Method vs Strategy** | Template Method uses inheritance and is fixed at compile time. Strategy uses composition and can change at runtime. Factory Method is a specialised Template Method. |
| **Composite vs Decorator** | Composite groups many children. Decorator wraps one object. The two can be combined. |
| **Visitor vs Command** | The notes call Visitor "a more powerful Command". |
| **Prototype vs Memento** | Prototype is simpler when state has no hard-to-recreate external links. Memento is for undo or rollback of state. |

Iterator and Visitor also meet: Visitor can run operations during iteration (Iterator note). Command and Chain of Responsibility also meet: handlers can be commands.

---

## 6. What we don't know

### 6.1 Contradictions in the notes, and how each is handled

- **22 vs 23 patterns.** The catalogue lists 22; the history page says the 1994 GoF book had 23. Handled: the site's 22 are a classic subset, and the notes are not silently aligned to either number. The missing pattern is not named in any note. Outside the notes, and unverified: the GoF book's other behavioural pattern is Interpreter, which is absent from all 22 notes. That is my recollection, not a checked fact.
- **Pattern-part names.** The landing page describes the parts differently from the what-is-pattern sub-page. The notes treat the sub-page as authoritative, but do not record the landing wording. Also, the sub-page's list (Intent, Motivation, Structure, Code example) has no Problem or Solution, yet every per-pattern note uses those labels. Not resolved: whether pattern pages have Problem and Solution headings, or whether they sit inside Motivation. [I] My guess is the latter; it needs a raw-page check.
- **Decorator and the Python cross-cutting list.** The Python notes list Decorator twice: once under "function-style" and once under "already in the language". Handled: the GoF Decorator is a class wrapper and Python's `@decorator` is a different mechanism with the same name. Singleton and Iterator also appear in both lists; there the two entries agree (module and `__iter__`/`yield`).
- **Creational caveat count.** The creational notes say "All 10 pages" and list parts that add to 13. Handled: no fact depends on this count; the page list was used as given.
- **Adapter target.** The general Adapter description uses a client interface. The Python example's Target is concrete. Not a contradiction; recorded as variance.
- **Cross-cutting claim.** The Python notes say `abc.ABC` with `@abstractmethod` is the most common feature. I counted from the notes: `abc.ABC` appears in 15 of 22 examples; `@abstractmethod` in 14 (Mediator uses `abc.ABC` without it). [I] Counted by me from the notes, not the code.

### 6.2 Open questions, with sources searched and who could answer

| Question | Searched so far | Who or what could answer |
|---|---|---|
| Which GoF pattern is not in the site's 22? | Catalogue, classification and history summaries (in the notes). None names it. | The 1994 GoF book's table of contents; or the raw HTML of `/design-patterns/catalog` and `/history`. |
| Do pattern pages use Problem and Solution headings? | What-is-pattern summary; the notes' per-pattern labels. | A raw fetch of 2 to 3 pattern pages (e.g. Factory Method, Strategy). |
| What does the landing page say about pattern parts? | Landing summary; the note records only that it differs. | A raw fetch of `https://refactoring.guru/design-patterns`. |
| Are the summarised facts accurate? | Every fact is a WebFetch summary from a small model. Nothing checked against raw text. | A raw fetch (curl or a browser) of all 4 index pages and 22 pattern pages. Check first: numbers, dates (1994, the four authors), and the roles listed for each Python example. |
| How common is each pattern? | The notes contain only wording ("very common", "fairly common", "commonly used", "not very common"). No data behind any of them. | No source in the notes. Would need an outside usage study. |
| Do the Python examples run, and do they match their descriptions? | Not run. Notes describe them from summaries. | Run each example in its own scratch directory, with `python3 -I`, once the code has been fetched. |
| Are the [I] "idiomatic Python" alternatives right? | Inferred by the note author; the site does not state them. | A reviewer who writes each alternative and checks it against the GoF example's behaviour. Standard-library claims (`functools.singledispatch`, `sys.intern`, `functools.lru_cache`) can be checked in the Python docs. |
| What are the complexity and popularity ratings? | Blank in the captured text (Python intro; Mediator Python page). | Raw fetch of the Python index and the Mediator Python page. |
| Site code quirks: Builder return type; Strategy `reversed` type. | Noted from summaries. | Raw fetch of the two Python pages. |
| Analogies for Flyweight and Memento. | Notes say none (Flyweight uses particle and forest examples instead). | Not an open issue; recorded as a fact of the site. |

### 6.3 Sources used in this synthesis

- Four note files only: /tmp/claude-1000/-home-karim-Desktop-projects-karim-skills/ec682d62-b0b7-45c4-a57d-2d90895cd6bb/scratchpad/patterns-creational.md, /tmp/claude-1000/-home-karim-Desktop-projects-karim-skills/ec682d62-b0b7-45c4-a57d-2d90895cd6bb/scratchpad/patterns-structural.md, /tmp/claude-1000/-home-karim-Desktop-projects-karim-skills/ec682d62-b0b7-45c4-a57d-2d90895cd6bb/scratchpad/patterns-behavioral.md, /tmp/claude-1000/-home-karim-Desktop-projects-karim-skills/ec682d62-b0b7-45c4-a57d-2d90895cd6bb/scratchpad/patterns-python.md
- No new web fetches were made for this document.
