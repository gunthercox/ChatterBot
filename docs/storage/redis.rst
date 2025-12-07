Redis Vector Storage Adapter
============================

.. note::

   **(December, 2025)**:
   The ``RedisVectorStorageAdapter`` is new and experimental functionality introduced as a "beta" feature. Its functionality might not yet be fully stable and is subject to change in future releases.

.. meta::
   :description: Redis vector storage for ChatterBot: semantic similarity search, vector embeddings, AI-powered contextual responses with HuggingFace transformers
   :keywords: redis vector database, semantic search, vector embeddings, sentence transformers, AI chatbot, natural language understanding, context-aware responses, vector similarity

.. image:: /_static/Redis_Logo_Red_RGB.svg
   :alt: Redis Logo
   :align: center
   :width: 200
..
    Imaged used in accordance with the Redis Trademark Policy
    https://redis.io/legal/trademark-policy/

The ``RedisVectorStorageAdapter`` enables advanced **semantic similarity search** for ChatterBot using Redis® as a :term:`vector database`.
Unlike traditional keyword-based storage adapters, this adapter uses **vector embeddings** and **cosine similarity** to understand conversational context and find semantically related responses.

**Key Features:**

- **Semantic Understanding**: Matches responses based on meaning, not just keywords
- **Vector Embeddings**: Uses HuggingFace ``sentence-transformers/all-mpnet-base-v2`` model for state-of-the-art text encoding
- **Confidence Scoring**: Returns similarity scores (0.0-1.0) based on vector distance for intelligent response ranking
- **Performance Optimized**: Automatic NoOpTagger eliminates unnecessary spaCy processing overhead
- **Context-Aware Responses**: Finds conversationally appropriate responses even when exact words differ

Vectors are mathematical representations of text (multi-dimensional embeddings) that capture semantic meaning.
The adapter calculates similarity between text by measuring the **cosine distance** between their vector representations,
allowing ChatterBot to understand that "How are you?" is similar to "How's it going?" even with different words.

For example, consider the following words:

.. code-block:: text

            (Speaking)
                ●
               / \
              /   \
    (Poetry) ●-----● (Rhyming)
              \   /
               \ /
                ●
            (Writing)

The acts of "speaking" and "writing" are both forms of communication, so they are included in the same cluster, but they are somewhat opposite to each other. Both "poetry" and "rhyming" closely related, and in some cases might possibly be used as synonyms within the context of either types of speech or types of writing.

Redis Setup
-----------

Before you use the ``RedisVectorStorageAdapter`` you will need to install
the dependencies required for `Redis`_ and generating vectors.
This can be done using the ``chatterbot[redis]`` extra when
installing ChatterBot. For example:

.. code-block:: bash

   pip install chatterbot[redis]

You will also need to have a Redis server running, with the additional
modules installed that enable searching using vectors. And easy way to
run one locally is to use Docker:

.. code-block:: yaml
   :caption: docker-compose.yml

   services:
     redis:
       # Use the latest version of the redis-stack image
       image: redis/redis-stack-server:latest
       # Expose the default Redis port
       ports:
         - "6379:6379"
       # Persist the Redis data
       volumes:
         - ./.database/redis/:/data

To start the Redis container, run:

.. code-block:: bash

   docker compose up -d

Likewise, you can run ``docker compose ps`` to review the status of your container, and ``docker compose down`` to stop it. For more information on Docker and ``docker compose``, see the `Docker Compose documentation`_.

Redis Configuration
-------------------

To use the ``RedisVectorStorageAdapter`` you will need to provide the following argument when configuring your ChatterBot instance:

.. code-block:: python

   from chatterbot import ChatBot

   chatbot = ChatBot(
         'Redis Bot',
         storage_adapter='chatterbot.storage.RedisVectorStorageAdapter',
         # Optional: Override the default Redis URI
         # database_uri='redis://localhost:6379/0'
   )

Storage-Aware Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Redis adapter automatically configures ChatterBot for optimal performance with vector-based search:

- **Automatic Tagger Selection**: Uses ``NoOpTagger`` instead of ``PosLemmaTagger`` to eliminate spaCy model loading overhead
- **Semantic Vector Search**: Automatically selects ``SemanticVectorSearch`` algorithm instead of text-based comparison
- **No Manual Configuration**: These optimizations are applied automatically when using the Redis adapter

This "storage-aware" design means ChatterBot adapts its processing pipeline based on the storage adapter's capabilities,
ensuring maximum performance and accuracy for vector-based semantic search.

.. code-block:: python

   # No need to specify tagger or search algorithm - Redis adapter handles it!
   chatbot = ChatBot(
       'Semantic Bot',
       storage_adapter='chatterbot.storage.RedisVectorStorageAdapter'
   )
   # Automatically uses:
   # - NoOpTagger (no spaCy overhead)
   # - SemanticVectorSearch (vector similarity)
   # - Confidence scores from cosine similarity

Semantic Search vs. Traditional Text Search
-------------------------------------------

The Redis adapter uses **semantic vector search** instead of traditional pattern matching:

.. list-table:: Comparison: Semantic Vector Search vs. Text-Based Search
   :widths: 30 35 35
   :header-rows: 1

   * - Feature
     - Traditional Text Search (SQL)
     - Semantic Vector Search (Redis)
   * - Search Method
     - POS-lemma bigram matching
     - 768-dimensional vector similarity
   * - Context Understanding
     - Structural patterns only
     - Deep semantic meaning
   * - "How are you?" matches "How's it going?"
     - ❌ No (different lemmas)
     - ✅ Yes (similar meaning)
   * - Confidence Scoring
     - Levenshtein distance
     - Cosine similarity (1 - distance/2)
   * - Processing Overhead
     - Requires spaCy models
     - No spaCy needed (NoOpTagger)
   * - Best For
     - Exact pattern matching
     - Conversational AI, context understanding

**Example: Semantic Similarity in Action**

.. code-block:: python

   # These inputs find similar responses despite different words:
   response1 = chatbot.get_response("What's the weather like?")
   response2 = chatbot.get_response("How's the climate today?")
   # Both queries find weather-related responses due to semantic similarity

   # Confidence scores help rank responses:
   # - Vector distance 0.1 → confidence ~0.95 (very similar)
   # - Vector distance 0.5 → confidence ~0.75 (somewhat similar)
   # - Vector distance 1.0 → confidence ~0.50 (loosely related)

Class Attributes
----------------

.. autoclass:: chatterbot.storage.RedisVectorStorageAdapter
   :members:

Performance Considerations
--------------------------

**Vector Embedding Model**: By default, the Redis adapter uses ``sentence-transformers/all-mpnet-base-v2`` from HuggingFace:

- **Dimensions**: 768-dimensional embeddings
- **Model Size**: ~420MB (downloaded once, cached locally)
- **Performance**: ~2000 sentences/second on CPU
- **Quality**: State-of-the-art semantic similarity (as of 2025)

**First-Time Setup**: The embedding model downloads automatically on first use:

.. code-block:: python

   # First initialization downloads model (~420MB)
   chatbot = ChatBot('Bot', storage_adapter='chatterbot.storage.RedisVectorStorageAdapter')
   # Subsequent uses load from cache (fast startup)

**Memory Usage**: Redis vector storage requires more memory than SQL due to embedding storage:

- Each statement: ~3KB (768 floats × 4 bytes)
- 10,000 statements: ~30MB vector data
- Trade-off: Higher memory for better semantic understanding

More on Vector Databases & Semantic Search
-------------------------------------------

For those looking to learn more about vector databases, vector embeddings, and semantic search in AI applications:

.. list-table:: Vector Database & AI Learning Resources
   :widths: 50 50
   :header-rows: 1

   * - Topic
     - Resource Link
   * - What is a vector database?
     - https://www.mongodb.com/resources/basics/databases/vector-databases
   * - Why use a vector database?
     - https://stackoverflow.blog/2023/09/20/do-you-need-a-specialized-vector-database-to-implement-vector-search-well/
   * - How to choose a vector database?
     - https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search-ai
   * - Redis as a vector database
     - https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/
   * - Sentence Transformers (Embeddings)
     - https://www.sbert.net/
   * - Understanding Cosine Similarity
     - https://en.wikipedia.org/wiki/Cosine_similarity
   * - Vector Search for AI/LLMs
     - https://www.pinecone.io/learn/vector-search-basics/


:sub:`* Redis is a registered trademark of Redis Ltd. Any rights therein are reserved to Redis Ltd.`


.. _Redis: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/
.. _Docker Compose documentation: https://docs.docker.com/compose/
