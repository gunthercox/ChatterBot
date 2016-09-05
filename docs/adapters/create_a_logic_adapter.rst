Creating a new logic adapter
============================

You can write your own logic adapters by creating a new class that
inherits from `LogicAdapter` and overides the overrides necessary
methods established in the base `LogicAdapter` class.

.. autofunction:: chatterbot.adapters.logic.LogicAdapter

.. code-block:: python

   from chatterbot.adapters.logic import LogicAdapter

   class MyLogicAdapter(LogicAdapter):
       def __init__(self, **kwargs):
           super(MyLogicAdapter, self).__init__(kwargs)

       def can_process(self, statement):
           return True

       def process(self, statement):
           return confidence, selected_statement

LogicAdapter: process
---------------------

This method is where you must implement your logic for selecting a response to
an input statement.

A confidence value and the selected response statement should be returned.
The confidence value represents a rating of how accurate the logic adapter
expects the selected response to be. Confidence scores are used to select
the best response from multiple logic adapters.

.. note::

   The confidence value should be a number between 0 and 1 where 0 is the
   lowest confidence level and 1 is the highest.

LogicAdapter: __init__
----------------------

The __init__ method is optional for any logic adapter you create.

.. note::

   If you override the `__init__` method on your logic adapter, you must
   call super().

All key word arguments that have been set in your ChatBot class's constructor
will also be passed to the init method of each logic adapter. This allows you
to access these variables if you need to use them in your logic adapter.
(An API key might be an example of a parameter you would want to access here.)

LogicAdapter: can_process
-------------------------

This is a preliminary method that can be used to check the input statement to
see if a value can possibly be returned when it is evaluated using the
adapter's process method.

This method returns a boolean value.

.. note::

   This method returns true by default if you do not override it.

