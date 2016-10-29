==========
ChatterBot
==========

The main class :code:`ChatBot` is a connecting point between each of
ChatterBot's adapters. In this class, an input statement is returned
from the input adapter, processed and stored by the logic and storage
adapters, and then passed to the output adapter to be returned to the
user.

.. autoclass:: chatterbot.ChatBot
   :members:

   :param name: A name is the only required parameter for the ChatBot class.
   :type name: str

   :param storage_adapter: The import path to a storage adapter class.
   :type storage_adapter: str

   :param logic_adapters: A list of string paths to each logic adapter the bot uses.
   :type logic_adapters: list

   :param input_adapter: The import path to an input adapter class.
   :type input_adapter: str

   :param output_adapter: The import path to an output adapter class.
   :type output_adapter: str

   :param trainer: The import path to the training class to be used with the chat bot.
   :type trainer: str

   :param filters: A list of import paths to filter classes to be used by the chat bot.
   :type filters: list

   :param logger: A :code:`Logger` object.
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


Enable logging
==============

ChatterBot has built in logging. You can enable ChatterBot's
logging by setting the logging level at the top of your python code.

.. code-block:: python

   import logging

   logging.basicConfig(level=logging.INFO)

   ChatBot(
       # ...
   )


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
