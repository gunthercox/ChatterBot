================
Storage Adapters
================

.. meta::
   :description: ChatterBot storage adapters: SQL, Redis vector database, MongoDB. Semantic search with vector embeddings for AI-powered contextual responses
   :keywords: storage adapter, database, SQL, Redis, MongoDB, vector database, semantic search, vector embeddings

Storage adapters provide an interface that allows ChatterBot
to connect to different storage technologies. Each adapter is optimized
for different use cases:

- **Redis Vector Storage**: Semantic similarity search using vector embeddings (best for contextual AI responses)
- **SQL Storage**: Traditional pattern matching with POS-lemma indexing (best for exact phrase matching)
- **MongoDB Storage**: NoSQL document storage with flexible schema
- **Django Storage**: Integrated with Django ORM for web applications

The storage adapter that your bot uses can be specified by setting
the ``storage_adapter`` parameter to the import path of the
storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.storage.SQLStorageAdapter"
   )

Built-in Storage Adapters
=========================

ChatterBot includes multiple storage adapters for different AI and database technologies:

.. toctree::
   :maxdepth: 2

   redis
   mongodb
   sql
   ../django/index

Choosing a Storage Adapter
===========================

**For Semantic AI Chatbots** (Recommended for modern conversational AI):

Note that as of December 2025, the Redis Vector Storage Adapter is still an experimental beta feature.

Use **Redis Vector Storage** when you need:

- Context-aware responses based on meaning, not keywords
- Vector embeddings for semantic similarity search
- Automatic confidence scoring from cosine similarity
- Best match for conversational AI and natural language understanding

**For Pattern-Based Matching**:

Use **SQL Storage** when you need:

- Exact phrase or pattern matching
- POS-lemma bigram indexing
- Traditional database features (ACID compliance)
- Lower memory footprint

**For Flexibility**:

Use **MongoDB** or **Django Storage** for schema flexibility and web framework integration.

Common storage adapter attributes
=================================

Each storage adapter inherits the following attributes and methods.

.. autoclass:: chatterbot.storage.StorageAdapter
   :members:

Database Migrations
===================

Various frameworks such as Django and SQL Alchemy support
functionality that allows revisions to be made to databases
programmatically. This makes it possible for updates and
revisions to structures in the database to be be applied
in consecutive version releases.

The following explains the included migration process for
each of the databases that ChatterBot comes with support for.

* Django: Full schema migrations and data migrations will
  be included with each release.
* SQL Alchemy: No migrations are currently provided in
  releases. If you require migrations between versions
  `Alembic`_ is the recommended solution for generating them.
* MongoDB: No migrations are provided.
* Redis: No migrations are provided.

Further Reading
===============

.. toctree::
   :maxdepth: 2

   text-search
   create-a-storage-adapter

.. _Alembic: https://alembic.sqlalchemy.org
