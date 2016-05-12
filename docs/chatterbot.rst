ChatterBot
==========

.. autofunction:: chatterbot.ChatBot

The main class :code:`ChatBot` is a connecting point between each of
ChatterBot's adapters. In this class, an input statement is returned
from the input adapter, processed and stored by the logic and storage
adapters, and then passed to the output adapter to be returned to the
user.

Getting a response
------------------

The method that is used to get a response to a given input
is :code:`get_response()`. This method takes an input value
which the chat bot's input adapter then converts into a
statement object before processing it.
