========
Glossary
========

.. glossary::

   adapters
      A pluggable class that allows a ChatBot instance to execute some kind of functionality.

   logic adapter
      An adapter class that allows a ChatBot instance to select a response to 

   storage adapter
      A class that allows a chat bot to store information somewhere, such as a database.

   input adapter
      An adapter class that gets input from somewhere and provides it to the chat bot.

   output adapter
      An adapter class that returns a chat bot's response.

   corpus
      In linguistics, a corpus (plural corpora) or text corpus is a large
      and structured set of texts. They are used to do statistical analysis
      and hypothesis testing, checking occurrences or validating linguistic
      rules within a specific language territory [1]_.

   preprocessors
      A member of a list of functions that can be used to modify text
      input that the chat bot receives before the text is passed to
      the logic adapter for processing.

   statement
      A single string of text representing something that can be said.

   response
      A single string of text that is uttered as an answer, a reply or
      an acknowledgement to a statement.

   untrained instance
      An untrained instance of the chat bot has an empty database.

.. [1] https://en.wikipedia.org/wiki/Text_corpus