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
