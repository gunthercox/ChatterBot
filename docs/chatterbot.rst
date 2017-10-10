==========
ChatterBot
==========

The main class ``ChatBot`` is a connecting point between each of
ChatterBot's :term:`adapters`. In this class, an input statement is returned
from the :term:`input adapter`, processed and stored by the :term:`logic adapter`
and :term:`storage adapter`, and then passed to the output adapter to be returned
to the user.

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

   :param input_adapter: The dot-notated import path to an input adapter class.
                         Defaults to ``"chatterbot.input.VariableInputTypeAdapter"``.
   :type input_adapter: str

   :param output_adapter: The dot-notated import path to an output adapter class.
                          Defaults to ``"chatterbot.output.OutputAdapter"``.
   :type output_adapter: str

   :param trainer: The dot-notated import path to the training class to be used with the chat bot.
   :type trainer: str

   :param filters: A list of dot-notated import paths to filter classes to be used by the chat bot.
   :type filters: list

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
       input_adapter='my.input.AdapterClass',
       output_adapter='my.output.AdapterClass',
       trainer='my.trainer.TrainerClass',
       filters=[
           'my.filter.FilterClass1',
           'my.filter.FilterClass2'
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
           'database_name': 'my-database'
       },
       logic_adapters=[
           {
               'import_path': 'my.logic.AdapterClass1',
               'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance'
               'response_selection_method': 'chatterbot.response_selection.get_first_response'
           },
           {
               'import_path': 'my.logic.AdapterClass2',
               'statement_comparison_function': 'my.custom.comparison_function'
               'response_selection_method': 'my.custom.selection_method'
           }
       ],
       input_adapter={
           'import_path': 'my.input.AdapterClass',
           'api_key': '0000-1111-2222-3333-DDDD'
       },
       output_adapter={
           'import_path': 'my.output.AdapterClass',
           'api_key': '0000-1111-2222-3333-DDDD'
       }
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
these are storage adapters, input adapters, output adapters and logic adapters.

Adapters types
--------------

1. Storage adapters - Provide an interface for ChatterBot to connect to various storage systems such as `MongoDB`_ or local file storage.
2. Input adapters - Provide methods that allow ChatterBot to get input from a defined data source.
3. Output adapters - Provide methods that allow ChatterBot to return a response to a defined data source.
4. Logic adapters - Define the logic that ChatterBot uses to respond to input it receives.

Accessing the chatbot instance
-------------------------------

When ChatterBot initializes each adapter, it sets an attribute named ``chatbot``.
The chatbot variable makes it possible for each adapter to have access to all of the other adapters being used.
Suppose two input and output adapters need to share some information or perhaps you want to give your logic adapter
direct access to the storage adapter. These are just a few cases where this functionality is useful.

Each adapter can be accessed on the chatbot object from within an adapter by referencing `self.chatbot`.
Then, ``self.chatbot.storage`` refers to the storage adapter, ``self.chatbot.input`` refers to the input adapter,
``self.chatbot.output`` refers to the current output adapter, and ``self.chatbot.logic`` refers to the logic adapters.

.. _MongoDB: https://docs.mongodb.com/
.. _`Python logging documentation`: https://docs.python.org/3/library/logging.html#logging-levels
