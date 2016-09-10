=======================================
Using tie breaking to choose a response
=======================================

A typical logic adapter designed to return a response
to an input statement will use two main steps to do this.
The first step involves searching the database for a known
statement that matches or closely matches the input statement.
Once a match is selected, the second step involves selecting a
known response to the selected match. Frequently, there will
be a number of existing statements that are responses to the
known match. To help with the selection of the response,
several tie-breaking methods are available.
 
.. autoclass:: chatterbot.adapters.logic.mixins.TieBreaking
   :members:

Using TieBreaking
=================

To use this mixin, have your logic adapter class inherit from it.

.. code-block:: python

   from chatterbot.adapters.logic.mixins import TieBreaking

   class MyLogicAdapter(TieBreaking, LogicAdapter):

Then, in your init method, add an attribute to get the
tie breaking method from the key word arguments.

.. code-block:: python

   def __init__(self, **kwargs):
       self.tie_breaking_method = kwargs.get(
           'tie_breaking_method',
           'first_response'
       )

When your logic adapter needs to select one of several possible
responses, call the tie breaking method and pass in the required parameters.

.. code-block:: python

   response = self.break_tie(
       input_statement,
       response_list,
       self.tie_breaking_method
   )
