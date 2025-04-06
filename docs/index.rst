.. meta::
   :description: ChatterBot documentation: ChatterBot is a machine learning, conversational dialog engine designed to support multiple languages.
   :keywords: ChatterBot, chatbot, chat, bot, natural language processing, nlp, artificial intelligence, ai

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
that it can reply and the accuracy of each response in relation to the input statement increase.

The program selects the closest matching :term:`response` by searching for the closest matching known
statement that matches the input, it then chooses a response from the selection of known responses
to that statement.

..  _process_flow_diagram:

Process flow diagram
--------------------

.. image:: _static/chatterbot-process-flow.svg
   :alt: ChatterBot process flow diagram

Contents:
---------

.. toctree::
   :maxdepth: 4

   setup
   quickstart
   tutorial
   examples
   training
   preprocessors
   logic/index
   storage/index
   filters
   chatterbot
   conversations
   large-language-models
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

.. _GitHub: https://github.com/gunthercox/ChatterBot/issues/
.. _Salvius: https://salvius.org
