==========================
Frequently Asked Questions
==========================

This document is comprised of questions that are frequently
asked about ChatterBot and chat bots in general.

.. toctree::
   :maxdepth: 2

   encoding

How do I deploy my chat bot to the web?
---------------------------------------

There are a number of excellent web frameworks for creating
Python projects out there. Django and Flask are two excellent
examples of these. ChatterBot is designed to be agnostic to
the platform it is deployed on and it is very easy to get set up.

To run ChatterBot inside of a web application you just need a way
for your application to receive incoming data and to return data.
You can do this any way you want, HTTP requests, web sockets, etc.

There are a number of existing examples that show how to do this.

1. An example using Django: https://github.com/gunthercox/ChatterBot/tree/master/examples/django_app
2. An example using Flask: https://github.com/chamkank/flask-chatterbot/blob/master/app.py

Additional details and recommendations for configuring Django can be found
in the :ref:`Webservices` section of ChatterBot's Django documentation.

What kinds of machine learning does ChatterBot use?
---------------------------------------------------

In brief, ChatterBot uses a number of different machine learning techniques to
generate its responses. The specific algorithms depend on how the chat bot is
used and the settings that it is configured with.

Here is a general overview of some of the various machine learning techniques
that are employed throughout ChatterBot's codebase.

1. Search algorithms
++++++++++++++++++++

Searching is the most rudimentary form of artificial intelligence. To be fair,
there are differences between machine learning and artificial intelligence but
lets avoid those for now and instead focus on the topic of algorithms that make
the chat bot talk intelligently.

Search is a crucial part of how a chat bot quickly and efficiently retrieves
the possible candidate statements that it can respond with.

Some examples of attributes that help the chat bot select a response include

- the similarity of an input statement to known statements
- the frequency in which similar known responses occur
- the likeliness of an input statement to fit into a category that known statements are a part of

2. Classification algorithms
++++++++++++++++++++++++++++

Several logic adapters in ChatterBot use `naive Bayesian classification`_
algorithms to determine if an input statement meets a particular set of
criteria that warrant a response to be generated from that logic adapter.

.. _naive Bayesian classification: https://en.wikipedia.org/wiki/Naive_Bayes_classifier
