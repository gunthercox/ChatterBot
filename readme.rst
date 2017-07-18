.. figure:: http://i.imgur.com/b3SCmGT.png
   :alt: Chatterbot: Machine learning in Python

   Chatterbot: Machine learning in Python

ChatterBot
==========

ChatterBot is a machine-learning based conversational dialog engine
build in Python which makes it possible to generate responses based on
collections of known conversations. The language independent design of
ChatterBot allows it to be trained to speak any language.

|Package Version| |Requirements Status| |Build Status| |Documentation
Status| |Coverage Status| |Code Climate| |Join the chat at
https://gitter.im/chatter\_bot/Lobby|

An example of typical input would be something like this:

    | **user:** Good morning! How are you doing?
    | **bot:** I am doing very well, thank you for asking.
    | **user:** You’re welcome.
    | **bot:** Do you like hats?

How it works
------------

An untrained instance of ChatterBot starts off with no knowledge of how
to communicate. Each time a user enters a statement, the library saves
the text that they entered and the text that the statement was in
response to. As ChatterBot receives more input the number of responses
that it can reply and the accuracy of each response in relation to the
input statement increase. The program selects the closest matching
response by searching for the closest matching known statement that
matches the input, it then returns the most likely response to that
statement based on how frequently each response is issued by the people
the bot communicates with.

Installation
------------

This package can be installed from `PyPi`_ by running:

::

    pip install chatterbot

Basic Usage
-----------

::

    from chatterbot import ChatBot

    chatbot = ChatBot(
        'Ron Obvious',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

    # Get a response to an input statement
    chatbot.get_response("Hello, how are you today?")

Training data
=============

Chatterbot comes with a data utility module that can be used to train
chat bots. At the moment there is three languages, English, Spanish and
Portuguese training data in this module. Contributions of ad

.. _PyPi: https://pypi.python.org/pypi/ChatterBot

.. |Package Version| image:: https://img.shields.io/pypi/v/chatterbot.svg
   :target: https://pypi.python.org/pypi/chatterbot/
.. |Requirements Status| image:: https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master
   :target: https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master
.. |Build Status| image:: https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master
   :target: https://travis-ci.org/gunthercox/ChatterBot
.. |Documentation Status| image:: https://readthedocs.org/projects/chatterbot/badge/?version=stable
   :target: http://chatterbot.readthedocs.io/en/stable/?badge=stable
.. |Coverage Status| image:: https://img.shields.io/coveralls/gunthercox/ChatterBot.svg
   :target: https://coveralls.io/r/gunthercox/ChatterBot
.. |Code Climate| image:: https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg
   :target: https://codeclimate.com/github/gunthercox/ChatterBot
.. |Join the chat at https://gitter.im/chatter\_bot/Lobby| image:: https://badges.gitter.im/chatter_bot/Lobby.svg
   :target: https://gitter.im/chatter_bot/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge