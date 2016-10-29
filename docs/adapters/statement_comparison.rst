====================
Statement comparison
====================

ChatterBot uses :code:`Statement` objects to hold information
about things that can be said. An important part of how a chat bot
selects a response is based on it's ability to compare two statements
to each other. There is a number of ways to do this, and ChatterBot
comes with a handfull of method built in for you to use.

Statement comparison methods
============================

.. automodule:: chatterbot.conversation.comparisons
   :members:

Setting the comparison selection method
=================================================

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