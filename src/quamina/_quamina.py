"""Python wrapper for the Quamina pattern matching library."""

import ctypes
import json
import platform
from pathlib import Path
from typing import Any, Self


class QuaminaError(Exception):
    """Base exception for Quamina errors."""


class QuaminaLibrary:
    """Low-level wrapper for the Quamina C library."""

    def __init__(self) -> None:
        """Load the Quamina shared library."""
        lib_path = self._find_library()
        self._lib = ctypes.CDLL(str(lib_path))

        # Define function signatures
        # Define function signatures
        self._lib.QuaminaNew.argtypes = []
        self._lib.QuaminaNew.restype = ctypes.c_int

        self._lib.QuaminaFree.argtypes = [ctypes.c_int]
        self._lib.QuaminaFree.restype = None

        self._lib.QuaminaAddPattern.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        self._lib.QuaminaAddPattern.restype = ctypes.c_void_p

        self._lib.QuaminaDeletePatterns.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self._lib.QuaminaDeletePatterns.restype = ctypes.c_void_p

        self._lib.QuaminaMatchesForEvent.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self._lib.QuaminaMatchesForEvent.restype = ctypes.c_void_p

        self._lib.QuaminaFreeString.argtypes = [ctypes.c_void_p]
        self._lib.QuaminaFreeString.restype = None

    def _find_library(self) -> Path:
        """Find the shared library based on the current platform."""
        system = platform.system()
        if system == "Darwin":
            lib_name = "libquamina.dylib"
        elif system == "Linux":
            lib_name = "libquamina.so"
        elif system == "Windows":
            lib_name = "libquamina.dll"
        else:
            msg = f"Unsupported platform: {system}"
            raise QuaminaError(msg)

        lib_path = Path(__file__).parent / "lib" / lib_name
        if not lib_path.exists():
            msg = f"Quamina library not found at {lib_path}"
            raise QuaminaError(msg)

        return lib_path

    def new(self) -> int:
        """Create a new Quamina instance."""
        handle = self._lib.QuaminaNew()
        if handle == 0:
            msg = "Failed to create Quamina instance"
            raise QuaminaError(msg)
        return handle

    def free(self, handle: int) -> None:
        """Free a Quamina instance."""
        self._lib.QuaminaFree(handle)

    def add_pattern(self, handle: int, pattern_id: str, pattern_json: str) -> None:
        """Add a pattern to the Quamina instance."""
        error_ptr = self._lib.QuaminaAddPattern(
            handle,
            pattern_id.encode("utf-8"),
            pattern_json.encode("utf-8"),
        )
        if error_ptr is not None and error_ptr != 0:
            error_msg = ctypes.string_at(error_ptr).decode("utf-8")
            self._lib.QuaminaFreeString(error_ptr)
            raise QuaminaError(error_msg)

    def delete_patterns(self, handle: int, pattern_id: str) -> None:
        """Delete patterns with the given ID."""
        error_ptr = self._lib.QuaminaDeletePatterns(
            handle,
            pattern_id.encode("utf-8"),
        )
        if error_ptr is not None and error_ptr != 0:
            error_msg = ctypes.string_at(error_ptr).decode("utf-8")
            self._lib.QuaminaFreeString(error_ptr)
            raise QuaminaError(error_msg)

    def matches_for_event(self, handle: int, event_json: str) -> list[str]:
        """Get matching pattern IDs for an event."""
        result_ptr = self._lib.QuaminaMatchesForEvent(
            handle,
            event_json.encode("utf-8"),
        )
        if result_ptr is None or result_ptr == 0:
            return []

        try:
            result_json = ctypes.string_at(result_ptr).decode("utf-8")
            return json.loads(result_json)
        finally:
            self._lib.QuaminaFreeString(result_ptr)


class Quamina:
    """High-level Python interface to Quamina pattern matching."""

    def __init__(self) -> None:
        """Create a new Quamina instance."""
        self._lib = QuaminaLibrary()
        self._handle = self._lib.new()

    def __del__(self) -> None:
        """Clean up the Quamina instance."""
        if hasattr(self, "_handle"):
            self._lib.free(self._handle)

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        self._lib.free(self._handle)

    def add_pattern(self, pattern_id: str, pattern: dict[str, Any]) -> None:
        """
        Add a pattern to match against.

        Args:
            pattern_id: Unique identifier for this pattern
            pattern: Pattern dictionary (will be converted to JSON)

        Raises:
            QuaminaError: If the pattern is invalid
        """
        pattern_json = json.dumps(pattern)
        self._lib.add_pattern(self._handle, pattern_id, pattern_json)

    def delete_patterns(self, pattern_id: str) -> None:
        """
        Delete all patterns with the given ID.

        Args:
            pattern_id: Pattern identifier to delete

        Raises:
            QuaminaError: If deletion fails
        """
        self._lib.delete_patterns(self._handle, pattern_id)

    def matches_for_event(self, event: dict[str, Any]) -> list[str]:
        """
        Find all patterns that match the given event.

        Args:
            event: Event dictionary (will be converted to JSON)

        Returns:
            List of pattern IDs that matched

        Raises:
            QuaminaError: If matching fails
        """
        event_json = json.dumps(event)
        return self._lib.matches_for_event(self._handle, event_json)
