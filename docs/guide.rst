User Guide
==========

This guide covers advanced topics and best practices for using Quamina.

Understanding Pattern Matching
-------------------------------

How Patterns Work
~~~~~~~~~~~~~~~~~

Quamina uses a sophisticated pattern matching algorithm that can evaluate
thousands of patterns against events very efficiently. Understanding how
patterns work will help you use Quamina effectively.

Field Matching
^^^^^^^^^^^^^^

Each field in a pattern specifies a list of acceptable values:

.. code-block:: python

   q = Quamina()
   q.add_pattern("p1", {"status": ["active", "pending"]})

   # Matches because status is in the list
   q.matches_for_event({"status": "active"})  # ['p1']

   # Doesn't match
   q.matches_for_event({"status": "inactive"})  # []

AND Semantics Across Fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a pattern has multiple fields, ALL fields must match:

.. code-block:: python

   q.add_pattern("p2", {
       "type": ["order"],
       "status": ["completed"]
   })

   # Both fields match
   q.matches_for_event({
       "type": "order",
       "status": "completed"
   })  # ['p2']

   # Only one field matches - no match
   q.matches_for_event({
       "type": "order",
       "status": "pending"
   })  # []

Type Sensitivity
~~~~~~~~~~~~~~~~

Quamina distinguishes between different types:

.. code-block:: python

   q = Quamina()
   q.add_pattern("string-pattern", {"id": ["123"]})
   q.add_pattern("number-pattern", {"id": [123]})

   # String matches string pattern
   q.matches_for_event({"id": "123"})  # ['string-pattern']

   # Number matches number pattern
   q.matches_for_event({"id": 123})  # ['number-pattern']

Supported types:

* **Strings**: ``"hello"``
* **Numbers**: ``42``, ``3.14``
* **Booleans**: ``True``, ``False``
* **Null**: ``None``

Working with Handlers
---------------------

Error Handling in Handlers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a handler raises an exception, Quamina logs it but continues processing
other handlers:

.. code-block:: python

   import logging

   logging.basicConfig(level=logging.INFO)

   q = Quamina()

   @q.handler("p1", {"x": [1]})
   def failing_handler(event):
       raise ValueError("Oops!")

   @q.handler("p2", {"x": [1]})
   def working_handler(event):
       return "success"

   # Both patterns match, but only working_handler succeeds
   results = q.process_event({"x": 1})
   print(results)  # ['success']
   # Error is logged but doesn't stop processing

Handler Return Values
~~~~~~~~~~~~~~~~~~~~~

Handlers can return any value, and all return values are collected:

.. code-block:: python

   q = Quamina()

   @q.handler("h1", {"x": [1]})
   def handler1(event):
       return "first"

   @q.handler("h2", {"x": [1]})
   def handler2(event):
       return "second"

   results = q.process_event({"x": 1})
   print(results)  # ['first', 'second']

Multiple Handlers per Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can register multiple handlers for the same pattern:

.. code-block:: python

   q = Quamina()

   def log_handler(event):
       print(f"Logging: {event}")

   def metrics_handler(event):
       print(f"Recording metric: {event}")

   # Register multiple handlers for the same pattern
   q.register_handler("events", {"type": ["metric"]}, log_handler)
   q.register_handler("events", {"type": ["metric"]}, metrics_handler)

   # Both handlers are called
   q.process_event({"type": "metric", "value": 42})

Performance Considerations
--------------------------

Pattern Count
~~~~~~~~~~~~~

Quamina is designed to handle many patterns efficiently. The matching time
scales well even with thousands of patterns:

.. code-block:: python

   q = Quamina()

   # Add many patterns
   for i in range(10000):
       q.add_pattern(f"pattern-{i}", {"id": [i]})

   # Still fast
   import time
   start = time.time()
   matches = q.matches_for_event({"id": 5000})
   elapsed = time.time() - start
   print(f"Matched in {elapsed*1000:.2f}ms")  # Typically < 1ms

Event Size
~~~~~~~~~~

Matching time increases with event size, but remains efficient for typical events:

.. code-block:: python

   # Small event - very fast
   small_event = {"x": 1}

   # Large event - still fast
   large_event = {f"field_{i}": i for i in range(100)}

   # Both are processed efficiently
   q.matches_for_event(small_event)
   q.matches_for_event(large_event)

Memory Management
~~~~~~~~~~~~~~~~~

Quamina instances manage Go memory automatically:

.. code-block:: python

   # Option 1: Automatic cleanup with context manager (recommended)
   with Quamina() as q:
       q.add_pattern("p1", {"x": [1]})
       # ... use q ...
   # Automatically cleaned up

   # Option 2: Manual cleanup
   q = Quamina()
   try:
       q.add_pattern("p1", {"x": [1]})
       # ... use q ...
   finally:
       del q  # Triggers cleanup

Best Practices
--------------

Use Specific Pattern IDs
~~~~~~~~~~~~~~~~~~~~~~~~

Pattern IDs should be descriptive and unique:

.. code-block:: python

   # Good
   q.add_pattern("high-value-orders", {"amount": [1000, 2000]})
   q.add_pattern("failed-payments", {"status": ["failed"]})

   # Bad
   q.add_pattern("p1", {"amount": [1000, 2000]})
   q.add_pattern("p2", {"status": ["failed"]})

Organize Patterns by Purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Group related patterns together:

.. code-block:: python

   # Orders
   q.add_pattern("order.created", {"event": ["order.created"]})
   q.add_pattern("order.completed", {"event": ["order.completed"]})
   q.add_pattern("order.cancelled", {"event": ["order.cancelled"]})

   # Payments
   q.add_pattern("payment.success", {"event": ["payment.success"]})
   q.add_pattern("payment.failed", {"event": ["payment.failed"]})

Validate Events
~~~~~~~~~~~~~~~

Ensure events are valid before matching:

.. code-block:: python

   def process_event(q, event):
       # Validate event structure
       if not isinstance(event, dict):
           raise ValueError("Event must be a dictionary")

       # Match and process
       matches = q.matches_for_event(event)
       return matches

Use Type Hints
~~~~~~~~~~~~~~

Leverage type hints for better code quality:

.. code-block:: python

   from typing import Any
   from quamina import Quamina

   def create_order_matcher() -> Quamina:
       q = Quamina()
       q.add_pattern("orders", {"type": ["order"]})
       return q

   def handle_event(event: dict[str, Any]) -> list[str]:
       q = create_order_matcher()
       return q.matches_for_event(event)

Advanced Patterns
-----------------

Nested Field Matching
~~~~~~~~~~~~~~~~~~~~~

While Quamina works with flat events, you can flatten nested structures:

.. code-block:: python

   def flatten_event(event: dict[str, Any], prefix: str = "") -> dict[str, Any]:
       flat = {}
       for key, value in event.items():
           flat_key = f"{prefix}.{key}" if prefix else key
           if isinstance(value, dict):
               flat.update(flatten_event(value, flat_key))
           else:
               flat[flat_key] = value
       return flat

   # Original nested event
   nested_event = {
       "order": {
           "id": "123",
           "status": "completed"
       }
   }

   # Flatten it
   flat_event = flatten_event(nested_event)
   # {'order.id': '123', 'order.status': 'completed'}

   # Now you can match on flattened fields
   q = Quamina()
   q.add_pattern("completed-orders", {
       "order.status": ["completed"]
   })
   matches = q.matches_for_event(flat_event)

Combining with Other Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quamina works well with other Python libraries:

.. code-block:: python

   from quamina import Quamina
   import json

   # Load patterns from JSON
   with open("patterns.json") as f:
       patterns = json.load(f)

   q = Quamina()
   for pattern_id, pattern in patterns.items():
       q.add_pattern(pattern_id, pattern)

   # Use with async frameworks
   async def handle_async_event(event):
       matches = q.matches_for_event(event)
       # Process matches asynchronously
       return matches

Troubleshooting
---------------

Pattern Not Matching
~~~~~~~~~~~~~~~~~~~~

If a pattern isn't matching as expected:

1. Check that all fields in the pattern exist in the event
2. Verify field types match (string vs number)
3. Ensure values are in the pattern's value list
4. Remember: extra fields in events are OK, but missing fields cause no match

.. code-block:: python

   q = Quamina()
   q.add_pattern("test", {"x": [1]})

   # Debug: print what's being matched
   event = {"x": "1"}  # Oops, string not number
   print(f"Event: {event}")
   print(f"Matches: {q.matches_for_event(event)}")  # []

   # Fix: use correct type
   event = {"x": 1}
   print(f"Matches: {q.matches_for_event(event)}")  # ['test']

Library Not Found
~~~~~~~~~~~~~~~~~

If you get a "library not found" error:

1. Ensure the package was installed correctly
2. Check that you're on a supported platform (Linux, macOS, Windows)
3. Verify the native library exists in the package:

.. code-block:: python

   from quamina._quamina import QuaminaLibrary
   import quamina

   # Check library location
   import pathlib
   lib_dir = pathlib.Path(quamina.__file__).parent / "lib"
   print(f"Library directory: {lib_dir}")
   print(f"Contents: {list(lib_dir.iterdir())}")
