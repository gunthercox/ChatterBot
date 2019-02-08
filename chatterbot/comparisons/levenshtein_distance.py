from .comparator import Comparator
from chatterbot.conversation import Statement

# Use python-Levenshtein if available
try:
    from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher


class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, statement, bot_statement_list):
        """
        Compare the two input statements.

        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """
        # Return 0 if either statement has a falsy text value
        if not statement.text or not bot_statement_list:
            return 0

        # Get the lowercase version of both strings
        statement_text = str(statement.text.lower())
        m_confidence = 0.0
        m_statement = Statement('')
        for other_statement in bot_statement_list:
            other_statement_text = str(other_statement.text.lower())

            similarity = SequenceMatcher(
                None,
                statement_text,
                other_statement_text
            )

            # Calculate a decimal percent of the similarity
            percent = round(similarity.ratio(), 2)
            if percent > m_confidence:
                m_confidence = percent
                m_statement = other_statement

        m_statement.confidence = m_confidence
        return m_statement
