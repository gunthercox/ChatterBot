from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob import TextBlob


class SentimentAdapter(LogicAdapter):
    """
    This adapter selects a response with the closest
    matching sentiment value to the input statement.
    """

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
        return abs(input_sentiment - response_sentiment)

    def process(self, statement):
        input_blob = TextBlob(statement.text)
        input_sentiment = input_blob.sentiment.polarity

        self.logger.info(
            u'"{}" has a sentiment polarity of {}.'.format(
                statement.text, input_sentiment
            )
        )

        response_list = self.context.storage.filter()

        best_response = response_list[0]
        max_closeness = 0.0

        for response in response_list:
            blob = TextBlob(response.text)
            sentiment = blob.sentiment.polarity

            closeness = self.calculate_closeness(input_sentiment, sentiment)
            if closeness < max_closeness:
                best_response = response
                max_closeness = closeness

        return max_closeness, best_response
