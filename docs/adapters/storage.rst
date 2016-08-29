================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage backends.

The storage adapter that your bot uses can be specified by setting the `storage_adapter` parameter to the import path of the storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter"
   )

Read Only Mode
==============

If you instantiate your chatterbot with the parameter `read_only=True`
then the database will not be altered when input is given to the chatterbot.
The `read_only` parameter is set to false by default.

Json Database Adapter
=====================

.. autofunction:: chatterbot.adapters.storage.JsonFileStorageAdapter

"chatterbot.adapters.storage.JsonFileStorageAdapter"

The JSON Database adapter requires an additional parameter (`database`) to be
passed to the ChatterBot constructor. This storage adapter uses a local file
database so this parameter is needed to specify the location of the file.

Mongo Database Adapter
======================

.. autofunction:: chatterbot.adapters.storage.MongoDatabaseAdapter

"chatterbot.adapters.storage.MongoDatabaseAdapter"

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

Twitter Adapter
==============================

.. autofunction:: chatterbot.adapters.storage.TwitterAdapter

"chatterbot.adapters.storage.TwitterAdapter"

Create an app from you twiter acccount, Once created
It will have following app credentails that are required to work with 
TwitterAdapter.

twitter_consumer_key
--------------------
Consumer key of twitter app.

twitter_consumer_secret
-----------------------
Consumer secret of twitter app.

twitter_access_token_key
------------------------
Access token key of twitter app.

twitter_access_token_secret
---------------------------
Access token secret of twitter app.

Creating a new storage adapter
==============================

It is fairly easy to write your own storage adapter to connect to just about
any database or storage endpoint. To get started, you will need to create a
new class that inherits from `StorageAdapter` which is located in
`chatterbot.adapters.storage`.

.. autofunction:: chatterbot.adapters.storage.StorageAdapter

You will then need to implement the interface established by the `StorageAdapter` class.

.. literalinclude:: ../../chatterbot/adapters/storage/storage_adapter.py
   :language: python

