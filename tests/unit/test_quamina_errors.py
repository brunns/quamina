"""Test error handling and edge cases."""

import pathlib
import platform

import pytest
from hamcrest import assert_that, equal_to

from quamina import Quamina, QuaminaError
from quamina._quamina import QuaminaLibrary


def test_unsupported_platform(when):
    """Test error when running on unsupported platform."""
    when(platform).system().thenReturn("AmigaOS")
    with pytest.raises(QuaminaError, match="Unsupported platform"):
        QuaminaLibrary()


def test_library_not_found(when):
    """Test error when library file doesn't exist."""
    when(platform).system().thenReturn("Linux")
    when(pathlib.Path).exists(...).thenReturn(False)  # noqa: FBT003
    with pytest.raises(QuaminaError, match="library not found"):
        QuaminaLibrary()


def test_windows_library_name(when):
    """Test that Windows uses .dll extension."""
    when(platform).system().thenReturn("Windows")
    when(pathlib.Path).exists(...).thenReturn(False)  # noqa: FBT003
    with pytest.raises(QuaminaError, match="libquamina.dll"):
        QuaminaLibrary()


def test_instance_creation_failure(when):
    """Test error when Quamina instance creation fails."""
    lib = QuaminaLibrary()

    # Mock QuaminaNew to return 0 (failure)
    when(lib._lib).QuaminaNew().thenReturn(0)

    with pytest.raises(QuaminaError, match="Failed to create"):
        lib.new()


def test_add_pattern_invalid_handle():
    """Test adding pattern with invalid handle."""
    lib = QuaminaLibrary()

    # Use an invalid handle (999 doesn't exist)
    with pytest.raises(QuaminaError, match="invalid handle"):
        lib.add_pattern(999, "test", '{"x": [1]}')


def test_delete_patterns_invalid_handle():
    """Test deleting patterns with invalid handle."""
    lib = QuaminaLibrary()

    with pytest.raises(QuaminaError, match="invalid handle"):
        lib.delete_patterns(999, "test")


def test_matches_for_event_invalid_handle():
    """Test matching with invalid handle returns empty list."""
    lib = QuaminaLibrary()

    # Invalid handle should return empty list
    matches = lib.matches_for_event(999, '{"x": 1}')
    assert_that(matches, equal_to([]))


def test_context_manager_cleanup():
    """Test that context manager properly cleans up."""
    with Quamina() as q:
        q.add_pattern("test", {"x": [1]})
        matches = q.matches_for_event({"x": 1})
        assert_that(len(matches), equal_to(1))

    # After exiting context, the instance should be freed
    # (no way to directly test this, but it shouldn't crash)


def test_destructor_cleanup():
    """Test that destructor properly cleans up."""
    q = Quamina()
    q.add_pattern("test", {"x": [1]})

    # Delete the instance
    del q

    # The Go instance should be freed
    # (no way to directly test this, but it shouldn't crash)


def test_unicode_in_pattern():
    """Test patterns with unicode characters."""
    q = Quamina()

    q.add_pattern("unicode", {"name": ["こんにちは", "Hello"]})

    matches = q.matches_for_event({"name": "こんにちは"})
    assert_that(len(matches), equal_to(1))


def test_unicode_in_event():
    """Test events with unicode characters."""
    q = Quamina()

    q.add_pattern("test", {"emoji": ["🎉", "🎊"]})

    matches = q.matches_for_event({"emoji": "🎉"})
    assert_that(len(matches), equal_to(1))


def test_special_characters():
    """Test special characters in patterns and events."""
    q = Quamina()

    q.add_pattern("special", {"path": ["/test/path", "/other/path"]})

    matches = q.matches_for_event({"path": "/test/path"})
    assert_that(len(matches), equal_to(1))


def test_matches_for_event_null_pointer(when):
    """Test that matches_for_event handles NULL pointer from Go library gracefully.

    This tests the error path when the Go library returns NULL (catastrophic failure).
    """
    q = Quamina()
    q.add_pattern("test", {"x": [1]})

    # Mock the Go library to return None (simulating NULL pointer)
    when(q._lib._lib).QuaminaMatchesForEvent(...).thenReturn(None)
    matches = q._lib.matches_for_event(q._handle, '{"x": 1}')

    # Should return empty list, not crash
    assert_that(matches, equal_to([]))
