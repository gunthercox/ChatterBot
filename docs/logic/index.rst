==============
Logic Adapters
==============

Logic adapters determine the logic for how ChatterBot selects a response to a given input statement.

.. toctree::
   :maxdepth: 1

   response-selection
   create-a-logic-adapter

The logic adapter that your bot uses can be specified by setting the ``logic_adapters`` parameter
to the import path of the logic adapter you want to use.


.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       logic_adapters=[
           "chatterbot.logic.BestMatch"
       ]
   )


It is possible to enter any number of logic adapters for your bot to use.
If multiple adapters are used, then the bot will return the response with
the highest calculated confidence value. If multiple adapters return the
same confidence, then the adapter that is entered into the list first will
take priority.

.. image:: ../_static/dialog-processing-flow.svg
   :alt: ChatterBot dialog processing flow


Common logic adapter attributes
=================================

Each logic adapter inherits the following attributes and methods.

.. autoclass:: chatterbot.logic.LogicAdapter
   :members:


Best Match Adapter
==================

.. autofunction:: chatterbot.logic.BestMatch

The ``BestMatch`` logic adapter selects a response based on the best known match to a given statement.

How it works
------------

The best match adapter uses a function to compare the input statement to known statements.
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
               "statement_comparison_function": chatterbot.comparisons.LevenshteinDistance,
               "response_selection_method": chatterbot.response_selection.get_first_response,
               "maximum_similarity_threshold": 0.7
           }
       ]
   )

.. note::

   The values for ``response_selection_method`` and ``statement_comparison_function`` can be a string
   of the path to the function, or a callable.

    See the :ref:`statement-comparison` documentation for the list of functions included with ChatterBot.

    See the :ref:`response-selection` documentation for the list of response selection methods included with ChatterBot.

``maximum_similarity_threshold`` controls when the search stops and, when a default response is configured, whether
an adapter result is accepted instead of that default. If omitted, it uses the selected comparison function's
``default_threshold``: 0.70 for Levenshtein and spaCy similarity, and 0.50 for Jaccard similarity. Custom comparison
functions default to 0.95 and can define their own ``default_threshold`` attribute. Set
``maximum_similarity_threshold`` explicitly to override these starting values. These defaults are not calibrated to
a particular corpus; validate them with representative matches and non-matches for your application.


Excluding words from replies
----------------------------

Set ``excluded_words`` on the ``BestMatch`` adapter to filter its response
candidates. For example, with SQL storage:

.. code-block:: python

   from chatterbot import ChatBot

   blocked_words = {"exampleword"}
   chatbot = ChatBot(
       "Word filter example",
       storage_adapter="chatterbot.storage.SQLStorageAdapter",
       logic_adapters=[{
           "import_path": "chatterbot.logic.BestMatch",
           "excluded_words": list(blocked_words),
           "default_response": "I do not have a suitable reply.",
       }],
   )

SQL storage matches case-insensitive substrings in candidate replies. The
setting does not check the user's input, prevent learning it, or generate a
warning message. Choose a suitable default response as well, because default
responses are not filtered through the candidate query.

To return a specific message for rejected input, check it before calling the
bot. This small application helper uses whole-word matching for its example
list:

.. code-block:: python

   import re

   def reply_to(text):
       words = set(re.findall(r"\w+", text.casefold()))
       if blocked_words.intersection(words):
           return "Please choose different words."
       return str(chatbot.get_response(text))

Rejected text never reaches ``get_response``, so it is not learned through
that call. Adapt the input check to your application's language and matching
requirements; it is separate from the SQL output filter. Preprocessors
transform statements before matching but do not provide this application-level
early return.


Time Logic Adapter
==================

.. autofunction:: chatterbot.logic.TimeLogicAdapter

The ``TimeLogicAdapter`` identifies statements in which a question about the current time is asked.
If a matching question is detected, then a response containing the current time is returned.

.. code-block:: text

   User: What time is it?
   Bot: The current time is 4:45PM.


Mathematical Evaluation Adapter
===============================

.. autofunction:: chatterbot.logic.MathematicalEvaluation

The ``MathematicalEvaluation`` logic adapter checks a given statement to see if
it contains a mathematical expression that can be evaluated.
If one exists, then it returns a response containing the result.
This adapter is able to handle any combination of word and numeric operators.

.. code-block:: text

   User: What is four plus four?
   Bot: (4 + 4) = 8


Specific Response Adapter
=========================

If the input that the chat bot receives, matches the input text specified
for this adapter, the specified response will be returned.

.. autofunction:: chatterbot.logic.SpecificResponseAdapter

Specific response example
-------------------------

.. literalinclude:: ../../examples/specific_response_example.py
   :language: python

Low confidence response example
-------------------------------

.. literalinclude:: ../../examples/default_response_example.py
   :language: python
