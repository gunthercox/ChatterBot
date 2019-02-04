from .comparator import Comparator
from chatterbot import utils
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentComparison(Comparator):
    """
    Calculate the similarity of two statements based on the closeness of
    the sentiment value calculated for each statement.
    """

    def __init__(self):
        super().__init__()

        self.sentiment_analyzer = None

    def initialize_nltk_vader_lexicon(self):
        """
        Download the NLTK vader lexicon for sentiment analysis
        that is required for this algorithm to run.
        """
        utils.nltk_download_corpus('vader_lexicon')

    def get_sentiment_analyzer(self):
        """
        Get the initialized sentiment analyzer.
        """
        if self.sentiment_analyzer is None:

            self.sentiment_analyzer = SentimentIntensityAnalyzer()

        return self.sentiment_analyzer

    def compare(self, statement, other_statement):
        """
        Return the similarity of two statements based on
        their calculated sentiment values.

        :return: The percent of similarity between the sentiment value.
        :rtype: float
        """
        sentiment_analyzer = self.get_sentiment_analyzer()
        statement_polarity = sentiment_analyzer.polarity_scores(statement.text.lower())
        statement2_polarity = sentiment_analyzer.polarity_scores(other_statement.text.lower())

        statement_greatest_polarity = 'neu'
        statement_greatest_score = -1
        for polarity in sorted(statement_polarity):
            if statement_polarity[polarity] > statement_greatest_score:
                statement_greatest_polarity = polarity
                statement_greatest_score = statement_polarity[polarity]

        statement2_greatest_polarity = 'neu'
        statement2_greatest_score = -1
        for polarity in sorted(statement2_polarity):
            if statement2_polarity[polarity] > statement2_greatest_score:
                statement2_greatest_polarity = polarity
                statement2_greatest_score = statement2_polarity[polarity]

        # Check if the polarity if of a different type
        if statement_greatest_polarity != statement2_greatest_polarity:
            return 0

        values = [statement_greatest_score, statement2_greatest_score]
        difference = max(values) - min(values)

        return 1.0 - difference
