Creating a new storage adapter
==============================

You can write your own storage adapters by creating a new class that
inherits from ``StorageAdapter`` and overrides necessary
methods established in the base ``StorageAdapter`` class.

You will then need to implement the interface established by the ``StorageAdapter`` class.

.. literalinclude:: ../../chatterbot/storage/storage_adapter.py
   :language: python
