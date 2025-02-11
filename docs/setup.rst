============
Installation
============

The recommended method for installing ChatterBot is by using `pip`_.

Installing from PyPi
--------------------

If you are just getting started with ChatterBot, it is recommended that you
start by installing the latest version from the Python Package Index (`PyPi`_).
To install ChatterBot from PyPi using pip run the following command in your terminal.

.. code-block:: bash

   pip install chatterbot


Optional dependencies
---------------------

ChatterBot offers two collections of optional dependencies: ``dev`` and ``test``. Neither of these are required for all ChatterBot use cases, but both provide full support for additional features. The ``dev`` collection includes dependencies such as ``nltk``, and ``spacy``. Separately the ``test`` collection includes dependencies such as ``flake8``, and ``coverage``. The specifics of each collection of optional dependencies can be reviewed via the project's ``pyproject.yml`` file. To install these optional dependencies, you can use the following commands.

.. code-block:: bash

   pip install chatterbot[dev]


.. code-block:: bash

   pip install chatterbot[test]


.. code-block:: bash

   pip install chatterbot[dev,test]


Similarly, if you have `cloned the repository <#installing-from-source>`_ and want to install the optional dependencies, you can run commands in the following format:

.. code-block:: bash

   pip install .[dev,test]


Installing from GitHub
----------------------

You can install the latest **development** version of ChatterBot directly from GitHub using ``pip``.

.. code-block:: bash

   pip install git+git://github.com/gunthercox/ChatterBot.git@master


Installing from source
----------------------

1. Download a copy of the code from GitHub. You may need to install `git`_.

.. code-block:: bash

   git clone https://github.com/gunthercox/ChatterBot.git

2. Install the code you have just downloaded using pip

.. code-block:: bash

   pip install ./ChatterBot


Checking the version of ChatterBot that you have installed
==========================================================

If you already have ChatterBot installed and you want to check what version you
have installed you can run the following command.

.. code-block:: bash

    python -m chatterbot --version

Upgrading ChatterBot to the latest version
==========================================

.. toctree::
   :maxdepth: 4

   upgrading

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _pip: https://pip.pypa.io/en/stable/installing/
.. _PyPi: https://pypi.python.org/pypi
