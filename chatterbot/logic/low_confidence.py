from chatterbot.conversation import Statement
from .best_match import BestMatch


class LowConfidenceAdapter(BestMatch):
    """
    Returns a default response with a high confidence
    when a high confidence response is not known.

    :kwargs:
        * *threshold* (``float``) --
          The low confidence value that triggers this adapter.
          Defaults to 0.65.
        * *default_response* (``str``) or (``iterable``)--
          The response returned by this logic adaper.
        * *response_selection_method* (``str``) or (``callable``)
          The a response selection method.
          Defaults to ``get_first_response``.
    """

    def __init__(self, **kwargs):
        super(LowConfidenceAdapter, self).__init__(**kwargs)

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
        # Select the closest match to the input statement
        closest_match = self.get(input_statement)

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
