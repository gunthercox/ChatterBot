=====================
Large Language Models
=====================

.. warning::

    Starting in ChatterBot 1.2.7 experimental support for :term:`large language models`
    is being added. This support is not yet complete and is not yet ready for general
    use beyond experimental purposes. The API will likely change in the future and the
    functionality may not be fully implemented.

.. warning::

    **Do not deploy LLM-enabled ChatterBot applications in production without:**

    * Comprehensive security review and hardening
    * Enabling security scanning (see :doc:`security`)
    * Additional rate limiting and abuse prevention
    * Monitoring and alerting for security violations
    * Understanding of OWASP Top 10 for LLM Applications
    * Regular security audits and penetration testing

    The API may change in future releases as LLM support matures.

    **Security Considerations:**

    LLM applications are vulnerable to prompt injection, jailbreaking, and other
    attacks. ChatterBot provides optional security scanning via llm-guard (see
    :doc:`security`), but this is a baseline defense and not sufficient for
    production deployment without additional hardening.

    Review the `OWASP Top 10 for LLM Applications <https://owasp.org/www-project-top-10-for-large-language-model-applications/>`_
    before deploying any LLM-enabled application.

LLM Roadmap
===========

The following phases of development are the general roadmap for LLM support
in ChatterBot. The goal is to provide a simple and consistent interface for
LLM integration, and to make it easy to add support for new LLMs as they
become available.

.. note::
    * Added April 1st, 2025
    * Last updated: February 2nd, 2026

**Phase 1:**

Support for local and remote LLMs.

1. ☑ Support for `Ollama LLMs`_, which at the current time appear to be the easiest to set up and run on local hardware.
2. ☑ Support for accessing LLMs that use the OpenAI API.

**Phase 2:**

* ☐ Streaming response support across features in ChatterBot.

.. note::
    This functionality is being skipped for now, but may be reprioritized in the future.
    This would be more important to implement if streaming inputs, eg. text from streaming
    audio or video sources were being supported (which is not currently something this
    project aims to address, nor do most LLMs support).

**Phase 3:**

LLM integration with specific logic adapter features via MCP tool calling.

* ☑ Mathematical operations :class:`~chatterbot.logic.MathematicalEvaluation` via :mod:`mathparse`
* ☑ Date and time :class:`~chatterbot.logic.TimeLogicAdapter`
* ☑ Unit conversion ``UnitConversion``

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

Phase 3 has been implemented using the MCP tool format to allow LLMs to invoke
logic adapters as tools.

The implementation supports:

* **Native tool calling** for models that support it (Ollama llama3.1+, mistral, qwen2.5; all OpenAI models)
* **Prompt-based fallback** for models without native tool support using structured JSON
* **Hybrid configurations** where LLM adapters work alongside traditional logic adapters in consensus voting

.. list-table:: Comparison of ChatterBot Architectures
   :class: table-justified
   :header-rows: 1

   * - Classic ChatterBot (Logic Adapters)
     - LLM with MCP
   * - .. image:: _static/dialog-processing-flow.svg
     - .. image:: _static/dialog-processing-flow-llm.svg

LLM adapters now participate in ChatterBot's consensus voting mechanism alongside
traditional logic adapters. This allows multiple adapters (LLM and non-LLM) to
"vote" on the best response, with the highest confidence response winning.

Basic LLM Configuration
------------------------

.. code-block:: python

    from chatterbot import ChatBot

    bot = ChatBot(
        'My Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.OllamaLogicAdapter',
                'model': 'llama3.1',
                'host': 'http://localhost:11434'
            }
        ]
    )

LLM with Tool Support
---------------------

Enable specialized tools by passing logic adapters in the ``logic_adapters_as_tools`` parameter:

.. code-block:: python

    bot = ChatBot(
        'My Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.OllamaLogicAdapter',
                'model': 'llama3.1',
                'logic_adapters_as_tools': [
                    'chatterbot.logic.MathematicalEvaluation',
                    'chatterbot.logic.TimeLogicAdapter',
                    'chatterbot.logic.UnitConversion'
                ]
            }
        ]
    )

When a tool-capable model is used (e.g., llama3.1, mistral, qwen2.5, or any OpenAI model),
the LLM will be able to invoke these tools using native function calling. For models without
native support, the adapter automatically falls back to prompt-based tool calling.

Hybrid Configuration
--------------------

Combine LLM adapters with traditional logic adapters for consensus voting:

.. code-block:: python

    bot = ChatBot(
        'My Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.OllamaLogicAdapter',
                'model': 'llama3.1',
                'logic_adapters_as_tools': [
                    'chatterbot.logic.MathematicalEvaluation',
                    'chatterbot.logic.TimeLogicAdapter'
                ],
                'min_confidence': 0.6,
                'max_confidence': 0.9
            },
            'chatterbot.logic.BestMatch',
            'chatterbot.logic.SpecificResponseAdapter'
        ]
    )

In this configuration, the LLM adapter votes alongside BestMatch and SpecificResponseAdapter,
with the highest confidence response being selected. The ``min_confidence`` and ``max_confidence``
parameters control the LLM's confidence range for voting purposes.

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


.. _`Ollama LLMs`: https://ollama.com/library?sort=popular
