=============
Conversations
=============

ChatterBot supports the ability to have multiple concurrent conversations.
A conversations is where the chat bot interacts with a person, and supporting
multiple concurrent conversations means that the chat bot can have multiple
different conversations with different people at the same time.

Conversation scope
------------------

If two :code:`ChatBot` instances are created, each will have conversations separate from each other.

An adapter can access any conversation as long as the unique identifier for the conversation is provided.

Conversation example
--------------------

The following example is taken from the Django :code:`ChatterBotView` built into ChatterBot.
In this method, the unique identifiers for each chat session are being stored in Django's
session objects. This allows different users who interact with the bot through different
web browsers to have separate conversations with the chat bot.

.. literalinclude:: ../chatterbot/ext/django_chatterbot/views.py
   :language: python
   :pyobject: ChatterBotView.post
   :dedent: 4


..  _conversation_statements:

Statements
==========

ChatterBot's statement objects represent either an input statement that the
chat bot has received from a user, or an output statement that the chat bot
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
statements. A response indicates that one statement was issued in
response to another statement.

.. autoclass:: chatterbot.conversation.Response
   :members:

Statement-response relationship
===============================

ChatterBot stores knowledge of conversations as statements. Each statement can have any
number of possible responses.

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
