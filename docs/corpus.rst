ChatterBot Corpus
=================

This is a :term:`corpus` of dialog data that is included in the chatterbot module.

Corpus language availability
----------------------------

Corpus data is user contributed, but it is also not difficult to create one if you are familiar with the language.
This is because each corpus is just a sample of various input statements and their responses for the bot to train itself with.

To explore what languages and sets of corpora are available, check out the `chatterbot/corpus/data`_ directory in the repository.

.. note::
   If you are interested in contributing a new language corpus, or adding content to an existing language in the corpus,
   please feel free to submit a pull request on ChatterBot's GitHub page. Contributions are welcomed!


Exporting your chat bot's database as a training corpus
=======================================================

Now that you have created your chat bot and sent it out into the world, perhaps
you are looking for a way to share what it has learned with other chat bots?
ChatterBot's training module provides methods that allow you to export the
content of your chat bot's database as a training corpus that can be used to
train other chat bots.

Here is an example:

.. code-block:: python

   chatbot = ChatBot("Export Example Bot")
   chatbot.trainer.export_for_training('./export.json')

.. glossary::

   corpus
      In linguistics, a corpus (plural corpora) or text corpus is a large
      and structured set of texts. They are used to do statistical analysis
      and hypothesis testing, checking occurrences or validating linguistic
      rules within a specific language territory [1]_.

.. [1] https://en.wikipedia.org/wiki/Text_corpus

.. _chatterbot/corpus/data: https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/corpus
