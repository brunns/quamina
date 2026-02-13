# Architecture

This document describes the architecture of the Python wrapper for Quamina.

## Overview

The wrapper uses **Go shared libraries** (via CGo) to provide high-performance pattern matching while maintaining a Pythonic API. This approach balances performance (native Go speed) with ease of use (Python interface).

```
┌─────────────────────────────────────────┐
│           Python Application            │
└────────────────┬────────────────────────┘
                 │
                 │ Python API
                 ▼
┌─────────────────────────────────────────┐
│      quamina._quamina.Quamina           │
│  (High-level Python wrapper)            │
└────────────────┬────────────────────────┘
                 │
                 │ JSON serialization
                 ▼
┌─────────────────────────────────────────┐
│   quamina._quamina.QuaminaLibrary       │
│  (Low-level ctypes wrapper)             │
└────────────────┬────────────────────────┘
                 │
                 │ ctypes FFI
                 ▼
┌─────────────────────────────────────────┐
│     libquamina.{dylib,so,dll}           │
│  (Go shared library with CGo exports)   │
└────────────────┬────────────────────────┘
                 │
                 │ Go function calls
                 ▼
┌─────────────────────────────────────────┐
│      quamina.net/go/quamina             │
│  (Original Quamina Go library)          │
└─────────────────────────────────────────┘
```

## Components

### 1. Go Shared Library (`go-quamina/`)

**File**: `wrapper.go`

This is the bridge between Python and the Quamina Go library. It:
- Exports C-compatible functions using CGo
- Manages Quamina instances using handles (integer IDs)
- Handles memory management for strings crossing the C/Go boundary
- Converts between Go types and C types

**Key exported functions**:
- `QuaminaNew()` - Creates a new Quamina instance, returns handle
- `QuaminaFree(handle)` - Destroys a Quamina instance
- `QuaminaAddPattern(handle, patternID, patternJSON)` - Adds a pattern
- `QuaminaDeletePatterns(handle, patternID)` - Deletes patterns
- `QuaminaMatchesForEvent(handle, eventJSON)` - Matches events
- `QuaminaFreeString(ptr)` - Frees C strings allocated by Go

**Memory management**:
- Pattern IDs and JSON data are passed as C strings (copied from Python)
- Return values are C strings allocated by Go (must be freed by caller)
- Quamina instances are stored in a Go map, indexed by handle

### 2. Python Low-Level Wrapper (`src/quamina/_quamina.py`)

**Class**: `QuaminaLibrary`

This class provides a thin wrapper around the shared library using `ctypes`:
- Loads the correct shared library for the platform (.dylib/.so/.dll)
- Defines C function signatures using ctypes
- Handles string encoding/decoding (UTF-8)
- Manages memory cleanup (calling QuaminaFreeString)
- Converts C return values to Python types

**Key responsibilities**:
- Platform detection (macOS/Linux/Windows)
- Library loading and function signature definition
- Memory management (ensuring C strings are freed)
- Error handling (converting C errors to Python exceptions)

### 3. Python High-Level API (`src/quamina/_quamina.py`)

**Class**: `Quamina`

This class provides a Pythonic interface to Quamina:
- Accepts Python dictionaries (not JSON strings)
- Returns Python lists
- Implements context manager protocol (`__enter__`/`__exit__`)
- Implements destructor (`__del__`) for cleanup
- Provides type hints for IDE support

**Key features**:
- Automatic JSON serialization/deserialization
- Automatic resource cleanup
- Type-safe API with type hints
- Context manager support

## Build Process

```
┌─────────────────┐
│   wrapper.go    │
│  (CGo exports)  │
└────────┬────────┘
         │
         │ go build -buildmode=c-shared
         ▼
┌─────────────────┐
│  libquamina.*   │
│ (shared library)│
└────────┬────────┘
         │
         │ copy
         ▼
┌─────────────────┐
│ src/quamina/lib/│
│  (Python pkg)   │
└─────────────────┘
```

**Build script**: `build_go.sh`
- Detects platform (macOS/Linux/Windows)
- Builds appropriate shared library
- Copies library to Python package directory

## Design Decisions

### Why shared library over HTTP/gRPC?

**Pros**:
- ✅ No network overhead
- ✅ In-process (no separate service to manage)
- ✅ Lower latency
- ✅ Simpler deployment

**Cons**:
- ❌ Platform-specific binaries required
- ❌ More complex build process
- ❌ Tighter coupling between Go and Python

### Why ctypes over cffi?

**Ctypes**:
- ✅ Built into Python standard library
- ✅ No additional dependencies
- ✅ Sufficient for our simple C interface

**CFFI** would be better for:
- More complex C APIs
- Better error messages
- Automatic ABI/API mode

### Memory Management

**Key principle**: Whoever allocates memory is responsible for freeing it.

1. **Python → Go**: Python-allocated strings are automatically handled by ctypes
2. **Go → Python**: Go allocates C strings with `C.CString()`, Python must free with `QuaminaFreeString()`
3. **Quamina instances**: Stored in Go map, freed when handle is released

**Safety measures**:
- Using `c_void_p` instead of `c_char_p` for return values to prevent ctypes auto-conversion
- Wrapping string reads in try/finally to ensure cleanup
- Context managers and destructors for automatic cleanup

## Performance Characteristics

- **Pattern addition**: O(n) where n is pattern complexity
- **Event matching**: ~O(1) relative to pattern count (Quamina's key feature)
- **FFI overhead**: Minimal - only JSON serialization and function call overhead
- **Memory**: Quamina instances persist in Go, patterns stored in optimized data structures

## Testing Strategy

1. **Unit tests** (`tests/unit/test_quamina.py`):
   - Test core functionality (add, delete, match)
   - Test various pattern types
   - Test error handling

2. **Error path tests** (`tests/unit/test_quamina_errors.py`):
   - Platform detection errors
   - Invalid handles
   - Memory management
   - Edge cases

3. **Integration examples** (`examples/`):
   - Real-world usage patterns
   - Demonstrate advanced features
   - Serve as documentation

## Future Enhancements

Potential improvements:
- [ ] Support for more Quamina options (e.g., custom flatteners)
- [ ] Async API (using background threads)
- [ ] Performance benchmarks
- [ ] Wheels with pre-built binaries for common platforms
- [ ] Support for Quamina's advanced pattern types (wildcards, regex)
