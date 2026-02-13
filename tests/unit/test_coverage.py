"""Tests to achieve 100% code coverage for edge cases."""

from unittest.mock import patch

from hamcrest import assert_that, equal_to

from quamina import Quamina


def test_matches_for_event_null_pointer():
    """Test that matches_for_event handles NULL pointer from Go library gracefully.

    This tests the error path when the Go library returns NULL (catastrophic failure).
    """
    q = Quamina()
    q.add_pattern("test", {"x": [1]})

    # Mock the Go library to return None (simulating NULL pointer)
    with patch.object(q._lib._lib, "QuaminaMatchesForEvent", return_value=None):
        matches = q._lib.matches_for_event(q._handle, '{"x": 1}')

    # Should return empty list, not crash
    assert_that(matches, equal_to([]))
