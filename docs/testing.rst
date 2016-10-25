============
Unit Testing
============

ChatterBot's built in tests can be run using nose.
See the `nose documentation`_ for more information.

.. sourcecode:: sh

   nosetests

Note that nose also allows you to specify individual test cases to run.
For example, the following command will run all tests in the test-module `tests/logic_adapter_tests`

.. sourcecode:: sh

   nosetests tests/logic_adapter_tests

Tests for Django integration have been included in the example Django app and
can be run with:

.. sourcecode:: sh

   python examples/django_app/manage.py test

..  _`nose documentation`: https://nose.readthedocs.org/en/latest/
