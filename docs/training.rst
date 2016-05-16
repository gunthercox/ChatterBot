========
Training
========

ChatterBot has tools that simplify the process of training a bot instance.
These tools range from simple utility methods that update relations of known
statements, to a corpus of pre-loaded training data that you can use.

Training via list data
======================

For the training, process, you will need to pass in a list of statements where the order of each statement is based on it's placement in a given conversation.

For example, if you were to run bot of the following training calls, then the resulting chatterbot would respond to both statements of "Hi there!" and "Greetings!" by saying "Hello".

.. code-block:: python

   from chatterbot.training.trainers import ListTrainer

   chatterbot = ChatBot("Training Example")
   chatterbot.set_trainer(ListTrainer)

   chatterbot.train([
       "Hi there!",
       "Hello",
   ])

   chatterbot.train([
       "Greetings!",
       "Hello",
   ])

You can also provide longer lists of training conversations.
This will establish each item in the list as a possible response to it's predecessor in the list.

.. code-block:: python

   chatterbot.train([
       "How are you?",
       "I am good.",
       "That is good to hear.",
       "Thank you",
       "You are welcome.",
   ])

Training with corpus data
=========================

ChatterBot comes with a corpus data and utility module that makes it easy to
quickly train your bot to communicate. To do so, simply specify the corpus
data modules you want to use.

.. code-block:: python

   from chatterbot.training.trainers import ChatterBotCorpusTrainer

   chatterbot = ChatBot("Training Example")
   chatterbot.set_trainer(ChatterBotCorpusTrainer)

   chatterbot.train(
       "chatterbot.corpus.english"
   )

Specifying corpus scope
-----------------------

It is also possible to import individual subsets of ChatterBot's at once.
For example, if you only wish to train based on the english greetings and
conversations corpora then you would simply specify them.

.. code-block:: python

   chatterbot.train(
       "chatterbot.corpus.english.greetings",
       "chatterbot.corpus.english.conversations"
   )

Creating a new training class
=============================

You can create a new trainer to train your chat bot from your own
data files. You may choose to do this if you want to train your
chat bot from a data source in a format that is not directly supported
by ChatterBot.

Your custom trainer should `chatterbot.training.trainers.Trainer` class.
Your trainer will need to have a method named `train`, that can take any
parameters you choose.

Take a look at the existing `trainer classes on GitHub`_ for examples.

The ChatterBot Corpus
=====================

This is a :term:`corpus` of data that is included in the chatterbot module.

Corpus language availability
----------------------------

Corpus data is user contributed, but it is also not difficult to create one if you are familiar with the language.
This is because each corpus is just a sample of various input statements and their responses for the bot to train itself with.

To explore what languages and sets of corpora are available, check out the `chatterbot/corpus/data`_ directory in the repository.

If you are interested in contributing a new language corpus, or adding a module to an existing language, please create a pull request. Contributions are welcomed!

.. glossary::

   corpus
      In linguistics, a corpus (plural corpora) or text corpus is a large
      and structured set of texts. They are used to do statistical analysis
      and hypothesis testing, checking occurrences or validating linguistic
      rules within a specific language territory [1]_.

.. [1] https://en.wikipedia.org/wiki/Text_corpus

.. _chatterbot/corpus/data: https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/corpus
.. _`trainer classes on GitHub`: https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/training
