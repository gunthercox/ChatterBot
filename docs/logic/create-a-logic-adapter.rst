============================
Creating a new logic adapter
============================

You can write your own logic adapters by creating a new class that
inherits from :code:`LogicAdapter` and overrides the necessary
methods established in the :code:`LogicAdapter` base class.

Logic adapter methods
=====================

.. autoclass:: chatterbot.logic.LogicAdapter
   :members:

Example logic adapter
=====================

.. code-block:: python

   from chatterbot.logic import LogicAdapter


   class MyLogicAdapter(LogicAdapter):
       def __init__(self, **kwargs):
           super(MyLogicAdapter, self).__init__(**kwargs)

       def can_process(self, statement):
           return True

       def process(self, statement):
           import random

           # Randomly select a confidence between 0 and 1
           confidence = random.uniform(0, 1)

           # For this example, we will just return the input as output
           selected_statement = statement
           selected_statement.confidence = confidence

           return selected_statement

Directory structure
===================

If you create your own logic adapter you will need to have it in a separate file from your chat bot.
Your directory setup should look something like the following:

.. code-block:: text

   project_directory
   ├── cool_chatbot.py
   └── cool_adapter.py

Then assuming that you have a class named :code:`MyLogicAdapter` in your *cool_chatbot.py* file,
you should be able to specify the following when you initialize your chat bot.

.. code-block:: python

   ChatBot(
       # ...
       logic_adapters=[
           {
               'import_path': 'cool_chatbot.MyLogicAdapter'
           }
       ]
   )

Responding to specific input
============================

If you want a particular logic adapter to only respond to a unique type of
input, the best way to do this is by overriding the :code:`can_process`
method on your own logic adapter.

Here is a simple example. Let's say that we only want this logic adapter to
generate a response when the input statement starts with "Hey Mike". This
way, statements such as "Hey Mike, what time is it?" will be processed,
but statements such as "Do you know what time it is?" will not be processed.

.. code-block:: python

   def can_process(self, statement):
       if statement.text.startswith('Hey Mike')
           return True
       else:
           return False

Interacting with services
=========================

In some cases, it is useful to have a logic adapter that can interact with an external service or
api in order to complete it's task. Here is an example that demonstrates how this could be done.
For this example we will use a fictitious API endpoint that returns the current temperature.

.. code-block:: python

   def can_process(self, statement):
       """
       Return true if the input statement contains
       'what' and 'is' and 'temperature'.
       """
       words = ['what', 'is', 'temperature']
       if all(x in statement.text.split() for x in words)
           return True
       else:
           return False

   def process(self, statement):
       from chatterbot.conversation import Statement
       import requests

       # Make a request to the temperature API
       response = requests.get('https://api.temperature.com/current?units=celsius')
       data = response.json()

       # Let's base the confidence value on if the request was successful
       if response.status_code == 200:
           confidence = 1
       else:
           confidence = 0

       temperature = data.get('temperature', 'unavailable')

       response_statement = Statement('The current temperature is {}'.format(temperature))

       return confidence, response_statement

Providing extra arguments
=========================

All key word arguments that have been set in your ChatBot class's constructor
will also be passed to the :code:`__init__` method of each logic adapter.
This allows you to access these variables if you need to use them in your logic adapter.
(An API key might be an example of a parameter you would want to access here.)

You can override the :code:`__init__` method on your logic adapter to store additional
information passed to it by the ChatBot class.


.. code-block:: python

   class MyLogicAdapter(LogicAdapter):
       def __init__(self, **kwargs):
           super(MyLogicAdapter, self).__init__(**kwargs)

           self.api_key = kwargs.get('secret_key')

The :code:`secret_key` variable would then be passed to the ChatBot class as shown bellow.

.. code-block:: python

   chatbot = ChatBot(
       # ...
       secret_key='************************'
    )
