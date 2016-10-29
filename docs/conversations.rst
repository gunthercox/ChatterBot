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