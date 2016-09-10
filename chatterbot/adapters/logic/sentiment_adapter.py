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
        return abs(input_sentiment - response_sentiment)

    def process(self, statement):
        input_blob = TextBlob(statement.text)
        input_sentiment = input_blob.sentiment.polarity

        response_list = self.context.storage.filter(
            in_response_to__contains=statement.text
        )

        if not response_list:
            return 0, self.context.storage.get_random()

        best_response = response_list[0]
        max_closeness = 1

        for response in response_list:
            blob = TextBlob(response.text)
            sentiment = blob.sentiment.polarity

            closeness = self.calculate_closeness(input_sentiment, sentiment)
            if closeness < max_closeness:
                best_response = response
                max_closeness = closeness

        # The confidence is the percentage of closeness
        confidence = 1.0 - max_closeness

        return confidence, best_response
