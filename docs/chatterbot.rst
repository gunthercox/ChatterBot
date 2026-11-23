==========
ChatterBot
==========

The main class ``ChatBot`` is a connecting point between each of
ChatterBot's :term:`adapters`. In this class, an input statement is
processed and stored by the :term:`logic adapter` and :term:`storage adapter`.
A response to the input is then generated and returned.

.. autoclass:: chatterbot.ChatBot
   :members:

Example chat bot parameters
===========================

.. code-block:: python

   ChatBot(
       'Northumberland',
       storage_adapter='my.storage.AdapterClass',
       logic_adapters=[
           'my.logic.AdapterClass1',
           'my.logic.AdapterClass2'
       ],
       logger=custom_logger
   )


Example expanded chat bot parameters
====================================

It is also possible to pass parameters directly to individual adapters.
To do this, you must use a dictionary that contains a key called ``import_path``
which specifies the import path to the adapter class.

.. code-block:: python

   ChatBot(
       'Leander Jenkins',
       storage_adapter={
           'import_path': 'my.storage.AdapterClass',
           'database_uri': 'protocol://my-database'
       },
       logic_adapters=[
           {
               'import_path': 'my.logic.AdapterClass1',
               'statement_comparison_function': chatterbot.comparisons.LevenshteinDistance
               'response_selection_method': chatterbot.response_selection.get_first_response
           },
           {
               'import_path': 'my.logic.AdapterClass2',
               'statement_comparison_function': my_custom_comparison_function
               'response_selection_method': my_custom_selection_method
           }
       ]
   )


Enable logging
==============

ChatterBot has built in logging. You can enable ChatterBot's
logging by setting the logging level in your code.

.. code-block:: python

   import logging

   logging.basicConfig(level=logging.INFO)

   ChatBot(
       # ...
   )

The logging levels available are
``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG``, and ``NOTSET``.
See the `Python logging documentation`_ for more information.

Using a custom logger
=====================

You can choose to use your own custom logging class with your chat bot.
This can be useful when testing and debugging your code.

.. code-block:: python

   import logging

   custom_logger = logging.getLogger(__name__)

   ChatBot(
       # ...
       logger=custom_logger
   )

Saving a conversation transcript
================================

Diagnostic logging describes how adapters choose responses. To record the
input and the final reply together, log them around ``get_response`` in your
application. This works independently of the storage adapter, including when
``read_only=True`` disables conversational learning.

For an existing, non-streaming ``chatbot`` instance, the following helper
appends one JSON object per line to a UTF-8 file:

.. code-block:: python

   import json
   from datetime import datetime, timezone

   def get_logged_response(chatbot, text, conversation, log_path="conversation.jsonl"):
       response = chatbot.get_response(text, conversation=conversation)
       record = {
           "timestamp": datetime.now(timezone.utc).isoformat(),
           "conversation": response.conversation,
           "input": text,
           "response": response.text,
           "confidence": response.confidence,
       }
       with open(log_path, "a", encoding="utf-8") as log_file:
           log_file.write(json.dumps(record, ensure_ascii=False) + "\n")
       return response

JSON escapes newlines inside messages, so each transcript entry still occupies
one line. Open the file in append mode to preserve earlier entries, and use a
stable conversation identifier to group turns from the same session.

The corpus trainer does not attach a training file path to each generated
response. This transcript helps identify unwanted replies during testing but
does not recover their source filename. To track that provenance, keep a
separate text-to-source index when preparing your training data.


Adapters
========

ChatterBot uses adapter modules to control the behavior of specific types of tasks.
There are four distinct types of adapters that ChatterBot uses,
these are storage adapters and logic adapters.

Adapters types
--------------

1. Storage adapters - Provide an interface for ChatterBot to connect to various storage systems such as `MongoDB`_ or local file storage.
2. Logic adapters - Define the logic that ChatterBot uses to respond to input it receives.

Accessing the ChatBot instance
-------------------------------

When ChatterBot initializes each adapter, it sets an attribute named ``chatbot``.
The chatbot variable makes it possible for each adapter to have access to all of the other adapters being used.
Suppose logic adapters need to share some information or perhaps you want to give your logic adapter
direct access to the storage adapter. These are just a few cases where this functionality is useful.

Each adapter can be accessed on the chatbot object from within an adapter by referencing `self.chatbot`.
Then, ``self.chatbot.storage`` refers to the storage adapter, and ``self.chatbot.logic`` refers to the logic adapters.

.. _MongoDB: https://docs.mongodb.com/
.. _`Python logging documentation`: https://docs.python.org/3/library/logging.html#logging-levels
