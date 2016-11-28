====================
How ChatterBot Works
====================

ChatterBot is a Python library designed to make it easy to create software that can engage in conversation.

An :term:`untrained instance` of ChatterBot starts off with no knowledge of how to communicate.
Each time a user enters a statement, the library saves the text that they entered and the text
that the statement was in response to. As ChatterBot receives more input the number of responses
that it can reply and the accuracy of each response in relation to the input statement increase.

The program selects the closest matching response by searching for the closest matching known
statement that matches the input, it then returns the most likely response to that statement
based on how frequently each response is issued by the people the bot communicates with.

..  _process_flow_diagram:

Process flow diagram
====================

.. image:: _static/chatterbot-process-flow.svg

Definitions
===========

.. glossary::

   untrained instance
      An untrained instance of the chat bot has an empty database.
