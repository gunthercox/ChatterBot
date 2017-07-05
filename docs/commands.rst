==================
Command line tools
==================

ChatterBot comes with a few command line tools that can help

Get the installed ChatterBot version
====================================

If have ChatterBot installed and you want to check what version
you have then you can run the following command.

.. code-block:: bash

   python -m chatterbot --version

Locate NLTK data
=================

ChatterBot uses the Natural Language Toolkit (NLTK) for various
language processing functions. ChatterBot downloads additional
data that is required by NLTK. The following command can be used
to find all NLTK data directories that contain files.

.. code-block:: bash

   python -m chatterbot list_nltk_data
