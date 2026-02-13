Contributing
============

Thank you for your interest in contributing to Quamina! This guide will help you
get started.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

To contribute to Quamina, you'll need:

* Python 3.11 or later
* Go 1.25.7 or later
* uv (Python package manager)
* Git

Setting Up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/brunns/quamina.git
   cd quamina

2. Install dependencies:

.. code-block:: bash

   uv sync

3. Build the Go library:

.. code-block:: bash

   cd go-quamina
   make darwin  # or 'make linux' or build manually on Windows
   cp libquamina.dylib ../src/quamina/lib/  # adjust extension as needed
   cd ..

4. Run the tests to verify setup:

.. code-block:: bash

   uv run pytest tests/unit/

Development Workflow
--------------------

Running Tests
~~~~~~~~~~~~~

Run all tests:

.. code-block:: bash

   uv run pytest tests/unit/

Run with coverage:

.. code-block:: bash

   uv run pytest tests/unit/ --cov=src/quamina --cov-report=term-missing

Run performance tests:

.. code-block:: bash

   uv run pytest tests/performance/

Code Quality
~~~~~~~~~~~~

Format code:

.. code-block:: bash

   uv run ruff format .

Lint code:

.. code-block:: bash

   uv run ruff check .

Type check:

.. code-block:: bash

   uv run pyright

Run all checks:

.. code-block:: bash

   uv run ruff format . --check
   uv run ruff check .
   uv run pyright

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

Build the documentation:

.. code-block:: bash

   cd docs
   uv run sphinx-build -b html . _build/html

View the built documentation:

.. code-block:: bash

   open _build/html/index.html  # macOS
   xdg-open _build/html/index.html  # Linux

Contributing Guidelines
-----------------------

Code Style
~~~~~~~~~~

* Follow PEP 8 style guidelines
* Use type hints for all function signatures
* Keep functions focused and small (max complexity: 5)
* Write descriptive variable and function names

Testing
~~~~~~~

* Write tests for all new functionality
* Maintain 100% test coverage
* Use pytest and pytest-mockito for testing
* Add performance tests for performance-critical code

Documentation
~~~~~~~~~~~~~

* Add docstrings to all public functions and classes
* Use Google-style docstrings
* Update relevant documentation pages
* Include code examples in docstrings

Commit Messages
~~~~~~~~~~~~~~~

Write clear, descriptive commit messages:

.. code-block:: text

   Add feature to match patterns with wildcards

   - Implement wildcard matching in pattern fields
   - Add tests for wildcard functionality
   - Update documentation with wildcard examples

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

Pull Request Process
--------------------

1. Create a feature branch:

.. code-block:: bash

   git checkout -b feature/my-new-feature

2. Make your changes and commit them:

.. code-block:: bash

   git add .
   git commit -m "Add my new feature"

3. Push to your fork:

.. code-block:: bash

   git push origin feature/my-new-feature

4. Open a pull request on GitHub

5. Ensure all CI checks pass:

   * Tests on all platforms (Linux, macOS, Windows)
   * Tests on all Python versions (3.11, 3.12, 3.13, 3.14)
   * 100% code coverage
   * Linting and type checking pass

6. Address any review comments

7. Once approved, your PR will be merged

Project Structure
-----------------

.. code-block:: text

   quamina/
   ├── .github/              # GitHub workflows and configs
   │   └── workflows/
   │       ├── ci.yml        # Continuous integration
   │       └── release.yml   # Release automation
   ├── docs/                 # Sphinx documentation
   │   ├── conf.py          # Sphinx configuration
   │   ├── index.rst        # Documentation index
   │   └── ...              # Other documentation files
   ├── examples/            # Example scripts
   ├── go-quamina/          # Go library wrapper
   │   ├── wrapper.go       # C wrapper for Go library
   │   ├── go.mod           # Go dependencies
   │   └── Makefile         # Build scripts
   ├── src/quamina/         # Python package
   │   ├── __init__.py      # Package exports
   │   ├── _quamina.py      # Main implementation
   │   └── lib/             # Native libraries (gitignored)
   ├── tests/               # Test suite
   │   ├── unit/            # Unit tests
   │   └── performance/     # Performance benchmarks
   ├── pyproject.toml       # Python project configuration
   └── README.md            # Project readme

Areas for Contribution
----------------------

We welcome contributions in several areas:

Bug Fixes
~~~~~~~~~

Found a bug? Please:

1. Check if it's already reported in GitHub Issues
2. If not, create a new issue with:
   * Clear description of the bug
   * Steps to reproduce
   * Expected vs actual behavior
   * Your environment (OS, Python version)
3. If you can fix it, submit a PR!

New Features
~~~~~~~~~~~~

Want to add a feature? Please:

1. Open an issue first to discuss the feature
2. Get approval before starting work
3. Keep the scope focused and manageable
4. Add comprehensive tests and documentation

Documentation
~~~~~~~~~~~~~

Documentation improvements are always welcome:

* Fix typos or unclear explanations
* Add more examples
* Improve API documentation
* Add tutorials or guides

Performance
~~~~~~~~~~~

Performance improvements should:

* Include benchmarks showing the improvement
* Not sacrifice code readability
* Be backed by profiling data

Getting Help
------------

If you need help:

* Check the documentation
* Look through existing GitHub Issues
* Open a new issue with your question
* Tag it with the "question" label

Reporting Security Issues
-------------------------

If you discover a security vulnerability, please:

1. Do NOT open a public issue
2. Email security concerns to: simon@brunningonline.net
3. Include:
   * Description of the vulnerability
   * Steps to reproduce
   * Potential impact
   * Suggested fix (if any)

We will respond as quickly as possible.

Code of Conduct
---------------

Be Respectful
~~~~~~~~~~~~~

* Use welcoming and inclusive language
* Be respectful of differing viewpoints
* Accept constructive criticism gracefully
* Focus on what is best for the community

Our Standards
~~~~~~~~~~~~~

Examples of behavior that contributes to a positive environment:

* Demonstrating empathy toward others
* Being respectful of differing opinions
* Giving and gracefully accepting constructive feedback
* Focusing on what is best for the project

Examples of unacceptable behavior:

* Trolling, insulting/derogatory comments, and personal attacks
* Public or private harassment
* Publishing others' private information without permission
* Other conduct which could be considered inappropriate

License
-------

By contributing to Quamina, you agree that your contributions will be licensed
under the MIT License.
