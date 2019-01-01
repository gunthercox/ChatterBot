from chatterbot.conversation import Statement


class Search:
    """
    :param statement_comparison_function: The dot-notated import path
        to a statement comparison function.
        Defaults to ``levenshtein_distance``.

    :param search_page_size:
        The maximum number of records to load into memory at a time when searching.
        Defaults to 1000
    """

    name = 'search'

    def __init__(self, chatbot, **kwargs):
        from chatterbot.comparisons import levenshtein_distance

        self.chatbot = chatbot

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

    def search(self, input_statement):
        """
        Search for close matches to the input. Confidence scores for
        subsequent results will order of increasing value.

        :param input_statement: A statement.
        :type input_statement: chatterbot.conversation.Statement
        :rtype: Generator yielding one closest matching statement at a time.
        """
        self.chatbot.logger.info('Beginning search for close text match')

        input_search_text = input_statement.search_text

        if not input_statement.search_text:
            self.chatbot.logger.warn(
                'No value for search_text was available on the provided input'
            )

            input_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(
                input_statement.text
            )

        statement_list = self.chatbot.storage.filter(
            search_text_contains=input_search_text,
            persona_not_startswith='bot:',
            page_size=self.search_page_size
        )

        closest_match = Statement(text='')
        closest_match.confidence = 0

        self.chatbot.logger.info('Processing search results')

        # Find the closest matching known statement
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement)

            if confidence > closest_match.confidence:
                statement.confidence = confidence
                closest_match = statement

                self.chatbot.logger.info('Similar text found: {} {}'.format(
                    closest_match.text, confidence
                ))

                yield closest_match
