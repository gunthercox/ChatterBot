from .base_match import BaseMatchAdapter

from chatterbot.utils.pos_tagger import POSTagger
from chatterbot.utils.stop_words import StopWordsManager
from chatterbot.utils.word_net import Wordnet


class ClosestMeaningAdapter(BaseMatchAdapter):
    """
    This adapter selects a response by comparing the tokenized form of the
    input statement's text, with the tokenized form of possible matching
    statements. For each possible match, the sum of the Cartesian product of
    the path similarity of each statement is compared. This process simulates
    an evaluation of the closeness of synonyms. The known statement with the
    greatest path similarity is then returned.
    """

    def __init__(self, **kwargs):
        super(ClosestMeaningAdapter, self).__init__(**kwargs)

        self.wordnet = Wordnet()
        self.tagger = POSTagger()
        self.stopwords = StopWordsManager()

    def get_tokens(self, text, exclude_stop_words=True):
        """
        Takes a string and converts it to a tuple
        of each word. Skips common stop words such
        as ("is, the, a, ...") is 'exclude_stop_words'
        is True.
        """
        lower = text.lower()
        tokens = self.tagger.tokenize(lower)

        # Remove any stop words from the string
        if exclude_stop_words:
            excluded_words = self.stopwords.words("english")

            tokens = set(tokens) - set(excluded_words)

        return tokens

    def get_similarity(self, string1, string2):
        """
        Calculate the similarity of two statements.
        This is based on the total similarity between
        each word in each sentence.
        """
        import itertools

        tokens1 = self.get_tokens(string1)
        tokens2 = self.get_tokens(string2)

        total_similarity = 0

        # Get the highest matching value for each possible combination of words
        for combination in itertools.product(*[tokens1, tokens2]):

            synset1 = self.wordnet.synsets(combination[0])
            synset2 = self.wordnet.synsets(combination[1])

            if synset1 and synset2:

                max_similarity = 0

                # Get the highest similarity for each combination of synsets
                for synset in itertools.product(*[synset1, synset2]):
                    similarity = synset[0].path_similarity(synset[1])

                    if similarity and (similarity > max_similarity):
                        max_similarity = similarity

                # Add the most similar path value to the total
                total_similarity += max_similarity

        return total_similarity

    def get(self, input_statement, statement_list=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.get_available_statements(statement_list)

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        # Get the text of each statement
        text_of_all_statements = []
        for statement in statement_list:
            text_of_all_statements.append(statement.text)

        # Check if an exact match exists
        if input_statement.text in text_of_all_statements:
            return 1, input_statement

        closest_statement = None
        closest_similarity = -1
        total_similarity = 0

        # For each option in the list of options
        for statement in text_of_all_statements:
            similarity = self.get_similarity(input_statement.text, statement)

            total_similarity += similarity

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_statement = statement

        try:
            confidence = closest_similarity / total_similarity
        except:
            confidence = 0

        return confidence, next(
            (s for s in statement_list if s.text == closest_statement), None
        )
