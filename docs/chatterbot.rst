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

Parameters
==========

name
----

A name is the only required parameter for the ChatBot class.
This should be a string representing the name of your chat bot.

.. code-block:: python

   ChatBot('Northumberland')

storage_adapter
---------------

.. code-block:: python

   ChatBot(
       # ...
       storage_adapter='my.storage.AdapterClass'
   )

See the documentation on storage adapters for more information.

logic_adapters
--------------

.. code-block:: python

   ChatBot(
       # ...
       storage_adapter='my.logic.AdapterClass'
   )

See the documentation on logic adapters for more information.

input_adapter
-------------

.. code-block:: python

   ChatBot(
       # ...
       storage_adapter='my.input.AdapterClass'
   )

See the documentation on input adapters for more information.

output_adapter
--------------

.. code-block:: python

   ChatBot(
       # ...
       storage_adapter='my.output.AdapterClass'
   )

See the documentation on output adapters for more information.

filters
-------

.. code-block:: python

   ChatBot(
       # ...
       filters=[
           'my.filter.FilterClass1',
           'my.filter.FilterClass2'
       ]
   )

See the documentation on filters for more information.

trainer
-------

.. code-block:: python

   ChatBot(
       # ...
       trainer='my.trainer.TrainerClass'
   )

See the documentation on training for more information.

logger
------

You can choose to use your own custom logging class with your chat bot.
This can be useful when testing and debugging your code.

.. code-block:: python

   import logging

   custom_logger = logging.getLogger(__name__)

   ChatBot(
       # ...
       logger=custom_logger
   )

Note that ChatterBot has built in info-level logging. You can enable ChatterBot's
logging by setting the logging level to INFO at the top of your python code.

.. code-block:: python

   import logging

   logging.basicConfig(level=logging.INFO)

   ChatBot(
       # ...
   )

