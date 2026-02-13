#!/usr/bin/env python3
"""Basic usage example for the Quamina Python wrapper."""

from quamina import Quamina

# Create a Quamina instance
q = Quamina()

# Add patterns to match against
print("Adding patterns...")

# Pattern 1: Match images with specific dimensions
q.add_pattern(
    "large-image",
    {
        "Image": {
            "Width": [800, 1024],
            "Height": [600, 768],
        }
    },
)

# Pattern 2: Match active users
q.add_pattern("active-user", {"User": {"Status": ["active"]}})

# Pattern 3: Match high-value orders
q.add_pattern("high-value-order", {"Order": {"Amount": [1000, 5000, 10000]}})

# Test event 1: Large image
print("\n--- Testing large image event ---")
event1 = {"Image": {"Width": 800, "Height": 600, "Format": "JPEG"}}
matches1 = q.matches_for_event(event1)
print(f"Event: {event1}")
print(f"Matched patterns: {matches1}")

# Test event 2: Active user
print("\n--- Testing active user event ---")
event2 = {"User": {"Status": "active", "Name": "Alice"}}
matches2 = q.matches_for_event(event2)
print(f"Event: {event2}")
print(f"Matched patterns: {matches2}")

# Test event 3: High-value order
print("\n--- Testing high-value order event ---")
event3 = {"Order": {"Amount": 5000, "Customer": "Bob"}}
matches3 = q.matches_for_event(event3)
print(f"Event: {event3}")
print(f"Matched patterns: {matches3}")

# Test event 4: No match
print("\n--- Testing event that doesn't match ---")
event4 = {"Random": {"Data": "value"}}
matches4 = q.matches_for_event(event4)
print(f"Event: {event4}")
print(f"Matched patterns: {matches4}")

# Delete a pattern and test again
print("\n--- Deleting 'active-user' pattern ---")
q.delete_patterns("active-user")

event5 = {"User": {"Status": "active", "Name": "Charlie"}}
matches5 = q.matches_for_event(event5)
print(f"Event: {event5}")
print(f"Matched patterns: {matches5}")

# Using context manager for automatic cleanup
print("\n--- Using context manager ---")
with Quamina() as q2:
    q2.add_pattern("test-pattern", {"x": [1, 2, 3]})
    matches = q2.matches_for_event({"x": 2})
    print(f"Matches: {matches}")
# Instance is automatically cleaned up when exiting the context

print("\n✅ All examples completed successfully!")
