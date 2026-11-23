=======
Filters
=======

Filters are an efficient way to create queries that can be passed to ChatterBot's storage adapters.
Filters will reduce the number of statements that a chat bot has to process when it is selecting a response.

Recent responses in BestMatch
=============================

On its text-search path, ``BestMatch`` calls
``get_recent_repeated_responses`` directly. Removing it from a ``filters``
configuration list does not disable that call. This behavior reduces loops
where the bot keeps giving the same reply.

By default, the helper examines the last 10 stored statements in the current
conversation. Among the three most common texts, any occurring at least
three times is excluded from response candidates. The history includes both
user inputs and bot replies. This can be undesirable for an FAQ where several
questions intentionally share the same answer: that answer can be filtered
out even when the input has an exact training match, causing a fallback reply.

To allow repeated answers for a particular call, override ``exclude_text``
with an empty list:

.. code-block:: python

   response = chatbot.get_response(
       "Who are you?",
       conversation="faq-session",
       additional_response_selection_parameters={"exclude_text": []},
   )

For the SQL ``BestMatch`` path, the additional parameters apply to both the
primary and fallback candidate queries. This override only disables the
recent-text exclusion for that call. It does not disable learning, choose a
deterministic response selector, or remove the separate excluded-word filter.
See :ref:`response-selection` for response selection methods.

.. automodule:: chatterbot.filters
   :members:
