===========
Comparisons
===========

.. _statement-comparison:

Statement comparison
====================

ChatterBot uses :code:`Statement` objects to hold information
about things that can be said. An important part of how a chat bot
selects a response is based on its ability to compare two statements
to each other. There are a number of ways to do this, and ChatterBot
comes with a handful of methods built in for you to use.

.. automodule:: chatterbot.comparisons
   :members:

Use your own comparison function
++++++++++++++++++++++++++++++++

You can create your own comparison function and use it as long as the function takes two statements
as parameters and returns a numeric value between 0 and 1. A 0 should represent the lowest possible
similarity and a 1 should represent the highest possible similarity.

.. code-block:: python

   def comparison_function(statement, other_statement):

       # Your comparison logic

       # Return your calculated value here
       return 0.0

Setting the comparison method
-----------------------------

To set the statement comparison method for your chat bot, you
will need to pass the :code:`statement_comparison_function` parameter
to your chat bot when you initialize it. An example of this
is shown below.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.comparisons import levenshtein_distance

   chatbot = ChatBot(
       # ...
       statement_comparison_function=levenshtein_distance
   )
