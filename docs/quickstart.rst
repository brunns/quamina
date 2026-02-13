Quick Start
===========

This guide will help you get started with Quamina in just a few minutes.

Installation
------------

Install Quamina using pip:

.. code-block:: bash

   pip install quamina

The package includes pre-compiled native libraries for Linux, macOS, and Windows,
so no additional compilation steps are needed.

Basic Usage
-----------

Creating a Matcher
~~~~~~~~~~~~~~~~~~

First, create a Quamina instance:

.. code-block:: python

   from quamina import Quamina

   q = Quamina()

Adding Patterns
~~~~~~~~~~~~~~~

Patterns define what events you want to match. Each pattern has a unique ID and
a dictionary of field matchers:

.. code-block:: python

   # Match events where x is 1, 2, or 3
   q.add_pattern("number-pattern", {"x": [1, 2, 3]})

   # Match events where name is "Alice" or "Bob"
   q.add_pattern("name-pattern", {"name": ["Alice", "Bob"]})

   # Match events with multiple fields
   q.add_pattern("complex-pattern", {
       "type": ["order", "payment"],
       "status": ["completed"],
       "amount": [100, 200, 500]
   })

Matching Events
~~~~~~~~~~~~~~~

To find which patterns match an event:

.. code-block:: python

   # This matches "number-pattern"
   matches = q.matches_for_event({"x": 2})
   print(matches)  # ['number-pattern']

   # This matches "name-pattern"
   matches = q.matches_for_event({"name": "Alice"})
   print(matches)  # ['name-pattern']

   # This matches "complex-pattern"
   matches = q.matches_for_event({
       "type": "order",
       "status": "completed",
       "amount": 100
   })
   print(matches)  # ['complex-pattern']

   # No matches
   matches = q.matches_for_event({"x": 99})
   print(matches)  # []

Using Context Managers
~~~~~~~~~~~~~~~~~~~~~~

Quamina supports context managers for automatic cleanup:

.. code-block:: python

   with Quamina() as q:
       q.add_pattern("test", {"x": [1]})
       matches = q.matches_for_event({"x": 1})
       print(matches)  # ['test']
   # Automatically cleaned up

Registering Handlers
--------------------

For event-driven applications, you can register handler functions that are
automatically called when patterns match:

Using register_handler
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina

   q = Quamina()

   def handle_order(event):
       print(f"Order received: {event}")
       return event['order_id']

   # Register a handler for order events
   q.register_handler(
       "order-pattern",
       {"type": ["order"]},
       handle_order
   )

   # Process an event - handlers are automatically called
   results = q.process_event({
       "type": "order",
       "order_id": "12345"
   })
   print(results)  # [12345]

Using the Decorator
~~~~~~~~~~~~~~~~~~~

The decorator syntax is even more convenient:

.. code-block:: python

   from quamina import Quamina

   q = Quamina()

   @q.handler("high-value-order", {
       "type": ["order"],
       "amount": [1000, 2000, 5000]
   })
   def handle_high_value_order(event):
       print(f"High value order: ${event['amount']}")
       return event['order_id']

   # Process events
   results = q.process_event({
       "type": "order",
       "amount": 2000,
       "order_id": "67890"
   })
   # Prints: High value order: $2000

Deleting Patterns
-----------------

You can delete patterns when they're no longer needed:

.. code-block:: python

   q = Quamina()
   q.add_pattern("temp", {"x": [1]})

   # Delete the pattern
   q.delete_patterns("temp")

   # Now it won't match
   matches = q.matches_for_event({"x": 1})
   print(matches)  # []

For handlers, use ``unregister_handlers`` which deletes the pattern and removes handlers:

.. code-block:: python

   q.register_handler("temp", {"x": [1]}, lambda e: None)

   # Unregister handlers and delete pattern
   q.unregister_handlers("temp")

Pattern Matching Rules
----------------------

* **All fields must match**: An event matches a pattern only if ALL fields in the
  pattern match corresponding fields in the event
* **OR semantics within fields**: Values in a field list are OR'd together
* **Type sensitive**: String "1" and number 1 are different
* **Extra fields allowed**: Events can have fields not in the pattern

Examples:

.. code-block:: python

   q = Quamina()
   q.add_pattern("p1", {
       "x": [1, 2],
       "y": ["a", "b"]
   })

   # Matches - both fields match
   q.matches_for_event({"x": 1, "y": "a"})  # ['p1']
   q.matches_for_event({"x": 2, "y": "b"})  # ['p1']

   # Matches - extra field "z" is ignored
   q.matches_for_event({"x": 1, "y": "a", "z": 99})  # ['p1']

   # No match - x doesn't match
   q.matches_for_event({"x": 3, "y": "a"})  # []

   # No match - y doesn't match
   q.matches_for_event({"x": 1, "y": "c"})  # []

   # No match - missing field y
   q.matches_for_event({"x": 1})  # []

Next Steps
----------

* Read the :doc:`guide` for more advanced usage
* Check the :doc:`api` for complete API documentation
* See :doc:`examples` for more code examples
