"""Tests for handler registration and event processing."""

from hamcrest import assert_that, contains_inanyorder, empty, equal_to, has_length
from mockito import mock, verify

from quamina import Quamina


def test_register_handler(when):
    """Test registering a handler for a pattern."""
    q = Quamina()
    handler = mock()
    when(handler).__call__({"x": 1}).thenReturn("handled")

    q.register_handler("test-pattern", {"x": [1]}, handler)

    # Process an event that matches
    results = q.process_event({"x": 1})

    # Handler should have been called
    verify(handler, times=1).__call__({"x": 1})
    assert_that(results, equal_to(["handled"]))


def test_register_multiple_handlers_same_id(when):
    """Test registering multiple handlers for the same pattern ID.

    When multiple patterns share an ID, all handlers for that ID are called
    when any of the patterns match.
    """
    q = Quamina()
    handler1 = mock()
    handler2 = mock()
    when(handler1).__call__(...).thenReturn("result1")
    when(handler2).__call__(...).thenReturn("result2")

    q.register_handler("test-pattern", {"x": [1]}, handler1)
    q.register_handler("test-pattern", {"x": [2]}, handler2)

    # Process an event that matches first pattern
    results = q.process_event({"x": 1})

    # Both handlers called because they share the same pattern_id
    verify(handler1, times=1).__call__(...)
    verify(handler2, times=1).__call__(...)
    assert_that(results, contains_inanyorder("result1", "result2"))


def test_register_handlers_different_ids(when):
    """Test registering handlers for different pattern IDs."""
    q = Quamina()
    handler1 = mock()
    handler2 = mock()
    when(handler1).__call__(...).thenReturn("result1")
    when(handler2).__call__(...).thenReturn("result2")

    q.register_handler("pattern-1", {"x": [1]}, handler1)
    q.register_handler("pattern-2", {"x": [2]}, handler2)

    # Process an event that matches first pattern only
    results = q.process_event({"x": 1})

    verify(handler1, times=1).__call__(...)
    verify(handler2, times=0).__call__(...)
    assert_that(results, equal_to(["result1"]))


def test_handler_decorator():
    """Test using the decorator to register handlers."""
    q = Quamina()
    calls = []

    @q.handler("decorator-pattern", {"x": [1, 2, 3]})
    def my_handler(event):
        calls.append(event)
        return "handled"

    # Process matching event
    results = q.process_event({"x": 2})

    assert_that(calls, has_length(1))
    assert_that(calls[0], equal_to({"x": 2}))
    assert_that(results, equal_to(["handled"]))


def test_unregister_handlers(when):
    """Test unregistering handlers."""
    q = Quamina()
    handler = mock()
    when(handler).__call__(...).thenReturn(None)

    q.register_handler("temp-pattern", {"x": [1]}, handler)
    q.process_event({"x": 1})
    verify(handler, times=1).__call__(...)

    # Unregister
    q.unregister_handlers("temp-pattern")

    # Process again - handler should not be called (still only 1 call total)
    q.process_event({"x": 1})
    verify(handler, times=1).__call__(...)


def test_process_event_no_matches(when):
    """Test processing an event that doesn't match any patterns."""
    q = Quamina()
    handler = mock()
    when(handler).__call__(...).thenReturn(None)

    q.register_handler("pattern", {"x": [1]}, handler)

    results = q.process_event({"y": 2})

    verify(handler, times=0).__call__(...)
    assert_that(results, equal_to([]))


def test_process_event_multiple_matches(when):
    """Test processing an event that matches multiple patterns."""
    q = Quamina()
    handler1 = mock()
    handler2 = mock()
    handler3 = mock()
    when(handler1).__call__(...).thenReturn("result1")
    when(handler2).__call__(...).thenReturn("result2")
    when(handler3).__call__(...).thenReturn("result3")

    q.register_handler("pattern-1", {"x": [1]}, handler1)
    q.register_handler("pattern-2", {"x": [1, 2]}, handler2)
    q.register_handler("pattern-3", {"y": [5]}, handler3)

    results = q.process_event({"x": 1, "y": 5})

    # All three handlers should be called
    verify(handler1, times=1).__call__(...)
    verify(handler2, times=1).__call__(...)
    verify(handler3, times=1).__call__(...)
    assert_that(results, contains_inanyorder("result1", "result2", "result3"))


def test_handler_exception_doesnt_stop_processing(when):
    """Test that an exception in one handler doesn't prevent others from running."""
    q = Quamina()
    handler1 = mock()
    handler2 = mock()
    when(handler1).__call__(...).thenRaise(ValueError("Handler error"))
    when(handler2).__call__(...).thenReturn("result2")

    # Use different pattern IDs to ensure separate handler lists
    q.register_handler("pattern-1", {"x": [1]}, handler1)
    q.register_handler("pattern-2", {"x": [1]}, handler2)

    # Should not raise, and should call both handlers
    results = q.process_event({"x": 1})

    verify(handler1, times=1).__call__(...)
    verify(handler2, times=1).__call__(...)
    # Only the second handler's result is included (first one raised exception)
    assert_that(results, equal_to(["result2"]))


def test_handler_receives_full_event():
    """Test that handlers receive the complete event, not just matched fields."""
    q = Quamina()
    received_events = []

    @q.handler("pattern", {"x": [1]})
    def capture_event(event):
        received_events.append(event)

    q.process_event({"x": 1, "y": 2, "z": 3})

    assert_that(received_events[0], equal_to({"x": 1, "y": 2, "z": 3}))


def test_multiple_handlers_same_pattern_id():
    """Test multiple handlers registered for the same pattern ID.

    All handlers for a pattern ID are called when any pattern with that ID matches.
    """
    q = Quamina()
    calls = []

    @q.handler("multi", {"x": [1]})
    def handler1(event):
        calls.append("handler1")
        return 1

    @q.handler("multi", {"y": [2]})
    def handler2(event):
        calls.append("handler2")
        return 2

    # Event matching first pattern - both handlers called
    results = q.process_event({"x": 1})
    assert_that(calls, contains_inanyorder("handler1", "handler2"))
    assert_that(results, contains_inanyorder(1, 2))

    calls.clear()

    # Event matching second pattern - both handlers called
    results = q.process_event({"y": 2})
    assert_that(calls, contains_inanyorder("handler1", "handler2"))
    assert_that(results, contains_inanyorder(1, 2))


def test_handler_return_values():
    """Test that handler return values are collected."""
    q = Quamina()

    @q.handler("pattern-1", {"x": [1]})
    def handler1(event):
        return event["x"] * 2

    @q.handler("pattern-2", {"x": [1, 2]})
    def handler2(event):
        return event["x"] + 10

    results = q.process_event({"x": 1})

    assert_that(results, contains_inanyorder(2, 11))


def test_event_routing_example():
    """Test a realistic event routing scenario."""
    q = Quamina()
    processed = []

    @q.handler("high-temp", {"temperature": [80, 90, 100]})
    def alert_high_temp(event):
        processed.append(f"High temp alert: {event['temperature']}°F")

    @q.handler("critical-temp", {"temperature": [100, 110]})
    def alert_critical_temp(event):
        processed.append(f"CRITICAL temp: {event['temperature']}°F")

    # Normal temperature - no handlers
    q.process_event({"temperature": 70})
    assert_that(processed, has_length(0))

    # High temperature - one handler
    q.process_event({"temperature": 80})
    assert_that(processed, has_length(1))

    processed.clear()

    # Critical temperature - both handlers
    q.process_event({"temperature": 100})
    assert_that(processed, has_length(2))
    assert_that(processed[0], equal_to("High temp alert: 100°F"))
    assert_that(processed[1], equal_to("CRITICAL temp: 100°F"))
