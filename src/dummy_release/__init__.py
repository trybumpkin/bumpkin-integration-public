"""Synthetic greeting package, not a production dependency."""


def greet(name: str, *, excited: bool = False) -> str:
    """Return a greeting for the supplied name."""
    emphasis = "!!" if excited else "!"
    return f"Hello, {name}{emphasis}"
