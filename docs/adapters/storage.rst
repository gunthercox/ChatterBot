================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage backends.

The storage adapter that your bot uses can be specified by setting the `storage_adapter` parameter to the import path of the storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.storage.JsonFileStorageAdapter"
   )

Read Only Mode
==============

If you instantiate your chatterbot with the parameter `read_only=True`
then the database will not be altered when input is given to the chatterbot.
The `read_only` parameter is set to false by default.

Json File Storage Adapter
=========================

.. autofunction:: chatterbot.storage.JsonFileStorageAdapter

"chatterbot.storage.JsonFileStorageAdapter"

The JSON Database adapter requires an additional parameter (`database`) to be
passed to the ChatterBot constructor. This storage adapter uses a local file
database so this parameter is needed to specify the location of the file.

.. note::

   The json file storage adapter will display an UnsuitableForProductionWarning
   when it is initialized because it is not intended for use in large scale production
   applications. You can silence this warning by setting `silence_performance_warning=True`
   when initializing the adapter.

Mongo Database Adapter
======================

.. autofunction:: chatterbot.storage.MongoDatabaseAdapter

"chatterbot.storage.MongoDatabaseAdapter"

database
--------

The MongoDB Database adapter requires an additional parameter, `database`,
to be passed to the ChatterBot constructor. This value will be the name
of the database you choose to connect to.

.. code-block:: python

   database='chatterbot-database'

database_uri
------------

If you need to connect to a remote instance of MongoDB, you
can set the `database_uri` parameter to the uri of your database.

.. code-block:: python

   database_uri='mongodb://example.com:8100/'
