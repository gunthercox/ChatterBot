==============
Logic Adapters
==============

Logic adapters determine the logic for how ChatterBot selects a responses to a given input statement.

.. toctree::
   :maxdepth: 2

   multi-logic-adapter

The logic adapter that your bot uses can be specified by setting the `logic_adapters` parameter to the import path of the logic adapter you want to use.

It is possible to enter any number of logic adapters for your bot to use.
If multiple adapters are used, then the bot will return the response with
the highest calculated confidence value. If multiple adapters return the
same confidence, then the adapter that is entered into the list first will
take priority.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       logic_adapters=[
           "chatterbot.logic.ClosestMatchAdapter"
       ]
   )


Closest Match Adapter
=====================

.. autofunction:: chatterbot.logic.ClosestMatchAdapter

The `ClosestMatchAdapter` selects a response based on the closest know match to a given statement.

How it works
------------

The closest match algorithm determines the similarity between the input statement and a set of known statements. For example, there is a 65% similarity between the statements *"where is the post office?"* and *"looking for the post office"*. The closest match algorithm selects the highest matching known statements and returns a response based on that selection.


Closest Meaning Adapter
=======================

.. autofunction:: chatterbot.logic.ClosestMeaningAdapter

The `ClosestMeaningAdapter` selects a response based on how closely two statements match each other based on the closeness of the synsets of each word in the word matrix formed by both sentences.

How it works
------------

The closest meaning algorithm uses the `wordnet`_ functionality of `NLTK`_ to determine the similarity of two statements based on the path similarity between each token of each statement. This is essentially an evaluation of the closeness of synonyms. The statement that has the closest path similarity of synsets to the input statement is returned.


Approximate Sentence Match Adapter
==================================

.. autofunction:: chatterbot.logic.ApproximateSentenceMatchAdapter

The `ApproximateSentenceMatchAdapter` calculates a Jaccard index and give result to a given statement.

How it works
------------

The Jaccard index is composed of a numerator and denominator.
  In the numerator, we count the number of items that are shared between the sets.
  In the denominator, we count the total number of items across both sets.
  Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent. Here are two sample sentences:

      The young cat is hungry.
      The cat is very hungry.

  When we parse these sentences to remove stopwords, we end up with the following two sets:

      {young, cat, hungry}
      {cat, very, hungry}

  In our example above, our intersection is {cat, hungry}, which has count of two.
  The union of the sets is {young, cat, very, hungry}, which has a count of four.
  Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.


Time Logic Adapter
==================

.. autofunction:: chatterbot.logic.TimeLogicAdapter

The `TimeLogicAdapter` identifies statements in which a question about the current time is asked.
If a matching question is detected, then a response containing the current time is returned.

Example
-------

| User: What time is it?
| Bot: The current time is 4:45PM.


Mathematical Evaluation Adapter
===============================

.. autofunction:: chatterbot.logic.MathematicalEvaluation

The `MathematicalEvaluation` logic adapter checks a given statement to see if
it contains a mathematical expression that can be evaluated. If one exists,
then it returns a response containing the result.
This adapter is able to handle any combination of word and numeric operators.

Example
-------

| User: What is four plus four?
| Bot: (4 + 4) = 8


SentimentAdapter
================

.. autofunction:: chatterbot.logic.SentimentAdapter

This is a logic adapter that selects a response that has the closest matching
sentiment value to the input.


Low Confidence Response Adapter
===============================

This adapter returns a specified default response if a response can not be
determined with a high amount of confidence.

.. autofunction:: chatterbot.logic.LowConfidenceAdapter

Example usage
-------------

.. literalinclude:: ../../examples/default_response_example.py
   :language: python


Specific Response Adapter
=========================

If the input that the chat bot recieves, matches the input text specified
for this adapter, the specified response will be returned.

.. autofunction:: chatterbot.logic.SpecificResponseAdapter

Example usage
-------------

.. literalinclude:: ../../examples/specific_response_example.py
   :language: python

.. _wordnet: http://www.nltk.org/howto/wordnet.html
.. _NLTK: http://www.nltk.org/
.. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
