============
Unit Testing
============

*"A true professional does not waste the time and money of other people by handing over software that is not reasonably free of obvious bugs;
that has not undergone minimal unit testing; that does not meet the specifications and requirements;
that is gold-plated with unnecessary features; or that looks like junk."* – Daniel Read

Running tests
-------------

You can run ChatterBot's main test suite using Python's built-in test runner. For example:

.. sourcecode:: sh

   python -m unittest discover -s tests -v

This command will run all tests including Django integration tests (if Django is installed).

*Note* that the ``unittest`` command also allows you to specify individual test cases to run.
For example, the following command will run all tests in the test-module `tests/logic/`

.. sourcecode:: sh

   python -m unittest discover -s tests/logic/ -v

To run a specific test in a test class you can specify the test method name using the following pattern:

.. sourcecode:: sh

   python -m unittest tests.logic.test_best_match.BestMatchTestCase.test_match_with_response

Tests can also be run in "fail fast" mode, in which case they will run until the first test failure is encountered.

.. sourcecode:: sh

   python -m unittest discover -f tests

Django integration tests
------------------------

Django integration tests are included in ``tests/django_integration/`` and will automatically run 
when you execute the main test suite (if Django is installed). If Django is not available, 
these tests will be gracefully skipped.

To run only Django integration tests:

.. sourcecode:: sh

   python -m unittest discover -s tests/django_integration/ -v

The Django example app tests can be run separately with the following command from within 
the `examples/django_example` directory:

.. sourcecode:: sh

   python manage.py test

Benchmark tests
---------------

You can run a series of benchmark tests that test a variety of different chat bot configurations for
performance by running the following command.

.. sourcecode:: sh

   python tests/benchmarks.py


Testing documentation builds
----------------------------

The HTML documentation for ChatterBot can be compiled using using `Sphinx`_. To build it run the following command from the root directory of the project:

.. sourcecode:: sh

   sphinx-build -nW -b dirhtml docs/ html/


.. _Sphinx: http://www.sphinx-doc.org/
.. _unittest documentation: https://docs.python.org/3/library/unittest.html#command-line-interface
