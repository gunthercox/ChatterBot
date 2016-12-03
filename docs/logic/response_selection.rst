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
are build in to ChatterBot for selecting a response from the
available options.

.. _response-selection:

Response selection methods
==========================

.. automodule:: chatterbot.conversation.response_selection
   :members:

Setting the response selection method
=====================================

To set the response selection method for your chat bot, you
will need to pass the :code:`response_selection_method` parameter
to your chat bot when you initialize it. An example of this
is shown bellow.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.conversation.response_selection import get_most_frequent_response

   chatbot = ChatBot(
       # ...
       response_selection_method=get_most_frequent_response
   )

Response selection in logic adapters
====================================

When a logic adapter is initialized, the response selection method
parameter that was passed to it can be called using :code:`self.select_response`
as shown bellow.

.. code-block:: python

   response = self.select_response(
       input_statement, list_of_response_options
   )
