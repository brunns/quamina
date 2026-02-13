# quamina

Python wrapper for [timbray/quamina](https://github.com/timbray/quamina) - a fast pattern-matching library for JSON events.

## Features

- **High-performance pattern matching**: Leverages Quamina's Go implementation via shared library for maximum speed
- **Simple Python API**: Pythonic interface for pattern management and event matching
- **Type-safe**: Full type hints for better IDE support and type checking
- **Context manager support**: Automatic resource cleanup

## Installation

Requires:
- Python 3.14+
- Go 1.20+ (for building the shared library)
- [uv](https://docs.astral.sh/uv/) for development
- [xc](https://xcfile.dev/) for task running

## Quick Start

```python
from quamina import Quamina

# Create a Quamina instance
with Quamina() as q:
    # Add a pattern
    q.add_pattern("my-pattern", {
        "x": [1, 2, 3],
        "y": ["a", "b"]
    })

    # Match an event
    matches = q.matches_for_event({"x": 2, "y": "a"})
    print(matches)  # ["my-pattern"]
```

See `examples/basic_usage.py` for more examples.

## Performance

Quamina's Go implementation provides significant performance advantages over pure Python pattern matching:

- **100 patterns**: ~5x faster than naive Python
- **1,000 patterns**: ~40x faster than naive Python
- **Scales efficiently**: Performance advantage grows with pattern count

The library uses optimized data structures and algorithms for fast event matching, making it ideal for production systems with hundreds or thousands of patterns.

Run benchmarks with:
```sh
xc bench
```

## Getting Started from Scratch

```sh
xc build      # Build the Go shared library
xc pc         # Verify everything works (uv installs dependencies automatically)
xc example    # Try the examples
```

## Development

### Prerequisites

- Python 3.14+
- Go 1.20+
- [uv](https://docs.astral.sh/uv/) for Python package management
- [xc](https://xcfile.dev/) for task running

### Available Tasks

Run `xc` or `xc --no-tty` to see all available tasks.

### Claude Code Pre-commit Hook

A pre-commit hook is configured at `.claude/hooks/pre-commit-check` that automatically runs `xc pc` before each commit when using Claude Code. This ensures all code is formatted, linted, and tested before committing.

## Tasks

### build

Build the Go shared library

run: once

```sh
cd go-quamina
if [ "$(uname -s)" = "Darwin" ]; then
    make darwin
    cp libquamina.dylib ../src/quamina/lib/
elif [ "$(uname -s)" = "Linux" ]; then
    make linux
    cp libquamina.so ../src/quamina/lib/
else
    make windows
    cp libquamina.dll ../src/quamina/lib/
fi
cd ..
echo "✅ Go library built successfully"
```

### format-go

Format Go code

```sh
cd go-quamina
gofmt -w wrapper.go
cd ..
```

### lint-go

Lint Go code

```sh
cd go-quamina
go fmt ./...
go vet ./...
cd ..
```

### format-py

Format Python code

```sh
uv run ruff format .
uv run ruff check . --fix
```

### lint-py

Lint Python code

```sh
uv run ruff format . --check
uv run ruff check .
uv run pyright
```

### format

Format all code (Go and Python)

Requires: format-go, format-py

### lint

Lint all code (Go and Python)

Requires: lint-go, lint-py

### test

Run all tests

Requires: unit

### unit

Run unit tests with coverage

Requires: build

```sh
uv run pytest tests/unit/ --durations=10 --cov-report term-missing --cov-fail-under 100 --cov quamina
```

### example

Run example scripts

Requires: build

```sh
echo "Running basic usage example..."
uv run python examples/basic_usage.py
echo ""
echo "Running advanced patterns example..."
uv run python examples/advanced_patterns.py
```

### pc

Pre-commit checks

Requires: test, lint, example

### bench

Run performance benchmarks (not part of pre-commit checks due to runtime)

Requires: build

```sh
uv run pytest tests/performance/ --benchmark-only --benchmark-columns=min,mean,stddev,ops --benchmark-sort=name --quiet -s
echo ""
echo "📊 Performance Summary:"
echo "  • Simple patterns: Python faster (FFI overhead)"
echo "  • 100 patterns:    Quamina ~5x faster"
echo "  • 1000 patterns:   Quamina ~40x faster ⭐"
```

### clean

Clean build artifacts

```sh
cd go-quamina
make clean
cd ..
rm -rf .pytest_cache .ruff_cache .coverage
rm -rf src/quamina/__pycache__ tests/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "✅ Cleaned build artifacts"
```
