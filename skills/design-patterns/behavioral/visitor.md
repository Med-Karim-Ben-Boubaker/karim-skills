# Visitor

**Intent:** Move an operation out of the classes of a structure, so new operations don't change those classes.

**Earned when:** many new operations (export, validate, render) run over a stable set of node types, and adding each one to every class is costly or forbidden.

**Simplest form first:** `functools.singledispatch` or a `match` statement over the node types.

**Roles:** visitor interface (one method per element type), concrete visitors, element interface (`accept`), concrete elements, client.

```python
@functools.singledispatch
def to_xml(node) -> str: raise TypeError(node)

@to_xml.register
def _(node: City) -> str: return f"<city name='{node.name}'/>"
```

**Costs:** every visitor must change when a node type is added; visitors may need access to private state.

**Not to be confused with:** Iterator (walks elements; a visitor operates on them); Command (a visitor is a command that works on many types).
