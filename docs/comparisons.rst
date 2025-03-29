===========
Comparisons
===========

.. _statement-comparison:

Statement comparison
====================

ChatterBot uses ``Statement`` objects to hold information
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
will need to pass the ``statement_comparison_function`` parameter
to your chat bot when you initialize it. An example of this
is shown below.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.comparisons import LevenshteinDistance

   chatbot = ChatBot(
       # ...
       statement_comparison_function=LevenshteinDistance
   )


Taggers
=======

ChatterBot supports a number of different taggers that can be used to
process the input text. The taggers are used to identify the parts of speech
in the input text and can be used to improve the accuracy of the response selection.

.. automodule:: chatterbot.tagging
   :members:
   :undoc-members:

Languages
=========

ChatterBot's ``languages`` module contains helper classes for working with
language codes and names.

.. autoclass:: chatterbot.languages.ENG

.. autoclass:: chatterbot.languages.FRE

.. autoclass:: chatterbot.languages.GER

.. autoclass:: chatterbot.languages.ITA

.. autoclass:: chatterbot.languages.JPN

.. autoclass:: chatterbot.languages.KOR

.. autoclass:: chatterbot.languages.POR

.. autoclass:: chatterbot.languages.RUS

.. autoclass:: chatterbot.languages.SPA

.. autoclass:: chatterbot.languages.SWE

.. autoclass:: chatterbot.languages.TUR

.. autoclass:: chatterbot.languages.ZHT

See ``chatterbot.languages`` for the full list of languages.
