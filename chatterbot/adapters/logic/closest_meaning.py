from .base_match import BaseMatchAdapter


class ClosestMeaningAdapter(BaseMatchAdapter):
    """
    This adapter selects a response by comparing the tokenized form of the
    input statement's text, with the tokenized form of possible matching
    statements. For each possible match, the sum of the Cartesian product of
    the path similarity of each statement is compared. This process simulates
    an evaluation of the closeness of synonyms. The known statement with the
    greatest path similarity is then returned.
    """

    def __init__(self, **kwargs):
        super(ClosestMeaningAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import synset_distance

        self.statement_comparison_function = kwargs.get(
            'statement_comparison_function',
            synset_distance
        )

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                self.logger.info(
                    u'No statements have known responses. ' +
                    u'Choosing a random response to return.'
                )
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        closest_similarity = -1
        total_similarity = 0

        # For each option in the list of options
        for statement in statement_list:
            similarity = self.statement_comparison_function(
                input_statement,
                statement
            )

            total_similarity += similarity

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_match = statement

        try:
            confidence = closest_similarity / total_similarity
        except:
            confidence = 0

        return confidence, closest_match
