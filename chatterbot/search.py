class IndexedTextSearch:
    """
    :param statement_comparison_function: The dot-notated import path
        to a statement comparison function.
        Defaults to ``levenshtein_distance``.

    :param search_page_size:
        The maximum number of records to load into memory at a time when searching.
        Defaults to 1000
    """

    name = 'indexed_text_search'

    def __init__(self, chatbot, **kwargs):
        from chatterbot.comparisons import embedded_wordvector, levenshtein_distance

        self.chatbot = chatbot

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            embedded_wordvector
        )

        self.search_page_size = kwargs.get(
            'search_page_size', 10000
        )

    def search(self, input_statement, **additional_parameters):
        """
        Search for close matches to the input. Confidence scores for
        subsequent results will order of increasing value.

        :param input_statement: A statement.
        :type input_statement: chatterbot.conversation.Statement

        :param **additional_parameters: Additional parameters to be passed
            to the ``filter`` method of the storage adapter when searching.

        :rtype: Generator yielding one closest matching statement at a time.
        """
        self.chatbot.logger.info('Beginning search for close text match')

        input_search_text = input_statement.search_text

        if not input_search_text:
            self.chatbot.logger.debug(
                'No value for search_text was available on the provided input'
            )

        search_parameters = {
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        statement_list = self.chatbot.storage.filter(**search_parameters)

        self.chatbot.logger.info('Processing search results')
        # Find the closest matching known statement
        statement = self.compare_statements(input_statement, statement_list)
        yield statement
