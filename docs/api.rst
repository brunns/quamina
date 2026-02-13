API Reference
=============

This page contains the complete API documentation for Quamina.

Main Classes
------------

Quamina
~~~~~~~

.. autoclass:: quamina.Quamina
   :members:
   :special-members: __init__, __enter__, __exit__, __del__
   :member-order: bysource

QuaminaError
~~~~~~~~~~~~

.. autoclass:: quamina.QuaminaError
   :members:
   :show-inheritance:

Low-Level API
-------------

These classes provide low-level access to the Quamina library. Most users
should use the high-level :class:`~quamina.Quamina` class instead.

QuaminaLibrary
~~~~~~~~~~~~~~

.. autoclass:: quamina._quamina.QuaminaLibrary
   :members:
   :member-order: bysource

Type Definitions
----------------

Pattern Type
~~~~~~~~~~~~

A pattern is a dictionary mapping field names to lists of acceptable values:

.. code-block:: python

   pattern: dict[str, list[Any]] = {
       "field1": [value1, value2, ...],
       "field2": [value3, value4, ...],
       ...
   }

Values can be:

* Strings: ``"hello"``
* Numbers: ``42``, ``3.14``
* Booleans: ``True``, ``False``
* Null: ``None``

Example:

.. code-block:: python

   pattern = {
       "type": ["order", "payment"],
       "status": ["completed"],
       "amount": [100, 200, 500]
   }

Event Type
~~~~~~~~~~

An event is a dictionary of field names to values:

.. code-block:: python

   event: dict[str, Any] = {
       "field1": value1,
       "field2": value2,
       ...
   }

Example:

.. code-block:: python

   event = {
       "type": "order",
       "status": "completed",
       "amount": 100,
       "customer_id": "12345"
   }

Handler Type
~~~~~~~~~~~~

A handler is a callable that takes an event and returns any value:

.. code-block:: python

   from typing import Any, Callable

   Handler = Callable[[dict[str, Any]], Any]

Example:

.. code-block:: python

   def my_handler(event: dict[str, Any]) -> str:
       return f"Processed event: {event['id']}"

Pattern ID Type
~~~~~~~~~~~~~~~

A pattern ID is a string that uniquely identifies a pattern:

.. code-block:: python

   pattern_id: str = "my-unique-pattern-id"

Examples:

.. code-block:: python

   # Good pattern IDs
   "order.created"
   "payment.failed"
   "high-value-transaction"
   "user-signup-email-domain-company.com"

   # Bad pattern IDs (not descriptive)
   "p1"
   "pattern"
   "temp"

Constants
---------

Platform-Specific Library Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The library uses platform-specific shared library names:

* **Linux**: ``libquamina.so``
* **macOS**: ``libquamina.dylib``
* **Windows**: ``libquamina.dll``

These are automatically selected based on your platform.

Module Exports
--------------

The main ``quamina`` module exports:

.. code-block:: python

   from quamina import Quamina, QuaminaError

Public API
~~~~~~~~~~

* :class:`~quamina.Quamina` - Main pattern matching class
* :class:`~quamina.QuaminaError` - Exception raised for errors

Private API
~~~~~~~~~~~

The following are implementation details and should not be used directly:

* ``quamina._quamina.QuaminaLibrary`` - Low-level library wrapper
