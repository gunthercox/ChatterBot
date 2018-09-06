====================================
How logic adapters select a response
====================================

A typical logic adapter designed to return a response to
an input statement will use two main steps to do this.
The first step involves searching the database for a known
statement that matches or closely matches the input statement.
Once a match is selected, the second step involves selecting a
known response to the selected match. Frequently, there will
be a number of existing statements that are responses to the
known match.

To help with the selection of the response, several methods
are built into ChatterBot for selecting a response from the
available options.

.. _response-selection:

Response selection methods
==========================

.. automodule:: chatterbot.response_selection
   :members:

Use your own response selection method
++++++++++++++++++++++++++++++++++++++

You can create your own response selection method and use it as long as the function takes 
two parameters (a statements and a list of statements). The method must return a statement.

.. code-block:: python

   def select_response(statement, statement_list, storage=None):

       # Your selection logic

       return selected_statement

Setting the response selection method
=====================================

To set the response selection method for your chat bot, you
will need to pass the :code:`response_selection_method` parameter
to your chat bot when you initialize it. An example of this
is shown below.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.response_selection import get_most_frequent_response

   chatbot = ChatBot(
       # ...
       response_selection_method=get_most_frequent_response
   )

Response selection in logic adapters
====================================

When a logic adapter is initialized, the response selection method
parameter that was passed to it can be called using :code:`self.select_response`
as shown below.

.. code-block:: python

   response = self.select_response(
       input_statement,
       list_of_response_options,
       self.chatbot.storage
   )
