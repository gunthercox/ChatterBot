============
Unit Testing
============

*"A true professional does not waste the time and money of other people by handing over software that is not reasonably free of obvious bugs;
that has not undergone minimal unit testing; that does not meet the specifications and requirements;
that is gold-plated with unnecessary features; or that looks like junk."* – Daniel Read

ChatterBot tests
----------------

ChatterBot's built in tests can be run using nose.
See the `nose documentation`_ for more information.

.. sourcecode:: sh

   nosetests

*Note* that nose also allows you to specify individual test cases to run.
For example, the following command will run all tests in the test-module `tests/logic_adapter_tests`

.. sourcecode:: sh

   nosetests tests/logic_adapter_tests

Django integration tests
------------------------

Tests for Django integration have been included in the `tests_django` directory and
can be run with:

.. sourcecode:: sh

   python runtests.py

Django example app tests
------------------------

Tests for the example Django app can be run with the following command from within the `examples/django_app` directory.

.. sourcecode:: sh

   python manage.py test

Benchmark tests
---------------

You can run a series of benchmark tests that test a variety of different chat bot configurations for
performance by running the following command.

.. sourcecode:: sh

   python tests/benchmarks.py

Running all the tests
---------------------

You can run all of ChatterBot's tests with a single command: ``tox``.

Tox is a tool for managing virtual environments and running tests.

Installing tox
++++++++++++++

You can install ``tox`` with ``pip``.

.. code-block:: bash

   pip install tox

Using tox
+++++++++

When you run the ``tox`` command from within the root directory of
the ``ChatterBot`` repository it will run the following tests:

1. Tests for ChatterBot's core files.
2. Tests for ChatterBot's integration with multiple versions of Django.
3. Tests for each of ChatterBot's example files.
4. Tests to make sure ChatterBot's documentation builds.
5. Code style and validation checks (linting).
6. Benchmarking tests for performance.

You can run specific tox environments using the ``-e`` flag.
A few examples include:

.. code-block:: bash

   # Run the documentation tests
   tox -e docs

.. code-block:: bash

   # Run the tests with Django 1.10
   tox -e django110

.. code-block:: bash

   # Run the code linting scripts
   tox -e lint

To see the list of all available environments that you can run tests for:

.. code-block:: bash

   tox -l

To run tests for all environments:

.. code-block:: bash

   tox

..  _`nose documentation`: https://nose.readthedocs.org/en/latest/
