SQL Storage Adapter
===================

Removing a learned statement
----------------------------

For a bot using ``SQLStorageAdapter``, pass the statement's text to
``chatbot.storage.remove``:

.. code-block:: python

   unwanted_text = "An unwanted reply"
   chatbot.storage.remove(unwanted_text)

The argument is a string, not a ``Statement`` object, database ID, training
list, or corpus filename. Removal applies to every stored statement whose
text matches that string, including duplicates learned in different
conversations. Other statement texts are retained. The adapter also removes
the deleted statements' tag associations.

This removes database entries; it does not edit the list or corpus used for
training. Remove the unwanted example from that source too before training
again, or it will be learned again. Statements that refer to the deleted text
through ``in_response_to`` are not recursively deleted.


.. autoclass:: chatterbot.storage.SQLStorageAdapter
   :members:
