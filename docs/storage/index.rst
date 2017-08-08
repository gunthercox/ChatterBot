================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage backends.

.. toctree::
   :maxdepth: 1

   create-a-storage-adapter

The storage adapter that your bot uses can be specified by setting
the :code:`storage_adapter` parameter to the import path of the
storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.storage.SQLStorageAdapter"
   )

SQL Storage Adapter
===================

.. autoclass:: chatterbot.storage.SQLStorageAdapter
   :members:

MongoDB Storage Adapter
=======================

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:
