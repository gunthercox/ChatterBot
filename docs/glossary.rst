========
Glossary
========

.. glossary::

   adapters
      A base class that allows a ChatBot instance to execute some kind of functionality.

   chat bot
      Computer software that can converse conversation with human users or other chat bots [1]_.

   logic adapter
      An adapter class that allows a ChatBot instance to select a response to 

   RAG
      Retrieval-Augmented Generation. A method of by which a large language model
      can retrieve information from a database or other source of information.

   storage adapter
      A class that allows a chat bot to store information somewhere, such as a database.

   corpus
      In linguistics, a corpus (plural corpora) or text corpus is a large
      and structured set of texts. They are used to do statistical analysis
      and hypothesis testing, checking occurrences or validating linguistic
      rules within a specific language territory [2]_.

   large language models
      A type of artificial intelligence model that can generate generate
      human-like text, often trained on a significantly large corpus of
      text data.

   MCP
      Model Context Protocol. A protocol for providing context data to a large
      language model to enable or improve its ability to perform various tasks.

   preprocessors
      A member of a list of functions that can be used to modify text
      input that the chat bot receives before the text is passed to
      the logic adapter for processing.

   statement
      A single string of text representing something that can be said.

   search word
      A word that is not a stop word and has been trimmed in some way (
      for example through stemming).

   stemming
      A process through which a word is reduced into a derivative form.

   stop word
      A common word that is often filtered out during the process of
      analyzing text.

   response
      A single string of text that is uttered as an answer, a reply or
      an acknowledgement to a statement.

   untrained instance
      An untrained instance of the chat bot has an empty database.

   vector
      A mathematical representation of text that can be used to calculate
      the similarity between two pieces of text based on the distance
      between their vectors.

   vector database
      Any database capable of storing vectors.

----

.. [1] https://en.wikipedia.org/wiki/Chatbot
.. [2] https://en.wikipedia.org/wiki/Text_corpus
