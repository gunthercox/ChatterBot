=============
Conversations
=============

..  _conversation_statements:

Statements
==========

ChatterBot's statement objects represent either an input statement that the
chat bot has recieved from a user, or an output statement that the chat bot
has returned based on some input.

.. autoclass:: chatterbot.conversation.Statement
   :members:

..  _conversation_responses:

Responses
=========

ChatterBot's response objects represent the relationship between two
statements. A response indicates that one statements was issued in
response to another statement.

.. autoclass:: chatterbot.conversation.Response
   :members:

Statement-response relationship
===============================

.. image:: _static/statement-response-relationship.svg
   :alt: ChatterBot statement-response relationship

Each :code:`Statement` object has an :code:`in_response_to` reference which links the
statement to a number of other statements that it has been learned to be in response to.
The :code:`in_response_to` attribute is essentially a reference to all parent statements
of the current statement.

The :code:`Response` object's :code:`occurrence` attribute indicates the number of times
that the statement has been given as a response. This makes it possible for the chat bot
to determine if a particular response is more commonly used than another.

Statement comparison
====================

ChatterBot uses :code:`Statement` objects to hold information
about things that can be said. An important part of how a chat bot
selects a response is based on it's ability to compare two statements
to each other. There is a number of ways to do this, and ChatterBot
comes with a handfull of method built in for you to use.

.. automodule:: chatterbot.conversation.comparisons
   :members:

Setting the comparison method
-----------------------------

To set the statement comparison method for your chat bot, you
will need to pass the :code:`statement_comparison_function` parameter
to your chat bot when you initialize it. An example of this
is shown bellow.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.conversation.comparisons import levenshtein_distance

   chatbot = ChatBot(
       # ...
       statement_comparison_function=levenshtein_distance
   )