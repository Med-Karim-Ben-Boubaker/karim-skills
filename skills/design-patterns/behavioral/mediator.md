# Mediator

**Intent:** Components stop calling each other and talk only through one coordinator.

**Earned when:** a group of objects call each other in a tangle, so none can be reused or changed alone (form fields, UI widgets, services that coordinate a workflow).

**Simplest form first:** an event bus or a dict of callbacks, when the coordination is simple.

**Roles:** mediator interface (usually one `notify`), concrete mediator (knows the components, holds the coordination rules), components (hold the mediator).

```python
class SignupForm:
    def notify(self, sender: Field, event: str) -> None:
        if sender is self.has_dog and event == "changed":
            self.breed.visible = self.has_dog.checked
```

**Costs:** the mediator can grow into a god object that knows everything.

**Not to be confused with:** Facade (adds no coordination, and the subsystem doesn't know it exists); Observer (one-way links; a mediator is often built on it).
