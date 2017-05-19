from __future__ import unicode_literals
from .best_match import BestMatch


class BestMatchLang(BestMatch):
    """
    A logic adater that returns a response based on known responses to
    the closest matches to the input statement.  Comparision methods need two
    parameters, lang and language.

    """

    def __init__(self, **kwargs):
        super(BestMatchLang, self).__init__(**kwargs)
        self.language = kwargs.get('language', 'english')
        self.lang = kwargs.get('lang', 'eng')

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.chatbot.storage.get_response_statements()

        if not statement_list:
            if self.chatbot.storage.count():
                # Use a randomly picked statement
                self.logger.info(
                    'No statements have known responses. ' +
                    'Choosing a random response to return.'
                )
                random_response = self.chatbot.storage.get_random()
                random_response.confidence = 0
                return random_response
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        closest_match.confidence = 0

        # Find the closest matching known statement
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement, lang=self.lang, language=self.language)

            if confidence > closest_match.confidence:
                statement.confidence = confidence
                closest_match = statement

        return closest_match
