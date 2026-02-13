"""Unit tests for Quamina pattern matching."""

import pytest
from hamcrest import assert_that, contains_inanyorder, empty

from quamina import Quamina, QuaminaError


class TestQuaminaBasics:
    """Test basic Quamina functionality."""

    def test_create_instance(self):
        """Test creating a Quamina instance."""
        q = Quamina()
        assert q is not None

    def test_context_manager(self):
        """Test using Quamina as a context manager."""
        with Quamina() as q:
            assert q is not None

    def test_add_pattern_and_match(self):
        """Test adding a pattern and matching an event."""
        q = Quamina()

        # Add a simple pattern
        pattern = {"x": [1, 2]}
        q.add_pattern("test-pattern", pattern)

        # Match with an event that should match
        event = {"x": 1}
        matches = q.matches_for_event(event)

        assert_that(matches, contains_inanyorder("test-pattern"))

    def test_no_match(self):
        """Test that non-matching events return empty list."""
        q = Quamina()

        pattern = {"x": [1, 2]}
        q.add_pattern("test-pattern", pattern)

        # Event that doesn't match
        event = {"x": 3}
        matches = q.matches_for_event(event)

        assert_that(matches, empty())

    def test_multiple_patterns(self):
        """Test matching against multiple patterns."""
        q = Quamina()

        # Add multiple patterns
        q.add_pattern("pattern-1", {"x": [1]})
        q.add_pattern("pattern-2", {"x": [2]})
        q.add_pattern("pattern-3", {"y": ["test"]})

        # Event that matches pattern-1 only
        matches = q.matches_for_event({"x": 1})
        assert_that(matches, contains_inanyorder("pattern-1"))

        # Event that matches pattern-3 only
        matches = q.matches_for_event({"y": "test"})
        assert_that(matches, contains_inanyorder("pattern-3"))

        # Event that matches nothing
        matches = q.matches_for_event({"z": 99})
        assert_that(matches, empty())

    def test_complex_pattern(self):
        """Test a more complex pattern with nested objects."""
        q = Quamina()

        pattern = {
            "Image": {
                "Width": [800],
                "Animated": [False],  # noqa: FBT003
            }
        }
        q.add_pattern("image-pattern", pattern)

        # Matching event
        event = {"Image": {"Width": 800, "Height": 600, "Animated": False}}
        matches = q.matches_for_event(event)
        assert_that(matches, contains_inanyorder("image-pattern"))

        # Non-matching event (different width)
        event = {"Image": {"Width": 1024, "Height": 768, "Animated": False}}
        matches = q.matches_for_event(event)
        assert_that(matches, empty())


class TestPatternManagement:
    """Test pattern addition and deletion."""

    def test_delete_pattern(self):
        """Test deleting a pattern."""
        q = Quamina()

        q.add_pattern("temp-pattern", {"x": [1]})

        # Should match
        matches = q.matches_for_event({"x": 1})
        assert_that(matches, contains_inanyorder("temp-pattern"))

        # Delete the pattern
        q.delete_patterns("temp-pattern")

        # Should no longer match
        matches = q.matches_for_event({"x": 1})
        assert_that(matches, empty())

    def test_same_pattern_id_multiple_times(self):
        """Test adding patterns with the same ID."""
        q = Quamina()

        # Add two patterns with the same ID
        q.add_pattern("dup-id", {"x": [1]})
        q.add_pattern("dup-id", {"y": [2]})

        # Both should match their respective events
        matches = q.matches_for_event({"x": 1})
        assert_that(matches, contains_inanyorder("dup-id"))

        matches = q.matches_for_event({"y": 2})
        assert_that(matches, contains_inanyorder("dup-id"))

        # Delete all patterns with this ID
        q.delete_patterns("dup-id")

        # Neither should match anymore
        matches = q.matches_for_event({"x": 1})
        assert_that(matches, empty())

        matches = q.matches_for_event({"y": 2})
        assert_that(matches, empty())


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_pattern(self):
        """Test that invalid patterns raise errors."""
        q = Quamina()

        # Quamina patterns require leaf values to be arrays
        invalid_pattern = {"x": 1}  # Should be {"x": [1]}

        with pytest.raises(QuaminaError):
            q.add_pattern("bad-pattern", invalid_pattern)

    def test_delete_nonexistent_pattern(self):
        """Test deleting a pattern that doesn't exist."""
        q = Quamina()

        # This should not raise an error (Quamina allows this)
        q.delete_patterns("nonexistent-pattern")


class TestPatternTypes:
    """Test different pattern matching types."""

    def test_string_matching(self):
        """Test matching with string values."""
        q = Quamina()

        q.add_pattern("string-pattern", {"name": ["Alice", "Bob"]})

        matches = q.matches_for_event({"name": "Alice"})
        assert_that(matches, contains_inanyorder("string-pattern"))

        matches = q.matches_for_event({"name": "Charlie"})
        assert_that(matches, empty())

    def test_numeric_matching(self):
        """Test matching with numeric values."""
        q = Quamina()

        q.add_pattern("number-pattern", {"count": [42, 100]})

        matches = q.matches_for_event({"count": 42})
        assert_that(matches, contains_inanyorder("number-pattern"))

        matches = q.matches_for_event({"count": 50})
        assert_that(matches, empty())

    def test_boolean_matching(self):
        """Test matching with boolean values."""
        q = Quamina()

        q.add_pattern("bool-pattern", {"active": [True]})  # noqa: FBT003

        matches = q.matches_for_event({"active": True})
        assert_that(matches, contains_inanyorder("bool-pattern"))

        matches = q.matches_for_event({"active": False})
        assert_that(matches, empty())

    def test_null_matching(self):
        """Test matching with null values."""
        q = Quamina()

        q.add_pattern("null-pattern", {"value": [None]})

        matches = q.matches_for_event({"value": None})
        assert_that(matches, contains_inanyorder("null-pattern"))

        matches = q.matches_for_event({"value": "something"})
        assert_that(matches, empty())


class TestMultipleMatches:
    """Test scenarios with multiple matching patterns."""

    def test_multiple_patterns_match_same_event(self):
        """Test when multiple patterns match the same event."""
        q = Quamina()

        q.add_pattern("pattern-1", {"x": [1]})
        q.add_pattern("pattern-2", {"x": [1, 2]})
        q.add_pattern("pattern-3", {"y": [5]})

        event = {"x": 1, "y": 5}
        matches = q.matches_for_event(event)

        # All three patterns should match
        assert_that(matches, contains_inanyorder("pattern-1", "pattern-2", "pattern-3"))


class TestEmptyEvents:
    """Test handling of empty events and patterns."""

    def test_empty_event(self):
        """Test matching against an empty event."""
        q = Quamina()

        q.add_pattern("pattern-1", {"x": [1]})

        matches = q.matches_for_event({})
        assert_that(matches, empty())

    def test_event_with_extra_fields(self):
        """Test that extra fields in events are ignored."""
        q = Quamina()

        q.add_pattern("pattern-1", {"x": [1]})

        # Event has extra fields that aren't in the pattern
        event = {"x": 1, "y": 2, "z": 3}
        matches = q.matches_for_event(event)

        assert_that(matches, contains_inanyorder("pattern-1"))
