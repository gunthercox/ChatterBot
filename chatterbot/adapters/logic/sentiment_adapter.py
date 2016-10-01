from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob import TextBlob
from .mixins import TieBreaking


class SentimentAdapter(TieBreaking, LogicAdapter):
    """
    This adapter selects a response with the closest
    matching sentiment value to the input statement.
    """

    def __init__(self, **kwargs):
        super(SentimentAdapter, self).__init__(**kwargs)

        self.tie_breaking_method = kwargs.get(
            'tie_breaking_method',
            'first_response'
        )

    def calculate_closeness(self, input_sentiment, response_sentiment):
        """
        Return the difference between the input and response
        sentiment values.
        """
        self.logger.info(
            u'Comparing input equality of {} to response of {}.'.format(
                input_sentiment, response_sentiment
            )
        )
        values = [input_sentiment, response_sentiment]

        return max(values) - min(values)

    def process(self, input_statement):
        input_blob = TextBlob(input_statement.text)
        input_sentiment = input_blob.sentiment.polarity

        self.logger.info(
            u'"{}" has a sentiment polarity of {}.'.format(
                input_statement.text, input_sentiment
            )
        )

        response_list = self.context.storage.get_response_statements()

        best_match = response_list[0]
        max_closeness = 1

        for response in response_list:
            blob = TextBlob(response.text)
            sentiment = blob.sentiment.polarity

            closeness = self.calculate_closeness(input_sentiment, sentiment)
            if closeness < max_closeness:
                best_match = response
                max_closeness = closeness

        confidence = 1.0 - max_closeness

        # Get all statements that are in response to the closest match
        response_list = self.context.storage.filter(
            in_response_to__contains=best_match.text
        )

        # Choose a response from the selection
        response_statement = self.break_tie(input_statement, response_list, self.tie_breaking_method)

        return confidence, response_statement
