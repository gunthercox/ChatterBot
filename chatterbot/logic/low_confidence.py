from __future__ import unicode_literals
from chatterbot.conversation import Statement
from .best_match import BestMatch


class LowConfidenceAdapter(BestMatch):
    """
    Returns a default response with a high confidence
    when a high confidence response is not known.
    """

    def __init__(self, **kwargs):
        super(LowConfidenceAdapter, self).__init__(**kwargs)

        self.confidence_threshold = kwargs.get('threshold', 0.65)

        default_response = kwargs.get(
            'default_response', "I'm sorry, I do not understand."
        )

        self.default_response = Statement(text=default_response)

    def process(self, input_statement):
        """
        Return a default response with a high confidence if
        a high confidence response is not known.
        """
        # Select the closest match to the input statement
        closest_match = self.get(input_statement)

        # Confidence should be high only if it is less than the threshold
        if closest_match.confidence < self.confidence_threshold:
            self.default_response.confidence = 1
        else:
            self.default_response.confidence = 0

        return self.default_response
