====================================
How logic adapters select a response
====================================

A typical logic adapter designed to return a response to
an input statement will use two main steps to do this.
The first step involves searching the database for a known
statement that matches or closely matches the input statement.
Once a match is selected, the second step involves selecting a
known response to the selected match. Frequently, there will
be a number of existing statements that are responses to the
known match.

To help with the selection of the response, several methods
are built into ChatterBot for selecting a response from the
available options.

.. _response-selection:

Response selection methods
==========================

.. automodule:: chatterbot.response_selection
   :members:

Use your own response selection method
++++++++++++++++++++++++++++++++++++++

You can create your own response selection method and use it as long as the function takes 
two parameters (a statements and a list of statements). The method must return a statement.

.. code-block:: python

   def select_response(statement, statement_list, storage=None):

       # Your selection logic

       return selected_statement

Setting the response selection method
=====================================

To set the response selection method for your chat bot, you
will need to pass the ``response_selection_method`` parameter
to your chat bot when you initialize it. An example of this
is shown below.

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.response_selection import get_most_frequent_response

   chatbot = ChatBot(
       # ...
       response_selection_method=get_most_frequent_response
   )

Getting repeatable answers
==========================

The same input can have several learned responses. Random response selection,
learning during a conversation, and filtering recent repeated responses can
each change the answer. Choosing the first response alone does not freeze
the other two behaviors.

For a ``BestMatch`` bot using a trained SQL database, disable conversational
learning and select the first candidate:

.. code-block:: python

   from chatterbot import ChatBot
   from chatterbot.response_selection import get_first_response

   chatbot = ChatBot(
       "Helpdesk",
       database_uri="sqlite:///helpdesk.sqlite3",
       read_only=True,
       logic_adapters=[{
           "import_path": "chatterbot.logic.BestMatch",
           "response_selection_method": get_first_response,
       }],
   )

Order the SQL candidates by ID and allow the same answer even when it appears
in recent conversation history:

.. code-block:: python

   response = chatbot.get_response(
       "How do I reset my password?",
       conversation="helpdesk-demo",
       additional_response_selection_parameters={
           "order_by": ["id"],
           "exclude_text": [],
       },
   )

With unchanged training data and settings, this makes candidate selection
repeatable. ``read_only`` prevents this bot from learning through
``get_response``; it does not stop explicit training or other processes from
changing the database. Other logic adapters and randomly chosen default
responses can also introduce variation, so review those separately if they
are part of your configuration.


Response selection in logic adapters
====================================

When a logic adapter is initialized, the response selection method
parameter that was passed to it can be called using ``self.select_response``
as shown below.

.. code-block:: python

   response = self.select_response(
       input_statement,
       list_of_response_options,
       self.chatbot.storage
   )


Selecting a response from multiple logic adapters
=================================================

The ``generate_response`` method is used to select a single response from the responses
returned by all of the logic adapters that the chat bot has been configured to use.
Each response returned by the logic adapters includes a confidence score that indicates
the likeliness that the returned statement is a valid response to the input.

Response selection
++++++++++++++++++

The ``generate_response`` will return the response statement that has the greatest
confidence score. The only exception to this is a case where multiple logic adapters
return the same statement and therefore *agree* on that response.

For this example, consider a scenario where multiple logic adapters are being used.
Assume the following results were returned by a chat bot's logic adapters.

+------------+--------------+
| Confidence | Statement    |
+============+==============+
| 0.2        | Good morning |
+------------+--------------+
| 0.5        | Good morning |
+------------+--------------+
| 0.7        | Good night   |
+------------+--------------+

In this case, two of the logic adapters have generated the same result.
When multiple logic adapters come to the same conclusion, that statement
is given priority over another response with a possibly higher confidence score.
The fact that the multiple adapters agreed on a response is a significant
indicator that a particular statement has a greater probability of being
a more accurate response to the input.

When multiple adapters agree on a response, the greatest confidence score that
was generated for that response will be returned with it.
