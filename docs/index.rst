Quamina Documentation
=====================

Quamina is a Python wrapper for the `Quamina pattern matching library <https://github.com/timbray/quamina>`_.
It provides fast, efficient event pattern matching for Python applications.

Overview
--------

Quamina is a high-performance pattern matching library originally written in Go by Tim Bray.
This Python wrapper provides a Pythonic interface to the Quamina library, allowing you to:

* Match events against complex patterns at high speed
* Register handler functions that are automatically called when patterns match
* Use a simple, declarative syntax for defining patterns
* Process thousands of events per second with minimal overhead

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   guide
   api
   examples
   contributing

Features
--------

* **High Performance**: Written in Go and exposed via C bindings for maximum speed
* **Simple API**: Easy-to-use Python interface with context manager support
* **Pattern Matching**: Match events against multiple patterns simultaneously
* **Event Handlers**: Register callbacks that are automatically invoked on matches
* **Type Safety**: Full type hints for better IDE support and code quality
* **Cross-Platform**: Works on Linux, macOS, and Windows

Quick Example
-------------

.. code-block:: python

   from quamina import Quamina

   # Create a matcher instance
   q = Quamina()

   # Add a pattern
   q.add_pattern("my-pattern", {
       "x": [1, 2, 3],
       "y": ["hello", "world"]
   })

   # Match events
   matches = q.matches_for_event({"x": 2, "y": "hello"})
   print(matches)  # ['my-pattern']

Installation
------------

.. code-block:: bash

   pip install quamina

Note: The package includes pre-compiled native libraries for Linux, macOS, and Windows.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
