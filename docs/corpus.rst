ChatterBot Corpus
=================

This is a :term:`corpus` of dialog data that is included in the chatterbot module.

Additional information about the ``chatterbot-corpus`` module can be found
in the `ChatterBot Corpus Documentation`_.

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

   The ``chatterbot-corpus`` is distributed in its own Python package so that it can
   be released and upgraded independently from the ``chatterbot`` package.


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
.. _ChatterBot Corpus Documentation: http://chatterbot-corpus.readthedocs.io/
