=============
Preprocessors
=============

ChatterBot's preprocessors are simple functions that modify the input statement
that a chat bot receives before the statement gets processed by the logic adaper.

Here is an example of how to set preprocessors. The :code:`preprocessors`
parameter should be a list strings of the import paths to your preprocessors.

.. code-block:: python

   chatbot = ChatBot(
       'Bob the Bot',
       preprocessors=[
           'chatterbot.preprocessors.clean_whitespace'
       ]
   )

Preprocessor functions
======================

ChatterBot comes with several preprocessors build in.

.. autofunction:: chatterbot.preprocessors.clean_whitespace

.. autofunction:: chatterbot.preprocessors.unescape_html


Creating new preprocessors
==========================

It is simple to create your own preprocessors. A preprocessor is just a function
with a few requirements.

1. It must take two parameters, the first is a :code:`ChatBot` instance, the second is a :code:`Statement` instance.
2. It must return a statement instance.
