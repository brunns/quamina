"""Test error handling and edge cases."""

from unittest.mock import Mock, patch

import pytest
from hamcrest import assert_that, equal_to

from quamina import Quamina, QuaminaError
from quamina._quamina import QuaminaLibrary


class TestLibraryLoading:
    """Test library loading and initialization errors."""

    def test_unsupported_platform(self):
        """Test error when running on unsupported platform."""
        with patch("platform.system", return_value="AmigaOS"):
            with pytest.raises(QuaminaError, match="Unsupported platform"):
                QuaminaLibrary()

    def test_library_not_found(self):
        """Test error when library file doesn't exist."""
        with patch("platform.system", return_value="Linux"):
            with patch("pathlib.Path.exists", return_value=False):
                with pytest.raises(QuaminaError, match="library not found"):
                    QuaminaLibrary()

    def test_windows_library_name(self):
        """Test that Windows uses .dll extension."""
        with patch("platform.system", return_value="Windows"):
            with patch("pathlib.Path.exists", return_value=False):
                with pytest.raises(QuaminaError, match="libquamina.dll"):
                    QuaminaLibrary()

    def test_instance_creation_failure(self):
        """Test error when Quamina instance creation fails."""
        lib = QuaminaLibrary()
        original_new = lib._lib.QuaminaNew

        # Mock QuaminaNew to return 0 (failure)
        lib._lib.QuaminaNew = Mock(return_value=0)

        with pytest.raises(QuaminaError, match="Failed to create"):
            lib.new()

        # Restore original function
        lib._lib.QuaminaNew = original_new


class TestInvalidHandle:
    """Test operations with invalid handles."""

    def test_add_pattern_invalid_handle(self):
        """Test adding pattern with invalid handle."""
        lib = QuaminaLibrary()

        # Use an invalid handle (999 doesn't exist)
        with pytest.raises(QuaminaError, match="invalid handle"):
            lib.add_pattern(999, "test", '{"x": [1]}')

    def test_delete_patterns_invalid_handle(self):
        """Test deleting patterns with invalid handle."""
        lib = QuaminaLibrary()

        with pytest.raises(QuaminaError, match="invalid handle"):
            lib.delete_patterns(999, "test")

    def test_matches_for_event_invalid_handle(self):
        """Test matching with invalid handle returns empty list."""
        lib = QuaminaLibrary()

        # Invalid handle should return empty list
        matches = lib.matches_for_event(999, '{"x": 1}')
        assert_that(matches, equal_to([]))


class TestMemoryManagement:
    """Test proper memory management."""

    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up."""
        with Quamina() as q:
            q.add_pattern("test", {"x": [1]})
            matches = q.matches_for_event({"x": 1})
            assert_that(len(matches), equal_to(1))

        # After exiting context, the instance should be freed
        # (no way to directly test this, but it shouldn't crash)

    def test_destructor_cleanup(self):
        """Test that destructor properly cleans up."""
        q = Quamina()
        q.add_pattern("test", {"x": [1]})

        # Delete the instance
        del q

        # The Go instance should be freed
        # (no way to directly test this, but it shouldn't crash)


class TestJSONEdgeCases:
    """Test JSON serialization edge cases."""

    def test_unicode_in_pattern(self):
        """Test patterns with unicode characters."""
        q = Quamina()

        q.add_pattern("unicode", {"name": ["こんにちは", "Hello"]})

        matches = q.matches_for_event({"name": "こんにちは"})
        assert_that(len(matches), equal_to(1))

    def test_unicode_in_event(self):
        """Test events with unicode characters."""
        q = Quamina()

        q.add_pattern("test", {"emoji": ["🎉", "🎊"]})

        matches = q.matches_for_event({"emoji": "🎉"})
        assert_that(len(matches), equal_to(1))

    def test_special_characters(self):
        """Test special characters in patterns and events."""
        q = Quamina()

        q.add_pattern("special", {"path": ["/test/path", "/other/path"]})

        matches = q.matches_for_event({"path": "/test/path"})
        assert_that(len(matches), equal_to(1))
