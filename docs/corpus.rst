ChatterBot Corpus
=================

This is a :term:`corpus` of dialog data that is included in the chatterbot module.

Corpus language availability
----------------------------

Corpus data is user contributed, but it is also not difficult to create one if you are familiar with the language.
This is because each corpus is just a sample of various input statements and their responses for the bot to train itself with.

To explore what languages and collections of corpora are available,
check out the `chatterbot_corpus/data`_ directory in the separate chatterbot-corpus repository.

.. note::
   If you are interested in contributing content to the corpus, please feel free to
   submit a pull request on ChatterBot's corpus GitHub page. Contributions are welcomed!

   https://github.com/gunthercox/chatterbot-corpus

   The :code:`chatterbot-corpus` is distributed in its own Python package so that it can
   be released and upgraded independently from the :code:`chatterbot` package.


Data Format
-----------

The data file contained in ChatterBot Corpus is formatted using `YAML`_ syntax.
This format is used because it is easily readable by both humans and machines.

.. list-table:: Corpus Properties
   :widths: 15 10 30
   :header-rows: 1

   * - Property
     - Required
     - Description
   * - categories
     - Required
     - A list of categories that describe the conversations.
   * - conversations
     - Optional
     - A list of conversations. Each conversation is denoted as a list.

Here is an example of the corpus data:

.. code-block:: yaml
   :name: corpus-example.yml

   categories:
   - english
   - greetings
   conversations:
   - - Hello
     - Hi
   - - Hello
     - Hi, how are you?
     - I am doing well.
   - - Good day to you sir!
     - Why thank you.
   - - Hi, How is it going?
     - It's going good, your self?
     - Mighty fine, thank you.

The values in this example have the following relationships.

.. list-table:: Evaluated statement relationships
   :widths: 15 40
   :header-rows: 1

   * - Statement
     - Response
   * - Hello
     - Hi
   * - Hello
     - Hi, how are you?
   * - Hi, how are you?
     - I am doing well.
   * - Good day to you sir!
     - Why thank you.
   * - Hi, How is it going?
     - It's going good, your self?
   * - It's going good, your self?
     - Mighty fine, thank you.


Exporting your chat bot's database as a training corpus
-------------------------------------------------------

Now that you have created your chat bot and sent it out into the world, perhaps
you are looking for a way to share what it has learned with other chat bots?
ChatterBot's training module provides methods that allow you to export the
content of your chat bot's database as a training corpus that can be used to
train other chat bots.

.. code-block:: python

   chatbot = ChatBot('Export Example Bot')
   chatbot.trainer.export_for_training('./export.yml')

Here is an example:

.. literalinclude:: ../examples/export_example.py
   :language: python

.. _chatterbot_corpus/data: https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data
.. _YAML: http://www.yaml.org/
