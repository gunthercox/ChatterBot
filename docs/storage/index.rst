================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage technologies.

.. toctree::
   :maxdepth: 1

   text-search
   create-a-storage-adapter

The storage adapter that your bot uses can be specified by setting
the ``storage_adapter`` parameter to the import path of the
storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.storage.SQLStorageAdapter"
   )


Common storage adapter attributes
=================================

Each storage adapter inherits the following attributes and methods.

.. autoclass:: chatterbot.storage.StorageAdapter
   :members:


SQL Storage Adapter
===================

.. autoclass:: chatterbot.storage.SQLStorageAdapter
   :members:

MongoDB Storage Adapter
=======================

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:
