=====================
Large Language Models
=====================

.. warning::

    Starting in ChatterBot 1.2.7 experimental support for :term:`large language models`
    is being added. This support is not yet complete and is not yet ready for
    general use beyond experimental purposes. The API will likely change in the
    future and the functionality may not be fully implemented.

LLM Roadmap
===========

The following phases of development are the general roadmap for LLM support
in ChatterBot. The goal is to provide a simple and consistent interface for
LLM integration, and to make it easy to add support for new LLMs as they
become available.

.. note::
    * Added April 1st, 2025
    * Last updated: April 6th, 2025

**Phase 1:**

Support for local and remote LLMs.

1. ☑ Support for Ollama LLMs, which at the current time appear to be the easiest to set up and run on local hardware.
2. ☑ Support for accessing LLMs that use the OpenAI API.

**Phase 2:**

* ☐ Streaming response support across features in ChatterBot.

**Phase 3:**

LLM integration with specific logic adapter features via :term:`RAG` or similar approach.

* ☐ Mathematical operations :class:`~chatterbot.logic.MathematicalEvaluation` via :mod:`mathparse`
* ☐ Date and time :class:`~chatterbot.logic.TimeLogicAdapter`
* ☐ Unit conversion ``UnitConversion``

One of the concepts / theories here that we want to evaluate is, for example,
that it may be easier (and more efficient) to teach AI to use a calculator
than it is to teach it the rules of mathematics. Whether this is because it
lets us use smaller LLMs that don't have a strong understanding of math, or
because in general it allows us to offload processing of other complex tasks,
there is likely a strong use case here.

Both interestingly and conveniently, ChatterBot's existing architecture used
for its logic adapters is already very similar to approaches used to provide
additional tools to LLMs. The Model Context Protocol (:term:`MCP`) supported by a
`range of MCP server implementations <https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file#what-is-mcp>`_
currently seems like a strong candidate for this.

.. list-table:: Comparison of ChatterBot Architectures
   :class: table-justified
   :header-rows: 1

   * - Classic ChatterBot (Logic Adapters)
     - LLM with MCP
   * - .. image:: _static/dialog-processing-flow.svg
     - .. image:: _static/dialog-processing-flow-llm.svg

The choice to enforce one LLM per chat bot instance is currently based on the
notion that one capable model per chat bot is likely simpler and more efficient
than trying to reconcile the output of multiple models.

**Phase 4:**

* ☐ LLM integration with the ChatterBot training process

The ideal outcome for this phase would be the ability to use the existing training
pipelines to fine-tune LLMs. It isn't clear yet if this will be possible to do with
common hardware, but right now this is the goal. An alternative may be to use a RAG
approach to allow the LLM to access the chat bot's database when generating responses.

Ollama Support
==============

ChatterBot's experimental support for using Ollama LLMs can be tested using the following setup:

1. Have Docker installed and running
2. Install ChatterBot and the Ollama client library
3. Use the following ``docker-compose`` file to run the Ollama server:

.. code-block:: yaml
   :caption: docker-compose.yml

   services:

    # NOTE: This setup is for AMD GPUs
    ollama:
        image: ollama/ollama:rocm
        ports:
        - "11434:11434"
        volumes:
        - ./.database/ollama:/root/.ollama
        devices:
        - /dev/kfd
        - /dev/dri

The following commands can be used to download various Ollama models:

.. code-block:: bash

    docker compose up -d

.. code-block:: bash

    # Create a shell in the docker container
    docker compose exec ollama bash

    # Download and run the Gemma 3 model
    ollama run gemma3:1b


* More notes on the ``ollama`` container: https://hub.docker.com/r/ollama/ollama
* Ollama model library: https://ollama.com/library

The following is an example of how to use the Ollama LLM in ChatterBot. Before running
them you will need to install the ``ollama`` client library. This can be done directly
using pip or by using the extra option from the ChatterBot package that includes it:

.. code-block:: bash

    pip install chatterbot[dev]

.. literalinclude:: ../examples/ollama_example.py
   :caption: examples/ollama_example.py
   :language: python

Using the OpenAI client
=======================

The following is an example of how to use the OpenAI client in ChatterBot. Before running
the example you will need to install the ``openai`` client library. This can be done directly
using pip or by using the extra option from the ChatterBot package that includes it:

.. code-block:: bash

    pip install chatterbot[dev] python-dotenv

1. Obtain an OpenAI API key: https://platform.openai.com/settings/organization/api-keys
2. Create a ``.env`` file to hold your API key in the parent directory from where your code is running.

.. code-block:: bash
    :caption: ../.env

    OPENAI_API_KEY="API Key Here"

.. literalinclude:: ../examples/openai_example.py
   :caption: examples/openai_example.py
   :language: python
