#!/usr/bin/env python3
"""Example demonstrating handler registration for event-driven pattern matching."""

from quamina import Quamina

# Create a Quamina instance
q = Quamina()


# Method 1: Register handlers using the decorator
@q.handler("high-temperature", {"temperature": [80, 90, 100]})
def handle_high_temp(event):
    """Handler for high temperature events."""
    print(f"⚠️  High temperature alert: {event['temperature']}°F")
    return "high-temp-alert"


@q.handler("critical-temperature", {"temperature": [100, 110, 120]})
def handle_critical_temp(event):
    """Handler for critical temperature events."""
    print(f"🚨 CRITICAL temperature: {event['temperature']}°F - Take action!")
    return "critical-alert"


# Method 2: Register handlers using the method
def handle_normal_temp(event):
    """Handler for normal temperature events."""
    print(f"✅ Temperature normal: {event['temperature']}°F")
    return "normal"


q.register_handler("normal-temperature", {"temperature": [60, 65, 70, 75]}, handle_normal_temp)


# Register handlers for different event types
@q.handler("error-event", {"type": ["error"], "severity": ["high"]})
def handle_error(event):
    """Handler for error events."""
    print(f"❌ Error: {event.get('message', 'Unknown error')}")
    return "error-handled"


@q.handler("success-event", {"type": ["success"]})
def handle_success(event):
    """Handler for success events."""
    print(f"✨ Success: {event.get('message', 'Operation completed')}")
    return "success-handled"


# Process events - handlers are called automatically
print("=== Processing temperature events ===\n")

# Normal temperature - one handler
print("Event 1:")
results = q.process_event({"temperature": 70})
print(f"Results: {results}\n")

# High temperature - one handler
print("Event 2:")
results = q.process_event({"temperature": 85})
print(f"Results: {results}\n")

# Critical temperature - two handlers (both match!)
print("Event 3:")
results = q.process_event({"temperature": 100})
print(f"Results: {results}\n")

print("\n=== Processing application events ===\n")

# Error event
print("Event 4:")
results = q.process_event({"type": "error", "severity": "high", "message": "Database connection failed"})
print(f"Results: {results}\n")

# Success event
print("Event 5:")
results = q.process_event({"type": "success", "message": "User registration completed"})
print(f"Results: {results}\n")

# Event that doesn't match any pattern
print("Event 6:")
results = q.process_event({"type": "info", "message": "Just some info"})
print(f"Results: {results} (no handlers matched)\n")

# Demonstrate unregistering handlers
print("\n=== Unregistering handlers ===\n")
q.unregister_handlers("normal-temperature")
print("Unregistered 'normal-temperature' handlers")

print("\nProcessing event 7 (should not trigger normal handler):")
results = q.process_event({"temperature": 70})
print(f"Results: {results} (normal handler was unregistered)\n")

print("✅ Example completed!")
