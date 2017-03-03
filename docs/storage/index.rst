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
       storage_adapter="chatterbot.storage.JsonFileStorageAdapter"
   )

Json File Storage Adapter
=========================

.. autoclass:: chatterbot.storage.JsonFileStorageAdapter
   :members:
   :special-members: AdapterUnsuitableForProductionWarning

Mongo Database Adapter
======================

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:
