========
Training
========

ChatterBot has tools that simplify the process of training a chat bot instance.
ChatterBot's training process works by creating or building upon the graph data structure that represents the sets of
known statements and responses. When a chat bot trainer is provided with a data set, it creates the necessary entries
in the chat bot's knowledge graph so that the statement inputs and responses are correctly represented.

Several trainers come built-in with ChaterBot. These utilities range from allowing you to update the knowledge graph
based on a list of statements representing a conversation, to tools that allow you to train your bot based on a corpus
of pre-loaded training data.

The case that someone wants to create a custom training module typically comes up when they have data in some format that they want to train the bot with.

..  _set_trainer:


Setting the training class
==========================

ChatterBot comes with training classes built in, or you can create your own
if needed. To use a training class you must import it and pass it to
the `set_trainer()` method before calling `train()`.


Training via list data
======================

.. autofunction:: chatterbot.trainers.ListTrainer

For the training, process, you will need to pass in a list of statements where the order of each statement is based on it's placement in a given conversation.

For example, if you were to run bot of the following training calls, then the resulting chatterbot would respond to both statements of "Hi there!" and "Greetings!" by saying "Hello".

.. code-block:: python

   from chatterbot.trainers import ListTrainer

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

.. autofunction:: chatterbot.trainers.ChatterBotCorpusTrainer

ChatterBot comes with a corpus data and utility module that makes it easy to
quickly train your bot to communicate. To do so, simply specify the corpus
data modules you want to use.

.. code-block:: python

   from chatterbot.trainers import ChatterBotCorpusTrainer

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


Training with the Twitter API
=============================

.. autofunction:: chatterbot.trainers.TwitterTrainer

Create an new app using you twiter acccount. Once created,
it will provide you with the following credentails that are
required to work with the Twitter API.

+-------------------------------------+-------------------------------------+
| Parameter                           | Description                         | 
+=====================================+=====================================+
| :code:`twitter_consumer_key`        | Consumer key of twitter app.        |
+-------------------------------------+-------------------------------------+
| :code:`twitter_consumer_secret`     | Consumer secret of twitter app.     | 
+-------------------------------------+-------------------------------------+
| :code:`twitter_access_token_key`    | Access token key of twitter app.    | 
+-------------------------------------+-------------------------------------+
| :code:`twitter_access_token_secret` | Access token secret of twitter app. | 
+-------------------------------------+-------------------------------------+

Twitter training example
------------------------

.. literalinclude:: ../examples/twitter_training_example.py
   :language: python


Training with the Ubuntu dialog corpus
======================================

.. autofunction:: chatterbot.trainers.UbuntuCorpusTrainer

This training class makes it possible to train your chat bot using the Ubuntu
dialog corpus. Becaue of the file size of the Ubuntu dialog corpus, the download
and training process may take a considerable amount of time.

This training class will handle the process of downloading the compressed corpus
file and extracting it. If the file has already been downloaded, it will not be
downloaded again. If the file is already extracted, it will not be extracted again.


Creating a new training class
=============================

You can create a new trainer to train your chat bot from your own
data files. You may choose to do this if you want to train your
chat bot from a data source in a format that is not directly supported
by ChatterBot.

Your custom trainer should inherit `chatterbot.trainers.Trainer` class.
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
.. _`trainer classes on GitHub`: https://github.com/gunthercox/ChatterBot/blob/master/chatterbot/trainers.py
