Responding using rule-based matching with spaCy
===============================================

.. note::
    This tutorial requires ChatterBot 1.2.3 or newer.

ChatterBot includes logic adapters that support `spaCy's rule-based matching`_ as a method for selecting responses to input statements. This functionality can be useful for cases where you need a chat bot to respond or carry out actions for specific inputs.

Matching phrase patterns
------------------------

To get started we'll need to set up a chat bot using the :ref:`Specific Response Adapter` (``SpecificResponseAdapter``) class.

.. code-block:: python
    :caption: tutorial.py

    from chatterbot import ChatBot
    from chatterbot.logic import SpecificResponseAdapter

    chatbot = ChatBot(
        'Example Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'What is your name?',
                'output_text': 'My name is ChatterBot.'
            },
            {
            'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, please try asking a different question.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )

    response = chatbot.get_response('What is your name?')
    print(response)

    response = chatbot.get_response('What is your purpose?')
    print(response)

By default, the ``SpecificResponseAdapter`` uses a case-sensitive exact match to determine if the input statement matches its defined ``input_text`` value. Only when an exact match is found, will the response will be returned with a confidence of 1. Otherwise, the response will be returned with a confidence of 0, and the next logic adapter in the list will be used to select a response. In this case, the ``BestMatch`` logic adapter is used as a fallback, configured with a predefined ``default_response``.

Matching an exact string is not always practical, in some cases for example it may be necessary to match a part or phrase pattern contained within a string of text. To achieve this, we can use spaCy's rule-based matching to define a pattern that the input statement must match.

.. code-block:: python
    :caption: tutorial.py

    from chatterbot import ChatBot
    from chatterbot.logic import SpecificResponseAdapter
    from spacy.matcher import Matcher

    # Pattern to match phrases close to "check if the website is up"
    # and "check is the website is down"
    pattern = [
        {'LOWER': 'check'}, {}, {}, {'LOWER': 'website'}, {},
        {'LEMMA': {'IN': ['up', 'down']}}
    ]

    chatbot = ChatBot(
        'Example Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'matcher': Matcher,
                'input_text': pattern,
                'output_text': 'I will check the website status.'
            },
            {
            'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, please try asking a different question.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )

    response = chatbot.get_response('Check if the website is up')
    print(response)

    response = chatbot.get_response('Check if the website is down')
    print(response)

.. note::
    An alternative to the ``Matcher`` class is the `PhraseMatcher`_ class, which can be used to match against a list of phrases (strings).

Calling a function in response to a match
-----------------------------------------

In some cases, it may be necessary to call a function in response to a match. This can be achieved by defining a function that takes the input statement as an argument, and then passing that function to the ``output_text`` parameter.

.. code-block:: python
    :caption: tutorial.py

    from chatterbot import ChatBot
    from chatterbot.logic import SpecificResponseAdapter
    from spacy.matcher import Matcher

    def check_website_status():
        from urllib.request import urlopen

        HOSTNAME = 'https://docs.chatterbot.us/'

        try:
            urlopen(HOSTNAME)
            return 'The website is up.'
        except Exception:
            return 'The website is down.'

    pattern = [
        {'LOWER': 'check'}, {}, {}, {'LOWER': 'website'}, {},
        {'LEMMA': {'IN': ['up', 'down']}}
    ]

    chatbot = ChatBot(
        'Example Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'matcher': Matcher,
                'input_text': pattern,
                'output_text': check_website_status
            },
            {
            'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, please try asking a different question.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )

    response = chatbot.get_response('Check if the website is up')
    print(response)

    response = chatbot.get_response('Check if the website is down')
    print(response)

.. _`spaCy's rule-based matching`: https://spacy.io/usage/rule-based-matching
.. _`PhraseMatcher`: https://spacy.io/usage/rule-based-matching#phrasematcher
