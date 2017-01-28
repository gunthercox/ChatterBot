=============
Conversations
=============

ChatterBot supports the ability to have multiple concurrent conversations.
A conversation occurs when the chat bot interacts with a person, and supporting
multiple conversations means that your chat bot can have multiple different
conversations with different people at the same time.

.. autoclass:: chatterbot.conversation.session.Conversation
   :members:

.. autoclass:: chatterbot.conversation.session.ConversationManager
   :members:

Conversation scope
------------------

If two :code:`ChatBot` instances are created, each will have conversations separate from each other.

An chat bot's logic adapters can access any conversation as long as the unique identifier for the conversation is provided.

Conversation example 
--------------------

The following example is taken from the Django :code:`ChatterBotView` built into ChatterBot.
In this method, the unique identifiers for each conversation are being stored in Django's
session objects. This allows different users who interact with the bot through different
web browsers to have seperate conversations with the chat bot.

.. literalinclude:: ../chatterbot/ext/django_chatterbot/views.py
   :language: python
   :pyobject: ChatterBotView.post
   :dedent: 4

..  _conversation_statements:

Statements
==========

ChatterBot's statement objects represent either an input statement that the
chat bot has recieved from a user, or an output statement that the chat bot
has returned based on some input.

.. autoclass:: chatterbot.conversation.Statement
   :members:

   .. autoinstanceattribute:: chatterbot.conversation.Statement.confidence

      ChatterBot's logic adapters assign a confidence score to the statement
      before it is returned. The confidence score indicates the degree of
      certainty with which the chat bot believes this is the correct response
      to the given input. 

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

ChatterBot stores knowledge of conversations as statements. Each statement can have any
number possible responses.

.. image:: _static/statement-response-relationship.svg
   :alt: ChatterBot statement-response relationship

Each :code:`Statement` object has an :code:`in_response_to` reference which links the
statement to a number of other statements that it has been learned to be in response to.
The :code:`in_response_to` attribute is essentially a reference to all parent statements
of the current statement.

.. image:: _static/statement-relationship.svg
   :alt: ChatterBot statement relationship

The :code:`Response` object's :code:`occurrence` attribute indicates the number of times
that the statement has been given as a response. This makes it possible for the chat bot
to determine if a particular response is more commonly used than another.

.. _statement-comparison:

Statement comparison
====================

ChatterBot uses :code:`Statement` objects to hold information
about things that can be said. An important part of how a chat bot
selects a response is based on it's ability to compare two statements
to each other. There is a number of ways to do this, and ChatterBot
comes with a handfull of method built in for you to use.

.. automodule:: chatterbot.comparisons
   :members:

Use your own comparison function
++++++++++++++++++++++++++++++++

You can create your own comparison function and use it as long as the function takes two statements
as parameters and returns a numeric value between 0 and 1. A 0 should represent the lowest possible
similarity and a 1 should represent the highest possibel similarity.

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
is shown bellow.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.comparisons import levenshtein_distance

   chatbot = ChatBot(
       # ...
       statement_comparison_function=levenshtein_distance
   )
