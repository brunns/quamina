"""Python wrapper for the Quamina pattern matching library."""

from quamina._quamina import Quamina, QuaminaError

__all__ = ["Quamina", "QuaminaError"]


def hello() -> str:
    """Legacy hello function for testing."""
    return "Hello from quamina!"
