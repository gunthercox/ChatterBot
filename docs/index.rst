.. image:: ../graphics/banner.png

About ChatterBot
================

ChatterBot is a Python library that makes it easy to generate automated
responses to a user's input. ChatterBot uses a selection of machine learning
algorithms to produce different types of responces. This makes it easy for
developers to create chat bots and automate conversations with users.
For more details about the ideas and concepts behind ChatterBot see the :ref:`process flow diagram <process_flow_diagram>`.

An example of typical input would be something like this:

| **user:** Good morning! How are you doing?  
| **bot:**  I am doing very well, thank you for asking.  
| **user:** You're welcome.  
| **bot:** Do you like hats?  

Simple Example
==============

.. literalinclude:: ../examples/basic_example.py
   :language: python

Language Independence
=====================

The language independent design of ChatterBot allows it to be trained to speak any language.
Additionally, the machine-learning nature of ChatterBot allows an agent instance to improve
it's own knowledge of possible responses as it interacts with humans and other sources of informative data.

Training
========

ChatterBot comes with a data utility module that can be used to train chat bots.
Lists of statements representing conversations can also be used for training.
More information is available in the :ref:`training documentation <set_trainer>`

Report an Issue
===============

Please direct all bug reports and feature requests to the project's issue
tracker on `GitHub`_.

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   tutorial
   examples
   training
   adapters/index
   filters/index
   chatterbot
   conversations
   utils
   about
   django/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _GitHub: https://github.com/gunthercox/ChatterBot/issues/
