from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter


class LowConfidenceAdapter(LogicAdapter):
    """
    Returns a default response with a high confidence
    when a high confidence response is not known.

    :param threshold:
          The low confidence value that triggers this adapter.
          Defaults to 0.65.
    :type threshold: float

    :param default_response:
          The response returned by this logic adaper.
    :type default_response: str or list or tuple

    :param response_selection_method:
          The a response selection method.
          Defaults to ``get_first_response``
    :type response_selection_method: collections.abc.Callable
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.confidence_threshold = kwargs.get('threshold', 0.65)

        default_responses = kwargs.get(
            'default_response', "I'm sorry, I do not understand."
        )

        # Convert a single string into a list
        if isinstance(default_responses, str):
            default_responses = [
                default_responses
            ]

        self.default_responses = [
            Statement(text=default) for default in default_responses
        ]

    def process(self, input_statement):
        """
        Return a default response with a high confidence if
        a high confidence response is not known.
        """
        search_results = self.search_algorithm.search(input_statement)

        # Use the input statement as the closest match if no other results are found
        closest_match = next(search_results, input_statement)

        # Search for the closest match to the input statement
        for result in search_results:

            # Stop searching if a match that is close enough is found
            if result.confidence >= self.maximum_similarity_threshold:
                closest_match = result
                break

        # Choose a response from the list of options
        response = self.select_response(
            input_statement,
            self.default_responses,
            self.chatbot.storage
        )

        # Confidence should be high only if it is less than the threshold
        if closest_match.confidence < self.confidence_threshold:
            response.confidence = 1
        else:
            response.confidence = 0

        return response
