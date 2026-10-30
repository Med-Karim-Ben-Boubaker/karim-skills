# Facade

**Intent:** One simple entry point in front of a complex subsystem.

**Earned when:** callers repeat the same setup and call order against a library or subsystem, and vendor details leak into business code.

**Simplest form first:** a module with a few functions.

**Roles:** facade (delegates and sequences calls), subsystem (unaware of the facade), client.

In `video.py`:

```python
def convert(path: Path, fmt: str) -> Path:
    clip = ffmpeg.input(str(path))
    out = path.with_suffix(f".{fmt}")
    clip.output(str(out), codec=CODECS[fmt]).run()
    return out
```

**Costs:** grows into a catch-all coupled to everything; split it by task when it does.

**Not to be confused with:** Adapter (makes one object fit an existing interface); Mediator (components talk through it; a facade adds no coordination of its own); Proxy (same interface as the service).
