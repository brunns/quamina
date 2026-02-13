#!/usr/bin/env python3
"""Advanced pattern matching examples."""

from quamina import Quamina

q = Quamina()

print("=== Advanced Pattern Matching Examples ===\n")

# Example 1: Multiple values in a pattern
print("1. Multiple values in a pattern")
q.add_pattern("status-pattern", {"status": ["active", "pending", "processing"]})
print(f"   Match 'active': {q.matches_for_event({'status': 'active'})}")
print(f"   Match 'completed': {q.matches_for_event({'status': 'completed'})}")

# Example 2: Nested objects
print("\n2. Nested objects")
q.add_pattern(
    "nested-pattern",
    {"user": {"address": {"city": ["New York", "San Francisco"]}}},
)
event = {"user": {"name": "Alice", "address": {"city": "New York", "zip": "10001"}}}
print(f"   Event: {event}")
print(f"   Matches: {q.matches_for_event(event)}")

# Example 3: Mixed types
print("\n3. Mixed types (numbers, strings, booleans, null)")
q.add_pattern("mixed-pattern", {"count": [0, 1, 2], "name": ["test"], "active": [True], "value": [None]})

for event in [
    {"count": 1},
    {"name": "test"},
    {"active": True},
    {"value": None},
]:
    print(f"   Event: {event} -> Matches: {q.matches_for_event(event)}")

# Example 4: Multiple patterns matching the same event
print("\n4. Multiple patterns matching the same event")
q.add_pattern("high-temp", {"temperature": [80, 90, 100]})
q.add_pattern("high-temp-alert", {"temperature": [90, 100, 110]})
q.add_pattern("critical-temp", {"temperature": [100, 110, 120]})

for temp in [80, 90, 100, 110]:
    event = {"temperature": temp}
    matches = q.matches_for_event(event)
    print(f"   Temperature {temp}°F: {len(matches)} pattern(s) matched - {matches}")

# Example 5: Same pattern ID for multiple patterns
print("\n5. Same pattern ID for multiple patterns")
q.add_pattern("alert", {"type": ["error"]})
q.add_pattern("alert", {"level": ["critical"]})
q.add_pattern("alert", {"source": ["database"]})

print(f"   Error event: {q.matches_for_event({'type': 'error'})}")
print(f"   Critical event: {q.matches_for_event({'level': 'critical'})}")
print(f"   Database event: {q.matches_for_event({'source': 'database'})}")
print(f"   Combined event: {q.matches_for_event({'type': 'error', 'level': 'critical'})}")

# Example 6: Extra fields don't prevent matching
print("\n6. Extra fields in events are ignored")
q.add_pattern("simple", {"x": [1]})
event = {"x": 1, "y": 2, "z": 3, "extra": "data"}
print("   Pattern requires only 'x': {'x': [1]}")
print(f"   Event has extra fields: {event}")
print(f"   Still matches: {q.matches_for_event(event)}")

print("\n✅ All advanced examples completed successfully!")
