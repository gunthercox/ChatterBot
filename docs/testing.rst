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

For more information on ``unittest`` functionality, see the `unittest documentation`_.

Django integration tests
------------------------

Tests for Django integration have been included in the `tests_django` directory and
can be run with:

.. sourcecode:: sh

   python runtests.py

Django example app tests
------------------------

Tests for the example Django app can be run with the following command from within the `examples/django_example` directory.

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

   sphinx-build -nW -b dirhtml docs/ build/


.. _Sphinx: http://www.sphinx-doc.org/
.. _unittest documentation: https://docs.python.org/3/library/unittest.html#command-line-interface
