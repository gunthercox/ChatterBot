==========
ChatterBot
==========

The main class ``ChatBot`` is a connecting point between each of
ChatterBot's :term:`adapters`. In this class, an input statement is
processed and stored by the :term:`logic adapter` and :term:`storage adapter`.
A response to the input is then generated and returned.

.. autoclass:: chatterbot.ChatBot
   :members:

   :param name: A name is the only required parameter for the ChatBot class.
   :type name: str

   :keyword storage_adapter: The dot-notated import path to a storage adapter class.
                             Defaults to ``"chatterbot.storage.SQLStorageAdapter"``.
   :type storage_adapter: str

   :param logic_adapters: A list of dot-notated import paths to each logic adapter the bot uses.
                          Defaults to ``["chatterbot.logic.BestMatch"]``.
   :type logic_adapters: list

   :param logger: A ``Logger`` object.
   :type logger: logging.Logger

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
