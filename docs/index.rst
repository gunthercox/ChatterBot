Welcome to ChatterBot's documentation!
======================================

.. image:: ../graphics/banner.png

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   tutorial
   examples
   training
   adapters/index
   chatterbot
   conversations
   utils

About ChatterBot
================

ChatterBot is a Python library that makes it easy to generate automated
responses to a user's input. ChatterBot uses a selection of machine learning
algorithms to produce different types of responces. This makes it easy for
developers to create chat bots and automate conversations with users.

An example of typical input would be something like this:

| **user:** Good morning! How are you doing?  
| **bot:**  I am doing very well, thank you for asking.  
| **user:** You're welcome.  
| **bot:** Do you like hats?  

How it works
============

An untrained instance of ChatterBot starts off with no knowledge of how to communicate. Each time a user enters a statement, the library saves the text that they entered and the text that the statement was in response to. As ChatterBot receives more input the number of responses that it can reply and the accuracy of each response in relation to the input statement increase. The program selects the closest matching response by searching for the closest matching known statement that matches the input, it then returns the most likely response to that statement based on how frequently each response is issued by the people the bot communicates with.

Simple Example
==============

.. literalinclude:: ../examples/basic_example.py
   :language: python

Training
========

ChatterBot comes with a data utility module that can be used to train chat bots.
Lists of statements representing conversations can also be used for training.
More information is available in the :ref:`training documentation <set_trainer>`

Language Independence
=====================

The language independent design of ChatterBot allows it to be trained to speak any language.
Additionally, the machine-learning nature of ChatterBot allows an agent instance to improve
it's own knowledge of possible responses as it interacts with humans and other sources of informative data.

Report an Issue
===============

Please direct all bug reports and feature requests to the project's issue
tracker on `GitHub`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GitHub: https://github.com/gunthercox/ChatterBot
