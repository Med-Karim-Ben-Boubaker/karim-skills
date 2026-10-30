# Bridge

**Intent:** Split a class that varies in two independent ways into two hierarchies joined by composition.

**Earned when:** subclasses multiply as the product of two dimensions (`PdfInvoice`, `HtmlInvoice`, `PdfReceipt`, ...).

**Simplest form first:** pass the second dimension in as an object or a callable at construction.

**Roles:** abstraction (holds an implementation), refined abstractions, implementation interface, concrete implementations.

```python
class Report:
    def __init__(self, renderer: Renderer): self._renderer = renderer

class InvoiceReport(Report):
    def render(self, invoice) -> bytes:
        return self._renderer.table(invoice.lines)
```

**Costs:** needless indirection when the class doesn't actually vary in two ways.

**Not to be confused with:** Adapter (retrofitted to fix a mismatch; Bridge is planned up front); Strategy (swaps one algorithm, not a whole dimension).
