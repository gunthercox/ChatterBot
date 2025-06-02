from chatterbot.comparisons import LevenshteinDistance, SpacySimilarity


class BaseTextSearch:
    """
    Base class for performing text search using ChatterBot comparison functions.
    """

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

        # Use a better semantic comparator if available (SpacySimilarity is more contextual)
        comparison_class = kwargs.get('statement_comparison_function', SpacySimilarity)

        self.compare_statements = comparison_class(language=self.chatbot.tagger.language)

        # Max results returned and how many records to load from storage at once
        self.search_page_size = kwargs.get('search_page_size', 1000)
        self.max_results = kwargs.get('max_results', 5)

    def _search_statements(self, input_statement, filter_parameters):
        """
        Shared internal method to search for similar statements.
        :param input_statement: The input statement to compare against known responses.
        :param filter_parameters: Filter arguments for querying the storage.
        :return: List of top-N similar statements with confidence scores.
        """
        self.chatbot.logger.info('Fetching candidate statements from storage...')
        candidates = self.chatbot.storage.filter(**filter_parameters)

        results = []

        for candidate in candidates:
            # Compare input statement to the 'in_response_to' field
            comparison_text = candidate.in_response_to or candidate.text

            confidence = self.compare_statements.compare_text(
                input_statement.text,
                comparison_text
            )

            # Store the confidence in the statement object
            candidate.confidence = confidence
            results.append(candidate)

        # Sort results by descending confidence
        results.sort(key=lambda stmt: stmt.confidence, reverse=True)

        # Limit to top-N best results
        return results[:self.max_results]


class IndexedTextSearch(BaseTextSearch):
    """
    Indexed search that restricts candidates to those where input matches part of 'in_response_to'.
    """

    name = 'indexed_text_search'

    def search(self, input_statement, **additional_parameters):
        self.chatbot.logger.info('Performing indexed text search...')

        search_parameters = {
            'search_in_response_to_contains': input_statement.search_text,
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        return self._search_statements(input_statement, search_parameters)


class TextSearch(BaseTextSearch):
    """
    General search that compares input with all known responses.
    """

    name = 'text_search'

    def search(self, input_statement, **additional_parameters):
        self.chatbot.logger.info('Performing general text search...')

        search_parameters = {
            'persona_not_startswith': 'bot:',
            'page_size': self.search_page_size
        }

        if additional_parameters:
            search_parameters.update(additional_parameters)

        return self._search_statements(input_statement, search_parameters)
