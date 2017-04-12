Creating a new storage adapter
==============================

You can write your own storage adapters by creating a new class that
inherits from :code:`StorageAdapter` and overrides the overrides necessary
methods established in the base :code:`StorageAdapter` class.

.. autofunction:: chatterbot.storage.StorageAdapter

You will then need to implement the interface established by the :code:`StorageAdapter` class.

.. literalinclude:: ../../chatterbot/storage/storage_adapter.py
   :language: python
