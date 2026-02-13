# Quick Start Guide

## What is this?

This is a Python wrapper for [Quamina](https://github.com/timbray/quamina), a high-performance pattern-matching library written in Go. It allows you to match JSON events against patterns extremely quickly.

## Installation & Building

```bash
xc build   # Build the Go library (uv installs Python dependencies automatically)
```

## Basic Usage

```python
from quamina import Quamina

# Create a Quamina instance
with Quamina() as q:
    # Add patterns
    q.add_pattern("large-image", {
        "Image": {
            "Width": [800, 1024],
            "Height": [600, 768]
        }
    })

    q.add_pattern("active-user", {
        "User": {"Status": ["active"]}
    })

    # Match events against patterns
    event = {"Image": {"Width": 800, "Height": 600}}
    matches = q.matches_for_event(event)
    print(matches)  # ["large-image"]

    # Delete patterns
    q.delete_patterns("large-image")
```

## Key Concepts

### Patterns
Patterns are JSON objects where leaf values are **arrays** of possible matches:
```python
{
    "field": ["value1", "value2"],  # Matches if field is "value1" OR "value2"
    "nested": {
        "field": [123, 456]  # Works with numbers, strings, booleans, null
    }
}
```

### Events
Events are regular JSON objects:
```python
{
    "field": "value1",
    "nested": {"field": 123},
    "extra": "ignored"  # Extra fields don't prevent matching
}
```

### Pattern IDs
- Can use the same ID for multiple patterns
- All patterns with a given ID are returned if matched
- Useful for grouping related patterns

## Examples

See the `examples/` directory:
- `basic_usage.py` - Simple patterns and matching
- `advanced_patterns.py` - Complex patterns, multiple matches, etc.

## Running Tests

```bash
# Unit tests
xc unit

# All tests
xc test

# Format code
xc format

# Lint and type check
xc lint

# Pre-commit checks (runs all quality checks)
xc pc

# Run examples
xc example
```

## Performance

Quamina is extremely fast:
- Matching is approximately O(1) relative to pattern count
- Can match millions of events per second
- Scales with unique fields, not total patterns

## Architecture

```
Python (dict) → JSON → ctypes → Go shared library → Quamina
```

See `ARCHITECTURE.md` for detailed information.

## Troubleshooting

### Library not found
- Make sure you've run `xc build`
- Check that `src/quamina/lib/libquamina.*` exists

### Pattern errors
- Remember: leaf values must be arrays: `{"x": [1]}` not `{"x": 1}`
- Patterns must be valid JSON

### Platform issues
- Supported: macOS (.dylib), Linux (.so), Windows (.dll)
- Rebuild the library when changing platforms
