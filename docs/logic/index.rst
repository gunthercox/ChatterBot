==============
Logic Adapters
==============

Logic adapters determine the logic for how ChatterBot selects a responses to a given input statement.

.. toctree::
   :maxdepth: 1

   multi-logic-adapter
   response_selection
   create-a-logic-adapter

The logic adapter that your bot uses can be specified by setting the :code:`logic_adapters` parameter
to the import path of the logic adapter you want to use.

It is possible to enter any number of logic adapters for your bot to use.
If multiple adapters are used, then the bot will return the response with
the highest calculated confidence value. If multiple adapters return the
same confidence, then the adapter that is entered into the list first will
take priority.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       logic_adapters=[
           "chatterbot.logic.BestMatch"
       ]
   )


Best Match Adapter
==================

.. autofunction:: chatterbot.logic.BestMatch

The :code:`BestMatch` logic adapter selects a response based on the best know match to a given statement.

How it works
------------

The best match adapter determines uses an function to compare the input statement to known statements.
Once it finds the closest match to the input statement, it uses another function to select one of the
known responses to that statement.

Setting parameters
------------------

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       logic_adapters=[
           {
               "import_path": "chatterbot.logic.BestMatch",
               "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
               "response_selection_method": "chatterbot.response_selection.get_first_response"
           }
       ]
   )

.. note::

   The values for :code:`response_selection_method` and :code:`statement_comparison_function` can be a string
   of the path to the function, or a callable.

    See the :ref:`statement-comparison` documentation for the list of functions included with ChatterBot.

    See the :ref:`response-selection` documentation for the list of response selection methods included with ChatterBot.


Time Logic Adapter
==================

.. autofunction:: chatterbot.logic.TimeLogicAdapter

The :code:`TimeLogicAdapter` identifies statements in which a question about the current time is asked.
If a matching question is detected, then a response containing the current time is returned.

.. code-block:: text

   User: What time is it?
   Bot: The current time is 4:45PM.


Mathematical Evaluation Adapter
===============================

.. autofunction:: chatterbot.logic.MathematicalEvaluation

The :code:`MathematicalEvaluation` logic adapter checks a given statement to see if
it contains a mathematical expression that can be evaluated.
If one exists, then it returns a response containing the result.
This adapter is able to handle any combination of word and numeric operators.

.. code-block:: text

   User: What is four plus four?
   Bot: (4 + 4) = 8


Low Confidence Response Adapter
===============================

This adapter returns a specified default response if a response can not be
determined with a high amount of confidence.

.. autofunction:: chatterbot.logic.LowConfidenceAdapter

Low confidence response example
-------------------------------

.. literalinclude:: ../../examples/default_response_example.py
   :language: python


Specific Response Adapter
=========================

If the input that the chat bot recieves, matches the input text specified
for this adapter, the specified response will be returned.

.. autofunction:: chatterbot.logic.SpecificResponseAdapter

Specific response example
-------------------------

.. literalinclude:: ../../examples/specific_response_example.py
   :language: python
