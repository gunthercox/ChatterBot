.. meta::
   :description: ChatterBot documentation: Python machine learning chatbot library with semantic vector search, AI conversational dialog engine supporting multiple languages and vector databases
   :keywords: ChatterBot, chatbot, chat, bot, natural language processing, nlp, artificial intelligence, ai, machine learning, vector database, semantic search, vector embeddings, conversational ai, python chatbot library

.. container:: banner

   .. image:: ../graphics/banner.png
      :alt: ChatterBot Banner
      :align: center

About ChatterBot
================

ChatterBot is a Python library that makes it easy to generate automated
responses to a user's input. ChatterBot uses a selection of machine learning
algorithms to produce different types of responses. This makes it easy for
developers to create chat bots and automate conversations with users.

**Modern AI Capabilities** (2025):

- **Semantic Vector Search**: Advanced context understanding using vector embeddings and Redis vector database
- **Large Language Model (LLM) Integration**: Direct support for Ollama and OpenAI models (in development)
- **Storage-Aware Architecture**: Automatic optimization based on storage backend capabilities
- **Multi-Language Support**: Language-independent design with spaCy integration

For more details about the ideas and concepts behind ChatterBot see the
:ref:`process flow diagram <process_flow_diagram>`.

An example of typical input would be something like this:

.. code-block:: text

   user: Good morning! How are you doing?
   bot:  I am doing very well, thank you for asking.
   user: You're welcome.
   bot:  Do you like hats?

Originally, ChatterBot was created as a part of the codebase for the humanoid robot `Salvius`_. As the project grew, the :code:`chatterbot` library was released as a separate open-source project.

Language Independence
---------------------

The language independent design of ChatterBot allows it to be trained to speak any language.
Additionally, the machine-learning nature of ChatterBot allows an agent instance to improve
it's own knowledge of possible responses as it interacts with humans and other sources of informative data.

.. note::

   Starting in version 1.2.0 ChatterBot has started to implement some features that are
   language specific. This change is being made to improve the quality of responses that
   ChatterBot can generate.

How ChatterBot Works
--------------------

ChatterBot is a Python library designed to make it easy to create software that can engage in conversation.

An :term:`untrained instance` of ChatterBot starts off with no knowledge of how to communicate.
Each time a user enters a :term:`statement`, the library saves the text that they entered and the text
that the statement was in response to. As ChatterBot receives more input the number of responses
that it can reply to, and the accuracy of each response in relation to the input statement increases.

The program selects the closest matching :term:`response` by searching for the closest matching known
statement that matches the input, it then chooses a response from the selection of known responses
to that statement.

.. admonition:: April 2025

   The dialog processing flow will be slightly different when using
   large language models (LLMs). See the :ref:`LLM Roadmap` for more details.

..  _process_flow_diagram:

Process flow diagram
--------------------

.. image:: _static/chatterbot-process-flow.svg
   :alt: ChatterBot process flow diagram

Contents:
---------

.. toctree::
   :maxdepth: 4

   About <self>
   setup
   quickstart
   tutorial
   examples
   training
   preprocessors
   logic/index
   storage/index
   large-language-models
   filters
   chatterbot
   conversations
   comparisons
   utils
   corpus
   django/index
   faq
   commands
   development
   glossary

Report an Issue
---------------

Please direct all bug reports and feature requests to the project's issue
tracker on `GitHub`_.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Sponsors
--------

ChatterBot is sponsored by:

.. raw:: html

   <div style="font-size:21px; color:black; text-align: center;">Browser testing via 
      <a href="https://www.lambdatest.com/?utm_source=chatterbot&utm_medium=sponsor" target="_blank">
         <img src="https://www.lambdatest.com/blue-logo.png" style="vertical-align: middle;" width="250" height="45" />
      </a>
   </div>

   <p>
      If you, or your organization is interested in sponsoring the ChatterBot project, you can do so directly via <a href="https://github.com/sponsors/gunthercox">GitHub Sponsors</a> as well as reach out directly via <code>community@chatterbot.us</code> for more information and to discuss sponsorship opportunities.
   </p>

.. _GitHub: https://github.com/gunthercox/ChatterBot/issues/
.. _Salvius: https://salvius.org
