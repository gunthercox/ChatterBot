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
   
Makefile Utility
----------------

Makefiles are a simple way to perform code compilation on ``Linux platforms``.

We often forgot to build docs, run nosetes or Django tests whenever we make any change in existing files,
and when we create a pull request for the same,it fails the build giving the explanation : 
`Some checks were not successful`

To avoid all your problems with the Travis CI, use the ``MAKEFILE``. It will help you with the code to avoid problems,
failing the build by Travis CI.

To see the list of avaliable commands with MAKEFILE:

.. sourcecode:: sh

   make help

To run all tests:

.. sourcecode:: sh

   make all

To clean your workspace with un-versioned files

.. sourcecode:: sh

   make clean

..  _`nose documentation`: https://nose.readthedocs.org/en/latest/
