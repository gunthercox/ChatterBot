==========================
Contributing to ChatterBot
==========================

There are numerous ways to contriubte to ChatterBot. All of which are highly encouraged.

- Contributing bug reports and feature requests

- Contributing documentation

- Contributing code for new features

- Contributing fixes for bugs

Every bit of help received on this project is highly appreciated.


Setting Up a Development Environment
====================================

To contribute to ChatterBot's development, you simply need:

- Python

- pip

- A few python packages: 

.. code-block:: bash

   pip install requirements.txt
   pip install dev-requirements.txt

- A text editor


Reporting a Bug
===============

If you discover a bug in ChatterBot and wish to report it, please be
sure that you adhere to the following when you report it on GitHub.

1. Before creating a new bug report, please search to see if an open or closed report matching yours already exists.
2. Please include a description that will allow others to recreate the problem you encountered.


Requesting New Features
=======================

When requesting a new feature in ChatterBot, please make sure to include
the following details in your request.

1. Your use case. Describe what you are doing that requires this new functionality.


Contributing Documentation
==========================

ChatterBot's documentation is written in reStructuredText and is
compiled by Sphinx. The reStructuredText source of the documentation
is located in ``docs/``.

To build the documentation yourself, run:

.. code-block:: bash

     sphinx-build ./docs/ ./build/

You can then open the index.html file that will be created in the build directory.


Contributing Code
=================

The development of ChatterBot happens on GitHub. Code contributions should be
submitted there in the form of pull requests.

Pull requests should meet the following criteria.

1. Fix one issue and fix it well.
2. Do not include extraneous changes that do not relate to the issue being fixed.
3. Include a descriptive title and description for the pull request.
4. Have descriptive commit messages.
