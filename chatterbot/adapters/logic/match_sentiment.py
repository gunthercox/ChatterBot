from .logic import LogicAdapter


class MatchSentimentAdapter(LogicAdapter):

    def get(self, text, list_of_statements):
        """
        Evaluates the sentiment values for the text provided
        and for each statement in the list of statements.
        The statement from the list that most closely matches
        the sentiment values of the input text will be
        returned.
        """
