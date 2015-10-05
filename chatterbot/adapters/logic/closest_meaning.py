from .logic import LogicAdapter

from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk import word_tokenize


class ClosestMeaningAdapter(LogicAdapter):

    def __init__(self):
        super(ClosestMeaningAdapter, self).__init__()
        from nltk.data import find
        from nltk import download

        # Download data if needed

        try:
            find('wordnet.zip')
        except LookupError:
            download('wordnet')

        try:
            find('stopwords.zip')
        except LookupError:
            download('stopwords')

        try:
            find('punkt.zip')
        except LookupError:
            download('punkt')

    def get_tokens(self, text, exclude_stop_words=True):
        """
        Takes a string and converts it to a tuple
        of each word. Skips common stop words such
        as ("is, the, a, ...") is 'exclude_stop_words'
        is True.
        """
        lower = text.lower()
        tokens = word_tokenize(lower)

        # Remove any stop words from the string
        if exclude_stop_words:
            excluded_words = stopwords.words("english")

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

            synset1 = wordnet.synsets(combination[0])
            synset2 = wordnet.synsets(combination[1])

            if synset1 and synset2:

                # Compare the first synset in each list of synsets
                similarity = synset1[0].path_similarity(synset2[0])

                if similarity:  
                    total_similarity = total_similarity + similarity

        return total_similarity

    def get(self, text, list_of_statements, current_conversation=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # Check if there is no options
        if not list_of_statements:
            return text

        # Check if an exact match exists
        if text in list_of_statements:
            return text

        closest_statement = list_of_statements[0]
        closest_similarity = 0

        # For each option in the list of options
        for statement in list_of_statements:
            similarity = self.get_similarity(text, statement)

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_statement = statement

        return closest_statement

